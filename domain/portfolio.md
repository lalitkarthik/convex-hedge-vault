# Portfolio — `/portfolio`

> Stamped 2026-08-24. The screen is new — the only portfolio on it was created that day.

Depth note. Combines finished [backtest](backtest-engine.md) runs into one book and reports what
the combination does that the runs alone do not.

## A leg is a run, not an option leg

**The vocabulary collides with everything else in this vault.** Here a **leg** is one completed
backtest run. A two-leg portfolio is two runs held together, and each of those runs may itself
trade four-legged iron condors. Read "leg" on this screen as "strategy allocation".

Composition names the strategy, a **run id**, the window, the capital and a **state** (`OK`).
The run id is what makes a leg reproducible — the same strategy run twice with different
parameters gives two different legs.

## Building one

**New portfolio** and **Edit legs** open the same picker: every finished run, filterable by
strategy and by live-from / live-to. Pick runs; capital is summed from them rather than entered.

**One underlying per book.** Runs on another asset stay listed but carry
*"Different underlying — this book is SPXW"* against them. The first leg fixes the asset.

Actions on a saved book: **Rename**, **Edit legs**, **Delete**.

## Capital track only

Stated in the header, and worth understanding rather than skipping:

> A portfolio has no per-unit track, because "one unit" means something different in every leg.

A single run offers a **Capital / Per Unit** toggle. A portfolio cannot: one unit of a NIFTY
strangle and one unit of an SPXW condor are not comparable quantities, so only the capital track
is defined. The same reasoning appears again in the day log — see below.

## Date range is an intersection

The window is the **intersection** of the legs' windows, not their union. A leg that stops early
truncates the whole book. `FROM` / `TO` / `ALL` re-slice it.

## Overview

Everything a single run reports, plus three things only a combination can have.

**Headline** — net P&L (% and absolute), annualised, max drawdown, Sharpe, Sortino, Calmar, and
**peak margin** with its utilisation and the date it occurred. Combined equity curve with a
drawdown overlay, anchored to summed capital; the overlay can be hidden, and zoom/pan reset.

**Performance** — total P&L, portfolio capital (`Σ legs`), total and annualised return, average
daily and weekly return; max drawdown with absolute and **duration**, the three ratios, annualised
**downside deviation**; **VaR 95** and **CVaR 95**.

**Contribution** — per leg: capital, P&L, **share of total**, Sharpe, max drawdown. This is where
an apparently even split shows up uneven: on `FF-Test`, two runs of the *same* strategy at the
same capital contributed 47.0% and 53.0%.

**Diversification** — the reason the screen exists:

- A **correlation matrix** of daily P&L between legs. The two `FF-Test` legs correlate **0.37**
  despite being the same strategy on the same asset over the same window — different parameters
  produce genuinely different day-to-day behaviour.
- A **no-diversification baseline**: max drawdown against `Σ legs`, and volatility against the
  `ρ=1` bound, each with the benefit stated. On `FF-Test`, −$4,191 against −$4,783 summed
  (+12.4%), and 4.9% against 5.9% (+17.1%).

That second table is the honest version of "diversification helps" — it names the counterfactual
instead of asserting the benefit.

## Day log

Merged daily ledger, exportable as **merged daily CSV**: date, P&L, return, cumulative return,
equity, margin, utilisation.

**Expanding a day gives a per-leg breakdown** with a genuine subtlety: each leg shows both
**return (leg)** — against its own capital — and **return (book)** — against the portfolio's. The
`BOOK` row deliberately leaves return (leg) as `—`, and says why:

> The legs' own anchors are different capitals, and averaging them would denominate against
> nothing.

P&L, book return and margin sum down the column; leg return does not. Averaging the leg returns
would be the natural mistake and the screen refuses to make it.

## Trades

Every leg of every trade across the whole book, tagged with which run produced it
(`spxw_0dte_strangle · f9890597`). 936 rows on `FF-Test`.

Filters: **strategy** (by run id, not just name), **tag**, **side**, **result** (win / loss).
CSV export.

Columns match the run-level trades tab — entry, exit, structure, strike, type, side, entry and
exit price, quantity, lot, hold, tag, gross P&L, cost, net P&L, group, instance.

**Tags carry entry and exit together** — `premium-entry → stop-loss`,
`premium-reentry → profit-take`, `premium-reentry → EXPIRY`. That pairing is more legible than the
run-level view and makes re-entry behaviour visible: on 2026-02-03 one run stopped out, re-entered,
stopped out again, re-entered a third time.

## What to check before trusting a book

- **Peak utilisation.** `FF-Test` peaked at 93.6% of capital on a single day. A book that nearly
  exhausts its margin has no room for a leg to be added or a bad day to be survived.
- **Correlation is measured, not assumed.** Two legs of the same strategy at ρ=0.37 is the useful
  case; two legs at ρ=0.95 would be one strategy wearing two hats.
- **The intersection window can hide a leg's worst period.** If one run covers Feb–Jul and another
  Jan–Dec, the book only ever sees Feb–Jul.
- Everything inherits the run's caveats — see [backtest-engine](backtest-engine.md), especially
  sizing artefacts and margin not reconciling between long and short books.

## Open questions

1. What sets a leg's `STATE`, and what states exist besides `OK`?
2. Can the same run be added twice, and does the picker prevent it?
3. Is capital always summed from the legs, or can a book be given its own capital?
4. Does the correlation use net or gross daily P&L?
5. What happens to a book if one of its runs is deleted?
6. Is there any cross-asset book, or is one-underlying a hard rule?
