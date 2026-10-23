> Lane frontier, 47 sources read, 9 cards, 2026-10-08

## Summary

- The same-day literature from 2022 to 2026 is now large: about 20 academic papers, Cboe's own notes, and Fed, BIS and ECB studies. Its settled facts are in *Known and taken* below. Nothing there is new.
- The unconditional same-day premium is real and small. Vilkov puts the median at about 0.0011% of the index from 10:00. Chong and Todorov find it sits in large jumps, and they find no arbitrage in small moves. Every independent backtest of condors and flies fails once the spread is paid.
- The dealer-gamma papers agree on the sign of the effect: gamma is mostly positive and lowers volatility. They do not agree on who holds it (Cboe against Beckmeyer et al.), or on whether 0DTE volume raises volatility (Brogaard et al. against Adams et al.). Adams et al. and Ardia-Vaudescal place the dampening in the **older expiries**, not the same-day flow.
- Intraday momentum, the base of most "trend" ideas, has no unconditional slope in the 0DTE era. It shows only on days when dealers are short gamma (one seller's data, weak).
- The papers leave four gaps. Nobody studies the first half-hour: Almeida et al. and Song both start at 10:00 because of spreads. Nobody prices a 10:00 release inside the day. Nobody splits the same-day premium by wing on minute quotes, and the two papers that touch it disagree. Nobody tests the closing-auction ten minutes for P&L.
- Strongest cards: the 10:00 release premium (card 1), which also bears on oddity 1; down-trend half-hours carry the tail (card 2, oddity 3); which wing carries the premium (card 3).
- Oddity 2 (implied vol rises on falls, flat on rises) has a known shape in the literature, from Hibbert et al. and from the EuroStoxx and DAX intraday work. My own reading (card 5) is that a held strike mixes two effects: a shift of the whole smile level and a slide along a U-shaped smile. That would make the asymmetry partly mechanical. It is testable on the desk's data.

## Cards

### 1. The 10:00 release premium

1. **Name.** Options charge for the 10:00 releases inside the first half-hour.
2. **Mechanism.** Several US releases come out at 10:00 New York time: ISM manufacturing and services, JOLTS, University of Michigan sentiment, new and pending home sales, factory orders and construction spending. They fall inside the 9:35 to 10:05 window. Dealers and hedgers who are short same-day gamma must quote through a known jump time. The event papers show that the premium is paid where the uncertainty resolves. Johannes, Kaeck and Seeger find FOMC straddles lose over the statement. Song finds that 0DTE prices "any regularly anticipated concentration of price discovery". Londono and Samadi find ISM-spanning expirations dearer, though only marginally. Ordinary days have no such jump. So if the first half-hour's excess charge is an event premium, it should sit on release days.
3. **Prediction.** For the 9:35 to 10:05 straddle, the ratio of realised to charged variance is lower on days with a scheduled 10:00 release than on days without one, on both half-years. Within the window, realised variance on release days concentrates in 10:00 to 10:03.
4. **Kill line.** The ratio is the same, within its day-reshuffled spread, on release and non-release days. Or the excess charge is as large on no-release days.
5. **Data needed.** Held: one-minute quotes, the forward and the window variance as already built. Also needed, free: the release calendars (BLS for JOLTS, ISM, University of Michigan, Census). FirmTape and Bloomberg also carry the calendar.
6. **Evidence.**
   - Release-spanning SPX expirations carry higher IV and VRP; ISM effects marginal. https://www.federalreserve.gov/econres/ifdp/the-price-of-macroeconomic-uncertainty-evidence-from-daily-options.htm, June 2023, "most of these estimates are marginally statistically significant" [exchange or regulator]
   - 0DTE prices scheduled concentrations of price discovery by accumulation and release. https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7412318, August 2026, "whether macroeconomic or microstructural" [academic]
   - Straddles spanning the FOMC statement lose; the premium is paid at resolution. https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4484011, 2023/2026, "ATM straddle returns falling by 4-5% around the announcement" (discussant's summary) [academic]
   - Gao et al.: first half-hour digests news; momentum stronger on news days. https://www.sciencedirect.com/science/article/abs/pii/S0304405X18301351, 2018, "The digestion of new information usually takes about 30 minutes" [academic]
7. **Already tested?** I searched for 0DTE studies of 10:00 releases and of the opening half-hour. Londono and Samadi test at the expiry level only. Almeida et al., Song and Vilkov all start at 10:00 or later. Not found tested on SPXW 0DTE in the sources read.
8. **Why it may fail.** The spread is widest at the open (Almeida et al.), so even a real premium may not pay. The excess may come from the opening auction or overnight news, not the 10:00 data; a rival card is 1b below. Most 10:00 releases are minor, so the release set must be fixed before the data is opened.

**1b (rival, same test).** If the excess charge is the same on release and non-release days, the opening itself is the focal burst. In that case the excess should sit in 9:35 to 9:45, and it should shrink on days with a small overnight gap. This is still not tested in the sources read.

### 2. Down-trend half-hours carry the tail

1. **Name.** Skip only after a loud *falling* half-hour.
2. **Mechanism.** Customer positioning in index options leans to puts. The ECB box argues that one-sided positioning makes hedging impact "skewed to the downside (upside)" when puts (calls) dominate. A loud fall also raises implied vol (oddity 2; Hibbert et al.), so a seller re-entering after a fall loses on vega as well as gamma. Continuation appears only when hedgers are short gamma (Baltussen et al.; FirmTape's dealer-short days; Dim-Eraker-Vilkov's low-gamma states). Short gamma on the downside is the usual case after a fall.
3. **Prediction.** Split the desk's "skip after a loud trending half-hour" rule by the sign of that half-hour. Skips after falls deliver most of the worst-day reduction on both half-years. Skips after rises cost average return and cut little tail.
4. **Kill line.** Rise-triggered and fall-triggered skips cut the worst day by similar amounts.
5. **Data needed.** Held.
6. **Evidence.**
   - Positioning one-sided in puts skews hedging impact downward. https://www.ecb.europa.eu/press/financial-stability-publications/fsr/focus/2023/html/ecb.fsrbox202311_02~0cf2c71d00.it.html, November 2023, "skewed to the downside (upside)" [exchange or regulator]
   - Momentum stronger in low-gamma states, 10 bp per hour. https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4692190, June 2025, "positive (negative) Market Makers' inventory gamma strengthens intraday price reversal (momentum)" [academic]
   - 0DTE-era continuation only on dealer-short days. https://firmtape.com/research/is-intraday-momentum-still-alive, August 2026, "continuation reappears with the right sign in all five years" [seller]
   - The return-implied vol asymmetry is concentrated in extreme moves. https://faculty.fiu.edu/~dupoyetb/return_vola.pdf, 2008, "most closely associated with extreme changes in the index returns" [academic]
7. **Already tested?** I searched for intraday momentum and reversal conditioned on the sign of the prior move in 0DTE options. None of the papers splits by sign for a seller's next window. Not found tested on SPXW 0DTE in the sources read.
8. **Why it may fail.** The desk's year holds few tail days, so one or two days can decide the result. This is a second filter on the same 249 days, so it must be fixed now and judged on new days. It costs nothing in spread, because it only removes trades.

### 3. Which wing carries the same-day premium

1. **Name.** Upside or downside: where the 0DTE premium lives.
2. **Mechanism.** Two sources disagree. Almeida, Freire and Hizmeri find that for 0DTE only, "good" (upside) VRP is larger than downside VRP. They link it to a pricing kernel that is high for gains, which suggests buyers of calls overpay (retail is 69% calls in Bryzgalova et al.). Vilkov finds put ratio spreads (short far puts) the best same-day structure and call ratio spreads unattractive. That says the premium is in the downside wing. Both used SPX; the samples and entry times differ.
3. **Prediction.** For each 30-minute window, build the implied upside and downside semivariance from OTM calls and OTM puts (the split Vilkov uses). Set each against realised up and down semivariance from one-minute forwards. If Almeida is right, the realised/implied ratio is lower on the call side, on both half-years.
4. **Kill line.** It is lower on the put side, which favours Vilkov. Or the two sides are equal within the reshuffled spread.
5. **Data needed.** Held (all strikes each minute).
6. **Evidence.**
   - Upside VRP exceeds downside VRP for 0DTE only. https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4701401, June 2025, "investors require more compensation for positive market returns" [academic]
   - Put ratio spread net Sharpe 0.93 out of sample; call ratio unattractive. https://github.com/vilkovgr/0dte-strategies/blob/main/docs/paper/paper-annotated.md, January 2026, "selective timing opportunities rather than ... a broad unconditional edge" [academic]
7. **Already tested?** Almeida et al. measure the split at 10:00 to 14:00 to the close, 2012 to March 2025. Vilkov tests structures to the close. Neither tests 30-minute windows on minute quotes in 2025-26. Not found tested on SPXW 0DTE in the sources read.
8. **Why it may fail.** Almeida et al. show their mispricing trade "mostly stagnates" after 2022, so the upside premium may be gone. A single year also cannot separate the wing premium from the year's drift.

### 4. Sell the statement, not the press conference

1. **Name.** On FOMC days the premium ends at 14:00.
2. **Mechanism.** Hedgers buy protection for the 14:00 statement. Song finds 0DTE event uncertainty rises from 0.60% at 10:00 to 0.78% before 14:00, collapses to 0.34%, then rebuilds to 0.42% before the 14:30 press conference. Johannes, Kaeck and Seeger find straddles lose over the statement and break even over the press conference. They disagree on where most event variance resolves.
3. **Prediction.** A hedged 0DTE straddle sold at 13:55 and bought at 14:20 earns more per unit of charged variance than one sold at 14:20 and bought at 15:00.
4. **Kill line.** The statement window's realised/charged ratio is at least 1, or no lower than the press-conference window's.
5. **Data needed.** Held, but about 8 FOMC days in the year. Earlier years cost money; later days are free.
6. **Evidence.** Song (S24) and Johannes-Kaeck-Seeger (S26), as above. Wright: S&P FOMC event VRP 0.248, significant. https://www.nber.org/system/files/working_papers/w28306/w28306.pdf, 2020, "Average variance risk premia are large and significantly positive" [academic]
7. **Already tested?** JKS test straddles on SPX options up to 60 days; Song tests implied uncertainty, not P&L. Not found tested on SPXW 0DTE P&L in the sources read.
8. **Why it may fail.** Eight days a year is anecdote. Spreads widen sharply at 14:00. FOMC-day straddles priced "roughly double" and were "largely respected" (FlashAlpha).

### 5. The held-strike asymmetry is smile geometry (explanation test for oddity 2)

1. **Name.** Level shift plus smile slide.
2. **Mechanism (my inference, built from Bandi et al. and Almeida et al.).** A held strike's IV change has two parts. One is the shift of the whole smile when spot moves, the leverage effect, which is negative. The other is the slide of the strike along the smile as it moves away from the money. The 0DTE smile is U-shaped: leverage sets its slope and vol-of-vol its curvature (Bandi et al.), and Almeida et al. find a rich call side. The slide therefore adds IV when spot moves either way. On a fall, the shift and the slide both add, so IV rises. On a rise, the level falls and the slide adds, so the two roughly cancel and IV is flat. That is the desk's pattern.
3. **Prediction.** Measured at fixed standardised moneyness (log(K/F)/(σ√τ)), the slope of IV change on index change is close to symmetric. The held-strike asymmetry is predicted by the local smile curvature at the start of the window.
4. **Kill line.** ATM IV at fixed moneyness shows the same asymmetry as the held strike, about 3 points per 1% down and near 0 up. Then the asymmetry is in the level and is behavioural (Hibbert et al.), not geometry.
5. **Data needed.** Held.
6. **Evidence.**
   - Leverage sets the 0DTE ATM skew; vol-of-vol sets ATM convexity. https://westernfinance-portal.org/viewpaper?n=915376, 2023-26, "the latter impacts the at-the-money convexity of the implied volatility surface" [academic]
   - Intraday smiles follow neither sticky strike nor sticky delta. https://sage.cnpereading.com/doi/10.3233/AF-150048, 2015, "1.3 to 1.5 times stronger than the sticky strike rule predicts" [academic]
   - Return-implied vol relation strongly negative and asymmetric, intraday. https://faculty.fiu.edu/~dupoyetb/return_vola.pdf, 2008, "Neither the leverage hypothesis nor the volatility feedback hypothesis adequately explains" [academic]
7. **Already tested?** No 0DTE source splits held-strike from moneyness-level spot-vol slopes by sign. Not found tested on SPXW 0DTE in the sources read.
8. **Why it may fail.** This card is a measurement, not an edge. If it holds, the desk's skew-aware hedge should be built in moneyness coordinates. The 10% variance reduction already found may then be what is available.

### 6. Trend continuation needs low older-expiry gamma (needs open interest)

1. **Name.** Older expiries set whether a loud half-hour continues.
2. **Mechanism.** Adams et al. find the dampening comes from positions built in longer-dated options that roll into expiry. Pre-existing positions add 25 bp of hedging need, new same-day trades 3 bp. Ardia and Vaudescal find public-OI gamma of non-0DTE expiries predicts next-bar RV 36% lower; the 0DTE bucket tracks dealer inventory poorly. So the state that decides continuation is visible at 9:30 from yesterday's open interest.
3. **Prediction.** After a loud trending half-hour, the seller's next-window loss is larger on days in the bottom tercile of non-0DTE OI gamma than in the top tercile.
4. **Kill line.** No difference across terciles on both half-years.
5. **Data needed.** **Not held:** open interest by strike and expiry, daily. Available from Cboe DataShop, OptionMetrics, ThetaData or OCC series reports.
6. **Evidence.** Adams et al. (S5): "not from same-day 0DTE trading but from positions accumulated earlier", https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5641974, July 2026 [academic]. Ardia-Vaudescal (S18), https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7202999, July 2026, "nearly twice the published coefficient" [academic].
7. **Already tested?** Both test realised variance, not the seller's P&L after a trending window. Zarattini et al. test gamma imbalance against a breakout strategy on SPY. Not found tested on SPXW 0DTE in the sources read.
8. **Why it may fail.** The sign convention for OI gamma is a guess about who is long. FirmTape finds convention books carry nothing, and Singh finds the sign reversed in 2025.

### 7. Opening demand pressure from retail buyers (needs flow data)

1. **Name.** Retail buys the morning.
2. **Mechanism.** Retail is 50-60% of SPX 0DTE trading (Cboe). It buys single legs, mostly calls, holds about half an hour (Bogousslavsky-Muravyev), and enters early: 61.7% of retail trades come with 3 to 6.5 hours left (Beckmeyer et al.). Dealers who are net short after this flow quote the morning higher, which is demand pressure on option prices.
3. **Prediction.** The first half-hour's excess charge is larger on days with high retail opening-buy volume, and it sits in OTM calls more than puts. The call-side part is testable on held data: 9:35 IV of 10-25-delta calls minus its 10:30 value, with spot held constant, against the same for puts.
4. **Kill line.** The 9:35-to-10:30 fall in IV at fixed moneyness is equal for calls and puts, and it is unrelated to retail opening volume.
5. **Data needed.** Partly held (IV by strike). Retail flow is not held: Cboe Open-Close data by origin, or OPRA trade conditions SLAN and MLAT (paid).
6. **Evidence.** Cboe (S8), https://www.cboe.com/insights/posts/0-dt-es-decoded-positioning-trends-and-market-impact/, May 2025, "retail now makes up around 50-60% of SPX 0DTE trading" [exchange or regulator]. Beckmeyer et al. (S3), https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4404704, 2024, "end consumers buy more 0DTE options than they sell" [academic].
7. **Already tested?** Beckmeyer et al. measure retail losses by hour, not price pressure by time of day. Not found tested on SPXW 0DTE in the sources read.
8. **Why it may fail.** Cboe finds buys and sells "remarkably balanced". Mid-quote IV at 9:35 is noisy at wide spreads.

### 8. The closing-auction ten minutes

1. **Name.** 15:50 to 16:00 as a priced burst.
2. **Mechanism.** At 15:50 the exchanges publish closing imbalances, and the MOC entry deadline passes. Song finds 15:50 to 16:00 holds more jump variance than any other ten minutes, about 1.9 times the day's average, and that 0DTE prices it like an event. If, as with the statement, the premium is paid where uncertainty resolves, the seller should earn here.
3. **Prediction.** A straddle sold at 15:50 at the bid and held to settlement has a realised/charged ratio below 1 on both half-years.
4. **Kill line.** The ratio is at least 1, which matches the desk's finding that no half-hour but the first is rich.
5. **Data needed.** Held. The settlement value needs the official SPX close.
6. **Evidence.** Song (S24), https://afajof.org/management/viewp.php?n=260400, September 2026, "concentrates more discontinuous volatility than any other ten-minute interval" [academic]. Pearce (S32), weak: 15:55/15:58 condors, Option Omega logs [unknown].
7. **Already tested?** Song measures implied accumulation, not P&L, and drops quotes after 15:40. The only P&L source is a weak practitioner backtest. Not found tested on SPXW 0DTE in the sources read.
8. **Why it may fail.** Quotes after 15:50 are thin and the spread is a large part of a tiny premium. Song excludes the period for this reason.

### 9. Morning vol-of-vol and tomorrow's straddle (found once)

1. **Name.** A high-uncertainty morning makes tomorrow's options cheap.
2. **Mechanism.** Bevilacqua and Hizmeri find VVIX at 10:00 predicts next-day variance-asset returns, with t up to 5.6, gone after 11:00. They attribute it to limited attention and slow updating. Intraday, 10:00 to 16:00, the relation is flat. If longer variance prices underreact, the next day's 0DTE implied vol may be set too low after such mornings.
3. **Prediction.** When the 10:00 0DTE smile curvature (a vol-of-vol proxy, after Bandi et al.) is in its top quartile, the next day's whole-day 0DTE straddle has a realised/charged ratio above that of other days.
4. **Kill line.** No difference, or the opposite sign.
5. **Data needed.** Held for the proxy. VVIX intraday is not held (Cboe sells it).
6. **Evidence.** https://wp.lancs.ac.uk/fofi2026/files/2026/03/FoFI-2026-091-Mattia-Bevilacqua.pdf, 2026, "intraday returns display a flat relationship with morning VVIX" [academic].
7. **Already tested?** Found once, on VIX futures and variance swaps 2006 to 2022. Not found tested on SPXW 0DTE in the sources read.
8. **Why it may fail.** The curvature proxy may not track VVIX. One year gives about 60 top-quartile days.

## The desk's three oddities: what the literature says

| Oddity | What bears on it | Verdict |
|---|---|---|
| First half-hour (9:35-10:05) is the only window charged more than came | Muravyev-Ni predict the **opposite** for clock-priced options: the morning should be cheap. Almeida et al. and Song both skip it because spreads are widest. Tastylive (3 days) and Option Alpha say IV is high at the open and sellers enter about 10:15. Song and JKS show premia sit where scheduled uncertainty resolves. Londono-Samadi price ISM, marginally. Retail enters early (Beckmeyer). | No paper measures it. Two mechanisms are testable: 10:00 releases (card 1), opening burst (1b); a third needs flow data (card 7). |
| Held-strike IV rises about 3 points per 1% fall, flat on rises | Asymmetric return-implied vol: Hibbert et al. (2008, intraday VIX). Smiles move 1.3-1.5 times sticky strike (EuroStoxx/DAX). Bandi et al.: leverage sets skew, vol-of-vol sets convexity. Chong-Todorov give an estimator of the leverage effect from short options. | Known in shape, not measured on 0DTE strikes. Card 5 tests whether it is geometry or level. |
| Skipping after a loud trending half-hour cut the worst day but not the mean | Gao et al.: continuation stronger on volatile days (pre-2014). FirmTape: no unconditional continuation 2022-26, only on dealer-short days. Dim-Eraker-Vilkov and Adams et al.: momentum when gamma or hedging needs are low. Vol clusters (Amaya et al. GARCH). | Consistent with a tail that clusters after trends and a mean that does not. Cards 2 and 6 test which trends. |

## Known and taken

One line each. These have been tested on same-day or very short index options; do not propose them as new.

**Volatility premium, within the day and overnight**
- 0DTE VRP is positive, significant, tiny: median about 0.0011% of spot from 10:00; ES 1% 0.58-1.58%. Vilkov, SPXW 09/2016-01/2026. [link](https://github.com/vilkovgr/0dte-strategies/blob/main/docs/paper/paper-annotated.md)
- Annualised 0DTE VRP 1.54-2.95% against 0.55% for 1DTE; upside VRP larger than downside for 0DTE only; VRP negatively predicts the intraday return. Almeida-Freire-Hizmeri, 2012-03/2025. [link](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4701401)
- Stochastic-dominance violations profitable to 2022, then stagnant. Same paper.
- Annualised VRP to expiry rises through the day, sharply in the last bars; about 0.01% a day. Dim-Eraker-Vilkov, 2012-06/2023. [link](https://westernfinance-portal.org/viewpaper?n=950096)
- No local arbitrage in small moves; premium sits in large jumps; after costs, not mispriced. Chong-Todorov, 2020-2024. [link](https://economics.smu.edu.sg/sites/economics.smu.edu.sg/files/economics/pdf/Seminar/2024/20241212.pdf)
- Delta-hedged SPX option returns -1.0% overnight, +0.3% intraday; options priced as if day and night vol per hour were equal. Muravyev-Ni, 2004-2013. [link](https://www.sciencedirect.com/science/article/abs/pii/S0304405X19302193)
- 10:00 SPY straddle about 13% rich (0.589 vs 0.674); close inside band 71%. FlashAlpha [seller], Wednesdays 07/2022-04/2026. [link](https://flashalpha.com/articles/are-0dte-straddles-overpriced-193-spy-sessions-data-study)
- VIX1D rises by day and falls by night by construction. Albers-Kestner 2024. [link](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4650419)
- One-day VRP in Europe 2.5 and 3.4 points; seller's bid halves it. Wilkens 2026. [link](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7283819)
- Higher 0DTE share lowers 1-day VRP payoff. Khalil (thesis), 2011-2022. [link](https://research-api.cbs.dk/ws/portalfiles/portal/105671291/1775874_O._Khalil_Zero_Day_to_Expiry_Options_Trading_and_Variance_Risk_Premium.pdf)

**Time of day**
- Analyses start at 10:00 because the relative spread is lowest from 10:00 to 14:00 and highest at open and close. Almeida et al.; Song uses 10:00-15:40.
- 15:50-16:00 holds the most jump variance of any ten minutes (1.9 times average); 0DTE prices it by accumulation. Song 2026. [link](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7412318)
- Morning VVIX predicts next-day variance returns; flat intraday. Bevilacqua-Hizmeri, 2006-2022. [link](https://wp.lancs.ac.uk/fofi2026/files/2026/03/FoFI-2026-091-Mattia-Bevilacqua.pdf)
- ATM 0DTE IV falls through the day; widest range in first 15-30 min. Tastylive [seller], three days only. [link](https://www.youtube.com/watch?v=JSfxso7awzc)
- Monday best, Tuesday/Thursday/Friday negative for platform users; profitable users enter about 10:15, exit about 12:00. Option Alpha [seller]. [link](https://optionalpha.com/blog/0dte-options-strategy-performance)

**Event days**
- FOMC event vol 0.88% on average, predictive, carries VRP; no return premium pre-FOMC. Johannes-Kaeck-Seeger. [link](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4484011)
- FOMC 0DTE implied uncertainty builds 10:00 to 14:00; forecasts post-announcement RV (R² 78-85%); pre-FOMC drift ended March 2016. Song. [link](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7412318)
- Event VRP the night before: S&P FOMC 0.248, payrolls 0.204. Wright, NBER 2020 / JTSA 2025. [link](https://www.nber.org/papers/w28306)
- Expirations spanning CPI/FOMC/NFP/GDP 2.5-7.5% dearer in IV; FOMC VRP 44% larger. Londono-Samadi, Fed 2023. [link](https://www.federalreserve.gov/econres/ifdp/the-price-of-macroeconomic-uncertainty-evidence-from-daily-options.htm)
- FOMC 0DTE hedged returns negative before, positive around, not significant (68 days). Almeida et al. footnote 28.
- FOMC/CPI days triple the loss per SPY condor; skipping them does not make it pay. OptionKrafter [seller]. [link](https://optionkrafter.com/blog/0dte-iron-condor)

**Dealer gamma and the index**
- MM 0DTE gamma positive on average; one SD more lowers next log variance 7.3% of SD; momentum 10 bp/hour more in low gamma. Dim-Eraker-Vilkov, 2021-06/2023. [link](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4692190)
- 10-minute vol 61 bp lower on 0DTE days; dampening from older positions (25 bp) not same-day trades (3 bp); gamma strengthens order-flow reversal about 30 min. Adams et al., 2018-2024. [link](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5641974)
- Maximum gamma impact +3.3 points daily vol, +6.4 on 30-minute vol; median lowers vol. Amaya-Garcia-Ares-Pearson-Vasquez, 07/2020-06/2023. [link](https://cdn.cboe.com/resources/education/research_publications/gammasqueezes.pdf)
- MM net gamma 0.04-0.17% of futures liquidity; flow balanced. Cboe 2023. [link](https://www.cboe.com/insights/posts/volatility-insights-evaluating-the-market-impact-of-spx-0-dte-options/) At most 0.2%, 2025. [link](https://www.cboe.com/insights/posts/0-dt-es-decoded-positioning-trends-and-market-impact/)
- One SD more 0DTE volume raises vol 9.10% of mean. Brogaard-Han-Won. [link](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4426358)
- Public-OI non-0DTE gamma predicts next half-hour RV 36% lower. Ardia-Vaudescal 2026. [link](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7202999)
- Flow-gamma sign for 5-30 min variance reverses in 2025; maximum-gamma strike does not attract the index. Singh 2026. [link](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7350465)
- 0DTE did not cause the low VIX of 2023; structured-product hedging may have. BIS 2024. [link](https://www.bis.org/publ/qtrpdf/r_qt2403x.htm)

**Momentum and reversal within the day**
- First half-hour predicts last half-hour, R² 1.6%, 1993-2013. Gao et al. [link](https://www.sciencedirect.com/science/article/abs/pii/S0304405X18301351)
- Rest-of-day predicts last 30 minutes in 60+ futures, tied to short-gamma hedging, 1974-2020. Baltussen et al. [link](https://pure.eur.nl/en/publications/hedging-demand-and-market-intraday-momentum/)
- No unconditional slope 2022-2026 (t 0.6); continuation only on dealer-short days. FirmTape [seller]. [link](https://firmtape.com/research/is-intraday-momentum-still-alive)
- Breakout with trailing stops on SPY, Sharpe 1.33 net, 2007-2024. Zarattini-Aziz-Barbon. [link](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4824172)
- Hour-to-hour momentum positive when hedging needs low, negative when high. Adams et al.

**The smile and the wings**
- Edgeworth model prices 80% of 0DTEs within the spread; volatility jumps hardly matter. Bandi-Fusari-Renò. [link](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4503344)
- ATM term structure oscillates across 0-7 day tenors. Bandi-Fusari-Gazzani-Renò 2026. [link](https://arxiv.org/abs/2603.29430)
- Short OTM wins up to 75% of days; means not distinguishable from zero; put ratio spread best (net Sharpe 0.93 out of sample); risk reversal only structure with positive mean, median and 25th percentile. Vilkov.
- Pricing kernel U-shaped for 0DTE; only 6% of ATM 0DTEs meet dominance bounds. Almeida et al.

**Practitioner structures, and who verified them**
- Iron condors/flies: unconditional net Sharpe -0.96 (Vilkov, independent, academic); logistic rule -0.20 out of sample.
- SPY 16-delta condor at 10:00 with 50% target and 2x stop loses at real fills (-$655, 602 trades), wins at mid. OptionKrafter [seller]; not independently verified.
- 3,909 Option Alpha user backtests: 99.9% "profitable", heavily overfit. Kam 2026 (summary of a seller's platform). [link](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7055179)
- MEIC (multiple-entry condor) and variants: entry filters "not sufficiently predictive"; drawdown cut by tighter second stop; backtest only. Theta Profits [seller]. [link](https://www.thetaprofits.com/inside-a-0dte-iron-condor-strategy-built-for-smaller-drawdowns/)
- Late-day condors (15:55/15:58): stops near the close are arbitrary. Pearce [unknown], Option Omega logs.
- Credit-spread gate on QQQ condors adds one standard error after 820 trials. Zonted [unknown]. [link](https://zonted.com/posts/nothing-looked-wrong/)
- Opening-range entries: only seller guides (Volatility Box) and Zarattini's SPY breakout (stock, not options). No independent 0DTE options backtest found.
- **No independent source verified any practitioner's profitable condor, fly or credit-spread result after costs.** The only independent results (Vilkov) are negative for condors and flies.

**Retail trading and its losses**
- Retail lost $241,000 a day (2021-2023), $350,000 after May 2022; 70% is transaction cost; loses on buys, gains on sells. Beckmeyer-Branger-Gayda. [link](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4404704)
- Retail prefers weeklies, 12.6% quoted spread; lost $2.1 billion 2019-2021. Bryzgalova-Pavlova-Sikorskaya. [link](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4065019)
- Trader-level: average option trade -0.9%, 0DTE -4.6%; naked sales +20%. Bogousslavsky-Muravyev 2024. [link](https://www.lsu.edu/business/files/event-files/2025-finance-mardi-gras/retail_option_trading_v2.pdf)
- Over 95% of 0DTE trades capped-risk; 4% naked short; retail 50-60%. Cboe 2025.
- 0DTE holding returns -32,000% annualised; leverage above 400. BIS 2024.

### Disagreements a test on one-minute quotes could settle

| Question | Side A | Side B | Settled by |
|---|---|---|---|
| Who is short 0DTE gamma? | Beckmeyer et al.: MMs net short | Cboe, Dim et al., Amaya et al.: mostly long | Needs trade-capacity data; not settleable on quotes |
| Does 0DTE raise volatility? | Brogaard et al.: yes, +9.1% | Adams et al.: -61 bp on 0DTE days | Not on quotes alone |
| Which wing holds the premium? | Almeida et al.: upside | Vilkov: downside (put ratio spreads) | Card 3, held data |
| Where does FOMC uncertainty resolve? | Song: statement, builds before | JKS: press conference, no build | Card 4, held data (few days) |
| How much do retail lose? | Beckmeyer, Bryzgalova: large, 3-9%/trade | Bogousslavsky-Muravyev: -0.9%/trade | Not on quotes |
| Does intraday momentum survive? | Gao, Baltussen: yes (to 2013/2020) | FirmTape: flat 2022-26 | Index only; desk can rerun on its forward |

## Ten sources worth reading in full

| Link | Author | Date | Why |
|---|---|---|---|
| [0DTE Trading Rules](https://github.com/vilkovgr/0dte-strategies/blob/main/docs/paper/paper-annotated.md) | Vilkov | Jan 2026 | The benchmark for every same-day structure, with code |
| [0DTE Asset Pricing](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4701401) | Almeida, Freire, Hizmeri | Jun 2025 | Upside premium, the wing question (card 3) |
| [Pre-FOMC Uncertainty Accumulation](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7412318) | Song | Aug 2026 | Only paper on how 0DTE prices known burst times, including the close |
| [Do S&P 500 Options Increase Market Volatility?](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5641974) | Adams, Dim, Eraker, Fontaine, Ornthanalai, Vilkov | Jul 2026 | Where dampening comes from; momentum vs hedging need |
| [Do Equity and Options Markets Agree about Volatility?](https://economics.smu.edu.sg/sites/economics.smu.edu.sg/files/economics/pdf/Seminar/2024/20241212.pdf) | Chong, Todorov | 2024 | Why the median window is rich and the sum is fair |
| [Why do option returns change sign from day to night?](https://www.sciencedirect.com/science/article/abs/pii/S0304405X19302193) | Muravyev, Ni | 2020 | The clock-time mechanism the first-half-hour oddity contradicts |
| [The Price of Macroeconomic Uncertainty](https://www.federalreserve.gov/econres/ifdp/the-price-of-macroeconomic-uncertainty-evidence-from-daily-options.htm) | Londono, Samadi | Jun 2023 | Release premia, including ISM (card 1) |
| [0DTE Option Pricing](https://westernfinance-portal.org/viewpaper?n=915376) | Bandi, Fusari, Renò | 2023-26 | Smile shape: leverage and vol-of-vol (card 5) |
| [0DTE Index Options and Market Volatility](https://cdn.cboe.com/resources/education/research_publications/gammasqueezes.pdf) | Amaya, Garcia-Ares, Pearson, Vasquez | Jan 2025 | Minute-level MM gamma from every trade; sizes the worst case |
| [Retail Traders Love 0DTE Options](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4404704) | Beckmeyer, Branger, Gayda | Jul 2024 | Who trades when, and who loses (card 7) |

## Could not open

- Song, AFA PDF, via WebFetch: returned binary. Read in full through Exa instead.
- Fed IFDP 1376 PDF, via WebFetch: returned binary. Read through the whenthefedspeaks mirror.
- Local PDF text extraction (Python) was blocked by the permission settings, so no PDF was parsed on disk.
- Brogaard-Han-Won full PDF, Adams-Fontaine-Ornthanalai (4881008) full PDF, Johannes-Kaeck-Seeger full PDF, Ardia-Vaudescal, Singh, Wilkens, Kam: abstract pages only (SSRN). Numbers above come from abstracts or, for JKS, the discussant's slides.
- Albers (2025) on VIX1D forecasting, Alexiou-Bevilacqua-Hizmeri (2026): seen only in FirmTape's list; not opened; nothing cited from them.

## Appendix: source notes as read

Each entry was written as the source was read: data, dates, findings, what the authors leave open, contradictions.

### S1. Vilkov, "0DTE Trading Rules" (SSRN 4641356; annotated paper on GitHub, data to January 2026) [academic]
- Link: https://github.com/vilkovgr/0dte-strategies/blob/main/docs/paper/paper-annotated.md
- Data: Cboe 30-minute SPXW bars with NBBO quotes, ThetaData 1-minute bars; September 2016 to January 2026; moneyness 0.98 to 1.02; entries 16:00 the day before, 10:00 (main), 13:00, 15:00; held to 16:00, no intraday hedging.
- Found: VRP positive and significant but tiny, "median realized VRP from 10:00 ET to expiration is approximately 0.0011% of underlying". Short slightly OTM options win in up to 75% of days; means not distinguishable from zero. Risk reversal the only structure with positive mean, median and 25th percentile (about 0.01% of spot). Iron fly/condor interquartile range "roughly symmetric around zero". Realised variance explains at most about 4.5% of P&L; realised skewness explains more. Post-May-2022 breaks "economically non-trivial" but statistically weak. Costs: half-spread + 0.5 bp. Out-of-sample logistic rules (April 2019 to January 2026, 252-day rolling): put ratio spread net Sharpe 0.93, straddle/strangle 0.39, iron fly/condor -0.20; ES 1% 0.58 to 1.58% of the index.
- Left open: no intraday hedging, no dynamic rebalancing, no causal market-impact design; "extend event conditioning"; signals restricted to 10:00 information. Later entries (15:00) load more on realised skewness.

### S2. Almeida, Freire, Hizmeri, "0DTE Asset Pricing" (SSRN 4701401, draft 20 June 2025) [academic] — full PDF read
- Link: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4701401
- Data: Cboe 1-minute SPX option quotes, volume, open interest, 6 January 2012 to 18 March 2025, 1,815 0DTE dates (about 40% after 11 May 2022). Entry times 10:00 to 14:00 every half-hour, held to close. The window 10:00 to 14:00 was chosen because "the relative option bid-ask spread is reasonably stable at its minimum" there; spread is highest at open and close.
- Found: ATM delta-hedged calls and straddles lose significantly (VRP positive). Annualised 0DTE VRP 1.54% to 2.95% against 0.55% for 1DTE and 0.81% for 22DTE. Upside ("good") VRP larger than downside VRP for 0DTE only; reverses from 5DTE on. VRP negatively predicts intraday index return, driven by the upside part. Pricing kernel U-shaped (high for positive returns). Only about 30% of 0DTEs (6% of ATM) satisfy stochastic-dominance bounds; a delta-hedged ATM trade on bound violations had Sharpe 0.1 to 0.2 per trade after costs up to 2022, then "mostly stagnates". VRP "almost always positive" before 2022; "afterwards negative values become more frequent". Mispricing stronger when 0DTE volume, realised variance and Google-trends attention are low. Futures-based realised variance is larger than cash-index realised variance, so VRP shrinks (to 2.25%) with E-mini returns.
- Left open: FOMC days (68) too few to conclude; footnote 28: before the announcement hedged returns mostly negative, around it positive, "not statistically significant due to the small sample". Times before 10:00 and after 14:00 not studied (spreads).

### S3. Beckmeyer, Branger, Gayda, "Retail Traders Love 0DTE Options... But Should They?" (SSRN 4404704, version 27 July 2024) [academic] — full PDF read
- Link: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4404704
- Data: Cboe intraday trades with the Automated Price Improvement Mechanism flag to identify retail, February 2021 to September 2023; Cboe Open/Close data by participant.
- Found: over 75% of retail S&P 500 option trades are 0DTE; retail share of 0DTE volume above 6%. Retail lost $241,000 a day on average, $350,000 a day after 16 May 2022; more than $125 million in total; about 70% of losses are transaction costs. Retail loses on buys and makes money on sells; single-leg is 60 to 80% of volume since mid-2022. Losses negative in every hour (table by hour, 9:30 to 15:00). End users buy more 0DTE than they sell, "which in turn leaves the option market maker with a net-short position", grown since May 2022. 61.7% of retail and 57.5% of non-retail trades are entered with 3 to 6.5 hours left (first half of the day). Retail profits rise on high-range days; realised variance, realised skewness and FOMC days show no relation to aggregate retail profit. Buying higher-IV contracts gives lower returns.
- Left open / contradicts: their net-short market-maker finding conflicts with Cboe's "balanced" flow (S6) and with the net-long-gamma dealer finding of Adams et al. (see below).

### S4. Dim, Eraker, Vilkov, "0DTEs: Trading, Gamma Risk and Volatility Propagation" (SSRN 4692190, version 6 June 2025) [academic] — full PDF read
- Link: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4692190
- Data: Cboe Open/Close by trader type for net gamma, January 2021 to 14 June 2023; SPX/SPXW intraday 01/2012 to 30/04/2024 for volume tests.
- Found: market-maker 0DTE net gamma "on average positive"; about one-third of observations negative, with magnitude about three times smaller. "The major option sellers are non-professional customers." Market-maker gamma falls monotonically towards expiry; customers' stays roughly constant. One SD more market-maker gamma lowers next log variance by 7.3% of its SD. Intraday momentum strategy earns 10 bp per hour more in low-gamma than high-gamma states. Projected hedge flows "routinely exceeding 5% of the intraday volume". Volume jumps do not change the return distribution; after volume jumps positive returns shrink, negative unaffected. Flow correlation between 0DTE and underlying rose from 0.25-0.30 before 2021 to 0.58 in 2023-24. Cites Vasquez, Amaya, Pearson, Garcia-Ares (2025): maximum gamma impact about 3.3 vol points a year on daily vol, 6.4 on 30-minute vol.
- Left open: "we do not extrapolate to a scenario where the market makers' inventories become very negative"; margin and mark-to-market rules "beyond the scope". Contradicts S3 (market makers net short).

### S5. Adams, Dim, Eraker, Fontaine, Ornthanalai, Vilkov, "Do S&P 500 Options Increase Market Volatility? Evidence from 0DTEs" (SSRN 5641974, draft 15 July 2026) [academic; one author at the Bank of Canada] — full PDF read
- Link: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5641974
- Data: SPX/SPXW options, E-mini futures order flow; baseline 1 January 2018 to 19 May 2022 (Tuesday/Thursday 0DTE presence from holidays and end-of-month/quarter as the natural experiment), extended to December 2024.
- Found: on 0DTE expiry days the 10-minute realised vol of the index is 61 annualised bp lower (about 7% of the 9.10% mean). The weekday difference vanishes once 0DTEs expire daily. 0DTE presence raises market-maker hedging needs by 0.15 percentage points of S&P 500 shares; multiplier about 4 (1 bp more counter-trend hedging, 4 bp less vol). **The shift comes "not from same-day 0DTE trading but from positions accumulated earlier in longer-dated options"**: pre-existing positions add 25 bp, new same-day positions 3 bp. One SD of 10-minute net gamma lowers next 10-minute vol by about 23 bp; effect lasts about an hour. Net gamma strengthens E-mini order-flow reversal for about 30 minutes. Hour-to-hour momentum is positive when hedging needs are low and negative (reversal) when high.
- Left open: "dynamic management of hedging needs over multiple days"; "variation in hedging needs may introduce a distinct source of aggregate risk with further asset pricing implications for the stock and option markets" — i.e. whether option prices reflect the dampening is not tested. Other markets "for future research". Disagrees with Brogaard, Han, Won (S7).

### S6. Amaya, Garcia-Ares, Pearson, Vasquez, "0DTE Index Options and Market Volatility: How Large is Their Impact?" (25 January 2025, hosted by Cboe) [academic] — intro, data and model sections read
- Link: https://cdn.cboe.com/resources/education/research_publications/gammasqueezes.pdf
- Data: every Cboe SPX/SPXW trade record with trader capacity (442.6 million records), January 2020 to June 2023; Algoseek one-minute BBO; market-maker (OMM) net position cumulated from series inception, gamma each minute; GARCH-MIDAS on one-minute E-mini returns.
- Found: OMM gamma "typically positive, is often negative"; mean of daily means 408.8 before May 2022, 234.2 after; after May 2022 gamma is negative at some point on at least half of days. Median effect lowers daily vol by 0.08 points; maximum raises daily vol by 3.3 points and 30-minute vol by 6.4 points, "not unusual" against all-cause changes. 0DTE volume: customer-buys-from-MM 14.95%, customer-sells-to-MM 14.06% of all SPX volume (near balance). The 9:30 gamma includes overnight trades.
- Left open: only the maximum impact is studied; the timing within the day of negative-gamma episodes is not related to option prices.

### S7. Cboe (Mandy Xu), "Volatility Insights: Much Ado About 0DTEs" (8 September 2023) [exchange or regulator]
- Link: https://www.cboe.com/insights/posts/volatility-insights-evaluating-the-market-impact-of-spx-0-dte-options/
- Found: MM net 0DTE gamma $170mm to $670mm through the day, 0.04% to 0.17% of S&P futures daily liquidity; median at 15:30 +$173mm, interquartile -$1.1bn to +$2.4bn. Close-to-close vs intraday realised vol spread 2.7 points YTD, equal to the 10-year average. No rise in 2-sigma one-minute gap moves, including the last hour. 15 August 2023: MMs long about $2bn gamma at 15:00 when the index fell.
- Contradicts: Brogaard, Han, Won (S9) and Beckmeyer et al. (S3, MMs net short).

### S8. Cboe (Mandy Xu), "0DTEs Decoded: Positioning, Trends, and Market Impact" (2 May 2025) [exchange or regulator]
- Link: https://www.cboe.com/insights/posts/0-dt-es-decoded-positioning-trends-and-market-impact/
- Found: SPX 0DTE almost 2 million contracts a day; retail 50-60% of 0DTE trading, fell from 57% to 47% in early April 2025 and returned to 60%; over 95% of 0DTE trades are capped-risk; "Only 4% of SPX 0DTE trading is in naked short options." Net MM gamma hedging "at best, just 0.2% of the SPX daily liquidity".

### S9. Brogaard, Han, Won, "Does 0DTE Options Trading Increase Volatility?" (SSRN 4426358, written 22 April 2023, revised 21 January 2026) [academic] — abstract page read
- Link: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4426358
- Found: staggered introduction of index weeklies as instrument; one SD more 0DTE trading raises volatility by 9.10% of its mean; positive even after controlling for MM gamma, "primarily driven by speculative retail investors". Earlier version: +24.5%.
- Contradicts: Adams et al. (S5, lower vol on 0DTE days), Dim-Eraker-Vilkov (S4), Cboe (S7).

### S10. BIS Quarterly Review box, "What could explain the recent drop in VIX?" (4 March 2024) [exchange or regulator]
- Link: https://www.bis.org/publ/qtrpdf/r_qt2403x.htm
- Found: 0DTE leverage above 400; holding 0DTEs averages -32,000% annualised, maximum +79,000%; 0DTE growth did not draw activity away from one-month options. Alternative: dealers hedging yield-enhancing structured products dampen volatility.

### S11. ECB Financial Stability Review box, "The risks from hidden leverage in short-term equity options" (22 November 2023) [exchange or regulator]
- Link: https://www.ecb.europa.eu/press/financial-stability-publications/fsr/focus/2023/html/ecb.fsrbox202311_02~0cf2c71d00.it.html
- Found: argument, not a test: short 0DTE sellers hedging with the trend could amplify intraday spirals; impact depends on one-sided positioning, "skewed to the downside (upside)" when puts (calls) dominate. Eurex added daily EURO STOXX 50 weeklies on 28 August 2023.

### S12. Federal Reserve, Senior Credit Officer Opinion Survey, special questions on 0DTE (September 2023) [exchange or regulator]
- Link: https://www.federalreserve.gov/data/scoos/files/scoos_202309.pdf
- Found: dealers say 0DTE clients are a small fraction; three-fifths collect margin intraday only when volatility is elevated; two-fifths collect none; "the great majority" could not judge clients' appetite for downside risk on days with elevated early-session volatility. No price result.

### S13. Hibbert, Daigler, Dupoyet, "A behavioral explanation for the negative asymmetric return-volatility relation" (Journal of Banking & Finance 32, 2008) [academic] — introduction and sections 1-2 read
- Link: https://faculty.fiu.edu/~dupoyetb/return_vola.pdf
- Data: S&P 500 and Nasdaq 100 with VIX and VXN, daily and intraday (30-minute and 5-minute).
- Found: strong negative and asymmetric return-implied-volatility relation at daily and intraday frequency; neither leverage nor volatility feedback explains it; consistent with representativeness, affect and extrapolation; the asymmetry is concentrated in extreme return quintiles and relates to the slope of the skew.
- Bears on oddity 2 (implied vol rises on falls, flat on rises). Old and on 30-day options, not 0DTE.

### S14. "Smile in motion: An intraday analysis of asymmetric implied volatility" (Algorithmic Finance, 13 April 2015) [academic] — abstract read
- Link: https://sage.cnpereading.com/doi/10.3233/AF-150048
- Data: EuroStoxx 50 options 2000-2011, DAX options 1995-2011, 14 million transactions.
- Found: intraday smile moves fit neither sticky strike nor sticky delta; "1.3 to 1.5 times stronger than the sticky strike rule predicts"; the main driver of the adjustment factor is the index return itself.

### S15. Bandi, Fusari, Renò, "0DTE Option Pricing" (SSRN 4503344, 7 July 2023, revised 22 September 2026; Journal of Finance forthcoming) [academic] — abstract and sections 1-6 (Western Finance version) read
- Link: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4503344 ; https://westernfinance-portal.org/viewpaper?n=915376
- Found: Edgeworth-like small-time expansion; leverage (spot-vol covariance) sets the ATM skew and vol-of-vol sets ATM convexity; prices within the bid-ask for 80% of options; IV RMSE 0.48 against 1.17 for Black-Scholes; volatility jumps "hardly affect the price of 0DTEs". Ends with "suggestive evidence of nearly instantaneous predictability" from structurally estimated return and variance premia.
- Left open: the predictability result is called suggestive, not tested as a trading rule.

### S16. Chong and Todorov, "Do Equity and Options Markets Agree about Volatility?" (SMU seminar version, December 2024; summarised by HKUST 18 April 2026 as "Are 0DTE Options Mispriced?") [academic] — abstract and introduction read
- Link: https://economics.smu.edu.sg/sites/economics.smu.edu.sg/files/economics/pdf/Seminar/2024/20241212.pdf ; https://bm.hkust.edu.hk/bizinsight/2026/04/are-0dte-options-mispriced
- Data: 0DTE SPX options 2020-2024.
- Found: no risk premium should attach to small frequent moves (truncated volatility); option-implied truncated vol agrees with return-based truncated vol; "no evidence of such local arbitrage". Risk premia are large but sit in big jumps; transaction costs and estimation risk make the arbitrage Sharpe insignificant. "Expensive but do not appear to be mispriced."
- Bears on: the desk's median-window 0.6 vs pooled 1.0 result (premium paid for the tail, not the typical window).

### S17. Adams, Fontaine, Ornthanalai, "The Market for 0DTE: The Role of Liquidity Providers in Volatility Attenuation" (SSRN 4881008, May 2024, revised 20 June 2025; Bank of Canada) [academic] — abstract read
- Link: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4881008
- Found: index vol 60-90 annualised bp lower on 0DTE days, 2019-2023; market makers match most 0DTE flow but absorb end-user trades in long-dated options that become 0DTE positions. Predecessor of S5.

### S18. Ardia and Vaudescal, "The Intraday Gamma-Variance Channel with Public Options Data" (SSRN 7202999, 29 July 2026) [academic] — abstract read
- Link: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7202999
- Found: five years of half-hour SPX bars; one SD of non-0DTE net gamma from public open interest predicts next-bar realised variance about 36% lower, "nearly twice the published coefficient"; the 0DTE bucket correlates only 0.53 with a dealer-inventory benchmark. Reproduces on SPY and QQQ.
- Consequence: OI-based gamma from the older expiries, not 0DTE flow, carries the signal. Needs open interest (not held).

### S19. Singh, "Inherited State, New Flow, and Intraday Volatility in SPX 0DTE Options" (SSRN 7350465, 25 August 2026; independent student) [academic, weak] — abstract read
- Link: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7350465
- Found: 735 days, January 2023 to December 2025, one-minute; quote-classified flow gamma negative for next 5-30 min variance, but "improves in 2024 and reverses in 2025"; non-0DTE evidence rules out a 0DTE-only mechanism; "Broad MVC attraction is not supported" (the maximum-gamma strike does not pull the index).

### S20. Wilkens, "One-Day Volatility Indices and the Variance Risk Premium in European Equity Markets" (SSRN 7283819, 14 August 2026) [academic] — abstract read
- Link: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7283819
- Found: Eurex one-minute order books; one-day implied minus realised vol 2.5 (EURO STOXX 50) and 3.4 (DAX) points; valuing at the seller's bid cuts it by 48% and 34%. One-day index changes correlate only 0.56 with 30-day; that variation adds about 25 points of R² to a next-day variance forecast.

### S21. Kam, "The Efficacy of 0DTE Options Strategies: An Empirical Study of 3,909 Option Alpha Backtests" (SSRN 7055179, 4 July 2026; Circunfluencia Investimento) [academic, weak; data is a seller's platform] — abstract read
- Link: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7055179
- Found: 90.6% SPX; 78.7% iron condors, iron flies or credit spreads; median win rate 53.7%, median profit factor 1.98, 99.9% profitable; heavy right skew, small samples, "materially overstates realistic forward expectations". Not an independent backtest: it summarises user backtests on a seller's tool.

### S22. Khalil, "Zero-Day-to-Expiry Options Trading and Variance Risk Premium" (Copenhagen Business School master's thesis) [academic, weak]
- Link: https://research-api.cbs.dk/ws/portalfiles/portal/105671291/1775874_O._Khalil_Zero_Day_to_Expiry_Options_Trading_and_Variance_Risk_Premium.pdf
- Found: 2011-2022, about 900 dates, 1-day synthetic variance swaps against 5-minute futures RV; one point more 0DTE share of volume lowers 1-day VRP payoff by 0.0735 points (IV-2SLS).

### S4 addendum. Dim, Eraker, Vilkov, Western Finance version, Figure 4
- Annualised VRP to expiry, by 30-minute bar, 01/2012 to 14/06/2023: "clearly increasing during the day, and sharply so in the last several bars". In daily terms the 0DTE VRP is "only about 0.01%".

### S23. Muravyev and Ni, "Why do option returns change sign from day to night?" (JFE 136, 2020; SSRN 2820264) [academic] — journal page with introduction read
- Link: https://www.sciencedirect.com/science/article/abs/pii/S0304405X19302193
- Data: SPX and equity options, 2004-2013.
- Found: delta-hedged SPX returns -0.7%/day: -1.0% close to open, +0.3% open to close, "non-negative in all intraday subperiods". Best explanation: options priced as if day and night per-hour vol were equal; day/night per-hour ratio fell from 3 (2004) to 2 (2013). Equity-option returns follow the U-shape (more positive morning and afternoon); morning-to-midday and afternoon-to-midday vol ratios explain them across stocks.
- Left open: "the lack of statistical power prevents us" from running the intraday-seasonality test on SPX index options. Pre-0DTE; multi-day options.

### S24. Song, "Pre-FOMC Uncertainty Accumulation: Evidence from 0DTE Options" (SSRN 7412318, 23 August 2026; AFA version 15 September 2026; HEC Montréal PhD) [academic] — full text read
- Link: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7412318 ; https://afajof.org/management/viewp.php?n=260400
- Data: SPX 0DTE options restricted to 10:00-15:40 "to limit microstructure noise from the thin quoting near the open and close"; ES futures 9:30-16:00 for realised vol; 2012/2016-2023.
- Found: FOMC event uncertainty rises from 0.60% at 10:00 to 0.78% before 14:00 (30% in four hours), collapses to 0.34% at the statement, rebuilds to 0.42% before the 14:30 press conference, decays to 0.22%. Rate-change days run 0.83% to 1.08%. Level and build forecast post-announcement RV (R² 78-85%) but not pre-announcement RV. Implied skewness uniformly negative and not predictive. Pre-FOMC drift vanished from March 2016, the first meeting after Wednesday SPX expiries. **Same accumulate-and-release pricing around the closing auction**: 15:50-16:00 holds "more discontinuous volatility than any other ten-minute interval", about 1.9 times the within-day average.
- Contradicts: Johannes, Kaeck, Seeger (2026), who find no pre-announcement trend and put most event variance at the press conference; their straddle returns are significantly negative over the statement and indistinguishable from zero over the press conference.
- Left open: the open (9:30-10:00) is excluded; straddle returns on non-FOMC focal times are not computed.

### S25. Wright, "Event-day Options" (NBER w28306, December 2020; Journal of Time Series Analysis 46(6), 2025) [academic] — working paper read
- Link: https://www.nber.org/system/files/working_papers/w28306/w28306.pdf
- Data: Wednesday and Friday weekly options on Treasury and S&P 500 futures, implied vol the night before.
- Found: S&P 500 event VRP 0.248 (FOMC, significant at 1%) and 0.204 (employment report, 5%); press-conference meetings raise S&P implied variance (0.328, 10%) while the meeting dummy alone is -0.062 (insignificant). About half of the FOMC rise in Treasury implied variance is premium.

### S26. Johannes, Kaeck, Seeger, "FOMC Event Risk" (SSRN 4484011, revised 3 July 2026; Journal of Finance forthcoming) [academic] — abstract and discussant slides (Leyla Han, 2024) read
- Link: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4484011 ; https://www.leylahan.com/uploads/1/2/7/3/127380698/2024cdi2.pdf
- Found: ex-ante FOMC event vol averages 0.88%, predicts realised event vol, carries a significant VRP; ATM straddle returns fall 4-5% around the announcement; no expected-return premium pre-FOMC or across it; pre-FOMC drift tied to VIX. Disagrees with Song (S24) on whether uncertainty builds before 14:00.

### S27. Albers and Kestner, "The daily rise and fall of the VIX1D: causes and solutions of its overnight bias" (Finance Research Letters 62, 2024; SSRN 4650419) [academic] — abstract read
- Link: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4650419
- Found: VIX1D rises through the session and falls overnight because of business-time calculation and weighting of next-term options that carry overnight premium; "more pronounced than the day-of-the-week effect". Consequence: VIX1D is not a clean measure of the same-day variance charged; the desk's own per-window measure avoids this.

### S28. Muravyev and Ni, "Option Returns Night and Day" (2015 working version, McGill) [academic] — sections 1-3 read
- Link: https://www.mcgill.ca/desautels/files/desautels/muravyevninov2015.pdf
- Extra to S23: intraday gains "particularly in the afternoon"; intraday index skewness "changes its sign from negative to positive during a trading day"; "VIX is mechanically higher at the open and lower at the close because it is computed based on calendar instead of business time". Earlier explanation offered: traders fail to update time to expiry within the day.

### S29. OptionKrafter, "The 0DTE iron condor: a 75% win rate that still loses money" (undated, data April 2023 to December 2025) [seller: backtesting app]
- Link: https://optionkrafter.com/blog/0dte-iron-condor
- Found: SPY 0DTE condor, 16-delta shorts, $5 wings, 10:00 entry, 50% target, 2x stop, 15:45 exit; 602 trades, win 75.4% against 76.6% needed; net -$655 realistic, +$427 at mid. FOMC/CPI days expectancy -$3.00 against -$0.93; skipping them does not flip the sign. 2024 lost $1,599, much of it in early August.

### S30. Theta Profits, "Inside a 0DTE Iron Condor strategy built for smaller drawdowns" (John Einar Sandvand, 6 September 2026) [seller: community and courses around MEIC]
- Link: https://www.thetaprofits.com/inside-a-0dte-iron-condor-strategy-built-for-smaller-drawdowns/
- Found: an interviewee "did not find anything sufficiently predictive" for MEIC entries; tightened second stop after one side stops out; 71 billion rows of tick data because "one-minute data was not detailed enough to model stops"; max drawdown about $3,000 against $9,000 for MEIC over four years; backtest only.

### S31. Zonted, "Point Your Agent at This Condor: A 0DTE Implementation Plan" (10 August 2026) [unknown, blog]
- Link: https://zonted.com/posts/nothing-looked-wrong/
- Found: QQQ/SPY 0DTE condors, February 2024 to August 2026, minute data; ungated condor Sharpe 2.00; credit-spread gate adds +1.08 against a standard error of 1.04 after 820 configurations. A spread estimator on minute bars overstated round-trip cost (7.1% vs about 1.8% of premium). Admits no held-out test.

### S32. "Ultra short-dated option spreads as a fund strategy" (Pearce, studylib upload, October 2025) [unknown]
- Link: https://studylib.net/doc/27926930/ultra-short-dated-option-spreads-as-a-fund-strategy--pearce-
- Found: Option Omega backtest logs 2013 to 2025, SPX 0DTE condors entered 15:55 vs 15:58; win 80.9% vs 89.2%; stops near the close are "quasi-arbitrary"; the backtester had bugs that the author cleaned by hand. Weak.

### S33. Gao, Han, Li, Zhou, "Market intraday momentum" (JFE 129, 2018; SSRN 2440866) [academic] — introduction and sections 2-3 read
- Link: https://www.sciencedirect.com/science/article/abs/pii/S0304405X18301351
- Data: SPY, TAQ, February 1993 to December 2013.
- Found: first half-hour return (from prior close) predicts last half-hour return: slope 6.94 (x100), R² 1.6%; with the 12th half-hour, R² 2.6%; out of sample 1.4% and 2.0%. When first-half-hour vol is low, R² 0.6% and r1 insignificant; high vol, 3.3%. Stronger on high volume, recession and news days. Mechanisms: infrequent rebalancing (Bogousslavsky 2016) and late-informed trading.

### S34. Baltussen, Da, Lammers, Martens, "Hedging Demand and Market Intraday Momentum" (JFE, October 2021) [academic] — abstract read
- Link: https://pure.eur.nl/en/publications/hedging-demand-and-market-intraday-momentum/
- Found: over 60 futures, 1974-2020; rest-of-day return predicts the last 30 minutes; reverts over the next days; linked to short-gamma hedging by option market makers and leveraged ETFs.

### S35. FirmTape, "Is intraday momentum still alive?" (27 August 2026) [seller: GEX terminal, LIVE $49/month]
- Link: https://firmtape.com/research/is-intraday-momentum-still-alive
- Found: 1,085 SPX sessions, 14 April 2022 to 20 August 2026; slope of last half-hour on rest-of-day 0.006 (t 0.6), flat every year. On the 15% of days the tape-signed dealer book is short gamma at 15:30, continuation returns (added slope +0.055, t 3.1), positive in all five years; the open-interest-convention book shows nothing. Author's own caveat: four short closes in the holdout.
- Contradicts: S33 and S34 for the 0DTE era (unconditional effect gone).

### S36. FirmTape, "What the 0DTE literature actually claims" (24 August 2026) [seller, as S35] — read
- Link: https://firmtape.com/research/what-the-0dte-literature-claims
- Useful as a map: 25 papers. States "No published paper was found that forecasts intraday realised volatility at a 30-minute horizon from option state and benchmarks it against trailing RV." Reports Vilkov's unconditional net Sharpe: straddle -0.51, iron fly/condor -0.96. Claims (unverified by me) that Muravyev-Ni's split reproduces on SPXW at bid/ask.

### S37. Zarattini, Aziz, Barbon, "Beat the Market: An Effective Intraday Momentum Strategy for SPY" (SSRN 4824172, 10 May 2024, revised 22 September 2025) [academic co-author; Zarattini at Concretum Group, Aziz at Bear Bull Traders, which sells day-trading courses] — abstract read
- Link: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4824172
- Found: noise-band breakout with dynamic trailing stops, 2007 to early 2024; net return 1,985%, 19.6% a year, Sharpe 1.33; tests whether estimated dealer gamma imbalance predicts profitability.

### S38. Bandi, Fusari, Gazzani, Renò, "Ultra-short-term volatility surfaces" (arXiv 2603.29430, 2026) [academic] — abstract and introduction read
- Link: https://arxiv.org/abs/2603.29430
- Found: ATM implied-vol term structure across 0-7 day tenors "often exhibits pronounced oscillations" (example 18 August 2022); tenors under 7 days are about 70% of SPX volume by 2023. Edgeworth++ adds a deterministic shift per tenor to fit them.
- Bears on the desk's "price of each expiry against the next": the oscillation is a known fact, partly event days.

### S39. Chong and Todorov, "Volatility of Volatility and Leverage Effect from Options" (arXiv 2305.04137v2, 2024) [academic] — abstract and introduction read
- Link: https://arxiv.org/abs/2305.04137
- Found: model-free estimators of spot vol, vol-of-vol and the leverage effect (covariance of price and vol increments) from high-frequency short-dated options. Method only, no effect size. Bears on oddity 2: it gives a way to measure the spot-vol covariance separately for up and down moves.

### S40. Londono and Samadi, "The Price of Macroeconomic Uncertainty: Evidence from Daily Options" (Federal Reserve Board IFDP 1376, June 2023) [exchange or regulator; Fed staff] — full text read
- Link: https://www.federalreserve.gov/econres/ifdp/the-price-of-macroeconomic-uncertainty-evidence-from-daily-options.htm
- Data: SPX daily expirations January 2017 to May 2023; Bloomberg economic calendar.
- Found: expirations spanning CPI, FOMC, payrolls, GDP are dearer than neighbours: ATM IV +44 bp (GDP) to +134 bp (FOMC), 2.5% to 7.5%; 10-delta put minus call up to +58 bp (payrolls); VRP for FOMC-spanning options 44% (63 bp) larger. Wider set: cost "somewhat larger" for ADP, jobless claims, **ISM Manufacturing** and Markit PMI, "though most of these estimates are marginally statistically significant". CPI forward equity premium from 54 bp (12 May 2017) to 12.2% (12 January 2023), annualised.
- Left open: works at the expiry level (which expiry spans the release); does not split the day into windows, so it does not show where inside the session a 10:00 release is paid for.

### S41. Bryzgalova, Pavlova, Sikorskaya, "Retail Trading in Options and the Rise of the Big Three Wholesalers" (Journal of Finance 78(6), 2023; SSRN 4065019) [academic] — introduction and section 1 read
- Link: https://www.sikorskaya.net/files/Bryzgalova_Pavlova_Sikorskaya_2023.pdf
- Data: OPRA transactions with the price-improvement-auction flag, November 2019 to June 2021 (pre-daily-0DTE).
- Found: retail over 60% of option volume; prefers weekly options with average quoted spread 12.6% (effective 6.6%); aggregate loss $2.1 billion at a 10-day horizon; indirect trading costs $6.4 billion against $0.9 billion commissions.

### S42. Bogousslavsky and Muravyev, "An Anatomy of Retail Option Trading" (29 August 2024) [academic] — introduction read
- Link: https://www.lsu.edu/business/files/event-files/2025-finance-mardi-gras/retail_option_trading_v2.pdf
- Data: trader-level, $15 billion of retail stock and option trades from an online trading journal, 2020-2022.
- Found: typical trade is a purchase of a one-day S&P 500 call or put held about an hour; median holding half an hour; average option trade -0.9%; 0DTE trades lose 4.6% per trade (-2.95% with controls) while other options earn about zero; naked sales earn about 20%.
- Contradicts: aggregate-proxy studies (S3, S41) that report 3-9% losses per trade; the authors attribute the gap to proxies that see only spread-crossing orders and to fixed holding horizons.

### S43. tastylive, "Timing Zero-Day Trades: Volatility Patterns Uncovered" (YouTube, 16 January 2026; transcript read) [seller: broker-affiliated media]
- Link: https://www.youtube.com/watch?v=JSfxso7awzc
- Found: "three days of data on zero DT spx options" every 10 minutes; ATM IV declines through the day; first 15-30 minutes have the widest IV range; advice to sell early. Three days is anecdote, not a test.

### S44. FlashAlpha, "Are 0DTE Straddles Overpriced? We Tested 193 SPY Sessions (2022-2026)" (Tomasz Dobrowolski, 21 July 2026, updated 13 September 2026) [seller: options data API]
- Link: https://flashalpha.com/articles/are-0dte-straddles-overpriced-193-spy-sessions-data-study
- Found: Wednesdays July 2022 to April 2026; 10:00 straddle; close inside the 1-sigma band 71.0% (fair 68.3%); median realised/implied move 0.589 vs 0.674 (about 13% rich); median implied move 0.72%; worst 9 April 2025, +8.72% against 3.51%. FOMC straddles priced about double neighbouring weeks and were "largely respected".

### S45. Hull Tactical, "0DTE Options: Tiny Edge, Huge Distribution" (8 July 2026) [fund or issuer document; Hull Tactical runs a fund, commentary on Vilkov]
- Link: https://hulltactical.com/2026/07/08/0dte-options-tiny-edge-huge-distribution/
- Found: a reading of Vilkov's earlier version (September 2016 to 11 January 2024). Proposes, without testing, the conditional programme: overnight gaps, low RV regimes, macro days, "after large morning moves".

### S46. Moontower (Kris Abdelmessih), "Pricing 0dte's" (6 January 2026) [named practitioner; also seller: moontower.ai tools]
- Link: https://moontowermeta.com/pricing-0dtes/
- Found: worked example only; "volatility time" against "wall time"; straddle vega falls below 30-minute theta by about noon, so "a difference of 10 minutes" of assumed vol time is worth several vol points. No backtest.

### S47. Option Alpha, "0DTE Options: Strategy Insights from the Top Performing Trades" (undated, 230,000 trades) [seller: automated trading platform]
- Link: https://optionalpha.com/blog/0dte-options-strategy-performance
- Found: 81% SPY; iron flies and condors 78% of positions, win rates 66.76% and 70.19%; 49.64% of traders profitable; Monday most profitable, Tuesday, Thursday, Friday negative; profitable traders enter about 10:15 and exit shortly after 12:00. Survivor-selected, no costs model stated.
