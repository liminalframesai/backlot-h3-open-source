#!/usr/bin/env python3
"""Validate the public Backlot closure before a GitHub commit/push."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote


REPO = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {".cff", ".csv", ".json", ".md", ".py", ".txt", ".xml", ".fcpxml", ".gitignore"}
PRIVATE_BYTES = (
    b"/us" + b"ers/",
    b"/vol" + b"umes/",
    b".ts" + b".net",
    b"jo" + b"hn",
)
PRIVATE_TEXT = (
    re.compile(r"(?:^|[^0-9])10(?:\.[0-9]{1,3}){3}(?:[^0-9]|$)"),
    re.compile(r"(?:^|[^0-9])192\.168(?:\.[0-9]{1,3}){2}(?:[^0-9]|$)"),
    re.compile(r"(?:^|[^0-9])172\.(?:1[6-9]|2[0-9]|3[01])(?:\.[0-9]{1,3}){2}(?:[^0-9]|$)"),
)


def hash_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def check_json(errors: list[str]) -> int:
    count = 0
    for path in REPO.rglob("*.json"):
        try:
            json.loads(path.read_text(encoding="utf-8"))
            count += 1
        except Exception as error:  # diagnostic script
            fail(errors, f"invalid JSON: {path.relative_to(REPO)}: {error}")
    return count


def check_closure(errors: list[str]) -> tuple[int, int, int]:
    source_index = REPO / "workflows/final-sources/final-source-index.csv"
    with source_index.open(newline="", encoding="utf-8-sig") as handle:
        sources = list(csv.DictReader(handle))
    if len(sources) != 31:
        fail(errors, f"expected 31 final sources, found {len(sources)}")
    for row in sources:
        candidates = [
            REPO / "media/final-sources" / row["item_name"],
            REPO / "workflows/final-sources" / row["api_workflow_file"],
            REPO / "workflows/final-sources" / row["prompt_file"],
        ]
        if row["ui_workflow_file"]:
            candidates.append(REPO / "workflows/final-sources" / row["ui_workflow_file"])
        for path in candidates:
            if not path.is_file():
                fail(errors, f"missing final-source closure file: {path.relative_to(REPO)}")

    input_dir = REPO / "assets/comfyui-input"
    assets = {path.name for path in input_dir.iterdir() if path.is_file()}
    if len(assets) != 58:
        fail(errors, f"expected 58 direct inputs, found {len(assets)}")

    direct_references: set[str] = set()
    api_dir = REPO / "workflows/final-sources/workflows/api"
    for graph_path in api_dir.glob("*.json"):
        graph = json.loads(graph_path.read_text(encoding="utf-8"))
        for node in graph.values():
            class_type = node.get("class_type")
            inputs = node.get("inputs", {})
            key = {"LoadImage": "image", "LoadAudio": "audio", "LoadVideo": "file"}.get(class_type)
            if key and isinstance(inputs.get(key), str):
                name = Path(inputs[key].replace(" [output]", "")).name
                direct_references.add(name)
                if name not in assets:
                    fail(errors, f"missing direct input {name} used by {graph_path.name}")
    if len(direct_references) != 58:
        fail(errors, f"expected 58 graph input references, found {len(direct_references)}")
    return len(sources), len(assets), len(direct_references)


def check_privacy(errors: list[str]) -> int:
    scanned = 0
    for path in REPO.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        if path == REPO / "release-assets/backlot-2160p-youtube.mp4":
            continue
        scanned += 1
        data = path.read_bytes()
        lower = data.lower()
        for pattern in PRIVATE_BYTES:
            if pattern in lower:
                fail(errors, f"private byte pattern {pattern!r} in {path.relative_to(REPO)}")
        if path.suffix.lower() in TEXT_SUFFIXES or path.name == ".gitignore":
            text = data.decode("utf-8", errors="replace")
            for pattern in PRIVATE_TEXT:
                if pattern.search(text):
                    fail(errors, f"private network pattern in {path.relative_to(REPO)}")
    return scanned


def check_sizes(errors: list[str]) -> list[str]:
    warnings: list[str] = []
    for path in REPO.rglob("*"):
        if not path.is_file() or "release-assets" in path.parts or ".git" in path.parts:
            continue
        size = path.stat().st_size
        if size >= 100 * 1024 * 1024:
            fail(errors, f"GitHub-blocked file >=100 MiB: {path.relative_to(REPO)}")
        elif size >= 50 * 1024 * 1024:
            warnings.append(f"GitHub large-file warning: {path.relative_to(REPO)} ({size} bytes)")
    return warnings


def check_final_media(errors: list[str]) -> None:
    expected = {
        "media/final/backlot-1080p.mp4": "cc9d5e8cd506aaaabe38285928060f1dc1b989d866d0c59c3eb8747a1c918e53",
        "release-assets/backlot-2160p-youtube.mp4": "2ca3bb5da2b5657742a2be971c1c1fadf8e432c1a8eaf3476492c5845a1cab62",
    }
    for relative, digest in expected.items():
        path = REPO / relative
        if not path.is_file():
            fail(errors, f"missing final media: {relative}")
        elif hash_file(path) != digest:
            fail(errors, f"unexpected hash for {relative}")


def check_timeline(errors: list[str]) -> None:
    path = REPO / "timeline/Main-final-locked.sanitized.fcpxml"
    text = path.read_text(encoding="utf-8")
    refs = re.findall(r'<media-rep src="([^"]+)"', text)
    if len(refs) != 62:
        fail(errors, f"expected 62 FCPXML media references, found {len(refs)}")
    if any(not value.startswith("file:///RELINK/media/final-sources/") for value in refs):
        fail(errors, "FCPXML contains a non-placeholder media path")
    summary = json.loads((REPO / "timeline/audits/av-sync-summary.json").read_text())
    if summary.get("creative_video_occurrences") != 62:
        fail(errors, "A/V audit does not contain 62 creative occurrences")
    if summary.get("source_offset_mismatches") != 0:
        fail(errors, "A/V audit reports source-offset mismatches")


def check_symlinks(errors: list[str]) -> None:
    for path in REPO.rglob("*"):
        if path.is_symlink():
            fail(errors, f"unexpected symlink: {path.relative_to(REPO)}")


def check_markdown_links(errors: list[str]) -> int:
    checked = 0
    for path in REPO.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text):
            target = target.strip().split("#", 1)[0]
            if not target or "://" in target or target.startswith(("mailto:", "#")):
                continue
            checked += 1
            destination = (path.parent / unquote(target)).resolve()
            if not destination.exists():
                fail(errors, f"broken Markdown link in {path.relative_to(REPO)}: {target}")
    return checked


def main() -> int:
    errors: list[str] = []
    check_symlinks(errors)
    link_count = check_markdown_links(errors)
    json_count = check_json(errors)
    sources, assets, references = check_closure(errors)
    scanned = check_privacy(errors)
    warnings = check_sizes(errors)
    check_final_media(errors)
    check_timeline(errors)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(
        f"PASS: {sources} sources, {assets} assets, {references} graph references, "
        f"{json_count} JSON files, {scanned} files privacy-scanned, "
        f"{link_count} relative links"
    )
    for warning in warnings:
        print(f"WARN: {warning}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
