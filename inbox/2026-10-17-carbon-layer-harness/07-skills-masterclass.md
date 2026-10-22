# 07 — Skills Masterclass

- **Title:** Skills Masterclass
- **Channel:** The Carbon Layer (Ankit Desai)
- **Id / link:** `nrh1YtPKRD0` — https://www.youtube.com/watch?v=nrh1YtPKRD0
- **Length:** 31:54
- **Article edition:** https://thecarbonlayer.com/agent-skills/
- **Source of these notes:** auto-generated English subtitles, read in full.

## Core thesis

A **skill** is a reusable procedure that the harness loads when a recurring class of work appears. It does not capture the expert; it captures the *repeatable part* of the expert's procedure. Skills are **procedural memory** the harness can find, load progressively, test against a baseline, and maintain like code.

## Running example

A pull request that changes authentication middleware; the user says "review this PR before merge". Every team has one strong reviewer who checks the denied path and runs focused checks, but that person does not scale, so review quality is uneven.

## The escalation (why each earlier layer is not enough)

1. **Better prompt** ("review carefully, look for bugs…"). Helps, but the procedure stays in the user's head and must be retyped.
2. **Instructions** (`AGENTS.md`: prioritize correctness, security, tests). Now in the environment, but **passive**: cannot find changed files, choose the test command, or produce a structured report.
3. **Tools** (git diff, `pnpm test auth`, CI, issue search). The agent can act, but tools do not know *which* action, in *what* order.
4. **Skill.** Writes down how a serious review happens: trigger, steps, examples of good findings, output format, scripts, gotchas from past reviews. "The model still has to reason, but the harness has given it a better path through the work."

## Concepts and principles

- **Placement in the harness map:** primitive 9, "skills and procedures", after sub-agents (8). In his 10-primitive list the last box is **proof and learning**.
- **Skill vs sub-agent.** "Skill is the procedure. Sub-agent is one possible executor." Agent keeps inventing the process → make a skill. Needs a separate window, narrower tools, or parallelism → use a sub-agent. A review sub-agent without a review skill is "a fresh model loop with a vague job".
- **Two maps, both true.** In the harness map a skill is its own primitive (the harness discovers, chooses, loads it). In the memory map (video 04) a skill is procedural memory. *Semantic*: "auth middleware lives in `src/server/auth`". *Procedural*: "here is the review sequence".
- **Progressive loading / disclosure.** Load the description first, then the top-level `skill.md`, then deeper reference files (for example an auth review file) only when the diff touches that area. Do not treat the skill library as one big prompt.
- **Skill anatomy:** trigger; **non-trigger** (when not to load: summarize the PR, write release notes, implement the fix); inputs; process; preferred tools; output format; **gotchas** ("do not claim tests pass unless you ran them").
- **The description is part of the system, not marketing copy.** Too vague → never loads. Too broad → loads everywhere.
- **Use a skill-creator skill** for the first draft; review it like code; test it on real PRs.
- Cites Anthropic's June 2026 Claude Code skills write-up: good skills are focused, capture what the model tends to miss, start small and grow from edge cases; measure usage and under-triggering.

## Evaluating a skill (agentskills.io frame)

Create realistic tasks → run **without** the skill (baseline) → run **with** it → capture outputs, timing, token cost, grades → write assertions for objective parts → human review for judgment → iterate.

- **Eval set example:** five seeded PRs — auth middleware missing a denied-path test; a migration dropping a nullable default; a front-end mobile overflow bug; an API response change that breaks a documented client; a pure refactor with no behaviour change.
- **Objective assertions:** identifies the changed auth boundary; separates blockers from suggestions; one file reference per finding; no claim of passing tests without evidence.
- **Five measures:** bug catch rate vs baseline; false positives; evidence quality; cost (did tokens triple for a small gain?); trigger behaviour.

## Five failure modes

1. **Over-broad scope** — one "engineering" skill becomes a second system prompt.
2. **Under-triggering** — description "helps with quality" never matches "review this PR".
3. **Stale procedure** — repo moved from Jest to Vitest; the skill still says `npm test auth` and sounds official.
4. **Context bloat** — 40-line diff, 8,000 words of review philosophy loaded.
5. **False confidence** — repeatable is not proven; skills must demand receipts.

## Skills as living artifacts

Start from one recurring failure; add the first gotcha; run on real work; route each miss to the right home (skill, script, test, instruction, product). **Prune** too: models improve, and old steps become noise. At scale you need a **registry, owners, a promotion path** (experimental → shared after evals), usage signals, and **deprecation**. Example ownership: owner = platform team; eval set = seeded PRs; review monthly or after a test-runner change; local repo first, promote after passing evals.

## Rule of thumb: make a skill when all four are true

1. The task repeats. 2. The procedure matters. 3. Mistakes are expensive. 4. The right behaviour is not obvious from the prompt.
Otherwise: one global sentence → instructions; a capability → tool; separation → sub-agent.

## Diagram to redraw (all layers on one PR review)

A vertical stack feeding one agent, each box labelled with its PR-review job:

1. Instructions → general priorities.
2. Context delivery → PR description, diff, changed files, CI logs.
3. Context management → which of these is visible now; which skill files load.
4. Tools → read, search, run tests, check CI.
5. Execution environment → where commands run.
6. Durable state → project conventions, prior review lessons.
7. Orchestration → when to ask a human, retry, stop.
8. Sub-agents → security / front-end / test reviewers, each with a narrower skill.
9. **Skills** → the review procedure (highlight), with child files: `auth-review.md`, `migration-review.md`, `frontend-review.md`.
10. Proof and learning → receipts, and misses fed back into the skill (arrow from 10 back to 9).

Second small diagram: **Run 1 (no skill)** → shallow "code is cleaner, add tests"; **Run 2 (skill)** → "missing-token request still passes the admin guard; file; evidence; verification; fix".

## Code or repos

None shown. References: agentskills.io; Anthropic's Claude Code skills post (June 2026).

## What this means for our options-research harness

1. Make skills for our repeated research procedures: Bilal's bucket test, the backtest rules (decide on candle i−1, trade on i; 150k per lot; no compounding), the Databento pull with holiday handling, the findings-page build.
2. Give each skill a non-trigger section (for example "not for live-trading changes").
3. Eval each skill with seeded cases: a strategy with known look-ahead bias, a holiday half-day, a cost-free backtest. Measure catch rate against a no-skill baseline.
4. Keep deep references (AFML chapters, cost model detail) as child files loaded only when needed.
5. Give each skill an owner and a review date; prune when the model no longer needs a step.
