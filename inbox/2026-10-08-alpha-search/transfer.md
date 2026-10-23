> Lane transfer, 38 sources read, 7 cards, 2026-10-08

Staging note, not canon. Source numbers (T1 to T38) refer to the notes at the end of this file.

## Summary

1. The strongest transfers are about **what the last half-hour was made of**, not how loud it was. The desk found that implied volatility already follows trailing realised volatility. Volatility research says two parts of that trailing number forecast differently: jumps forecast little (T1, T2), and up-moves forecast *calmer* markets while down-moves forecast rougher ones (T1). Minute data on SPX options shows implied volatility over-adjusts and drifts after jumps (T14), and single-stock implied-volatility jumps overshoot (T15). Cards 1 and 2 test whether 0DTE quotes make the same mistake. The desk holds every input.
2. **The bid-ask spread as a state, not a cost** (card 3). Two literatures disagree on what a wide option quote means: dealer inventory, which pays the seller (T7, T8), or a warning of a move, which costs the seller (T5, T25, T26). The sign is the test. Nobody I read has measured it window by window on SPXW 0DTE.
3. **Today's chain against tomorrow's** (card 4). In SPX at monthly horizons the slope of the variance term structure predicts the premium and an inverted curve flips its sign (T9). In single stocks the sign is the opposite (T4). The desk can measure the same slope between 0DTE and 1DTE every minute.
4. **Fast one-way runs mostly reverse** in futures markets (T17). A band hedger who is short gamma buys the run and sells the reversal. Card 5 tests whether pausing the hedge after such a run pays.
5. **A NIFTY natural experiment** (card 6). NIFTY expiry settlement moved from a 30-minute average to a single closing auction on 3 Aug 2026, and SEBI is already consulting on moving it back (T20 to T22). An averaged settlement carries far less last-half-hour risk than a single print. The window to test it may close.
6. Several known expiry-day effects do **not** carry to SPXW: Deribit's 30-minute average settlement, KOSPI and old NIFTY arbitrage unwinds, crypto's large premium for unhedgeable jumps. They are listed under "Known and taken" with the reason.
7. One contradiction worth raising: Dew-Becker et al. find the variance premium sits at the *shortest* maturity (T3). The desk's own numbers show no premium inside the day (pooled ratio 1.01) and a 5% to 13% premium over a day or a week. At hours, the pattern runs the other way.
8. Caution for every card: SPX option quotes at one-minute sampling are sticky relative to the spread (T23), and mid-quote bounce can fake an implied-volatility overreaction (T24).
9. Not covered: Euro Stoxx, DAX and Nikkei expiries; I ran out of budget for them before finding a primary source.

## Cards

### Card 1. A jump is charged as if it will last

- **Mechanism.** After a sharp one-minute move, 0DTE market makers re-mark implied volatility at once, and buyers who want protection after a shock arrive. Volatility research shows that the variance from a jump fades quickly, while the variance from many small moves persists (T2; S&P 500, currencies, bonds). Many jumps sit on macro announcements, which resolve uncertainty rather than create it (T2). In SPX index options, implied volatility keeps drifting for minutes after a jump: after negative jumps it rises for about 20 minutes and is still up an hour later (T14). In single stocks, jumps in implied volatility overshoot, and sellers of delta-hedged options earn abnormal returns afterwards (T15). If 0DTE quotes treat a jump-heavy half-hour like a diffuse loud half-hour, the next window is priced too dear.
- **Prediction.** Define the **jump share** of a 30-minute window as the largest squared one-minute forward return divided by the window's realised variance (or 1 − bipower variation ÷ realised variance; bipower variation is the sum of products of adjacent absolute returns, which is blind to single jumps). Compare windows within the same trailing-realised-variance quintile. The next window's pooled ratio of realised to implied variance is at least 0.1 lower after windows in the top jump-share quintile than after windows in the bottom quintile.
- **Kill line.** On fresh days the gap is under 0.05 or has the opposite sign.
- **Data needed.** Held: the one-minute implied forward and the window implied variance. Mark scheduled releases (8:30, 10:00, 14:00) from a public calendar, which is free.
- **Evidence.**
  - Jumps fade fast; continuous variation carries the forecast. Andersen, Bollerslev and Diebold, Nov 2005, https://www.nber.org/papers/w11775: "jumps are both highly prevalent and distinctly less persistent". [academic]
  - Jump sign matters for what follows. Patton and Sheppard, 7 Oct 2011, https://public.econ.duke.edu/~ap172/Patton_Sheppard_Realized_Semivariance_7oct11.pdf: "negative (positive) jumps in prices leading to significantly higher (lower) future volatility". [academic]
  - SPX option implied volatility adjusts slowly and keeps drifting after jumps. Kanniainen and Magris, 29 Oct 2018, https://arxiv.org/abs/1810.12200: "delayed and gradual movements in implied volatility after the arrival of return jumps". [academic]
  - Implied-volatility jumps overshoot in single stocks; hedged sellers earn about 10% against 3% normally. Wasielewski, 2026, http://wp.lancs.ac.uk/fofi2026/files/2026/03/FoFI-2026-134-Niklas-Wasielewski.pdf: "on average such jumps represent an over reaction of the market". [academic; working paper]
  - Against: Cboe counted two-sigma one-minute moves and found them no more common after 0DTE growth. Cboe, 8 Sep 2023, https://www.cboe.com/insights/posts/volatility-insights-evaluating-the-market-impact-of-spx-0-dte-options/: "no uptick in intraday gap moves in the S&P over the past year". [exchange or regulator]
- **Already tested?** I searched for tests of intraday jumps, bipower variation or jump share as predictors of 0DTE option returns. Vilkov's 0DTE models use only one-day-lagged realised variance and skewness (T19). The desk's tests used total trailing realised volatility. Not found tested on SPXW 0DTE in the sources read.
- **Why it may fail.** Kanniainen and Magris found the post-jump drift unprofitable after spreads in 3- to 9-month options (T14). One-minute mids can bounce inside a wide spread, which looks like an overreaction and is not (T23, T24). Jump windows are rare, so each quintile is thin. After 14:00 FOMC jumps, volatility often rises; event minutes must be handled apart.

### Card 2. Calm after a rise goes unpriced

- **Mechanism.** In the S&P 500, the semivariance of past *negative* returns predicts future volatility much more strongly than that of positive returns, and positive jumps predict *lower* volatility (T1). (Realised semivariance is realised variance counted only over the up minutes, or only over the down minutes.) The desk already knows its quotes: implied volatility rises when the index falls and "does little when it rises". In SPX options, the implied-volatility drop after a positive jump lasts only minutes and has almost vanished within an hour (T14). If the market's quote is flat after an up-dominated half-hour while what follows is calmer, the seller of the next window is paid for variance that does not come.
- **Prediction.** Within the same trailing-realised-variance quintile, the next window's pooled realised-to-implied ratio after windows whose up-semivariance share exceeds 0.65 is lower than after windows whose down-semivariance share exceeds 0.65, by at least 0.1.
- **Kill line.** On fresh days the ratio after up-dominated windows is not lower than after down-dominated windows.
- **Data needed.** Held.
- **Evidence.**
  - Patton and Sheppard (above): "future volatility is much more strongly related to the volatility of past negative returns". S&P 500 1997-2008, horizons from one day. [academic]
  - Kanniainen and Magris (above): after positive jumps the implied-volatility fall has "almost vanished within an hour". [academic]
  - Vilkov shows that up-against-down realised variation (realised skewness) explains same-day 0DTE P&L more than realised variance does, but uses it only after the fact (T19). [academic]
- **Already tested?** The desk measured how implied volatility moves *with* the index in the same window, not whether the split forecasts the next window. Vilkov uses semivariances only ex post. Not found tested on SPXW 0DTE in the sources read.
- **Why it may fail.** Patton and Sheppard work at one day and longer; at 30 minutes the sign split may only restate whether the window trended, which the desk found describes returns and does not predict them. Overlaps with card 1 when a single jump dominates. The edge must exceed a spread of about 2% of the premium.

### Card 3. A wide quote: inventory premium or alarm?

- **Mechanism.** Two published readings of a wide option quote predict opposite things. *Inventory:* market makers who have absorbed one-sided flow widen the quote and shift the mid, so the option is dear and the seller is paid; in single-stock options, illiquid options earn 2.5% to 3.4% a day more for the liquidity provider (T7), and inventory, not information, drives option price impact (T8). *Warning:* market makers widen when they fear informed or fast flow, and a move follows; the de-trended implied-volatility spread forecasts jump intensity (T25), intraday option spreads follow volatility rather than inventory (T26), and E-mini option price jumps are driven by illiquidity (T16). In SPXW the desk sees every quote every minute. The measurable state is the ATM straddle's spread against its usual level for that minute of the day.
- **Prediction.** Take the ATM straddle's relative spread at the start of each window as a z-score against the same minute over the previous 20 days. Control for the trailing realised variance. In the top decile, the next window's pooled realised-to-implied ratio is at least 0.1 *above* the other deciles (the warning reading). If it is 0.1 *below*, the inventory reading holds and the rule flips from "skip" to "sell".
- **Kill line.** On fresh days the top decile's ratio is within 0.05 of the rest.
- **Data needed.** Held: bid and ask of every contract each minute.
- **Evidence.**
  - Inventory: Christoffersen, Goyenko, Jacobs and Karoui, RFS 2018, https://ruslangoyenko.com/wp-content/uploads/2019/09/illiquidity-premia-in-the-equity-options-market.pdf: "positive illiquidity premia compensate them for the risks and costs". [academic]
  - Inventory: Muravyev, JF 2016, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1963865: "inventory risk faced by market-makers has a first-order effect on option prices". [academic]
  - Warning: Hsieh and Jarrow, revised 31 May 2017, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2264261: "de-trended percentage volatility spread explains future jump intensities better". [academic]
  - Warning: Easley, López de Prado and O'Hara, RFS 2012, https://www.stern.nyu.edu/sites/default/files/assets/documents/con_035928.pdf: "VPIN metric is a useful indicator of short-term, toxicity-induced volatility". [academic]
  - Against the warning: Andersen and Bondarenko, 2013, https://repec.econ.au.dk/repec/creates/rp/13/rp13_42.pdf: "we find no evidence of incremental predictive power of VPIN for future volatility". [academic]
  - SPX spreads move with volatility and, near the close, with end-user imbalance. Cao, Jacobs and Ke, 28 Dec 2023, https://benny.aeaweb.org/conference/2024/program/paper/DFs2GZND: "a significantly positive relationship between volatilities and SPX options spreads". [academic]
- **Already tested?** I searched for the 0DTE spread as a predictor. Vilkov puts the 10:00 spread level in a daily model zoo; I found no reported effect (T19). A blog post claims 0DTE spreads widen "minutes before volatility spikes" but is behind a paywall with no data visible (see "Could not open"). The desk has treated the spread only as a cost. Not found tested on SPXW 0DTE in the sources read.
- **Why it may fail.** Andersen and Bondarenko's point applies: the spread may only restate current volatility, which implied volatility already follows. The spread widens mechanically as expiry nears (T25), so the clock pattern must be removed. Minute quotes are sticky at the tick (T23). The windows it flags are exactly where the seller pays the widest spread.

### Card 4. The slope from today to tomorrow prices risk, not tomorrow

- **Mechanism.** In S&P 500 options, the slope of the variance term structure tells you the price of variance risk, not where variance is going. When the curve is upward-sloping, sellers of variance earn more; when it inverts, buyers of variance earn money, at every maturity tested (T9). The likely flow: in stress, hedgers buy the nearest expiry, so its price carries the premium and the forecast is a small part of it. The desk holds today's chain and tomorrow's every minute, so it can read the same slope at a horizon of hours.
- **Prediction.** At 10:00, compute the ratio of tomorrow's forward variance rate (1DTE implied variance minus today's remaining 0DTE implied variance, per unit of time, with the night handled as in the one-day study) to today's remaining 0DTE variance rate. In the lowest quintile of this ratio (inverted), the 10:00-to-close seller's pooled realised-to-implied ratio is at least 0.15 higher than in the highest quintile.
- **Kill line.** On fresh days the quintiles show no order, or the opposite order (the single-stock sign of T4).
- **Data needed.** Held. Event calendar (free) to split FOMC, CPI and payroll days.
- **Evidence.**
  - Johnson, JFQA 2017, https://www.travislakejohnson.com/pdfs/Johnson%20VIXTS%202017%20(JFQA).pdf: "SLOPE negatively predicts future returns of 18 variance assets". Straddles included; next-day quintile spreads 29-181 bp. [academic]
  - Opposite sign in single stocks. Vasquez, JFQA 2017, https://www.cambridge.org/core/journals/journal-of-financial-and-quantitative-analysis/article/equity-volatility-term-structures-and-the-cross-section-of-option-returns/F0A40E99FD2458367DD9A56A89783D38: "slope of the implied volatility term structure is positively related to future option returns". [academic]
  - The premium sits on near-term variance, not forward variance. Dew-Becker et al., May 2015, https://www.nber.org/papers/w21182: investors "indifferent to news about future variance". [academic]
  - Longer implied volatility overreacts to shorter. Stein 1989, https://stein.scholars.harvard.edu/publications/overreactions-options-market: "long-maturity options tend to 'overreact' to changes in the implied volatility of short-maturity options". Disputed by T12 and T13. [academic]
- **Already tested?** I searched for 0DTE-against-1DTE slope tests. Vilkov uses the next-day expiry only for close-to-close alignment (T19). The desk's own-data card 6 uses the *level* of tomorrow's charge to predict tomorrow, not the slope to predict today. A MenthorQ guide on 0DTE term structure appeared in the search results; I saw only its search extract, which describes spikes and reports no test. Not found tested on SPXW 0DTE in the sources read.
- **Why it may fail.** Inversions cluster on event days, when a dear front is justified; split them out and the sample shrinks. Johnson's horizon is a day to a year, not hours. Fridays put a weekend into "tomorrow". The model-free variance must be used, because model implied volatilities create false term-structure effects (T13).

### Card 5. After a fast one-way run, pause the hedge

- **Mechanism.** In liquid futures, short explosive one-way runs ("drift bursts") happen about once a week, mostly 25 to 200 basis points, and about two thirds reverse. The cause is liquidity: market makers step back or charge for immediacy, then the price comes back; short-gamma hedging is one amplifier (T17). In SPX, dealers' long gamma from positions that become 0DTE strengthens order-flow reversals within about 30 minutes (T36). A seller hedged on a band buys into an up-run and sells into the reversal, so a reverting run costs the hedger twice. Pausing re-hedging during a detected burst would recover part of that.
- **Prediction.** Flag minutes where the one-minute forward has moved the same way for at least five minutes and by more than the window's implied one-sigma move. Over the next 30 minutes the forward reverses part of the run on more than 60% of flags, and a band hedger who pauses for 30 minutes after a flag ends that span with a better P&L than the desk's band, on average.
- **Kill line.** Reversal on 50% of flags or fewer on fresh days, or no P&L gain from pausing.
- **Data needed.** Held. Tick data would detect bursts better (COR use five-second statistics); E-mini futures ticks are not held.
- **Evidence.**
  - Christensen, Oomen and Renò, J. Econometrics 2022, https://arxiv.org/abs/2601.08974: "the majority of them are accompanied by subsequent price reversion". [academic]
  - Adams, Dim, Eraker, Fontaine, Ornthanalai and Vilkov, draft 2026, https://www.jean-sebastienfontaine.com/papers/0dte-options-volatility.pdf: dealer hedging "predicts stronger order-flow reversals, lower momentum returns, and lower intraday volatility". [academic]
- **Already tested?** The desk found trending windows cost the seller and left "how straight the day has run" as a lead; the forums lane proposes a band set by the day's autocorrelation. Neither conditions on a local burst. Not found tested on SPXW 0DTE in the sources read.
- **Why it may fail.** One-minute bars blur bursts into ordinary trends, and the desk already found trends cost the seller. A burst that does not reverse leaves the paused hedger with a large open delta. Bursts are rare: perhaps a few dozen a year in the index.

### Card 6. NIFTY: from an averaged settlement to an auction (NIFTY card, not SPXW)

- **Mechanism.** Until 31 July 2026 the NIFTY close, and so NIFTY option settlement, was the average of the last 30 minutes' prices of its constituents (T20). An option on a 30-minute average carries only part of the last half-hour's risk: by my arithmetic, the variance of the average of a random walk over a window is one third of the variance of its end point. Since 3 August 2026 the close is a single closing auction, 3:20-3:30 pm with a random end (T21), like the US close that settles SPXW. Closing auctions on expiry days raise volatility and push prices in Korea (T28, T29). If NIFTY option makers did not reprice the last hour for the change, the late-day straddle has been too cheap since August. SEBI is consulting on moving settlement back to an average (T22), so the test window may close.
- **Prediction.** On NIFTY weekly expiry days, the ratio of realised variance from 15:00 to settlement to the variance priced by the 15:00 ATM straddle is higher after 3 Aug 2026 than in the months before.
- **Kill line.** No rise, or the 15:00 straddle's price relative to recent realised volatility rose at least as much.
- **Data needed.** NIFTY minute option quotes: **not held** (the desk plans to add NIFTY). Official settlement prices: free from NSE. Only about ten weekly expiries fell between 3 Aug and early October 2026.
- **Evidence.**
  - NSE, index FAQs, undated, https://www.nseindia.com/static/products-services/indices-faqs: closing prices use the "last half an hour weighted average closing prices of the constituents". [exchange or regulator]
  - SEBI circular, 16 Jan 2026, https://www.sebi.gov.in/sebi_data/attachdocs/jan-2026/1768576287344.pdf: CAS "implemented in the cash segment from August 03, 2026". [exchange or regulator]
  - SEBI consultation, Sep 2026, https://www.sebi.gov.in/sebi_data/attachdocs/sep-2026/1789202841824.pdf: "settlement price on the expiry day of Index Derivatives has changed". [exchange or regulator]
  - KCMI, undated, https://www.kcmi.re.kr/en/report/report_view?report_no=256: KOSPI 200 expiry volatility higher; it is the only major index derivative still settled on a closing auction. [academic; Korea Capital Market Institute]
- **Already tested?** I searched NSE and SEBI pages for studies of the change and found the consultation paper only. Not found tested in the sources read; it is two months old.
- **Why it may fail.** Ten expiries cannot separate a small effect. SEBI may revert before more data accrue. NIFTY costs (STT on futures hedges) may swamp any edge.

### Card 7. The same half-hour as yesterday (weak)

- **Mechanism.** Institutions split large orders over days and trade at the same clock time each day. In US stocks, returns, volume and changes in volatility at a given half-hour repeat at the same half-hour on later days, for at least 40 days (T18). A 0DTE implied variance is one number for the rest of the day; it follows the average clock pattern (the desk found the window ratio flat through the day on average) but not a day-specific pattern.
- **Prediction.** After removing the average time-of-day pattern and today's trailing windows, a window's realised-to-implied ratio today has a positive rank correlation (at least 0.1) with the same window's ratio averaged over the previous five days.
- **Kill line.** Correlation at or below zero on fresh days.
- **Data needed.** Held.
- **Evidence.**
  - Heston, Korajczyk and Sadka, JF 2010, https://ar5iv.labs.arxiv.org/html/1005.3535: "return continuation at half-hour intervals that are exact multiples of a trading day". [academic]
- **Already tested?** Not found tested on SPXW 0DTE in the sources read.
- **Why it may fail.** The evidence is for the cross-section of stocks, not the index. Scheduled releases at fixed times create a false repetition and must be removed. Weak: one source, a different market.

## Known and taken

| Effect | Where shown | Why it is not a card here |
|---|---|---|
| Strike pinning on expiry | Single stocks, 16.5 bp a stock (T27); S&P futures (flows lane) | Needs net long dealer gamma at a strike; flows lane covers SPX; Cboe reports 0DTE dealer gamma balanced |
| Declustering away from strikes at the closing auction | KOSPI 200 (T28) | Needs short-gamma hedgers at the close; SPX 0DTE dealers are net long or flat (T36); closing burst is flows card 1 |
| Arbitrage unwinds at a closing-auction expiry | KOSPI 200 (T29), NIFTY before weeklies (T30) | SPXW daily expiries have no once-a-month unwind; NIFTY effect vanished after weeklies (T30), though T31 disagrees |
| 30-minute average settlement damps last-minute risk | Deribit (T33), NIFTY before Aug 2026 (T20) | SPX settles on one print; carries to NIFTY only (card 6) |
| Roll hour at settlement | Deribit 8:00 GMT (T32) | A possible mechanism for the own-data lane's card 1 (first half-hour dear), but 0DTE income-fund flows are small (flows lane) |
| Large crypto premium for unhedgeable jumps | Deribit (T33) | SPX is hedgeable; mechanism absent |
| VPIN predicts toxicity-induced volatility | E-mini (T5) | Disputed (T6); needs signed trades, not held |
| Order imbalance predicts option returns | Equity options (T8) | Needs signed volume, not held |
| Long-dated implied volatility overreacts to short | S&P 100 (T11) | Disputed (T12) and removed by model-free tests (T13) |
| Left-tail factor in weekly options | SPX weeklies (T10) | Predicts equity returns over weeks, not same-day variance |
| Night premium, intraday momentum, dealer gamma damping | See `inbox/2026-10-07-long-gamma-research/literature-report.md` and the frontier lane | Already in the desk's known list |
| Implied-volatility index falls on Indian expiry days | India VIX (T37) | A mechanical roll of the index, not a price effect |

## Ten sources worth reading in full

| Source | Author, date | Why |
|---|---|---|
| https://arxiv.org/abs/1810.12200 | Kanniainen and Magris, Oct 2018 | Minute SPX implied volatility after jumps; the closest thing to card 1 and 2 already done |
| https://public.econ.duke.edu/~ap172/Patton_Sheppard_Realized_Semivariance_7oct11.pdf | Patton and Sheppard, Oct 2011 | The semivariance and signed-jump forecasts behind cards 1 and 2 |
| https://www.nber.org/papers/w11775 | Andersen, Bollerslev and Diebold, 2005 | How to split jumps from continuous variation (bipower variation) |
| https://www.travislakejohnson.com/pdfs/Johnson%20VIXTS%202017%20(JFQA).pdf | Johnson, 2017 | The term-structure slope as a premium signal; card 4 |
| https://arxiv.org/abs/2601.08974 | Christensen, Oomen and Renò, 2022 | Detecting fast runs and their reversal; card 5 |
| https://ruslangoyenko.com/wp-content/uploads/2019/09/illiquidity-premia-in-the-equity-options-market.pdf | Christoffersen, Goyenko, Jacobs and Karoui, 2018 | The inventory reading of spreads; card 3 |
| https://repec.econ.au.dk/repec/creates/rp/13/rp13_42.pdf | Andersen and Bondarenko, 2013 | How a plausible microstructure signal dies once current volatility is controlled |
| https://exa.ai/library/publication/q3fnhcv52xp | Kaeck, van Kervel and Seeger, 2021 | Why one-minute SPX option quotes are sticky; a limit on every card |
| https://www.sebi.gov.in/sebi_data/attachdocs/sep-2026/1789202841824.pdf | SEBI, Sep 2026 | The NIFTY settlement change and the proposals to undo it |
| http://wp.lancs.ac.uk/fofi2026/files/2026/03/FoFI-2026-134-Niklas-Wasielewski.pdf | Wasielewski, 2026 | Implied-volatility jumps overshoot; method for detecting them |

## Could not open

| Link | Reason |
|---|---|
| https://wire.insiderfinance.io/how-wide-do-spreads-get-before-big-market-moves-and-what-its-really-telling-you-f804d3edde11 | Member-only; only the teaser is visible, no data. Claims 0DTE spreads widen before volatility spikes. Not cited as evidence |
| https://www.cambridge.org/core/journals/journal-of-financial-and-quantitative-analysis/article/equity-volatility-term-structures-and-the-cross-section-of-option-returns/F0A40E99FD2458367DD9A56A89783D38 | Vasquez full text paywalled; abstract only |
| https://www.jstor.org/stable/43869115 | Muravyev JF 2016 full text behind login; SSRN abstract and the internet appendix used instead |
| https://academic.oup.com/rfs/article/25/5/1457/1569929 | ELO RFS paywalled; working-paper PDF used instead |
| https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2264261 | WebFetch returned 403; abstract read through another tool |
| NSE Clearing CAS SOP PDF (avantiscdnprodstorage link in T21's search) | Binary PDF could not be parsed; the SEBI circular and NSE page were used instead |
| https://www.kci.go.kr/kciportal/ci/sereArticleSearch/ciSereArtiView.kci?sereArticleSearchBean.artiId=ART000993079 | Korean journal page with no abstract text visible |
| https://zenodo.org/records/19220278 | Opened, but the NIFTY expiry "study" uses "a simulated yet realistic dataset"; not evidence |
| Patton and Sheppard beyond page 3 | Read pages 1-3 only (abstract and introduction) |

## Source notes

### T1. Patton and Sheppard, "Good Volatility, Bad Volatility: Signed Jumps and the Persistence of Volatility", working paper 7 Oct 2011; Review of Economics and Statistics 97(3), 2015 [academic] — pages 1-3 read
https://public.econ.duke.edu/~ap172/Patton_Sheppard_Realized_Semivariance_7oct11.pdf
S&P 500 index and 105 stocks, 1997-2008, high-frequency data. Future volatility depends far more on the semivariance of past negative returns than of positive ones. Negative jumps raise future volatility; positive jumps lower it. Averaged over both signs, jumps forecast almost nothing, which is why earlier work found jumps of little use. Holds from one day to three months. Quote: "negative (positive) jumps in prices leading to significantly higher (lower) future volatility".

### T2. Andersen, Bollerslev and Diebold, "Roughing It Up: Including Jump Components in the Measurement, Modeling and Forecasting of Return Volatility", NBER w11775, Nov 2005; REStat 2007 [academic] — NBER abstract page read
https://www.nber.org/papers/w11775
Splits realised variance into a continuous part and a jump part (bipower variation). In currencies, equity index and bonds, the jump part is large but far less persistent; nearly all predictability of daily to monthly volatility comes from the continuous part. Many jumps sit on macro announcements. Quote (abstract): jumps "distinctly less persistent than the continuous sample path variation".

### T3. Dew-Becker, Giglio, Le and Rodriguez, "The Price of Variance Risk", NBER w21182, May 2015; JFE 123(2), 2017 [academic] — NBER abstract page read
https://www.nber.org/papers/w21182
Variance swaps 1996-2014. Investors were indifferent to news about future variance at horizons from one month to 14 years; only transitory, unexpected realised variance carried a price. Forward variance claims earned about nothing; the premium sat at the shortest maturity. Quote: "indifferent to news about future variance at horizons ranging from 1 month to 14 years".

### T4. Vasquez, "Equity Volatility Term Structures and the Cross Section of Option Returns", JFQA 52(6), 2017 [academic] — journal abstract page read; full text paywalled
https://www.cambridge.org/core/journals/journal-of-financial-and-quantitative-analysis/article/equity-volatility-term-structures-and-the-cross-section-of-option-returns/F0A40E99FD2458367DD9A56A89783D38
Single stocks. Straddles on firms with a steep upward implied-volatility term structure beat those with a flat or inverted one, significantly; not explained by known factors or jump risk. Quote: "The slope of the implied volatility term structure is positively related to future option returns." The return spread itself is not in the abstract; I did not read the body.

### T5. Easley, López de Prado and O'Hara, "Flow Toxicity and Liquidity in a High Frequency World", RFS 25(5), 2012 [academic] — working-paper PDF (NYU Stern) read in extract
https://www.stern.nyu.edu/sites/default/files/assets/documents/con_035928.pdf
VPIN (volume-synchronised probability of informed trading) measures one-sided order flow in volume time. On E-mini S&P 500 futures, VPIN correlates 0.40 with the next absolute return (44,537 observations). Mechanism: toxic flow makes market makers lose, so they withdraw, and prices move. Quote: "VPIN metric is a useful indicator of short-term, toxicity-induced volatility". Needs signed trades.

### T6. Andersen and Bondarenko, "Reflecting on the VPIN Dispute", CREATES RP 2013-42 [academic] — PDF read in extract
https://repec.econ.au.dk/repec/creates/rp/13/rp13_42.pdf
Direct disagreement with T5. Once current volume and volatility are controlled for, VPIN adds no forecasting power; it was not at an extreme before the flash crash. Quote: "we find no evidence of incremental predictive power of VPIN for future volatility". Lesson for any quote-based alarm: test it against trailing realised volatility, which the desk already knows implied volatility follows.

### T7. Christoffersen, Goyenko, Jacobs and Karoui, "Illiquidity Premia in the Equity Options Market", RFS 31(3), 2018 [academic] — author PDF read in extract
https://ruslangoyenko.com/wp-content/uploads/2019/09/illiquidity-premia-in-the-equity-options-market.pdf
S&P 500 stocks, 2004-2012, intraday OPRA trades and quotes. Options with wider effective spreads earn higher delta-hedged returns: long-illiquid minus long-liquid earns 3.4% a day for ATM calls, 2.5% for ATM puts. Their reading: market makers in single-stock options are net *long* (end users sell), and the spread pays them for that inventory. The authors warn the alphas "are not readily earned by investors who must pay the spread". Quote: "positive illiquidity premia compensate them for the risks and costs".

### T8. Muravyev, "Order Flow and Expected Option Returns", Journal of Finance 71(2), 2016 [academic] — SSRN abstract read
https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1963865
Equity options. The price impact of option trades splits into inventory risk and information; the inventory part is larger. Past order imbalances predict option returns better than any common predictor. Quote: "inventory risk faced by market-makers has a first-order effect on option prices".

### T9. Johnson, "Risk Premia and the VIX Term Structure", JFQA 52(6), 2017 [academic] — author PDF read in extract
https://www.travislakejohnson.com/pdfs/Johnson%20VIXTS%202017%20(JFQA).pdf
S&P 500, 1996 onward. The slope of the VIX term structure tells you about the price of variance risk, not about where the VIX is going. One factor, SLOPE, predicts excess returns of variance swaps, VIX futures and S&P 500 straddles at all six maturities, next day and next month; negative in all 36 tests, 33 significant. The sign: an upward slope means buyers of variance lose more (sellers earn more); in the lowest SLOPE quintile (inverted curve) variance assets earn *positive* returns, e.g. 12-month straddles +30 bp a day. Next-day spread between extreme quintiles: 29 to 181 bp. Quote: "SLOPE negatively predicts future returns of 18 variance assets". Data free at https://www.travislakejohnson.com/data.html. Note the opposite sign to T4 (single stocks).

### T10. Andersen, Fusari and Todorov, "Short-Term Market Risks Implied by Weekly Options", JF 72(3), 2017; CREATES RP 2018-08 [academic] — working-paper PDF read in extract
https://pure.au.dk/ws/files/120488629/rp18_08.pdf
SPX weekly options. The left jump tail (deep OTM puts) moves on its own, not spanned by volatility, and predicts equity returns. Shown with a ratio of −7% to −6% OTM put prices at under four days, which "varies widely and quite persistently". Quote: "negative jump tail risk which is not spanned by market volatility". Shows short-dated wings carry a separate factor; it is about returns over weeks, not intraday variance.

### T11. Stein, "Overreactions in the Options Market", JF 44(4), 1989 [academic] — abstract read
https://stein.scholars.harvard.edu/publications/overreactions-options-market
S&P 100 options, 1983-87. Implied volatility mean-reverts, so a longer option's implied volatility should move by less than a shorter one's. It moves by more. Quote: "long-maturity options tend to 'overreact' to changes in the implied volatility of short-maturity options".

### T12. Diz and Finucane, "Do the Options Markets Really Overreact?", Journal of Futures Markets 13(3), 1993 [academic] — PDF read in extract
https://repec.udesa.edu.ar/pub/Finanzas/Journals/Journal%20of%20Futures%20Markets/Volume%2013-1993/Issue%203/5934509.pdf
Disagreement with T11. With a different estimator (EGLS, first differences) the same data show no overreaction, and in one subperiod slight underreaction. Quote: "The results provide no indication of overreaction in the market for index options."

### T13. "Misreaction or misspecification? A re-examination of volatility anomalies", Journal of Banking and Finance, 2010 [academic] — ScienceDirect abstract and introduction read
https://www.sciencedirect.com/science/article/abs/pii/S0378426610000920
SPX 1988-2007. Summarises Poteshman (2001): "long-horizon overreaction" and "short-horizon underreaction" in SPX implied volatility. Then shows model-free tests remove all of it: the patterns were Black-Scholes and Heston misspecification. Quote: "find no evidence of market misreaction". Lesson: test term-structure ideas on model-free variance (the desk's straddle-implied variance), not on model implied volatilities.

### T14. Kanniainen and Magris, "Option market (in)efficiency and implied volatility dynamics after return jumps", arXiv 1810.12200, 29 Oct 2018 [academic] — arXiv abstract and full HTML text read in extract
https://arxiv.org/abs/1810.12200
Minute-by-minute S&P 500 index options. After a one-minute return jump, ATM and OTM-put implied volatility does not adjust at once: it keeps drifting for minutes. After negative jumps it keeps rising for about 20 minutes and stays up an hour later. After positive jumps it falls for two or three minutes and the fall has "almost vanished within an hour". OTM-call implied volatility adjusts at once. Not profitable after spreads in their sample (3- to 9-month options). Quote: "delayed and gradual movements in implied volatility after the arrival of return jumps".

### T15. Wasielewski, "Overreaction in Implied Volatility Jumps", Frontiers of Factor Investing 2026 conference paper (Lancaster) [academic] — PDF read in extract
http://wp.lancs.ac.uk/fofi2026/files/2026/03/FoFI-2026-134-Niklas-Wasielewski.pdf
US single-stock options 1996-2023. Jumps in ATM implied volatility (detected with the Lee-Mykland test) overshoot: the volatility premium after a jump is abnormally large, and the model-free delta-hedged return to *selling* a 30-day ATM option rises from about 3% to about 10% (calls) or 6% (puts) of the premium. Quote: "on average such jumps represent an over reaction of the market". Horizon 30 days, single stocks; working paper, not yet refereed.

### T16. Kapetanios, Konstantinidi, Neumann and Skiadopoulos, "Jumps in option prices and their determinants: Real-time evidence from the E-mini S&P 500 options market", Journal of Financial Markets 46, 2019 [academic] — IDEAS abstract read
https://ideas.repec.org/a/eee/finmar/v46y2019ics1386418118300168.html
High-frequency E-mini S&P 500 options. Option prices jump on their own, not together across strikes and not with the futures. 14%-28% of option jumps fall near scheduled news, but illiquidity drives them, not news content: dealers widen spreads against fast traders. Quote: "it is illiquidity rather than the news content that drives these jumps". In SPX index options illiquidity did not drive jumps.

### T17. Christensen, Oomen and Renò, "The Drift Burst Hypothesis", Journal of Econometrics 227(2), 2022; arXiv 2601.08974 [academic] — arXiv HTML and ScienceDirect introduction read in extract
https://arxiv.org/abs/2601.08974
Tick data on liquid futures (equity, rates, FX, commodities). Short explosive one-way runs ("drift bursts") happen about once a week, mostly 25-200 bp. About two thirds reverse afterwards; reversal is stronger after negative bursts with large volume. Mechanism: market makers withdraw or demand a price for immediacy (Grossman-Miller), then the price comes back. Lists "dynamic hedging of short-gamma positions" among amplifiers. Quote: "the majority of them are accompanied by subsequent price reversion".

### T18. Heston, Korajczyk and Sadka, "Intraday Patterns in the Cross-section of Stock Returns", JF 65(4), 2010 [academic] — author PDF (Houston) and arXiv 1005.3535 read in extract
https://ar5iv.labs.arxiv.org/html/1005.3535
US stocks 2001-2005, half-hour returns. A stock's return in a half-hour predicts its return at the same half-hour on later days, for at least 40 days (t-statistics above 9.6 in the first week). Volume, order imbalance and changes in volatility show the same daily periodicity; spreads do not. Mechanism: institutions split orders and trade at the same clock time each day. Quote: "return continuation at half-hour intervals that are exact multiples of a trading day". Cross-section of stocks, not the index.

### T19. Vilkov, "0DTE Trading Rules", SSRN 4641356, annotated paper on GitHub, sample 09/2016-01/2026 [academic] — GitHub page read twice for its predictor list
https://github.com/vilkovgr/0dte-strategies/blob/main/docs/paper/paper-annotated.md
Used here only as a boundary. The 10:00 conditional models use: lagged strategy P&L, implied variance and implied skewness to the close, "slope proxies" (not defined in the text I read), one-day-lagged realised return, variance and skewness, flow and GEX variables, and liquidity (half-spread, depth, relative spread). Next-day expiries enter only at 16:00 "for close-to-close alignment". No intraday jump split, no semivariance, no 0DTE/1DTE term slope. The spread level at 10:00 is in the model zoo; I did not find its separate contribution reported. Realised up and down semivariances appear only *ex post* (10:00 to close) as explanations of P&L, where realised skewness explains more than realised variance.

### T20. NSE India, "Settlement Price" and "FAQs about Indices" pages; NSE Clearing, "Settlement Price" [exchange or regulator] — pages read
https://www.nseindia.com/static/products-services/equity-derivatives-settlement-price ; https://www.nseindia.com/static/products-services/indices-faqs
Index options settle on the closing index value. Before August 2026: "The NIFTY closing prices are calculated by taking the last half an hour weighted average closing prices of the constituents". So a NIFTY 0DTE option settled on a 30-minute average, not on one print.

### T21. SEBI circular HO/47/11/11(3)2025-MRD-POD2/I/2765/2026, "Introduction of Closing Auction Session (CAS) in the Equity Cash Segment", 16 Jan 2026; NSE CAS page (updated 12 Aug 2026); NSE derivatives modalities circular (via Dion Global, 29 Jul 2026) [exchange or regulator] — read
https://www.sebi.gov.in/sebi_data/attachdocs/jan-2026/1768576287344.pdf ; https://www.nseindia.com/static/products-services/closing-auction-session
From 3 August 2026 the closing price of F&O stocks is set by a closing auction, 3:15-3:35 pm (order entry 3:20-3:30 with random closure), reference price the 3:00-3:15 VWAP, band ±3%. Derivatives trade to 3:40 pm. Index settlement becomes "based on the closing price of the constituents", i.e. on the auction. The exchange publishes indicative equilibrium prices, imbalance quantities and an indicative index during the auction. Quote: "CAS shall be implemented as a separate session of 20 minutes".

### T22. SEBI, "Consultation Paper on Review of Certain Aspects of the Closing Auction Session, Market Timings and Settlement Methodology for Derivatives Contracts", Sep 2026 [exchange or regulator] — read in extract
https://www.sebi.gov.in/sebi_data/attachdocs/sep-2026/1789202841824.pdf
One month after the change, SEBI proposes to move index-derivative expiry settlement back off the auction: Option 1 a "Blended VWAP" of the last 30 minutes of continuous trading plus the 10-minute auction; Option 2 the pre-August "CTS VWAP" only, for at least a year. It records that settlement since 3 Aug 2026 has been "based on CAS". The paper notes market participants' concerns about expiry-day settlement. Quote: "the methodology for determining the settlement price of derivatives contracts on the expiry day has also undergone a change".

### T23. Kaeck, van Kervel and Seeger, "Price impact versus bid-ask spreads in the index option market", Journal of Financial Markets, 2021 [academic] — full text read in extract
https://exa.ai/library/publication/q3fnhcv52xp
S&P 500 options. Option trades move the index and its volatility only a little; the average effective half-spread is 169 bp, more than thirty times the price impact. At one-minute sampling their effects vanish: option price changes are 7 to 10 times smaller than the spread, so quotes "often fall within the bid and ask quotes and do not update frequently". A warning for any one-minute quote signal.

### T24. Muravyev, Internet Appendix to "Order Flow and Expected Option Returns" [academic] — PDF read in extract
https://dmurav.com/Internet%20Appendix%20to%20Order%20Flow%20and%20Option%20Returns.pdf
Order imbalance predicts option returns through future imbalance (inventory), not through future volatility (information). Also: a one-standard-deviation rise in ATM implied volatility (4 points) predicts a 0.39% *lower* option return the next day, which he attributes to "bid-ask midpoint bounce". The same bounce can fake an implied-volatility overreaction in minute data.

### T25. Hsieh and Jarrow, "Volatility Uncertainty, Time Decay, and Option Bid-Ask Spreads in an Incomplete Market", Johnson School RP 14-2013, revised 31 May 2017 [academic] — SSRN abstract read
https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2264261
The implied-volatility bid-ask spread widens at an increasing rate as expiry nears; market makers set it from inventory risk in directional and volatility risk. After removing the maturity trend, the spread "explains future jump intensities better" than the raw spread. A spread measured against its own clock pattern carries information about coming jumps.

### T26. Verousis, "The intraday determination of liquidity in the NYSE LIFFE equity option markets", University of Essex repository [academic] — PDF read in extract
https://repository.essex.ac.uk/24175/1/The%20intraday%20determination%20of%20liquidity%20in%20the%20NYSE%20LIFFE%20equity%20option%20markets.pdf
Amsterdam, London, Paris equity options. Intraday spreads and depth follow option volatility, not inventory: "Inventory management models cannot explain the intraday variation in option spreads and depths." Disagrees with T7/T8 on what spreads measure, at the intraday horizon.

### T27. Ni, Pearson and Poteshman, "Stock Price Clustering on Option Expiration Dates", JFE 78, 2005; SSRN 519044 [academic] — SSRN abstract read
https://papers.ssrn.com/sol3/papers.cfm?abstract_id=519044
Optionable stocks close at strikes on expiry days; returns shifted by at least 16.5 bp per expiry. Causes: hedge rebalancing by market makers who are net long gamma, and manipulation by proprietary traders. Quote: "closing prices of stocks with listed options cluster at option strike prices".

### T28. Sung and Oh, study of the KOSPI 200 closing auction on option expiry days (Korean, DBpia) [academic] — abstract read (Korean)
https://www.dbpia.co.kr/journal/articleDetail?nodeId=NODE01960482
The opposite of pinning. In the closing auction on KOSPI 200 option expiry days the index moves more than on other days and moves *away* from strikes ("주가디클러스터링", stock-price declustering). The authors tie it to institutions that sold options keeping them delta-neutral, i.e. short-gamma hedgers. My translation; I read the abstract only.

### T29. Chay and Ryu, "Expiration-day effects of the KOSPI 200 futures and options", Asia-Pacific Journal of Financial Studies 35(1), Feb 2006 [academic] — abstract read
https://scholarx.skku.edu/handle/2021.sw.skku/87724
Minute data 1997-2004. Volume and volatility of KOSPI 200 stocks rise in the last 30 minutes before expiry, with price reversals afterwards: arbitrageurs unwinding at a closing-auction settlement. They note such effects are "generally not found in other stock markets". KCMI (https://www.kcmi.re.kr/en/report/report_view?report_no=256) adds that KOSPI 200 is the only major index derivative still settled on a closing auction.

### T30. Kiran Kumar, "Does Short-dated Options Introduction Mitigate Expiry Day Effects? Evidence from the Introduction of Weekly Index Options", 2022 [academic] — full text read in extract
https://exa.ai/library/publication/691txyn1nxs
NIFTY 50, one year before and after weekly options (11 Feb 2019). Before: expiry-day volatility rose and reversed the next day, with upward price pressure. After weeklies: these effects disappeared. Quote: "adverse expiration day effects disappear in the period after the introduction of weekly options". One year each side; GARCH dummies.

### T31. Chhimwal, Pandey and Pandey, "Effect of multiple index derivative expiry on volatility, volume, and connectedness: a tale of two stock indices in India", Review of Derivatives Research 28(3), 2025 [academic] — IDEAS abstract read
https://ideas.repec.org/a/kap/revdev/v28y2025i3d10.1007_s11147-025-09221-8.html
Disagrees with T30 in spirit. One-minute data: after Bank Nifty's expiry moved from Thursday to Wednesday, volume and volatility of both indices rose, which they read as traders "actively trading on the expiry date due to the expiry day anomaly".

### T32. Hoang and Phan, "Time-of-day effects in the Bitcoin options market", 15 Apr 2026 [academic] — abstract read
https://exa.ai/library/publication/g01rfbk2m1b
Deribit. Option trading clusters at 8:00-9:00 GMT and 14:00-15:00 GMT. The first is investors rolling and re-opening expiring options around the 8:00 settlement; it is stronger on days with more expiring contracts and for short maturities, weekends included. The second follows the NYSE open. Quote: "driven by investors rolling over and re-establishing expiring options around the 8:00 GMT settlement".

### T33. Alexander, Deng, Feng and Wan, "Net buying pressure and the information in bitcoin option trades", Journal of Financial Markets 63, 2023; arXiv 2109.02776 [academic] — arXiv full text read in extract
https://arxiv.org/pdf/2109.02776
Deribit hourly data. 1-day and 2-day options are about 20% of volume. Hourly option volume predicts next-hour returns and realised volatility; net buying pressure moves implied volatility, with effects lasting up to five days. Volatility-motivated demand drives ATM prices. Deribit settles at 8:00 UTC on an index averaged over the last 30 minutes (also stated in https://arxiv.org/html/2410.15195v2).

### T34. Cao, Jacobs and Ke, "Derivative Spreads: Evidence from SPX Options", version 28 Dec 2023 (AEA 2024 programme) [academic] — PDF read in extract
https://benny.aeaweb.org/conference/2024/program/paper/DFs2GZND
SPX options, intraday. Percentage spreads peak around 10:00, fall through the first hour, then hold steady; they bounce at 16:00. Spreads rise with realised volatility all day; end-user demand imbalance widens them, an effect that fades near the close. Contemporaneous, not predictive. Quote: "a significantly positive relationship between volatilities and SPX options spreads".

### T35. Cboe, "Volatility Insights: Much Ado About 0DTEs - Evaluating the Market Impact of SPX 0DTE Options", 8 Sep 2023 [exchange or regulator] — page read
https://www.cboe.com/insights/posts/volatility-insights-evaluating-the-market-impact-of-spx-0-dte-options/
Counts two-sigma one-minute SPX moves (against the preceding 30-minute realised volatility): no rise since 0DTE growth, including the last hour. Dealer net 0DTE gamma is 0.04% to 0.17% of daily S&P futures liquidity. Quote: "no uptick in intraday gap moves in the S&P over the past year". Also in the flows lane as F6.

### T36. Adams, Dim, Eraker, Fontaine, Ornthanalai and Vilkov, "Do S&P 500 Options Increase Market Volatility? Evidence from 0DTEs", draft (author site) [academic] — PDF read in extract
https://www.jean-sebastienfontaine.com/papers/0dte-options-volatility.pdf
Already in the frontier lane (S5). Used here for card 5: dealer net gamma, mostly from positions opened before expiry day, predicts stronger E-mini order-flow reversals for about 30 minutes and weaker hour-to-hour momentum. Quote: "predicts stronger order-flow reversals, lower momentum returns, and lower intraday volatility".

### T37. Shaikh and Padhi, "The behavior of option's implied volatility index", Business: Theory and Practice (VGTU), 2015 [academic] — PDF read in extract
https://journals.vilniustech.lt/index.php/BTP/article/download/8279/7143/19585
India VIX 2007-2013. India VIX rises on Mondays and falls about 3% on monthly expiry days. Quote: "India VIX fall significantly on the day of expiration". Likely the index rolling its near-month leg, not a price effect; listed under "Known and taken".

### T38. KCMI (Korea Capital Market Institute), "A study on expiration-day effects of KOSPI200 futures and options", undated report page [academic] — page read
https://www.kcmi.re.kr/en/report/report_view?report_no=256
After the closing-auction crash of 11 Nov 2010. On KOSPI 200 option expiry days, volume and volatility are higher and returns lower; the US and Japan moved settlement to a special opening price, the UK and Germany to an intraday auction. KOSPI 200 is the only major index derivative still settled on a closing auction. Quote: "expiration day effects are caused by arbitragers who have to liquidate".
