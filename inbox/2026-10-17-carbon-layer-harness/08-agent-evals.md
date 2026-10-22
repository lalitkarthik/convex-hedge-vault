# 08 — AI Agent Evals: Does the Agent We Built Actually Work?

- **Title:** AI Agent Evals | Does the Agent We Built Actually Work?
- **Channel:** The Carbon Layer (Ankit Desai)
- **Id / link:** `B9NPE_CaK5Q` — https://www.youtube.com/watch?v=B9NPE_CaK5Q
- **Length:** 37:18
- **Article edition:** https://thecarbonlayer.com/agent-evaluation/
- **Source of these notes:** yt-dlp hit HTTP 429; transcript from Firecrawl's YouTube scrape, read in full.
- **Errata (from his description):** he says "75 percent accurate" where the slide's 79% is right; he says 0.789 where the baseline pass fraction is 0.787.

## Core thesis

A general coding agent is hard to grade; a **domain agent** has definable correct behaviour, so it is measurable. He turns the series agent into **CrikIT**, a cricket-stats agent over an amateur-league database, builds an **evaluation harness** around it, and runs two fix loops. Pass rate moves 0.787 → 0.973 and **confidently wrong answers move from 11 to 0**, every number backed by a fingerprinted results file. The habit to keep: before trusting an agent, ask **what kind of wrong** it is when it is wrong.

## Turning a general agent into a domain agent

No fork of the harness. About 10 lines of configuration on the same agent class: a **system prompt** (a commentator persona), about **15 deterministic read-only tools** (top run scorers, player batting summary, team standings…), a **guarded fallback** (a generic aggregate tool where the model writes its own query), and a **read-only policy**. Everything runs against a frozen, redacted local snapshot. He expects many narrow agents built by general agents.

## The eval vocabulary (five words)

- **Dataset** — a collection of items.
- **Item** — one real question (ID, question, category, expected answer kind, a function that computes the **gold answer** from the database, expected tool).
- **Metric** — what you measure per item (match, right tool, time, cost).
- **Score** — what a metric produces on a run.
- **Runs over time** — tracking scores across changes tells real improvement from feel.

Baseline: 25 items × 3 repeats on local Gemma 4 26B A4B. Repeats separate skill from luck.

## Six things worth measuring

1. **Outcome** — did the answer match the database? Baseline 0.787 (about 79%).
2. **Trajectory** — which path? Correct tool rate 0.933. The confident "124" (true answer 152) came from **zero tool calls** on every attempt: a guess. Outcome says it is wrong; trajectory says why, and "why" is what you act on.
3. **Cost** — about 5,262 tokens and 6.4 s per answer.
4. **Reliability** — same question three times.
5. **Safety** — prompt injections, destructive requests, personal-data fishing, out-of-domain: all declined, score 1.0. Partly **architecture, not model**: read-only tools on a snapshot mean no code path can modify anything.
6. **Experience** — stays in character, clear, admits when it cannot find data, asks a clarifying question when ambiguous. The last scored **3%**.

**Category split matters.** Happy path 0.92; adversarial and edge 1.0; known-weak 0.67; ambiguous 0.17; no matching tool 0.33. Ten happy-path checks would have shown 92% and hidden the rest.

## Concepts

- **pass@k vs pass^k.** pass@3 = right at least once in 3 tries (0.84). pass^3 = right every time (0.76). The gap is **flakiness**. It concentrates where the model writes its own query (the fallback), not where a deterministic tool answers.
- **Confident hallucination vs abstention.** Of graded answers: 59 correct, 11 confidently wrong, 5 declined. Hallucination rate about 0.15. A decline ("my query returned nothing") is the **safe kind of wrong**. On a scoreboard both look the same; to a user they differ completely. Measure them separately and engineer toward abstention.
- **Grade with plain code first.** Code checks are cheap, deterministic, and never change their mind. Two agent design choices make them possible: every reply ends with a small **machine-readable JSON answer block** (value and kind) under the persona prose — its presence held at about 97.3% — and the **gold answer is computed** by the same deterministic query functions, never hand-typed, so the key cannot drift from the data.
- **LLM judge, small remit, calibrated.** For persona, clarity, admitting, clarifying: four yes/no criteria with an allowed "unknown". The judge is the same local model (it grades its own homework), so he **hand-labelled 24 answers** and checked agreement: **kappa 1.0**, the only reason judge scores appear. Judge results: persona 97%, clarity 97%, admitting 84%, clarifying 3%. "This agent would rather guess than ask."
- **Labels the eval will need are added at build time.** The harness traces every call for free (observability primitive). The author adds labels: each tool declares its **tier** (domain or fallback); runtime adds whether the result was ok, error, or **empty**. The eval harness lives outside the agent and reads only those attributes. Cheaper to add while building than to retrofit.
- **The fallback log is a shopping list.** Fallback rate 0.147; routing correct (used when expected, never when a tool existed). But counting centuries and fifties have no tool, and the model's own aggregation gets them wrong. Questions that keep hitting the fallback and failing are the next deterministic tools to build.
- **Escape hatches invite over-trying.** Centuries/fifties burned about 6,500 tokens each and still failed. "Man of the match": on 2 of 3 attempts, 5 constructed queries, 6 tool calls, nearly 29,000 tokens — over 5× average — to fail; the third declined in one call.
- **Long-horizon chains and weighted checkpoints.** Question: who holds the highest score record, and that player's career runs and wickets? Three dependent steps, no planner (plain drive loop), so nothing structural guarantees the sequence — that is why it needs measuring. Grade with **weighted checkpoints** (some credit for the record holder, more for runs, full for wickets) so partial credit localizes the break. Result 1.0 on all three runs (164 career runs, 6 wickets). Capability profile: **strong at sequencing tools, weak at authoring queries** — "far more useful than 75% accurate".
- **Fault injection for recovery.** Force the first tool call to return empty; the trace marks it empty; the agent retried and still answered correctly (`faulted: true`, retried).
- **Behaviour drift from layers you do not control.** A harness release (domain code untouched) moved the result budget into the harness, so CrikIT dropped its own 6,000-character truncation. Headline 0.787 → 0.813, but abstentions fell 5 → 0; fifties began answering (382, right on 2 of 3); man-of-the-match now thrashed on all 3 (about 29k tokens, no answer block); average cost up about 14%. The polite abstention "was never a personality trait. It was the plumbing." Track configuration version, model, dataset and harness baseline; any change triggers a rerun.

## The two fix loops

1. **Schema map.** The fallback failures shared one cause: queries written against a schema never seen. Fix used an existing primitive: write an `AGENTS.md` data map (which collection holds per-innings batting, IDs not names, exact field names) and point the loader at it. No new tools, no model change. Centuries 0/3 → 3/3 (answers 15); fifties flaky 2/3 at 16–19k tokens → stable 3/3; about 5,900 tokens and one query each. Full suite 0.813 → **0.960**. The 124 question now answers 152; man-of-the-match collapses to a clean decline; "best player" declines properly. **Regression flagged:** "How did we do this year?" (ambiguous "we") used to hold back on 2 of 3; now all 3 dump the standings — the richer prompt made it answer-eager.
2. **Ambiguity guard.** One paragraph in `AGENTS.md`: if the subject is unspecified, do not assume and do not answer with all of them; ask, because a confident wrong guess is worse than a clarifying question. Full suite → **0.973**; pass@k 1.0; pass^k 0.96; confident-wrong 11 → **0**. Remaining gap: one flaky man-of-the-match item, failing the safe way.

The loop: **watch it fail → read the trace → change one primitive → rerun the same questions → watch every number move, including the ones you did not mean to move.**

## Eval has a bill

25 × 3 = 75 answers × about 5,262 tokens ≈ 400,000 tokens per pass, on a toy set. The EvalEval Coalition (Hugging Face blog) cites about $2,800 for one run of one agent benchmark. Choose which agents and skills deserve evals, item count, repeats, rerun frequency. He prefers 25 sharp items run on every change over 500 run quarterly.

## Diagram to redraw

1. **Domain agent** box = same harness + system prompt + 15 deterministic tools + fallback tool + read-only policy, over a **frozen DB snapshot**.
2. **Tracer** on the agent emits spans with labels (tier, ok/error/empty).
3. **Eval harness** (outside the agent): **dataset** (25 items) → runner (×3 repeats) → agent → spans + JSON answer block → **graders**: code checks (gold answer from the same query functions; right tool; tokens) and **LLM judge** (4 criteria, calibrated vs 24 hand labels).
4. Graders → **scores per metric** (outcome, trajectory, cost, reliability pass@k/pass^k, safety, experience) → **fingerprinted results file** → **runs-over-time** chart keyed by model, harness, config and dataset version.
5. Side outputs: **fallback log → tool shopping list**; **fault injector** feeding empty results into a tool.
6. Loop arrow: results → change one primitive (`AGENTS.md`) → rerun.

## Links

Article: https://thecarbonlayer.com/agent-evaluation/ · EvalEval on eval costs: https://huggingface.co/blog/evaleval/eval-costs-bottleneck

## What this means for our options-research harness

1. Build a small, sharp eval set for the research agent: questions with computed gold answers from our own data (for example "SPXW 0DTE ATM IV at 10:00 on a given date", "P&L of a fixed straddle rule on a fixed week"). Compute gold with the same deterministic functions the tools use.
2. Require a machine-readable result block at the end of every research answer (value, unit, data window, trial ID) so code grades it.
3. Score confident-wrong separately from "could not determine". In finance, a confident wrong number is the worst outcome; reward abstention.
4. Label tools by tier (deterministic data tool vs free-form query/code) and log the fallback rate; questions that keep falling back become the next deterministic tool.
5. Report pass@k and pass^k with repeats; a strategy result that appears in only some reruns is flaky, not real.
6. Rerun the eval set whenever model, harness, config or dataset changes, and fingerprint each results file.
