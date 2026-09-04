# Income Paths and Honest Base Rates — Factual Report

Scope note: this reports what is documented. It contains no recommendations, allocations, or trade suggestions. Where I could not verify a number, I say so rather than filling the gap.

---

## 0. The two facts that reorder everything else

**(i) As an Indian resident, US options are largely closed to you.** RBI's Liberalised Remittance Scheme permits USD 250,000/year outward, but remittance for *margin trading, futures and options, and leveraged products abroad* is explicitly prohibited. LRS money can buy US **equities and ETFs**; it cannot fund a US options account. Zerodha's own Varsity note on this is the least-conflicted public write-up. Anything you read about US retail options economics is therefore **technique transfer, not a venue** — which matches your brief's weighting instruction, but the constraint is legal, not stylistic. (I did not verify whether the GIFT City/IFSC route materially changes this for resident individuals; the overseas-derivatives prohibition appears to survive, but treat that as unverified.)

**(ii) Deribit — the dominant crypto options venue — is not FIU-IND registered.** In October 2025 FIU-IND ordered blocking of 25 offshore crypto platforms for PMLA non-registration (BitMEX, BTSE, CEX.IO, HitBTC among them); ~49–50 platforms are registered. Deribit is not on the registered list. So "crypto vol" as an individual path from India runs through domestically registered venues (Delta Exchange India offers INR-settled BTC/ETH options — *I did not verify its current FIU status or its options book depth; check both before modelling anything*), not through the venue where the liquidity actually is.

Together these mean: of your four candidate strategy classes, **two are venue-constrained before you get to a single line of maths.**

---

## (A) Capital vs strategy viability, with real numbers

### A1. Indian index options selling — the arithmetic of the fixed-cost floor

Cost stack per order/leg (NSE index options, rates effective 1 Oct 2024):

| Component | Rate |
|---|---|
| STT (sell side, on premium) | 0.10% |
| NSE txn charge (both sides, on premium) | 0.03503% |
| Stamp duty (buy side) | 0.003% |
| SEBI turnover fee | ₹10 / crore |
| Brokerage | ~₹20 per order, flat (discount brokers) |
| GST | 18% on (brokerage + txn + SEBI fee) |

**Worked round trip, 1 lot NIFTY (lot = 75), sell @ ₹100, buy back @ ₹40:**

- STT ₹7.50 · txn ₹3.68 · stamp ₹0.09 · SEBI ₹0.01 · brokerage ₹40 · GST ₹7.86 → **≈ ₹59**
- Gross P&L ₹4,500 → costs = **1.3% of gross**. Not the problem.

**Same size, 4-leg iron condor (8 orders):**

- Brokerage + GST alone ≈ ₹189. Total ≈ **₹210** against a max profit of ~₹3,000. That is **7% of max profit**, and if you exit at 30% of max (the standard management rule), costs are **~23% of the realised target**.

**The floor is the flat per-order fee, not the ad-valorem charges.** Brokerage is per *order*, not per lot, so it dilutes ~10× going from 1 lot to 10 lots. Multi-leg structures become fee-viable at roughly **10 lots**, which for a defined-risk Nifty condor (200-point wings) means ~₹1.2L margin, so **~₹1.5–2L is the hard floor for defined-risk multi-leg selling**.

**Undefined-risk selling has a much higher floor** driven by margin, not fees: a NIFTY short strangle runs roughly **₹1.5–2L SPAN+exposure per lot**, a 0DTE short straddle ~₹3–3.25L per lot (broker/practitioner figures; margins are volatility-dependent and change daily — verify on a live margin calculator). Add SEBI's requirement that **50% of margin be cash or cash-equivalent**, so a ₹20L "account" running strangles is not ₹20L of deployable margin.

**Scaling arithmetic (no return assumption implied — this is just division):** at a net 1%/month on deployed margin you need ~₹1 crore of margin to gross ₹1L/month; at 2%/month, ~₹50L. Then F&O profit is **business income at slab** — top marginal 30% + surcharge + 4% cess. There is no configuration of this arithmetic in which a sub-₹25L account produces income competitive with a finance salary inside two years.

**Regulatory headwind, stated bluntly:** SEBI's Nov 2024 package — lot size increased to ₹15L+ notional (NIFTY 75), weekly expiries cut to one benchmark index per exchange, STT on options raised from 0.0625% to 0.10% — was *designed* to raise the cost floor for exactly this activity. Zerodha reported a ~40% YoY hit to brokerage revenue in the following June quarter. The regulator is an active adversary of the small-account version of this strategy.

### A2. US options
Not a viable venue for you as a resident (see §0). For completeness on the *technique-source* side: FINRA has **abolished** the $25,000 pattern-day-trader minimum. SR-FINRA-2025-017 was approved; the PDT designation and $25k floor are replaced by real-time intraday margin excess, **effective 4 June 2026**, with phase-in permitted to 20 Oct 2027. Baseline margin minimum reverts to **$2,000** (Reg T). Portfolio margin thresholds (nominally $125k under FINRA 4210(g), lower at some brokers) — **I did not verify current levels.** Note this change makes US retail options *cheaper to access for Americans* while you remain excluded — the crowding on US-origin techniques will increase.

### A3. Crypto funding carry (cash-and-carry / perp basis)
Mechanically the lowest-capital-floor strategy on the list: no lot size, no minimum notional, fractional sizing. The floor is set by **exchange fees, transfer/withdrawal costs, and margin buffer to survive funding-rate reversals and basis widening**, not by a contract size.

Reported returns require heavy discounting. The double-digit "delta-neutral APY" figures in circulation come overwhelmingly from arbitrage-tool marketing sites and fail your source filter outright. The defensible statements:
- Funding is paid every 8h and is **regime-dependent, not a yield**: strongly positive in bull phases, near zero or negative in drawdowns. Glassnode publishes a `btc futures annualized yield` workbench metric — that is the honest reference series and it is free to inspect.
- The mechanism (long spot, short perp) is real and the drawdown profile is genuinely small **until it isn't** — the failure modes are exchange/counterparty risk, forced liquidation of the short leg on a wick, funding sign flip, and stablecoin depeg. Institutional carry desks lost money on all four in 2022.
- One peer-reviewed source exists: *The Two-Tiered Structure of Cryptocurrency Funding Rate Markets*, Mathematics (MDPI) 2026, 14(2):346 — it documents structure, not a tradeable P&L.

**Then India's tax code eats it.** See §C3 — for an Indian resident, the after-tax carry can be *negative while the gross carry is positive*. This is the single most under-appreciated fact in this whole report.

### A4. Crypto vol (options)
Highest infrastructure requirement, lowest legal accessibility from India. Deribit's own VIP tiering starts around $100k USDC equity / $250k total equity, and market-maker treatment requires a negotiated agreement with quoting-time, spread, and size obligations. That is the *entry* to being treated as a serious participant — and it is not available to you as a resident. Domestic venue options books are thin enough that surface-fitting work (your SVI/SSVI comparative advantage) has little to bite on.

---

## (B) Honest base rates

### B1. SEBI — three studies, not one

**Jan 2023 (FY22):** ~89% of individual traders in equity F&O made losses; average loss ~₹1.1 lakh. Sample: individual clients of the **top 10 brokers** by active clients (~45 lakh individuals), FY19 vs FY22 comparison.

**Sep 2024 (FY22–FY24), Press Release 37/2024:** **1.13 crore unique individual traders**, aggregate net loss **₹1.81 lakh crore** inclusive of transaction costs over three years.
- 92.8% (>1 crore people) lost, averaging ~₹2 lakh each over three years.
- Top 3.5% of loss-makers (~4 lakh people) averaged **₹28 lakh** loss each.
- 7.2% profited; **only 1% of all traders earned more than ₹1 lakh net of costs over three years.**
- Loss-makers spent an *additional* ~27% of their losses on transaction costs. (I have seen a component split of that cost total — brokerage vs exchange vs STT — but **could not verify the percentages**; the PDF is image-based and did not extract. Do not quote a split.)

**Jul 2025 (FY25):** **91%** loss rate, essentially unchanged from FY24. Net losses **grew 41% to ₹1.05–1.06 lakh crore**. Sample: top **13** brokers, ~96 lakh unique F&O clients. Unique individual traders fell **61.4 lakh (Q1FY25) → 42.7 lakh (Q4FY25)**, a ~30% decline attributed to the Nov 2024 measures.

**Read the FY25 pair together, because it is the most informative fact in the set:** participation fell ~30% while aggregate losses rose 41%. The population shrank and the survivors lost *more*. That is not consistent with a story where regulation weeded out the unskilled and left a profitable core.

**What these studies do NOT show — be strict about this:**
1. **No conditioning on skill, capital, or strategy.** A ₹5,000 0DTE lottery-ticket buyer and a ₹50L systematic seller are one pooled statistic. The studies do not report P&L by account size or by strategy type.
2. **No persistence test.** They do not establish whether the 7.2% profitable cohort is skilled or lucky — there is no year-over-year re-ranking. This is precisely the question SEBI does not answer and Barber et al. do (B3).
3. **No hedger control.** Clients hedging cash portfolios book F&O losses offset elsewhere. SEBI acknowledges non-speculative participants exist but does not strip them out.
4. **Client-broker window, not lifetime.** P&L is measured per client at sampled brokers over a fixed window. Multi-broker traders and cohort entry/exit timing are not tracked as a hazard curve.
5. **Pre-tax, and no capital base.** Losses are stated in rupees, not as return on capital deployed. You cannot derive a Sharpe or even a percentage return from these numbers.
6. **Brokers are not randomly sampled.** Top-10/top-13 by active-client count skews toward discount brokers, i.e. toward exactly the small speculative account.

None of these caveats make the picture good. They make it *imprecise in a way that does not obviously favour you.*

### B2. Brazil — Chague, De-Losso & Giovannetti, *Day Trading for a Living?* (SSRN 3423101, rev. Jun 2020)
CVM records on **19,646 individuals** who began day trading **mini-Ibovespa index futures** 2013–2015, followed through 2017.
- **97% of those who persisted more than 300 days lost money.**
- **1.1%** earned more than the Brazilian minimum wage; **0.5%** more than a bank teller's starting salary — and those with high risk.
- **No evidence of learning by doing.**

**What it does not show:** single instrument, single style (leveraged intraday index futures), retail cohort with no stated prior training. It says nothing about multi-day holding periods, defined-risk structures, or people entering with institutional-grade quantitative preparation. The "no learning" result is the part that generalises least comfortably and is also the part most worth sitting with — it is the direct empirical rebuttal to "I'll be profitable once I've done my two years."

### B3. Taiwan — Barber, Lee, Liu & Odean, *The Cross-Section of Speculator Skill* (JFM 2014)
Full-population day-trader data, Taiwan, 1992–2006. The only study here with a proper **persistence** design.
- **Less than 1% of day traders predictably and reliably earn positive abnormal returns net of fees.**
- Predictably profitable traders were **<3%** of day traders and generated only ~9.8% of day-trading volume.
- Sorting on year *y* returns: top-500 traders go on to earn **+37.9 bps/day after fees** in year *y+1*; bottom-ranked **−28.9 bps/day after fees**.

**This is the most useful number in the report for you.** It says skill is real, persistent, and detectable — and concentrated in a sub-1% tail. It also says the persistent winners are *identifiable in advance from track record*, which means the honest test is empirical and self-administered: does your own live, cost-inclusive record show persistence? Nothing else answers it.

### B4. Prop firms
Best available dataset: **FPFX Technologies**, ~300,000+ accounts across ~100,000 traders at 10 firms —
- **~14% pass an evaluation.**
- **~45% of funded traders ever receive a payout.**
- **⇒ ~7% of everyone who buys a challenge ever sees money back.**
- Long-term funded, withdrawing beyond six months: **1–3%** of participants.

FTMO **publishes no official pass rate**; the 9–12% figures in circulation are third-party estimates, mostly from affiliate-monetised comparison sites. Treat every prop-firm statistics page as marketing until proven otherwise.

Structural caveats that matter more than the percentages: most of these are **simulated/CFD accounts**, the **challenge fee is the revenue model** (which aligns the firm against your passing), the CFTC's 2023 action against My Forex Funds showed the sector's regulatory fragility, and the model is **forex/futures, not options** — it does not test the skill you actually have.

### B5. Longitudinal data on semi-professional derivatives traders
**This does not exist in usable public form, and you should know that.** Barber et al. (Taiwan) and Chague et al. (Brazil) are the closest, and both study *retail day traders*, not capitalised systematic traders with quant training. There is no published longitudinal study of the specific population you belong to. Anyone who tells you the base rate for "quant with a day job trading own capital systematically" is extrapolating. So am I, if I did. I won't.

---

## (C) Cost structures and required gross edge

### C1. Indian F&O — taxation
- **Non-speculative business income**, taxed at **slab** (top marginal 30% + surcharge up to 25% + 4% cess). Not capital gains.
- **Business expenses are deductible** — brokerage, data, software, internet, depreciation on hardware. This is a genuine structural advantage over the crypto regime.
- **Losses**: non-speculative business loss sets off against other heads (not salary) in-year, carries forward 8 years against business income.
- **Tax audit (s.44AB)**: required above **₹10 crore** turnover for fully-digital traders (₹1cr threshold applies only if cash receipts/payments exceed 5%). F&O turnover is computed on absolute-profit-plus-premium conventions, not notional — but it inflates fast with trade count.
- **Trap**: if you have opted into **s.44AD** presumptive taxation in an earlier year and later declare below 6% of turnover or a loss, with total income above the exemption limit, **audit becomes mandatory even at tiny turnover**. Salary income guarantees you're above the exemption limit. Do not touch 44AD.

**Required gross edge, Indian index options selling:** friction ≈ 0.19% of premium turnover per round trip (ad-valorem) **plus ~₹47 per order in brokerage+GST**. Then multiply the surviving profit by ~1/0.69 for slab tax. A strategy grossing 15%/yr on margin nets roughly 10%/yr post-tax before fixed-fee drag, and the fixed-fee drag is what determines whether a small account gets there at all.

### C2. STT cliff (mechanism, worth knowing precisely)
STT on **exercised in-the-money long options** is charged on the **settlement (intrinsic) value**, not premium — an order-of-magnitude different base from the 0.10% premium charge on sales. This is the classic mechanism by which expiry-day long positions destroy accounts that thought they were profitable. It bites buyers, not sellers, but it distorts expiry-day price behaviour that any seller must model. **Verify the current rate and base with your broker's contract note — I did not verify the exact percentage in this pass.**

### C3. Crypto — the tax structure is the strategy constraint
- **s.115BBH: flat 30% + surcharge + 4% cess** on VDA transfer gains. Unchanged by Finance Act 2025.
- **No deduction except cost of acquisition.** Gas fees, exchange fees, data, infrastructure — all non-deductible.
- **No loss set-off.** Not against other VDAs, not against any other head, **no carry-forward**.
- **s.194S: 1% TDS** on transfer consideration above ₹50,000/yr (specified persons) or ₹10,000 (others). Creditable against final liability — but deducted on **turnover**.

**Why this specifically kills delta-neutral carry:** a cash-and-carry position is long spot and short perp. If both legs are treated under 115BBH with no offset, you are taxed at 30% on the leg that gains while the leg that loses is **not deductible**. On a ₹10L delta-neutral position where spot rises 20%, you owe ~30% on ₹2L (₹60k+) while your ₹2L perp loss is worthless to you. The gross carry — say ₹80k/yr — is gone. **The classification of perp/derivative P&L under 115BBH vs. business income is genuinely unsettled**, and the answer determines whether the strategy is viable at all for a resident. This is a question for a chartered accountant, not for me and not for a backtest.

**Why 1% TDS kills turnover:** a strategy rolling monthly touches ~12× notional per year → **12% of notional deducted and locked up** until refund. A daily-turnover strategy deducts multiples of the account. The Esya Centre (Nov 2023) documented the consequence empirically: **>₹3.5 lakh crore** of Indian VDA volume moved offshore Jul 2022–Oct 2023, offshore venues capturing **>90%** of Indian trading, domestic exchanges losing **81% of volume in four months**; 3–5 million users migrated. Methodology: 13,000 P2P traders, web-traffic analysis of 20 offshore exchanges, exchange-executive surveys — decent primary work, but web-traffic-derived volume estimates carry wide error bars. Note the migration route it documents is now substantially closed by the FIU-IND blocking (§0).

### C4. US
Post-June-2026 the $25k PDT floor is gone; $2,000 Reg-T minimum. Commission-free equity options at most US brokers (per-contract fees ~$0.65 or zero), plus regulatory fees. **Irrelevant to you as a venue**; relevant because it means US retail cost structures are *not* transferable as a viability assumption to Indian ones. Indian frictions are roughly an order of magnitude higher per unit of premium.

---

## (D) Solo vs firm — bluntly, per skill

| Skill | Monetises solo? | The honest reason |
|---|---|---|
| **Vol surface modelling (SVI/SSVI)** | **No, not directly.** | It is an *input*, not a strategy. At a firm it is table stakes — every options desk has a calibrated surface; nobody is paid for having one. Its two solo monetisation routes are (a) intra-surface relative value, which requires quoting infrastructure and spreads you cannot access, and (b) generating a rich/cheap signal for positions you take directionally — which collapses back into premium selling. You have already built the thing; the thing is not the edge. The edge would be the data pipeline and execution, which you do not have and which a firm does. |
| **Regime detection** | **Yes** — the only clean solo-scalable item. | Needs no infrastructure, no latency, no venue relationship. Works as a position-sizing/on-off overlay on strategies you already run. Blunt counterweight: this is also the area with the **weakest out-of-sample evidence base** in all of quant finance. Published regime models (HMM, changepoint, clustering-on-vol) are overwhelmingly overfit, and regime labels are only unambiguous in hindsight. Treat every published regime result as fragile until you have reproduced it with a walk-forward and a cost model. |
| **Market making** | **No. Institution only.** | Requires exchange membership or a negotiated MM agreement, quoting-obligation compliance (min % time quoted, max spread, min size), colocation, sub-millisecond stack, rebate-tier economics, and inventory capital. Deribit's MM programme is a negotiated agreement; NSE's schemes are for registered trading members. There is no retail version of this. Every "retail market making" claim you encounter is either wide-spread scalping or marketing. |
| **Stat arb** | **Partially, and worse than it looks.** | Cross-sectional Indian equity stat arb is largely closed to individuals: **cash-market shorting is intraday-only** and the SLB market is thin, so you cannot hold the short leg. Crypto cross-exchange/cross-venue stat arb is genuinely retail-accessible but is capital- and infrastructure-hungry, margins have compressed severely since 2021, and India's TDS + no-offset regime taxes the gross legs of a spread independently (see C3). |
| **Options premium selling** | **Yes — fully accessible.** | Which is exactly why it is crowded, and exactly what the SEBI numbers are measuring. It is the one item on this list an individual with margin can run at institutional-identical mechanics. The risk is not mean edge — it is **skew**. Short-vol P&L is negatively skewed with a fat left tail; a single gap (Indian election day, 4 Jun 2024: Nifty ~−6% intraday) can exceed multiple years of carry. Nothing about SVI competence protects against this; the exposure is to the jump, not to the surface. |

Summary in one line: **the skill you have invested most in (surface modelling) is the least solo-monetisable; the one that is fully solo-monetisable (premium selling) is the most crowded and the most tail-exposed.** That is an uncomfortable fact and it is the fact.

---

## (E) Quant-adjacent income that is not a software job

**Numerai — real money, brutal distribution. Not income.**
Cumulative payouts >$43M; $1.3M in NMR distributed for the 2024 season. But of **14,378 models** submitting in the trailing year, only **2,641 finished net-positive**. Median positive earner: **~0.1 NMR ≈ $1**. 90th percentile: **~26 NMR ≈ $235**. 99th percentile: **~1,001 NMR ≈ $9,000+**. And you must **stake NMR** — your own capital, in a volatile token, at risk of burn. Verdict: **a hobby with a lottery tail**, correctly classified alongside the trading base rates rather than alongside income.

**Kaggle-hosted quant competitions (Jane Street, Optiver, Two Sigma) — recruiting funnel, not income.** Prize pools typically $100k–$120k split among the top ~5 of several thousand teams. The realistic return is a credential and a recruiter conversation. Given you are excluding a job, the credential is the only product, and it has zero cash value to you. *(I did not verify current live competitions or prize levels in this pass.)*

**Systematic-strategy licensing — the flagship attempt failed.**
**QuantConnect Alpha Streams**, the most serious retail alpha-licensing marketplace ever built, was **wound down** — sales disabled, renewals disabled, live alpha hosts stopped, existing licensees refunded or rehomed, wallet balances paid out. The reason is the one that matters: **there were not enough buyers.** Institutions do not license black-box alphas from anonymous individuals.

What remains:
- **Darwinex**: 20% performance fee on third-party profit, of which **15% to the strategy provider**, 5% to Darwinex, paid quarterly on a high-water mark. Real, and structurally sound. Binding constraint is **attracting third-party AUM**, which is a distribution and track-record problem, not a quant problem.
- **Collective2**: subscription-revenue share — **50% baseline, 60% with Trades-Own-Strategy certification, 75% with C2Star**. Highest-grossing strategy lifetime **>$500k**; a few approaching $100k. Those are the extreme right tail of a platform hosting thousands of strategies over many years.

Verdict on licensing: **it pays a handful of people, and the gate is a 2–3 year live, audited, cost-inclusive track record before anyone subscribes.** That gate consumes your entire stated horizon before the first rupee. It is not a two-year path; it is a path that *begins* at year two.

**Paid research writing — real but small, and brand-gated.** The people earning meaningful money writing quant research publicly almost universally arrived with an institutional brand first. Writing does not bootstrap the brand quickly enough to matter on a two-year clock. *(No verified income distribution data exists for this; I am reporting the absence.)*

**Data products — a genuine gap, and one you are structurally blocked from filling.** Indian minute-level index options data is expensive, poorly served, and there is real demand for cleaned IV surfaces on NIFTY/Sensex. But: (a) redistributing exchange-derived data requires an **NSE-authorised data vendor licence**, and (b) the minute-wise data you are about to receive comes through an employer relationship — **you cannot resell what you get at work**, and attempting to would be the fastest possible way to end both the job and the path. This one is closed for reasons that have nothing to do with skill.

**Consulting** — pays genuine rates, but it is freelancing under a different name, which your brief excludes.

**Aggregate honest read on (E): none of these produce income on a two-year horizon.** The licensing routes are real but their gating requirement *is* the two years. Numerai and competitions are hobbies with tails. The one item with genuine market demand (data products) is the one your employment situation forecloses.

---

## The arithmetic nobody states plainly

At your stage the binding constraint is **capital, not skill**. A ₹25 lakh account returning a genuinely excellent, sustained **20% net** produces ₹5L gross, **~₹3.5L after slab tax** — a fraction of a finance salary, from a strategy performing at a level that Barber et al. place in the sub-1% persistent tail. To make the income question interesting rather than academic, the account has to be an order of magnitude larger, and the salary is the only documented mechanism that gets it there inside two years. That is division, not advice.

---

*Personal-account-dealing policies vary substantially between employers — pre-clearance requirements, holding periods, restricted instrument lists, and outright bans on trading instruments the firm covers — and should be checked against the specific contract you sign before any of the above is actionable.*

---

## Sources

- [SEBI Press Release 37/2024 — 93% of individual traders incurred losses FY22–FY24](https://www.sebi.gov.in/media-and-notifications/press-releases/sep-2024/updated-sebi-study-reveals-93-of-individual-traders-incurred-losses-in-equity-fando-between-fy22-and-fy24-aggregate-losses-exceed-1-8-lakh-crores-over-three-years_86906.html)
- [Business Standard — Net losses of individual F&O traders widened in FY25 (SEBI study)](https://www.business-standard.com/markets/news/net-losses-of-traders-in-fo-widens-in-fy25-sebi-study-125070701221_1.html)
- [Business Standard — SEBI study, 89% retail F&O losses FY22 (Jan 2023)](https://www.business-standard.com/article/markets/sebi-study-suggests-89-retail-traders-in-equity-f-o-suffered-losses-123012501466_1.html)
- [Business Standard — Individual investors in F&O shrink 20% post-SEBI intervention](https://www.business-standard.com/markets/news/individual-investors-shrink-20-percent-fo-segment-125070800801_1.html)
- [CFA Institute — India's Derivatives Market and Retail Investors](https://blogs.cfainstitute.org/marketintegrity/2025/11/05/indias-derivatives-market-and-retail-investors/)
- [Chague, De-Losso, Giovannetti — *Day Trading for a Living?* (SSRN 3423101)](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3423101)
- [Barber, Lee, Liu, Odean — *The Cross-Section of Speculator Skill* (full PDF, Haas)](https://faculty.haas.berkeley.edu/odean/papers/day%20traders/The%20Cross-Section%20of%20Speculator%20Skill.pdf)
- [Barber et al. — *Do Day Traders Rationally Learn About Their Ability?*](https://faculty.haas.berkeley.edu/odean/papers/Day%20Traders/Day%20Trading%20and%20Learning%20110217.pdf)
- [The Prop Firm Guide — prop firm statistics (FPFX dataset)](https://thepropfirmguide.com/prop-firm-statistics/)
- [Zerodha Z-Connect — Revision in exchange transaction charges and STT from 1 Oct 2024](https://zerodha.com/z-connect/business-updates/revision-in-exchange-transaction-charges-and-securities-transaction-tax-from-october-1-2024)
- [Zerodha — full charges list](https://zerodha.com/charges/)
- [NSE Clearing — Securities Transaction Tax, equity derivatives](https://www.nseclearing.in/clearing-settlement/equity-derivatives/securities-transaction-tax)
- [Zerodha Varsity — Can Indians trade in US F&O?](https://zerodha.com/z-connect/varsity/can-indians-trade-in-the-us-fo)
- [FINRA Regulatory Notice 26-10 — replacement of day-trading margin requirements](https://www.finra.org/rules-guidance/notices/26-10)
- [SEC — SR-FINRA-2025-017 approval order](https://www.sec.gov/files/rules/sro/finra/2026/34-105226.pdf)
- [Schwab — SEC approves scrapping the $25,000 day trader minimum](https://www.schwab.com/learn/story/sec-approves-scrapping-25000-day-trader-minimum)
- [Cryptact — VDA income tax India 2025 (s.115BBH, s.194S)](https://www.cryptact.com/en/blog/vda-income-tax-india-2025-complete-guide-to-crypto-tax-rules-sections-and-filing-process)
- [ClearTax — TDS under s.194S](https://cleartax.in/s/tds-under-section-194s-of-income-tax-act)
- [Business Standard — FIU notices to 25 offshore crypto platforms (Oct 2025)](https://www.business-standard.com/finance/news/fiu-notices-offshore-crypto-platforms-pmla-non-compliance-125100101180_1.html)
- [Charltons Quantum — India crypto crackdown 2025, FIU-IND blocks 25 offshore exchanges](https://charltonsquantum.com/india-crypto-crackdown-2025-fiu-blocks-exchanges/)
- [Business Today — Esya Centre: 3–5 million users shifted offshore after 1% TDS](https://www.businesstoday.in/personal-finance/news/story/up-to-5-million-crypto-users-shifted-to-offshore-trading-platforms-report-405221-2023-11-09)
- [MDPI Mathematics 14(2):346 — The Two-Tiered Structure of Cryptocurrency Funding Rate Markets](https://www.mdpi.com/2227-7390/14/2/346)
- [Glassnode Workbench — BTC futures annualized yield](https://studio.glassnode.com/workbench/btc-futures-annualized-yield)
- [Deribit — fee schedule and VIP tiers](https://support.deribit.com/hc/en-us/articles/25944746248989-Fees)
- [Deribit — An introduction on market making](https://medium.com/deribitofficial/an-introduction-on-market-making-3d50d927f3ab)
- [QuantConnect forum — Alpha Streams wind-down](https://www.quantconnect.com/forum/discussion/13441/alpha-streams-refactoring-2-0/)
- [Darwinex — performance fees for DARWIN providers](https://help.darwinex.com/performance-fees-darwin-provider)
- [Collective2 — how trade leaders get paid](https://trade.collective2.com/trade-leaders-get-paid/)
- [nmrdash — Numerai vs Kaggle payout distribution](https://nmrdash.com/articles/numerai-vs-kaggle)
- [Balakrishna & Co — F&O tax audit requirement FY 2025-26 / AY 2026-27](https://www.balakrishnaandco.com/news-and-articles/56-tax-audit-requirement-for-f-o-trading-fy-2025-26-ay-2026-27)