# 05 — Meta-Harness: Designing Multi-Agent AI Systems

- **Title:** Meta-Harness | Designing Multi-Agent AI Systems
- **Channel:** The Carbon Layer (Ankit Desai)
- **Id / link:** `HRUBDPdvaHU` — https://www.youtube.com/watch?v=HRUBDPdvaHU
- **Length:** 35:36
- **Article edition:** https://thecarbonlayer.com/meta-harness/
- **Source of these notes:** yt-dlp hit HTTP 429; transcript from Firecrawl's YouTube scrape, read in full.
- **Part 1 of 2.** Part 2 (the build and 20 runs) is video 10.

## Core thesis

He runs several coding agents (one implements, others review) and finds that he has become "the glue": he decides who runs next, copies artifacts, tracks which commit each reviewer saw, handles failures, enforces revision limits. A **meta-harness** sits one level above agent harnesses and coordinates several harnessed agents as **workers**. Thesis to test: a meta-harness **moves coordination outside the agents**, so the system does not depend on one supervisor model behaving perfectly. If a weak worker goes off track, times out, ignores an instruction, or returns the wrong shape, the outer system contains it.

## The running workflow

His meta-harness is **Bhai** ("Blueprint Harness for AI"). Each workflow is a **versioned blueprint**; a source (GitHub, Jira, CI, schedule, API) triggers it. The example blueprint: an **implementer** changes code → two **reviewers** in parallel (correctness, security; possibly on different harnesses) → a **consolidator** merges overlapping findings → if a blocker remains, the implementer gets **one** controlled revision → stop for a **human**.

## Requirements he writes first

- **Functional:** accept work from many sources and pick the versioned workflow; run agents on different harnesses; independent instructions and context per worker; sequence and run concurrently; exchange structured artifacts; per-role permissions; start, stop, cancel, time out, retry, resume; preserve progress when a branch fails; track which worker produced or reviewed each artifact; stop for human approval.
- **Non-functional:** extensibility across harnesses, reproducibility, least privilege, failure containment, observability, bounded cost and execution, and **no dependency on one supervisor model** carrying the process in its context. That last one shapes the design.

## Why a supervisor agent is not enough

A lead agent with sub-agents is legitimate (Anthropic's multi-agent research system; Databricks Omnigent's **Polly** supervisor). But the supervisor becomes part of the **control path**: it must remember finished branches, enforce revision counts, preserve artifacts, handle failures, decide human gates. Some of that is **judgment**; much is **bookkeeping and policy**. He trusts a model to judge whether two findings are the same bug, not to remember that the security reviewer timed out and the revision limit is one. Rules are easier to inspect and test outside the model. Supervisors can still be used inside steps where judgment helps.

## The eight components (each added when the simple script breaks)

Start: a plain Python script calling `run(carbon, task)` then two reviews in parallel. It hides worker definitions in functions; next week you cannot say which model or instructions ran.

1. **Agent package registry.** Each reusable worker is an inspectable, versioned package (a folder): harness, default model, base instructions, tools and skills, input/output contract, environment needs, resource limits. A workflow says "carbon reviewer v1". Answers: *what worker is available, and can I reproduce it?*
2. **Harness adapter layer.** A common **worker contract** over SDKs, CLIs (Codex headless), HTTP, streaming, ACP (Agent Client Protocol). Plus a **capability description** (for example streaming true, cancel false, resume true, pause false, structured output true) so a workflow never assumes a feature the harness lacks. Answers: *how do we invoke and control different harnesses through one contract?*
3. **Role and policy binder.** The same package can be implementer, read-only reviewer, or consolidator with no repo. Effective worker = package defaults + workflow role + task artifacts + runtime policy + **organizational policy ceiling**. Authority only **narrows** as it moves down; a role may never expand beyond the limit above it. Answers: *what is this worker expected and allowed to do here?*
4. **Workflow engine.** Sequence, fan-out, join, conditions, bounded loops, failure paths, human gates. He prefers **code over YAML**: once YAML gains parallel/map/retry expressions "we are slowly building a programming language with worse debugging". Agents judge *inside* steps; code controls the **transitions**. Guarantees (both reviews before consolidation, one revision, final state awaiting human, never merged) no longer depend on a model remembering them.
5. **Worker lifecycle manager.** Identity and a state machine (pending, running, completed, failed, cancelled, paused; retry, resume). Owns worker and session IDs, heartbeats, timeouts, cancellation. Records which recovery mode occurred (resume session vs replacement from a checkpoint). Enforces bounds that do not belong in prompts: max duration, attempts, cost, revision rounds. "Asking the model to stop after 10 minutes is not a timeout implementation."
6. **Execution environment manager.** Makes policy real: workspace or git worktree, writable vs read-only paths, network rules, credential and secret delivery, sandbox choice, CPU/memory/disk limits, local vs remote. Example: implementer gets a writable checkout; reviewers get clean read-only views of the same commit; the consolidator gets review artifacts and no repo; nobody gets merge or deploy credentials. A planning agent must not inherit the developer's push rights just because it runs on the same laptop. Omnigent's **contextual policies** change authority with history (downloading a new package can make a later `git push` need approval).
7. **State and artifact store.** Two things: **workflow state** (runs, worker runs, attempts, transitions, pending gates, human decisions) and **artifacts** (task, commits, diffs, reviews, tests, checkpoints) with **lineage** (candidate at commit A → reviews at A → consolidated findings → candidate at commit B). Lineage answers what a transcript cannot: which commit each reviewer saw, whether the revision was re-reviewed. **Durable execution** reuses valid stored results instead of redoing work, which needs **idempotency**, checkpoints, and clear ownership of side effects (a commit made before contact was lost; a PR opened but no completion event). Keep apart "progress was recorded" and "workflows can resume safely".
8. **Event and control plane.** Events: workflow started, worker started, tool called, artifact created, policy denied, approval requested, worker timed out, workflow completed. Consumers: logs and traces, metrics and cost, UI, policy evaluation, approvals, future observer agents. **Observation and control are different capabilities**: seeing a wrong tool call does not let you pause, inject guidance and resume; that needs an explicit control path (cancel, approve/deny, pause, provide a decision, inspect, steer or replace).

Plus, shown as designed but not built: **intake and activation** (source adapters, trigger bindings, deduplication) that maps an event to a versioned blueprint.

## The master diagram to redraw

1. Left: **Sources** (GitHub, Jira, CI webhook, schedule, API) → **Intake & activation** → selects a **versioned blueprint**.
2. Centre: **Workflow engine** running the blueprint.
3. Engine → **Role & policy binder**, which reads the **Agent package registry** and the **org policy ceiling**.
4. Binder → **Lifecycle manager** → **Harness adapter layer** → workers on different harnesses (Carbon via SDK, Codex via CLI, ACP agents).
5. **Execution environment manager** draws a boundary box around each worker (worktree, paths, network, secrets, limits).
6. Every component writes to the **State & artifact store** (workflow state + artifact lineage graph).
7. Every component emits to the **Event & control plane**, which feeds traces, metrics, UI, approvals; control arrows go back to lifecycle and adapters.
8. Right: **Human handoff** gate at the end.

Seams overlap; ownership is the useful separation. Example: a timeout starts as a lifecycle rule, becomes a `worker.timed_out` event, updates durable state, and makes the engine choose a failure path.

## One request through the system

Event (repo, base commit, requested behaviour, acceptance criteria, allowed verification commands) → intake validates, picks blueprint, creates a run → engine picks implementer role → binder resolves to the Carbon implementer package with writable policy → environment manager creates an isolated checkout → lifecycle manager starts it via the adapter → implementer returns a **candidate artifact** (base commit, candidate commit, changed files, verification). The runtime **checks deterministic parts first** (commit exists, descends from base, file list matches diff, test artifact exists) → fan-out to correctness (Carbon) and security (Codex) reviewers on read-only views of the same commit and task contract; neither gets the implementer's conversation; different adapters, same result contract → consolidator groups findings and keeps lineage; code checks that findings point to real review evidence → one revision if a blocker remains → human handoff. If the revision was not re-reviewed, the package says so. "At no point does one agent have to remember the entire process."

## Failure thought experiment

Correctness review done; security reviewer times out. Lifecycle records and cancels; store keeps the completed review; engine follows the branch's failure policy (retry once, swap in a compatible reviewer, wait for a human, or fail). Must not happen: one review silently counting as two. Ideal: do not rerun the valid correctness review. A thin prototype may only keep the artifact and stop: **partial recovery, not resume**.

## Omnigent mapping

Agent directories = packages; harness interface = adapters; YAML config = binder; runner and session = lifecycle; Omnibox and cloud sandboxes = environments; contextual policies = state-aware control; server interfaces and collaboration = event/control plane. Polly = agent-led composition with cross-vendor review and human merge. His design picks **external code** for repeatable workflows; a mature system may combine both (code for the outer lifecycle and policy, a supervisor for bounded decisions inside steps).

## Questions for the build (video 10)

Can outside orchestration contain a weak worker's mistakes without the worker noticing them? Does cross-harness review find what same-harness review misses? What survives a branch timeout? How much recovery does a thin runtime give before a real durable-execution engine is needed? Do packages and adapters make workers interchangeable? Which controls belong in code and which decisions still benefit from an agent?

## Vocabulary bridge

"Components" (this video) explain *why* a capability is needed; "primitives" (in the Bhai code) are the reusable code boundaries that implement them. Long-term: a catalogue of SDLC blueprints = an "agentic software factory".

## Links

Anthropic: https://www.anthropic.com/engineering/building-effective-agents and https://www.anthropic.com/engineering/multi-agent-research-system · Omnigent: https://github.com/omnigent-ai/omnigent · Polly: https://omnigent.ai/docs/use/builtin-agents/polly · Zed ACP: https://zed.dev/acp · Carbon: https://github.com/thecarbonlayer/carbon · Refinery: https://github.com/thecarbonlayer/refinery

## What this means for our options-research harness

1. Write research workflows as versioned Python blueprints (for example `feature-test@v2`: data pull → feature build → bucket test → reviewer → findings page → human). The model judges inside steps; code owns transitions and limits.
2. Give each worker a package (model, instructions, tools, limits) and a role with a policy ceiling: the reviewer of a backtest gets read-only access to results and code, never write access.
3. Keep an artifact lineage graph: data snapshot hash → feature file → backtest result → review → findings page. Then "which data did this result use?" has one answer.
4. Put timeouts, cost caps and attempt limits in a lifecycle manager, not in prompts (this matches our memory that run records can lie about "running").
5. Use cross-harness or cross-model review for strategy claims: a second, independent reviewer that never saw the builder's conversation.
6. Separate observation from control: a dashboard that shows a runaway job is not enough; we also need a cancel path.
