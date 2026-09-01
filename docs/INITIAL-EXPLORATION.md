# Initial agent brief and first-night exploration

Backlot began on August 24, 2026, as an open-ended test: could a first-time ComfyUI
filmmaker, a local RTX 3080 Ti, MiniMax H3, and an agent-coordinated production system
build a complete native-audiovisual short in one week?

The first overnight run produced three one-minute concept drafts. None contributed footage
to the final edit. They were still productive: **Weather Department** explored people
creating a soundtrack inside the world of the film, which led directly to Backlot's
cross-cutting Foley-stage premise.

## The initial brief

This is the original human brief with private endpoints and infrastructure details removed.
It is preserved because the challenge specifically encouraged sharing how MCP and agent
prompts were used.

> Check out the environment and start orchestrating a new task: win the Comfy H3 Sync
> Sound Community Challenge.
>
> Here is the local ComfyUI instance: `<redacted local endpoint>`. The agent environment
> can reach it through `<redacted local connection>`.
>
> Do the majority of work through the agent environment. You are manager, chief of staff,
> and orchestrator of this project, so wake up often enough to make sure everything stays
> on task, and farm tasks out through the agents. Use the available tools to develop a
> story or music-video concept, create necessary assets to feed into H3, assemble
> agent-edited tests, and use whatever evaluation and testing strategy seems most
> effective.
>
> I am not participating tonight. I have a recently configured, local H3 environment and
> want to see how far the agents can get without me. I will be available over the next few
> days for final external edits or to get story and ideas back on track.
>
> Do not finish one simple thing and stop; you have all night. If you think you are done
> early, start another idea. Waking up to three finished drafts is better than waking to
> one with six hours idle, but do not compromise quality for volume. If the team is busy
> all night making one great entry, that is even better. Only one entry can go to the
> contest; if several are made, I will choose one for further refinement.
>
> Use the official MiniMax H3 base and reference-video prompting guides, and incorporate
> our existing structured video-prompting knowledge. ComfyUI can be used for image and
> music generation as well as H3 video generation. Read the rules and clarifications. The
> important constraint appears to be that audio and video are generated together, while
> input audio and music may guide generation. Favor subject matter with a rich,
> directional soundscape that can benefit from stereo editing.
>
> Install and use a ComfyUI MCP server if possible; the challenge includes an MCP category.
> There are only seven days, and the primary prize is an RTX 5090.

The official guides referenced by that brief were:

- [MiniMax H3 reference-video prompt-writing guide](https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/docs/VIDEO_PROMPT_WRITING_GUIDE_ref_en.md)
- [MiniMax H3 base prompt-writing guide](https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/docs/VIDEO_PROMPT_WRITING_GUIDE_base_en.md)

## The three drafts

| Draft | Runtime | What it contributed |
|---|---:|---|
| [Weather Department](../media/early-exploration/weather-department-draft-v3.mp4) | 78.574 s | The conceptual seed for cutting between cinematic action and the people creating its sound |
| [Sweep](../media/early-exploration/Sweep-draft-960x544.mp4) | 77.000 s | An alternate story and early test of unattended multi-shot assembly |
| [Anvil Hour](../media/early-exploration/anvil-hour-draft-v1.mp4) | 62.000 s | A second alternate story and early local H3 production test |

These are presented as process evidence, not polished work. The poor sound balance,
continuity drift, and visual inconsistency made the next requirements obvious: inspectable
prompts, explicit reference mapping, production locks, an ordered queue, and human review
for performance and physical continuity. Those requirements shaped the production system
documented in [`MCP-CASE-STUDY.md`](MCP-CASE-STUDY.md).
