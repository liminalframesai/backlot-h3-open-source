# Backlot — all final-used H3 workflows and prompts

This public bundle contains the exact ComfyUI generation metadata for every unique H3 MP4 source used by the frozen **Backlot** final timeline.

- 31 unique final H3 source clips
- 31 exact API graphs
- 31 extracted H3 prompts
- 13 embedded visual UI workflows
- 18 API-only automated-render graphs
- 0 missing final sources

`final-source-index.csv` maps each final source filename to its prompt and workflow files without exposing the editor's local filesystem paths.

## Formats

- `workflows/ui/*.workflow.json` can be opened as visual ComfyUI workflows.
- `workflows/api/*.api.json` are exact executable API graphs embedded in the H3 MP4s.
- `prompts/*.txt` are the exact H3 prompts recovered from those API graphs.

The automated queue embedded exact API graphs but not the visual canvas layout in 18 outputs. Those files are labeled API-only rather than being reconstructed or represented as original UI workflows.

For a self-contained starting example, use `../submission/`. The complete set of direct
inputs for every graph is in `../../assets/comfyui-input/`.

## Credit

Eleven final sources use the filmmaker's R2V adaptation of
[ALPHA-T1](https://github.com/newbmechanix-ship-it/ALPHA-T1), published by
`newbmechanix-ship-it` and shared by Spectro (@Spectromachina), licensed under MIT. The
upstream license notice is preserved in the repository's `THIRD_PARTY_LICENSES/` folder.

Core audiovisual generation: ComfyUI + MiniMax H3.
