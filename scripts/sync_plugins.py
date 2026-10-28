#!/usr/bin/env python3
"""Publish self-contained Agent plugins from registered public Git repositories."""

import argparse
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import tarfile
import tempfile

SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
NAME = re.compile(r"[a-z0-9]+(?:[.-][a-z0-9]+)*")


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path, value):
    content = json.dumps(value, ensure_ascii=False, indent=2) + "\n"
    if path.exists() and path.read_text(encoding="utf-8") == content:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def relative_path(value):
    path = PurePosixPath(value)
    if not value or path.is_absolute() or ".." in path.parts or "\\" in value or path == PurePosixPath("."):
        raise ValueError(f"Unsafe package path: {value!r}")
    return path


def sources(root):
    config = read_json(root / "sources.json")
    names, destinations = set(), []
    for item in config["plugins"]:
        if not NAME.fullmatch(item["name"]) or item["name"] in names:
            raise ValueError("Plugin names must be unique lowercase identifiers")
        names.add(item["name"])
        if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", item["repository"]):
            raise ValueError("Expected a public GitHub owner/repository")
        if not re.fullmatch(r"[A-Za-z0-9_][A-Za-z0-9_./-]*", item["ref"]):
            raise ValueError("Invalid Git reference")
        relative_path(item["path"])
        dest = relative_path(item["destination"])
        if len(dest.parts) < 2 or dest.parts[0] != "plugins":
            raise ValueError("Publication destinations must be under plugins/")
        if any(dest == other or dest in other.parents or other in dest.parents for other in destinations):
            raise ValueError("Publication destinations must not overlap")
        destinations.append(dest)
    return config


def version(value):
    if not isinstance(value, str) or not re.fullmatch(r"\d+\.\d+\.\d+", value):
        raise ValueError("Published versions must use major.minor.patch")
    return tuple(map(int, value.split(".")))


def digest(folder):
    result = hashlib.sha256()
    for path in sorted(folder.rglob("*")):
        if path.is_symlink():
            raise ValueError(f"Publication must not contain symlinks: {path}")
        if path.is_file():
            mode = b"755" if path.stat().st_mode & 0o111 else b"644"
            result.update(path.relative_to(folder).as_posix().encode() + b"\0" + mode + b"\0")
            result.update(hashlib.sha256(path.read_bytes()).digest())
    return result.hexdigest()


def validate_package(folder, expected_name):
    manifest = read_json(folder / "plugin.json")
    if manifest.get("$schema") != SCHEMA or manifest.get("name") != expected_name:
        raise ValueError(f"Plugin identity mismatch: {expected_name}")
    version(manifest.get("version"))
    if manifest.get("license") != "CC-BY-NC-4.0":
        raise ValueError("Aegyce original packages must declare CC-BY-NC-4.0")
    for filename in ("LICENSE", "COMMERCIAL-LICENSE.md"):
        if not (folder / filename).is_file():
            raise ValueError(f"Missing {filename} in {expected_name}")
    interface = manifest["extensions"]["com.openai"]["interface"]
    for field in ("displayName", "shortDescription", "longDescription", "developerName", "websiteURL"):
        if not isinstance(interface.get(field), str) or not interface[field].strip():
            raise ValueError(f"Missing plugin presentation field: {field}")
    if not manifest.get("description"):
        raise ValueError("Missing plugin description")
    for key in ("composerIcon", "logo", "logoDark"):
        if key in interface:
            value = interface[key]
            if not value.startswith("./") or not (folder / relative_path(value)).is_file():
                raise ValueError(f"Unresolved plugin asset: {key}")
    skill_names = set()
    for skill in sorted((folder / "skills").glob("*/SKILL.md")):
        text = skill.read_text(encoding="utf-8")
        if not text.startswith("---\n") or "\n---" not in text[4:]:
            raise ValueError(f"Missing Skill frontmatter: {skill}")
        header = text.split("---", 2)[1]
        match = re.search(r"(?m)^name:\s*([^\n]+)$", header)
        skill_name = match.group(1).strip().strip("\"'") if match else ""
        if not NAME.fullmatch(skill_name) or skill_name in skill_names or skill_name != skill.parent.name:
            raise ValueError(f"Invalid or duplicate Skill name: {skill}")
        if not re.search(r"(?m)^description:\s*\S", header):
            raise ValueError(f"Missing Skill description: {skill}")
        skill_names.add(skill_name)
    if (folder / "mcp.json").exists():
        if not isinstance(read_json(folder / "mcp.json").get("mcpServers"), dict):
            raise ValueError("Invalid MCP server configuration")
    digest(folder)  # Reject links before copying a package.
    return manifest


def extract_archive(data, destination):
    with tarfile.open(fileobj=io.BytesIO(data)) as archive:
        for member in archive:
            target = destination / relative_path(member.name)
            if member.isdir():
                target.mkdir(parents=True, exist_ok=True)
            elif member.isfile():
                target.parent.mkdir(parents=True, exist_ok=True)
                with archive.extractfile(member) as stream:
                    target.write_bytes(stream.read())
                target.chmod(0o755 if member.mode & 0o111 else 0o644)
            else:
                raise ValueError(f"Unsupported publication file: {member.name}")


def fetch_package(item, temporary, previous=None, repositories=None):
    repositories = {} if repositories is None else repositories
    key = (item["repository"], item["ref"])
    url = f"https://github.com/{item['repository']}.git"
    if key not in repositories:
        ref = item["ref"] if item["ref"].startswith("refs/heads/") else "refs/heads/" + item["ref"]
        response = subprocess.run(["git", "ls-remote", "--exit-code", url, ref],
                                  check=True, capture_output=True, timeout=30)
        commit = response.stdout.decode().split()[0]
        repositories[key] = {"commit": commit, "checkout": None}
    source = repositories[key]
    commit = source["commit"]
    if previous and commit == previous["commit"]:
        return None, commit, previous["tree"]

    def git(*args):
        process = subprocess.run(["git", "-C", str(source["checkout"]), *args], check=True,
                                 capture_output=True, timeout=120)
        return process.stdout

    if source["checkout"] is None:
        source["checkout"] = temporary / "checkout"
        source["checkout"].mkdir()
        git("init", "-q")
        git("fetch", "--quiet", "--depth=1", url, commit)
    tree = git("rev-parse", f"{commit}:{item['path']}").decode().strip()
    if previous and tree == previous["tree"]:
        return None, commit, tree
    package = temporary / "package"
    package.mkdir()
    extract_archive(git("archive", f"{commit}:{item['path']}"), package)
    return package, commit, tree


def catalog_entry(item, manifest):
    return {
        "name": item["name"],
        "source": {"source": "local", "path": "./" + item["destination"]},
        "policy": item["policy"],
        "category": item["category"],
        "description": manifest["description"],
        "interface": manifest["extensions"]["com.openai"]["interface"],
    }


def synchronize(root, repository="", fetcher=fetch_package):
    config = sources(root)
    if repository and repository not in {s["repository"] for s in config["plugins"]}:
        raise ValueError("Dispatch repository is not registered in sources.json")
    lock_path = root / "sources.lock.json"
    previous = {p["name"]: p for p in read_json(lock_path)["plugins"]} if lock_path.exists() else {}
    pending, records, entries = [], [], []
    repositories = {}
    with tempfile.TemporaryDirectory(prefix="aegyce-publish-") as temp:
        for number, item in enumerate(config["plugins"]):
            staging = Path(temp) / str(number)
            staging.mkdir()
            old = previous.get(item["name"])
            destination = root / item["destination"]
            reusable = old if old and destination.is_dir() and digest(destination) == old["sha256"] else None
            if reusable and any(old.get(key) != item[key] for key in ("repository", "ref", "path", "destination")):
                reusable = None
            if repository and item["repository"] != repository and reusable:
                package, commit, tree = None, old["commit"], old["tree"]
            else:
                package, commit, tree = fetcher(item, staging, reusable, repositories)
            unchanged = package is None
            package = destination if unchanged else package
            manifest = validate_package(package, item["name"])
            content_hash = digest(package)
            if old and old["sha256"] != content_hash and version(manifest["version"]) <= version(old["version"]):
                raise ValueError(f"{item['name']}: changed package content requires a higher version")
            record = {key: item[key] for key in ("name", "repository", "ref", "path", "destination")}
            record.update(commit=commit, tree=tree, version=manifest["version"], sha256=content_hash)
            if old and all(old.get(key) == record[key] for key in ("repository", "ref", "path", "destination", "sha256")):
                record = old  # Unrelated Agent commits do not create catalog updates.
            records.append(record)
            entries.append(catalog_entry(item, manifest))
            if not unchanged:
                pending.append((package, destination))
        # Only materialize after every source has passed validation.
        destinations = {item["destination"] for item in config["plugins"]}
        for old in previous.values():
            if old["destination"] not in destinations:
                stale = relative_path(old["destination"])
                if len(stale.parts) < 2 or stale.parts[0] != "plugins":
                    raise ValueError("Invalid old publication destination")
                shutil.rmtree(root / stale, ignore_errors=True)
        for package, destination in pending:
            if destination.exists():
                shutil.rmtree(destination)
            shutil.copytree(package, destination)
        catalog = dict(config["marketplace"], plugins=entries)
        write_json(root / ".agents/plugins/marketplace.json", catalog)
        write_json(lock_path, {"plugins": records})
    return records


def check(root):
    config = sources(root)
    records = {p["name"]: p for p in read_json(root / "sources.lock.json")["plugins"]}
    entries = []
    if set(records) != {p["name"] for p in config["plugins"]}:
        raise ValueError("Source lock and registered plugins differ")
    for item in config["plugins"]:
        folder = root / item["destination"]
        manifest = validate_package(folder, item["name"])
        record = records[item["name"]]
        for field in ("repository", "ref", "path", "destination"):
            if record[field] != item[field]:
                raise ValueError("Source lock does not match source configuration")
        if digest(folder) != record["sha256"] or manifest["version"] != record["version"]:
            raise ValueError("Publication content does not match its source lock")
        entries.append(catalog_entry(item, manifest))
    if read_json(root / ".agents/plugins/marketplace.json") != dict(config["marketplace"], plugins=entries):
        raise ValueError("Catalog does not match published package metadata")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", default="", help="Validate the dispatch sender against registered sources")
    parser.add_argument("--check", action="store_true", help="Validate published files without network access")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    if args.check:
        check(root)
        print("Published catalog, metadata, resources and source lock are consistent.")
    else:
        records = synchronize(root, args.repository)
        for item in records:
            print(f"{item['name']} {item['version']} <- {item['repository']}@{item['commit']}")


if __name__ == "__main__":
    main()
