> Merged from five lanes, 157 sources across them, 20 re-opened at the merge, 2026-10-09. Staging note, not canon.

# Read first: new hypotheses for SPXW same-day options

The five lane reports are [frontier](frontier.md), [flows](flows.md), [transfer](transfer.md), [forums](forums.md) and [own-data](own-data.md). The brief is [_brief.md](_brief.md). The desk's own results are in [results.md](../2026-10-08-feature-experiments/results.md).

Two measures appear on every card. The **charged variance** of a window is the variance that the at-the-money (ATM) same-day straddle prices for that window at its start. The **realised/charged ratio** is the realised variance of the window divided by the charged variance. *Pooled* means the sum of realised variance over all windows divided by the sum of charged variance. A pooled ratio below 1 pays the seller. A ratio above 1 pays the buyer.

## In one page

New hypotheses for this market come from two places. The first place is the clock. The session holds a few fixed times when some group must trade or when news must arrive: the 10:00 releases, the closing auction from 15:50, the Friday close before a weekend, the third-Friday open, and the last business day of the month. The second place is the *shape* of the last half-hour, not its size. The desk already found that implied volatility follows recent realised volatility. The literature says that the sign of recent moves and the share of a single jump forecast differently from total volatility. The desk has not tested either.

Two windows of the day were reached by several lanes from different sides. The last 25 minutes and the closing auction came from frontier (Song's closing burst), flows (heavy auction days), and forums (a former market maker and an ES trader). The first half-hour and the 10:00 releases came from own-data (the only half-hour priced dearer than it moved), frontier and flows. Each window is now one card that keeps all lanes' sources. The agreement is less independent than it looks. Frontier and flows both rest on the same paper (Song 2026) for both windows. Forums cites frontier's notes in its cards 1 and 4.

The strongest candidate is the closing ten minutes. It has a documented mechanism: market-on-close orders and published imbalances from 15:50, and the settlement of every expiring SPXW contract on the official close. An academic paper finds the most jump variance of the day there and finds that same-day options price it. Nobody computed whether the seller or the buyer of that window earns money. The lanes disagree on the sign, and that is the test.

The next strongest are the 10:00 releases, the weekend, and the third-Friday morning. The 10:00 card is weaker than the lanes say: a Fed paper that the merge re-opened finds that most second-tier releases are not priced. The weekend card is stronger than the forums lane says. A Journal of Finance paper (Jones and Shemesh 2018), which no lane had found, documents the same mispricing over weekends in S&P 500 index puts from 1996 to 2014. Nobody has tested it on the Monday expiry in the same-day era. The third-Friday card rests on a paper whose sample ends in December 2021, before daily expiries.

Every card here is a hypothesis. No source tested any of the top eight on SPXW same-day options for profit and loss. Several cards occur rarely: 12 third Fridays, 12 month-ends and about 8 FOMC days a year. One year of quotes cannot decide them. Earlier years are paid data.

The search did not find several things. It found no primary source that sizes the money that trades at the close by day type. It could not read Reddit with any tool. It did not cover Euro Stoxx, DAX or Nikkei expiries. It found no test of the option spread as a signal on same-day options. Two lane claims remain unverified: the April 2026 move of the JPMorgan collar to CME options, and a trader's memory that the 15:50 burst began in 2020.

## The candidates

| Rank | Name | Mechanism in one line | Testable on data held | Evidence | Lane |
|---|---|---|---|---|---|
| 1 | The closing ten minutes | MOC orders and imbalances from 15:50 make a known burst before the official close that settles SPXW | yes (official close is free) | moderate | frontier, flows, forums |
| 2 | The 10:00 releases and the opening half-hour | Hedgers pay for 10:00 release risk, so the 9:35 to 10:05 window is dear on release days | yes (calendar is free) | weak | own-data, frontier, flows |
| 3 | The weekend charged by convention | Pricers count part of the weekend as trading time, so Friday's price of the Monday expiry is too high | yes | strong (general), none on SPXW | forums, merge |
| 4 | The third-Friday morning give-back | Prices rise into the a.m. settlement print, then fall back by noon inside the same-day session | yes | strong to 2021, none after | flows |
| 5 | The JPMorgan collar strike | A known fund's expiring strikes at month-end change dealer gamma near those strikes | partly (strikes from filings) | weak | flows |
| 6 | The sign of the last half-hour | Falls predict rougher markets and rises calmer ones; quotes may price both alike | yes | moderate | frontier, transfer, own-data |
| 7 | Which wing carries the premium | Buyers of calls or buyers of puts overpay, and the two papers disagree | yes | moderate | frontier |
| 8 | A jump is charged as if it will last | Jump variance fades fast; quotes may treat it like persistent variance | yes | moderate | transfer |
| 9 | Today's expiry against tomorrow's | The slope from 0DTE to 1DTE prices variance risk, not tomorrow's variance | yes | moderate | transfer, forums |
| 10 | Sell the statement, not the press conference | On FOMC days the premium resolves at 14:00 | yes (about 8 days a year) | moderate | frontier |
| 11 | Month-end rebalancing in the last hour | Pension funds rebalance against the month's equity gain at the close | partly (bond proxy free) | moderate | flows |
| 12 | NIFTY: from an averaged settlement to an auction | The August 2026 change put the last half-hour's full risk into settlement | no (NIFTY quotes) | moderate | transfer |
| 13 | Older-expiry gamma sets continuation | Positions from older expiries decide whether a loud half-hour continues | no (open interest) | moderate | frontier |
| 14 | A wide quote: inventory or alarm | A wide straddle spread either pays the seller or warns of a move | yes | moderate | transfer, own-data |
| 15 | The held-strike asymmetry, and a hedge that leans short | The fall-only rise of held-strike IV is partly smile geometry; a hedge can allow for it | yes | moderate | frontier, own-data |
| 16 | After a fast one-way run, pause the hedge | Fast runs mostly reverse; a band hedger pays twice | yes | moderate | transfer |
| 17 | Next-day calls sold on a rule | Index rules fix the strike and minute of call sales | yes | weak | flows |
| 18 | Retail buys the morning | Retail call buying makes the morning dear on the call side | partly | weak | frontier |
| 19 | Event premium set off the last event | FOMC and CPI straddles follow the last reaction | no (needs years) | weak | forums |
| 20 | Morning vol-of-vol and tomorrow | A high-uncertainty morning makes tomorrow's options cheap | partly (proxy) | weak | frontier |
| 21 | Hedge back to the band edge | Trading only the excess delta cuts whipsaw cost | yes | weak | forums |
| 22 | The same half-hour as yesterday | Split institutional orders repeat at a clock time | yes | weak | transfer |
| 23 | The end of the pattern-day-trader rule | Small accounts can now sell before the close | yes | weak | flows |
| 24 | Band width from the day's autocorrelation | Narrow the band in trends, widen it in chop | yes | weak | forums |
| 25 | A dear tomorrow is too dear | High one-day charges overshoot | yes | weak | own-data |
| 26 | Quiet, then a break | A quiet half-hour precedes a directional move | yes | weak | own-data |
| 27 | The day that has run straight | Sellers overprice continuation after a straight day | yes | weak | own-data |
| 28 | Do not sell the week when it is cheap | A weekly straddle cheap against last week is not cheap enough | yes | weak | own-data |

Why each card sits where it does:

1. Closing ten minutes: the most specific mechanism (who, the minute, the settlement rule) in exchange rules and a 2026 paper, testable with free data, and nobody measured its profit.
2. 10:00 releases: a specific clock time and free calendar, but the re-opened Fed paper weakens the premium for most releases.
3. Weekend: a refereed paper documents the mechanism and the desk holds the exact contract, but the general effect is known, so novelty is only partial.
4. Third Friday: a refereed-quality mechanism with a time of reversal, but only 12 days a year, and the effect reaches a straddle seller only through the hedge.
5. JPMorgan collar: the most precise "who and which strike" of any card, but the effect is disputed, few days fall near a strike, and the strikes are not yet in hand.
6. Sign of the last half-hour: well documented at daily horizons, cheap to test as a filter, but the mechanism names no one who must trade.
7. Wing: two academic papers that disagree make a clean test, but the mechanism is about who overpays, not about a fixed time.
8. Jump share: strong at daily horizons, but the one minute-level test found no profit after spreads.
9. to 28.: each is weaker on one of the four criteria; the reason is in *The rest*.

## The top candidates in full

### 1. The closing ten minutes

The S&P 500 official close is not the last trade of the day. The exchanges set it in closing auctions at 16:00. A **market-on-close (MOC) order** is an order to trade at that closing price. At 15:50 the exchanges start to publish the **closing imbalance**, the excess of buy over sell orders waiting for the close. On NYSE, 15:50 is also the MOC entry deadline. Every expiring SPXW contract settles on the official close, not on the last index tick.

Song (2026) finds that 15:50 to 16:00 holds more jump variance than any other ten minutes of the day, about 1.9 times the within-day average. He also finds that same-day options price this burst in advance: the implied jump size predicts the closing burst with R² of 41% to 46%. He does not compute anyone's profit. His option data stop at 15:40. The desk's twelve windows end at 15:35. So the last 25 minutes are untested by everyone.

Four lane cards reach this window and they disagree on the sign. Frontier expects the seller to earn, because elsewhere the premium is paid where uncertainty resolves (the FOMC statement). Forums cites a former index market maker who says the last 10 to 30 minutes are *cheap*. In his account, market-maker models price off futures while the cash print decides settlement, and he stopped quoting ten minutes before the close. Flows expects the burst to be larger on heavy-auction days (month-end, quarter-end, index rebalance) and the price not to scale with it. Forums card 5 expects a step in variance at 15:50 that the chain prices too smoothly.

1. **Name.** The closing ten minutes.
2. **Mechanism.** Index funds, rebalancing institutions and funds whose options expire must trade at the 16:00 close. Their orders show in the imbalance from 15:50. The official close settles SPXW. Market makers may withdraw or widen in the last minutes. The resulting burst is known in advance in time but not in size.
3. **Prediction.** (a) The pooled realised/charged ratio from 15:50 to the official close, charged by the 15:50 ATM straddle mid, differs from 1 beyond the day-reshuffled band on both half-years. Frontier predicts below 1; forums predicts above 1.1. Run the same test from 15:35. (b) On month-end, quarter-end and S&P rebalance days the ratio is above that of other days. (c) Realised variance per minute from 15:50 to 16:00 is at least 1.5 times that from 15:35 to 15:50.
4. **Kill line.** The pooled ratio lies inside the reshuffled band around 1 on both half-years. Or a ratio outside the band does not survive the bid for the seller, or the ask for the buyer. For (b), heavy days are not above ordinary days on new days.
5. **Data needed.** Held: quotes to 16:00 and the implied forward. Not held, free: official SPX closing values (Cboe or S&P) and a heavy-day calendar. Not held, paid: auction imbalance data (NYSE imbalance feed, Nasdaq NOII). Heavy days need earlier years.
6. **Evidence.**
   - Song, "Pre-FOMC Uncertainty Accumulation: Evidence from 0DTE Options", 23 August 2026 (SSRN) and 15 September 2026 (AFA version), [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7412318), [AFA PDF](https://afajof.org/management/viewp.php?n=260400). The closing window "concentrates more discontinuous volatility than any other ten-minute interval". His footnote dates the imbalance publication and the MOC deadline to 15:50. [academic] Re-opened.
   - FSU, Elite Trader, "Underpriced SPX options at expiration", 29 October 2017, [thread](https://www.elitetrader.com/et/threads/underpriced-spx-options-at-expiration.314509/). Says expiring SPX options are cheap in the last 10 to 30 minutes and that "the models broke down in the last minutes of trading on expiration". He kept no record. [anonymous, credible: says 25 years as an OEX market maker] Re-opened.
   - jlabtrades, NexusFi, "Does anybody use Market on Close (MOC) imbalance values in their trading?", 7 August 2023, [thread](https://nexusfi.com/showthread.php?p=889041&t=60003). Says the first move on the final imbalance often goes against its sign, and that "a larger intraday move usually means a less volatile MOC". [unknown] Re-opened.
   - Strasmore, "What Is the Closing Auction?", 7 July 2026, [page](https://www.strasmore.com/blog/what-is-the-closing-auction). AAPL's auction was 33.2% of its day on quarter-end 30 June 2026 against 14.4% on 2 July. [seller: tape data] Not re-opened.
   - Harvey, Mazzoleni, Melone, NBER w33554, March 2025, [paper](https://www.nber.org/papers/w33554). Rebalancing predictability is "strong at month end but absent at other times". [academic] Not re-opened.
7. **Already tested?** Song measures implied pricing, not profit, and stops at 15:40. Vilkov enters at 15:00 and holds to the close unhedged, with no ratio for the last slice (frontier S1). A late-day condor log (Pearce, frontier S32) is weak. A forum poster's last-hour short strangle claim rests on screenshots that nobody could read. Not found tested on SPXW 0DTE in the sources read.
8. **Why it may fail.** The relative spread is widest at the close, and Song drops quotes after 15:40 for that reason. A ten-minute straddle is small, so a spread of a few ticks is a large share of it. FSU's edge may be execution inside a wide market, which a mid or ask test cannot copy. Market makers know the auction calendar, and Song finds pricing scaled to information content.

### 2. The 10:00 releases and the opening half-hour

Several US releases come out at 10:00 New York time: the ISM surveys, JOLTS, University of Michigan sentiment, new and pending home sales, factory orders and construction spending. They fall inside the desk's first window, 9:35 to 10:05. That window is the only half-hour whose pooled ratio was below 1 on both half-years: 0.77 on the seen days and 0.80 on the fresh days.

Song argues that same-day options price "any regularly anticipated concentration of price discovery". If a 10:00 release is priced and resolves at 10:00, the excess charge should sit on release days. Londono and Samadi (Fed, 2023) test release pricing at the level of whole daily expiries. They find clear premia for CPI, FOMC, payrolls and GDP. For ISM Manufacturing the cost is somewhat larger but "marginally statistically significant". For most other releases they find no price at all.

So the release story may not hold, and two rivals stay open. One rival is the opening itself (frontier card 1b): the excess sits in 9:35 to 9:45 and shrinks after a small overnight gap. The other is retail demand at the open (card 18). The own-data lane gives its own warning: twelve half-hours were looked at, so one of them below 1 on both samples is weak evidence by itself.

1. **Name.** The 10:00 releases and the opening half-hour.
2. **Mechanism.** Hedgers who are short same-day gamma quote through a known jump time at 10:00 on release days. If the premium is paid where uncertainty resolves, the first window is dear on release days and fair on other days.
3. **Prediction.** The 9:35 to 10:05 pooled ratio is lower on days with a scheduled 10:00 release than on days without one, on both half-years. On release days realised variance concentrates in 10:00 to 10:03. Split ISM days from other release days. Rival 1b: if the ratio is equal across release and non-release days, the excess sits in 9:35 to 9:45 and is smaller after small overnight gaps.
4. **Kill line.** The ratio is the same on release and non-release days within the reshuffled band, or the excess charge is as large on no-release days. For 1b: no concentration in 9:35 to 9:45.
5. **Data needed.** Held: quotes and the window variance. Not held, free: release calendars from BLS, ISM, Census and the University of Michigan. Fix the release set before opening the data.
6. **Evidence.**
   - Desk's own number, part 1, experiment 4: pooled ratio 0.77 and 0.80 for 9:35 to 10:05 ([own-data](own-data.md), card 1). Noticed after the data was opened.
   - Song, as card 1. Same-day options price "any regularly anticipated concentration of price discovery", tested on FOMC, FOMC Minutes and the close only. [academic] Re-opened.
   - Londono and Samadi, "The Price of Macroeconomic Uncertainty: Evidence from Daily Options", Fed IFDP 1376, June 2023, [Fed page](https://www.federalreserve.gov/econres/ifdp/the-price-of-macroeconomic-uncertainty-evidence-from-daily-options.htm). ISM and other second-tier releases: "most of these estimates are marginally statistically significant". Also: "The majority of additional releases that we examine are not priced". [exchange or regulator: Fed staff] Re-opened (abstract page and full text in extract).
   - Gao, Han, Li, Zhou, "Market intraday momentum", JFE 2018, [journal page](https://www.sciencedirect.com/science/article/abs/pii/S0304405X18301351). The first half-hour digests overnight news. [academic] Not re-opened.
7. **Already tested?** Almeida et al., Song and Vilkov all start at 10:00 or later because of spreads. Londono and Samadi work at the expiry level and do not split the day. Not found tested on SPXW 0DTE in the sources read.
8. **Why it may fail.** The spread is widest at the open. Most 10:00 releases are not priced even at the expiry level. The excess may come from overnight news or the opening auction. Only part of the year has a 10:00 release on a given weekday.

### 3. The weekend charged by convention

An option model must say how much time passes between Friday's close and Monday's open. A calendar-day model counts three days. A business-day model counts close to none. The market sits between the two, and where it sits is a convention of the people who quote, not a measurement of weekend variance.

Jones and Shemesh (Journal of Finance, 2018) find that delta-hedged option returns are strongly negative over weekends and holidays and about zero on other days. For delta-hedged equity puts the gap is −0.86% per period, January 1996 to August 2014. They find strong evidence in S&P 500 index puts and weaker evidence in index calls. They attribute it to mispricing: implied volatilities embed sizable variance while the market is closed. Kris Abdelmessih, a former market maker, says that with a 365-day model the market decayed options by only about 2/3 of model theta over a weekend. The two views fit together: the market charges less than a full calendar weekend, but still more than the weekend delivers.

The desk holds the exact contract for this. On Friday afternoon the Monday SPXW expiry is a one-trading-day option that spans the weekend. On Monday morning it is the same-day expiry. The desk found that nights are about a third of a week's movement, but it never split the weekend out.

1. **Name.** Friday's price of the Monday expiry is too high.
2. **Mechanism.** Quoters set Friday prices with a time convention that counts part of the weekend as trading time. Weekend variance is smaller than that count. Sellers who hold over the weekend are paid for variance that does not come.
3. **Prediction.** For the Monday-expiry ATM straddle, the variance charged from Friday 15:55 to Monday 9:35 (the drop in total implied variance) exceeds the realised variance of the forward over the same span. Its pooled ratio is below the pooled ratio of weekday nights (Monday to Thursday close into the next day's open), on both half-years.
4. **Kill line.** The weekend ratio is not below the weekday-night ratio by more than one round-trip spread, on both half-years.
5. **Data needed.** Held: the Monday expiry sits in the one-to-seven-day file on Friday (strikes within 5% of the money, enough for ATM).
6. **Evidence.**
   - Jones and Shemesh, "Option Mispricing around Nontrading Periods", Journal of Finance 73(2), April 2018, [author PDF](https://faculty.marshall.usc.edu/Christopher-Jones/pdf/jones_shemesh_2018_jf.pdf). "option returns are significantly lower over nontrading periods". [academic] Opened at the merge; no lane had it.
   - Kris Abdelmessih, Moontower, "weekend theta", 20 March 2025, [post](https://moontower.ai/blog/weekend-theta). "the market seemed to only decay the options by 2/3". He warns it "is not free money": weekend gaps are larger. [named practitioner; seller: moontower.ai tools] Re-opened.
   - newwurldmn, Elite Trader, "Theta over weekends versus overnight", 12 January 2018, [thread](https://www.elitetrader.com/et/threads/theta-over-weekends-versus-overnight.316988/). "it's not okay to ascribe a full trading day". [anonymous, credible] Re-opened.
   - SteadyOptions forum, "Theta Decay Question", 28 August 2013, [thread](https://steadyoptions.com/forums/forum/topic/1473-theta-decay-question/). A poster relays a market maker who moves his model clock forward one day from Thursday 11:00. [unknown, second-hand] Not re-opened.
7. **Already tested?** Jones and Shemesh test equity options and S&P 500 index options close to close, 1996 to 2014. That is before the Monday SPXW expiry and the same-day era. A tastytrade study is cited second-hand in a forum and was not read. Not found tested on SPXW 0DTE or the Monday expiry in the sources read.
8. **Why it may fail.** About 50 weekends a year, and a few large gaps decide the result. The effect was published in 2018 and may be priced now. Monday 9:35 quotes are noisy. The seller cannot hedge the weekend gap, so carries the full tail.

### 4. The third-Friday morning give-back

The monthly a.m.-settled SPX options and the futures settle on the **Special Opening Quotation (SOQ)**, an index value built from each stock's first trade on the third Friday. Baltussen, Terstegge and Whelan find that from 2003 to 2021 the SOQ exceeds Thursday's close by 18 basis points on average (t = 3.5). E-mini futures drift up overnight, peak at the SOQ, and the rise "fully reverts afterward by about noon". No such pattern exists around the p.m. settlement.

They propose **charm** as the channel. Charm is the change in an option's delta with the passage of time alone. Market makers who hedge the expiring a.m. options must trade as their deltas decay overnight, and that trade pushes the open. The authors also report that the spike was not priced into options at Thursday's close.

The reversal from 9:30 to noon falls inside the life of that day's p.m.-settled SPXW contract. The paper's sample ends in December 2021, before daily expiries existed. The desk can see whether the give-back survives in 2025-26.

1. **Name.** Third-Friday morning give-back.
2. **Mechanism.** Hedging of the expiring a.m. options lifts prices into the SOQ print. Once the print is set, the pressure ends and prices revert by about noon.
3. **Prediction.** On third Fridays, the change of the same-day implied forward from 9:35 to 12:00 is more negative than on other Fridays. The flows lane reads the paper's chart as roughly 10 basis points; that reading is not checked.
4. **Kill line.** On third Fridays in 2025-26 the 9:35 to 12:00 forward change is not below that of other Fridays, or the gap is under 3 basis points.
5. **Data needed.** Held: the implied forward each minute. Twelve third Fridays a year; earlier years are paid.
6. **Evidence.**
   - Baltussen, Terstegge, Whelan, "The Derivative Payoff Bias", version September 2024, AEA 2025 programme, [paper](https://www.aeaweb.org/conference/2025/program/paper/N7rsBN2N). "the SOQ exceeds the index closing price by an average of 18 basis points". The authors also state that a strategy on the spike is profitable after costs, in futures. [academic] Re-opened.
7. **Already tested?** The paper ends in December 2021. No test on same-day options was found. Not found tested on SPXW 0DTE in the sources read.
8. **Why it may fail.** The paper is public since 2024 and the effect may be traded away. A straddle seller gains from a known drift only through the hedge, and the hedge's own cost may eat 10 basis points. Twelve days a year give little power.

### 5. The JPMorgan collar strike

Three JPMorgan Hedged Equity funds each hold a three-month **put-spread collar** on the S&P 500. A collar here is three options: buy a put about 5% below the market, sell a put about 20% below, and sell a call 3.5% to 5.5% above to pay for the puts. The funds reset on staggered dates: the last business day of March, June, September and December for the first fund, and the next two months for the other two. So every month-end is a reset day for one fund. On that day the expiring legs are same-day SPX options.

SpotGamma puts the legs at about 30,000 to 35,000 contracts each in early 2026. It says the dealers who sold the fund its long put were short about $1 billion of gamma at the 6475 strike the day before the March 2026 expiry. If dealers still hold the other side on expiry day, they are long gamma near the short-call strike, which damps moves. They are short gamma near the long-put strike, which amplifies moves.

Gary Norden, a former options trader, argues the opposite. By expiry the original dealers have traded the strike risk away across SPX, SPY, ES and weeklies. Open interest stays high only because the fund still holds its side. A further claim, not verified, says the Q2 2026 collar moved to CME month-end options in April 2026.

1. **Name.** The JPMorgan strike on its own expiry day.
2. **Mechanism.** A known holder's large expiring strikes, at known dates, change the gamma of the dealers who took the other side.
3. **Prediction.** On reset days with spot within 0.5% of the expiring short-call strike at 14:00, the 14:00 to 16:00 realised/charged ratio is lower than on other month-ends. Within 0.5% of the long-put strike it is higher.
4. **Kill line.** No difference in the ratio between near-call, near-put and other reset days.
5. **Data needed.** Held: quotes. Not held, free: strikes from each fund's quarterly **N-PORT** filing (the holdings report a US fund files with the SEC) on EDGAR, and press reports.
6. **Evidence.**
   - J.P. Morgan Asset Management, "JPMorgan Hedged Equity Fund Series" brochure, 2026, [PDF](https://am.jpmorgan.com/content/dam/jpm-am-aem/americas/us/en/literature/brochure/BRO-HE.pdf). Reset dates: "Last business day of December, March, June, September" for the first fund. [fund or issuer document] Re-opened.
   - SpotGamma, "GEX & JPM Collar", 1 April 2026, [post](https://spotgamma.com/gex-jpm-collar/). "approximately 30,000–35,000 contracts per leg in SPX index options". [seller: positioning data] Re-opened.
   - Gary Norden, "Calling BS On Some Of The JPM Options Trade Analysis", 30 December 2022, [post](https://garynorden.com/articles/calling-bs-on-jpm-options-trade-analysis/). The strike risk "has by now, been spread across multiple participants". [named practitioner] Re-opened.
   - Golez and Jackwerth, "Pinning in the S&P 500 futures", JFE 2012, [journal page](https://www.sciencedirect.com/science/article/abs/pii/S0304405X12001365). Futures pinned to the ATM strike on expiry days, 1992 to 2009. [academic] Not re-opened.
7. **Already tested?** Only practitioner commentary and Reuters were found. Not found tested on SPXW 0DTE in the sources read.
8. **Why it may fail.** Norden's argument. Spot sits near a collar strike on few reset days. If the collar moved to CME, the dealer hedge still runs through E-mini futures, so the test may still see it, but the strikes must come from new sources.

### 6. The sign of the last half-hour

**Realised semivariance** is realised variance counted only over the up minutes, or only over the down minutes. Patton and Sheppard find, in the S&P 500 from 1997 to 2008, that future volatility depends much more on past downside semivariance than on upside. Negative jumps raise future volatility; positive jumps lower it. This holds from one day to three months ahead.

Option quotes react to the sign in a known way. In minute data on S&P 500 index options, Kanniainen and Magris find that implied volatility keeps moving for some time after a negative jump. The desk sees a held strike's implied volatility rise about 3 points per 1% fall and do little on a rise. If quotes stay flat after an up-dominated half-hour while what follows is calmer, the next window's seller is overpaid. After a down-dominated half-hour the opposite may hold, and the tail may cluster there.

The desk's own result points the same way. Skipping after a loud trending half-hour cut the worst day (−27.9 against −47.0 points on the seen days, −18.1 against −25.9 on the fresh days) but not the average. Frontier card 2 asks whether falls carry all of that cut. The ECB argues that when positioning leans to puts, hedging impact is skewed to the downside. Dim, Eraker and Vilkov find momentum stronger when market-maker gamma is low.

1. **Name.** The sign of the last half-hour.
2. **Mechanism.** Falls raise the variance that follows and rises lower it. Quotes may not lower implied volatility after rises, and may underprice the continuation after falls, when hedgers short gamma trade with the move.
3. **Prediction.** (a) Within the same trailing-realised-variance quintile, the next window's pooled ratio after windows whose up-semivariance share exceeds 0.65 is at least 0.1 lower than after windows whose down share exceeds 0.65. (b) Split the desk's skip rule by the sign of the trigger window: skips after falls give most of the worst-day cut on both half-years; skips after rises cost average return and cut little tail.
4. **Kill line.** (a) On fresh days the ratio after up-dominated windows is not lower. (b) Rise and fall skips cut the worst day by similar amounts.
5. **Data needed.** Held.
6. **Evidence.**
   - Patton and Sheppard, "Good Volatility, Bad Volatility: Signed Jumps and the Persistence of Volatility", working paper 7 October 2011 (REStat 2015), [PDF](https://public.econ.duke.edu/~ap172/Patton_Sheppard_Realized_Semivariance_7oct11.pdf). "negative (positive) jumps in prices leading to significantly higher (lower) future volatility". [academic] Re-opened.
   - Kanniainen and Magris, "Option market (in)efficiency and implied volatility dynamics after return jumps", arXiv, 29 October 2018, [abstract](https://arxiv.org/abs/1810.12200). "delayed and gradual movements in implied volatility after the arrival of return jumps". [academic] Re-opened (abstract).
   - ECB, Andrzej Sowiński, "The risks from hidden leverage in short-term equity options", Financial Stability Review box, 22 November 2023, [box](https://www.ecb.europa.eu/press/financial-stability-publications/fsr/focus/2023/html/ecb.fsrbox202311_02~0cf2c71d00.it.html). Hedging impact "skewed to the downside (upside)" when puts (calls) dominate. An argument, not a test. [exchange or regulator] Re-opened.
   - Dim, Eraker, Vilkov, SSRN 4692190, June 2025, [paper](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4692190). Momentum earns 10 basis points an hour more in low-gamma states. [academic] Not re-opened.
   - Desk: part 2, section 5 ([own-data](own-data.md), card 5).
7. **Already tested?** The desk measured how implied volatility moves *with* the index, not whether the sign forecasts the next window. Vilkov uses semivariances only after the fact. Not found tested on SPXW 0DTE in the sources read.
8. **Why it may fail.** At 30 minutes the sign may only restate whether the window trended, and trend describes returns without predicting them. The year holds few tail days. This is a second filter on the same 249 days, so it must be judged on new days. As a skip rule it removes trades and adds no spread cost.

### 7. Which wing carries the premium

The variance a straddle seller is paid for can be split into an upside part, priced by out-of-the-money calls, and a downside part, priced by out-of-the-money puts. The **variance risk premium (VRP)** is the excess of implied over realised variance. Almeida, Freire and Hizmeri find that for same-day options only, the VRP comes mainly from the upside. Investors pay more for exposure to gains than to losses. Their trade on mispriced bounds was profitable to 2022 and then dissipated.

Vilkov finds the opposite in structure returns. Put ratio spreads, which sell far puts, are the best same-day structure out of sample (net Sharpe 0.93). Call ratio spreads stay unattractive. That places the premium in the downside wing. The two use different samples and entry times. The desk can measure both wings each half-hour.

1. **Name.** Upside or downside: where the same-day premium lives.
2. **Mechanism.** One group of end users overpays for one wing. Almeida's reading: buyers of calls (retail buys calls more than puts). Vilkov's reading: buyers of downside protection.
3. **Prediction.** For each 30-minute window, build implied upside and downside semivariance from OTM calls and OTM puts and set each against realised up and down semivariance from the minute forward. If Almeida is right, the call-side ratio is lower on both half-years.
4. **Kill line.** The put side is lower (Vilkov), or the two are equal within the reshuffled band.
5. **Data needed.** Held (all strikes each minute).
6. **Evidence.**
   - Almeida, Freire, Hizmeri, "0DTE Asset Pricing", SSRN 4701401, written 20 January 2024, revised 20 June 2025, [paper](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4701401). "investors require more compensation for positive market returns than for negative returns". [academic] Re-opened.
   - Vilkov, "0DTE Trading Rules", annotated paper, data September 2016 to January 2026, [GitHub](https://github.com/vilkovgr/0dte-strategies/blob/main/docs/paper/paper-annotated.md). Put ratio spread net Sharpe 0.93 out of sample; "Call ratio spreads remain unattractive". [academic] Re-opened.
7. **Already tested?** Almeida et al. measure from 10:00 to 14:00 entries held to the close, 2012 to March 2025. Vilkov tests structures to the close. Neither tests 30-minute windows on minute quotes in 2025-26. Not found tested on SPXW 0DTE in the sources read.
8. **Why it may fail.** Almeida et al. show their trade fading after 2022, so the upside premium may be gone. One year cannot separate a wing premium from the year's drift. Far wings have wide relative spreads.

### 8. A jump is charged as if it will last

Realised variance in a window has two parts: many small moves, and a few single large moves called **jumps**. **Bipower variation** sums the products of adjacent absolute returns. A single jump hardly changes it, so realised variance minus bipower variation estimates the jump part. The **jump share** of a window is that jump part divided by realised variance (or, more simply, the largest squared one-minute return divided by realised variance).

Andersen, Bollerslev and Diebold find that jumps in the S&P 500, the dollar and bonds are frequent but far less persistent than the small-move part. Almost all forecast power for daily to monthly volatility comes from the small-move part. Many jumps fall on macro news. Baule and Wasielewski find that jumps in single-stock implied volatility overshoot: the delta-hedged seller earns about 10% (calls) or 6% (puts) of the premium afterwards, against about 3% normally.

The desk found that implied volatility at a window's start follows trailing realised volatility closely (rank correlation 0.79 and 0.86). If the quotes do not separate a jump-heavy half-hour from a broadly loud one, the next window is charged too much after a jump.

1. **Name.** A jump is charged as if it will last.
2. **Mechanism.** Market makers re-mark implied volatility after a sharp move, and protection buyers arrive after a shock. The jump's variance fades fast, so the next window delivers less than it is charged.
3. **Prediction.** Within the same trailing-realised-variance quintile, the next window's pooled ratio is at least 0.1 lower after windows in the top jump-share quintile than after windows in the bottom quintile. Mark scheduled release minutes and treat them apart.
4. **Kill line.** On fresh days the gap is under 0.05 or has the opposite sign.
5. **Data needed.** Held. Free: the release calendar.
6. **Evidence.**
   - Andersen, Bollerslev, Diebold, "Roughing It Up", NBER w11775, November 2005, [abstract](https://www.nber.org/papers/w11775). "jumps are both highly prevalent and distinctly less persistent". [academic] Re-opened.
   - Kanniainen and Magris, as card 6. Under actual spreads, "our results do not imply abnormal option returns". [academic] Re-opened.
   - Baule and Wasielewski, "Overreaction in Implied Volatility Jumps", 15 December 2025, Frontiers of Factor Investing 2026, [PDF](http://wp.lancs.ac.uk/fofi2026/files/2026/03/FoFI-2026-134-Niklas-Wasielewski.pdf). "on average such jumps represent an over reaction of the market". US single stocks 1996 to 2023, 30-day options. [academic, working paper] Re-opened.
   - Cboe, "Volatility Insights: Evaluating the Market Impact of SPX 0DTE Options", 8 September 2023, [post](https://www.cboe.com/insights/posts/volatility-insights-evaluating-the-market-impact-of-spx-0-dte-options/). Against: no rise in two-sigma one-minute moves. [exchange or regulator] Not re-opened.
7. **Already tested?** Vilkov's models use only one-day-lagged realised variance and skewness. The desk used total trailing realised volatility. Not found tested on SPXW 0DTE in the sources read.
8. **Why it may fail.** Kanniainen and Magris found no profit after spreads in index options. One-minute mids bounce inside a wide spread, which can look like an overreaction. Jump windows are rare, so each quintile is thin. After 14:00 FOMC jumps, volatility often rises.

## The rest

Each line: mechanism, prediction, data, best links. "Not re-opened" applies to every link in this section.

**9. Today's expiry against tomorrow's** (transfer 4, forums 4). In S&P 500 options the slope of the variance term structure predicts variance-asset returns, and an inverted curve pays buyers. A forum poster says he is always a buyer of same-day index options against later expiries. *Prediction:* at 10:00, in the lowest quintile of tomorrow's forward variance rate over today's remaining rate, the 10:00-to-close seller's pooled ratio is at least 0.15 higher than in the highest quintile. A second form: a gamma-matched 0DTE-long, 1DTE-short calendar from 10:00 to 15:35 earns after both spreads. *Data:* held. *Links:* [Johnson, JFQA 2017](https://www.travislakejohnson.com/pdfs/Johnson%20VIXTS%202017%20(JFQA).pdf); [destriero, Elite Trader, 30 Sep 2023](https://www.elitetrader.com/et/threads/0dte-options-craze.376425/). *Rank:* testable and new at hours, but nobody documents who buys the nearest expiry in stress, and Almeida et al. find the same-day premium larger than the next day's.

**10. Sell the statement, not the press conference** (frontier 4). Event uncertainty builds to 14:00 and collapses; Song puts 71% of priced event variance at the statement. *Prediction:* a hedged straddle sold 13:55 and bought 14:20 earns more per unit of charge than one sold 14:20 and bought 15:00. *Data:* held, about 8 days a year. *Links:* [Song 2026](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7412318) (re-opened for card 1); [Johannes, Kaeck, Seeger](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4484011). *Rank:* specific and documented, but eight days a year is too few.

**11. Month-end rebalancing in the last hour** (flows 2). Pension funds sell stocks at month-end after stocks beat bonds. *Prediction:* on the last business day, the 15:00-to-close forward change has the opposite sign to month-to-date stock-minus-bond return more than half the time. *Data:* held forward; official close and FRED yields free. *Link:* [Harvey, Mazzoleni, Melone, NBER w33554, Mar 2025](https://www.nber.org/papers/w33554). *Rank:* primary source, but the paper says the trade is anticipated days earlier, and direction helps a straddle seller only through the hedge.

**12. NIFTY: from an averaged settlement to an auction** (transfer 6). From 3 August 2026 NIFTY settles on a closing auction, not a 30-minute average. *Prediction:* on NIFTY expiry days, the 15:00-to-settlement ratio is higher after 3 August than before. *Data:* not held (NIFTY minute quotes). *Links:* [SEBI circular, 16 Jan 2026](https://www.sebi.gov.in/sebi_data/attachdocs/jan-2026/1768576287344.pdf); [SEBI consultation, Sep 2026](https://www.sebi.gov.in/sebi_data/attachdocs/sep-2026/1789202841824.pdf). *Rank:* a clean regulator-dated break, but no data and about ten expiries so far, and SEBI may reverse it.

**13. Older-expiry gamma sets continuation** (frontier 6). Dampening comes from positions built in older expiries. *Prediction:* after a loud trending half-hour, the seller's next-window loss is larger in the bottom tercile of non-0DTE open-interest gamma. *Data:* open interest not held. *Links:* [Adams et al., Jul 2026](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5641974); [Ardia and Vaudescal, Jul 2026](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7202999). *Rank:* strong papers, but the data is missing and the sign convention is a guess.

**14. A wide quote: inventory or alarm** (transfer 3; own-data's unused "width of the quote"). A wide straddle spread either pays the seller for inventory or warns of a move. *Prediction:* in the top decile of the spread's z-score against the same minute of the last 20 days, the next window's ratio differs from the rest by at least 0.1; the sign decides the reading. *Data:* held. *Links:* [Christoffersen et al., RFS 2018](https://ruslangoyenko.com/wp-content/uploads/2019/09/illiquidity-premia-in-the-equity-options-market.pdf); [Hsieh and Jarrow, 2017](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2264261). *Rank:* testable and untested, but no one is forced to trade, and the spread may only restate current volatility.

**15. The held-strike asymmetry, and a hedge that leans short** (frontier 5, own-data 2). A held strike's IV change mixes a shift of the smile level with a slide along a U-shaped smile; the desk's hedge to the Black delta is left long about 0.05. *Prediction:* at fixed standardised moneyness the spot-vol slope is near symmetric; a band narrower below the strike lowers the hedged seller's variance and worst day with no fall in average. *Data:* held. *Links:* [Bandi, Fusari, Renò](https://westernfinance-portal.org/viewpaper?n=915376); [Hibbert et al. 2008](https://faculty.fiu.edu/~dupoyetb/return_vola.pdf). *Rank:* a measurement and a hedge, not an edge; it trades often.

**16. After a fast one-way run, pause the hedge** (transfer 5). Short explosive runs ("drift bursts") in futures mostly reverse. *Prediction:* after a five-minute same-sign run larger than the window's one-sigma move, the forward reverses part of it on more than 60% of flags, and a 30-minute hedge pause beats the band. *Data:* held; tick data would be better. *Links:* [Christensen, Oomen, Renò](https://arxiv.org/abs/2601.08974); [Adams et al. draft](https://www.jean-sebastienfontaine.com/papers/0dte-options-volatility.pdf). *Rank:* academic, but one-minute bars blur bursts into trends, which the desk found costly.

**17. Next-day calls sold on a rule** (flows 5). Index rules fix the strike and minute of next-day call sales. *Prediction:* at 9:35 the call IV at yesterday's rule strike dips below its neighbours. *Data:* held; VIX closes free. *Links:* [S&P PP&CC methodology](https://www.spglobal.com/spdji/en/documents/methodologies/methodology-sp-500-pp-cc-index.pdf); [Roundhill XDTE prospectus](https://www.roundhillinvestments.com/assets/pdfs/xdte_prospectus.pdf). *Rank:* exact documents, but the funds sell about 440 contracts a day against 2.3 million.

**18. Retail buys the morning** (frontier 7). Retail enters early and buys calls. *Prediction:* the 9:35-to-10:30 fall in IV at fixed moneyness is larger for 10-25-delta calls than for puts. *Data:* IV held; retail flow not held. *Links:* [Cboe, May 2025](https://www.cboe.com/insights/posts/0-dt-es-decoded-positioning-trends-and-market-impact/); [Beckmeyer, Branger, Gayda](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4404704). *Rank:* Cboe finds buys and sells balanced, and the flow part needs data.

**19. Event premium set off the last event** (forums 7). Sellers hurt at the last FOMC or CPI mark the next one up. *Prediction:* event-day straddle premium over its five-day average correlates (rank above 0.3) with the previous same-type event's move; the realised move does not. *Data:* needs several years of history. *Link:* [Rhoads, reposted on Elite Trader, 30 Jan 2024](https://www.elitetrader.com/et/threads/spx-ndx-and-rut-1-day-option-history-around-fomc-annoucements.378153/). *Rank:* charts only, and about 20 events a year.

**20. Morning vol-of-vol and tomorrow** (frontier 9). VVIX at 10:00 predicts next-day variance returns. *Prediction:* after a top-quartile 10:00 smile curvature, tomorrow's whole-day straddle ratio is higher. *Data:* proxy held; VVIX not held. *Link:* [Bevilacqua and Hizmeri, FoFI 2026](https://wp.lancs.ac.uk/fofi2026/files/2026/03/FoFI-2026-091-Mattia-Bevilacqua.pdf). *Rank:* found once, on other instruments.

**21. Hedge back to the band edge** (forums 3). Trade only the delta beyond the band, not back to zero. *Prediction:* hedge trades fall by at least 30% and the saved cost exceeds the added variance's worth. *Data:* held. *Link:* [sle, Elite Trader, 2 Nov 2018](https://www.elitetrader.com/et/threads/managing-deltas-hedging-frequency.326612/). *Rank:* a method, not a mechanism; the hedging-with-costs literature was not opened by any lane.

**22. The same half-hour as yesterday** (transfer 7). Institutions split orders over days at the same clock time. *Prediction:* a window's ratio today correlates (rank at least 0.1) with the same window over the last five days, after the time-of-day pattern is removed. *Data:* held. *Link:* [Heston, Korajczyk, Sadka, JF 2010](https://ar5iv.labs.arxiv.org/html/1005.3535). *Rank:* one source, on single stocks.

**23. The end of the pattern-day-trader rule** (flows 7). From 4 June 2026 small accounts can sell before the close. *Prediction:* afternoon 10-delta IV over ATM IV falls after June 2026, against the morning. *Data:* held. *Link:* [FINRA Notice 26-10, 20 Apr 2026](https://www.finra.org/rules-guidance/notices/26-10). *Rank:* the date is primary, the mechanism is the lane's own.

**24. Band width from the day's autocorrelation** (forums 6). Narrow the band when the tape trends. *Prediction:* a band set from the trailing 60-minute variance ratio beats the fixed one-sixth band after cost. *Data:* held. *Link:* [TheBigShort in the sle thread, Nov 2018](https://www.elitetrader.com/et/threads/managing-deltas-hedging-frequency.326612/). *Rank:* the desk's own result argues against it.

**25. A dear tomorrow is too dear** (own-data 6). *Prediction:* top-quarter one-day charges realise below 0.95 pooled. *Data:* held. *Source:* desk part 4, section 5. *Rank:* noticed after the data was opened; no mechanism source.

**26. Quiet, then a break** (own-data 4). *Prediction:* trailing Gap and the unhedged seller's next return correlate less than the time of day alone gives. *Data:* held. *Source:* desk part 1, experiment 2. *Rank:* an effect of 0.04 of a rank correlation, no mechanism source.

**27. The day that has run straight** (own-data 3). *Prediction:* the straightest quarter gives the hedged seller the best return. *Data:* held. *Source:* desk part 2, section 4. *Rank:* passed on one half only and breaks even with the spread.

**28. Do not sell the week when it is cheap** (own-data 7). *Prediction:* the lowest quarter of the weekly gap gives the weekly seller a lower return. *Data:* held. *Source:* desk part 4, section 3. *Rank:* about 45 independent weeks.

## Known and taken

Each line is documented or tested on same-day or very short index options, or in the market named. Do not propose it as new.

**Volatility premium, within the day and overnight**
- 0DTE VRP positive and tiny, median about 0.0011% of spot from 10:00. Vilkov. [link](https://github.com/vilkovgr/0dte-strategies/blob/main/docs/paper/paper-annotated.md)
- 0DTE VRP larger than 1DTE; upside larger than downside for 0DTE only. Almeida, Freire, Hizmeri. [link](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4701401)
- VRP to expiry rises through the day, sharply in the last bars. Dim, Eraker, Vilkov. [link](https://westernfinance-portal.org/viewpaper?n=950096)
- No arbitrage in small moves; premium sits in large jumps. Chong and Todorov. [link](https://economics.smu.edu.sg/sites/economics.smu.edu.sg/files/economics/pdf/Seminar/2024/20241212.pdf)
- Delta-hedged SPX returns negative overnight, positive intraday. Muravyev and Ni. [link](https://www.sciencedirect.com/science/article/abs/pii/S0304405X19302193)
- Option returns lower over weekends and holidays, SPX puts included, 1996 to 2014. Jones and Shemesh (added at the merge). [link](https://faculty.marshall.usc.edu/Christopher-Jones/pdf/jones_shemesh_2018_jf.pdf)
- 10:00 SPY straddle about 13% rich. FlashAlpha [seller]. [link](https://flashalpha.com/articles/are-0dte-straddles-overpriced-193-spy-sessions-data-study)
- VIX1D rises by day and falls by night by construction. Albers and Kestner. [link](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4650419)
- One-day VRP in Europe halved by the seller's bid. Wilkens. [link](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7283819)
- Higher 0DTE share lowers one-day VRP payoff. Khalil (thesis). [link](https://research-api.cbs.dk/ws/portalfiles/portal/105671291/1775874_O._Khalil_Zero_Day_to_Expiry_Options_Trading_and_Variance_Risk_Premium.pdf)
- Variance premium sits at the shortest maturity, one month and up. Dew-Becker et al. [link](https://www.nber.org/papers/w21182)

**Time of day**
- Spreads lowest 10:00 to 14:00, so studies start at 10:00. Almeida et al. [link](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4701401)
- 15:50 to 16:00 holds the most jump variance; 0DTE prices it. Song. [link](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7412318)
- SPX option spreads peak near 10:00, rise with volatility. Cao, Jacobs, Ke. [link](https://benny.aeaweb.org/conference/2024/program/paper/DFs2GZND)
- Morning VVIX predicts next-day variance returns. Bevilacqua and Hizmeri. [link](https://wp.lancs.ac.uk/fofi2026/files/2026/03/FoFI-2026-091-Mattia-Bevilacqua.pdf)
- ATM 0DTE IV falls through the day. tastylive [seller], three days. [link](https://www.youtube.com/watch?v=JSfxso7awzc)
- Platform users' best entries about 10:15. Option Alpha [seller]. [link](https://optionalpha.com/blog/0dte-options-strategy-performance)
- Retail 0DTE timing U-shaped; retail share 30-35% by OPRA codes. OptionMetrics [seller]. [link](https://optionmetrics.com/blog/how-much-of-0-dte-is-really-retail-evidence-from-spx-and-spy-options/)

**Event days**
- FOMC event vol carries a VRP; straddles lose over the statement. Johannes, Kaeck, Seeger. [link](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4484011)
- FOMC 0DTE uncertainty builds 10:00 to 14:00; pre-FOMC drift ended 2016. Song. [link](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7412318)
- Event VRP the night before FOMC and payrolls. Wright. [link](https://www.nber.org/papers/w28306)
- CPI, FOMC, payrolls, GDP expirations dearer; most other releases not priced. Londono and Samadi. [link](https://www.federalreserve.gov/econres/ifdp/the-price-of-macroeconomic-uncertainty-evidence-from-daily-options.htm)
- FOMC and CPI days triple the condor loss. OptionKrafter [seller]. [link](https://optionkrafter.com/blog/0dte-iron-condor)

**Dealer gamma and the index**
- Market-maker 0DTE gamma mostly positive; lowers next variance. Dim, Eraker, Vilkov. [link](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4692190)
- Dampening from older positions, not same-day trades. Adams et al. [link](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5641974)
- Maximum gamma impact +3.3 points of daily vol. Amaya et al. [link](https://cdn.cboe.com/resources/education/research_publications/gammasqueezes.pdf)
- Market-maker net gamma small, flow balanced. Cboe 2023. [link](https://www.cboe.com/insights/posts/volatility-insights-evaluating-the-market-impact-of-spx-0-dte-options/)
- 0DTE volume raises volatility. Brogaard, Han, Won. [link](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4426358)
- Public-OI non-0DTE gamma predicts lower next-bar RV. Ardia and Vaudescal. [link](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7202999)
- Flow-gamma sign reverses in 2025; max-gamma strike does not attract. Singh. [link](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7350465)
- Structured-product hedging, not 0DTE, may explain low VIX in 2023. BIS. [link](https://www.bis.org/publ/qtrpdf/r_qt2403x.htm)

**Momentum and reversal within the day**
- First half-hour predicts the last, 1993 to 2013. Gao et al. [link](https://www.sciencedirect.com/science/article/abs/pii/S0304405X18301351)
- Rest-of-day predicts last 30 minutes, short-gamma hedging. Baltussen et al. [link](https://pure.eur.nl/en/publications/hedging-demand-and-market-intraday-momentum/)
- No unconditional slope 2022 to 2026; continuation on dealer-short days. FirmTape [seller]. [link](https://firmtape.com/research/is-intraday-momentum-still-alive)
- SPY breakout with trailing stops. Zarattini, Aziz, Barbon. [link](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4824172)
- Leveraged-ETF end-of-day rebalancing: present, small, shrinking. Lenkey. [link](https://www.aimspress.com/article/doi/10.3934/QFE.2024031?viewType=HTML)

**The smile and the wings**
- Edgeworth model prices 80% of 0DTEs inside the spread. Bandi, Fusari, Renò. [link](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4503344)
- ATM term structure oscillates across 0-7 day tenors. Bandi et al. 2026. [link](https://arxiv.org/abs/2603.29430)
- Put ratio spread best, condors negative. Vilkov. [link](https://github.com/vilkovgr/0dte-strategies/blob/main/docs/paper/paper-annotated.md)
- Left jump tail in weekly options predicts equity returns. Andersen, Fusari, Todorov. [link](https://pure.au.dk/ws/files/120488629/rp18_08.pdf)
- Long-dated IV "overreaction" vanishes with model-free variance. JBF 2010. [link](https://www.sciencedirect.com/science/article/abs/pii/S0378426610000920)

**Expiry, settlement and fund flows** (group added at the merge)
- Third-Friday price spike and noon reversal, 2003 to 2021. Baltussen, Terstegge, Whelan. [link](https://www.aeaweb.org/conference/2025/program/paper/N7rsBN2N)
- S&P futures pinned on expiry days, 1992 to 2009. Golez and Jackwerth. [link](https://www.sciencedirect.com/science/article/abs/pii/S0304405X12001365)
- Single-stock closes cluster at strikes. Ni, Pearson, Poteshman. [link](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=519044)
- KOSPI 200 expiry arbitrage unwinds at the closing auction. Chay and Ryu. [link](https://scholarx.skku.edu/handle/2021.sw.skku/87724)
- NIFTY expiry effects vanished after weeklies. Kiran Kumar. [link](https://exa.ai/library/publication/691txyn1nxs)
- Bitcoin option roll hour at the 8:00 settlement. Hoang and Phan. [link](https://exa.ai/library/publication/g01rfbk2m1b)
- S&P 500 daily-call income funds are small, under $1bn. Dividend Vision. [link](https://www.dividendvision.com/lists/0dte-income-etfs)
- Calendar rebalancing predicts next-day returns. Harvey et al. [link](https://www.nber.org/papers/w33554)
- Settle a backtest on the official close, not the last bar. Concretum. [link](https://concretumgroup.substack.com/p/spx-0dte-options)

**Practitioner structures, and who verified them**
- Iron condors and flies: net Sharpe −0.96 unconditional. Vilkov. [link](https://github.com/vilkovgr/0dte-strategies/blob/main/docs/paper/paper-annotated.md)
- SPY 16-delta condor loses at real fills. OptionKrafter [seller]. [link](https://optionkrafter.com/blog/0dte-iron-condor)
- 3,909 user backtests, heavily overfit. Kam. [link](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7055179)
- MEIC entry filters "not sufficiently predictive". Theta Profits [seller]. [link](https://www.thetaprofits.com/inside-a-0dte-iron-condor-strategy-built-for-smaller-drawdowns/)
- No independent source verified any profitable practitioner condor, fly or credit spread after costs. Frontier lane. [link](frontier.md)

**Retail trading and its losses**
- Retail lost $241,000 a day, 70% of it cost. Beckmeyer, Branger, Gayda. [link](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4404704)
- Retail lost $2.1bn in options, 2019 to 2021. Bryzgalova et al. [link](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4065019)
- Average retail option trade −0.9%, 0DTE −4.6%. Bogousslavsky and Muravyev. [link](https://www.lsu.edu/business/files/event-files/2025-finance-mardi-gras/retail_option_trading_v2.pdf)
- Customers sit at the best offer in OTM 0DTE. SEC DERA. [link](https://www.sec.gov/files/dera-hope-reasonable-prc-2503.pdf)

**Microstructure warnings and what stopped working**
- VPIN adds no forecast once volatility is controlled. Andersen and Bondarenko. [link](https://repec.econ.au.dk/repec/creates/rp/13/rp13_42.pdf)
- One-minute SPX option quotes are sticky inside the spread. Kaeck, van Kervel, Seeger. [link](https://exa.ai/library/publication/q3fnhcv52xp)
- Midpoint bounce can fake an IV overreaction. Muravyev appendix. [link](https://dmurav.com/Internet%20Appendix%20to%20Order%20Flow%20and%20Option%20Returns.pdf)
- Overnight drift in index futures gone since 2021. NY Fed. [link](https://libertystreeteconomics.newyorkfed.org/2026/07/the-disappearing-overnight-drift/)
- Dominance-bound trade stagnant after 2022. Almeida et al. [link](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4701401)

## Where the lanes disagree

| Question | One side | Other side |
|---|---|---|
| Who earns in the last 25 minutes | Seller: premium is paid where uncertainty resolves ([frontier](frontier.md) card 8, after [Song](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7412318)); a last-hour short strangle paid, 2018 onward ([dorietrading](https://www.elitetrader.com/et/threads/day-trading-0dte-condors.378216/page-6), screenshots unread) | Buyer: last 10-30 minutes cheap ([FSU, 2017](https://www.elitetrader.com/et/threads/underpriced-spx-options-at-expiration.314509/)); the 15:50 step under-charged ([forums](forums.md) card 5) |
| Are 10:00 releases priced | Yes: 0DTE prices "any regularly anticipated concentration" ([Song](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7412318)) | Mostly no: ISM marginal, majority not priced ([Londono and Samadi](https://www.federalreserve.gov/econres/ifdp/the-price-of-macroeconomic-uncertainty-evidence-from-daily-options.htm)) |
| Weekend decay | Too much: weekend options earn sellers money ([Jones and Shemesh](https://faculty.marshall.usc.edu/Christopher-Jones/pdf/jones_shemesh_2018_jf.pdf)); seven days over five, per OIC ([ET thread](https://www.elitetrader.com/et/threads/no-decay-over-weekends.351639/)) | Less than calendar: about 2/3 ([Moontower](https://moontower.ai/blog/weekend-theta)); Harwood, quoted in the thread: no decay, Friday discounts it |
| Does the JPM collar matter at expiry | Yes: dealers short about $1bn gamma at the put strike ([SpotGamma](https://spotgamma.com/gex-jpm-collar/)) | No: risk spread across products ([Norden](https://garynorden.com/articles/calling-bs-on-jpm-options-trade-analysis/)) |
| Which wing holds the premium | Upside ([Almeida et al.](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4701401)) | Downside ([Vilkov](https://github.com/vilkovgr/0dte-strategies/blob/main/docs/paper/paper-annotated.md)) |
| Is the same-day expiry cheap against the next | Yes ([destriero](https://www.elitetrader.com/et/threads/0dte-options-craze.376425/)) | No: 0DTE VRP larger than 1DTE ([Almeida et al.](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4701401)) |
| Term-structure slope sign | Index: upward slope pays sellers ([Johnson](https://www.travislakejohnson.com/pdfs/Johnson%20VIXTS%202017%20(JFQA).pdf)) | Single stocks: opposite ([Vasquez](https://www.cambridge.org/core/journals/journal-of-financial-and-quantitative-analysis/article/equity-volatility-term-structures-and-the-cross-section-of-option-returns/F0A40E99FD2458367DD9A56A89783D38)) |
| What a wide option spread means | Inventory, pays the provider ([Christoffersen et al.](https://ruslangoyenko.com/wp-content/uploads/2019/09/illiquidity-premia-in-the-equity-options-market.pdf), [Muravyev](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1963865)) | Warning of jumps ([Hsieh and Jarrow](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2264261)); follows volatility, not inventory ([Verousis](https://repository.essex.ac.uk/24175/1/The%20intraday%20determination%20of%20liquidity%20in%20the%20NYSE%20LIFFE%20equity%20option%20markets.pdf)) |
| Where FOMC uncertainty resolves | Statement, 71% of priced variance ([Song](https://afajof.org/management/viewp.php?n=260400)) | Press conference ([Johannes, Kaeck, Seeger](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4484011)) |
| Who is short 0DTE gamma | Market makers net short ([Beckmeyer et al.](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4404704)) | Mostly long ([Dim et al.](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4692190), [Cboe](https://www.cboe.com/insights/posts/volatility-insights-evaluating-the-market-impact-of-spx-0-dte-options/)) |
| Does 0DTE raise volatility | Yes, +9.1% ([Brogaard et al.](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4426358)) | No, −61 bp ([Adams et al.](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5641974)) |
| Retail share of SPX 0DTE | 50-60% by broker identity ([Cboe](https://www.cboe.com/insights/posts/0-dt-es-decoded-positioning-trends-and-market-impact/)) | 30-35% by OPRA codes ([OptionMetrics](https://optionmetrics.com/blog/how-much-of-0-dte-is-really-retail-evidence-from-spx-and-spy-options/)) |
| Intraday momentum today | Yes, to 2013 and 2020 ([Gao et al.](https://www.sciencedirect.com/science/article/abs/pii/S0304405X18301351), [Baltussen et al.](https://pure.eur.nl/en/publications/hedging-demand-and-market-intraday-momentum/)) | Flat 2022 to 2026 ([FirmTape](https://firmtape.com/research/is-intraday-momentum-still-alive)) |
| Fixed delta band | Works as hysteresis ([sle](https://www.elitetrader.com/et/threads/managing-deltas-hedging-frequency.326612/)) | The worst choice (TommyR, same thread) |
| Variance premium by horizon | Largest at the shortest maturity ([Dew-Becker et al.](https://www.nber.org/papers/w21182)) | Desk: pooled 1.01 inside the day, 5-13% over a day or a week ([results](../2026-10-08-feature-experiments/results.md)) |
| NIFTY expiry effects | Gone after weeklies ([Kiran Kumar](https://exa.ai/library/publication/691txyn1nxs)) | Present with multiple expiries ([Chhimwal et al.](https://ideas.repec.org/a/kap/revdev/v28y2025i3d10.1007_s11147-025-09221-8.html)) |

## What needs data the desk does not hold

| Data | Where to get it | Cards it unlocks |
|---|---|---|
| Official SPX closing values | Cboe or S&P, free | 1, 11 |
| Release calendars (ISM, JOLTS, sentiment, housing) | BLS, ISM, Census, University of Michigan, free | 2, 8 |
| Closing auction imbalances | NYSE imbalance feed, Nasdaq NOII, paid | 1 |
| JPMorgan collar strikes | Fund N-PORT filings on SEC EDGAR, free; press | 5 |
| Earlier years of SPXW minute quotes | Vendor; the desk's free window covers the last 12 months only | 1 (heavy days), 3, 4, 5, 10, 19 |
| Open interest by strike and expiry | Cboe DataShop, OptionMetrics, ThetaData, OCC | 13; pinning |
| Retail and customer flow | Cboe Open-Close data; OPRA trade conditions | 18 |
| VIX and VVIX, intraday | Cboe, paid; VIX closes free | 17, 20 |
| Month-to-date bond returns | FRED Treasury yields, free | 11 |
| E-mini futures ticks | CME or a vendor, paid | 16 |
| NIFTY minute option quotes; NSE settlement prices | NSE and vendors; settlement free | 12 |

## Reading list

Papers and primary documents first. "Length" is given where the merge saw it.

| # | Source | Author | Date | Length | What you get |
|---|---|---|---|---|---|
| 1 | [Pre-FOMC Uncertainty Accumulation](https://afajof.org/management/viewp.php?n=260400) | Yuhan Song | Sep 2026 | 86 pages (SSRN) | How same-day options price known burst times, the close included (cards 1, 2, 10) |
| 2 | [Option Mispricing around Nontrading Periods](https://faculty.marshall.usc.edu/Christopher-Jones/pdf/jones_shemesh_2018_jf.pdf) | Jones, Shemesh | Apr 2018 | 40 pages | The weekend mispricing and its causes (card 3) |
| 3 | [0DTE Trading Rules](https://github.com/vilkovgr/0dte-strategies/blob/main/docs/paper/paper-annotated.md) | Grigory Vilkov | Jan 2026 | not measured | The benchmark for every same-day structure, with code |
| 4 | [0DTE Asset Pricing](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4701401) | Almeida, Freire, Hizmeri | Jun 2025 | 89 pages | The upside premium and the wing question (card 7) |
| 5 | [The Derivative Payoff Bias](https://www.aeaweb.org/conference/2025/program/paper/N7rsBN2N) | Baltussen, Terstegge, Whelan | Sep 2024 | not measured | A forced flow with a time of reversal (card 4) |
| 6 | [The Price of Macroeconomic Uncertainty](https://www.federalreserve.gov/econres/ifdp/the-price-of-macroeconomic-uncertainty-evidence-from-daily-options.htm) | Londono, Samadi | Jun 2023 | 55 pages (SSRN) | Which releases options price, and which they do not (card 2) |
| 7 | [Do S&P 500 Options Increase Market Volatility?](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5641974) | Adams, Dim, Eraker, Fontaine, Ornthanalai, Vilkov | Jul 2026 | not measured | Where dampening comes from (cards 13, 16) |
| 8 | [Good Volatility, Bad Volatility](https://public.econ.duke.edu/~ap172/Patton_Sheppard_Realized_Semivariance_7oct11.pdf) | Patton, Sheppard | Oct 2011 | not measured | Signed semivariance and signed jumps (cards 6, 8) |
| 9 | [Do Equity and Options Markets Agree about Volatility?](https://economics.smu.edu.sg/sites/economics.smu.edu.sg/files/economics/pdf/Seminar/2024/20241212.pdf) | Chong, Todorov | 2024 | not measured | Why the median window is rich and the sum is fair |
| 10 | [Option market (in)efficiency after return jumps](https://arxiv.org/abs/1810.12200) | Kanniainen, Magris | Oct 2018 | not measured | Minute-level IV after jumps in index options (cards 6, 8) |
| 11 | [Risk Premia and the VIX Term Structure](https://www.travislakejohnson.com/pdfs/Johnson%20VIXTS%202017%20(JFQA).pdf) | Travis Johnson | 2017 | not measured | The slope as a premium signal (card 9) |
| 12 | [weekend theta](https://moontower.ai/blog/weekend-theta) | Kris Abdelmessih | Mar 2025 | 9-minute read | Day counts and "volatility time" from a market maker's side (card 3) |

## Methods for finding patterns

From [forums](forums.md). These are the methods worth the desk's time. Each comes with the objection raised against it.

**M1. Hypothesis first, then beat random entries.** Write the structural reason first, then compare the rule with many random entries of the same count and holding time. *Objection:* without a prior hypothesis, some random rules look like an edge, and every varied parameter is another test. [Elite Trader, 25 Jan 2007](https://www.elitetrader.com/et/threads/is-there-way-to-statistically-quantify-or-find-an-edge-in-a-system.85578/)

**M2. Pick from the plateau, not the peak.** Sweep a parameter and choose the middle of a broad profitable range; reject settings where neighbours fail. *Objection:* this swaps curve-fitting for selection bias, and any rule with parameters is optimised. [Elite Trader, 24 Feb 2010](https://www.elitetrader.com/et/threads/how-do-you-avoid-overfitting-or-over-optimization-in-your-backtest.192056/)

**M4. Freeze the hypothesis and never re-explain a failure.** Fix the windows before running and drop a rule that fails out of sample. *Objection:* walk-forward fitting on small windows destroyed one poster's rule that a plain split kept. [Elite Trader, 5 Jan 2020](https://www.elitetrader.com/et/threads/your-thoughts-on-walk-forward-testing-to-assess-robustness.339240/)

**M6. Correct for the number of buckets.** Count every hypothesis, use Benjamini-Hochberg, White's Reality Check, Hansen's SPA or Romano-Wolf, and require the effect in sub-periods. This fits the twelve half-hours of card 2 exactly. *Objection:* Bonferroni is too strict, and news, not the clock, drives most intraday returns. [Quant SE, Feb 2011](https://quant.stackexchange.com/questions/140/what-are-the-popular-methodologies-to-minimize-data-snooping)

**M7. Measure realised vol as the hedger earns it.** Simulate a book with fixed gamma, flatten delta at each band crossing, and convert the scalping P&L back into a volatility. *Objection:* slow, and the answer depends on the band. [Matt Amberson (ORATS), 1 Jan 2022](https://www.elitetrader.com/et/threads/calculation-of-historical-realized-volatility.363900/)

**M8. Price the window, not the trade.** Compare the distribution of index moves over the window with what the options implied at entry, before adding any exit rule. *Objection:* it ignores the path-dependent exits a trader uses. [Elite Trader, Feb 2024](https://www.elitetrader.com/et/threads/day-trading-0dte-condors.378216/page-6)

**M9. Find the market's own clock first.** Record how much model theta the market takes over nights and weekends, and read only departures from that as volatility moves. *Objection:* the error is small in vol points, and weekend variance changes over time. [Moontower, 20 Mar 2025](https://moontower.ai/blog/weekend-theta)

**M10. Fit a smooth smile and look for strikes off it, in bid-ask terms.** Fit a spline with fewer degrees of freedom than strikes, flag outliers, then convert bid and ask to vols. *Objection:* out-of-the-money candidates are usually unfillable. [Rob Carver, Elite Trader, 5 Mar 2020](https://www.elitetrader.com/et/threads/how-do-you-value-vol.341175/)

**M11. Audit the measuring stick.** Check that a "30-day regime" is not the 30-day window, compare like with like, and do not compare buckets of very different size. No objection was raised. [Elite Trader, 30 Jan 2020](https://www.elitetrader.com/et/threads/if-you-had-to-choose-between-vrp-and-trp.339940/)

Four more methods are of less use on historical data. M3 (halve or double only, hide the test set) repeats what the seen and fresh split already does. M5 (many rolling rounds) needs more than one year; its critic called a million-variant search "vibe-statistics". M12 (disprove fast with small live trades) and M13 (a pre-written stop rule and a public log) apply only to a live pilot.

| Method | On the desk's one-minute SPXW quotes |
|---|---|
| M1 random entries | Yes: compare any timed rule with random entry minutes, same count and holding time |
| M2 plateau | Yes: sweep band width or entry time, keep broad profitable ranges |
| M3 halve or double, hidden set | Yes: the seen and fresh split already hides; add later days as a third set |
| M4 freeze the hypothesis | Already the desk's practice |
| M5 rolling rounds | Partly: one year gives few rounds |
| M6 multiplicity | Yes: across the twelve half-hours and any multi-window card |
| M7 hedger's realised vol | Yes, on the minute forward with the desk's band |
| M8 price the window | Yes: the desk's frame; use it for card 1 before any exit rule |
| M9 market's clock | Yes: decay of 0DTE and 1DTE variance through the day, nights and weekends (card 3) |
| M10 smile residuals | Yes, each minute, after converting bid and ask to vols |
| M11 audit the stick | Yes: window overlaps and bucket sizes in every table |
| M12 trade small | Not on historical data |
| M13 stop rule and log | Not on historical data |

## What was checked and what was not

**Re-opened at the merge: 20 sources.** One of them (Jones and Shemesh) is new; no lane had it.

| Source | Result |
|---|---|
| Song, SSRN abstract and AFA PDF | Confirmed: 1.9 times the within-day average, R² 41-46%, the 15:50 imbalance and MOC deadline (footnote), the quote on "any regularly anticipated concentration". Added: 71% of priced FOMC event variance resolves at the statement. |
| FSU, Elite Trader | Confirmed: date 29 Oct 2017, last 10-30 minutes, stopped quoting about ten minutes before, "models broke down". His example index level was a typo (2181 for 2581), fixed in the thread. |
| Londono and Samadi, Fed page and full text in extract | Confirmed the ISM sentence. **Added a point no lane reported:** "The majority of additional releases that we examine are not priced". This weakens card 2. The AEA copy words it differently ("A small proportion ... are significantly priced"). |
| Baltussen, Terstegge, Whelan | Confirmed: 18 bp, t = 3.5, reversal "by about noon", 2003-2021, September 2024 version, charm. Added: the authors report the spike not priced into options at Thursday's close. The "roughly 10 bp" baseline is the flows lane's chart reading; the chart axis runs to about 12 bp; not re-measured. |
| JPMorgan BRO-HE brochure | Confirmed the reset dates and the collar shape. |
| SpotGamma, "GEX & JPM Collar" | Confirmed: 1 Apr 2026, 6475 put, about 32,000 contracts, 30,000-35,000 a leg, about $1bn dealer short gamma. |
| Norden | Confirmed quote and date (30 Dec 2022); he puts the trade at "around 40,000". |
| Moontower, "weekend theta" | Confirmed: 2/3 of model theta, 0.25 of a day for a night, "not free money". **Corrected:** forums glosses the warning as "weekend gaps grow when more assets trade over the weekend"; the post says only that weekend gaps are larger. |
| newwurldmn, Elite Trader | Confirmed quote and date. |
| Jones and Shemesh, JF 2018 | Opened at the merge. The weekend effect is documented in general, so card 3 is new only on the Monday SPXW expiry. |
| Patton and Sheppard | Confirmed quote, S&P 500 and 105 stocks, 1997-2008, one day to three months. |
| Kanniainen and Magris, arXiv abstract | Confirmed: minute S&P 500 index options, gradual IV moves after jumps, no abnormal returns under actual spreads. **Not confirmed:** the durations (20 minutes, "within an hour") and the 3- to 9-month maturities, which transfer took from the full text. |
| Almeida, Freire, Hizmeri | Confirmed the upside premium and the fade after daily expiries. Written 20 Jan 2024, revised 20 Jun 2025. |
| ECB box | Confirmed quote and date; author Andrzej Sowiński. It is an argument, not a test. |
| Vilkov, GitHub | Confirmed 0.0011%, net Sharpe 0.93, 0.39 and −0.20, call ratio spreads unattractive, sample. **Not confirmed:** frontier's quote "selective timing opportunities rather than ... a broad unconditional edge"; the reading tool returned a different passage. It is not used here. |
| Andersen, Bollerslev, Diebold | Confirmed quote and November 2005. |
| Baule and Wasielewski | **Corrected:** transfer gives the author as "Wasielewski, 2026". The paper is by Rainer Baule and Niklas Wasielewski, dated 15 Dec 2025, for the FoFI 2026 conference. Figures (3% to 10% and 6%) confirmed. |
| NexusFi MOC thread | Confirmed jlabtrades' points; the thread opened 7 Aug 2023. **Not confirmed:** josh's memory that the 15:50 burst began in 2020; his post was not in the part read. Forums dates it 20 Aug 2023. |

**Independence.** Frontier and flows both rest on Song for the closing and 10:00 cards. Forums cites frontier's notes in its cards 1 and 4. The own-data cards have no outside source. Agreement across these lanes is not independent evidence.

**Not re-opened.** Every source marked "Not re-opened" above, and every link in *The rest*, *Known and taken*, *Where the lanes disagree* and the methods section, stands on the lane's reading only. In particular: the claimed move of the JPMorgan collar to CME options (flows F11, unverified in its own lane), SpotGamma's count of four put-strike tests since 2020, the Strasmore auction shares, dorietrading's last-hour strangle result (screenshots unread), and the tastytrade weekend study (never read by anyone).

**Dropped.** Nothing from the Reddit list at the end of [forums](forums.md) is cited; nobody read those threads. No claim was dropped for want of support; the two quotes that could not be confirmed (Vilkov's phrase, josh's 2020 date) are not used as evidence.

**Source count.** The header's 157 is the lanes' own counts (frontier 47, flows 36, transfer 38, forums 32 threads and 3 pages) plus one source added at the merge. Several sources appear in more than one lane (Song, Cboe 2023, Adams et al., Vilkov), so the number of distinct sources is lower.
