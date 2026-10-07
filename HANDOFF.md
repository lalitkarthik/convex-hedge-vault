# Handoff — 2026-10-07

Two repos are involved: this vault, and `D:\Convex Hedge\convex-hedge-strategy` (Meghav's repo, `MeghavPradeep/convex-hedge-strategy`).

## Start here

Teach **lesson 2 of 16, the breakeven move**. The list is the section "To teach on 8 October" in [plan.md](inbox/2026-10-07-long-gamma-research/plan.md); lesson 1 (item A1) is done. Follow the pattern of lesson 1: one item per message, short paragraphs, a small table of real numbers, one PNG chart from the repo's own days sent with the file tool, nothing asked of Lalit. Lesson 1 used 1 June 2026 and the straddle chosen at 9:35 (strike 7575); its chart is [01-theta-over-gamma.png](teach/long-gamma-research/01-theta-over-gamma.png). Lesson 2 starts from its closing number: √(2 × theta ÷ gamma) = 1.93 points a minute at 9:36.

## In flight

- **Nothing is running for this work.** No branch, worktree or PR of ours is open in `convex-hedge-strategy`. Local checkout is on `main` at `0ff3c74`.
- **Uncommitted, not ours to commit:** `notebooks/spxw_hedged_straddle.ipynb` in the strategy repo shows as modified (200 lines changed). Lalit has it open in VS Code. *Inferred:* VS Code re-saved it or he ran cells. Leave it; ask before reverting or committing.
- **Lessons 2 to 16:** not taught.
- **PR #24** (`feature/theta-vega-chart`) is Meghav's and open. Not touched.
- **Another build runs on this machine that this session did not start:** `orch-iv-vs-rv` in `Convex-Hedge-Trading-Engine`. Accounts b and c were spent until about 15:30 and 15:40 IST; a was free (read from `cx status` at hand-off).
- **Vault:** `inbox/2026-10-06-iv-vs-rv-research/` is untracked and predates this session. Left alone.

## What changed this session

In `convex-hedge-strategy`, all on `main`:

- PR #19 (Meghav's Greek ratios) merged **with the market data in it**, on Lalit's say.
- PR #26, issue #20: the hedged straddle results table (tickets #21, #22, #23). Built by the feature-loop orchestrator.
- PR #27, issue #25: the hedged straddle study and `notebooks/spxw_hedged_straddle.ipynb`. Built by one worker.
- Verified at hand-off: on local `main` the notebook re-ran top to bottom in 227 s with no error; on the study branch before merge 179 tests passed, mypy and ruff clean.

In this vault: [plan.md](inbox/2026-10-07-long-gamma-research/plan.md), [literature-report.md](inbox/2026-10-07-long-gamma-research/literature-report.md), the lesson 1 chart, and the 7 October entries of [session-log.md](session-log.md).

## Decisions made

- The 20 planning decisions (target, hedge rules, costs, sources, proof): table in [plan.md](inbox/2026-10-07-long-gamma-research/plan.md).
- Band, hedge target, unpriced hedges: decisions 0020, 0021, 0022 in `convex-hedge-strategy/Strategy-Research/Decisions/`.
- The five tests and their pass bar: [issue #25](https://github.com/MeghavPradeep/convex-hedge-strategy/issues/25).
- Verdict on each idea: the five pages in `convex-hedge-strategy/Strategy-Research/Strategies/`.
- Where the study left its spec and the usual process: body of [PR #27](https://github.com/MeghavPradeep/convex-hedge-strategy/pull/27).
- Lalit reads part D of the descriptive notebook on his own; it is not part of the lessons.

## Open questions

- **Blocked on Lalit: three readings of the skipped-hedge rule**, set out in [this comment on #20](https://github.com/MeghavPradeep/convex-hedge-strategy/issues/20#issuecomment-6032875176). They change the notebook's skipped-hedge counts, not the tests. A change is a small fix to one loop and its tests.
- **What goes to the seniors.** Plan decision 19 named a one-page summary for the daily meet. Not written. The notebook's Part 2 and Part 3 hold the figures.
- **Sources.** Three of the five ideas rest on papers read as abstracts only (Muravyev and Ni; Zakamouline; Andersen and Bollerslev). The 7 October literature report's other links are still unopened by hand.
- **Not tested, by design:** a buyer in the first hour. The descriptive study pointed there; it has no published source, so it is description only.
- **Unchecked:** which dates the desk's backtest tool holds. The later proof needs days outside 31 March to 30 September 2026.
- **Vault canon is stale.** [strategy-research](domain/strategy-research.md) is stamped at `4bcf653` and does not know the table, the study or the merged data. The inbox plan is staging; nothing is promoted. [session-log.md](session-log.md) is 288 lines, over the 200-line bound.
- *Assumed:* Lalit wants builds run by the feature-loop orchestrator, not gated by hand in the planning session. He stopped a manual check mid-run and asked for the orchestrator.

## Traps found

- **A dead worker still says "running".** The study worker died mid-command and `~/.claude/accounts/runs/<name>.json` kept `"running": true` for 36 minutes. Check the transcript's modified time under `~/.claude-<account>/projects/…/<session>.jsonl`, and look for the process. `cx send <name> "…"` resumed it with its context.
- **The feature-loop dashboard stops on its own.** Restart it in the project root: `node ~/.claude/skills/feature-loop/scripts/dashboard.mjs --detach` (port 8765).
- **`data/` is now tracked on `main`** (PR #19), against the repo's own rule. Every worktree carries about 650 MB. The two hedged tables are *not* tracked: a fresh checkout must run `uv run python scripts/build_hedged.py` before the notebook runs.
- **This repo is not set up for feature-loop.** The orchestrator needed an override prompt (no auto-merge, no flow check, never print a result). It is at `%TEMP%\feature-loop-orch-hedged-straddle-table.md`; reuse it.
- **`/mattpocock-skills:to-spec`, `to-tickets` and `handoff` can only be typed by the user.**
- A Bash command holding several heredocs with apostrophes failed to parse. Write the files with the file tool, then run the command.

## Read these

1. [plan.md](inbox/2026-10-07-long-gamma-research/plan.md) — decisions, facts, the five hypotheses, the sixteen lessons.
2. `convex-hedge-strategy/notebooks/spxw_hedged_straddle.ipynb` — the result. Open it locally; sliders do not draw on GitHub.
3. [session-log.md](session-log.md), the three 7 October entries.
4. `convex-hedge-strategy/Strategy-Research/Guide/` — the pages for the hedged straddle results and for the study.
5. Memory notes on teaching: `teach-dont-quiz`, `explanation-style-paragraphs-ste`, `phone-cannot-show-widgets`.
