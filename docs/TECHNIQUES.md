# Techniques and findings

## 1. Treat the H3 reference prompt as an interface

The reliable pattern behaved less like decorative prose and more like a structured API:

1. `subject_definitions`
2. `summary`
3. `retention_analysis`
4. `detailed_description`
5. `overall_soundscape`
6. `non_diegetic_music`

The counterintuitive naming rule mattered: define `<Picture N>` as its own entry only when
that picture itself is later used as a concrete frame/keyframe. Character and location
sheets normally enter inside a `<Subject N>` definition, and the rest of the prompt refers
to the subject.

Bracketed modes in `summary` were operative. `[keyframe completion + reference generation
+ audio reuse]` produced materially different behavior from merely saying that Picture 1
should be the first frame.

## 2. Keyframe completion creates real opening-frame authority

The working recipe was:

- connect the still as the correctly numbered R2V picture input;
- define Picture 1 as the first frame of Shot 1;
- declare `keyframe completion` in `summary`;
- mark Picture 1 `fully_preserved` in `retention_analysis`;
- begin Shot 1 from that keyframe in `detailed_description`.

Free-form phrases such as “begin exactly on its pixels” were not an adequate substitute
for H3's task mode.

## 3. Native audio can be copied, referenced, or regenerated deliberately

- `fully_copy` with `[audio reuse]` carried complete input audio into a new H3 pass.
- `partially_copy` preserved a named portion or sound class while allowing a new mix.
- `[audio reference]` guided newly generated audio by material, rhythm, timbre, or role.

Exact-length reference audio was more reliable than feeding a short clip to a much longer
target. Audio extracted from a loaded video could be connected as an audio reference
without conditioning on all its video frames.

## 4. Sound recognition mattered more than frame-exact onset

The editorial mechanism is a perceptual rhyme: the audience hears a Foley action, then
recognizes its cinematic counterpart. The edit owns exact timing; the generated pair needs
to read as the same physical source in material, gesture, and timbre.

That specific evaluation question worked better than generic audiovisual-quality scoring.
Broad multimodal critiques sometimes produced confident but false timing claims.

## 5. A low-resolution test can become a production asset

A strong test's audio and motion are not disposable. A later H3 R2V pass can:

- retain the chosen test's native audio with `fully_copy`;
- use its motion, cuts, rhythm, and temporal structure as a `weak_reference` video;
- supply a cleaner, higher-resolution keyframe plus character/location subjects;
- ask H3 to regenerate visual detail while retaining useful temporal authority.

This changed testing from pure cost into **testing with upside**. Any prompt test could
unexpectedly produce the motion, edit rhythm, Foley signature, voice, or mix worth carrying
forward.

## 6. Edge-video motion carriers separate motion from appearance

The project independently developed this technique during an earlier film and refined it
on Backlot. Similar methods may exist; this is a description of the project's own
discovery and use, not a claim of universal first invention.

```sh
ffmpeg -i source.mp4 \
  -vf "edgedetect=low=0.1:high=0.4,negate" \
  -c:a copy motion-edge.mp4
```

The edge clip retains motion, cuts, timing, and optional native audio while discarding
most surface detail. In H3 it can be a weak `<Video N>` reference beside a new high-quality
Picture 1 and character/location subjects. This gave the model more room to rerender every
frame rather than passing through unwanted old appearance.

It is not guaranteed “upscaling.” It is a **re-resolution route**: motion and sound remain
the temporal authority while appearance is generated again. The repository includes:

- [`tools/edge_carrier.py`](../tools/edge_carrier.py), a standalone safe wrapper;
- [`custom_nodes/ComfyUI-FFmpeg-Edge-Carrier/`](../custom_nodes/ComfyUI-FFmpeg-Edge-Carrier/),
  a small ComfyUI preprocessing node;
- [`workflows/edge-motion-carrier/edge-motion-carrier.workflow.json`](../workflows/edge-motion-carrier/edge-motion-carrier.workflow.json).

Use it as a two-stage process: create the carrier, refresh ComfyUI's selectors, then load
it into the H3 R2V graph. Copy audio when it is already valuable; choose AAC only when the
source codec cannot be remuxed into MP4.

## 7. A fast R2V adaptation enabled local iteration

The filmmaker adapted the public [ALPHA-T1](https://github.com/newbmechanix-ship-it/ALPHA-T1)
I2V workflow into a reference-to-video graph using:

- the H3 `ref2va` int8 ConvRot model;
- LightX2V R2V turbo LoRA at 0.5;
- Euler + `bong_tangent`;
- 12 steps, CFG 1;
- Fused Modulation;
- Sol-Attn at tau 1.3, `min_tokens=4096`, `exact_kv`;
- Qwen3-VL 32B H3 Q4_K_M encoder;
- `ref_image_size=match`;
- 24 fps and H3's valid `17k+5` frame sequence.

Eleven unique final clips came from that family. It was a productive middle ground between
artifact-prone four-step tests and slow 20-step high-resolution/video-reference runs.

## 8. Reference image size is a major performance lever

Encoding high-resolution reference sheets at source size can multiply runtime because
their tokens travel through sampling. `ref_image_size=match` kept most tests practical.
Larger/max encoding was reserved for shots where faces truly needed the detail.

## 9. Acceleration must remain shot-specific

Four-step Lightning tests often showed character-sheet bleed, strange compositing, and
under-resolved complex motion. The action was not simplified merely to fit four steps.
Production returned to known-good 20-step runs, then adopted the separately tested
12-step Alpha-derived path.

One acceptable fast result is not proof that an accelerated configuration is safe for all
shots.

## 10. Repeated image edits can accumulate invisible-to-model defects

Repeated image-model edits sometimes accumulated a mottled, overprocessed texture,
especially on fabric. It could be obvious to a human but missed by visual-language
evaluators.

Mitigations were to restart from a clean source, include the original character reference,
name the artifact explicitly during restoration, render several candidates, and inspect
the opening frame at full size. H3 often cleared the issue after a cut, but keyframe
completion faithfully preserved it in frame zero.

## 11. Recover final-used workflows from outputs, not memory

Exploration produced 535 videos; the edit used only 31 unique sources. The final package
was built by parsing the frozen timeline, locating each H3 output, and extracting its
embedded prompt/API/UI metadata. This made the publication closure exact even though the
editor had copied candidate clips into a separate selects folder.
