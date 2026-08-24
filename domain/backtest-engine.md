# Backtest engine — `/backtest`

Depth note. What a run is, what it reports, and which of its numbers can be trusted.

## A run

One execution of a [strategy](strategies.md) over a date range with a capital base. Runs are
versioned and accumulate history — one strategy had 32. Rows carry **Rerun** and **Delete**.

The list reports: strategy, org, underlying, period, capital, status, launched, net P&L, total
return, Sharpe, Sortino, Calmar, max drawdown, trades, avg/day, win %.

**Expanding a row (`▸`) prints the exact parameter JSON the run used**, alongside its capital.
This is the most useful control on the page and the easiest to miss. On an `spxw_0dte_strangle`
run: `max_dte`, `min_dte`, `entry_time`, `exit_time`, `inflow_pct`, `profit_pct`, `n_sl_cycles`,
`premium_pct`, `stop_multiples` (a list — `[1.25, 1.3, 1.4]`), `cooldown_minutes`,
`profit_reentries`.

Two consequences worth holding on to:

- **It is how a parameter sweep is read.** Thirteen runs of the same strategy over the same window
  differ only here, and their results range from +4.40% to +11.04%. Expanding each row is the only
  way to see which setting produced which outcome.
- **It is how the dead-parameter trap gets tested.** [strategies](strategies.md) records that some
  declared parameters are never read. Two runs whose JSON differs *only* in such a field, returning
  identical results, would prove it — and the same test would expose a field that does matter.

**`SELECT RUNS` is bulk delete, nothing else.** It relabels to `SELECT RUNS TO DELETE` and adds a
checkbox column. Not a comparison tool, despite reading like one. Cancel exits it.

A run page has four tabs and a **Capital / Per Unit** basis toggle.

## Overview

Returns, risk, distribution and cost, all at once:

- equity curve with drawdown overlay, anchored to starting capital
- total, annualised, average daily and average weekly return
- max drawdown and its duration, Sharpe, Sortino, Calmar
- daily returns distribution with KDE, mean, **VaR** and **CVaR** at 95%
- best and worst day, order counts, rejected orders, average margin
- monthly returns heatmap with year totals
- **cost model**, named and versioned

## Daylog

A per-day ledger, expandable per row, exportable as CSV: date, signals, orders, closed, open, DTE,
margin per unit, realized, unrealized, cost, daily MTM, total P&L, return on capital, cumulative
return.

Realized and unrealized are separated, which is the only way to tell a strategy that closes daily
from one carrying risk overnight.

## Trades

Every leg, not every position: entry and exit time, structure, strike, type, side, entry and exit
price, quantity, lot, hold time, tag, gross P&L, cost, net P&L, group, instance. CSV export.

**Group** and **instance** are what reassemble legs into structures — two rows sharing a group are
the two sides of one strangle.

## Diagnostics

The screen that matters most for learning to trade, and the least obvious.

It records **market state at every decision**: time, tag, event, spot, forward, ATM IV, DTE,
regime, status, net P&L. Filterable by tag, by entry/exit, by filled/rejected, and by regime.

So it answers *what did the market look like when this rule fired* — which is the question behind
"when should I enter". Sorting entries by ATM IV, or comparing the IV at profitable entries against
losing ones, is a study this screen supports directly.

Tags name the reason, and the vocabulary is richer than the trades tab suggests:
`premium-entry`, `premium-reentry`, `profit-take`, `stop-loss`, `time-exit`, and `EXPIRY`.
`premium-reentry` is worth noticing — some strategies re-enter after being stopped out, several
times a day.

**The `regime` column renders empty (`{}`) on every row.** The field exists and is filterable; it
is not populated.

## Costs are modelled properly

Every run names a versioned cost model — `ibkr_per_contract v1` for SPXW, `india_legacy_pct v1` for
NIFTY — and reports charges as a share of returns. On one SPXW run, charges were **18.7% of
returns**. A strategy trading 474 times is a different proposition gross and net, and this engine
will not let you forget it.

## What to distrust

**Returns can pass −100%, and that is sizing, not a bug.** `expiryday_long_strangle` reports −1037%
on ₹1,00,000. The per-leg arithmetic is exact — a leg bought at 3.45 and sold at 0.05 on 200 lots of
50 gives −34,000 precisely. What produces the headline is that the engine sizes ~10,000 units,
paying roughly ₹75,000 of premium per trade against a ₹1,00,000 account, and keeps sizing the same
after the account is notionally gone, while reporting against the fixed anchor.

So: **check whether a run is capital-constrained before believing any percentage it prints.**
A long option's loss is bounded per trade; it is the sizing and the anchor that are not.

**Margin does not reconcile between long and short strategies.** The NIFTY long-strangle run reports
average margin ₹646 per day while paying tens of thousands in premium. Long premium is paid in full,
so that number cannot mean what it appears to. The SPXW short-strangle run reports margin near its
full capital, which is plausible. Something differs between the two, and the label alone does not
say what.

**Rejected orders can be a large share.** 84 of 182 on one run — 46%. Most likely a premium filter
declining entries, which would make rejection a normal outcome rather than a failure. Unconfirmed,
and it changes how the number should be read.

**Everything inherits the chain's data caveats.** Fills are against last-traded prices with no
bid/ask, so no spread is ever crossed. See [option-chain](option-chain.md).

## Reading a run honestly

The `spxw_0dte_strangle` run is the one that looks good: +6.82% over six months, Sharpe 1.93,
max drawdown 1.87%, win rate 72.2%, profit factor 1.15.

Win rate 72% with a profit factor of only 1.15 is the signature of a short-premium strategy —
frequent small wins against rare large losses. The number to interrogate is not the Sharpe but
whether the sample contains a bad enough day. Cross-check the period against
[volatility](volatility.md): this run spans February to July 2026, which includes the stretch where
realised volatility crossed above implied. That it survived is the interesting fact, and it is worth
finding which days hurt.

## Where a run goes next

A finished run is the unit a [portfolio](portfolio.md) is built from. On that screen a run is
called a **leg**, and combining several exposes correlation and diversification that no single run
reports.

## Open questions

1. What exactly does margin per unit mean, and why does it differ so between long and short books?
2. What populates `regime`, and why is it empty?
3. What causes an order to be rejected?
4. Is there any capital constraint available, so a run can stop when the account is exhausted?
5. What is `org`, and what would a second one be?
6. What does Rerun do to run history — new version, or overwrite?
