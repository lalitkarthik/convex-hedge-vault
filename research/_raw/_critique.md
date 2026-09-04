# COMPLETENESS CRITIQUE — nine reports, gaps only

Note: this is an analysis of the supplied excerpts. I ran no verification searches (excerpts are truncated; several gaps below may be filled in the untruncated tails — I mark those `[may be truncated-out]`).

---

## 1. FIELDS NOT COVERED BY ANY AGENT

**1.1 Realised-volatility estimation from minute data.** Nothing on microstructure-noise bias, optimal sampling frequency, realised kernels, bipower/jump-robust estimators, or intraday vol seasonality (the NSE U-shape plus the 15:20–15:30 expiry spike). Every VRP claim in `landscape` is IV-minus-RV, and no report says how RV is to be measured. His single largest new asset is minute bars; the estimator choice is the first thing that touches them and it is absent.

**1.2 Discrete-hedging error theory.** `backtest-and-data` quotes Sinclair that a $0.10/share hedge cost equals ~2 vol points, then stops. No Leland, no Zakamouline/Whalley-Wilmott hedging bands, no Davis-Panas-Zariphopoulou. This is the direct answer to "how often do I hedge", it is closed-form, it is implementable this week, and it dominates the surface work in P&L terms.

**1.3 Margin as a modelled object.** SPAN/PRISM appears only as the phrase "you need a margin model". Nothing on NSE's PRISM risk-parameter files, portfolio margining across legs, intraday margin recomputation, or margin-driven forced liquidation as a backtest event. For an undefined-risk Indian book margin is the binding constraint and it is fully simulable from published exchange files.

**1.4 Execution and microstructure.** No Almgren-Chriss, no Obizhaeva-Wang, no order-flow-imbalance/microprice literature, no queue-position reasoning, no treatment of the fact that minute bars erase the information execution research needs. `vol-surface-to-trade` gets the closest (Klassen on wing quotes) and that is quote-*quality*, not execution.

**1.5 Dispersion / implied correlation.** NIFTY-vs-constituent single-stock vol is one of the few structurally uncrowded Indian options trades. It appears exactly once — as a casualty in `crypto-plumbing`'s tax arithmetic — with no source, no liquidity assessment of NSE single-stock options, and no mention that SEBI's stock-F&O eligibility churn makes the constituent set non-stationary.

**1.6 The SEBI Nov-2024 F&O rationalisation as a structural break in his data.** No agent mentions it. Weekly expiry consolidation to one per exchange, contract-size increase, and the removal of index weeklies changed the microstructure of exactly the instrument he is about to backtest. Any NIFTY study spanning the change is pooling two different markets. `income-base-rates` prices a lot of 75 without flagging that pre-change data uses a different lot.

**1.7 Indian index-options *tax* treatment.** `crypto-plumbing` gives 900 words of VDA arithmetic and no agent states the treatment of NSE F&O — business income, full set-off, carry-forward, s.43(5)(d) non-speculative status, tax-audit thresholds. The asymmetry between the two regimes is arguably the single largest determinant of which venue he should build for, and only one side of it was computed.

**1.8 Crypto *options* (as distinct from perps).** Crypto is weighted 40% and he is an options specialist. `crypto-strategies` covers funding carry, cash-and-carry, liquidation cascades. Nothing on Deribit surface dynamics, DVOL, perp-vs-option basis, the option-implied funding relation, or Deribit block/RFQ structure. The intersection of his actual skill with the heaviest-weighted region is empty. `[may be truncated-out]`

**1.9 Position sizing and risk of ruin.** "Survival-through-drawdown design" is named as the requirement and no source is given for it. No Kelly/fractional-Kelly, no drawdown-constrained sizing, no Thorp/Sinclair sizing material.

**1.10 PnL attribution and greek bookkeeping.** Sticky-strike vs sticky-delta, vega bucketing, calendar-vs-business-time theta, unexplained-PnL as a model-error detector. Klassen's YouTube series is named in one line as containing this; nobody treats it as a field. It is the diagnostic layer that tells him whether any of the above is working.

**1.11 Market making as a discipline.** One repo (`adityatomar15`). No Avellaneda-Stoikov, no Guéant, and — more usefully — no honest statement of whether a retail participant can quote Indian options at all without exchange MM incentives.

---

## 2. ASSERTED BUT UNVERIFIED, AND DECISION-CHANGING

Ranked by how much his plan moves if the claim is false.

**2.1 `backtest-and-data`:** "an **August 2026 correction notice on the repo** states a unit-scale error charged the bid-ask half-spread at 1/100 of its true size… After the fix, *no strategy or basket retains a positive net Sharpe*." This is the load-bearing artefact of that entire report and the evidentiary basis for "treat every 0DTE result as unproven". No independent confirmation is offered that the notice exists or says this. Verify the repo commit/notice directly before quoting it to anyone.

**2.2 `income-base-rates`:** LRS prohibits funding a US options account. The report itself flags GIFT City/IFSC as "unverified" and sources the main claim to a broker's education page. If a compliant route exists, the US moves from "technique source" to "venue" and the weighting of his whole plan changes.

**2.3 `income-base-rates`:** Delta Exchange India's FIU status and options book depth — explicitly not verified, and it is named as the *only* remaining crypto-options venue. If depth is inadequate, the 40% crypto weight has no options expression at all.

**2.4 `crypto-plumbing`:** the 115BBH same-asset-netting question. Self-flagged as contested with no circular, and the report states the consequence correctly: transaction-level reading makes every hedged crypto book non-viable. Currently the single largest unresolved P&L switch in the whole set.

**2.5 `practitioners`:** "dealer-positioning proxies are computable from open interest + a Black-Scholes gamma map, and the OPEX-window effects are testable directly." Stated as fact. Dealer sign is not observable from OI; GEX-style proxies require an assumption about who is long which side. No evidence of out-of-sample value on NIFTY is offered. This is presented as the one implementable framework from that report and it rests on an unstated identifying assumption.

**2.6 `landscape`:** SEBI's "91% of individual F&O traders lost money, ₹1.06 lakh crore in FY25", used to support "a large share of that is naive short vol". The statistic (if the figure is right) says nothing about strategy composition. The inference is the report's, not SEBI's, and it is doing real work in the "Indian VRP is fat but lethal" conclusion.

**2.7 `income-base-rates`:** margin figures (₹1.5–2L/lot strangle, ₹3–3.25L 0DTE straddle) — self-flagged as broker/practitioner numbers. They set his hard capital floor.

**2.8 `regime-and-strategy`:** (a) "Gaussian HMMs fail to reproduce volatility clustering" — self-flagged unverified; (b) the stronger claim that *most* impressive published HMM backtests are contaminated by smoothed states. No specific contaminated example is cited. The second claim is the report's central verdict and rests on no named instance.

**2.9 `vol-surface-to-trade`:** both Bennett PDF links verified "via search result metadata only — I did not download either file". Also the CBOE RMC 2025 Klassen talk, self-flagged unverified.

**2.10 `social-sweep`:** `rajmaurya0904/bhav`'s "realistic Indian cost model" is the repo's own README text, unaudited, 26 stars. It is simultaneously described as "the single most on-target" Indian item.

---

## 3. DIRECT CONTRADICTIONS

**3.1 Is the fit residual a signal? `landscape` vs `vol-surface-to-trade`.**
- `landscape`: "Where it is still alive: *intraday* refitting on minute data, quote-quality filtering, and detecting when the fit residual itself is the signal."
- `vol-surface-to-trade`: the mid "is the wrong input in the wings… tick-size quantization that makes wing mid-IVs pure artefact"; "Zero-bid options drag mid-IV down in both wings"; and "Settlement prices for illiquid series are *themselves* produced by a fitted surface — so a residual measured against exchange settlement data is partly measuring someone else's fitter."

The residuals are largest exactly where the second report says they are measurement artefacts. `landscape` offers residual-as-signal as the surviving use of his SVI work; `vol-surface-to-trade` deletes most of its support. Neither reconciles this and it decides whether his existing SVI codebase has a trade in it.

**3.2 Crypto funding carry: do it, or cannot do it? `crypto-strategies` vs `crypto-plumbing` + `income-base-rates`.**
- `crypto-strategies`: "The trade still works… **Hummingbot `scripts/v2_funding_rate_arb.py`**… Working multi-venue funding arb."
- `crypto-plumbing`: "note *which* strategies have W/L near 1: delta-hedged option books, market-making, stat-arb, **funding carry**… A high-Sharpe, high-turnover book is the worst possible thing to run inside 115BBH."
- `income-base-rates`: "**Deribit… is not FIU-IND registered**… 'crypto vol' as an individual path from India runs through domestically registered venues."

One report hands him a runnable implementation; two others say the venue is blocked and the tax code inverts the sign of the return. No agent resolves it.

**3.3 Cost lever vs premium size.**
- `landscape` on VRP: "the only options 'return stream' that is a compensated risk premium rather than a forecasting bet."
- `backtest-and-data` quoting Sinclair: a daily-hedged short straddle at "$0.10/share hedging cost differs from the costless-hedge version by roughly two volatility points — i.e. your cost model is as big a lever as your entire vol forecast."

If hedging costs consume ~2 vol points and Indian IV-RV spreads are of comparable order, the "compensated premium" framing is not obviously true net of execution. Nobody puts the two numbers on the same page.

**3.4 Unresolved, not strictly contradictory:** `regime-and-strategy` declares regime detection largely broken as a conditioning layer; `landscape` lists it as a live field. Cannot judge from the truncation which way `landscape` calls it.

---

## 4. UNDERREPRESENTED SOURCE CLASSES

- **Indian practitioners: zero.** Not one named Indian options trader, blog, or repo author with code and a cost model. The 30% India weighting is met with regulation, tax and fee tables — no craft. This is the largest structural hole in the set.
- **Primary exchange/regulator documents: zero.** No NSE circulars, no SPAN/PRISM file specs, no SEBI study PDFs, no Deribit/Delta/Upstox API docs. Indian claims are sourced to taxguru, koinly, an accounting blog and Zerodha Varsity — secondary throughout, on precisely the points where the arithmetic is load-bearing.
- **Working repos with Indian cost models: one, unaudited** (`bhav`). Everything else in `social-sweep` is US/crypto or a calibration notebook he does not need.
- **Honest failure reports: two** (Vilkov's self-correction, the Oct-10 SSRN post-mortem) — both institutional. No first-person "I ran this with money and it lost" account, no fund letters, no post-mortem of a blown-up Indian short-vol book. Test (4) counts double in his filter and the set barely satisfies it.
- **Books: one (Bennett).** He has IIT-KGP institutional access; Sinclair (*Volatility Trading*, *Positional Option Trading*), Natenberg, Taleb *Dynamic Hedging*, Bouchaud *Trades, Quotes and Prices* are all reachable and none appear. `practitioners` even establishes Sinclair's credibility, then cites only two podcasts.
- **Video and X: swept by nobody.** `social-sweep` states this outright ("X and YouTube were not swept at all"). Klassen's and Karsan's free, non-paywalled substance lives mostly there. A named, acknowledged hole that no other agent covered.
- **Crypto-options sources: near-zero**, against a 40% weight.

---

## 5. THREE HIGHEST-VALUE FOLLOW-UP QUESTIONS

**5.1 What is the actual bid-ask half-spread and realistic fill for NIFTY weekly options, in basis points, by moneyness and DTE — and does the Vilkov correction notice say what report A1 claims?** One number decides whether any of this survives, both reports that raise cost-model risk raise it about US products, and no agent supplies the Indian equivalent. Pair the verification with a direct measurement from his own minute data. Everything else is conditional on this.

**5.2 What is the complete Indian tax and margin arithmetic for NSE index options — business-income treatment, set-off, carry-forward, audit thresholds — set side by side with the 115BBH VDA arithmetic, and with SPAN/PRISM margin computed from the exchange's own risk-parameter files?** The set has computed one half (crypto) in detail and the other half not at all, then implicitly recommends across both. Also settles whether the ₹1.5–3.25L/lot figures are right.

**5.3 Does a residual-versus-error-bar signal survive out-of-sample on intraday NIFTY, once wing quotes are excluded per Klassen's criteria — and what data vendor gives him point-in-time chain, OI and timestamp semantics clean enough to test it?** This is the direct resolution of contradiction 3.1, it converts his existing SVI work into a falsifiable test rather than infrastructure, and it forces the data-provenance question (§1.8 of the gaps) that no agent asked.