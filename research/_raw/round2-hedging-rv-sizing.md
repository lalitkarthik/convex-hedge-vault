# Round Two — (A) Discrete hedging bands, (B) RV from minute data, (C) sizing

Everything below was opened and read except where explicitly flagged. Where a primary document was unreachable I say so rather than substituting a summary.

---

## (A) DISCRETE HEDGING AND HEDGING BANDS

### A1. Zakamouline, *Optimal Hedging of Options with Transaction Costs* (EFMA 2005 working paper)
**URL:** `https://efmaefm.org/0efmameetings/efma%20annual%20meetings/2005-Milan/papers/284-zakamouline_paper.pdf`
(TLS cert on efmaefm is broken — `curl -k` works, browsers will warn. I downloaded and read the full text.)

**What it concretely gives him:** this single free paper contains, in one place and in consistent notation, *all five* strategies he asked about, plus the empirical horse-race between them. Verbatim from the paper:

- **Leland (eq. 4):** σ_m² = σ²(1 + √(8/π) · λ/(σ√Δt)), hedge at Δ = N(d₁(σ_m)). Explicitly noted: "as Δt → 0 the modified volatility becomes unbounded and Leland's hedge amounts to the super-replicating strategy where a single share of stock is held."
- **Whalley–Wilmott (eq. 12):** no-trade band Δ = ∂V/∂S ± H_ww, with **H_ww = ( (3/2) · e^{−r(T−t)} · λ S Γ² / γ )^{1/3}** — the cube root. Centred on the BS delta, **no volatility adjustment**.
- **Barles–Soner (eqs. 13–14):** band *plus* a gamma-dependent vol adjustment σ_m² = σ²(1 + f(e^{r(T−t)}γ²S²Γ)), where f solves a nonlinear ODE.
- **Hodges–Neuberger / Davis–Panas–Zariphopoulou:** the exponential-utility formulation Δ(τ) = y_w(τ) − y₀(τ), solved numerically; the paper reproduces the setup faithfully and notes Davis et al.'s result that the option price is approximately invariant to the *form* of the utility function — "mainly only the level of absolute risk aversion plays an important role."
- **Zakamouline's own approximation (eq. 15–22):** Δ = ∂V(σ_m)/∂S ± (H_w + H₀), σ_m² = σ²(1 ± H_Δ). Fitted forms (I recovered the *published* constants from runnable code, see A2, because Greek glyphs are lost in the WP's text layer):
  - H₀ = λ / (γ S σ² (T−t))  — the term the two asymptotic strategies lack entirely
  - H_w = 1.12 · λ^0.31 · (T−t)^0.05 · (e^{−rT}/σ)^0.25 · (|Γ|/γ)^0.5
  - H_Δ = −4.76 · (λ^0.78 / (T−t)^0.02) · (e^{−rT}/σ)^0.25 · (γ S²|Γ|)^0.15

**Empirical result (100,000 paths, 250 rebalance opportunities, mean-variance *and* mean-VaR frontiers):** approximation > Whalley–Wilmott > Barles–Soner ≈ delta-tolerance ≈ asset-tolerance > Leland > BS. Two mechanisms are named: (i) WW and BS have no H₀, so deep ITM/OTM options get a near-zero band, which is "clearly suboptimal"; (ii) delta-tolerance, asset-tolerance and WW have no vol adjustment, and "either undervaluation or overvaluation of the volatility adjustment results in a *drastic* deterioration."

**The line that should change what he builds:** *"When λ < 0.001, our approximation strategy and both the asymptotic strategies produce practically identical results."* NIFTY-futures λ is ≈ **1.3 bps = 0.00013** (derivation in A6), an order of magnitude below that threshold. **For hedging NIFTY delta with NIFTY futures, Zakamouline buys him nothing over plain Whalley–Wilmott.** Build WW, spend the saved weeks on (B). The calculus flips if he hedges with *options* (NIFTY weekly half-spread ≈ 0.05 on ~100 premium = 5 bps, ×2 legs → λ well above 0.001), where the vol adjustment starts to matter.

**Tests passed:** (3) — Zakamouline is an academic, not a trader, so *not* (3); (4) **counts double** — the paper names its own failure mode explicitly ("to implement the approximation for another type of European option one needs to start with the numerical calculations… unlikely to be commonly used by practitioners"; asymptotics overvalue both band and vol adjustment at realistic parameters); (5) reproducible — it is a pure Monte Carlo, no data needed.

**Honest caveat:** the WP's fitted constants (1.08, 6.85) differ from the published *Quantitative Finance* version's (1.12, −4.76). The calibration is only valid on r∈[0,0.1], σ∈[0.1,0.4], T−t∈[0,1.5], λ∈[0.001,0.02], γ∈[0.05,15] at S=100 — **NIFTY's λ sits outside the calibrated range on the low side**, so the fitted exponents are extrapolation. Another reason to just use WW.

### A2. `sweliam/zakamouline` — Python implementation
**URL:** `https://github.com/sweliam/zakamouline` (`zakamouline.py`)

**What it gives him:** the three fitted functions above as literal Python, plus `hedgebands(position, lambda_, gamma_lower)` returning `(h_plus, h_neg)` for a whole option *position* (uses portfolio gamma, so it extends to spreads). This is the fastest way to pin down the published constants and sign conventions without buying the QF paper.

**Tests passed:** (1) runnable code, (5) reproducible.
**Honest caveat:** the author flags his own bug — the `isLong` flag is read from leg 0, so it silently mis-signs the volatility adjustment for any structure that is not uniformly long or uniformly short (a short condor breaks). Depends on a local `bsm` module not in the repo. Treat it as a formula reference, not a library.

### A3. `pfnet-research/pfhedge` — Whalley–Wilmott as a production module
**URL:** `https://github.com/pfnet-research/pfhedge` · docs: `https://pfnet-research.github.io/pfhedge/generated/pfhedge.nn.WhalleyWilmott.html`

**What it gives him:** `pfhedge.nn.WhalleyWilmott(derivative, a=1.0)` implementing width = (3cΓ²S / 2a)^{1/3} with `a` the exponential-utility risk aversion, differentiable in PyTorch, and a `BrownianStock(cost=1e-5)` cost model wired into the simulator. Gives him a WW baseline to benchmark anything he writes, and a deep-hedging comparison for free.

**Tests passed:** (1), (2) — cost is a first-class constructor argument, not an afterthought; (5).
**Honest caveat:** industrial-research code from Preferred Networks, not a trading desk. Their cost model is a single proportional rate — it cannot represent NIFTY's *asymmetric* (sell-side-only STT) cost, which is the dominant term. He will have to patch that.

### A4. Derman & Kamal, *When You Cannot Hedge Continuously* (Goldman Sachs QSRN, Risk Jan 1999)
**URL:** `https://emanuelderman.com/wp-content/uploads/1998/12/risk-non_continuous_hedge.pdf`
**Runnable replication:** `https://github.com/MarcosCarreira/DermanPapers` → `DiscreteHedging.ipynb`

**What it gives him — the other half of the trade-off, in closed form.** WW/Zakamouline price the *cost* of hedging; this prices the *risk* of not hedging. From the paper (50,000 paths, 1-month ATM put, S=K=100, σ=20%):

- std(P&L) ≈ √(π/4) · (1/√N) · Vega · σ, i.e. ≈ 0.886 σ·Vega/√N
- expressed in vol points, the one-sd replication error is ≈ **σ/√N**
- measured numbers: N=21 (daily) → σ(P&L) = **16.3% of premium**; N=84 → **8.1%**. Quadrupling the hedge frequency halves the error.
- mean P&L is *zero* — discrete hedging adds noise, not bias. That is the correct null and most people get it wrong.
- the error distribution is close to Gaussian, so a standard deviation is a meaningful risk number here.

**Tests passed:** (1) runnable replication notebook exists, (3) Goldman Sachs Equity Derivatives Research, (4) counts double — the note ends by naming exactly what it excludes: "the advantage gained by increased rehedging must be weighed against the losses due to transaction costs and potentially adverse market impact… including jumps, changes in the future levels of volatility, and transaction costs will only increase the need for an even larger cushion."
**Honest caveat:** pure Black–Scholes Monte Carlo — constant known σ, no jumps, no costs, no spot-vol correlation. It is the *risk* leg only. Also: real weekly NIFTY options are nowhere near lognormal-with-known-σ.

### A5. Sepp, *When You Hedge Discretely: Optimization of Sharpe Ratio…* (J. Investment Strategies 3(1), 2013) + his blog post
**URLs:** `https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1865998` (free download) · blog with the results laid out: `https://artursepp.com/2017/05/01/how-to-optimize-volatility-trading-and-delta-hedging-strategies-under-the-discrete-hedging-with-transaction-costs/` · MATLAB code, MathWorks File Exchange #54345

**What it gives him — the objective function that A1 and A4 are inputs to.** Sepp derives analytic P&L mean, P&L variance *and* expected transaction costs under four dynamics (lognormal, jump-diffusion, stochastic vol, SV+jumps), then maximises the Sharpe ratio over hedging frequency. The structure (from the blog, which states them explicitly):

- E[P&L] = (σ_imp² − σ_real²) · (½ Γ S₀²) · T — **independent of hedging frequency**
- σ(P&L) = √(returns_vol²/N + residual_vol²) — the Derman term plus an irreducible floor
- E[costs] = bid-ask · √N · C — costs grow as **√N**, not N, because each rebalance is smaller
- ⇒ Sharpe is **humped** in N. There is an interior optimum and a closed form for it in the paper.
- Bid-ask modelled explicitly: buys at S(1+½s), sells at S(1−½s).
- Empirically (his Fig. 6): **price and delta bands beat fixed-time rebalancing** — same Sharpe, lower realised costs.

**Tests passed:** (1) MATLAB code published, (2) explicit bid-ask, (3) practitioner — Sepp has run derivatives/systematic books at Merrill, BofA, Julius Baer, LGT, (4) counts double — he states the model assumes **sticky-strike** implied vol dynamics and that the position is held to maturity: "for positions terminated early or non-vanilla products, the risk of changes in the implied volatility can be significant."

**Honest caveat:** sticky-strike is exactly wrong for NIFTY index options — the whole point of A7 is that NIFTY's spot-vol correlation is large and negative. Sepp's *frequency* result survives; his *P&L* result needs the MV-delta correction bolted on.

### A6. The cost model — primary NSE / SEBI documents, not a broker blog
Round one used taxguru. These are the actual documents.

| Item | Primary source | Verified number |
|---|---|---|
| Exchange transaction charge | **NSE circular NSE/FA/64232, 27 Sep 2024** — `https://nsearchives.nseindia.com/content/circulars/FA64232.pdf` | Equity **futures: ₹1.73 per lakh, each side** (= 0.173 bp). Equity options: ₹35.03 per lakh of **premium**, each side. Effective 1 Oct 2024, uniform for all members per SEBI/HO/MRD/TPD-1/P/CIR/2024/92. |
| STT | Finance (No. 2) Act 2024, amending s.98 of Finance (No.2) Act 2004, w.e.f. 1 Oct 2024 | Sale of **futures: 0.02%** of traded value (seller). Sale of **options: 0.1%** of premium (seller). Exercised options: 0.125% of intrinsic (buyer). |

**λ for delta-hedging NIFTY with NIFTY futures (one-way, cost averaged over a round trip):**

| Component | bp per side |
|---|---|
| STT (sell side only, 2.0 bp, halved over round trip) | **1.00** |
| Exchange charge (both sides) | 0.17 |
| Stamp duty (buy side, 0.002%) — *not primary-verified* | ~0.10 |
| GST 18% on exchange charge + brokerage | ~0.03 |
| Half-spread (1 tick = 0.05 on ~24,000) | 0.01 |
| **λ ≈** | **≈ 1.3 bp = 0.00013** |

Three consequences he will not find stated anywhere:

1. **The spread is irrelevant. The tax is the cost.** STT is ~77% of λ. The half-spread on NIFTY futures is 0.01 bp — a hundred times smaller. Every US paper on hedging costs is about spread and impact; in NIFTY it is about a statutory levy.
2. **STT is sell-side-only, which violates the symmetric-proportional assumption of Leland, Whalley–Wilmott, Barles–Soner and Zakamouline.** All four derive a *symmetric* band around Δ. With a one-sided cost the true no-trade region is asymmetric: the sell boundary should sit further from Δ than the buy boundary. Nobody has published this for the Indian market. It is a clean, small, publishable extension and it takes days, not weeks.
3. **λ^{1/3} scaling means the cost input barely matters and that is the point.** Band ∝ λ^{1/3}: to halve the band you must cut costs 8×. Doubling λ widens the band only 26%. Rebalance count ∝ h^{−2} ∝ λ^{−2/3}. Total transaction cost over the option's life ∝ λ·h·(rebalance count) ∝ **λ^{2/3}**. So a 2× cost shock costs him only 59% more, not 100% more — *provided he re-widens the band*. If he keeps the band fixed he eats the full 2×. That is the whole practical value of the cube root.

**Unverified and material:** secondary sources state the Finance Act 2026 raised futures STT to 0.05% and options STT to 0.15% of premium w.e.f. 1 April 2026. **I could not reach the primary Act text — incometaxindia.gov.in returns 403 to non-browser clients.** If true, λ ≈ 2.8 bp and the WW band widens by (2.8/1.3)^{1/3} = **1.29×**. He must confirm this from an actual contract note or the Act before calibrating anything.

### A7. Hull & White, *Optimal Delta Hedging for Options* (JBF 82, 2017) — the minimum-variance delta
**URL:** `https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2658343` (free). A full-text mirror that I read end-to-end: `http://spekulant.com.pl/article/Delta%20Hedging/Optimal%20Delta%20Hedging.pdf`

**The rule, verbatim (their eqs. 2, 5, 6):**

- δ_MV = δ_BS + ν_BS · ∂E(σ_imp)/∂S
- Empirical model: **δ_MV = δ_BS + (ν_BS /(S√T)) · (a + b·δ_BS + c·δ_BS²)**
- Equivalently: E(Δσ_imp) = [(a + bδ_BS + cδ_BS²)/√T] · (ΔS/S)
- Estimate a, b, c by OLS on **Δf − δ_BS ΔS = (ν_BS/√T)(ΔS/S)(a + bδ_BS + cδ_BS²) + ε**, separately for puts and calls, on a rolling 36-month window, refit monthly. Window length 12–60 months made no material difference.

**Results (S&P 500, 2004–2015, 1.3M quotes, out-of-sample):** variance-reduction Gain **26% for calls, 23% for puts**; **42% for the highest-strike (OTM) calls**, 17% for ITM. δ_MV − δ_BS was **negative in every moneyness/maturity bucket** — *under-hedge calls, over-hedge puts*. Beats a daily-recalibrated SABR (t = 8.24 calls, 11.52 puts) and beats local vol badly, using 312 parameters against SABR's ~100,000. R² of Δσ_imp = (α/√T)(ΔS/S) is **0.60** for δ=0.1 calls, declining as δ rises.

**Tests passed:** (2) — no, they use mid-quotes and say so; (3) — no; (4) **counts double**, several times over: gains are smaller for individual stocks and ETFs than for indices; MV hedging works worse for puts because put IVs carry more idiosyncratic variation; put-call parity was "seriously violated" before Dec 2008; and — **the one that matters most for him** — *"We confined our test to options with maturities greater than 13 days… Including the very short maturity options slightly worsens our results due to the large gammas of short-term options that are close to the money."* (5) reproducible on any option panel.

**Why the BS delta is systematically wrong on NIFTY, and what to do:** the mechanism is δ_MV = δ_BS + ν·∂E(σ)/∂S, and ∂E(σ)/∂S is large and negative for an equity index. NIFTY has a steep, persistent negative skew and a strongly negative NIFTY/India VIX correlation, so the correction is *at least* as large as SPX's. But **nobody has published a, b, c for NIFTY**, and Hull-White's own exclusion of sub-14-day options excludes almost the entire NIFTY weekly complex — which is where the volume is. So:

- The primary methodology document for the vol series is NSE's own: **India VIX white paper**, `https://nsearchives.nseindia.com/web/sites/default/files/inline-files/white_paper_IndiaVIX.pdf` (verified live; CBOE method adapted with natural cubic-spline interpolation of missing/wide strikes, forward level taken from the **traded NIFTY future**, time-to-expiry in **minutes**, MIBOR as the risk-free rate).
- His first concrete deliverable: estimate α in Δσ_imp = (α/√T)(ΔS/S) on NIFTY, **conditioned on days-to-expiry**, using his minute data. Then estimate the full (a,b,c) quadratic. Because NSE now runs a **weekly Tuesday** expiry cycle (see A8), α will almost certainly be a function of position in the weekly cycle, which is a structure the SPX literature does not have.

### A8. NSE / SEBI primary documents that change the hedging problem
All URLs verified reachable and read.

- **SEBI/HO/MRD/TPD/P/CIR/2024/132, 1 Oct 2024** — *Measures to Strengthen Equity Index Derivatives Framework.* `https://www.sebi.gov.in/legal/circulars/oct-2024/measures-to-strengthen-equity-index-derivatives-framework-for-increased-investor-protection-and-market-stability_87208.html` — additional **2% ELM on all short option contracts on expiry day** (from 20 Nov 2024), ₹15 lakh minimum contract size, upfront premium collection, **removal of calendar-spread margin benefit on expiry day**, intraday position-limit monitoring.
- **SEBI/HO/MRD/MRD-TPD-1/P/CIR/2025/76, 26 May 2025** — expiry standardised to Tuesday or Thursday per exchange. `https://www.sebi.gov.in/legal/circulars/may-2025/final-settlement-day-expiry-day-for-equity-derivatives-contracts_94189.html`
- **NSE/FAOP/68747, 25 Jun 2025** — `https://nsearchives.nseindia.com/content/circulars/FAOP68747.pdf` — NIFTY weekly, monthly, quarterly and half-yearly all move **Thursday → Tuesday**; new contracts expiring on/after 1 Sept 2025 issued on the Tuesday cycle from 26 Jun 2025 EOD. **His pre-Sept-2025 and post-Sept-2025 minute data are two different seasonal regimes and must not be pooled.**
- **NSE settlement price page** — `https://www.nseindia.com/static/products-services/equity-derivatives-settlement-price` — index option **final exercise settlement = closing price of the underlying index in the CM segment on the last trading day**, and the index close is the **last-half-hour weighted-average price** (15:00–15:30).

### A9. The expiry-day problem, stated properly, and the override
The task's framing ("bands collapse, formulas demand infinite trading") is half right. What actually happens as τ → 0:

- **ATM:** Γ ~ 1/(Sσ√τ) → ∞, so H_ww ∝ (λSΓ²/γ)^{1/3} ∝ **τ^{−1/3} → ∞**. The band *widens* past the entire feasible delta range [0,1]. The model is not asking for infinite trading; it is saying **the position is unhedgeable and you should stop**. The small-cost asymptotic premise λΓ → 0 has failed.
- **Away from ATM:** Γ → 0, so H_ww → 0, but Zakamouline's H₀ = λ/(γSσ²τ) → ∞. Both terms diverge, from opposite directions.
- **Leland:** σ_m² = σ²(1 + √(8/π)λ/(σ√Δt)) → ∞ as Δt → 0 regardless of τ; the hedge degenerates to holding one share.

So **every** formula in this literature fails on the final session and they fail loudly, not silently. The practitioner override is not a better band — it is to stop treating expiry day as a hedging problem and treat it as a *sizing* problem (which is (C)):

1. **Cap gamma ex ante.** Decide the maximum dollar-gamma you will carry into the final session at position-entry time, when you can still choose. There is no rebalancing rule that rescues a position that is too big on Tuesday afternoon.
2. **NSE-specific: your futures hedge has structural basis risk on expiry day by construction.** Final settlement is the **15:00–15:30 VWAP of the spot index**, not the futures, not the close. A delta hedge in futures cannot replicate a 30-minute VWAP of a different instrument. This is also precisely what SEBI's +2% expiry-day ELM is compensating for — the circular's own stated rationale is "significant basis risk at expiry where the value of the contract expiring on the day can move differently from similar contracts."
3. **Roll or close before the final session** if the gamma is material; or hedge gamma with a same-expiry option rather than delta with futures.
4. After 15:30 you hold an unhedgeable position through the settlement window. Size for that, not around it.

### A10. Mapping all of this to minute bars — what is measurable and what is not
NSE continuous session is 09:15–15:30 = **375 minutes/day**.

**Time-based rules (rebalance every Δt ≥ 1 min) are exactly measurable on minute bars.** Fill at the bar close, plus half-spread, plus λ. No approximation.

**Band rules are NOT exactly measurable on minute bars, and the bias is one-directional.** A delta band is touched *inside* a minute. Two wrong ways to handle it:
- Check only bar closes → you under-count crossings, hedge late, and *overstate* the strategy (you get a free look-ahead-free but lucky fill).
- Use bar high/low to detect the touch and assume a fill *at the band level* → you are assuming a resting limit order was filled at the touch, i.e. you assume zero adverse selection. This is the standard silent optimism in band backtests.

Honest rule of thumb for when minute bars are adequate: NIFTY per-minute return sd ≈ 13%/√(250×375) ≈ **4.2 bp**. If the band's half-width in *spot* terms, h/(ΓS), is less than roughly 2× that (≈ 8 bp), a typical minute contains multiple crossings and minute bars will not resolve the strategy. Narrow bands — which is exactly what low λ and high Γ produce, i.e. exactly NIFTY weeklies near expiry — are the case where he needs tick data. **Calibrate the time-based rule on minute bars honestly; treat band-rule minute-bar results as an upper bound and validate the winner on ticks.**

**Worked answer to "how often should I hedge", from verified inputs.** Weekly NIFTY straddle, 5 sessions = 1,875 minutes, σ = 13%, λ = 1.3 bp. Derman noise (σ/√N, in vol points) vs Leland cost (σ_m/σ − 1, in vol points):

| Rebalance | N | Derman noise (vol pts) | Leland cost (vol pts) |
|---|---|---|---|
| daily | 5 | 5.8 | 0.16 |
| hourly | 31 | 2.3 | 0.4 |
| 15-min | 125 | 1.16 | 0.8 |
| 5-min | 375 | 0.67 | 1.35 |
| 1-min | 1875 | 0.30 | 2.9 |

**The trade-off bottoms out around 5–15 minutes and is flat between them.** Daily hedging is indefensible — it throws away 5.8 vol points of noise to save 1 vol point of cost. Minute hedging is indefensible in the other direction. This is arithmetic, not opinion; he should redo it with his own λ and σ, and note that the two columns are not strictly additive (one is a P&L standard deviation, one is a mean drag) — the correct objective is Sepp's Sharpe, which the table approximates.

### A11. Honest negatives for (A)
- **Whalley & Wilmott (1997), *Math. Finance* 7(3):307–324 — I could not reach the original.** Every free restatement I verified (Zakamouline eq. 12, pfhedge's docs and source) agrees on the form, so I am confident in the formula, but he should pull the original through IIT-KGP for the derivation and the regularity conditions. Free related paper by the same author, reachable: `https://warwick.ac.uk/fac/soc/wbs/subjects/finance/faculty1/elizabeth_whalley/whalleypartialtcjan06.pdf` (*Optimal partial hedging of options with small transaction costs*).
- **Hodges & Neuberger (1989), *Review of Futures Markets* 8:222–239, and Davis–Panas–Zariphopoulou (1993), *SIAM J. Control Optim.* 31:470–493 — I could not reach either primary.** Zakamouline's WP restates both faithfully and is free; that is the best available substitute and I am flagging it as a substitute rather than pretending otherwise.
- **There is no credible free first-person account of how an Indian index-options market maker actually sets his hedge trigger.** I looked. The free Indian material is all broker education or content marketing and is auto-rejected. The two usable practitioner voices on this question in any market are Sepp (A5) and Sinclair. This is a genuine gap, and it means he has to derive the answer rather than look it up — which the table in A10 shows is a day's work, not a research programme.
- **No published estimate of Hull–White (a, b, c) or of α for NIFTY exists** as far as I could find. Novel, cheap, high-value.

---

## (B) REALISED VOLATILITY FROM MINUTE DATA

### B1. Liu, Patton & Sheppard, *Does anything beat 5-minute RV?* (J. Econometrics 187(1), 2015)
**URL (free full text, verified, read):** `https://public.econ.duke.edu/~ap172/Liu_Patton_Sheppard_JoE_2015.pdf`

**What it gives him:** the decision, made for him, on evidence. 420 estimators (RV, subsampled RV, Bandi–Russell optimal sampling, RVac1, TSRV, MSRV, MLRV, realized range, realized kernels, pre-averaging, plus 228 jump-robust variants), 31 assets, 5 asset classes, 11 years of tick data, tested with Romano–Wolf stepwise multiple testing and the Hansen model confidence set. Result: **nothing significantly beats 5-minute RV** except for one asset (10-year Treasury futures).

Four operational findings I extracted from the paper that matter more than the headline:

- **Subsampling helps at 5-min and 15-min; it hurts at 1-min and below.** Subsampled 5-min RV — the "second-best estimator" of Zhang–Mykland–Aït-Sahalia — is among the top performers.
- **Transaction prices beat mid-quotes at low frequencies**; quotes only win at 1-tick/1-second.
- **Tick-time sampling beats calendar-time at 5-min and 15-min**; calendar-time wins only at 1s/5s.
- **The single most important line for him:** *"more sophisticated realized measures generally perform significantly worse in non-US markets than in US markets… potentially indicative of different market microstructure effects in non-US markets."* The realized-kernel/TSRV machinery is tuned to NYSE/CME microstructure. It has *no* demonstrated advantage on NSE and some demonstrated disadvantage outside the US.

**Tests passed:** (1) — all measures computed with Kevin Sheppard's free Oxford Realized / MFE Toolbox (footnote 16), (5) reproducible, (4) counts double — they explicitly report the non-US degradation, and report that 5-min RV does *not* appear in the top-10 by average rank for any asset class, i.e. they publish the evidence against their own headline.
**Honest caveat:** the target (quadratic variation) is latent; the ranking depends on a noisy proxy plus an instrument. And "5 minutes" is calibrated to very liquid US assets; the authors say so in footnote 23.

### B2. Andersen, Bollerslev, Diebold & Labys, *Great Realisations* (Risk, March 2000) — the volatility signature plot
**URL (free, verified, read):** `https://www.sas.upenn.edu/~fdiebold/papers/paper29/temp.pdf`

**What it gives him — the diagnostic he must run before choosing anything in B1.** Plot average realised volatility against sampling interval k. Two shapes, and they mean opposite things:

- **Liquid asset:** RV is *highest* at the smallest k and falls as k rises, stabilising ≈ k = 20 min. Cause: **negative** serial correlation from bid-ask bounce. Naive 1-minute RV is biased **up**.
- **Illiquid asset:** RV is *lowest* at small k and rises, stabilising ≈ k = 15 min. Cause: **positive** serial correlation from inactive/stale trading. Naive 1-minute RV is biased **down**.

Note what the *originators of the tool* recommended for their own data: **k = 20 minutes**, not 5.

**This is decisive for his instrument choice.** The **NIFTY 50 index** is a weighted average of 50 stocks that do not print synchronously. At high frequency it exhibits the *illiquid* signature — positive autocorrelation from staleness — so **1-minute RV on the index is biased downward**, opposite to the standard bid-ask-bounce story, and 5 minutes may not be enough. The **front-month NIFTY future** is a single, extremely liquid instrument with a 0.05 tick and will show the *liquid* signature. **He should compute RV on the future, not the index**, and he should draw both signature plots and look at them before writing another line of code. This is 30 minutes of work and it determines everything downstream.

**Tests passed:** (3) — Diebold and Bollerslev are academics but the piece is a *Risk* technical article written for a desk audience; (4) counts double — it names microstructure bias, the bias/variance trade-off, and Epps-effect asynchrony as the multivariate failure mode; (5) trivially reproducible.
**Honest caveat:** a Risk magazine article, informal, 2000-vintage; no formal test.

### B3. Zhang, Mykland & Aït-Sahalia, *A Tale of Two Time Scales* (JASA 100:1394–1411, 2005) — TSRV
**URL (free, verified):** `https://www.princeton.edu/~yacine/twoscales.pdf`

**What it gives him:** the theory of why naive high-frequency RV fails (with observation noise ε, RV converges to 2n·Var(ε), i.e. to the *noise* variance, not the price variance), the optimal-sampling-frequency result when noise is asymptotically small, and the "five estimators" ladder culminating in TSRV = subsampled slow-scale RV bias-corrected by the fast-scale RV. Crucially it also establishes that **subsampling without averaging is inferentially wrong** — which is why the "subsampled RV" of B1 works.

**Tests passed:** (1) implemented in both toolchains in B4, (5).
**Honest caveat:** this is the *theory*; B1 is the *evidence*, and B1 says TSRV does not beat subsampled 5-min RV in practice on real assets, and does worse outside the US. Read it to understand the bias, not to choose the estimator.

### B4. Toolchain: `highfrequency` (R) — the only complete, peer-reviewed, free implementation
**Paper (open access, verified, read):** Boudt, Kleen & Sjørup, *Analyzing Intraday Financial Data in R: The highfrequency Package*, JSS 104(8), 2022 — `https://www.jstatsoft.org/article/view/v104i08`
**Package:** `https://cran.r-project.org/package=highfrequency`

I verified every function he needs is actually in there:
- Cleaning: `tradesCleanup`, `quotesCleanup`, `aggregateTS`, `makeReturns`
- Realized measures: `rRVar`, `rAVGCov` (subsampled), `rKernelCov` (realized kernels), `rTSCov` / `rRTSCov` (two-scale, robust two-scale), `rMRCov` (pre-averaging/modulated), `rThresholdCov`, `rHYCov` (Hayashi–Yoshida), `rQuar`, `rQPVar`
- Jump-robust: `rBPCov` (bipower), MinRV/MedRV, `rSemiCov` (realized semivariance)
- **Jump tests:** `BNSjumpTest` (daily, Barndorff-Nielsen–Shephard, JV = RV − BPV) and `intradayJumpTest` (Lee–Mykland, identifies *which minute* contains the jump)
- **Intraday periodicity — the one he specifically needs:** `spotVol(..., periodicVol = "TML" | "WSD")` implementing Boudt, Croux & Laurent (2011) Truncated-ML (parametric, smooth) and Weighted-SD (non-parametric, jump-robust). The JSS paper's own Figure 6 shows the diurnality factor running ~2.3 at the open down to ~0.8 mid-session.
- Forecasting: `HARmodel` (Corsi HAR)

**Tests passed:** (1) obviously, (5) obviously, (4) — the JSS paper is candid that the non-parametric WSD periodicity estimate is jagged with small samples and that daily jump tests "cannot be used to detect the *number* of jumps".
**Honest caveat and an honest negative:** **there is no Python equivalent of comparable completeness or peer review.** The closest free things are Kevin Sheppard's MATLAB **MFE Toolbox** (`https://github.com/bashtage/mfe-toolbox`, `realized_variance`, `realized_kernel`, `realized_variance_optimal_sampling` implementing Bandi–Russell, MinRV/MedRV, TSRV, MSRV — this is the code LPS 2015 actually used) and an abandoned WIP port `JannesKlaas/MFE-Toolbox-Python`. If he is a Python shop he will be writing RV estimators himself or calling R. Better to know that now.

### B5. Hansen & Lunde, *A Realized Variance for the Whole Day Based on Intermittent High-Frequency Data* (J. Financial Econometrics 3(4), 2005) — the overnight gap
**Free working-paper version (verified, downloadable):** `https://papers.ssrn.com/sol3/papers.cfm?abstract_id=531422`

**What it gives him:** three estimators of whole-day IV and the assumptions each requires, and — the useful part — the **optimal linear combination** RV_day = ω₁·r²_overnight + ω₂·RV_open-to-close, with weights determined by minimising MSE *despite IV being latent*. Their DJIA finding: **~80% of daily volatility occurs in the active session** (active/inactive ratio ≈ 4), correlation between r²_overnight and active-period RV ≈ 0.30, and the MSE-optimal weights put **disproportionately more weight on RV** because the single squared overnight return is a far noisier estimator of its own period's variance than RV is of the session.

Two things this rules out for him: **do not** just add r²_overnight to RV (their estimator 2), and **do not** scale open-to-close RV up by a constant factor (their estimator 1). Both are dominated.

**Tests passed:** (1) — the estimator is in `highfrequency` and MFE, (5) — reproducible on any daily+intraday panel, (4) counts double — the paper's whole structure is "here are three estimators and here are the assumptions under which each one is wrong."
**Honest caveat / honest negative:** **the DJIA number does not transfer.** The NIFTY overnight window is 15:30 → 09:15 = **17.75 hours**, spanning the entire US session and GIFT Nifty's overnight trading, plus a pre-open auction at 09:00–09:08. **Nobody has published the active/inactive variance ratio for NIFTY.** He must estimate it, and it is a genuinely important number: for a *weekly* option with 5 sessions to run, the option prices 7 calendar days of variance while he can only measure 5×375 minutes of it — the overnight/weekend share of a weekly option's remaining variance is far larger than for a monthly. Get this wrong and the entire IV-vs-RV comparison is biased.

### B6. Intraday seasonality on NSE specifically — Singh & Gangwar (MPRA 89689)
**URL (free PDF, verified, read):** `https://mpra.ub.uni-muenchen.de/89689/1/MPRA_paper_89689.pdf`

**What it gives him:** the only free study I could find that actually measures NIFTY intraday volatility on real minute data (1-minute NIFTY *futures*, 1 Jan 2011 – 31 Aug 2018, Muhurat and special Saturday sessions removed). Their Table 1, pooled 2011–Aug 2018, hourly-scaled volatility in %:

| 09:15–10:00 | 10:00–11:00 | 11:00–12:00 | 12:00–13:00 | 13:00–14:00 | 14:00–15:00 | 15:00–15:30 |
|---|---|---|---|---|---|---|
| **0.3496** | 0.2380 | **0.2248** | 0.2460 | 0.2850 | **0.3268** | 0.2799 |

**Read this carefully, because it is not the textbook U.** Open/trough vol ratio = 1.56 (**variance ratio 2.4×**). But the **last half-hour is *lower* than 14:00–15:00** (0.2799 vs 0.3268). NSE's shape is a **J with a clipped right arm**, not a U: the peak of the afternoon is 14:00–15:00, and volatility *falls* into the close. If he imports a US-calibrated U-shaped diurnal factor he will over-deseasonalise the last 30 minutes and systematically distort exactly the window that (a) sets the daily settlement price and (b) is the expiry settlement VWAP window. Friday is the highest-volatility weekday, all-day.

**Tests passed:** (5) reproducible on his own data — that is the only test it passes cleanly.
**Honest caveat, stated plainly:** **this source does not pass the filter and I am not recommending it as authority.** It has no cost model, is not by a practitioner, is a student working paper in a non-refereed archive, and its methodology text says volatility is "converted from per minute to hourly by multiplying with a factor of 60" — which is wrong (it must be √60); the reported levels are only consistent with correct √-scaling, so the description and the arithmetic disagree and I cannot tell which is the error. **Use the table for the *shape* only, as a prior to check your own estimate against, and re-estimate everything on your own data with `spotVol(periodicVol="WSD")`.** I am including it because "the shape is a clipped J, not a U" is a real and checkable claim, and because an honest weak source flagged as weak beats a confident US import.

**Three NSE-specific seasonality facts I could verify from primary exchange documents, which no paper covers:**
1. **Pre-open auction 09:00–09:08 exists** (since 18 Oct 2010), so the 09:15 open already absorbs part of the overnight gap. The first minute bar is a *post-auction* bar, not a gap bar. Do not treat 09:15 as the gap.
2. **The 15:00–15:30 window is the daily settlement window** — futures daily settlement is the last-30-minute VWAP, and the index close is the last-30-minute weighted average (NSE settlement-price page, verified). Volume and volatility in that window are mechanically driven by settlement, not information.
3. **On expiry day that same 15:00–15:30 window is the *final* settlement window for every expiring index option.** So expiry-day seasonality is not a general "expiry effect" — it is a specific, dated, half-hour pinning mechanism whose location he knows in advance, and which **moved from Thursday to Tuesday for contracts expiring on/after 1 Sept 2025** (NSE/FAOP/68747). Estimate the periodicity factor separately for {expiry day, non-expiry day} × {pre-Sept-2025, post-Sept-2025}. Four regimes minimum.

### B7. The recommended estimator, and the first project made concrete

**Recommended: subsampled 5-minute RV on the front-month NIFTY *future*, computed in tick time, on transaction prices, open-to-close, plus a Hansen–Lunde-weighted overnight term — with the sampling interval confirmed (not assumed) by his own volatility signature plot.**

Reasoning, in order: LPS 2015 says nothing beats 5-min RV and that sophisticated estimators degrade outside the US (B1); LPS says subsampling helps at 5-min, tick-time beats calendar-time at 5-min, and trades beat quotes at 5-min (B1); ABDL says draw the signature plot first because the answer is asset-specific and *their* answer was 20 minutes (B2); the future rather than the index because index staleness biases high-frequency RV *downward* (B2); Hansen–Lunde weights rather than naive addition for the overnight (B5).

**The deseasonalised-RV vs remaining-implied-variance project, specified exactly:**

1. **RV pipeline.** Front-month NIFTY future, minute bars → `aggregateTS` to 5-min in tick time → subsampled RV over the 5 offset grids (`rAVGCov`) → this is `RV_d`. Also compute `rBPCov` and MedRV on the same grid.
2. **Deseasonalise.** `spotVol(periodicVol = "WSD")` (Boudt–Croux–Laurent, jump-robust) estimated **separately per regime** {expiry / non-expiry} × {pre-Sept-2025 / post-Sept-2025}. Deseasonalised return r̃_t = r_t / d̂_t. Use the deseasonalised series for *spot-vol* and jump detection; use raw RV for the daily aggregate (deseasonalising does not change the daily sum, it changes what "a big move" means intraday).
3. **Overnight.** Estimate NIFTY's active/inactive variance split yourself; then RV_total = ω₁ r²_ON + ω₂ RV_OC with Hansen–Lunde MSE-optimal ω. Report the estimated split — it is a publishable number.
4. **The comparison, done right.** The remaining implied variance at minute t is σ_imp(t)² · τ(t) with **τ in calendar years to the 15:30 settlement**, because the option prices calendar time including weekends. Remaining realised variance is Σ_{s>t} r̃_s² over the surviving minutes **plus every overnight to expiry**, weighted per step 3. Mismatch these two clocks and the whole study is noise.
5. **Weight by dollar gamma, not equally.** This is the step that makes it a trade rather than a statistic. The delta-hedged short-option P&L is ½∫Γ_s S_s² (σ_imp² − σ_s²) ds — a **dollar-gamma-weighted** average of the variance gap, which is exactly Sepp's E[P&L] = (σ_imp² − σ_real²)(½ Γ S₀²)T (A5). A variance risk premium that lives in the low-gamma part of the option's life is not tradeable. Compute both the plain VRP and the dollar-gamma-weighted VRP and report the difference; if they disagree, the plain one is a mirage.
6. **Decompose and stress it.** RV = BPV + JV via `BNSjumpTest`, and locate the jump minutes with `intradayJumpTest`. Then re-run the whole thing excluding jump days. **Compare implied to RV including jumps** (that is what the hedged P&L actually eats), but report the BPV-only version alongside — the gap between the two tells him whether he is harvesting a variance premium or writing crash insurance, and that distinction is the entire content of section (C).

---

## (C) POSITION SIZING AND RISK OF RUIN

### C1. Sinclair & Brooks, *The Skewness and Kurtosis of European Options and the Implications for Trade Sizing* (SSRN 2956161, 2017)
**URL:** `https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2956161` — free download, 13 pages, 2,069 downloads.

**What it gives him:** exactly the paper the task was pointing at. Closed-form skewness and kurtosis of European call and put *returns* (not of the underlying), then a power-series expansion giving a **simple approximation to the Kelly fraction under non-normal returns**, then the demonstration that the higher moments have an "economically significant" effect on optimal size. The point being: a short option's return distribution is so skewed and so kurtotic that a mean-variance Kelly fraction (f* ≈ μ/σ²) computed from a backtest is not merely imprecise — it is the wrong functional, and it is wrong in the direction of oversizing.

**Tests passed:** (3) — Sinclair traded options at Bluefin for two decades and says so on the paper; (4) counts double — the entire premise is that the standard tool fails in a specific, named way on this specific instrument class; (5) reproducible, it is closed-form.
**Honest caveat:** SSRN returns 403 to non-browser clients, so **I read the abstract, author affiliation and metadata but did not open the 13-page PDF and I am not going to reproduce a formula I did not see.** He should download it directly — it is free and short. Also note the paper is about a *single* option's return moments; a portfolio of correlated short options across strikes and expiries needs the multivariate version, which the paper does not give.

Related and also free: **Sinclair, *Confidence Intervals for the Kelly Criterion*** (SSRN 2457368) — the estimation-error side, which is arguably more important than the moment correction.

### C2. Busseti, Ryu & Boyd, *Risk-Constrained Kelly Gambling* (J. Investing 25(3):118–134, 2016)
**Free PDF:** `https://stanford.edu/~boyd/papers/pdf/kelly.pdf` · **arXiv:** `https://arxiv.org/abs/1603.06183` · **Code:** `https://github.com/cvxgrp/kelly_code` (two notebooks: `finite_outcome.ipynb`, `infinite_outcome.ipynb`)

**What it gives him — the single most implementable thing in this whole section.** Instead of ad-hoc fractional Kelly, impose the drawdown constraint directly:

maximise E log(rᵀb) s.t. 1ᵀb = 1, b ≥ 0, **E(rᵀb)^{−λ} ≤ 1**, with **λ = log β / log α**

where α is the drawdown level and β the tolerated probability. This is a **convex** problem (log-sum-exp composition) and its entire CVXPY specification is six lines, given verbatim in the paper's Appendix B and runnable in the repo.

The properties that make it better than fractional Kelly:
- The constraint bounds the **entire CDF** of minimum wealth: P(W_min < α) ≤ α^λ for *all* α, not just the one you specified. Their example: α=0.7, β=0.1 → λ=6.46 → the probability of ever losing half your capital is bounded by 0.5^6.46 = **1.1%**.
- λ = 0 recovers unconstrained Kelly exactly; λ can be used directly as a risk-aversion dial.
- Simulations show it **dominates fractional Kelly** — higher growth at the same drawdown risk, or lower drawdown risk at the same growth.
- Its quadratic approximation reduces to Markowitz, which tells you exactly what mean-variance is throwing away.

**Tests passed:** (1) runnable CVXPY code with worked notebooks, (5) reproducible on any empirical return sample, (4) counts double — the paper is explicit that the constraint is a *restriction* (the feasible set is strictly smaller than the true drawdown-constrained set), i.e. it is deliberately conservative and it tells you so, and it validates the bound against Monte Carlo rather than asserting it.
**Honest caveat, and it is the caveat for all of (C):** the method takes the return distribution as **given**. Feed it the empirical distribution of your backtested short-gamma trades and it will hand you a confidently oversized position, because the empirical distribution does not contain the loss that has not happened yet. See C4.

### C3. Thorp, *The Kelly Criterion in Blackjack, Sports Betting, and the Stock Market*
**Free PDF (verified):** `https://gwern.net/doc/statistics/decision/2006-thorp.pdf` (also mirrored from edwardothorp.com)

**What it gives him:** the practitioner formulas — growth rate as a function of the betting fraction, the "when will Kelly dominate" time-horizon results (which are far longer than people assume), the drawdown properties of full Kelly, and why practitioners bet fractions below f*. Thorp's Wall Street section is a first-person account of running the criterion on real capital over thirty years.

**Tests passed:** (3) — Thorp ran Princeton/Newport Partners; the paper describes actual deployment, (4) counts double — the "when will Kelly dominate" section is the paper telling you when its own recommendation is useless over your horizon, and it explicitly notes Kelly fractions are reduced in practice for higher-variance payoffs, (5).
**Honest caveat:** the securities-market application assumes a known edge and a known distribution. Thorp had a *measurable* edge (card counting, statistical arbitrage) with a huge sample. A short-gamma option book has neither.

### C4. Why full Kelly is wrong for options — the argument he should be able to state, sourced

1. **Kelly is optimal for the distribution you feed it, and your backtest sample does not contain your loss distribution.** A short-gamma book's P&L is a series of small positive numbers punctuated by a large negative one. If the sample contains zero or one tail events, the estimated μ is biased up, the estimated σ² is biased down, and f* = μ/σ² is biased up **multiplicatively in both terms**. This is not a small error; it is the dominant error.
2. **The moment correction points the same way.** Sinclair & Brooks (C1): the third and fourth moments of an option's own return distribution shift f* materially, and for short options they shift it **down**.
3. **Kelly's own bad properties.** Full Kelly's expected maximum drawdown is unbounded in the limit and the time to dominance is long enough (Thorp, C3) that a solo trader will be stopped out — by his own nerve or his broker — long before the asymptotics arrive.
4. **The right fix is not "use half-Kelly" — it is C2.** Fractional Kelly is an ad hoc knob; risk-constrained Kelly makes the drawdown tolerance the *primitive* and derives the fraction. Busseti et al. show it dominates fractional Kelly on both axes.

### C5. Margin expansion as a sizing constraint — primary Indian documents
This is the part that has nothing to do with the maths and will kill him first.

- **SEBI/HO/MRD/TPD/P/CIR/2024/132, 1 Oct 2024** (verified, URL in A8). Four measures that are *directly* sizing constraints, not compliance trivia:
  - **+2% ELM on all short options on expiry day** (from 20 Nov 2024). Your margin rises on the day your gamma is largest, and the circular's stated reason is expiry basis risk.
  - **Removal of calendar-spread margin benefit on expiry day.** If he is short the near and long the far, his margin does not net on expiry day. A position that is margin-efficient for six days becomes margin-expensive on the seventh, by rule, predictably.
  - **Intraday monitoring of position limits** (random snapshots), so breaches are caught mid-session rather than at EOD.
  - **₹15 lakh minimum contract size** — which sets the granularity floor on any Kelly fraction. Below a certain account size the optimal fraction is not attainable and the *quantisation* is the binding constraint, not the maths.
- **NSE Clearing SPAN risk parameter files** — `https://www.nseindia.com/static/products-services/equity-derivatives-span-risk-parameter-files` and `https://www.nseclearing.in/risk-management/equity-derivatives/span-risk-parameters`. The operative fact: **risk parameters are revised six times a day** — on prices/yields at 11:00, 12:30, 14:00, 15:30, 17:00, EOD and BOD. Your margin requirement can be raised **four times during the session you are losing money in**. That is the mechanism of margin expansion during stress, and it is documented, scheduled, and public.
- **NSE Clearing FAQ on Risk Management** — `https://www.nseclearing.in/sites/default/files/2025-01/NCL%20-%20FAQ%20RISK%20MANAGEMENT.pdf`

**Tests passed:** these are regulator and exchange primary documents — (2) they *are* the cost/constraint specification, (5) obtainable.
**Honest negative, important:** **NSE does not publish a documented, bulk-downloadable historical archive of SPAN risk parameter files.** The files are distributed via the member CORE portal after login. So he **cannot** backtest historical margin expansion from primary files without member access. The workaround is to reconstruct margin from the published SPAN methodology (scan range as a multiple of the volatility estimate subject to an index floor, plus short-option minimum charge, plus ELM, plus the expiry-day add-on) and validate it against a handful of current-day files. I looked for a public historical archive and did not find one; I am reporting that as a gap rather than pretending otherwise.

### C6. The one-line rule

> **Size every short-gamma position so that a single overnight gap of the worst magnitude you can *imagine* — not the worst in your sample — combined with a SPAN scan-range widening and the expiry-day ELM add-on, still leaves you funded; then take the risk-constrained-Kelly fraction for your stated drawdown tolerance (λ = log β / log α) and halve it, because your edge is estimated with far more error than your loss.**

Unpacked into the four things it is doing, each traceable to a source above:
- *worst you can imagine, not worst in sample* — the C4 argument; the backtest never sampled the loss.
- *SPAN widening + expiry ELM* — C5; the constraint that binds is liquidity, not P&L, and it binds intraday on a published six-times-a-day schedule.
- *λ = log β / log α* — Busseti–Ryu–Boyd (C2); makes the drawdown tolerance the primitive rather than a fudge factor, and is six lines of CVXPY.
- *then halve it* — Sinclair & Brooks' moment correction (C1) plus Sinclair's own confidence-intervals-on-Kelly paper; the halving is not superstition, it is a crude stand-in for the estimation variance of f*, and he should replace it with the actual confidence interval once he has read that paper.

---

## PAID — worth considering later (no free equivalent)

- **Euan Sinclair, *Positional Option Trading* (Wiley, 2020)** — the trade-sizing chapter is the book-length version of C1, and the only sustained practitioner treatment of sizing an option book that I know of. IIT-KGP library likely has it.
- **Aït-Sahalia & Jacod, *High-Frequency Financial Econometrics* (Princeton, 2014)** — the reference text behind everything in (B). Library, not purchase.
- **Whalley & Wilmott (1997), *Mathematical Finance* 7(3):307–324** — paywalled; reachable through his institutional access. Only needed if he wants the derivation rather than the formula.
- **Zakamouline (2006), *Quantitative Finance* 6(5)** — the published version of A1 with the final fitted constants. The free 2005 WP plus the code in A2 give him everything except the exact published constants.

## Could not verify — flagged, not glossed

- **Finance Act 2026 STT rates** (reportedly futures 0.05%, options 0.15% of premium, w.e.f. 1 Apr 2026). Multiple secondary sources agree; `incometaxindia.gov.in` returns 403 to programmatic requests and I did not reach the Act text or a CBDT notification. **This roughly doubles λ and widens his hedging band ~29%.** Confirm from an actual contract note before calibrating.
- **Stamp duty on derivatives (0.002% buy side)** — used in the λ table, not primary-verified.
- **Whether NSE transaction charges are still ₹1.73 / ₹35.03 per lakh in August 2026.** The circular I read and verified is dated 27 Sep 2024. There may be a later revision; check the NSE circular archive before using the number.
- **Hodges & Neuberger (1989)** and **Davis, Panas & Zariphopoulou (1993)** originals — not reached; Zakamouline's free WP is used as a faithful restatement and labelled as such.
- **Sinclair & Brooks PDF body** — abstract and metadata read, full text not opened (SSRN 403). No formula from it is reproduced above.
- **Public historical archive of NSE SPAN risk parameter files** — searched, not found; likely member-login only.