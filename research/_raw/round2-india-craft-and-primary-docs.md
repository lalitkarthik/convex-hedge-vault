# Round Two — Indian Options Craft and the Primary Documents

---

## (A) PEOPLE AND CODE — the honest finding first

**Verdict: essentially nobody clears the bar for *Indian options* specifically.** I searched GitHub systematically (repository search across `nifty options backtest`, `banknifty`, `nifty implied volatility surface`, `options backtest STT slippage nse`, `dispersion trading implied correlation`, `kite zerodha options backtest`, `india options greeks volatility library`), read the actual cost code in every plausible candidate, and searched the blog/newsletter layer. What exists is three distinct populations, none of which is what you want:

1. **Broker-API wrappers and data libraries** (`nsepy`, `nsetools`, `nselib`, `bandl`, `fenix`, `py5paisa`, `ShoonyaApi-py`). Real, maintained, useful — but they are plumbing. No cost model, no backtest, nothing to assess.
2. **Live order-placement scripts for short straddles/strangles.** This is the bulk of it. `buzzsubash/algo_trading_strategies_india` is representative: `SL_SLIPPAGE_BUFFER = 5.0` is a limit-price padding constant for stop-loss orders, not a cost model. There is no backtester behind it at all.
3. **Recently-vibe-coded "platforms."** A large and growing cohort (`aaryansinha16/AI-trader`, `mimran-khan/deltaforge`, `Midas-09/STRATKIFS.01`, `aravindharajtr/master_intraday`, dozens more), most pushed in the last six months, near-zero stars, README claims far ahead of the code.

Searching `nifty implied volatility surface` on GitHub returns **375 repos of which none are a serious NIFTY vol-surface implementation** — the top hits are web-developer interview questions and arXiv scrapers. Searching `dispersion trading implied correlation` returns **zero** India-relevant repos. **For someone who has already implemented SVI/SSVI, there is no Indian open-source prior art to stand on. You are not behind the field; there is no field.**

What this implies practically: the Indian options-research public commons is a data commons, not a methods commons. Your comparative advantage against the domestic retail population is not the model — it is having a correct cost and settlement model at all, which as shown below almost nobody does. Treat US/European sources as the methods library and Indian sources as the data-and-rules library, and do not expect to find the two joined anywhere.

---

### AUDIT: `rajmaurya0904/bhav` — the "realistic Indian cost model" claim **does not hold**

- **URL:** https://github.com/rajmaurya0904/bhav (MIT, 26 stars, last commit 2026-07-19, v0.2)
- **Author:** Raj Kumar — LinkedIn lists him as Data Manager at NextGen Share Registry. No evidence he trades this.

I cloned it and read `bhav/engine/costs.py`, `bhav/engine/portfolio.py`, `bhav/engine/bar_engine.py`, and `bhav/data/underlyings.py`. Four defects, two of them disqualifying.

**1. The STT rate is the pre-October-2024 rate.** `IndianCostModel` hardcodes:
```python
stt_sell_rate: float = 0.000625     # docstring: "Numbers current as of 2025."
```
STT on the sale of an option rose from **0.0625% → 0.1% of premium with effect from 1 October 2024** (Finance (No. 2) Act 2024). The bundled sample dataset spans **Jul 2025 – Jun 2026** — entirely inside the post-change regime. For a short-premium strategy STT is the single largest cost line, and this understates it by 37.5% of its true value. Every net P&L the engine reports on its own shipped data is wrong in the favourable direction.

**2. The expiry/exercise path is dead code.** `costs()` takes an `exercised_itm` flag that applies the 0.125% exercise rate. I grepped the entire repository: **`exercised_itm=True` is never passed anywhere.** `BarEngine` has `square_off_time = "15:15"` and calls `ctx.close_all(reason="eod_square_off")` unconditionally. The engine is intraday-only and cannot model holding to expiry at all — so the single most-traded Indian structure (an expiry-day short straddle carried into settlement) is not backtestable, and the ITM-exercise STT that actually determines expiry-day P&L never fires. Separately, the flag is on the wrong side: STT on exercise is paid by the option **buyer**, but `costs()` only reaches the STT branch when `is_buy=False`.

**3. Lot sizes are a single static snapshot, and two of them are wrong against the circular the file itself cites.** `underlyings.py` says "Lot sizes reflect the NSE/BSE revisions effective from the January 2026 expiry cycle. Sources: NSE circular FAOP70616." I opened FAOP70616 (verified below). It sets NIFTY 75→65 ✓, MIDCPNIFTY 140→120 ✓ — but **BANKNIFTY 35→30 (bhav says 25) and FINNIFTY 65→60 (bhav says 65)**. Worse, the table has no time dimension: run the bundled Jul–Dec 2025 data and it will size NIFTY at 65 when the live lot was 75.

**4. Slippage is one tick, flat.** `fill_price()` moves the bar price by `slippage_ticks * 0.05` against you. Applied on every fill (this part is genuinely wired up, unlike the exercise path) — but ₹0.05 is 0.025% on a ₹200 ATM and 2.5% on a ₹2 wing. No spread model, no depth, no queue. Fills also occur at the close of the same bar the decision was made on, i.e. zero latency.

**Tests passed: 1 (runnable code) and 5 (reproducible) only.** Fails 2 (the cost model is stated but materially wrong), fails 3, fails 4. **Honest caveat:** the architecture is decent and the Upstox `expired-instruments` integration is the one genuinely valuable idea in it — historical expired option chains without a paid vendor. Fork it for the data layer, throw away `costs.py`, and never use the shipped sample results.

---

### The two Indian sources that *do* survive the filter

#### 1. Anirudh Vadrevu — "IMMR-H: The Signal Was Brilliant. The Costs Destroyed It."
- **URL:** https://anirudh-vadrevu.github.io/Quant-Journals/IMMR-Hybrid.html
- **What it concretely gives you:** the best-argued worked example I found of Indian transaction costs killing a statistically real signal. Monthly Spearman IC of 0.1758 (n=106, t≈12.4) — genuinely predictive — and a net return of **−7.15% p.a. with Sharpe −3.27** over 2015–2024, from 541 trades/year at ~0.35% round-trip. Cost stack modelled from first principles including **Almgren-Chriss market impact** and SSF borrow cost, not a flat bps assumption. The limitations section is unusually rigorous: he names survivorship bias as "the single most important methodological caveat," flags that his short leg ignores the **F&O ban list** (95%-of-MWPL rule), and flags that Yahoo data is not production-grade.
- **Tests passed:** 2 (costs explicit and decomposed), 3 (he built and ran it), **4 (names its own failure modes — counts double)**. That is a clear pass.
- **Honest caveat:** the backtest **code is not published** — the repo `anirudh-vadrevu/Quant-Journals` contains only the write-up. So it fails test 1. It is also cash equities, not options. Read it for the cost discipline, not for reuse.

#### 2. `DMZ22/vajra-quant`
- **URL:** https://github.com/DMZ22/vajra-quant (last commit 2026-07-25)
- **What it concretely gives you:** the only correctly-built Indian cost model I found in open source. `vajra/core/costs.py` gets delivery equity right — STT 0.1% on **both** sides, exchange 0.00297%, SEBI ₹10/crore, stamp 0.015% buy-only, DP charge ₹15.93 per scrip-sell, GST 18% on (brokerage+exchange+SEBI), 3 bps slippage — and, critically, **every rate lives in `config.yaml`, not in the source**, precisely so a regulatory rate change doesn't silently invalidate old runs. That is the design decision bhav got wrong. It also benchmarks against a **costed** buy-and-hold and publishes a results table in which three of its four strategies lose to it, and says so.
- **Tests passed:** 1, 2, 4 (double), 5.
- **Honest caveat:** **no options.** It trades NIFTY/index ETFs on free Yahoo EOD data. Take `core/costs.py` as your template and the delivery-vs-F&O rate distinction as your starting point; ignore the strategies.

#### Marginal / partial
- **`NagarajuGunda/PyAlgoMate`** (https://github.com/NagarajuGunda/PyAlgoMate, 137★) — `pyalgomate/core/slippage_tracker.py` does something nobody else does: it **records realised slippage in live trading** (market price at decision vs. actual fill price, per order type), to CSV. That is an empirical slippage distribution for Indian options rather than an assumption. There is no backtest cost model. Use it as an instrument, not a backtester.
- **Prof. Jayanth R. Varma** — blog https://jrvarma.wordpress.com/, papers https://www.jrvarma.in/fullist.html. He chaired the SEBI committee that designed India's derivatives risk-containment system and later sat on the RBI MPC; he writes about Indian derivatives structure in the first person and for free. Directly on-point for you: **Kumar, Agarwalla, Varma & Virmani, "Harvesting the volatility smile in a large emerging market: A Dynamic Nelson–Siegel approach," *Journal of Futures Markets* 43(11), 1615–1644 (2023)**, DOI 10.1002/fut.22450 — models the NSE smile as a term structure in **delta**, estimates it by Kalman filter in state-space form, sorts on model-implied mispricing, and trades long-top-decile / short-bottom-decile. This is the closest published thing to "SVI/SSVI, but for NSE, evaluated as a trade." **What I could not verify:** the paper is paywalled and I could not open the full text, so **I cannot confirm whether it nets transaction costs** — the abstract does not say, and given the strategy trades single-stock options monthly across deciles, that is the question that decides whether the result survives. Pull it via IIT KGP and check Section 5 first. Companion: Agarwalla's free Fama-French/momentum factor database for India at https://sites.google.com/iima.ac.in/prof-sobhesh-kumar-agarwalla/research-and-publications.

#### Explicitly rejected
The entire "I lost ₹X / I made 7.5% this month" Indian options-diary genre (theknowledgepulse, smartsourav, moneysavingsplans, the Medium day-journals) — anecdotal, no code, no reproducible method. Rejected. `raahibhushan.substack.com` is better written and genuinely first-person with real trade-level numbers, but it is discretionary firefighting narrative, not method. `hedgewithdatta.com` advertises "Sharpe 3.23, max drawdown −2.51% over a 5-year backtest" with no published code or cost model — auto-reject on the marketing rule. QuantInsti/EPAT project write-ups (including the dispersion one cited below) funnel to a paid programme — auto-reject as recommendations, though I use one factually below.

---

## (B) PRIMARY DOCUMENTS

### B1. SEBI's Oct-2024 derivatives rationalisation — **the structural break in your data**

**SEBI/HO/MRD/TPD-1/P/CIR/2024/132, 1 October 2024, "Measures to Strengthen Equity Index Derivatives Framework for Increased Investor Protection and Market Stability"**
https://www.sebi.gov.in/legal/circulars/oct-2024/measures-to-strengthen-equity-index-derivatives-framework-for-increased-investor-protection-and-market-stability_87208.html

I extracted the full 8-page text. The circular's own Applicability table (para 7):

| Measure | Effective from |
|---|---|
| Upfront collection of option premium from buyers | **1 Feb 2025** |
| Removal of calendar-spread treatment on expiry day | **1 Feb 2025** |
| Intraday monitoring of position limits | **1 Apr 2025** |
| Contract size for index derivatives (≥₹15 lakh) | **20 Nov 2024** |
| Rationalisation of weekly index derivatives products | **20 Nov 2024** |
| Increase in tail-risk coverage on options expiry day | **20 Nov 2024** |

Details that matter for a backtest:
- **§5.4.1** — "a derivative contract shall have a value not less than Rs. 15 lakhs at the time of its introduction… the lot size shall be fixed in such a manner that the contract value… is within Rs. 15 lakhs to Rs. 20 lakhs." Applies to **contracts introduced after 20 Nov 2024**, not to live contracts.
- **§5.5.2** — "each exchange may provide derivatives contracts for only **one** of its benchmark index with weekly expiry."
- **§5.6.1** — "an **additional ELM of 2%** for short options contracts," applying to all open shorts at start of day *and* shorts opened intraday that expire that day.
- **§5.2.2/5.2.3** — worst-scenario loss computed **separately** for same-day-expiring contracts; the illustration (29th/30th/31st) is explicit that a 30th–31st spread keeps its benefit on the 29th.

**Exactly which weeklies died, and when** — NSE circular **NSE/FAOP/64506** (10 Oct 2024), https://nsearchives.nseindia.com/content/circulars/FAOP64506.pdf. NSE retained weeklies **only on NIFTY**. Last weekly expiries: **BANKNIFTY 13 Nov 2024, MIDCPNIFTY 18 Nov 2024, FINNIFTY 19 Nov 2024**. On BSE: SENSEX50 14 Nov 2024, BANKEX 18 Nov 2024. If you backtest BANKNIFTY weeklies you are backtesting an instrument that no longer exists; the series does not merely thin out, it terminates on a known date.

**Also on 1 Oct 2024, unrelated to this circular but same day:** STT on option sale went **0.0625% → 0.1%** of premium and STT on futures sale **0.0125% → 0.02%**; NSE simultaneously cut its options transaction charge to **₹3,503 per crore (0.03503%)** of premium. Your cost function must be a function of date.

### B2. Expiry-day standardisation, Sept 2025

**SEBI/HO/MRD/MRD-TPD-1/P/CIR/2025/76, 26 May 2025, "Final Settlement Day (Expiry Day) for Equity Derivatives Contracts"**
https://www.sebi.gov.in/legal/circulars/may-2025/final-settlement-day-expiry-day-for-equity-derivatives-contracts_94189.html (PDF: `/sebi_data/attachdocs/may-2025/1748266377271.pdf`)

Verbatim, §3.1–3.3: expiries limited to **either Tuesday or Thursday**; one weekly benchmark index option per exchange on the chosen day; and — the part that is routinely missed — "**all other equity derivatives contracts, viz., all benchmark index futures contracts, non-benchmark index futures/options contracts, and all single stock futures/options contracts will be offered with a minimum tenor of 1 month**, and the expiry will be in the last week of every month." Single-stock options are now monthly-only, last Tuesday. Note the circular itself **names no day and no date** — those came from the exchanges.

The NSE implementation chain, which is where the backtest trap is:
- **NSE/FAOP/68589** (17 Jun 2025) — SEBI agreed to NSE's choice of **Tuesday**; Thursday retained for contracts expiring on or before **31 Aug 2025**; Tuesday from **1 Sept 2025**, monthlies on the **last Tuesday**.
- **NSE/FAOP/68685** (23 Jun 2025) — "The circular shall come into effect from **August 28, 2025 (EOD)** i.e. Expiry day for all existing contracts will be revised to 'New Expiry Day' on August 28, 2025 (EOD)."
- **NSE/FAOP/68747** (25 Jun 2025), https://nsearchives.nseindia.com/content/circulars/FAOP68747.pdf — long-dated NIFTY/BANKNIFTY options realigned to Tuesday on **31 Jul 2025 EOD**; new contracts with Tuesday expiry generated from **26 Jun 2025 EOD**.

**The trap:** the expiry dates of *already-live* contracts were **rewritten in the contract master on 28 Aug 2025 EOD**. If you rebuild your instrument universe by re-downloading contract masters today, contracts that traded for weeks under a Thursday expiry will present as Tuesday-expiry. Snapshot the contract master per date; do not reconstruct it.

BSE moved the opposite way — it had been on **Tuesday** and went to **Thursday** on the same date. Cross-exchange work spanning Sept 2025 crosses a swap, not a one-sided move.

### B3. Lot-size revisions — **NSE/FAOP/70616, 3 October 2025**
https://nsearchives.nseindia.com/content/circulars/FAOP70616.pdf (opened and read in full)

Issued under SEBI's periodic-revision mandate (SEBI/HO/MRD-PoD2/CIR/P/2024/00181, 30 Dec 2024):

| Index | Present lot | Revised lot |
|---|---|---|
| NIFTY | 75 | **65** |
| BANKNIFTY | 35 | **30** |
| FINNIFTY | 65 | **60** |
| MIDCPNIFTY | 140 | **120** |
| NIFTYNXT50 | 25 | unchanged |

Contract value computed on the **average closing index level for September 2025**. Effective **28 Oct 2025 (EOD)**; existing weekly/monthly contracts keep the old lot **until the 30 Dec 2025 expiry**; quarterly and half-yearly contracts revised on **30 Dec 2025 EOD**. Day-spread order books suppressed for the Nov'25–Jan'26, Dec'25–Jan'26 and Dec'25–Feb'26 combinations.

**Full NIFTY lot history you need:** 25 → **75** (contracts introduced from 20 Nov 2024, per NSE/FAOP/64625) → **65** (from 28 Oct 2025 EOD for new contracts; all contracts by 30 Dec 2025). Any P&L-per-lot series that crosses these dates without a date-keyed lot table is wrong by 3× and then by 13%.

### B4. The SEBI P&L studies — what they show, and the correction you need

**The 2024 headline document is only a 3-page press release**, not the study: PR 37/2024, 23 Sept 2024, https://www.sebi.gov.in/sebi_data/attachdocs/sep-2024/1727086965496.pdf. The actual study is *Analysis of Profits & Losses in the Equity Derivatives Segment (FY22–FY24)*.

Real methodology, read from the study text:
- **Section 1** — entire NSE F&O population, 95.7 lakh traders, FY24 only. P&L here is **squared-off gross P&L only** — *not* net of transaction costs, and **excludes open positions at end-FY24**.
- **Section 2** — **top 15 brokers** by individual F&O turnover in FY24 (~90% of individuals, ~75% of individual turnover), individuals + HUF + NRI, excluding prop/institutions/corporates/partnerships. FY22–FY24. **Realised** P&L only; physically-delivered contracts excluded; a contract with one leg outside the window is included only if the *closing* leg is inside.
- SEBI states in the document that Sections 1 and 2 "are not strictly comparable." The earlier Jan-2023 study used **top 10** brokers (~67% of FY22 individual turnover), so the 89% → 93% progression is partly a sample change.
- Aggregate: 1.13 crore unique individuals FY22–FY24; combined **gross** loss ₹1,31,903 cr, combined **net** loss ₹1,81,383 cr. 92.8% net loss-makers.

**What none of the P&L studies show — and the round-one claim that must be retracted.** The FY22–FY24 and FY25 studies report P&L by product category (index options / stock options / index futures / stock futures), demographics, turnover and geography. **They contain no buy/sell decomposition whatsoever.** They cannot tell you whether losses came from selling or buying volatility. Round one's inference that "a large share is naive short vol" was not supported by those documents.

**And SEBI has now published the document that settles it — 22 August 2026, one week ago.** Two new DEPA studies:

- **Profitability of Individual Traders in the Equity Derivatives Segment (FY25–FY26)** — https://www.sebi.gov.in/reports-and-statistics/research/aug-2026/study-profitability-of-individual-traders-in-the-equity-derivatives-segment-fy25-fy26-_103835.html
- **Trading Behaviour of Individual Traders in the Equity Derivatives Segment (FY25–FY26)** — https://www.sebi.gov.in/reports-and-statistics/research/aug-2026/study-trading-behaviour-of-individual-traders-in-the-equity-derivatives-segment-fy25-fy26-_103836.html (PDF: `/sebi_data/attachdocs/aug-2026/1787233601328.pdf`, 53 pp. — I read it)

The behaviour study classifies traders by strategy using **clearing-corporation MTM-settled value, traded value and margin data**, on a random sample of 5,050 individuals drawn from the 1.23 crore who traded in FY25–FY26. Result, FY26:

| Category | Share of traders | Loss-makers | Avg. loss per loss-making trader |
|---|---|---|---|
| Only Options Buyers | **93%** | 90% | ₹1.3 lakh |
| Majorly Options Buyers | 4.2% | 75% | ₹4.6 lakh |
| Majorly Options Sellers | **2.1%** | **44%** | **₹51.7 lakh** |
| Majorly Futures Traders | 0.9% | 61% | ₹1.7 lakh |

**The retail base is 97% option *buyers*, not sellers.** The sellers are the smallest group, have the *lowest* loss rate — and lose 11× more when they lose, and the category still net-lost ₹543 crore in FY26. SEBI's own framing: "relatively high win rates may mask a tail-risk profile." Also: **~59% of index-options turnover is 0DTE, ~75% within one day of expiry, ~97% within one week.**

**Honest caveat on this study, which SEBI states itself:** the strategy classification rests on n=5,050, of which **Majorly Options Sellers = 105 traders in FY26 and 109 in FY25**. The ₹51.7 lakh average is a 46-observation mean of a fat-tailed variable. SEBI repeats the small-sample warning three times. Treat the direction as solid and the magnitude as indicative.

The FY25 study (7 Jul 2025) used **top 13 brokers**, ~96 lakh unique traders, and found net losses widened 41% to ₹1,05,603 cr with 91% loss-makers — but note the quarterly path (₹21,255cr → ₹25,942cr → ₹33,661cr → ₹24,745cr) turns in Q4 FY25, the first full quarter after the 20 Nov 2024 measures.

### B5. Final settlement — **resolved, and it is neither of the two answers you had**

**NSE Clearing, Settlement Price (equity derivatives)**, updated 07/05/2024 — https://www.nseclearing.in/clearing-settlement/equity-derivatives/settlement-price. Verbatim:

> **Futures & Options Contracts on Index — Final Settlement:** "Final settlement price for a Index derivative contract shall be based on the **close price of the relevant underlying index** in the Exchange on the last trading day of such contract…"
>
> **Futures & options Contracts on Individual Securities — Final Settlement:** "…based on the **last 30 minutes volume weighted average price of the relevant underlying security** across Exchanges on the last trading day…"

So: **index options settle on the index CLOSE; single-stock derivatives settle on a 30-minute VWAP of the stock.** These are different rules, and the widely-repeated claim (e.g. optionx.trade) that NIFTY settles on "the VWAP of the Nifty index from 3:00–3:30" is **wrong**. The confusion arises because, historically, the index close was itself computed from constituent closing prices, and each constituent's close *was* its last-30-minute VWAP. A weighted sum of per-stock VWAPs is **not** the VWAP of the index series — they differ whenever constituent volume profiles differ over the window. If you were reconstructing settlement by VWAP-ing the index tick series, you have been computing the wrong number for every expiry.

**And that rule changed three weeks ago.** SEBI circular **SEBI/HO/47/11/11(3)2025-MRD-POD2/I/2765/2026, 16 January 2026** introduced a **Closing Auction Session**; NSE implemented via **NSE/CMTR/72394** (19 Jan 2026) and the SOP circular **NSE/CMTR/73362, 18 March 2026** (https://nsearchives.nseindia.com/content/circulars/CMTR73362.pdf — read in full). Live from **3 August 2026**:

- **CAS applies first to exactly the stocks that have derivatives** — i.e. the entire NIFTY/BANKNIFTY constituent set.
- §5.1.1: "For securities on which CAS is applicable, **closing price shall be determined based on the equilibrium price determination mechanism in CAS**." Fallback if no equilibrium price: the 3:00–3:15 VWAP (§2.1); then LTP; then previous close.
- CAS runs **3:15–3:35 p.m.** as a separate 20-minute call auction; **equity derivatives trade until 3:40 p.m.**
- Only limit and market orders; **no disclosed-quantity, no stop-loss orders**; algo market orders newly permitted in CAS.
- Cash-segment price band in CAS is **±3%** off the CAS reference price; stock-futures bands are re-flexed to ±3% from 3:15 to 3:40 and the "last half hour" for dynamic flexing is redefined as **2:45–3:15**. **Options price bands and LPP are explicitly unchanged** (§3.2.2.1).
- §6.5 — during the phased rollout NSE disseminates **both** an actual index value and an *indicative index close* value, because some constituents are in CAS while others are still in continuous trading.

**Net effect: from 3 August 2026 the NIFTY close — and therefore the final settlement value of every index option — is derived from single-print auction equilibrium prices of the constituents, not from any VWAP.** This is a live structural break in the middle of the data you are about to receive, it changes the microstructure of the last 25 minutes of every expiry day, and expiry-day strategies calibrated on pre-August-2026 data are calibrated on a mechanism that no longer exists.

### B6. Settlement / closing price for illiquid option series

From the NSE contract-specification pages (primary; identical text across NIFTY, BANKNIFTY, MIDCPNIFTY, NIFTYCPSE) — https://www.nseindia.com/static/products-services/equity-derivatives-nifty50:

- On **introduction** of a new option contract, base price = **Black-Scholes theoretical value** (formula given in full on the page).
- On subsequent days, base price = daily close of the option, where the close is:
  1. **traded in the last half hour** → last-half-hour **weighted average price**;
  2. **traded during the day but not in the last half hour** → **last traded price**;
  3. **not traded at all that day** → **Black-Scholes theoretical price**.
- For **unexpired illiquid futures**, daily settlement is theoretical: `F = S·e^{rt}` (NSE Clearing settlement-price page).

Consequence you must handle: a large fraction of your minute-wise chain will carry closes that are model outputs, not transactable prices. Rule 3 in particular manufactures a smooth, arbitrage-free-looking wing that no one could have traded. Any surface fit that uses EOD closes without filtering on `TtlNbOfTxsExctd > 0` is partly fitting NSE's own Black-Scholes output back to itself — which will make your SVI fits look far better in the wings than reality warrants.

### B7. Stock F&O eligibility and the churn

**SEBI/HO/MRD/MRD-PoD-2/P/CIR/2024/116, 30 August 2024, "Review of eligibility criteria for entry/exit of stocks in derivatives segment"** — https://www.sebi.gov.in/legal/circulars/aug-2024/review-of-eligibility-criteria-for-entry-exit-of-stocks-in-derivatives-segment_86373.html. Effective immediately; first revision since the Apr-2018 framework.

| Criterion (rolling 6 months) | Old | New |
|---|---|---|
| Median Quarter Sigma Order Size (MQSOS) | ₹25 lakh | **₹75 lakh** |
| Market Wide Position Limit (MWPL) | ₹500 cr | **₹1,500 cr** |
| Average Daily Delivery Value (ADDV) | ₹10 cr | **₹35 cr** |

Average daily market cap and ADTV (top-500 test) unchanged. **Exit:** fail any criterion for **3 consecutive months** → exit; no new contracts issued, existing unexpired contracts trade to expiry with new strikes still introduced; **no re-inclusion for one year**; 3-month gestation for incumbents, and exit rules only bite 6 months after introduction. A stock eligible on **any** exchange is eligible on **all**.

Layered on top is the **Product Success Framework** for single-stock derivatives: ≥15% of members active in stock derivatives (or 200, whichever is lower) must have traded it monthly; trading on ≥75% of days; **average daily turnover (futures + options premium) ≥ ₹75 cr**; **average daily notional OI ≥ ₹500 cr**.

**Why this makes any single-stock constituent set non-stationary:** membership is determined by a *rolling six-month* window on *cash-market* statistics and re-reviewed continuously, so entry and exit are endogenous to liquidity, one-year re-entry bans create hysteresis, and the thresholds themselves were tripled in one step in Aug 2024 (contemporary broker analysis identified ~23 names at immediate exit risk and 5 candidates for entry). Any study that takes today's ~210-name F&O list and runs it backwards has survivorship bias of exactly the kind Vadrevu flags: names get thrown out *because* their liquidity deteriorated. There is no free point-in-time constituent file; you have to build one by differencing the daily F&O bhavcopy universe, which you can do — see below.

---

## (C) DISPERSION IN INDIA — verdict with numbers

I computed this from the **actual NSE F&O bhavcopy for 27 August 2026** (`BhavCopy_NSE_FO_0_0_0_20260827_F_0000.csv.zip`, downloaded from `nsearchives.nseindia.com/content/fo/`), cross-referenced against the live NIFTY 50 constituent list (`nsearchives.nseindia.com/content/indices/ind_nifty50list.csv`).

**Universe (one trading day):**

| | Underlyings | Option series listed | Series with ≥1 trade | Notional turnover |
|---|---|---|---|---|
| Stock options | 210 | 23,741 | 7,893 (33%) | ₹3.25 lakh cr |
| Index options | 6 | 4,700 | 1,083 (23%) | **₹77.3 lakh cr** |

**Index options are 24× the whole single-stock option complex.** NIFTY alone: ₹74.9 lakh cr across 769 traded series.

**NIFTY 50 constituents specifically — the actual dispersion basket:**
- **All 50 have listed options.** So on a naive screen the trade looks feasible.
- Aggregate constituent option notional: **₹1.41 lakh cr** vs NIFTY index options **₹74.9 lakh cr** — a **53:1** ratio.
- Median per-constituent: **₹1,789 cr** notional, **46 traded strikes** (across all expiries).
- **11 of 50 are below ₹1,000 cr/day.** The weakest: MAXHEALTH ₹214 cr (36 traded strikes), NESTLEIND ₹270 cr, GRASIM ₹568 cr, TATACONSUM ₹611 cr, BAJAJFINSV ₹797 cr, CIPLA ₹868 cr, TRENT ₹919 cr (only **29** traded strikes), WIPRO ₹929 cr, HCLTECH ₹960 cr, POWERGRID ₹995 cr, SBILIFE ₹995 cr.
- Concentration across all 210 F&O names: top 10 = 26.5%, top 20 = 40.1%, top 50 = 65.7% of stock-option notional.

**Verdict: dispersion on NIFTY is not viable for you, but the binding constraints are structural, not liquidity.** Liquidity is the *least* of the four problems:

1. **Single-stock options are physically settled — decisively.** SEBI/HO/MRD/DOPI/CIR/P/2018/161 (31 Dec 2018) made physical settlement mandatory for all stock derivatives, fully phased in by the **October 2019** expiry. Index options are cash-settled; stock options are not. A long-constituent-options leg held into expiry generates a delivery obligation of **full notional** on every ITM leg. Delivery margins ramp from **E-4** (typically 10% → 25% → 45% of VaR+ELM+Adhoc, then 25% of *contract value* at E-1, then 50% on expiry day for long ITM), and brokers additionally block **25% of contract value on expiry day for OTM strikes within 1% of spot** because they may turn ITM. Across 50 legs this is not a margin inconvenience; it is a different business. Held-to-expiry dispersion in India requires being set up for delivery on 50 names simultaneously.

2. **The expiry calendar no longer lines up.** Since 1 Sept 2025 (SEBI 2025/76 §3.3) single-stock options are **monthly only, last Tuesday**. NIFTY has weeklies. So the natural weekly dispersion trade has no stock leg at all, and the monthly trade puts your entire short-index leg into the one expiry where the +2% expiry-day ELM and the removed calendar-spread benefit both bite.

3. **Margin is computed leg-by-leg with no correlation offset across underlyings.** SPAN scans each underlying's portfolio independently; there is no cross-margin between NIFTY options and its constituents' options. You post margin as if you held 51 unrelated books. The whole economic point of dispersion — that the basket is nearly hedged — earns you nothing in margin.

4. **Eligibility churn is real but secondary.** The Aug-2024 tripling of MQSOS/MWPL/ADDV plus the PSF thresholds (₹75 cr daily turnover, ₹500 cr notional OI) mean names enter and leave; with a one-year re-entry ban, a constituent that drops out is gone for four quarters. It doesn't kill the trade — the NIFTY 50 are all comfortably above the thresholds — but it kills the *backtest*, because your historical constituent×eligibility intersection is not what a live desk faced.

**Where the ratio is actually attractive:** Jain, Varma & Agarwalla (JFM 2019) found the risk premium embedded in Indian **single-stock** option IV is *higher* than in other markets and higher than theory suggests, which is the wrong sign for classic dispersion (you want to *buy* cheap constituent vol). Varma's own summary: "the implied volatility of Indian single stock options consistently exceeds realized volatility by too large an amount to be easily explained as a rational risk premium." If anything the Indian data argues for **reverse dispersion** — short constituent vol, long index vol — which is exactly the leg that physical settlement punishes hardest.

The only public Indian dispersion write-up I found is a QuantInsti EPAT project (blog.quantinsti.com/dispersion-trading-on-nse-stocks, 2017) on BANKNIFTY vs its bank constituents, 15-minute data, delta-hedged with futures. It concludes "very profitable low risk hedged strategy." It has **no cost model, no margin treatment, no physical-settlement handling**, and it funnels to a paid programme. Auto-reject; I cite it only to establish that this is the state of the published art.

**If you still want the correlation exposure:** BANKNIFTY vs. its 12 constituents is the one place where the basket is small enough and every name is top-decile liquid (HDFCBANK ₹18,668 cr, ICICIBANK ₹8,437 cr, KOTAKBANK ₹8,868 cr, SBIN ₹4,790 cr, AXISBANK ₹4,387 cr). But BANKNIFTY lost its weeklies on 13 Nov 2024, so both legs are now monthly-only — which at least makes the calendars match, at the cost of one observation per month.

---

## PAID — worth considering later

- **Kumar, Agarwalla, Varma & Virmani (2023), "Harvesting the volatility smile in a large emerging market: A Dynamic Nelson–Siegel approach," *JFM* 43(11) 1615–1644**, DOI 10.1002/fut.22450. Paywalled (Wiley); **free via IIT KGP**. The only published work that takes a smile parameterisation on NSE data all the way to a sorted trading portfolio. Verify the cost treatment before trusting the Sharpe.
- **Jain, Varma & Agarwalla (2019), "Indian equity options: Smile, risk premiums, and efficiency," *JFM* 39(2) 150–163**, DOI 10.1002/fut.21971. Paywalled; free via KGP. Establishes the single-stock IV-over-RV premium that governs the dispersion sign. Free précis by Varma at https://jrvarma.wordpress.com/2018/11/02/indian-single-stock-option-pricing/.

---

## What I could not verify

- **The full text of the DNS "Harvesting the volatility smile" paper** — paywalled at Wiley; no free preprint found on iima.ac.in or jrvarma.in. I therefore cannot say whether its trading results are net of costs. This is the single most important open question in this report for you.
- **NSE consolidated F&O circular NSE/FAOP/67775 (30 Apr 2025), clause 1.4** — the canonical F&O closing-price mechanism the CAS SOP cross-references. `nsearchives.nseindia.com` and `archives.nseindia.com` both return an HTML error page for this ref regardless of headers. I substituted the **NSE contract-specification pages**, which state the same three-branch rule verbatim and are equally primary; but I have not read clause 1.4 itself and note the substitution rather than passing it off.
- **Whether the Nov-2024 +2% expiry-day ELM has since been modified** by any of the 2025–26 risk circulars (in particular the 29 May 2025 delta-based/Future-Equivalent OI circular). I confirmed it took effect 20 Nov 2024; I did not trace it forward and you should before using it in margin simulation.
- **Whether the ~₹51.7 lakh average loss for "Majorly Options Sellers"** is robust — it rests on 46 loss-making traders out of a 105-trader FY26 cell. SEBI flags this itself; I am repeating the flag rather than resolving it.