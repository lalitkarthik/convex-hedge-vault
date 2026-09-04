# Regime Detection & Strategy Research — Stress-Tested

Verification note up front: I ran ~15 searches/fetches. Items marked **[verified]** I fetched or read directly. Items marked **[unverified]** I am reporting from search metadata only — treat the claim, not the source, as provisional. Where I could not find a practitioner who ran something with real money, I say so rather than inventing one.

---

## 1. Hidden Markov Models for regime classification

### Verdict: the HMM itself is the weakest link. The literature has largely moved past it, and the move is the useful finding.

**The core defect is not statistical, it is operational.** A Gaussian-emission HMM fitted by Baum-Welch gives you *smoothed* state probabilities `P(s_t | y_1..y_T)`. Every published equity curve that uses smoothed states is contaminated — it uses the future to label the present. The only legitimate object is the *filtered* probability `P(s_t | y_1..y_t)`, and filtered probabilities are (a) far noisier and (b) lag the turn by roughly the persistence horizon implied by the diagonal of the transition matrix. If your senior colleague's HMM looks good, the first thing to check is whether he called `predict()` (Viterbi over the full sample) rather than running an expanding-window filter. This single bug accounts for most impressive HMM regime backtests.

Second defect: **state-count instability**. BIC/AIC on financial returns is close to flat between k=2,3,4, and the argmin moves as you extend the sample. A 4-state model typically resolves into {low-vol drift up, low-vol chop, high-vol down, crisis} on one window and into something with a degenerate near-empty state on the next. A state that exists in one training window and vanishes in the next is not a regime; it is a fitting artefact. Test this directly: refit on rolling 5-year windows and check label correspondence via the Hungarian algorithm on state means/covs. If labels permute or a state collapses, the model is not deployable.

Third: **Gaussian HMMs reproduce fat tails and zero return autocorrelation but fail to reproduce volatility clustering** — the one property you actually need for options. **[unverified — stated in search results from the jump-model literature; worth confirming yourself with a quick simulation, which is cheap.]** This matters enormously for you: an HMM regime label is a poor conditioning variable for a vol-selling book precisely because it does not capture the ACF of |r|.

#### What to use instead — Statistical Jump Models
- **`jump-models` (Yizhan Shu, with Petter Kolm / John Mulvey / Onat Aydınhan)** — https://github.com/Yizhan-Oliver-Shu/jump-models, plus https://github.com/Yizhan-Oliver-Shu/continuous-jump-model
- Paper: *Downside Risk Reduction Using Regime-Switching Signals: A Statistical Jump Model Approach* — https://arxiv.org/abs/2402.05272; extension in Annals of OR — https://link.springer.com/article/10.1007/s10479-024-06035-z
- **What it concretely gives you:** scikit-learn-style API, pandas in/out, discrete + continuous + **sparse** (feature-selecting) variants. The jump penalty λ is an *explicit* regularizer on state persistence — you are tuning the thing that HMMs leave implicit and unstable in the transition matrix. The sparse variant is the one that matters: it tells you which of your candidate features (realized vol at multiple horizons, downside deviation, Sortino, skew) actually carry regime information, which kills a lot of feature-fishing.
- **Tests passed:** (1) runnable code, (5) reproducible on obtainable data (their example runs on Nasdaq daily), (4) partially — the papers are explicit that they benchmark *against* HMM on regime-persistence and lag, i.e. they name the thing that breaks.
- **Caveat, and it is a real one:** Kolm is NYU/practitioner-adjacent and Mulvey is Princeton, but **I found no evidence any of these authors ran this with client money.** The comparison "JM beats HMM beats buy-and-hold" is an in-sample-of-the-research-program result. The λ penalty is a free parameter that does exactly what state-count did in the HMM — it moves the overfitting one level up. Tune λ inside a purged CV, not on the full sample.

#### Runnable HMM baselines (for the comparison, not for trading)
- `statsmodels.tsa.regime_switching.MarkovRegression` / `MarkovAutoregression` — in your stack already, no install, and critically it exposes `filtered_marginal_probabilities` separately from `smoothed_marginal_probabilities`. Use it to demonstrate the look-ahead gap to your colleague in about 30 lines: plot both, plot the equity curve under each, show the gap. That demonstration is more persuasive than any paper.
- `hmmlearn` — fine, but note `GaussianHMM.fit` is EM with random restarts; results are initialisation-dependent. Fix `random_state` and run 50 restarts to see the spread of log-likelihoods and resulting label sequences. The spread is usually embarrassing.

#### Who has run it with money
Honest answer: **I could not verify a single named fund that attributes P&L to an HMM regime filter.** Macrosynergy (https://macrosynergy.com/research/classifying-market-regimes/) publishes regime-classification research with the `macrosynergy` Python package and Jupyter notebooks, and their house convention lags signals to avoid look-ahead — but the site returned **403** to my fetch, so I have **not verified** the article's contents, its cost treatment, or whether it reports negatives. Check it yourself; the package is on PyPI/GitHub. Beyond that, "Man/AHL/Two Sigma use regime models" is folklore I cannot source and you should not repeat.

**Maintenance cost:** high and recurring. Refit cadence, λ or k re-selection, feature drift, and a permanent label-correspondence monitor. Budget this as a *supervised* model in production, not a set-and-forget feature.

**Where it stops working:** at the only moments you want it. Regime detection is a change-point problem with a detection delay bounded below by the signal-to-noise of the feature; in a fast vol event (Feb 2018, Mar 2020, the Aug 2024 yen unwind) the label flips *after* the gap move. For a short-gamma book, a regime filter that flips after the gap is worse than useless — it makes you flatten into the bottom. Only use regime labels for things with slow decision horizons (position sizing, hedge budget), never as a gate on entering/exiting short-premium.

---

## 2. Diebold-Yilmaz spillover / connectedness

### Verdict: excellent descriptive instrument, close to worthless as a live signal, and the reason is structural.

**What it actually is:** a rolling-window generalized (Pesaran-Shin) FEVD of a reduced-form VAR, renormalized to rows summing to 100. It is a *measurement* of realized co-movement transmission. It is not a forecast, and the authors' own program is framed as measurement.

#### The runnable implementations — both are real, both are good
- **`ConnectednessApproach` (David Gabauer)** — https://github.com/GabauerDavid/ConnectednessApproach — R, on CRAN. This is the one to use. Static + dynamic connectedness, time-domain and frequency-domain, joint and extended-joint spillover, over **orthogonalized / generalized / QVAR / LASSO-VAR / Ridge-VAR / ElasticNet-VAR / TVP-VAR**. Ships bundled datasets that **replicate a battery of published connectedness papers**. Docs and replications at https://gabauerdavid.github.io/ConnectednessApproach/. **[verified: repo + docs site exist and describe exactly this]**
- **`frequencyConnectedness` (Tomáš Krehlík)** — https://github.com/tomaskrehlik/frequencyConnectedness — implements Baruník-Křehlík (2018) frequency decomposition plus classic DY09/DY12; `spilloverRollingDY09` has a parallel version. CRAN manual: https://cran.r-project.org/web/packages/frequencyConnectedness/. **[verified]**
- Retrospective by the originators: *On the Past, Present, and Future of the Diebold-Yilmaz Approach* — https://arxiv.org/abs/2211.04184. **[abstract verified only — arXiv abs page fetched, full text not read.]**

**Tests passed:** (1) runnable code — emphatically, (5) reproducible — the packages ship the replication data. That is two, so it qualifies. It does **not** pass (2) or (3): there is no cost model anywhere in this literature because there is no trade in it.

#### The failure modes, stated bluntly
1. **Rolling-window artefact.** The connectedness index is a function of the covariance structure inside a window of length W. When a crisis enters the window the index jumps; when it *exits* the window, W days later, the index drops — with no market event at all. Practitioners repeatedly mistake the exit-drop for "spillover normalising." Every DY time series has this sawtooth baked in. TVP-VAR (Antonakakis-Chatziantoniou-Gabauer 2020, implemented in Gabauer's package) exists specifically to kill the window artefact and is the version you should use if you use any.
2. **Generalized FEVD does not identify anything.** GFEVD sidesteps Cholesky ordering-dependence, but the price is that the "directional spillovers" are not structural — they are variance shares under a non-orthogonal shock, and the rows only sum to 100 after an ad-hoc renormalisation. You cannot read "A causes B" off the matrix. Papers do this constantly. Don't.
3. **It is contemporaneous with volatility, so it adds nothing to a vol signal.** Total connectedness rises in crises. So does realized vol, so does correlation, so does VIX. Before building anything on a connectedness matrix, regress your connectedness index on cross-sectional realized correlation and average realized vol. In my experience the residual is small. **If it is small, the matrix is a repackaged vol signal with 20× the maintenance cost.** This is the single test that decides whether your colleague's spillover work survives, and it costs an afternoon.
4. **Out-of-sample instability:** the H-step FEVD horizon, lag order p, and window W are three free parameters and the index level is sensitive to all three. The *shape* over time is more robust than the *level* — so never threshold on the level.

#### The one use I would defend
As a **cross-asset diversification diagnostic, not a signal**: net directional connectedness tells you which of your positions are net *receivers* of shocks, and therefore where your apparent diversification is fake. For a book that is short vol on NIFTY and long crypto vol, "how much of BTC's forecast error variance is explained by SPX/vol shocks in a stress window" is a legitimate, decision-relevant number. Run it monthly, look at the matrix with your eyes, do not automate a trade off it.

**Who has run it with money:** nobody I can identify. This is an academic industry — thousands of "connectedness between X and Y" papers, essentially zero trading track record. Gabauer works in industry analytics; that is not the same as trading it. Be blunt with your colleague on this one.

**Maintenance:** low if descriptive/monthly, absurd if you try to make it live (VAR refit stability, window edge handling, missing-data alignment across venues and time zones — and NIFTY/BTC/SPX do not share a session, so your VAR is estimated on misaligned bars, which itself creates spurious directional spillover from the market that closes later).

---

## 3. Clustering (KNN, HDBSCAN) for parameter optimisation / overfit reduction

### Verdict: clustering parameter space does not reduce overfitting. It reduces *variance of your estimate of the overfit*. These are different things, and conflating them is the most common error here.

**The honest framing:** picking a "robust plateau" in parameter space via clustering is a smoothing operator on the backtest-Sharpe surface. Smoothing reduces the variance of the selected parameter's OOS performance, and slightly reduces selection bias versus argmax. It does **not** address the fact that you ran N trials. If you tried 500 parameter combinations and then clustered them, you still tried 500 combinations, and your best cluster centroid's Sharpe still needs deflating by the same multiple-testing correction. Clustering that just relabels overfitting is exactly the right suspicion.

#### The correct tooling — and it is not clustering
- **`purged-cross-validation` (eslazarev)** — https://github.com/eslazarev/purged-cross-validation. scikit-learn-compatible purged K-fold, embargo, walk-forward, **Combinatorial Purged CV, and Deflated Sharpe Ratio in the same package**. **[verified via search result title/description]** This is the single highest-value item in this whole section for you: CPCV gives you a *distribution* of OOS paths rather than one, and DSR is the correction that makes "I tried 500 things" quantitative.
- **`timeseriescv` (sam31415)** — https://github.com/sam31415/timeseriescv — purged/embargoed combinatorial CV, older and simpler, useful to read as reference implementation.
- Underlying: López de Prado, *Advances in Financial Machine Learning* ch.7 (purging/embargo) and ch.12 (CPCV); Bailey & López de Prado, *The Deflated Sharpe Ratio* (JPM 2014). Both accessible via IIT KGP.

**Tests passed:** (1) runnable code, (4) **double-weighted** — the purging/embargo machinery exists *because* the author names the specific leakage failure mode (overlapping labels) that invalidates naive CV, (5) reproducible on any data.

**Caveat, and it is significant:** López de Prado is a real practitioner (AQR, Guggenheim, ADIA Lab) but CPCV itself has drawn credible criticism — with T observations and overlapping paths, the CPCV paths are heavily correlated, so the "distribution of Sharpes" is narrower than it looks and DSR applied to it can still be optimistic. Also, purging matters most when labels overlap (triple-barrier style). For a **minute-wise intraday NIFTY options strategy that opens and closes within the session, label overlap is near zero and purging buys you almost nothing** — your real leakage risks are different: expiry-day survivorship in the option chain, strike-selection using the day's realized ATM, and quoting off a stale mid.

#### On HDBSCAN specifically
I searched and found **no credible finance practitioner source applying HDBSCAN to strategy-parameter selection.** What comes back is microscopy, astronomy, and the docs. The docs themselves are worth reading for the parameter semantics — https://hdbscan.readthedocs.io/en/latest/parameter_selection.html and https://scikit-learn.org/stable/modules/generated/sklearn.cluster.HDBSCAN.html — `min_cluster_size` is "smallest grouping you'd call a cluster" and `min_samples` controls how aggressively points become noise.

Note the recursion, which is the fatal objection: **HDBSCAN has hyperparameters, so using it to pick your strategy's hyperparameters means you now have hyperparameters selecting hyperparameters, tuned on the same data.** People then Bayesian-optimise HDBSCAN's parameters (Optuna, etc.), which adds a third layer. Each layer is another set of trials that DSR must account for and that nobody counts.

**KNN for this purpose is simply local averaging of the Sharpe surface.** If that is what you want, say so and use a Gaussian kernel smoother — it is one line, has one bandwidth parameter, and is honest about being a smoother.

**What I would actually do:** drop the clustering entirely. Replace with — (a) sensitivity of Sharpe to each parameter one-at-a-time, plotted; (b) require the strategy to be profitable across a *contiguous region*, not a cluster centroid; (c) count every trial you ran, including the ones you abandoned, and deflate. Item (c) is the one everyone skips and it is the one that matters.

**Maintenance:** near zero — this is offline research hygiene, not production infrastructure.

---

## 4. Delta-neutral construction, hedging cadence, management

### Verdict: this one survives, and it is the only item in the list where cadence is a genuinely solved problem with closed-form answers you can implement this week.

**The key result your colleague may be missing:** the optimal response to transaction costs is **not** "hedge less often on a timer." It is a **no-trade band around delta whose width scales as (cost × gamma × S / γ_risk_aversion)^(1/3)** — the cube root is the signature of the asymptotic solution. Time-based rebalancing (hourly, EOD) is dominated by band-based rebalancing at essentially every cost level, and the gap widens with gamma. With minute NIFTY data you can measure this directly.

- **Zakamouline, *Optimal Hedging of Options with Transaction Costs*** — free PDF: https://efmaefm.org/0efmameetings/efma%20annual%20meetings/2005-Milan/papers/284-zakamouline_paper.pdf. Analytic approximations to both no-trade boundaries, with coefficients as explicit functions of model parameters. **[verified: URL is a live free PDF from search]** Directly implementable.
- **Whalley & Wilmott asymptotic bands** — the small-cost limit; Whalley's partial-hedging extension free at https://warwick.ac.uk/fac/soc/wbs/subjects/finance/faculty1/elizabeth_whalley/whalleypartialtcjan06.pdf
- **`pfhedge` (Preferred Networks Research)** — https://github.com/pfnet-research/pfhedge — PyTorch deep-hedging framework that **ships `pfhedge.nn.WhalleyWilmott` as a baseline strategy** alongside BS-delta and learned hedgers, with an explicit cost parameter in the environment. https://pfnet-research.github.io/pfhedge/generated/pfhedge.nn.WhalleyWilmott.html. **Tests passed:** (1) code, (2) costs are a first-class parameter, (5) reproducible. This is the cleanest way to benchmark cadence policies against each other under a cost model. **Caveat:** it is a *simulator* — GBM/Heston paths by default. Deep-hedging results on simulated paths are a statement about your SDE, not about NIFTY. Its real value to you is as a harness: swap in your own minute path generator (or bootstrapped real minute paths) and use the built-in WhalleyWilmott/BS baselines as the control arm. Do not deploy a learned hedger.
- **`sweliam/zakamouline`** — https://github.com/sweliam/zakamouline — Python implementation of the Zakamouline bands. **[unverified — I did not open it; small repo, treat as a starting point to check against the paper's equations rather than as trusted code.]**
- **Hull & White, *Optimal Delta Hedging for Options*** (JBF 2017) — the minimum-variance delta correction `δ_MV = δ_BS + vega·(∂E[σ_imp]/∂S)`, empirically estimated. On US equity index options the MV delta removes a large fraction of the residual variance of a delta-hedged position, purely because of the leverage effect (spot down → IV up). **This is highly relevant to you:** NIFTY has a strong, persistent spot-vol correlation, so a BS delta systematically over-hedges puts and under-hedges calls. Estimating the Hull-White quadratic on your own minute NIFTY data is a genuinely tradeable, self-contained project and the results will be *different* from the US because the skew dynamics differ. **Caveat:** it is a variance-minimising, not P&L-maximising, delta, and the fitted coefficients are regime-dependent (which is where §1 legitimately re-enters — as a slow conditioning variable on the MV coefficients, not as a trade gate).

**Where it stops working:** the band solutions all assume a diffusion. In a gap (Indian budget day, RBI, US CPI print, a crypto liquidation cascade) the band framework is silent and the gamma cost is realised instantly regardless of your cadence. For NIFTY specifically, the 0-DTE expiry-day gamma explosion breaks every asymptotic assumption — as T→0 the bands go to zero width and the formula demands infinite trading. You need a hard override: stop band-hedging inside some threshold of expiry and manage by position size instead.

**Maintenance:** moderate. Costs must be re-estimated (Indian STT/exchange charges are *known and computable*, which is a real advantage over US — but impact/spread is not). The bands need live gamma, so your Greeks pipeline becomes production-critical.

---

## 5. Trend-following applied to options rather than futures

### Verdict: the strongest-founded item on the list, and the only one where I can point to a named person managing real money who published the analysis for free.

- **Bhansali & Holdom (LongTail Alpha), *Relationship Between Trend-Following and Options*, Nov 2024** — https://www.longtailalpha.com/wp-content/uploads/2024/11/Relationship-Between-Trend-Following-And-Options-2024.11.06.pdf **[verified: I extracted and read the full PDF]**

**What it concretely gives him.** The paper makes the trend↔option identity operational, not decorative:

- The exact decomposition: replicated straddle P&L = payoff range − ½ Σ Γ_{s-1}(S_s − S_{s-1})² — **the quadratic-variation term is named as the slippage cost of replication**, and theta in the option is identified as the *same quantity* as whipsaw + transaction cost in the trend program. That gives you a direct arithmetic test: compute Σ½Γ·(ΔS)² for your trend rule and compare it to the actual straddle premium. Whichever is cheaper is how you should express the trade. This is a real, runnable decision rule.
- The moving-average crossover threshold ↔ straddle strike; the position-sizing ramp ↔ delta; the speed of the ramp ↔ gamma.
- **Strangles ↔ entry thresholds:** spreading the strikes is exactly "require confirmation before entering," and the stated cost is slower convexity accrual — "the cost of patience."
- **Stop-losses ↔ knock-out options.** A trend program with stops is *short a tail put below the stop level* and is exposed to jump risk there. Their prescription: if the option is cheap enough, replace the stop with the option outright. They cite Kaminski & Lo (2014) on stops reducing expected return under random walks.
- The concrete architecture they propose: **replicate the long-horizon signal with a long-dated lookback-straddle analogue, and buy short-dated options to insure the reversal risk**, so you are not stopped out of a position that later re-trends.
- Empirical anchor is BTOP50 + global equities, 50/50 — increases CAGR, reduces equity beta and drawdown over the long sample, but **explicitly states that over the most recent two decades the 50/50 did not keep up with 100% equity CAGR** and only won on risk-adjusted terms. That is a volunteered negative.

**Tests passed:** (3) authors run LongTail Alpha, an actual tail-risk manager, with named contact details — real money; (4) **double** — reversal risk is called "the Achilles heel," "a feature, not a bug," and the stop-loss/knock-out jump exposure is named precisely; (2) costs are treated analytically and explicitly (quadratic variation, theta, and *liquidity* — they state that when liquidity is low the quadratic-variation cost of replication escalates and options become the better vehicle).

**Honest caveat — and it is the one that matters:** **there is no backtest in this paper.** No cost-modelled equity curve, no parameter set, no data appendix. It is an analytic framework plus illustrative exhibits, and it ends with "more details will be forthcoming in a future paper." It also has an obvious commercial interest: a tail-risk manager arguing that trend-followers should buy options is arguing for its own product. The framework is correct and useful regardless, but do not treat it as evidence that the overlay pays after costs. **You have to build that test yourself** — and you can, with minute NIFTY data, because the whole thing reduces to comparing Σ½Γ(ΔS)² against actual traded straddle prices.

**Supporting, unverified but from real managers:** CFM's *The Convexity of Trend Following* — https://www.cfm.com/wp-content/uploads/2022/12/266-2018-The-Convexity-of-trend-following.pdf (CFM manages real money); Man Group, *Creating Portfolio Convexity* — https://www.man.com/insights/creating-portfolio-convexity. **[both unverified — search results only.]**

**Also directly relevant, and don't skip it:** **Hoffstein, Faber & Braun, *Rebalance Timing Luck*** — https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3673910 and https://www.thinknewfound.com/rebalance-timing-luck. Hoffstein runs Newfound / Return Stacked — real money. The finding that matters to you: they replicated a **self-financing 3-month put-spread collar** where implementations differed *only in rebalance date*, and found **annualised tracking error in excess of 400bp between implementations**. For equity factor indices the luck term exceeded 100bp/yr. **[verified via search summary; SSRN paper not fetched.]** Translation for your work: any options overlay you backtest on a fixed roll schedule has a several-hundred-bp/yr random component from the roll date alone. The fix is overlapping tranches (roll 1/n of the book each period). If your backtest platform rolls on a single fixed date, its results are not reproducible in the sense that matters.

---

## 6. Indian and crypto implementation surface — an honest, mostly negative report

**Indian.** Applying your filter mechanically kills nearly the entire Indian options-education ecosystem. Zerodha Varsity, Sensibull, and the large "option selling" YouTube/blog complex are **broker-affiliated with order flow as the business model → auto-reject**. QuantInsti/EPAT content funnels to a paid course → **auto-reject**. What survives is infrastructure and raw data, not research:

- **`marketcalls/openalgo`** — https://github.com/marketcalls/openalgo — AGPL self-hosted execution layer, Flask + React, 30+ Indian broker adapters behind one API plus Delta Exchange for crypto derivatives, with option-chain / IV smile / vol surface / GEX / straddle-PnL tooling built in. **[verified: repo and docs at https://docs.openalgo.in/]** **Tests passed:** (1) code, (5) reproducible. **Blunt caveat:** the author (Rajandran R / Marketcalls) does sell paid offerings elsewhere, which puts it near your auto-reject line — but OpenAlgo itself is genuinely free, open-source, and is *execution plumbing*, making no strategy performance claim, so there is nothing to be sold on. Use it as a broker abstraction; ignore any strategy content around it.
- The NIFTY/BankNifty straddle repos that surfaced (`umeshpalai/...Banknifty-Straddle`, `buzzsubash/algo_trading_strategies_india`, `aeron7/nifty-banknifty-intraday-data`) — **I did not verify cost models in any of them, and the visible descriptions do not mention one.** Under your rule, a backtest with no cost model is an auto-reject. Read them as plumbing examples (expiry handling, strike selection, data schema), never as evidence.

**Crypto.** Thinner than it looks.
- **`bottama/cryptocurrency-derivatives-pricing-and-delta-neutral-volatility-trading`** — https://github.com/bottama/cryptocurrency-derivatives-pricing-and-delta-neutral-volatility-trading — Deribit public-API collection into SQLite plus a delta-neutral straddle backtest on the mean-reversion of IV. **I fetched the DeltaHedging README specifically and it states no transaction costs, no fees, no slippage, no rebalancing cadence, and no backtest date range.** Last updated Sept 2021. **This fails your filter as evidence.** Its value is the ingestion pipeline: Deribit's public endpoints need no auth for instrument/quote data, so it is a working template for building your own crypto option-chain store.
- **CryptoDataDownload Deribit CSVs** — https://www.cryptodatadownload.com/data/deribit/ — free BTC/ETH options OHLCV by maturity, futures/perp OHLCV, funding rates, and the **DVOL index**. **[unverified — search result only; check the granularity, since free tiers here are often daily, which would not support minute-level hedging-cadence work.]**

The crypto-specific point worth making to your colleague: **crypto is where the delta-neutral and cadence work in §4 pays best and the regime work in §1 pays worst.** Deribit is 24/7 with no gaps-over-weekend, so the diffusion assumption behind Zakamouline bands holds better than in NIFTY; but perpetual funding introduces a carry term in the hedge leg that none of the classical band literature models, and that term can dominate the transaction-cost term. That is an unfilled gap and a genuinely publishable/tradeable piece of work for you.

---

## 7. The empty `regime` column in the backtest platform

Not an oversight to fix by picking a model — it is a schema stub, and what it should hold depends on a decision nobody has made. In production systems this field is normally one of four things, in descending order of how common they are:

1. **A low-cardinality categorical label, one per bar, from a small enumerated set** (`trend_up | trend_down | range | stress`, or `vol_q1..q4`). Almost always the label is *not* from an HMM — it is a deterministic rule over slow observables: trailing realized vol bucketed by its own trailing percentile, term-structure slope sign (VIX/VIX3M, or NIFTY near/next IV), and a drawdown-from-high flag. Deterministic rules are used because they are auditable, have no refit, and cannot silently leak.
2. **A continuous score plus a threshold**, stored as the score, with bucketing done at query time. Preferred by teams that were burned by state-count instability.
3. **An as-of-bar filtered probability vector** from a model, stored with an explicit `model_version` and `fit_asof` column. This is the correct way to store a model-derived regime, and the presence of `fit_asof` is the tell that whoever built it understood look-ahead.
4. **A post-hoc analyst label** (`covid_crash`, `2022_rate_shock`) used for slicing P&L reports and explicitly forbidden from entering signals.

The critical distinction to enforce before anyone populates it: **(1)-(3) are point-in-time and legal as inputs; (4) is retrospective and is an attribution field only.** If the column is going to be filled, it needs a sibling boolean like `is_point_in_time` or the two uses will get mixed within a quarter, and a smoothed/retrospective label leaking into a signal is exactly the bug in §1.

The genuinely useful thing to say in the meeting: **an empty regime column is a better state than a wrongly-populated one.** Ask what decision the field is supposed to change. If the answer is "position size" or "hedge budget," a deterministic vol-percentile rule is sufficient and costs a day. If the answer is "whether to enter short-premium," the field should stay empty, because detection lag makes it actively harmful there.

---

## PAID — worth considering later

- **Euan Sinclair, *Volatility Trading* and *Positional Option Trading*** (Wiley). I searched for free equivalents and there is no substitute for the hedging-cadence and vol-premium-harvesting material, particularly his treatment of how much of the variance premium survives realistic costs and why most retail short-vol programs are short a hidden jump. He traded professionally. The academic literature does not cover what he covers. **[I could not verify any free code repository associated with either book.]**
- **Hari Krishnan, *The Second Leg Down*** — the practitioner counterpart to the LongTail trend/options paper, on managing convexity positions *after* the initial shock. No free equivalent found.

Neither is required to start; both are worth buying once the §4 and §5 work is running.

**Sources:** [jump-models](https://github.com/Yizhan-Oliver-Shu/jump-models) · [continuous-jump-model](https://github.com/Yizhan-Oliver-Shu/continuous-jump-model) · [Jump model paper](https://arxiv.org/html/2402.05272v2) · [Annals of OR extension](https://link.springer.com/article/10.1007/s10479-024-06035-z) · [Macrosynergy regimes (403, unverified)](https://macrosynergy.com/research/classifying-market-regimes/) · [ConnectednessApproach](https://github.com/GabauerDavid/ConnectednessApproach) · [Gabauer docs](https://gabauerdavid.github.io/ConnectednessApproach/Rpackage) · [frequencyConnectedness](https://github.com/tomaskrehlik/frequencyConnectedness) · [frequencyConnectedness CRAN manual](https://cran.r-project.org/web/packages/frequencyConnectedness/frequencyConnectedness.pdf) · [DY retrospective](https://arxiv.org/pdf/2211.04184) · [purged-cross-validation](https://github.com/eslazarev/purged-cross-validation) · [timeseriescv](https://github.com/sam31415/timeseriescv) · [HDBSCAN parameter selection](https://hdbscan.readthedocs.io/en/latest/parameter_selection.html) · [sklearn HDBSCAN](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.HDBSCAN.html) · [Zakamouline](https://efmaefm.org/0efmameetings/efma%20annual%20meetings/2005-Milan/papers/284-zakamouline_paper.pdf) · [Whalley partial hedging](https://warwick.ac.uk/fac/soc/wbs/subjects/finance/faculty1/elizabeth_whalley/whalleypartialtcjan06.pdf) · [pfhedge](https://github.com/pfnet-research/pfhedge) · [pfhedge WhalleyWilmott](https://pfnet-research.github.io/pfhedge/generated/pfhedge.nn.WhalleyWilmott.html) · [sweliam/zakamouline](https://github.com/sweliam/zakamouline) · [LongTail Alpha trend/options](https://www.longtailalpha.com/wp-content/uploads/2024/11/Relationship-Between-Trend-Following-And-Options-2024.11.06.pdf) · [CFM convexity of trend](https://www.cfm.com/wp-content/uploads/2022/12/266-2018-The-Convexity-of-trend-following.pdf) · [Man Group convexity](https://www.man.com/insights/creating-portfolio-convexity) · [Rebalance Timing Luck SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3673910) · [Newfound RTL](https://www.thinknewfound.com/rebalance-timing-luck) · [OpenAlgo](https://github.com/marketcalls/openalgo) · [OpenAlgo docs](https://docs.openalgo.in/) · [bottama Deribit delta-neutral](https://github.com/bottama/cryptocurrency-derivatives-pricing-and-delta-neutral-volatility-trading) · [CryptoDataDownload Deribit](https://www.cryptodatadownload.com/data/deribit/)