# MCP and agent coordination case study

Backlot was the filmmaker's first complete ComfyUI project. Agent-connected tools were not
a novelty layer around an already-finished pipeline; they were the production
infrastructure that made rapid local exploration manageable.

## What the tooling did

- indexed shot cards, prompts, references, variants, and rendered takes;
- maintained an ordered render queue with pause/block/fix semantics;
- submitted H3 graphs and monitored output without manual repetitive setup;
- surfaced prompt text and input provenance for debugging;
- established shared character, location, door, and audio locks;
- generated broad overnight coverage and preserved every candidate;
- recovered embedded workflows/prompts from the exact clips used by the final edit;
- audited timeline A/V source offsets and packaged reproducibility evidence.

## Human and agent roles

The productive split was iterative rather than “automation versus manual work.” Agents
were strongest at breadth, bookkeeping, structured prompt conversion, queue management,
provenance, and repeatable audits. Human review was strongest at continuity, hand/action
physics, texture defects, performance, sound recognition, and deciding whether a few
seconds were editorially useful.

The final interactive generations reused agent-developed prompts, repaired keyframes,
production locks, audio anchors, and tested workflow settings. Likewise, manual discoveries
about H3's exact prompt vocabulary fed back into automated prompt generation. MCP did not
“fail and get replaced”; it remained valuable through final tuning and evidence recovery.

## What initially went wrong

- a copied queue UI did not initially dispatch ready work correctly;
- finished items were visually mixed with active queue items;
- prompts were initially hard to inspect;
- opening frames and shot identifiers drifted;
- early R2V prompts used emphatic prose where H3 expected specific task modes;
- evaluator models missed visible artifacts and sometimes hallucinated timing quality;
- aggressive four-step settings were generalized beyond the shots where they worked.

Each failure became a pipeline requirement: prompt preview, exact input mapping, production
locks, first-frame task modes, conservative sampler baselines, and audit data that did not
depend on evaluator confidence.

## General lesson

An agent system is most useful here as a production coordinator with explicit state—not
as an oracle for aesthetic quality. The durable artifacts are a queue record, exact graph,
prompt, input manifest, source hash, and output. A human can then make a creative decision
without losing reproducibility.

The implementation details of the private production network are intentionally excluded.
This repository publishes the workflows and evidence, not hostnames, paths, credentials,
or deployment topology.
