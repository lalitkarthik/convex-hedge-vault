# Structures book — five paper positions a day

Readings alone do not teach what to do with them. Every sitting opens the same five structures on
paper, using the IV, the GEX levels and the structure chain to place them, and the next sitting
shows what each became. Part of [the plan](PLAN.md). **Paper only: nothing here is traded, and a
mid price is not a price anyone can deal at.**

## How the three tools are used

| Tool | What it answers | How it places a structure |
|---|---|---|
| **IV level** (header, [normal-ranges](normal-ranges.md)) | Is premium rich or thin for this root at this DTE? | Rich favours selling, thin favours buying. The verdict is written down before the result is known. |
| **Implied move** (ATM straddle ÷ spot) | How far do the options say the index goes? | It is the ruler: every short strike's distance is given in implied moves. |
| **Skew** (smile tiles) | Which side costs more, and by how much? | The dearer side is where a seller collects more for the same distance. A ratio sells the dear strikes and buys the cheaper ones on the same side. |
| **GEX walls and flip** (GEX, Spot + GEX) | Where may hedging hold the index, and where may it let go? | Short strikes go at or beyond R1 and S1. Spot above the flip is read as a market that damps moves; below it, one that feeds them. |
| **Structure chain** | What does this structure cost at every strike and width, and what is it exposed to? | The price grid picks the cell; the Δ, Γ, Ν, Θ views show the net exposure of that cell; *per contract* turns it into money. |

The GEX reading rests on one assumption, that dealers are long the calls and short the puts
([engine-dashboard](../../domain/engine-dashboard.md)). It is stated each time it is used.

## The five structures

| # | Structure | Strikes | What it is a bet on | Workshop |
|---|---|---|---|---|
| 1 | **ATM straddle**, sold | Call and put at the strike nearest the forward | The index moves less than the implied move | 1, 2 |
| 2 | **25Δ strangle**, sold | The 25Δ put and the 25Δ call, from the smile's dots | The index stays between two strikes about one implied move apart | 1, 2 |
| 3 | **10Δ strangle**, sold | The 10Δ put and the 10Δ call | The same, wider: wins more often, earns less | 2 |
| 4 | **Call ratio 1:3:2** | The ratio grid's cell whose sold strike is the first at or beyond R1 | The index rises a little, not a lot; sells the call wall | 5, 7 |
| 5 | **Put ratio 1:3:2** | The cell whose sold strike is the first at or beyond S1 | The index falls a little, not a lot; sells the put wall and the dear side of the skew | 4, 5, 7 |

- Structure 1 is also read the other way round, as a **bought straddle**: the same row with the
  sign turned. That is the bought straddle of the notebook's section D8.
- **The placing rule for 4 and 5 is Claude's starting choice**, made so the days compare. Rahul
  places his ratios where IV is elevated against its own history. When his rule is written down,
  it replaces this one and the book says so.
- Workshops are those of [teach/option-structures](../option-structures/PLAN.md). The book gives
  each workshop a live example; it does not replace one.

## What is written when a structure opens

In the day record, one row per structure:

- the time, the strikes and the DTE;
- the net premium at mid, and again with the spread paid (sold at the bid, bought at the ask);
- net delta, gamma, vega and theta from the structure chain;
- each short strike's distance from spot in implied moves, and whether it sits inside or outside
  the walls;
- for the ratios, the IV at the sold strike less the IV at the bought ones;
- one line: what the IV level, the skew and the GEX said about this structure today.

## What is written when it is looked at again

| Market | A set opens | It is marked again | It settles |
|---|---|---|---|
| SPXW | every sitting | at the end of that sitting | at the next sitting, from the closing level |
| NIFTY, SENSEX | at the first sitting of each weekly expiry | at every sitting until expiry | on expiry day, from the closing level |

Each look splits the change into its three causes, with the figures: **the move** (delta and
gamma against how far the index went), **time** (theta against the days gone) and **IV** (vega
against the change in the strike's volatility). What the three do not account for is written down
as left over, not explained away.

Every structure is held to expiry and **not hedged**. The hedged versions are the engine's own
instances on the Strategies page and the notebook's part D; the day record sets the three side by
side when they hold the same strikes.

## The running tally

One row per structure per root, updated at every settle. The rows behind it are in `days/`.

| Root | Structure | Settled | Above zero | Median | Worst | Best |
|---|---|---|---|---|---|---|
| SPXW | ATM straddle, sold | 1 | 0 | −5.55 | −5.55 | −5.55 |
| SPXW | 25Δ strangle, sold | 1 | 0 | −1.65 | −1.65 | −1.65 |
| SPXW | 10Δ strangle, sold | 1 | 1 | +2.70 | +2.70 | +2.70 |
| SPXW | Call ratio 1:3:2 | 1 | 1 | +0.05 | +0.05 | +0.05 |
| SPXW | Put ratio 1:3:2 | 1 | 1 | +0.05 | +0.05 | +0.05 |
| NIFTY | ATM straddle, sold | 1 | 0 | −20.97 | −20.97 | −20.97 |
| NIFTY | 25Δ strangle, sold | 1 | 1 | +20.10 | +20.10 | +20.10 |
| NIFTY | 10Δ strangle, sold | 1 | 1 | +12.05 | +12.05 | +12.05 |
| NIFTY | Call ratio 1:3:2 | 1 | 1 | +26.68 | +26.68 | +26.68 |
| NIFTY | Put ratio 1:3:2 | 1 | 1 | +3.48 | +3.48 | +3.48 |

NIFTY 06-OCT and SENSEX 08-OCT sets opened 6 October ([record](days/2026-10-06-india.md)).
NIFTY 06-OCT settled at the last candle, 22,776.10 ([record](days/2026-10-07-india.md)); the
candles from 15:16 to 15:28 are missing and at 22,717.70 the straddle is +37.43, not −20.97.
NIFTY 13-OCT set opened 7 October at 10:38.
First SPXW set opened 5 October ([record](days/2026-10-05-us.md)) and settled at about 7,775
([record](days/2026-10-06-us.md)). That close is known to about 2 points, and the call ratio and
the 25Δ strangle change sign inside that band. Second set opened 6 October at 12:11 ET.
The ratios are placed 10 points apart, about half an implied move: the grid's default of 50 leaves
one usable column on a same-day expiry.

## What the tally is not

- Not a backtest and not a result. A handful of days, opened at one clock time, at mid.
- Not comparable with the notebook's part D figures, which are hedged every minute for free.
- A reason to look closer when a structure keeps losing in a market the readings called quiet, or
  keeps winning on days the IV level called thin.
