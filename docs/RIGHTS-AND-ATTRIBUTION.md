# Rights, licensing, and attribution

This is a provenance record, not legal advice.

## Repository license split

- Original source code and scripts: [MIT](../LICENSE)
- Original documentation, prompts, project images, project audio references, final-used H3
  generations, and finished film: [CC BY 4.0](../LICENSE-MEDIA.md), to the extent copyright
  or related licensable rights exist and are held by Liminal Frames
- ALPHA-T1-derived workflow material: upstream MIT terms and notice preserved in
  [`THIRD_PARTY_LICENSES/ALPHA-T1-LICENSE.txt`](../THIRD_PARTY_LICENSES/ALPHA-T1-LICENSE.txt)
- Model weights, third-party software, and services: not included and not relicensed

## Project media declarations

The producer states that:

- all project input images and characters were AI-generated for this production;
- some early style/reference assets were generated with Midjourney under a current paid
  subscription;
- GPT Image was used for reference/keyframe development, and Nano Banana Pro was used
  sparingly for restoration;
- the recurring music guide was generated in Suno while the producer had a paid
  subscription and continues to have one;
- final timeline picture and sound come from local ComfyUI/MiniMax H3 generations; the
  Suno guide is not a standalone edit-track source.

Suno's current official terms state that, subject to compliance, a Pro or Premier user is
assigned Suno's rights in outputs generated from that user's submissions during the paid
subscription term, while also warning that copyright may not vest in machine-generated
output: <https://about.suno.com/terms>.

Midjourney's current official terms say users own assets they create to the fullest extent
possible under applicable law, subject to listed exceptions and third-party rights:
<https://docs.midjourney.com/hc/en-us/articles/32083055291277-Terms-of-Service>.

These service terms can change. Preserve the subscription/generation records and recheck
the governing terms before a materially different commercial redistribution.

## ALPHA-T1 credit

- Project: [ALPHA-T1](https://github.com/newbmechanix-ship-it/ALPHA-T1)
- Publisher: `newbmechanix-ship-it`
- Shared by: Spectro ([@Spectromachina](https://x.com/Spectromachina))
- License: MIT
- Use: foundation for the later **H3 fast r2v** workflow

The adaptation changes the graph from H3 I2V to the reference-video family, uses
`MiniMaxH3ReferenceToVideo`, adds numbered image/audio/video references, and uses
`ref_image_size=match`. Eleven final-source clips use this adapted family.

## MiniMax prompt documentation

Prompts were developed against MiniMax's official
[full-reference](https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/docs/VIDEO_PROMPT_WRITING_GUIDE_ref_en.md)
and [base](https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/docs/VIDEO_PROMPT_WRITING_GUIDE_base_en.md)
guides.

## Attribution request

When redistributing the CC-licensed project material, credit **Backlot / Liminal Frames**
and link to the eventual public repository. Retain third-party notices and identify
material changes.
