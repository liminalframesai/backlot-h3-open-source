# Reproducibility guide

## Final-used source closure

`workflows/final-sources/final-source-index.csv` maps each unique final source to:

- an exact API graph;
- an extracted prompt;
- an embedded visual workflow when ComfyUI wrote one;
- source occurrence counts and original source hash.

`assets/ASSET-MANIFEST.csv` maps all 58 direct inputs to the graphs that use them.
`media/final-sources/FINAL-SOURCE-MANIFEST.csv` maps the 31 source clips back to their
graphs and prompts.

## ComfyUI setup

The graphs name their exact model and node dependencies. The recurring production family
uses filenames such as:

- `minimax_h3_ref2va_pruned_int8_convrot.safetensors`
- `minimax_h3_ref2v_lightx2v_turbo_4step_v0.1_resized_avg_rank_20_bf16.safetensors`
- `qwen3vl-32B-MiniMax-H3-Q4_K_M.gguf`
- `minimax_h3_video_vae_fp16.safetensors`
- `minimax_h3_audio_vae_fp32.safetensors`

Model weights are intentionally not included. Install compatible ComfyUI/MiniMax H3
support and any custom nodes named by the graph.

Copy every file under `assets/comfyui-input/` into the top level of ComfyUI's input
directory. The public graphs use those flat, normalized filenames. Two filenames and one
output-selector reference were normalized for privacy/portability; render parameters,
prompts, seeds, model names, and connector structure were otherwise preserved.

## Timeline relinking

`timeline/Main-final-locked.sanitized.fcpxml` points to the placeholder root
`file:///RELINK/media/final-sources/`. Import it into Resolve, select the offline clips,
and relink to this repository's `media/final-sources/` directory.

The opaque Resolve project export is not published because project databases can retain
private workstation paths. The portable FCPXML plus all source files and audits provides
the public edit closure.

## Verify

From the repository root:

```sh
python3 tools/verify_repo.py
shasum -a 256 -c checksums/SHA256SUMS
```

The verifier checks counts, workflow/input closure, JSON validity, private-path patterns,
symlinks, missing files, and GitHub's normal 100 MiB object limit. The ignored 4K release
asset is verified separately by its published hash.

## Expected variance

Generative runs may vary across seeds, ComfyUI/node revisions, driver/library changes, and
model builds even when a graph is unchanged. This package establishes exact provenance
and a runnable starting point; it does not claim bit-identical generative determinism.
