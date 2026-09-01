# Backlot

**Backlot** is an 88-second native-audiovisual horror short made locally with
[ComfyUI](https://github.com/Comfy-Org/ComfyUI) and MiniMax H3 for the Comfy H3 Sync
Challenge. The film cuts between a rain-soaked horror scene and the Foley stage making
its sounds—until the film world reaches through the door.

This repository is the compact, final-cut closure of the project: the finished 1080p
film, every H3 source clip used by the timeline, every direct image/audio/video reference
used to generate those sources, their exact API graphs and prompts, the available visual
workflows, a relinkable timeline, and an independent A/V-sync audit. The other 501 local
experiments are intentionally omitted; three first-night drafts are included to show how
the final idea emerged.

## Watch

- [`media/final/backlot-1080p.mp4`](media/final/backlot-1080p.mp4) — 1920×1080, 24 fps,
  88.125 seconds, stereo AAC
- `backlot-2160p-youtube.mp4` — 4K YouTube master, supplied as a GitHub Release asset;
  see [`release-assets/README.md`](release-assets/README.md)

Both deliverables were produced from the uncompressed Resolve master in one FFmpeg
finishing graph so they share the same Lanczos upscale, mild sharpening, and film-grain
pass. The exact command is in [`docs/REPRODUCIBILITY.md`](docs/REPRODUCIBILITY.md#final-finishing-and-delivery-encodes).

Headphones or speakers are recommended: the edit is built around recognizable sound
continuity between each Foley gesture and its cinematic counterpart.

## What is reproducible here

- **31/31 final source clips** and their native sound
- **31/31 exact executable API graphs** recovered from H3 output metadata
- **31/31 exact prompts**
- **13/31 embedded visual ComfyUI workflows**; the other 18 automated outputs contained
  an API graph but no visual canvas, and are labeled accordingly
- **58/58 directly referenced inputs**, in a flat ComfyUI-ready directory
- the frozen Resolve timeline as a path-sanitized FCPXML
- a frame-level audit of all 62 creative timeline occurrences

Start with [`workflows/submission/Backlot-H3-fast-r2v-annotated.workflow.json`](workflows/submission/Backlot-H3-fast-r2v-annotated.workflow.json)
for one documented final-used workflow. For the whole film, use
[`workflows/final-sources/final-source-index.csv`](workflows/final-sources/final-source-index.csv).

## Key contributions

1. **H3 prompts as a structured interface.** The official full-reference vocabulary—
   including `keyframe completion`, numbered subjects, retention modes, and audio reuse—
   proved much more deterministic than free-form prompting.
2. **Testing with upside.** A low-resolution test with good motion or native audio can be
   promoted in a later R2V pass rather than discarded.
3. **Edge-video motion carriers.** An FFmpeg edge transform can retain motion, cuts,
   rhythm, and optional native audio while giving H3 room to regenerate surface detail
   from cleaner still/character/location references.
4. **Native-audio editorial proof.** All 62 final picture occurrences have correctly
   source-aligned H3 audio. The edit deliberately carries many native-audio segments past
   their picture cuts—sometimes for several seconds or across multiple picture
   segments—and crossfades them with other H3-native audio. The frame-level audit found no
   source-offset mismatch and no picture frame without H3-native audio coverage.
5. **MCP as production infrastructure.** Agent tooling handled queueing, workflow and
   prompt surfacing, input/provenance management, batch exploration, and post-edit
   evidence recovery. Interactive generation then built directly on those prompts,
   references, and tests for the final shot-by-shot tuning.

Read [`docs/TECHNIQUES.md`](docs/TECHNIQUES.md),
[`docs/H3-PROMPTING.md`](docs/H3-PROMPTING.md), and
[`docs/MCP-CASE-STUDY.md`](docs/MCP-CASE-STUDY.md) for the practical findings.
The sanitized initial brief and three exploratory films are documented in
[`docs/INITIAL-EXPLORATION.md`](docs/INITIAL-EXPLORATION.md).

## Repository map

| Path | Contents |
|---|---|
| `media/final/` | Finished 1080p film |
| `media/final-sources/` | The 31 unique H3 clips used in the final timeline |
| `media/early-exploration/` | Three first-night concept drafts; none appears in the final film |
| `assets/comfyui-input/` | All 58 direct reference assets, ready for ComfyUI input |
| `workflows/submission/` | Annotated representative workflow and four inputs |
| `workflows/final-sources/` | All recovered API/UI workflows and prompts |
| `workflows/edge-motion-carrier/` | ComfyUI preprocessing workflow |
| `custom_nodes/` | Small FFmpeg edge-carrier ComfyUI node |
| `timeline/` | Sanitized FCPXML and sync-audit data |
| `tools/` | Edge-carrier, manifest, timeline, and verification utilities |
| `checksums/` | Release integrity hashes |

## Reopen a final workflow

1. Install ComfyUI with MiniMax H3 support and the nodes/models named by the graph. Model
   weights are not redistributed here.
2. Copy the contents of `assets/comfyui-input/` into the ComfyUI input directory.
3. Open a `*.workflow.json` file, or submit a corresponding `*.api.json` graph.
4. Keep the graph's numbered picture/video/audio inputs aligned with its prompt tags.
5. Expect seed- and implementation-dependent variance; the files document the exact
   inputs/settings used, not a promise of pixel-identical regeneration.

See [`docs/REPRODUCIBILITY.md`](docs/REPRODUCIBILITY.md) for model filenames, relinking,
and verification.

## Licensing and attribution

Original code is MIT-licensed. Original documentation and project media are offered
under CC BY 4.0 to the extent the publisher holds licensable rights. Third-party material
and model weights retain their own terms. The ALPHA-T1 workflow lineage and MIT notice are
preserved. See [`docs/RIGHTS-AND-ATTRIBUTION.md`](docs/RIGHTS-AND-ATTRIBUTION.md) and the
license files before reuse.

No workstation paths, hostnames, credentials, private project database, or network
topology are included in this public package.
