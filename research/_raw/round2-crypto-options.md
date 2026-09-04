## What I verified myself (primary, reproducible — run these, don't cite me)

Every number below came from live public endpoints on 2026-08-28 ~15:30 UTC. All are unauthenticated and free. Re-run them; they are the backbone of everything that follows.

| Probe | Endpoint | Result |
|---|---|---|
| BTC option ladder | `public/get_instruments?currency=BTC&kind=option` | 1,014 instruments, 13 expiries |
| OI concentration | `public/get_book_summary_by_currency` | 25SEP26 + 25DEC26 = **68.7% of BTC OI**; 40.0%/29.1% for ETH |
| Strike spacing | derived | matches published policy exactly (below) |
| Skew term structure | derived from `mark_iv` | **sign flips with tenor** (below) |
| Put-call parity vs listed future | derived | closes to **±0.04%** (below) |
| DVOL futures | `get_instruments?currency=USDC` | **one contract, OI 8.1, 24h volume $160** |
| Deribit free trade history | `get_last_trades_by_currency_and_time` | **zero for any historical date** |

---

## 1. Deribit market structure

### Deribit API reference (`docs.deribit.com`) + live JSON-RPC
**https://docs.deribit.com/** · **https://www.deribit.com/api/v2/public/get_instruments?currency=BTC&kind=option**

The authoritative object. `get_instruments` returns, per contract: `tick_size` 0.0001 BTC with `tick_size_steps: [{above_price: 0.005, tick_size: 0.0005}]`, `min_trade_amount` 0.1, `contract_size` 1.0, `maker_commission`/`taker_commission` 0.0003, `block_trade_min_trade_amount` **25 BTC**, `block_trade_commission` 0.0003, `settlement_period` day/week/month, `instrument_type: "reversed"`. Naming is `BTC-29AUG26-70000-C` — day-month-year with no zero padding, so your parser needs `%d%b%y` and must tolerate both `4SEP26` and `29AUG26`.

Tests passed: (1) runnable, (5) reproducible. Caveat: the docs index page is nearly contentless — go to `docs.deribit.com/llms.txt` for the real page list, or skip docs and introspect the live API, which is what I did.

### Contract Introduction Policy — the published expiry and strike ladder
**https://support.deribit.com/hc/en-us/articles/25944688876957-Contract-Introduction-Policy**

The exchange's own listing rules. BTC options: 4 dailies, 3 weeklies, 3 monthlies, 4 quarterlies. Strike intervals by bracket:

| TTE | ATM | Outer | Wings |
|---|---|---|---|
| ≤ 4 days | $500 | $500 | $1,000 |
| 1 week / 1 month | $1,000 | $2,000 | $5,000 |
| 3 months | $2,000 | $5,000 | $10,000 |

ETH: $20/$50/$100 → $100/$200/$500. Strikes are listed to cover **0.1–0.9 delta**, and "ATM" means 40–60 delta, "wings" <20 delta.

My measured ladder confirms it exactly — 29AUG26 shows spacings `{500: 14, 1000: 12}`, 25SEP26 shows `{1000: 20, 5000: 19, 2000: 16, 20000: 6}`. **This is the single biggest structural difference from NIFTY**: Deribit strike spacing is a step function of tenor and moneyness, not a constant. Your surface fitter cannot assume a uniform grid, and the far expiries carry strikes to $320,000 against a $79k spot — a 4× call. NIFTY gives you a dense uniform ladder over a narrow band; Deribit gives you a sparse non-uniform ladder over an enormous band.

Also buried here and materially new: *"when an option expires in the money, it is first physically settled into the corresponding futures contract at the strike price, which then cash settles… live for all linear options from early April 2026."*

Tests passed: (5), and (4) in the weak sense that it states its own discretion to deviate. Caveat: it explicitly says the tables are "a guide only" and Deribit may alter intervals; treat the API as truth, the policy as intent.

### Index Prices + Settlement (the 30-minute TWAP)
**https://support.deribit.com/hc/en-us/articles/25944739377309-Index-Prices** · **https://support.deribit.com/hc/en-us/articles/29734325712413-Settlement**

Index is a **capped-median**, not a plain median: each constituent is clamped to ±0.5% of the initial median, then a weighted average of the clamped values is taken. Circuit breaker halts derivatives if the index moves >10% between 1-second ticks; a constituent that fails to update for 3 minutes is dropped; with only two sources live the max allowed spread is 2.5%. BTC/USD and ETH/USD "typically have five or more constituents."

Settlement: delivery price = **30-minute TWAP of the index, 07:30–08:00 UTC, sampled every 4 seconds** (450 samples). Options are European, cash-settled, auto-exercised.

The part that actually changes behaviour: **delta of expiring options decays linearly to zero over the last 30 minutes**, and the risk matrix underlying converges to the Estimated Delivery Price, so *"a -10% scenario 15 min into expiry will actually use the underlying value if the index were to move -5%."* If you pin-risk trade, your reported delta from the API goes to ~0 on a deep ITM call near 08:00. That is a deliberate exchange convention, not a bug, and it will silently break a naive hedger.

Tests passed: (5), (4) — the index article enumerates its own manipulation attack surface and the mitigations. Caveat: the page opens with *"These are for educational purposes only, the below are not official Deribit policies."* The exchange is disclaiming its own methodology document, which is worth knowing before you build settlement logic on it.

### Portfolio Margin Engine — PME model deck
**https://statics.deribit.com/files/DeribitPortfolioMarginModel.pdf**

A real 10-page spec with formulas, not marketing. Maximum price move ±15% for BTC/ETH; max IV shock = `Volatility Range% × (30/days_to_expiry)^VegaPower` with **Vol Range Up 45%, Vol Range Down 30%**, and Vega Power switching between Short Term and Long Term at the 30-day boundary. Contingency: 0.01 BTC per net short option per strike, 0.6% of underlying value on gross futures. The ATM Range Adjustment (10% band) and the roll-up/roll-down pairing algorithm are worked through with a full numeric example on p.7.

Tests passed: (5), and (4) partially — it names the trap explicitly: *"it is possible for a portfolio made up solely of long options to be liquidated"* under PM, and recommends a standard-margin subaccount for long-only books.

**Honest caveat, and it is a big one: this deck is dated Jan 2022 and is superseded.** The current model is described at https://support.deribit.com/hc/en-us/articles/25944756247837-Portfolio-Margin and https://insights.deribit.com/exchange-updates/introducing-changes-to-deribit-portfolio-margin-model/ — option and futures contingency have been **removed**, replaced by Delta Shock and Roll Shock, and an Extended Table now runs −66% to +500% (vol-up only, fractional P&L, with a dampener). Main table is 9 buckets across a ±16% Price Range. Maintenance Margin Factor default 0.80. **I could not obtain current numeric values** for Vol Range Up/Down, Short/Long Term Vega Power, Delta Total Liquidity Shock Threshold, or Max Delta Shock — Deribit exposes them on the logged-in margin page and via `private/pme/simulate`, not publicly. `Segregated_Portfolio_Margin_Guidev1.pdf` is linked from the Insights post but returns 403. Use the old deck for *structure*, and pull live parameters from your own account.

### Block RFQ
**https://docs.deribit.com/articles/block-rfq-api-walkthrough.md**

Minimum block size is in the instrument object, not the article: **25 BTC** notional for BTC options (`block_trade_min_trade_amount`), block fee 0.03% flat with no maker/taker distinction. Mechanics: taker creates an RFQ with per-leg specs and optionally names makers; makers quote **each leg individually** (unlike combos, which price as one unit); there is a **5-second grace period during which the taker cannot see quotes or trade**; `disclosed` mode reveals aliases both ways. Requires `block_rfq:read_write` scope and account enablement.

Tests passed: (1), (5). Caveat: 25 BTC ≈ $2M notional. This channel is structurally closed to you, and you should model it as the reason the lit book looks the way it does — the institutional flow is not in the order book you are fitting. Round one's mention of Paradigm is now largely historical: Deribit has built the RFQ in-house as Block RFQ, and Deribit was acquired by Coinbase (completed 14 Aug 2025, https://www.coinbase.com/blog/deribit-joins-coinbase-unlocking-the-future-of-global-crypto-derivatives).

### Fees — and the fee cap that dominates short-dated crypto options
**https://support.deribit.com/hc/en-us/articles/25944746248989-Fees**

Standard tier options: **3 bps of underlying notional, capped at 12.5% of premium**, maker = taker. Block 3 bps. Option combos with at least one buy and one sell leg get the cheaper direction's fees zeroed — straddles and strangles do **not** qualify (all legs same direction).

I worked the cap through at spot $79,398:

| Premium | as % spot | Fee (one way) | % of premium | Round trip | Binding |
|---|---|---|---|---|---|
| $100 | 0.13% | $12.50 | 12.50% | **25.0%** | cap |
| $190 | 0.24% | $23.75 | 12.50% | **25.0%** | cap |
| $437 | 0.55% | $23.82 | 5.45% | 10.9% | notional |
| $1,826 | 2.30% | $23.82 | 1.30% | 2.6% | notional |
| $7,275 | 9.16% | $23.82 | 0.33% | 0.7% | notional |

The cap binds below premium = 0.0003/0.125 = **0.24% of spot**. Below that you pay a flat 12.5% each way — 25% round trip. Above it you pay a fixed $23.82 per BTC regardless of the option's value.

**This is the single most important number for a crypto vol trader and it has no NIFTY analogue.** NSE charges on premium; Deribit charges on notional. Every OTM wing and every short-dated option on Deribit carries a fee that is enormous relative to its premium. Any strategy that trades cheap options frequently — gamma scalping the dailies, wing-buying, ratio structures — is dead on arrival at retail fee tier.

Tests passed: (2) explicitly and quantitatively, (5). Caveat: tiers move fast and VIP1 needs $100k USDC equity; assume standard tier.

### My measurement: the tick size is the hidden tax
Deribit's inverse-option tick is a fixed **BTC** amount, so its USD value scales with spot, and the `tick_size_steps` jump at 0.005 BTC means an option priced just above that has a tick of 0.0005 BTC ≈ **$40**.

| Expiry | n (2-sided) | median tick as % of premium | median quoted spread % | median ticks wide | median premium |
|---|---|---|---|---|---|
| 29AUG26 | 41 | 2.41% | **16.87%** | 10.0 | $1,648 |
| 30AUG26 | 48 | 2.80% | **16.58%** | 6.0 | $1,241 |
| 1SEP26 | 54 | 2.86% | 11.46% | 4.0 | $1,092 |
| 4SEP26 | 61 | 2.08% | 6.67% | 4.0 | $1,866 |
| 25SEP26 | 112 | 0.66% | 3.18% | 4.5 | $6,044 |
| 25JUN27 | 100 | 0.33% | 2.06% | 6.0 | $12,148 |

Across all two-sided BTC options with premium < $500 (n=194): **median tick = 9.09% of premium, median quoted spread = 24.00%.**

Combine with the fee table: on a sub-$200 option you pay 25% round-trip in fees *plus* cross a ~24% spread. Your edge must exceed roughly 50% of premium. **Conclusion: the Deribit wings and dailies are untradeable at retail size, and this is a fee-and-tick fact, not a liquidity opinion.** Concentrate on 25SEP26/25DEC26 where OI is 69% of the book and spreads are 2–3%.

---

## 2. The crypto vol surface

### My measurement: live 25-delta skew term structure, both coins

Computed from `mark_iv` with a Black-Scholes delta at each strike, spot $79,207 (BTC) / $2,505 (ETH):

| Expiry | days | BTC ATM | BTC RR25 (C−P) | BTC BF25 | ETH ATM | ETH RR25 |
|---|---|---|---|---|---|---|
| 29AUG26 | 0.7 | 33.1 | **+1.14** | +0.86 | 40.0 | **+2.82** |
| 4SEP26 | 6.7 | 36.8 | **+2.44** | +0.76 | 45.8 | **+3.66** |
| 25SEP26 | 27.7 | 37.5 | +0.26 | +1.05 | 50.0 | +1.11 |
| 30OCT26 | 62.7 | 37.5 | +0.06 | +1.17 | 51.9 | +0.99 |
| 27NOV26 | 90.7 | 39.4 | **−0.28** | +0.78 | 52.9 | +0.48 |
| 25DEC26 | 118.7 | 40.3 | **−0.38** | +0.75 | 53.6 | −0.27 |
| 25JUN27 | 300.7 | 42.5 | **−0.85** | +1.35 | 56.0 | +0.27 |

Two things an equity-index trader would not predict, both directly observable:

1. **The skew sign flips with tenor.** Short-dated BTC risk reversals are *positive* — calls bid over puts by 1–2.4 vol points — and go negative only beyond ~90 days. ETH is call-skewed essentially the whole curve. In SPX the risk reversal is negative at every tenor and steepens with maturity; here it is positive at the front and mildly negative at the back. Any model you port from equities with a hard-coded negative ρ will fight the front of this surface.
2. **Term structure is in steep contango** (33 → 42.5 for BTC) while the front is call-skewed. That combination — cheap near vol, call-skewed, upward-sloping — is the crypto signature.

Butterflies are uniformly positive and remarkably stable at +0.7 to +1.4 across the whole curve for both coins, which is the one thing that *does* look like equities.

Tests passed: (5) — you can reproduce this in ~30 lines. Caveat: I used Deribit's `mark_iv` (their model), and my delta is a Black-Scholes delta computed off the index rather than the expiry forward, so the 25-delta strikes are approximate — good enough for sign and shape, not for a quoting engine. Redo with the forward from §5.

### Echenim, Gobet & Maurice — "Unbiasing and robustifying implied volatility calibration in a cryptocurrency market with large bid-ask spreads and missing quotes" (Kaiko)
**https://marketing.kaiko.com/hubfs/Factsheets/KAIKO_IVSmile_Methodology.pdf**

**This is the single best answer to "does SVI calibrate here, and what broke."** Free full PDF, CNRS/École Polytechnique authors with Kaiko's quant data lead, using real Deribit BTC data.

What it concretely gives you:
- A **theorem** (their Thm 3.1) that calibrating SVI on mid-prices produces a *systematic underestimation* of implied vol in the wings. Not a heuristic — a proof, with the direction of the bias.
- The reason: *"the relative tick size (and thus the relative spread) for options on cryptos is roughly 10 to 50 times larger than for options on traditional markets."* My own measurement above independently confirms this — 9% of premium in the wings.
- An **"anchor price"** built from bid and ask whose bias is third-order in the tick size, replacing the mid.
- A **Beta-distribution data-augmentation** procedure for one-sided and missing quotes, which is the exact failure you will hit on Deribit wings.
- Hard liquidity counts: over 27 Jun–3 Jul 2022, **~30 BTC option trades per hour across all strikes** for 1-week and 1-month expiries, **~5/hour** for 3- and 6-month, **1–2/hour** for 9-month and 1-year. That is the whole market.
- Measured improvement: calibration error down 25–30%.
- They filter to OTM only, because ITM implied vol is far more spread-sensitive.

Tests passed: (2) — spreads and tick size are the entire subject; (4) **double** — the paper *is* an enumeration of where naive SVI breaks on crypto; (5). Caveat: no code is released, and the data is Kaiko's (paid). You must implement the anchor price and the augmentation yourself, and the 2022 sample predates the current liquidity regime — re-measure the trade counts before believing them.

### Magadini, Sinclair & Chepal — real-time SVI calibration in crypto
**https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4899357** (free PDF, 28pp, Jul 2024)

Euan Sinclair (Bluefin Trading, author of *Volatility Trading*) and Gregoire Magadini (Genesis Volatility → Amberdata) — two people who have run crypto option books and built the surface infrastructure commercially. Covers SLSQP optimisation, rough-then-refine calibration, and liquidity-adjusted pricing for the low-liquidity regime.

Tests passed: (3) — both authors demonstrably built and traded this; (4) — the paper is framed around instability and low liquidity as the failure mode; (5). Caveat: the calibration process is repeatedly described as **"proprietary."** You get the architecture and the problem framing, not the reproducible recipe. Read it alongside the Kaiko paper, which gives you the maths the Sinclair paper withholds. Pair them and you have a working method.

### Alexander & Imeraj — "Delta hedging bitcoin options with a smile"
**https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4097909** (free preprint) · *Quantitative Finance* 23(5):799–817

Hourly Deribit option data, synthetic constant maturities of 10/20/30 days, comparing smile-implied and smile-adjusted deltas against Black-Scholes, reported as hedging-error variance ratios over two one-year periods.

Two findings you can act on:
- *"bitcoin implied volatility curves behave very differently from those of equity index options"* — consistent with my measured positive front-end risk reversals.
- **Hedge with the perpetual, not the calendar future**, because perp basis risk is far smaller. Efficiency gains **>30% for OTM puts** and ~15% for short-term OTM calls *during periods when the IV curve slopes upwards* — i.e. exactly the call-skewed regime I measured.

Tests passed: (3) — Alexander has run and advised crypto derivatives desks; (5) — Deribit data, obtainable; (4) — results are explicitly regime-conditional and the paper says so. Caveat: it is a hedging-error-variance study with **no transaction cost model**, which given the fee table in §1 is a serious omission. The 30% variance reduction is a gross number; rehedging frequency at 3bps-of-notional will eat a chunk of it. Test that yourself before believing it.

### Lucic & Sepp — "Valuation and hedging of cryptocurrency inverse options"
**https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4606748** (free) · *Quantitative Finance* 24(7):851–869 · code: **https://github.com/ArturSepp/StochVolModels** (234★, actively pushed Aug 2026, MIT)

The inverse-option payoff is genuinely different maths, not a cosmetic quirk — the option is quoted and settled in the numéraire whose price you are optioning. Deribit's own docs confirm the mechanics (below), and this paper does the joint vanilla/inverse valuation properly, with **backtest simulations on Deribit data**. Sepp's broader log-normal SV programme is specifically motivated by *positive* return-volatility correlation, which is exactly the crypto skew sign I measured at the front of the curve — the one place where a ported equity model fails structurally.

Tests passed: (1) runnable and maintained, (3) — Sepp has been a practising crypto/vol quant at LGT and Sygnum, (5). Caveat: `StochVolModels` is a *pricing analytics* library, not a trading system — no fees, no execution, no data plumbing. It gives you a correct inverse-option pricer and calibrator; everything else is on you.

### Deribit's own inverse-option specification and Black-Scholes convention
**https://support.deribit.com/hc/en-us/articles/31424939096093-Inverse-Options**

Read this before you fit anything. The exchange publishes its exact formulas: `C = X·N(d1) − K·N(d2)·e^(−RT)`, with **X = index**, **F = forward**, and the interest rate *defined* as `R = ln(F/X)/T`. Crucially: *"The implied volatility displayed uses the forward, rather than the index, as the underlying price."* Get this wrong and your IVs will disagree with the screen by a spread-sized amount, and you will spend a week chasing it.

**On the weekend effect** — this article answers it definitively and it is not what folklore says: *"The full amount of time is included in the calculations,"* with the worked example `(1 + 17/24)/365`. Deribit uses **pure calendar time, no business-day or weekend weighting whatsoever.** So the weekend "effect" is not a modelling artefact you must undo — it is a genuine, tradeable dip in quoted IV going into Friday, because the exchange charges the trader for calendar theta the market knows will not be delivered. Whether that dip is *exploitable* net of the 25%-of-premium round-trip on short-dated options in §1 is precisely the question, and I found nobody who has published the answer with costs.

Also here: **options are limit-order-only — market orders are not accepted by the matching engine.** And the allowed trading bandwidth is derived from the portfolio-margin risk matrix plus a constant of 0.015, with orders outside it silently adjusted rather than rejected.

Tests passed: (5), (2) — mistrade rules, adjustment windows and the 2-hour claim deadline are all stated. Caveat: it is exchange documentation, so it describes intent; the mistrade section makes clear that "theoretical price" is ultimately settled by consulting primary market makers, which is a discretionary backstop you cannot model.

### Honest negative on events
I could **not** find a credible, cost-aware empirical study of the BTC/ETH surface around scheduled events — ETF decisions, halvings, CPI/FOMC. What exists is vendor commentary (Block Scholes, Amberdata, Glassnode) with no reproducible methodology and, in Block Scholes' case, co-branding with Bybit, which trips the broker-affiliation filter. The specific claim that DVOL fell 63→43 between Nov and Dec 2025 recurs across secondary sources; I could not trace it to a primary measurement, though you can now verify it yourself in one call (§3). **This is a genuine gap — event-vol in crypto options is essentially unpublished with costs, and it is a strong candidate for original work** given you have the data access.

---

## 3. DVOL

### Methodology
**https://insights.deribit.com/exchange-updates/dvol-deribit-implied-volatility-index/**

Full construction, and it differs from VIX in ways that matter:
- Picks the two expiries bracketing 30 days, **ignoring any instrument listed less than 1 hour ago** (so spreads can normalise).
- Price per instrument is a **depth-VWAP**, not a mid: walk 5 levels or 2 BTC cumulative, take `(DepthAsk + DepthBid)/2`. Fallback chain if the spread is too wide: last-minute trade VWAP → mark price from 60–90s ago.
- **Discards ITM options and anything under 5 delta** — explicitly to avoid strikes where tick size swamps vega, which is the same pathology I measured in §1.
- Forward from the call/put synthetic; strike cutoff at the strike nearest forward.
- Variance-swap integral, interpolate the two expiries, then **EMA over the last 240 one-second points**.

**What it does not measure:** it is not a pure 30-day variance swap rate. The 5-delta truncation means it systematically **understates** the true variance swap strike (it throws away the tails that a variance swap pays on) — the same direction of error as the Kaiko mid-price bias, and for a related reason. The 240-point EMA also means DVOL *lags* by construction; it is unsuitable as a realtime signal for anything faster than a few minutes. And the depth-VWAP construction means DVOL moves when *liquidity* changes, not only when vol changes.

Tests passed: (5) — fully reproducible; (4) — it names the delta truncation and the reason for it. Caveat: Deribit calls this a "whitepaper" but there is no separate PDF with proofs; the article is the spec. Several construction details (exact interpolation weights, EMA seeding) are described in prose, not formulas.

### Is it tradeable? Measured answer: **no.**

`get_instruments?currency=USDC` across all kinds returns exactly **one** DVOL instrument: `BTCDVOL_USDC-30SEP26`. Live state:

```
bid 40.0 / ask 41.0        (a full vol point wide, 2.5%)
open_interest    8.1       (~$324 notional)
24h volume       4.0       (= $160)
last trade       one, 2026-08-28T08:36 UTC
```

Book beyond the touch: bids 42 @ 40, 50 @ 39, 49.9 @ 38 …; asks 20.2 @ 41, 25 @ 41.1, then a gap to 45, 50, 55 — and a 1-lot ask at **352**. There is no ETH DVOL future at all (though the ETH DVOL *index* is live and queryable).

The Contract Introduction Policy confirms this is by design: BTC DVOL has **"1 monthly"** listing, rolled a week before the prior one expires. So the entire crypto listed-vol complex is one monthly contract with three-figure daily turnover, three years after launch.

**Conclusion: DVOL is an excellent free measurement instrument and a non-existent trading instrument.** Treat it as a data series, never as a hedge. The SignalPlus piece (https://insights.deribit.com/industry/demystifying-dvol-futures/) explains correctly why replicating it with vanillas is hard — you need the variance replication *plus* a vol-of-vol convexity adjustment — but it was written at launch in 2023 and its optimism about calendar spreads and ETH/BTC DVOL relative value never materialised, because those instruments do not exist.

**The valuable part is the free index history.** `public/get_volatility_index_data` returns OHLC for BTC and ETH DVOL and I verified data returns for March of 2022, 2023, 2024, 2025 and 2026 — a multi-year, free, primary 30-day IV series at arbitrary resolution. That is your VRP measurement input (§4).

---

## 4. The crypto variance risk premium

### Almeida, Grith, Miftachov & Wang — "Risk Premia in the Bitcoin Market"
**https://arxiv.org/abs/2410.15195** (free, arXiv)

The most rigorous current measurement. Deribit options plus realized returns. Headline numbers:
- **BVRP averages 14% annualized** at the one-month horizon, versus **~2% for the S&P 500** (Bollerslev-Tauchen-Zhou).
- Bitcoin premium averages **66%/yr**; Martin-style lower bound 66%, Chabi-Yo/Loudis bound 84%.
- Sharpe ~0.8, roughly double SPX.
- The regime result is the useful one: clustering option-implied RNDs yields two volatility regimes, and **BVRP is high in the low-vol regime and lower in high-vol states** — i.e. the premium is *not* highest when vol is highest. They read this as investors being most concerned about variance and *upside* risk when things are calm, which fits the positive front-end call skew I measured.
- Return-premium decomposition: **large positive returns (+20% to +60%) account for 39% of the Bitcoin premium**, versus under a third of SPX's premium coming from positive returns at all. The right tail carries the information in crypto. This is the cleanest statement I found of why equity intuition inverts here.

Tests passed: (5) — Deribit data, method fully specified; (4) — the regime conditioning *is* the failure-mode statement, and they are explicit that the point estimate of the first-moment premium is noisy. Caveat: **no transaction costs anywhere in the paper**, and the sample ends before the 2025–26 regime. A 14% variance premium is comfortably inside the round-trip costs of §1 for short-dated options, so this is a statement about the risk-neutral/physical gap, not about a harvestable return. Do not read 14% as a strategy Sharpe.

### Is it still positive in 2026, and where has it decayed?
**I could not verify this from a primary source, and I want to be blunt about it.** Every 2026 claim I found — "BTC IV overstates RV by 10–15 vol points," "the premium has faded" — traces to vendor blogs or exchange-affiliated commentary with no published methodology. The Deribit "contango → VRP mean +15 points" figure circulates widely and I could not find its underlying calculation.

The structural fact I *can* verify is that the venue landscape shifted: Deribit's share of BTC options open interest reportedly fell below 39% in Jan 2026 (from >90% in 2020) after IBIT ETF options launched in Nov 2024. If true, that fragments the flow that historically generated the premium, and any Deribit-only VRP measurement after 2024 is measuring a shrinking slice. I could not confirm the 39% figure from a primary exchange or OCC source.

**What you should do instead of citing anyone:** DVOL history is free back to at least 2022 (§3), and minute-wise BTC spot is trivially obtainable. Compute `DVOL²` versus subsequent 30-day realized variance yourself, split by the Almeida et al. regime definition. That is a two-day project, it is genuinely original for 2026, and it settles the question with your own measurement rather than an assertion. This is the highest-value piece of unclaimed work in the entire brief.

---

## 5. Perp-vs-option basis and the option-implied funding relation

### My measurement: the triangle is closed

Put-call parity for inverse options is `C − P = (F − K)/F` in coin terms, so `F = K/(1 − (C−P))`. I computed the parity-implied forward from mid-quotes at the strike nearest spot, and compared it to the listed future's mark:

| Expiry | Strike | F implied | F future | diff $ | diff % |
|---|---|---|---|---|---|
| 29AUG26 | 79,000 | 79,194.03 | 79,183.36 | +10.67 | +0.0135% |
| 30AUG26 | 79,000 | 79,197.99 | 79,194.97 | +3.02 | +0.0038% |
| 4SEP26 | 79,000 | 79,277.47 | 79,253.65 | +23.82 | +0.0301% |
| 25SEP26 | 79,000 | 79,436.90 | 79,422.16 | +14.74 | +0.0186% |
| 27NOV26 | 79,000 | 80,142.02 | 80,111.69 | +30.33 | +0.0379% |
| 26MAR27 | 80,000 | 81,321.47 | 81,324.95 | −3.48 | −0.0043% |
| 25JUN27 | 80,000 | 82,346.89 | 82,334.72 | +12.17 | +0.0148% |

**Maximum deviation across the whole curve: 0.038%, or $30 on $79,000.** Now compare that to the frictions I measured on the same book: one option tick is $7.94–$40, the median ATM quoted spread on the front month is 6.67% of premium, and the fee is $23.82 per BTC per leg. A parity arb needs four legs. **The mispricing is an order of magnitude smaller than the cost of one leg.**

Tests passed: (5), (2) — I priced the costs against the same live book. Caveat: I used mid-quotes, so these are *indicative* forwards, not executable ones; the true executable deviation is smaller still, because you'd cross spreads on both options.

### The futures term structure is a clean, flat carry curve

| Expiry | days | basis | annualised |
|---|---|---|---|
| PERPETUAL | — | +0.021% | — |
| 4SEP26 | 6.7 | +0.095% | +5.29% |
| 25SEP26 | 27.7 | +0.307% | +4.13% |
| 27NOV26 | 90.7 | +1.178% | +4.83% |
| 25DEC26 | 118.7 | +1.554% | +4.86% |
| 26MAR27 | 209.7 | +2.711% | +4.77% |
| 25JUN27 | 300.7 | +3.986% | +4.86% |

Annualised basis is **flat at ~4.8%** from three months to ten months, with the front stub noisier. That is a term structure of USD funding, and it is remarkably well-behaved — which is exactly why the parity triangle closes. The perp sits at +0.021% to index, essentially flat.

**Conclusion on the triangle: not exploitable at retail size, and the reason is structural, not cyclical.** The three markets are on one venue, one margin engine, one index, with professional market makers arbitraging them continuously. What *is* usable is the inverse: the parity-implied forward is a free, accurate, per-expiry forward that you should use as the underlying in your IV calculations (as Deribit itself does), rather than the index. That materially changes your fitted skew.

### Alexander, Chen, Deng & Wang — "Arbitrage opportunities and efficiency tests in crypto derivatives"
*Journal of Financial Markets* 71 (2024) · **https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4495548** · ScienceDirect: https://www.sciencedirect.com/science/article/pii/S138641812400048X

The formal version of what I measured. Introduces a **fiat-currency-free put–call parity** appropriate to inverse contracts, and uses it to build arbitrage tests for options-only *and* option-versus-perpetual cross-markets — precisely your triangle. Findings: BTC and ETH derivative markets are becoming more efficient, especially for **maturities ≥ 15 days**; BTC more efficient than ETH; but they report strategies remaining profitable "even under conservative transaction cost scenarios."

Tests passed: (2) — transaction cost scenarios are central to the paper's claims; (5) — Deribit data; (3) — Alexander has direct industry involvement in crypto derivatives. Caveat and an important tension: **their conclusion is more optimistic than my live measurement.** Two likely reconciliations — their sample is older (efficiency has improved since), and academic "conservative transaction costs" rarely include the 12.5%-of-premium fee cap or the 9%-of-premium tick that bite hardest on the cheap options where deviations look largest. **Read their profitability claims as an upper bound and re-test on current data with the §1 cost model.** That re-test is itself a worthwhile piece of work.

An open-access version exists at https://sussex.figshare.com/articles/journal_contribution/Arbitrage_opportunities_and_efficiency_tests_in_crypto_options/25931488 but **it returned 403 to me and I could not confirm the PDF is downloadable** — worth trying from your IITKGP network.

---

## 6. Data and code

### Tardis.dev — the only realistic free deep history, and I tested it
**https://docs.tardis.dev/historical-data-details/deribit** · datasets: `https://datasets.tardis.dev/v1/deribit/options_chain/YYYY/MM/01/OPTIONS.csv.gz`

**I downloaded a real file with no API key**: `2026/06/01` returned HTTP 200 and **4,122,864,811 bytes gzipped** for a single day of the Deribit options chain. Verified schema:

```
exchange,symbol,timestamp,local_timestamp,type,strike_price,expiration,
open_interest,last_price,bid_price,bid_amount,bid_iv,ask_price,ask_amount,
ask_iv,mark_price,mark_iv,underlying_index,underlying_price,
delta,gamma,vega,theta,rho
```

Sample row includes `XRP_USDC-2JUN26-1D32-P` — so coverage extends past BTC/ETH to the newer linear alt options. Microsecond timestamps, **both exchange and local timestamps** (so you can measure feed latency), full greeks, both-side IVs and sizes, and open interest.

**The free tier is the first day of every month, no key required**, across all data types (incremental L2 book, snapshots, trades, quotes, book tickers, derivative tickers, liquidations). Deribit coverage starts **2019-03-30**. Book updates are collected raw with **sequence-number validation** against Deribit's feed.

Tests passed: (5) decisively — I obtained the data; (1) — `tardis-python` (146★, MPL-2.0, pushed 2026-08-23) and `tardis-node` are maintained clients; (2) indirectly, since local_timestamp lets you model fills honestly.

Caveats, and they are real: **4 GB compressed per day** means ~90 first-of-month days is a few hundred GB — plan storage before you start, and filter on ingest. The free days are *first-of-month only*, so you get monthly snapshots, not a continuous series: fine for surface cross-sections and calibration research, **useless for event studies or path-dependent backtests**. Continuous history is paid.

### Deribit's own public API as a historical source — mostly a dead end
Verified negatives, so you don't waste a week:
- `get_last_trades_by_currency_and_time` returned **0 trades** for 2023-03-01, 2024-03-01, 2025-03-01 and 2026-03-01. There is no deep free trade history by currency.
- `get_instruments?expired=true` returned **114 instruments, all expiring 2026-08-28** — i.e. only the most recent expiry. Expired instruments roll off, so you cannot enumerate historical contracts.
- `get_last_trades_by_instrument` on an expired instrument returned 0.
- **The exception:** `get_volatility_index_data` returned data for March 2022, 2023, 2024, 2025 and 2026 for both BTC and ETH. **DVOL history is free, multi-year, arbitrary resolution.**

Practical consequence: **if you want continuous Deribit options history, you must either pay, or start recording now.** Stand up a snapshot recorder today — `get_book_summary_by_currency` gives you the entire chain with mark IVs and OI in one call, which is what I used throughout. Cheap to run, and in six months you own something you cannot otherwise buy for free.

### Code — assessed, not README-skimmed

**ArturSepp/StochVolModels** — https://github.com/ArturSepp/StochVolModels · 234★, MIT, pushed 2026-08-28. The reference implementation behind the Lucic-Sepp inverse-options paper. Log-normal SV with quadratic drift, Heston, closed-form and Monte Carlo. **Recommended.** Caveat: pricing analytics only, no data layer or execution.

**ArturSepp/OptionChainAnalytics** — https://github.com/ArturSepp/OptionChainAnalytics · 2★. Point-in-time option-chain containers with a real `data/deribit.py`. I read the source: 339 lines, proper numpy-style docstrings, and the module docstring correctly states the hard parts — *"Deribit option prices are inverse: BTC contracts are quoted in BTC… implied volatilities are converted from provider percentages to decimals, and contract sizes remain 0.1 BTC or 1 ETH,"* and it reads spot from a Tardis perpetual archive. Someone who understands the conventions wrote this. **Honest caveat: 2 stars, and the repo contains `AGENTS.md` and `CLAUDE.md` — substantially AI-assisted.** The docstrings are better than the battle-testing. Read it as a well-organised reference for the Deribit normalisation gotchas; do not run it unexamined.

**Stale — do not build on these.** `dwasse/vol-surface-visualizer` (63★, last push **2022-12**, no licence, naive Black-Scholes off mid); `nostoz/deribit_volatility_download_and_visualize` (33★, **2023-10**, MIT, a 5-minute parquet snapshotter — the *idea* is right and worth copying, the code is three years cold); `alexanderkudryashov3/Crypto-Options` (17★, **2022-12**, notebooks, SABR not SVI, no licence).

**Honest negative on code:** I searched GitHub by both relevance and recency. Almost everything currently active in "Deribit + options + volatility" is zero-star, days-old, and AI-generated — `hemv-857/svi-scanner`, `znmahbub/SVCJ-Deribit-Inverse-Options-Pricer`, `dakshbtc/quantlab` and similar. **There is no maintained, credible, open-source crypto options analytics stack.** Nothing here is the hftbacktest of crypto options. Given you have already implemented SVI and SSVI, you are better served writing your own thin layer over `get_book_summary_by_currency` plus Sepp's pricers than adopting any of these.

---

## 7. Venue reality for an Indian resident

### Deribit: not restricted, not registered — and those are different things

**Primary, verified:** Deribit's Restricted Jurisdictions page (**https://support.deribit.com/hc/en-us/articles/25944487427741-Restricted-Jurisdictions**) lists Belarus, Canada, CAR, Congo, Cuba, Guam, Iran, Iraq, Japan, DPRK, Libya, Myanmar, Panama (retail spot only), Puerto Rico, Russia, American Samoa, Somalia, South Sudan, Sudan, Syria, sanctioned Ukraine regions, UAE (retail spot only), UK (no retail clients), US, USVI, Yemen. **India does not appear.** From Deribit's side, an Indian resident is not blocked.

**Primary, verified:** the FIU-IND enforcement action of 01 Oct 2025 (**https://www.pib.gov.in/PressReleasePage.aspx?PRID=2173758**, Ministry of Finance) named **25 offshore VDA SPs** issued Section 13 PMLA non-compliance notices *and* Section 79(3)(b) IT Act URL-takedown notices: Huione, BC.game, Paxful, Changelly, CEX.IO, LBank, Youhodler, BingX, PrimeXBT, BTCC, CoinEx, Remitano, Poloniex, **BitMEX**, Bitrue, LCX, ProBit, BTSE, HitBTC, LocalCoinSwap, AscendEX, Phemex, ZooMex, CoinCola, CoinW. **Deribit is not on that list.** The release states 50 VDA SPs have registered to date.

**What I could not verify, and you should not let anyone tell you otherwise:** FIU-IND **does not publish a machine-readable register of registered entities.** I fetched `VDA08012026.pdf`, `VDASP15092025.pdf` and `VDASP20012025.pdf` from fiuindia.gov.in — all are scanned images with no text layer. I rendered and read them: `VDA08012026` is the AML/CFT Guidelines updated 08.01.2026, and `VDASP15092025` is the registration *process* circular (in-person meeting with Designated Director and Principal Officer, incorporation docs, 3 years of MCA filings and GST returns). **None of them is a list of registrants.** The counts (28 → 47 → 49/50) come from PIB releases and Lok Sabha answers (e.g. Unstarred Q. No. 3418, 16 Dec 2024), not from a published register.

**So the honest position: Deribit is neither registered with FIU-IND nor currently sanctioned by it.** That is a live regulatory gap, not a clearance. Note the direction of travel: the Oct 2025 action shows FIU-IND enumerating offshore venues serving Indian users and issuing takedowns, and the release states the obligations *"are activity-based and are not contingent on physical presence of the entity in India."* Deribit is now Coinbase-owned, and Coinbase itself registered with FIU-IND and reopened Indian services in Dec 2025 — which makes Deribit's continued non-registration look more like a pending question than a settled one. **Treat access as revocable.** Do not build anything whose viability depends on Deribit remaining reachable from India, and get tax advice before trading it (30% flat on VDA gains, 1% TDS, no loss set-off).

### Delta Exchange India: I measured the book — round one's gap is now closed

**Registration, verified:** Delta Exchange India is operated by **Excelium Technologies Private Limited**, FIU-IND registered reporting entity, **REID VA00041101**. (Delta's own disclosure; note their Jan 2024 public statement said the application was merely "under processing" — registration came later.)

**Their API is reachable but `api.india.delta.exchange` resets the TLS handshake from outside India.** `https://cdn.india.deltaex.org/v2/...` serves the same v2 API and works. That is a practical detail worth knowing.

**Measured BTC options book (their own API, `/v2/tickers`, 621 BTC option instruments):**

| Expiry | nOpt | 2-sided | OI (USD) | 24h turnover (USD) | strikes | range |
|---|---|---|---|---|---|---|
| 290826 | 71 | **71** | 228,112,076 | 837,932,399 | 36 | 74,800–83,600 |
| 300826 | 58 | **58** | 39,958,672 | 95,793,894 | 29 | 76,800–83,600 |
| 040926 | 106 | **106** | 131,560,384 | 128,389,277 | 54 | 58,000–90,000 |
| 250926 | 89 | **89** | 45,527,621 | 13,800,693 | 46 | 48,000–93,000 |
| 301026 | 89 | **89** | 27,842,826 | 4,338,531 | 47 | 52,000–98,000 |
| 271126 | 65 | **65** | 0 | 0 | 33 | 66,000–98,000 |

**Total: $486M open interest, $1.10B 24h turnover, and every single listed strike is two-sided.** That last fact is the headline — Deribit had 41 of 54 two-sided on its front expiry; Delta has 100% coverage on all nine, which reflects enforced market-maker obligations.

**Depth, measured properly.** A two-sided quote is not depth, and a 5-level comparison is meaningless across venues with different ticks (Delta's tick is $0.01; Deribit's is $7.94–$40). So I measured **BTC notional resting within ±2% and ±5% of mid premium**, which is tick-independent:

| Contract | venue | mid $ | bid ±2% | ask ±2% | bid ±5% | ask ±5% |
|---|---|---|---|---|---|---|
| ~1-day ATM call | **Deribit** | 437 | **0.0** | **0.0** | **0.0** | **0.0** |
| ~1-day ATM call | **Delta** | 488 | 24.1 | 14.9 | 58.6 | 36.7 |
| ~1-week ATM call | Deribit | 1,826 | 0.0 | 0.0 | 49.4 | 51.6 |
| ~1-week ATM call | Delta | 1,838 | 18.8 | 12.2 | 40.3 | 23.4 |
| ~1-month ATM call | Deribit | 3,593 | 37.8 | 33.5 | 86.3 | 111.8 |
| ~1-month ATM call | Delta | 3,595 | 12.7 | 8.5 | 40.1 | 21.1 |

The zeros are not missing data. **On Deribit's daily expiry, one tick is already more than 2% of the premium, so nothing can rest inside a ±2% band.** Delta's finer tick means its short-dated book is genuinely tighter: measured spreads of **1.75–2.34%** on the 1-day ATM versus Deribit's **10.9–19.1%** on the same contracts.

**The honest reversal:** for short-dated BTC options, Delta Exchange India is *tighter and more accessible* than Deribit, because Deribit's fixed-BTC tick is punitive on cheap options. Deribit wins decisively at **one month and beyond** — 3–5× the resting notional and 130 strikes versus 46 — and wins overwhelmingly on tenor (out to Jun-2027 versus Delta's Nov-2026) and on strike range.

**Costs, primary (https://www.delta.exchange/fees):** options 0.03% of notional maker and taker (0.010% promotional), **capped at 10% of premium (3.5% promotional)**, **plus 18% GST on the fee**, plus a settlement fee on open contracts at expiry charged at taker rates. Structurally the same notional-based charge as Deribit with a slightly tighter cap — so the §1 analysis carries over: cheap options are punished on both venues.

**Contract specs (https://guides.delta.exchange/delta-exchange-india-user-guide/derivatives-guide/options-guide):** `C-BTC-50000-200821`, expiry **17:30 IST** (not 08:00 UTC — different settlement time from Deribit, which creates a genuine cross-venue calendar), 30-min TWAP settlement, lot = 0.001 BTC (so ~₹7,000 notional — far smaller than Deribit's 0.1 BTC minimum). Published strike differences: D1 $200, D2 $250, W1–W3 $1,000, M1 $1,000, M2 $2,000, M3 $5,000, with delta range 0.2–0.8 and minimum strike counts. Mark price is an impact-size book average **clamped to model IV ±25%** — a band you must respect, since it drives liquidations.

**No India price premium.** Measured simultaneously: Deribit `btc_usd` index 79,222.36 versus Delta India spot 79,217.1 — a **−0.007%** difference, and Delta's perp mark −0.037% to Deribit's index. The "India premium" folklore applies to INR-funded spot venues, not to Delta's USD-margined book. There is no cross-venue basis trade here.

Tests passed for Delta: (5) — every number above is from their public API; (2) — fees, GST and settlement fees are published. Caveats: their D1/D2 strike differences ($200/$250) do not match my measured near-expiry ladder, so the published spec is aspirational — trust the API. Their ticker `time` field read `2026-08-27T15:29Z` while turnover was clearly live, so **at least one timestamp field in their v2 tickers response is stale or mislabelled** — do not key anything off it without checking. And $486M OI is roughly 1/8th of Deribit's BTC book at comparable spot; the depth advantage is real but narrow and confined to the front.

---

## What nobody has published (your openings)

1. **Crypto VRP measured with a real cost model, 2024–2026.** Almeida et al. stop earlier and include no costs; everything after is vendor assertion. Free DVOL history plus your minute data settles it. Highest-value gap here.
2. **The weekend theta trade, costed.** Deribit uses pure calendar time by published convention; the Friday IV dip is real and observable. Whether it survives 25%-of-premium round-trip on short-dated options is unpublished.
3. **Event vol in crypto options with costs.** ETF decisions, halvings, FOMC. Nothing credible and reproducible exists.
4. **Re-testing Alexander et al.'s arbitrage profitability on 2026 data with the fee cap and tick modelled.** My live parity measurement (±0.04%) suggests their conclusion no longer holds. Worth demonstrating rather than asserting.
5. **Deribit vs Delta India as a genuine liquidity study.** I have given you the method and a single snapshot; nobody has published the time series, and you can record it.

## PAID — worth considering later

- **Tardis.dev continuous history** — https://tardis.dev/. The free first-of-month days are excellent for cross-sections but cannot support event studies. This is the only vendor I verified actually delivers Deribit options data at tick granularity with sequence-validated books. Buy only after the free days prove your pipeline.
- **Amberdata Derivatives** — https://docs.amberdata.io/. Deribit-endorsed for DVOL analytics, and Magadini's Genesis Volatility folded into it. Relevant mainly if you want their pre-computed surfaces rather than fitting your own — which, given you have SVI/SSVI already, you probably don't.
- **Kaiko** — https://www.kaiko.com/. Worth it only if you want the data behind the Echenim-Gobet-Maurice methodology. The paper is free and the method is implementable on Deribit data you can get yourself.
- **Alexander & Imeraj (2023) and Lucic & Sepp (2024)**, *Quantitative Finance* — both have free SSRN preprints, so paywalled versions are unnecessary. Use your IITKGP access only if you need the final typeset versions.