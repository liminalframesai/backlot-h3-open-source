# Comfy H3 Sync Challenge — submission summary

## Project

**Backlot** is an 88-second horror short in which a Foley crew performs the sounds of a
woman being pursued through a rain-soaked movie backlot—until the film world appears to
invade the soundstage. Every final picture and sound source was generated locally in
ComfyUI with MiniMax H3. DaVinci Resolve was used only for trimming, crossfades, volume and
pan, color work, and delivery.

The finished film uses 62 timeline occurrences from 31 unique H3 clips. All 62 have native
audio from the same source at a zero-frame source offset. Sound editing is a major part of
the construction: many native-audio segments continue for seconds beyond their picture
cuts or across several picture segments, then overlap and crossfade with other H3-native
audio. A frame-level audit found no retimes, source-offset mismatches, or picture frames
without H3-native audio coverage.

## Workflow to feature

Use
[`workflows/submission/Backlot-H3-fast-r2v-annotated.workflow.json`](../workflows/submission/Backlot-H3-fast-r2v-annotated.workflow.json)
as the single featured workflow. It is a final-used, annotated adaptation of the public
MIT-licensed ALPHA-T1 graph from `newbmechanix-ship-it`, shared by Spectro
(@Spectromachina). Its exact API graph, prompt, and four inputs are beside it.

The repository also contains every final-used graph, prompt, direct input, and source clip
for reviewers who want the full closure.

## MCP use

MCP-connected agents were used as production infrastructure: building and managing the H3
queue, exposing prompts and references, maintaining shot/character/location/audio locks,
submitting and monitoring local generations, running broad test coverage, and recovering
the exact workflows from the clips that survived the edit.

Final interactive tuning did not replace that work. It used agent-developed prompts,
keyframes, reference stacks, sound anchors, and workflow settings as its starting point.
After picture lock, the same tooling parsed the timeline and generated a reproducible,
privacy-sanitized evidence package.

## Findings worth highlighting

### Testing with upside

Low-resolution tests were treated as potential production assets. If a test produced
excellent motion or audio, a later H3 R2V pass could fully copy its native sound, weakly
reference its cuts/rhythm/motion, and regenerate appearance from a cleaner keyframe and
character/location references.

### Edge-video motion carriers

An FFmpeg edge transform was used to separate temporal structure from unwanted surface
appearance:

```sh
ffmpeg -i source.mp4 \
  -vf "edgedetect=low=0.1:high=0.4,negate" \
  -c:a copy motion-edge.mp4
```

The carrier gives H3 motion, cuts, timing, and optional native audio while leaving room to
re-render visual detail. This repository includes a standalone tool and a small ComfyUI
preprocessing node/workflow for the technique.

### Prompting as structured control

H3's full-reference format behaved like an interface, not merely prompt style. Exact task
modes such as `keyframe completion`, correct Picture/Subject declaration, retention
strengths, numbered connector order, and consistent audio-reuse language dramatically
improved first-frame, character, location, voice, and soundtrack control.

## Compact facts

- 535 local H3 generations during exploration
- 31 unique source clips in the final cut
- 31 exact API graphs and prompts recovered
- 58 direct generation inputs published
- 30/31 final prompts use the full six-section H3 structure
- 11 final clips use the Alpha-derived 12-step R2V workflow family
- 1080p film included in Git; 4K YouTube master supplied as a release asset

Replace this repository's relative links with the public GitHub URL when the remote is
created.
