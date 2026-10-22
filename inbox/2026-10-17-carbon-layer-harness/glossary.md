# Harness engineering — glossary

Every term in the vocabulary of The Carbon Layer's harness series (videos 01–11) and the IBM talk (12), with a one-line definition and the video that introduces or explains it. Speaker's own names are kept. Principles are in [principles](principles.md); the picture is in [diagram-spec](diagram-spec.md).

| Term | Definition | Source |
|---|---|---|
| Abstention | The agent declines ("could not find it") instead of guessing; the safe kind of wrong. | 08 |
| Acceptance rule | A candidate must be at least as good on held-in and held-out tasks and strictly better on one; else reject. | 02 |
| ACP (Agent Client Protocol) | A protocol for driving agents from a client; one of the harness types an adapter can wrap. | 05 |
| Adapter (harness adapter) | The only code that knows how to start and control one harness (SDK, CLI, HTTP, ACP) behind a common worker contract. | 05, 10 |
| Adapter (storage route) | One access route to a store for one tool, for example a logical reference for `read_file` or an environment variable for `bash`. | 11 |
| Agent | Model + harness + UI; everything that makes it feel like an agent is in the harness. | 03 |
| Agent harness | The system around the model that decides what it sees, can do, remembers, delegates, and how work is checked; "grounding in reality" in IBM's terms. | 01, 12 |
| Agent package | A versioned folder that defines a reusable worker: harness, model, instructions, tools, contract, limits. | 05, 10 |
| Agent package registry | The catalogue of agent packages; stamps the worker identity on every step. | 05, 10 |
| Agentic loop / runtime | The loop in which the model reasons, acts, observes and repeats. | 01, 03, 12 |
| Agentic software factory | His long-term picture: a catalogue of versioned SDLC blueprints run by a meta-harness. | 05 |
| Agents as tools | A manager agent calls specialists as tools and keeps control (OpenAI SDK pattern). | 01 |
| `AGENTS.md` / `CLAUDE.md` | Instruction files the harness loads into the prompt; semantic memory in the memory map. | 01, 03, 04 |
| Approval fatigue | People approve by reflex after many small prompts, so frequent approvals stop being security. | 09 |
| Approval gate | A pause where a human (or policy) must allow a risky call; fails closed with no approver. | 03, 05 |
| AReaL | A paper on self-evolving agents; source of "choose the right kind of fix", "explain or drift", rollback as first class. | 02 |
| Artifact lineage | The chain linking each artifact to what produced and reviewed it (commit A → reviews at A → revision B). | 05 |
| Attempt loop | An outer loop that reruns a step or a whole harness attempt up to a cap. | 10, 12 |
| Bash adapter | The environment-variable route that lets `bash` reach the run scratch store. | 11 |
| Behaviour drift | A score moves because a layer you did not touch changed (harness release, model alias). | 08 |
| Behaviour-focused testing | System-level tests on real examples that check what the agent does, not only unit behaviour. | 11 |
| Bhai | "Blueprint Harness for AI", his meta-harness. | 05, 10 |
| Binder (role and policy binder) | Resolves a role to a package and computes the effective worker under the policy ceiling; gates each tool call. | 05, 10 |
| Blast radius | How much damage an action can do if it goes wrong; the basis for choosing a boundary. | 03, 09 |
| Blueprint | A versioned workflow file the runtime reads and executes. | 05, 10 |
| Boundaries / Evidence / Isolation / Promotion | The four properties a self-improving loop needs from the delivery system around it. | 11 |
| Bubblewrap / Landlock / seccomp / Seatbelt | OS-level sandbox mechanisms (Linux namespaces, path rules, syscall filter; macOS). | 09 |
| Candidate | A proposed result or change that a gate or acceptance rule must check before it advances. | 02, 05, 10 |
| Candidate runner | Applies one candidate to a marked working copy, runs the full suite, then reverts. | 02 |
| Capability description | What a harness supports (streaming, cancel, resume, pause, structured output), so workflows assume nothing. | 05 |
| Capability mismatch | A strong proposer suggests a fix too clever for the weak model to follow. | 02 |
| Carbon | The series' teaching agent, built from scratch one primitive per chapter. | 03 |
| Category split | Scores reported per question category, which exposes weak areas an aggregate hides. | 08 |
| Clamp | Cut a tool output to the first N characters. | 02, 03, 11 |
| Clash | Facts in the window contradict each other. | 06 |
| Cluster | A group of failures with one provable shared cause. | 02 |
| CoALA | The paper that maps the four cognitive memory types onto language agents. | 04 |
| Compaction / compress | Summarise older history to free the window; lossy and itself a model call. | 01, 03, 06 |
| Confident hallucination | A wrong answer stated as fact; the dangerous kind of wrong. | 08 |
| Confusion | Irrelevant material in the window degrades the answer. | 06 |
| Consolidator | A worker that merges overlapping review findings while keeping lineage. | 05 |
| Context builder | The harness part that retrieves, ranks, resolves and assembles each turn's prompt. | 04 |
| Context delivery | Giving the model the material it needs (files, tests, traces), for example by `@path`. | 01, 03 |
| Context management | Deciding what reaches the model on this turn, to protect a finite attention budget. | 01, 06 |
| Context readout | A view of what the window actually holds, section by section. | 06 |
| Contextual policies | Authority that changes with history (Omnigent); a risky earlier action makes a later one need approval. | 05 |
| Contradiction handling | A new fact updates current state and the old one is kept as history. | 04 |
| Control plane | The explicit path to cancel, approve, pause, steer or replace a worker. | 05, 10 |
| CrikIT | His cricket-league app and domain agent, used for memory and eval examples. | 04, 08 |
| Dataset / item / metric / score / runs over time | The five words of the eval vocabulary. | 08 |
| Delegation problem (parallel inconsistency) | Each sub-agent invents its own process, so parallel results disagree. | 01 |
| Derive the candidate | The adapter reads the result from git after the worker exits instead of trusting the worker's report. | 10 |
| Distraction | The context is so long that the model leans on it instead of its training. | 06 |
| Domain agent | A narrow agent with definable correct behaviour, so it can be measured. | 08 |
| Durable execution | Reuse valid stored step results after a failure instead of redoing them; needs idempotency. | 05 |
| Durable state | The workbench that survives the turn: plans, checkpoints, logs, diffs, memory stores. | 01, 03 |
| Dynamic (on-the-fly) harness | IBM's forecast: an agent builds its own harness before doing a task. | 12 |
| Editable surface | A short, named, versioned list of what an improver may change. | 02, 11 |
| Effective configuration | Package + role + tool profile + workspace mode, serialised and hashed per step. | 10 |
| Episodic memory | What happened and when: timestamped session records. | 04 |
| Episodic / session search | A tool that searches stored past sessions by keyword or full text. | 03, 04, 06 |
| Event stream (event and control plane) | One append-only record of every boundary, gate and worker event, feeding all views. | 05, 10 |
| Evolution (of the harness) | Turning each failure into infrastructure so the same class finds it harder to return. | 01 |
| Execution environment | Where a tool call becomes bounded reality: file scope, network, credentials, sandbox. | 01, 05 |
| Experience metric | Persona, clarity, admitting gaps, asking for clarification. | 08 |
| Explain or drift | A self-evolving system that cannot explain its change is drifting, not improving. | 02 |
| Fallback (guarded fallback / escape hatch) | A generic tool where the model writes its own query; useful but invites over-trying. | 08 |
| Fallback log (shopping list) | Questions that keep falling back and failing; the next deterministic tools to build. | 08 |
| Fault injection | Force a tool to fail or return empty to test recovery. | 08 |
| Filing cabinet and desk | Durable stores (cabinet) versus the working window (desk); the model only works at the desk. | 04 |
| Fingerprint | Hashes and ids (harness, loop, model, config, dataset, environment) stamped on a run or file. | 02, 08, 11 |
| Five-level ladder | Weng's levels of self-improvement: prompt, context, workflow, harness code, the improver itself. | 02 |
| Forgetting strategies | Temporal decay, contradiction handling, compression, manual curation. | 04 |
| Frozen model | The weights never change; improvement happens around the model. | 02 |
| Gate | A deterministic check the worker cannot see, call or skip; on failure the run stops. | 10 |
| Gold answer | The correct answer, computed by the same deterministic functions the tools use. | 08 |
| Guardrails | Composable limits such as max steps or max messages that kill or compress a run. | 12 |
| gVisor (Sentry) | A user-space kernel that handles most syscalls for a sandboxed process. | 09 |
| Handoff | The conversation moves to a specialist agent (OpenAI SDK pattern). | 01 |
| Harness handler | Deterministic harness code that clears a known obstacle (for example login) using secrets the model never sees. | 12 |
| Head and tail | Keep the start and the end of an output or history; drop or summarise the middle. | 03, 11 |
| Held-in / held-out | Tasks shown to the fixer versus tasks hidden from it. | 02 |
| Held-out leakage | Using held-out tasks to choose candidates slowly leaks them; retire and replace them. | 02 |
| Hermes | An agent cited for session search, memory files and skills. | 01, 04, 06 |
| Human handoff | The terminal step where the workflow stops in "pending" for a person. | 05, 10 |
| Instantiation event | An event emitted before a worker starts, carrying its hashed effective configuration. | 10 |
| Instructions | Standing guidance (system prompt, `AGENTS.md`); passive, cannot discover or inspect. | 01, 03, 07 |
| Intake and activation | Maps an incoming event (GitHub, CI, schedule) to a versioned blueprint and creates a run. | 05 |
| Intent versus containment | What you ask the model to do versus what holds when it does something else. | 03, 09 |
| Intentional compaction | Dex Horthy's practice: research file, plan file, fresh window per implementation step. | 06 |
| Isolate | Give a sub-task its own window and bring back only the result. | 06 |
| Lethal trifecta | Willison's term (cited): secrets plus untrusted input plus an exit path make exfiltration possible. | 09 |
| Lifecycle design question | Who creates, names, reads, exposes, cleans up and shares a harness-created file. | 11 |
| Lifecycle manager (worker) | Owns worker identity, state machine, heartbeats, timeouts, cancellation, retry and resume. | 05 |
| LLM judge (calibrated) | A model that grades fuzzy criteria, trusted only after agreement with human labels (kappa). | 08 |
| Logical reference | A stable name for a scratch file that `read_file` resolves inside the current run. | 11 |
| Long-horizon chain (weighted checkpoints) | A multi-step question graded with partial credit per step to locate the break. | 08 |
| Loop engineering | Weng's name for improving an agent by improving the loop around a frozen model. | 02 |
| Lost in the middle | Models use the start and end of a long context well and the middle poorly. | 06 |
| MCP (Model Context Protocol) | A standard way to expose tools to a model. | 01 |
| Memory | The harness deciding what to keep, recall, update and forget across turns and sessions. | 04 |
| Meta-harness | A layer above agent harnesses that coordinates harnessed agents as workers. | 05, 10 |
| Micro-VM (Firecracker) | A small virtual machine with its own guest kernel; isolation sized for tenants. | 09 |
| Miners versus regression guards | Tasks expected to fail (to find gaps) versus tasks expected to pass (to catch breakage). | 02 |
| Model | The reasoning engine: prompt in, text out; knows only training data and the prompt. | 01, 03 |
| Mutation testing | Change the code on purpose to see whether the tests catch it. | 11 |
| Non-trigger | The part of a skill that says when not to load it. | 07 |
| Observability | The recorder: traces, tool timelines, cost, latency, versions, approval events. | 01, 03 |
| Observation versus control | Seeing a problem and being able to stop or steer it are separate capabilities. | 05, 10 |
| Offload strategy | Write the full tool output to a file and give the model a compact reference. | 11 |
| One emit, many sinks | The tracer emits each event once; UI, JSONL, console and OTel consume it. | 03, 10 |
| OpenTelemetry (OTel) | The open tracing standard used so traces can go to any backend. | 03, 06, 10 |
| Orchestration | How work moves: hooks, retries, approval gates, step order, routing; the model plans, the harness drives. | 01, 03 |
| Output contract | One fenced JSON block per answer, validated against the role's declared shape. | 10 |
| Paired confirmation | Rerun the candidate side by side with a fresh baseline; it must win every pair with no regression. | 11 |
| pass@k / pass^k | Right at least once in k tries versus right on all k tries; the gap is flakiness. | 08 |
| Pass fraction | The share of repeated runs a task passes (for example 2/3). | 02 |
| Pi | A minimal agent harness that influenced Carbon. | 01, 03, 11 |
| Poisoning | A wrong fact enters the window and is later treated as true. | 06 |
| Policy ceiling (organisational) | The upper limit on authority; roles can only narrow it. | 05 |
| Primitive | One named harness layer; his teaching unit (not an agreed standard). | 01 |
| Procedural memory | How work gets done: runbooks, skills, tool schemas, orchestration code. | 04, 07 |
| Progressive disclosure | Load only skill descriptions first; read bodies and child files on demand. | 03, 07 |
| Prompt-cache stability (stable prefix) | Keep the early prompt identical so the provider's cache discount holds. | 06 |
| Proof and learning | The tenth primitive in the later count: verification, observability and evolution together. | 07 |
| Propose, validate, confirm, accept | The promotion path for a change to the editable surface. | 11 |
| Proposer versus patient | A stronger external model diagnoses and proposes; the weak model under test stays frozen. | 02 |
| Reachability problem | Moving a file outside the tool root makes it safe but unreachable. | 11 |
| Recovery count | The share of targeted test cases where the model retrieved the answer from the offloaded file. | 11 |
| Refinery | The series' self-improvement loop around Carbon. | 02, 11 |
| Replay checks | Six checks that a stored step result is still valid before resume reuses it. | 10 |
| Research, plan, implement | A three-phase workflow where each phase writes a file and the next starts fresh. | 06 |
| Resume versus restart | Reuse stored completed steps versus rerun everything. | 05, 10 |
| Revision cap | The maximum number of revise rounds, enforced in code. | 05, 10 |
| Role | A job in a workflow: purpose, allowed actions, required answer shape. | 05, 10 |
| Rollback (first class) | Undoing a change is a normal operation, not an emergency. | 02 |
| Run scratch space | A private directory per run, created and deleted by the harness, also on failure. | 11 |
| Runner | Runs one step: dispatches to a worker, counts attempts, writes the artifact. | 10 |
| Sandbox stack | Five isolation layers: runtime isolate/WASM, OS sandbox, container, user-space kernel, micro-VM. | 09 |
| Second persistent surface | A harness-made copy of sensitive bytes that outlives the run. | 11 |
| Select | Pull only the slice this turn needs, and place it well. | 06 |
| Self-Harness | A paper on self-improving harnesses; source of weakness mining, held-in/held-out and the acceptance rule. | 02 |
| Semantic memory | Standing facts free of time: user facts, conventions, current state. | 04 |
| Session boundary | A new session starts with nothing; memory must be rebuilt by the harness. | 04 |
| Skill | A reusable procedure loaded when a recurring class of work appears. | 03, 07 |
| Skill creator | A skill that drafts new skills, to be reviewed like code. | 07 |
| Source map / confidence table | Durable state for research work: sources, extracted quotes, confidence levels. | 01 |
| Stale procedure | A runbook or skill that no longer matches reality but still sounds official. | 04, 07 |
| Start closed | No network, scoped writes and no credentials until configuration grants them. | 03, 09 |
| State and artifact store | Holds workflow state and artifacts with lineage. | 05, 10 |
| Strategy pattern | Each output-handling behaviour is a module selected by configuration. | 11 |
| Sub-agent | A model with a narrower job, context and tool set that returns a reply to the parent. | 01, 03 |
| Supervisor agent | A lead model that coordinates others; legitimate, but puts a model in the control path. | 05 |
| System call path | The route of a file read through the kernel, where sandbox policy acts. | 09 |
| Temporal decay | Older memories lose priority unless pinned or recently used. | 04 |
| Temporal knowledge graph | A store that records when each fact was true. | 04 |
| Terminal state | The final state of a workflow; forced to "pending" for human approval. | 10 |
| Three boundaries | What the model can call (registry), what tools can reach (credentials), where execution touches (sandbox). | 09 |
| Tier (tool tier) | A label on each tool: deterministic domain tool or fallback. | 08 |
| Tool interface | Tools as name, description, input schema and often output schema. | 01, 03, 12 |
| Tool registry | The set of tools the model may call. | 03, 09, 12 |
| Tool selection / retrieval | Choosing which tools to expose this turn; retrieve them like documents at scale. | 06 |
| Trace | The recorded history of model calls, tool calls and results for a run. | 03, 12 |
| Trajectory | The path the agent took (which tools, in which order), as opposed to the outcome. | 08 |
| Verification | Asking for receipts: tests, builds, type checks, screenshots, evals. | 01, 03, 12 |
| Verify step | IBM's deterministic check that reads the trace after an attempt. | 12 |
| Weakness mining | Run the agent, collect failures, and group those with one shared cause. | 02 |
| Worker contract | The common interface every adapter exposes to the meta-harness. | 05 |
| Workflow engine | Runs a blueprint: sequence, fan-out, join, conditions, bounded loops, gates. | 05, 10 |
| Working memory | The active context window this turn; a budget, not persistence. | 04 |
| Workspace | The directory an agent owns, to which its tools are rooted. | 03, 11 |
| Write | Move what you cannot afford to lose out of the window into a file on disk. | 06 |
