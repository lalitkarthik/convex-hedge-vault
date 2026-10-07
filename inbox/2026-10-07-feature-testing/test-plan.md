# Feature testing: the plan as it stands

> Staging note, 2026-10-07. As of `convex-hedge-strategy@0ff3c74`. Nothing here is built. Parts marked **proposal** are Claude's and wait for Lalit's or Bilal's word.

Read [meeting.md](meeting.md) first: it holds what Bilal asked for. This page turns that into a test we can run on the data in `convex-hedge-strategy`, and lists the features to put through it.

## 1. Bilal's test, made exact

One row per window. A window is 30 minutes long.

| Column | Definition | Status |
|---|---|---|
| IV | at-the-money implied volatility, annualised | his |
| RV | standard deviation of the 30 one-minute log returns of the forward, annualised with √(252 × 390) | his; the annualising is decision 0005 |
| Gap | IV − RV | his |
| Pace | IV ÷ RV | his |
| Variance ratio | RV² ÷ IV² | discussed in the meeting |
| Straddle return | ln(price at end) − ln(price at start), sign reversed for the seller | his |
| Forward return | ln(forward at end) − ln(forward at start) | his |

Then: scatter each feature against each return, sort the windows into buckets by the feature, and test whether the buckets' returns differ.

### Choices the meeting left open (all **proposal**)

- **The clock.** Bilal's 9:17 is the Indian market (it opens at 9:15). SPXW opens at 9:30 New York, and this repo takes its opening reading at 9:35 (decision 0017). So the first window here is 9:35 to 10:05.
- **Which straddle.** The strike nearest the forward at the start of the window, and the same two contracts priced at the end. A new at-the-money strike at the end would not be a return anyone could earn.
- **Prices.** Mid first, as on his sheet. Beside it, the result with the spread paid, because the research found that mid fills create edges that do not exist.
- **Where IV is read.** At the start of the window, where it is a forecast of the 30 minutes ahead. His sheet shows it on the end row. Build both and label them; they answer different questions.
- **Explain or predict.** His table sets a feature against the return of the same window. That shows whether the feature explains the return. To show that it predicts, set the feature of one window against the return of the next. Run both, and call the first one description.
- **Hedging.** Two return series: the plain straddle (delta neutral at entry only, as on his sheet), and the delta-hedged straddle that the repo already builds.
- **Overlap.** A window that rolls one minute shares 29 of its 30 minutes with the next one, so the rows are not independent and a plain test will look far too significant. Use rolling rows for the charts. For the tests use windows that do not overlap (twelve a day), with whole days as the unit when reshuffling. The repo already reshuffles by day.
- **Which tests.** Three, because Bilal cares about more than the mean: a rank test of the buckets' centres (the repo's `groups_row`), a Brown-Forsythe test of their spread (`spread_row`), and a two-sample comparison of the top and bottom buckets' whole distributions. Correct them together (decisions 0014 and 0019).
- **Buckets.** Four equal groups now (decision 0018). Deciles need more days than the 127 held.
- **RV sampling.** Bilal asked for 30 one-minute points. Decision 0013 uses five-minute returns. The two differ; the notebook must say which it uses.

## 2. The features to put through the test

### From the meeting

Gap, Pace, the variance ratio, delta²/gamma, delta/gamma, theta/gamma.

### What delta²/gamma means

For a move of x points, a position changes by Δ·x + ½Γ·x². A hedged straddle starts with zero delta. After a move of x its delta is Γ·x and its gain is ½Γ·x². So:

- Δ/Γ = x, the distance in points from where the position was flat;
- Δ²/(2Γ) = ½Γ·x², the gain a hedge now would lock in.

Theta per unit of time is ½Γσ²F². So Δ²/(2Γ) divided by the theta paid since the last hedge equals x² ÷ (σ²F² × time): realised variance over implied variance for that interval. Delta²/gamma is the volatility premium measured between two hedges.

Real numbers: 1 June 2026, the 7575 straddle chosen at 9:35, buyer's side.

| Time | Forward − strike | Delta | Gamma | Δ/Γ | Δ²/(2Γ) | Implied move left |
|---|---|---|---|---|---|---|
| 12:00 | 9.1 | 0.33 | 0.034 | 9.7 | 1.6 | 21 |
| 13:00 | 20.6 | 0.71 | 0.023 | 30.3 | 10.8 | 20 |
| 14:00 | 37.1 | 0.91 | 0.009 | 103 | 46.9 | 22 |

The formula holds near the strike (9.7 against a true 9.1) and fails far from it, because gamma is not constant.

**Meghav's caution applies to theta/gamma.** For one option it equals ½σ²F² per unit of time. It is a formula of implied volatility and nothing else. The ratios carry information only for a position that has moved, or when they are set against what was realised.

### The Greeks of the clock (Lalit asked for these)

- **Charm**: the change of delta per minute, forward held still.
- **Colour**: the change of gamma per minute, forward held still.
- **Speed**: the change of gamma per point of the forward.

One rule for colour, derived from Black-76 with m = ln(F/K):

- ∂ ln Γ / ∂T = m² / (2σ²T²) − σ²/8 − 1/(2T)
- so gamma grows as time passes while |m| < σ√T × √(1 + σ²T/4), which is close to σ√T.

In words: gamma grows with the clock while the strike is within about one implied move of the forward, and dies outside it. The table above agrees: rising at 12:00 (9 points away, implied move 21), collapsed by 14:00 (37 away, implied move 22). A straddle bought at 9:35 stops being a gamma position once the market is one implied move away, while its buyer still pays theta.

All three can be computed by moving the clock or the forward by one step in the repo's existing pricing function. No new formula needs trusting.

### The experiments proposed

| # | Experiment | Why |
|---|---|---|
| 1 | Variance ratio for each half hour: by time of day, and whether a high window follows a high one | The buyer breaks even at 1. The half-hour averages are close (RV 0.076, IV 0.078), so the question is when it is above 1 |
| 2 | Δ²/(2Γ) against theta paid, for every hedge interval of the hedged straddle | The premium per hedge; a test of the hedge band rule |
| 3 | Colour and charm maps across strike distance and time; check the one-implied-move rule on real chains | Where the clock gives gamma and where it takes it |
| 4 | Split each minute's delta change into the market's part (Γ × move), the clock's part (charm) and the rest | How much hedging the clock causes |
| 5 | Share of the day the held strike stays within one implied move, against the hedged result | Whether a dead straddle explains the losing days |
| 6 | Change in at-the-money IV against the forward's return, minute by minute | If IV rises when the market falls, the Black delta is the wrong hedge |
| 7 | A one-page sheet for the five highest and five lowest days of each feature | Look at days, not only at correlations |

## 3. Order of work (**proposal**, not approved)

1. Bilal's table of section 1 on the 127 days held, for Gap, Pace and the variance ratio, against the straddle's return and the forward's return. This is what he asked to see at the next meeting.
2. Add delta²/gamma and delta/gamma for the held, hedged straddle (experiment 2).
3. The clock Greeks (experiments 3 to 5).

Form: one exploratory notebook, `notebooks/spxw_feature_experiments.ipynb`, on a branch. Each experiment opens with one sentence that states the claim and the result that would kill it. Functions move into the tested module only if a feature survives.

## 4. Limits

- **127 days.** A rank correlation must exceed about 0.17 to pass alone, and about 0.25 when ten tests are corrected together.
- **The hold-out was given up** (decision 0015), so everything found on these days is description. The older days being downloaded are the first fresh data.
- **One market.** Bilal wants results that hold in India and the US. Only SPXW is on disk. Databento does not carry NIFTY.

## 5. Data

On disk: SPXW same-day options, one-minute quotes, 31 March to 30 September 2026 (127 days), with chains, Greeks and half-hour tables already derived.

Asked for, not yet downloaded (the state is in [HANDOFF.md](../../HANDOFF.md)):

| Part | What | Lands in |
|---|---|---|
| ES futures | one-minute bars, all hours, 1 April 2024 to 30 September 2026 | `data/ES/` |
| More same-day SPXW | every trading day, 1 April 2024 to 30 March 2026, about 500 days | `data/history/SPXW/` |
| Week ahead | SPXW expiring 1 to 7 calendar days later, strikes within 5% of the money, every minute, all days | `data/week-ahead/SPXW/` |

The script is `convex-hedge-strategy/scripts/databento_download.py`. New days are kept out of `data/SPXW/` so that the existing 127-day studies do not change when they are rebuilt.

**Overlap to settle.** Meghav's issue [#28](https://github.com/MeghavPradeep/convex-hedge-strategy/issues/28), opened the same afternoon, plans a ten-day Greek-ratio study with its own download into `data/SPXW-10DTE/`. The week-ahead download stops at seven days, so it does not cover #28. One download should serve both.

## 6. Where the method comes from

[pipeline.md](../2026-10-07-research-pipeline/pipeline.md) holds what 212 public sources say about researching a strategy. Three of its points bear on this plan: write the claim and its kill line before the run; a ratio screen is a start and not a hypothesis; count every trial.
