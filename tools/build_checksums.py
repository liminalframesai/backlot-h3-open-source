#!/usr/bin/env python3
"""Write deterministic SHA-256 manifests for repository and release assets."""

from __future__ import annotations

import hashlib
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
MAIN = REPO / "checksums/SHA256SUMS"
RELEASE = REPO / "checksums/RELEASE-ASSETS.sha256"


def digest(path: Path) -> str:
    result = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            result.update(block)
    return result.hexdigest()


def line(path: Path) -> str:
    return f"{digest(path)}  {path.relative_to(REPO).as_posix()}"


def main() -> int:
    MAIN.parent.mkdir(parents=True, exist_ok=True)
    excluded = {MAIN, RELEASE, REPO / "release-assets/backlot-2160p-youtube.mp4"}
    files = sorted(
        path for path in REPO.rglob("*")
        if path.is_file()
        and ".git" not in path.parts
        and ".verification" not in path.parts
        and "__pycache__" not in path.parts
        and path.name != ".DS_Store"
        and path.suffix != ".pyc"
        and path not in excluded
    )
    MAIN.write_text("\n".join(line(path) for path in files) + "\n", encoding="utf-8")
    release_asset = REPO / "release-assets/backlot-2160p-youtube.mp4"
    RELEASE.write_text(line(release_asset) + "\n", encoding="utf-8")
    print(f"hashed {len(files)} repository files and one release asset")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
