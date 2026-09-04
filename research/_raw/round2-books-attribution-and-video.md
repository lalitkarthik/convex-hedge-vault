# ROUND TWO — CANON, PNL ATTRIBUTION, VIDEO/X

## 0. Correction that reframes the whole round

**"Kevin Klassen" does not exist. You mean Timothy Klassen.** PhD particle physics (Chicago) → equity derivatives quant under Emanuel Derman at Goldman (2000) → designed the 2003 "new VIX" for Cboe → built Getco's options analytics infrastructure and quant team → founded Vola Dynamics 2016 (Jim Gatheral is an advisor). Verified: [databento.com/blog/quants-worth-following-timothy-klassen](https://databento.com/blog/quants-worth-following-timothy-klassen), [voladynamics.com/team/timothy-klassen/](https://voladynamics.com/team/timothy-klassen/).

He is simultaneously the single best free source for **(B)** and the main find for **(C)**. Everything below in Section B.1 and C.1 is him. I opened and read the actual PDFs rather than trusting metadata.

---

# (A) THE BOOK CANON, RANKED FOR YOUR POSITION

Ranking premise: you have the surface maths (SVI/SSVI implemented). What you lack is (i) how a book behaves over time, (ii) what the costs actually are, (iii) how to tell whether a model is broken. Books are ranked by marginal value **given that**, not by general quality.

### Access reality first — stated honestly

I could not verify IIT Kharagpur's specific holdings; [library.iitkgp.ac.in](https://library.iitkgp.ac.in/) requires institutional login and its e-resource list is not publicly enumerable. What I can state:

- **ONOS (One Nation One Subscription)**, live Jan 2025 and the thing IIT KGP's library now leads with, is a **journals** deal. It does not cover monographs. Do not expect it to deliver any book on this list.
- Indian institutional subscriptions typically include **Wiley journals**, not **Wiley Online Books**. Sinclair, Taleb, Gatheral, Lopez de Prado and Rebonato are all Wiley — so the most likely outcome is that **none of the Wiley titles are reachable** and you buy them.
- **Springer/Palgrave eBooks** are commonly held by IITs. That makes Leoni (Palgrave) the one title most likely free to you.
- **Cambridge Core** books (Bouchaud) are plausible but institution-specific.
- Natenberg is McGraw-Hill Professional — effectively never in an Indian academic package.

Action: ask the library for the **e-books A–Z list** and specifically whether Wiley Online Books and Cambridge Core Books (not just journals) are in the subscription. That is a two-minute email that resolves ~₹40,000 of purchasing decisions.

---

### Tier 1 — buy these, in this order

**1. Euan Sinclair, *Volatility Trading* (2nd ed., Wiley 2013)**
- **Uniquely gives:** the only book that treats an options trade as a *statistical bet with a cost structure* rather than a payoff diagram. The hedging chapter derives the path-dependence of a delta-hedged option's P&L explicitly — i.e. why your realised P&L is not (σ_realised² − σ_implied²) × vega but a gamma-weighted path integral. The money-management chapter (Kelly, fractional Kelly, drawdown) is where most quant-trained people are actually weakest.
- **Chapters that matter:** volatility measurement/estimators; hedging; money management; trade evaluation. **Skippable:** the introductory BSM derivation, the options-basics chapter.
- **Where dated/wrong:** pre-0DTE, pre-electronic-retail, US-centric. Its vol-forecasting chapter (GARCH-family) is the weakest part and has been overtaken. Nothing on the modern dealer-flow literature.
- **Free equivalent:** none. This is the book with no substitute.
- **Tests:** (2) costs and fills discussed explicitly, (3) 25+ years trading vol, (4) repeatedly names where his own methods fail — **counts double**. Passes cleanly.
- **Caveat:** Sinclair teaches on QuantInsti's paid EPAT programme ([quantinsti.com/faculty/euan-sinclair](https://www.quantinsti.com/faculty/euan-sinclair)). The book does not funnel; his ancillary presence does. Judge the book alone.

**2. Lorenzo Bergomi, *Stochastic Volatility Modeling* (CRC 2016)** — **and Chapters 1 and 2 are free**
- URL: [lorenzobergomi.com/contents-sample-chapters](https://www.lorenzobergomi.com/contents-sample-chapters) — Ch.1 and Ch.2 are direct PDF downloads.
- **Uniquely gives:** the correct answer to "what happens to my book when spot moves." Chapter 1 (24 pp, free, I read it) is titled §1.1 *Characterizing a usable model — the Black-Scholes equation* and §1.2 ***How (in)effective is delta hedging?*** with §1.2.2 *The real case*. It derives the P&L of a delta-hedged short option from break-even accounting, then shows empirically how much hedging error survives. That is Section B's core content, free, from a Société Générale head of quant research.
- **Chapters that matter for you:** 1, 2 (free), 8 (*The smile of stochastic volatility models* — where the skew-stickiness ratio is derived), 9 (*Linking static and dynamic properties*), 10 (*What causes equity smiles?*). **Skippable:** 11 (multi-asset), 12 (LSV) unless you go exotic.
- **Where dated:** written before the 0DTE regime and before rough vol became mainstream; Ch.6 (Heston) is there mostly to be criticised.
- **Free equivalent:** the two free chapters plus his SSRN/paper page [lorenzobergomi.com/papers](https://www.lorenzobergomi.com/papers) (*Smile Dynamics* I–IV) cover perhaps 40% of the book's practical value at zero cost. Read those before deciding to buy.
- **Tests:** (3) built and ran SG's equity-derivatives models, (4) explicitly enumerates where each model class fails and why — double. (5) reproducible.
- **Caveat:** notation is dense and idiosyncratic; there is no code. You will be re-deriving.

**3. Nassim Taleb, *Dynamic Hedging* (Wiley 1997)**
- **Uniquely gives:** the *bookkeeping* of an options book — how a market maker organises risk when he has 500 positions in one name. The vega/volatility-surface chapter and the "bucketing and topography" material are the only book-length treatment of **vega bucketing** written by someone who did it on a desk. Also the only serious treatment of what happens between the greeks (the "delta paradox", pin risk, wing risk, dividend/early-exercise pathologies).
- **Chapters that matter:** the greek "modules" section; vega and the volatility surface; bucketing/topography; the American-options and pin-risk chapters. **Skippable:** the philosophical asides, the exotic-pricing chapters (superseded), anything on rates.
- **Where dated or wrong:** pre-smile-model. It predates SVI, SABR, everything you have implemented. It has no coherent spot-vol dynamics — precisely the gap Bergomi and Klassen fill. Its exotics pricing is obsolete. Read it *for the taxonomy of risk*, not for models.
- **Free equivalent:** none, and nothing has replaced it.
- **Tests:** (3) traded, (4) the entire book is a catalogue of where textbook greeks stop working — double. Passes.
- **Caveat:** badly organised, badly edited, and Taleb's later public persona has made people dismiss the book. Do not. But budget for frustration.

**4. Bouchaud, Bonart, Donier, Gould, *Trades, Quotes and Prices* (CUP 2018)**
- **Uniquely gives:** the cost side, quantitatively. Square-root impact law, order-flow long memory, the propagator model, why your backtest's fill assumptions are the dominant error term. This is the discipline that makes "pure research usable in a trade."
- **Chapters that matter:** the impact chapters (square-root law, propagators), order-book statistics, and the market-making/liquidity chapters. **Skippable:** the latent-liquidity theory chapters unless you go deep.
- **Where dated:** equities/futures-centric; options microstructure is essentially absent, which matters because NIFTY option books behave differently from the underlying.
- **Free equivalent — real one:** Bouchaud, Farmer & Lillo, *How Markets Slowly Digest Changes in Supply and Demand*, [arXiv:0809.0822](https://arxiv.org/abs/0809.0822). ~100 pages, free, covers a large fraction of Parts II–III. **Read this before buying the book.**
- **Tests:** (3) Bouchaud runs CFM, (4) explicit about the domain of validity of the square-root law, (5) reproducible on minute data — you have it. Passes.
- **Caveat:** it will not tell you anything specific about Indian markets, and impact calibration on NIFTY options is unpublished territory.

---

### Tier 2 — worth owning, conditionally

**5. Euan Sinclair, *Positional Option Trading* (Wiley 2020).** The value is the negative result: he argues most named option "strategies" carry no edge and that the edge, where it exists, is in position sizing, selection and exit. Chapters on bet sizing and on the psychology/process are the keepers. Skippable: the strategy-by-strategy catalogue. Caveat: substantial overlap with *Volatility Trading*; buy second, not first.

**6. Sheldon Natenberg, *Option Volatility and Pricing* (2nd ed. 2015).** For you, ~70% is below your level. The parts that are not: the "risk considerations" material on how a spread's greeks migrate as spot and time move, and the market-maker chapters added in the 2nd edition. **Free equivalent:** Harel Jacobson's *Think Like a Market Maker* covers the useful residue ([volquant.medium.com/think-like-a-market-maker-understanding-implied-volatility-b53c25739aa0](https://volquant.medium.com/think-like-a-market-maker-understanding-implied-volatility-b53c25739aa0)). **Recommendation: skip the purchase.** Fails test (2) — no cost model anywhere.

**7. Jim Gatheral, *The Volatility Surface* (Wiley 2006).** You have already absorbed the parametrisation content via SVI/SSVI. What remains valuable: the *dynamics of the volatility skew* chapter and the variance-swap/vol-derivatives chapter. **Free equivalent:** his Baruch MFE lecture notes and slides, [mfe.baruch.cuny.edu](https://mfe.baruch.cuny.edu/) — these overlap the book heavily and are free. **Recommendation: use the notes, skip the book.**

**8. Peter Leoni, *The Greeks and Hedging Explained* (Palgrave 2014).** Short, cheap, and the publisher's own description names exactly your Section-B gaps: *"themes omitted from textbooks but which occur in practice — including the effect of day conventions, interest rates and sticky deltas."* Author: PhD math physics, KBC Asset Management risk, ING exotics front-office quant, then GDF Suez / Macquarie trading. [link.springer.com/book/10.1057/9781137350749](https://link.springer.com/book/10.1057/9781137350749). **Most likely title on this list to be free via your institution** (Springer/Palgrave). Caveat: thin — it is a monograph, not a reference; it will not replace Bergomi.

**9. Marcos Lopez de Prado, *Advances in Financial Machine Learning* (Wiley 2018).** Include it *only* for four things: the triple-barrier labelling scheme, meta-labelling, purged/embargoed cross-validation, and the deflated Sharpe ratio. Those four are genuinely load-bearing if you ever run an ML overlay on option signals. Everything else — HRP, fractional differentiation, the structural-break chapters — is contested and I found no independent practitioner reproduction that vindicates them. **Free equivalent:** Chapter 1 is free on SSRN ([abstract 3104847](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3104847)) and his code sits at quantresearch.org. **Honest negative:** I searched specifically for a substantive published critique of AFML's reproducibility and did not find one from a credible named practitioner — the criticism circulates as forum folklore, not as a citable document. Treat the book's claims as unvalidated rather than validated.

---

### Tier 3 — do not buy

**10. Riccardo Rebonato, *Volatility and Correlation* (2nd ed. 2004).** Parts III and IV — the majority of the book — are interest-rate volatility (LMM, CEV rates, Markov-chain rates). Irrelevant to NIFTY index options. Parts I–II are good but wholly superseded by Bergomi for your purposes. **Skip.**

**11. Euan Sinclair, *Option Trading* (2010).** Largely superseded by his other two. Its market-making-techniques chapter (Ch.10) is the one distinctive piece.

**12. Mack & Sinclair, *Retail Options Trading* (2024, self-published, ~377 pp).** Verified to exist. Positioned at retail-scale edge-finding with Kelly sizing. Reviews are split on level — one credible review says it oscillates between explaining what a long call is and computing rolling VIX z-scores. Given your level, **skip**.

**Books that arguably earn a slot and were not on your list:** Derman & Miller, *The Volatility Smile* (2016) — but Derman's Columbia lecture notes are free and cover most of it. Larry Harris, *Trading and Exchanges* (2002) — the canonical market-structure text, still unmatched, and cheap. Lehalle & Laruelle, *Market Microstructure in Practice* — execution-cost companion to Bouchaud.

---

# (B) PNL ATTRIBUTION AND GREEK BOOKKEEPING

**Headline finding: the field is real, it is documented, and almost all of the good free material was published in the last 18 months by one person — Timothy Klassen. Round one missed it because it searched for "PnL attribution" as an academic topic rather than as a vendor/desk engineering problem.**

### B.1 — Vola Dynamics: the primary corpus

All free, no registration, named author with the CV above. Index page: **[voladynamics.com/media/](https://voladynamics.com/media/)**

**(a) *Spot-vol Dynamics and Deltas for SPX Options*, subtitled "Does anyone know how to calculate the correct delta of a vanilla option?"**
[voladynamics.com/pdf/Vola_SpotVolDynamicsDeltasSPX_LI_20200107.pdf](https://voladynamics.com/pdf/Vola_SpotVolDynamicsDeltasSPX_LI_20200107.pdf) (13 pp — I read all of it)

**What it concretely gives you, and it is directly executable on your minute data:**
- The exact statement δ = δ_BS + vega · (∂σ/∂F), so the whole delta problem reduces to estimating dVdF.
- The estimation recipe: *"the (realized) vol sensitivities can be determined reasonably well using, say, one day's worth of 1-minute or 5-minute snapshot data using a linear regression, with some outlier treatment for robustness."* You are about to receive minute-wise NIFTY data. This is a one-day project.
- The independent check: regress vol changes on forward changes **per strike** to get an empirical dVdF curve, then compare against the one-snapshot model prediction. He shows the two agree.
- Concrete numbers: SSR ≈ 1.3 typical, → 2.0 on big down days, 1 ≤ SSR ≤ 2 with theoretical reason, **KOSPI often above 2** (the one named non-US index — relevant, since NIFTY may behave more like KOSPI than SPX).
- Magnitude of the error you are currently making: ATM delta adjustment ≈ −0.06; put-wing peak ≈ −0.08; and **in the call wing above NS ≈ 1.2 the correct delta is essentially zero while naive BS delta is still 0.03** — a 100% relative error on tradable OTM calls.
- Explicit falsification: *"the 'null-hypothesis' … namely 'sticky-strike', would mean that dVdF is flat at 0. The above results reject that idea on both the absolute and standard deviation level conclusively (ditto for 'sticky-delta' dynamics, or any simple 'combination' of the two)."*
- And the subtlety most people get wrong: **SSR = 1 does not mean sticky-strike.** It means sticky-strike *at the money only*; the wings still move. He shows a day (2018-01-22) where SSR ≈ 1 and dVdF is strongly non-zero in both wings.
- **Tests passed:** (2) — the whole point is quote/spread-aware fitting and he discusses wide markets and error bars; (3) — Getco, Goldman, Cboe; (4) — names where the linear-dVdF approximation "breaks down so dramatically for NS > 0.5", and gives the proof (negative ATF curvature means the ATM parabola cannot describe the call-wing knee); (5) — reproducible on any minute-level option chain, including yours. **Four of five, with (4) double.**
- **Honest caveat:** this is marketing collateral for a paid C++ library. The self-serving claim is explicit — *"Good vol curves that can actually match the market implied vols for liquid names (none in the public domain do)"*. Since you built SVI, take that as a hypothesis to test, not a fact.

**(b) *Real-Time Implied Volatility Surfaces: A Practitioner's View of the Black Arts*, Cboe RMC Quant Conference, 2 Oct 2025** (100 slides)
[voladynamics.com/pdf/Klassen_IVS-BlackArts_CBOE_20251002_distrib.pdf](https://voladynamics.com/pdf/Klassen_IVS-BlackArts_CBOE_20251002_distrib.pdf)

Read slide 74, "**Spot-Vol Dynamics Myths**", which is your Section-B question answered in eight lines:
> *Myth: common "vol regimes" are "sticky-by-strike" or "sticky-by-delta". **Sticky-strike scenarios are still commonly used by risk departments.** In equities, at least, neither has happened for 20y+. Sticky-delta implies SSR=0 for all terms. Never happens. Sticky-strike implies SSR=1 (i.e. sticky-strike around ATM). Even when vols are sticky-by-strike around ATM, they never are in the wings.*

Also in this deck and directly relevant to you:
- Slide 6 and 58: **a quantitative attack on the model you already implemented.** SVI/S5 has "not much shape flexibility, e.g. they do not allow W-shapes as required around events." Of ~5,630 OPRA names, only ~1.2% are bias-free-fittable with SVI; SSVI manages 73%; **SPX/SPY/ES need 16–18 parameters and some market makers use ~25**. Empirical scaling: nParams ≈ (nOptions/5)^(1/3). On IBIT he shows fits "13–70× better than SVI" in the price-difference metric, which he calls "the ultimate test."
- Slide 68: SSR has *term structure* now, can exceed 2 or fall below 1 at the short end, and shows horizon dependence (1-min vs 5-min vs intraday-vs-overnight). If you estimate SSR from 1-minute NIFTY data you will get a different number than from close-to-close, and he says so.
- Slides 82–99: the "vol time" (business/trading time) machinery, event times, and **settlement effects including exchange and bank holidays** — the exact mechanism behind your weekend/holiday theta question.
- **Caveat:** slides without narration. Many pages are plots with two-line captions. You will get maybe 60% of the value without the talk audio.

**(c) The 2025 video series** — short, free, named, no funnel. Verified titles via YouTube oEmbed:
| Video | URL | Why it matters |
|---|---|---|
| **PnL Attribution #1: The Greeks** | [youtube.com/watch?v=GM2vWXKtx6U](https://www.youtube.com/watch?v=GM2vWXKtx6U) | The Taylor/greek decomposition on a real book |
| **PnL Attribution #2: Scenarios** | [youtube.com/watch?v=VNhMExVMlpc](https://www.youtube.com/watch?v=VNhMExVMlpc) | Full-revaluation attribution vs greek attribution — i.e. where the unexplained residual comes from |
| **Thetas and Time Conventions** | [youtube.com/watch?v=35l1FoQ9RvY](https://www.youtube.com/watch?v=35l1FoQ9RvY) | Calendar-day vs trading-day theta, exactly your question |
| **Sticky-by-Strike or Sticky-by-Delta? Neither!** | [youtube.com/watch?v=ShluExtp5xA](https://www.youtube.com/watch?v=ShluExtp5xA) | |
| **If sticky strike is not the answer, what is?** | [youtube.com/watch?v=jDTC2hqFTCU](https://www.youtube.com/watch?v=jDTC2hqFTCU) | Calibrating SSR |
| **Event Modeling: Decomposing Vol Surfaces Around Events** | [youtube.com/watch?v=7Ni8ihAs6vA](https://www.youtube.com/watch?v=7Ni8ihAs6vA) | Two-jump Merton event model; RBI policy / budget / election analogue for NIFTY |

There is a matching LinkedIn article, *Thetas and Time Conventions in the Vola Library* (Dec 2025), listed on the media page. **I could not open LinkedIn** (login wall) — flagging that rather than paraphrasing a summary of it.

### B.2 — Bergomi Chapter 1, free — the derivation itself

[lorenzobergomi.com/contents-sample-chapters](https://www.lorenzobergomi.com/contents-sample-chapters) → Chapter 1 PDF (24 pp).

Gives you the P&L decomposition from first principles as an *accounting identity*, not a model result — his framing: *"a pricing equation is essentially an analytical accounting device: rather than predicting anything about the future dynamics of the underlying securities, a model's pricing equation supplies a decomposition of the profit and loss (P&L) experienced on a derivative position as time elapses."* Then §1.2 *How (in)effective is delta hedging?* with §1.2.2 *The real case* quantifies the residual. **Tests:** (3), (4) — double, (5). **Caveat:** no code, and it stops before multi-factor vega attribution, which is Chapters 8–9 (paid).

### B.3 — The regulator has already answered "how much unexplained P&L means the model is broken"

**BCBS d457, *Minimum capital requirements for market risk* (Jan 2019).** Primary PDF: **[bis.org/bcbs/publ/d457.pdf](https://www.bis.org/bcbs/publ/d457.pdf)** — I downloaded and read the relevant chapters.

**MAR32 — the P&L Attribution (PLA) test.** This is the only quantitative, published, universally-applied standard for "is my risk model explaining my P&L." Exact content:
- Compare **RTPL** (risk-model valuation P&L) against **HPL** (hypothetical P&L: yesterday's positions revalued with today's market data, no intraday trading, no new deals, fees and commissions excluded) — MAR32.20, 32.25, 32.26.
- Two metrics on a **rolling 250-day** window (MAR32.34–32.41): **Spearman rank correlation** of the two P&L series, and the **Kolmogorov–Smirnov** statistic (max absolute gap between the two empirical CDFs).
- **Thresholds (MAR32.42), verbatim:** green requires correlation **> 0.80 AND KS < 0.09** (p = 0.264). Red is correlation **< 0.70 OR KS > 0.12** (p = 0.055). Anything between is amber and carries a capital surcharge.
- Note MAR32.27 footnote 2, which is precisely your theta question: *"P&L due to the passage of time should be included in the APL and should be treated consistently in both HPL and RTPL. Time effects can include… the theta effect… and carry or costs of funding."* The regulator's answer to calendar-vs-business time is **"pick one and be consistent across all three P&L measures"** — inconsistency there is itself a model failure.

**MAR21 — the published vega bucketing specification.** Equity vega risk factors are defined *along one dimension only, the maturity of the option*, mapped to tenors **0.5, 1, 3, 5, 10 years** (MAR21.8–21.14). Within-bucket vega correlation is ρ = min(ρ_delta × ρ_maturity, 1) with ρ_maturity = exp(−α|T_k − T_l| / min(T_k,T_l)) and **α = 1%** (MAR21.93, 21.95).

**The instructive negative:** the Basel standard **does not bucket equity vega by strike or moneyness at all**. Skew risk is pushed into the curvature charge and the residual-risk add-on. So the regulator's own bucketing scheme is deliberately cruder than what your book needs. Use MAR21 as the *floor* — a strike-bucketed vega grid is a strict improvement, and the α = 1% maturity-decay kernel is a defensible, free, published starting point for your own correlation matrix.

- **Tests:** (2) — the whole standard is about valuation and cost adjustments; (3) — written by the people who supervise real books; (4) — MAR32.45 explicitly discusses when the test itself fails ("regime shift", "cross-border financial market stress") — double; (5) — fully reproducible, it is arithmetic.
- **Honest caveat, and it is a real one:** the PLA test compares **model P&L to model P&L** (RTPL vs HPL), *not* model P&L to realised cash. It answers "is my risk system consistent with my pricing system," which is a weaker question than "is my model right about the market." It is also distributional over 250 days, so it gives you **no per-day threshold** for "today's residual is too big." For that, you have to set your own bar — and nobody has published one.

### B.4 — Managing Smile Risk: the primary document on reported delta being wrong

**Hagan, Kumar, Lesniewski, Woodward, *Managing Smile Risk*, Wilmott, 2002.** Free PDF: [deriscope.com/docs/Hagan_2002.pdf](https://www.deriscope.com/docs/Hagan_2002.pdf).

Everyone cites this as "the SABR paper." Its actual thesis is your Section-B question: local-volatility models predict that when spot falls the smile shifts to *higher* prices, whereas real smiles move *with* the underlying — so "delta and vega hedges derived from the model can be unstable and may perform worse than naive Black-Scholes hedges." The backbone concept (how ATM vol moves as the forward moves) is the rates-market ancestor of Bergomi's SSR and Klassen's dVdF. **Tests:** (3) — Hagan/Lesniewski were at Bear Stearns/BNP; (4) — the paper's central claim *is* a failure-mode statement about the then-dominant model, double; (5). **Caveat:** rates/swaptions-native. The SABR parametrisation itself is inferior to what you already have; read it for the diagnosis, not the cure.

### B.5 — Ahmad & Wilmott, *Which Free Lunch Would You Like Today, Sir?*

Wilmott magazine, 2005. Landing page: [wilmott.com/which-free-lunch-would-you-like-today-sir-delta-hedging-volatility-arbitrage-and-optimal-portfolios-riaz-ahmad-and-paul-wilmott/](https://www.wilmott.com/which-free-lunch-would-you-like-today-sir-delta-hedging-volatility-arbitrage-and-optimal-portfolios-riaz-ahmad-and-paul-wilmott/).

Closed-form expected P&L **and variance of P&L** for hedging at three distinct volatilities — true, implied, and your own hedge vol — for a single option and for a portfolio. This is the analytic result behind the empirical fact that "I was right about vol and still lost money." **Tests:** (4) — it is entirely about the dispersion of outcomes when you are right on average; (5) — trivially reproducible. **Caveat:** I could not find a clean free PDF on a stable primary host; the free copies I located are on Scribd/ResearchGate. Fails a strict primary-source standard. Your institutional access likely reaches it via Wilmott's archive.

### B.6 — Honest negatives on (B)

- **There is no credible open-source P&L-explain engine.** I searched GitHub systematically. The best-known hit, [github.com/philippchan/optionsPnL](https://github.com/philippchan/optionsPnL), is a **single Jupyter notebook** (delta/gamma/theta/vega/volga/vanna decomposition with a residual, plus plots). Everything else returned by a targeted GitHub search is a **zero-star toy repo**. Every production implementation is commercial and closed (Vola Dynamics, Murex, Bloomberg MARS). **Conclusion: you will write this yourself, and that is a genuine, defensible piece of work.**
- **The Wikipedia article "PnL explained" is the only free general reference**, and it is thin. That is a statement about the field, not about Wikipedia.
- **Burghardt & Hanweck, "Calendar-Adjusted Volatilities," *Journal of Derivatives*, Winter 1993** is the seminal citation for business-time vs calendar-time variance weighting. I could not reach a free copy, and Portfolio Management Research (which owns JOD) is rarely in Indian institutional packages. Flagging this as **unreachable rather than substituting a blog summary of it**.
- Round one's Moontower has two directly on-topic free posts (weekend theta; cleaning implied vols). Already covered — not re-reported, but do not skip them because of that.

### B.7 — The Indian weekend/holiday problem: the two primary documents

You need these because the business-time question in India is now a *moving target*, not a constant.

1. **NSE Circular 103/2025, Download Ref NSE/FAOP/68589, 17 June 2025 — "Revision in Expiry Day of Index and Stock derivatives contracts."** Primary PDF, verified: [nsearchives.nseindia.com/content/circulars/FAOP68589.pdf](https://nsearchives.nseindia.com/content/circulars/FAOP68589.pdf). Contracts expiring on or before 31 Aug 2025 keep Thursday; contracts expiring on or after **1 Sep 2025 expire Tuesday**, with monthlies on the **last Tuesday**. It cites its parent: **SEBI/HO/MRD/TPD-1/P/CIR/2025/76 dated 26 May 2025**, *Final Settlement Day (Expiry Day) for Equity Derivatives Contracts*.
2. **The NSE trading-holiday circular for the relevant year** (same `nsearchives.nseindia.com/content/circulars/` path). India runs ~14–16 exchange holidays, unevenly clustered around Oct–Nov. That is the driver: a Tuesday-expiry weekly spans 7 calendar days but between **3 and 5 trading days** depending on the week. A calendar-day theta will mis-state a Diwali-week weekly by a large fraction, and the mis-statement flips sign across the holiday.

Why this matters more than in the US: with a Tuesday expiry, the *weekend now sits in the middle of the option's life*, not at the start. Under a calendar-day convention your Monday theta and your Friday theta are the same number; under trading-day they are not, and the difference is the entire P&L of a short weekly on a holiday week. **Nobody has published on business-time theta calibration for NIFTY weeklies.** That is a real gap, and with minute data you are positioned to close it: estimate intraday vs overnight vs weekend variance shares directly from 1-minute returns, then compare the implied vol you back out under each time convention.

---

# (C) THE VIDEO AND X LAYER

**Method disclosure, because it changes how you should read this section:** X/Twitter is login-walled and I could not fetch threads directly. I therefore refuse to hand you a list of "must-read threads" I have not opened. What follows is people whose X output is **mirrored in free, verifiable, long-form material off-platform**, which is the only form of it I could actually check. Treat any thread-level recommendation from any round-one-style report as unverified.

### C.1 — Timothy Klassen (the person you were actually looking for)

Everything in **B.1** is the answer to (C) as well. His YouTube channel is [youtube.com/@VolaDynamics](https://www.youtube.com/@VolaDynamics). Additionally free:
- **Cboe RMC Quant Conference 2025** and **QuantMinds 2023** decks — *State of the Smile: The Ever-Surprising Evolution of the Equity Options Market* ([voladynamics.com/pdf/Klassen_StateOfTheSmile_QMI_20231115_final.pdf](https://voladynamics.com/pdf/Klassen_StateOfTheSmile_QMI_20231115_final.pdf)).
- **Bloomberg Quant (BBQ) Seminar keynote, 24 Feb 2025**, *Secrets of the Implied Volatility Surface: Inferring Rates, Dividends, Events, and Risk-Neutral Densities from Options Prices* — deck at [voladynamics.com/pdf/Klassen_SecretsVolSurface_BBQ_20250225.pdf](https://voladynamics.com/pdf/Klassen_SecretsVolSurface_BBQ_20250225.pdf).
- **CQF Institute QuantSpeak podcast** interview, Sept 2024: [youtube.com/watch?v=O3MA6PYpQEs](https://www.youtube.com/watch?v=O3MA6PYpQEs) (free, on CQF Institute's channel).
- Older but the most narrative of the decks: *Tools for Options Trading in a Crazy World*, MathFin 2021, [voladynamics.com/pdf/Timothy_Klassen_MathFin_20210316_talk.pdf](https://voladynamics.com/pdf/Timothy_Klassen_MathFin_20210316_talk.pdf).

**What to watch, in order, for your specific gap:** *PnL Attribution #1 → #2 → Thetas and Time Conventions → Sticky-by-Strike or Sticky-by-Delta? Neither! → If sticky strike is not the answer, what is?* Then read the *Spot-vol Dynamics* PDF with a notebook open. That sequence is the (B) curriculum.

**Tests:** (2), (3), (4)-double, (5). **Caveat:** vendor. He is selling a library, and the decks argue "buy vs build" in his favour. The content survives that, but you should independently benchmark his SVI criticisms against your own SVI fits on NIFTY before accepting "SVI is inadequate" as a fact about *your* market. He is talking about SPX with 20,000 listed options; NIFTY chains are far smaller, and the parameter-count scaling law he gives (nParams ≈ (nOptions/5)^(1/3)) implies **NIFTY needs materially fewer parameters than SPX** — possibly making SVI/SSVI adequate where it is not for SPX. Test it; don't assume either way.

### C.2 — Sasha Stoikov, *Where market making meets market microstructure*

[youtube.com/watch?v=S7eig5VXFpY](https://www.youtube.com/watch?v=S7eig5VXFpY) — on his own channel, [youtube.com/@sstoikov](https://www.youtube.com/@sstoikov). Verified via oEmbed.

Round one gave you the Avellaneda–Stoikov *paper*. This is Stoikov himself, at Cornell Financial Engineering Manhattan, connecting the reservation-price/inventory framework to what actually happens in a limit order book — micro-price, queue position, adverse selection. It is the bridge between the model you were handed and the fills you will actually get. **Tests:** (3) — he is the author and has worked with trading firms; (4) — his public position is consistently that the closed-form AS model is a starting point whose assumptions fail in real books; (5). **Caveat:** equities/LOB framing, not options. Options market making adds the vol-surface layer that Klassen covers and Stoikov does not.

### C.3 — Cem Karsan: what is actually there, and what is not

**Best free long-form, ranked by technical density:**
1. **Mutiny Fund, Episode 24** — [mutinyfund.com/cem-karsan/](https://mutinyfund.com/cem-karsan/). Free, long, and has a **written transcript**, which makes it the efficient one. Covers dealer hedging → vanna/charm → why positioning pins or accelerates the index.
2. **The Derivative (RCM Alternatives), *Vol Curves and Vanna Charm***, Oct 2020 — [rcmalternatives.com/2020/10/vol-curves-and-vanna-charm-with-cem-karsan-the-derivative/](https://www.rcmalternatives.com/2020/10/vol-curves-and-vanna-charm-with-cem-karsan-the-derivative/). The origin episode; he walks through his market-making background before the framework.
3. **Market Huddle Ep. 113, "Charming Vanna"** — [youtube.com/watch?v=AdN2_7Xat1o](https://www.youtube.com/watch?v=AdN2_7Xat1o). Verified. More conversational, less structured.

**What each teaches:** the mechanism by which a dealer book that is systematically short calls / long puts must buy weakness and sell strength; why charm (delta decay) concentrates flow into the last hours before monthly OpEx; why vanna dominates in a falling-vol grind.

**Honest caveat, and it is severe: Karsan has never published the computation.** In none of the free long-form does he specify how gamma/vanna exposure is estimated from open interest, what the dealer-sign assumption is, or how it is validated. The framework as he presents it is **unfalsifiable as stated**. Two consequences:
- The commonly-cited underlying methodology is SqueezeMetrics' *The Implied Order Book* ([squeezemetrics.com/download/The_Implied_Order_Book.pdf](https://squeezemetrics.com/download/The_Implied_Order_Book.pdf)) — which is **anonymous** and attached to a paid data product. **Under your own filter that is an auto-reject on two counts.** I am reporting it so you know what the chain of custody is, not recommending it.
- The credible, named, free, testable version of the same claim is **Barbon & Buraschi, *Gamma Fragility*** (Univ. of St. Gallen School of Finance RP 2020/05) — free PDF at [alexandria.unisg.ch/bitstreams/25fec636-90a2-4735-a3a4-dfc0b68d3feb/download](https://alexandria.unisg.ch/bitstreams/25fec636-90a2-4735-a3a4-dfc0b68d3feb/download), SSRN [abstract 3725454](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3725454). It finds intraday momentum under negative aggregate dealer gamma and reversal under positive, **conditional on illiquidity**. That conditioning is the failure mode Karsan never states. **Read Barbon–Buraschi first, then Karsan as colour.** With NIFTY OI data and minute bars, this is directly replicable on an Indian index — and to my knowledge unpublished there.

### C.4 — Benn Eifert (QVR Advisors)

Media index: [qvradvisors.com/media](https://www.qvradvisors.com/media). Verifiable CV — founder/CIO of QVR, a real vol-arb manager; no course, no signal service.

**Specific episodes worth your time:**
- **Alpha Exchange, June 2025** — on **crowded risk-managed option strategies**: buffer ETFs, systematic overwriting, and his conclusion that many of these "often reduce beta without providing meaningful downside protection." This is the most directly useful thing he has said, because it is a structural-supply argument about *why* certain parts of the surface are priced where they are.
- **Forward Guidance, June 2022** — the broadest single overview: puts as insurance vs as trades, single-stock vs index vol, retail flow, market-structure evolution.
- **The Derivative, Feb 2021** (~1h31m) and **ReSolve Riffs with Eifert & Scott Maidel** — more on implementation.

**What it teaches that books do not:** how a vol book is actually funded, sized and stopped out; where the crowding is; why a strategy that backtests can be uninvestable at size. **Tests:** (2) — he is unusually explicit about spreads, capacity and financing; (3); (4) — he is the most reliable public source for "this popular trade does not do what its marketing says," double. **Caveat:** audio only, no slides, no code, and he is talking his book — QVR sells the sophisticated version of the products he criticises.

### C.5 — Harel Jacobson — the closest thing to a free, written, market-maker-perspective course

[volquant.medium.com](https://volquant.medium.com/) — all free, no paywall, no funnel. ~15 years in FX vol trading.

**The specific pieces, in order:**
1. **"(Almost) Everything You Wanted To Know About FX Volatility Smile," Parts I / II / III** ([Part I](https://volquant.medium.com/almost-everything-you-wanted-to-know-about-fx-volatility-smile-part-i-intro-to-the-fx-market-4a3ba8052e08), [Part II](https://volquant.medium.com/almost-everything-you-wanted-to-know-about-fx-volatility-smile-part-ii-exotic-options-vol-b849e00ab6a9), [Part III](https://volquant.medium.com/almost-everything-you-wanted-to-know-about-fx-volatility-smile-part-iii-options-flows-c9987354b95d)). **Part II is the one that matters for you even though you trade index, not FX**: it explains *why* the smile has the shape it has as a consequence of dealers hedging exotic books — RR to hedge vanna from barriers, BF to hedge volga from digitals/touches. That is a supply-side explanation of skew and convexity that no equity-options text gives you. Part III is dealer-positioning done by someone who states his assumptions.
2. **"Volatility Smile and Delta Hedging," Parts 1 & 2** — smile-consistent delta hedging, the same question as Klassen's dVdF, worked in the FX conventions.
3. **"Think Like a Market Maker — Understanding Implied Volatility."**
4. **"A Common Sense Guide to Volatility Trading [Code Included]"** — the one with runnable code, which is why he passes test (1).
5. **Flirting with Models, S5E10, "Trading FX Volatility"** with Corey Hoffstein — free, transcribed.

**Tests:** (1) — code in at least one piece; (3) — 15 years FX vol; (4) — he is explicit that his positioning model is "less generalized" and microstructure-specific; (5). **Caveat:** FX conventions (delta-strike quoting, RR/BF, premium-adjusted deltas) do not transfer to NIFTY without translation, and he tells you so. Also his most substantive recent output has migrated to LinkedIn, which I could not fetch.

### C.6 — Alpha Exchange (Dean Curnutt) as an archive, not an episode

[axpod.com](https://www.axpod.com/) / [youtube.com/@Alpha_Ex_LLC](https://www.youtube.com/@Alpha_Ex_LLC). Curnutt founded Macro Risk Advisors in 2008 after ~30 years in markets. Free, hundreds of episodes, guests are almost uniformly people who ran real books. Use it as a **search index over desk practitioners**, not as a curriculum. **Caveat:** it is a conversation show — no maths, no code, and the signal-to-length ratio is guest-dependent.

### C.7 — Honest negatives on (C), which are load-bearing

- **The Bloomberg Quant (BBQ) Seminar recordings are not freely available.** The series is chaired by Bruno Dupire and the speaker list is excellent, but every 2024–25 event page routes to a registration wall and the webcast link is emailed on registration. **The speakers' own slide PDFs are frequently free** (that is how Klassen's Feb 2025 keynote is reachable). Strategy: register for the free webinars going forward; retroactively, chase speakers' personal sites for decks.
- **There is no free "Baruch MFE Financial Engineering Practitioners Seminar" video archive.** I searched for it specifically. What Baruch has publicly is the Pre-MFE programme (paid seminars) and free *lecture notes/slides* at [mfe.baruch.cuny.edu](https://mfe.baruch.cuny.edu/) — Gatheral's included. The Columbia IEOR seminar of that name is a for-credit course (IEOR E4798), not public video.
- **The Indian options video and X layer contains essentially nothing that passes your filter.** I looked. Effectively all Indian long-form options content is either broker-affiliated education (auto-reject), course/mentorship funnels (auto-reject), or "I made ₹X" content (auto-reject). **The correct conclusion is that for Indian-market-specific options craft there is no free practitioner video layer, and you should not go looking for one.** Your Indian-specific inputs should be exchange and regulator primary documents (NSE circular archive at `nsearchives.nseindia.com/content/circulars/`, SEBI circulars) plus your own data — and the technique layer should come from the US/EU sources above, translated.
- **On X specifically:** I could not access it. I am not going to list handles or threads I have not read. If you want that layer swept properly it needs a session with a logged-in browser, and the honest expected yield is low — the people worth reading on X (Eifert, Jacobson, Karsan) all publish their substantive work off-platform, which is exactly why they are in this report.

---

## What I could not verify

- IIT Kharagpur's actual e-book holdings — library site is login-gated. All access claims in (A) are inference from publisher and consortium patterns, flagged as such.
- Any LinkedIn article (login wall), including Klassen's *Thetas and Time Conventions in the Vola Library*. The YouTube video of the same name is verified and is the accessible substitute.
- Burghardt & Hanweck (1993) — no free copy located.
- Chapter-level content for Taleb, Natenberg, Rebonato, Sinclair and Lopez de Prado is from prior knowledge, not from opening the books this round. Chapter *titles* I have named should be treated as approximately, not exactly, correct.
- Video durations for the Vola Dynamics series — oEmbed confirms existence, title and channel, not length.
- No substantive published critique of *Advances in Financial Machine Learning* was found. Its methods should be treated as unreplicated rather than as either validated or refuted.