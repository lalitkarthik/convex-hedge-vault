> As of convex-hedge-strategy@292f816, 2026-10-23

# Strategy research — Meghav's SPXW studies

`convex-hedge-strategy` (`MeghavPradeep/convex-hedge-strategy`, cloned to
`D:\Convex Hedge\convex-hedge-strategy`) studies past market data to find trading ideas and test
them before they go into the [trading-engine](trading-engine.md). **No study has yet produced a rule
the desk trades.** Every idea it has tested as a strategy reads *failed*, and its four successful
hypotheses are facts about the market, not trades. **Its own pages are canon; this note only says
where to look and which figures we lean on.**

## Front doors

| Question | Page in the repo |
|---|---|
| What is this project? | `Strategy-Research/Home.md` |
| What did the descriptive study find? | `Strategy-Research/Guide/SPXW 0DTE descriptive statistics.md` |
| What did the smile study find? | `Strategy-Research/Guide/SPXW 0DTE smile study.md` |
| What did a hedged straddle make, at each entry time? | `Strategy-Research/Guide/Hedged straddle results table.md`, then `Guide/SPXW 0DTE hedged straddle study.md` |
| How is IV and each Greek worked out? | `Strategy-Research/Guide/Implied volatility and Greeks tables.md` |
| How is IV set against realised volatility, by hand? | `Strategy-Research/Guide/Implied against realised volatility calculations.md` |
| Why was a choice made? | `Strategy-Research/Decisions/` (0001–0022) |
| What does a word mean? | `Strategy-Research/Glossary/`, `CONTEXT.md` |
| Which ideas were tested as strategies? | `Strategy-Research/Strategies/` (five pages, all failed) |
| Which claims are being tested, passed or dropped? | `hypothesis/README.md`, then `hypothesis/testing/`, `success/`, `failure/` |
| What changed, when? | `Strategy-Research/Guide/Changelog.md` (stops at 13 October; see *Drift*) |

**The notebooks.** The first two are `notebooks/spxw_descriptive_stats.ipynb` (parts A to D,
sixteen tests, twelve predictability tests) and `notebooks/spxw_smile_study.ipynb`. Since 5 October
`notebooks/` has grown to seventeen: the hedged straddle study, the Greek ratios, the four feature
experiments, regime and window backtests, and a Greek attribution of the short straddle.
`hyp_test_notebooks/` holds one notebook per hypothesis. **The charts with a day slider do not draw
on GitHub.** Open the notebooks in VS Code or Jupyter from the local clone.

## What the data is

**The studies** (descriptive, smile, hedged straddle) read SPXW options expiring the same day, one
quote a minute, **127 trading days from 31 March to 30 September 2026**. The index is the implied
forward read from option prices, so every range reads slightly low. Other expiries, volume and open
interest are not in the data.

**The repo now holds a year.** On 8 October the 122 earlier days, **1 October 2025 to 30 March
2026**, were bought and opened as fresh days for the feature experiments
([feature-testing](feature-testing.md)). The descriptive notebook gained one table over all 249
days; every other figure in it is unchanged. The hypothesis tests train on the earlier half and
judge on the later one.

## The yardstick for watching SPXW live

These are the few figures a live reading is set against, from the 127 days unless a row says
otherwise. Everything else stays in the guide pages.

| Reading | A usual day | The extremes |
|---|---|---|
| Range, low to high | 0.72% | 0.26% (12 August) to 3.18% (9 June) |
| Move from the 9:35 reading to the close | 0.34% | a fall of 1.95% (5 June) |
| Implied volatility at 9:35 | 8.0% a year | 4.5% to 17.5% |
| Implied volatility at 9:35, October 2025 to September 2026 | 8.7% a year (10.2% in October to March) | up to 20.5% (21 November 2025) |
| Move as a share of the implied move | 0.63 | 3.78 (5 June) |
| Implied minus realised volatility | +0.97 points | −16.5 points (9 June) |

- **Opening IV goes with how wide the day is, not with its direction.** Rank correlation +0.55
  with the range. Nothing known at the open said which way the day would go.
- **The morning moves most**; the afternoon before the last half-hour is quietest.
- **A hedged option seller won on two days in three or more, and the losing days were larger.**
  The short straddle's worst day cost about ten times what its median day earned.
- **The earlier half-year opened about two points higher.** A live day in the 10% range is
  ordinary by the year, though it looks high against the 127 days alone.

## What the later work found

- **The hedged straddle study** (7 October): twelve entry times from 9:35 to 15:00, buyer and
  seller, hedged every minute or on a band. The median seller made money and the median buyer lost
  in every cell held to the close, while the seller's worst days were many times its median. Five
  published ideas, H1 to H5, were tested; only H1 was a finding, and against its idea: the buyer of
  the 14:30 straddle lost on 86 of 112 days. All five are recorded as failed strategies.
- **The hedge band** (decisions 0020–0022). The engine's band is the whole day's expected move ÷ 6.
  The study uses a share (⅙ and ½) of the move expected **in the time left**, so late entries are
  still hedged; at 9:35 it nearly equals the engine's NIFTY band ([engine-strategies](engine-strategies.md)).
  A hedge brings the position back to zero delta, and a hedge that cannot be priced is skipped and
  counted.
- **The feature experiments** (8 October) and the **long-gamma question** have notes of their own:
  [feature-testing](feature-testing.md) and [long-gamma-research](long-gamma-research.md).
- **The hypothesis folder** (merged 16 October): each claim is one file that moves between
  `testing/`, `success/` and `failure/` only with its evidence written in. Four passed, all
  relationships rather than trades: realised volatility persists from one 30-minute window to the
  next and IV follows it; the index, the put skew and the straddle price against its implied move
  each partly mean-revert within the day. The index effect is small: about 6% of a 30-minute move
  comes back in the next 30 minutes. A claim that uses information from its own outcome period goes
  to `failure/` however strong it is.

## Limits that change how to read it

- **Nothing here is a trading rule, and a finding is not a profit.**
- **The hold-out is spent** (decision 0015). Any idea shaped on the 127 days can only be proved on
  days after 30 September 2026. *Live observation is that proof, day by day.*
- **The hypothesis split judges on read days.** Its test half, April to September 2026, is the same
  127 days the descriptive, smile and hedged studies had already read. A pass there was chosen
  knowing those results. Days after 30 September are still the only unseen ones.
- **Free hedges are an upper limit.** The descriptive study and the every-minute columns of the
  hedged study assume the hedge costs nothing. Only the hedge-band columns pay for each hedge.
- **Exploratory tests.** The hedged study's five tests were chosen after earlier results were
  known, so a pass is a lead to check on new days.
- **127 days is one kind of market.** The six months before them priced options higher.
- One implied move is not the fair middle: priced exactly, the median move would still be about
  two thirds of it.

## How it connects

- The 30 September meeting asked for exactly this: six to twelve months of history, the 0DTE
  one-minute data, and a generic statistical check of a signal
  ([recap](../meetings/30-09-26-recap.txt), items 9 and 10). The repo now has the twelve months.
- The maths comes from `payoff-project` (its decision 0002).
- Its `CONTEXT.md` now defines strategy words itself (target position, hedge band, synthetic
  forward, entry cutoff, stop loss, take profit, time exit, decision cadence) where it used to point
  into the engine's glossary.
- India has no such study. The daily records in
  [teach/market-observation](../teach/market-observation/PLAN.md) begin its baseline.

## Drift found on 2026-10-23

- `Strategy-Research/Guide/Changelog.md` stops at 13 October. It does not record the merged feature
  experiments (PR #24), the regime and window backtests (#29), the hypothesis folder (#30) or the
  Greek attribution (#31).
- `hypothesis/` and `hyp_test_notebooks/` sit outside the `Strategy-Research/` vault, and no vault
  page links them.
- The descriptive notebook's opening text still says it reads 127 days, beside its new 249-day table.

## Related

[engine-dashboard](engine-dashboard.md) · [volatility](volatility.md) ·
[product-direction](product-direction.md) · [feature-testing](feature-testing.md) ·
[long-gamma-research](long-gamma-research.md)
