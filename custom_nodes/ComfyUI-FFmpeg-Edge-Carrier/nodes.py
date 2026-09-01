"""ComfyUI node for preparing FFmpeg edge-video motion carriers."""

from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path

import folder_paths


VIDEO_EXTENSIONS = {".avi", ".m4v", ".mkv", ".mov", ".mp4", ".webm"}


def _input_root() -> Path:
    return Path(folder_paths.get_input_directory()).resolve()


def _video_choices() -> list[str]:
    root = _input_root()
    return sorted(
        str(path.relative_to(root))
        for path in root.rglob("*")
        if path.is_file() and path.suffix.lower() in VIDEO_EXTENSIONS
    ) or ["put-a-video-in-ComfyUI-input.mp4"]


def _safe_source(value: str) -> Path:
    root = _input_root()
    candidate = (root / value).resolve()
    try:
        candidate.relative_to(root)
    except ValueError as error:
        raise ValueError("source video must be inside ComfyUI's input directory") from error
    if not candidate.is_file():
        raise FileNotFoundError(candidate)
    return candidate


def _safe_prefix(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "-", value).strip(".-")
    if not cleaned:
        raise ValueError("output prefix must contain a letter or number")
    return cleaned[:120]


def _next_output(root: Path, stem: str) -> Path:
    candidate = root / f"{stem}.mp4"
    counter = 1
    while candidate.exists():
        candidate = root / f"{stem}-{counter:03d}.mp4"
        counter += 1
    return candidate


class FFmpegEdgeMotionCarrier:
    """Prepare an edge-only video in input/edge-carriers for a later R2V pass."""

    OUTPUT_NODE = True
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("comfy_input_path",)
    FUNCTION = "create"
    CATEGORY = "video/preprocessors"
    DESCRIPTION = (
        "Creates an FFmpeg edge-motion carrier under ComfyUI/input/edge-carriers. "
        "Refresh file selectors, then load that MP4 as a weak H3 video reference."
    )

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "source_video": (_video_choices(),),
                "low": ("FLOAT", {"default": 0.1, "min": 0.0, "max": 1.0, "step": 0.01}),
                "high": ("FLOAT", {"default": 0.4, "min": 0.0, "max": 1.0, "step": 0.01}),
                "negate": ("BOOLEAN", {"default": True}),
                "audio": (["copy", "aac_320k", "none"],),
                "output_prefix": ("STRING", {"default": "motion-edge"}),
                "crf": ("INT", {"default": 18, "min": 0, "max": 51}),
                "preset": (["medium", "slow", "slower"],),
            }
        }

    def create(
        self,
        source_video: str,
        low: float,
        high: float,
        negate: bool,
        audio: str,
        output_prefix: str,
        crf: int,
        preset: str,
    ):
        if not 0 <= low < high <= 1:
            raise ValueError("require 0 <= low < high <= 1")
        ffmpeg = shutil.which("ffmpeg")
        if not ffmpeg:
            raise RuntimeError("ffmpeg was not found on PATH")
        source = _safe_source(source_video)
        output_root = _input_root() / "edge-carriers"
        output_root.mkdir(parents=True, exist_ok=True)
        destination = _next_output(output_root, _safe_prefix(output_prefix))
        video_filter = f"edgedetect=low={low}:high={high}"
        if negate:
            video_filter += ",negate"
        command = [
            ffmpeg,
            "-hide_banner",
            "-loglevel",
            "error",
            "-n",
            "-i",
            str(source),
            "-map",
            "0:v:0",
            "-map",
            "0:a?",
            "-vf",
            video_filter,
            "-c:v",
            "libx264",
            "-preset",
            preset,
            "-crf",
            str(crf),
            "-pix_fmt",
            "yuv420p",
            "-fps_mode",
            "passthrough",
            "-map_metadata",
            "-1",
        ]
        if audio == "copy":
            command += ["-c:a", "copy"]
        elif audio == "aac_320k":
            command += ["-c:a", "aac", "-b:a", "320k"]
        else:
            command += ["-an"]
        command.append(str(destination))
        subprocess.run(command, check=True)
        relative = str(destination.relative_to(_input_root()))
        return {"ui": {"text": [relative]}, "result": (relative,)}


NODE_CLASS_MAPPINGS = {"FFmpegEdgeMotionCarrier": FFmpegEdgeMotionCarrier}
NODE_DISPLAY_NAME_MAPPINGS = {
    "FFmpegEdgeMotionCarrier": "FFmpeg Edge Motion Carrier"
}
