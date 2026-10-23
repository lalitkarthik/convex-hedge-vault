promoted: 2026-10-23
# 10 — Meta-Harness: Testing Multi-Agent AI Systems Across 20 Runs

- **Title:** Meta-Harness | Testing Multi-Agent AI Systems Across 20 Runs
- **Channel:** The Carbon Layer (Ankit Desai)
- **Id / link:** `RSOQ0lQ2-1M` — https://www.youtube.com/watch?v=RSOQ0lQ2-1M
- **Length:** 45:37
- **Article edition:** https://thecarbonlayer.com/meta-harness-build/
- **Source of these notes:** yt-dlp hit HTTP 429; transcript from Firecrawl's YouTube scrape, read in full.
- **Part 2 of 2.** Watch video 05 first.

## Core thesis

He builds **Bhai** (Blueprint Harness for AI), the meta-harness designed in video 05, and runs it 20 times against a deliberately weak worker model (Gemma 26B). He walks **seven failure modes** of multi-agent systems and which component catches each. "The thing under test is not the model. It's the layer around the model." Not one fix is a better prompt. Writing the layers was easy (mostly written by a coding agent); the hard part was deciding where each check goes and which decisions a model may make.

## Bhai's vocabulary

- **Blueprint** — a versioned workflow file the runtime reads and executes, not a pipeline welded into the runtime.
- **Engine** — walks a blueprint from first step to last.
- **Runner** — runs one step: dispatches to a worker, counts attempts, writes the artifact to disk.
- **Adapter** — one per harness; the only code that knows what the Pi CLI or Codex CLI is.
- **Role** — a job: what the step is for, what it may touch, what shape its answer must have. An **agent package** is bound to a role; the binding is the only place they meet, so a worker can be swapped without the workflow noticing.
- Layering: Bhai → workflows → roles → bound agent harnesses → models. Carbon is a harness (one loop); Bhai exists because "one good worker and a reliable multi-agent system are two different problems".

## The seven failure modes and their answers

| # | Failure | Component that answers | What the runs showed |
|---|---|---|---|
| 1 | **Worker reports work it did not do** | Workflow-engine **gate** (checks against git) | Implementer reported a commit hash that did not exist; the gate asked git and stopped the run |
| 2 | **No way to tell which worker ran** | **Registry** stamps identity on every step | Harness changed version three times and name once in a week; only the stamps told runs apart |
| 3 | **Unusable output and stalls** | **Output contract** (inside the attempt loop) + **budget** | Invalid JSON retried; one attempt took 8.5 minutes; stopped at 4 attempts |
| 4 | **Authority nobody granted** | **Binder** (deny at the gate) + **environment** (never grant) | Chained `git add && git commit` denied 3 times, then split commands allowed |
| 5 | **Partial failure in a fan-out** | **State and artifact store** + resume | Correctness review kept; only the security review rerun |
| 6 | **No convergence / worker decides it is done** | Engine **cap** + forced terminal state | Cap held, but the final revision shipped two syntax errors unreviewed |
| 7 | **No way to see any of it** | **Event stream** | 253 events in one append-only file, rendered and exported to OpenTelemetry |

### 1 — Reporting work that never happened

The diff was real, so a reviewer could review it without the commit existing; every downstream step did real work on a false label. "Agent is the worst available detector of its own fabrication." The **gate** is one line of the workflow, runs after the worker exits, and the worker cannot see, call or skip it. On failure the run is marked failed and stops; no retry (the step already "succeeded") and resume would replay the same bad result. Six checks: commit exists; it descends from the base; the task is named; claimed changed files match the real diff; the referenced test artifact exists; the working tree is clean and no git remote is configured (nothing can be pushed). A quieter case: the base hash copied with one character dropped (39 instead of 40). **Design change he recommends:** stop asking the model what it did. The adapter now **derives the candidate from git** after the worker exits (stage, commit, read back the hash, take the real diff, run the allow-listed test command). No commit and no changes → step failure, so the attempt budget can retry. "Validating a claim and not needing the claim at all are different levels of trust."

### 2 — Which worker ran?

Configuration is assembled at runtime (manifest, flags, installed harness version, a model alias that may point at a new snapshot). Reading today's config answers a question about today, not last Tuesday. The binder resolves the role to one package; Bhai builds an **effective configuration** (package ID and fingerprint, role, tool profile = intersection of package and role permissions, workspace mode), serializes and **hashes** it, and the adapter emits an **instantiation event** before the worker starts. Three lines per adapter, so Pi, Carbon and Codex runs give one comparable record. A package is just a folder: short manifest, instruction file, limits — data you can diff. "The registry doesn't make a run reproducible on its own. It makes the run answerable."

### 3 — Unusable output and stalls

A model's input is a prompt, and a prompt accepts any string, so a wrong shape never throws; the next model "does its best with nonsense". The **output contract** runs inside the runner's attempt loop: write result and trace to disk on every attempt (even failures leave evidence), extract exactly one fenced JSON block, validate it against the role's declared shape. A failed validation *is* a failed attempt; "the contract decides and the budget bounds how many times it gets to decide". Contrast: the gate in (1) runs once, outside, and ends the run. Asides: a harness that fails to *start* is never retried; there is **no loop detection** — the outer layer cannot see a worker repeating the same tool call, but it can refuse to wait past a time or token budget declared in the manifest. "Containment without detection is a weaker guarantee, and it's also most of what you actually need."

### 4 — Authority nobody granted

Agents on a shared machine inherit its authority by default; "read-only" in a system prompt "is a request, not a boundary". The binder's gate is a callback handed to the harness before the worker starts and fires on every tool call, so it can correct mid-flight (it refuses shell metacharacters outright rather than parse them). But the model still split the chained command and owned the commit — the run that led to deriving candidates from git. Reviewers were never denied a write in 20 runs because they never had the capability: Codex ran with a read-only sandbox on a read-only clone. Two containments: **deny the action** (a rule) vs **never grant it** (infrastructure); the second is strictly stronger and the one people skip. **Mirror case — too little authority:** in a triage workflow, the history lens had only a file-read tool (no git), returned empty, was the slowest branch, and the gate passed it because it checked only the label. A well-formed empty result from a worker without the capability looks the same as "nothing to report".

### 5 — Partial failure in a fan-out

Two wrong answers: treat one review as enough (silently a one-reviewer design), or restart everything (pay twice for an unchanged commit). The right answer needs to know which branch finished, that its result is still valid, and that rerunning only the broken one is safe. Run: correctness review succeeded in 21 s; security review hit its 10-minute ceiling (he froze the process with a stop signal, because a short timeout made which reviewer finished first a coin flip). **Restart** is cheap to build, expensive to run; **resume** needs durable stored work. On resume: implement and correctness served from disk, security ran fresh in 28 s, then consolidate and handoff. **Six replay checks** per step: results file exists; parses as a worker result; worker succeeded; output still extracts; still validates against the role shape; the step's workspace clone still exists. Any miss → rerun ("fail closed"). Resume appends a marker to the same event stream. Limits: no mid-worker resume; workspace clones must still exist. Resume landed between parts 1 and 2. "Resume isn't a repair": if the cause remains, the step breaks again.

### 6 — Convergence and terminal state

Two directions: an endless review/revise loop, or a worker deciding it is done and taking a terminal action (merge, deploy, close). The revision cap (one) is structural: asking for a second revision raises an error. The handoff forces approval status to **pending** whatever the caller passes, and refuses to write anything if any workspace has a git remote (checked before any file or event, so no half handoff). **Where he got it wrong:** with a cap of one, the revision is always last and never reviewed. In the dashboard run, reviewers found 5 issues (4 blocking); the revision added two syntax errors (an unterminated f-string in the server, an invalid assignment in front-end script). The lineage gate passed (it checks provenance, not whether code runs). `pytest` exited 0 because the tests never imported the server. He noticed four days later. Lessons: a review that never executes anything is "a reading rather than a check" (the reviewer made 12 tool calls, all file reads); an exit code is worth only as much as what the tests load. What went right: the package recorded that the final revision was not independently reviewed; status pending; nothing merged or pushed. What went wrong: the known-limitations list was empty — it flagged the structural gap but not the specific one. **Fix:** separate *bounded* from *reviewed*: no revision ships unreviewed; cap at about five and exit when review has no blockers; or, cheaper, make the gate require that verification touched the changed files.

### 7 — Seeing it

Per-worker logs do not answer questions about the space *between* workers; a branch cancelled before it started wrote nothing, which looks the same as one never scheduled. One **append-only event stream** with four kinds of writer (engine and runner: boundaries, gates, resume marker; adapters: instantiation and worker events). Carbon's synchronous turns run on an OS thread, so the sink takes a **threading lock**. The runtime builds **one sink** and hands it to every writer, so the order in one file is trustworthy. Three surfaces from the same data: raw JSONL (253 events), a rendered view (folds 243 worker lines, shows decisions with reasons), and an **OpenTelemetry** trace (run → steps → workers → model turns) where parallel reviewers visibly start and end together. Gotcha: observability tooling assumes long-lived servers; a short run produces a value, not a time series (nine empty dashboard panels). Limit held: **observation is built, control is not** — Bhai can see a wrong tool call but cannot pause it.

## Did it generalize?

A second workflow (triage) reused the engine, adapters, permission model, event stream and resume unchanged, but needed **eight new artifact types and its own join gate** inside Bhai. "A gate has to know what it is looking at": a new workflow in a known domain is cheap; a new domain changes the runtime. He accepts this, since letting workflows ship their own gates makes the guarantee only as strong as the workflow author. Triage ran the same blueprint three ways (question: 1 step; feature: 2 steps; bug: 5 steps with a 3-way fan-out) chosen by a Python dictionary: "The model decides what kind of issue it's looking at, and the code decides what happens next." Swapping the implementer between harnesses was one package reference.

## Answers to part 1's questions

External orchestration contained a weak worker's mistakes (the invented commit); cross-harness review found two security findings the correctness reviewer missed (one run, a data point); a branch timeout leaves the completed branch, its validated result and the workspace; a thin runtime replays completed steps but cannot resume mid-worker; workers are interchangeable at step granularity; caps, gates, permissions and terminal state belong in code, judgment stays in steps.

## Closing question for any multi-agent setup

Look between the agents: who decides the next step runs, who remembers the first reviewer finished, who holds the revision limit, who may say the work is done? If the answer is "a model holding it in context", you are hoping, not ruling.

## Diagram to redraw

Use video 05's master diagram, then overlay seven red failure markers, each with an arrow to its catching component: (1) gate between implementer and reviewers, with a side arrow "ask git"; (2) registry → identity stamp on each step; (3) contract + budget inside the runner's attempt loop (loop arrow, "max 4"); (4) binder callback on each tool call + read-only environment box around reviewers; (5) state store with "served from disk" arrows on resume; (6) engine cap + handoff forced to "pending"; (7) one event sink receiving from engine, runner and adapters, fanning out to JSONL, renderer, OTel.

## What this means for our options-research harness

1. Derive results from artifacts, not from the agent's report: the harness reads the backtest output file and the git commit itself; the agent's summary never enters the record.
2. Hash an effective configuration for every research step (model snapshot, prompt file hash, data snapshot hash, tool profile) so any number can be traced to what produced it.
3. Validate one fenced JSON result block per step against a declared schema; invalid output is a failed attempt with a fixed budget.
4. A reviewer of a strategy must *execute* something (rerun the backtest on a held-out window), not only read code. Make the gate require that verification touched the changed files.
5. Never cap revisions so that the last change goes unreviewed; loop until the reviewer has no blockers or a cap of a few rounds is hit.
6. Write every decision to one append-only event file per run; render it, and export to OpenTelemetry later.
7. Watch for "too little authority": a data-quality lens without the data tool will return a clean-looking empty result.
