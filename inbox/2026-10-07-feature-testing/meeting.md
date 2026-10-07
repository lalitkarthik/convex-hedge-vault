# Daily meet, 7 October 2026: how to test a feature

> Staging note. Written by Claude from the recap, the transcript and two screenshots. The transcript is machine-typed Malayalam and English and is badly garbled, so each point is marked **clear** (the words or the sheet say it) or **read** (my reading of a garbled passage). Confirm the **read** points with Bilal.

Sources, all on this machine:

- `meetings/07-10-26-recap.txt` and `meetings/07-10-26-transcript.txt`
- `sources/07-10-26-sheet.png` — Bilal's spreadsheet (not pushed)
- `sources/07-10-26-dashboard.webp` — Bilal's regime dashboard (not pushed)
- `sources/07-10-26-images.md` — every number on the two screenshots (not pushed)

People: Bilal Sagar Razak and Rahul J Perumatty (seniors), Meghav Pradeep, Lalit Karthikeyan.

## 1. The test Bilal described (transcript 36:53 to 48:54, and the sheet)

The idea: take a feature, take the short straddle's return over the same window, sort the windows by the feature, and ask whether the returns in each group have a different distribution.

**The sheet** (clear). Columns: Time, IV, RV, Gap, Pace, Returns of Short Straddle.

| Row | IV | RV | Gap | Pace | Return |
|---|---|---|---|---|---|
| 09:17 | — | — | — | — | — |
| 09:47 | a | A | a − A | a / A | r1 = ln(9:47 straddle price) − ln(9:17 straddle price) |
| 09:48 | a2 | … | … | … | ln(9:48 straddle price) − ln(9:18 straddle price) |

**The steps.**

1. Start at 9:17 with one-minute data. (clear)
2. Realised volatility needs at least 30 points of look-back, so there is no value before 9:47. (clear)
3. At each minute record IV (at-the-money implied volatility), RV (realised over the last 30 minutes), Gap = IV − RV and Pace = IV / RV. (clear, from the sheet)
4. The return is the change in the log of the straddle's price over the same 30 minutes. Log is used because it is "more stationary". (clear)
5. Roll one minute at a time: 9:17 to 9:47, then 9:18 to 9:48. (clear)
6. IV and RV must be in the same units: annualise the 30-minute RV, or scale IV down to 30 minutes. (clear)
7. "Same format, minus return": the short side is the negative of the price change. (read)
8. Scatter the returns against the gap and look for clusters. (clear)
9. Sort and cut into deciles, or into about four buckets from very low to very high. (clear)
10. Test whether the return distribution differs between buckets. Lalit named ANOVA and the F test. Bilal's null hypothesis: the mean and variance are similar. The alternative: the distribution is different. (clear)

Build the same table for two return series: the straddle, and the spot taken as the implied forward. (clear, 51:43 to 52:15)

## 2. What Bilal and Rahul said to focus on

- **The shape of the distribution, not only the average.** Variance and tails. "Are the return distribution characteristics different? That is when regimes changed." If two buckets differ, they are distinct regimes. (clear, 47:26 to 48:17)
- **Name the returns.** Lalit said RV/IV² is highly correlated with returns. Bilal asked "with what returns?" The answer he wanted: a short straddle, delta neutral at the signal. (clear, 33:05 to 34:50)
- **Practical use decides.** A measure with no use, put on a dashboard, is fooling ourselves and the clients. Rahul: find whether it has significance for the strategy. (read, 31:38 to 32:23)
- **Use it as a filter.** Cut off the worst bucket, about 10%, and trade the rest. (read, 53:03)
- **A bad regime gives a smaller return, not always a negative one.** (clear, 55:44 to 55:58)
- **A correlation of about 40% is good enough for a signal.** (read, 36:22)
- **Keep it simple.** On Lalit's idea of weighting each minute by its usual volatility: if the difference is under 1%, it is of no use. More complexity is overfitting. "What we need is robust alpha." It must hold in Indian and US markets. (clear, 17:17 to 18:47)
- **Bring distributions to the next meeting**, not only profit and loss. (clear, 55:24)
- **Features to try through the same test:** delta²/gamma, delta/gamma, theta/gamma. Keep the ones that explain. (clear, 53:51)

## 3. Other points from the meeting

- **Realised-volatility estimators** (13:47 to 16:16, clear). Close-to-close includes the overnight gap, because the first candle uses the last close. Parkinson and Garman-Klass use only open, high, low and close, so they are intraday measures. One-minute or five-minute sampling are both acceptable.
- **Horizon** (25:30 to 26:58, clear). No 30-day trades. One week is the longest. Several entries and exits within a day. Seven-day constant maturity with a seven-day look-back is fine.
- **Seven-day implied volatility** (26:58 to 28:36). Lalit proposed interpolating between expiries to get an exact seven-day at-the-money IV, set against seven-day RV. Bilal's reply is garbled: "we can't take that; one thing is we can use ATM IV of our current one". (read: he may prefer the IV of the expiry actually traded over a built index.) Lalit said he would test it.
- **Delta²/gamma** (33:31, clear). Lalit: delta²/gamma over theta is equivalent to RV²/IV². Bilal said he was looking at the same thing.
- **Meghav's caution** (54:46, read). These ratios are Black-Scholes formulas of IV, so they may carry nothing beyond IV.
- **Rahul on the live strategy** (56:04, clear). The delta-neutral strategy is profitable on about 65 to 70 days of 100. The question is how to make it better, for example by controlling drawdowns.
- **Rahul's data ask** (57:51, read). Look at short-gamma results over the last two financial years, from April.
- **Morning trades** (52:47, read). Something about buying straddles in the first hour and only selling after. Not clear enough to act on.

## 4. The regime dashboard (second screenshot)

Bilal showed a page that splits past weeks into four regimes by volatility (low or high) and by direction (choppy or trending). For each regime it gives total profit, weeks, win rate, profit factor and maximum drawdown. His point: the spread of returns is different in each regime, and that difference is the evidence of a regime. He wants the same kind of split found with RV. The exact figures are in `sources/07-10-26-images.md`.

## 5. Action items (from the recap)

- Lalit tests the seven-day implied against realised approach.
- Someone researches the practical use of the RV/IV measure.
- Someone writes out and tests candidate delta and gamma features.

## 6. What the meeting left open

These decide how the test is built. Each is taken up in [test-plan.md](test-plan.md).

- Whether the return is the buyer's or the seller's (the sheet's formula is the buyer's).
- Which straddle is priced at the end of the window: the strikes sold at the start, or the new at-the-money strikes.
- Whether IV is read at the start or the end of the window. The sheet shows it on the 9:47 row.
- Whether the straddle is hedged during the 30 minutes, or only delta neutral at entry.
- Rolling windows overlap, so the rows are not independent.
- ANOVA compares means, while the stated interest is in variance and tails.
