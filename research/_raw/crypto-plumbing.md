# Crypto Market Structure, Venues, and the Indian Reality

Everything below is descriptive. The tax/FEMA section reports rules and their arithmetic; it is not tax or legal advice, and the contested points are flagged as contested. Verify with a CA before acting.

---

## 1. THE INDIAN ARITHMETIC — read this first, it determines what is worth building

### 1.1 The three rules

| Rule | Statute | Effect |
|---|---|---|
| 30% flat on VDA gains + 4% cess (+ surcharge) → **31.2% minimum effective** | s.115BBH, Finance Act 2022 (carried into the Income-tax Act 2025, in force 1 Apr 2026, renumbered — verify the new section on your ITR) | Applies irrespective of slab |
| **No deduction except cost of acquisition** | s.115BBH(2) | Exchange fees, funding paid, data subscriptions, VPS, infra are **not deductible** |
| **No set-off, no carry-forward of VDA losses** | s.115BBH(2)(b) | Loss on one VDA transfer cannot offset gain on another, on any other income, or on next year |
| 1% TDS on consideration (not on profit) above ₹50,000/FY (₹10,000 for non-specified persons) | s.194S | Withheld on the sale leg; both legs in crypto-to-crypto |

Sources: [taxguru — 115BBH & 194S](https://taxguru.in/income-tax/taxation-cryptocurrency-virtual-digital-assets-india-understanding-sections-115bbh-194s-method-taxation.html), [Koinly India guide](https://koinly.io/guides/crypto-tax-india/), [Patron Accounting — IT Act 2025 treatment](https://www.patronaccounting.com/blog/crypto-vda-taxation-income-tax-act-2025-rules).

### 1.2 What the no-offset rule does — the number that kills strategies

Tax is levied on **gross gains**, not net. Let a book's yearly gross winning P&L be `W` and gross losing P&L be `L`. Then:

```
post-tax P&L  =  (W − L) − 0.312·W
              =  0.688·W − L
```

Break-even requires **W/L ≥ 1.4535**.

Work an example. ₹1 crore book, delta-hedged short vol, one year:
- gross gains ₹40,00,000, gross losses ₹32,00,000 → net **+₹8,00,000 (8% return)**
- tax = 0.312 × 40,00,000 = **₹12,48,000**
- post-tax = **−₹4,48,000**

A profitable 8%-return book returns −4.5%. This is not a fee, it is a structural sign flip. And note *which* strategies have W/L near 1: delta-hedged option books, market-making, stat-arb, funding carry, calendar spreads, dispersion — i.e. exactly the low-variance, high-Sharpe strategies you would want to run. A directional punt with W/L = 3 survives the tax fine. **The Indian VDA tax code is precisely anti-selected against good vol trading.** A high-Sharpe, high-turnover book is the worst possible thing to run inside 115BBH.

Note also the second-order effect: because fees and funding paid are not deductible, they are paid out of post-tax money, i.e. a 0.05% taker fee costs you 0.05%/0.688 = **0.0727% in pre-tax-equivalent terms**. Multiply every quoted cost in your backtest by 1.45.

**Contested point, and it is the single most consequential open question for your P&L:** whether losses net *within the same VDA* (BTC against BTC) before 115BBH bites, or whether the tax is transaction-by-transaction. The statute bars offsetting loss from *one* VDA against gain from *another*; CBDT's 2022 Lok Sabha reply took the restrictive reading. Many practitioners file on a same-asset-netting basis. There is no circular. If transaction-level is correct, no hedged book is viable; if same-asset netting is allowed, a pure-BTC book is viable and a BTC-vs-ETH relative-value book is not. Get a written opinion before you size anything.

### 1.3 What 1% TDS does — capital decay, not a fee

TDS is **creditable and refundable** against final liability. It is not a 1% cost. The damage is mechanical cash-flow decay: 1% of gross sale consideration leaves the trading account on every disposal and does not come back until after you file.

Deployable capital after `N` round trips:

```
C_N = C·(0.99)^N ≈ C·e^{−0.01N}
```

- 25 round trips/yr → 78% of capital still deployable
- **69 round trips → half your capital is sitting with the Income Tax Department**
- 230 round trips → 10%

A strategy at one round trip per week (52/yr) ends the year with 59% of its capital immobilised. A daily strategy (250/yr) ends with 8%. **Any strategy with more than roughly weekly turnover is not fundable in VDA form in India**, independent of whether it makes money. That is the correct framing — not "1% eats your edge," but "1% converts your trading capital into a tax receivable."

Combine with 1.2 and the conclusion is unambiguous: **do not run high-turnover crypto spot/VDA strategies as an Indian resident inside the VDA regime.** Research them, paper them, and understand that the venue for actually deploying them is either (a) the derivatives route below, if your CA blesses it, or (b) not India.

### 1.4 The derivatives route, and why it is a grey area rather than a solution

INR-settled crypto futures and options on **Delta Exchange India** (FIU-IND registered, VA00041101) are marketed on the basis that a cash-settled derivative is not itself a VDA under s.2(47A), therefore: no 1% TDS, no 115BBH, taxed as business income at slab, losses offsettable. See [Delta's own support page](https://www.delta.exchange/support/solutions/articles/80001132761-is-there-30-vda-tax-applicable-on-trading-profits-).

Treat that page as an interested party's interpretation, not law. The neutral position, confirmed across practitioner writing: **no CBDT circular, no binding clarification, no judicial precedent.** ([Karnanica](https://www.karnanica.com/taxation-of-crypto-futures-in-india/), [CA Delhi India](https://www.caindelhiindia.com/blog/crypto-futures-taxation/)) The practitioner consensus leans toward slab-rate business income, with notices reported on the other side.

Two further points nobody markets:
- Crypto derivatives are not traded on a "recognised stock exchange" for s.43(5)(d), so the likely characterisation is **speculative business income** — losses then only offset speculative income and carry forward 4 years, not 8. This is my reading of the statute, not something I verified against a ruling. Check it.
- Delta India is effectively the *only* venue for this. That is single-counterparty concentration on a mid-sized firm, with liquidity and spreads far worse than Deribit. You would be trading a structurally inferior market for a tax treatment that has not been confirmed.

### 1.5 FEMA / LRS — what the rules actually say

The RBI's own [LRS FAQ](https://www.rbi.org.in/commonperson/english/scripts/FAQs.aspx?Id=1834) permits USD 250,000/FY for listed purposes and explicitly prohibits, among others:

> "Remittance from India for margins or margin calls to overseas exchanges / overseas counterparty"
> "Remittance for trading in foreign exchange abroad"

**Cryptocurrency and VDAs are not mentioned anywhere in the LRS FAQ.** There is no RBI banking prohibition on crypto post-*IAMAI v. RBI* (SC, March 2020) and RBI's 2021 withdrawal of its 2018 circular. But the "margins to overseas exchanges" prohibition is a named, literal prohibition, and funding a margin account at Deribit is, on the face of the text, a remittance of margin to an overseas exchange. That is the rule as written; I am not going to characterise it further or discuss workarounds.

Also relevant and to be verified with your CA: 20% TCS on LRS remittances above ₹10 lakh per FY (creditable against tax liability), and Schedule VDA / foreign asset reporting obligations in the ITR.

Adjacent factual points: Binance (registered Aug 2024, after ₹18.82 crore penalty) and KuCoin (March 2024) are FIU-IND registered and serve Indian users; ~49–54 VDA service providers are registered with FIU-IND per the FY2024-25 annual report and a March 2026 parliamentary disclosure. ([PIB show-cause notices](https://www.pib.gov.in/PressReleasePage.aspx?PRID=1991372&reg=48&lang=2), [Fintech Singapore](https://fintechnews.sg/95665/digitalassets/binance-and-kucoin-approved-to-provide-virtual-asset-services-in-india-by-fiu/)) **India is not on Deribit's restricted-country list** (US, Ontario, Japan, Cuba, Iran, Iraq, Panama, Syria, DPRK, Sudan, Guam), so the exchange-side barrier is not the constraint — the funding rail and the tax code are.

---

## 2. DERIBIT MARKET STRUCTURE — the parts that differ from NIFTY and SPX in ways that change your model

### 2.1 The inverse-contract problem

BTC options on Deribit are coin-margined: contract size 1 BTC, premium paid in BTC, settled in BTC. A "call" pays `max(S−K,0)/S` BTC. In the BTC numéraire this is **not a vanilla** — it is a quanto/self-referencing payoff, and the Black-Scholes IV Deribit quotes is the USD-numéraire IV of a USD payoff you never receive. If you build a surface from Deribit marks and then price a USDC-settled structure off it, you are wrong by the correlation between the underlying and the settlement asset — which for BTC-settled BTC options is 1. Deribit also lists USDC- and USDT-margined linear options; the two families have different liquidity and different vols for the same strike. This has no NIFTY or SPX analogue at all and it is the first thing to get right in your pricer.

### 2.2 Tick size — the constraint nobody mentions

Option prices are quoted in BTC with a minimum tick of 0.0001 BTC (0.00005 for low-priced options). At BTC = $100,000, one tick is **$10**. A 10-delta weekly wing worth $25 has a minimum quotable increment of 40% of its own value. Compare NIFTY's ₹0.05 premium tick on a ₹5 option, or SPX's $0.05.

Consequence: **systematic wing trading on Deribit is a fiction at small size.** Your backtest will happily buy the 10-delta put at mid; the real book has a two-tick spread that is 80% of the premium. Any tail-hedging or skew-harvesting result you produce must be re-run with the true tick grid and the recorded book, not marks.

### 2.3 Fees, and where the binding cost actually is

Base-tier Deribit ([fee schedule](https://support.deribit.com/hc/en-us/articles/25944746248989-Fees), revised 1 Aug 2026 — [announcement](https://insights.deribit.com/exchange-updates/new-fee-schedule-on-deribit/)):

- **Options: 0.03% of the underlying index price per contract, capped at 12.5% of the option price. Maker AND taker both pay — there is no maker rebate in options.**
- **Perps/futures: 0.00% maker / 0.05% taker.**
- Liquidation fee: 1% across all products (new, tied to the Liquidity Support Program).
- Delivery/expiry: roughly half the taker rate (~0.02% options, ~0.025% futures); OTM expiry is free.
- Block trades: 10% discount.

Work the arithmetic for a 30-day ATM straddle at 50 vol, notional = S:

| Cost | Size |
|---|---|
| Straddle premium ≈ 0.8·σ·√T·S | 11.5% of S |
| Option fees, 2 legs in + 2 out, 0.03% each | 0.12% of S ≈ **1.0% of premium** |
| Daily delta hedging on the perp, taker: E\|ΔΔ\|/day ≈ Γ·S·σ√dt ≈ 7.3% of notional/day × 5 bps × 30d | 0.11% of S ≈ **1.0% of premium** |
| Quoted bid-ask, 1.5 vol points wide, vega ≈ 0.115% of S per vol pt, in and out | 0.34% of S ≈ **3.0% of premium** |

Three implementable conclusions:
1. **The spread, not the fee, is the binding cost.** Your backtest must consume recorded order books. Mid-price backtests of Deribit vol strategies are worthless.
2. **Delta hedge with limit orders on the perpetual**, not with futures or spot — perp maker is 0.00%, and passive hedging drives the hedge cost from 1% of premium to approximately zero (at the price of hedge-timing error, which is the honest trade-off and is measurable in your minute data).
3. The 12.5%-of-premium cap only binds on options cheaper than 0.24% of spot. For everything liquid, you pay the full notional-based fee — which means **fee cost scales with notional, not with premium**, so short-dated cheap options are proportionally brutal and long-dated expensive options are nearly free. This is the exact opposite of NIFTY's premium-based brokerage and inverts which part of the surface is economically tradeable.

### 2.4 Portfolio margin — the real structural advantage

Deribit's PME ([support page](https://support.deribit.com/hc/en-us/articles/25944756247837-Portfolio-Margin), [full model PDF](https://statics.deribit.com/files/DeribitPortfolioMarginModel.pdf)) computes a risk matrix over underlying moves of −16% to +16% for BTC/ETH plus an extended table of −66%, −33%, +50%, +100%, +200%, +300%, +400%, +500%, crossed with vol-up/same/down scenarios, then takes the worst case, adds a delta shock and a roll shock. IM = worst case; MM = IM × maintenance factor. There are additionally **vega concentration limits** — exceed them and Deribit raises your MM by 5% per day until you comply ([vega limits](https://support.deribit.com/hc/en-us/articles/30856172663837-Vega-Concentration-Limits)).

Why this matters versus India: NSE SPAN gives you nothing like a +500% scenario, and Indian retail cannot get true cross-margin on an option book at all; SPX portfolio margin requires a $100k+ US brokerage account. **Deribit gives a genuinely risk-based margin engine at low account size.** For a hedged vol book this is a 3–5× capital efficiency difference versus anything available in India, and it is the strongest single argument for Deribit as the research venue. The PDF is worth reading end-to-end — it is a specification you can implement and margin-simulate against, which makes margin a *modelled* constraint in your backtest rather than an afterthought. Most crypto backtests ignore margin entirely and are therefore fantasy.

### 2.5 Settlement, expiries, term structure

- **Settlement: 30-minute TWAP of the Deribit index (a multi-exchange composite) ending 08:00 UTC.** Contrast NIFTY (last-30-min VWAP of spot, 15:30 IST, on a single venue) and SPX (AM-settled SET opening print vs PM-settled SPXW). The TWAP-of-composite is materially harder to manipulate, so **pin-risk and expiry-manipulation strategies that work on NIFTY do not transfer.** Conversely, expiry-day gamma effects are weaker and less exploitable.
- **Real term structure out to 6–12 months** with genuine open interest, unlike NIFTY where anything beyond two months is a quote and not a market. Calendar and term-structure trades are actually executable here; they are not in India.
- Liquidity concentrates in the nearest weekly and the nearest monthly, roughly ±25 delta, with large OI parked at round strikes ($100k, $120k, $150k) and at quarter-end expiries. Wings and back months are quotable but wide.
- **24/7, no close.** No overnight gap risk, but also no flat state: hedging error accrues continuously, weekend books are thin and funding regimes shift. Your Indian intuition of "square off before close" has no counterpart.
- **No CCP.** NSE has a clearing corporation with member capital and a settlement guarantee fund; OCC backs SPX. Deribit has an insurance fund and a liquidation waterfall. Your counterparty is the exchange.

---

## 3. PERPETUAL SWAPS — funding, mark, liquidation, ADL

### 3.1 Funding is not one mechanism, it is several

**Binance** ([FAQ](https://www.binance.com/en/support/faq/360033525031)):
```
F = P + clamp(I − P, −0.05%, +0.05%),   I = 0.01% per 8h
P = time-weighted average premium index, weights 1,2,…,n over the interval
```
Paid every 8 hours, **only if you hold the position at the timestamp.** Per-contract funding caps exist separately from the ±0.05% clamp inside the formula (BTCUSDT's cap is larger — I did not verify the current number; look it up before you rely on it).

**Hyperliquid** ([docs](https://hyperliquid.gitbook.io/hyperliquid-docs/trading/funding)): same functional form, `I = 0.01%/8h = 0.00125%/hr`, premium **sampled every 5 seconds and averaged over the hour**, **paid hourly**, capped at 4%/hour.

**Deribit**: 8h-quoted rate but accrued continuously rather than at a snapshot. (I am confident in this from the product design but did not verify it in this session — check the docs.)

**Why the difference creates and destroys strategies:**
- Binance's discrete snapshot creates a genuine, well-known microstructure trade: enter just before, exit just after — or the reverse, to dodge paying. It also produces a repeatable order-flow pattern in the minutes bracketing 00:00/08:00/16:00 UTC. That flow is visible in minute data and is the kind of thing you can actually test. It is also crowded and latency-sensitive at the exact tick.
- Hyperliquid's hourly, 5-second-sampled funding **eliminates that trade** and makes the carry close to a continuous dividend yield. So a "funding capture" strategy validated on Binance data does not exist on Hyperliquid, and vice versa. Cross-venue funding-rate dispersion (same asset, different formula, different cap, different interval) is itself a tradeable term structure, and it is the most implementable crypto-specific idea on this page.
- Funding is the crypto equivalent of a dividend/repo term structure. The whole vol-surface-vs-carry apparatus you learned for equity indices maps onto it directly, which is the highest-value transfer of your existing SVI/SSVI work.

### 3.2 Mark price and liquidation

You are liquidated on **mark**, never on last trade. Binance mark = index + EMA of the basis. Hyperliquid uses a robust median construction over the oracle, the book mid, and external references. Deribit marks perps off the index with a funding adjustment.

This is the single most common backtest error in crypto: simulating liquidation against traded price. Wicks on the venue's own book routinely do not move the mark, and — the important direction — **a mark constructed from a multi-venue index can move against you when your own venue's book has not.** Any leveraged strategy you backtest must reconstruct the venue's actual mark formula from recorded index data, or the survivability numbers are fiction.

### 3.3 ADL — why "perfectly hedged" is a lie

Liquidation waterfall: position taken over by the liquidation engine → liquidation fee (Deribit: 1% across all products from Aug 2026) → shortfall absorbed by the insurance fund → if the fund is exhausted, **auto-deleveraging** force-closes profitable counterparties, ranked by profit × leverage.

The implication is structural and it is the honest counterweight to everything in section 2: **ADL is an uncompensated, unhedgeable forced exit that fires precisely at the tail.** Cash-and-carry, long-tail-option books, short-gamma hedges, and anything whose payoff is concentrated in a crash are exactly the positions ranked at the top of the ADL queue at the moment they pay off. This has no equivalent on NSE or the OCC, and it means:
- backtested tail payoffs need a haircut you cannot calibrate from price data alone;
- being *more* profitable and *more* levered puts you *earlier* in the queue;
- diversifying across venues is a real risk control here, not a platitude, because ADL is per-venue.

---

## 4. DATA AND APIs

| Source | URL | What it concretely gives you | Tests passed | Honest caveat |
|---|---|---|---|---|
| **Binance public data** | `data.binance.vision` | Free, no key, complete history: aggTrades, 1-second klines, bookTicker, bookDepth, and futures `metrics` (funding rate, open interest, long/short ratios). Monthly + daily zips. | (1) tooling exists, (5) trivially reproducible | Spot/futures only, **no options**. bookDepth is snapshots, not a replayable L2 stream. |
| **Tardis.dev** | [tardis.dev](https://tardis.dev/) · [docs](https://docs.tardis.dev/) · [python client](https://docs.tardis.dev/api/python) | Tick L2/L3, trades, quotes, OI, funding, and **Deribit options chain** (from the ticker channel, which is what makes IV surface history possible at all). `datasets.download()` for bulk. | (1) Python + Node clients, (5) reproducible | Paid beyond samples. **But**: a [free API key gives full Deribit history for Q4 2021 – Q1 2022](https://insights.deribit.com/exchange-updates/celebrating-our-tardis-dev-partnership-get-free-historical-data/), plus first-day-of-month free across all exchanges. Two quarters of real tick options data spanning a genuine regime change is enough for a serious SVI/SSVI-on-crypto project at zero cost. Start here. |
| **Deribit native API** | [docs.deribit.com](https://docs.deribit.com/) · [rate limits](https://support.deribit.com/hc/en-us/articles/25944617523357-Rate-Limits) | Free public REST + WS. Full book, ticker, `get_last_trades_by_instrument_and_time`, and the **DVOL** index (30-day forward IV — the direct VIX analogue, with a futures market on it). | (1), (2) fees documented, (5) | Rate limits: matching-engine requests cost 500 credits against a 50,000 credit bucket refilling at 10,000/s (~20 req/s sustained, ~100 burst). **Critically: expired instruments drop out of the endpoints. There is no retrievable options history.** If you want your own dataset, you must start a recorder today; every day you wait is permanently gone. |
| **Deribit best-practices pages** | [market data](https://support.deribit.com/hc/en-us/articles/29592500256669-Market-Data-Collection-Best-Practices) · [order mgmt](https://support.deribit.com/hc/en-us/articles/29514039279773-Order-Management-Best-Practices) · [server infra](https://support.deribit.com/hc/en-us/articles/25944617582877-Server-Infrastructure) | The venue telling you exactly how to build the recorder and the execution layer. | (3) written by the operator, (4) names its own limits | Short. Read all three in twenty minutes. |
| **schepal/deribit_data_collector** | [github](https://github.com/schepal/deribit_data_collector) | Downloads the entire BTC/ETH option chain. A working starting point for your recorder. | (1) runnable | Small, unmaintained; treat as a reference implementation, not a dependency. |
| **nostoz/deribit_volatility_download_and_visualize** | [github](https://github.com/nostoz/deribit_volatility_download_and_visualize) | Loading + surface construction + visualisation from Deribit. | (1) runnable | I did not run it or review the IV solver. Verify its inverse-contract handling specifically (see §2.1) before trusting any surface it produces. |

Deliberately **not** recommended: CoinGecko/CoinMarketCap price APIs (daily OHLC, no book, no options — useless for anything you want to do), and the various "crypto backtest framework" repos, which almost universally fail the cost-model test.

---

## 5. LATENCY — what is and is not reachable from India

**Deribit's matching engine is at Equinix LD4, Slough, UK.** Access is via colocation/cross-connect at LD4 or AWS PrivateLink; the low-latency multicast feed is available to AWS clients in **eu-west-2 (London)** and **ap-northeast-1 (Tokyo)** at close-to-colo latency ([server infrastructure](https://support.deribit.com/hc/en-us/articles/25944617582877-Server-Infrastructure)).

Order-of-magnitude RTT from a Mumbai consumer/office connection: London ~110–130 ms, Singapore ~50–60 ms, Tokyo ~120–140 ms. So trading Deribit from your laptop in India means a **~120 ms floor**, plus load-balancer hops on the public endpoint.

The fix is cheap and you should do it before anything else: **a small instance in `eu-west-2` puts you at single-digit milliseconds to the matching engine for roughly $30–60/month.** There is no excuse for running a live book from a laptop in India. The same logic gives Binance/Bybit `ap-northeast-1` and `ap-southeast-1` respectively — check each venue's stated region rather than guessing.

Honest boundary:

- **Not reachable, ever, at your setup:** passive top-of-book quoting in liquid ATM options, latency arbitrage, funding-snapshot sniping at the tick, liquidation-cascade participation, cross-venue triangular arb. These are colo games against firms with dedicated fibre. Do not build them.
- **Fully reachable:** anything with a holding period beyond a few seconds — vol surface relative value, term-structure and skew trades, calendars, dispersion, funding carry and cross-venue funding dispersion, systematic delta hedging at minute granularity, DVOL-vs-realised. Your minute-wise data instinct from the NIFTY side maps onto this directly.
- **The rule to internalise:** on Deribit you are either a taker paying the spread, or a passive quoter who must model adverse selection. Price-time priority without colocation means your passive fills are systematically the ones you did not want. Any backtest that fills you at your limit price whenever the market touches it is overstating your P&L by roughly the entire edge.

---

## 6. CUSTODY AND COUNTERPARTY, POST-FTX

**The structural change worth knowing: Deribit was acquired by Coinbase, closing August 2025 (~$2.9bn).** ([announcement](https://insights.deribit.com/exchange-updates/deribit-to-join-coinbase-a-new-chapter-in-global-crypto-derivatives-2025/)) Your counterparty for a crypto options book is now a US-listed public company with audited financials rather than an offshore private entity. That is a genuine, material improvement in counterparty quality and it is the strongest non-microstructure argument for Deribit as your venue.

**Off-exchange settlement** (Copper ClearLoop, Binance/Ceffu, Fireblocks Off-Exchange) is the institutional answer: assets stay in MPC custody, the exchange receives a trading credit, settlement is off-chain at T+1. ClearLoop connects Coinbase, OKX, Bybit, Deribit, Bitget and others. ([Ceffu explainer](https://www.ceffu.com/blog/ceffu-understanding-off-exchange-settlement), [Valmar report](https://www.valmar.io/blog/report-on-crypto-custody-and-off-exchange-settlement-solutions)) **This is not reachable at intern size** — institutional minimums, onboarding, legal agreements. Know that it exists and that its own residual risks are real (reliance on the settlement operator, enforceability of the mirroring agreement, the T+1 window).

Be blunt about **proof-of-reserves**: a Merkle tree of customer liabilities plus an attestation of on-chain assets proves neither the absence of undisclosed off-balance-sheet liabilities nor that the keys weren't borrowed for the snapshot. PoR is a lower bound on honesty, not an audit. Treat it as weak evidence.

At your size the practical controls are unglamorous and sufficient: keep only working margin on-venue and sweep realised P&L out; split across at least two venues (which also diversifies ADL); hardware-key 2FA and address whitelisting with a time-locked change window; and size every position on the assumption that the on-venue balance can go to zero for reasons unrelated to your trading.

---

## 7. WHAT THIS MEANS FOR WHAT YOU BUILD

1. **Start the Deribit recorder this week.** Options history is not retrievable after the fact. Pull the free Tardis Q4-2021/Q1-2022 Deribit key today for a backfill you can do research on immediately, and record forward from now.
2. **Do your vol research on Deribit; do not assume you will deploy it there.** The Indian tax arithmetic in §1.2 and §1.3 means a high-Sharpe hedged crypto book is post-tax negative under 115BBH. Know that before you spend six months on it, not after.
3. **Your SVI/SSVI work transfers, with one correction and one addition.** The correction is the inverse-contract numéraire (§2.1). The addition is that funding is a stochastic dividend yield with a venue-dependent formula, so the forward is not a clean `S·e^{(r−q)T}` and your calibration must take the forward from the listed future, not construct it.
4. **Model the tick grid and the recorded spread, not mid.** For Deribit wings the tick alone can exceed the edge (§2.2). This is the single most common way crypto options research is wrong.
5. **Implement the PME margin model as a constraint in your backtest** (§2.4). Deribit publishes the specification. A vol backtest without a margin simulator is not a backtest.
6. **The one genuinely uncrowded, implementable idea in this document** is cross-venue funding-rate dispersion (§3.1) — same asset, different formula, interval, sampling and cap across Binance / Hyperliquid / Deribit / OKX. The data is free (Binance public data + Hyperliquid API + Deribit API), the holding period is hours to days so latency is not the constraint, and the mechanism is structural rather than statistical. Its honest weakness: capacity is limited, the carry is small relative to the counterparty and ADL risk you take to collect it, and it is not tax-viable for an Indian resident under §1.

---

## Things I could not verify in this session

- Deribit's exact post-1-Aug-2026 fee tier table. [The support page returned HTTP 403 to automated fetch](https://support.deribit.com/hc/en-us/articles/25944746248989-Fees); the numbers in §2.3 are corroborated across secondary sources and match the pre-change schedule, but open the page in a browser before you hard-code them.
- Binance's current per-contract funding cap for BTCUSDT (the ±0.05% figure in the search results is the in-formula clamp, which is a different thing from the cap).
- Whether Deribit accrues perp funding continuously or at snapshots — stated from product knowledge, not verified this session.
- The new section number replacing 115BBH under the Income-tax Act 2025 (in force from 1 Apr 2026). Substance is preserved; numbering is not confirmed in any source I found.
- Whether crypto derivatives fall under s.43(5) speculative treatment — that is my reading of the statute, and it is consequential enough that you should not rely on my reading.

**No paid items to recommend.** Everything above is free, including the Tardis Deribit backfill. The only recurring cost worth paying is the ~$40/month AWS eu-west-2 instance, which is infrastructure, not content.