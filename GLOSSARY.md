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
`NOT VALIDATED` state. What authors an Echo strategy, and what validation checks, is not yet known.

**Fork**:
Taking a copy of an existing strategy to modify. Offered on every strategy page beside New Run.

**Signal**:
A named, tagged rule that fires on a candle to open or close a position. A strategy is a set of
signals evaluated per candle, not a script that runs start to finish.

**Group / Instance**:
The two identifiers that reassemble individual legs into the structure they belonged to. Legs
sharing a group were one trade.

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

**GEX**:
Net gamma exposure by strike, in currency per index point — how much the dealer community must
trade for each one-point move. Inferred from open interest under an assumption about who is on
which side, never observed.

**Gamma Flip**:
The level where net GEX crosses zero. Above it dealer hedging conventionally damps moves; below it
it amplifies them.

**Call Wall / Put Wall**:
The strikes carrying the largest positive and negative gamma exposure. Read as where hedging
pressure is heaviest, not as price predictions.

**PCR**:
Put open interest divided by call open interest, across the expiries in view.

**Reserve Table**: (inferred)
A DTE-keyed schedule of how much capital a hedged strategy holds back — more near expiry, where
gamma forces frequent re-hedging.

**Synthetic Forward**:
The instrument a delta hedger trades, built from options rather than from a futures contract.
Used because no futures series exists in the data — the same absence `payoff-project` refuses to
paper over.

**Regime**:
A field stamped on every backtest diagnostic row and filterable in the UI, intended to classify
market conditions at a decision. **Currently empty on every row.**

## The feed engine (`delta-exchange-payoff`)

Canon for these is `delta-exchange-payoff/CONTEXT.md`; this section holds only the terms vault notes
use. The map is [feed-engine](domain/feed-engine.md).

**Split mode / Monolith**: The seven-service composition over Redis (`DELTA_BUS=redis`), and the
default single process with an in-process bus.

**Stream / Consumer group**: A stream is one Redis key of entries; a consumer group is one service's
place in it. Never used for each other.

**Lossless / Drop-oldest**: A subscription that reads through a group and drops nothing (`store`),
and one that keeps only the newest and counts what it skipped (the chain cache).

**Retention**: Thirty minutes, by age. What a restarted `store` can still recover.

**Seal**: Closing a minute's bucket. Final — a minute sealed while its data is unread is lost.

**Store flush**: Writing sealed bars to Parquet every 300 s; the only durability boundary.
_Avoid_: save, write, persist

**Watermark / Checkpoint / Generation**: The last flushed entry per stream; the file holding the
watermarks; the number in a flush file's name. See [bar-store](domain/bar-store.md).

**Ladder**: The chain as the screen shows it, rows ascending by strike.

**Computed chain**: Our own IV, Greeks and forward, beside the venue's reference figures.

**`measured` / `assumed` / `derived`**: The provenance tag every number carries — observed in a named
run, chosen by a person, or computed from the other two. One origin each, never re-tagged.

**Instance**: One EC2 machine. _Avoid_: box, node.

## Collisions between the two

Recorded rather than reconciled, as [platform-map](domain/platform-map.md) does for `payoff-project`.

- **Tag.** On the terminal, a leg's exit reason. In the engine, a number's provenance.
- **Instance.** On the terminal, half of the Group / Instance leg identifier. In the engine, an EC2 machine.
- **Signal.** On the terminal, a rule that fires on a candle. In the engine, what an adapter reports
  about its socket (the connection signal).
- **Run.** On the terminal, one backtest execution. In the engine, one measurement window, named with its dates.
- **Snapshot vs Ladder.** Both are one chain at one moment; the terminal's is reconstructed from
  history, the engine's is live and rebuilt on arrival.
