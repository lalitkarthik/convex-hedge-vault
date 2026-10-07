> Lane qse-forums, 42 sources read, 2026-10-07

## Summary

1. Quant StackExchange (QSE) is strong on testing, weak on ideas. Its best answers on data snooping, sample size and out-of-sample tests date from 2011-2012 and come from people with verifiable jobs.
2. The clearest account of where ideas come from is a 2009 Elite Trader thread. The poster screens each idea for a reason it should work, such as forced flows. Then he tests each part against a null of randomness. Only then does he look at an equity curve.
3. Two practitioners begin from the same null: "assume the market is efficient, model what that looks like, then look for deviations."
4. On options, the forum pros agree that the edge is relative (one option against another) or that it is a premium paid for gap risk. They warn that an IV screen alone is not a hypothesis. In their view, IV means nothing until you compare it with RV.
5. The best options-research teaching in this lane is a NuclearPhynance thread. In it, a former junior quant describes his day-two drill: hedge one option by hand, find the breakeven vol, then separate gamma from vega.
6. Two 2026 QSE posts show the full loop on one idea. One takes an option-momentum paper, fixes the test in advance, fills at bid and ask, and gets a net Sharpe of 0.10. The other pre-registers an idea and writes up its rejection.
7. Synthetic option prices built from VIX, and mid-price fills, are the two traps named most often. Pros say both invent edges that never existed.
8. Notebooks: the options forums say almost nothing. General threads agree on one sequence: explore in the notebook, move repeated code into a module, and restart-and-run-all before you share. One part-time options trader keeps his whole backtest in a single notebook.
9. On going live, people disagree. One side says only live trading is free of data snooping. Others prescribe a step-up path: simulator, then small size, then scale. One adds control charts: compare live trade returns against the backtest's mean and standard deviation.
10. Wilmott's forum and NuclearPhynance were mostly unreachable (captcha, refused connection). QuantNet is careers talk, and Hacker News is general rather than options. Elite Trader and QSE carry the lane.

Terms used below: **data snooping** means reusing the same data to choose among many models, so one wins by chance. **Pre-registration** means writing down the test and the pass mark before looking at results. **Walk-forward** means fitting on a rolling past window and testing on the next window. **VRP** is the volatility risk premium (implied above realised on average). **SSR** is the skew stickiness ratio. **OPRA** is the US consolidated options quote feed.

## 1. Where hypotheses come from

**Market structure and forced flows.**
- An Elite Trader trader begins with "is there a reason this idea should work?", meaning market structure or economics. His example is index funds that must sell an S&P 500 deletion before the effective date. https://www.elitetrader.com/et/threads/how-to-research-and-verify-trading-ideas.181368/ (2009-11-03). "I'm very reluctant to trade something that I can't understand a reason for." `[anonymous, credible]` (talontrading; says 15 years in the business, runs a team, sells nothing.)
- The same poster explains who pays. A pension fund buying size does not care that you buy ahead of it. https://www.elitetrader.com/et/threads/how-to-research-and-verify-trading-ideas.181368/ (2009-11-03). "you are wrong to assume someone takes the other side of your trade." `[anonymous, credible]`
- An anomaly persists for one of two reasons: it carries hidden risk, or limits to arbitrage (borrowing, attention, computation) keep arbitrageurs out. https://quant.stackexchange.com/questions/1895 (accepted, score 21, 2011-10-14, Ryogi, rep 3,470). "An anomaly might persist because there are limits to arbitrage". `[unknown]`
- Some anomalies survive because big funds cannot trade them. Turn-of-the-month is the example. https://quant.stackexchange.com/questions/1895 (score 18, 2011-09-12, vonjd, Holger von Jouanne-Diedrich, professor; rep 28,179). "many anomalies didn't exist in the first place". `[academic]`
- In options firms, ideas also come from exchange mechanics. Examples: private fill acknowledgements that arrive before public data, and broker IDs (MPIDs) that show which market maker you traded with. https://quant.stackexchange.com/questions/61549 (accepted, score 11, 2021-03-07, databento, rep 2,755). "smaller options trading firms might simply follow a large market maker like Optiver on the rolls." `[seller: market data]`

**Start from the efficient market and look for the gap.**
- One process begins from the premise that the market is perfectly efficient. You model what efficiency looks like, then backtest whether reality departs from the model. When it does, you first suspect your own assumptions. https://news.ycombinator.com/item?id=34771269 (2023-02-13, Kranar; says he founded a trading company in 2012; arbitrage, market making, events). "every strategy starts from the premise that the market is perfectly efficient". `[anonymous, credible]` `[general, not options]`
- Elite Trader's talontrading uses the same null in his statistics: "every pattern ... is first assumed to be random." https://www.elitetrader.com/et/threads/how-to-research-and-verify-trading-ideas.181368/ (2009-11-03). `[anonymous, credible]`

**Papers.**
- A QSE reading list of academic option-strategy backtests includes Doran, Szado's collars and Kapadia-Szado's buy-write. The answerer also replicated Stutzer's "backtest Madoff" paper in R. https://quant.stackexchange.com/questions/1391 (accepted, score 23, 2011-07-11, vonjd). "You could do some backtests on your own with freely available data". `[academic]`
- A second list from the same thread works as a bank of screens. It covers IV against RV in the cross-section, risk-neutral skew, option-return momentum, weekend effect and dispersion. https://quant.stackexchange.com/questions/1391 (score 11, 2011-07-22, Tal Fishman, rep 13,739). `[unknown]`
- Skew trading built straight from a paper's definition: the Bakshi-Kapadia-Madan model-free implied skewness, tested by Bali-Murray. https://quant.stackexchange.com/questions/2079 (accepted, score 19, 2011-10-03, Tal Fishman). `[unknown]`
- A hypothesis from a model's prediction: Bergomi says the short-dated SSR is about 2, while the realised ratio is lower, so he trades a hedged risk reversal. https://quant.stackexchange.com/questions/59457 (q score 20, 2020-11-18). `[unknown]`
- Firms "hire people who can read the latest investment research, form a hypothesis and test" it. https://news.ycombinator.com/item?id=16923660 (2018-04-25, thisisit). `[unknown]` `[general, not options]`

**Ratio and statistic screens.**
- Two screens over 40-50 liquid ETFs:
  - 30-day IV beyond its 95th or 5th percentile, checked against HV volatility cones;
  - the 30-vs-90-day ATM IV term-structure slope beyond its percentiles.

  https://www.elitetrader.com/et/threads/the-first-step-for-the-pros-only.237122/ (2012-02-21, Cren1, says "not a pro"). "This time series very often bounces from a floor to a cap". `[unknown]`
- A good option seller knows each name's skew by month and by strike, and sells when it jumps. https://www.elitetrader.com/et/threads/the-first-step-for-the-pros-only.237122/ (2012-02-21, rmorse, Robert Morse, long-time ET options broker). "Option prices over time tend to be too high." `[seller: brokerage]`
- A pro's warning: a high-IV screen without RV is a trap. MARA's realised vol was 300 %, and size limits apply. https://www.elitetrader.com/et/threads/backtest-results-with-neutral-options-strategies-on-stocks-with-highest-implied-vola.377672/ (2023-12-30, destriero). "MARA has 300% RV." `[anonymous, credible]`
- High IV can be high for a reason: an informed buyer may be on the other side. https://www.elitetrader.com/et/threads/trading-options-how-to-have-an-edge.286459/ (2014-09-13, butterfacetrader). `[unknown]`

**Relative value and desk experience.**
- The usual option edge is relative, one option against another, and it differs from a strategy edge. https://www.elitetrader.com/et/threads/trading-options-how-to-have-an-edge.286459/ (2014-09-12, SIUYA). "Option prices are relative to other option prices --- that is usually where an 'edge' is." `[anonymous, credible]`
- One former bank options trader says the most successful traders are relative-value traders and market makers. He also says his bank strongly preferred long vol and long gamma, which contradicts rmorse's short-vega view above. https://www.elitetrader.com/et/threads/the-first-step-for-the-pros-only.237122/ (2012-02-21, newwurldmn). "My bank had a very STRONG preference to being long vol/gamma." `[anonymous, credible]`
- A former junior quant lists where strategies come from:
  - short gamma across 100+ names;
  - then buying back index gamma (dispersion);
  - then directional vega.

  https://nuclearphynance.com/Show%20Post.aspx?PostIDKey=186515 (2018-05-08/09, ronin, member since 2006). "It's up to you to come up with your own strategies." `[anonymous, credible]`
- Pros swap ideas in an invite-only, unpaid Telegram vol chat of 35 people. https://www.elitetrader.com/et/threads/backtest-results-with-neutral-options-strategies-on-stocks-with-highest-implied-vola.377672/ (2023-12-30, destriero). `[anonymous, credible]`
- Some traders use no scanners. They study a small core of underlyings deeply. https://www.elitetrader.com/et/threads/the-first-step-for-the-pros-only.237122/ (2012-02-21, spindr0, opt789). `[unknown]`

**Sources they warn against.**
- Most arXiv/SSRN papers are worthless to a practitioner, so triage by the abstract. https://quant.stackexchange.com/questions/82511 (comment score 5, 2025, Dimitri Vulis, rep 14,909, says he worked at a large bank). "Much of it is totally worthless". `[anonymous, credible]`
- A disagreement on the same page. Tidblom says read papers, but only to answer a set question, because authors exaggerate (score 7): "don't read just for the sake of reading." KaiSqDist (score 3) says skip papers and read textbooks. https://quant.stackexchange.com/questions/82511 (2025). `[unknown]`
- Retail content as a source: a Seeking Alpha diagonal idea "Sounds good in theory, not so in practise." https://www.elitetrader.com/et/threads/creating-synthetic-option-prices-for-backtest.372787/ (2023-02-22). A tastytrade straddle study could not be reproduced: 31 of 56 winners against their claimed 42 of 56. https://www.elitetrader.com/et/threads/my-backtest-results-different-than-tastytrade.298259/ (2016-03-04). `[unknown]`
- Technical indicators: talontrading "haven't been able to verify a statistic edge to those indicators". https://www.elitetrader.com/et/threads/how-to-research-and-verify-trading-ideas.181368/ (2009-11-02). Another poster says "If someone says their algorithm relies on some sort of TA, run for the hills." https://news.ycombinator.com/item?id=16923660 (2018). `[anonymous, credible]` / `[unknown]`

## 2. From idea to testable statement

- A three-step written screen. (1) Is there a reason the idea should work? (2) Test each piece separately for statistical evidence against randomness. (3) Only then draw "as if" equity curves. The steps are iterative and done with other traders. https://www.elitetrader.com/et/threads/how-to-research-and-verify-trading-ideas.181368/ (2009-11-03). "it helps to have other traders around to bounce ideas off of." `[anonymous, credible]`
- The scientific method, with the P&L held back until the effect is measured. https://quant.stackexchange.com/questions/147 (score 13, 2011-02-07, Paul Young, rep 231). "Step away from the P&L!" `[unknown]`
- Name who pays. The VRP is "compensation for taking on unhedgeable risks", namely "gap events mostly". https://www.elitetrader.com/et/threads/is-trading-implied-vol-the-real-edge-here-and-anything-directional-has-no-edge.375825/ (2023-08-20, newwurldmn). `[anonymous, credible]`
- A big apparent arbitrage always had a cause, such as halted withdrawals, fees or a slow venue. https://news.ycombinator.com/item?id=16925917 (2018-04-25, simonhughes22). "If there's a big price differences there's always a reason". `[unknown]` `[general, not options]`
- Split the bet into its P&L sources before testing. A skew trade has three: the slope change, the vol realised across strikes, and the implied vol met at the new strike. Vanilla structures cannot separate them. https://quant.stackexchange.com/questions/2079 (score 10, 2012-11-26, Strange, rep 750, says he runs skew strategies). `[anonymous, credible]`
- A model artefact can pass for an edge. Under rough volatility, an SSR below 2 is expected. https://quant.stackexchange.com/questions/59457 (score 2, 2025-10-31, Frido, rep 3,910). "may not be an arbitrage at all if vol is rough." `[unknown]`
- A full pre-specified test of a paper idea (option momentum, Heston et al. JF 2023). The universe, dates, structure, hold, formation window, fill rule, commissions, liquidity screens and data were all fixed before running. Result: net Sharpe 0.0963 over 138 months. https://quant.stackexchange.com/questions/85743 (2026-08-01, ALi Saleh, rep 11). "Setup was fixed in advance". `[unknown]`
- Pre-registered hypotheses, an explicit cost model, and a written rejection. A 1-2 bp reversal against a 6.5 bp round trip killed the idea. https://quant.stackexchange.com/questions/85730 (2026-07-26). "I consider the original hypothesis rejected." `[unknown]` `[general, not options]`
- Meucci's "The Prayer", a ten-step checklist for modelling a P&L distribution. https://quant.stackexchange.com/questions/3225 (score 3, 2012-04-12, vonjd). `[academic]`

## 3. Data

- **Synthetic prices from VIX invent edges.** VIX overstates vol because of skew, and a monthly vol cannot price weekly event vol. https://www.elitetrader.com/et/threads/creating-synthetic-option-prices-for-backtest.372787/ (2023-02-23, newwurldmn). "Your extrapolation will be dumb and you find opportunities that wouldn't have existed." The asker's own check confirmed it: the synthetic series drifted upward. `[anonymous, credible]`
- Use real historical option prices and back out implied vols. Do not use Black-Scholes with VIX. https://quant.stackexchange.com/questions/3210 (accepted, score 5, 2012-04-08). `[unknown]`
- **OptionMetrics.** Index and option closes are not simultaneous, because options close 15 minutes later. The method changed on 2008-03-05 (from end-of-day prices to bid/offer near 4 pm). https://quant.stackexchange.com/questions/41762 (2018-09-17). The vendor's American early-exercise adjustment "is a bit of a blackbox" (accepted, score 8, phdstudent, rep 9,366). `[academic]` / `[unknown]`
- **Cleaning an IV surface.** First apply hard filters: zero, locked or crossed quotes, stale settlements, prices near intrinsic. Then enforce no-arbitrage in price or total-variance space, and repair with an arbitrage-free fit such as SVI/SSVI. https://quant.stackexchange.com/questions/85513 (accepted, score 3, 2026-04-16, carry_and_pray, rep 96). "The first pass should be hard quote filters and not statistical outlier filters." `[unknown]`
- Missing deep in-the-money quotes reflect the market, not a data fault, because liquidity sits in OTM options. https://quant.stackexchange.com/questions/7777 (2019-08-12, demully, rep 5,241). `[unknown]`
- Point-in-time data: you need when an item happened and when you could act on it. https://quant.stackexchange.com/questions/147 (score 12, 2011-02-03, chrisaycock, Chris Aycock, quant firms, rep 9,967). "a good data warehouse will be bitemporal or point-in-time." `[named practitioner]`
- Full option chains are not free, so practitioners build their own. "First focus on the data." https://quant.stackexchange.com/questions/27793 (accepted, score 3, 2016-06-28, Ariel Silahian). Another answer advises starting to collect early. https://quant.stackexchange.com/questions/27793 (score 4, 2020-05-30, jason m). `[unknown]`
- Cost of data: "maybe a couple ten thousand for a good dataset". https://quantnet.com/threads/individual-retail-quant.59345/ (2024, MikeLawrence). `[unknown]`
- Free, 15-minute-delayed data will not carry an intraday edge. https://quant.stackexchange.com/questions/85734 (score 4, 2026-07-30, del_nabla, says he works in the industry). `[unknown]`
- Versioned ("time travel") storage gives point-in-time copies of revised series and an audit trail of how backtest results changed. https://news.ycombinator.com/item?id=41309997 (2024-08-25, jjmunro, James Munro, Man Group ArcticDB). A long-time user disagrees (blitzar, 5+ years): he never used versioning and reprocesses from raw data "as of date". `[named practitioner]` `[general, not options]`
- Renaissance "employ several PHDs to just clean data" (per Nick Patterson). https://quant.stackexchange.com/questions/85456 (accepted, score 5, 2026-02-05, AKdemy, rep 11,126). `[anonymous, credible]`

## 4. Notebooks

The options forums in this lane say almost nothing about notebook layout. Most of the findings below are `[general, not options]`.

- One part-time options trader keeps his entire backtest in "a Jupyter Notebook crunching data I've collected over the years". https://news.ycombinator.com/item?id=34791160 (2023-02-14, Shocka1). `[unknown]`
- The options drill starts before any notebook: a spreadsheet. Hedge one option daily at a flat vol, then vary the vol to find the breakeven. Then over- and under-hedge, separate gamma from vega, and add term structure and skew. "At one point, you'll probably move from Excel to something else." https://nuclearphynance.com/Show%20Post.aspx?PostIDKey=186515 (2018-05-03, ronin). "that was an actual exercise they made me do on my second day." `[anonymous, credible]`
- Explain the backtest's P&L by Greek before you add complexity. https://quant.stackexchange.com/questions/27793 (score 4, 2020-05-30, jason m). "Find ways to explain your PnL to yourself in the backtest". `[unknown]`
- A vol backtest setup cannot easily be efficient, flexible and easy to use all at once. https://nuclearphynance.com/Show%20Post.aspx?PostIDKey=186515 (2018-05-08/09, Strange; ronin replies). "it's easy to get any 2 out of these three things" / "1 out of 3 is hard enough". `[anonymous, credible]`
- Research code is mostly thrown away, and the conclusion is the product. https://quant.stackexchange.com/questions/1966 (2011-09-20, asker). "once I have reached a conclusion, that code is not really needed any more." Replies there:
  - A three-person shop uses GitHub, static checks and code review. A former team ran three-week cycles: research, then build, then integration (score 8, Steve Severance).
  - Version-control even throwaway code (accepted, score 7, wburzyns). `[anonymous, credible]` / `[unknown]`
- When code moves out of the notebook: play in the notebook, turn cells into functions, then turn functions into a module. https://news.ycombinator.com/item?id=17857904 (2018-08-28, Certhas). "Notebooks excel as ad hoc interfaces to libraries and modules." `[unknown]`
- A seven-part notebook layout: imports, own modules, parameters, data loaders, settled analysis functions, a "main" cell, working cells. Code used twice goes to a module. https://news.ycombinator.com/item?id=17857976 (2018-08-28, Mvandenbergh). `[unknown]`
- Reproducibility: restart the kernel and run all cells before sharing. https://news.ycombinator.com/item?id=17857272 (2018-08-28, teekert). RMarkdown renders from a clean environment and keeps old notes as a design document. https://news.ycombinator.com/item?id=17858717 (dracodoc). `[unknown]`
- **Against notebooks.** If your workflow is "run cells until I get to the one I'm working on", stop and build it properly. https://news.ycombinator.com/item?id=17857329 (2018-08-28, FridgeSeal). "Notebooks are fine for early stage experimenting". Another prefers the REPL and exports its history. https://news.ycombinator.com/item?id=17858441 (daveguy). `[unknown]`
- **For notebooks as a record.** One user can reopen work from years ago and see what he did, "mistakes and all". https://news.ycombinator.com/item?id=17858730 (analog31). `[unknown]`
- A fund's view of tooling: quants pull in-memory DataFrames and use pandas, Polars or DuckDB. "Python is a tool for Quants not a career." https://news.ycombinator.com/item?id=41345892 (2024-08-25, jjmunro). A quant-fund CTO says versioned DataFrame storage helps attract "productive quant researchers". https://news.ycombinator.com/item?id=41346291 (nzjrs). `[named practitioner]` / `[anonymous, credible]`
- AI-written notebook code: an assistant told to use a window from t-N to t-1 silently included t. https://quant.stackexchange.com/questions/85456 (2026-02-05, William Wang). "you often cannot tell from a backtest result alone". `[unknown]`

## 5. The backtest

- **The ronin method.** Buy the actual option and track inventory. Delta-hedge daily, mark option, hedge and cash at mid, and settle at expiry. Use the surface as it actually was each day. https://nuclearphynance.com/Show%20Post.aspx?PostIDKey=186515 (2018-05-01). "If you think backtesting options is hard, wait till you start trading them..." `[anonymous, credible]`
- **Disagreement.** For skew strategies your assumed surface dynamics (sticky strike or sticky delta) set your delta, so they belong in the backtest. https://nuclearphynance.com/Show%20Post.aspx?PostIDKey=186515 (2018-05-04, Strange). `[anonymous, credible]`
- An alternative: Monte Carlo over historical joint daily changes in spot, rates, vol and time, with P&L attributed by Greek plus a nonlinear residual. Delta-hedged P&L is path-dependent: variance realised where you hold no gamma does not pay. https://nuclearphynance.com/Show%20Post.aspx?PostIDKey=186515 (2018-04-29/05-05, day1pnl). `[anonymous, credible]`
- **Fills.** Mid-price fills are unrealistic in options; use the worst price. Market makers move IV against size. https://quant.stackexchange.com/questions/16538 (score 2, 2015-03-08, Nathan S.). "Use the worst pricing assumption on this". `[unknown]`
- Option momentum at ask-in and bid-out fills, with $0.65 commission: Sharpe 0.0963. https://quant.stackexchange.com/questions/85743 (2026-08-01). A reply argues that daily delta re-hedging adds the underlying spread about 20 times a month, so hedging makes it worse; it cites Muravyev (2016) on anomalies that vanish with real quotes (score 0, 2026-08-18, Russlan Ramdowar). "mid quotes are academic fantasy land". `[unknown]`
- A gamma-scalping backtest without tick data: split P&L into scalping gains, vega gains and theta losses using RV and historical IV. https://www.elitetrader.com/et/threads/is-it-possible-to-backtest-an-gamma-scalping-strategy.133004/ (2008-07-31, IV_Trader). "You need to break your PnL into 3 parts". `[unknown]`
- Wrong forwards cost about 5 % a year, and dividends matter. Run everything in vol space off a surface. https://www.elitetrader.com/et/threads/creating-synthetic-option-prices-for-backtest.372787/ (2023-02-22, newwurldmn). `[anonymous, credible]`
- **Backtest and live code.** One view: give backtest and live the same interface so strategy code is reused, and accept that a backtest need not give accurate P&L. https://quant.stackexchange.com/questions/70829 (accepted, score 5, 2022-05-10, databento). The opposing view: keep a fast research backtester separate from a safe live trader, "quantity over quality" (score 0, 2023, nanvel). `[seller: market data]` / `[unknown]`
- A serious backtester simulates queue position and runs parallel market-impact scenarios to find the worst case. https://news.ycombinator.com/item?id=34771269 (2023-02-13, Kranar). `[anonymous, credible]` `[general, not options]`
- A strategy is signals, execution, risk and infrastructure, and outsiders over-focus on signals. https://news.ycombinator.com/item?id=16929156 (2018-04-26, imcoconut). "The entire strategy is only as good as its weakest link." `[unknown]` `[general, not options]`
- Professionals backtest options on OneTick or KDB; retail traders use broker tools. https://quant.stackexchange.com/questions/74 (accepted, score 17, 2011-02-01, Shane, quant researcher and the QSE site's proposer, rep 9,415). Later answers in that thread are mostly vendor posts. `[anonymous, credible]`

## 6. Checks against fooling yourself

- **Data snooping is multiple testing.** A hold-out sample does not cure it when many models are tried. Read Benjamini-Hochberg first, then White's Reality Check and Romano-Wolf. https://quant.stackexchange.com/questions/140 (accepted, score 23, 2011-02-05, gappy, Giuseppe Paleologo). "implicitly multiple tests of hypothesis are being run at the same time." `[named practitioner]`
- Other answers in the same thread:
  - Hansen's SPA test (shabbychef, former ML quant, score 10).
  - Fewer degrees of freedom; parameters where the error changes sharply mean overfitting (Shane, score 19).
  - Test sub-periods (Richard Herron, score 7).
  - Compare against random trades (Patrick Burns, Portfolio Probe software, score 7): "the only non-datasnooping method there is is to trade live." `[seller]`
- **Size the test before running it.** n = (2·s·α/Δ)². His live market-making model needed 3,458 trades; a Sharpe-3, 1.5 %-a-month model needs 45 months. https://quant.stackexchange.com/questions/1891 (accepted, score 50, 2011-09-13, chrisaycock). "I was trading live and I couldn't be too choosy with money on the line." Correlated names are not independent observations (score 4, Michael WS). `[named practitioner]`
- **A hold-out sample is used up once you look at it.** Aronson, quoted by vonjd: "It is lost as soon as it is used one time." Chan suggests roughly equal halves. https://quant.stackexchange.com/questions/1480 (accepted, score 10, 2011-07-22). `[academic]`
- **Is walk-forward out-of-sample? They disagree.**
  - No: if you edit the model after seeing walk-forward P&L, that data is validation, not out-of-sample. Keep a hold-out and score it only a few times. https://quant.stackexchange.com/questions/50806 (accepted, score 5, 2020-02-01, Jacques Joubert, Hudson & Thames, which sells the mlfinlab library). "Backtesting is not a research tool - Feature importance is." (quoting López de Prado). `[seller: ML library]`
  - Yes: vonjd called it time-series cross-validation, so out-of-sample (score -1, voted down).
  - It is fine with enough data: "Walk forward is good. But fitting using small amounts of data is crazy." https://www.elitetrader.com/et/threads/your-thoughts-on-walk-forward-testing-to-assess-robustness.339240/ (2020-01-05, globalarbtrader, signs "GAT"; widely taken to be Rob Carver, not verified here). `[anonymous, credible]`
  - It is overrated: walk-forward "isn't at all what it's cracked up to be". https://www.elitetrader.com/et/threads/how-to-research-and-verify-trading-ideas.181368/ (2009-11-03, talontrading). `[anonymous, credible]`
  - It is useless: "as useless as backtest" (richDude, same 2020 ET thread). `[unknown]`
  - If even the final 20 % decides whether you keep the model, only real time proves it. https://quant.stackexchange.com/questions/737 (accepted, score 7, 2011-03-17, bill_080). `[unknown]`
- **Report every trial.** Cross-validation would work if all K trials were published; hiding them "amounts to p-hacking". https://quant.stackexchange.com/questions/65539 (score 8, 2021-06-14, Jase). `[unknown]`
- **Eckhardt's five tests**: overfitting, post-dictiveness, maldistribution of returns, statistical artefacts, non-repeatable circumstances. Add a position-permutation test (null: positioning no better than random) and a "torture test" that worsens entries and exits. https://quant.stackexchange.com/questions/3225 (q score 20, 2012; babelproofreader, score 5). `[unknown]`
- **Pre-registration in industry.** One fund made traders submit models weeks before production, then re-backtested them without hindsight. https://quant.stackexchange.com/questions/147 (score 12, 2011-02-03, chrisaycock). "required traders to submit their models weeks before production". `[named practitioner]`
- **Pre-registration by an individual** (2026). He kept datasets of accepted and rejected signals, separated decision-time features from labels, used a session block bootstrap, and validated on an independent period. https://quant.stackexchange.com/questions/85730. One reply labels its own best number as in-sample: "we publish it labeled that way." Another found a profit factor of 2.25 was a fluke of the parameter grid. "The stuff that held up had fewer knobs and traded less." `[unknown]` `[general, not options]`
- **Replicate a known result to test your own code.** https://www.elitetrader.com/et/threads/my-backtest-results-different-than-tastytrade.298259/ (2016-03-04, Shay). "the best way to do that, is to take known results and see if i get similar results". A published study may be the best of hundreds of runs (botpro). `[unknown]`
- **Distrust a deviation first.** https://news.ycombinator.com/item?id=34771269 (2023, Kranar). "we are very skeptical when our backtesting deviates from our model." `[anonymous, credible]`
- **Review by a colleague.** "code reviews more than anything else lead to better code." https://quant.stackexchange.com/questions/1966 (2011-09-21, Steve Severance). The biggest risk is you: "Knowledge leads to profit BUT NOT the reverse." https://quant.stackexchange.com/questions/147 (Paul Young). `[anonymous, credible]` / `[unknown]`
- Every risk on one list is one the answerer has hit himself. https://quant.stackexchange.com/questions/147 (score 43, 2011-02-03, pteetor, Paul Teetor, quant developer and author). "This is not a theoretical list. I've made all these mistakes personally." `[named practitioner]`

## 7. From a passed test to real money

Options-specific material here is thin. Most findings are `[general, not options]`.

- **The step-up path:** simulator, then live at very small scale, then scaling over time. https://news.ycombinator.com/item?id=34771269 (2023, Kranar). `[anonymous, credible]`
- **Control charts.** Keep the backtest's mean and standard deviation of trade returns. Watch for many trades beyond ±3 s.d. Compare recent, longer-run and backtest statistics. https://www.elitetrader.com/et/threads/how-to-research-and-verify-trading-ideas.181368/ (2009-11-03, talontrading). "kind of like manufacturing processes keep control charts." `[anonymous, credible]`
- Stop live trading when returns run above the backtest's thresholds, or when there are too many wins in a row. Paper-trade until the numbers fall back in range. https://news.ycombinator.com/item?id=34771054 (2023, smdz). `[unknown]`
- Build tests that let you drop a model "at the first sign of trouble". https://quant.stackexchange.com/questions/737 (2011, bill_080). `[unknown]`
- Measure costs from your own fills. One trader compared 125 real fills against the close and found his guess was too pessimistic. A grid-search winner lost on paper and was shut off. https://quant.stackexchange.com/questions/85730 (2026-08-02, Chris, rep 11). `[unknown]`
- Psychology breaks the live test. One trader lost about $100k after cutting trades short because he did not trust the algorithm. https://news.ycombinator.com/item?id=16923294 (2018, pfarnsworth). "algo trading is mostly psychological". `[unknown]`
- Options voice: "You won't know if it's an edge until after you're out!" https://www.elitetrader.com/et/threads/is-trading-implied-vol-the-real-edge-here-and-anything-directional-has-no-edge.375825/ (2023-08-20, destriero). `[anonymous, credible]`
- Expect live profits to be a fraction of simulated ones, and expect every idea to have a half-life. https://quant.stackexchange.com/questions/147 (pteetor). `[named practitioner]`

## 8. Records and killing ideas

- **Most ideas die.** "you'll dump far more models than you'll keep." https://quant.stackexchange.com/questions/737 (2011-03-17, bill_080). `[unknown]`
- **Kill, do not rescue.** "DO NOT adjust the hypothesis to explain the data the previous one failed on." https://www.elitetrader.com/et/threads/your-thoughts-on-walk-forward-testing-to-assess-robustness.339240/ (2020-01-05, gaussian). The QSE 85730 asker writes up his rejection and refuses to retune. https://quant.stackexchange.com/questions/85730 (2026). `[unknown]`
- **An options trade log.** For each trade, record strategy, underlying, plan, edge, management rule, and a result of "win, lose, or learn". https://www.elitetrader.com/et/threads/trading-options-how-to-have-an-edge.286459/ (2014-09-13, traderlux). `[unknown]` destriero kept a public "dest everything journal" of trades (2023, S36 thread above). `[anonymous, credible]`
- Keep even dead research code in version control. https://quant.stackexchange.com/questions/1966 (2011, wburzyns). `[unknown]`
- **How long one idea takes.** An intern produced the index add/drop statistics in under a week. https://www.elitetrader.com/et/threads/how-to-research-and-verify-trading-ideas.181368/ (2009-11-03). "it took an intern less than a week to crank out the numbers". `[anonymous, credible]` At the other extreme, one team spent 22 months on 19 research architectures and "thousands of hypotheses" without finding a provable edge. https://quant.stackexchange.com/questions/85734 (2026-07-29). `[unknown]`
- Learning options, by contrast, takes months: "These are all quite hard problems that may take you months to solve." https://quant.stackexchange.com/questions/27793 (2020, jason m). `[unknown]`
- Use the notebook or RMarkdown file as the research record (S28 above: analog31, dracodoc). `[unknown]` `[general, not options]`

## Hypothesis sources, ranked

| Source of ideas | Practitioners in this lane who named it | Strongest link |
|---|---|---|
| Papers and the academic literature | 6 (vonjd, Tal Fishman, thisisit, ALi Saleh, Bergomi-SSR asker, talontrading citing index-change papers); 3 warn (Vulis, Tidblom, Ramdowar on mid-quote results) | https://quant.stackexchange.com/questions/85743 |
| Market structure, forced flows, limits to arbitrage | 5 (talontrading, Ryogi, vonjd, databento, Kranar) | https://www.elitetrader.com/et/threads/how-to-research-and-verify-trading-ideas.181368/ |
| Ratio screens (IV percentile, IV vs HV cones, term-structure slope, skew per name, VRP) | 4 (Cren1, rmorse, destriero, Tall Mike); 2 warn that IV alone misleads (destriero, butterfacetrader) | https://www.elitetrader.com/et/threads/the-first-step-for-the-pros-only.237122/ |
| Relative value: one option against another, dispersion | 3 (SIUYA, newwurldmn, ronin) | https://nuclearphynance.com/Show%20Post.aspx?PostIDKey=186515 |
| Desk experience and mentor drills | 2 (ronin, newwurldmn) | https://nuclearphynance.com/Show%20Post.aspx?PostIDKey=186515 |
| Peers: other traders, chats, Discords | 3 (talontrading, destriero, Andy Nguyen) | https://www.elitetrader.com/et/threads/backtest-results-with-neutral-options-strategies-on-stocks-with-highest-implied-vola.377672/ |
| A model's prediction tested against realised data | 2 (Bergomi-SSR asker, Kranar) | https://quant.stackexchange.com/questions/59457 |
| Retail media and vendor studies (Seeking Alpha, tastytrade) | 2 used them, and both failed to hold up (Zwaen, Shay) | https://www.elitetrader.com/et/threads/my-backtest-results-different-than-tastytrade.298259/ |
| Technical indicators, pattern mining | 0 recommend; 3 warn (talontrading, thisisit, Tall Mike's "mixed bag") | https://www.elitetrader.com/et/threads/how-to-research-and-verify-trading-ideas.181368/ |

## Ten sources worth reading in full

1. https://nuclearphynance.com/Show%20Post.aspx?PostIDKey=186515 — ronin, Strange and day1pnl, all veterans with long posting records. A complete beginner's path for backtesting delta-hedged options, with a real disagreement on surface dynamics.
2. https://www.elitetrader.com/et/threads/how-to-research-and-verify-trading-ideas.181368/ — talontrading. The three-step idea screen, forced flows as the source of edge, and control-chart monitoring (pages 1-10).
3. https://quant.stackexchange.com/questions/140 — Giuseppe Paleologo and others. The shortest correct statement of data snooping as multiple testing.
4. https://quant.stackexchange.com/questions/1891 — Chris Aycock. How many trades you need before you believe a result, with a live example.
5. https://quant.stackexchange.com/questions/147 — Paul Teetor, Chris Aycock and others. The risk list, plus a fund that pre-registered models before production.
6. https://quant.stackexchange.com/questions/85743 — A 2026 fill-level replication of an options-momentum paper, fixed in advance; it shows how a paper idea dies at bid and ask.
7. https://quant.stackexchange.com/questions/85730 — A 2026 pre-registered test, a written rejection, and replies on measuring real fills and labelling in-sample numbers.
8. https://news.ycombinator.com/item?id=34771269 — Kranar, a firm founder. The "efficient market as null" process and the simulator-to-small-to-scale path.
9. https://www.elitetrader.com/et/threads/the-first-step-for-the-pros-only.237122/ — Actual option screens (IV percentile, term-structure slope, skew), and pros disagreeing on long vs short vol.
10. https://quant.stackexchange.com/questions/85513 — The cleaning order for an IV surface: hard filters, then no-arbitrage repair, never z-score deletion.

## Could not open

- https://forum.wilmott.com/viewtopic.php?t=78085 ("How to get somewhere with a trading strategy") and https://forum.wilmott.com/viewtopic.php?p=880449 ("Delta Hedging P&L"). The whole Wilmott forum returns a "Verify You Are Human" captcha to plain download, to a scraper and to the fetch tool. I did not try to get past it. Neither thread is in the Wayback Machine, and the archive holds no copies of the Trading Forum index (f=38). No Wilmott forum content is cited.
- https://nuclearphynance.com/Show%20Post.aspx?PostIDKey=155289 (a search snippet suggests it covers how many strategies fail live). The live NuclearPhynance site refused connections from every tool, and this post is not in the Wayback Machine. Only PostIDKey=186515 was read, via its 2019-06-17 Wayback copy.
- https://quantnet.com/threads/projects-in-quantitative-finance.51829/ and other QuantNet threads. Plain download hits a browser check; only one thread was read through the scraper. Search results showed QuantNet is mostly careers content.
- The Elite Trader thread 181368 has 62 pages; I read pages 1-6, 8 and 10, starter posts only. Threads 237122, 375825 and 339240 were read on page 1, or on page 1 plus selected posters.
- The Wayback availability API returned HTTP 429 (rate limit); I used direct `id_` snapshot URLs instead.
