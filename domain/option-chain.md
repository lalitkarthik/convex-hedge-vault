# Option chain — `/chain`

Depth note. One reconstructed snapshot of every option quoted for one expiry, at one minute.
The screen the rest of the terminal is built out of: [structure-chain](structure-chain.md) prices
combinations of these rows, and backtests fill orders against them.

Surface overview in [platform-map](platform-map.md). Vocabulary in [GLOSSARY.md](../GLOSSARY.md).

## The snapshot model

Three coordinates fix what you are looking at: **asset**, **date**, **minute**. The minute is a
slider with prev/next steps and a position counter (`84/414` — the 84th of 414 minutes captured
that day). Nothing on the screen is live; everything is replay.

**The timezone and the multiplier follow the asset**, and the header states them rather than
assuming you know:

| | NIFTY | SPXW |
|---|---|---|
| Units | `INR · ×65 · IST` | `USD · ×100 · ET` |
| Expiries | weekly, then monthly, then quarterly | **daily** |
| Front DTE seen | 1.8d | 0.8d |
| ATM IV seen | 18.84% | 9.67% |
| Strikes on front expiry | 113 | 51 |

The multiplier is labelled *"Contract multiplier as of \<date\>"* — it is resolved per period, not
hardcoded. Backtest trades in 2024 carry lot 50; the 2026 chain shows ×65. The engine knows the lot
size changed. Do not carry one across dates.

## Expiry strip

A tab per expiry, each labelled with its own DTE — `13-APR 1.8d` … `29-DEC 177.8d`. Selecting one
changes the whole table **and the header**, because forward, ATM IV and row count are all
per-expiry.

## Forward is per-expiry, and it is not spot

At NIFTY 10-APR-2026 10:30, spot was **24,019.20**, and:

| Expiry | DTE | Forward | Basis | ATM IV | Rows |
|---|---|---|---|---|---|
| 13-APR | 1.8d | 24,021.96 | +2.76 | 18.84% | 113 |
| 29-DEC | 177.8d | 25,169.58 | **+1,150.38** | 14.07% | **11** |

Two things a trader has to take from this:

**The far ATM strike is nowhere near spot.** At the December expiry the money sits ~1,150 points
above the index. Building a "straddle at the money" off spot there would put you 1,150 points off
centre and hand you a directional position you did not ask for. This is the concrete reason
`payoff-project/CONTEXT.md` insists the model consumes Forward and never Spot.

**Treat the far forward with suspicion.** That +1,150 over 177.8 days implies roughly 9.6%
continuously-compounded carry, which is high, and it is fitted from a chain with **11 strikes**.
`payoff-project/CONTEXT.md` warns the forward "on a thin chain may not be recoverable at all" —
this is what that looks like in the wild. Row count is the tell: read it before trusting the
forward.

**Term structure was inverted** on this snapshot — 18.84% at 1.8d against 14.07% at 177.8d. Near
expiries carrying more vol than far ones usually means a known near-term event, and it is the
opposite of the textbook upward slope.

## Columns

Eleven per side, mirrored around a central STRIKE column, calls left and puts right. Eight show by
default; the hidden three are the second-order Greeks.

`OI · VOL · VANNA · VOLGA · CHARM · VEGA · THETA · GAMMA · DELTA · IV · LTP`

- **VANNA** — how delta moves when volatility moves
- **VOLGA** — how vega moves when volatility moves
- **CHARM** — how delta moves as time passes

Exposing these at all is a statement of intent: this is a vol-trading tool, not a payoff drawer.

## What is shared between a call and a put

At one strike and expiry, only **delta** and **theta** differ between the call and the put.
Everything else is identical, and that is not a display shortcut — it is what put-call parity
requires. Deltas differ by exactly 1, so anything derived from the *difference* cancels.

NIFTY 24,000, 13-APR expiry, 1.8 DTE:

| | Call | Put |
|---|---|---|
| Delta | +0.526 | −0.474 |
| Theta | −50.68 | −50.69 |
| IV | 18.84% | 18.84% |
| Vega | 8.08 | 8.08 |
| Gamma | 0.0010 | 0.0010 |
| Charm | +0.0104 | +0.0104 |
| Vanna | −0.0010 | −0.0010 |

**One IV per strike, not one per option.** Call and put IV match exactly at every strike. The
engine fits a single volatility per strike rather than inverting each quote separately — so an
IV here is a property of the strike, and a call/put IV gap can never be read off this screen.

**Vanna and charm change sign across the money.** Below the forward they run one way, above it the
other, crossing near ATM (vanna −0.0037 → −0.0010 → +0.0018 across 23,950 / 24,000 / 24,050).

## What time to expiry does to the Greeks

Same strike, same minute, two expiries — this single comparison contains most of what "structures
behave differently at different DTE" means:

| Greek at 24,000 | 1.8 DTE | 177.8 DTE | Effect |
|---|---|---|---|
| Vega | 8.08 | **73.47** | ×9 — long-dated options are the vol trade |
| Theta | −50.68 | **−2.74** | ÷18 — decay is a short-dated phenomenon |
| Gamma | 0.0010 | 0.0001 | ÷10 — gamma concentrates into expiry |
| Volga | 0.00 | **0.61** | dead at the front, alive at the back |
| Charm | +0.0104 | +0.0003 | delta stops drifting when expiry is far |
| Delta | +0.526 | +0.666 | not a mistake — see below |

The delta of +0.666 is the forward effect again: 24,000 is near the money for April and well
in-the-money for December, because December's forward is 25,169. Delta is measured against the
**forward**, so the same strike is a different moneyness at every expiry.

Theta and vega trade places as DTE grows. That single fact decides which expiry a structure belongs
in, and it is visible here without any modelling.

## Data caveats

**LTP is a last traded price, not a quote.** There is no bid or ask on this screen. Deep OTM
strikes trade rarely, so their LTP can be hours stale, and prices go **non-monotonic** across
strikes as a result — NIFTY puts ran 0.80, 0.75, 0.80, 0.80, 0.95 across 20,900→21,100, which no
live book would ever show.

**Greeks go blank where the IV solve fails.** Far-OTM rows show a price and dashes for every Greek.
The strike still exists and still has OI; it simply has no usable vol. A structure with a leg out
there is priced off a number nobody solved.

**Whole rows can be one-sided.** At NIFTY 26,000 on the December expiry the put has full data and
the call side is empty — that call never traded.

**The price column changed on the SPX chain.** By 2026-09-30 the lab's SPX chain and Structure
Chain label prices **MID ($)**, the bid/ask midpoint, not LTP. Checked on SPX 25-Sep-2026 09:31: the
7,710 straddle cell −25.90 equals the 7,710 call mid 13.80 plus the put mid 12.10. The LTP caveats
above still describe the NIFTY chain as mapped in August.

**SPX shows OI and VOL as 0 on every row** (25-Sep-2026), so liquidity cannot be judged from the
SPX chain.

**The late-session forward can jump.** At 15:51 on the 0DTE expiry the forward read 7,751.23 with
spot 7,740.75. The likely cause is stale or wide quotes feeding the parity fit. A rule that acts on
that forward acts on a bad mark.

Related, in the other repo: `payoff-project/docs/data-quality.md`.

## Same-day expiries (SPXW, read 2026-09-30)

**`DTE (NOW)` counts trading-day fractions.** It shows 0.96 d at 09:31 and 0.00 at 15:59 on a 0DTE
expiry. With it, the rule of thumb for an ATM straddle reproduced the screen:

- straddle ≈ 0.8 × F × IV × √(DTE / 252)
- 25.86 against 25.90 at 09:31; 16.4 against about 16 at 13:16

**On 0DTE, THETA equals the whole time value left.** The 7,710 call shows theta −12.10, which is its
mid 13.80 less 1.70 intrinsic against the forward. The column reports one day of decay, and on the
last day that decay is capped at expiry.

**An ATM straddle's delta is near zero, not exactly zero.** The call and put deltas differ by
exactly 1, so the straddle's delta is 2Δ(call) − 1. That is zero only where the call delta is
exactly 0.5, which under lognormal pricing sits slightly away from the forward. NIFTY 13-APR at
24,050 showed +0.515 / −0.485, a straddle delta of +0.030.

## Open questions

1. What exactly makes the IV solve fail — a price floor, a vol cap, or an arbitrage check? The
   boundary did not fall on a clean price.
2. How is the per-strike IV fitted, given call and put agree exactly? Parity-implied forward first,
   then one solve against the more liquid side?
3. Is the ×65 multiplier read from a contract-spec table or inferred? The tooltip says "as of", so
   something dated exists.
4. What is `VOL` as a column — session volume, presumably, but confirm against OI.
5. Are the 414 minutes every traded minute, or a fixed grid with gaps filled?
6. A study session on 2026-09-27 read the 13-APR forward at 10:30:59 as **24,066.72** against spot
   24,019.20; this note records **24,021.96** for 10:30. Did the minute, the dataset or the forward
   calculation change? A 47.52-point gap at 1.8 days is itself worth checking against data quality.
