# Convex Hedge Glossary

Canonical terms as Convex Hedge uses them. One or two sentences each: what the term *is*. Where
several words name one concept, pick one and list the rest under `_Avoid_`.

Sourced from the terminal itself, [platform-map](domain/platform-map.md). Terms marked
**(inferred)** are read off the interface and not yet confirmed by anyone at the company.

## The terminal

**Terminal**:
`app.convexhedge.ai`. An options backtesting terminal over historical index option data. It replays
the past minute by minute; it does not route orders.

**Snapshot**: (inferred)
The reconstructed option chain for one asset at one date and one minute. Every research screen is a
view of a single snapshot, and the time slider moves between them.

## Structures

**Structure**:
A multi-leg option position priced as one thing — a straddle, a strangle, a ratio spread. The unit
the Structure Chain quotes.
_Note_: `payoff-project` deliberately bans this word and calls the object a Strategy. On the
terminal they are different things; see **Strategy**.

**Structure Chain**:
A grid that prices a whole family of structures at one minute at once. Rows are strikes, columns are
**offsets**; the `D=0` column is a straddle and each wider column is a strangle.

**Offset**:
The distance in index points from the anchor strike to each wing, forming the columns of the
Structure Chain. `D` in the grid header.

**Feature**:
Which quantity the Structure Chain grid displays — price, IV, delta, gamma, vega, or ΔOI. Changing
the Feature repaints the same structures in a different unit.

**Basis**:
Whether numbers are shown **per unit** of the index or **per contract** (premium × lot size). A
toggle, not a stored property.
_Avoid_: units, multiplier view

## Strategies and runs

**Strategy**:
A parameterised, backtestable rule — entry time, exit time, DTE bounds, premium targets — that
opens and closes structures over a date range. Not a shape; the shape is in the name.

**Registry**:
A strategy that ships with the engine.

**Echo**: (inferred)
The other source a strategy can come from, distinct from Registry, and able to sit in a
`NOT VALIDATED` state. What authors an Echo strategy is not yet known.

**Run**:
One execution of a Strategy over one date range with one capital base. Versioned — a strategy
accumulates run history, and runs can be re-run.

**Capital Track**: (inferred)
The basis on which a run's returns are expressed: performance measured against the capital
**anchor** the run started with, rather than against a compounding balance.

**Anchor**:
The starting capital a run's equity curve and percentage returns are measured from.

**Tag**:
The recorded reason a leg opened and closed, written as a pair — `premium-target-entry → time-exit`,
`→ profit-take`, `→ EXPIRY`. The exit-reason audit trail.

**Cost Model**:
The named, versioned fee schedule applied to a run — `ibkr_per_contract v1`, `india_legacy_pct v1`.
Costs are part of the run's identity, not a post-hoc adjustment.

## Prices and vol

**Spot**:
The index level itself.

**Forward**:
The forward price implied by the chain for a given expiry. Displayed alongside Spot, never merged
with it, and it is Forward that smile offsets are measured from.
_Avoid_: futures price, fair value

**ATM IV**:
The implied volatility at the strike nearest the money, shown in the chain header.

**Smile**:
Implied volatility plotted across strikes for one expiry, with the x-axis labelled both by strike
and by offset from Forward.

**Realised Volatility (RV)**:
Volatility computed from the underlying's own past movement, by a chosen estimator —
close-close, log return, Parkinson, Garman-Klass, Rogers-Satchell, or Yang-Zhang — over a window.
Set against IV to ask whether options were dear or cheap.

**Constant Maturity**: (inferred)
Holding DTE fixed while time advances, by rolling across expiries, so an IV series is comparable
over long spans. Contrasted with **front**, which follows the nearest expiry.

**GEX**: (inferred)
Gamma exposure, the second view on the open-interest screen. Not yet loaded; confirm before use.
