# H3 full-reference prompting notes

Backlot's reliable prompts follow MiniMax's official full-reference structure. The exact
final prompts are in `workflows/final-sources/prompts/`; this page records the operating
rules learned during production.

Official guides:

- [Full-reference prompt guide](https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/docs/VIDEO_PROMPT_WRITING_GUIDE_ref_en.md)
- [Base prompt guide](https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/docs/VIDEO_PROMPT_WRITING_GUIDE_base_en.md)

## Reference declaration rules

- Create a `<Picture N>` definition only when that exact picture is used directly later,
  such as a first or last keyframe.
- Put character/location/reference-sheet filenames inside a `<Subject N>` definition;
  refer to the subject afterward.
- If one subject appears in several assets, name each asset's role inside the same subject
  definition.
- Numbered tags must match connector order exactly. An almost-correct graph/prompt pair can
  fail semantically while still rendering.
- Do not add remembered negatives for conditions the video model never saw. Describe the
  wanted state directly.

## Minimal frame-zero pattern

```text
subject_definitions:
<Picture 1> is the first frame of [Shot 1], showing ...
<Subject 1> is ... whose character reference comes from <Picture 2> and who appears in
<Picture 1>.
<Audio 1> is ...

summary:
[keyframe completion + reference generation + audio reuse] ...

retention_analysis:
<Picture 1> ([Shot 1] first frame): fully_preserved - ...
<Subject 1> (...): fully_preserved - ...
<Audio 1>: fully_copy - ...
```

Then make Shot 1's keyframe explicitly correspond to Picture 1 in
`detailed_description`.

## Audio relationships

Use the guide's declared operation and retention language consistently:

- exact waveform/track: `audio reuse` + `fully_copy`;
- selected sounds or segment: `audio reuse` + `partially_copy`;
- newly rendered sound guided by a reference: `audio reference` with the appropriate
  reference strength.

Avoid claiming `fully_copy` in one section and describing a different regenerated mix in
another. Match reference duration to target duration when exact retention matters.

## Multi-shot prompts

Timed cuts worked when each shot had a clear visual action and audio responsibility. Four
sampling steps were often insufficient for difficult hands, material deformation, crowds,
or multi-character blocking; that is a sampling decision, not a reason to weaken the
creative beat.

Of the 31 final prompts, 30 use the six-section structure, 20 declare keyframe completion,
22 declare audio reuse, and 9 use H3's language-tagged dialogue syntax.
