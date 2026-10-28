import importlib.util
import io
import json
from pathlib import Path
import tarfile
import tempfile
import unittest
from unittest.mock import patch
from types import SimpleNamespace

MODULE = Path(__file__).resolve().parents[1] / "scripts/sync_plugins.py"
spec = importlib.util.spec_from_file_location("sync_plugins", MODULE)
sync = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sync)


class PublicationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "market"
        self.root.mkdir()
        self.package = Path(self.temp.name) / "source"
        self.package.mkdir()
        self.item = {
            "name": "aesy-language", "repository": "Aegyce/agent-aesy", "ref": "main",
            "path": "plugins/language", "destination": "plugins/aesy/language",
            "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
            "category": "Productivity",
        }
        self.config = {"marketplace": {"name": "test-market"}, "plugins": [self.item]}
        sync.write_json(self.root / "sources.json", self.config)
        self.manifest = {
            "$schema": sync.SCHEMA, "name": "aesy-language", "version": "0.1.0",
            "license": "CC-BY-NC-4.0", "description": "Review technical language.",
            "extensions": {"com.openai": {"interface": {
                "displayName": "Aesy:language", "shortDescription": "Review technical language.",
                "longDescription": "Review technical language and preserve facts.",
                "developerName": "Aegyce", "websiteURL": "https://github.com/Aegyce/agent-aesy",
                "logo": "./assets/icon.svg",
            }}},
        }
        sync.write_json(self.package / "plugin.json", self.manifest)
        (self.package / "LICENSE").write_text("Test license fixture")
        (self.package / "COMMERCIAL-LICENSE.md").write_text("Test authorization fixture")
        (self.package / "assets").mkdir()
        (self.package / "assets/icon.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg"/>')
        skill = self.package / "skills/language/SKILL.md"
        skill.parent.mkdir(parents=True)
        skill.write_text("---\nname: language\ndescription: Review technical language.\n---\n\nPreserve facts.\n")
        self.commit = "a" * 40

    def fetch(self, item, temporary, previous=None, repositories=None):
        return self.package, self.commit, "b" * 40

    def publish(self):
        return sync.synchronize(self.root, fetcher=self.fetch)

    def snapshot(self):
        return {p.relative_to(self.root).as_posix(): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}

    def test_same_commit_only_checks_remote_sha(self):
        previous = {"commit": self.commit, "tree": "b" * 40}
        response = SimpleNamespace(stdout=(self.commit + "\trefs/heads/main\n").encode())
        with patch.object(sync.subprocess, "run", return_value=response) as run:
            result = sync.fetch_package(self.item, self.root, previous, {})
        self.assertEqual(result, (None, self.commit, "b" * 40))
        self.assertEqual(run.call_count, 1)
        self.assertEqual(run.call_args.args[0][1], "ls-remote")

    def test_same_tree_does_not_export_package(self):
        previous = {"commit": "d" * 40, "tree": "b" * 40}
        responses = [SimpleNamespace(stdout=(self.commit + "\trefs/heads/main\n").encode()),
                     SimpleNamespace(stdout=b""), SimpleNamespace(stdout=b""),
                     SimpleNamespace(stdout=("b" * 40 + "\n").encode())]
        with patch.object(sync.subprocess, "run", side_effect=responses) as run:
            result = sync.fetch_package(self.item, self.root, previous, {})
        self.assertEqual(result, (None, self.commit, "b" * 40))
        self.assertFalse(any("archive" in call.args[0] for call in run.call_args_list))

    def test_publication_contains_metadata_icons_and_local_source(self):
        self.publish()
        sync.check(self.root)
        entry = sync.read_json(self.root / ".agents/plugins/marketplace.json")["plugins"][0]
        self.assertEqual(entry["source"], {"source": "local", "path": "./plugins/aesy/language"})
        self.assertEqual(entry["interface"]["displayName"], "Aesy:language")
        self.assertTrue((self.root / "plugins/aesy/language/assets/icon.svg").is_file())
        self.assertEqual(entry["description"], self.manifest["description"])

    def test_unrelated_source_commit_does_not_change_publication(self):
        self.publish()
        before = self.snapshot()
        self.commit = "c" * 40
        self.publish()
        self.assertEqual(before, self.snapshot())

    def test_content_change_requires_a_version_bump_without_partial_writes(self):
        self.publish()
        before = self.snapshot()
        (self.package / "assets/icon.svg").write_text("changed icon")
        with self.assertRaisesRegex(ValueError, "higher version"):
            self.publish()
        self.assertEqual(before, self.snapshot())

    def test_higher_version_updates_and_records_exact_commit(self):
        self.publish()
        self.manifest["version"] = "0.1.1"
        sync.write_json(self.package / "plugin.json", self.manifest)
        self.commit = "c" * 40
        records = self.publish()
        self.assertEqual(records[0]["commit"], self.commit)
        self.assertEqual(records[0]["version"], "0.1.1")
        sync.check(self.root)

    def test_downgrade_is_rejected(self):
        self.publish()
        self.manifest["version"] = "0.0.9"
        sync.write_json(self.package / "plugin.json", self.manifest)
        with self.assertRaisesRegex(ValueError, "higher version"):
            self.publish()

    def test_missing_asset_prevents_publication(self):
        (self.package / "assets/icon.svg").unlink()
        with self.assertRaisesRegex(ValueError, "asset"):
            self.publish()
        self.assertFalse((self.root / "sources.lock.json").exists())

    def test_package_symlinks_are_rejected(self):
        (self.package / "linked").symlink_to(self.root / "sources.json")
        with self.assertRaisesRegex(ValueError, "symlinks"):
            self.publish()

    def test_generated_content_tampering_is_detected(self):
        self.publish()
        (self.root / "plugins/aesy/language/LICENSE").write_text("modified")
        with self.assertRaisesRegex(ValueError, "source lock"):
            sync.check(self.root)

    def test_unknown_dispatch_sender_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "not registered"):
            sync.synchronize(self.root, "Unknown/repository", self.fetch)

    def test_unsafe_destination_is_rejected(self):
        self.config["plugins"][0]["destination"] = "../outside"
        sync.write_json(self.root / "sources.json", self.config)
        with self.assertRaisesRegex(ValueError, "Unsafe"):
            self.publish()

    def test_archive_traversal_and_links_are_rejected(self):
        for filename, kind in [("../escape", tarfile.REGTYPE), ("link", tarfile.SYMTYPE)]:
            with self.subTest(filename=filename):
                data = io.BytesIO()
                with tarfile.open(fileobj=data, mode="w") as archive:
                    item = tarfile.TarInfo(filename)
                    item.type = kind
                    item.linkname = "../outside" if kind == tarfile.SYMTYPE else ""
                    archive.addfile(item, io.BytesIO())
                with self.assertRaises(ValueError):
                    sync.extract_archive(data.getvalue(), self.root)


if __name__ == "__main__":
    unittest.main()
