#!/usr/bin/env python3
"""Build public media manifests from the final workflow/source indexes."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
from collections import defaultdict
from pathlib import Path


def arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    return parser.parse_args()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def probe(path: Path) -> dict:
    command = [
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration:stream=codec_type,codec_name,width,height,sample_rate,channels,r_frame_rate",
        "-of", "json", str(path),
    ]
    return json.loads(subprocess.check_output(command, text=True))


def technical_summary(data: dict) -> str:
    parts: list[str] = []
    for stream in data.get("streams", []):
        if stream.get("codec_type") == "video":
            parts.append(
                f"video={stream.get('codec_name','?')} "
                f"{stream.get('width','?')}x{stream.get('height','?')} "
                f"fps={stream.get('r_frame_rate','?')}"
            )
        elif stream.get("codec_type") == "audio":
            parts.append(
                f"audio={stream.get('codec_name','?')} "
                f"{stream.get('sample_rate','?')}Hz ch={stream.get('channels','?')}"
            )
    duration = data.get("format", {}).get("duration")
    if duration:
        parts.append(f"duration={float(duration):.3f}s")
    return "; ".join(parts)


def input_provenance(filename: str, kind: str) -> str:
    lower = filename.lower()
    if kind == "image":
        return "AI-generated or AI-restored project reference image"
    if "anchor" in lower:
        return "Voice anchor extracted from a project H3 native-audio take"
    if lower.startswith("music-") or "backlot shadows" in lower or "backlot-shadows" in lower:
        return "Prepared segment of the project Suno-generated music guide"
    if "edge" in lower:
        return "FFmpeg edge-motion carrier derived from a project H3 video"
    if kind == "video":
        return "Project H3 video used as a motion, continuation, or audio reference"
    return "Sound/audio reference extracted or prepared from project-generated material"


def graph_input_usage(repo: Path) -> list[dict[str, str]]:
    usage: dict[str, set[str]] = defaultdict(set)
    kinds: dict[str, str] = {}
    api_dir = repo / "workflows/final-sources/workflows/api"
    for graph_path in sorted(api_dir.glob("*.json")):
        graph = json.loads(graph_path.read_text(encoding="utf-8"))
        for node in graph.values():
            class_type = node.get("class_type")
            inputs = node.get("inputs", {})
            key_kind = {
                "LoadImage": ("image", "image"),
                "LoadAudio": ("audio", "audio"),
                "LoadVideo": ("file", "video"),
            }.get(class_type)
            if not key_kind:
                continue
            key, kind = key_kind
            if not isinstance(inputs.get(key), str):
                continue
            filename = Path(inputs[key].replace(" [output]", "")).name
            usage[filename].add(graph_path.name)
            kinds[filename] = kind
    return [
        {
            "public_filename": filename,
            "kind": kinds[filename],
            "used_by_graph_count": str(len(graphs)),
            "used_by_graphs": ";".join(sorted(graphs)),
        }
        for filename, graphs in sorted(usage.items(), key=lambda pair: pair[0].casefold())
    ]


def write_input_manifest(repo: Path) -> None:
    usage = graph_input_usage(repo)
    rows = []
    for item in usage:
        filename = item["public_filename"]
        path = repo / "assets" / "comfyui-input" / filename
        rows.append({
            "path": path.relative_to(repo).as_posix(),
            "kind": item["kind"],
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
            "direct_workflow_count": item["used_by_graph_count"],
            "direct_workflows": item["used_by_graphs"],
            "provenance": input_provenance(filename, item["kind"]),
            "technical": technical_summary(probe(path)),
        })
    output = repo / "assets" / "ASSET-MANIFEST.csv"
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def write_source_manifest(repo: Path) -> None:
    index_path = repo / "workflows" / "final-sources" / "final-source-index.csv"
    with index_path.open(newline="", encoding="utf-8-sig") as handle:
        index = list(csv.DictReader(handle))
    rows = []
    for item in index:
        path = repo / "media" / "final-sources" / item["item_name"]
        data = probe(path)
        rows.append({
            "index": item["index"],
            "path": path.relative_to(repo).as_posix(),
            "video_occurrences": item["video_occurrences"],
            "audio_occurrences": item["audio_occurrences"],
            "workflow_format": item["workflow_format"],
            "api_workflow": "workflows/final-sources/" + item["api_workflow_file"],
            "ui_workflow": (
                "workflows/final-sources/" + item["ui_workflow_file"]
                if item["ui_workflow_file"] else ""
            ),
            "prompt": "workflows/final-sources/" + item["prompt_file"],
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
            "original_embedded_source_sha256": item["source_sha256"],
            "technical": technical_summary(data),
        })
    output = repo / "media" / "final-sources" / "FINAL-SOURCE-MANIFEST.csv"
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    args = arguments()
    repo = args.repo.resolve()
    write_input_manifest(repo)
    write_source_manifest(repo)
    print("wrote input and final-source manifests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
