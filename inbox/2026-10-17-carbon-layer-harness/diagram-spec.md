promoted: 2026-10-23
# Harness engineering — master diagram spec (Excalidraw-ready)

The master architecture that the series builds across videos 01–11, with the IBM talk (12) folded in where it agrees. Draw it as five horizontal bands, top to bottom. Each node has an id, a name, what it does, its inputs and outputs, and its source videos. Edges follow, grouped by layer. Terms are in [glossary](glossary.md); the reasons behind each box are in [principles](principles.md).

## Layout and style

- **Canvas:** about 3200 × 2400 px. Five bands, each a large rectangle frame with its name in the top-left corner.
- **Band order (top to bottom):** L0 Intake → L1 Meta-harness → L2 Agent harness (largest band, about half the height) → L3 Proof → L4 Evolution.
- **Colours (one per band):** L0 grey, L1 blue, L2 green, L3 orange, L4 purple. Boundary overlays in red dashed lines.
- **Shapes:** process = rectangle; store = cylinder; decision or gate = diamond; human = rounded rectangle with a person icon; external model = ellipse.
- **Arrows:** solid = data or control flow; dashed = event or trace emission; red = boundary crossing that needs a capability or approval.
- **Draw order for teaching:** build L2 first (it is video 01's picture), then wrap L1 around it, then add L3 and L4 below, then the red overlays.

## L0 — Intake (video 05)

| Id | Node | What it does | Inputs | Outputs |
|---|---|---|---|---|
| N01 | Sources | Places where work comes from: GitHub, Jira, CI, schedule, API. | External events | Raw events |
| N02 | Intake and activation | Validates and deduplicates an event, picks a blueprint, creates a run. | Raw events, blueprint catalogue | Run record, chosen blueprint |
| N03 | Blueprint catalogue | Holds versioned workflow files. | Authored blueprints | Blueprint by name and version |

## L1 — Meta-harness (videos 05, 10)

| Id | Node | What it does | Inputs | Outputs |
|---|---|---|---|---|
| N04 | Workflow engine | Walks the blueprint: sequence, fan-out, join, conditions, bounded loops, gates, caps, failure paths. | Blueprint, run record, step results, events | Step requests, gate decisions, terminal state |
| N05 | Agent package registry | Stores versioned worker packages; stamps identity on each step. | Package folders | Package definition and fingerprint |
| N06 | Role and policy binder | Binds a role to a package; computes the effective configuration; gates each tool call. | Step request, package, policy ceiling | Hashed effective configuration, allow/deny per call |
| N07 | Organisation policy ceiling | The upper limit on any worker's authority. | Policy files | Limits to the binder |
| N08 | Worker lifecycle manager | Starts, times out, cancels, retries and resumes workers; enforces budgets. | Effective configuration, control commands | Worker sessions, lifecycle events |
| N09 | Harness adapter layer | One adapter per harness behind a common worker contract; derives the candidate from git after exit. | Start/stop commands, task contract | Worker results, instantiation events |
| N10 | Execution environment manager | Creates the worktree or clone, path rules, network rules, secret delivery, resource limits per role. | Effective configuration | An isolated environment per worker |
| N11 | State and artifact store | Keeps workflow state and artifacts with lineage; serves valid results on resume. | Results, transitions, human decisions | Stored artifacts, replay-checked results |
| N12 | Event and control plane | One append-only event stream; feeds views; carries control commands back. | Events from N04, N08, N09, N06 | Traces, metrics, UI, approvals; cancel/approve/steer |
| N13 | Human handoff | The final gate; status forced to pending; nothing merged or pushed. | Consolidated package with lineage and known limits | Human decision |
| N14 | Workflow gate (deterministic checks) | Checks a worker's claim against ground truth: commit exists, descends from base, files match diff, test artifact exists, no remote. | Candidate, git | Pass, or failed run |
| N15 | Output contract | Extracts one JSON block and validates its shape inside the attempt loop. | Raw worker output | Valid result, or failed attempt |

## L2 — Agent harness, one worker (videos 01, 03, 04, 06, 07, 09, 11, 12)

| Id | Node | What it does | Inputs | Outputs |
|---|---|---|---|---|
| N16 | UI | Shows conversation and live trace; hosts approvals; consumes events, never owns them. | Events, user messages | User messages, approval answers |
| N17 | Instructions | System prompt and `AGENTS.md`: identity, rules, conventions. | Files | Stable prefix text |
| N18 | Context delivery | Reads referenced files, tests and logs on request. | `@path` references | File contents |
| N19 | Memory stores | Episodic (session JSONL), semantic (fact files), procedural (skills, schemas, orchestration). | Saved turns, facts, procedures | Candidate items for the builder |
| N20 | Context builder | Select, rank, resolve conflicts by time, assemble the turn's prompt. | N17, N18, N19, N27 descriptions, history | Assembled window |
| N21 | Context window | Stable cached prefix plus a moving tail; the model's only view. | Assembled window, tool results | Prompt to the model |
| N22 | Compactor | Summarises the middle of history; keeps head and tail; trigger and prompt are designed. | Window near its limit | Shorter window |
| N23 | Model | Reasons and chooses a reply or tool call. | Prompt | Text or tool call with arguments |
| N24 | Agent loop | Reason, act, observe, repeat, with max steps. | Model output, tool results | Next prompt, final reply |
| N25 | Tool registry | Named tools with schemas and tiers (domain or fallback); validates arguments. | Tool call | Validated call |
| N26 | Tool-call gate | Approval for boundary-crossing calls; binder callback; fails closed. | Validated call, policy | Allowed or denied call |
| N27 | Skills library | Skill descriptions in the prompt; bodies and child files read on demand. | Skill folders | Procedures |
| N28 | Execution sandbox | Runs the call start-closed; covers child processes. | Allowed call | Raw tool output |
| N29 | Credential holder | Holds keys; performs sensitive steps harness-side. | Secrets, handler requests | Completed actions, never key text |
| N30 | Harness handlers | Deterministic code for known obstacles (login, vendor errors); posts a harness message. | Environment state each turn | Fixed state, a note to the model |
| N31 | Output strategy selector | Clamp, head and tail, or offload, set on the editable surface. | Raw tool output, config | Context slice or reference |
| N32 | Run scratch store | Private per-run directory; created and deleted by the harness, also on failure. | Offloaded bytes, lifecycle commands | Bytes via `read_file` or `bash` adapter |
| N33 | Orchestrator | Model plans steps as JSON; harness gates, executes and retries each. | Plan | Step calls into the loop |
| N34 | Sub-agents | Fresh loops with narrower context, tools and the same skill; `delegate` and `fan_out`. | Sub-task | One reply each |
| N35 | Verifier | Refuses "done" until a receipt exists, read from ground truth or the trace. | Trace, files, exit codes | Pass, or back to the loop |
| N36 | Tracer | Spans for model calls, tool calls, plan and verify steps; tokens, latency, cost, labels. | Every step | Events to sinks (JSONL, UI, OTel) |
| N37 | Attempt loop | Outer loop of whole attempts with a hard cap (IBM). | Verifier result | Retry or honest failure |

## L3 — Proof (videos 08, 10, 11)

| Id | Node | What it does | Inputs | Outputs |
|---|---|---|---|---|
| N38 | Eval dataset | Items with category, expected tool and a computed gold answer. | Real questions, deterministic functions | Items |
| N39 | Eval runner | Runs each item k times; injects faults. | Items, agent build | Answers, traces |
| N40 | Code graders | Match against gold, right tool, cost, answer block present. | Answers, traces, gold | Scores |
| N41 | LLM judge | Small remit, yes/no/unknown criteria; calibrated against human labels. | Answers, labels | Experience scores, agreement |
| N42 | Fingerprinted results file | Scores keyed by harness, loop, model, config, dataset and environment. | Scores, fingerprints | Comparable record |
| N43 | Runs-over-time board | Per-task and per-category trends; pass@k, pass^k; confident-wrong versus abstention. | Results files | Decisions on what to fix |
| N44 | Fallback log | Questions that keep falling back and failing. | Tier labels in traces | Next deterministic tools |

## L4 — Evolution (videos 01, 02, 07, 11)

| Id | Node | What it does | Inputs | Outputs |
|---|---|---|---|---|
| N45 | Weakness miner | Groups failures with one provable cause into clusters; parks noise. | Traces, results | Clusters |
| N46 | Fix-type router | Missing fact → memory; plumbing → harness; everywhere → model; recurring procedure → skill. | Cluster | Fix target |
| N47 | Editable surface | Versioned config of allowed knobs and named strategies, schema-validated. | Accepted changes | Harness configuration |
| N48 | Proposer model | A stronger external model writes candidate edits only to the surface. | Held-in failing trace, surface schema | Candidates with risk notes |
| N49 | Held-in / held-out split | Shown tasks versus hidden tasks; answer keys fingerprinted and out of the proposer's reach. | Suite | Two task sets |
| N50 | Candidate runner | Applies one candidate to a marked copy, runs the full suite, reverts. | Candidate, suite | Per-task pass fractions |
| N51 | Acceptance and paired confirmation | No worse anywhere, better somewhere; then paired runs against a fresh baseline. | Pass fractions, baseline | Accepted candidate or rejection |
| N52 | Pull request and human review | The change waits for a person with a per-task table. | Accepted candidate | Merge, or no merge |
| N53 | Rollback | Undo is a normal operation. | Merged change | Previous configuration |

## Edges

### L0 → L1

| Id | From → To | What flows |
|---|---|---|
| E01 | N01 → N02 | Raw event (repo, base commit, request, acceptance criteria) |
| E02 | N03 → N02 | Blueprint by name and version |
| E03 | N02 → N04 | Run record and blueprint |

### L1 — Meta-harness

| Id | From → To | What flows |
|---|---|---|
| E04 | N04 → N06 | Step request with role |
| E05 | N05 → N06 | Package definition and fingerprint |
| E06 | N07 → N06 | Authority ceiling |
| E07 | N06 → N08 | Hashed effective configuration |
| E08 | N06 → N10 | Environment policy for the role |
| E09 | N10 → N09 | Isolated environment handle (worktree, read-only clone, no repo) |
| E10 | N08 → N09 | Start, cancel, resume commands; budgets |
| E11 | N09 → L2 (N24) | Task contract into a worker's agent loop |
| E12 | L2 (N24) → N15 | Raw worker output |
| E13 | N15 → N08 | Failed attempt (retry within budget) |
| E14 | N09 → N14 | Candidate derived from git |
| E15 | N14 → N04 | Pass, or stop the run |
| E16 | N04 → N11 | Transitions, pending gates, human decisions |
| E17 | N09 → N11 | Artifacts with lineage |
| E18 | N11 → N04 | Replay-checked results on resume |
| E19 | N04, N06, N08, N09 → N12 (dashed) | Events (started, denied, timed out, completed) |
| E20 | N12 → N08 (red) | Control: cancel, approve, pause, steer |
| E21 | N04 → N13 | Consolidated package, status pending |
| E22 | N06 → N26 | Per-call allow/deny callback |

### L2 — Agent harness

| Id | From → To | What flows |
|---|---|---|
| E23 | N16 → N24 | User message |
| E24 | N17 → N20 | Instructions for the stable prefix |
| E25 | N18 → N20 | Delivered file contents |
| E26 | N19 → N20 | Candidate memories with timestamps |
| E27 | N27 → N20 | Skill descriptions (bodies on demand) |
| E28 | N20 → N21 | Assembled window |
| E29 | N22 ↔ N21 | Compaction of the middle |
| E30 | N21 → N23 | Prompt |
| E31 | N23 → N24 | Reply or tool call |
| E32 | N24 → N25 | Tool call with arguments |
| E33 | N25 → N26 | Validated call |
| E34 | N26 → N16 (red) | Approval request for boundary-crossing calls |
| E35 | N26 → N28 | Allowed call |
| E36 | N29 → N28 / N30 | Harness-side use of secrets (never into the window) |
| E37 | N28 → N31 | Raw tool output |
| E38 | N31 → N21 | Clamped or head-and-tail slice, or compact reference |
| E39 | N31 → N32 | Full bytes (offload) |
| E40 | N32 → N28 | Bytes back through the `read_file` or `bash` adapter |
| E41 | N30 → N21 | Harness message after a fixed obstacle |
| E42 | N24 ↔ N19 | Save each turn; search past sessions |
| E43 | N33 → N24 | One planned step at a time |
| E44 | N24 → N34 → N24 | Sub-task out, one reply back |
| E45 | N27 → N34 | Same skill to every sub-agent |
| E46 | N24 → N35 | Claimed "done" |
| E47 | N35 → N24 / N37 | Pass, or continue / retry the attempt |
| E48 | all L2 nodes → N36 (dashed) | Spans with labels |
| E49 | N36 → N16 and N12 (dashed) | Events to UI and meta-harness stream |

### L2 → L3 → L4 (proof and learning)

| Id | From → To | What flows |
|---|---|---|
| E50 | N38 → N39 | Items |
| E51 | N39 → L2 (N24) | Questions, k times, with injected faults |
| E52 | N36 → N40 / N44 | Traces with tier and empty labels |
| E53 | N39 → N40, N41 | Answers with JSON answer block |
| E54 | N40, N41 → N42 | Scores plus fingerprints |
| E55 | N42 → N43 | Comparable results over time |
| E56 | N43, N36 → N45 | Failing traces |
| E57 | N45 → N46 | Clusters |
| E58 | N46 → N19 / N27 / N47 | Fix lands in memory, a skill, or the editable surface |
| E59 | N49 → N48 | Held-in failing traces only |
| E60 | N48 → N50 | Candidate edits |
| E61 | N49 → N50 | Both task sets (keys out of the proposer's reach) |
| E62 | N50 → N51 | Per-task pass fractions |
| E63 | N51 → N52 | Accepted candidate and per-task table |
| E64 | N52 → N47 | Merged configuration |
| E65 | N47 → N31 and other L2 knobs | Live strategy settings |
| E66 | N53 → N47 (red) | Revert |

## Red overlays

1. **Three boundaries (video 09):** three concentric dashed rings around N23: tool registry (N25), credentials (N29), sandbox (N28). The approval gate N26 sits on the arrow that crosses the outer ring.
2. **Project root boundary (video 11):** a dashed box around the workspace and project tools; N32 sits outside it, reached only by E40.
3. **Seven failure markers (video 10):** red dots with labels on N14 (false work), N05 (which worker ran), N15 (bad output and stalls), N06/N10 (authority), N11 (partial fan-out failure), N04 (no convergence), N12 (cannot see it).
4. **Four properties (video 11):** labels on L4's frame: Boundaries at N47, Evidence at N42, Isolation at N32, Promotion at N52 and N53.

## Where to read each part

- L2 core: [01](01-harness-engineering-masterclass.md), [03](03-agent-from-scratch.md), [12](12-ibm-harnesses-deep-dive.md). Context and memory nodes: [06](06-context-management.md), [04](04-agent-memory.md). Skills: [07](07-skills-masterclass.md). Sandbox and credentials: [09](09-agent-sandboxing.md). Output strategies and scratch: [11](11-self-improving-agent-engineering.md).
- L1: [05](05-meta-harness-design.md), [10](10-meta-harness-20-runs.md). L3: [08](08-agent-evals.md). L4: [02](02-self-improving-agents.md), [11](11-self-improving-agent-engineering.md).
