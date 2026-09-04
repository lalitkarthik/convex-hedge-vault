# From a fitted surface to an actual trade

Verification note: everything below was checked against the live page or PDF unless explicitly marked **[unverified]**. Items I could not verify are labelled rather than dressed up.

---

## PART A — SURFACE → TRADE

### A1. Vola Dynamics (Timothy Klassen) — the single best source here
- **Asian indices fitting examples** — https://voladynamics.com/examples/asian-indices *(fetched and read)*
- **"Arbitrage-Free Parametric Volatility Surfaces and Real-Time Fitting", Global Derivatives Chicago 2017 (PDF)** — https://voladynamics.com/pdf/Klassen_GD_Chicago_2017.pdf *(fetched and read)*
- **Media & Research index** — https://voladynamics.com/media/ *(fetched)*. Lists a CBOE RMC Oct-2025 talk, *"Real Time Implied Volatility Surfaces: A Practitioner's View of the Black Arts"* — described as covering "where standard approaches like SVI break down". **[unverified — I did not locate the direct PDF/slide link, only the index entry]**. Free YouTube series covers PnL-attribution-by-Greeks, calendar-vs-vol-time theta for 0DTE, and Skew Stickiness Ratio calibration.

**What it concretely gives him:**
- The correct answer to "how big must a residual be": Vola attaches **error bars to every fitted vol**, widening automatically as quote quality degrades. Tradeable residual = residual that exceeds the fitter's own uncertainty at that strike, not a fixed 2-vol-point rule.
- Explicit statement that the **mid is the wrong input in the wings**: their KOSPI example shows puts quoting 0.02×0.03 next to 0.01×0.02 — tick-size quantization that makes wing mid-IVs pure artefact. Low-latency clients feed size-weighted / book-depth micropricess with temporal smoothing instead of mids. This is exactly the "wings are noise" failure mode in your brief, stated by someone who sells the fix to ~50 options firms.
- Zero-bid options drag mid-IV down in both wings; a naive fitter chases it, a robust one does not.
- Dividend modelling: spot vs hybrid (cash-buffer) models, and why hybrid wins; de-Americanisation before any implied vol is even meaningful. This is where "surfaces that look mispriced because of dividends/borrow" actually comes from.
- Settlement prices for illiquid series are *themselves* produced by a fitted surface — so a residual measured against exchange settlement data is partly measuring someone else's fitter.

**Tests passed:** (2) partly — quote-level microstructure, not commissions; (3) strongly — it is a production fitter sold to trading firms; (4) **double** — the Asian-indices page is essentially a catalogue of its own failure modes, and the 2025 talk is advertised as "where SVI breaks down"; (5) — reproducible on any bid/ask snapshot.

**Honest caveat:** the good stuff (C-curve design, the 12- and 14-parameter curves, the error-bar machinery) is client-only. The free material tells you *what* breaks and roughly why, not how their fitter fixes it. Also: they are selling something, so "SVI can't fit W-shaped earnings smiles" is a true statement made by an interested party.

### A2. Colin Bennett, *Trading Volatility, Correlation, Term Structure and Skew*
- Free PDF from the author's own site: http://trading-volatility.com/Trading-Volatility.pdf ; a mirror of the original Santander research compendium: https://physikinvest.com/wp-content/uploads/2022/06/book-colin-bennett-et-al-volatility-trading-santander-full-doc.pdf **[link existence verified via search result metadata only — I did not download either file this session]**

**Concretely:** the structural half of "surface → trade" — when a calendar expresses term-structure view vs. when it is just a vega/theta mismatch, why risk reversals and put-spread-vs-put financing behave differently as skew moves, how a skew position bleeds through spot moves rather than through skew itself. Bennett was head of derivatives strategy at Santander/Barclays; the book is desk research, not academia.

**Tests:** (3) author actually built and sold these structures institutionally; (4) reasonably explicit about when each structure disappoints.

**Caveat:** European institutional index-vol frame, ~2012 vintage. No code, no cost model worth the name, and nothing about weeklies or 0DTE. It tells you what trade to put on, never whether the edge survives your spread.

### A3. Moontower — Kris Abdelmessih (free, no funnel)
- https://moontower.substack.com/p/primer-3-the-nature-of-edge
- https://moontower.substack.com/p/market-maker-privilege
- https://moontowermeta.com/notes-on-trading-volatility-correlation-term-structure-and-skew/ (his notes on Bennett)

**Concretely:** the definition of fair value you need before "rich/cheap" means anything — fair value is *where you can actually transact*, not where your model says. 12 years making markets on NYC floors; blunt that institutional options is a low-margin scale business where edge per trade is small and infrastructure/commission tier decides survival. That reframes the residual question correctly: a 1-vol residual inside a 3-vol-wide market is not an edge, it's a quote.

**Tests:** (3) verifiable market-maker career; (4) repeatedly, including on why retail-visible vol edges are fake.

**Caveat:** essays, not method. No code, no numbers you can lift into a threshold. Use it to calibrate judgement, not the engine.

### A4. Bali, Beckmeyer, Mörke, Weigert — *Option Return Predictability with Machine Learning and Big Data*, RFS 36(9), 2023
- https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3895984

**Concretely:** 12M delta-hedged US equity-option observations, 265 characteristics, and — the reason it is here — long/short performance reported **gross and net of transaction costs** using quoted/effective spreads. It is the cleanest public calibration of how much of an options cross-sectional signal survives crossing the spread.

**Tests:** (2) explicit cost treatment; (5) OptionMetrics-reproducible.

**Caveat, blunt:** monthly rebalancing on US single-name options. The effective-vs-quoted-spread assumption does most of the work in the "profits survive costs" claim; at full quoted spread much of it does not. This is *academically popular and practically fragile* — treat it as a cost-sensitivity template, not a strategy.

### A5. Crypto leg — SVI on Deribit with hedging costs
- **Matic, Packham, Härdle, "Hedging Cryptocurrency Options"** — https://arxiv.org/pdf/2112.06807 — search result indicates SVI parameterisation applied to Deribit option data with hedging-cost analysis **[content confirmed only from search snippet; I did not read the PDF]**.
- Deribit's public history API + Tardis.dev free samples make this the one venue where you can genuinely reproduce an institutional-grade surface study yourself.

**Tests:** (2), (5).

**Caveat:** Deribit's BTC/ETH surface is inverse-settled and quoted in coin terms; a naive SVI in USD-strike log-moneyness silently mixes a quanto effect into your skew residual. Also, the surface has *very* few liquid expiries (weeklies, monthlies, quarterlies) — SSVI term fitting there is fitting through 6-8 points.

---

## Rejected under your own filter (so you don't waste time when they surface)

- **flashalpha.com, menthorq.com, riskhub.org, optionx.trade, thesilenttrader.in, dev.to "complete guide" posts** — SEO content with paid API/subscription funnels. FlashAlpha in particular tells you "residual > 2 vol points = sell it, ≈$0.50 edge per contract on 30-DTE SPY" with **no spread analysis at all**, attached to a $1,199/mo endpoint. That number is the exact naive rule your brief is trying to avoid.
- **GitHub: MiniKetch/vol-surface, tfrmma/options-volatility-trading-strats, Lexian-6/adaptive-volatility-arbitrage, mo-479/options-vol-surface, iceokoli/SVI-Crypto, arkonique/ssvi** — anonymous authors, no verifiable background, several dated 2026 with README prose that reads machine-generated; `mo-479` admits its chain is **synthetic**; `Lexian-6` admits **"no bid-ask spread modeling for options"**. Auto-reject. Two are still worth *reading* for structure (not authority): `tfrmma` uses Whalley–Wilmott no-transaction-cost hedging bands instead of clock-based rebalancing, and has a test that a calendar-arb constraint actually rejects fits an unconstrained SVI would accept — both are the right ideas regardless of who wrote them.
- **Zerodha/Sensibull/Samco/Angel One "education"** — broker-affiliated, order flow is the business model.
- **QVR / Benn Eifert** — I went looking for him as a practitioner source on crowded vol-RV. What I found instead: Bloomberg, May 2026, QVR closing its hedge fund after a ~30% loss Jan–Apr 2026. His public writing on crowding remains substantively good and he is maximally verifiable, but there is no free letter I could locate that documents method — only interviews and X threads. Not a primary source. The blow-up itself is the honest data point: vol relative value run by one of its most articulate practitioners lost 30% in four months.

---

## PART B — DOES SVI WORK ON NIFTY WEEKLIES?

### The finding first: nobody has published this, and that is real open ground.

I searched for practitioner work, Indian quant blogs, and academic literature applying SVI/SSVI to NIFTY/BankNifty/Sensex. What exists:

1. **Indian academic IV literature is descriptive, not parametric.** "Stylized patterns of implied volatility in India: a case study of NSE Nifty options"; "Determinants of the implied volatility function on the Nifty index" (AAMJAF 2008, https://ejournal.usm.my/aamjaf/article/download/aamjaf_vol4-no1-2008_3/pdf/641); "Modeling of implied volatility surfaces of Nifty index options", Int. J. Financial Engineering 2019 (https://www.worldscientific.com/doi/abs/10.1142/S2424786319500282 — **paywall blocked my fetch; method unverified**, but the surrounding literature is smile-shape and determinants-of-IV work, not arbitrage-free parameterisation). None of it trades anything.
2. **Vola Dynamics — the strongest indirect evidence.** On their Asian-indices page they write that Indian index options have become by some metrics the most traded in the world and invite you to "contact us" about fitting NIFTY and BANKNIFTY — i.e. the people who actually solve this treat it as a commercial product and publish nothing. Their KOSPI/Nikkei/HSI examples are the closest public analogue to what NIFTY wings do.
3. **One hackathon repo, and it is the only public SVI-on-NIFTY artefact I found:** https://github.com/who-else-but-arjun/SVI-IV-Surface-Model — regime-segmented SVI (KNN regime classifier → 24 separate surfaces across 3 regimes × 2 option types × 4 maturities), multi-start L-BFGS-B in total-variance space, post-hoc corrections for put-call parity, calendar monotonicity, butterfly convexity, IV floor at 5%. Validation RMSE ≈ 0.58 vol points. NQFO hackathon, IIT Guwahati. **Caveat:** it is an IV *imputation* competition, not a trading study; fitting per option type separately is a red flag (a correct fit uses OTM only and one curve per slice); no costs anywhere.
4. **A genuine first-hand account, low authority:** https://www.linkedin.com/posts/daksh-dagariya_last-month-i-built-a-real-time-implied-volatility-activity-7466135692683915264-6a0v — built a live NIFTY SVI surface, reports NSE chain data is "far messier than I initially assumed", strikes sparse or stale, raw fits jagged and unstable near spot, so he warm-starts each slice from the previous solution to stop tick-to-tick jitter and weights ATM strikes more heavily. Verifiable person, no institutional backing, no cost model. Treat as a field report, not a result.
5. **Generic NSE data plumbing** (Bhavcopy pipelines): https://github.com/sajal101agrawal/nse-options-last-5-years and https://github.com/nesarw/IndexVol — EOD settlement data, IV/Greeks, smile and surface views. Useful only as ingestion reference; both compute IV off settlement prices, which for illiquid strikes are exchange-model outputs, not market prices.

### Structural facts that decide the answer (regulatory changes verified; the modelling consequences are my reasoning, not a cited source)

- **SEBI, Oct 2024: one weekly expiry per exchange.** BankNifty, FinNifty and Nifty Midcap Select weeklies ended 13/18/19 Nov 2024. **BankNifty is monthly-only now.** Any SSVI/calendar-arbitrage work on BankNifty has ~3 usable maturities. Your BankNifty term structure research is, structurally, no longer available.
- **NSE expiry moved Thursday → Tuesday effective 1 Sep 2025** (BSE Sensex on Thursday). Every historical NIFTY term-structure dataset has a break at that date: DTE-to-calendar mapping, day-of-week vol seasonality, and expiry-day gamma effects all shift. Any minute-wise backtest spanning Sept 2025 that doesn't handle this is broken and will not tell you.
- **Forward is the first thing that breaks, before SVI ever runs.** NIFTY weekly options have no matching weekly future. If you take the forward from the nearest monthly future, or worse from spot with a dividend-yield guess, the error enters as an apparent put-call IV asymmetry that looks exactly like a skew dislocation. Imply the forward per expiry from put-call parity on the liquid near-ATM strikes and fit OTM-only — otherwise your best-looking "residuals" are your own forward error.
- **Wing quotes are tick-quantized to ₹0.05.** A NIFTY weekly put quoting 0.05×0.10 is a 67% relative spread; in vol terms the bid-ask straddles tens of vol points. This is Vola's KOSPI problem in a more extreme form, and it means: *the wings of a NIFTY weekly do not contain a fittable vol level at all*. Fitting SVI's linear-in-|k| wings to them is fitting to the tick grid.
- **The front slice is 0-2 DTE most of the time.** Total variance w = σ²T is ~1e-4 there; the SVI loss surface in (a,b,ρ,m,σ) becomes nearly flat in ρ vs m, and calibration pins ρ at its bound — the identifiability failure that shows up even on clean synthetic chains. SVI's asymptotically-linear wings are a large-T argument; at 1 DTE the true smile is jump-dominated and V-shaped near the money.

### What to actually do instead — my recommendation, stated as recommendation

Fit **SVI only on the band where the market genuinely quotes two-sided size** (roughly 10Δ–10Δ on NIFTY weeklies, tighter on expiry day), in total variance, on OTM-only mids with a width-based weight (weight ∝ 1/vega-spread), and **extrapolate the wings** rather than fit them. Publish an error bar per strike from the quote width and refuse to call anything rich or cheap unless the residual exceeds it. Anyone claiming a wing dislocation on a NIFTY weekly put quoting 0.05×0.10 is reporting a tick, not a trade. The tradeable relative-value in that chain is almost certainly *term structure across the weekly/monthly stack and the expiry-day ATM* — not the wings.

**This is genuinely unpublished ground.** With minute-wise NIFTY data, a rigorous public study of "where does SVI's fit residual exceed its own error bar on NIFTY weeklies, and does that residual mean-revert net of the ₹0.05 tick and STT" would be the first of its kind that I can find. That is a paper and a strategy at the same time.

---

## PAID — worth considering later (no free equivalent found)

- **Euan Sinclair, *Volatility Trading* (2ed) and *Positional Option Trading*.** He traded for two decades, states costs and edge decay explicitly, names failure modes throughout, and is the standard reference for sizing off vega/gamma rather than notional. There is no free substitute for the position-sizing chapters. Check IIT Kharagpur's Wiley access before buying.
- **Vola Dynamics library.** Commercial. The free talks tell you what breaks; the library is what fixes it.