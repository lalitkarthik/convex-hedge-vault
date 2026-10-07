> Lane youtube, 13 sources read, 2026-10-07

## Summary

- **Limit of this lane:** 13 talks read of 25 to 30 planned, five of them by one person (Euan Sinclair), and no Indian channels except one Sinclair interview hosted by an Indian broker. Where this report says "practitioners", it mostly means Sinclair.
- **Hypotheses** come from statistics on related series (vol ratios, skew, implied against realised), from mechanical facts of the market, and from papers. Speakers warn against news, stories, indicator mining and time-of-day patterns.
- **The reason comes before the test.** Sinclair and Carver both say this. An edge is either a risk premium or an inefficiency, and you must say which one.
- **The backtest confirms a theory; it does not find one.** Show the effect in its simplest form with round numbers. Voisin goes further and distrusts backtests altogether.
- **Robustness means neighbours.** The effect must hold for nearby deltas, tenors, indices and hedge frequencies. Chan and Carver choose parameters on simulated data, not on real history.
- **Going live:** start with one lots or about 5% of the account. Tweaks added after a month live replace a large sample with a tiny one. Speakers disagree on paper trading.
- **Records:** a half-hour after the close, and a comparison of live results against the expected distribution. No talk gave a count of ideas that die.
- **Notebooks:** no talk showed a research notebook. This is the weakest heading in the lane.
- **Two cautionary talks:** a seller with no verifiable results (S2), and evidence by chart-scrolling (S8).

## 1. Where hypotheses come from

Most of this heading comes from Sinclair's five talks. Each finding ends with the source number (see the appendix), the date, a timestamp link and the label.

### Sources they trust

- **Statistics on related series.** Sinclair's screen is ratios of vols across indices, VIX against VVIX, VIX against ATM vol, the SKEW index against risk-reversal skew, and curve spreads. He treats each as a mean-reverting pair. "It's not like overlaying lines on charts. it's actually doing statistics on things that are related." — S11 Sinclair, 2025-03-30, [16:00](https://youtu.be/uOY6kRco6r4?t=960), [18:00](https://youtu.be/uOY6kRco6r4?t=1080). `[named practitioner]`
- **Learn what normal looks like, then look for the break.** His example is S&P VIX above Nasdaq VIX, which happens about 2.5 to 3% of the time. "become so familiar with how things usually are that when something different happens" — S11 Sinclair, 2025-03-30, [2:00](https://youtu.be/uOY6kRco6r4?t=120). `[named practitioner]`
- **Implied against realised, matched to the strikes you trade.** VolQ (an ATM-only Nasdaq vol index) was above later realised vol 62% of the time; VIX almost 80%, because VIX includes OTM puts. Rhoads picks the index that matches his strikes. No quote recorded in the note. — S5 Rhoads, 2021-09-01, [33:22](https://youtu.be/JA3NB24odl8?t=2002). `[named practitioner]` / `[academic]`
- **Implied earnings move against the stock's own history.** Khribi compares the option-implied move with the 2-year and 10-year distribution of past earnings moves, and builds a minute-by-minute median curve of straddle IV before earnings. "earnings moves ... drawn from really statistical probability distributions" — S2 Khribi, 2026-05-04, [20:22](https://youtu.be/xd4id6xp-4s?t=1222), [11:30](https://youtu.be/xd4id6xp-4s?t=690). `[seller]` (Earnings Watcher subscription). See the caution under heading 6.
- **A mechanical fact of the market.** VIX futures converge to spot VIX into expiry. Rhoads sells only when spot is below the front future, which halves the worst move. No quote recorded in the note. — S5 Rhoads, 2021-09-01, [4:25](https://youtu.be/JA3NB24odl8?t=265). `[named practitioner]` / `[academic]`
- **Order flow as information.** At a market maker, a large directional order is treated as informed, and the model is adjusted to it. "generally means it's paper and usually paper knows what it's doing" — S1 Harding, 2022-09-26, [32:33](https://youtu.be/FtDqj4ezhmQ?t=1953). `[named practitioner]`
- **Know which kind of edge you have.** An edge is an inefficiency (a mispricing that will go) or a risk premium (pay for carrying a risk). Trade an inefficiency hard and fast; a risk premium can carry a career. "it's really important to know the difference between those" — S9 Sinclair, 2021-01-28, [10:01](https://youtu.be/WB8t4WrdR3I?t=601), [12:02](https://youtu.be/WB8t4WrdR3I?t=722). He repeats it in S13, 2020-09-25, [22:35](https://youtu.be/09miq5C88k4?t=1355). `[named practitioner]`
- **Ask who is forced to trade.** Sinclair puts a "belief factor" of 0 to 10 on top of the statistics. Stocks go up = 10, chart patterns = 0. An idea with no named forced participant scores low. "Can you give me an example of some of these people? No." — S10 Sinclair, 2026-04-25, [29:00](https://youtu.be/Rzae3gyhpwc?t=1740), [33:00](https://youtu.be/Rzae3gyhpwc?t=1980). `[named practitioner]` (also heading 6)
- **Places where everyone's assumptions fail.** After the variance premium (implied vol tends to be above the vol that follows, which pays sellers), look at Monday against Friday, weekends, overnight against day, holidays, elections, FOMC, earnings, and extreme levels of vol, correlation, vol-of-vol and skew. "These are all the sort of questions that are legitimate to ask and can be tested" — S12 Sinclair, 2023-06-07, [40:01](https://youtu.be/LAiGKUIlwSo?t=2401). `[named practitioner]`; host QuantInsti is a `[seller]` of courses.
- **Observation first, model second.** Machine learning should improve an edge already found, not find one. "You never start with a model" — S12 Sinclair, 2023-06-07, [9:00](https://youtu.be/LAiGKUIlwSo?t=540), [11:01](https://youtu.be/LAiGKUIlwSo?t=661). `[named practitioner]`; host `[seller]`
- **Papers.** Sinclair searches SSRN for "option" and "vix", then follows Google Scholar "cited by" chains from a paper he likes. He finds arXiv q-fin too black-box now. "literally once a week" — S9 Sinclair, 2021-01-28, [1:01:01](https://youtu.be/WB8t4WrdR3I?t=3661). `[named practitioner]`. An open area he names is volatility against stock fundamentals: "like five papers written on that" — [1:15:02](https://youtu.be/WB8t4WrdR3I?t=4502).
- **Theory, published research, folklore, common sense.** Carver lists these as the "tacit" sources and says ideas come first, not data. "market folklore" — S3 Carver, 2017-12-12, [7:02](https://youtu.be/-aT55uRJI8Q?t=422), [7:37](https://youtu.be/-aT55uRJI8Q?t=457). `[named practitioner]` `[general, not options]`
- **Published work you did not know about.** Chan found afterwards that Carr and López de Prado (2014) had published his idea. He does not mind. "our objective is not to get a tenure" — S4 Chan, 2018-12-18, [42:23](https://youtu.be/UD92QBqA8Eo?t=2543). `[named practitioner]` `[general, not options]`
- **Old traders.** "find someone old who's been trading way back before there were computers" — S12 Sinclair, 2023-06-07, [26:02](https://youtu.be/LAiGKUIlwSo?t=1562). `[named practitioner]`; host `[seller]`
- **Audiences and newcomers.** Rhoads takes an idea from a question: "i have never thought about using vvix ... let me write that down" — S5 Rhoads, 2021-09-01, [27:48](https://youtu.be/JA3NB24odl8?t=1668). `[named practitioner]` / `[academic]`. Sinclair says retail traders bring new ideas because "everyone in the industry's read the same books" — S11, 2025-03-30, [38:02](https://youtu.be/uOY6kRco6r4?t=2282). `[named practitioner]`
- **Another trader's indicator.** Simmen takes a paid service's "VIX light" (term structure, VIX against SPX, VVIX, 10/20-day HV) and swaps in 9-day VIX and VVIX as his own market-top signal. Quote: "VIX light". — S8 Simmen, 2021-07-28, [0:33](https://youtu.be/nGIJ42bo1tA?t=33), [21:24](https://youtu.be/nGIJ42bo1tA?t=1284). `[unknown]`. See the caution under heading 6.
- **An inherited rule set that broke.** The Rhino rules came from its author's 2013–2015 backtest. After 2016 "some branches ... were missing", so Voisin kept one "prevailing principle" and rewrote the rest. — S6 Voisin, 2021-04-20, [3:52](https://youtu.be/xixmOR-tvwE?t=232), [30:37](https://youtu.be/xixmOR-tvwE?t=1837). `[unknown]` (also heading 8)
- **Conditioning on a vol level.** Voisin sets wing size by VIX quartile. "I checked back in history and I would have probably saved a lot of money" — S6 Voisin, 2021-04-20, [1:05:05](https://youtu.be/xixmOR-tvwE?t=3905). `[unknown]`
- **Event tests for a newcomer.** Get an options database and test specific dates. "you're not going to be data mining here" — S12 Sinclair, 2023-06-07, [54:02](https://youtu.be/LAiGKUIlwSo?t=3242). `[named practitioner]`; host `[seller]` (also heading 3)
- **A realistic baseline.** A good equity anomaly moves the up-day rate from 52% to 55%. Effects decay: the US turn-of-month effect shrank from 5–6 days to about 2. The professional edge is combining "50 little effects". — S10 Sinclair, 2026-04-25, [35:01](https://youtu.be/Rzae3gyhpwc?t=2101), [36:02](https://youtu.be/Rzae3gyhpwc?t=2162), [37:00](https://youtu.be/Rzae3gyhpwc?t=2220). `[named practitioner]`
- **Short-vol and long-vol ideas come from different places.** Short-vol ideas can be found "by looking at statistics". Long-vol ideas bet on something new, so a study of past series cannot find them. — S9 Sinclair, 2021-01-28, [1:12:00](https://youtu.be/WB8t4WrdR3I?t=4320). `[named practitioner]`

### Sources they warn against

- **News and opinion.** Reading the Wall Street Journal "is not going to help you". The hard part is "being right and different from the market consensus". — S9 Sinclair, 2021-01-28, [6:00](https://youtu.be/WB8t4WrdR3I?t=360), [9:00](https://youtu.be/WB8t4WrdR3I?t=540). `[named practitioner]`
- **Stories about causes.** They describe; they do not predict. "people love stories and so they always like to put a reason on top of an observation" — S11 Sinclair, 2025-03-30, [6:03](https://youtu.be/uOY6kRco6r4?t=363). `[named practitioner]`
- **A trader's stated reasons.** Copy what a good trader does, not the explanation. "what they do is correct but the reasons they give you might just be stupid" — S9 Sinclair, 2021-01-28, [48:02](https://youtu.be/WB8t4WrdR3I?t=2882). `[named practitioner]`
- **Confusing the trade structure with the effect.** A structure changes the shape of the P&L distribution, rarely its mean. "confusing the structure of the trade with the phenomenon that's driving the edge" — S9 Sinclair, 2021-01-28, [15:00](https://youtu.be/WB8t4WrdR3I?t=900). `[named practitioner]` (also heading 2)
- **Indicator mining.** "if your strategy only works by using a 15 period sma that's not a strategy" — S13 Sinclair, 2020-09-25, [27:00](https://youtu.be/09miq5C88k4?t=1620). `[named practitioner]` (also heading 6)
- **A time-of-day edge.** The NIFTY 9:20 short straddle is a plain variance-premium trade; the danger is not knowing that. "if it only works at 9:20 and it doesn't work at 9:30 ... What you found is luck" — S10 Sinclair, 2026-04-25, [40:00](https://youtu.be/Rzae3gyhpwc?t=2400). `[named practitioner]` (also heading 6)
- **Stacked filters.** For example, selling a straddle only when the S&P is above its 200-day moving average. "it's quite likely none of them are meaningful" — S11 Sinclair, 2025-03-30, [19:00](https://youtu.be/uOY6kRco6r4?t=1140). `[named practitioner]` (also heading 6)
- **Volatility forecasting models.** Sinclair changed his mind: GARCH forecasts no longer pay. "most of that is priced in most of the time" — S11 Sinclair, 2025-03-30, [31:01](https://youtu.be/uOY6kRco6r4?t=1861). `[named practitioner]`
- **Open-interest and option-flow signals.** "an effect, but it's a minor effect"; telling buyer from seller needs order-book data. — S11 Sinclair, 2025-03-30, [58:01](https://youtu.be/uOY6kRco6r4?t=3481). `[named practitioner]`
- **Looking at a result and then changing the rule.** Carver calls this implicit fitting. "you've just made a fitting decision" — S3 Carver, 2017-12-12, [5:23](https://youtu.be/-aT55uRJI8Q?t=323). `[named practitioner]` `[general, not options]` (also heading 6)
- **Research as a trap.** Pricing VIX options consistently with SPX is "a black hole of intellectual curiosity". Four or five simple strategies at 80% beat one at 95%. — S10 Sinclair, 2026-04-25, [23:01](https://youtu.be/Rzae3gyhpwc?t=1381), [1:00:00](https://youtu.be/Rzae3gyhpwc?t=3600). `[named practitioner]` (also heading 8)

### Disagreements

**Filters on market state.** Voisin sets his wing size by VIX quartile and says history shows it would have saved money (S6). Sinclair says filters added to a simple short-vol trade are probably all meaningless (S11). Sinclair also accepts conditioning on extreme states (S12), so the line he draws is between a state with a reason and a filter found by search.

**Other people's ideas.** Simmen builds on a paid service's indicator (S8). Rhoads writes down an audience suggestion (S5). Sinclair seeks out old traders (S12) but says their reasons may be wrong (S9), and says the industry has "read the same books" (S11).

**Data first or idea first.** Carver says ideas first, never data first (S3). Sinclair says short-vol ideas can be found by looking at statistics (S9), but also that the reason must come before the test (S11, heading 2).

## 2. From idea to testable statement

- **The reason comes before the test.** Without it you will test many things and keep the one that worked. "the reason has to become before the the testing and the statistics" — S11 Sinclair, 2025-03-30, [13:02](https://youtu.be/uOY6kRco6r4?t=782). `[named practitioner]` (also heading 6)
- **State the effect in its simplest form.** Use unoptimised round numbers. His test: sell a two-month 25-delta SPY risk reversal, Reg-T margin, delta-hedge weekly, roll with two weeks left. "this is absolutely not the way you would actually trade this effect" — S9 Sinclair, 2021-01-28, [22:02](https://youtu.be/WB8t4WrdR3I?t=1322), [24:00](https://youtu.be/WB8t4WrdR3I?t=1440). `[named practitioner]` (also heading 5)
- **Separate the phenomenon from the structure.** Write down the effect first; the choice of straddle, strangle or spread is a second decision. Finding and quote under heading 1 — S9 Sinclair, 2021-01-28, [15:00](https://youtu.be/WB8t4WrdR3I?t=900), [16:00](https://youtu.be/WB8t4WrdR3I?t=960). `[named practitioner]`
- **Write the framework before the idea.** A framework answers entry, exit, stops and sizing in advance, so the rule has only one question left to answer. No quote recorded in the note. — S3 Carver, 2017-12-12, [14:13](https://youtu.be/-aT55uRJI8Q?t=853), [22:55](https://youtu.be/-aT55uRJI8Q?t=1375). `[named practitioner]` `[general, not options]`
- **Name who pays.** Sinclair's "belief factor" asks for a named participant who is forced to trade (finding under heading 1, S10 [33:00](https://youtu.be/Rzae3gyhpwc?t=1980)). "You'll never see that in the statistics" — S10 Sinclair, 2026-04-25, [34:01](https://youtu.be/Rzae3gyhpwc?t=2041). `[named practitioner]`

No talk in this lane showed a written hypothesis template or a stated "what result would kill it".

## 3. Data

- **A market maker records everything.** "not just the trades but also all the order updates all the price updates"; a "data czar" sifts it. — S1 Harding, 2022-09-26, [2:44](https://youtu.be/FtDqj4ezhmQ?t=164), [18:40](https://youtu.be/FtDqj4ezhmQ?t=1120). `[named practitioner]`
- **Test with production data.** The firm wires live market-data feeds into exchange certification environments for realistic load. No quote recorded in the note. — S1 Harding, 2022-09-26, [27:36](https://youtu.be/FtDqj4ezhmQ?t=1656). `[named practitioner]`
- **Use public data so others can replicate.** Rhoads uses only VolQ and VIX. "talk about something that you can't replicate" — S5 Rhoads, 2021-09-01, [36:09](https://youtu.be/JA3NB24odl8?t=2169). `[named practitioner]` / `[academic]`
- **A retail trader's stack.** TD Ameritrade REST APIs plus Cboe end-of-day data pegged to the 15:45 Chicago snapshot. "purchased a lot of data historical data myself and written a few back testing engines" — S8 Simmen, 2021-07-28, [13:33](https://youtu.be/nGIJ42bo1tA?t=813), [55:30](https://youtu.be/nGIJ42bo1tA?t=3330). `[unknown]` (also heading 4)
- **Snapshot time is an options data trap.** Simmen is unsure whether his backtest tool's prices are the 15:45 or the 16:00 snapshot. — S8 Simmen, 2021-07-28, [34:08](https://youtu.be/nGIJ42bo1tA?t=2048). `[unknown]` (finding under heading 5)
- **Historical option prices are costly.** Khribi uses Polygon (now Massive) under a commercial licence, and gives historical option prices only to lifetime members. No quote recorded in the note. — S2 Khribi, 2026-05-04, [52:47](https://youtu.be/xd4id6xp-4s?t=3167). `[seller]` (Earnings Watcher subscription)
- **Open interest does not show dealer positions.** The "calls short, puts long" assumption in dealer-gamma models is false; doing it properly means tracking every buy and sell. — S12 Sinclair, 2023-06-07, [58:01](https://youtu.be/LAiGKUIlwSo?t=3481). `[named practitioner]`; host `[seller]`
- **Know where the data runs out.** "we just don't have enough data to know if teeny puts are overpriced" — S9 Sinclair, 2021-01-28, [31:02](https://youtu.be/WB8t4WrdR3I?t=1862). `[named practitioner]` (finding under heading 6)

No talk in this lane covered cleaning steps, stale quotes, early exercise, corporate actions or survivorship.

## 4. Notebooks

No talk in this lane showed a research notebook, described its layout, or argued for or against notebooks. The notes record only the tools speakers use.

- **In-house code.** Sinclair uses in-house Python and R, with legacy VBA. "i don't really use anyone else's code" — S9 Sinclair, 2021-01-28, [1:03:00](https://youtu.be/WB8t4WrdR3I?t=3780). `[named practitioner]`
- **An LLM as a junior.** Sinclair uses ChatGPT "like a very smart junior trader". It writes hundreds of lines of Python for him, such as a GARCH model, which he must still debug. He says start with linear regression before machine learning. — S12 Sinclair, 2023-06-07, [49:02](https://youtu.be/LAiGKUIlwSo?t=2942), [51:05](https://youtu.be/LAiGKUIlwSo?t=3065). `[named practitioner]`; host `[seller]`
- **A public library, not a notebook.** Carver's framework is public Python (pysystemtrade). His fake-data generator is "like 20 lines of Python code". — S3 Carver, 2017-12-12, [18:34](https://youtu.be/-aT55uRJI8Q?t=1114), [38:07](https://youtu.be/-aT55uRJI8Q?t=2287). `[named practitioner]` `[general, not options]`
- **Front-ends for traders.** At a market maker, traders get Python and spreadsheet front-ends to the firm's back-end APIs to "feed parameters back into some of our curves". — S1 Harding, 2022-09-26, [19:17](https://youtu.be/FtDqj4ezhmQ?t=1157). `[named practitioner]`
- **A retail trader writes his own engines.** Simmen built his own site and backtesting engines and plans to drop OptionNet Explorer. Quote under heading 3. — S8 Simmen, 2021-07-28, [55:30](https://youtu.be/nGIJ42bo1tA?t=3330). `[unknown]`

## 5. The backtest

- **Backtest to confirm, not to find.** One realised path of an instrument priced on uncertainty "is almost overfitting right from the start". "back test to confirm a theory that you've already got" — S12 Sinclair, 2023-06-07, [35:01](https://youtu.be/LAiGKUIlwSo?t=2101), [36:00](https://youtu.be/LAiGKUIlwSo?t=2160). `[named practitioner]`; host `[seller]` (also heading 6)
- **Calendar and event questions are tests, not backtests.** Of asking whether Mondays differ from Fridays: "That's not back testing" — S12 Sinclair, 2023-06-07, [41:00](https://youtu.be/LAiGKUIlwSo?t=2460). `[named practitioner]`; host `[seller]`
- **Design before you look at performance.** Carver's steps: framework, idea, one real scenario (2008) plus common sense to shape the rule, then synthetic data with known trend lengths to choose parameters, turnover and costs. Real data is used only for a sensitivity check; the one real-data fit is the capital allocation, done out of sample. No quote recorded in the note. — S3 Carver, 2017-12-12, [14:13](https://youtu.be/-aT55uRJI8Q?t=853). `[named practitioner]` `[general, not options]` (also heading 6)
- **Screen on cost before performance.** Costs are predictable and returns are not. Carver caps costs at 13 basis points of Sharpe ratio (return per unit of risk) a year. "the second most important thing in finance is costs" — S3 Carver, 2017-12-12, [20:44](https://youtu.be/-aT55uRJI8Q?t=1244), [42:26](https://youtu.be/-aT55uRJI8Q?t=2546). `[named practitioner]` `[general, not options]`
- **Costs of adjustments.** "they're always there and they're always small", so weigh each adjustment's value against its cost. Sinclair admits he does not remember whether the backtest he showed included costs. — S9 Sinclair, 2021-01-28, [40:01](https://youtu.be/WB8t4WrdR3I?t=2401), [1:11:02](https://youtu.be/WB8t4WrdR3I?t=4262). `[named practitioner]`
- **0DTE costs.** The edge in dollars is tiny and costs relative to it are huge. "I would argue you have to be better" — S10 Sinclair, 2026-04-25, [7:02](https://youtu.be/Rzae3gyhpwc?t=422). `[named practitioner]`
- **Commissions on VIX-product options.** "commissions took a solid 10 to 15" percent of a paid service's profits that year. — S8 Simmen, 2021-07-28, [1:18:18](https://youtu.be/nGIJ42bo1tA?t=4698). `[unknown]`
- **Hedging band.** A market maker's traders set a delta band and change it intraday. "don't start hedging until you've accumulated at least five Delta". The hedger is seen as a cost centre. — S1 Harding, 2022-09-26, [33:09](https://youtu.be/FtDqj4ezhmQ?t=1989), [37:13](https://youtu.be/FtDqj4ezhmQ?t=2233). `[named practitioner]`
- **Stops.** Sinclair uses stops only as disaster hedges, triggered about once a quarter. No quote recorded in the note. — S10 Sinclair, 2026-04-25, [46:01](https://youtu.be/Rzae3gyhpwc?t=2761). `[named practitioner]`
- **Choice of structure caps the loss.** Rhoads expresses a short-VIX-future idea with a deep ITM put whose break-even stops improving. No quote recorded in the note. — S5 Rhoads, 2021-09-01, [10:34](https://youtu.be/JA3NB24odl8?t=634). `[named practitioner]` / `[academic]`
- **Decompose the position.** Voisin checks the theta of each sub-combination and drops a part that no longer contributes. No quote recorded in the note. — S6 Voisin, 2021-04-20, [22:42](https://youtu.be/xixmOR-tvwE?t=1362), [34:59](https://youtu.be/xixmOR-tvwE?t=2099). `[unknown]`
- **Liquidity and margin.** At size, Voisin uses only strikes at multiples of 50 or 100, where the open interest is. Portfolio margin gives him 1.3 to 1.5 times Reg-T gearing. No quote recorded in the note. — S6 Voisin, 2021-04-20, [1:01:15](https://youtu.be/xixmOR-tvwE?t=3675), [1:03:24](https://youtu.be/xixmOR-tvwE?t=3804). `[unknown]`
- **Click-through backtests.** People "were just clicking day day day ... plus day" in OptionVue without knowing the market of that day. Options have many dimensions, so "you will need a lot more history to have some statistical validity". — S6 Voisin, 2021-04-20, [12:14](https://youtu.be/xixmOR-tvwE?t=734). `[unknown]` (also heading 6)
- **A broker replay tool as a backtest.** Simmen uses thinkorswim ThinkBack to compare structures over one chosen week. An attendee calls it a "poor man's back test engine". — S8 Simmen, 2021-07-28, [34:08](https://youtu.be/nGIJ42bo1tA?t=2048). `[unknown]`

### Disagreements

**Is an options backtest worth anything?** Voisin: "I don't believe in rules. Same way as as I don't really believe in back tests" (S6, [12:14](https://youtu.be/xixmOR-tvwE?t=734)). Sinclair: useful only to confirm a theory you already hold (S12). Carver: run it, but choose parameters on synthetic data so the real history is not used up (S3). Rhoads and Simmen use a backtest directly as the guide to the trade (S5, S8).

**How large are costs?** Sinclair calls them "always small" for adjustments (S9), yet huge relative to edge for 0DTE (S10). Carver puts costs second only to risk and screens on them first (S3). Simmen reports 10 to 15% of profits lost to commissions (S8).

No talk in this lane discussed event-driven against vectorised backtests, or fill assumptions.

## 6. Checks against fooling yourself

- **Every look is a fit.** Carver names three kinds of fitting: explicit (the computer optimises), implicit (you look and then change something), and tacit (prior knowledge you cannot remove). Quote under heading 1. — S3 Carver, 2017-12-12, [5:23](https://youtu.be/-aT55uRJI8Q?t=323). `[named practitioner]` `[general, not options]`
- **Never drop a losing variant.** Leave it in and let the optimiser weight it to zero; removing it inflates the Sharpe ratio. No quote recorded in the note. — S3 Carver, 2017-12-12, [52:20](https://youtu.be/-aT55uRJI8Q?t=3140). `[named practitioner]` `[general, not options]`
- **Why overfitting happens.** "the number of trading signals is far fewer than the number of prices", so parameters pick out a few past trades. — S4 Chan, 2018-12-18, [1:48](https://youtu.be/UD92QBqA8Eo?t=108). `[named practitioner]` `[general, not options]`
- **More history is not a cure.** Old data can come from a different market structure, such as spreads before decimal pricing. No quote recorded in the note. — S4 Chan, 2018-12-18, [3:30](https://youtu.be/UD92QBqA8Eo?t=210). `[named practitioner]` `[general, not options]`
- **Optimise on simulated paths.** Fit a time-series model to prices, simulate 10,000 paths, choose the trading parameter on those, then test once on real out-of-sample data (data the fit never saw). "it's just not okay to fit a trading model" — S4 Chan, 2018-12-18, [26:37](https://youtu.be/UD92QBqA8Eo?t=1597). `[named practitioner]` `[general, not options]`
- **An honest negative result.** Chan's "optimal" k=0.08 lost to an arbitrary k=0 out of sample. The optimum is for the average path, not the one you live through, so it pays only across many instruments. Adding GARCH to the simulator moved the optimum to k=0. No quote recorded in the note. — S4 Chan, 2018-12-18, [37:52](https://youtu.be/UD92QBqA8Eo?t=2272), [40:43](https://youtu.be/UD92QBqA8Eo?t=2443), [43:29](https://youtu.be/UD92QBqA8Eo?t=2609). `[named practitioner]` `[general, not options]`
- **Look first.** Sinclair's first check is the equity curve by eye, "chi by eye", before any statistics. "it starts here low on the left and it ends up here high on the right" — S9 Sinclair, 2021-01-28, [26:01](https://youtu.be/WB8t4WrdR3I?t=1561). `[named practitioner]`
- **Use every risk measure and know each one's weakness.** "there's no such thing as a bad risk measurement" — S9 Sinclair, 2021-01-28, [25:02](https://youtu.be/WB8t4WrdR3I?t=1502). `[named practitioner]`
- **Robustness means neighbours.** The effect works for every risk-reversal delta, every tenor and "practically every index". Hedge frequency (daily, weekly, monthly, band) did not change the conclusion, and he would not trust the best past setting. "the more confirmation you have of an effect the more confidence you can have" — S9 Sinclair, 2021-01-28, [28:00](https://youtu.be/WB8t4WrdR3I?t=1680), [1:24:00](https://youtu.be/WB8t4WrdR3I?t=5040). `[named practitioner]`
- **Straddle but not strangle is a warning.** If it works for one and not the other, "you've probably found an idea that isn't robust". — S12 Sinclair, 2023-06-07, [36:00](https://youtu.be/LAiGKUIlwSo?t=2160). `[named practitioner]`; host `[seller]`
- **Many definitions of one phenomenon.** Check a trend idea with moving averages, momentum and breakouts. "if all of them point to the same thing then you get into the indicators" — S13 Sinclair, 2020-09-25, [28:08](https://youtu.be/09miq5C88k4?t=1688). `[named practitioner]`
- **Do not trade what you cannot measure.** "if i can't measure it i can't predict it so i'm not going to trade it" — S9 Sinclair, 2021-01-28, [31:02](https://youtu.be/WB8t4WrdR3I?t=1862). `[named practitioner]`
- **Choose trades with fast feedback.** Far-OTM condors win so often that "you're not going to be able to distinguish between luck and skill". — S9 Sinclair, 2021-01-28, [17:00](https://youtu.be/WB8t4WrdR3I?t=1020). `[named practitioner]`
- **Selection is built in.** "you're only ever going to do a trade if it's worked for a while" — S10 Sinclair, 2026-04-25, [28:00](https://youtu.be/Rzae3gyhpwc?t=1680). `[named practitioner]`
- **The statistical bar for a trader.** With a t-statistic of two (the usual academic threshold) the effect "is going to be reasonably well known at that point". Aim for "pretty sure it's true, but I can't prove it". Conditioning on extreme states throws data away; accept that. — S12 Sinclair, 2023-06-07, [42:01](https://youtu.be/LAiGKUIlwSo?t=2521). `[named practitioner]`; host `[seller]`
- **Handicap every tweak.** If the original gave a Sharpe of 2, ask about 3 from the tweaked version. "every time you're adding something to it, you're making it less robust" — S11 Sinclair, 2025-03-30, [12:00](https://youtu.be/uOY6kRco6r4?t=720). `[named practitioner]` (also heading 7)
- **Look at the worst case per entry.** Rhoads studies the maximum adverse move per entry day as much as the average P&L. "focus maybe even more on the potential losses than the potential gains" — S5 Rhoads, 2021-09-01, [8:17](https://youtu.be/JA3NB24odl8?t=497). `[named practitioner]` / `[academic]`

See also, from heading 1: the belief factor and the time-of-day red flag (S10), stacked filters (S11), indicator mining (S13). From heading 5: Carver's design steps (S3), Voisin on click-through backtests (S6), Sinclair on one realised path (S12).

### Cautionary examples

**A seller with no verifiable results (S2).** Asked "is there a way to verify the performance?", Khribi points to member results on Discord and a blog recap with "70% 65% win rate". The note records no out-of-sample or cost evidence. — S2 Khribi, 2026-05-04, [55:34](https://youtu.be/xd4id6xp-4s?t=3334). `[seller]` (Earnings Watcher subscription; coupon pitched in the talk). His screens under heading 1 are a description of a method, not evidence that it works.

**Evidence by chart-scrolling (S8).** Simmen's support for his market-top signal is a run of charts. "it's just example after example ... you should study this on your own". An audience member at once finds a counter-example (May 31) and he concedes "absolutely it can happen". There is no count of hits and misses. — S8 Simmen, 2021-07-28, [26:20](https://youtu.be/nGIJ42bo1tA?t=1580), [31:23](https://youtu.be/nGIJ42bo1tA?t=1883). `[unknown]`

### Disagreements

**How formal must the check be?** Chan and Carver use simulation and a single out-of-sample test (S4, S3). Sinclair starts with the eye and settles for "pretty sure it's true, but I can't prove it", because an effect with a t-statistic of two is already known (S9, S12).

**Is there enough history?** Voisin says options need far more history than people use (S6). Chan says older history may describe a different market (S4). Carver says even 30 flat years is not enough to throw a rule away (S3, heading 8). Sinclair says that where data runs out, do not trade (S9).

No talk in this lane mentioned walk-forward testing, multiple-testing corrections, a count of trials, pre-registration, or review by a colleague.

## 7. From a passed test to real money

- **Paper trading does not help.** Trade one lots. "Paper trading won't help you. It's not the same" — S12 Sinclair, 2023-06-07, [1:00:00](https://youtu.be/LAiGKUIlwSo?t=3600). `[named practitioner]`; host `[seller]`
- **What live trading teaches.** Execution, intraday volatility, "adverse selection and that's really hard to back test". — S11 Sinclair, 2025-03-30, [10:01](https://youtu.be/uOY6kRco6r4?t=601). `[named practitioner]`
- **Live tweaks destroy the sample.** After a month live, people add "don't trade Thursday, enter half an hour later". The result is "a trading strategy based on 20 observations that's got three free parameters", in place of a 1,000-observation backtest. — S11 Sinclair, 2025-03-30, [9:00](https://youtu.be/uOY6kRco6r4?t=540). `[named practitioner]`
- **New ideas get a small allocation.** "i'm better at exploring than exploiting", so new trades get "five percent of my account" and move to the main account if they earn confidence. — S13 Sinclair, 2020-09-25, [13:28](https://youtu.be/09miq5C88k4?t=808). `[named practitioner]` (also heading 8)
- **Low-belief ideas: trade small and watch.** A found edge is more likely zero than negative, so the downside is limited. Size it big enough to matter if right and not a disaster if wrong. No quote recorded in the note. — S10 Sinclair, 2026-04-25, [30:00](https://youtu.be/Rzae3gyhpwc?t=1800), [31:00](https://youtu.be/Rzae3gyhpwc?t=1860). `[named practitioner]`
- **Sizing.** Sinclair splits the account into a safe part (about 90%) and a risky part run at full Kelly (the bet size that maximises long-run growth). No quote recorded in the note. — S11 Sinclair, 2025-03-30, [46:01](https://youtu.be/uOY6kRco6r4?t=2761). `[named practitioner]`
- **Edge first, then "can I do this trade?"** The second question covers capital, attention and psychology. — S11 Sinclair, 2025-03-30, [55:01](https://youtu.be/uOY6kRco6r4?t=3301). `[named practitioner]`
- **Do not automate early.** "if you automate too early, you're going to be solving problems you think you're going to have". A simple VIX/SPX spread had five implementation problems, "all edge cases". Adverse selection is hard to see in data because your own orders change the market. — S10 Sinclair, 2026-04-25, [1:06:01](https://youtu.be/Rzae3gyhpwc?t=3961), [1:07:01](https://youtu.be/Rzae3gyhpwc?t=4021), [1:05:01](https://youtu.be/Rzae3gyhpwc?t=3901). `[named practitioner]`
- **Compare live results with the expected distribution.** Sinclair uses "the kolmogorov smirnoff test" (a test of whether two samples come from the same distribution). "the only way you know that is if you keep records" — S13 Sinclair, 2020-09-25, [38:32](https://youtu.be/09miq5C88k4?t=2312). `[named practitioner]`
- **Compare live against the model on a schedule.** "i trade it and then i update it and then i compare how did my trading do" against the model, about every six to twelve months. — S5 Rhoads, 2021-09-01, [5:00](https://youtu.be/JA3NB24odl8?t=300). `[named practitioner]` / `[academic]` (also heading 8). He shows a backtest paper trade beside a real trade for the same period, [25:38](https://youtu.be/JA3NB24odl8?t=1538).
- **Discipline, then an exception.** "the system is always smarter than i am", but after an outlier gain of about 700 points Rhoads now takes the trade off. That is a discretionary rule added after the backtest. — S5 Rhoads, 2021-09-01, [23:29](https://youtu.be/JA3NB24odl8?t=1409). `[named practitioner]` / `[academic]`
- **What a professional book must deliver.** 1.5 to 2% a month with a smooth weekly NAV. "you can make people happy if you can provide 15% per annum" — S6 Voisin, 2021-04-20, [32:16](https://youtu.be/xixmOR-tvwE?t=1936), [1:04:29](https://youtu.be/xixmOR-tvwE?t=3869). `[unknown]`
- **A seller's paper mode.** Earnings Watcher has a paper-trading mode and a journal where members note "this went wrong because of this". — S2 Khribi, 2026-05-04, [51:43](https://youtu.be/xd4id6xp-4s?t=3103). `[seller]` (Earnings Watcher subscription) (also heading 8)

### Disagreements

**Paper trading.** Sinclair says it does not help and one lots are the test (S12). Khribi's product offers a paper mode (S2, a seller). Rhoads shows a paper trade beside the real one as a check (S5).

**Changing the rule after going live.** Rhoads added a discretionary exit after one outlier (S5). Sinclair says exactly this kind of change swaps a large sample for a small one, and any tweak must clear a higher bar (S11).

## 8. Records and killing ideas

- **A half-hour after the close.** Sinclair writes down what each strategy made and how it filled: "this strategy made this amount of money ... my average fill quality was this". He says ideas come from that unfocused time. — S11 Sinclair, 2025-03-30, [29:01](https://youtu.be/uOY6kRco6r4?t=1741). `[named practitioner]`
- **Records at the aggregate level.** As a market maker, track the bid-ask spread captured over time. "if the amount of bid ask spread you're getting is a tenth of what it used to be" you must know it. — S13 Sinclair, 2020-09-25, [39:36](https://youtu.be/09miq5C88k4?t=2376). `[named practitioner]`
- **Cut the weight, not the rule.** Fast trend on equity indices has been flat since about 1990, which gives p≈30%. That is "nowhere near enough data to throw it away". — S3 Carver, 2017-12-12, [59:01](https://youtu.be/-aT55uRJI8Q?t=3541). `[named practitioner]` `[general, not options]`
- **Refit rarely.** The refit cadence should match the trading speed. Carver has not changed parameters since December 2014. No quote recorded in the note. — S3 Carver, 2017-12-12, [57:24](https://youtu.be/-aT55uRJI8Q?t=3444). `[named practitioner]` `[general, not options]`
- **A strategy has bad cycles.** Sinclair's last earnings cycle was "the worst ever ... in like over a decade and a half"; a couple before it was the best. — S10 Sinclair, 2026-04-25, [1:09:00](https://youtu.be/Rzae3gyhpwc?t=4140). `[named practitioner]`
- **How long an idea takes.** On improving the earnings trade: "I've been looking at that trade for 15 years and I haven't found any really great improvements". — S10 Sinclair, 2026-04-25, [1:01:00](https://youtu.be/Rzae3gyhpwc?t=3660). `[named practitioner]`
- **A trade journal, not a research journal.** Rulison's journal has a trade number that ties opening, adjustment and closing fills together, net P&L per trade, and days in trade. He admits "i've ... always dropped the ball" on keeping one. — S7 Rulison, 2023-11-15, [6:16](https://youtu.be/13gpaozVtwo?t=376), [0:35](https://youtu.be/13gpaozVtwo?t=35). `[unknown]`
- **The broker export is the hard part.** Keep raw downloads on one tab and parsed fields on another; the "crosswalk" between them is the work. Rulison logs the web sources behind ideas in Zotero. — S7 Rulison, 2023-11-15, [5:41](https://youtu.be/13gpaozVtwo?t=341), [7:58](https://youtu.be/13gpaozVtwo?t=478), [2:52](https://youtu.be/13gpaozVtwo?t=172). `[unknown]`
- **An honest non-answer on returns.** "i haven't gotten creamed" — S5 Rhoads, 2021-09-01, [38:57](https://youtu.be/JA3NB24odl8?t=2337). `[named practitioner]` / `[academic]`

See also: Voisin on a rule set that broke and was rewritten (S6, heading 1); Sinclair's 5% account for new ideas and Rhoads's six-to-twelve-month comparison (heading 7); the Earnings Watcher journal (S2, heading 7).

### Disagreement

**When to stop.** Carver keeps a rule that has been flat for 30 years at a lower weight, because the data cannot reject it (S3). Sinclair tests live results against the expected distribution and expects an inefficiency to disappear (S13, S9). Voisin kept one principle and rewrote every rule when the market changed (S6).

No talk in this lane gave a count of ideas that die, or described a log of failed ideas.

## Hypothesis sources, ranked

Counts are distinct speakers out of 9 who said anything on heading 1. Sinclair's five talks count as one speaker.

| Source of ideas | Speakers who named it | Strongest link |
|---|---|---|
| Statistics on related series: vol ratios, skew, term structure, implied against realised, implied move against history | 5 — Sinclair, Rhoads, Voisin `[unknown]`, Simmen `[unknown]`, Khribi `[seller]` | S11 [16:00](https://youtu.be/uOY6kRco6r4?t=960) |
| Other people: old traders, audiences, retail newcomers, another trader's indicator, an inherited rule set | 4 — Sinclair, Rhoads, Simmen `[unknown]`, Voisin `[unknown]` | S12 [26:02](https://youtu.be/LAiGKUIlwSo?t=1562) |
| Market structure and mechanics: who is forced to trade, convergence, informed order flow | 3 — Sinclair, Rhoads, Harding | S10 [33:00](https://youtu.be/Rzae3gyhpwc?t=1980) |
| Papers and published research | 3 — Sinclair, Carver, Chan (found his idea already published) | S9 [1:01:01](https://youtu.be/WB8t4WrdR3I?t=3661) |
| Calendar and event windows where standard assumptions fail | 2 — Sinclair, Khribi `[seller]` | S12 [40:01](https://youtu.be/LAiGKUIlwSo?t=2401) |
| Theory, folklore and common sense ("ideas first") | 1 — Carver `[general, not options]` | S3 [7:02](https://youtu.be/-aT55uRJI8Q?t=422) |
| Own trading records and unfocused time after the close | 1 — Sinclair | S11 [29:01](https://youtu.be/uOY6kRco6r4?t=1741) |
| **Warned against:** indicator and parameter mining, stacked filters | 3 — Sinclair, Carver, Chan | S13 [27:00](https://youtu.be/09miq5C88k4?t=1620) |
| **Warned against:** news, opinion, stories about causes | 1 — Sinclair | S9 [6:00](https://youtu.be/WB8t4WrdR3I?t=360) |
| **Warned against:** time-of-day patterns with no named counterparty | 1 — Sinclair | S10 [40:00](https://youtu.be/Rzae3gyhpwc?t=2400) |
| **Warned against:** backtesting options to find ideas | 2 — Sinclair, Voisin `[unknown]` | S12 [35:01](https://youtu.be/LAiGKUIlwSo?t=2101) |
| **Warned against:** volatility forecasting models; open-interest flow signals | 1 — Sinclair | S11 [31:01](https://youtu.be/uOY6kRco6r4?t=1861) |

## Ten sources worth reading in full

1. [Sinclair on the Outlier Podcast](https://www.youtube.com/watch?v=uOY6kRco6r4) (S11, 2025-03-30) — how a hypothesis is spotted, and why live tweaks destroy a backtest.
2. [Sinclair at RDU Traders](https://www.youtube.com/watch?v=WB8t4WrdR3I) (S9, 2021-01-28) — one effect demonstrated end to end: simplest form, eye check, neighbours, limits of data.
3. [Sinclair, QuantInsti webinar](https://www.youtube.com/watch?v=LAiGKUIlwSo) (S12, 2023-06-07) — "the process of trading options": observation first, backtest only to confirm. The host sells courses.
4. [Sinclair on Trading with Groww](https://www.youtube.com/watch?v=Rzae3gyhpwc) (S10, 2026-04-25) — the belief factor, the NIFTY 9:20 straddle, and why not to automate early. The only Indian context in this lane.
5. [Carver, "Designed, Not Fitted"](https://www.youtube.com/watch?v=-aT55uRJI8Q) (S3, 2017) — a full design sequence that barely touches real data. `[general, not options]`
6. [Chan, "Optimizing without Overfitting"](https://www.youtube.com/watch?v=UD92QBqA8Eo) (S4, 2018-12-18) — optimising on simulated paths, with an honest negative result. `[general, not options]`
7. [Rhoads, "Systematic Option Strategies"](https://www.youtube.com/watch?v=JA3NB24odl8) (S5, 2021-09-01) — a hypothesis from a mechanical fact, public data, live against model.
8. [Voisin, "Evolution of the Rhino"](https://www.youtube.com/watch?v=xixmOR-tvwE) (S6, 2021-04-20) — how a retail rule set breaks and is rebuilt, and the case against click-through backtests. `[unknown]`
9. [Sinclair, "Edge is in the Numbers"](https://www.youtube.com/watch?v=09miq5C88k4) (S13, 2020-09-25) — detecting a failing strategy from records; the 5% exploring account.
10. [Simmen, "Volatility Trading"](https://www.youtube.com/watch?v=nGIJ42bo1tA) (S8, 2021-07-28) — watch as the cautionary example: the audience counter-example at 31:23 shows what chart-scrolling evidence lacks. `[unknown]`

Left out: S1 Harding and S7 Rulison (both thin on research process), and S2 Khribi (a seller's product talk; read only as the other cautionary example).

## Could not open

These planned talks were never read. The notes record no link for any of them.

| Planned talk | Reason |
|---|---|
| Robert Carver at Pepperstone CodeFest | not reached before the account quota ran out |
| Lopez de Prado at QuantCon | not reached before the account quota ran out |
| Darwinex "Quant Workflow" series | not reached before the account quota ran out |
| An IMC quant research masterclass | not reached before the account quota ran out |
| Prashant Mullick on the AlgoTest channel | not reached before the account quota ran out |
| Indian NIFTY and BANKNIFTY backtesting channels | not reached before the account quota ran out |

## Appendix: source notes

Each note gives the talk, its date, a label, and the claims with timestamps. Q numbers refer to the eight headings.

### S1. Eric Harding (Blackedge Capital, SPX options market maker, technologist), RDU Traders meetup
https://www.youtube.com/watch?v=FtDqj4ezhmQ — 2022-09-26, 49:47. [named practitioner] (developer at a market maker, not a trader; says so). Read in full. Thin on research process.
- Q3 The firm records "not just the trades but also all the order updates all the price updates" from exchanges (t=2:44 https://youtu.be/FtDqj4ezhmQ?t=164); an MFE "data czar" sifts it (t=18:40 ?t=1120).
- Q4 Traders are being given Python and spreadsheet front-ends to the firm's back-end APIs to "feed parameters back into some of our curves" (t=19:17 ?t=1157).
- Q5 Hedging band: "don't start hedging until you've accumulated at least five Delta" — trader-set, changed intraday (t=33:09 ?t=1989); hedger seen as a cost centre (t=37:13 ?t=2233).
- Q1 A large directional order "generally means it's paper and usually paper knows what it's doing" — the MM adjusts its model to the information (t=32:33 ?t=1953).
- Q3 Testing: they wire production market-data feeds into exchange certification environments for realistic load (t=27:36 ?t=1656).

### S2. Amin Khribi (founder, Earnings Watcher), "Repeatable and Statistical Edges in Earnings Trading", RDU Traders
https://www.youtube.com/watch?v=xd4id6xp-4s — 2026-05-04, 1:00:16. [seller] — Earnings Watcher subscription, $50/month, $480/yr, $1,000 lifetime; coupon pitched at 44:03. Read in full.
- Q1 Screen: compare the option-implied earnings move with the stock's own historical earnings-move distribution (2-year vs 10-year average, standard deviation, "beat rate" = share of past moves bigger than implied). Long vol where the recent regime is more volatile than the long run and the implied move is below it; short vol where moves are tight and stable (t=20:22–22:01 https://youtu.be/xd4id6xp-4s?t=1222). Quote: "earnings moves ... drawn from really statistical probability distributions".
- Q1 Pre-earnings "IV rush": built a minute-by-minute median curve of ATM straddle IV across all past earnings for each stock, then compares live IV with it (t=11:30–12:34 ?t=690).
- Q7/Q8 Has a paper-trading mode and a "journal" where members note "this went wrong because of this" (t=51:43 ?t=3103).
- Q6 (red flag) Asked "is there a way to verify the performance?", answer is member results on Discord and a blog recap with "70% 65% win rate" (t=55:34 ?t=3334). No out-of-sample or cost evidence given.
- Q3 Data: Polygon (now Massive) under a commercial licence; historical option prices only for lifetime members because costly (t=52:47 ?t=3167).

### S3. Robert Carver (ex-AHL/Man), "Trading Strategies that are Designed, Not Fitted", QuantCon NYC 2017
https://www.youtube.com/watch?v=-aT55uRJI8Q — talk 2017, upload 2017-12-12, 1:00:37. [named practitioner]. [general, not options]. Read in full.
- Q1/Q6 Three kinds of fitting: explicit (computer optimises), implicit ("anytime you look at a training strategy ... and then make a decision to throw it away or change it ... you've just made a fitting decision"), tacit (prior knowledge you cannot remove) (t=5:23 https://youtu.be/-aT55uRJI8Q?t=323).
- Q1 Tacit sources of ideas: theory, previous published research, "market folklore", common sense (t=7:02 ?t=422). "Ideas first", not data first (t=7:37 ?t=457).
- Q2 Write the framework and the conditions before the idea; a framework answers most design questions (entry, exit, stops, sizing) so only one question is left for the rule (t=14:13; 22:55 ?t=853).
- Q5/Q6 Design steps: framework → idea → one real scenario (2008) plus common sense to shape the algorithm without looking at performance → fake (synthetic) data with known trend lengths to choose parameters, turnover and costs → real data only for parameter-sensitivity and a sense check → the only real-data fit is the capital allocation, done out of sample (t=14:13–15:53 ?t=853).
- Q5 Costs: "the second most important thing in finance is costs"; costs are predictable, returns are not, so screen variants on cost before performance; cap of 13 bp of Sharpe per year (t=20:44; 42:26 ?t=1244).
- Q6 Never drop a losing variant from the backtest; let the optimiser weight it to zero, otherwise the Sharpe is inflated (t=52:20 ?t=3140).
- Q8 Killing ideas: fast trend on equity indices flat since ~1990 gives p≈30%, "nowhere near enough data to throw it away" — cut weight, not the rule (t=59:01 ?t=3541). Refit cadence should match trading speed; he has not changed parameters since Dec 2014 (t=57:24 ?t=3444).
- Q4 Framework is public Python (pysystemtrade); fake-data generator is "like 20 lines of Python code" on his site (t=18:34; 38:07).

### S4. Ernest Chan (QTS Capital), "Optimizing Trading Strategies without Overfitting", QuantCon 2018
https://www.youtube.com/watch?v=UD92QBqA8Eo — upload 2018-12-18, 46:17. [named practitioner] (also sells workshops/books; not pitched here). [general, not options]. Read in full.
- Q6 Root of overfitting: "the number of trading signals is far fewer than the number of prices", so parameters cherry-pick a few past trades (t=1:48 https://youtu.be/UD92QBqA8Eo?t=108).
- Q6 More history is not a cure: old data can come from a different market structure (pre-decimalisation spreads) (t=3:30 ?t=210).
- Q6 Method: fit a time-series model to prices (many data points), simulate 10,000 paths, optimise the trading parameter on the simulated paths, then test once on real out-of-sample data (t=26:37–28:53 ?t=1597). Quote: "it's okay to fit a time series model to historical prices it's just not okay to fit a trading model".
- Q6 Honest negative result shown: the "optimal" k=0.08 lost to an arbitrary k=0 out of sample (t=37:52 ?t=2272); the optimum is for the average path, not the one path you will live through, so it only pays across many instruments (t=40:43–41:49 ?t=2443). Adding GARCH to the simulator changed the optimum to k=0 (t=43:29 ?t=2609).
- Q1 Ideas from others: found afterwards that Carr and López de Prado (2014) had published the same idea; "our objective is not to get a tenure" (t=42:23 ?t=2543).

### S5. Russell Rhoads (ex-Cboe Options Institute; Indiana Kelley School; consults for Nasdaq and exchanges), "Systematic Option Strategies", RDU Traders
https://www.youtube.com/watch?v=JA3NB24odl8 — 2021-09-01, 58:59. [named practitioner] / [academic]. Says "i'm not selling anything" (t=13:55); discloses that his early Cboe talks aimed partly at raising volume (t=5:33). Read in full.
- Q1 Hypothesis from a mechanical fact: VIX futures converge to spot VIX into expiry; he only sells when spot is below the front future, which halves the worst move (t=4:25–8:17 https://youtu.be/JA3NB24odl8?t=265).
- Q7/Q8 Live vs model: "i trade it and then i update it and then i compare how did my trading do relative to what the model says ... about every six to twelve months" (t=5:00 ?t=300).
- Q6 Looks at the maximum adverse move per entry day as much as average P&L: "focus maybe even more on the potential losses than the potential gains" (t=8:17 ?t=497).
- Q5 Expresses the short-VIX-future idea with a deep ITM put whose break-even stops improving, capping loss (t=10:34–12:15 ?t=634).
- Q7 System discipline then a stated exception: "the system is always smarter than i am" but after an outlier gain of ~700 points he now takes it off — a discretionary rule added after the backtest (t=23:29–25:07 ?t=1409). Shows a backtest paper trade next to a real trade for the same period (t=25:38 ?t=1538).
- Q3 Uses only public data (VolQ, VIX) so listeners can replicate: "the worst thing in the world is i could sit here and talk about something that you can't replicate" (t=36:09 ?t=2169).
- Q1 Screening statistic: VolQ (ATM-only Nasdaq vol index) exceeded later realised vol 62% of the time, VIX almost 80%, because VIX includes OTM puts; so he picks the index that matches the strikes he trades (t=33:22 ?t=2002).
- Q1 Ideas come from audiences: asked about VVIX for VIX strikes, "i have never thought about using vvix ... let me write that down" (t=27:48 ?t=1668).
- Q8 Honest non-answer on returns: "i haven't gotten creamed" (t=38:57 ?t=2337).

### S6. Bruno Voisin, "Evolution of the Rhino Trading Strategy", RDU Traders
https://www.youtube.com/watch?v=xixmOR-tvwE — 2021-04-20, 1:45:03. [unknown] — says he trades SPX broken-wing butterflies for a European prop firm; former mentor at Aeromir (a paid mentoring service); says "i've got nothing to sell" (t=1:14:29). Employer not verifiable from the talk. Read in full.
- Q1/Q8 How a retail strategy evolves: the original rules came from a 2013–2015 backtest by its author; after Brexit/2016 "runaway" markets "some branches [of the decision tree] were missing", so he kept one "prevailing principle" (flattish, slightly negative delta over the widest range) and rewrote the rest (t=3:52–10:00 https://youtu.be/xixmOR-tvwE?t=232; t=30:37 ?t=1837).
- Q5/Q6 Against click-through backtests: people "were just clicking day day day ... plus day" in OptionVue without knowing the market of that day; options are multi-dimensional so "you will need a lot more history to have some statistical validity" (t=12:14–13:21 ?t=734). Quote: "I don't believe in rules. Same way as as I don't really believe in back tests".
- Q1 Conditioning on a screen: wing size set by VIX quartile (above Q3 ≈19.5 wider wings, 100/75 normal, 75/50 in low vol); "I checked back in history and I would have probably saved a lot of money" (t=1:05:05–1:06:10 ?t=3905).
- Q5 Decompose the position and check each sub-combo's theta; drop a part that no longer contributes (t=22:42–24:29 ?t=1362; 34:59 ?t=2099).
- Q5 Liquidity: trading size, he only uses strikes at multiples of 50 or 100 where open interest is (t=1:01:15 ?t=3675); portfolio margin lets him gear 1.3–1.5x Reg-T (t=1:03:24 ?t=3804).
- Q7 Professional target vs retail: 1.5–2% a month, "you can make people happy if you can provide 15% per annum"; NAV must be smooth week to week (t=32:16; 1:04:29 ?t=3869).

### S7. Mike Rulison, "Trading Journals – Spreadsheets and Online", RDU Traders
https://www.youtube.com/watch?v=13gpaozVtwo — 2023-11-15, 11:33. [unknown] (retail options trader, member). Read in full. Thin.
- Q8 A trade journal, not a research journal: a trade number that ties opening, adjustment and closing fills together, net P&L per trade, days in trade (for annualised return) (t=6:16 https://youtu.be/13gpaozVtwo?t=376). Admits "i've ... always dropped the ball" on keeping one (t=0:35 ?t=35).
- Q8 The hard part is the "crosswalk" from broker export to the fields you analyse; keep raw downloads on one tab and parsed fields on another (t=5:41; 7:58 ?t=341). Uses Zotero to log the web sources behind ideas (t=2:52 ?t=172).

### S8. Ryan Simmen, "Volatility Trading", RDU Traders
https://www.youtube.com/watch?v=nGIJ42bo1tA — 2021-07-28, 1:20:07. [unknown] — retail swing trader with a full-time job; subscriber to Option Pit (a paid service, ~$100/month) whose signals he discusses. Read in full.
- Q1 Hypothesis from another trader's indicator: takes Option Pit's "VIX light" (term structure, VIX vs SPX, VVIX, 10/20-day HV) and swaps in 9-day VIX and VVIX as his own market-top signal (t=0:33–2:47 https://youtu.be/nGIJ42bo1tA?t=33; t=21:24 ?t=1284).
- Q6 (cautionary) The evidence is chart-scrolling: "it's just example after example ... you should study this on your own" (t=26:20 ?t=1580). An audience member immediately finds a counter-example (May 31) and he concedes "absolutely it can happen" (t=31:23 ?t=1883). No count of hits and misses.
- Q3/Q4 Builds his own tools: a site on TD Ameritrade REST APIs plus Cboe end-of-day data pegged to the 15:45 Chicago snapshot; has "purchased a lot of data historical data myself and written a few back testing engines" and plans to drop OptionNet Explorer (t=13:33; 55:30 ?t=3330).
- Q5 Uses thinkorswim ThinkBack, which an attendee calls a "poor man's back test engine", to compare structures over one chosen week; unsure whether its prices are the 15:45 or 16:00 snapshot (t=34:08–36:18 ?t=2048).
- Q5 Costs: on VIX-product options "commissions took a solid 10 to 15" percent of Option Pit's profits that year (t=1:18:18 ?t=4698).


### S9. Euan Sinclair (Hull Tactical Asset Management; author), talk to RDU Traders, 2021-01-28
https://www.youtube.com/watch?v=WB8t4WrdR3I — talk 2021-01-28, upload 2021-01-31, 1:30:52. [named practitioner] (writes books; none pitched; says he wants no subscribers, t=1:29:01). Read in full. The best single talk in this lane on Q1 and on how to demonstrate an effect.
- Q1 Edge is either an inefficiency or a risk premium, and you must know which: "it's really important to know the difference between those" (t=10:01 https://youtu.be/WB8t4WrdR3I?t=601). Trade an inefficiency hard and fast because it will go; a risk premium can carry a career (t=12:02 ?t=722).
- Q1 Warns against news and opinion as a hypothesis source: reading the Wall Street Journal "is not going to help you"; the hard part is "being right and different from the market consensus" (t=6:00 ?t=360). If everyone in an industry looks stupid to you, "it's much more likely that you don't understand the situation" (t=9:00 ?t=540).
- Q1/Q2 Separate the phenomenon from the structure: "confusing the structure of the trade with the phenomenon that's driving the edge" (t=15:00 ?t=900). Structures change the distribution shape, rarely the mean (t=16:00 ?t=960).
- Q2/Q5 Demonstrate an effect in the simplest possible form, unoptimised round numbers: "this is absolutely not the way you would actually trade this effect" (t=22:02 ?t=1322). His test: sell a two-month 25-delta SPY risk reversal, Reg-T margin, delta-hedge weekly, roll at two weeks left (t=24:00 ?t=1440).
- Q6 First check is the eye: "it starts here low on the left and it ends up here high on the right" — "chi by eye" before any statistics (t=26:01 ?t=1561). Use all risk measures and know each one's weakness: "there's no such thing as a bad risk measurement" (t=25:02 ?t=1502).
- Q6 Robustness = neighbours: it works for every risk-reversal delta, every tenor and "practically every index", and "the more confirmation you have of an effect the more confidence you can have" (t=28:00–29:02 ?t=1680). Hedge frequency varied (daily, weekly, monthly, band) without changing the conclusion; he would not trust "the best way to do it in the past" (t=1:24:00 ?t=5040).
- Q6 Know where data runs out: "we just don't have enough data to know if teeny puts are overpriced"; "if i can't measure it i can't predict it so i'm not going to trade it" (t=31:02–32:00 ?t=1862).
- Q6 Choose trades that give fast feedback; far-OTM condors win so often "you're not going to be able to distinguish between luck and skill" (t=17:00–18:01 ?t=1020).
- Q1 Papers are a main source of ideas: SSRN keyword search "literally once a week" for "option" and "vix", then Google Scholar "cited by" chains from a paper he likes; arXiv q-fin now too black-box (t=1:01:01–1:03:00 ?t=3661).
- Q1 Distrust a trader's stated reasons: "what they do is correct but the reasons they give you might just be stupid" (t=48:02 ?t=2882). Short-vol ideas can be found "by looking at statistics"; long-vol ideas bet on something new, so time-series study cannot find them (t=1:12:00–1:13:00 ?t=4320). Open area he names: volatility versus stock fundamentals, "like five papers written on that" (t=1:15:02 ?t=4502).
- Q5 Costs: "they're always there and they're always small", so balance each adjustment's value against its cost; pros get this wrong too (t=40:01–41:01 ?t=2401). Admits he does not remember whether the shown backtest included costs (t=1:11:02 ?t=4262).
- Q4/Q3 Tools: in-house Python and R, legacy VBA; "i don't really use anyone else's code" (t=1:03:00 ?t=3780).

### S10. Euan Sinclair, "30 Years of Options Trading: The Truth About What Actually Works", Trading with Groww
https://www.youtube.com/watch?v=Rzae3gyhpwc — upload 2026-04-25, 1:10:57. [named practitioner] (now at an ETF manager running ML timing plus option overlays, t=3:02; mentions his co-written book). Channel belongs to Groww, an Indian broker. Read in full. Indian context (NIFTY 9:20 straddle, turn of month).
- Q1/Q6 A time-of-day edge is a red flag: "if it only works at 9:20 and it doesn't work at 9:30 ... What you found is luck" (t=40:00 https://youtu.be/Rzae3gyhpwc?t=2400). The 9:20 short straddle is a plain variance-premium trade; the danger is not knowing that (t=39:02–41:01 ?t=2342).
- Q1/Q6 A "belief factor" on top of statistics, 0 to 10: stocks go up = 10, pattern charts = 0, "gold goes up on Fridays" ≈ 3 because "you look at enough things ... you're going to see something like that" (t=29:00–30:00 ?t=1740). Ask for a named participant who is forced to trade: "Can you give me an example of some of these people? No." (t=33:00 ?t=1980). "You'll never see that in the statistics" (t=34:01 ?t=2041).
- Q7 Low-belief ideas: trade them small, watch P&L and costs; a found edge is more likely zero than negative, so the downside is limited (t=30:00–31:00 ?t=1800). Sizing rule: big enough to matter if right, not a disaster if wrong (t=31:00 ?t=1860).
- Q6 You only test what has already worked: "you're only ever going to do a trade if it's worked for a while" (t=28:00 ?t=1680).
- Q1 Effects decay and change shape: turn-of-month in the US went from 5–6 days to ~2 days (t=35:01 ?t=2101). Set a realistic baseline: a good equity anomaly moves the up-day rate from 52% to 55% (t=36:02 ?t=2162). Pros' edge is combining "50 little effects", not knowing secret ones (t=37:00 ?t=2220).
- Q1/Q8 Research is a trap for traders: pricing VIX options consistently with SPX is "a black hole of intellectual curiosity" (t=23:01 ?t=1381). On improving the earnings trade: "I've been looking at that trade for 15 years and I haven't found any really great improvements" (t=1:01:00 ?t=3660). Better four or five simple strategies at 80% than one at 95% (t=1:00:00 ?t=3600).
- Q7 Do not automate early: "if you automate too early, you're going to be solving problems you think you're going to have" (t=1:06:01 ?t=3961). Execution problems such as adverse selection are hard to see in data "because your presence in the market's going to change what you see" (t=1:05:01 ?t=3901). Their simple VIX/SPX delta-one spread had five implementation problems, "all edge cases" (t=1:07:01 ?t=4021).
- Q5 0DTE: edge in dollars is tiny and costs relative to it are huge, "I would argue you have to be better" (t=7:02 ?t=422). Stops only as disaster hedges, triggered about once a quarter (t=46:01–47:02 ?t=2761).
- Q8 A strategy has bad cycles that must be lived through: last earnings cycle "the worst ever ... in like over a decade and a half", a couple before "the best ever" (t=1:09:00 ?t=4140).

### S11. Euan Sinclair on the Outlier Podcast, "How to Build Options Strategies That Work"
https://www.youtube.com/watch?v=uOY6kRco6r4 — upload 2025-03-30, 1:03:21. [named practitioner]. Promotes his book with Andrew Mack (t=0:02). Read in full. Strongest single source in this lane on how a hypothesis is spotted and why live tweaks destroy a backtest.
- Q1 Learn what normal looks like, then look for the break: "become so familiar with how things usually are that when something different happens" you notice (t=2:00 https://youtu.be/uOY6kRco6r4?t=120). Example: S&P VIX above Nasdaq VIX, which happens "about two and a half 3% of the time" (t=2:00).
- Q1 His screen is statistics on related series, not charts: ratios of vols across indices, VIX vs VVIX, VIX vs ATM vol, SKEW index vs risk-reversal skew, curve spreads; "all of these things are mean reverting trades" (t=16:00–17:01 ?t=960). "It's not like overlaying lines on charts. it's actually doing statistics on things that are related" (t=18:00 ?t=1080).
- Q1 Stories about causes are descriptive, not predictive; "people love stories and so they always like to put a reason on top of an observation" (t=6:03–7:02 ?t=363). Analyst knowledge does not make money (Jimmy Johnson example, t=7:02 ?t=422).
- Q2/Q6 The reason must come before the test: "the reason has to become before the the testing and the statistics because otherwise you'll test a whole bunch of things" (t=13:02 ?t=782).
- Q6/Q7 Live-trading tweaks: after a month live, people add "don't trade Thursday, enter half an hour later" — "a trading strategy based on 20 observations that's got three free parameters" replacing a 1,000-observation backtest (t=9:00 ?t=540). If you retest a tweak, handicap it: want Sharpe ~3 where the original gave 2, "every time you're adding something to it, you're making it less robust" (t=12:00–13:02 ?t=720).
- Q7 What live trading is good for: "execution ... intrrade volatility ... adverse selection and that's really hard to back test" (t=10:01 ?t=601).
- Q1/Q6 Engineers over-filter: selling a straddle "when the S&P is above its 200 day moving average" etc.; "it's quite likely none of them are meaningful". Better: find a second simple strategy (QQQ, IWM 0DTE) than push one from Sharpe 1 to 2 (t=19:00–20:00 ?t=1140).
- Q1 Changed belief: volatility forecasting (GARCH) no longer pays — "most of that is priced in most of the time"; look for big distortions where the model does not matter (t=31:01–33:00 ?t=1861).
- Q8 Records: a half-hour after the close writing "this strategy made this amount of money ... my average fill quality was this" (t=29:01 ?t=1741); ideas come from that unfocused time.
- Q1 Retail brings new ideas because "everyone in the industry's read the same books" (t=38:02–39:00 ?t=2282). Option-flow / OI-by-strike signals: "an effect, but it's a minor effect"; telling buyer from seller needs order-book data (t=58:01–59:00 ?t=3481).
- Q7 Start with the edge, then ask "can I do this trade?" — capital, attention, psychology (t=55:01 ?t=3301). Sizing: splits the account into a safe part (~90%) and a risky part run at full Kelly (t=46:01 ?t=2761).

### S12. Euan Sinclair, "Volatility Trading Strategies" webinar, QuantInsti
https://www.youtube.com/watch?v=LAiGKUIlwSo — upload 2023-06-07, 1:02:20. [named practitioner]; host channel [seller] — QuantInsti sells courses (an options volatility course at "75% discount" is pitched at t=44:01). Read in full. A talk about "the process of trading options" (t=2:01).
- Q1 Phenomenon first, model second: "edge comes from observation"; "You never start with a model" (t=9:00–10:01 https://youtu.be/LAiGKUIlwSo?t=540). Machine learning should improve an edge already found, not find one (t=11:01 ?t=661).
- Q1 Where to look after the variance premium: places where everyone's assumptions fail — Monday vs Friday, weekends, overnight vs day, holidays, elections, FOMC, earnings, releases; extreme levels of vol, correlation, vol-of-vol, skew (t=40:01–42:01 ?t=2401). "These are all the sort of questions that are legitimate to ask and can be tested" — "That's not back testing" (t=41:00 ?t=2460).
- Q1 Old floor traders as a source: "find someone old who's been trading way back before there were computers" (t=26:02 ?t=1562).
- Q5/Q6 Against backtesting options to find ideas: one realised path of an uncertainty-priced instrument "is almost overfitting right from the start" (t=35:01–36:00 ?t=2101). "back test to confirm a theory that you've already got" (t=36:00 ?t=2160). If it works for a straddle but not a strangle, "you've probably found an idea that isn't robust" (t=36:00–37:01 ?t=2160).
- Q6 Statistical bar for a trader: with a t-stat of two "it's going to be reasonably well known at that point"; aim for "pretty sure it's true, but I can't prove it" (t=42:01–43:01 ?t=2521). Extreme-state conditioning throws away data, accept that.
- Q1/Q3 For a newcomer: get an options database and do event tests on specific dates, "you're not going to be data mining here" (t=54:02 ?t=3242).
- Q4 Uses ChatGPT "like a very smart junior trader"; it writes "hundreds of lines of Python" for him, e.g. a GARCH model, which he must still debug (t=49:02–50:01 ?t=2942). Start with linear regression before ML (t=51:05 ?t=3065).
- Q7 "Paper trading won't help you. It's not the same" — trade one lots (t=1:00:00–1:01:01 ?t=3600).
- Q3 Dealer gamma models: the "calls short, puts long" open-interest assumption is false; doing it properly means tracking every buy and sell (t=58:01–59:02 ?t=3481).

### S13. Euan Sinclair, "Edge is in the Numbers", Futures Radio Show (Anthony Crudele)
https://www.youtube.com/watch?v=09miq5C88k4 — upload 2020-09-25, 44:01. [named practitioner]; the show is sponsored by CME and brokers (t=0:32). Read in full. Thinner; mostly psychology versus edge.
- Q1/Q6 Indicator mining fails: "you've data mined something till you found something that happened to work in the past"; "if your strategy only works by using a 15 period sma that's not a strategy" (t=27:00 https://youtu.be/09miq5C88k4?t=1620). Check the phenomenon with many definitions (moving averages, momentum, breakouts); "if all of them point to the same thing then you get into the indicators" (t=28:08 ?t=1688).
- Q7 Detecting a failing strategy: compares live results with the expected distribution using "the kolmogorov smirnoff test"; "the only way you know that is if you keep records" (t=38:32–39:03 ?t=2312).
- Q8 Records at aggregate level: as a market maker, track the bid-ask captured over time; "if the amount of bid ask spread you're getting is a tenth of what it used to be you've got to be aware of that" (t=39:36 ?t=2376).
- Q7/Q8 New ideas get a small allocation: "i'm better at exploring than exploiting", so new trades get "five percent of my account"; if they earn confidence they move to the big account (t=13:28–14:01 ?t=808).
- Q1 Two kinds of edge again (inefficiency vs risk premium), traded differently (t=22:35–24:49 ?t=1355).
