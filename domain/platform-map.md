# Platform map — app.convexhedge.ai

The Convex Hedge terminal, surface by surface. A map of what exists and what each screen is *for*.
Depth notes live in their own files; this one never grows into them.

Mapped 2026-08-21 against **v0.1 · Phase 1**. Access is Google SSO, authorised accounts only.

## What the product is

An **options backtesting terminal** over historical Indian and US index option data. Not a
live-trading front end: there is no order ticket, no broker connection, no position blotter.
Everything is replay and research.

Two underlyings carry data: **NIFTY** (INR, IST) and **SPXW** (USD, US 0DTE).

The spine of the whole terminal is a **minute-level time machine**. Every research screen takes an
asset, a date, and a time, and exposes a minute slider (`208/414`) with prev/next-minute steps. You
are always looking at one reconstructed snapshot of the option chain, and you scrub it.

## The six surfaces

| Nav | Path | What it is | Depth note |
|---|---|---|---|
| BKT | `/backtest` | Backtest runs — the landing page. Every run with its performance | [backtest-engine](backtest-engine.md) |
| LIB | `/strategies` | Strategy library. 19 rules, the things backtests are run *from* | [strategies](strategies.md) |
| CHN | `/chain` | Option chain at one minute. Per-strike quotes and Greeks | [option-chain](option-chain.md) |
| STR | `/structure-chain` | Multi-leg structures priced across a whole grid at once | [structure-chain](structure-chain.md) |
| VOL | `/iv-surface` | Volatility: smile, and implied vs realised | [volatility](volatility.md) |
| — | `/oi` | Open interest and gamma exposure | [open-interest](open-interest.md) |

### `/backtest` — runs and results

Table across: strategy, org, underlying, period, capital, status, launched, and then the
performance block — Net P&L, total return, Sharpe, Sortino, Calmar, max drawdown, trades, avg/day,
win %. Rows carry **Show params**, **Rerun run**, **Delete run**.

A run detail page has four tabs — **Overview**, **Daylog**, **Trades**, **Diagnostics** — plus
version history (one run had 32 versions) and a **Capital / Per Unit** basis toggle.

Overview carries equity + drawdown curve, returns and risk blocks, VaR and CVaR at 95%, a daily
returns KDE, a monthly returns heatmap, best/worst day, order counts, average margin, and an
explicit **cost model** (`ibkr_per_contract v1` for SPXW, `india_legacy_pct v1` for NIFTY).
Charges ran 18.7% of returns on one SPXW run — costs are not an afterthought here.

Trades tab lists every leg: entry/exit time, structure, strike, type, side, entry and exit price,
qty, lot, hold time, tag, gross P&L, cost, net P&L, group, instance. Exportable as CSV.

The **tag** field records why a leg opened and closed — `premium-target-entry → time-exit`,
`→ profit-take`, `→ EXPIRY`. That is the exit-reason audit trail.

### `/strategies` — the library

19 strategies, filterable by source, status, owner, asset, and run count. Two sources:
**REGISTRY** and **ECHO**; Echo entries can carry a `NOT VALIDATED` status. Names describe the
structure and the regime — `daily_iron_condor`, `weekly_roll_short_straddle`,
`daily_straddle_delta_hedged`, `spxw_0dte_strangle`, `expiryday_strangle_premium_sl`.

Strategies are parameterised, not hand-drawn. One run's params: `max_dte`, `min_dte`, `entry_time`,
`exit_time`, `min_entry_premium`, `entry_premium_target`, `target_multiplier`.

### `/chain` — the option chain

Calls mirrored against puts around a centre **STRIKE** column. Per side: OI, VOL, VEGA, THETA,
GAMMA, DELTA, IV, LTP. Column set is configurable (`8/11` shown).

Header carries **SPOT**, **FORWARD**, **ATM IV**, **DTE**, row count, and an expiry strip with each
expiry's DTE (`13-APR 1.8D` … `29-DEC 177.8D`). Units are stated explicitly: `INR · ×65 · IST`.

Spot and Forward are shown as **separate numbers** — see [vocabulary](#vocabulary-collisions).

Far-OTM strikes show quotes but dashes for Greeks: below some premium the IV solve does not return.

### `/structure-chain` — the one to understand

Two tabs: **Straddle / Strangle** and **Ratio Spreads**.

Straddle/Strangle is a grid, not a list. Rows are strikes around ATM; columns are **offsets**
(0, 50, 100, 150, 200). Column `D=0` is a straddle; each column past it is a strangle of that width.
One screen therefore prices the entire straddle-and-strangle family at that minute.

Ratio Spreads gives three legs — **A / B / C**, each independently long or short (defaulting
long-short-long, a butterfly) — with independent call and put axes, drawn as two grids.

A **FEATURE** selector offers **PRICE · IV · Δ · Γ · Ν · ΔOI**, but in v0.1 **only PRICE is
built** — the other five are disabled and marked "Coming soon". The screen prices structures; it
does not yet show their Greeks. See [structure-chain](structure-chain.md).

Also carries a LONG/SHORT direction toggle, which flips the sign of every cell, and a
Per Unit / Per Contract basis toggle.

### `/iv-surface` — volatility

Two tabs: **Smile** and **IV vs RV** (`VOL` is the page's short name, not a tab).

Smile plots IV against strike, with the x-axis dual-labelled by strike and by **offset from
forward** — again forward, not spot. Comparison baselines can be overlaid: prev close, day open,
prev expiry, n-avg, primary. Observed skew was steep: ~55% IV on the low put wing against ~18% ATM.

IV vs RV is a date-range study: constant-maturity / front / user expiry, a target DTE, a window
and bar size, and **six realised-vol estimators** — close-close, log return, Parkinson,
Garman-Klass, Rogers-Satchell, Yang-Zhang.

### `/oi` — open interest

Takes asset, date, time, and a strike window (5/10/15/20/25/All). Two views: **OI** and **GEX**,
both fully built. Aggregates across expiries, unlike every other screen. GEX derives a gamma flip
level and labelled call/put walls. See [open-interest](open-interest.md).

## What is not built yet

v0.1 is further along than "Phase 1" suggests, but it is uneven, and the gaps are not where you
would guess:

- **Structure Chain shows price only.** Its IV, Δ, Γ, Ν and ΔOI views are disabled placeholders.
  The screen that looks like it answers "how do structures carry the Greeks" does not yet.
- **ΔOI exists elsewhere.** [open-interest](open-interest.md) has a working OI-change view over five
  lookbacks. The capability is built, just not wired into the grid.
- **`regime` is an empty field.** Backtest diagnostics can filter by it; nothing populates it.
- **Some strategy parameters are decorative.** They display as tunable and are hard-coded in the
  source. See [strategies](strategies.md) — this one can silently invalidate a study.

Everything else — the chain, both volatility tabs, both OI tabs, the whole backtest reporting
stack — is complete and behaves.

## Vocabulary collisions

The vault glossary is canon for Convex Hedge's terms. Where `payoff-project` uses a word
differently, both are recorded rather than reconciled:

- **Spot vs Forward.** Both agree, and both keep them separate. `payoff-project/CONTEXT.md` insists
  the model consumes Forward and never Spot; the terminal displays both side by side and measures
  smile offsets from Forward. This is the strongest point of agreement between the two.
- **"Structure".** `payoff-project/CONTEXT.md` bans the word and calls the thing a Strategy. The
  terminal makes **Structure Chain** a first-class screen, and uses **Strategy** for a parameterised,
  backtestable rule. They are not the same object.
- **Premium sign.** `payoff-project` treats a debit as positive Net Premium. The Structure Chain
  shows a long straddle as **negative**. Opposite conventions; check which one a number is in.
- **Lot size.** Both refuse to store it on a leg. The terminal applies it per period — lot 50 on
  2024 trades, ×65 on the 2026 chain.

## Pointers

- Our own engine's architecture, written as a design rather than inferred from modules:
  `delta-exchange-payoff/docs/design/hld.md` for the parts and the traffic between them, and
  `delta-exchange-payoff/docs/design/events.md` for the events that carry it. Different system
  from this map — theirs is a backtesting terminal, ours is a live feed — but the vocabulary for
  a chain, a leg and an expiry is shared, and the design documents are where ours is fixed.
- Backtest engine truth, once the repo lands — _access pending._
- Payoff and Greek maths, reimplemented independently: `payoff-project/docs/calculations.md`
- Vocabulary for that project: `payoff-project/CONTEXT.md`
