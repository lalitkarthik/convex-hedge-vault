# Open interest — `/oi`

Depth note. Two tabs: **OI** and **GEX**. Both fully built. The page needs an asset, a date and a
minute before it renders anything, and the date picker only enables days that have data.

Unlike the other screens this one aggregates **across expiries** — a multi-select lists every expiry
with its DTE, and the header states how many are in view (`NIFTY · 1 EXP · 31 STRIKES`).

A strike-window control (5 / 10 / 15 / 20 / 25 / ALL) sets how far either side of the money to draw.

## OI tab

Horizontal bars of call and put open interest by strike, with spot marked and **max call OI** and
**max put OI** flagged.

The header carries **call total**, **put total** and **PCR**. At NIFTY 10-APR-2026 09:15: calls
6.51 Cr, puts 3.91 Cr, PCR **0.60** — which is simply puts ÷ calls.

**OI change** can be shown over five lookbacks: **open · prev · 5m · 15m · 1h**. This is the ΔOI
capability that the [structure chain](structure-chain.md) lists but has not built. Here it works.

Change matters more than level. A large OI at a strike says positions exist; a large *change* says
they are being put on now, and the direction of the change is the only part carrying a timestamp.

## GEX tab

Net gamma exposure by strike, in **₹ crore per point** — how much the dealer community must buy or
sell for each one-point move in the index.

**Gamma flip** is the headline number: the level where net gamma crosses zero. At 10-APR-2026 09:15
the flip sat at **23,800.41** with spot at **23,895.50**, so spot was above the flip.

The conventional reading, worth holding loosely until someone at Convex Hedge confirms how the sign
is computed:

- **Spot above the flip** — dealers are long gamma and hedge against the move, selling rallies and
  buying dips. Ranges tend to hold and realised volatility is suppressed.
- **Spot below the flip** — dealers are short gamma and hedge with the move, amplifying it. Trends
  extend and realised volatility rises.

That is a direct bridge to [volatility](volatility.md): gamma positioning is one mechanism by which
realised volatility comes in under or over implied.

The screen also derives labelled levels from the GEX profile:

| | Label | Strike | GEX |
|---|---|---|---|
| R1 | call wall | 24,000 | +₹712.17 Cr |
| R2 | resistance | 24,200 | +₹560.15 Cr |
| R3 | resistance | 24,500 | +₹480.39 Cr |
| R4 | resistance | 24,300 | +₹375.84 Cr |
| S1 | put wall | 23,500 | −₹320.19 Cr |
| S2 | support | 23,700 | −₹218.51 Cr |
| S3 | support | 23,600 | −₹199.85 Cr |
| S4 | support | 23,400 | −₹120.07 Cr |

The ranks follow **GEX magnitude, not distance from spot** — R3 at 24,500 outranks R4 at 24,300.
They are strength ranks, not proximity ranks, and reading them as nearest-first would be wrong.

The **call wall** and **put wall** are the largest positive and negative concentrations. They are
where hedging pressure is heaviest, and so where a move most often stalls.

## Caution

These are inferred dealer positions, not observed ones. The exchange publishes open interest, not
who is long or short it. Every GEX model assumes a convention — customarily that customers buy
options and dealers take the other side — and that assumption is sometimes wrong. Treat the flip
and the walls as a hypothesis about where hedging flow sits, never as a fact about positioning.

## Open questions

1. What sign convention does the GEX calculation assume for dealer positioning?
2. Are the walls computed per selected expiry, or across everything in view?
3. Does GEX use the same per-strike IV the [option chain](option-chain.md) fits?
4. Is PCR computed on open interest only, or is there a volume variant?
5. What does `prev` compare against — the previous day's close, or the previous snapshot?
