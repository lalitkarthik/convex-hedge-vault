# Crypto Strategies, 2026: Alive vs. Decayed

**Verification note up front.** Roughly 70% of what surfaces on these topics is content-farm or broker-affiliated and was rejected mechanically. Specifically rejected: `coinmarketcap.com/academy`, `arbitragescanner.io`, `cryptowisser.com`, `blofin.com`, `tv-hub.org`, `sparkcore.fund`, `wundertrading`, `bjftradinggroup`, `hyrotrader`, `dexly`, `supa.is`, `vaasblock` (all funnel to a platform, signal service, or affiliate link; none carry a cost model). Also rejected: **Everstrike's "7 Arbitrage Strategies Still Accessible to Retail Quants"** — it is the most-cited retail piece on this and it is written by an options exchange promoting its own zero-fee venue, i.e. broker-affiliated education where order flow is the business model. Auto-reject, regardless of the fact that some of its content is correct.

Where a number below is not attributable to a source I actually opened, I say so.

---

## 1. Perpetual funding carry / cash-and-carry — **ALIVE, but the risk is not where retail thinks it is**

The trade still works. What has changed is that the failure mode is now documented with a date and a body count.

### The evidence that matters: 10–11 October 2025

**Anatomy of the Oct 10–11 2025 Crypto Liquidation Cascade** — https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5611392

~$19bn open interest liquidated, 1.6M accounts, $3.21bn in a single minute at 21:15 UTC. The mechanism that matters to you: **auto-deleveraging (ADL) forcibly closed market makers' short perp legs against their long spot** — the profitable side of the delta-neutral book was the side the exchange took away, leaving participants unhedged long spot into a 14% BTC drawdown.

- Tests passed: (4) names its own failure mode, in the strongest possible form — an actual post-mortem; (5) reproducible, the event is in every Deribit/Binance/Bybit tape you can buy from Tardis.
- Caveat: it is a post-mortem paper, not a strategy. No code, no backtest. Use it as the stress scenario your carry backtest must survive, not as a source of alpha.

**Corroboration with real consequences:** Stream Finance's xUSD marketed an ~18% delta-neutral yield and depegged >77% in early November 2025 after ~$93M in losses, with post-mortems tracing the damage to ADL breaking hedges during Oct 10–11. Coindesk (Jan 2026) reports BitMEX's finding that the crash left market makers stuffed with unhedged inventory and produced the thinnest liquidity since 2022 — https://www.coindesk.com/markets/2026/01/08/october-s-crypto-crash-left-market-makers-stuffed-with-coins-slowing-trading-bitmex

### Runnable implementation

**Hummingbot `scripts/v2_funding_rate_arb.py`** — https://github.com/hummingbot/hummingbot/blob/master/scripts/v2_funding_rate_arb.py

Working multi-venue funding arb with a profitability threshold, executor-based position management, and a backtestable controller framework (Quants Lab).

- Tests passed: (1) runnable code, Apache 2.0; (3) built and operated by a team that runs it live; (5) reproducible on free exchange APIs.
- Caveat, and it is a big one: read the open issues before you trust it. Issue #7295 documents a **double fill on Hyperliquid perps after stopping the strategy** — https://github.com/hummingbot/hummingbot/issues/7295. The hedge-integrity bugs are in the harness, not just in the market. Your delta-neutral book is only neutral if the order state machine is correct.

### Honest numbers

Funding has structurally compressed. 2021 bull-phase prints of 0.15–0.20% per 8h (>200% annualised) have given way to a 2024–2026 baseline that sits near **0.01% per 8h ≈ 11% annualised** before costs, spiking only in leverage-euphoria windows. CME annualised basis was around 10% by May 2025 and dipped **below zero** in February 2025.

- **Capital:** meaningful only above ~$50–100k, because you are running two collateral pools on two venues and must hold buffer against ADL/margin calls on both. Below $25k, fees and funding-rate volatility dominate.
- **Infrastructure:** low. REST + websocket, a reliable box, and a margin monitor. No colocation.
- **Latency sensitivity:** low for entry, **high for the unwind** — Oct 10 punished slow unwinds.
- **Solo-viable:** yes. This is the most solo-viable strategy on your list.
- **The claim to disbelieve:** the "19.26% annual, 0.80% max drawdown, positive all 12 months of 2025" figure is circulating widely across the rejected sources with no attribution and no cost model. I could not trace it to a primary source. Treat it as marketing until proven otherwise. A strategy that was positive all 12 months of 2025 was, by construction, not honestly accounting for October.

---

## 2. Deribit options vol selling / VRP — **ALIVE but the published evidence is weaker than its reputation**

This is the area where the gap between academic popularity and implementable evidence is widest, and you should know that before you commit months to it.

**Risk Premia in the Bitcoin Market** — https://arxiv.org/html/2410.15195v2

BVRP averages 0.14 vs ~0.02 for SPX. 5.38M transactions, July 2017–Dec 2022, Deribit. Regime split: 0.12 in high-vol, **0.17 in low-vol** — the premium is *larger* when things are calm, which is the opposite of the equity intuition and is directly tradeable as a regime filter.

- Tests passed: (5) fully reproducible — Deribit data via Tardis from 2019-03-30. That is genuinely all it passes.
- Caveat, stated bluntly: **no transaction costs, no implementation, no trading discussion, and the sample ends in 2022.** It fails your two-of-five filter on its own. I am including it because the *number* is load-bearing for your sizing and the data is obtainable — not because it qualifies as a source. The premium goes negative (March–April 2020 is the shaded region); the paper excludes estimates below −2, which is exactly the tail that kills a short-vol book.

**Deribit Insights — "Bitcoin Options: Finding edge in four years of volatility regimes"** — https://insights.deribit.com/industry/bitcoin-options-finding-edge-in-four-years-of-volatility-regimes/

Backtests daily-delta-hedged risk reversals, systematic short straddles, butterflies, and event-driven long vol, Apr 2019–Dec 2022.

- Tests passed: (3) exchange-practitioner authorship; (4) names failure modes honestly — Black Thursday, unlimited straddle loss, butterflies destroyed by paying two premiums, and event-driven results resting on **fewer than 15 trades per backtest**, which the author admits.
- Caveat: it explicitly marks-to-mark. Its own words: the mark price P&L "is not entirely realistic in practice." No code. And it stops in 2022 — it says nothing about whether the premium survived the ETF era and the 2025 vol regime.

**What I could not verify, and you should treat as an open question:** I found no credible, cost-inclusive study establishing that the crypto VRP is still positive *net of Deribit's fee cap and bid-ask* in 2025–2026. Kaiko/MerQube found IBIT and Deribit priced skew and put-wing convexity materially differently across 2025 (https://www.kaiko.com/news/kaiko-research-highlights-tail-risk-divergence-between-ibit-and-deribit-options) — which is a real, current, cross-venue structural dislocation and is probably the more interesting thing on this list for someone with your SVI background. It is also the thing nobody has published a tradeable study on.

- **Capital:** $25k+ for delta-hedged short vol on Deribit; the hedging leg is what needs the room.
- **Infrastructure:** moderate. You need a surface fitter (you have one), a delta-hedge scheduler, and tick data. Deribit fees are capped at 12.5% of option premium, which matters enormously for cheap wings and is the single most common omission in retail crypto-options backtests.
- **Latency:** low. Daily or Whalley-Wilmott-banded hedging.
- **Solo-viable:** yes, and this is where your existing SVI/SSVI work has the highest transfer.

**Data:** Tardis.dev has full Deribit options history from 2019-03-30, and **first-day-of-each-month CSVs are free without an API key** — https://docs.tardis.dev/historical-data-details/deribit. That is enough to prototype a surface pipeline at zero cost before paying for anything.

---

## 3. Market making — **ALIVE on CEX perps for a solo dev; the LP/AMM version is largely folklore**

**hftbacktest** — https://github.com/nkaz001/hftbacktest

The single best technical resource on this list. Full L2 MBP / L3 MBO order-book reconstruction, explicit **queue-position-aware fill simulation**, and separate **feed latency and order latency** models you can override. Binance Futures and Bybit. Rust core with a live trading deployment path that runs the same strategy code as the backtest.

- Tests passed: (1) runnable code; (2) explicit latency/fill/queue modelling, which is the crypto-MM equivalent of a cost model and stricter than most; (4) the README argues directly about backtest realism and the danger of both optimistic and pessimistic simulation; (5) works on obtainable Binance/Bybit tick data.
- Caveat: this tells you your fills are honest, not that your strategy is good. It is a measuring instrument. Also, "same code backtest and live" is Rust-only — the Python path is research-only.

**NautilusTrader** — https://github.com/nautechsystems/nautilus_trader — nanosecond event-driven, configurable fill/fee/latency models, queue-position and liquidity-consumption tracking, Rust core with a Python strategy API. Passes (1), (2), (3). Caveat: heavier abstraction cost than hftbacktest, and its crypto adapters are less battle-tested than its general engine.

**Hyperliquid** is the venue where solo MM is currently most reachable — official Python SDK, on-chain fills you can audit, 0.015% maker rebates as of March 2026. But look hard at HLP's own record before assuming the economics: ~$136.9M cumulative profit since May 2023, TVL peaking at $603.9M in Sept 2025, historical APY roughly **3–8% with negative months**, and profit concentrated in a few high-volatility events. That is the *protocol's* professionally-run MM book with rebate and liquidation privileges you will not have. Your unlevered solo expectation should be below that, not above it.

- **Capital:** $10–25k to be meaningful on one or two liquid perps; below that, per-order minimums and inventory granularity fight you.
- **Infrastructure:** the real cost. A VPS near the matching engine (AWS Tokyo for Binance/Bybit), tick data capture, and a disciplined inventory/skew controller.
- **Latency:** high sensitivity — this is the one strategy on the list where 10ms matters.
- **Solo-viable:** yes on a small number of mid-cap perps. No on BTC/ETH top-of-book against Wintermute.

### The LP / AMM version: mostly a losing trade dressed as yield

**Impermanent loss and loss-versus-rebalancing** — https://arxiv.org/pdf/2410.00854 and https://arxiv.org/pdf/2502.04097

The honest framing: an LP is profitable iff fees > LVR. Empirically, one analysis of 17 Uniswap v3 pools found **$199.3m fees earned vs $260.1m impermanent loss — LPs were $60.8m worse off than simply holding.** Bancor/IntoTheBlock separately found >51% of v3 LPs unprofitable. Uniswap's own blog (https://blog.uniswap.org/fee-returns) counters that non-rebalancing v3 positions beat v2 by ~54% on fees — note that this is v3-vs-v2, not LP-vs-HODL, and it is published by the protocol whose TVL depends on the answer.

Concentrated-liquidity LPing is a short-gamma position sold to arbitrageurs at a price you do not set. Fee APR headline numbers are gross of LVR and are the single most misleading number in DeFi. Skip this unless you are specifically researching LVR mitigation as a topic.

---

## 4. Cross-exchange and triangular arbitrage — **DECAYED. This is retail folklore.**

I found no source passing the filter that shows a solo retail trader profitably running latency arb in 2025–2026. Everything claiming otherwise was broker-affiliated or a bot vendor.

The arithmetic: cross-venue spreads now sit roughly 0.1–2%, and at 0.1% taker fee per side you need 0.2% just to break even — before slippage, before the fact that capturing it requires pre-positioned inventory on both venues (you cannot transfer BTC in the arb window), and before the funding cost of that idle split capital.

- **Capital:** you must pre-fund every venue, so effective capital requirement is N × position size, and most of it is idle.
- **Latency:** decisive, and you lose.
- **Solo-viable:** no. The residual retail version — waiting for withdrawal-gated spreads on small venues — is unhedgeable counterparty risk on exchanges most likely to abscond.

The one legitimate residual: **funding-rate dispersion across venues** (the same perp funding paying differently on Binance vs Bybit vs Hyperliquid), which is slow-moving and capital-rewarded rather than speed-rewarded. That is section 1, not this section.

---

## 5. Momentum / trend-following — **PARTLY DECAYED, and the decay is regime-shaped**

**Time-Series and Cross-Sectional Momentum in the Cryptocurrency Market** (AUT) — https://acfr.aut.ac.nz/__data/assets/pdf_file/0009/918729/Time_Series_and_Cross_Sectional_Momentum_in_the_Cryptocurrency_Market_with_IA.pdf

The finding that survives: **TSMOM produced negative annual returns through the choppy 2022–2023 regime**, while cross-sectional momentum (rank assets, go long-short) limited losses better because its market-neutral construction survives the absence of a trend. Recent work covering Jan 2020–Oct 2025 across eight majors still finds momentum economically meaningful, but the effect is now regime-conditional rather than unconditional.

- Tests passed: (5) trivially reproducible on free daily OHLCV. That is one. **These are papers, and by your own filter they do not qualify.**
- Caveat, and this is the important one: crypto TSMOM is the most academically over-published and practically fragile item on your list. Every backtest you will find applies no funding cost to the perp leg — and holding a levered long perp through a positive-funding regime costs you the very 11%/yr that section 1 is trying to earn. **Momentum backtests that ignore funding are not backtests.** If you build one thing here, build the funding-inclusive version; it will look materially worse than every published result, and that gap is the honest answer.
- **Capital:** low, $5k+. **Latency:** none. **Solo-viable:** yes, trivially. Which is precisely why the edge is thin.

---

## 6. MEV and on-chain — **DECAYED to the point of inaccessibility for a solo person. Do not spend time here.**

**Measuring CEX-DEX Extracted Value and Searcher Profitability** — https://arxiv.org/html/2507.13023v1

The most decisive evidence on this list. Aug 2023 – Mar 2025, 7.2M arbitrage transactions, $233.8M extracted:

- Wintermute, SCP and Kayle captured ~73% of total extracted value, rising to **~90% by Q1 2025**, with smaller competitors exiting.
- Wintermute and SCP each transfer **~90% of arbitrage revenue to their integrated builders** (rsync, beaverbuild) to buy auction priority — a subsidy you cannot match.
- Leaders execute $10,000+ trades with minimal slippage; smaller players are confined to <$5,000, and the median per-trade profit for integrated searchers "rarely exceeds $5."
- One tracked searcher, Graves, ran at **−272.1% margin.** People are losing money at this in size.

Corroborating structural facts: labelled active searchers fell to 11 by Q1 2025 with 3 taking 90% of volume; Titan alone built ~50% of Ethereum blocks by May 2026.

- Tests passed: (2) explicitly quantifies the cost side (builder payment as % of revenue); (4) names exactly where the technique stops working, for whom, and why; (5) on-chain, fully reproducible.
- Caveat: it is a measurement paper, not a how-to. It will not teach you to build a searcher. It will save you six months of trying.

**Verdict:** you cannot reach this. The barrier is not skill, it is the integrated-builder relationship, and that is a commercial arrangement, not an engineering problem.

---

## 7. Volatility harvesting / rebalancing premium — **RETAIL FOLKLORE. The most misunderstood item here.**

**Witte, "Volatility Harvesting: Extracting Return from Randomness"** — https://arxiv.org/pdf/1508.05241

Read it to get the maths right, then stop. Shannon's Demon shows that rebalancing between a zero-drift volatile asset and cash produces positive log growth. The universal retail error is reading this as free alpha. It is not: the "rebalancing bonus" is the difference between arithmetic and geometric mean, i.e. you are being paid for **selling variance and providing liquidity**, which means the payoff is short-gamma and mean-reversion-dependent, and it inverts in a trending market. Shannon himself never traded it meaningfully.

In crypto specifically it fails twice over: taker fees on every rebalance, and the fact that BTC's realised drift has historically dominated the harvest term — meaning the strategy has mostly been an expensive way to underperform holding. And note the structural conflict with section 5: volatility harvesting and trend-following are the same bet in opposite directions. Running both without an explicit regime allocator is paying two spreads to hold no position.

The one honest version of this idea is the **delta-hedged short-gamma book in section 2**, where you at least get paid an explicit, measurable variance risk premium for the exposure instead of stumbling into it.

- **Capital:** any. **Solo-viable:** yes, and that is the problem.

---

## Ranked, for your situation specifically

1. **Deribit vol surface work → cross-venue skew dislocation (Deribit vs IBIT).** Your SVI/SSVI implementation is directly reusable, the free monthly Tardis snapshots let you start today, and the Kaiko finding points at a structural dislocation with no published tradeable study. Highest edge-per-hour for you, and the least crowded.
2. **Funding carry, built to survive Oct 10 2025.** Start from the Hummingbot script, read its double-fill issue first, and make ADL your primary stress scenario rather than a footnote.
3. **hftbacktest as infrastructure, regardless of strategy.** Even if you never run MM, having a queue-aware, latency-aware fill simulator makes every other backtest you write honest — including the Indian index options work.
4. Momentum — only with funding costs in the P&L. Expect the result to be disappointing and treat that as the finding.
5. Ignore MEV, cross-exchange latency arb, AMM LPing, and volatility harvesting.

## Two structural warnings

**Crypto backtests fail differently from equity backtests.** The two errors that invalidate almost every crypto result you will read are (a) omitting perp funding from any levered directional hold, and (b) marking options at mark price on a venue where the fee is capped at 12.5% of premium. Both were present in sources otherwise worth reading, including Deribit's own.

**Nothing here has an ADL analogue in Indian index options.** The single largest difference between the crypto book and the NIFTY book you are building is that a crypto exchange can unilaterally close the profitable leg of your hedge. Whatever risk framework you carry over from the index work will not model this, and October 2025 is the proof.

## PAID — worth considering later

Nothing on this list requires a paid course. Two genuine data costs, neither urgent:

- **Tardis.dev full historical Deribit options / Binance L2** (~$200+/mo). Free first-day-of-month CSVs are sufficient for prototyping; only pay once your surface pipeline works.
- **Amberdata / Kaiko institutional feeds** — only relevant if you pursue the Deribit-vs-IBIT skew dislocation seriously, and likely available through IIT Kharagpur's institutional access before you pay retail.