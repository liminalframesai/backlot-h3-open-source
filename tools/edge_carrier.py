#!/usr/bin/env python3
"""Create an edge-video motion carrier with FFmpeg.

The output preserves timing and, by default, copies the source audio bit-for-bit while
discarding most surface appearance. It can then be used as a weak video reference in a
new H3 R2V pass beside cleaner keyframes and character/location references.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path


def arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--low", type=float, default=0.1)
    parser.add_argument("--high", type=float, default=0.4)
    parser.add_argument("--no-negate", action="store_true")
    parser.add_argument("--audio", choices=("copy", "aac", "none"), default="copy")
    parser.add_argument("--crf", type=int, default=18)
    parser.add_argument("--preset", default="slow")
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def build_command(args: argparse.Namespace) -> list[str]:
    edge_filter = f"edgedetect=low={args.low}:high={args.high}"
    if not args.no_negate:
        edge_filter += ",negate"
    command = [
        shutil.which("ffmpeg") or "ffmpeg",
        "-hide_banner",
        "-loglevel",
        "error",
        "-y" if args.overwrite else "-n",
        "-i",
        str(args.input),
        "-map",
        "0:v:0",
        "-map",
        "0:a?",
        "-vf",
        edge_filter,
        "-c:v",
        "libx264",
        "-preset",
        args.preset,
        "-crf",
        str(args.crf),
        "-pix_fmt",
        "yuv420p",
        "-fps_mode",
        "passthrough",
        "-map_metadata",
        "-1",
    ]
    if args.audio == "copy":
        command += ["-c:a", "copy"]
    elif args.audio == "aac":
        command += ["-c:a", "aac", "-b:a", "320k"]
    else:
        command += ["-an"]
    return command + [str(args.output)]


def main() -> int:
    args = arguments()
    if not args.input.is_file():
        raise SystemExit(f"input not found: {args.input}")
    if not 0 <= args.low <= 1 or not 0 <= args.high <= 1 or args.low >= args.high:
        raise SystemExit("require 0 <= low < high <= 1")
    if not 0 <= args.crf <= 51:
        raise SystemExit("CRF must be between 0 and 51")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(build_command(args), check=True)
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
