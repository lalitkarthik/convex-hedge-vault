promoted: 2026-10-23
> Lane podcasts, 28 sources read, 2026-10-07

## Summary

- The source of ideas named most often is market structure: find who is forced to trade, then test whether the price shows it. Ten guests named it.
- Ratio screens (implied against realised, skew, term structure) find candidates. They do not decide. Eifert, Abdelmessih and Curnutt each warn that a level on a screen is not a trade without a reason from flow.
- Most options guests write the reason for the edge before the test: premium or inefficiency, who pays, and why it should continue.
- Notebooks are the research tool at Jane Street, and the same people distrust a notebook as a record because cells run out of order. No guest described how a research notebook is laid out.
- "The research is what you do before you run the backtest" (Macrocephalopod). The backtest is a last check and it is always optimistic.
- The checks named most: limit the count of hypotheses, hold back markets or names, split by regime, perturb the backtest, and test in a simulation where the truth is known.
- Live trading starts small. One measure is tracked in both backtest and live, and the simulator is re-run on what was just traded.
- Most ideas die. Johnson, Sun and Meredith keep written records; Abdelmessih says the trades you passed on cannot be logged.
- Open disagreements: whether dealer positions can be known (Karsan against Curnutt), how strict to be on multiple testing (Hoffstein against the rest), simulation against one historical path, and stops.

Each finding ends with its source: episode link, guest, date, timestamp, label. Episode numbers match the appendix. "No quote" means the note recorded none.

## 1. Where hypotheses come from

### Who is forced to trade

This is the source named most often. The idea starts from a participant who must trade for a reason other than price, and the hypothesis is that the price is pushed away from fair value by that trade.

- A risk premium exists because someone must trade and nobody is the natural other side. Pemex buys puts to hedge its oil output, and the dealer must "charge enough" because that risk cannot be diversified. "There is no natural to being on the other side of the S&P going down." ([S5](https://mutinyfund.com/kris-abdelmessih/) Abdelmessih, Aug 2023, transcript p.10, `[named practitioner]`, also `[seller: moontower.ai]`)
- A premium is a flow imbalance, so it changes when the flow changes. Pension consultants' papers (2012–16) pushed call overwriting (selling calls against stock you hold) and put selling to "$800,000,000 of vega a month", until market makers were "choking on the one way supply". "Risk premium are not constant nor should you think of them as constant." ([S7](https://www.flirtingwithmodels.com/episodes/If53y6iMsVe) Eifert, 2020-07-06, 15:26–17:21, `[named practitioner]`)
- Check the flow story with the dealer, not the textbook: "if you ask a market maker, what is supply and demand in short term S and P options". ([S7](https://www.flirtingwithmodels.com/episodes/If53y6iMsVe) Eifert, 2020-07-06, 15:26–17:21, `[named practitioner]`)
- The volatility risk premium (VRP: implied volatility above the volatility later realised) shrinks toward zero late in a cycle as sellers crowd in. The Cboe condor index (CNDR) is public evidence that a premium died. No quote. ([S7](https://www.flirtingwithmodels.com/episodes/If53y6iMsVe) Eifert, 2020-07-06, 13:00–14:12 and 18:27–19:33, `[named practitioner]`)
- Implied probabilities move with flow alone. One overwriter who sells 20,000 calls moves them "and nothing changed other than a transaction". ([S7](https://www.flirtingwithmodels.com/episodes/If53y6iMsVe) Eifert, 2020-07-06, 43:24, `[named practitioner]`)
- Eifert's book is a set of "strategy sleeves", each driven by a dislocation or an end-user flow. Finding the flow is easy for someone who talks to dealers: "that's not that hard of a question to answer if you're a really active market participant". ([S19](https://www.flirtingwithmodels.com/episodes/8LFggZddP5i) Eifert, 2019-05-30, 18:11 and 20:43–21:23, `[named practitioner]`)
- From flow to a data screen: for cross-sectional trades he will "historically map a lot of data to try to understand" which data predicts the dislocation. Before trading he checks that the cheapening was not caused by realised volatility. ([S19](https://www.flirtingwithmodels.com/episodes/8LFggZddP5i) Eifert, 2019-05-30, 19:21 and 20:07, `[named practitioner]`)
- Prices show who is selling. After a spike, a front-month VIX future at 32 against spot VIX at 50 meant "everybody's selling it"; the VIX future is "the tourist instrument". ([S20](https://podscripts.co/podcasts/odd-lots/lots-more-on-how-tiktok-options-traders-got-quiet) Eifert, 2025-04-26, 20:47, `[named practitioner]`)
- As a market maker, Karsan saw trades that looked rich "relative to our surfaces" lose again and again, and that forced him to build a flow model: "regularly seeing them not be profitable". ([S2](https://mutinyfund.com/cem-karsan/) Karsan, c. Feb 2021, ~41:32, `[named practitioner]`)
- Karsan's example: 30-day skew is structurally rich because hedging volume peaks one month out. He tests it as a statistical relation between skew at two expiries. No quote. ([S2](https://mutinyfund.com/cem-karsan/) Karsan, c. Feb 2021, no timestamp, `[named practitioner]`)
- Skew in grain options comes from producers and end users, who carry different risks: "the marginal buyer or seller determines the price". ([S9](https://www.flirtingwithmodels.com/episodes/3xG50jvisGY) Krishnan, 2024-01-08, 13:51 and 35:23, `[named practitioner]`)
- To find the forced trader, "it's largely asking around": ask banks which structured products sell and who buys them, then check where listed open interest clusters. Sell-side research disappointed him, but broker chats and flows are "a rich source of ideas for concentration risk". ([S28](https://www.flirtingwithmodels.com/episodes/MeUsl8ow3Z3) Krishnan, 2022-08-08, 21:05–21:18 and 53:35–54:04, `[named practitioner]`)
- Size the forced flow against market volume. Before February 2018 Curnutt's firm showed that a 6-point VIX rise meant "about a 30,000 VIX futures or more to buy in one day", more than a day's volume. For 1987 he gauged portfolio insurance by counting newspaper mentions. ([S22](https://www.flirtingwithmodels.com/episodes/l8s5fwO9IGb) Curnutt, 2023-09-11, 42:36 and 10:35, `[named practitioner]`)
- Biases in option prices come "in derivatives markets, mostly flows": yield sellers, insurers, structured-product hedging. An edge does not move to another product. He will not run his S&P method on Russell or Nasdaq because "the biases that are present in the S and P are completely different in those products". ([S24](https://www.flirtingwithmodels.com/episodes/UOAP6wBZT0R) Anderson, 2023-08-14, 44:02 and 45:06, `[named practitioner]`, also `[seller: option-overlay accounts]`)
- Jacobson's edge "comes from the fact that I understand the market players and how dealers run their exposure", in niche currency pairs: "a big fish in a small pond". ([S27](https://www.flirtingwithmodels.com/episodes/TCrhgAEhKLB) Jacobson, 2022-08-01, 35:09, `[named practitioner]`)
- At a bank flow desk Sidial learned what clients traded and why: "Some of those guys were trading some very simple strategies". ([S15](https://www.flirtingwithmodels.com/episodes/2A6apAi6jOo) Sidial, 2020-09-08, 14:50, `[named practitioner]`)
- The other side is often weak. Bank traders with heavy flow may have no edge of their own: "when this ball gets low, I'm gonna buy it... it's a little bit naive. It's not gonna work." ([S6](https://www.flirtingwithmodels.com/episodes/EdhZsWMO5mh) Abdelmessih, 2024-07-29, 42:49, `[named practitioner]`)
- `[general, not options]` Chan's edge is that large holders cannot cut risk at the open: "a large amount of rebalancing and hedging activity, is what we are trying to piggyback on". He tested many markets and it worked only in the S&P, which he ties to S&P derivatives hedging. ([S21](https://www.flirtingwithmodels.com/episodes/oORMI7LTpcO) Chan, 2020-07-10, 15:41 and 31:39, `[named practitioner]`, also `[seller: books, courses, machine-learning service]`)
- `[general, not options]` The Jane Street example hypothesis starts from a client's flow and 13F filings (the quarterly US filing of institutional holdings). No quote on this point. ([S1](https://signalsandthreads.com/finding-signal-in-the-noise/) Cho and Minsky, 2025-03-10, 11:55–14:04, `[named practitioner]`)
- `[general, not options]` Old macro premia worked partly because data and markets were hard to reach. When access improved, the "inefficiency component" left. ([S11](https://www.flirtingwithmodels.com/episodes/4kGccf3znLs) Macrocephalopod, 2023-05-29, 7:12–8:09, `[anonymous, credible]`)

**Disagreement: can dealer positions be known?**

Karsan says yes. He takes flow from executing and prime brokers, tags each trade as dealer or customer and as hedge or not, and runs it through volatility-surface models to estimate dealer gamma, vanna, charm and volga by expiry. Market sayings such as "never short a dull market" then become testable claims: "We can measure these and measure the flows". ([S26](https://www.flirtingwithmodels.com/episodes/bPhUORxdAP5) Karsan, 2021-05-03, 14:18–14:49 and 17:38–22:29, `[named practitioner]`)

Curnutt doubts it. Of charts that show gamma by strike he asks "how do you know how they're trading it?" An overwriter may delta-hedge, and dispersion traders react in a different way. ([S22](https://www.flirtingwithmodels.com/episodes/l8s5fwO9IGb) Curnutt, 2023-09-11, 52:56–54:05, `[named practitioner]`)

Karsan himself admits one of his flow effects rests on thin evidence; see heading 6.

### Screening ratios and statistics

- Reduce an option chain to four dimensions: straddle (implied against realised), vertical (skew), strangle (tails), time spread (term structure). Then compare each against liquid benchmarks and against its own percentile: "throwing all these assets onto a cross sectional diagram". Example: XLK term structure flat against SPY's steep, put skew in a high percentile, so buy calls and sell stock instead of buying puts. ([S6](https://www.flirtingwithmodels.com/episodes/EdhZsWMO5mh) Abdelmessih, 2024-07-29, 58:27–64:26, `[named practitioner]`, and `[seller: moontower.ai]` because the steps describe his tool)
- A high implied volatility is not a reason to sell. In April 2020 he bought futures-option volatility at record levels and sold USO volatility, because USO had become "an option on a barrel of oil". The edge came from structure, not from the level. ([S6](https://www.flirtingwithmodels.com/episodes/EdhZsWMO5mh) Abdelmessih, 2024-07-29, 28:37–35:08, `[named practitioner]`)
- "VIX minus realised volatility" is the wrong screen for the VRP. VIX prices a variance swap and sits above at-the-money volatility. Only at-the-money implied against realised, or VIX squared against realised variance, are valid: "those are apples to apples comparisons". A positive VIX-minus-realised gap may still lose on at-the-money straddles. ([S7](https://www.flirtingwithmodels.com/episodes/If53y6iMsVe) Eifert, 2020-07-06, 10:21–13:00, `[named practitioner]`)
- He repeats the point five years later: "The right number to compare would be like at the money implied ball" (machine transcript, as written in the note). The size of the gap differs between the two notes: 2 to 3 points in calm markets (S7), about 3 to 10 points (S20). ([S20](https://podscripts.co/podcasts/odd-lots/lots-more-on-how-tiktok-options-traders-got-quiet) Eifert, 2025-04-26, 11:16, `[named practitioner]`)
- Warning: you "can't just look at the level of the wizzou parameter on a screen". "Wizzou" is a made-up parameter, his joke about staring at a Greek level without a flow story. ([S20](https://podscripts.co/podcasts/odd-lots/lots-more-on-how-tiktok-options-traders-got-quiet) Eifert, 2025-04-26, 18:47, `[named practitioner]`)
- Curnutt's cheap-volatility screen: "favorable realized to implied spreads, but also low implied at the same time". It is rare and short-lived. His warning on low prices: "looks mouthwateringly cheap, but you just gotta respect the fact that it got that low". ([S22](https://www.flirtingwithmodels.com/episodes/l8s5fwO9IGb) Curnutt, 2023-09-11, 73:20–73:43 and 32:22, `[named practitioner]`)
- Screen first, then explain. A statistical screen, "low price, no action, forgotten", finds candidates. Colleagues with industry contacts then keep the ones with "a potential fundamental driver". ([S9](https://www.flirtingwithmodels.com/episodes/3xG50jvisGY) Krishnan, 2024-01-08, 23:57 and 36:07–36:38, `[named practitioner]`)
- If S&P put skew looks too steep against history, there are two causes to separate: the true distribution has fatter tails, or "there's some structural pressure that's pushing up the skew". ([S28](https://www.flirtingwithmodels.com/episodes/MeUsl8ow3Z3) Krishnan, 2022-08-08, 21:56–22:46, `[named practitioner]`)
- How you measure realised volatility changes the result. Johnson keeps a dashboard of several estimators and horizons. When the short-horizon realised term structure turns backwardated, that is his "don't sell" warning. ([S14](https://www.flirtingwithmodels.com/episodes/hwaXEsvOJtR) Johnson, 2021-05-10, 21:01–21:54 and 28:36–29:51, `[unknown]`)
- The single-stock VRP is "spotty at best", and he notes that the literature has a gap there. ([S14](https://www.flirtingwithmodels.com/episodes/hwaXEsvOJtR) Johnson, 2021-05-10, 33:40, `[unknown]`)
- Sinclair sorts trades into "situational" and "model driven". Situational trades rest on "similar situations that have happened in the past"; they are noisier and more profitable. ([S12](https://www.flirtingwithmodels.com/episodes/nUbY8jKizyr) Sinclair, 2020-07-27, 22:24–24:01, `[named practitioner]`)

**Two views on screens.** Abdelmessih builds his process on a ratio screen. Eifert and Curnutt say a level alone means nothing. The two views meet in practice: Abdelmessih also says a high level is not a reason to sell, and Krishnan uses the screen only to pick what to explain.

### Watching the screen and desk experience

- Lindstrom's process for discretionary ideas: "I study the vol surface every one and a half minutes". For each kink she asks what she is missing, who is betting on what, and whether they are "expressing it wrong". ([S8](https://www.flirtingwithmodels.com/episodes/QJXQ5hBMDGp) Lindstrom, 2021-05-24, 16:41–17:36, `[named practitioner]`)
- Training at SIG worked as a school for ideas. Senior traders explained each day's trades, "why they were good, why they were bad", and there was mock trading twice a week. ([S8](https://www.flirtingwithmodels.com/episodes/QJXQ5hBMDGp) Lindstrom, 2021-05-24, 03:27, `[named practitioner]`)
- At Parallax, Abdelmessih scanned "all the markets" for volatility he already thought was cheap and bought it on days it underperformed: "So I'm working screens." ([S6](https://www.flirtingwithmodels.com/episodes/EdhZsWMO5mh) Abdelmessih, 2024-07-29, 22:07, `[named practitioner]`)
- Edge lives where data is sparse and nobody has structured it. Where you can "data hack things to death", the trade is crowded: "in areas where data is highly structured, it's going to be very competitive." He also watches where good traders stand. ([S6](https://www.flirtingwithmodels.com/episodes/EdhZsWMO5mh) Abdelmessih, 2024-07-29, 27:19–28:37, `[named practitioner]`)
- "you learn the most about markets by studying the periods when things go horribly wrong" ([S22](https://www.flirtingwithmodels.com/episodes/l8s5fwO9IGb) Curnutt, 2023-09-11, 6:51, `[named practitioner]`)

### Your own losses

- As an S&P market maker in 2007–10, Karsan put on trades with "a significant amount of edge" that lost "more times than not". An attribution analysis showed the edge leaking into skew and the distribution. That finding became his framework. ([S26](https://www.flirtingwithmodels.com/episodes/bPhUORxdAP5) Karsan, 2021-05-03, 8:48–9:27, `[named practitioner]`)
- `[general, not options]` A 35% drawdown in August 2011 started Chan's search: "So we spend the next year looking for a tail head strategy" (as written in the note). ([S21](https://www.flirtingwithmodels.com/episodes/oORMI7LTpcO) Chan, 2020-07-10, 9:30–10:02, `[named practitioner]`, also `[seller]`)
- `[general, not options]` After each loss "we come up with a lot of ideas", and each becomes a candidate feature: "Why is there this big loss? ... let's put that in, and we train the system". ([S21](https://www.flirtingwithmodels.com/episodes/oORMI7LTpcO) Chan, 2020-07-10, 34:53 and 45:24, `[named practitioner]`, also `[seller]`)

### Papers, books, forums and other people

- `[general, not options]` "I used to predominantly get my ideas from reading papers". Papers are good "when you are starting out", but they lag industry by "something like five to ten years". Later sources: new datasets, "just watching the market", thinking about your own execution and who could exploit it, and talking to other traders. ([S11](https://www.flirtingwithmodels.com/episodes/4kGccf3znLs) Macrocephalopod, 2023-05-29, 57:18–60:09, `[anonymous, credible]`)
- Look where the papers are few. Time-series volatility forecasting is "heavily picked over"; factor models for options had "eight papers". "If I was completely starting over, I'd be looking at fundamental factors using them to directly predict volatility." ([S12](https://www.flirtingwithmodels.com/episodes/nUbY8jKizyr) Sinclair, 2020-07-27, 38:48–40:33, `[named practitioner]`)
- `[general, not options]` Start from an intuitive reason, then survey the literature. Meredith warns that academics may share less than before. No quote. ([S17](https://www.flirtingwithmodels.com/episodes/LcHLCLoqRU9) Meredith, clip 2023-02-13, original 2019-06-21, 10:39–10:57, `[named practitioner]`)
- Johnson learned from Sinclair's books, hired a freelance quant to walk him through Black-Scholes "line by line", and built scenario drills. ([S14](https://www.flirtingwithmodels.com/episodes/hwaXEsvOJtR) Johnson, 2021-05-10, 17:10–18:11, `[unknown]`)
- Ten to fifteen years ago Jacobson's ideas came from the Wilmott and Nuclear Phynance forums and bank quant research notes. Banks "stopped producing those", so now "I mostly read Twitter, Medium, and I listen to podcasts". ([S27](https://www.flirtingwithmodels.com/episodes/TCrhgAEhKLB) Jacobson, 2022-08-01, 46:54–47:48, `[named practitioner]`)
- Sun says tastytrade's free content "really accelerated my learning curve". His thesis is the VRP alone, with no entry signal "by choice". ([S25](https://www.flirtingwithmodels.com/episodes/QpdJve76shu) Sun, 2022-06-27, 6:25, 12:49 and 34:01, `[unknown]`)
- Compare notes with people in other markets, "not to copy their trades, but to see what they're seeing". ([S28](https://www.flirtingwithmodels.com/episodes/MeUsl8ow3Z3) Krishnan, 2022-08-08, 22:46–23:13, `[named practitioner]`)
- `[general, not options]` Discretionary managers were useful reviewers of quant signals: "tell me what you think about it... what can go wrong". ([S13](https://www.flirtingwithmodels.com/episodes/Ur6kzQiOUD5) Korgaonkar, 2021-08-09, 27:23, `[named practitioner]`)
- Short-horizon factors often appear as a by-product of long-horizon research. No quote. ([S16](https://www.flirtingwithmodels.com/episodes/X3niO6Jnu0S) Israelov, 2023-05-22, 27:56, `[named practitioner]`)

**Views on papers differ.** Macrocephalopod: good for a beginner, but five to ten years late. Sinclair: go where few papers exist. Meredith: academics now share less. Eifert (S7, above): consultants' papers were the cause of a crowded trade.

### Product mechanics and fundamentals

- Johnson rebuilt VXX and UVXY from the prospectus in Excel and Python to find the edge. The edge then decayed in stages as others found it. No quote. ([S14](https://www.flirtingwithmodels.com/episodes/hwaXEsvOJtR) Johnson, 2021-05-10, 55:44–58:56, `[unknown]`)
- Baird looks for an "inflection point" in supply and demand, where options give a large payout if the shift becomes "a much bigger deal". ([S10](https://www.flirtingwithmodels.com/episodes/08kOEaCjRLN) Baird, 2020-07-13, 26:01, `[named practitioner]`)
- For a directional options trade, "most of the work is upstream of the option expression". The option part is "super trivial" once you have a view on the distribution. ([S5](https://mutinyfund.com/kris-abdelmessih/) Abdelmessih, Aug 2023, transcript p.8–9, `[named practitioner]`, also `[seller: moontower.ai]`)
- Options force a dated, specific thesis: "You're not just bullish. You're bullish with constraint." ([S6](https://www.flirtingwithmodels.com/episodes/EdhZsWMO5mh) Abdelmessih, 2024-07-29, 56:37, `[named practitioner]`)

### Sources they warn against

- Data mining without a cause. "People use great data sets and then data mine them... That hasn't been our approach." Start from causality and use statistics to optimise. ([S2](https://mutinyfund.com/cem-karsan/) Karsan, c. Feb 2021, no timestamp, `[named practitioner]`)
- "I couldn't have modeled or come up with these theories by just data mining". The pit experience came first, then the quantitative framework. ([S26](https://www.flirtingwithmodels.com/episodes/bPhUORxdAP5) Karsan, 2021-05-03, 9:27–10:21, `[named practitioner]`)
- The two dead ends for a retail quant: sell tails until ruin, or bleed for years while waiting. No quote. ([S15](https://www.flirtingwithmodels.com/episodes/2A6apAi6jOo) Sidial, 2020-09-08, 30:44–31:35, `[named practitioner]`)

## 2. From idea to testable statement

- `[general, not options]` Research has four stages: exploration, data collection, modelling, productionisation. "I think there are roughly four stages of research." ([S1](https://signalsandthreads.com/finding-signal-in-the-noise/) Cho and Minsky, 2025-03-10, 11:55–14:04, `[named practitioner]`)
- First sort the idea into risk premium or inefficiency: "You have to know if your edge is coming from a risk premium or a genuine inefficiency." A premium: trade with care, for ever. An inefficiency (earnings, splits, takeovers): trade large, but it may not come back. ([S12](https://www.flirtingwithmodels.com/episodes/nUbY8jKizyr) Sinclair, 2020-07-27, 19:23, `[named practitioner]`)
- Edge first, structure second: "The most important thing to do when you do a trade is look for your edge". Options traders "get that the wrong way around." ([S12](https://www.flirtingwithmodels.com/episodes/nUbY8jKizyr) Sinclair, 2020-07-27, 36:36, `[named practitioner]`)
- `[general, not options]` The question asked of every new strategy at Man AHL: "why do you think that thing is gonna work in the future?" A backtest is "a comfort blanket". ([S13](https://www.flirtingwithmodels.com/episodes/Ur6kzQiOUD5) Korgaonkar, 2021-08-09, 49:43 and 33:55, `[named practitioner]`)
- "we'll only run with it if we know or have some inkling as to why such mispricing exists." ([S9](https://www.flirtingwithmodels.com/episodes/3xG50jvisGY) Krishnan, 2024-01-08, 41:06, `[named practitioner]`)
- Three views are needed before an options trade: on the underlying, on the structure, and on the option's price. "all good options trading has to start from biases in options prices". ([S24](https://www.flirtingwithmodels.com/episodes/UOAP6wBZT0R) Anderson, 2023-08-14, 42:12–43:49, `[named practitioner]`, also `[seller]`)
- `[general, not options]` Name your edge first. There are four kinds: market access, speed, information, analytics. "do I have an edge, and what does my edge look like?" At Tudor he had none of the first three: "By the time information hit me, it had basically exhausted its power." ([S23](https://www.flirtingwithmodels.com/episodes/QTd278077Qx) Cameron, 2021-06-07, 18:20–18:57 and 20:55, `[named practitioner]`)
- `[general, not options]` A strategy is a rule set: "a series of trades that had the same entry, logic, structure, and exits". ([S23](https://www.flirtingwithmodels.com/episodes/QTd278077Qx) Cameron, 2021-06-07, 28:39, `[named practitioner]`)
- `[general, not options]` Keep the signal explainable. A strategy needs "a sensible fundamental reason"; without one you are tempted to stop it in a drawdown. Chan uses machine learning only to size trades the base rule makes (meta-labeling: a second model that predicts whether each base trade will win). ([S21](https://www.flirtingwithmodels.com/episodes/oORMI7LTpcO) Chan, 2020-07-10, 32:59 and 20:03–24:00, `[named practitioner]`, also `[seller]`)
- Judge an option trade as price against payoff probability. A tight call spread is a binary bet that shows the market's implied probability; compare it with your own estimate. No quote. ([S7](https://www.flirtingwithmodels.com/episodes/If53y6iMsVe) Eifert, 2020-07-06, 41:30–43:17, `[named practitioner]`)
- State which kind of dislocation trade it is. Some "make money on realized dynamics" and need the gap to stay open. Others pay only "when it reverts"; for those ask "where is this dislocation coming from? What flows are driving it?" A persistent flow means no trade. ([S20](https://podscripts.co/podcasts/odd-lots/lots-more-on-how-tiktok-options-traders-got-quiet) Eifert, 2025-04-26, 17:29–18:47, `[named practitioner]`)
- `[general, not options]` "always ask what's the trade?" Writing the actual trade shows why an "absurd" price is not absurd. Start from "the market is right, and I'm the one who's missing something". ([S18](https://www.flirtingwithmodels.com/episodes/hCWkkcwpYaY) Hoffstein, 2023-08-28, 23:19–24:34 and 31:38–32:33, `[named practitioner]`)
- Forecast first, then choose the product and structure that pays most if the forecast is right. Quote as written in the note: "it's always better to have an opinion and have no forecast than to not have one". ([S14](https://www.flirtingwithmodels.com/episodes/hwaXEsvOJtR) Johnson, 2021-05-10, 31:28, `[unknown]`)
- Write the edge as an expectancy equation: win rate, win size, loss size. Fix the loss size with a stop, then choose a delta whose win rate beats breakeven: "we fix the risk reward ratio and then design or enter trades that have a probability of winning higher". ([S25](https://www.flirtingwithmodels.com/episodes/QpdJve76shu) Sun, 2022-06-27, 14:38–16:53, `[unknown]`)
- Karsan builds his model in three layers: the distribution of outcomes by VIX bucket, then vanna and charm adjustments, then directional signals. No quote. ([S2](https://mutinyfund.com/cem-karsan/) Karsan, c. Feb 2021, ~23:12, `[named practitioner]`)
- `[general, not options]` Every research proposal goes on a template with a "modified information ratio": expected return or cost saving, scaled by risk, times the assets it would affect, weighed against the data cost. ([S17](https://www.flirtingwithmodels.com/episodes/LcHLCLoqRU9) Meredith, clip 2023-02-13, original 2019-06-21, 11:27–12:08, `[named practitioner]`)

Two worked examples:

- USO in April 2020. Abdelmessih wrote down three separate reasons why USO volatility should be below futures-option volatility: a put-like premium to net asset value, the roll into less volatile back months, and no bid side in the voice market. He built it "ten minutes to the open" in a spreadsheet. ([S6](https://www.flirtingwithmodels.com/episodes/EdhZsWMO5mh) Abdelmessih, 2024-07-29, 28:37–35:08, `[named practitioner]`)
- After a weekly move of two standard deviations, Sidial runs Hurst and ADF tests (two tests for mean reversion) on the series. If they pass, he sells the inflated one-week wings for the fall in volatility, hedged by long tails elsewhere in the book. No quote. ([S15](https://www.flirtingwithmodels.com/episodes/2A6apAi6jOo) Sidial, 2020-09-08, 57:31–60:35, `[named practitioner]`)

See also heading 5: Macrocephalopod on the work that comes before a backtest.

## 3. Data

- `[general, not options]` Build the first dataset by hand, so that you learn which checks matter: "you could do it all manually and you could check things very, very carefully." ([S1](https://signalsandthreads.com/finding-signal-in-the-noise/) Cho and Minsky, 2025-03-10, 15:29, `[named practitioner]`)
- Tools on the Jane Street options desk are mostly "data collection, visualization, and alerting and monitoring". A trader in one name thinks about hundreds of related instruments at once. ([S4](https://signalsandthreads.com/building-tools-for-traders/) Henry, 2025-05-28, no timestamp, `[named practitioner]`)
- A small desk can start simply. As a sole proprietor Abdelmessih hired a high-school senior who knew Java: "We'll buy some data. You make a database ... we could query charts from." Then a standard set of volatility metrics across markets, and judgement per asset. ([S6](https://www.flirtingwithmodels.com/episodes/EdhZsWMO5mh) Abdelmessih, 2024-07-29, 47:03, `[named practitioner]`)
- Options data was expensive in 2009–10 (iVolatility), so Johnson began with simulated paths in Python: "I use random data at first because option data at that time was expensive." ([S14](https://www.flirtingwithmodels.com/episodes/hwaXEsvOJtR) Johnson, 2021-05-10, 19:31–21:01, `[unknown]`)
- Do the work on raw prices yourself: "you should go get the data, get every historical price of every VIX future and do some work." His result: the VIX futures curve is mostly risk premium, not forecast. ([S7](https://www.flirtingwithmodels.com/episodes/If53y6iMsVe) Eifert, 2020-07-06, 33:50, `[named practitioner]`)
- A result that is too good points to bad data. A wing-buying backtest made money, which should not happen; the volatility series had been divided by 100 at one point. "just double check your prices every single time ... If it doesn't make sense, just dig into the data". ([S27](https://www.flirtingwithmodels.com/episodes/TCrhgAEhKLB) Jacobson, 2022-08-01, 48:07–49:15, `[named practitioner]`)
- Weight older data less. Price series from the 1980s are "not an equal comparison" to today's market. ([S15](https://www.flirtingwithmodels.com/episodes/2A6apAi6jOo) Sidial, 2020-09-08, 20:58, `[named practitioner]`)
- Natural gas has "almost real time" data (pipeline scrapes, storage, LNG loadings), "depending on the amount of money you wanna spend". ([S10](https://www.flirtingwithmodels.com/episodes/08kOEaCjRLN) Baird, 2020-07-13, 28:26, `[named practitioner]`)
- `[general, not options]` Build derived numbers yourself instead of taking vendor analytics. Check outliers and review scraped data by hand: "the least fun part of our job". ([S17](https://www.flirtingwithmodels.com/episodes/LcHLCLoqRU9) Meredith, clip 2023-02-13, original 2019-06-21, 8:51–9:49, `[named practitioner]`)
- Karsan builds dealer-positioning data from broker flow and surface models. Curnutt doubts such data. Both sides are under heading 1.

Nothing found in this lane on stale quotes, wide spreads as a data error, early exercise, corporate actions or survivorship.

## 4. Notebooks

All notebook findings come from Jane Street engineers, not from options traders. The options guests in this lane describe spreadsheets, Python scripts and dashboards.

- `[general, not options]` Half of Mazare's time is research in a Python notebook; the other half is production code in OCaml. "the first half of my time is spent using Python, and that's mostly for research purposes." ([S3](https://signalsandthreads.com/python-ocaml-and-machine-learning/) Mazare, 2020-10-07, 05:36, `[named practitioner]`)
- `[general, not options]` Notebook code is written for the data in front of you: "you actually want it to work on your data rather than on any potential data." ([S3](https://signalsandthreads.com/python-ocaml-and-machine-learning/) Mazare, 2020-10-07, no timestamp, `[named practitioner]`)
- `[general, not options]` The hidden-state problem: "it's very easy to create a notebook state and not remember how you actually reached that state". His fix is to restart and reach the conclusion again from the top. ([S3](https://signalsandthreads.com/python-ocaml-and-machine-learning/) Mazare, 2020-10-07, 47:10, `[named practitioner]`)
- `[general, not options]` What moves out of the notebook: firm services (market data, publishing values) are wrapped from OCaml into Python, so the notebook only calls library functions. Shared, heavily used functions live in the typed language. No quote. ([S3](https://signalsandthreads.com/python-ocaml-and-machine-learning/) Mazare, 2020-10-07, no timestamp, `[named practitioner]`)
- `[general, not options]` Notebooks are good for sharing and annotation and bad for production. Reproducible results matter for research too, not only for production. ([S1](https://signalsandthreads.com/finding-signal-in-the-noise/) Cho and Minsky, 2025-03-10, 34:01 and 37:08, `[named practitioner]`)
- `[general, not options]` There are two research styles: simulate the real production system, or study a simplified offline dataset and port later. Quick study tools "has bitten us". ([S1](https://signalsandthreads.com/finding-signal-in-the-noise/) Cho and Minsky, 2025-03-10, 18:54–20:03, `[named practitioner]`)
- `[general, not options]` Each researcher has a "sandbox" copy of a "gold standard" environment: "you can mess up your sandbox all you want". It is refreshed from the gold copy, and production code gets version control. ([S17](https://www.flirtingwithmodels.com/episodes/LcHLCLoqRU9) Meredith, clip 2023-02-13, original 2019-06-21, 15:51–17:36, `[named practitioner]`)
- Abdelmessih first wrote his process down "methodically ... in a flow" only when he coached a developer, who turned each step into code and a user interface. ([S6](https://www.flirtingwithmodels.com/episodes/EdhZsWMO5mh) Abdelmessih, 2024-07-29, 48:35, `[named practitioner]`, also `[seller: moontower.ai]`)

**Disagreement: for and against notebooks.** Mazare and Cho use notebooks for research every day. Minsky argues against them in two episodes. First: "Things get evaluated in just whatever damn order you click the buttons". ([S1](https://signalsandthreads.com/finding-signal-in-the-noise/) Minsky, 2025-03-10, 34:34, `[named practitioner]`, `[general, not options]`) Second, a notebook is not a trustworthy record: "no guarantees that the stuff that's in the notebook reflects what would happen if you reran". Jane Street's alternative is the expect test, a plain-text file that always reruns from top to bottom and flags any output that changed. ([S4](https://signalsandthreads.com/building-tools-for-traders/) Minsky with Henry, 2025-05-28, 01:11:35, `[named practitioner]`)

Nothing found in this lane on how a research notebook is laid out, and no public example notebook or repo.

## 5. The backtest

### What a backtest is for

- `[general, not options]` "the research is what you do before you run the backtest". First ask "is there something predictable here?" with features and linear regressions on forward returns. Then come volatility forecasts, a risk model and limits. Only then simulate. ([S11](https://www.flirtingwithmodels.com/episodes/4kGccf3znLs) Macrocephalopod, 2023-05-29, 14:51–16:39, `[anonymous, credible]`)
- `[general, not options]` A backtest has three uses: a final check; a test of each assumption (impact, fill rate, borrow, latency) by plotting profit against it; and a comparison of two variants on the same engine, where you trust the difference and not the level. No quote. ([S11](https://www.flirtingwithmodels.com/episodes/4kGccf3znLs) Macrocephalopod, 2023-05-29, 16:53–17:50, `[anonymous, credible]`)
- "There was some scenario for any option strategy, even the silliest one, that pays out pretty nicely". So Krishnan frames structure choice as a decision tree by regime: put, put spread or put butterfly, and when. ([S28](https://www.flirtingwithmodels.com/episodes/MeUsl8ow3Z3) Krishnan, 2022-08-08, 57:25–57:57, `[named practitioner]`)

### Fills, costs and hedging

- "I just factor in normal, bad, and horrific entry and exit points". When a long-convexity trade is in profit, assume wider spreads. Live example: the model says exit at 20 vol and you exit at 15 "because market is 10 vol wide". ([S27](https://www.flirtingwithmodels.com/episodes/TCrhgAEhKLB) Jacobson, 2022-08-01, 49:15–49:50 and 50:59, `[named practitioner]`)
- Stops slip. "With slippage, your loss might become more like 2.2 or 2.3" against a 2.0 stop. In COVID the worst stop fills were 3.3 to 3.4 times the credit. Fixed costs (wings, commissions, slippage) rule out smaller underlyings. ([S25](https://www.flirtingwithmodels.com/episodes/QpdJve76shu) Sun, 2022-06-27, 20:45, 24:11 and 40:11, `[unknown]`)
- Funding is a hidden cost. A 600 basis point gap between borrow and lend rates makes a bought call carry a much higher implied volatility than it shows. No quote on this point. ([S6](https://www.flirtingwithmodels.com/episodes/EdhZsWMO5mh) Abdelmessih, 2024-07-29, 51:43–55:06, `[named practitioner]`)
- The backtest assumes "one swing at the plate per cycle", rolled a few weeks before expiry. Live fills need patience with limit orders. ([S9](https://www.flirtingwithmodels.com/episodes/3xG50jvisGY) Krishnan, 2024-01-08, 38:37, `[named practitioner]`)
- As Karsan's model improved, he shortened the rebalance interval; a better model "allows us to pay a little bit more slippage... to capture more edge". ([S2](https://mutinyfund.com/cem-karsan/) Karsan, c. Feb 2021, no timestamp, `[named practitioner]`)
- `[general, not options]` A square-root impact model with slow decay can be gamed inside a simulation: "what seems to empirically fit the best... cannot be correct". Start crude on impact and fills; you "end up needing to model these things very accurately" as you scale. ([S11](https://www.flirtingwithmodels.com/episodes/4kGccf3znLs) Macrocephalopod, 2023-05-29, 53:14–53:49 and 55:05, `[anonymous, credible]`)
- Building a large exposure across many strikes is "an experimentation process to some extent". ([S19](https://www.flirtingwithmodels.com/episodes/8LFggZddP5i) Eifert, 2019-05-30, 24:20, `[named practitioner]`)
- A delta-hedged VRP position still carries some market beta, from the correlation of spot and volatility. Neutralise it. No quote. ([S16](https://www.flirtingwithmodels.com/episodes/X3niO6Jnu0S) Israelov, 2023-05-22, 47:30–47:44, `[named practitioner]`)
- Sidial uses a backtested "delta optimization point" for staggered short-tenor sales, and aims his sizing at Kelly (the bet size that gives the highest long-run growth). ([S15](https://www.flirtingwithmodels.com/episodes/2A6apAi6jOo) Sidial, 2020-09-08, 47:37 and 40:20, `[named practitioner]`)

### Options-specific traps

- Do not rank option structures by backtest profit when they carry "embedded deltas". A 50/20 call spread that wins in a soybean rally shows the rally, not the structure. ([S9](https://www.flirtingwithmodels.com/episodes/3xG50jvisGY) Krishnan, 2024-01-08, 41:06, `[named practitioner]`)
- Academic short-volatility returns are quoted on premium, not on margin, and that misleads: "you have to be very careful when you look at academic studies, particularly on the short vol side." He normalises trades by constant vega. ([S12](https://www.flirtingwithmodels.com/episodes/nUbY8jKizyr) Sinclair, 2020-07-27, 44:44 and 45:47, `[named practitioner]`)
- For short options, a Sharpe ratio based on volatility misleads. Size with stress tests of the prime-broker kind (equity down 20%, implied volatility shocked). No quote. ([S16](https://www.flirtingwithmodels.com/episodes/X3niO6Jnu0S) Israelov, 2023-05-22, 52:39–53:05, `[named practitioner]`)
- Stress, not notional. Take each major risk factor "to a very extreme level that you've never seen historically", then test the hidden assumptions of the stress framework itself. A put spread has twice the gross notional of a naked put and less risk. ([S19](https://www.flirtingwithmodels.com/episodes/8LFggZddP5i) Eifert, 2019-05-30, 51:33, 56:46 and 55:25, `[named practitioner]`)
- Test a structure by shocking it. A client's 1-by-2 put spread was sold as a hedge: "Let's shock prices down ... by x and vol up by x". It was not a hedge. ([S22](https://www.flirtingwithmodels.com/episodes/l8s5fwO9IGb) Curnutt, 2023-09-11, 67:03, `[named practitioner]`)
- Hindsight in long-volatility tests. A COVID chart makes the day to sell look obvious, but "when you're standing in the middle of it, those monetization decisions are very, very hard". ([S24](https://www.flirtingwithmodels.com/episodes/UOAP6wBZT0R) Anderson, 2023-08-14, 52:23–52:37, `[named practitioner]`, also `[seller]`)
- Path dependence. Collars rolled on a calendar carry exposure that depends on expiry timing; a hedged-equity fund may hold only 40 to 80% delta. No quote. ([S24](https://www.flirtingwithmodels.com/episodes/UOAP6wBZT0R) Anderson, 2023-08-14, 16:20–17:27, `[named practitioner]`, also `[seller]`)
- Delta-hedged replication fails at events. Black-Scholes assumes continuous trading and slow news: "you're gonna be rethinking everything that you know at 01:59 on Fed announcement day". ([S24](https://www.flirtingwithmodels.com/episodes/UOAP6wBZT0R) Anderson, 2023-08-14, 59:40–60:43, `[named practitioner]`, also `[seller]`)
- To take profit on long options: mix tenors and strikes, take some profit, then be "increasingly patient". Work stops only on long-dated options, which reprice slowly. ([S28](https://www.flirtingwithmodels.com/episodes/MeUsl8ow3Z3) Krishnan, 2022-08-08, 34:39–35:46, `[named practitioner]`)
- `[general, not options]` Jensen's inequality: averaging signals before a convex step (ranks, caps) gives a different result from averaging after it. No quote. ([S18](https://www.flirtingwithmodels.com/episodes/hCWkkcwpYaY) Hoffstein, 2023-08-28, 27:09–29:36, `[named practitioner]`)

Nothing found in this lane on event-driven against vectorised engines by name, or on margin beyond Sinclair's point.

## 6. Checks against fooling yourself

### Count and limit the hypotheses

- `[general, not options]` With little data, keep more of it in-sample but limit how many hypotheses you test: "be very careful about the number of hypotheses that you test". Many people testing similar ideas on one holdout also leaks; the fix is "not duplicating hypotheses across groups". ([S1](https://signalsandthreads.com/finding-signal-in-the-noise/) Cho and Minsky, 2025-03-10, 38:51 and about 40:30, `[named practitioner]`)
- `[general, not options]` Chan left machine learning for ten years because 1990s models gave excellent backtests and no profit. "It's okay to generate false positives for your boss because you get paid a salary anyway." ([S21](https://www.flirtingwithmodels.com/episodes/oORMI7LTpcO) Chan, 2020-07-10, 6:07, `[named practitioner]`, also `[seller]`)

**Disagreement: how strict to be.** Hoffstein argues the two errors are not equal. A false positive costs noise minus trading costs; a false negative costs the whole alpha. So "it may actually be prudent to reduce the statistical requirements". ([S18](https://www.flirtingwithmodels.com/episodes/hCWkkcwpYaY) Hoffstein, 2023-08-28, 24:59–25:42, `[named practitioner]`, `[general, not options]`) Cho, Minsky and Chan, above, take the strict side.

### Holdouts and review by a colleague

- `[general, not options]` At Man AHL every idea gets two peer reviewers, one from another unit, then a held-back out-of-sample set with pass criteria agreed in advance. "We always put two researchers to kind of peer review test the idea." ([S13](https://www.flirtingwithmodels.com/episodes/Ur6kzQiOUD5) Korgaonkar, 2021-08-09, 12:30–13:35, `[named practitioner]`)
- `[general, not options]` Review uses in-sample data only. The researcher then tests the original and the modified version on the untouched set. Reviewer suggestions added 0.9 Sharpe in one credit case. No quote. ([S13](https://www.flirtingwithmodels.com/episodes/Ur6kzQiOUD5) Korgaonkar, 2021-08-09, 31:59–32:54, `[named practitioner]`)
- A backtest counts only if it is "well specified ... not burning all the data, at least withholding other markets". Then check that the theme holds across all grains or all softs. ([S9](https://www.flirtingwithmodels.com/episodes/3xG50jvisGY) Krishnan, 2024-01-08, 41:06, `[named practitioner]`)
- `[general, not options]` Split the universe: research on half the names and check the other half. "does this still hold in the other half of the universe?" A market with few assets gives no such check, and "it becomes much easier to fool yourself". ([S11](https://www.flirtingwithmodels.com/episodes/4kGccf3znLs) Macrocephalopod, 2023-05-29, 12:33 and 13:13, `[anonymous, credible]`)
- `[general, not options]` "Your backtest is always gonna be optimistic". Errors "almost always ... go against you". ([S11](https://www.flirtingwithmodels.com/episodes/4kGccf3znLs) Macrocephalopod, 2023-05-29, 16:04–16:53, `[anonymous, credible]`)
- `[general, not options]` Cameron is "uncomfortable trading on any untested assumptions or heuristics". Machine learning is "not necessarily the edge"; it improves an edge you already have. ([S23](https://www.flirtingwithmodels.com/episodes/QTd278077Qx) Cameron, 2021-06-07, 58:17 and 42:09, `[named practitioner]`)

### Split by regime

- The backtest is "a guide", not "the holy grail". Split the sample by VIX level (low, medium, high, very high) and test each strategy per regime and per underlying: "I like to break down VIX into different regimes." ([S15](https://www.flirtingwithmodels.com/episodes/2A6apAi6jOo) Sidial, 2020-09-08, 28:29–29:27, `[named practitioner]`)
- Measure correlations in stress windows, not calm ones: "I wanna see how the correlation's acting when everything is hitting the fan". ([S15](https://www.flirtingwithmodels.com/episodes/2A6apAi6jOo) Sidial, 2020-09-08, 54:29, `[named practitioner]`)
- After the model, traders add a "confidence interval" from experience. ([S15](https://www.flirtingwithmodels.com/episodes/2A6apAi6jOo) Sidial, 2020-09-08, 28:29 and 32:23, `[named practitioner]`)
- Curnutt sorts S&P returns into realised-volatility buckets: "I just bucketed periods when realized vol is below 10". He calls the result a fact about the same period, not a forecast. ([S22](https://www.flirtingwithmodels.com/episodes/l8s5fwO9IGb) Curnutt, 2023-09-11, 50:11–51:17, `[named practitioner]`)

### Perturb the backtest

- `[general, not options]` "A backtest is just a single draw of a stochastic process". Vary the parameters, entry and exit timing and slippage. Remove random parts of the universe and random periods. Add look-ahead on purpose to find the upper bound. ([S18](https://www.flirtingwithmodels.com/episodes/hCWkkcwpYaY) Hoffstein, 2023-08-28, 29:36 and 30:36–31:38, `[named practitioner]`)
- `[general, not options]` Timing luck. The result of the 10-month moving-average paper depended on the rebalance day. Across every possible day, short-run results spread widely and long-run returns could not be told apart. No quote. ([S18](https://www.flirtingwithmodels.com/episodes/hCWkkcwpYaY) Hoffstein, 2023-08-28, 7:45–9:07, `[named practitioner]`)
- `[general, not options]` Run the counterfactual. A factor-timing paper's result sat in the top percentiles of a distribution of random baskets. "So did a naive equally weighted portfolio". ([S18](https://www.flirtingwithmodels.com/episodes/hCWkkcwpYaY) Hoffstein, 2023-08-28, 17:12–18:16, `[named practitioner]`)
- `[general, not options]` Cross-validate hyperparameters and keep the search light: "we don't over hyper optimize". Feature-importance rankings changed with each random seed until averaged over about 100 seeds. ([S21](https://www.flirtingwithmodels.com/episodes/oORMI7LTpcO) Chan, 2020-07-10, 46:50 and 39:15–41:20, `[named practitioner]`, also `[seller]`)

### Simulation against one historical path

Johnson and Israelov both say history is one path, and both test in simulation. They differ in how.

- Johnson started with simulation alone, on Monte Carlo paths with set drift and volatility, and looked at the median and the worst case. "when you backtest with actual data, that's only one path." ([S14](https://www.flirtingwithmodels.com/episodes/hwaXEsvOJtR) Johnson, 2021-05-10, 21:01, `[unknown]`)
- Israelov tests each question twice: on real data, then in a simulation where the answer is known. In "Pathetic Protection" he used S&P put data first, then simulated prices (geometric Brownian motion) with option prices that carry no VRP, to separate the cost of puts from their benefit. ([S16](https://www.flirtingwithmodels.com/episodes/X3niO6Jnu0S) Israelov, 2023-05-22, 42:16–43:27, `[named practitioner]`)
- Why simulate: "because you know the truth", and "history gives us one path. And it's easy to over index on that single path". ([S16](https://www.flirtingwithmodels.com/episodes/X3niO6Jnu0S) Israelov, 2023-05-22, 58:30–58:54, `[named practitioner]`)

The other side works from history. Eifert says "go get the data" and do the work on every historical price (S7, heading 3). Krishnan and Macrocephalopod rely on held-back markets or names (above). Hoffstein agrees a backtest is one draw, but he perturbs the historical backtest. The notes record no guest who argues against simulation outright.

### History that does not know the world

- A model on history alone misses structure. Japan's positive skew in 2013 looked rare, but "it was really a sucker's trap to look at SKU and look at a historical dataset". In February 2018 such a model would have sold VIX calls that were cheap, given how exchange-traded products had to rebalance. ([S19](https://www.flirtingwithmodels.com/episodes/8LFggZddP5i) Eifert, 2019-05-30, 27:37 and 29:21–30:18, `[named practitioner]`)
- Backtests ignore crowding. Pension programmes rely on backtests of 25 to 30 years and ignore "equilibrium effects on risk premium". Ask "how much larger is positioning in that than ... twenty years ago in their back test". ([S19](https://www.flirtingwithmodels.com/episodes/8LFggZddP5i) Eifert, 2019-05-30, 37:36 and 53:00–53:57, `[named practitioner]`)
- A machine-learning trap: minimising model variance across chunks of data makes a model learn "be long" for 2010–21. Train on weighted down periods or add constraints. ([S28](https://www.flirtingwithmodels.com/episodes/MeUsl8ow3Z3) Krishnan, 2022-08-08, 60:22–61:07, `[named practitioner]`)
- Karsan agrees that his quarterly-expiry and passive-flow effect rests on "only a few data points. It's more of a hunch" (the host's words). ([S2](https://mutinyfund.com/cem-karsan/) Karsan with Buck, c. Feb 2021, no timestamp, `[named practitioner]`)

### Skewed payoffs hide the truth

- A skewed payoff hides the mean. With an iron condor, "You see the mode, and the mode is unbelievably good." ([S12](https://www.flirtingwithmodels.com/episodes/nUbY8jKizyr) Sinclair, 2020-07-27, 35:15, `[named practitioner]`)
- Sinclair selects trades with a generalised Sharpe ratio (it includes skew and kurtosis) and Kelly, not with expected value. No quote. ([S12](https://www.flirtingwithmodels.com/episodes/nUbY8jKizyr) Sinclair, 2020-07-27, 49:07–50:01, `[named practitioner]`)
- Sell nearer the money (30 to 35 delta or more) to get feedback on whether the volatility forecast has edge: "I can just be fooled by the fact that I'm so far away". He used a Kelly spreadsheet to choose strikes and profit-taking. ([S14](https://www.flirtingwithmodels.com/episodes/hwaXEsvOJtR) Johnson, 2021-05-10, 41:27 and 39:46–40:22, `[unknown]`)
- `[general, not options]` Judge the idea and the trade separately, on a 2-by-2 of good or bad prediction against good or bad trade: "sometimes you can be right and lose money, and sometimes you can be wrong and make money". ([S23](https://www.flirtingwithmodels.com/episodes/QTd278077Qx) Cameron, 2021-06-07, 49:30–52:38, `[named practitioner]`)
- Test a hunch against the records. FOMC days felt like losers, so "I finally pulled out our back test log and our live trade log". The win rate was a little lower, not enough to skip those days. ([S25](https://www.flirtingwithmodels.com/episodes/QpdJve76shu) Sun, 2022-06-27, 38:08–38:56, `[unknown]`)

Nothing found in this lane on walk-forward testing or pre-registration by name. Korgaonkar's "criteria agreed in advance" is the nearest.

## 7. From a passed test to real money

### Compare live results with the backtest

- `[general, not options]` Every day or week, re-run the simulator over what you just traded and explain every gap: "how well does my backtest match reality?" He calls this step "underappreciated". ([S11](https://www.flirtingwithmodels.com/episodes/4kGccf3znLs) Macrocephalopod, 2023-05-29, 17:50, `[anonymous, credible]`)
- `[general, not options]` Crude cost assumptions are survivable while you are small. On scale-up, "your simulation will be saying, great ... in your live book, you're just losing money hand over fist". Larger size is the only source of the data that fixes the model. ([S11](https://www.flirtingwithmodels.com/episodes/4kGccf3znLs) Macrocephalopod, 2023-05-29, 55:05–56:18, `[anonymous, credible]`)
- Use one yardstick in backtest and live. Sun's is "premium capture rate", net profit over premium sold: "as I'm live training or forward testing, it lets you gauge, am I above or below my typical expectancy". ([S25](https://www.flirtingwithmodels.com/episodes/QpdJve76shu) Sun, 2022-06-27, 18:15–19:32, `[unknown]`)
- When you are small in a liquid market, a wrong model costs about half the spread. Profit statistics, watched "as a separate kind of indicator", tell you in the end. ([S12](https://www.flirtingwithmodels.com/episodes/nUbY8jKizyr) Sinclair, 2020-07-27, 25:10, `[named practitioner]`)
- `[general, not options]` At Man AHL the researcher and the reviewers each forecast the live Sharpe of a signal: "what do you think the sharp ratio of this signal is gonna be in live trading?" The firm scores who forecasts well and who is too optimistic. ([S13](https://www.flirtingwithmodels.com/episodes/Ur6kzQiOUD5) Korgaonkar, 2021-08-09, 30:31–31:21, `[named practitioner]`)
- `[general, not options]` A colleague watched Cameron for two years and said "I was right 60% of the time, but my trade entry and my trade management was terrible". The fix was tighter stops and repeated entries; the focus moved from hit rate to payoff ratio. ([S23](https://www.flirtingwithmodels.com/episodes/QTd278077Qx) Cameron, 2021-06-07, 21:44 and 22:20–23:10, `[named practitioner]`)

### Size and cost

- The realised edge of a professional volatility book "works out to something that looks like a penny per contract". With retail costs "you're just gonna get chiseled to death". ([S6](https://www.flirtingwithmodels.com/episodes/EdhZsWMO5mh) Abdelmessih, 2024-07-29, 51:43–55:06, `[named practitioner]`)
- "if you make money every day, you're not maximizing". Hedging is a cost; run the highest risk you can bear for the edge you have. ([S6](https://www.flirtingwithmodels.com/episodes/EdhZsWMO5mh) Abdelmessih, 2024-07-29, 25:23–25:47, `[named practitioner]`)
- A sizing rule that came from a live loss. COVID losses on large credits led Sun to "credit targeting": the same premium per trade, so high implied volatility means fewer contracts or a lower delta. On risk: "you usually don't find your risk tolerance. It will find you". ([S25](https://www.flirtingwithmodels.com/episodes/QpdJve76shu) Sun, 2022-06-27, 26:15–28:48 and 32:35, `[unknown]`)
- Scale risk to how good the opportunities are: "do you only wanna have 30 or 40% of risk on?" ([S19](https://www.flirtingwithmodels.com/episodes/8LFggZddP5i) Eifert, 2019-05-30, 20:43, `[named practitioner]`)
- Sizing is "a little bit of a recursive process", because it depends on the rest of the portfolio. "we never like to be dependent on a trade performing to provide a hedge". ([S10](https://www.flirtingwithmodels.com/episodes/08kOEaCjRLN) Baird, 2020-07-13, 53:46, `[named practitioner]`)
- Write limits in risk units. Every strategy has "guardrails": minimum and maximum market exposure, minimum and maximum convexity, and scenario limits. ([S24](https://www.flirtingwithmodels.com/episodes/UOAP6wBZT0R) Anderson, 2023-08-14, 40:30, `[named practitioner]`, also `[seller]`)
- `[general, not options]` "Behavioral time is decades longer than statistical time". A drawdown of several years is a small mark on the equity curve and very hard to live through. ([S18](https://www.flirtingwithmodels.com/episodes/hCWkkcwpYaY) Hoffstein, 2023-08-28, 25:59–27:09, `[named practitioner]`)

**Disagreement: stops.** Sinclair exits when the edge is gone, not on a loss: "you've done it the wrong size" if a loss forces you out. ([S12](https://www.flirtingwithmodels.com/episodes/nUbY8jKizyr) Sinclair, 2020-07-27, 52:22–54:09, `[named practitioner]`) Sun builds his whole method on a fixed stop (heading 2), and Cameron's fix was tighter stops (above). Krishnan uses stops only on long-dated options (heading 5).

**Disagreement: follow the model, or add judgement.** Chan follows it. His filter blocked all trades from November 2019 to January 2020 and turned on again on 1 February 2020, when the team doubted it: "we were a bit concerned that the system is overly cautious, but we follow". ([S21](https://www.flirtingwithmodels.com/episodes/oORMI7LTpcO) Chan, 2020-07-10, 26:07, `[named practitioner]`, also `[seller]`, `[general, not options]`) Eifert rates himself "seven or eight out of 10" on the systematic scale, with trader judgement on top. ([S19](https://www.flirtingwithmodels.com/episodes/8LFggZddP5i) Eifert, 2019-05-30, 23:02, `[named practitioner]`) Krishnan gives clients scenario payout tables but warns "too much rigidity in the process is not ideal". ([S28](https://www.flirtingwithmodels.com/episodes/MeUsl8ow3Z3) Krishnan, 2022-08-08, 50:00–50:52, `[named practitioner]`) Sidial adds a judgement band after the model (heading 6).

Nothing found in this lane on paper trading as a named step. Sun's "forward testing" is the nearest.

## 8. Records and killing ideas

- `[general, not options]` "In research, most of the ideas are bad." Keep the iteration time short ("time to joy"), so that bad ideas die fast. ([S1](https://signalsandthreads.com/finding-signal-in-the-noise/) Minsky, 2025-03-10, 22:07, `[named practitioner]`)
- `[general, not options]` "We have a huge graveyard of ideas... In research, it's a low percentage shot." ([S17](https://www.flirtingwithmodels.com/episodes/LcHLCLoqRU9) Meredith, clip 2023-02-13, original 2019-06-21, 10:29, `[named practitioner]`)
- `[general, not options]` Keep computing a dropped idea. A rejected factor is still calculated on every database rebuild, so it can be checked out of sample later: "even though you don't put it inside, you still calculate it". ([S17](https://www.flirtingwithmodels.com/episodes/LcHLCLoqRU9) Meredith, clip 2023-02-13, original 2019-06-21, 13:31–14:41, `[named practitioner]`)
- `[general, not options]` Kill a project on opportunity cost, not on sunk cost: "just because you started the project and spent two years on it... not good enough." ([S13](https://www.flirtingwithmodels.com/episodes/Ur6kzQiOUD5) Korgaonkar, 2021-08-09, 17:17, `[named practitioner]`)
- Measure the value of a better model before you build it. In a simulation, blend your volatility estimate with the true volatility and see if a smaller error pays. If it does not, stop. "shot selection as a researcher is very important". ([S16](https://www.flirtingwithmodels.com/episodes/X3niO6Jnu0S) Israelov, 2023-05-22, 59:59–60:58, `[named practitioner]`)
- Johnson keeps "binders and binders full of notes from just observations". His test that an edge is gone: "is this starting to be hard money?" Then he moves on. ([S14](https://www.flirtingwithmodels.com/episodes/hwaXEsvOJtR) Johnson, 2021-05-10, 49:12 and 59:12–61:10, `[unknown]`)
- Sun keeps a backtest log and a live trade log, and checks hunches against both (heading 6). ([S25](https://www.flirtingwithmodels.com/episodes/QpdJve76shu) Sun, 2022-06-27, 38:08–38:56, `[unknown]`)
- Some records cannot be kept. Logging the trades you passed on is "a pretty diabolical problem", because nobody records what would have happened. ([S6](https://www.flirtingwithmodels.com/episodes/EdhZsWMO5mh) Abdelmessih, 2024-07-29, 36:57–37:38, `[named practitioner]`)
- An idea tested and found dead. Implied event weights can be backed out of overnight volatilities, but "you couldn't make money trading those events during the last two, three years". One-off geopolitical events cannot be tested: "there is only one event". ([S27](https://www.flirtingwithmodels.com/episodes/TCrhgAEhKLB) Jacobson, 2022-08-01, 43:05 and 44:15, `[named practitioner]`)
- Edges decay because you trade them. Dealers repriced the volatility he bought: "effectively, I improve the market. So now I need to find new edges". ([S27](https://www.flirtingwithmodels.com/episodes/TCrhgAEhKLB) Jacobson, 2022-08-01, 36:36–37:01, `[named practitioner]`)
- Alpha "is fleeting and you have to keep refining" it. ([S5](https://mutinyfund.com/kris-abdelmessih/) Abdelmessih, Aug 2023, transcript p.10, `[named practitioner]`, also `[seller: moontower.ai]`)
- A good edge can be too rare to live on. One VIX trade has "literally never lost money" in four years, but it appears four or five times a year. ([S12](https://www.flirtingwithmodels.com/episodes/nUbY8jKizyr) Sinclair, 2020-07-27, 21:43, `[named practitioner]`)
- `[general, not options]` How long a prototype takes: Cameron's first trading agent took about eighteen months on the E-mini S&P alone, and was then tried on currencies and single stocks. No quote. ([S23](https://www.flirtingwithmodels.com/episodes/QTd278077Qx) Cameron, 2021-06-07, 36:38 and 61:15–62:17, `[named practitioner]`)

Nothing found in this lane on what share of ideas dies, as a number.

## Hypothesis sources, ranked

Counts are of guests in this lane's notes, not of episodes. A guest who appears in two episodes counts once.

| Source of ideas | Guests who named it | Strongest link |
|---|---|---|
| Who is forced to trade (flow, market structure) | 10: Abdelmessih, Eifert, Karsan, Krishnan, Curnutt, Anderson, Jacobson, Sidial, Chan, Cho | [S7 Eifert, "Bad Ideas"](https://www.flirtingwithmodels.com/episodes/If53y6iMsVe) |
| Screening ratios and statistics | 7: Abdelmessih, Eifert, Curnutt, Krishnan, Johnson, Sidial, Karsan | [S6 Abdelmessih](https://www.flirtingwithmodels.com/episodes/EdhZsWMO5mh), 58:27–64:26 |
| Watching the screen, desk experience | 5: Lindstrom, Abdelmessih, Karsan, Sidial, Macrocephalopod | [S8 Lindstrom](https://www.flirtingwithmodels.com/episodes/QJXQ5hBMDGp), 16:41–17:36 |
| Asking dealers, brokers and other traders | 5: Eifert, Krishnan, Macrocephalopod, Abdelmessih, Korgaonkar | [S28 Krishnan](https://www.flirtingwithmodels.com/episodes/MeUsl8ow3Z3), 21:05 |
| Papers and books | 4: Macrocephalopod, Sinclair, Meredith, Johnson | [S11 Macrocephalopod](https://www.flirtingwithmodels.com/episodes/4kGccf3znLs), 57:18–60:09 |
| Product mechanics (prospectus, fund structure, rebalancing) | 4: Johnson, Abdelmessih, Curnutt, Eifert | [S14 Johnson](https://www.flirtingwithmodels.com/episodes/hwaXEsvOJtR), 55:44–58:56 |
| Your own losses, attributed | 3: Karsan, Chan, Sun | [S26 Karsan](https://www.flirtingwithmodels.com/episodes/bPhUORxdAP5), 8:48–9:27 |
| Fundamentals (supply and demand) | 3: Baird, Krishnan, Sinclair | [S10 Baird](https://www.flirtingwithmodels.com/episodes/08kOEaCjRLN), 26:01 |
| Forums, social media, free content | 2: Jacobson, Sun | [S27 Jacobson](https://www.flirtingwithmodels.com/episodes/TCrhgAEhKLB), 46:54–47:48 |
| New or sparse datasets | 2: Macrocephalopod, Abdelmessih | [S6 Abdelmessih](https://www.flirtingwithmodels.com/episodes/EdhZsWMO5mh), 27:19–28:37 |
| Past crises | 1: Curnutt | [S22 Curnutt](https://www.flirtingwithmodels.com/episodes/l8s5fwO9IGb), 6:51 |
| Market sayings turned into tests | 1: Karsan | [S26 Karsan](https://www.flirtingwithmodels.com/episodes/bPhUORxdAP5), 17:38–22:29 |
| By-product of other research | 1: Israelov | [S16 Israelov](https://www.flirtingwithmodels.com/episodes/X3niO6Jnu0S), 27:56 |
| Data mining with no causal story (warned against) | 3 warn: Karsan, Abdelmessih, Chan | [S2 Karsan](https://mutinyfund.com/cem-karsan/) |

## Ten sources worth reading in full

1. [S6 Abdelmessih, "Life Through a Volatility Lens"](https://www.flirtingwithmodels.com/episodes/EdhZsWMO5mh). The only step-by-step account of a ratio screen, with a worked trade.
2. [S7 Eifert, "Bad Ideas"](https://www.flirtingwithmodels.com/episodes/If53y6iMsVe). Why the common VRP screen is wrong, and how flow sets a premium.
3. [S11 Macrocephalopod](https://www.flirtingwithmodels.com/episodes/4kGccf3znLs). The clearest order of work: research, then backtest, then daily reconciliation with live trading.
4. [S25 Sun, "Expectancy Hacking"](https://www.flirtingwithmodels.com/episodes/QpdJve76shu). SPX 0DTE at small scale, the nearest to Lalit's own study; costs, stops and one live yardstick.
5. [S14 Johnson, "Independently Shorting Volatility"](https://www.flirtingwithmodels.com/episodes/hwaXEsvOJtR). A self-taught trader's full path: books, simulation, dashboard, binders of notes.
6. [S12 Sinclair, "Positional Option Trading"](https://www.flirtingwithmodels.com/episodes/nUbY8jKizyr). Premium against inefficiency, and where the literature is thin.
7. [S16 Israelov](https://www.flirtingwithmodels.com/episodes/X3niO6Jnu0S). Test twice, once on data and once in a simulation where the truth is known; when to stop research.
8. [S13 Korgaonkar, "Optimizing the Research Process"](https://www.flirtingwithmodels.com/episodes/Ur6kzQiOUD5). Peer review, holdout rules and scored forecasts of live Sharpe at Man AHL.
9. [S18 Hoffstein, "15 Ideas"](https://www.flirtingwithmodels.com/episodes/hCWkkcwpYaY). A list of ways to perturb a backtest, and the case against strict thresholds.
10. [S1 Signals and Threads, "Finding Signal in the Noise"](https://signalsandthreads.com/finding-signal-in-the-noise/). The four stages of research and the best material on notebooks.

## Could not open

None recorded by the earlier workers.

## Appendix: source notes

Notes from the earlier workers, one note per episode, numbered S1 to S28. S6, S7 and S11 each join two notes on the same episode. Quotes and timestamps are as the earlier workers wrote them; nothing was re-opened.


### S1. Signals and Threads ep. 22, "Finding Signal in the Noise" — In Young Cho and Ron Minsky (Jane Street), 2025-03-10
URL: https://signalsandthreads.com/finding-signal-in-the-noise/ — full transcript on page. Label: [named practitioner]. [general, not options]
- Q1/Q2: research has four stages: exploration, data collection, modelling, productionisation. Example hypothesis starts from a client's flow and 13F filings (11:55–14:04). "I think there are roughly four stages of research."
- Q3: build the first dataset by hand to learn which checks matter (15:29). "you could do it all manually and you could check things very, very carefully."
- Q4: notebooks are good for sharing and annotation, bad for production (34:01). Minsky: out-of-order execution breaks reproducibility (34:34): "Things get evaluated in just whatever damn order you click the buttons". Reproducibility matters for research too, not only production (37:08).
- Q4: two research styles: simulate the real production system, or study a simplified offline dataset and port later (18:54–20:03). Quick-and-dirty study tools "has bitten us".
- Q6: with little data, keep more data in-sample but limit the count of hypotheses tested (38:51): "be very careful about the number of hypotheses that you test". Cross-team leakage: many people testing similar ideas on one holdout (40:30s): "not duplicating hypotheses across groups".
- Q8: "In research, most of the ideas are bad." (Minsky, 22:07). Short iteration time — "time to joy" — so bad ideas die fast.

### S2. Mutiny Fund ep. 24 — Cem Karsan (Kai Volatility) with Jason Buck, c. Feb 2021 (GameStop discussed as topical; page undated)
URL: https://mutinyfund.com/cem-karsan/ — full transcript on page. Label: [named practitioner]
- Q1: hypotheses come from market-maker experience of who is forced to trade — trades that looked rich "relative to our surfaces" kept losing, which forced a flow model (~41:32): "putting on things relative to our surfaces that looked like tremendous trades. And regularly seeing them not be profitable."
- Q1 (against data mining): start from causality, then use statistics to optimise: "People use great data sets and then data mine them... That hasn't been our approach." / "They're just playing correlation and those things are fleeting."
- Q1 example: 30-day skew is structurally rich because hedging volume peaks one month out (supply/demand), a statistical relationship between skew at two expiries.
- Q2: model in three layers — distribution of outcomes by VIX bucket, then vanna/charm adjustments, then directional signals (~23:12).
- Q5/Q7: rebalance interval tightened as the model improved; "allows us to pay a little bit more slippage... to capture more edge".
- Q6 (weakness): the quarterly-OPEX/passive-flow effect is admitted to rest on "only a few data points. It's more of a hunch" (host Jason Buck, Karsan agrees it is flow).

### S3. Signals and Threads ep. 5, "Python, OCaml, and Machine Learning" — Laurent Mazare (Jane Street, ex-Goldman, ex-DeepMind), 2020-10-07
URL: https://signalsandthreads.com/python-ocaml-and-machine-learning/ — full transcript. Label: [named practitioner]. [general, not options]. Another lane also uses this episode; expect a duplicate when the six reports are merged.
- Q4: research half of his time is Python in a notebook; production half is OCaml (05:36): "the first half of my time is spent using Python, and that's mostly for research purposes."
- Q4: notebook code is written for this data, not all data (≈ expect-test discussion): "you actually want it to work on your data rather than on any potential data."
- Q4: hidden-state problem (47:10): "it's very easy to create a notebook state and not remember how you actually reached that state". Fix: restart and re-reach the conclusion from scratch.
- Q4: firm services (market data, publishing values) are wrapped from OCaml into Python so the notebook only calls library functions; shared, heavily-used functions live in the typed language, not the notebook.

### S4. Signals and Threads ep. 23, "Building Tools for Traders" — Ian Henry (Jane Street options desk), 2025-05-28
URL: https://signalsandthreads.com/building-tools-for-traders/ — full transcript. Label: [named practitioner]
- Q4: Minsky (01:11:35) on why notebooks are untrustworthy as record: "there are no guarantees that the stuff that's in the notebook reflects what would happen if you reran the notebook from beginning to end." Their alternative is the expect test: a plain-text file that always reruns top to bottom and flags any changed output.
- Q3: options desk tools are mostly "data collection, visualization, and alerting and monitoring"; a trader in one name thinks about hundreds of related instruments at once.

### S5. Kris Abdelmessih on Mutiny Fund, ep. 54 "Alpha Is Illusive" (Aug 2023)
URL https://mutinyfund.com/kris-abdelmessih/ — transcript PDF (Rev.com) linked from the page. `[named practitioner]` ex-SIG market maker, ran commodity RV vol at Parallax; co-founder moontower.ai `[seller: options analytics tool]`.
- Q1: Risk premia come from who is forced to trade. "There is no natural to being on the other side of the S&P going down." Example: Pemex buys puts to hedge oil output; the dealer must "charge enough" because that risk is not diversifiable. (transcript p.10)
- Q1: For a directional options trade, "most of the work is upstream of the option expression"; the option piece is "super trivial" once the distribution view exists. (p.8–9)
- Q1/Q8: Alpha "is fleeting and you have to keep refining" it; beta is the premium for risk nobody else wants. (p.10)

### S6. Kris Abdelmessih on Flirting with Models S7E10 "Life Through a Volatility Lens" (29 Jul 2024)
URL https://www.flirtingwithmodels.com/episodes/EdhZsWMO5mh — full transcript on page. `[named practitioner]`, `[seller: moontower.ai]` (for the screening steps the seller label applies: moontower.ai is the option-analytics tool the steps describe). Two notes merged; where they gave different time ranges for one passage, both are shown.
- Q1 (desk/screen): at Parallax he scanned "all the markets" for vol he already thought was cheap and bought it on days it underperformed: "So I'm working screens." [22:07]
- Q1 (sparse data): edge is most interesting "when they don't have a lot of large data precedents"; where you can "data hack things to death" is crowded. Second note (range to 28:37): watch where good traders stand; "in areas where data is highly structured, it's going to be very competitive." [27:19–28:16]
- Q2/Q5 worked example, USO 2020: three separate reasons USO vol should be below futures-option vol (put-like NAV premium, roll into less volatile back months, no bid side in the voice market). Built "ten minutes to the open" in "a spreadsheet open and we were throwing numbers in" and switched to a model allowing negative prices. Second note (Q1, range 28:37 to 35:08): a high IV is not a reason to sell; in April 2020 he bought futures-option vol at record levels but sold USO vol because USO had become "an option on a barrel of oil". [28:48–34:44]
- Q3/Q4 (tools): as a sole prop "we weren't coders"; hired a high-school senior who knew Java: "We'll buy some data. You make a database ... we could query charts from." A "standard set of vol metrics to normalize across the markets", then discretion per asset. [47:03]
- Q4: He first wrote his process down "methodically ... in a flow" only when coaching a developer, who turned each step into code and a UI — that became the moontower.ai dashboards. [48:35]
- Q5/Q7 (costs): realised edge for a professional vol book "works out to something that looks like a penny per contract"; "a retail cost structure, you're just gonna get chiseled to death". Funding spread example: 600 bp borrow/lend spread makes a bought call carry a much higher implied vol than it appears. Second note (Q7, range 51:43 to 55:06): retail cost and funding spreads kill delta-neutral vol trading at home. [52:07–54:18]
- Q7 (sizing): "if you make money every day, you're not maximizing" — hedging is a cost; run "the highest tolerable risk for a given amount of edge". [25:23–25:47]
- Q1 (screening ratios, step by step, 58:27–64:26): reduce the chain to four dimensions — straddle (IV vs RV), vertical (skew), strangle (tails), time spread (term structure/forward vol). Then compare each cross-sectionally against liquid benchmarks and its own percentile: "throwing all these assets onto a cross sectional diagram". Example: XLK term structure flat vs SPY's steep, IV/RV premium "similar... to other names", put skew in a high percentile, so buy calls and sell stock rather than buy puts.
- Q1 (who is on the other side): flow-heavy bank traders often lack a standalone edge: "when this ball gets low, I'm gonna buy it... it's a little bit naive. It's not gonna work." (42:49)
- Q8 (data you can't capture): logging trades you passed on is "a pretty diabolical problem" — the counterfactual is unrecorded (36:57–37:38).
- Q1: what makes options useful as a thinking tool — they force a dated, specific thesis (56:37): "You're not just bullish. You're bullish with constraint."

### S7. Benn Eifert on Flirting with Models S3E3 "Bad Ideas" (6 Jul 2020)
URL https://www.flirtingwithmodels.com/episodes/If53y6iMsVe — transcript on page. `[named practitioner]` QVR Advisors (QVR wound down 2026; see `research/_raw/practitioners.md`). Two notes merged; where they gave different time ranges for one passage, both are shown.
- Q1 (who is forced to trade): a premium is a flow imbalance, not a constant. "Risk premium are not constant nor should you think of them as constant." Pension consultants' white papers (2012–16) pushed overwriting and put selling to "$800,000,000 of vega a month" until market makers were "choking on the one way supply". Ask the market maker, not the textbook. Second note (range from 15:26): VRP is regime-dependent and set by flow, the supply coming from overwriting and put-writing programs; check the story against the dealer: "if you ask a market maker, what is supply and demand in short term S and P options". [15:48–17:21]
- Q3/Q6: on VIX futures, test carry against prediction yourself: "you should go get the data, get every historical price of every VIX future and do some work" — he reports the curve is "much more risk premium than ... predictive". [33:50]
- Q1 (screening ratio trap): "VIX minus realised vol" is the wrong VRP screen — VIX prices a variance swap and sits 2–3 points over ATM vol in calm markets (10:21–13:00): "those are apples to apples comparisons" only ATM-vs-realised or VIX²-vs-realised variance. A positive VIX–RV gap "may have well been a breakeven or a money loser" on ATM straddles.
- Q1: VRP compresses toward zero late in cycles as sellers crowd in (13:00–14:12); Cboe CNDR condor index as public evidence a premium died (18:27–19:33).
- Q2: evaluate an option trade as price vs payoff probability; a tight call spread is a binary that reads the market's implied probability, which you compare with your own estimate (41:30–43:17).
- Q1: implied probabilities move with flow alone — one overwriter selling 20,000 calls moves them "and nothing changed other than a transaction" (43:24).

### S8. Tina Lindstrom on Flirting with Models S4E4 "Commodity Volatility" (24 May 2021)
URL https://www.flirtingwithmodels.com/episodes/QJXQ5hBMDGp — transcript on page. `[named practitioner]` ex-SIG options market maker, now prop vol trader in oil.
- Q1 (watching the screen): her stated process for discretionary ideas: "I study the vol surface every one and a half minutes", then for each kink: "What am I missing? Why is this kink here?" — identify who is betting on what ("He's a delta guy") and whether they are "expressing it wrong". [16:41–17:36]
- Q1: SIG training as idea school: senior traders explained each day's trades "why they were good, why they were bad", plus mock trading twice a week. [03:27]

### S9. Hari Krishnan on Flirting with Models S7E4 "Hedging a Commodity Bull Market" (8 Jan 2024)
URL https://www.flirtingwithmodels.com/episodes/3xG50jvisGY — transcript on page. `[named practitioner]` options fund manager (author of *The Second Leg Down*).
- Q1 (screen, then fundamentals): a statistical screen — "low price, no action, forgotten" — finds candidates; colleagues with industry contacts then pick the subset with "a potential fundamental driver". [23:57, 36:07–36:38]
- Q1 (who is forced to trade): skew in grains comes from producers and end users having different risks; "the marginal buyer or seller determines the price". [13:51, 35:23]
- Q6 (holdout): backtests count only if "well specified ... not burning all the data, at least withholding other markets", then checking a theme holds across all ags or all softs. [41:06]
- Q2/Q6: "we'll only run with it if we know or have some inkling as to why such mispricing exists." [41:06]
- Q5 trap: never rank option structures by backtest P&L when they carry "embedded deltas" — a 50/20 call spread winning in a soybean rally shows the rally, not the structure. [41:06]
- Q5: backtest assumes "one swing at the plate per cycle", rolled a few weeks before expiry; live fills need patience working limits. [38:37]

### S10. Jeffrey Baird on Flirting with Models S3E6 "Commodity Convexity" (13 Jul 2020)
URL https://www.flirtingwithmodels.com/episodes/08kOEaCjRLN — transcript on page. `[named practitioner]` Merit Point Partners, discretionary commodity options.
- Q1 (fundamentals): looks for an "inflection point" in supply/demand where options give "very leverage payout" if the shift becomes "a much bigger deal". [26:01]
- Q3: natural gas has "almost real time" data — pipeline scrapes, storage, LNG loadings — "depending on the amount of money you wanna spend". [28:26]
- Q7 (sizing): sizing is "a little bit of a recursive process in terms of what else is in the portfolio"; "we never like to be dependent on a trade performing to provide a hedge". [53:46]

### S11. Macrocephalopod on Flirting with Models S6E5 "Managing a Mid-Frequency Crypto Prop Desk" (29 May 2023) `[general, not options]`
URL https://www.flirtingwithmodels.com/episodes/4kGccf3znLs — transcript on page. `[anonymous, credible]` — anonymous X user; ex hedge-fund quant researcher, runs a crypto prop desk; author of the "24 days of backtest errors" thread series. Two notes merged; where they gave different time ranges for one passage, both are shown.
- Q1 (ranked by career stage): "I used to predominantly get my ideas from reading papers", good "when you are starting out"; but papers lag industry by "something like five to ten years". Later sources: new datasets, "just watching the market" (replaying historic data), thinking about your own execution and who could exploit it, and talking to other traders. [57:18–60:09]
- Q2/Q4, and Q5/Q6 in the second note: "the research is what you do before you run the backtest": look at data, build features, test hypotheses, ask "is there something predictable here?" with linear regressions on forward returns before any simulation. Second note (range to 16:39): then vol forecasts, risk model and limits, and only then simulate. [14:51–16:04]
- Q5: uses of a backtest: a final check; comparing simulation assumptions (impact, fill rate, borrow, latency) by plotting P&L against each; comparing two variants on the same engine, trusting the delta not the level. [16:53–17:50]
- Q6: "Your backtest is always gonna be optimistic"; errors "almost always ... go against you". Second note gives 16:39 to 16:53. [16:04–16:53]
- Q7 (live vs backtest): every day/week, re-run the simulator over what was just traded: "how well does my backtest match reality?" — "underappreciated". Second note: reconcile daily and explain every gap. [17:50]
- Q7 (scaling): crude cost assumptions are survivable while small; on scale-up "your simulation will be saying, great ... in your live book, you're just losing money hand over fist". Bigger size is the only source of the data to fix the model. [55:05–56:18]
- Q6: split the universe — research on half the names, check the other half (12:33): "does this still hold in the other half of the universe?" Few-asset markets give you no such check, "it becomes much easier to fool yourself" (13:13).
- Q1: old macro premia worked partly because of access barriers to data and markets; when access improved, the "inefficiency component" left (7:12–8:09).
- Q5: a square-root impact model with slow decay can be gamed in simulation — "what seems to empirically fit the best... cannot be correct" (53:14–53:49). Start crude on impact and fills, but you "end up needing to model these things very accurately" as you scale (55:05).

### S12. Flirting with Models S3E12 — Euan Sinclair, "Positional Option Trading", 2020-07-27
URL: https://www.flirtingwithmodels.com/episodes/nUbY8jKizyr — full Deepgram transcript (JSON linked from page). Label: [named practitioner]
- Q1/Q2: first sort every idea into risk premium or inefficiency (19:23): "You have to know if your edge is coming from a risk premium or a genuine inefficiency." Premium: trade cautiously, forever. Inefficiency (earnings, splits, takeovers): trade big but it may not recur.
- Q1: second axis — "situational" vs "model driven" trades (22:24–24:01). Situational = based on "similar situations that have happened in the past", noisy, more profitable.
- Q1 (where to look): GARCH/time-series vol forecasting is "heavily picked over" (thousands of SSRN papers); factor models for options had "eight papers" (38:48–40:33). "If I was completely starting over, I'd be looking at fundamental factors using them to directly predict volatility."
- Q2: think edge first, structure second: "The most important thing to do when you do a trade is look for your edge" (36:36). Options traders "get that the wrong way around."
- Q5: academic short-vol returns quoted on premium, not margin, mislead (44:44): "you have to be very careful when you look at academic studies, particularly on the short vol side." He normalises trades by constant vega (45:47).
- Q6: skewed payoffs hide the mean — iron condor shows the mode (35:15): "You see the mode, and the mode is unbelievably good."
- Q6: trade selection uses generalised Sharpe (skew/kurtosis), Kelly, not expected value (49:07–50:01).
- Q7: when small in a liquid market, a wrong model costs about half the spread; P&L statistics, monitored "as a separate kind of indicator", eventually tell you (25:10).
- Q7/Q8: exit when edge is gone, not on a stop (52:22–54:09): "If you ever had to get out of the trade because you lost money, you've done it the wrong size."
- Q8: one VIX trade has "literally never lost money" over four years but appears 4–5 times a year; can't build a business on it (21:43).

### S13. Flirting with Models S4E15 — Russell Korgaonkar (CIO, Man AHL), "Optimizing the Research Process", 2021-08-09
URL: https://www.flirtingwithmodels.com/episodes/Ur6kzQiOUD5 — full transcript. Label: [named practitioner]. [general, not options] (AHL's options trading sits in its "Specialist" unit, 11:12)
- Q6: every idea gets two peer reviewers, one from another unit, then a held-back out-of-sample set with criteria agreed in advance (12:30–13:35): "We always put two researchers to kind of peer review test the idea."
- Q6: review happens only on in-sample data; the researcher then tests original and modified versions on the untouched set; reviewer suggestions added 0.9 Sharpe in one credit RV case (31:59–32:54).
- Q7/Q8: researcher and reviewers each forecast the live Sharpe of a signal; AHL scores who forecasts well and who is over-optimistic (30:31–31:21): "what do you think the sharp ratio of this signal is gonna be in live trading?" Value is judged "not in backtest, but in live trading."
- Q8: kill projects on opportunity cost, not sunk cost (17:17): "just because you started the project and spent two years on it... not good enough."
- Q1/Q2: the question asked of every new strategy (49:43): "why do you think that thing is gonna work in the future? Not just because it's worked in the past". Backtests are "a comfort blanket" (33:55).
- Q1: discretionary PMs (GLG) were useful reviewers of quant signals: "tell me what you think about it... what can go wrong" (27:23).

### S14. Flirting with Models S4E2 — Darrin Johnson, "Independently Shorting Volatility", 2021-05-10
URL: https://www.flirtingwithmodels.com/episodes/hwaXEsvOJtR — full transcript. Label: [unknown] (named independent trader; track record self-reported, not verifiable). Options-specific and retail-scale, so close to Lalit's position.
- Q1: learned from Sinclair's books, hired a freelance quant to walk him through Black-Scholes "line by line", built scenario drills (17:10–18:11).
- Q3/Q4: options data was expensive in 2009–10 (iVolatility), so he started with simulated paths in Python (19:31–21:01): "I use random data at first because option data at that time was expensive." Monte Carlo with set drift and vol, look at median and worst case.
- Q6: argues simulation over a single historical path (21:01): "when you backtest with actual data, that's only one path."
- Q3/Q1: how realized vol is measured changes profitability; he keeps a composite dashboard of several RV estimators and horizons (21:01–21:54); short-horizon RV term structure turning backwardated is his "don't sell" warning (28:36–29:51).
- Q2: forecast first, then choose the product and structure that pays most if right (31:28): "it's always better to have an opinion and have no forecast than to not have one".
- Q1: single-stock VRP is "spotty at best", and he notes the gap in the literature (33:40).
- Q6: sell nearer the money (≥30–35 delta) to get feedback on whether the vol forecast has edge (41:27): "I can just be fooled by the fact that I'm so far away". Used a Kelly spreadsheet to choose strikes and profit-taking (39:46–40:22).
- Q1: replicate a product from its prospectus (VXX/UVXY) in Excel and Python to find the edge (55:44–58:56); edge then decayed in stages as others found it.
- Q8: keeps "binders and binders full of notes from just observations" (49:12). Edge-gone test (59:12–61:10): "is this starting to be hard money?" — then "On to the next table."

### S15. Flirting with Models S3E14 — Kris Sidial (Ambrus Group), "Long Volatility for the New Regime", 2020-09-08
URL: https://www.flirtingwithmodels.com/episodes/2A6apAi6jOo — full transcript. Label: [named practitioner]
- Q1: at a bank flow desk he learned what clients traded and why; "Some of those guys were trading some very simple strategies" (14:50).
- Q6 (regime split): the backtest is "a guide", not "the holy grail"; split the sample by VIX regime — low, medium, high, super high — and test each strategy per regime and per underlying (28:29–29:27): "I like to break down VIX into different regimes."
- Q3/Q6: weight older data less; 1980s price series are "not an equal comparison" to today's market (20:58).
- Q6: measure correlations in stress windows, not calm ones (54:29): "I wanna see how the correlation's acting when everything is hitting the fan".
- Q2/Q5 (worked example of a tested idea, 57:31–60:35): after a 2-standard-deviation weekly move, run Hurst and ADF tests (mean-reversion tests) on the series, then sell the inflated one-week wings for the vol crush; hedged by long tails elsewhere in the book.
- Q5: a backtested "delta optimization point" for staggered short-tenor sales (47:37). Sizing aims at Kelly (40:20).
- Q1 (warning): the two retail-quant dead ends — sell tails until ruin, or bleed for years waiting (30:44–31:35).
- Q6 (discretion): after the model, traders add a "confidence interval" from experience (28:29, 32:23).

### S16. Flirting with Models S6E4 — Roni Israelov (ex-AQR options strategies lead, CIO NDVR), 2023-05-22
URL: https://www.flirtingwithmodels.com/episodes/X3niO6Jnu0S — full transcript. Label: [named practitioner]
- Q6 (method — test twice): each question is tested on real data and then in a simulation where the answer is known. "Pathetic Protection": S&P put data first, then simulated GBM prices with option prices carrying no VRP, to separate the cost of puts from their benefit (42:16–43:27).
- Q6: why simulate (58:30–58:54): "because you know the truth" and "history gives us one path. And it's easy to over index on that single path".
- Q8 (when to stop): measure the value of a better model before building it. In a simulation, blend your vol estimate with the true vol ("essentially cheating") to see if less estimation error pays; if not, stop (59:59–60:58): "shot selection as a researcher is very important" / "figuring out an optimal stopping point".
- Q5/Q6 (risk measure for short options): Sharpe on volatility misleads; use prime-broker-style stress tests (equity −20%, IV shocked) to size short options; "Which Index Option Should You Sell" (52:39–53:05).
- Q5: delta-hedged VRP still leaves residual beta from spot-vol correlation; neutralise it (47:30–47:44).
- Q1: short-horizon factors often appear as a by-product of long-horizon research (27:56).

### S17. Flirting with Models archive clip, "What does a full-stack quant research platform and process look like?" (2023-02-13), from S2E10 Chris Meredith (O'Shaughnessy AM), original 2019-06-21
URL: https://www.flirtingwithmodels.com/episodes/LcHLCLoqRU9 (full S2E10: https://www.flirtingwithmodels.com/episodes/weOrt7bkJPd) — full transcript. Label: [named practitioner]. [general, not options]
- Q8: "We have a huge graveyard of ideas... In research, it's a low percentage shot." (10:29)
- Q8 (log and keep tracking failed ideas): a dropped factor (owner-operator ownership, ~80 bp that flattened when "you flip it another way") is still computed on every database rebuild so it can be checked out of sample later (13:31–14:41): "even though you don't put it inside, you still calculate it".
- Q2: every research proposal goes on a template with a "modified information ratio" — expected return or cost saving, scaled by risk, times the assets it would affect — weighed against data cost (e.g. $250k/yr for ~20 bp) (11:27–12:08).
- Q1: start from an intuitive reason, then literature surveys; warns academics may share less than before (10:39–10:57).
- Q4: each researcher has a "sandbox" copy of a "gold standard" environment: "you can mess up your sandbox all you want", refreshed from the gold copy; production code then gets version control (15:51–17:36). Platform rebuilt from scratch four times.
- Q3: build derived numbers yourself rather than take vendor analytics; outlier checks and manual review of scraped data ("the least fun part of our job") (8:51–9:49).

### S18. Flirting with Models special — Corey Hoffstein (CIO Newfound Research), "15 Ideas, Frameworks, and Lessons from 15 Years", 2023-08-28
URL: https://www.flirtingwithmodels.com/episodes/hCWkkcwpYaY — full transcript (solo monologue). Label: [named practitioner]. [general, not options]
- Q6 (perturb the backtest): "A backtest is just a single draw of a stochastic process" (29:36). Techniques (30:36–31:38): vary parameters, entry/exit timing, slippage; randomly remove chunks of the universe; randomly remove periods of time; deliberately add look-ahead ("a crystal ball") to find the upper bound and confidence bands.
- Q6 (timing luck): the 10-month MA paper's result depended on the rebalance day; varying it across every trading day gave large short-run dispersion with indistinguishable long-run returns (7:45–9:07).
- Q6 (run the counterfactual): a factor-timing paper's result sat in the top percentiles of a brute-forced random-basket distribution — "So did a naive equally weighted portfolio" (17:12–18:16).
- Q6 (disagreement with strict multiple-testing): type I vs type II errors are asymmetric — a false positive costs noise minus costs, a false negative costs the alpha — "it may actually be prudent to reduce the statistical requirements" (24:59–25:42).
- Q2: "always ask what's the trade?" — writing the actual trade exposes why an "absurd" price isn't (23:19–24:34). Default to "the market is right, and I'm the one who's missing something" (31:38–32:33).
- Q7: "Behavioral time is decades longer than statistical time" — a multi-year drawdown is a blip on the equity curve and unbearable live (25:59–27:09).
- Q4/Q5: Jensen's inequality — averaging signals before vs after a convex step (ranks, caps) changes results (27:09–29:36).

### S19. Flirting with Models S2E2 — Benn Eifert (QVR Advisors), "Volatility Investing", 2019-05-30
URL: https://www.flirtingwithmodels.com/episodes/8LFggZddP5i — full transcript. Label: [named practitioner]
- Q1 (who is forced to trade): the book is a set of "strategy sleeves", each "driven by some particular type of dislocation or ... underlying flow that ... end users are generating" (18:11). Finding the flow is easy if you talk to dealers (20:43–21:23): "that's not that hard of a question to answer if you're a really active market participant".
- Q1/Q3 (from flow to a data screen): for opportunistic cross-sectional trades, "historically map a lot of data to try to understand ... what pieces of data are helpful in identifying and predicting that" (19:21). Then triangulate: check that the cheapening was not driven by realised vol before trading (20:07).
- Q6 (a historical model that does not know the world): Japan 2013 positive skew looked rare, but "it was really a sucker's trap to look at SKU and look at a historical dataset" (27:37). Feb 2018: a model on history alone would have sold VIX calls that were cheap given ETP rebalancing (29:21–30:18).
- Q6 (backtests and crowding): pension programmes rely on "twenty five, thirty year historical backtests" and ignore "equilibrium effects on risk premium" (37:36). Ask "how much larger is positioning in that than ... twenty years ago in their back test" (53:00–53:57).
- Q5 (stress, not notional): take each major risk factor "to a very extreme level that you've never seen historically" (51:33), then probe the hidden assumptions in the stress framework (56:46). A put spread has twice the gross notional of a naked put and less risk (55:25).
- Q5/Q7 (execution and sizing): building a large exposure across many strikes is "an experimentation process to some extent" (24:20). Risk is scaled by how attractive the opportunity set is: "do you only wanna have 30 or 40% of risk on?" (20:43). Self-rated "seven or eight out of 10" on the systematic scale, with trader judgement on top (23:02).

### S20. Odd Lots "Lots More" — Benn Eifert (QVR), "How TikTok Options Traders Got Quiet", 2025-04-26
URL: https://podscripts.co/podcasts/odd-lots/lots-more-on-how-tiktok-options-traders-got-quiet — machine transcript (podscripts). Label: [named practitioner]
- Q2 (two kinds of dislocation trade): some trades "make money on realized dynamics" and need the gap to stay open; others pay only "when it reverts" (17:29–18:07). For the second kind ask: "where is this dislocation coming from? What flows are driving it?" — persistent flow means no trade; temporary supply and demand means a trade (18:07–18:47).
- Q1 (screening ratio, again): VIX against realised is the wrong comparison because VIX is a variance-swap level; "The right number to compare would be like at the money implied ball" — ATM sits about 3 to 10 points under VIX (11:16).
- Q1 (who is selling): read the front-month VIX future against spot VIX after a spike — 32 against 50 meant "everybody's selling it"; the VIX future is "the tourist instrument" (20:47).
- Q1 (warning): you "can't just look at the level of the wizzou parameter on a screen" — a made-up parameter, his joke for staring at a Greek level without a flow story (18:47).

### S21. Flirting with Models S3E5 — Ernest Chan (QTS Capital), "Tail Reaper", 2020-07-10
URL: https://www.flirtingwithmodels.com/episodes/oORMI7LTpcO — full transcript. Label: [named practitioner]; also [seller] (books, courses, and the machine-learning service he launches in the episode). [general, not options] — the strategy trades E-mini futures, no options.
- Q1 (idea from your own pain): a 35% drawdown in Aug 2011 on a 14x-levered FX strategy started the search: "So we spend the next year looking for a tail head strategy" (9:30–10:02).
- Q1 (who is forced to trade): the edge is that large holders cannot de-risk at the open; "a large amount of rebalancing and hedging activity, is what we are trying to piggyback on" (15:41). Tested on many markets; it worked only in the S&P, which he ties to S&P derivatives hedging volume (31:39).
- Q1/Q8 (ideas from losing trades): after each loss "we come up with a lot of ideas" — rates, reversal days, the open (34:53). These become candidate features: "Why is there this big loss? ... let's put that in, and we train the system" (45:24).
- Q6 (why he abandoned machine learning for ten years): 1990s models gave excellent backtests and no profit. "It's okay to generate false positives for your boss because you get paid a salary anyway." (6:07)
- Q2/Q6 (keep the signal explainable): no machine learning in the signal itself, because a strategy needs "a sensible fundamental reason"; without one, in a drawdown "one is tempted to shut the gun [it down]" (32:59). Machine learning only sizes trades the base rule generates (meta-labeling, a second model that predicts whether each base trade will win) (20:03–24:00).
- Q6 (tuning): cross-validate hyperparameters and keep the search light: "we don't over hyper optimize" (46:50). Feature-importance rankings changed with each random seed until averaged over about 100 seeds; out-of-sample performance did not depend on it (39:15–41:20).
- Q7 (following the model live): the filter blocked all trades Nov 2019–Jan 2020, then turned on 1 Feb 2020 when the team doubted it: "we were a bit concerned that the system is overly cautious, but we follow" (26:07).

### S22. Flirting with Models S6E16 — Dean Curnutt (Macro Risk Advisors; host of Alpha Exchange), "The Reflexivity of Equity Volatility", 2023-09-11
URL: https://www.flirtingwithmodels.com/episodes/l8s5fwO9IGb — full transcript. Label: [named practitioner] (ex-Lehman and BofA equity derivatives; runs an agency broker).
- Q1 (crises as the source): "you learn the most about markets by studying the periods when things go horribly wrong" (6:51).
- Q1 (size the forced flow against volume): before Feb 2018 his firm showed that a 6-point VIX rise meant "about a 30,000 VIX futures or more to buy in one day", above daily volume (42:36). For 1987 he gauged portfolio-insurance size by counting newspaper mentions (10:35).
- Q1 (warning on dealer-positioning charts): "I see a lot of charts with gamma by strike, and I just ask myself, how do you know how they're trading it?" An overwriter may delta-hedge; dispersion traders react differently (52:56–54:05).
- Q1/Q6 (bucket by realised vol): S&P returns sorted into realised-vol buckets (<10, 10–15, 15–25, >50): "I just bucketed periods when realized vol is below 10". He calls it a concurrent fact, not a forecast (50:11–51:17).
- Q1 (his cheap-vol screen): look for "favorable realized to implied spreads, but also low implied at the same time" — rare and short-lived (73:20–73:43). Warning: a low price "looks mouthwateringly cheap, but you just gotta respect the fact that it got that low" (32:22).
- Q5 (test a structure by shocking it): a client's 1-by-2 put spread sold as a hedge: "Let's shock prices down ... by x and vol up by x" — it was not a hedge (67:03).

### S23. Flirting with Models S4E6 — Angus Cameron (Liminal Capital; ex-Bankers Trust, Tudor), "Trade Structuring: Systematizing a Hidden Edge", 2021-06-07
URL: https://www.flirtingwithmodels.com/episodes/QTd278077Qx — full transcript. Label: [named practitioner]. [general, not options] (macro and futures; options appear only as structures).
- Q1/Q2 (name your edge first): four kinds — market access, speed, information, analytics. "do I have an edge, and what does my edge look like?" (18:20–18:57). At Tudor he had none of the first three: "By the time information hit me, it had basically exhausted its power." (20:55)
- Q2 (a strategy is a rule set): each strategy was "a series of trades that had the same entry, logic, structure, and exits" (28:39).
- Q6 (judge the idea and the trade separately): a 2-by-2 of good or bad prediction against good or bad trade; "sometimes you can be right and lose money, and sometimes you can be wrong and make money" (49:30–52:38).
- Q7/Q8 (what a review found): a colleague who watched him for two years said "I was right 60% of the time, but my trade entry and my trade management was terrible" (21:44). The fix was tighter stops and repeated entries, so the focus moved to payoff ratio over hit rate (22:20–23:10).
- Q6: "uncomfortable trading on any untested assumptions or heuristics" (58:17). Machine learning is "not necessarily the edge"; it "enhances whatever edge that you've developed" (42:09).
- Q8 (how long a prototype takes): the first agent took about eighteen months to build on E-mini S&P alone, then was tried on currencies and single stocks (36:38, 61:15–62:17).

### S24. Flirting with Models S6E14 — Devin Anderson (Convexitas; ex-Deutsche Bank derivatives structuring), "Strategy versus Structure in Tail Hedging", 2023-08-14
URL: https://www.flirtingwithmodels.com/episodes/UOAP6wBZT0R — full transcript. Label: [named practitioner]; also [seller] (sells option-overlay accounts).
- Q1/Q2 (three views before an options trade): a view on the underlying, on the structure, and on the option's price. "all good options trading has to start from biases in options prices" (42:12–43:49). The bias comes "in derivatives markets, mostly flows" — yield sellers, insurers, structured-product hedging (44:02).
- Q1 (an edge does not port): he refuses to run his S&P method on Russell or Nasdaq options because "the biases that are present in the S and P are completely different in those products" (45:06).
- Q5 (the hindsight trap in long-vol tests): COVID charts make the sale day look obvious, but "when you're standing in the middle of it, those monetization decisions are very, very hard" (52:23–52:37).
- Q5 (path dependence): calendar-rolled collars carry exposure that depends on expiry timing; a hedged-equity fund may hold only 40–80% delta (16:20–17:27).
- Q5 (why delta-hedged replication fails): Black-Scholes assumes continuous trading and slow news; "you're gonna be rethinking everything that you know at 01:59 on Fed announcement day" (59:40–60:43).
- Q7 (limits written in risk units): every strategy has "guardrails" — minimum and maximum market exposure, minimum and maximum convexity, plus scenario limits (40:30).

### S25. Flirting with Models S5E5 — David Sun (runs two small option-selling funds; electrical engineer, self-taught), "Expectancy Hacking", 2022-06-27
URL: https://www.flirtingwithmodels.com/episodes/QpdJve76shu — full transcript. Label: [unknown] (named; track record self-reported). Options-specific, SPX 0DTE premium selling, so close to Lalit's own study.
- Q1 (where he learned): tastytrade's free content "really accelerated my learning curve" (6:25). His thesis is the volatility risk premium alone, with no entry signal "by choice" (12:49, 34:01).
- Q2 (write the edge as an expectancy equation): expectancy depends on win rate, win size, loss size. Fix loss size with a stop, then choose a delta whose win rate beats the breakeven: "we fix the risk reward ratio and then design or enter trades that have a probability of winning higher" (14:38–16:53).
- Q5 (costs and stops in the backtest): "With slippage, your loss might become more like 2.2 or 2.3" against a 2.0 stop (20:45). In COVID the worst stop fills were 3.3–3.4 times credit (24:11). Fixed costs (wings, commissions, slippage) rule out smaller underlyings (40:11).
- Q5/Q7 (a sizing rule born from a live loss): COVID losses on large credits led to "credit targeting" — the same premium per trade, so high IV means fewer contracts or lower delta (26:15–28:48).
- Q7 (one yardstick across backtest and live): "premium capture rate", net P&L over premium sold; "as I'm live training or forward testing, it lets you gauge, am I above or below my typical expectancy" (18:15–19:32). On sizing: "you usually don't find your risk tolerance. It will find you" (32:35).
- Q6/Q8 (test a hunch against the records): FOMC days felt like losers, so "I finally pulled out our back test log and our live trade log"; the win rate was slightly lower, not enough to skip them — "we wanna be data led" (38:08–38:56).

### S26. Flirting with Models S4E1 — Cem Karsan (Kai Volatility / Aegea), "The Market Voting Machine", 2021-05-03
URL: https://www.flirtingwithmodels.com/episodes/bPhUORxdAP5 — full transcript. Label: [named practitioner]
- Q1/Q8 (an idea found by attributing your own losses): as an S&P market maker in 2007–10, trades put on with "a significant amount of edge" lost "more times than not ... And then you go do an attribution analysis and say, okay. Why is that?" The edge was leaking into skew and the distribution (8:48–9:27).
- Q1 (against data mining): "I couldn't have modeled or come up with these theories by just data mining, by looking at the data on hand." The qualitative pit experience came first, then the quantitative framework (9:27–10:21).
- Q3 (how the positioning data is built): flow from executing and prime brokers is tagged as dealer or customer and as hedge or not, then run through vol-surface models to estimate dealer gamma, vanna, charm, volga by expiry (14:18–14:49). This disagrees with Curnutt (S22), who doubts anyone can know how the other side is hedging.
- Q1 (market adages as hypotheses): sayings such as "never short a dull market" become testable claims about vanna and charm: "We can measure these and measure the flows" (17:38–22:29).

### S27. Flirting with Models S5E10 — Harel Jacobson (ex-prop FX and rates options trader; now derivatives research), "Trading FX Volatility", 2022-08-01
URL: https://www.flirtingwithmodels.com/episodes/TCrhgAEhKLB — full transcript. Label: [named practitioner]
- Q1 (where ideas come from, then and now): ten to fifteen years ago, the Wilmott and Nuclear Phynance forums and bank quant research notes; banks "stopped producing those", so now "I mostly read Twitter, Medium, and I listen to podcasts" (46:54–47:48).
- Q1 (who is forced to trade): his edge "comes from the fact that I understand the market players and how dealers run their exposure", in niche pairs — "a big fish in a small pond" (35:09).
- Q3 (bad data caught by a result that was too good): a wing-buying backtest made money, which should not happen; the vol series had been divided by 100 at one point. "just double check your prices every single time ... If it doesn't make sense, just dig into the data" (48:07–49:15).
- Q5 (fill assumptions): "I just factor in normal, bad, and horrific entry and exit points"; when a long-convexity trade is in profit, assume wider spreads (49:15–49:50). Live example: the model says exit at 20 vol, you exit at 15 "because market is 10 vol wide" (50:59).
- Q1/Q8 (an idea tested and found dead): implied event weights can be backed out of overnight vols; his research showed "you couldn't make money trading those events during the last two, three years" (43:05). One-off geopolitical events cannot be tested: "there is only one event" (44:15).
- Q8 (edges decay because you trade them): dealers repriced the vols he bought: "effectively, I improve the market. So now I need to find new edges" (36:36–37:01).

### S28. Flirting with Models S5E11 — Hari Krishnan (SCT Capital; author of *Market Tremors*), "Market Tremors & Tail Hedging", 2022-08-08
URL: https://www.flirtingwithmodels.com/episodes/MeUsl8ow3Z3 — full transcript. Label: [named practitioner]
- Q1 (finding the forced trader): "it's largely asking around" — ask banks what structured products sell and who buys them, then check where listed open interest clusters (21:05–21:18). Sell-side research disappointed him; "looking at all of the broker chats and all the flows ... is a rich source of ideas for concentration risk" (53:35–54:04).
- Q1 (screen, then explain): if S&P put skew looks too steep against history, either the true distribution is fatter or "there's some structural pressure that's pushing up the skew"; separate the two (21:56–22:46). Also compare notes with people in other markets, "not to copy their trades, but to see what they're seeing" (22:46–23:13).
- Q5/Q6 (what backtesting option structures taught him): "There was some scenario for any option strategy, even the silliest one, that pays out pretty nicely" — so he frames structure choice as a regime-dependent decision tree: put, put spread or put butterfly, and when (57:25–57:57).
- Q5 (monetising long options): mix tenors and strikes, take some profit and then be "increasingly patient"; work stops only on long-dated options, which reprice slowly (34:39–35:46).
- Q6 (a machine-learning trap): minimising model variance across data chunks makes a model learn "be long" for 2010–21, so train on weighted down periods or add constraints (60:22–61:07).
- Q7: clients ask for scenario payout matrices by horizon and move size; he gives them, but warns "too much rigidity in the process is not ideal" (50:00–50:52).
