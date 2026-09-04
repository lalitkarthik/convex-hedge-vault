# THE LANDSCAPE MAP — 24 fields, triaged

Legend for filter tests: **(1)** runnable code · **(2)** states costs/slippage/fills · **(3)** author traded/built it · **(4)** names its own failure modes *(counts double)* · **(5)** reproducible on obtainable data.

Verification note: every URL below was either returned by search this session or is a canonical repo/paper location I state confidence on. Where I could not verify, I say so explicitly rather than padding.

---

## A. OPTIONS & VOLATILITY (his core)

### 1. Arbitrage-free surface modelling (SVI / SSVI / local vol)
1. **What it is.** Parametric fitting of the implied vol surface subject to static no-arbitrage (butterfly, calendar) constraints, plus the Dupire/local-vol bridge. Output is a clean, interpolable, differentiable surface.
2. **Uniquely solves.** Every other options technique needs a surface that does not produce negative densities or fake calendar arbitrage at 09:20 when the chain is garbage. Nothing else gives you that.
3. **ALIVE as infrastructure, DECAYED as alpha.** Fitting SVI is not a trade and has not been one since roughly 2012. Where it is still alive: *intraday* refitting on minute data, quote-quality filtering, and detecting when the fit residual itself is the signal.
4. **Prereqs.** He has them. Infra: a tick-to-surface pipeline and a fast constrained optimiser. Capital: zero.
5. **Time-to-first-useful-result.** He's done it — so: 2-3 weeks to convert it from a research artefact into a minute-wise NIFTY surface service with residual diagnostics.
6. **Solo-viable.** Entirely.
7. **Sources.**
 - Gatheral & Jacquier, *Arbitrage-free SVI volatility surfaces* — arXiv:1204.0646. Passes (4)(5). Names exactly where SSVI's no-arb conditions bind and fail.
 - Zeliade Systems white paper, *Quasi-Explicit Calibration of Gatheral's SVI Model* (zeliade.com, ZWP-0005). Passes (1-adjacent)(4)(5) — gives the calibration failure geometry, not just the formula.
 - Colin Bennett, *Trading Volatility* — free full PDF at https://trading-volatility.com/Trading-Volatility.pdf. Passes (3)(4). Ex-Santander head of derivatives strategy; explicitly discusses where skew/term-structure trades stop working.
8. **WHY THIS MIGHT WASTE YOUR TIME.** You already did it, and a better surface fit has never by itself made anyone money — you are polishing a lens, not finding something to look at.

---

### 2. Volatility risk premium harvesting (short vol / systematic overwriting)
1. **What it is.** Selling implied vol against subsequently realised vol, systematically, with delta hedging or without. The single most documented positive-expectancy structure in options.
2. **Uniquely solves.** It is the only options "return stream" that is a compensated risk premium rather than a forecasting bet — it pays you for supplying insurance.
3. **DECAYED in the US, ALIVE and structurally distorted in India.** SPX VRP is the most crowded trade in the retail-adjacent world; 0DTE has compressed it. Indian VRP is *fatter* but the fat part is precisely the part that kills you (expiry-day gaps, event days, no borrow, wide fills). SEBI's own data: 91% of individual F&O traders lost money, ₹1.06 lakh crore net in FY25 — a large share of that is naive short vol.
4. **Prereqs.** Minimal maths. What you actually need is a margin model and a survival-through-drawdown design. Capital: this is the one field where being small hurts — SPAN margin on Indian index shorts is unforgiving.
5. **Time-to-first-useful-result.** 3-4 weeks to a cost-honest backtest. Years to know whether it survives.
6. **Solo-viable**, but the risk of ruin is the highest of anything on this list.
7. **Sources.**
 - CBOE PUT / BXM / CNDR index methodologies + full history (cboe.com/tradable_products/buywrite/). Passes (2)(5). The public benchmark that makes your alpha claim falsifiable.
 - SEBI, *Study on Profit and Loss of Individual Traders in Equity F&O* (FY24 & FY25). Passes (5) and effectively (4) — it is a census of failure modes with a cost decomposition. Verified via multiple 2025 reports; get the PDF from sebi.gov.in.
 - Moontower / Kris Abdelmessih — https://moontowermeta.com. Passes (3)(4) doubly: 21 years market-making at SIG and Parallax, and the writing is unusually explicit about when vol selling is unpaid.
8. **WHY THIS MIGHT WASTE YOUR TIME.** The edge is real, small, and levered; your backtest will show a beautiful Sharpe that is entirely a description of what has not happened yet.

---

### 3. Dispersion / correlation trading
1. **What it is.** Short index vol against long single-name vol (or vice versa), monetising the spread between index-implied and constituent-implied correlation.
2. **Uniquely solves.** It isolates *correlation* as a tradeable asset — no directional or single-name view survives the construction.
3. **ALIVE but institutional.** The classic short-index/long-singles leg is a genuine premium but requires many legs, cheap borrow, and portfolio margin. In India it is close to impossible: single-stock option liquidity outside the top ~15 names is a rounding error.
4. **Prereqs.** Correlation matrix estimation, vega-weighting schemes, and a margin engine. Capital: high — this is where solo dies.
5. **Time-to-first-useful-result.** 6-10 weeks to a paper study; the paper study will not be tradeable.
6. **Firm-only** at any meaningful size.
7. **Sources.**
 - Bennett, *Trading Volatility* — the dispersion chapters are the best free treatment in existence. Passes (3)(4).
 - Bossu, *A Practical Guide to Dispersion* / *Introduction to Variance Swaps* (JPMorgan, widely mirrored). Passes (3)(4). Verify the mirror you use; the original bank PDFs circulate without a stable canonical URL — I could not confirm one.
8. **WHY THIS MIGHT WASTE YOUR TIME.** You will build it, find it works on paper, and discover you cannot get filled on the 30 single-name legs at anything resembling mid.

---

### 4. Options market making (quoting, inventory, adverse selection)
1. **What it is.** Continuously two-sided quoting with inventory-aware skew, where P&L is edge-per-trade minus adverse selection minus hedging cost.
2. **Uniquely solves.** It is the only options activity where you are paid the spread rather than paying it — the sign of the cost term flips.
3. **ALIVE in crypto, DEAD to outsiders in Indian index options.** NSE index option quoting is a latency and colocation game against firms with sub-100µs stacks. Crypto options (Deribit) and crypto perps still have quotable, un-colocated corners.
4. **Prereqs.** Avellaneda-Stoikov and successors, queue models, real exchange connectivity, and enough capital to hold inventory. Colo for anything Indian.
5. **Time-to-first-useful-result.** 2-3 months on crypto testnet/small size. Never, for NSE.
6. **Firm-only for equities/index; solo-viable in crypto at small size.**
7. **Sources.**
 - Hummingbot — https://github.com/hummingbot/hummingbot. Passes (1)(2)(3)(5). Apache-2.0, ~16.9k stars, production-used; fee and slippage handling is explicit.
 - hftbacktest — https://github.com/nkaz001/hftbacktest. Passes (1)(2)(4)(5). Models queue position, feed *and* order latency, and fee models; the docs are candid that fill assumptions are the dominant error term.
 - Avellaneda & Stoikov (2008), *High-frequency trading in a limit order book*. Passes (4)(5). Read it for the reservation-price logic, not the parameters.
8. **WHY THIS MIGHT WASTE YOUR TIME.** Market making is 10% model and 90% infrastructure, ops, and exchange relationships — the part you enjoy is the part that matters least.

---

### 5. Options flow & dealer positioning (GEX, vanna, charm)
1. **What it is.** Inferring the dealer hedging book from open interest and trade-side classification, then predicting the mechanical hedging flow it forces.
2. **Uniquely solves.** It is the only framework that predicts *flow* — a forced, non-discretionary buyer or seller — rather than value.
3. **Half-DECAYED in the US, LARGELY UNEXPLORED in India.** SPX GEX is now a retail meme; the simple "long gamma = pinned" trade is crowded. India is the genuine opportunity: OI data is published, participant-wise category data (FII/DII/Pro/Client) is published daily by NSE, and almost nobody has built a serious dealer-book reconstruction on minute data.
4. **Prereqs.** Trade-side classification (the hard part — you must infer who is buying), OI reconciliation, and a surface for the greeks. Capital: low.
5. **Time-to-first-useful-result.** 4-6 weeks to a NIFTY dealer-gamma series on minute data. This is his single highest-leverage build.
6. **Solo-viable.** Yes — and the Indian version is genuinely under-served.
7. **Sources.**
 - SqueezeMetrics, *The Implied Order Book* — https://squeezemetrics.com/download/The_Implied_Order_Book.pdf. Passes (3)(4)(5). Verified live. The GEX construction plus honest admission of the sign-assignment assumption that makes or breaks it.
 - NSE participant-wise OI and F&O bhavcopy (nseindia.com archives). Passes (5). Free, daily, and the raw material for the India version.
 - Volland white paper — https://vol.land/VollandWhitePaper.pdf (surfaced this session; treat as *partially verified*, I did not read it in full). Covers dealer-flow impact on equity returns.
8. **WHY THIS MIGHT WASTE YOUR TIME.** The whole edifice rests on guessing which side of each trade the dealer took; get that classification wrong and you have built a very sophisticated random number generator.

---

### 6. Event-driven volatility (earnings, macro prints, expiry)
1. **What it is.** Trading the term-structure kink around a scheduled event: implied vol embeds an event premium that decays deterministically once the event passes.
2. **Uniquely solves.** It gives a *dated*, non-stationary edge with a known catalyst — the only options trade where you know in advance when you find out if you were right.
3. **ALIVE.** Earnings vol crush is durable in the US mid-cap tail; Indian equivalents (RBI policy, budget day, election, expiry-day) are less picked over. The crowded part is single-name US mega-cap earnings.
4. **Prereqs.** A clean event calendar, an event-vol extraction model (strip the event from the term structure), and brutal cost discipline — these are wide-spread trades.
5. **Time-to-first-useful-result.** 3-5 weeks.
6. **Solo-viable.** Yes.
7. **Sources.**
 - Bennett, *Trading Volatility*, earnings/event chapters. (3)(4).
 - Dubinsky & Johannes, *Earnings Announcements and Equity Options* — the canonical event-vol decomposition. Passes (4)(5). Academic, no cost model — use it as structure only.
 - Euan Sinclair's public talks/papers (free; the books are paid — see PAID section). Passes (3)(4).
8. **WHY THIS MIGHT WASTE YOUR TIME.** The premium is real and the bid-ask is wider than the premium in exactly the names where the premium is largest.

---

### 7. Delta hedging, discrete-hedging error, and P&L attribution
1. **What it is.** The mechanics of turning an options position into a vol position: hedge frequency, band choice, and the decomposition of realised P&L into theta, gamma, vega, vanna, and residual.
2. **Uniquely solves.** It is the only thing that tells you *why* you made money. Without attribution, every options result is unattributable luck.
3. **ALIVE and permanently so.** This is not an alpha field; it is the accounting layer that makes every other options field legible. It is also the single most common thing solo traders skip.
4. **Prereqs.** Minute data (he has it), a greeks engine, a cost model.
5. **Time-to-first-useful-result.** 1-2 weeks. Fastest payoff on this entire document.
6. **Solo-viable.** Trivially.
7. **Sources.**
 - Wilmott's discrete-hedging-error treatment; Zakamouline on hedging bands with transaction costs. Passes (2)(4)(5).
 - Bennett, appendix on shadow greeks. (3)(4).
 - His own repo: `payoff-project` already has the payoff/greeks scaffolding to extend.
8. **WHY THIS MIGHT WASTE YOUR TIME.** It generates no signal whatsoever — it only tells you the truth about signals you already have, which is unglamorous and therefore usually skipped.

---

## B. MICROSTRUCTURE, EXECUTION, HFT

### 8. Market microstructure (LOB dynamics, adverse selection, queue)
1. **What it is.** The study of how price forms from the order book: queue priority, order flow imbalance, trade classification, and the information content of quotes.
2. **Uniquely solves.** It is the only field that explains *why your fill differed from your backtest* — the gap between paper and live P&L lives entirely here.
3. **ALIVE and undervalued by solo traders.** OFI as a 1-5 second predictor is well known but genuinely still works; it is not tradeable without low latency, but it *is* usable to improve entry timing on slower strategies.
4. **Prereqs.** L2/L3 data (his minute data is too coarse — this needs tick), queue models, and serious data engineering.
5. **Time-to-first-useful-result.** 6-8 weeks, gated entirely on data acquisition.
6. **Solo-viable for research and execution improvement; firm-only as standalone alpha.**
7. **Sources.**
 - hftbacktest — https://github.com/nkaz001/hftbacktest. (1)(2)(4)(5).
 - Cont, Kukanov & Stoikov, *The Price Impact of Order Book Events*. Passes (4)(5). The OFI result, with its own stated limits.
 - Bouchaud, Bonart, Donier, Gould, *Trades, Quotes and Prices* (CUP) — practitioner-authored (CFM), states failure modes throughout. (3)(4). Paid book; a large fraction of its content exists as free arXiv preprints by the same authors.
8. **WHY THIS MIGHT WASTE YOUR TIME.** All the real signal lives at horizons shorter than your latency, so you will learn a great deal and be able to act on almost none of it.

---

### 9. Execution algorithms & transaction cost analysis
1. **What it is.** Scheduling a parent order into children (TWAP/VWAP/IS/POV) to trade off market impact against price risk, plus measuring the result against benchmarks.
2. **Uniquely solves.** It converts a theoretical edge into a realised one. For a strategy with 5bp edge and 4bp cost, execution *is* the strategy.
3. **ALIVE, permanently.** Not crowded — it is a cost-reduction discipline, and cost reduction cannot be arbitraged away.
4. **Prereqs.** Almgren-Chriss, an impact model calibrated to *your* instruments, and honest fill logging.
5. **Time-to-first-useful-result.** 2-3 weeks for TCA on your own fills; months for a calibrated impact model.
6. **Solo-viable.** Yes, and disproportionately valuable at small size in Indian options where spreads dominate.
7. **Sources.**
 - Almgren & Chriss, *Optimal Execution of Portfolio Transactions* — https://www.smallake.kr/wp-content/uploads/2016/03/optliq.pdf (verified live mirror). Passes (2)(4)(5). Almgren went on to build QB — (3) holds too.
 - Almgren et al., *Direct Estimation of Equity Market Impact* (Citigroup study). Passes (2)(3)(5).
 - Hummingbot's TWAP/VWAP executors — https://github.com/hummingbot/hummingbot. (1)(2)(3).
8. **WHY THIS MIGHT WASTE YOUR TIME.** At your size your orders have no market impact, so most of the literature's machinery is irrelevant — only the spread-crossing decision matters.

---

### 10. HFT / latency arbitrage
1. **What it is.** Competing on speed for stale-quote and cross-venue price discrepancies, measured in microseconds.
2. **Uniquely solves.** Captures the mechanically riskless component of price dislocation — no forecast required.
3. **DEAD to you.** Not decayed — structurally inaccessible. It is a capex race (colo, FPGA, microwave). There is no evening-hours version.
4. **Prereqs.** Seven figures of infrastructure and an exchange membership.
5. **Time-to-first-useful-result.** Never, as a solo.
6. **Firm-only. Absolutely.**
7. **Sources.** Budish, Cramton & Shim, *The High-Frequency Trading Arms Race* (QJE) — passes (4)(5), and is the best argument for *not* entering. Aquilina, Budish & O'Neill, *Quantifying the High-Frequency Trading "Arms Race"* (FCA) — (5), real message-level data.
8. **WHY THIS MIGHT WASTE YOUR TIME.** Reading about it is entertaining; there is a zero percent chance you can do it, and the reading crowds out fields where you can.

---

## C. SYSTEMATIC EQUITY & CROSS-ASSET

### 11. Statistical arbitrage / mean reversion (pairs, cointegration, cross-sectional)
1. **What it is.** Trading the residual of an asset against a hedged basket or partner, betting on reversion of a spread that has no reason to trend.
2. **Uniquely solves.** Market-neutral return with a mechanically defined hedge — the only way to make the market factor genuinely go away.
3. **HEAVILY DECAYED at daily frequency, ALIVE intraday.** Classic daily pairs on liquid US equities is arbitraged flat and has been for a decade. Intraday reversion in Indian stocks and cross-exchange crypto spreads still exist but are cost-dominated.
4. **Prereqs.** Cointegration, Ornstein-Uhlenbeck, Kalman filtering. Capital: moderate. Shorting in India is restricted to F&O names.
5. **Time-to-first-useful-result.** 3-4 weeks to a backtest, and the backtest will be wrong by roughly the size of the edge.
6. **Solo-viable at small scale.**
7. **Sources.**
 - Avellaneda & Lee, *Statistical Arbitrage in the U.S. Equities Market*. Passes (2)(4)(5) — includes a cost discussion and an explicit decay analysis.
 - Robot Wealth (robotwealth.com) — passes (1)(2)(3)(4); they trade their own capital and publish negative results, which is rare.
 - Robert Carver, https://qoppac.blogspot.com + https://github.com/robcarver17/pysystemtrade. Passes (1)(2)(3)(4). He runs it live 20h/day; costs are a first-class object in the codebase.
8. **WHY THIS MIGHT WASTE YOUR TIME.** Every published stat-arb result is a lower bound on how crowded it now is, and the surviving edge is smaller than the Indian STT + impact cost stack.

---

### 12. Factor investing / cross-sectional equity
1. **What it is.** Sorting a cross-section on characteristics (value, momentum, quality, low-vol) and holding the long-short spread.
2. **Uniquely solves.** Long-horizon compounding with capacity — the only field here that scales to serious AUM.
3. **DECAYED as alpha, ALIVE as a benchmark.** Post-publication decay is documented and severe; the replication crisis (Hou-Xue-Zhang, Harvey-Liu) gutted most of the zoo. Momentum and quality survive weakly. India has a documented small-cap/quality premium but liquidity and impermanent index inclusion effects contaminate it.
4. **Prereqs.** Panel data hygiene, survivorship-bias-free universe (the real barrier in India), and multiple-testing discipline.
5. **Time-to-first-useful-result.** 4-6 weeks, mostly spent on data cleaning.
6. **Solo-viable**, but the payoff horizon is years and the Sharpe is ~0.4.
7. **Sources.**
 - Hou, Xue & Zhang, *Replicating Anomalies*. Passes (4)(5) emphatically — it is a list of things that do not work.
 - Harvey, Liu & Zhu, *…and the Cross-Section of Expected Returns*. (4)(5).
 - AQR's published library (aqr.com/insights) — (3)(4); they run the money and publish when factors fail.
8. **WHY THIS MIGHT WASTE YOUR TIME.** It is slow, low-Sharpe, capacity-oriented investing dressed as quant research — the opposite of a minute-wise options trader's comparative advantage.

---

### 13. Trend following / time-series momentum
1. **What it is.** Long-horizon directional betting on the sign of past returns across a diversified futures basket, sized by inverse volatility.
2. **Uniquely solves.** Positive skew and crisis convexity — the only systematic strategy that reliably makes money when everything else is dying. Directly relevant to a firm called Convex Hedge.
3. **ALIVE but degraded.** Sharpe has fallen from ~1.0 (pre-2008) to ~0.4-0.5. Still the most robustly documented systematic return stream ever, and the convexity is the point, not the Sharpe.
4. **Prereqs.** Low maths. High diversification requirement — needs 30+ instruments, which means futures across asset classes. Capital: this is the binding constraint; Indian futures lot sizes make a diversified book expensive.
5. **Time-to-first-useful-result.** 2 weeks with pysystemtrade.
6. **Solo-viable** if you can access global futures; borderline India-only.
7. **Sources.**
 - Carver, https://github.com/robcarver17/pysystemtrade + qoppac.blogspot.com. Passes (1)(2)(3)(4) — all five effectively. Ex-AHL, runs it live, publishes his own failures.
 - Moskowitz, Ooi & Pedersen, *Time Series Momentum*. (4)(5).
 - Hurst, Ooi & Pedersen, *A Century of Evidence on Trend-Following Investing* (AQR). (3)(4).
8. **WHY THIS MIGHT WASTE YOUR TIME.** It needs breadth and patience, both of which you lack — a trend book on three Indian instruments is not trend following, it is gambling with extra steps.

---

### 14. Portfolio construction & risk (covariance, sizing, Kelly)
1. **What it is.** Turning a set of signals into position sizes: covariance estimation, shrinkage, risk parity, HRP, and leverage/Kelly fraction choice.
2. **Uniquely solves.** It determines the *geometric* return, which no signal research touches. Two traders with identical signals and different sizing have unrelated outcomes.
3. **ALIVE, permanently, and systematically underrated by researchers.** Not crowded — it is not a trade.
4. **Prereqs.** Linear algebra, Ledoit-Wolf shrinkage, an understanding of why mean-variance optimisers explode.
5. **Time-to-first-useful-result.** 2-3 weeks; immediately improves everything else he builds.
6. **Solo-viable.** Yes.
7. **Sources.**
 - Ledoit & Wolf, *Honey, I Shrunk the Sample Covariance Matrix*. (4)(5).
 - López de Prado, *Building Diversified Portfolios that Outperform Out-of-Sample* (HRP) — free on SSRN. Passes (1)(4)(5); code is in the paper.
 - Carver's pysystemtrade sizing module — (1)(2)(3).
8. **WHY THIS MIGHT WASTE YOUR TIME.** Optimal sizing of a nonexistent edge is exactly zero, and it is very easy to spend three months here instead of finding the edge.

---

### 15. Research methodology / backtest hygiene
1. **What it is.** The statistics of strategy selection: multiple-testing correction, deflated Sharpe, walk-forward design, and cost modelling as a first-class citizen.
2. **Uniquely solves.** It is the only defence against the dominant failure mode in solo quant work — believing a backtest.
3. **ALIVE and the single highest-ROI item on this list per hour spent.**
4. **Prereqs.** Statistics he already has. Discipline he may not.
5. **Time-to-first-useful-result.** One weekend to implement deflated Sharpe and a trial counter.
6. **Solo-viable.** Yes.
7. **Sources.**
 - Bailey & López de Prado, *The Deflated Sharpe Ratio* — https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2460551 (verified). Passes (1)(4)(5).
 - Bailey et al., *Pseudo-Mathematics and Financial Charlatanism* (Notices of the AMS, free). (4)(5).
 - Carver's blog posts on cost modelling and why his own backtests overstate. (2)(3)(4).
8. **WHY THIS MIGHT WASTE YOUR TIME.** It only ever tells you that things you liked do not work; it produces no strategies, only funerals.

---

## D. MACHINE LEARNING & DATA

### 16. ML applied to markets
1. **What it is.** Supervised/RL models on financial features, with the special problems of non-stationarity, low signal-to-noise, overlapping labels, and near-zero effective sample size.
2. **Uniquely solves.** Nonlinear interaction discovery across many weak features — genuinely hard to do by hand once you have >20 features.
3. **MOSTLY DECAYED at the retail/solo level, ALIVE narrowly.** The honest picture in 2026: ML wins where the label is short-horizon and microstructural (next-100ms mid move, fill probability, queue depletion) and loses almost everywhere else. Deep learning on daily OHLCV is a well-documented dead end. RL for execution scheduling is the one non-microstructure application with real traction.
4. **Prereqs.** He has the maths. The real prereq is purged/embargoed cross-validation and enough independent samples — minute options data gives him this where daily data would not.
5. **Time-to-first-useful-result.** 6-10 weeks, most of it spent discovering leakage.
6. **Solo-viable for narrow, well-posed problems** (fill probability, spread prediction). Firm-only for anything end-to-end.
7. **Sources.**
 - López de Prado's free SSRN corpus (triple-barrier labelling, meta-labelling, purged CV, fractional differentiation). Passes (1)(4)(5). The book is paid; the constituent papers are free.
 - Robot Wealth (robotwealth.com) — (1)(2)(3)(4), publishes ML attempts that failed.
 - hftbacktest for anything execution-RL — (1)(2)(4)(5).
8. **WHY THIS MIGHT WASTE YOUR TIME.** It is the most seductive and least productive field on this list for a solo trader: you will build impressive pipelines whose out-of-sample Sharpe is indistinguishable from a moving-average crossover, and the sunk cost will make you keep going.

---

### 17. Alternative data
1. **What it is.** Non-price inputs — satellite, card spend, web scrape, filings text, shipping, app downloads — mapped to fundamentals ahead of consensus.
2. **Uniquely solves.** True informational (not statistical) edge — actually knowing something before the market does.
3. **DECAYED at the top, ALIVE in obscure corners.** Every mainstream dataset is licensed by 200 funds and priced accordingly. The alive part for a solo is *self-collected* data nobody sells: exchange-published data that nobody bothers to parse, regulatory filings, on-chain state.
4. **Prereqs.** Scraping/ETL, storage, legal care. Capital: your time, or five figures for vendors.
5. **Time-to-first-useful-result.** 3+ months, and mostly engineering.
6. **Solo-viable only for self-collected data.** Firm-only for purchased.
7. **Sources.** I could not verify a source in this field that cleanly passes the filter and is free — most of the literature is vendor marketing. Treat this field as **unsourced** rather than let me pad it. The exception worth naming: NSE's own free participant-wise and OI archives (nseindia.com) are alt-data that almost nobody parses properly.
8. **WHY THIS MIGHT WASTE YOUR TIME.** For a solo trader this is 90% data engineering and 10% finance, and the 10% is only valuable if you have a stock-picking process to feed — which you do not.

---

### 18. Research & data infrastructure
1. **What it is.** The unglamorous layer: tick capture, a time-series store, point-in-time correctness, corporate-action and contract-roll handling, deterministic backtest/live parity.
2. **Uniquely solves.** It is the only thing that makes results reproducible and prevents lookahead. Minute-wise Indian options data is large and messy; without this layer nothing else is trustworthy.
3. **ALIVE and mandatory.** Not a crowding question.
4. **Prereqs.** Engineering. Parquet/Arrow, columnar storage, a symbology scheme for expiring option contracts.
5. **Time-to-first-useful-result.** 3-4 weeks, and it is the gate on every other field.
6. **Solo-viable.** Yes.
7. **Sources.**
 - NautilusTrader — https://github.com/nautechsystems/nautilus_trader. Passes (1)(2)(5); nanosecond event-driven, identical strategy code in backtest and live, which is the property that matters.
 - hftbacktest — (1)(2)(4)(5).
 - Arctic/ArcticDB (Man Group, open source) — (1)(3)(5); built and used by a real fund for exactly this problem.
8. **WHY THIS MIGHT WASTE YOUR TIME.** Infrastructure is infinitely extensible and has no natural stopping point; you can spend a year building a platform and zero days trading.

---

## E. CRYPTO (40% weight)

### 19. Perpetual funding, basis, and cash-and-carry
1. **What it is.** Harvesting the funding rate on perpetual swaps by holding the offsetting spot or dated future, and trading the basis term structure.
2. **Uniquely solves.** A mechanically defined, observable, high-frequency carry stream that exists nowhere else in finance — the funding rate is *printed* every 8 hours.
3. **ALIVE but compressed.** BTC/ETH basis is heavily farmed by ETF-arb desks and basis funds; annualised carry has fallen from 20%+ to single digits in calm regimes. The alive part: altcoin funding, funding *dislocations* during liquidation cascades, and cross-exchange funding spreads. Recent research finds ~17% of observations show ≥20bp arbitrage spreads but only ~40% of the top opportunities are profitable after costs — which is the honest headline.
4. **Prereqs.** Low maths, high operational competence: exchange API risk, margin/liquidation modelling, custody, counterparty risk.
5. **Time-to-first-useful-result.** 2-3 weeks. Fastest live-money result of anything here.
6. **Solo-viable.** The most solo-viable field on this list.
7. **Sources.**
 - Hummingbot — https://github.com/hummingbot/hummingbot. (1)(2)(3)(5). Cross-exchange and funding strategies with real fee handling.
 - *Designing funding rates for perpetual futures in cryptocurrency markets* — https://arxiv.org/abs/2506.08573. (4)(5). Mechanism design; tells you when the peg breaks.
 - *The Two-Tiered Structure of Cryptocurrency Funding Rate Markets* (MDPI Mathematics 14(2):346). (2)(5) — 35.7M one-minute observations, 26 exchanges, explicit post-cost analysis. Verified this session; I did not read it in full.
8. **WHY THIS MIGHT WASTE YOUR TIME.** The carry is small and the tail is exchange insolvency, oracle failure, or a liquidation cascade that takes your hedge leg out — you are short a catastrophe option to earn 6%.

---

### 20. Crypto options & DeFi volatility
1. **What it is.** Volatility trading on Deribit (and now CME/onshore venues), plus the DeFi analogue: option vaults, AMM liquidity provision as a short-gamma position.
2. **Uniquely solves.** It is where his existing SVI/SSVI machinery transfers *immediately* to a market with fat spreads, no colo requirement, 24/7 data, and few sophisticated participants relative to SPX.
3. **ALIVE — the least crowded serious options market that a solo can access.** DOVs (option vaults) as a *strategy* are decayed and were structurally underpriced from the start. But surface modelling, term structure, and skew RV on Deribit remain genuinely under-exploited.
4. **Prereqs.** Exactly what he already has, plus API plumbing. Note: crypto's surface has inverse-payoff and non-normal-collateral quirks that break naive SVI ports — that is the research problem.
5. **Time-to-first-useful-result.** 4-6 weeks; his SVI work is 70% of the way there.
6. **Solo-viable.** Yes. This is the strongest fit-to-skill ratio on the entire map.
7. **Sources.**
 - Deribit's own DVOL and options mechanics documentation (docs.deribit.com) — treat as venue *specification*, not education. Passes (5). Flagged: exchange-affiliated, so I am not counting it as a research source.
 - hftbacktest and Hummingbot for the execution layer — (1)(2)(4)(5).
 - Bennett, *Trading Volatility*, for the transferable structure — (3)(4).
 - Honest gap: I could **not verify a free, cost-explicit, practitioner-authored crypto-options research source** that clearly passes two tests. This is a real hole in the public literature, and it is also why the field is uncrowded.
8. **WHY THIS MIGHT WASTE YOUR TIME.** Deribit's liquidity is concentrated in a handful of BTC/ETH expiries; outside them the "opportunity" you find in the data is a quote nobody will trade against.

---

### 21. On-chain analytics & MEV
1. **What it is.** Reading blockchain state directly — DEX pool composition, liquidations, mempool — and, in MEV's case, competing to reorder or sandwich transactions.
2. **Uniquely solves.** Complete, free, real-time visibility into a market's entire order flow and positioning — an informational condition that exists in no traditional market.
3. **MEV is DECAYED and now a latency/relay oligopoly** (builder concentration, private orderflow). On-chain *analytics* — liquidation-level maps, stablecoin flow, perp-DEX open interest — is ALIVE and cheap.
4. **Prereqs.** Solidity/EVM literacy, node access or an indexer. MEV additionally needs colocated infra and a relay relationship.
5. **Time-to-first-useful-result.** Analytics: 3-4 weeks. MEV: don't.
6. **Analytics solo-viable; MEV effectively firm-only now.**
7. **Sources.** Daian et al., *Flash Boys 2.0* (arXiv:1904.05234) — (4)(5), the origin paper and honest about the systemic instability it identifies. Flashbots' public docs and MEV-Boost dashboards — (1)(3)(5). Verify current state; this field changes every quarter and my knowledge here is the least fresh on this document.
8. **WHY THIS MIGHT WASTE YOUR TIME.** It is a different discipline wearing a finance costume — you would be learning distributed systems engineering, not trading.

---

## F. INDIA-SPECIFIC (30% weight)

### 22. Indian market structure & regulatory regime
1. **What it is.** The rules that determine whether an Indian strategy is viable at all: STT/CTT, stamp duty, SEBI position limits, SPAN+ELM margining, lot sizes, and the expiry calendar.
2. **Uniquely solves.** It is the only thing that converts a US-derived technique into something that survives contact with NSE. Costs in India are not a rounding adjustment — STT on option *premium* plus exercise STT is a structural asymmetry that changes which structures are viable.
3. **ALIVE and actively changing — this is time-sensitive knowledge.** Verified this session: NSE moved its entire F&O expiry to **Tuesday** (BSE to Thursday) effective around September 2025, weekly expiries were cut to one index per exchange, and lot sizes were raised. Every backtest spanning 2024-2026 that assumes Thursday NIFTY expiry is silently wrong.
4. **Prereqs.** None mathematical. Pure diligence.
5. **Time-to-first-useful-result.** One week to build a correct cost-and-calendar model. It will invalidate several strategies immediately, which is the point.
6. **Solo-viable.** Mandatory, actually.
7. **Sources.**
 - SEBI circulars and the *Study on Profit and Loss of Individual Traders in Equity F&O* (sebi.gov.in). Passes (2)(4)(5) — a regulator's cost decomposition of 96 lakh traders is the best failure-mode document in Indian markets.
 - NSE circulars and product notes (nseindia.com) — (5). Primary source for lot sizes, margins, expiry.
 - **Explicit rejection:** Zerodha Varsity, Sensibull education, and every broker "learn" portal are auto-rejected under your filter — broker-affiliated education whose business model is your order flow. They are often factually accurate on mechanics; use them as a mechanics reference only, never as a strategy source.
8. **WHY THIS MIGHT WASTE YOUR TIME.** It is compliance reading, not research, and it goes stale — SEBI changes the rules faster than you can encode them.

---

### 23. Indian index options intraday structure
1. **What it is.** The specific behaviour of NIFTY/BankNifty/Sensex options intraday: the open-auction vol spike, lunch-hour decay, expiry-day gamma compression, and the retail flow signature.
2. **Uniquely solves.** It is the only field where his data advantage (minute-wise NIFTY/Sensex) is a genuine edge over the global research population, because almost nobody outside India studies this and almost nobody inside India studies it rigorously.
3. **ALIVE and genuinely under-researched.** The retail participation is enormous, documented, and loses money — which means there is identifiable flow to be on the other side of. The crowded part is the naive expiry-day short-straddle, which is being farmed by every algo desk in Mumbai.
4. **Prereqs.** His existing stack plus the cost/calendar model from field 22.
5. **Time-to-first-useful-result.** 3-4 weeks. This is the fastest path to something original.
6. **Solo-viable.** Yes, and this is where solo is *advantaged*.
7. **Sources.**
 - SEBI F&O study (FY24, FY25) — (2)(4)(5). Gives the shape of the losing flow.
 - NSE bhavcopy + participant-wise OI archives — (5). Free primary data.
 - Honest note: I could **not find a single free, code-backed, cost-explicit research source specifically on Indian intraday options microstructure.** The academic work I surfaced (e.g. arXiv:2507.04859 on expiry-day SIP timing) is thin and does not pass the filter. This vacuum is the opportunity, but it means no one will hand you a template.
8. **WHY THIS MIGHT WASTE YOUR TIME.** "Under-researched" and "unprofitable" look identical from the outside, and there is a real chance the reason nobody published is that the costs eat everything.

---

## G. ADJACENT

### 24. Fixed income & rates volatility
1. **What it is.** Swaption and cap/floor vol, the vol cube (expiry × tenor × strike), and SABR-family modelling.
2. **Uniquely solves.** It is the only vol market with a genuine third dimension (underlying tenor) — the modelling problem is strictly richer than equity vol.
3. **ALIVE but institutional-only.** OTC, dealer-intermediated, no retail access. India's rates market is shallow and access-restricted.
4. **Prereqs.** Curve construction, SABR/ZABR, multi-curve discounting. Data is not obtainable — fails test (5) for him.
5. **Time-to-first-useful-result.** Not applicable without data.
6. **Firm-only.**
7. **Sources.** Hagan et al., *Managing Smile Risk* (SABR) — (4)(5), and it explicitly names its own negative-density failure. Andersen & Piterbarg, *Interest Rate Modeling* — (3), paid.
8. **WHY THIS MIGHT WASTE YOUR TIME.** You cannot get the data or the access, so it is pure intellectual tourism — genuinely beautiful mathematics that you will never execute.

---

### 25. Tail hedging & convexity (relevant to the firm's name)
1. **What it is.** Deliberately paying a negative carry for a payoff that is convex in a crash — deep OTM puts, VIX call spreads, long-vol overlays — sized so the cost is survivable.
2. **Uniquely solves.** It is the only construction that pays off when correlations go to one and every diversification assumption breaks simultaneously.
3. **ALIVE as a portfolio function, DECAYED as a standalone.** The famous 2020 results are survivorship-selected; most tail funds bleed. It works only as an *overlay* whose size is chosen by portfolio maths, not by conviction.
4. **Prereqs.** Understanding of convexity decomposition and, critically, honest accounting of the bleed.
5. **Time-to-first-useful-result.** 3-4 weeks — and it is directly on-mission for Convex Hedge.
6. **Solo-viable** as research; needs a portfolio to overlay onto.
7. **Sources.**
 - Bennett, *Trading Volatility* — the "cheapest way to buy a crash" analysis. (3)(4).
 - Bhansali's published papers on tail-hedging cost (free versions on SSRN) — (3)(4); he ran it at PIMCO and is candid about the drag.
 - Trend-following as a *cheaper* convexity source: Hurst/Ooi/Pedersen, AQR. (3)(4).
8. **WHY THIS MIGHT WASTE YOUR TIME.** Tail hedges lose money 95% of the time by design, and there is no backtest length that will make you confident you sized it right.

---

# RANKED SHORTLIST — the 5 fields that fit *this* reader

**1. Options flow & dealer positioning, built on Indian index options (field 5, feeding field 23).**
This is the only intersection where his data advantage, his surface machinery, and a genuine research vacuum all coincide. NSE publishes OI and participant-category data free; almost nobody has reconstructed a dealer book on minute data. The SEBI census tells you the losing flow is real and large. Highest expected value on the map. Start with GEX reconstruction on NIFTY and validate against realised intraday pinning.

**2. Delta hedging, discrete-hedging error, and P&L attribution (field 7).**
Cheapest, fastest, and it is the measurement instrument for everything above. Two weeks. Without it, every subsequent result he produces is unattributable. Do this *first*, in parallel with #1.

**3. Crypto options volatility on Deribit (field 20).**
His SVI/SSVI work transfers directly into the least crowded serious options market accessible to a solo trader: no colo, 24/7 data, fat spreads, few sophisticated participants. It also satisfies the crypto weighting with the technique he already owns rather than a new discipline. The literature gap I could not fill is itself the argument for going there.

**4. Perpetual funding & basis (field 19).**
Included because it is the fastest path to a live, cost-honest, small-capital P&L, and because trading something real recalibrates every research judgement he makes afterwards. Low maths, high operational learning. Explicitly sized small — the tail is exchange failure.

**5. Research methodology + Indian cost/calendar modelling (fields 15 and 22, treated as one).**
Not a strategy — a filter. Deflated Sharpe plus a correct STT/SPAN/Tuesday-expiry model will kill several ideas he currently believes in, which is worth more than any new idea. One weekend for the statistics, one week for the cost model.

**Explicitly deprioritised for him, despite being interesting:** ML applied to markets (highest seduction-to-yield ratio on the map), HFT and MEV (structurally inaccessible), dispersion (capital-gated), factor investing (wrong time horizon for his temperament and data), rates vol (no data access).

---

## PAID — worth considering later (do not mix with the above)

- **Euan Sinclair, *Volatility Trading* and *Positional Option Trading*.** The only options books written by someone who ran a book and states his edge sizes and costs numerically. Passes (2)(3)(4). No free equivalent exists — Bennett is the closest and covers different ground.
- **Bouchaud, Bonart, Donier & Gould, *Trades, Quotes and Prices* (CUP).** Practitioner-authored microstructure. Much of the content exists as free arXiv preprints by the same authors, so buy only if the synthesis matters.
- **López de Prado, *Advances in Financial Machine Learning*.** Nearly all of its substance is in his free SSRN papers. Low marginal value.
- **Carver, *Systematic Trading* / *Advanced Futures Trading Strategies*.** pysystemtrade and qoppac.blogspot.com are free and cover most of it.

Sources: [Trading Volatility PDF](https://trading-volatility.com/Trading-Volatility.pdf) · [Hummingbot](https://github.com/hummingbot/hummingbot) · [NautilusTrader](https://github.com/nautechsystems/nautilus_trader) · [hftbacktest](https://github.com/nkaz001/hftbacktest) · [pysystemtrade](https://github.com/robcarver17/pysystemtrade) · [The Implied Order Book](https://squeezemetrics.com/download/The_Implied_Order_Book.pdf) · [Almgren & Chriss](https://www.smallake.kr/wp-content/uploads/2016/03/optliq.pdf) · [Deflated Sharpe Ratio](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2460551) · [Perpetual funding rate design](https://arxiv.org/pdf/2506.08573) · [Crypto funding rate market structure](https://www.mdpi.com/2227-7390/14/2/346) · [Moontower](https://moontowermeta.com) · [SEBI F&O loss study coverage](https://www.business-standard.com/markets/news/net-losses-of-traders-in-fo-widens-in-fy25-sebi-study-125070701221_1.html) · [Volland dealer-flow paper (partially verified)](https://vol.land/VollandWhitePaper.pdf)