# Market observation — plan

**Agreed 2026-10-05.** One sitting per market on every trading day, India and the US side by side.
First US sitting: Monday 5 October, evening. First India sitting: Tuesday 6 October, morning.

## Why

The 30 September meeting asked for it ([recap](../../meetings/30-09-26-recap.txt), items 9–10):

- **First focus is understanding**: how each underlying's IV behaves, per days to expiry, and what
  counts as low or high for it.
- **The new charts are the values to watch**: structure chain, gamma exposure, GEX with spot, skew
  at 25 and 10 delta.
- **Rahul's trades rest on that feel**: "place the ratio where IV is elevated", "buy subdued IV,
  sell elevated IV".

Observing means building a sense of normal, one reading a day, until an unusual reading stands
out without anyone pointing at it. Meghav's notebook is the same job done on six months of SPXW
history ([strategy-research](../../domain/strategy-research.md)). India has no such baseline, so
these records start one.

**Done when** Lalit can look at a reading for NIFTY, SENSEX or SPXW at a given DTE and say whether
it is low, usual or high, and what that would change in a trade.

## Where

| Market | Address | Session in IST | Sitting (default) |
|---|---|---|---|
| India | `india.convexhedge.ai` | 09:15–15:30 | **10:00**, 45 minutes |
| US | `spxw.convexhedge.ai` | 19:00–01:30 (an hour later from 2 November) | **20:00**, 45 minutes |

- **The same clock time every day.** IV decays through the session and GEX levels move, so
  readings compare day to day only at the same time.
- Outside its session an address answers 503. The map of the pages is
  [engine-dashboard](../../domain/engine-dashboard.md).
- Lalit signs in to the browser pane. Claude drives the pages and sends annotated screenshots,
  because the dashboard has no phone layout and inline widgets do not show on his phone.

## How a sitting runs

Claude teaches throughout: every figure is explained, with the answer stated. No questions, no
quizzes, no predictions asked for.

1. **The sweep (5 minutes).** Claude reads the fixed readings below from every page and adds one
   row per root to [normal-ranges](normal-ranges.md).
2. **The notebook's facts (7 minutes).** From [notebook-facts](notebook-facts.md): yesterday is
   closed out first, since a whole-day fact can only be checked once the day is over. Then three
   new facts and up to five returning ones, each stated with the notebook's figure and today's
   live number side by side. The ledger records the date and whether the day agreed.
3. **The day so far (8 minutes).** Two pages hold the session's history:
   - *Spot + GEX*: the candles since the open against the call wall, the put wall and the gamma
     flip. Where the index turned, where it ran through, when a wall moved.
   - *IV smile*: the curve now against today's open curve and yesterday's close curve. Whether the
     whole curve rose or fell, and whether one side moved more.
4. **One page in depth (15 minutes).** The page of the day, from the rotation below. Each figure on
   it is rebuilt from the chain once, so no number is taken on trust.
5. **The structures (10 minutes).** From [structures-book](structures-book.md): first what
   yesterday's five paper positions became, split into the move, time and IV. Then today's
   readings against [normal-ranges](normal-ranges.md), said plainly: premium rich or thin, which
   side dearer, spot above or below the flip. Then today's five are opened from those readings.
5a. **The deployed strategies, every sitting.** For each instance on the Strategies page: what it
   holds now, total and today's PnL (realised and unrealised), and a timeline of today's signals,
   fills and closed trades with their reasons. Yesterday's final result is read first, from the
   5D curve. Asked for by the team; reported as facts, with the rule explained at step 4.
6. **The sweep again, at the end.** A second row, so the sitting itself shows forty-five minutes
   of change.
7. **The record.** Claude writes `days/YYYY-MM-DD-<market>.md`, updates the ledger and commits.

## The concept ladder (since 2026-10-05)

Lalit knows the Greeks, the Taylor expansion of an option's price, and IV. Sitting 1 showed ten
new ideas at once, which was too many. From now on **a sitting teaches one or two concepts, two or
three a day across both markets**, in the order below. Each is derived first, then checked on that
sitting's live numbers. No term is used before its step; a reading that needs one is given as a
number only.

| Step | Concept | Taught |
|---|---|---|
| 1 | Taylor P&L of one option on a real day | 5 Oct |
| 2 | From IV to an expected move; why the straddle price equals it | 5 Oct |
| 3 | Theta against gamma: the breakeven move | 5 Oct |
| 4 | Reading the engine's strategies: entry rule, stop, hedge, and their PnL | 6 Oct |
| 5 | Put-call parity and the forward: where the implied index level comes from | 6 Oct |
| 6 | Intrinsic and time value; why decay speeds up on the last day | 7 Oct (India) |
| 7 | Delta as a label for a strike and as a probability: 25Δ and 10Δ | 7 Oct (India) |
| 8 | Skew and smile: IV by strike, risk reversal, butterfly | 7 Oct (India) |
| 9 | How the Greeks change through a 0DTE day: gamma gathers at the strike, vega fades | 7 Oct (India), worked out; live check on NIFTY's expiry day, 13 Oct |
| 10 | Ratios of Greeks: theta per gamma, vega per theta, vega per gamma, and what each compares | |
| 11 | Realised volatility: measuring it from candles; its pattern through the day | |
| 12 | Delta hedging: realised against implied; how often, and what it costs | |
| 13 | The volatility premium: implied above realised on most days, and the seller's rare large loss | |
| 14 | Bid, ask and mid: what a structure costs to trade | |
| 15 | Open interest against volume: what each can and cannot say | |
| 16 | Hedging as market flow: GEX at one strike | |
| 17 | Net GEX and the gamma flip | |
| 18 | Walls and pinning | |
| 19 | Reading the structure chain: the grid, net premium, net Greeks, per unit and per contract | |
| 20 | Strangles: payoff, breakevens, distance in implied moves | |
| 21 | Ratio spreads 1:3:2: payoff, where they win and lose | |
| 22 | Index and IV move against each other: what that does to a position | |
| 23 | IV by days to expiry: the weekly cycle in NIFTY and SENSEX, and expiry day | |

This replaces step 4 of *How a sitting runs* (one page in depth) and cuts the new notebook facts
from three a sitting to one, chosen to fit the concept. The sweep, the ledgers and the five paper
structures still run in full, in the background, and are reported in two or three sentences. The
market part of a sitting uses only concepts already taught, so it grows with the ladder. When the
ladder is done, sittings are observation only. Extended from ten steps to twenty-three on 5 and 6 October. Explanations are short paragraphs in Simplified
Technical English, not bullet lists.

## Making the notebook stick

One read of the notebook does not stay. Its facts are kept in
[notebook-facts](notebook-facts.md), about forty of them, and each returns on a widening gap: one
sitting later, then three, then seven, then every tenth. A fact is never asked for. It is shown
again, each time against a different real day, until today's number is read with the notebook's
already in mind. Every Friday Claude sends one picture card of the week's facts and their live
tallies. The India sitting holds the same facts up against NIFTY and SENSEX.

## Using the readings: five paper structures

Watching is not enough; the readings have to place something. Every sitting opens the same five
structures on paper: a sold ATM straddle, sold 25Δ and 10Δ strangles, and a 1:3:2 ratio on each
side. [structures-book](structures-book.md) says how the IV level, the implied move, the skew,
the GEX walls and the structure chain each choose a strike, what is written at the open, and how
each position is taken apart at the next sitting. SPXW opens a set every sitting; NIFTY and SENSEX
open one per weekly expiry and mark it daily.

## The fixed readings

Taken per root, at the start and the end of every sitting.

| Reading | Page | Why it is watched |
|---|---|---|
| Spot, forward, DTE | any header | Where the market is and how much time the options hold |
| ATM IV | header | The level of volatility; the figure "low or high" is about |
| ATM straddle price, as a share of spot | structure chain | The move the options charge for |
| 25Δ put skew, risk reversal, butterfly, skew slope | IV smile | The shape: how much more downside costs than upside |
| 10Δ put IV, 25Δ put IV, 25Δ call IV | IV smile | The points Rahul's ratios are placed on |
| Net GEX, gamma flip, R1, S1 | GEX | Where hedging may pin the index or let it run |
| Day's high, low and range so far | Spot + GEX | The movement that actually happened |
| Each strategy's PnL and number of hedges | Strategies | What a real short-gamma book did with that day |

## The rotation

Week one learns the pages. Week two follows a theme across them.

| Sitting | US, SPXW (0 DTE every day) | India, NIFTY and SENSEX |
|---|---|---|
| 1 | Mon 5 Oct — header and option chain on a same-day expiry; the implied move from the straddle; opening IV against the notebook's 8.0% | Tue 6 Oct — header and option chain on **NIFTY's expiry day**; SENSEX two days out beside it |
| 2 | Tue 6 — IV smile and its five tiles; the open curve against now | Wed 7 — IV smile; NIFTY's new weekly at its longest DTE |
| 3 | Wed 7 — GEX and Spot + GEX; why SPXW's open interest is a morning figure | Thu 8 — GEX and Spot + GEX on **SENSEX's expiry day** |
| 4 | Thu 8 — structure chain; the 25Δ and 10Δ strangles of the notebook's part D, priced live | Fri 9 — structure chain; the 1:3:2 ratio grid Rahul trades |
| 5 | Fri 9 — Strategies: each SPXW instance's entry, fills and PnL against the day's path | Mon 12 — Strategies: `nifty-straddle`, its hedges traced against the candles |
| 6 | Mon 12 — theme: IV through the day on a 0 DTE, open to close | Tue 13 — theme: IV by DTE, the second pass over each day of the week |
| 7 | Tue 13 — theme: implied move against the move so far | Wed 14 — theme: skew by DTE; is the put side dearer nearer expiry |
| 8 | Wed 14 — theme: skew through the day | Thu 15 — theme: did the walls hold; NIFTY against SENSEX |
| 9 | Thu 15 — theme: did the walls hold | Fri 16 — theme: implied move against the move that happened, all week |
| 10 | Fri 16 — review | Mon 19 — review |

A day the market is shut, or a sitting missed, moves the rotation on by one. Nothing is skipped.

## The review

After ten sittings per market, Claude reads every day record and
[normal-ranges](normal-ranges.md) and writes what held up into `domain/`: what is low, usual and
high IV for each root at each DTE, and how the skew and the walls behaved. That note is canon;
the day records stay raw record. SPXW conclusions are checked against the notebook, and any
disagreement is surfaced, not chosen silently.

## The record of one day

```
# YYYY-MM-DD — <market>, sitting N
Readings      the two sweep rows, per root
Notebook facts   yesterday closed out; each fact shown, its figure, today's figure, agrees or not
The day so far   what the candles, levels and curves did, with times
Page of the day  what was learned on it, each figure rebuilt once
Structures       yesterday's five settled or marked; today's verdict; today's five opened
Strategies       per instance: position, PnL, and the day's timeline of signals and fills
Not explained    anything that looked wrong or was not understood
For the team     three lines Lalit can paste to Rahul, Bilal and Meghav
```

Screenshots sent during the sitting are kept in `days/assets/` only when the record cites them.

## Beside this plan

- **Meghav's notebook**, parts B to D: Lalit reads it himself. Its facts are repeated here, in
  notebook order, so a sitting may show a fact before he has reached that part.
- **Option structures**: [teach/option-structures](../option-structures/PLAN.md), nine workshops,
  whenever there is time. A sitting here may borrow a live example for a workshop; it does not
  replace one.

## Defaults Lalit can change

- The two clock times, 10:00 and 20:00 IST.
- Forty-five minutes per sitting.
- Ten sittings before the review.
