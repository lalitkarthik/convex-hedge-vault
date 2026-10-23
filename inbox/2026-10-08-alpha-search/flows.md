promoted: 2026-10-23
> Lane flows, 36 sources read, 7 cards, 2026-10-08

## Summary

1. The largest fixed-time flows in SPX options are not the daily 0DTE income funds. Those are small: S&P 500 ones sell well under $1bn of notional each morning, about 440 contracts against 2.3M SPX 0DTE contracts a day (F1, F7, F15).
2. The large ones expire on two dates each month. At month-end: the three JPMorgan Hedged Equity collars, about 35,000 contracts a leg on the quarterly fund (F8, F11, F12), Innovator buffer FLEX (~$34bn in all; F19, F20), CME's new month-end options (F13) and pension calendar rebalancing (F31). In the third-Friday week: FT Vest buffers (~$47bn; F36) and the a.m. monthly SPX expiry (F23).
3. Four of the seven cards rest on those two dates. The desk's year holds 12 of each, so every card on them is low-powered. It needs earlier years of the same quotes; Databento's last 12 months are free, older data is paid.
4. Strongest card: **heavy-auction days**. The 15:50-16:00 closing burst is the most jump-prone ten minutes of the day, and 0DTE options price it (Song 2026, F32). Nobody I read splits it by month-end, quarter-end or rebalance day, or checks it against the official settlement print.
5. The JPMorgan collar strike on its own expiry day is the most-discussed flow in practitioner writing. I found no academic test, and practitioners disagree on whether it matters (F9 against F10). It may have moved to CME month-end options in April 2026 (F11). That claim is unverified, but if true it is a natural experiment inside the desk's year.
6. The third-Friday price spike (F23) reverses "by about noon", inside the 0DTE session. It was tested only to 2021, before daily expiries.
7. Two dated venue changes fall inside the desk's year. The pattern-day-trader rule ended on 4 June 2026 (F25). Retail brokers opened overnight SPX trading, for example tastytrade on 10 Aug 2026 (F24). Both are weak cards.
8. Market-maker net 0DTE gamma is small and balanced, per Cboe (F5, F6). I propose no "dealer gamma late in the day" card; that is taken and contested.
9. A possible mechanism for the own-data lane's "first half-hour priced too dear" card: 10:00 macro releases (card 6).

## Cards

### Card 1. Heavy-auction days: the closing burst is priced as on any day

- **Mechanism.** Three groups trade at the 16:00 close on dates known months ahead. First, institutions doing calendar rebalancing at month-end and quarter-end (F31). Second, buffer and collar funds whose options expire at the close: Innovator at month-end (F19), JPMorgan at month-ends (F12). Their dealers must unwind delta hedges at the close. Third, index funds on rebalance days. Quarter-end closing auctions are two to three times normal size (F22: AAPL 33.2% of its day on 30 Jun 2026 against 14.4% on 2 Jul). Expiring SPXW settles on the official close, which is built from the auctions (F22). The 0DTE market prices the 15:50-16:00 window as a focal event (F32). If the price of that window does not scale up on heavy-auction days, the 15:50 straddle is cheap on those days and dear on the others.
- **Prediction.** Take the move from the 15:50 implied forward to the official SPX close. Divide it by the move the 15:50 ATM 0DTE straddle prices. On month-end, quarter-end and S&P-rebalance days the median absolute ratio is above that of other days (sign +). On the other days the seller of the 15:50 straddle held to settlement earns more than on heavy days.
- **Kill line.** On days outside the sample, the heavy-day ratio is not above the ordinary-day ratio, or the 15:50 straddle is already dearer on heavy days by at least the gap in realised moves.
- **Data needed.** 0DTE quotes to 16:00: held. Official SPX closing values: not held, free from Cboe or S&P. A heavy-day calendar: public. Auction imbalance data (NYSE, Nasdaq NOII) would sharpen it: not held, paid. 12 month-ends and 4 quarter-ends a year, so more years are needed.
- **Evidence.**
  - Song: the closing window carries "about 1.9 times the within-day average" of jump volatility, and the 0DTE-implied jump size predicts it (R² 41-46%). https://afajof.org/management/viewp.php?n=260400, 15 Sep 2026, [academic].
  - Harvey, Mazzoleni, Melone: rebalancing predictability is "strong at month end but absent at other times". https://www.nber.org/papers/w33554, Mar 2025, [academic].
  - Strasmore tape count: "on quarter-end June 30 the same measure reached 33.2%". https://www.strasmore.com/blog/what-is-the-closing-auction, 7 Jul 2026, [seller: tape data].
  - Concretum: settlement "can differ from the last intraday SPX observation". https://concretumgroup.substack.com/p/spx-0dte-options, 1 Sep 2026, [named practitioner].
  - Nasdaq: imbalance data from "3:50 p.m. ET". https://www.nasdaqtrader.com/content/productsservices/Trading/ClosingCrossfaq.pdf, undated, [exchange or regulator].
  - Innovator: new FLEX bought "following the close of business on the last day of the Outcome Period". https://www.innovatoretfs.com/pdf/BJUL_Prospectus.pdf, 2026, [fund or issuer document].
- **Already tested?** I searched for 0DTE pricing of the closing auction and for closing-auction jumps on month-end days. Song tests whether the closing burst is priced on average. In the pages I read he does not split by day type or measure the seller's profit. Not found tested on SPXW 0DTE in the sources read.
- **Why it may fail.** Market makers know the calendar better than anyone, and Song finds the option market scales event pricing "to their information content". The heavy-day uplift may already be priced. Twelve or sixteen events a year cannot separate a few tenths of a point. The spread on a 15:50 ATM 0DTE straddle is a large share of a ten-minute premium.

### Card 2. The last hour of month-end follows the rebalancing signal

- **Mechanism.** Pension and target-date funds rebalance on the calendar toward fixed stock/bond weights, at month-end and most at quarter-end (F31). The trade's sign is known in advance: if stocks beat bonds during the month, funds sell stocks. Their orders concentrate at the close, so the index moves against the month's equity outperformance into the close.
- **Prediction.** On the last business day of the month, the 15:00-to-official-close change in the implied forward has the opposite sign to month-to-date (equity minus bond) return more often than 50%. Its size grows with the size of that gap, and is larger at quarter-ends.
- **Kill line.** On new month-ends, sign agreement at or below 50%, or no relation between size and the signal.
- **Data needed.** Implied forward: held. Official close: free. Bond return month-to-date: not held; 10-year Treasury yields from FRED (free) give a proxy.
- **Evidence.**
  - "a decrease in equity returns of 17 basis points over the next day" when stocks are overweight. https://www.nber.org/papers/w33554, Mar 2025, [academic].
  - Calendar rebalancing occurs "towards month- or quarter-end". Same source, working-paper PDF, [academic].
- **Already tested?** I searched for intraday or options tests of month-end rebalancing. Harvey et al. test daily returns in futures, not the last hour or 0DTE. Not found tested on SPXW 0DTE in the sources read.
- **Why it may fail.** The paper says the effect is front-run, so the price move may come days earlier, not in the last hour. A directional signal helps a straddle seller only through hedging, and is worth little against a 0.6% straddle. Twelve events a year.

### Card 3. The JPMorgan strike on its own expiry day

- **Mechanism.** On the last business day of each month, one of three JPMorgan Hedged Equity funds lets a three-month collar expire, and the expiring options are same-day SPX options that day (F8, F12). The quarterly fund's legs were about 35,000 contracts each in Q1 2026 (F9, F11); fund assets were $20.06bn on 31 Mar 2026 (F14). Dealers bought the short call from the fund, so if they still hold it they are long gamma there: the strike should damp moves. Dealers sold the long put, so near that strike they are short gamma and should amplify moves.
- **Prediction.** On expiry days with spot within 0.5% of the expiring short-call strike at 14:00, realised variance from 14:00 to 16:00 over the 14:00 0DTE implied variance is lower than on other days. Within 0.5% of the long-put strike it is higher.
- **Kill line.** No difference in the ratio between near-call, near-put and other days, in either direction.
- **Data needed.** Quotes: held. Collar strikes: public in quarterly N-PORT filings (F14) and in press reports (F9, F11); not held. Hedged Equity 2 and 3 strikes need their own N-PORTs.
- **Evidence.**
  - Collar legs, e.g. "Sell 45,000 contracts of the Dec 31st 4505 calls". https://spotgamma.com/jpm-morgan-collar-trade/, 30 Sep 2021, [seller: positioning data].
  - Disagreement: the dealers' strike risk "has by now, been spread across multiple participants". https://garynorden.com/articles/calling-bs-on-jpm-options-trade-analysis/, 30 Dec 2022, [named practitioner].
  - Reset dates across all three funds: "Last business day of January, April, July, October". https://am.jpmorgan.com/content/dam/jpm-am-aem/americas/us/en/literature/brochure/BRO-HE.pdf, 2026, [fund or issuer document].
  - A related academic pinning result: futures "pulled toward the at-the-money strike price" on expiry days. https://www.sciencedirect.com/science/article/abs/pii/S0304405X12001365, 2012, [academic].
  - The possible move to CME: the Q2 collar was "executed in a CME product built specifically for this purpose". https://longandshortmkts.substack.com/p/the-whale-changed-lanes, 31 Mar 2026, [unknown]. Unverified; see F14.
- **Already tested?** I searched for academic tests of the JPM collar and of known-holder strikes on expiry. I found only practitioner commentary (F9, F11) and Reuters (F34). Not found tested on SPXW 0DTE in the sources read.
- **Why it may fail.** Norden's point: by expiry the original dealers have spread the risk. Spot is near a collar strike on few expiry days (SpotGamma counts four put-strike tests since 2020). If the collar moved to CME month-end options, the dealer hedge still runs through E-mini futures, so the effect would not vanish from the index.

### Card 4. Third-Friday morning give-back

- **Mechanism.** On third Fridays the a.m.-settled monthly SPX options and the futures settle on the Special Opening Quotation (SOQ), a value built from each stock's opening trade. From 2003 to 2021, prices rose from Thursday's close to the SOQ by 18 bp and "fully reverts afterward by about noon". The authors propose market makers' charm hedging. Charm here is the change in delta with time alone. The reversal falls inside the life of that day's PM-settled 0DTE contract.
- **Prediction.** On third Fridays, the change in the 0DTE implied forward from 9:35 to 12:00 is more negative than on other Fridays. The baseline from the paper's figure is roughly 10 bp; that is my reading of the chart.
- **Kill line.** On third Fridays in 2025-2026 the 9:35-12:00 forward change is not below that of other Fridays, or the gap is under 3 bp.
- **Data needed.** Held: implied forward each minute, 12 third Fridays a year.
- **Evidence.**
  - "the SOQ exceeds the index closing price by an average of 18 basis points". https://www.aeaweb.org/conference/2025/program/paper/N7rsBN2N, Sep 2024 version, [academic].
  - The 3FPS (third-Friday price spike) "is confined to the a.m. settlement window". Same source, p. 1.
- **Already tested?** I searched for the third-Friday spike after 2021 and on 0DTE. The paper's sample ends December 2021. Not found tested on SPXW 0DTE in the sources read.
- **Why it may fail.** It was published in 2024 and may be traded away. For a straddle seller, a 10 bp drift matters only through the hedge, and the spread on the hedge may eat it.

### Card 5. Next-day calls sold on a rule

- **Mechanism.** Rule-based products sell short-dated SPX calls at a fixed minute with a strike rule anyone can compute. The S&P 500 Daily Covered Call Index, tracked by ProShares ISPY through swaps (F16), sells one-day calls. Its strike is set from VIX ("around 1% out-of-the-money" at VIX 15, "around 2%" at VIX 30) and a 10-minute index TWAP (F17). The S&P Protective Put and Covered Call Index strikes off the 12:00-12:10 TWAP (F18). Daily-call ETFs sell same-day OTM calls "at market open, or shortly thereafter" (F1-F4). Whoever buys these calls is long that strike the next day.
- **Prediction.** In the 9:35 0DTE smile, call IV at the strike the daily-covered-call rule picked yesterday is below the IV interpolated from its neighbours (a local dip). Separately, OTM call IV relative to ATM IV is lower at 9:35 than at 10:00 on average.
- **Kill line.** No dip beyond the quote noise of neighbouring strikes, and no 9:35-to-10:00 difference.
- **Data needed.** Quotes: held. VIX closes: free from Cboe. The exact TWAP window of the daily-covered-call index: in the S&P methodology, which I could not open.
- **Evidence.**
  - "At market open, or shortly thereafter, on every business day, the Fund will sell". https://www.roundhillinvestments.com/assets/pdfs/xdte_prospectus.pdf, current prospectus, [fund or issuer document].
  - "The short call option position is reestablished at the end of each day." https://www.proshares.com/globalassets/proshares/prospectuses/ispy_summary_prospectus.pdf, [fund or issuer document].
  - "Index TWAP Window for Strike Selection ... 12:00:00 12:10:00". https://www.spglobal.com/spdji/en/documents/methodologies/methodology-sp-500-pp-cc-index.pdf, [fund or issuer document].
- **Already tested?** I searched for the effect of daily covered-call funds on 0DTE prices and found nothing. Not found tested on SPXW 0DTE in the sources read.
- **Why it may fail.** Size. Funds that sell listed 0DTE calls themselves hold well under $1bn, about 440 contracts a day (F1, F15), against 2.3M (F7). ISPY's swap notional was not found. Most funds choose strikes at discretion. This is the weakest-sized card; keep it only if it is cheap to run.

### Card 6. 10:00 macro releases make the first half-hour dear

- **Mechanism.** Several scheduled releases land at 10:00 ET inside the session (ISM surveys, JOLTS, consumer sentiment). Song shows that 0DTE options price any "regularly anticipated concentration of price discovery" by building implied uncertainty into the event, then collapsing it (F32). If event premia are positive, as the literature report found for event days, the 9:35-10:05 window is dear mainly on release days. That would give the own-data lane's card 1 (pooled realised/implied 0.77-0.80 for 9:35-10:05) a mechanism.
- **Prediction.** For 9:35-10:05, realised variance over the variance charged is lower on 10:00-release days than on days without one. ATM 0DTE IV falls more from 9:58 to 10:02 on release days.
- **Kill line.** The 9:35-10:05 ratio is the same or higher on release days, or the overpricing is as large on days with no release.
- **Data needed.** Quotes: held. Release calendar: public (ISM, BLS, Census, University of Michigan calendars), not held.
- **Evidence.**
  - Event uncertainty "accumulates in advance and resolves at the event, not before it". https://afajof.org/management/viewp.php?n=260400, 15 Sep 2026, [academic]. Song covers FOMC, FOMC Minutes and the close, not 10:00 releases.
  - The only other support is the desk's own number (own-data card 1); weak.
- **Already tested?** I searched for 0DTE pricing of 10:00 releases and found none. Song covers FOMC, Minutes and the close. Not found tested on SPXW 0DTE in the sources read.
- **Why it may fail.** Many 10:00 releases move the index little, so the uplift may be too small to see. The 9:35-10:05 spread is the widest of the day (F29, on SPY).

### Card 7. The end of the pattern-day-trader rule

- **Mechanism.** Until 4 June 2026, accounts under $25,000 could make at most three day trades in five days (F25). A 0DTE option bought and held to settlement is not a day trade, so small accounts were pushed to hold to expiry. From 4 June 2026, as each broker adopts the new rule (by 20 Oct 2027 at the latest), they can sell before the close. Customer interest in 0DTE is almost all in OTM options (F26), and 95% of 0DTE trades are long options or spreads (F28). More retail selling-to-close in the afternoon should lower afternoon OTM wing prices relative to ATM.
- **Prediction.** After June 2026, the IV of 10-delta 0DTE options over ATM IV, measured at 14:00-15:30, is lower than before, against the same measure at 10:00 as a control.
- **Kill line.** No change in the afternoon-minus-morning wing ratio across the break, or a change of the opposite sign.
- **Data needed.** Quotes: held, both sides of the break inside the desk's year. Broker adoption dates: not held; from broker notices.
- **Evidence.**
  - "The effective date of the amendments is June 4, 2026". https://www.finra.org/rules-guidance/notices/26-10, 20 Apr 2026, [exchange or regulator].
  - OTM options "have customer interest at the best offer more than 80% of the time". https://www.sec.gov/files/dera-hope-reasonable-prc-2503.pdf, Mar 2025, [exchange or regulator].
- **Already tested?** I searched for the effect of the rule change on options and found nothing. It is four months old. Not found tested on SPXW 0DTE in the sources read.
- **Why it may fail.** The mechanism is mine and unsourced. Brokers adopt at different dates. The volatility regime changed over the same months. Many 0DTE retail traders already had over $25,000 or used cash accounts.

## Known and taken

- Market-maker net 0DTE gamma is small and customer flow balanced (Cboe): https://www.cboe.com/insights/posts/volatility-insights-evaluating-the-market-impact-of-spx-0-dte-options/
- 0DTE presence damps index volatility through pre-existing positions (Adams, Fontaine, Ornthanalai): https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4881008 ; Brogaard et al. disagree: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4426358
- FOMC event uncertainty accumulates from 10:00 to 14:00 in 0DTE; the pre-FOMC drift vanished in 2016; the closing window is priced as a focal event (Song): https://afajof.org/management/viewp.php?n=260400
- Third-Friday price spike and reversal by noon, 2003-2021 (Baltussen, Terstegge, Whelan): https://www.aeaweb.org/conference/2025/program/paper/N7rsBN2N
- Calendar and threshold rebalancing predicts next-day equity returns (Harvey, Mazzoleni, Melone): https://www.nber.org/papers/w33554
- Leveraged-ETF end-of-day rebalancing: statistically present, economically small, shrinking: https://www.aimspress.com/article/doi/10.3934/QFE.2024031?viewType=HTML
- Expiry-day pinning in S&P 500 futures, 1992-2009 (Golez, Jackwerth): https://www.sciencedirect.com/science/article/abs/pii/S0304405X12001365
- Customers supply liquidity with limit orders in OTM 0DTE (SEC DERA): https://www.sec.gov/files/dera-hope-reasonable-prc-2503.pdf
- Retail 0DTE timing is U-shaped in SPX, retail share 30-35% by public codes against 50-60% by Cboe: https://optionmetrics.com/blog/how-much-of-0-dte-is-really-retail-evidence-from-spx-and-spy-options/
- Settle expiring SPXW on the official close, not the last minute bar (a backtest point, not alpha): https://concretumgroup.substack.com/p/spx-0dte-options

## Ten sources worth reading in full

| Link | Author | Date | Why |
|---|---|---|---|
| https://afajof.org/management/viewp.php?n=260400 | Yuhan Song | 15 Sep 2026 | Closest prior work to cards 1 and 6; method for event uncertainty from 0DTE |
| https://www.aeaweb.org/conference/2025/program/paper/N7rsBN2N | Baltussen, Terstegge, Whelan | Sep 2024 | Card 4; a forced flow with a mechanism and a reversal time |
| https://www.nber.org/papers/w33554 | Harvey, Mazzoleni, Melone | Mar 2025 | Card 2; how to build the rebalancing signal |
| https://www.cboe.com/insights/posts/volatility-insights-evaluating-the-market-impact-of-spx-0-dte-options/ | Cboe | 8 Sep 2023 | The exchange's own market-maker gamma figures by time of day |
| https://www.sec.gov/Archives/edgar/data/1217286/000119312525261066/d79101d497k.htm | JPMorgan Trust I | 1 Nov 2025 | Collar rules in the fund's own words (card 3) |
| https://www.cftc.gov/sites/default/files/filings/ptc/25/09/ptc09032529901.pdf | CME | Sep 2025 | The new month-end options settled on the close |
| https://www.assettv.com/sites/default/files/2026-04/research-defining-paths-with-options-based-index-strategies.pdf | Edwards, Lee, Shah (S&P DJI) | 2026 | Rule-based option-writing indices and their strike rules (card 5) |
| https://www.morningstar.com/funds/how-largest-buffer-etf-providers-stack-up | Zachary Evens (Morningstar) | 18 Feb 2026 | Size and structure of buffer funds whose FLEX expire on fixed dates |
| https://www.sec.gov/files/dera-hope-reasonable-prc-2503.pdf | SEC DERA | Mar 2025 | Who sits on the 0DTE bid and offer; the tick rule at $3 |
| https://www.finra.org/rules-guidance/notices/26-10 | FINRA | 20 Apr 2026 | The rule break inside the desk's year (card 7) |

## Could not open

- https://go.cboe.com/l/77532/2025-05-02/fmjz38/77532/17461948884kPMLz2S/0DTEs_Decoded_Positioning_Trends_and_Market_Impact.pdf — full Cboe report returned an empty page; only the summary page was read.
- https://www.spglobal.com/spdji/en/documents/methodologies/methodology-sp-500-daily-covered-call-index.pdf — 403, then a timeout; the exact TWAP window of the daily covered call index is unread.
- https://www.roundhillinvestments.com/etf/xdte/ — holdings and AUM fields load by script; the fact sheet was used instead.
- JPMorgan Hedged Equity N-PORT, 30 Jun 2026 (https://www.sec.gov/Archives/edgar/data/1217286/000207169126021121/primary_doc.xml) — opened through a summariser that returned no option rows. Whether the Q2 2026 collar moved to CME is unverified.
- Hedged Equity 2 and 3 holdings and assets — not searched for lack of time.

## Appendix: source log

Each entry was written as the source was read. Card evidence cites these by F-number.

### F1. Roundhill XDTE prospectus and fact sheet [fund or issuer document]
- https://www.roundhillinvestments.com/assets/pdfs/xdte_prospectus.pdf ; fact sheet https://www.roundhillinvestments.com/assets/pdfs/xdte_etf_fact_sheet.pdf (as of 30 June 2026)
- "At market open, or shortly thereafter, on every business day, the Fund will sell out-of-the-money 0DTE call options on the S&P 500 Index". Strike: "does not seek to sell call options at a particular strike price". Long leg: deep ITM FLEX call. Inception 7 March 2024. AUM $324.4MM, 8,315,000 shares, 30 June 2026.
- Size: $324M of notional sold each morning; at SPX near 7,400-7,700 (see F36) that is about 420 to 440 SPX contracts a day (my arithmetic).

### F2. TappAlpha TSPY summary prospectus, 497K, 13 Aug 2024 [fund or issuer document]
- https://www.sec.gov/Archives/edgar/data/1771146/000199937124010204/tspy-497k_081324.htm
- "at the beginning of each trading day, the Adviser sells 'out-of-the-money' same day call options on SPY, SPX or XSP between 0% and 5% 'out of the money'". May close early "if the Adviser believes the option has yielded a majority of its potential return, and then open another option that expires the same day". Covers the entire notional, drift held within ±5%.

### F3. YieldMax S&P 500 0DTE (SDTY) summary prospectus 497K, 25 Nov 2025 [fund or issuer document]
- https://www.sec.gov/Archives/edgar/data/1924868/000199937125018562/sdty-497k_112525.htm
- "Each business day, typically at market open or shortly thereafter, the Fund sells out-of-the-money (OTM) call options on the Index (or Index ETFs) with zero days to expiration". European cash-settled index options.

### F4. Tuttle Capital SPY and 100 0DTE ETFs, 485A, 3 March 2026 [fund or issuer document]
- https://www.sec.gov/Archives/edgar/data/1771146/000177114626000498/tuttlecapspy1000dteetfs485.htm
- Sells 0DTE calls "on every business day" on SPY or SPX; may use 1DTE/2DTE FLEX when listed 0DTE is not available. No time of day given.

### F5. Cboe, "0DTEs Decoded: Positioning, Trends, and Market Impact", 2 May 2025 [exchange or regulator]
- https://www.cboe.com/insights/posts/0-dt-es-decoded-positioning-trends-and-market-impact/ (full PDF link did not open)
- SPX 0DTE "almost 2M contracts a day"; retail 50-60% (47% in early April 2025, back to 60%); over 95% limited-risk; "Only 4% of SPX 0DTE trading is in naked short options"; MM net gamma hedging "at best, just 0.2% of the SPX daily liquidity".

### F6. Cboe, "Evaluating the Market Impact of SPX 0DTE Options", 8 Sep 2023 [exchange or regulator]
- https://www.cboe.com/insights/posts/volatility-insights-evaluating-the-market-impact-of-spx-0-dte-options/
- MM net gamma $170mm to $670mm through the day; at 15:30 median +$173mm, interquartile -$1.1bn to +$2.4bn; whiskers -$5bn to +$7.7bn = 1.3% to 1.9% of daily futures notional. Example 15 Aug 2023: 4440 put, 52k buy vs 55k sell, MM short 3k. "the flow is, in fact, remarkably balanced between buy vs. sell."

### F7. Cboe, "The State of the Options Industry: 2025", 22 Jan 2026; and "SPX 0DTE Options Jump to Record 62% Share in August", 2 Sep 2025 [exchange or regulator]
- https://www.cboe.com/insights/posts/the-state-of-the-options-industry-2025/ ; https://www.cboe.com/insights/posts/spx-0-dte-options-jump-to-record-62-share-in-august/
- 2025: SPX 0DTE 2.3M contracts a day, 59% of SPX volume; FLEX volume 1.4M a day (+62%). August 2025: ~2.4M a day, 62.4%, retail ~53%. Notes "0DTE Exchange Traded Funds" as a 2026 growth area.

### F8. JPMorgan Hedged Equity Fund summary prospectus 497K, 1 Nov 2025; series brochure [fund or issuer document]
- https://www.sec.gov/Archives/edgar/data/1217286/000119312525261066/d79101d497k.htm ; https://am.jpmorgan.com/content/dam/jpm-am-aem/americas/us/en/literature/brochure/BRO-HE.pdf
- Hedge periods run "the first business day of January through the last business day of March" and so on quarterly. Put spread protects "5% to 20%, with potential upside generally capped at 3.5-5.5%". Options "may be based on the S&P 500 Index or on" S&P 500 ETFs. Three funds (JHEQX, JHQDX, JHQTX) on "staggered start dates" that "reset every three months".

### F9. SpotGamma, "JP Morgan Collar Trade", 29 Sep 2021 (updated) and "GEX & JPM Collar", 1 Apr 2026 [seller: sells options-positioning data]
- https://spotgamma.com/jpm-morgan-collar-trade/ ; https://spotgamma.com/gex-jpm-collar/
- 30 Sep 2021 roll: sold 45,000 Dec-31 4505 calls (delta 34), bought 45,000 4135 puts, sold 45,000 3480 puts; trade printed at 10:26 ET. Q1 2026: ~32,000 contracts at the 6475 put expiring 31 Mar 2026. Claims the market "holds near the JP Morgan put strike through expiration" — anecdotal, four instances.

### F10. Gary Norden, "Calling BS On Some Of The JPM Options Trade Analysis", 30 Dec 2022 [named practitioner: former options trader, author]
- https://garynorden.com/articles/calling-bs-on-jpm-options-trade-analysis/
- Disagrees with F9: the roll is done delta-neutral ("the market maker's hedge is included as part of the trade"), and by expiry the original dealers have spread the strike risk across SPX, SPY, ES, weeklies; open interest stays high only because the fund still holds its side.

### F11. Tickmill (Patrick Munnelly), "Institutional Insights: The JPM Collar", 1 Apr 2026; The Long & Short, "The Whale Changed Lanes", 31 Mar 2026; Doc McGraw, "What's up with the JPM collar?", 31 Mar 2026 [anonymous, credible / unknown]
- https://www.tickmill.com/blog/institutional-insights-the-jpm-collar-its-market-implications ; https://longandshortmkts.substack.com/p/the-whale-changed-lanes ; https://docmcgraw.substack.com/p/whats-up-with-the-jpm-collar
- Q1 2026 legs 7155 call / 6475 put / ~5310 put, ~35,000 contracts each. Claim: the Q2 2026 collar (5210/6180 put spread v 6865 call) was put on at the 31 Mar close in CME S&P 500 Month-End options (SME), settled to the 4pm cash close, executed by BTIC — not in SPX. **Unverified against a JPM filing; needs N-PORT.**

### F12. JPMorgan brochure BRO-HE and press release of 26 Feb 2021 (launch of JHQDX, JHQTX) [fund or issuer document]
- https://am.jpmorgan.com/content/dam/jpm-am-aem/americas/us/en/literature/brochure/BRO-HE.pdf ; https://www.nasdaq.com/press-release/j.p.-morgan-asset-management-launches-two-hedged-equity-funds:-jhqdx-and-jhqtx-2021
- Reset dates: Hedged Equity "Last business day of December, March, June, September"; Hedged Equity 2 "January, April, July, October"; Hedged Equity 3 "February, May, August, November". So **every month-end is a reset day for one of the three funds.** Morningstar (https://www.morningstar.com/funds/xnas/jhqdx/quote) adds that the laddered ETF resets a third of its options every month.

### F13. CME, S&P 500 Month-End futures and options: CFTC self-certification 25-316 (Sep 2025) and FAQ [exchange or regulator]
- https://www.cftc.gov/sites/default/files/filings/ptc/25/09/ptc09032529901.pdf ; https://www.cmegroup.com/articles/faqs/sanp-500-month-end-futures-and-options.html
- Listed for trade date Monday 22 September 2025. Futures and options expire "at 4:00 p.m. ET on the final business day of the contract month"; final settlement = "official closing value of the index"; futures trade only as BTIC (basis to the close). FAQ: launched to let traders "fine-tune exposures more accurately around key dates".

### F14. SEC N-PORT for JPMorgan Hedged Equity Fund, periods 31 Mar 2026 and 30 Jun 2026 [exchange or regulator filing]
- https://www.sec.gov/Archives/edgar/data/1217286/000207169126012745/primary_doc.xml ; https://www.sec.gov/Archives/edgar/data/1217286/000207169126021121/primary_doc.xml
- Net assets $20.06bn (31 Mar 2026) and $18.52bn (30 Jun 2026). 31 Mar 2026 report lists a written S&P 500 Index put, strike 5,470, expiring 2026-03-31 (Options Clearing Corporation), plus long E-mini futures. My reading tool returned no option rows for 30 Jun 2026, only 5,351 long E-mini Sep-26 futures. This neither confirms nor refutes the SME migration claim (F11); the reading was through a summariser and may be incomplete.

### F15. Dividend Vision 0DTE income ETF list (data as of 3 Oct 2026) and comparison post of 29 Jul 2026; LegalClarity summary, 9 Jul 2026 [unknown: fund-data websites]
- https://www.dividendvision.com/lists/0dte-income-etfs ; https://www.dividendvision.com/blog/0dte-etfs-weekly-income-odte-qdte-xdte ; https://legalclarity.org/0dte-options-etfs-how-they-work-risks-and-top-funds/
- 17 daily-option income ETFs. S&P 500 ones are small: XDTE ~$338M, SDTY ~$46M, ODTE ~$3M; the largest of the group, QDTE ($918M), is on the Nasdaq-100. Earliest entrant Defiance WDTE, 18 Sep 2023. **Order of size: well under $1bn of SPX notional sold each morning by funds that write listed 0DTE calls themselves**, against ~2.3M SPX 0DTE contracts a day (F7).

### F16. ProShares ISPY summary prospectus (497K, 2023 to 2026) [fund or issuer document]
- https://www.sec.gov/Archives/edgar/data/1174610/000168386323008426/f37197d1.htm ; https://www.proshares.com/globalassets/proshares/prospectuses/ispy_summary_prospectus.pdf
- Tracks the S&P 500 Daily Covered Call Index: "out-of-the-money S&P 500 Index call options having one day to expiration when sold". "The short call option position is reestablished at the end of each day." The fund uses swaps, so **the swap dealer, not the fund, sells the listed calls**. Inception 18 Dec 2023.

### F17. S&P DJI, "Get to know the S&P 500 Daily Covered Call Indices" (Talking Points) and S&P DJI research "Defining Paths with Options-Based Index Strategies" (Edwards, Lee, Shah, 2026) [fund or issuer document: index provider]
- https://www.spglobal.com/spdji/en/documents/education/talking-points-get-to-know-the-sp500-daily-covered-call-indices.pdf ; https://www.assettv.com/sites/default/files/2026-04/research-defining-paths-with-options-based-index-strategies.pdf
- Index sells "listed S&P 500 Weeklys Options one day from their maturity date"; strike set from VIX and "a 10-minute time-weighted average price (TWAP) window" of the index. "With VIX close to its median level of 15, the option strike will be around 1% out-of-the-money. With VIX at 30, it will be around 2%." Launched 5 Oct 2023. (The methodology PDF itself returned 403; the exact TWAP window times were not read.)

### F18. Cboe Daily Covered Call Indices methodology; Cboe Volatility Contingent Daily Covered Call methodology; S&P 500 Protective Put and Covered Call Index methodology [fund or issuer document: index provider]
- https://cdn.cboe.com/api/global/us_indices/governance/Cboe_Daily_BuyWrite_Indices_Methodology.pdf ; https://cdn.cboe.com/api/global/us_indices/governance/Cboe_Volatility_Contingent_Daily_Covered_Call_Indices_Methodology.pdf ; https://www.spglobal.com/spdji/en/documents/methodologies/methodology-sp-500-pp-cc-index.pdf
- Cboe: "On each roll date, a new call option expiring the following exchange listed PM-settled options expiration date is sold", priced at a TWAP of mids; SPDVDCC sells only when VIX at 14:00 > 20-day average and VIX futures are backwardated. S&P PP&CC: call strike = nearest to SPX TWAP over **12:00:00-12:10:00 ET**, the call expires next day. **Rule-based products fix the strike and the minute of sale of next-day calls, which become the following day's 0DTE strikes.**

### F19. Innovator U.S. Equity Buffer ETF prospectuses (BJUL, BAUG, BSEP, BOCT 497K Feb 2026) [fund or issuer document]
- https://www.innovatoretfs.com/pdf/BJUL_Prospectus.pdf ; https://www.sec.gov/Archives/edgar/data/1415726/000121390026021483/ea0276309-29_497k.htm
- FLEX options on SPY, held to "the final day of the Outcome Period"; outcome periods end on the **last day of a calendar month** (e.g. "July 1, 2026 through June 30, 2027"); new FLEX set "following the close of business on the last day of the Outcome Period".

### F20. Morningstar, "Defined Outcome ETF Landscape" (2026) and "How the Largest Buffer ETF Providers Stack Up", 18 Feb 2026; ETF Action weekly recaps 15 and 22 Jun 2026; Cboe, "How Outcome Based ETFs Are Reshaping Investor Demand", 7 Aug 2025 [named practitioner research / exchange]
- https://www.morningstar.com/funds/how-largest-buffer-etf-providers-stack-up ; https://www.etfaction.com/buffer-etf-aum-surges-to-94b-as-june-reset-drives-1-7b-in-flows/ ; https://www.cboe.com/insights/posts/how-outcome-based-etfs-are-reshaping-investor-demand/
- $78bn in 420 defined-outcome ETFs at end-2025; 74% on the S&P 500; First Trust ~$40bn, Innovator ~$27.5bn. $94bn across 505 ETFs by 22 Jun 2026 (FT Vest $46.7bn, Innovator $33.9bn); the "June reset" week brought FJUN +$706M. Cboe: over $70bn in July 2025, 98% buffers.

### F21. NYSE trading information page; Nasdaq Closing Cross FAQ [exchange or regulator]
- https://www.nyse.com/trade/trading-information ; https://www.nasdaqtrader.com/content/productsservices/Trading/ClosingCrossfaq.pdf
- NYSE: "3:50 p.m. to 4:00 p.m. ET - Closing Imbalance Period", closing auction at 4:00. Nasdaq: "Nasdaq begins disseminating the Net Order Imbalance Indicator (NOII) at 3:50 p.m. ET", every 10 seconds to 3:55, every second after; MOC entry stops 3:55, LOC entry 3:58.

### F22. Concretum Research, "SPX 0DTE Options", 1 Sep 2026; CashflowEngine, "SPX Settlement Explained", 11 Jul 2026; Strasmore, "What Is the Closing Auction?", 7 Jul 2026 [named practitioner (Concretum: Zarattini's research firm) / seller (CashflowEngine sells a backtester; Strasmore sells tape data)]
- https://concretumgroup.substack.com/p/spx-0dte-options ; https://cashflowengine.io/learn/spx-settlement/ ; https://www.strasmore.com/blog/what-is-the-closing-auction
- Expiring SPXW stops trading at 4:00 and settles on the official close built from the closing auctions, which "can differ from the last intraday SPX observation" (worked example 6,398 against 6,402). Strasmore tape counts: AAPL auction 14.4% of its day on 2 Jul 2026 and **33.2% on quarter-end 30 Jun 2026**; NVDA 24.7% at quarter-end. CashflowEngine: SPX GTH 8:15 p.m. to 9:25 a.m. ET as of July 2026.

### F23. Baltussen, Terstegge, Whelan, "The Derivative Payoff Bias", version Sep 2024 (AEA 2025 programme) [academic] — first three pages read
- https://www.aeaweb.org/conference/2025/program/paper/N7rsBN2N
- 2003-2021: on third Fridays "the SOQ exceeds the index closing price by an average of 18 basis points" (t = 3.5); E-mini prices drift up overnight, peak at the SOQ and "fully reverts afterward by about noon 3rd Friday" (the 3rd Friday Price Spike). No such pattern around the p.m. settlement. Call payoffs too high by ~$2.6bn a year; total wealth transfer ~$3.5bn a year. Proposed channel: market makers' charm hedging. Sample ends December 2021, before daily SPXW expiries.

### F24. Cboe Global Trading Hours pages and insight, 9 Feb 2026; Cboe press release, 28 May 2026; tastytrade press release, 10 Aug 2026 [exchange or regulator / broker]
- https://www.cboe.com/insights/posts/cboe-global-trading-hours ; https://ir.cboe.com/news/news-details/2026/Cboe-Receives-SEC-Approval-to-Offer-Extended-Trading-Hours-for-Select-Multi-Listed-Single-Stock-Options/default.aspx ; https://tastytrade.com/newsroom/press-releases/global-trading-hours/
- SPX, SPXW and XSP trade in GTH 8:15 p.m. to 9:25 a.m. ET, plus Curb 4:15-5:00 p.m. ET. "GTH and Curb volumes reached record levels in the first quarter of 2026, up 32%" year on year. tastytrade (10 Aug 2026) quotes Cboe: GTH "more than 4% of total SPX options volume, up sharply from roughly 3% just months earlier", and opened GTH to its retail customers that day. Equity-option pre-market (7:30-9:25) and post-market (4:00-4:15) sessions from 13 July 2026.

### F25. FINRA Regulatory Notice 26-10, 20 Apr 2026; SEC Release 34-105226, 14 Apr 2026 [exchange or regulator]
- https://www.finra.org/rules-guidance/notices/26-10 ; https://www.sec.gov/files/rules/sro/finra/2026/34-105226.pdf
- The pattern-day-trader designation and "$25,000 pattern day trader minimum equity requirement" are replaced by intraday margin standards. "The effective date of the amendments is June 4, 2026"; brokers may phase in until 20 October 2027. **This break falls inside the desk's data year**, but each broker's adoption date differs.

### F26. SEC DERA, "Hope at a Reasonable Price: Customer Use of Limit Orders in the 0DTE Market", March 2025 [exchange or regulator]
- https://www.sec.gov/files/dera-hope-reasonable-prc-2503.pdf
- SPXW limit-order book, 1 Jul 2020 to 28 Sep 2023. Customers sit at the best bid up to ~60% of the day (July 2023) for slightly OTM options, and "well out-of-the-money options have customer interest at the best offer more than 80% of the time". "a quarter of all 0DTE trades are customer MTOs and POs that got filled". Tick is $0.05 below $3 and $0.10 above; just-OTM calls reach the $0.05 range only in the last hour (January 2023).

### F27. OptionMetrics, "How Much of 0-DTE Is Really Retail? Evidence from SPX and SPY Options", 28 Sep 2026 [seller: sells option data]
- https://optionmetrics.com/blog/how-much-of-0-dte-is-really-retail-evidence-from-spx-and-spy-options/
- From OPRA condition codes, SPX 0DTE retail share 30-35% (Cboe's broker-identity estimate 50-60%). SPX retail volume is U-shaped, trough 12:00-12:45; retail share ~28% at the open, 31-34% the rest of the day. SPY shows a retail spike near 15:45 "consistent with 0-DTE positions being closed out ahead of expiration". Institutions front-load opening trades (~18% in the first 30 minutes).

### F28. FOW (Radi Khasawneh), "Cboe points to retail flow as zero-day options grow", 4 May 2025 [anonymous, credible: trade press quoting Cboe's president on an earnings call]
- https://www.fow.com/insights/analysis-cboe-points-to-retail-flow-as-zero-day-options-grow
- Robinhood went live with Cboe index options in October 2024 and rolled out "index options to all customers in late January" 2025; Q1 2025 0DTE ~2M a day, 55% of SPX volume; "95% of those in SPX 0DTE are what we call 'capped risk'"; put/call ratios "around 1".

### F29. Strasmore, "When Do 0DTE Options Trade? By the Hour", 12 Jul 2026 [seller: tape data]
- https://www.strasmore.com/blog/when-do-0dte-options-trade
- One session (10 Jul 2026): same-day flow 148.9k contracts a minute in the first half hour, low of 50.3k in the 14:00 hour, 62.6k in the last hour. SPY same-day spread 0.8% of mid in the opening half hour, 2.67% in the closing hour. One day only; weak.

### F30. Leveraged-ETF rebalancing: Shum, Hejazi, Haryanto, Rodier (Rev. Finance 2016, author copy); Lenkey survey (QFE 2024); Barbon, Beckmeyer, Buraschi, Moerke (SFI 22-40, 2022); Rodriguez (EFMA 2024) [academic]
- https://utoronto.scholaris.ca/bitstreams/55d149e5-bf5c-4211-a446-6326d2397019/download ; https://www.aimspress.com/article/doi/10.3934/QFE.2024031?viewType=HTML ; https://www.sfi.ch/en/publications/n-22-40-liquidity-provision-to-leveraged-etfs-and-equity-options-rebalancing-flows-evidence-from-end-of-day-stock-prices ; http://www.efmaefm.org/0EFMAMEETINGS/EFMA%20ANNUAL%20MEETINGS/2024-Lisbon/papers/LETF20231228EFMA.pdf
- Shum et al.: 2006-2011, potential LETF rebalancing averaged 6.57% of end-of-day dollar volume; raises end-of-day volatility, mostly on volatile days; rebalancing may start "as early as 3:30PM". Lenkey: associations are statistically significant but "the economic associations appear to be insignificant". Barbon et al.: LETF and option-hedging flows cause end-of-day momentum and reversal; "LETFs effects have decreased over time". **Known and taken.**

### F31. Harvey, Mazzoleni, Melone, "The Unintended Consequences of Rebalancing", NBER w33554, March 2025 [academic]
- https://www.nber.org/papers/w33554 ; PDF https://www.nber.org/system/files/working_papers/w33554/revisions/w33554.rev0.pdf
- Calendar and threshold rebalancing by institutions with "$20 trillion in U.S. retirement assets": when stocks are overweight, next-day equity returns are ~17 bp lower. "Calendar predictability is strong at month end but absent at other times", and stronger toward quarter-end. Cost ~$16bn a year. Signal = trailing equity minus bond return, known in advance. Daily horizon only; no intraday or options test.

### F32. Yuhan Song, "Pre-FOMC Uncertainty Accumulation: Evidence from 0DTE Options", 15 Sep 2026 (AFA submission, HEC Montréal) [academic] — pages 1-5 read
- https://afajof.org/management/viewp.php?n=260400
- FOMC days: 0DTE-implied event volatility rises from 0.60% at 10:00 to 0.78% at 14:00, collapses at the statement, rebuilds before the 14:30 press conference. The Lucca-Moench pre-announcement drift vanished at the first FOMC after Wednesday SPX expiries were listed (Feb 2016). **Closing window:** "The closing window of 15:50-16:00 ET concentrates more discontinuous volatility than any other ten-minute interval of the trading day, about 1.9 times the within-day average"; the 0DTE-implied expected jump magnitude predicts closing-window jump volatility with R² 41%-46%; the implied direction predicts nothing. **Not seen in pages read:** any split by month-end, quarter-end, rebalance or expiry day, or any seller-profit measure for the closing window.

### F33. Adams, Fontaine, Ornthanalai, "The Market for 0DTE: The Role of Liquidity Providers in Volatility Attenuation", SSRN 4881008 (2024) abstract; Brogaard, Han, Won, "Does 0DTE Options Trading Increase Volatility?", SSRN 4426358 (2023) abstract [academic]
- https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4881008 ; https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4426358
- Adams et al.: index vol falls 60-90 annualised bp on 0DTE days; market makers "absorb end-users' trades in long-dated options that eventually become 0DTE positions". Brogaard et al. disagree: one SD more 0DTE trading raises volatility, "primarily driven by speculative retail investors". (Frontier lane covers these in full.)

### F34. Reuters (Saqib Iqbal Ahmed), "How a massive options trade by a JP Morgan fund can move markets", 28 Jun 2022 and 30 Mar 2023 [anonymous, credible: wire service]
- https://www.reuters.com/markets/us/how-massive-options-trade-by-jp-morgan-fund-can-move-markets-2022-06-28/ ; https://www.reuters.com/markets/us/how-massive-options-trade-by-jp-morgan-fund-can-move-markets-2023-03-30/
- Fund assets $16.71bn (27 Jun 2022) and $14.71bn (29 Mar 2023); "analysts say the ... reset roiled markets in the closing hours of the last quarter". No measurement.

### F35. Golez and Jackwerth, "Pinning in the S&P 500 futures", Journal of Financial Economics 2012 (abstract and introduction on the journal page) [academic]
- https://www.sciencedirect.com/science/article/abs/pii/S0304405X12001365
- 1992-2009: futures pinned to the ATM strike on serial futures-option expiry days; "anti-cross-pinning" before SPX option expiry; shift "at least $115 million per expiration day". Mechanisms: dealer delta-hedge decay (anti-pinning) against investor reselling and early exercise (pinning). Pre-0DTE; not about a single known holder's strike.

### F36. First Trust FT Vest U.S. Equity Buffer ETF - June (FJUN) fund page and 497K, 22 Jun 2026 [fund or issuer document]
- https://www.ftportfolios.com/retail/etf/etfsummary.aspx?Ticker=FJUN ; https://www.sec.gov/Archives/edgar/data/1667919/000144554626004537/etf8_497k.htm
- Outcome period "June 22, 2026 through June 17, 2027"; SPY FLEX options; starting SPY value $746.74. So FT Vest series reset in the week of the monthly (third-Friday) expiry, while Innovator series (F19) reset at month-end. SPY $773.49 on 8 Oct 2026, so SPX is near 7,700 (my reading of SPY ×10).
