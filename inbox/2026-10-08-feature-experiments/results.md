promoted: 2026-10-23
# Feature experiments on SPXW: what was built and what it showed

> As of `convex-hedge-strategy@bc7d9a5`, branch `feature/feature-experiments` (local, not pushed), 2026-10-08. Staging note, not canon. Figures live in the four notebooks; this page keeps only the few each conclusion needs.

Built overnight on 8 October 2026 from [test-plan.md](../2026-10-07-feature-testing/test-plan.md), which turned Bilal's request of 7 October ([meeting.md](../2026-10-07-feature-testing/meeting.md)) into a test.

## Where everything is

| What | Where (in `convex-hedge-strategy`, on the branch) |
|---|---|
| Part 1: implied against realised volatility (experiments 1 to 4) | `notebooks/spxw_feature_iv_rv.ipynb` |
| Part 2: regimes, costs and a filter (experiment 5) | `notebooks/spxw_feature_regimes.ipynb` |
| Part 3: the Greek features (experiments 7 to 9) | `notebooks/spxw_feature_greeks.ipynb` |
| Part 4: one week (experiment 6) | `notebooks/spxw_week_iv_rv.ipynb` |
| The code, with tests | `src/convex_strategy/features/`, `tests/features/` |
| The build scripts | `scripts/build_windows.py`, `scripts/build_week.py` |

The worktree is `D:\Convex Hedge\convex-hedge-strategy.worktrees\feature-feature-experiments`. Open the notebooks from there. Each one opens with a table of what was found.

## How it was done

- **Two samples of days.** The 127 *seen* days (31 March to 30 September 2026) had been read by every earlier study. The 122 *fresh* days (1 October 2025 to 30 March 2026) were downloaded on 8 October and nobody had read them. Two more fresh days, 28 November and 24 December 2025, closed at 13:00 and are left out: the repo's chain maths counts every day to 16:00.
- **Claims first.** Every notebook was run on the seen days only, its claims and kill lines were written, and that state was committed. Then the fresh days were opened once. The commit order on the branch is the proof.
- **A window** is 30 minutes, twelve a day from 9:35, with a new at-the-money straddle sold at the start and bought back at the end.
- **Three returns**: not hedged; hedged every minute at no cost; the desk's one-sixth band with the spread paid.
- **P-values** come from reshuffling whole days, so that a day's windows stay together and the time of day cannot fake a relation.
- **Reviewed once.** A separate reviewer agent read the code, recomputed one real window by hand and tried 33 deliberate mistakes against the tests. It found no look-ahead. It found the half-day fault above and three smaller ones, all fixed before the final run, and the tests it showed to be weak were strengthened. 223 tests pass.

## What was found

**1. Bilal's table works as a description. Confirmed on fresh days.**
The Gap of a window (implied less realised volatility) sorts the seller's return over the same window. Rank correlation 0.60 on the seen days and 0.53 on the fresh days when hedged every minute; 0.33 and 0.23 when not hedged. The lowest bucket is a different regime: wider, with a far worse tail.

**2. It does not work as a signal.**
The trailing Gap, known at the start, does not sort the next window in a way that pays the spread. Nothing on the seen days; a small effect on the fresh days for the cost-free hedged return only. One lead stays open: for the seller who does not hedge, a quiet half-hour was followed by a slightly worse window on both samples (p 0.009 and 0.043).

**3. Why: implied volatility already follows realised volatility.**
Realised volatility persists strongly from one window to the next (0.75 and 0.85). Implied volatility at the start is tied to recent realised volatility just as closely (0.79 and 0.86). What is left over is small.

**4. "Realised above implied in the morning" is an effect of the comparison.**
Implied volatility at 9:35 prices the whole day. Set each window against what the options charged *for that window* and the ratio is flat through the day. In a typical window the market moves about 0.6 of what was charged. Added up over all windows it moves all of it: pooled ratio 1.01 and 1.02. The edge is in the typical window and the tail gives it back.

**5. Regimes describe; they do not filter.**
Choppy windows pay the seller, trending windows cost; the four regimes of volatility and direction have plainly different distributions, as on Bilal's dashboard (confirmed). But from what is known at the start, no regime and none of six features gave a filter that held on both half-years. One rule looked excellent on the seen days (better than 99% of random filters) and failed on the fresh days, where the windows it skipped were better than the ones it kept. One feature, how straight the day has run so far, points the same way on both half-years and is left as a lead.

**6. Costs decide.**
Selling every window is up on 62% to 73% of days at the mid price, close to Rahul's 65 to 70 in 100. With the spread paid it loses on both samples (−359 and −464 points on the band). The spread is about 2% of the premium a window; the median edge is 2% to 3%.

**7. The Greek ratios.**
Delta ÷ gamma is the distance from the strike. Theta ÷ gamma is implied variance and nothing else, as Meghav said. Delta²/gamma over theta is a realised-over-implied ratio of the *end point*: it explains the seller who does not hedge (−0.78) far better than the variance ratio does, and the hedged seller worse. It is **not** the same as RV²/IV² window by window (rank correlation 0.3). All confirmed on fresh days.

**8. Charm and colour.**
Charm causes under 2% of the change in delta for a straddle re-struck every half-hour, and about 10% in the last hour for one held all day. Gamma grows with the clock within one implied move of the strike and dies beyond it; this held on real chains.

**9. Implied volatility and the index.**
Implied volatility rises when the index falls (slope −3) and does little when it rises. A hedge that allows for it, with the slope taken from the seen days, lowered the variance of the hedged result by 10% on the fresh days. A seller hedged to the Black delta is left long by about 0.05 of a delta.

**10. One week (experiment 6): thin in variance, unsteady for the seller.**
The expiry seven calendar days ahead exists on almost every day, so its own implied volatility is used, as Bilal preferred. Against the movement that followed, with the nights counted, realised variance was 0.87 of implied on the seen days and 0.95 on the fresh days: a premium of 5% to 13%. **The nights are a third of a week's movement.** Leave them out and the ratio reads 0.51 and 0.62, which would make options look twice as dear as they are. The unhedged seller of the weekly straddle made nothing on the seen days (+0.2% of the premium) and a quarter of the premium on the fresh days (+24.9%); the claim that its average could not be told from zero was killed. The difference is whether the weeks trended or chopped. The trailing gap predicts nothing here either. Blending a missing expiry from its two neighbours is good to about 0.2 volatility points.

**11. One day ahead.**
What the options charge for tonight plus tomorrow, against what came, on days that do not overlap: the median day delivers 0.7 of it, and added up 0.94 to 0.95. The same shape as inside the day. The night is about 40% of it, added up.

## What to bring to the next meeting

- The bucket charts of part 1, experiment 1, and the regime cards of part 2, section 2. These are the distributions Bilal asked for.
- Three points on method: Pace and the variance ratio are one feature (one is 1 ÷ the other squared); implied volatility must be measured for the window, not for the day; and a filter must be drawn on one set of days and tested on another.
- The failed filter rule, shown in full in part 2, section 5.

## Choices that are Claude's and wait for a word from Bilal or Lalit

- Implied volatility is read at the **start** of the window (the sheet shows it on the end row).
- The same two contracts are priced at the end.
- Tests use twelve windows a day that do not overlap, with whole days reshuffled.
- Realised volatility uses one-minute returns as Bilal asked; five-minute figures are shown beside.
- The one-week reading is taken at 10:00 from the expiry seven calendar days ahead.
- Half days are left out. The better fix is in the repo's loader (the expiry time of a half day), which is Meghav's code.

## Limits

- **SPXW only.** Nothing here says anything about NIFTY.
- **One year**, in two half-years. The fresh days come *before* the seen days.
- **The windows are a measuring device**, not a strategy.
- **Not reviewed by Meghav.** The branch is local. It skipped the repo's spec and ticket steps, as the hedged straddle study did; it needs a spec issue before any page goes into his vault.

## Next steps

1. Lalit reads the four notebooks, summary tables first.
2. Decide with Meghav whether this becomes a feature in his repo (spec issue, then a PR from the branch).
3. Tell Meghav that `quotes/loader.py` prices half days to 16:00; any study that reads 28 November or 24 December 2025 is affected.
4. Delta²/gamma over theta on the band's own hedge intervals (part 3 names this).
5. A hedge that leans short on down moves (part 3, experiment 9).
6. The weekly straddle hedged on the band (part 4 names this).
7. The same tests on NIFTY when data is on disk.
