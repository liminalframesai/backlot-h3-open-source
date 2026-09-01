# Project statistics

## Local generation volume

The project window begins with the first local H3 smoke test. It contains **535 MP4s**;
all 535 probed successfully and contain audio.

| Output family | Clips | Role |
|---|---:|---|
| Backlot | 307 | Main queued exploration and production |
| ALPHA-T1 | 113 | Fast interactive workflow and shot variants |
| MiniMax | 49 | Direct template, smoke, and manual runs |
| Weather Department | 30 | Early concept exploration |
| Sweep | 19 | Early alternate concept exploration |
| Anvil Hour | 7 | Early alternate concept exploration |
| Backlot Recognition | 6 | Recognition-criterion sync experiment |
| Backlot Sync | 4 | Initial two-direction sync experiment |
| **Total** | **535** | Local ComfyUI H3 outputs |

## Final-cut concentration

- 88.125-second timeline at 24 fps
- 62 creative H3 video occurrences
- 31 unique H3 source MP4s (5.8% of generated clips)
- 197.715 seconds of unique raw final-source material
- 11 unique `ALPHA-T1_*` sources
- 18 unique queued `Backlot_*` sources
- 2 unique direct `MiniMax_H3_*` sources
- 58 unique direct reference inputs across the 31 workflows

## Workflow recovery

| Artifact | Recovery |
|---|---:|
| Exact API graphs | 31/31 |
| Exact H3 prompts | 31/31 |
| Embedded visual UI workflows | 13/31 |
| API-only automated graphs | 18/31 |
| Missing final sources | 0 |

API-only graphs are still executable. The automated queue did not embed a visual canvas in
those outputs, so this repository does not reconstruct one and call it original.

## Prompt corpus

- 30/31 use the six-section full-reference structure
- 20 declare `keyframe completion`
- 28 declare `reference generation`
- 22 declare `audio reuse`
- 8 declare `audio reference`
- 9 use language-tagged dialogue syntax
- one final legacy source predates the standardized rewrite

## Final workflow settings

- 30/31 unique sources use H3 R2V; one uses H3 I2V
- 29 use Euler + `bong_tangent`; two use `res_multistep` + `simple`
- 30 use the H3 `ref2va` int8 ConvRot model; one uses `fl2va`
- 11 use the Alpha-derived 12-step R2V family at 0.6, 0.8, or 1.0 megapixel

The file-level manifests in `assets/` and `media/final-sources/` contain sizes, hashes,
technical stream data, and workflow mappings for the published closure.
