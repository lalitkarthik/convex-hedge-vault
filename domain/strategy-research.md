> As of convex-hedge-strategy@4bcf653, 2026-10-05

# Strategy research — Meghav's SPXW studies

`convex-hedge-strategy` (`MeghavPradeep/convex-hedge-strategy`, cloned to
`D:\Convex Hedge\convex-hedge-strategy`) studies past market data to find trading ideas and test
them before they go into the [trading-engine](trading-engine.md). It proposes no trading rule yet.
**Its own pages are canon; this note only says where to look and which figures we lean on.**

## Front doors

| Question | Page in the repo |
|---|---|
| What is this project? | `Strategy-Research/Home.md` |
| What did the descriptive study find? | `Strategy-Research/Guide/SPXW 0DTE descriptive statistics.md` |
| What did the smile study find? | `Strategy-Research/Guide/SPXW 0DTE smile study.md` |
| How is IV and each Greek worked out? | `Strategy-Research/Guide/Implied volatility and Greeks tables.md` |
| Why was a choice made? | `Strategy-Research/Decisions/` (0001–0019) |
| What does a word mean? | `Strategy-Research/Glossary/`, `CONTEXT.md` |
| Which ideas were tested? | `Strategy-Research/Strategies/` (empty so far) |

The two notebooks are `notebooks/spxw_descriptive_stats.ipynb` (parts A to D, sixteen tests, twelve
predictability tests) and `notebooks/spxw_smile_study.ipynb`. **The charts with a day slider do
not draw on GitHub.** Open the notebooks in VS Code or Jupyter from the local clone.

## What the data is

SPXW options expiring the same day, one quote a minute, 127 trading days from 31 March to
30 September 2026. The index is the implied forward read from option prices, so every range reads
slightly low. Other expiries, volume and open interest are not in the data.

## The yardstick for watching SPXW live

These are the few figures a live reading is set against. Everything else stays in the guide page.

| Reading | A usual day | The extremes |
|---|---|---|
| Range, low to high | 0.72% | 0.26% (12 August) to 3.18% (9 June) |
| Move from the 9:35 reading to the close | 0.34% | a fall of 1.95% (5 June) |
| Implied volatility at 9:35 | 8.0% a year | — |
| Move as a share of the implied move | 0.63 | 3.78 (5 June) |
| Implied minus realised volatility | +0.97 points | −16.5 points (9 June) |

- **Opening IV goes with how wide the day is, not with its direction.** Rank correlation +0.55
  with the range. Nothing known at the open said which way the day would go.
- **The morning moves most**; the afternoon before the last half-hour is quietest.
- **A hedged option seller won on two days in three or more, and the losing days were larger.**
  The short straddle's worst day cost about ten times what its median day earned.

## Limits that change how to read it

- **Nothing here is a trading rule, and a finding is not a profit.**
- **The hold-out is spent** (decision 0015). Any idea shaped on these days can only be proved on
  days after 30 September 2026. *Live observation is that proof, day by day.*
- **The hedge is assumed free**, so every hedged result is an upper limit on what a seller kept.
- **127 days is one kind of market.**
- One implied move is not the fair middle: priced exactly, the median move would still be about
  two thirds of it.

## How it connects

- The 30 September meeting asked for exactly this: six to twelve months of history, the 0DTE
  one-minute data, and a generic statistical check of a signal
  ([recap](../meetings/30-09-26-recap.txt), items 9 and 10).
- The maths comes from `payoff-project` (its decision 0002).
- India has no such study. The daily records in
  [teach/market-observation](../teach/market-observation/PLAN.md) begin its baseline.

## Related

[engine-dashboard](engine-dashboard.md) · [volatility](volatility.md) ·
[product-direction](product-direction.md)
