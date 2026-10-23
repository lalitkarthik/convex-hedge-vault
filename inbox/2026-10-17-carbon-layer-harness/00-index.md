promoted: 2026-10-23
# Carbon Layer harness series — index

Study notes on The Carbon Layer's "Harness Engineering Masterclass" playlist (Ankit Desai, videos 01–11) and one IBM conference talk (Tejas Kumar, video 12). Written 2026-10-17 from the subtitles, in our own words. Raw subtitles stay in the session scratch folder and are not in the vault.

## What the series teaches as a whole

The series has one claim: an agent is a model inside a harness, and the harness is the part you engineer. The model is frozen, stateless and rented. What it sees, what it can touch, what it remembers, how its work is checked, and how the system learns from failure are all software decisions around it. When an agent fails, the right question is which harness layer ran out of road.

The series builds that claim in four stages. First it names the layers (video 01) and builds them one at a time in Python (03), with the IBM talk (12) as a short second view of the same idea. Then it goes deep on single layers: context management (06), memory (04), skills (07), and sandboxing (09). Next it asks how you know the agent works, with an evaluation harness (08). Finally it scales up in two directions: a loop that improves the harness itself (02, 11), and a meta-harness that coordinates several agents with code instead of a supervisor model (05, 10).

Three ideas run through every video. Put deterministic work in code and leave only judgment to the model. Hold boundaries in infrastructure, not in prompts. Accept nothing as done or improved without receipts that you can trace to an exact, fingerprinted configuration.

## Order to watch

The playlist numbers are not the best learning order. This order follows the dependencies the videos state.

1. **01** Harness Engineering Masterclass — the map of layers. Everything else hangs on it.
2. **12** IBM: Harnesses in AI — twenty minutes; the same idea from a different speaker, with a tiny live build.
3. **03** Agent from scratch — each layer as code; 02 and 11 assume it.
4. **06** Context management — the layer that fails first in long tasks.
5. **04** Agent memory — context assembled over time.
6. **07** Skills — procedural memory and the skill layer.
7. **09** Sandboxing — the execution environment and blast radius.
8. **08** Evals — how to measure an agent; 11 uses its fingerprinting.
9. **02** Self-improving agents — the improvement loop and its first PR.
10. **11** The engineering behind a self-improving agent — why that PR was rejected and what the real fix took.
11. **05** Meta-harness design — part 1, the eight components.
12. **10** Meta-harness, 20 runs — part 2, seven failure modes in practice.

## The notes

| # | Note | Length | One line |
|---|---|---|---|
| 01 | [Harness engineering masterclass](01-harness-engineering-masterclass.md) | 28:06 | The eleven (later ten) harness primitives and the "ran out of road" chain. |
| 02 | [Self-improving agents](02-self-improving-agents.md) | 35:19 | Improve the harness, not the model: mining, held-out tasks, editable surface, human-merged PR. |
| 03 | [Agent from scratch](03-agent-from-scratch.md) | 34:11 | Carbon built in fifteen chapters, one primitive per git tag. |
| 04 | [Agent memory](04-agent-memory.md) | 27:18 | Four memory types, the context builder, conflicts as state, forgetting as hygiene. |
| 05 | [Meta-harness design](05-meta-harness-design.md) | 35:36 | Bhai's eight components; coordination moved out of the agents. |
| 06 | [Context management](06-context-management.md) | 35:38 | Select, compress, write, isolate, and prompt-cache stability. |
| 07 | [Skills masterclass](07-skills-masterclass.md) | 31:54 | Skills as tested, owned, progressively loaded procedures. |
| 08 | [Agent evals](08-agent-evals.md) | 37:18 | Six measures, code graders, calibrated judge, confident-wrong 11 → 0. |
| 09 | [Agent sandboxing](09-agent-sandboxing.md) | 35:59 | Five sandbox layers, blast radius, three boundaries. |
| 10 | [Meta-harness, 20 runs](10-meta-harness-20-runs.md) | 45:37 | Seven multi-agent failure modes and the component that catches each. |
| 11 | [Self-improving agent engineering](11-self-improving-agent-engineering.md) | 24:50 | From a bigger number to named output strategies; boundaries, evidence, isolation, promotion. |
| 12 | [IBM: harnesses deep dive](12-ibm-harnesses-deep-dive.md) | 20:26 | A browser agent that stops lying once the harness verifies from the trace. |

Cross-cutting files: [glossary](glossary.md) (every term with its source), [principles](principles.md) (P1–P50 and the disagreements), [diagram-spec](diagram-spec.md) (the master architecture for Excalidraw).

## Concept map: which video covers which concept

Bold marks the main video for the concept.

| Concept | Videos |
|---|---|
| Model vs runtime vs harness | **01**, 03, 12 |
| Instructions (`AGENTS.md`) | **01**, 03, 07, 08 |
| Context delivery | **01**, 03 |
| Context management: select, compress, write, isolate | **06**, 01, 03 |
| Prompt-cache stability | **06** |
| Compaction, head and tail, clamp | **06**, 03, 02, 11, 12 |
| Output strategies (clamp, head-tail, offload) | **11** |
| Memory: working, episodic, semantic, procedural | **04**, 03, 07 |
| Tool interface and registry | **01**, 03, 09, 12 |
| Tool tiers and fallback | **08** |
| Execution environment and sandbox layers | **09**, 03, 05 |
| Start closed, blast radius, three boundaries | **09**, 03 |
| Credentials held by the harness | **09**, 01, 12 |
| Run scratch space and file lifecycle | **11** |
| Durable state | **01**, 03, 05 |
| Orchestration and planning | **01**, 03 |
| Sub-agents and delegation | **01**, 03, 06 |
| Skills and progressive disclosure | **07**, 03 |
| Verification and receipts | **01**, 03, 12, 10 |
| Observability and tracing (OTel) | **03**, 06, 08, 10 |
| Guardrails and attempt loops | **12**, 10 |
| Eval vocabulary, pass@k / pass^k, LLM judge | **08** |
| Confident-wrong vs abstention | **08** |
| Fingerprinting and reproducible runs | **08**, 02, 10, 11 |
| Weakness mining, clusters, fix-type choice | **02** |
| Held-in / held-out, acceptance rule | **02**, 11 |
| Editable surface | **02**, **11** |
| Four properties: boundaries, evidence, isolation, promotion | **11** |
| Meta-harness components | **05**, 10 |
| Gates, output contracts, derive from git | **10** |
| Resume vs restart, durable execution | **10**, 05 |
| Observation vs control | **05**, 10 |
| Dynamic on-the-fly harnesses | **12** |

## For our options-research harness

Each note ends with a section on what it means for our options-research harness. The cross-cutting version is principles P1–P50: write the harness as named layers, hold credentials harness-side, derive results from files and git, fingerprint every backtest, and change the harness only through a declared editable surface with held-out checks and a human merge.
