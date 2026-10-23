# Agent harness design — the principles that transfer

An **agent** is a model inside a **harness**. The model is frozen, stateless and rented: its
weights never change, it remembers nothing between calls, and the provider can change what is
served under the same name. Everything else is the harness: what the model sees, what it can
touch, what it remembers, how its work is checked, and how the system learns from failure. Those
are software decisions, and they are the part you engineer.

This note states the lessons as principles. They come from The Carbon Layer's twelve-video series
on harness engineering (Ankit Desai, with one IBM talk by Tejas Kumar) and from the 16 October
research into research harnesses. The study notes number the principles P1–P50; the numbers below
point at [principles](../inbox/2026-10-17-carbon-layer-harness/principles.md). How the options
research harness applies them: [options-research-harness](options-research-harness.md).

## Three ideas under everything

- **Deterministic work goes in code; only judgment goes to the model.** Order of steps, limits,
  storage and proof are code. The model decides what kind of task it faces; code decides what
  happens next (P28).
- **Boundaries live in infrastructure, not in prompts.** "Read-only" in a system prompt is a
  request. A boundary is what still holds when the instruction fails (P16).
- **Nothing is done or improved without receipts** that trace to an exact, fingerprinted
  configuration: harness commit, model, settings, data and environment (P34, P41).

When an agent fails, ask which layer ran out of road before you blame the model (P1). A strong
harness lifts a weak model, and a weak test model exposes harness gaps that a strong one hides (P4).

The series names about ten layers, each added because the one before runs out of road:
instructions, context delivery, context management, tools, the execution environment, durable
state, orchestration, sub-agents, skills, and **proof and learning**. The list is the speaker's
teaching device, not a standard ([01](../inbox/2026-10-17-carbon-layer-harness/01-harness-engineering-masterclass.md),
[03](../inbox/2026-10-17-carbon-layer-harness/03-agent-from-scratch.md)).

## Context: protect the model's attention

Context management decides what reaches the model on this call. Wrong context can be worse than
missing context, because it hands the model a plausible distraction (P6). It has four moves, each
with a cost ([06](../inbox/2026-10-17-carbon-layer-harness/06-context-management.md)):

- **Select** what goes in, and where it sits; models use the start and end of a long window best.
- **Compress** old history. It is lossy and is itself a model call; a good summary keeps the goal,
  the locked decisions, progress, key facts and the next step (P9).
- **Write** what you cannot lose to a file on disk.
- **Isolate** a sub-task in its own window, at the price of coordination.

Freeze a stable prefix (identity, instructions, tools) and move only the tail, or the prompt cache
breaks and every call costs more (P8). Never drop overflow blindly: keep head and tail, or
**offload** the full output to a file and pass a reference (P10). A bigger window is a bigger desk,
not memory (P14). Hand work between phases through files, not transcripts: research writes a
findings file, planning a plan file, and implementation starts fresh from the plan (P27).

## Memory: context assembled over time

Memory is the harness deciding what to keep, recall, update and forget
([04](../inbox/2026-10-17-carbon-layer-harness/04-agent-memory.md)). Keep four types apart (P11):

| Type | Holds | Example in a research harness |
|---|---|---|
| Working | This call's window; a budget, not persistence | The current card and tool results |
| Episodic | What happened and when | The run event files and the trial ledger |
| Semantic | Standing facts | Contract specs, the cost model, dated facts |
| Procedural | How work is done | Skills, tool schemas, orchestration code |

Conflicts are state problems: the newer fact becomes current, the older stays as history (P12).
Forgetting is hygiene: every fact has a date, every procedure an owner and a review date (P13). Memory can also spread an error: a leaky result stored as a precedent is
copied by later runs, so only validated results may enter cross-run memory
([validation](../inbox/2026-10-16-options-harness-research/validation.md)).

## Skills: the repeatable part of an expert's procedure

A **skill** is a written procedure the harness loads when a recurring kind of work appears
([07](../inbox/2026-10-17-carbon-layer-harness/07-skills-masterclass.md)). It has a trigger and a
non-trigger, loads progressively (description first, body and child files on demand), demands
receipts, and has an owner and a review date. Make one only when the task repeats, the procedure
matters, mistakes are expensive, and the right path is not obvious (P31). A skill is the
procedure; a sub-agent is one possible executor. Give every sub-agent the same skill, or each
invents its own process and parallel results disagree (P30). Evaluate a skill against a no-skill
baseline on seeded cases.

## Boundaries and sandboxing

Order of strength: **never grant** beats **deny**, and deny beats **ask** (P17). Start closed: no
network, scoped writes, no credentials until configuration grants them (P18). Agent safety has three
boundaries: what the model can call (the tool registry), what those tools can reach (credentials),
and where execution touches the system (the sandbox)
([09](../inbox/2026-10-17-carbon-layer-harness/09-agent-sandboxing.md)).

- Treat model-callable tools as public endpoints: a short list, narrow contracts, arguments
  validated at the boundary, structured choices over free strings (P19).
- Choose the cheapest sandbox layer that contains the failure you fear, and make it cover child
  processes; a notebook spawns kernels and a backtest spawns workers (P20).
- Keep secrets harness-side. The harness holds the key and makes the paid or sensitive call; the
  model gets the result and a note that the step was done (P23).
- Approvals are scarce on purpose: they mark only boundary-crossing actions (P21).
- The harness owns every file it creates, in per-run scratch space outside the project, deleted
  at run end on the failure path too (P24). A canary secret plus a disk scan after each run finds
  a second persistent copy ([11](../inbox/2026-10-17-carbon-layer-harness/11-self-improving-agent-engineering.md)).

## Coordination: the meta-harness

A **meta-harness** sits above several harnessed agents and coordinates them as workers. Its thesis
is to move coordination *out* of the agents, so the system does not depend on one supervisor model
remembering the process ([05](../inbox/2026-10-17-carbon-layer-harness/05-meta-harness-design.md)).
It has eight parts: a package registry, harness adapters, a role and policy binder, a workflow
engine, a lifecycle manager, an environment manager, a state and artifact store with lineage, and
one append-only event stream.

Twenty runs against a deliberately weak worker showed seven failure modes, each caught by code
([10](../inbox/2026-10-17-carbon-layer-harness/10-meta-harness-20-runs.md)):

| Failure | What catches it |
|---|---|
| A worker reports work it did not do | A gate that checks git; better, derive the result from git and never ask |
| Nobody can say which worker ran | A hashed effective configuration stamped on every step |
| Unusable output, or a stall | An output contract (one JSON block, schema-checked) inside a capped attempt loop |
| Authority nobody granted | Never grant it; reviewers get read-only copies |
| One branch of a fan-out fails | Stored results, replay checks, resume only the broken branch |
| No convergence, or a worker declares itself done | A revision cap in code; the terminal state is forced to "pending" for a person |
| Nothing can be seen | One event sink, rendered for people and exported to tracing |

**A check is only as strong as what it executes**: a review that only reads files is a reading, and
green tests prove nothing if they never load the changed code (P36). **Observation is not control**:
seeing a wrong tool call does not pause it (P33).

## Proof: evals and receipts

Stop asking the model what it did; read the outcome from ground truth (P35). For measuring an
agent ([08](../inbox/2026-10-17-carbon-layer-harness/08-agent-evals.md)):

- **Grade with code first.** Compute gold answers with the same deterministic functions the tools
  use; end every answer with a machine-readable block so code can grade it (P38).
- **Measure the kind of wrong.** Count confident-wrong answers apart from abstentions, and engineer
  toward the safe failure (P39). In research, a confident wrong number is the worst outcome.
- **Repeat and split.** Report pass@k (right at least once in k tries) and pass^k (right every time);
  the gap is flakiness. Never judge by the aggregate alone (P40).
- **Calibrate any LLM judge** against human labels before trusting it. In one 2026 study, an open
  audit prompt flagged most clean code; a closed flaw list fixed it, and a "skeptical reviewer"
  persona *raised* false positives ([validation](../inbox/2026-10-16-options-harness-research/validation.md)).
- **Fingerprint every run and rerun on any change**; behaviour drifts from layers you did not touch (P41).

## Evolution: improving the harness, not the model

A **self-improving agent** here is a loop that improves the harness and leaves the model frozen
([02](../inbox/2026-10-17-carbon-layer-harness/02-self-improving-agents.md)). Mine failures into
clusters with one provable cause (P45); classify the fix first: a missing fact goes to memory,
plumbing to the harness, a failure everywhere to the model choice (P44). A stronger model proposes
changes only to a declared **editable surface**; graders and answer keys stay out of its reach and
are fingerprinted (P46). A change is accepted only if it is at least as good on held-in and
held-out tasks and strictly better on one, then confirmed in paired runs (P47). It lands as a pull
request that a person merges, with rollback as a normal operation (P49).

The first such pull request passed every test and was rejected: a bigger output limit that kept the
structural failure. The fix exposed *behaviours* (clamp, head and tail, offload), not numbers (P48).
The loop is the easy part; boundaries, evidence, isolation and promotion are the engineering (P50).
Held-in and held-out tasks are in-sample and out-of-sample data; selecting on them leaks them (P46).

## Tools for agents: MCP

From the tool survey ([MCP and tools](../inbox/2026-10-16-options-harness-research/mcp-and-tools.md)):

- Separate free tools from billed ones, and give the billed one a hard cost cap. Return handles and
  file links, never rows. Long jobs follow prepare, start, status, result, cancel, with idempotency keys.
- Register write tools only behind a flag; a read-only reviewer gets a read-only tool list. A gate
  exposed as an optional tool can be skipped, so gates live inside your own servers, which write
  the ledger row before they return.
- Treat a third-party server as untrusted code: pinned, containerised, narrow key, no network, and
  its tool descriptions read, because they can steer the model.
- A typed decision model can answer narrow questions cheaply, but keep it out of the critic, any
  calculation and routing; code decides, and every step leaves a receipt
  ([Jev](../inbox/2026-10-16-options-harness-research/jev-deep-dive.md)).

## Where the sources disagree

| Question | One side | Other side |
|---|---|---|
| Retry after a failed check? | IBM retries the whole attempt | Stop the run: a retry replays fabricated work; retry only contract failures |
| Fix by instruction? | Two eval failures were fixed by `AGENTS.md` paragraphs | Never for plumbing; reconciled by P44 (knowledge suits instructions) |
| Who builds the harness? | IBM: agents generate their own | The series: a declared surface and a human merge |
| Who picks the next research axis? | A director agent (one research lane) | Code (another lane; the options harness chose this) |

## Open questions

- Does a headless Claude Code worker honour a per-package permission file on Windows? Untested (G6).
- Is a calibrated skeptic, re-running the work in a fresh context, worth its token cost on every
  hypothesis, or only on candidates that pass the cheaper gate steps?
- The series ran one small local model. Do its numbers hold for a frontier model, which hides gaps?

## Sources

- [Carbon Layer study notes](../inbox/2026-10-17-carbon-layer-harness/00-index.md):
  [principles](../inbox/2026-10-17-carbon-layer-harness/principles.md),
  [glossary](../inbox/2026-10-17-carbon-layer-harness/glossary.md),
  [diagram spec](../inbox/2026-10-17-carbon-layer-harness/diagram-spec.md),
  [12, IBM](../inbox/2026-10-17-carbon-layer-harness/12-ibm-harnesses-deep-dive.md), and 01–11 linked above
- [Agent harnesses](../inbox/2026-10-16-options-harness-research/agent-harnesses.md),
  [validation](../inbox/2026-10-16-options-harness-research/validation.md),
  [MCP and tools](../inbox/2026-10-16-options-harness-research/mcp-and-tools.md),
  [Jev](../inbox/2026-10-16-options-harness-research/jev.md) and its
  [deep dive](../inbox/2026-10-16-options-harness-research/jev-deep-dive.md)
