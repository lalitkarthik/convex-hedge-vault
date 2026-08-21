# Strategies — `/strategies`

Depth note. The library of backtestable rules, and what one is made of.

Their source is proprietary and stays in their repo. What follows is structure and behaviour only —
no code. See the rule in [CLAUDE.md](../CLAUDE.md).

## The library

19 strategies at time of mapping. Filterable by source, status, owner, asset, and run count.

**Source** is either **REGISTRY** or **ECHO**. Registry entries ship with the engine and are owned
by the account viewing them. The single Echo entry (`spxw_0dte-spreads`) is owned by another person
and carries a **`NOT VALIDATED`** status that no registry entry has. What authors an Echo strategy,
and what validation would consist of, is still unknown — worth asking rather than guessing.

Naming is descriptive and consistent: structure, plus regime, plus modifier —
`daily_iron_condor`, `weekly_roll_short_straddle`, `daily_straddle_delta_hedged`,
`expiryday_strangle_premium_sl`, `spxw_0dte_put_spread`.

Run counts are lopsided. `spxw_0dte_strangle` has 32 runs and `expiryday_long_strangle` 11, while
nine strategies have never been run at all. The library is a shelf of intentions more than a record
of work.

## A strategy page

Actions: **New Run**, **Fork**, **View Python**. Tabs: **Details** and **Runs**.

Details renders a **structured decomposition of the source**, with line references, in six sections:

| Section | Holds |
|---|---|
| Instrument / data | id, version, permitted assets, parameter defaults |
| Structures | the leg shape and side — e.g. a straddle as `SHORT · SELL CE · SELL PE` |
| Signals / conditions | internal state the strategy carries between candles |
| Entry signals | the predicate that opens a position |
| Exit signals | the predicate that closes it |
| Hedging | the hedging method, its trigger, its target and its reserve policy |

Entry and exit read as plain predicates — *if no position is open and the time is 09:30, enter*;
*if a position is open and the time is at or past 15:00, exit*. The engine is candle-driven, and a
strategy is a set of rules evaluated per candle rather than a script that runs start to finish.

A parameters table lists each name, type, and default.

## Hedging

`daily_straddle_delta_hedged` is the reference for this, described as an ATM short straddle with a
delta hedger. Its hedge is a **synthetic forward** method: it fires when the structure's absolute
delta exceeds **0.20**, targets **0.0** with a **±0.05** tolerance, and sizes a reserve from a
DTE-keyed table — roughly half the capital reserved at 0 DTE, falling to about 15% at 7 DTE.

Two things worth taking from that:

**The hedge is a synthetic forward, not a futures contract.** That matches `payoff-project`, which
refuses to name a futures price at all because no futures series exists in the data. Both are
solving the same absence the same way.

**More reserve is held as expiry approaches**, because gamma rises into expiry and a delta-neutral
book needs re-hedging more often and more violently. The reserve table is that fact expressed as
capital.

## The trap: parameters that do nothing

On `daily_straddle_delta_hedged`, the parameters table exposes `capital`, `entry_time`, `exit_time`,
`delta_band`, `tolerance` and `default_dte` — but **only `capital` is actually read**. The rest are
declared so the registry and dashboard pick the strategy up, while the real values are hard-coded.
The source says so plainly in its own docstrings: entry and exit times are *"currently
informational"*, and the hedger configuration is *"currently hard-coded"*.

**Change `entry_time` on a run and the run will not change.** A parameter sweep over those fields
would produce a table of identical results that looks like a finding.

Whether this affects only this strategy or others too is unchecked, and it is the single most
important thing to verify before trusting any parameter study. Check each strategy's own text
before sweeping anything.

## Parameters seen in the wild

From `expiryday_long_strangle`: `max_dte`, `min_dte`, `entry_time`, `exit_time`,
`min_entry_premium`, `entry_premium_target`, `target_multiplier`. That is a strategy that buys legs
priced near a premium target within a DTE window, and exits at a multiple of what it paid — a
lottery-ticket structure rather than a directional view.

## Open questions

1. What is Echo, who can author into it, and what does validation check?
2. Which other strategies declare parameters they do not read?
3. What does Fork produce — an editable copy, and where does it land?
4. Does New Run allow arbitrary parameter values, or only those the strategy honours?
5. What hedging methods exist besides synthetic forward?
6. What is the full set of signal tags a strategy can emit?
