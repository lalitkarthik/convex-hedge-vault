# Hypotheses from the desk's own data

> Lane own-data, 0 outside sources, 7 cards, 2026-10-08. Written by Claude from the four feature-experiment notebooks, as of `convex-hedge-strategy@cc8b0ef`. Staging note, not canon.

## Summary

These cards come from oddities in the desk's own notebooks, not from reading. Each figure is quoted from a notebook's written observations; the first number is for the seen days (31 March to 30 September 2026) and the second for the fresh days (1 October 2025 to 30 March 2026).

Every card here was **noticed after the data was opened**. Both half-years are used up for them. They are hypotheses to test on days outside that year, and none is a finding. The mechanisms are Claude's proposals and have no source behind them yet; the other three lanes may supply or contradict them.

## Cards

### 1. The first half-hour is priced too dear

- **Mechanism (proposed, unsourced).** At 9:35 the day's news is not yet absorbed and buyers of same-day protection pay up at the open. The options then charge for more movement in the first half-hour than comes.
- **Prediction.** For the window 9:35 to 10:05, realised variance added up over all days is below the variance the options charged for that window: a pooled ratio under 1. The seller hedged on the band, closed at 10:05, earns after the spread.
- **Kill line.** A pooled ratio at or above 1 on new days, or a result with the spread paid that is not above zero.
- **Data needed.** Held.
- **Evidence.** Part 1, Experiment 4: this is the only half-hour with a pooled ratio below 1 on both samples, 0.77 and 0.80.
- **Already tested?** Not by the desk as a claim. A related idea failed: buying at 10:00 after a busy first half-hour (`Strategies/Hedged straddle buyer after a busy first half-hour.md`).
- **Why it may fail.** The pooled ratio by time of day is noisy: one or two large windows decide each hour's figure. Twelve half-hours were looked at. If each were below 1 by the toss of a coin on each sample, about three of the twelve would be below 1 on both, so one being so is no evidence by itself; the case rests on the mechanism. The spread in this window has not been set against the edge.

### 2. A hedge that leans short on the way down

- **Mechanism.** Implied volatility of a held strike rises when the index falls and does not fall when it rises. A sold straddle hedged to the Black delta is therefore left long the index, and loses more than its delta says on a fall.
- **Prediction.** A band that is narrower below the strike than above it lowers the variance and the worst day of the seller's hedged result, with no fall in its average, against the symmetric one-sixth band.
- **Kill line.** No fall in variance on new days, or a fall in the average that is larger than the fall in the worst day is worth.
- **Data needed.** Held.
- **Evidence.** Part 3, Experiment 9: slope on down moves −3.05 and −3.04; on up moves +0.39 and −0.18. A hedge using one slope fitted on the seen days cut one-minute hedged variance by 9.7% on the fresh days. The single delta that would have hedged best was −0.06 and −0.08 for the holder against a Black delta of about zero.
- **Already tested?** The variance cut was tested once, on one-minute hedging at no cost. The asymmetric band was not tested. Only variance was measured, never the average.
- **Why it may fail.** A band hedger trades a few times an hour; one-minute steps overstate the gain. The slope by time of day did not agree between the two samples.

### 3. The day that has run straight

- **Mechanism (proposed, unsourced).** After a day that has moved in one direction, option sellers mark implied volatility up for a continuation that then comes less often than priced.
- **Prediction.** Windows that start when the day's efficiency so far is in its highest quarter for that time of day give the hedged seller a higher average return than the other three quarters.
- **Kill line.** The highest quarter is not the best on new days, or its margin over the others is under the cost of one round trip (about 2% of the premium).
- **Data needed.** Held.
- **Evidence.** Part 2, section 4: the straightest bucket is the best on both samples for both hedged returns: +1.9% against +1.1% to +1.5% (seen), +1.3% against 0.0% to +0.2% (fresh), hedged every minute.
- **Already tested?** No. It passed on the fresh days only (p 0.050 and 0.003) and was noticed there.
- **Why it may fail.** On the seen days the margin was nowhere near passing (p 0.36 and 0.88). With the spread paid the best bucket only breaks even (−0.4% and −0.3%).

### 4. Quiet, then a break

- **Mechanism (proposed, unsourced).** A half-hour that is quiet for its time of day is sometimes the compression before a directional move. The seller who does not hedge is paid on where the index ends, so a break-out hurts that seller most.
- **Prediction.** For the unhedged seller, the rank correlation between the trailing Gap and the next window's return is lower than the time of day alone produces.
- **Kill line.** The correlation is at or above the time-of-day figure on new days.
- **Data needed.** Held.
- **Evidence.** Part 1, Experiment 2: 0.087 against 0.141 from the time of day alone (p 0.009), and 0.067 against 0.106 (p 0.043).
- **Already tested?** This is the test. It passed its pre-written bar on the fresh days at the edge.
- **Why it may fail.** The p-value on the fresh days was 0.077 before two half days were removed. With the variance ratio in place of the Gap it gives p 0.19. The effect is 0.04 of a rank correlation.

### 5. Skipping after a loud, trending half-hour protects the worst day

- **Mechanism (proposed, unsourced).** The worst sessions for a seller are trend days, and a trend day shows itself early as a loud, one-directional half-hour. Standing aside after one removes part of the tail without changing the typical day.
- **Prediction.** Against selling every window, the rule lowers the size of the worst day by more than a random filter of the same size does in 95% of draws. Its average per window is not required to improve.
- **Kill line.** The worst day under the rule is matched or beaten by more than 5% of random filters on new days.
- **Data needed.** Held.
- **Evidence.** Part 2, section 5: worst day −27.9 against −47.0 points (seen) and −18.1 against −25.9 (fresh); on the fresh days only 3% of random filters matched it.
- **Already tested?** The rule was written to improve the average and failed at that on the fresh days. Its effect on the worst day was noticed afterwards.
- **Why it may fail.** A worst day is one observation per sample. The same rule was no better than random on the deepest fall on the fresh days (63% of random filters matched it).

### 6. A dear tomorrow is too dear

- **Mechanism.** Implied volatility as a forecast is too spread out: when it is high it overshoots what follows, and when it is low it undershoots.
- **Prediction.** On days when the variance charged for the next night and session is in its highest quarter, the pooled ratio of what came to what was charged is below 0.95; in the lowest quarter it is at or above 1.
- **Kill line.** The highest quarter's pooled ratio is not below the lowest quarter's on new days.
- **Data needed.** Held (the week-ahead files).
- **Evidence.** Part 4, section 5: highest bucket 0.89 and 0.82; lower buckets 0.98 to 1.05 and 1.13 to 1.40. These days do not overlap.
- **Already tested?** No. It was not a claim written beforehand.
- **Why it may fail.** Buckets hold 21 to 52 days. The night is 38% to 46% of the variance that came, added up, and cannot be hedged, so a seller carries gap risk for the whole edge.

### 7. Do not sell the week when it is cheap against last week

- **Mechanism.** The same as card 6, at one week, read from the other end: a weekly straddle priced low against last week's movement is not cheap enough.
- **Prediction.** The lowest quarter of the trailing gap (seven-day implied less last week's realised) gives the weekly unhedged seller a lower average return than the other three quarters.
- **Kill line.** The lowest quarter is not the worst or second worst on new weeks.
- **Data needed.** Held.
- **Evidence.** Part 4, section 3: lowest bucket −23% and 0% of the premium against +19% to +37% for most others. The rank correlation with the seller's return on the fresh days was 0.149 against a pre-written bar of 0.15.
- **Already tested?** As a lead; it missed its bar by a hair.
- **Why it may fail.** About 45 independent weeks in the year, five or six a bucket. On the seen days a second bucket was as bad.

## Quantities the desk holds and has not looked at

Part 2's closing names the kinds of feature that were not tried: the skew, the term structure, dealer positioning and the calendar of news. Three of them need no new data:

- **Tomorrow against today, minute by minute.** The desk holds today's chain and tomorrow's side by side. The difference of their total variances is what the market charges for tonight and tomorrow, and it can be followed through the day. Nobody at the desk has charted it.
- **The shape of the smile through the day.** The smile study measured it at fixed times; no feature test has used it.
- **The width of the quote.** Every test paid the spread as a cost. None used the spread itself, or its change, as a feature.

These are places to look, not hypotheses. Each needs a mechanism before it becomes a card.
