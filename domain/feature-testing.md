> As of convex-hedge-strategy@292f816, 2026-10-23

# Feature testing — Bilal's bucket method

How the desk decides whether a number is worth watching. Bilal set the method at the daily meet of
7 October 2026. The first full run of it, on SPXW, was built on 8 October. **The four notebooks in
`convex-hedge-strategy` are canon for every figure; this note keeps the method and the conclusions.**

## What a feature is

A **feature** here is a number that can be worked out for a stretch of market time and that might
tell a good stretch for the seller from a bad one: implied less realised volatility, a Greek ratio,
the time of day. It is a candidate, not a signal, until the test below says so.

The word collides with two other uses. On the terminal, **Feature** is the unit the Structure Chain
grid shows ([GLOSSARY](../GLOSSARY.md)). In the team's workflow, a feature is a unit of work with a
spec and tickets ([team-workflow](team-workflow.md)). This note means only the first sense above.

## The bucket test

The test asks one question: **do the returns of the windows in each group of the feature have a
different distribution?** Bilal cares about the shape — spread and tails — more than the average.
If two groups differ, they are two regimes.

1. Cut the day into **30-minute windows**. Bilal's sheet rolls them one minute at a time from 9:17,
   the Indian clock; on SPXW the first window starts at 9:35 New York.
2. For each window, record the feature: **IV** (at-the-money implied volatility), **RV** (realised
   over the 30 minutes), **Gap** = IV − RV, **Pace** = IV ÷ RV, or a Greek ratio. Put IV and RV in
   the same units first.
3. Record the **return of the short straddle** over the same window: the change in the log of its
   price, with the sign reversed for the seller. Build the same table for the forward's return.
4. Scatter return against feature. Sort the windows and cut them into **buckets**: four equal groups,
   or ten when the sample allows.
5. Test whether the buckets' return distributions differ. The null hypothesis: the same centre and
   spread.

**Its use is a filter.** Cut off the worst bucket, about a tenth of windows, and trade the rest. A bad
regime gives a smaller return, not always a loss. Bilal asked for distributions at meetings, not
only profit and loss, for simple measures over complex ones, and for results that hold in Indian and
US markets. A rank correlation near 0.4 is enough for a signal, in his reading.

## Made exact for a test

The meeting left choices open. These are the ones used on 8 October. They are Claude's, and **wait
for Bilal's or Lalit's word** ([results](../inbox/2026-10-08-feature-experiments/results.md)).

- **Explain and predict are two tests.** A feature set against the return of the *same* window
  explains it. Only a feature from the window *before* set against the next return predicts. Bilal's
  sheet is the first kind. Both are run and labelled.
- **The same two contracts** are priced at the window's end. A new at-the-money pair at the end is
  not a return anyone can earn.
- **IV is read at the window's start**, where it is a forecast. The sheet shows it on the end row.
- **Three returns:** not hedged; hedged every minute at no cost; and hedged on the desk's one-sixth
  band with the spread paid.
- **Windows that do not overlap** — twelve a day — for every test. Rolling windows share 29 of 30
  minutes and make a plain test look far too significant. P-values come from reshuffling whole days.
- **Three tests**, corrected together: a rank test of the buckets' centres, a Brown-Forsythe test of
  their spread, and a comparison of the top and bottom buckets' whole distributions.
- **Claims first.** Each claim and the result that would kill it was written and committed on the
  127 days already read, then tested once on 122 fresh days (October 2025 to March 2026, bought as
  described in [databento](databento.md)).

## What counts as evidence

- A relation that holds on days nobody had read when the claim was written.
- A predictive relation, not only an explanatory one, for any filter.
- A result that survives the spread. At the mid, many things look like an edge.
- A filter drawn on one set of days and tested on another.
- A whole distribution — centre, spread, worst bucket — not a mean alone.

## What the 8 October run found

SPXW same-day options, 249 days. Figures stay in the notebooks and the findings pages; these are
the conclusions.

1. **The test works as a description.** The Gap of a window sorts the seller's return over the same
   window: rank correlation 0.60 on the seen days and 0.53 on the fresh days when hedged every minute.
   The lowest bucket is a different regime, wider and with a far worse tail.
2. **It does not work as a signal.** The Gap of the window before does not sort the next one in a way
   that pays the spread.
3. **Why: implied volatility already follows realised.** RV persists strongly from window to window,
   and IV at the start is tied to recent RV just as closely. Little is left over to predict.
4. **"Realised above implied in the morning" is an effect of the comparison.** IV at 9:35 prices the
   whole day. Set each window against what the options charged *for that window* and the ratio is
   flat through the day. The median window moves about 0.6 of what was charged; summed over all
   windows, the market moves all of it. The edge is in the typical window and the tail gives it back.
5. **Regimes describe; they do not filter.** Choppy windows pay the seller and trending ones cost, as
   on Bilal's regime dashboard. No regime and no feature known at the start gave a filter that held
   on both half-years. One rule beat 99% of random filters on the seen days and failed on the fresh
   days.
6. **Costs decide.** Selling every window is up on 62% to 73% of days at the mid, close to Rahul's
   65 to 70 in 100. With the spread paid it loses on both samples. The spread is about 2% of a
   window's premium; the median edge is 2% to 3%.
7. **Pace and the variance ratio are one feature.** One is 1 ÷ the other squared, so they fill the
   same buckets.
8. **The Greek ratios.** See below. All confirmed on fresh days.
9. **Charm and colour are small** for a straddle re-struck each half-hour: under 2% of the change in
   delta. Gamma grows with the clock within about one implied move of the strike and dies beyond it.
10. **IV rises when the index falls** (slope about −3) and does little when it rises. A hedge that
    allows for it lowered the variance of the hedged result by 10% on fresh days.
11. **One week: the nights are a third of the movement.** Against the seven-day expiry's own IV,
    realised variance was 0.87 and 0.95 of implied. Leave the nights out and the ratio reads about
    half, which makes options look twice as dear as they are.
12. **One day ahead has the same shape**: the median day delivers about 0.7 of what was charged,
    and the sum about 0.95.
13. **The smile's tilt and wings** (a later page in the same folder, four tests written first). The
    tilt, ranked against its own last 20 days at the same time of day, sorted the next window's
    risk reversal at the mid on both half-years, but only before the correction for many tests; with
    the spread paid the risk reversal lost in every bucket. The wings claim held on the fresh
    half-year only. The two open questions were not findings.

## The Greek ratios as features

For a hedged straddle that was flat at the last hedge and has since moved x points:

- Δ ÷ Γ = x, the distance in points from where the position was flat.
- Δ² ÷ (2Γ) = ½Γx², the gain a hedge now would lock in.
- Θ per unit of time = ½Γσ²F², so **Θ ÷ Γ = ½σ²F²: implied variance and nothing else.** Meghav's
  caution that these ratios restate IV is right for this one.
- (Δ² ÷ 2Γ) ÷ Θ paid since the hedge = x² ÷ (σ²F²t): **realised over implied variance for that
  interval**, measured at its end point.

So Δ²/Γ over Θ is not the same as RV²/IV² window by window (rank correlation about 0.3). It measures
the end point, not the path. It explains the seller who does not hedge far better than the variance
ratio does; realised variance explains the seller who hedges.

## Status

- **The code and notebooks are on `main`** of `convex-hedge-strategy` (merge `cc8b0ef`, then
  pushed). They went in without a spec issue or a PR. Package `src/convex_strategy/features/`;
  notebooks `spxw_feature_iv_rv`, `spxw_feature_regimes`, `spxw_feature_greeks`, `spxw_week_iv_rv`.
- **A data fault was found in the repo's loader:** `quotes/loader.py` counts every day to 16:00, so
  the half days of 28 November and 24 December 2025 are priced on the wrong clock. They were left out.
- **The ratio Δ²/Γ ÷ Θ was then put through the bucket method in Bilal's backtest repo** on 12 October:
  [backtest-lab](backtest-lab.md).
- **SPXW only.** Nothing here says anything about NIFTY.

## Open questions

1. Does Bilal accept the six choices above — IV at the start, the same contracts, windows that do not
   overlap, one-minute RV, the 10:00 weekly reading, half days left out?
2. Has Meghav been told about the half-day fault in `quotes/loader.py`?
3. The lead left open on both samples: for the seller who does not hedge, a quiet half-hour was
   followed by a slightly worse window. And "how straight the day has run so far" pointed the same
   way on both half-years. Both need days neither sample holds.
4. Δ²/Γ over Θ on the band's own hedge intervals; a hedge that leans short on down moves; the weekly
   straddle hedged on the band — named as next steps, not built.
5. The same tests on NIFTY, once its data is on disk.

## Sources

- [meeting.md](../inbox/2026-10-07-feature-testing/meeting.md) — the meet, each point marked clear or read
- [test-plan.md](../inbox/2026-10-07-feature-testing/test-plan.md) — the test made exact, the Greek derivation
- [results.md](../inbox/2026-10-08-feature-experiments/results.md) — what was built and found
- [iv-vs-rv-findings.html](../inbox/2026-10-08-feature-experiments/iv-vs-rv-findings.html),
  [greeks-findings.html](../inbox/2026-10-08-feature-experiments/greeks-findings.html),
  [smile-findings.html](../inbox/2026-10-08-feature-experiments/smile-findings.html) — the rendered pages
- Daily capture: [2026-10-07](../inbox/2026-10-07.md), [2026-10-08](../inbox/2026-10-08.md)
- Code: `convex-hedge-strategy/notebooks/spxw_feature_*.ipynb`, `spxw_week_iv_rv.ipynb`

## Related

[strategy-research](strategy-research.md) · [realised-volatility-estimators](realised-volatility-estimators.md) ·
[long-gamma-research](long-gamma-research.md) · [backtest-lab](backtest-lab.md) · [volatility](volatility.md)
