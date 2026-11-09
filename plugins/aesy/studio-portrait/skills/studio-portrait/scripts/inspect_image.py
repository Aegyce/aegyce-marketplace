#!/usr/bin/env python3
"""Read image dimensions and report aspect-ratio facts without editing pixels."""

import argparse
import json
from fractions import Fraction
from pathlib import Path

from PIL import Image


def parse_ratio(value):
    try:
        width, height = (int(part) for part in value.split(":"))
        if width <= 0 or height <= 0:
            raise ValueError
        return Fraction(width, height)
    except (ValueError, ZeroDivisionError):
        raise argparse.ArgumentTypeError("Use a positive width:height ratio, e.g. 20:23")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("images", nargs="+", type=Path)
    parser.add_argument("--target-ratio", type=parse_ratio)
    args = parser.parse_args()
    reports = []
    for path in args.images:
        with Image.open(path) as picture:
            raw_width, raw_height = picture.size
            orientation = int(picture.getexif().get(274, 1))
            width, height = (raw_height, raw_width) if orientation in (5, 6, 7, 8) else (raw_width, raw_height)
            ratio = Fraction(width, height)
            report = {
                "filename": path.name,
                "format": picture.format,
                "stored_width": raw_width,
                "stored_height": raw_height,
                "exif_orientation": orientation,
                "display_width": width,
                "display_height": height,
                "display_ratio": f"{ratio.numerator}:{ratio.denominator}",
                "file_size_bytes": path.stat().st_size,
            }
            if args.target_ratio is not None:
                target = args.target_ratio
                report.update({
                    "target_ratio": f"{target.numerator}:{target.denominator}",
                    "exact_ratio_match": ratio == target,
                    "relative_ratio_error_percent": float(abs(ratio / target - 1) * 100),
                })
            reports.append(report)
    print(json.dumps(reports, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
