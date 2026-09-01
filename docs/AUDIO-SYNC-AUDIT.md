# Final native-audio alignment audit

The frozen timeline contains **62 creative H3 picture occurrences**, and all 62 have
paired audio from the same H3 source at an exact **0-frame source offset**.

The audit distinguishes **synchronization** from **editing coverage**. It does not count
the total number or duration of the film's audio overlaps.

- **59** picture occurrences have their own aligned source audio spanning the entire
  visible picture segment.
- **3** extend just 1–3 picture frames beyond the available same-source audio segment at
  one edge: two final 3-frame tails and one initial 1-frame head. Those frames are covered
  by adjacent H3-native audio.
- **0** picture frames lack native H3 audio coverage.
- **0** source-offset mismatches were found.
- **0** retimes appear in the FCPXML.

Therefore all 62 are correctly described as carrying synchronized native H3 audio. The
three-edge figure describes only that narrow same-source picture-coverage test; it is not
the number of crossfades, L/J edits, or extended audio tails in the film.

Audit data:

- [`timeline/audits/av-sync-summary.json`](../timeline/audits/av-sync-summary.json)
- [`timeline/audits/video-av-sync-audit.csv`](../timeline/audits/video-av-sync-audit.csv)
- [`timeline/audits/audio-lineage-audit.csv`](../timeline/audits/audio-lineage-audit.csv)

Only trims, crossfades, level/pan changes, and color correction were used in the final
edit. Native H3 audio is edited extensively: many segments continue beyond their picture
cuts, sometimes by several seconds and sometimes across multiple picture segments from
the same generated take, before crossfading with other H3-native audio. These are
intentional L/J-style sound edits, not timing slips. No external replacement soundtrack
appears on the timeline. A Suno-generated music guide was used as an H3 generation
reference, so its influence is inside H3-native clip audio rather than placed as a
standalone edit track.

The published CSVs and FCPXML use sanitized relink paths. The audit was performed against
the frozen Resolve project database before path sanitization.
