# ComfyUI FFmpeg Edge Motion Carrier

This small preprocessing node creates a line/edge version of a source video while
preserving its timing and, optionally, its native audio. The intended use is to give a
reference-to-video model motion, cuts, and rhythm without forcing it to preserve all of
the source video's surface appearance.

## Install

1. Copy this directory into `ComfyUI/custom_nodes/`.
2. Ensure `ffmpeg` is on the process `PATH`.
3. Restart ComfyUI.
4. Put a source video in `ComfyUI/input/` and add **FFmpeg Edge Motion Carrier**.

The node writes a new MP4 under `ComfyUI/input/edge-carriers/`. Refresh the file lists,
then load that MP4 in the generation workflow as a weak video reference. This is
deliberately a two-stage operation: ComfyUI file selectors are normally resolved before
the generation graph executes.

Default filter:

```sh
ffmpeg -i source.mp4 \
  -vf "edgedetect=low=0.1:high=0.4,negate" \
  -c:a copy motion-edge.mp4
```

If the input audio codec cannot be copied into MP4, select `aac_320k`.

Code: MIT License. See the repository root.
