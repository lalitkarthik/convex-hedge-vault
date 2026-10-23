# Glossary — research and the options research harness

> Split from [GLOSSARY](../GLOSSARY.md) on 2026-10-23, when the October research was promoted. These are
> the terms of the feature tests, the volatility research and the harness. Canon for the harness is
> its repo's `CONTEXT.md` (`options-research-harness/CONTEXT.md`); this note holds the terms vault
> notes use.

## Testing a feature

**Feature**: A number worked out for each window that might sort the option seller's return in it.
_Note_: the terminal's FEATURE selector and the workflow's "feature" (a unit of build work) are other
things; see the collisions in [GLOSSARY](../GLOSSARY.md). Map: [feature-testing](feature-testing.md).

**Bucket test**: Bilal's method. Sort 30-minute windows by a feature into equal groups, and test
whether the groups' short-straddle return distributions differ in centre, spread and tails.

**Seen days / fresh days**: Days read before a claim was written, against days opened once afterwards
to test it. A claim is checked only on fresh days.

**Window ratio**: Δ² ÷ (2Γ) at the window's end, over the theta earned in the window. Above 1, the
seller lost the window. Map: [backtest-lab](backtest-lab.md).

**Variance ratio**: RV² ÷ IV². At 1 the hedged option buyer breaks even.

**Pace**: Two meanings — IV ÷ RV on Bilal's sheet; (RV ÷ IV)², the variance ratio, on the trading
engine's IV vs RV page. Say which.

**Gap**: IV − RV, in volatility points.

## Volatility

Map: [realised-volatility-estimators](realised-volatility-estimators.md).

**Parkinson**: Realised volatility from the high-low range only.

**Garman-Klass**: Adds the open and close to the range; assumes no drift.

**Rogers-Satchell**: Free of drift; does not handle the overnight gap.

**Yang-Zhang**: Handles both drift and the overnight gap. None of the three above handles the gap.

**Time-of-day profile**: The usual share of a session's variance in each 15-minute bucket, used to
scale a part day.

**Long gamma**: A bought option position, usually hedged, that gains from movement and pays theta.
Map: [long-gamma-research](long-gamma-research.md).

**Hedge band**: Re-hedge when Δ ÷ Γ passes a share of the implied move left; the desk uses one sixth.

## The harness

Map: [options-research-harness](options-research-harness.md); principles:
[agent-harness-design](agent-harness-design.md).

**Harness**: Everything around a model that decides what it sees, what it can do, what it remembers,
and how its work is checked.

**Meta-harness**: Code above several harnessed agents that coordinates them as workers, so no model
holds the process.

**Editable surface**: The short, versioned list of what a self-improvement loop may change.

**Frozen layer**: The data, labels, splits, cost model and pass bar. Agents may read it and never
write it.

**Held year**: The free SPXW year we hold, 2025-10-01 to 2026-09-30: train half to 31 March, test
half from 1 April.

**Forward holdout**: Trading days after 2026-09-30, sealed from agents, opened once per hypothesis,
returning pass or fail only. It replaced the 2024–25 sealed year on 2026-10-17.

**Trial**: One evaluated variant — one strategy spec, on one sample, at one pricing.

**Trial ledger**: The table of every trial, rebuilt as a view from hash-chained `trial_recorded`
events. The honest trial count.

**Deflated Sharpe ratio (DSR)**: The probabilistic Sharpe ratio measured against the best Sharpe
expected from N no-skill trials. López de Prado asks for above 0.95.

**PBO (probability of backtest overfitting)**: The share of train/test splits where the in-sample best
trial ranks below the median out of sample.

**Same-period rule**: A reading that uses information from the period it explains fails, however
significant it is.

**Hypothesis card**: Name, mechanism, prediction, kill line, data needed, evidence, whether already
tested, and why it may fail. Map: [strategy-research-method](strategy-research-method.md).

## Places

**Lab**: `lab.convexhedge.ai`, the in-house copy of the terminal, where every registry strategy runs.
**research.convexhedge.ai** is the copy for external beta users. Map: [backtest-lab](backtest-lab.md).

## Collisions with other notes

- **Regime.** The terminal's field, empty on every row; Bilal's four volatility × direction regimes;
  the harness's *conditioning axis*, any axis known at decision time.
- **Bucket.** The feed engine's minute bucket; the time-of-day profile's 15-minute bucket; Bilal's
  feature quartile.
- **Card.** The trading engine's strategy cards; hypothesis cards; the harness's trial cards; the
  signal card asked for on 20 September.
- **Run.** Add: in the harness, one append-only event file per run.
- **Holdout.** `convex-hedge-strategy`'s spent hold-out (its decision 0015) against the harness's
  forward holdout.
- **Clock.** SPXW has three: `Backtest-Engine` counts 405 minutes a session (the harness's canon), the
  strategy repo 390, the trading engine whole sessions ÷ 252. IV levels on different clocks do not
  compare.
