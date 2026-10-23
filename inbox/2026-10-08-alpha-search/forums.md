promoted: 2026-10-23
> Lane forums, 32 threads read, 7 strategy cards, 13 methods, 2026-10-09

## Summary

- **Forums are good for** mechanisms from people who sat on the other side (market makers on how they quoted expiry day, how they marked time over a weekend, how they hedged), and for disputes that point straight at a test. **Forums are bad for** results: almost nothing is backed by a test, backtests appear as screenshots with unstated fills, journals end without a result, and sellers of tools and courses dominate the 0DTE threads after 2022.
- Reddit could not be read with any tool available to this run. Nothing from Reddit is cited.
- **Most useful find 1.** A former OEX market maker (FSU, 2017) says SPX options are cheap in the last 10-30 minutes of expiry day, because market makers price off futures while the cash close decides settlement, and he stopped quoting ten minutes before expiry. Another poster's backtest says the opposite (selling the last hour paid). The desk's windows end at 15:35, so the last 25 minutes are untested. That is card 1.
- **Most useful find 2.** Two practitioner accounts of how option prices treat the weekend: by convention, not by measurement. One market maker advanced his clock from Thursday 11:00. A former floor trader found the market decays about 2/3 of calendar theta over a weekend. The desk holds the Monday expiry on Friday afternoon, so it can measure this directly. That is card 2.
- **Most useful find 3.** Working methods that fit the desk's data: hedge back to the band edge, not to zero (sle). Measure realised volatility by simulating the hedger's own scalping (Matt_ORATS). Compare the distribution of moves in a window with what vol priced instead of backtesting stop fills. Measure the market's own clock before calling anything cheap.

## Strategy cards

Strongest first. "Desk can test" means on the one-minute SPXW quote data it holds.

### Card 1. The last 25 minutes are priced off the wrong underlying — desk can test

1. **Name.** Expiry-day options are cheap after 15:35.
2. **Mechanism.** Index option market makers price SPXW off ES futures for most of the day. In the last minutes of expiry day the cash index print decides settlement, books are thin, an option worth a few ticks is hard to monetise, and a market maker left near the strike at the close must scramble to trade delta into the futures close. So market makers pull back, widen, or stop quoting. FSU says he stopped about ten minutes before expiry. Prices in the last half-hour then follow stale models and a minimum-tick floor, not the variance still to come.
3. **Prediction.** Pooled over all days, the realised variance of the index from 15:35 to the 16:00 settlement is above 1.1 times the variance implied for that slice by the 15:35 at-the-money straddle mid. A straddle bought at the 15:35 ask and held to settlement earns above zero.
4. **Kill line.** A pooled ratio at or below 1.0 on the year, or a loss when the straddle is bought at the ask.
5. **Data needed.** Held: one-minute SPXW quotes to 16:00 and the implied forward. The official 16:00 SPX settlement value is public and free.
6. **Evidence.**
   - FSU [anonymous, credible: says 25 years as an OEX market maker on the floor; specific and consistent across many ET threads], Elite Trader, "Underpriced SPX options at expiration", 29 Oct 2017, https://www.elitetrader.com/et/threads/underpriced-spx-options-at-expiration.314509/ — buys near-money puts at about 0.20 with ten minutes left and needs a win only about one time in ten. He stopped quoting electronically about ten minutes before expiry because "the models broke down in the last minutes". He later posts a day on which it did not work. He kept no record in the thread.
   - Same thread, page 2. A reply whose handle the page text does not show says expiring index books are light and a pinned market maker must chase the futures close; this matters less today because of match-cash-close futures trading. JackRab [anonymous, credible: former European index market maker, detailed] says that on the last day market makers just look at the straddle value and limit exposure.
   - Against: dorietrading [unknown; posts backtest screenshots], Elite Trader, "Day trading 0DTE Condors", 7 Feb 2024, https://www.elitetrader.com/et/threads/day-trading-0dte-condors.378216/page-6 — a last-hour short strangle earned about $56 a day since 2018 after 10c slippage, with a worst drawdown of $1,317. Stop fills are taken at the option's 15-minute high. A critic in the thread distrusts those fills.
   - Ambiguous: Matt_ORATS [seller: ORATS data and backtester], "Sell daily SPX straddles?", Sep 2022, https://www.elitetrader.com/et/threads/sell-daily-spx-straddles.369734/page-2 — "trading the last 14 minutes" to expiry returned +3.6% of the index in 2022 YTD, Sharpe 1.01. The thread never makes clear whether that is long or short.
7. **Already tested?** Searched Elite Trader, NexusFi and Quant SE for last-half-hour 0DTE pricing. Found only the claims above. Not found tested on SPXW 0DTE in the sources read. The frontier lane's notes (frontier.md, S1) report that Vilkov tests entries at 15:00 held to the close, unhedged, without a variance ratio for the last slice.
8. **Why it may fail.** The spread is widest at the close; the frontier lane's S2 notes that Almeida et al. stop at 14:00 for that reason. Buying at the ask may eat the whole gap. One-minute quotes near 16:00 may be stale or crossed. FSU's own edge may be execution (working orders inside a wide market), which a mid-to-ask test cannot reproduce.

### Card 2. The weekend is charged by convention — desk can test

1. **Name.** Friday's price of the Monday expiry sheds more over the weekend than the weekend moves.
2. **Mechanism.** Market makers do not want to hold theta over a weekend, so they shade prices before it. One reported practice is to advance the pricing clock by a day from Thursday 11:00. How much weekend decay goes into Friday's quotes is therefore a desk convention (365-day, 252-day, or something in between), not a measurement of weekend variance. If the convention charges the weekend more than the weekend realises, Friday-afternoon sellers of the Monday expiry are overpaid. If it charges less, they are underpaid.
3. **Prediction.** From Friday 15:55 to Monday 9:35, the Monday-expiry ATM straddle loses more implied variance than the realised variance of the weekend gap. A Friday-close seller who buys back at Monday 9:35 earns more per unit of premium than the same trade made Monday to Thursday into the next day's expiry.
4. **Kill line.** The weekend version is not better than the weekday nights by more than one round-trip spread, on both half-years.
5. **Data needed.** Held. The Monday expiry sits in the one-to-seven-day file on Friday, and is the same day's expiry on Monday.
6. **Evidence.**
   - SteadyOptions forum, "Theta Decay Question", 28 Aug 2013, https://steadyoptions.com/forums/forum/topic/1473-theta-decay-question/ — a poster relays a market maker who sets his software clock forward one day from Thursday 11:00, and infers that selling in the morning beats selling at the close. [unknown], second-hand. SteadyOptions sells a newsletter: [seller].
   - Kris Abdelmessih, Moontower, "weekend theta", 20 Mar 2025, https://moontower.ai/blog/weekend-theta [named practitioner: former options market maker; seller: moontower.ai vol tools] — on the floor with a 365-day model, the market decayed options by about 2/3 of model theta over a weekend, which fits overnight ≈ 0.25 day and weekend days ≈ 0.5. Warns "this is not free money" because weekend gaps grow when more assets trade over the weekend.
   - newwurldmn [anonymous, credible: long record of specific vol answers], Elite Trader, "Theta over weekends versus overnight", 12 Jan 2018, https://www.elitetrader.com/et/threads/theta-over-weekends-versus-overnight.316988/ — zero weekend theta is acceptable, some is better, but "it's not okay to ascribe a full trading day."
   - Elite Trader, "No decay over weekends?", 22 Oct 2020, https://www.elitetrader.com/et/threads/no-decay-over-weekends.351639/ — BlueWaterSailor cites the OIC (seven days of decay over five trading days) and a tastytrade study. The opening post quotes Vance Harwood's claim that market makers discount before the weekend so that Monday opens unchanged. No test in the thread.
7. **Already tested?** Searched Elite Trader, SteadyOptions and Quant SE for weekend decay in SPX weeklies. Found claims and a tastytrade study cited second-hand, which I did not read. Not found tested on SPXW 0DTE or the Monday expiry in the sources read. The desk knows that nights are about a third of a week's movement and that one day ahead realises 5% to 13% under implied. It has not split the weekend out (own-data card 6 is close but not the same).
8. **Why it may fail.** About 50 weekends a year, and the result will hinge on a few weekend gaps. Monday 9:35 quotes are noisy. If the market already uses the 2/3 rule, the difference may be smaller than the spread.

### Card 3. Hedge back to the band edge, not to zero — desk can test

1. **Name.** Partial re-hedge to the band edge.
2. **Mechanism.** A short-gamma hedger whose delta crosses the band usually trades back to zero. In a market that mean-reverts inside the day (long-gamma dealers hedging against moves is one proposed cause), much of that hedge is reversed soon after, paying the futures spread twice. Trading only the excess, back to the band edge, cuts the whipsaw and the cost, while still bounding the delta.
3. **Prediction.** Re-run the desk's one-sixth band seller with hedges sized only back to the band edge. On both half-years, the number of hedge trades falls by at least 30%, and the cost saved is larger than the rise in the standard deviation of hedged window P&L is worth (judged against the desk's own variance budget).
4. **Kill line.** No fall in cost net of extra variance on the fresh half-year, or a worse worst day.
5. **Data needed.** Held (index path from the implied forward; the desk's band code).
6. **Evidence.**
   - sle [anonymous, credible: careful vol answers across many ET threads; other posters defer to the handle], Elite Trader, "Managing Deltas / Hedging Frequency", 2 Nov 2018, https://www.elitetrader.com/et/threads/managing-deltas-hedging-frequency.326612/ — a fixed delta limit works, better as a hysteresis band: "hedge to the limit, not to flat". Check at any interval and trade only the excess (delta 35 against a limit of 25 → trade 10). He says this does not change the expected P&L but cuts whipsaw losses and cost. In the same thread TommyR [unknown] calls fixed delta bounds the worst choice because they pick extremes, and TheBigShort leans short delta on short SPX straddles (own-data card 2 territory).
   - Quant SE, "Delta-hedging frequency directly affects PnL...?", Feb 2023, https://quant.stackexchange.com/questions/74687/delta-hedging-frequency-directly-affects-pnl-and-not-just-pnl-smoothness-and-va — with independent returns, frequency only changes P&L variance; "your P/L is definitely affected by your choice of hedging interval" once intraday returns are autocorrelated. [unknown]
7. **Already tested?** Not found tested on SPXW 0DTE in the sources read. A Wilmott thread on transaction costs names the Leland and Whalley-Wilmott hedging models, but I saw it only as a search excerpt and did not open it. The literature lane may hold those results.
8. **Why it may fail.** If the index trends inside the band more than it reverts, sitting at the edge leaves the book longer in the losing direction. Futures cost for a hedge is small next to the option spread, so the saving may be a rounding error.

### Card 4. Sell the overnight, buy the day — desk can test

1. **Name.** The same-day expiry is cheap against tomorrow's.
2. **Mechanism.** Yield-seeking sellers, mostly retail defined-risk spreads, concentrate supply in the same-day expiry. destriero says the flow has "flattened the surface". The next-day expiry carries the overnight, which the desk already knows is charged above what it delivers. A gamma-matched calendar (long the 0DTE straddle, short the 1DTE straddle, both delta-hedged over the same daytime window) strips the overnight out and isolates the daytime price difference.
3. **Prediction.** Enter at 10:00 with the two straddles matched on dollar gamma, hedge both on the desk's band, and close at 15:35. Average P&L after both spreads is above zero on both half-years. Put another way: 0DTE implied variance to 16:00 is below the 1DTE implied variance net of an overnight allowance set at the measured night share.
4. **Kill line.** Calendar P&L after spreads at or below zero, or the 0DTE daytime implied variance at or above the 1DTE daytime part on average.
5. **Data needed.** Held (0DTE and one-to-seven-day files).
6. **Evidence.**
   - destriero [anonymous, credible: long-time ET vol poster with detailed structure talk across hundreds of threads; abrasive], Elite Trader, "0DTE options craze", 30 Sep 2023, https://www.elitetrader.com/et/threads/0dte-options-craze.376425/ — "I am always a buyer of 0DTE in index". He holds them against short back-month vol to stay root-time-neutral in vega and pays the negative "switch" edge (front against second expiry) to be flat or long dollar gamma. In "ODTE options .... pros/cons?", 30 Mar 2023, https://www.elitetrader.com/et/threads/odte-options-pros-cons.372975/page-10 he says 0DTE flow flattened the surface.
   - Against: the frontier lane's notes (frontier.md, S2) report Almeida, Freire and Hizmeri finding an annualised variance premium of 1.54% to 2.95% for 0DTE against 0.55% for 1DTE. That says the same-day expiry is the richer one.
7. **Already tested?** Not found tested as a same-window calendar on SPXW in the sources read. The desk has measured each leg alone: windows realise 1.0 pooled for 0DTE, and one day ahead realises 0.87-0.95 with nights counted.
8. **Why it may fail.** Two spreads to pay. The overnight allowance is a choice, and the result may depend on it. destriero's practice is about vega neutrality across months, not about 0DTE versus 1DTE alone.

### Card 5. The 3:50 imbalance step — desk can test

1. **Name.** Variance steps up when the closing imbalance prints.
2. **Mechanism.** The NYSE closing-auction imbalance is published in stages before the close, with the final figure about ten minutes before. Index funds must trade at the close, and algorithms hedge the imbalance in ES as soon as it prints. A NexusFi trader dates a new burst of volatility at 15:50 to 2020. If the 0DTE chain prices the last 25 minutes smoothly, the step at 15:50 is under-charged.
3. **Prediction.** Realised variance per minute from 15:50 to 16:00 is at least 1.5 times that from 15:35 to 15:50. The 15:45 straddle mid prices the 15:45-16:00 slice below what is realised (pooled ratio above 1).
4. **Kill line.** Per-minute variance ratio below 1.2 (no step), or a pooled ratio at or below 1 (step already priced).
5. **Data needed.** Held for options and the forward. The imbalance figures themselves are not held (they are published by NYSE and relayed by news services).
6. **Evidence.**
   - josh [anonymous, credible: long-time NexusFi ES poster], NexusFi, "Does anybody use Market on Close (MOC) imbalance values in their trading?", 20 Aug 2023, https://nexusfi.com/showthread.php?p=889041&t=60003 — remembers the day in 2020 when 3:50 MOC algorithms started; before then "there was no volatility increase at 3:50". jlabtrades [unknown] in the same thread: the final figure comes 10 minutes before the close, the first reaction often goes against its sign and then reverses, and a large earlier move means a quieter close. Anecdote from a few days.
7. **Already tested?** Not found tested on SPXW 0DTE in the sources read. Can be run together with card 1.
8. **Why it may fail.** The step may be real and already priced (a smile and level that rise into 15:50). The last-minute spread may swamp it. The 2020 date is one trader's memory.

### Card 6. Band width set by the day's own autocorrelation — desk can test, weak

1. **Name.** Narrow the band when the tape trends, widen it when it chops.
2. **Mechanism.** A short-gamma hedger loses by waiting when moves continue and gains by waiting when they reverse. If the sign of intraday autocorrelation persists for an hour or two (for example, because dealer gamma changes slowly through the day), a band set from trailing autocorrelation beats a fixed band.
3. **Prediction.** Setting the band width each 30 minutes from the trailing 60-minute variance ratio (variance of 5-minute returns over five times the variance of 1-minute returns) raises the hedged seller's P&L after cost against the fixed one-sixth band, on both half-years.
4. **Kill line.** No improvement on the fresh half-year.
5. **Data needed.** Held.
6. **Evidence.**
   - TheBigShort [anonymous, credible: research-style posts using ORATS data across many threads], "Managing Deltas / Hedging Frequency", Nov 2018 (link in card 3) — tests autocorrelation to decide trending or reverting, narrows the band when short vol in a trend, and lets deltas run when mean-reverting. Work in progress; no result posted.
   - Wilmott, "What is Gamma scalping, really?", Dec 2017, https://forum.wilmott.com/viewtopic.php?t=101046 — one reply: let delta accumulate in trending markets and hedge more in sideways ones. [unknown]
7. **Already tested?** Not found tested on SPXW 0DTE in the sources read. **The desk's own result argues against it**: trending and choppy regimes describe returns and do not predict them, and own-data card 3 failed on the seen half.
8. **Why it may fail.** The desk has already shown that trailing straightness does not forecast the next window. This card survives only if the band reacts within a window, faster than the desk's 30-minute test did.

### Card 7. Event premium is set off the last event — needs more history

1. **Name.** FOMC and CPI straddles are priced from the last reaction, not the base rate.
2. **Mechanism.** Sellers who were hurt at the last event mark the next one up, and those who were paid mark it down. Event-day premium then follows the previous same-type event's move more than it follows the event's true spread of outcomes.
3. **Prediction.** Across FOMC and CPI days, the 9:45 event-day straddle premium above its prior five-day average has a rank correlation above 0.3 with the absolute move at the previous event of the same type, while the realised event-day move does not. Selling after a large previous move earns more than selling after a small one.
4. **Kill line.** No correlation of premium with the lagged move, or an equal correlation of the realised move with it.
5. **Data needed.** One year is held (about 8 FOMC and 12 CPI days), which is far too few. It needs several years of SPXW history from a vendor.
6. **Evidence.** Russell Rhoads PhD CFA [named practitioner: former Cboe education head and academic; seller: paid Substack], reposted by ajacobson on Elite Trader, "SPX, NDX, And RUT 1-Day Option History Around FOMC Announcements", 30 Jan 2024, https://www.elitetrader.com/et/threads/spx-ndx-and-rut-1-day-option-history-around-fomc-annoucements.378153/ — twelve FOMC days from July 2022 averaged ±1.19% in SPX, and 1-day ATM straddles underpriced the last three. "premiums following the outlier moves appear to be influenced by the most recent reaction". Charts only, no test.
7. **Already tested?** Not found tested on SPXW 0DTE in the sources read.
8. **Why it may fail.** Too few events per year to separate recency from a regime shift in Fed uncertainty. The spread widens on event mornings.

## Methods for finding patterns

**M1. Hypothesis first, then beat random entries.**
1. Write the structural reason before touching data.
2. Run the rule, then run many random entries with the same count and holding time.
3. Keep the rule only if it ranks well above the random set (one poster's bar: longs and shorts each beat 70% of random runs).
- *Meant to catch:* patterns that any entry on that sample would have shown.
- *Where it goes wrong:* NoWorries: without a prior hypothesis, "some would look like having an edge even though they're completely random"; every varied parameter is another test.
- Elite Trader, "is there way to statistically quantify or find an 'edge' in a system?", 25 Jan 2007, https://www.elitetrader.com/et/threads/is-there-way-to-statistically-quantify-or-find-an-edge-in-a-system.85578/ — TraDaToR, MustPlayOptions, NoWorries [unknown]. Quant SE answer by Patrick Burns (M6) makes the same random-trade comparison.

**M2. Pick from the plateau, not the peak.**
1. Sweep the parameter.
2. Look for a broad range that is profitable.
3. Choose the middle of the range and reject "fragile" settings, where 37 works but 36 and 38 fail.
- *Meant to catch:* a parameter that fits one or two lucky trades.
- *Where it goes wrong:* intradaybill: you swap curve-fitting for selection bias. Dacamic: any rule with parameters is optimised whether you swept it or not.
- Elite Trader, "How do you avoid overfitting or over-optimization in your backtest?", 24 Feb 2010, https://www.elitetrader.com/et/threads/how-do-you-avoid-overfitting-or-over-optimization-in-your-backtest.192056/ — stevegee58: "I look for 'fragile' settings". [unknown]

**M3. Halve or double only, and hide the test set on another machine.**
1. Change a parameter only by halving or doubling it, and move on if neither helps.
2. Keep the out-of-sample universe on a separate laptop so it cannot be peeked at during design.
3. Assume every strategy is curve-fitted until shown otherwise; ValeryN adds a checklist (1,000+ trades, survivorship, expect twice the backtest drawdown live).
- *Meant to catch:* fine-tuning and silent peeking.
- *Where it goes wrong:* Zwaen: over-testing costs the years in which an edge still works; test small with real money.
- Elite Trader, "How to know whether I am overfitting?", 26 May 2021, https://www.elitetrader.com/et/threads/how-to-know-whether-i-am-overfitting.358985/ — ValeryN and an unnamed reply [unknown].

**M4. Freeze the hypothesis and never re-explain a failure.**
1. Fix the fitting and testing windows before running.
2. If the rule fails out of sample, abandon it and start a new hypothesis.
3. Do not adjust the old one to explain the data it failed on, though a failure may still teach you why.
- *Meant to catch:* the drift from testing into story-telling.
- *Where it goes wrong:* globalarbtrader: walk-forward is fine but "fitting using small amounts of data is crazy". The original poster found that 30/10-day re-optimisation destroyed a rule that a plain 4-year/2-year split kept.
- Elite Trader, "Your Thoughts On Walk-forward Testing To Assess Robustness", 5 Jan 2020, https://www.elitetrader.com/et/threads/your-thoughts-on-walk-forward-testing-to-assess-robustness.339240/ — tommo, an unnamed reply, globalarbtrader.

**M5. Many rolling out-of-sample rounds, not one.**
1. Optimise on a short window (3 months).
2. Validate backward on a long window (3 years: two out-of-sample periods and five or six stress tests).
3. Test forward, roll, and repeat across history.
4. Trade only setups that survive every round, plus Monte Carlo and parameter-stability tests.
- *Meant to catch:* a result that held in one split by luck.
- *Where it goes wrong:* Tuxan: "You are doing vibe-statistics" — a search of a million variants is not made honest by later windows if the method itself kept changing.
- Elite Trader, "Many people mistake overfitting for backtesting...", 8 Aug 2026, https://www.elitetrader.com/et/threads/many-people-mistake-overfitting-for-backtesting-while-most-people-make-the-opposite-mistake.390877/ and "Debunking the myth...", 12 Aug 2026, https://www.elitetrader.com/et/threads/debunking-the-myth-if-you-backtest-too-many-ideas-you-will-just-overfit.390953/ — quantrader [seller: runs strategies offered as Darwinex investable "Darwins"], forex.

**M6. Correct for the number of buckets you looked at.**
1. Count every hypothesis tested, including the ones you dropped.
2. Use Benjamini-Hochberg, White's Reality Check, Hansen's SPA or Romano-Wolf rather than a lone t-test. Bonferroni (alpha divided by the number of buckets) is the strict fallback.
3. Split the sample into sub-periods and require the effect in each.
- *Meant to catch:* the one time bucket in 24 that clears 5% by chance (the own-data lane's twelve half-hours are exactly this case).
- *Where it goes wrong:* gappy: Bonferroni is too strict. Brumder: news, not the clock, drives most intraday returns, so the bucket test can be mis-specified.
- Quant SE, "What are the popular methodologies to minimize data snooping?", Feb 2011, https://quant.stackexchange.com/questions/140/what-are-the-popular-methodologies-to-minimize-data-snooping and "Hourly Returns Statistical test", Jan 2017, https://quant.stackexchange.com/questions/32078/hourly-returns-statistical-test — gappy, shabbychef, Richard Herron, Patrick Burns, Comp_Warrior, David Kozak [unknown].

**M7. Measure realised vol as the hedger would earn it.**
1. Give a simulated book an imaginary 1,000 gamma.
2. Flatten delta at every 0.5 SD (or $1) move and at the close, on tick data.
3. Book P&L as the average delta over each move times the move.
4. Convert the P&L back into a volatility, much as one solves for a day of theta, and compare that with implied vol.
- *Meant to catch:* the gap between close-to-close vol and what a band hedger actually collects.
- *Where it goes wrong:* he calls it time-consuming and expensive; the result depends on the chosen band.
- Matt_ORATS (Matt Amberson) [named practitioner: ran a group of floor traders; seller: ORATS], Elite Trader, "Calculation of historical/realized volatility", 1 Jan 2022, https://www.elitetrader.com/et/threads/calculation-of-historical-realized-volatility.363900/ — says it "matched what we were experiencing in the market".

**M8. Price the window, not the trade.**
1. Do not trust a backtest of stops and take-profits on option bars.
2. Take the distribution of index moves over the trade's window, across all days.
3. Compare it with the distribution the option prices implied at entry.
4. Only then add exit rules.
- *Meant to catch:* stop-fill fiction. The backtest in that thread filled stops at the option's 15-minute high.
- *Where it goes wrong:* it ignores path-dependent exits that a trader really uses (cesfx: the originator trades it with discretion).
- Elite Trader, "Day trading 0DTE Condors", 7-16 Feb 2024, https://www.elitetrader.com/et/threads/day-trading-0dte-condors.378216/page-6 — reply whose handle the page text does not show.

**M9. Find the market's own clock before calling vol cheap.**
1. Price with a calendar-day model.
2. Each Monday, record how much of the model's weekend theta the market actually took.
3. Add the untaken part back in vol points and call that "vol unchanged".
4. Read only departures from that benchmark as vol moves.
- *Meant to catch:* the false "vol rises on Monday" effect, and its intraday cousin: what time weighting the market applies to each part of the day.
- *Where it goes wrong:* he says the error is small in vol points, and weekend variance changes as more assets trade on weekends.
- Moontower, "weekend theta", 20 Mar 2025 (card 2).

**M10. Fit a smooth smile and look for strikes off it, in bid-ask terms.**
1. Plot implied vol against strike for one expiry.
2. Fit a spline with fewer degrees of freedom than strikes.
3. Points far above or below are candidates.
4. Translate bid and ask into vols; most "mispricings" sit inside the spread.
5. Also compare today's smile with its historic shape, shifted to pass through the ATM vol.
- *Meant to catch:* single strikes priced out of line with their neighbours or with history.
- *Where it goes wrong:* out-of-the-money candidates are usually unfillable, by his own warning.
- globalarbtrader [named practitioner: Rob Carver, former AHL portfolio manager; seller: books], Elite Trader, "How do you value vol?", 5 Mar 2020, https://www.elitetrader.com/et/threads/how-do-you-value-vol.341175/. Same idea per delta, intraday: VolSkewTrader [unknown, offers a data service] and the taowave skew ratio (25-delta put minus 25-delta call, over the 50-delta vol), in "Pricing Skew/Identifying Mispriced Non-ATM options", Apr 2020, https://www.elitetrader.com/et/threads/pricing-skew-identifying-mispriced-non-atm-options.343261/.

**M11. Audit the measuring stick.**
1. Check whether a regime that "lasts about 30 days" is just the 30-day window.
2. Compare like with like: ATM vol, not VIX, which sits near a 90%-moneyness strike.
3. Do not compare buckets of 3,102 days with buckets of 56.
4. Use vol points, not percent, for a mean-reverting series.
- *Meant to catch:* artefacts of the method.
- *Where it goes wrong:* nothing raised.
- morganpbrown [unknown] catches his own overlap artefact in "Calculation of historical/realized volatility" (M7 link); TheBigShort's critique in "If you had to choose between VRP and TRP?", 30 Jan 2020, https://www.elitetrader.com/et/threads/if-you-had-to-choose-between-vrp-and-trp.339940/.

**M12. Disprove fast and small.**
1. When history is missing or costly, trade the idea at minimum size to collect the data.
2. Treat the fees as the price of the test.
3. Drop most ideas quickly.
- *Meant to catch:* months spent building a test for an idea that fails at first contact.
- *Where it goes wrong:* a few live weeks are not a sample, and his 0DTE idea (straddle side from trailing realised against implied) is one the desk has already rejected.
- Kris Longmore [named practitioner; seller: Robot Wealth courses], "Trading 0DTE Options with the IBKR Native API", 24 Mar 2024, https://robotwealth.com/trading-0dte-options-with-the-ibkr-native-api/ (linked from the ET "0DTE automated options system" thread) — "I want to disprove ideas quickly".

**M13. Pre-commit a stop rule and a public log.**
1. Before going live, write the condition that ends the trial (kalapur73: three straight losses sends the trade back to paper).
2. Log every trade weekly with a written take-away.
3. Tally at a fixed horizon (caroy planned 16 trades over two months).
- *Meant to catch:* survivorship inside your own record.
- *Where it goes wrong:* caroy's journal ran 35 weeks, was profitable only marginally, and ended with "the returns are not where I want"; kalapur73 never reported back.
- Elite Trader, "0DTE options craze", Sep 2023 (card 4 link), and "Weekly Pin Butterfly Strategy", Jan-Oct 2021, https://www.elitetrader.com/et/threads/weekly-pin-butterfly-strategy.354495/ [unknown].

### What the desk could do with each method on one-minute SPXW quotes

| Method | On the desk's data |
|---|---|
| M1 random entries | Yes: compare any timed rule with random entry minutes, same count and holding time. |
| M2 plateau | Yes: sweep band width or entry time and keep only broad profitable ranges. |
| M3 halve/double, hidden set | Yes: the seen/fresh split already does the hiding; add later days as a third hidden set. |
| M4 freeze hypothesis | Already the desk's practice (claims committed before the fresh days were opened). |
| M5 rolling rounds | Partly: one year gives few rounds; useful once later days are added. |
| M6 multiplicity | Yes: apply BH or Bonferroni across the twelve half-hours and to any card here that tests several windows. |
| M7 hedger's realised vol | Yes, on the minute forward path with the desk's own band, in place of close-to-close realised vol. |
| M8 price the window | Yes: realised against implied variance per window is already the desk's frame; use it for cards 1 and 5 before any exit rule. |
| M9 market's clock | Yes: measure how 0DTE and 1DTE implied variance decays through the day and over nights and weekends (card 2). |
| M10 smile residuals | Yes, per minute: fit the smile and flag strikes off it after converting bid and ask to vols. |
| M11 audit the stick | Yes: check window overlaps and bucket sizes in every result table. |
| M12 trade small | Not on historical data; only as a live pilot. |
| M13 stop rule and log | Not on historical data; applies to any live pilot of a card. |

## What stopped working

- Overnight drift in index futures: about 3.7% a year in the 2:00-3:00 ET window in 1998-2020, about zero in 2021-2025. Reason given: the dispersion of last-hour order imbalance halved, from 6.5% to 2.9% (NY Fed Liberty Street, 1 Jul 2026, https://libertystreeteconomics.newyorkfed.org/2026/07/the-disappearing-overnight-drift/). ET posters were still asserting it in Nov 2022 (https://www.elitetrader.com/et/threads/the-overnight-drift-higher-in-index-futures.163298/page-33), and a Trade2Win poster called it "most reliable" in Jan 2026 (https://www.trade2win.com/threads/a-professional-approach-to-trading-futures.242544/page-33).
- Selling 0DTE ATM straddles at the open: lost money over 2022 in dorietrading's own backtest (−16,203 before costs, worst drawdown on 29 Apr 2022). TheDawn asserts it worked before Covid. https://www.elitetrader.com/et/threads/sell-daily-spx-straddles.369734/
- Index weekly iron condors and deep-ITM calls: two or three very good months then a slow bleed, and "February 2018 when nothing seemed to work anymore" (Corto, Dec 2018). https://www.elitetrader.com/et/threads/so-what-works-then.327885/
- Expiry-pin butterflies: Illini Trader made good profits in 2016-17 and then took many maximum losses from early 2018; caroy stopped his highest-open-interest fly strategy in Sep 2021. https://www.elitetrader.com/et/threads/weekly-pin-butterfly-strategy.354495/page-40
- Quiet SPX close: a 15:50 volatility burst began in 2020 when MOC algorithms appeared (josh, 2023). https://nexusfi.com/showthread.php?p=889041&t=60003
- Last-seconds index expiry trades: weaker than they were because of match-cash-close futures trading (unattributed reply, 2017). FSU adds that such trades come and go. https://www.elitetrader.com/et/threads/underpriced-spx-options-at-expiration.314509/page-2
- SPX surface shape: "0DTE has flattened the surface" (destriero, Mar 2023). https://www.elitetrader.com/et/threads/odte-options-pros-cons.372975/page-10

## Disagreements

| Point | One side | Other side | Test that settles it |
|---|---|---|---|
| Last half-hour of expiry day | Cheap: FSU (2017) buys it | Rich: dorietrading's last-hour short strangle paid 2018-23; Matt_ORATS's last-14-minutes result is ambiguous | Card 1: realised against implied variance, 15:35-16:00, at mid and at the ask |
| Weekend decay | OIC via BlueWaterSailor: seven days of decay over five | Harwood (quoted in the opening post): no decay, market makers discount on Friday; Moontower: about 2/3; newwurldmn: some, not a full day | Card 2: Friday 15:55 to Monday 9:35 premium drop against gap variance |
| Fixed delta band | sle: works, better as hysteresis | TommyR: the worst choice, it picks extremes | Card 3: fixed band to zero, against band to edge, against time-based hedging |
| Is index 0DTE cheap? | destriero: always a buyer | Almeida et al. (frontier lane): 0DTE variance premium larger than 1DTE | Card 4: gamma-matched 0DTE/1DTE calendar |
| Take a quick profit after selling | ffs1001: close within minutes at a small fixed profit after the open calms | TheDawn and dorietrading: same risk, cuts the winners | Seller at 9:45 with a take-profit rule against hold-to-15:35, same entries, on desk data |
| Hedge frequency and trend | TheBigShort, Wilmott reply: hedge more in trends | Quant SE: frequency changes only variance unless returns are autocorrelated | Measure intraday autocorrelation first; card 6 only if it is non-zero and persistent |
| Pinning at the max-open-interest strike | caroy: saw it as a MM in commodities | OptionsOptionsOptions, taowave: "an illusion" | Needs open interest by strike, which the desk does not hold |
| Overnight drift | steven46 (Trade2Win, 2026): most reliable | NY Fed (2026): gone since 2021 | Already settled against by the NY Fed sample |

## Handles and threads worth following

- **FSU** (Elite Trader): former OEX floor market maker; specific about expiry mechanics. Start with the underpriced-at-expiration thread.
- **sle** (Elite Trader): concise, institutional answers on hedging and vol; the hysteresis-band post.
- **newwurldmn** (Elite Trader): quotes real greek sizes from a live book; good at catching wrong numbers in journals.
- **destriero / dest** (Elite Trader): dense structure talk about switches and root-time-neutral vega; one of the few who says he is long index 0DTE.
- **TheBigShort** (Elite Trader): research-style posts with ORATS data; hedging bandwidth and the VRP size argument.
- **JackRab** (Elite Trader): former European index market maker; how the last day looks from the quoting side.
- **Matt_ORATS** (Elite Trader) [seller]: posts quick backtests and floor-era methods (the simulated-scalp realised vol).
- **globalarbtrader** (Elite Trader): Rob Carver; method discipline and the smile-residual approach.
- **dorietrading** (Elite Trader): posts backtests with stated rules; worth asking for fills and data source.
- **josh** (NexusFi): long-time ES poster with dated microstructure observations (the 3:50 change).

## Could not open

- Reddit — r/options, r/thetagang, r/quant, r/algotrading, r/Vitards. WebFetch refuses old.reddit.com; WebSearch refuses the reddit.com domain; Exa fetch returned SOURCE_NOT_AVAILABLE; curl and the Playwright browser needed permissions that were not granted in this run. Nothing from Reddit is cited.
- Wilmott forum search page (https://forum.wilmott.com/search.php?keywords=0DTE): HTTP 403. Individual topics opened through another tool. "Delta Hedging optimization" (t=93271) and "Transaction Costs and Volatility Level" (t=10292) were seen only as search excerpts and are not cited.
- NuclearPhynance: no archived threads surfaced in search; nothing cited.
- QuantNet forums: no relevant thread surfaced in search; not read.
- NexusFi Elite Trading Journals: members only.
- Elite Trader image attachments (dorietrading's result screenshots, Matt_ORATS's equity charts): images not readable as text; only figures stated in post text are used.
- The tastytrade weekend-decay study cited in the "No decay over weekends?" thread: not opened; cited only as what the poster said.

## Appendix: threads read

| # | Forum | Thread | Date |
|---|---|---|---|
| 1 | ET | Sell daily SPX straddles? (pp. 1-3) | Sep 2022 |
| 2 | ET | Managing Deltas / Hedging Frequency | Nov 2018 |
| 3 | ET | 0DTE automated options system | Mar 2024 – Aug 2025 |
| 4 | ET | Underpriced SPX options at expiration (pp. 1-2) | Oct-Dec 2017 |
| 5 | ET | Theta over weekends versus overnight | Jan 2018 |
| 6 | ET | No decay over weekends? | Oct 2020 |
| 7 | ET | ES/SPX volatility trading journal (pp. 1, 5, 7) — stops 8 Apr 2026 with no result | Apr 2026 |
| 8 | ET | 0DTE options craze | Sep 2023 |
| 9 | ET | ODTE options .... pros/cons? (pp. 1, 10) | Mar 2023 |
| 10 | ET | Day trading 0DTE Condors (pp. 1, 6) | Feb 2024 |
| 11 | ET | Calculation of historical/realized volatility | Jan 2022 |
| 12 | ET | If you had to choose between VRP and TRP? | Jan 2020 |
| 13 | ET | The Overnight Drift Higher In Index Futures (pp. 1, 33) | 2009-2022 |
| 14 | ET | Weekly Pin Butterfly Strategy (pp. 1, 40) | Jan-Oct 2021 |
| 15 | ET | Open Interest Pinning and Butterflies | Jan 2021 |
| 16 | ET | SPX, NDX, And RUT 1-Day Option History Around FOMC | Jan 2024 |
| 17 | ET | how to backtest this option idea? (p. 2) | Sep 2023 |
| 18 | ET | How do you value vol? | Mar 2020 |
| 19 | ET | Pricing Skew/Identifying Mispriced Non-ATM options | Apr 2020 |
| 20 | ET | So what works then? | Dec 2018 |
| 21 | ET | is there way to statistically quantify or find an "edge" | Jan 2007 |
| 22 | ET | How do you avoid overfitting or over-optimization | Feb 2010 |
| 23 | ET | Your Thoughts On Walk-forward Testing | Jan 2020 |
| 24 | ET | How to know whether I am overfitting? | May 2021 |
| 25 | ET | Many people mistake overfitting for backtesting... / Debunking the myth... | Aug 2026 |
| 26 | NexusFi | Does anybody use MOC imbalance values in their trading? | Aug 2023 – May 2026 |
| 27 | Wilmott | What is Gamma scalping, really? | Dec 2017 |
| 28 | Quant SE | What are the popular methodologies to minimize data snooping? | Feb 2011 |
| 29 | Quant SE | Delta-hedging frequency directly affects PnL...? | Feb 2023 |
| 30 | Quant SE | Hourly Returns Statistical test | Jan 2017 |
| 31 | SteadyOptions | Theta Decay Question | Aug 2013 |
| 32 | Trade2Win | A Professional Approach to Trading Futures (p. 33) | Jan-Feb 2026 |

Linked pages also read: Moontower "weekend theta" (Mar 2025); Robot Wealth 0DTE IBKR article (Mar 2024); NY Fed "The Disappearing Overnight Drift" (Jul 2026).

## Reddit threads found by search, not read

Added 9 October 2026 by Claude, after the lane finished. Search still returns Reddit threads, but no reading tool in the session will open one, so each line below rests on a search excerpt only. Nothing here is evidence until someone reads the thread. They are listed so that Lalit can open the ones that matter.

| Thread | Subreddit | Why it may matter (from the excerpt) |
|---|---|---|
| [Trading 0DTE SPX Options Going Into the Close - I'll take Long Gamma](https://www.reddit.com/r/options/comments/1sejgdw/trading_0dte_spx_options_going_into_the_close_ill/) | r/options | Long gamma at 3:50, 3:55 and 3:59 with closing-auction flow. Bears on cards 1 and 5. |
| [Backtesting SPX 0DTE short strangle](https://www.reddit.com/r/options/comments/1mqsn2i/backtesting_spx_0dte_short_strangle/) | r/options | Backtest sold at 9:31 and held to expiry, at the money against 40, 30, 20, 16 and 8 delta. |
| [0DTE straddle modeling](https://www.reddit.com/r/quant/comments/1su3zlr/0dte_straddle_modeling/) | r/quant | At-the-money straddle at the open, delta-hedged through the day: the desk's own structure. |
| [0-30 dte short straddles on SPX, delta hedging with SPY](https://www.reddit.com/r/options/comments/12j0n2y/030_dte_short_straddles_on_spx_delta_heding_with/) | r/options | Hedged short straddles; the replies split the result into theta, gamma and the volatility gap. |
| [Continuous 0DTE ATM short straddles every 5 pt move](https://www.reddit.com/r/options/comments/1msweej/continuous_0dte_atm_short_straddles_every_5_pt/) | r/options | Re-striking a short straddle on each 5-point move, with no hedge. |
| [SPX 0DTE Strangles](https://www.reddit.com/r/PMTraders/comments/1109jdd/spx_0dte_strangles/) | r/PMTraders | A poster who says he backtested puts, calls and strangles from 0 to 4 days. |
| [AMA: Ran a $XXM Systematic Options Book for 5 Years](https://www.reddit.com/r/quant/comments/1okr5l7/ama_ran_a_xxm_systematic_options_book_for_5_years/) | r/quant | Names intraday short gamma in 0DTE as one sleeve of a risk-premium book. |
| [Thinking about and trading volatility skew](https://www.reddit.com/r/quant/comments/1cq04af/thinking_about_and_trading_volatility_skew/) | r/quant | How people at an options shop think about trading the skew. |
| [Back to Thetagang, been trading 0DTE for over a year](https://www.reddit.com/r/thetagang/comments/1qskfpx/back_to_thetagang_been_trading_0dte_for_over_a/) | r/thetagang | A year of 0DTE trading; a reply raises the term structure of the short expiries. |
| [Tom Sosnoff's SPX 1DTE strategy](https://www.reddit.com/r/options/comments/12isx01/tom_sosnoffs_spx_1dte_strategy/) | r/options | Next-day expiry sold and scalped inside the day. |
| [My 3 months of SPX 0dte](https://www.reddit.com/r/options/comments/1kz8113/my_3_months_of_spx_0dte/) | r/options | A live record: three months traded, six on paper. |
| [Do you actually track weekend time decay in your options positions?](https://www.reddit.com/r/options/comments/1v2mmd3/do_you_actually_track_weekend_time_decay_in_your/) | r/options | Weekend decay, for card 2. |
| [theta decay over the weekend?](https://www.reddit.com/r/options/comments/11ap58t/theta_decay_over_the_weekend/) | r/options | A reply says the weekend's decay is taken on Friday. For card 2. |
| [How do you actually know when you've overfit?](https://www.reddit.com/r/algotrading/comments/1s37rar/how_do_you_actually_know_when_youve_overfit/) | r/algotrading | Method: study the data with plain statistics before any backtest. |
| [Backtesting: Methods To Avoid Overfitting](https://www.reddit.com/r/algotrading/comments/qtyuxb/backtesting_methods_to_avoid_overfitting/) | r/algotrading | Method: a held-back sample as the stand-in for live results. |
| [Backtesting vs Reality: How Do You Know a Strategy Truly Has an Edge?](https://www.reddit.com/r/algotrading/comments/1qwfs10/backtesting_vs_reality_how_do_you_know_a_strategy/) | r/algotrading | Method: trust a result that worsens slowly as the assumptions get harsher. |
