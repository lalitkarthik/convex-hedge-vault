> As of options-research-harness@1e64142, 2026-10-23

# Options research harness — agents that research SPXW 0DTE under rules they cannot change

The **options research harness** is a system in which AI agents do strategy research on SPXW
same-day (0DTE) options, the way the desk already does it by hand, but faster and with a record of
every step. An agent proposes an idea; other agents grill it, test it, review it and rebuild it;
plain code judges the result against rules that no agent can change. It does not trade. It starts
with one market and the one year of data we already hold.

It lives in Lalit's private repo `lalitkarthik/options-research-harness`, cloned to
`D:\Convex Hedge\options-research-harness`. **The repo's own docs are canon for anything inside
it**; this note is the map. Front door: `docs/design/00-overview.md`. Terms: `CONTEXT.md`.

## Why it exists

On 15 October 2026 Bilal asked Lalit and Meghav to read López de Prado's *Advances in Financial
Machine Learning* (AFML) and to build a faster research pipeline by connecting MCP servers. Two
facts from the research behind it shape the design
([validation](../inbox/2026-10-16-options-harness-research/validation.md)):

- **An agent tries configurations at machine speed.** The trial count grows faster than a person's,
  so the best in-sample Sharpe ratio climbs by selection alone. Every trial must be counted, and
  every reported number deflated by that count.
- **Statistics do not catch leakage.** In one 2026 study a planted look-ahead "oracle" passed both
  the deflated Sharpe ratio and the probability of backtest overfitting. Only a structural guard
  stops it: tools that cannot express look-ahead, and data and scoring the agent cannot touch.

No public options research harness of real quality was found
([agent harnesses](../inbox/2026-10-16-options-harness-research/agent-harnesses.md)). Every working
harness in other fields splits the work into propose, run and judge; the judge is never the
proposer; the agent edits one fenced surface; memory sits on disk in an append-only log.

## The layers

The layer names come from The Carbon Layer's harness series; the general lessons are in
[agent-harness-design](agent-harness-design.md).

| Layer | What it does | What it deliberately does not do |
|---|---|---|
| Ideas | A queue of hypothesis cards: alpha axes, papers, forums, the desk's own findings | Treat a forum post or a paper as evidence; they are leads |
| Meta-harness | Code that walks versioned blueprints and runs agents within limits | Put a model in charge of the order of steps |
| Agents | Specialists (scout, card reviewer, feature miner, combiner, strategist, critic, replicator), each with one job, its own tools and permissions | Grade its own work, or coordinate other agents |
| Tools | Every calculation as tested code copied from the company repos | Let a model compute a number itself |
| Frozen layer | Data, labels, splits, cost model, pass bar, and the holdout | Change during a run, or accept a write from any agent |
| Proof | The strategy gate, and evals that test the harness itself | Trust a judge that was not checked against a person |
| Evolution | An improvement loop that proposes harness changes as pull requests | Merge its own changes, or touch the frozen layer |

The **frozen layer** is the centre of the design. Everything that measures a strategy sits there,
and agents can read it but never write it. This is the same rule as the held-out tasks of a
self-improving agent: what grades the work must be out of reach of what is graded.

## The rules every part follows

1. Code owns the order of steps; agents judge only inside a step (repo decision 0001).
2. Nothing that measures a strategy can be changed by an agent (0002).
3. A result is read from files and git, never from what an agent says it did.
4. Every number comes from tested code; Backtest-Engine's maths is canonical (0003).
5. No look-ahead; the **same-period rule** is checked before any test.
6. Every trial is recorded; records are added, never edited.
7. The holdout is sealed from agents and opened once per hypothesis (0004).
8. Limits live in code: time, attempts, variants, revisions, budget.
9. Authority only narrows; never granting beats denying.
10. The harness changes only through pull requests a person merges (0005).
11. No paid data, and no action on any live account.

## Data: the held year and the forward holdout

Research uses only the **held year**: SPXW same-day quotes, one a minute, 1 October 2025 to
30 September 2026, downloaded free and kept in `convex-hedge-strategy/data/` (never in the harness
repo). It splits into a **train half** (to 31 March 2026) and a **test half** (from 1 April 2026).
Both halves have been read many times, so neither is an unbiased final test.

The final test is the **forward holdout**: every trading day after 30 September 2026. A script
downloads these days while they are under a year old, when Databento does not charge. Only the
judge's code opens the folder, once per hypothesis, and it returns pass or fail, never a score.
The holdout starts small (about twelve days in mid-October) and grows by about 21 days a month.
It is also one regime of its own: a strategy that fails there may only have met a different
market, and the verdict says so.

A paid 2024–2025 year was first chosen as the holdout and then dropped when it turned out to cost
money; see *Open questions* for the record that still says otherwise.

## The validation discipline

**The trial ledger.** A **trial** is one evaluated variant: one strategy spec, on one sample, at one
pricing. Every run writes one append-only event file in a git-ignored `records/` folder; each line
carries the hash of the line before it, so an edit or a deletion shows as a break. The **trial
ledger** is not a file anyone writes: it is a view rebuilt from the `trial_recorded` events, with
run reports, trial cards and an index page as HTML (repo decision 0007). Because every candidate
passes through one evaluation entry point, the count cannot be under-reported.

**Count independent trials, not rows.** A 9:35 straddle and a 9:40 straddle are nearly one trial.
The ledger should report the raw count and a clustered count (López de Prado and Lewis's method
groups trials by the correlation of their returns). The 2014 bound of "about 45 configurations on
five years of data" counts *independent* configurations; on one year the safe number is far
smaller.

**The deflated Sharpe ratio.** AFML's probabilistic Sharpe ratio corrects the Sharpe ratio for the
sample length T, the skewness γ₃ and the kurtosis γ₄ of the returns:

- PSR(SR\*) = Φ[ (SR − SR\*)·√(T − 1) / √(1 − γ₃·SR + ((γ₄ − 1)/4)·SR²) ]
- The **deflated Sharpe ratio** (DSR) is PSR with SR\* set to the expected best Sharpe of N trials
  that have no skill; N and the variance of the trials' Sharpe ratios come from the ledger.
- AFML asks for DSR above 0.95. A pre-registered single hypothesis (N = 1) faces almost no deflation.

Negative skew and fat tails enlarge the denominator, which is the penalty a short-volatility book
needs. The same algebra gives the **minimum track-record length**: with assumed numbers (a daily
Sharpe of 0.1, γ₃ = −3, γ₄ = 20) a short-volatility claim needs about 1.5 years of days, so one
year cannot prove a claim of that size.

**Adapting AFML to 0DTE.** The unit of independence is the **trading day**, not the 30-minute
window, because windows of one day share the open, the volatility level and the surface. Folds
are whole days, with at least one day of embargo; PBO and combinatorial purged cross-validation
run on daily P&L. Sharpe flatters option selling, so the tail report (CVaR, worst day against
premium, drawdown) sits beside it.

**The strategy gate.** A strategy reaches a person only after every step passes, in order. The
research proposed twelve; the first build has steps 1–5 and 11 (`docs/design/evals.md`):

1. The hypothesis card is frozen and hashed before any evaluation data is read.
2. Look-ahead is impossible by construction; the truncation test proves it (cut the data at t,
   recompute, every earlier value stays the same).
3. Data checks: quote age, crossed quotes, strikes that existed at the decision time.
4. The edge survives the spread, and twice the spread.
5. The **pass bar**: one variant, picked by Sharpe on the train half, read once on the test half,
   significant after Benjamini–Hochberg correction, and profitable with the spread paid.
6. to 10. DSR, PBO, a spread of results over many splits, the tail report, and robustness across
   volatility regimes and neighbouring parameters. Designed; built when the evals can calibrate
   their thresholds.
11. The forward holdout, opened once, pass or fail.
12. A separate skeptic, in a fresh context, re-runs the work and may veto it.

## Build order

Each feature is one plan and one pull request. The order changed on 19 October: the ledger and
the tools come before the frozen layer, because the frozen layer guards against agents and no agent
exists before the meta-harness.

| Step | Feature | Done when |
|---|---|---|
| 1 | F1 Event stream and ledger | A test run writes an event file; the run report and index open in a browser |
| 2 | F2 Deterministic tools (data reader, copied chain/IV/Greeks maths, bucket test, local backtest, results card) | Each tool is tested on the held year; every call is in the ledger |
| 3 | F0 Frozen layer | One command prints the senior's 10:00 straddle baseline card on the train half, matching a hand check |
| 4 | F3 Meta-harness runtime | A toy blueprint runs, a planted false report is caught, a stopped run resumes |
| 5 | F4 Research blueprint and agents | One real idea goes from card to verdict |
| 6 | F5 Harness evals | Three runs give per-task pass fractions and confident-wrong counts |
| 7 | F6 Improvement loop | One change arrives as a pull request with a per-task table |
| 8 | F7 Idea sources and context pack | The scout writes a card from a forum post with its source |
| — | F8 Engine adapter | Parked until the senior's MCP server for Backtest-Engine exists |

## Status (2026-10-23)

- **Designed, not built.** Four pull requests are merged: the design (#1), the new build order (#2),
  the feature-loop setup (#3) and the F1 spec (#4). No code exists; `pyproject.toml` arrives with F1.
- **F1 waits for the senior.** Lalit asked for docs the senior reads before any build. There is no
  feature issue and no tickets yet. The spec: `docs/specs/event-stream-and-ledger.md`.
- **A second contributor** may continue with his own Claude; the handoff is `docs/handoff.md`.
- The Carbon Layer study notes are copied into the repo at `docs/research/carbon-layer/`.

## Where the repo answers

| Question | Page in `options-research-harness` |
|---|---|
| What no agent can change | `docs/design/frozen-layer.md` |
| The twelve research steps | `docs/design/research-loop.md` |
| The gate and the harness evals | `docs/design/evals.md` |
| Every question and decision | `docs/design/grilling-log.md` (Q1–Q52), `docs/design/decisions/` |
| What is still unknown | `docs/design/research-gaps.md` (G1–G12) |

## Open questions

- **Which record of the holdout stands?** The session log of 15–17 October names the 2024–2025 year
  as the sealed holdout; the repo replaced it with the forward holdout (Q36, Q41, decision 0004).
- **How small a holdout is too small** for a verdict (G12)? Twelve days cannot pass a short-vol claim.
- **Sharpe picks the variant** in the pass bar, yet the validation research says Sharpe is the wrong
  main number for a short-volatility payoff. Should the train-half pick use a tail-aware measure?
- **Which pass bar does the company use?** Its code lets any variant pass; its newer workflow page
  judges one (G3). The senior should be told.
- **How far do results move** on Backtest-Engine's 405-minute clock against the strategy repo's
  390 (G2)? IV levels from the two are not comparable.
- **Can the holdout folder be made unreadable** to every worker on Windows (G7)?
- **The eval design** (items, gold answers, thresholds) is parked (G1); so are gate steps 6–10.
- **The senior's MCP server** for Backtest-Engine is planned only; its interface is unknown (G11).
- Does the feature-loop skill run on the second contributor's machine? Not checked.

## Sources

- [Harness research, six lanes](../inbox/2026-10-16-options-harness-research/_brief.md):
  [validation](../inbox/2026-10-16-options-harness-research/validation.md),
  [agent harnesses](../inbox/2026-10-16-options-harness-research/agent-harnesses.md),
  [MCP and tools](../inbox/2026-10-16-options-harness-research/mcp-and-tools.md),
  [options backtesters](../inbox/2026-10-16-options-harness-research/options-backtesters.md),
  [alpha axes](../inbox/2026-10-16-options-harness-research/alpha-axes.md),
  [Jev](../inbox/2026-10-16-options-harness-research/jev-deep-dive.md)
- [Harness planning facts, 17 October](../inbox/2026-10-17-harness-planning-facts.md)
- [Carbon Layer study notes](../inbox/2026-10-17-carbon-layer-harness/00-index.md)
- [session-log](../session-log.md), entries of 15–17 and 19–22 October
- `options-research-harness`: `docs/design/`, `CONTEXT.md`, `docs/handoff.md`
