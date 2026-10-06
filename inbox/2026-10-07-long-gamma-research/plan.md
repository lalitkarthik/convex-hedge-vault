> As of convex-hedge-strategy@168105a, 2026-10-07. Raw capture from a grilling session — staging, not canon.

# Long-gamma research on SPXW 0DTE — decisions, plan, and what to teach

The aim: use the SPXW same-day-expiry data in `convex-hedge-strategy` to reach a trading strategy
in the engine's shape, with at least one long-gamma strategy. The senior asked for one because the
desk's strategies are almost all short gamma.

Beside this file: [literature-report.md](literature-report.md), written by a headless research
run. **Its links have not been opened by hand yet.** Open each source before a hypothesis page
cites it.

## Decisions (19 questions, three rounds)

| # | Decision |
|---|---|
| 1 | "Done" is a strategy in the engine's shape (entry, structure, hedge rule, exit) with one page of evidence, on paper in the SPXW sandbox. A tested idea that failed, with its reason, also counts. |
| 2 | Work inside `convex-hedge-strategy`, under its rules, in a new notebook. Meghav keeps the descriptive study. Agree the split with him first. |
| 3 | Mechanism first. Each idea says who is forced to trade and why that leaves the straddle mispriced. One target: the result of a hedged ATM straddle after the spread. Greek ratios are units, not signals. |
| 4 | Main line: long straddle, delta-hedged on a band — the mirror of `nifty-straddle`. The unhedged long straddle (`spxw-straddle-low-iv`) is the comparison. Long wings over a short body: the literature is against it. |
| 5 | Every result is stated as "SPXW, intraday, 0DTE". Nothing is assumed to carry to NIFTY. |
| 6, 16 | The 127 days are all seen, so they find hypotheses and prove none. **No new download now.** Findings are presented as findings. A rule is proved later by a backtest in the desk's own tool — on days outside 31 March to 30 September 2026. *Check the tool's date range before relying on it.* |
| 7 | Sources: tier 1 papers with data and exchange research; tier 2 books by named practitioners; tier 3 a blog only when it shows data and method. A hypothesis needs tier 1 or 2. |
| 8 | One research note per hypothesis in `Strategy-Research/Research/`, written before any test: source, concept, mechanism, SPXW adaptation, feature, target, test, the result that kills it. Then one spec issue with the pass/fail bar, as the repo requires. |
| 9 | Keep the lead-lag tool (Meghav's `lead_lag`, PR #19). Change the two sides: a feature known at minute t against a later, tradable outcome. Greek ratio against IV is built in — his D4 text and PR #19 already show it. |
| 10 | Target windows: entry to close, and the next 60 minutes. Entries on the half-hour grid, 9:35 to 15:00. |
| 11 | First batch: **all five hypotheses**. They join the existing second set of twelve tests (decision 0019), so each is judged as one of seventeen. |
| 12 | Three hedge rules side by side: every minute; the desk band (delta ÷ gamma past implied move ÷ 6); a wide band (implied move ÷ 2). |
| 13 | Each result twice: at mid, and with the spread paid (buy at the ask, sell at the bid; each hedge pays half the synthetic forward's spread). No fees. |
| 14 | No tuned thresholds. Sort days into four equal groups by the feature; test the trend across groups on ranks and medians (decisions 0016, 0018). |
| 15 | The straddle keeps its entry strike until the window ends. |
| 17 | Three charts: the clock chart (share of movement against share of time value, by half-hour); an entry-by-exit grid of the hedged result; the day slider with index, ATM IV, straddle price and running hedged result on one axis, with a mark at each band hedge. |
| 18 | Two features. First the target table (band hedge, any-half-hour entry, cost model, tests). Then the five-hypothesis study, its notes and spec issue merged before the study code runs. Claude builds on branches; Meghav reviews. |
| 19 | To the next daily meet: the buyer's baseline, the morning lead, the five hypotheses with sources. |

## Facts the plan stands on

Figures are from `data/derived/` and the committed notebook; the rest stay in the repo.

- **Greek ratios restate IV and the clock.** The study defines theta as ½·IV²·F²·gamma per minute
  (`src/convex_strategy/descriptive/positions.py:95`). Theta ÷ gamma is IV² × forward². Vega ÷ theta
  is 2 × minutes left ÷ IV.
- **The plain hedged long straddle loses.** Bought 9:36, hedged every minute to expiry, hedge free,
  at mid: won 42 of 126 days, median −2.60 points, best +23.5, worst −15.6, sum −214. The ten best
  days sum to +140.
- **Nothing known at the open sorts the days.** No predictability test survives (smallest corrected
  p 0.45).
- **Time of day is the one lead.** IV at window start is above realised volatility over the window
  on 33% of days at 9:35 and 87% at 15:00. The repo marks the comparison "not like-for-like".
- **Five-minute returns reverse** (median lag correlation −0.052). It may be noise in the implied
  forward. Check before leaning on it.
- **Spread:** ATM straddle about 0.30 points on 30.4 at 9:35 (1%), 2.6% of the premium at 15:30.
  The seller's median day is +2.45 points.
- **Sample size:** 127 days confirm only an annualised Sharpe ratio near 2.8. A Sharpe ratio of 1
  needs roughly 800 to 1,200 days.
- **Hedge code** (`positions.py`: `pick_strikes`, `follow`, `_result`, `hold_day`) hedges every
  minute at zero cost. A band, a hedge cost and any-minute entry are to be added.

## The five hypotheses

Each needs its source opened and its research note written before any test.

| # | Hypothesis | Source of the concept | What the repo already shows |
|---|---|---|---|
| 1 | Long hedged straddle, last 90 minutes: time value runs off by the clock while movement rises into the close | Muravyev and Ni (day against night; afternoon gains) | Against: IV above realised on 87% of days at 15:00 |
| 2 | Long hedged straddle from 10:00 after a busy first half-hour: movement clusters, quotes react late | Intraday volatility clustering; Hizmeri (morning volatility) | Untested hedged; unhedged form (P10) found nothing |
| 3 | Long hedged straddle when the 10:00 implied variance is below a realised-volatility forecast | Corsi's HAR forecast | Simplest form dead (N11, P4, P12) |
| 4 | The band is a bet: a wide band pays the buyer on trending days, a tight band on reversing days | Whalley and Wilmott; Zakamouline; Sinclair | Five-minute returns reverse — supports the desk's band on the short side |
| 5 | Short hedged straddle over the midday lull, 11:30 to 13:30 | Same clock mechanism as 1, mirrored | Supported: realised volatility lowest 13:30 to 15:00 |

On this data the buyer's best hour is the first, not the last. A sixth candidate — long from 9:35
for the first hour — is the strongest lead in hand and has no source yet.

## Next steps, in order

1. Lalit reads part D of `spxw_descriptive_stats.ipynb` on his own (8 October). It is not part of
   the teaching sitting.
2. Claude teaches every concept below (8 October).
3. Lalit agrees the split with Meghav.
4. Open and check each source; write the five research notes.
5. Spec issue and build of the target table (feature 1).
6. Spec issue for the study, merged before it runs (feature 2). Run, correct as seventeen tests.
7. One page for the daily meet.

## To teach on 8 October — every concept this session used

Lalit asked to be taught all of it well: everything found today, all sixteen items. He reads part D
on his own, so the sitting does not walk through the notebook. Paragraphs first, charts as PNG from
the repo's own days, nothing asked of him. Four blocks, in this order, with a break after block B.

**A. Where a hedged straddle's money comes from**
1. The pricing link between theta and gamma; why theta ÷ gamma, vega ÷ theta and delta ÷ gamma are IV and the clock in other units.
2. The breakeven move, and the hedged result as gamma × (actual move² − breakeven move²), summed over the day.
3. Implied against realised variance; the variance risk premium; why the seller wins on most days.
4. Pay-off skew: win rate against size of win (42 of 126; ten days carry +140).

**B. The clock and the band**
5. Clock time against variance time; the U-shape of movement through the day; D3's left-over.
6. Delta ÷ gamma as a distance in points; how the desk's band uses it.
7. The band as a choice of scale: trend against reversal; autocorrelation of returns and the variance ratio.
8. Hedge cost against band width (Whalley and Wilmott); the synthetic forward and what it costs.

**C. How to trust a finding**
9. Mechanism first against scanning; a correlation that is built in; why two drifting series correlate by accident; what makes a lead-lag reading mean something.
10. In-sample and out-of-sample; the hold-out and why it is spent; writing the test down first.
11. The p-value; testing many things at once; the Benjamini-Hochberg correction; why 5 more tests make 17.
12. Rank correlation, four equal groups, medians against averages.
13. The Sharpe ratio and its error; why 127 days confirm only 2.8; how skew changes the count.

**D. The sources and the five hypotheses**
14. Muravyev and Ni; Vilkov's 0DTE results; intraday momentum and dealer hedging; event days; the HAR forecast.
15. Each of the five hypotheses: source, mechanism, what our data already says.
16. NIFTY in brief: who earns the premium there, and why transaction tax decides the hedge instrument.
