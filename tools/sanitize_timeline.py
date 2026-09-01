#!/usr/bin/env python3
"""Create public, relinkable timeline and audit files without workstation paths."""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path
from urllib.parse import quote


def arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fcpxml", type=Path, required=True)
    parser.add_argument("--fcpxml-output", type=Path, required=True)
    parser.add_argument("--audit-dir", type=Path, required=True)
    return parser.parse_args()


def sanitize_fcpxml(source: Path, destination: Path) -> int:
    text = source.read_text(encoding="utf-8")
    pattern = re.compile(r'<media-rep src="[^"]+" kind="original-media"/>')

    def replacement(match: re.Match[str]) -> str:
        src = re.search(r'src="([^"]+)"', match.group(0)).group(1)
        name = Path(src.replace("file://", "").replace("%20", " ")).name
        return (
            '<media-rep src="file:///RELINK/media/final-sources/'
            + quote(name)
            + '" kind="original-media"/>'
        )

    updated, count = pattern.subn(replacement, text)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(updated, encoding="utf-8")
    return count


def sanitize_csv(path: Path) -> int:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        return 0
    fieldnames = list(rows[0])
    changed = 0
    for row in rows:
        if "media_path" in row and row["media_path"]:
            row["media_path"] = "media/final-sources/" + Path(row["media_path"]).name
            changed += 1
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return changed


def main() -> int:
    args = arguments()
    xml_count = sanitize_fcpxml(args.fcpxml, args.fcpxml_output)
    csv_count = sum(sanitize_csv(path) for path in args.audit_dir.glob("*.csv"))
    print(f"sanitized {xml_count} timeline references and {csv_count} audit rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
