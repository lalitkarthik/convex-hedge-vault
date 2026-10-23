> As of convex-hedge-strategy@292f816, 2026-10-23 (re-checked: the study guides and the smile notebook
> are unchanged since `4bcf653`; the descriptive notebook only adds one 249-day table)

# Notebook facts — the ledger

The facts of Meghav's two SPXW notebooks, each one held up against a live day, again and again,
until it stays. The figures are his; canon is `Strategy-Research/Guide/SPXW 0DTE descriptive
statistics.md` and `Strategy-Research/Guide/SPXW 0DTE smile study.md`. Map:
[strategy-research](../../domain/strategy-research.md).

## How a fact is repeated

- **Never as a question.** Claude states the fact, puts today's live number beside the notebook's,
  and says whether today agrees.
- **Three new facts a sitting**, in the order below, in the US sitting.
- **Each fact returns** one sitting later, then three, then seven, then every tenth. A sitting
  carries at most five returning facts, the longest overdue first.
- **Facts about a whole day** (range, close, a seller's result) cannot be read at 20:00 IST. They
  are checked at the next sitting, on yesterday, from the Spot + GEX candles.
- **In the India sitting** the same facts are held up against NIFTY and SENSEX. Nothing says they
  hold there; the tally is India's first evidence either way.
- **Every Friday** Claude sends one picture card of the week's facts with their live tallies.
- *Shown* lists the dates. *Live* counts live days that agreed out of days checked, US then India.
  *due* means the fact was shown and its day is checked at the next sitting.
  A day agrees when it is within a quarter of the notebook's usual figure (Claude's rule).
  Every live day is after 30 September, so the tally is also the only unseen evidence there is.

SPXW, options expiring the same day, 127 days to 30 September 2026. D is the descriptive
notebook, S the smile notebook. "Usual" means the median day.

## Part A — how the index moves

| # | Fact | Source | Where it shows live | Shown | Live |
|---|---|---|---|---|---|
| A1 | A usual day travels **0.72%** from low to high. Calmest 0.26%, widest 3.18%. | D A3 | Candles, next day | 5 Oct, 6 Oct | US 1/1 (5 Oct: 0.89%); India 0/1 (6 Oct: 0.95%) |
| A2 | A usual day ends **0.34%** from its 9:35 reading, about half its range. | D A3 | Candles, next day | 5 Oct, 6 Oct | US 0/1 (5 Oct: 0.51%); India 0/1 (6 Oct: 0.85%) |
| A3 | A usual day travels **twice** the distance it keeps (range ÷ open-to-close move, 2.00). | D A4 | Candles, next day | 5 Oct, 6 Oct | US 1/1 (5 Oct: 1.75); India 0/1 (6 Oct: 1.12) |
| A4 | **The morning moves most.** Realised vol is 14.7% in the first half-hour and 8–9% from 11:30. | D A5, S 4 | Candle size through the session | | |
| A5 | **The high or the low is set early or late.** Of 252 highs and lows, 64 came before 10:00 and 34 after 15:30. 14:00 is the quietest window. | D A6 | Candles, next day | | |
| A6 | **Five-minute moves reverse a little.** Below zero on 63% of days, median −0.05. | D A7 | 5M candles | | |
| A7 | **A wide day tends to follow a wide day** (+0.28). | D A8 | Yesterday's range against today's | | |
| A8 | A big overnight gap goes with a wider day, **weakly** (+0.17, the weakest finding). | D A8 | First candle against yesterday's close | | |
| A9 | **No weekday effect was found, nor a news-day one.** Four Fed days ran 1.59% against 0.72%, too few to settle it. | D A9 | Calendar | | |
| A10 | **Nothing says which way the day goes.** The gap matched the day's direction on 53% of days. | D A2b | Gap against the close | | |
| A11 | The first half-hour does **not** foretell the last (+0.13, not a finding). | D A5b | Candles, next day | | |

## Part B — implied volatility at the open

| # | Fact | Source | Where it shows live | Shown | Live |
|---|---|---|---|---|---|
| B1 | A usual day **opens at 8.0%** a year. Lowest 4.5%, highest 17.5%. | D B1 | ATM IV at 9:35; smile's open curve | | |
| B2 | Through the day the level runs **8.2% at the open, 6.9% in the early afternoon, 8.5% after 15:30**. | S 2 | ATM IV at the sitting | | |
| B3 | **Higher opening IV, wider day** (+0.55). By quarter of days: 0.50%, 0.66%, 0.82%, 0.97%. | D B2, C2 | Opening IV, then yesterday's range | | |
| B4 | **Opening IV says how wide, not which way.** | D C2b | Same | | |
| B5 | The usual day's move to the close is **0.63 of the implied move**; the average day's is 0.79. | D B3 | Straddle-implied move, then the close | | |
| B6 | The index **closed inside** one implied move on 73% of days, but was **never outside** it on only 46%. The usual range is 1.33 implied moves. | D B3 | Same | | |
| B7 | **0.63 does not mean options are dear.** Priced exactly, it would still be about 0.67, and 68% of days inside. | D B3 | — | | |
| B8 | **Opening IV echoes yesterday**: +0.58 with yesterday's realised vol, +0.46 with yesterday's range. | D B4 | Yesterday's range, today's opening IV | | |
| B9 | Opening IV was **below 5% on 2 days of 126**, and never below 4%. | D C6 | ATM IV at 9:35 | | |
| B10 | **IV at 10:30 ranks the days** by how much they then move (+0.77). | S 5 | ATM IV at the sitting, which is 10:30 ET | | |

## Part C — implied against realised

| # | Fact | Source | Where it shows live | Shown | Live |
|---|---|---|---|---|---|
| C1 | Opening IV was **above the realised vol that followed on 78 of 126 days**, by 0.97 points on the usual day. | D C1 | Opening IV, then the day | | |
| C2 | The **average** gap is only 0.39 points: a few days fall far short. The worst was 16.5 below. | D C1 | Same | | |
| C3 | Opening IV less yesterday's realised vol **did not sort the days**. | D C3 | — | | |
| C4 | When IV stands well above the morning's realised vol, **the rest of the day is quieter** (−0.39). Mostly a quiet morning carrying on. | S 5 | IV against the morning's candles | | |

## Part D — what a seller earns

| # | Fact | Source | Where it shows live | Shown | Live |
|---|---|---|---|---|---|
| D1 | The hedged short straddle won on **84 of 126 days**: usual day +2.45 points, worst −23.71, about **ten times** the usual gain. | D D2 | Strategies page | 6 Oct (India) | due: 6 Oct result lost with the page's history; check 8 Oct on 7 Oct |
| D2 | **Wider wins more often and earns less.** 25Δ strangle 90 days, 10Δ strangle 99 days. | D D2 | Structure chain; Strategies | 7 Oct (India) | India 1/1 (06-OCT set: 25Δ +20.10, 10Δ +12.05) |
| D3 | **Time value and movement nearly cancel**: the straddle's usual day earned 13.7 and lost 13.9. | D D3 | Strategy details | | |
| D4 | **The breakeven move for a minute is IV × index × √(one minute).** At 6.9% it was 1.69 points. | D D4 | ATM IV, 1M candles | | |
| D5 | Opened again every half-hour, **little is left once the spread is paid**: 0.05 to 0.55 points. | D D6 | Bid and ask on the chain | | |
| D6 | The bought straddle, unhedged, **lost on 79 of 126 days**, 22% of its price on the usual day. A few large days paid most of it back. | D D8 | Straddle price open to close | | |
| D7 | **Late in the day it is about movement, not volatility.** One vol point is worth 96 minutes of theta at 9:36, 31 at 14:00, 6 at 15:30. | D D7, S 8 | Greeks on the chain through the day | | |
| D8 | **The hedge is assumed free**, so every hedged figure is an upper limit. | D limits | Strategy fills | | |

## The smile

| # | Fact | Source | Where it shows live | Shown | Live |
|---|---|---|---|---|---|
| S1 | **Shape is steadier than level.** The 25Δ put carries 1.11 times ATM IV, between 1.09 and 1.14. | S 2 | Smile tiles: 25Δ put IV ÷ ATM IV | | |
| S2 | **Puts cost more than calls**: 1.44 times ATM at the 5Δ put, 0.94 at the 25Δ call, at 10:00. | S 2 | Smile curve | | |
| S3 | **Far calls turn up in the afternoon**: the 5Δ call is at 1.15 by 13:30. | S 2 | Smile against its open curve | | |
| S4 | **The smile narrows.** The 5Δ put sits 1.2% below the index at the open and 0.3% after 15:30. | S 2 | Smile's strike axis | 6 Oct | US 1/1 (6 Oct: 0.59% at 12:11, 0.51% at 12:56) |
| S5 | **IV and the index move against each other** in the same half-hour (−0.51). A 1% fall goes with about 3.2 vol points. | S 6 | Candles against ATM IV | | |
| S6 | **Skew and the index move against each other** too (−0.35). | S 6 | Candles against 25Δ put skew | | |
| S7 | A change in IV or skew says **nothing about the next half-hour's** index return. | S 6 | — | | |
| S8 | **Big minutes are six times as common** as a bell curve gives: 1.65% of minutes beyond three standard deviations. | S 4 | 1M candles | | |
| S9 | **Far options are costly to trade.** At 5Δ the spread is 5–9% of the price in the morning, over 20% late. At the money, about 1%. | S 9 | Bid and ask on the chain | | |

## Reading the tally

One live day proves nothing, and neither do ten. A fact the live days keep contradicting is
surfaced in the review beside the notebook's figure, not corrected here.
