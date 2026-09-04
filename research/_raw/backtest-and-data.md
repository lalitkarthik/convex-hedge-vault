# (A) Options backtesting that doesn't lie

## A1. The single most useful artifact: a peer-reviewed 0DTE paper that died when its cost model was fixed

**Vilkov — `0dte-strategies` replication package** — https://github.com/vilkovgr/0dte-strategies
Grigory Vilkov (Frankfurt School), one of the few options academics who ships his replication code. Full pipeline: `python code/run_replication.py` reproduces every table and figure from the paper.

The reason this is item #1: an **August 2026 correction notice on the repo** states a unit-scale error charged the bid-ask half-spread at 1/100 of its true size — about **0.022 bp instead of 2.2 bp**. After the fix, *no strategy or basket retains a positive net Sharpe*. A published, peer-reviewed, code-shipping 0DTE result was entirely a decimal point in the cost model.

Passes (1)(2)(3-adjacent)(4, doubly — the author documented his own falsification)(5).
Caveat: raw inputs are proprietary Cboe/ThetaData; only interpolated panels ship. You can read the method, not re-derive it from scratch for free. Also: this is the strongest available evidence that **the 0DTE literature is crowded and fragile** — treat every 0DTE result you read as unproven until you see its half-spread in basis points.

## A2. Bias taxonomies worth actually working through

**Susan Potter — "A Taxonomy of Backtest Lies"** — https://www.susanpotter.net/quant/backtest-bias-taxonomy/
Verified background: risk modelling and market-data infrastructure at BNP Paribas, BofA, Citadel. Gives three families (data / methodology / reporting), code snippets for automated checks, the pandas index-alignment look-ahead trap specifically, and a scorecard producing a de-biased Sharpe estimate plus notes on wiring the audit into a pre-deploy pipeline.
Passes (1)(3)(4).
Caveat: **contains nothing options-specific.** No assignment, no margin, no expiry settlement, no chain staleness. Use it as the equities-grade floor, not the ceiling.

**Bailey & López de Prado — Deflated Sharpe Ratio** — https://www.davidhbailey.com/dhbpapers/deflated-sharpe.pdf (free full text; SSRN 2460551), and **Probability of Backtest Overfitting / CSCV** — https://sdm.lbl.gov/oapapers/ssrn-id2507040-bailey.pdf
Blunt assessment: DSR is academically popular and practically half-useless, because it requires *N*, the number of trials, and nobody honestly reports their own *N* — including the people citing DSR. **PBO via CSCV is the one you should actually implement**: it splits the backtest into S combinatorial train/test partitions and reports the probability that your IS-best configuration ranks below median OOS. It needs no *N* and it is computable from the artefacts you already have.
Passes (4)(5). Caveat: CSCV assumes your configurations are comparable and your returns series are aligned; it says nothing about whether your *fills* were real. It catches selection lies, not execution lies. Both failure modes are live in options.

**Sinclair, on the Outlier podcast / gvol podcast** — https://outliertrading.substack.com/p/euan-sinclair-on-quant-vs-retail-529 · https://amberdataderivatives.substack.com/p/gvolio-podcast-ep-8-euan-sinclair
He has actually run the book (Bluefin, now Hull Tactical). Two numbers worth internalising: a daily-hedged short straddle at **$0.10/share hedging cost differs from the costless-hedge version by roughly two volatility points** — i.e. your cost model is as big a lever as your entire vol forecast. And his line on backtesting: everyone cross-validates, walks forward, goes out of sample, and still finds something, *because they looked at so many things*.
Passes (2)(3)(4). Caveat: audio, no code, no reproducible numbers.

## A3. Open-source options backtesters — specific verdicts

**Trustworthy-with-work: QuantConnect LEAN** — https://github.com/QuantConnect/Lean
Real event-driven engine, real reality-modelling layer, source-readable option pricing (`Common/Securities/Option/QLOptionPriceModel.cs`). But read their own docs before trusting it: the **default fill model does not consider size or volume** (https://www.quantconnect.com/forum/discussion/6981/), and their Greeks/IV come from a QuantLib BSM that **admittedly diverges from vendor IVs**, with a fallback approximation when American-with-discrete-dividend has no closed form (https://www.quantconnect.com/docs/v2/writing-algorithms/securities/asset-classes/equity-options/greeks-and-implied-volatility/key-concepts).
Passes (1)(2)(4). Caveat: out of the box it will fill you at prices no one would give you; you must write a custom fill model. **It has no meaningful Indian options support** — for NIFTY/Sensex you are writing your own engine regardless, so use LEAN as a design reference for the reality-model separation, not as your runtime.

**Usable, honest about itself, wrong resolution: optopsy** — https://github.com/goldspanlabs/optopsy
Better than its reputation: it does model commissions (per-contract / base / min) and slippage (mid, spread, liquidity-based, per-leg). Its README disclaims exactly the right things: liquidity constraints, execution slippage, **assignment risk**.
Passes (1)(2)(4). Caveats, and they matter: no margin model, no assignment model, chain-snapshot oriented rather than intraday, and the project is **forked across three orgs** (`michaelchu`, `goldspanlabs`, `foxbupt`) — a reliable signal of abandonment. Use it to screen structures on EOD chains; do not use it for anything you intend to trade at minute resolution.

**Actively misleading if used for options — name them:**
- `vectorbt` / `backtesting.py` / `backtrader` with an option chain bolted on. None are options engines. Vectorised frames make look-ahead free and silent, none of them carry a contract-lifecycle or assignment concept, and `backtrader` has no options support at all despite endless blog posts pretending otherwise.
- **AlgoTest, Sensibull, Opstra, NiftyTrader/StockMojo simulators.** Closed engines, undisclosed fill assumptions, product funnels. As evidence they are worth zero; as a *cross-check on your own chain reconstruction* (does my strike list on 2024-03-14 match theirs?) they are mildly useful.
- **Zerodha's "In The Money" backtests** and Marketcalls-branded strategy content. Zerodha's business is order flow; Marketcalls' business is education. Per your own filter these are auto-rejects as sources of conclusions. The *code* under Marketcalls is a different matter — see B3.

**Genuinely trustworthy, wrong asset class, right philosophy: hftbacktest** — https://github.com/nkaz001/hftbacktest
Rust+Python. Reconstructs the book from L2 MBP and L3 MBO feeds, models **feed latency and order latency separately**, and simulates fills using **queue position** with a pluggable queue model (`src/backtest/models/queue.rs`), with worked Binance Futures market-making examples.
Passes (1)(2)(4)(5). Caveat: **no options support** — it is futures/perps. Its value to you is as the reference implementation of what an honest fill simulator looks like, and as the tool for the crypto leg of your work. It is also the concrete demonstration of why 1-minute options bars cannot answer passive-fill questions.

## A4. How practitioners actually check the backtest isn't lying

In descending order of how much they catch, in options specifically:

1. **Re-price the whole backtest at three cost levels: mid, mid±25% of half-spread, and full-spread-crossing.** If the sign of PnL changes, you have a cost-model result, not a strategy. This is the Vilkov failure, and it is the modal failure.
2. **Timestamp-shift test.** Move every entry and exit ±5, ±15, ±30 minutes. A real edge degrades smoothly. A microstructure artefact or a look-ahead bug falls off a cliff. Daily-bar backtests cannot run this test at all — this is one thing your minute data buys immediately.
3. **Quote-staleness audit before any PnL is computed.** Per strike per minute, compute time since the quote last changed and spread as % of mid. Recompute the backtest excluding any leg whose quote was stale > k minutes at decision time. The delta between the two runs is the size of your lie.
4. **Live-vs-backtest reconciliation on paper fills**: run the strategy forward, log *your intended* price and the market's next-print price, and track the distribution of the gap. After ~200 fills you have an empirical slippage model that replaces every guess in the backtest. Nothing else substitutes for this.
5. **CSCV/PBO over your configuration grid** (not DSR, per A2), plus walk-forward with a re-fit cadence that matches how often you'd actually re-fit in production — including the fit *cost* in the OOS window.
6. **Assignment and settlement replay** as a separate unit test, not part of the strategy loop: force expiry-day paths through the settlement rule and verify cash matches by hand for a few dates.

---

# (B) Spending the minute-resolution advantage

## B0. First, verify what you actually received — this decides everything below

Ask the vendor one question: **is each 1-minute bar OHLC of the last traded price, or does it carry a best bid / best ask snapshot?** Most Indian "1-minute options data" is **LTP-only**. If so, for any strike outside the few liquid ones the "price" in a bar can be a trade from minutes ago, arbitrarily far from the live quote, and **every fill assumption you build on it is fiction**. LTP-only minute data is still excellent for realized-variance and timing work (B4 items 1, 3, 5) and nearly useless for fill-sensitive work. Do not proceed until you know which you have.

## B1. Tractable at 1-minute vs. requires tick/L2

**Tractable at 1-min:** time-of-day realized-variance seasonality; intraday VRP; intraday surface dynamics (SVI/SSVI refit per minute); discrete delta-hedging error and gamma-scalping PnL; entry/exit-timing sensitivity; expiry-day pin behaviour; synthetic-forward vs futures basis; regime/event studies around 09:15–09:30 and 15:00–15:30.

**Not tractable at 1-min — needs L1-with-timestamps at minimum, L2 properly:** passive fill probability, queue position, adverse selection on resting orders, effective vs quoted spread, order-book imbalance signals, market making, anything holding < ~10–15 minutes. `hftbacktest`'s queue model exists precisely because this cannot be faked from bars.

**Working rule:** at 1-minute resolution, only backtest strategies that **cross the spread on entry and exit and hold ≥ 15 minutes**. Everything else is a guess wearing a Sharpe ratio.

## B2. Storage — pick this and stop thinking about it

Full NIFTY + Sensex option chains at 1-minute for several years is **tens of GB compressed**, not terabytes. That is small. Consequently:

- **Hive-partitioned Parquet on local disk + DuckDB as the query engine.** Partition `date=YYYY-MM-DD/underlying=NIFTY/`, sort within file by `(expiry, strike, right, ts)`, ZSTD. DuckDB queries Parquet directly and keeps peak memory bounded (~2.5 GB while scanning ~2 TB in published benchmarks: https://www.codecentric.de/en/knowledge-hub/blog/duckdb-vs-polars-performance-and-memory-with-massive-parquet-data). Use Polars or DuckDB SQL for transforms. **Do not use DuckDB's native `.duckdb` file as your system of record** — its on-disk format is not stable across versions; keep Parquet as truth.
- **ArcticDB** (https://docs.arcticdb.io/4.5.0/faq/, `man-group/ArcticDB`) is real, Man Group-built, works on LMDB locally as well as S3, and gives you bitemporal versioning, daily appends and historical corrections. That versioning is its only argument over Parquet, and it is a genuine one — vendor restatements of options data are common. But it is **last-writer-wins with no transaction isolation**, and versions cost storage. **Verdict: not worth it at your scale.** Adopt it only if you start receiving daily corrections you must audit.
- **kdb, ClickHouse, QuestDB, TimescaleDB: no.** They are the right answer at tick/L2 scale on a shared team feed. At single-researcher minute scale they are a second job, which is the thing you said you didn't want.
- **The piece everyone skips and everyone gets burned by:** a separate `contract_meta` table with `valid_from` / `valid_to` — lot size, tick size, expiry date, strike interval, index divisor. Never join on lot size as a constant. See B3.

## B3. Indian option-chain traps, specifically

- **Lot size changes are point-in-time facts, not constants.** NIFTY has moved 75 → 65 effective end-Oct 2025, BANKNIFTY 35 → 30, with a further index-derivative lot revision from **30 December 2025** (https://zerodha.com/marketintel/bulletin/429705/revision-in-lot-size-of-index-derivative-contracts-from-december-30-2025). A backtest that applies today's lot size to 2023 positions misstates every notional, every margin, and every per-lot cost.
- **Expiry day changed twice in recent history.** Weekly expiries on all indices except one benchmark were **withdrawn from 20 November 2024** (Bank Nifty, FinNifty, Midcap weeklies gone), and from **September 2025 NSE moved all expiries to Tuesday while BSE moved to Thursday** (https://www.venturasecurities.com/blog/changes-in-expiry-nse-and-bse/). Any day-of-week feature, any "expiry day" flag, and any DTE calculation must be derived from the contract master, never from a weekday rule. Cross-index expiry-day studies spanning 2024–2025 are comparing different market structures and are close to meaningless unless you regime-split.
- **Illiquid wings quote garbage.** Published practitioner spread estimates: ATM ₹1–3, OTM ₹5–15, with ≥₹2/lot/leg slippage even on liquid strikes (https://docs.openalgo.in/skills/backtesting). On far wings the quoted spread routinely exceeds the option's value. Enforce a hard filter — drop legs with spread > X% of mid, or with zero volume in the bar — *before* the strategy sees the chain, and report how many candidate trades the filter killed.
- **Forward, not spot.** Compute IV against the **synthetic forward from put-call parity per minute** (or the futures price), never against the index spot. India's index carry is non-trivial, dividends are lumpy, and using spot puts a fake skew in your surface that your SSVI fit will faithfully reproduce and you will then trade.
- **Expiry-day settlement mechanics.** Index options are cash-settled against the index close, and **STT on exercised ITM options is charged on intrinsic value (0.125%)**, which is a large, asymmetric, frequently-omitted cost that specifically penalises held-to-expiry short-premium backtests. **Could not verify in this session:** the exact NSE/NSE Clearing wording on whether the final settlement value uses the last-30-minute weighted average of the index — the NSE Clearing pages I hit stated only "closing price of the underlying." Read the NSE Clearing equity-derivatives settlement page directly (https://www.nseclearing.in/clearing-settlement/equity-derivatives/settlement-mechanism) before hard-coding a settlement rule; this single line decides the PnL of every expiry-day strategy.
- **Useful open code, dubious surrounding content:** `marketcalls/openengine` and OpenAlgo (https://github.com/marketcalls/openengine, https://docs.openalgo.in/skills/backtesting) are genuinely open source, broker-agnostic, and publish explicit Indian cost breakdowns (₹20/order, STT, exchange charges by segment). Passes (1)(2)(5). Caveat, stated plainly: the surrounding organisation sells education, so read the *cost tables and the code*, ignore the strategy claims.

## B4. Edges that only exist at minute resolution — where your advantage is actually spent

1. **Time-of-day-adjusted realized variance vs. remaining implied variance.** Intraday volatility is strongly U-shaped and the standard treatment is a multiplicative decomposition into a deterministic Fourier seasonal component and a stochastic factor (https://arxiv.org/pdf/2111.02376). Daily data cannot tell you that 1-minute RV of 12% annualised is *high* at 12:30 and *low* at 09:20. Deseasonalise RV, compare against the option's implied variance over its **remaining life only**, and you have an intraday VRP signal for expiry-day and next-day ATM structures. This is the highest-value first project: it uses machinery you already have and is invisible in EOD data.

2. **The intraday IV diurnal pattern itself is an execution edge before it's a strategy.** Documented: both calls and puts show lowest IV at the open with call IV drifting to a peak at the close (https://www.mdpi.com/1911-8074/17/1/39). Even if you never trade it directionally, it means "sell premium" backtests that fill at the close are systematically flattered and "buy premium at open" backtests systematically hurt — a bias that daily-bar work cannot even detect, let alone remove.

3. **Timing decomposition of any existing daily strategy.** Take any published Indian short-premium or calendar result, re-run it at every minute of the day, and plot PnL vs entry time. In almost every case the majority of the "edge" concentrates in two 15-minute windows, which tells you it is a microstructure artefact rather than a risk premium. This is a falsification tool that daily data physically cannot provide, and it will kill more of your ideas than anything else you build.

4. **Honest gamma-scalping and hedge-error estimation.** The variance of short-gamma PnL depends almost entirely on hedge frequency; daily-bar backtests silently assume one hedge per day and thereby overstate short-straddle Sharpe. With minute data you can compute the actual hedge-error distribution as a function of rebalance interval and threshold, and price the trade-off against Sinclair's finding that realistic hedging cost ≈ two vol points. **This is the single most decision-relevant thing minute data gives an options book.**

5. **Per-minute SSVI refits — the direct extension of work you have already done.** Fit the surface every minute and track (a) the time constant of smile relaxation after a jump, (b) intraday ATM-skew mean reversion, (c) **persistent no-arbitrage violations**. Violations lasting one or two minutes are stale quotes and give you a free, model-based staleness detector (see A4.3). Violations persisting longer are either a real calendar/butterfly trade or a data defect — and distinguishing them is exactly the kind of thing that is tradeable and that nobody with daily data can even look at. India's expiry-day chains, with the deepest short-dated liquidity in the world, are the best dataset on earth for this.

6. **Expiry-day pin and terminal-hour structure.** Elevated realized vol and dealer-gamma effects in the final hour of expiry are structurally adverse to short premium, with the documented edge sitting in *earlier* windows — a distinction that exists only at intraday resolution. Indian Tuesday/Thursday expiries give you two independent weekly samples of this per week across two exchanges.

7. **Synthetic forward vs futures, per minute.** The put-call-parity forward and the futures price should track. When they diverge, one of your three inputs (call quote, put quote, futures quote) is stale. This is a cheap, continuous data-quality monitor and occasionally an actual box-spread/conversion signal. Impossible at daily resolution because everything is synchronised at the close by construction.

## B5. Crypto (do this second, but design for it now)

- **Free Deribit history:** all instruments including every option since 2019-03-30; **first-day-of-each-month CSVs downloadable without an API key** (https://insights.deribit.com/exchange-updates/celebrating-our-tardis-dev-partnership-get-free-historical-data/, https://docs.tardis.dev/historical-data-details/deribit). Plus free Deribit options OHLCV by maturity, futures, funding and DVOL CSVs at https://www.cryptodatadownload.com/data/deribit/. Passes (1)(5). Caveat: the free tier is one day per month — enough to *build and validate your pipeline and your fill model*, not enough to backtest. Plan the schema now so paid history later is a drop-in.
- **`hftbacktest`** (A3) is the honest engine for the crypto leg: latency + queue + fees. Use it for perp/futures hedging legs, and steal its fill-model architecture for your options engine.
- **The structural difference that matters:** crypto options are 24/7 with no auction, no settlement-print games, no lot-size regime changes — so the *Indian* traps mostly vanish, and are replaced by exchange concentration risk (Deribit is effectively the market), funding-rate/perp-basis interaction with the vol surface, and cross-venue latency. The intraday seasonality work in B4.1 is *weaker* in crypto (no open/close) but the DVOL-vs-realized VRP work transfers directly.

---

# What I could not verify

- Exact NSE final-settlement-price formula for index options (last-30-minute weighted average vs simple close). NSE Clearing pages returned only "closing price of the underlying." Verify from the circular before coding settlement.
- Whether López de Prado publishes a maintained free reference implementation of DSR/CSCV at quantresearch.org — search did not confirm it. The papers themselves contain complete pseudocode; implement from those rather than trusting a third-party package.
- I did not test-run any of the repos above.

---

# PAID — worth considering later (not part of the recommendations above)

- **Euan Sinclair, *Positional Option Trading* (Wiley, 2020)** and ***Volatility Trading* 2nd ed.** — the cost-model discipline in A2 comes from here, and there is no free equivalent for the "how much does hedging cost actually change the answer" material. Check IIT KGP's Wiley Online Library access first; Wiley Trading titles are sometimes inside institutional packages, in which case this is free to you.
- **Sinclair & Mack, *Retail Options Trading* (2024)** — narrower, more implementation-oriented.
- **ThetaData / Massive** (US options intraday), **Tardis.dev** (crypto full history) — data, not education. Only relevant once your pipeline is proven on the free monthly Deribit slices and your Indian feed.