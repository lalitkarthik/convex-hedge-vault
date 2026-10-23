# Options backtest engines: how they model what makes options different

> Lane `options-backtesters.md` of the 2026-10-16 options-harness sweep ([brief](_brief.md)). Raw research capture, staging, not fact. Nothing here is promoted to `domain/`.

**Read marks.** `[full]` = I read the README or doc page in full. `[part]` = I read search highlights or selected source files only. `[summary]` = I read the page through a fetch summariser, not the text itself. Sources were read on 2026-10-16.

**Not repeated here.** How dashboards compute IV, RV and IV percentile (Sensibull, Opstra, AlgoTest VRP, ORATS fields) is in [research-dashboards.md](../2026-10-06-iv-vs-rv-research/research-dashboards.md). The cost-unit bug in Vilkov's 0DTE package and the "never fill at mid" advice are in [papers-tooling.md](../2026-10-07-research-pipeline/papers-tooling.md) and [pipeline.md](../2026-10-07-research-pipeline/pipeline.md).

## In one page

A stock engine holds one price series per symbol. An options engine holds a **chain**: for each time step, a grid of strike × expiry × call/put, each cell with a bid, an ask and Greeks. The contracts in the grid are born and die. Every engine below solves the same five problems in a different way: which cell to pick (by delta, by strike offset, by premium), which price to fill at (mid, bid/ask, or a fraction of the spread), where the Greeks come from (vendor column or own solver), what happens at expiry (settlement price, exercise, assignment) and how much capital a short position ties up (margin).

Three findings matter most for us. First, **the fill model is the most copied idea**: ORATS charges 75% of the bid-ask width for one leg, falling to 53% for four legs, and optopsy reproduces the same table. Second, **expiry is where engines are weakest**: LEAN settles every option at the underlying close (an open bug for AM-settled SPX), Option Omega values expiring legs at the 16:00 quote, optopsy exits at the last daily quote, and Databento's OPRA definitions stamp expiry at midnight UTC, so a naive loader kills the contract before its last session. Only small newer projects settle against the official index print. Third, **two commercial engines and one open-source engine already expose themselves to agents through MCP** (Option Omega, QuantConnect, optopsy-mcp), and ORATS has a clean job-based REST API with diagnostics. Their tool shapes are a ready template for our backtester station.

For NIFTY the tooling is thinner. Indian backtesters (AlgoTest, bhav) fill on traded 1-minute OHLC, not on bid/ask, and add a flat percentage as slippage. Margin is solvable offline: the NSE Clearing SPAN file carries a 16-scenario risk array per contract, and `marginism` computes SPAN from it. The rules changed often in 2024 to 2026 (weekly expiries, expiry day, lot size, STT), so a NIFTY engine must read these as dated tables, not constants.

## The engines

### optopsy and optopsy-mcp (open source, Python and Rust)

**What it is.** A Python options backtest library, AGPL-3.0, about 1,500 stars ([repo](https://github.com/michaelchu/optopsy) `[full]`), plus a 2026 Rust rewrite served as an MCP server ([optopsy-mcp](https://github.com/goldspanlabs/optopsy-mcp) `[full]`, 15 stars, created 28 Feb 2026, "breaking changes … may occur").

- **Chain.** A long table, one row per quote date × expiration × strike × type, with bid, ask and a **required delta column** ([parameters](https://goldspanlabs.github.io/optopsy/parameters/) `[full]`). Greeks come from the vendor; the library does not solve IV.
- **Fills.** Four modes: `mid`, `spread` (buy at ask, sell at bid), `liquidity` (volume-scaled), and `per_leg`, where the fill ratio grows by 0.073 per extra leg. Its own doc shows this gives 75%, 68%, 60%, 53% of the edge kept for one to four legs: the ORATS table, below.
- **Expiry.** In the Python source, a trade exits at the row whose DTE equals `exit_dte`; the default 0 means the last quote on expiry day (`optopsy/evaluation.py`, read in a downloaded copy `[part]`). I found no settlement against an index print and no margin model.
- **Strategies.** 38 named functions (verticals, condors, calendars, diagonals), each leg picked by a delta `TargetRange(target, min, max)`. Results are grouped by DTE bucket × delta bucket by default, which is close to our bucket method.
- **Agent interface.** optopsy-mcp exposes `backtest` (single run or grid/Bayesian sweep), walk-forward, permutation test, block-bootstrap Monte Carlo and `generate_hypotheses` "with FDR correction". Strategies are **Rhai scripts in a sandbox with no file or network access**. Data is Parquet with a `datetime` column, so intraday quotes load.

**Take:** the per-leg fill formula, the sandboxed strategy script, and the MCP tool list as a template. **Does not fit:** vendor delta is required, expiry exits at a quote, and AGPL means we must not copy its code into our engine.

### QuantConnect LEAN (open source engine, commercial cloud and data)

**What it is.** The largest open-source event-driven engine (C# core, Python API). Options are a first-class asset class.

- **Chain.** A canonical option symbol plus a universe filter (`Expiration(0, 0)`, `Strikes(-3, 3)`, delta filters) produces an `OptionChain` in each data slice. SPXW is its own ticker and has its own minute files ([index option universes](https://www.quantconnect.com/docs/v2/writing-algorithms/universes/index-options) `[part]`).
- **IV and Greeks.** A per-contract price model: Black-Scholes for European, Cox-Ross-Rubinstein binomial for American. New indicator-based models arrived on 19 Feb 2026; the old QuantLib models stay under `OptionPriceModels.QuantLib` ([pricing](https://www.quantconnect.com/docs/v2/writing-algorithms/reality-modeling/options-models/pricing) `[full]`). Greeks in a chain request are the **previous day's end-of-day values**; only Greeks in the data slice come from the model. The IV source ([ImpliedVolatility.cs](https://github.com/QuantConnect/Lean/blob/master/Indicators/ImpliedVolatility.cs) `[part]`) solves with Brent's method between 1e-7 and 4.0, uses the out-of-the-money side of the call/put pair when a mirror contract is given, and **on failure logs an error and returns 0**. Time to expiry is calendar days / 365 ([helper](https://github.com/QuantConnect/Lean/blob/master/Indicators/OptionGreekIndicatorsHelper.cs) `[part]`).
- **Expiry.** The settlement time is right: 0DTE PM-settled index options expire at 16:00 ET, AM-settled ones at the next open ([OptionSymbol.cs](https://github.com/QuantConnect/Lean/blob/master/Common/Securities/Option/OptionSymbol.cs) `[part]`). The settlement price is not: "All options use the close of the underlying", open since Jan 2024 ([issue 7728](https://github.com/quantconnect/lean/issues/7728) `[full]`), and the exercise price changes when extended hours are on ([issue 8050](https://github.com/QuantConnect/Lean/issues/8050) `[full]`).
- **Assignment.** The default model scans each hour; it exercises a short European option on expiry day if it is 5% in the money and profitable after fees ([assignment](https://www.quantconnect.com/docs/v2/writing-algorithms/reality-modeling/options-models/assignment) `[full]`).
- **Fills and margin.** `ImmediateFillModel` is the default for options, with combo market and limit fills ([fills](https://www.quantconnect.com/docs/v2/writing-algorithms/reality-modeling/trade-fills/key-concepts) `[full]`). The page does not say at which side of the quote an option fills; not verified. Margin uses `OptionMarginModel` plus position groups, so a bull call spread needs $0 rather than $130,649 ([buying power](https://www.quantconnect.com/docs/v2/writing-algorithms/reality-modeling/buying-power) `[full]`).
- **Agent interface.** An official MCP server with `create_project`, `create_compile`, `create_backtest`, `read_backtest`; the remote server needs a paid node ([MCP key concepts](https://www.quantconnect.com/docs/v2/ai-assistance/mcp-server/key-concepts) `[part]`). `lean data download` buys SPXW minute quotes at $0.15 per ticker-day per data type ([CLI datasets](https://www.quantconnect.com/docs/v2/lean-cli/datasets/quantconnect/index-options) `[part]`).

**Take:** pluggable models per concern (price, fill, assignment, exercise, margin) and position-group margin. **Does not fit:** the silent IV = 0 on solver failure is our known "signal that became a default" defect; settlement at the underlying close is wrong for AM SPX and for NIFTY.

### ORATS backtester and Intraday Backtester API (commercial, US)

**What it is.** A hosted backtester on ORATS data. The end-of-day version uses quotes **14 minutes before the close**, because ORATS finds quotes decay in the last minutes ([methodology](https://orats.com/university/backtesting-methodology) `[part]`).

- **Fills.** Buy at `bid + (ask − bid) × s`, sell at `ask − (ask − bid) × s`, with s = 0.75, 0.66, 0.56, 0.53 for one to four legs ([methodology](https://docs.orats.io/backtest-api-guide/backtester-methodology.html) `[full]`). Positions are marked at mid between trades ([common questions](https://orats.com/blog/answers-to-common-questions-backtesting) `[part]`). One ORATS blog says 56% for four legs ([50 million backtests](https://orats.com/blog/behind-the-scenes-of-over-50-million-options-backtests) `[part]`); the API docs say 53%.
- **Returns.** Daily return = option P&L ÷ stock price at entry; annual return is the **sum** of daily returns, not compounded, because "compounding returns create special problems in option trading".
- **Intraday API.** One-minute data from 1 Oct 2020, 18 strategies, legs set by delta band and DTE band, where DTE 1 = same day ([Intraday Backtester API](https://orats.com/docs/intraday-backtester-api) `[full]`). It has an `expiryTod` filter for AM- or PM-settled expirations, a `badPriceFilter` that skips markets wider than 5% of strike or 15% of mid, and signal-driven entries as a list of timestamps. Runs are jobs: submit, poll, fetch. Results carry `diagnostics` counters (entry days with no match, no chain) and an `effectiveConfig`, and the docs warn that "a summary of zeros means the legs matched nothing, not that the strategy broke even".
- **Gaps.** The settlement price used at expiry and the margin formula are not documented ([summary](https://orats.com/docs/intraday-backtester-api) `[summary]`). The strategy *label* picks the margin model, so the same legs under two labels give two margin figures.

**Take:** the leg-count spread table as our default cost, `effectiveConfig` and diagnostics in every result, the bad-price filter, and the job API shape. **Does not fit:** US only; no NIFTY.

### Option Omega (commercial, US, 0DTE focus)

**What it is.** A hosted backtester popular for SPX 0DTE. It uses OPRA bid/ask at one-minute resolution from 2013, fills at **mid by default**, and lets the user add slippage per position ([FAQ](https://docs.optionomega.com/backtesting-faq) `[full]`; [setup](https://docs.optionomega.com/backtesting/backtest-setup) `[part]`).

- **Data rules.** SPX means PM expirations only. The first options datapoint is 9:32, "since the previous two minutes are too noisy". Daily SPX expirations start in May 2022. DTE counts calendar days, so a 1 DTE trade cannot exist on a Friday.
- **Stops.** For SPX/SPY 0DTE, the intra-minute stop (IMSL) checks the stop against **1-second mids**; all else runs on 1-minute mids.
- **Greeks.** Black-Scholes, with IV from the data vendor ([OO FAQ](https://optionomega.com/faq/) `[part]`).
- **Expiry.** An expiring cash-settled leg is "reported at the position's actual price at 4:00 PM … without incorporating closing fees or slippage". That is the 16:00 quote, not the official settlement value.
- **Agent interface.** An MCP server at `mcp.optionomega.com` builds, runs, sweeps and compares backtests, with a daily run limit ([MCP](https://docs.optionomega.com/backtesting/advanced-options/mcp) `[full]`). The doc itself warns: "If you try several variants and keep the best one over a short window, the result is probably flattering."

**Take:** sub-minute stop checks, a "first usable minute" rule, per-agent run budgets. **Does not fit:** mid fills by default, the 16:00 quote as settlement.

### NautilusTrader (open source, Rust core, Python API)

**What it is.** A high-performance event-driven engine. First-class option chains landed in 2026 ([PR 3677](https://github.com/nautechsystems/nautilus_trader/pull/3677) `[part]`; [options guide](https://github.com/nautechsystems/nautilus_trader/blob/develop/docs/concepts/options.md) `[full]`).

- **Chain.** One `OptionChainSlice` per series (venue, underlying, settlement currency, expiry). Strikes are selected by `StrikeRange`: fixed, N above/below ATM, a percent band around ATM, or a delta band. ATM comes from the **forward price**, which "eliminates spot-forward basis error by design".
- **Greeks.** Either venue-supplied `OptionGreeks` records replayed from the catalog, or a local Black-Scholes calculator with shocks and portfolio aggregation ([greeks guide](https://github.com/nautechsystems/nautilus_trader/blob/7a3b321e/docs/concepts/greeks.md) `[part]`). For OPRA we must compute and store Greeks ourselves.
- **Fills.** "Matching is quote-driven for options": market orders cross the replayed BBO; resting limits fill when the BBO trades through. No queue position.
- **Databento.** The adapter loads OPRA definitions and quotes ([Databento integration](https://nautilustrader.io/docs/latest/integrations/databento/) `[part]`). OPRA definitions carry expiry at **midnight UTC**, so "the matching engine then treats the contract as expired before its final trading session"; the loader moves it to 16:00 New York by default, but "cannot distinguish … AM-settled SPX versus PM-settled SPXW". Index definitions (class `I`) are not yet supported.
- **Margin.** Not found for options.

**Take:** forward-based ATM, the Databento expiry trap (it bites any loader of ours), config objects as the run definition. **Does not fit:** crypto-first examples; no option margin.

### lambdaclass options_portfolio_backtester (open source, Rust core)

**What it is.** An MIT-licensed portfolio backtester for options plus stock, aimed at tail hedges ([repo](https://github.com/lambdaclass/options_portfolio_backtester/) `[full]`). A 17-year SPY chain of about 22 million rows runs in about 4 seconds; a 100-config sweep runs in parallel in Rust.

- **Models.** Every part is swappable: contract selectors (`NearestDelta`, `MaxOpenInterest`), fill models (`MarketAtBidAsk`, `MidPrice`, `VolumeAwareFill`), cost models (`SpreadSlippage`), and pre-trade risk limits (`MaxDelta`, `MaxVega`, `MaxDrawdown`).
- **Accounting.** At each rebalance it sells every option at the bid (long) or ask (short) and buys fresh: "no stale option value carried across rebalances". Data is daily and needs a delta column.
- **Reproducibility.** The canonical SPY Parquet files are **pinned by SHA-256**, and `make verify-articles` re-runs every published table and asserts it matches.

**Take:** Greek-limit gates, data hashes, a test that re-runs published results. **Does not fit:** daily only, no expiry-day logic, US ETF focus.

### OptionSuite, backtrader and zipline forks, vectorbt

- **OptionSuite** is an event-driven Python framework with strangle and put-vertical primitives on iVolatility end-of-day CSVs; it was "tested with Python 2.7+" ([repo](https://github.com/sirnfs/OptionSuite) `[full]`). Too old to use; its split into data handler, strategy, portfolio and option primitive is ordinary.
- **backtrader** has no options. The [options_backtesting_framework](https://github.com/options-testing-org/options_backtesting_framework) `[summary]` adds an option chain and an `option_expired` event, but its README says nothing on fills, margin or Greeks. [IDontReallyCode/OptionsBacktesting](https://github.com/IDontReallyCode/OptionsBacktesting) `[part]` runs expiry before mark-to-market each step and turns ITM options into stock.
- **zipline-reloaded** has no options ([BacktestScore review](https://www.backtestscore.com/tools/zipline-reloaded) `[part]`; [QuantRocket forum](https://support.quantrocket.com/t/how-well-supported-is-options-trading/957) `[part]`). The **ZIPLIME** fork adds `option_chain()` that "defaults to today — the 0DTE chain", and `option_greeks` "raises when it doesn't [have IV], rather than inventing a volatility". It warns that near a 0DTE close almost every delta is 0 or 1, "so select by `strike_offset` there instead" ([ZIPLIME docs](https://docs.ziplime.limex.com/language/strategy-language/futures-options-bonds) `[full]`).
- **vectorbt** has no options; its author said so in 2022 ([discussion 346](https://github.com/polakowo/vectorbt/discussions/346) `[part]`). VectorBT PRO ships `.claude/skills` for agents ([vectorbt.pro](https://vectorbt.pro/) `[part]`). An article claims a `vbt.options` extension and an Option Omega Python SDK `opy` ([tutorsbot](https://tutorsbot.com/blog/python-options-trading-backtesting-2026) `[part]`); I found neither in any primary source, so treat both as false.

**Take from this group:** ZIPLIME's "raise, never invent a volatility" rule and its 0DTE strike-offset warning.

### Cboe benchmark indices (documented commercial method)

Cboe's BuyWrite indices are a published backtest method ([methodology](https://cdn.cboe.com/api/global/us_indices/governance/Cboe_BuyWrite_Indices_Methodology.pdf) `[part]`). The new call is "deemed sold" at the **VWAP of its trades** in a fixed window (BXM: 11:30 to 13:30 ET since 2010), after removing spread and late trades by OPRA condition code; with no trades it uses the last bid. The expiring call settles at the SOQ. **Take:** a fill rule that is a window average of real trades, with a stated fallback. **Does not fit:** monthly, AM-settled, one structure.

### Pricing libraries: QuantLib, vollib, py_vollib_vectorized

- **QuantLib** is a pricing library, not a backtester. It has analytic European, binomial and finite-difference engines, and the finite-difference engine "is capable of pricing both European and American payoffs" ([QuantLib-Python docs](https://quantlib-python-docs.readthedocs.io/en/latest/pricing_engines/options.html) `[part]`; [vanilla engines](https://www.quantlib.org/reference/group__vanillaengines.html) `[part]`). LEAN used it as its legacy model. It builds an object graph per contract, which is slow for a full chain each minute.
- **vollib** (formerly py_vollib) wraps Jäckel's *Let's Be Rational*, which implies Black volatility "with as little as two iterations to maximum attainable precision" ([repo](https://github.com/vollib/py_vollib) `[full]`). It covers Black, Black-Scholes, Black-Scholes-Merton with analytic and numeric Greeks. A zero strike raises `ZeroDivisionError`. Version 1.0.7 makes `vollib` the canonical name.
- **py_vollib_vectorized** patches py_vollib to take NumPy arrays and DataFrames, with numba ([repo](https://github.com/marcdemers/py_vollib_vectorized) `[full]`). This is the fast path for a chain per minute.
- **Bad quotes.** What each library does with a price below intrinsic value: not checked in this sweep.

**Take:** Let's Be Rational on Black-76 with the forward from put-call parity, vectorised over the chain. **Does not fit:** none of these handle bad quotes for us; that is our filter's job.

### India: data, backtesters, margin

- **opstrat** draws payoff diagrams from yfinance; it has no backtest ([repo](https://github.com/hashABCD/opstrat) `[full]`).
- **jugaad-data** downloads NSE F&O bhavcopies (end-of-day) and per-contract history through a CLI, with caching "to play nice with NSE" ([repo](https://github.com/jugaad-py/jugaad-data) `[full]`). **nsepython** wraps NSE's live REST APIs in local and server editions ([repo](https://github.com/aeron7/nsepython) `[full]`). Neither gives intraday quotes for expired contracts.
- **bhav** is an open-source NSE options backtester on Upstox's expired-instrument 1-minute candles ([repo](https://github.com/rajmaurya0904/bhav) `[part]`; [summary](https://github.com/rajmaurya0904/bhav) `[summary]`). It has an Indian cost model (STT on sales and exercised ITM, brokerage, exchange, SEBI, stamp, GST), a SHA-256 checksum of metrics per run, and a strategy generator that calls the `claude` CLI behind an AST gate that rejects `os`, `subprocess`, `eval` and network imports. Its README says the gate "is not a full sandbox". No SPAN yet; lot sizes are a single "Jan 2026 revision" table.
- **marginism** computes NSE SPAN offline from the NSCCL `.spn` file ([PyPI](https://pypi.org/project/marginism/) `[part]`; [repo](https://github.com/marketcalls/marginism) `[part]`). Each contract has "a precomputed 16-scenario risk array", so margin is arithmetic with no pricing model. It adds exposure margin and the 2% expiry-day ELM. Lot sizes are not in the file.
- **AlgoTest** backtests on **1-minute OHLC of traded prices**, not bid/ask ([trade monitoring](https://docs.algotest.in/execution-settings/trade-monitoring/) `[part]`). Leg stops use the candle high and low; strategy-level rules use the close. Its 9:20 candle covers 9:19:00 to 9:19:59 ([candle definition](https://docs.algotest.in/product-blogs/algotest-candle-defintion/) `[part]`). If entry and stop fall in one candle it "checks the close of the current candle" to decide ([strategies that don't work](https://algotest.in/blog/types-of-strategies-that-do-not-work/) `[part]`). There is "no default slippage"; staff suggest 0.5% to 1% ([forum](https://algotest.in/forum/d/476-trailing-sl-implementation-in-live-market) `[part]`).
- **Stockmock, Opstra, Sensibull.** I found no public method doc for Stockmock or Opstra. AlgoTest, a competitor, says Opstra backtests are end-of-day from 2016 and Sensibull has no historical backtest ([AlgoTest comparison](https://algotest.in/blog/best-backtesting-software-for-options-trading-in-india/) `[part]`). Weigh that source.

## Comparison

| Engine | Chain unit | IV and Greeks | Fill | Expiry and settlement | Margin | Intraday | Agent interface |
|---|---|---|---|---|---|---|---|
| optopsy | row per date × expiry × strike × type | vendor delta (required) | mid / spread / volume / per-leg % | exit at last quote on DTE 0 | none found | Rust version | MCP (Rust), Python API |
| LEAN | OptionChain per slice, filtered universe | BS or binomial model per contract; IV 0 on solver failure | ImmediateFill, combo orders | right time, price = underlying close (bug for AM) | OptionMarginModel + position groups | minute, second | MCP (paid node), CLI |
| ORATS | hosted | ORATS data | 75/66/56/53% of width; marks at mid | not documented; AM/PM filter | label-chosen, formula not documented | 1-min since 2020 | REST jobs + diagnostics |
| Option Omega | hosted | BS, vendor IV | mid + fixed slippage | 16:00 quote | yes, method not read | 1-min, 1-sec stops | MCP with run limit |
| NautilusTrader | OptionChainSlice per series | venue records or local BS | crosses replayed BBO | OPRA expiry fix to 16:00 | none found for options | tick | Python config objects |
| lambdaclass | daily chain | vendor delta | bid/ask, mid, volume-aware | liquidate at rebalance | Greek limits only | no | Python API |
| ZIPLIME | 0DTE chain per day | data IV or raise | not read | intrinsic value | not read | minute | Python API |
| Cboe BXM | one call per month | n/a | trade VWAP in a window | SOQ | n/a | window | published PDF |
| AlgoTest | strike by ATM offset, premium, delta | not read | traded 1-min OHLC + user % | not read | not read | 1-min | web UI |
| bhav | NSE 1-min candles | not read | candle, cost model | not documented | none yet | 1-min | CLI, Claude generator |
| marginism | SPAN file | risk arrays | n/a | expiry-day ELM | NSE SPAN + exposure | n/a | Python, CLI |

## SPXW 0DTE: the 4:00 pm settlement, PM against AM

**The two settlement prints.** A PM-settled SPXW option settles to a value "calculated using the closing sales price in the primary market of each component security on the expiration date"; an AM-settled standard SPX option settles to the SOQ, built from each component's opening price, and stops trading the day before ([Cboe SPX spec](https://www.cboe.com/tradable_products/sp_500/spx_options/specifications) `[part]`). Expiring SPXW trades until 3:00 pm CT (4:00 pm ET); non-expiring series trade until 4:15 pm ET. The SOQ fell outside the day's high-low range in about 30% of quarterly expirations, and its median distance from the same day's close was 0.13% from 2009 to 2024 ([Cboe AM settlement paper](https://cdn.cboe.com/resources/spx/Settlement_of_Standard_AM_Settled_SP_500_Index_Options.pdf) `[part]`). Cboe plans to stop AM-settled options trading at 9:25 am ET on expiry day, date to be set ([24/5 FAQ](https://www.cboe.com/document/tech-spec/document/technical-specifications/cboe-options-exchange-245-faq) `[part]`).

**What backtests do with it.** Four practices exist:

- **Last quote.** Option Omega values the leg at its 16:00 quote; a Quant Galore study priced the spread at its 15:59 close, then found a difference of about $20 per contract against the official settlement ([Quant Galore](https://www.quant-galore.com/p/the-raw-realities-of-quantitative) `[part]`).
- **Underlying close.** LEAN uses the underlying's close at delisting (issue 7728 above).
- **Official print.** A trading firm marks "every expired contract against the official settlement value, because that is what the broker will post" ([cashflowengine](https://cashflowengine.io/learn/spx-settlement/) `[part]`). FirmTape's replication of Vilkov settles "on the official SPX close" ([FirmTape](https://firmtape.com/research/vilkov-0dte-rules-replication) `[part]`).
- **Close early.** Option Omega's own 0DTE guide exits survivors at 3:50 pm "so nothing rides into settlement" ([OO blog](https://optionomega.com/blog/how-to-backtest-a-0dte-iron-condor-on-spx/) `[part]`).

**Data consequences for us.** The official SPX close is not in OPRA; it comes from the Cboe index feed (Nautilus lists `MAIN.CGIF` as the index source). OPRA definitions from Databento carry expiry at midnight UTC (Nautilus doc above). Half days settle at 13:00 ET; our feature experiments already dropped two such days because "the repo's chain maths counts every day to 16:00" ([results](../2026-10-08-feature-experiments/results.md)). Reg-T margin for an uncovered SPX option is 100% of proceeds plus 15% of index value less the out-of-the-money amount, with a 10% floor ([Cboe SPX spec](https://www.cboe.com/tradable_products/sp_500/spx_options/specifications) `[part]`).

## NIFTY: NSE rules a backtest must carry as dated tables

**Settlement.** Index options are European, exercised automatically, and settle in cash on T+1 at the "close price of the relevant underlying index" on expiry day ([NSE Clearing settlement price](https://www.nseclearing.in/clearing-settlement/equity-derivatives/settlement-price) `[part]`; [settlement mechanism](https://www.nseclearing.in/clearing-settlement/equity-derivatives/settlement-mechanism) `[part]`). The NIFTY close is "the last half an hour weighted average closing prices of the constituents" ([NIFTY Indices FAQ](https://www.niftyindices.com/resources/index-concepts/faqs) `[part]`). So **NIFTY settles to a 30-minute average, not the 15:29 bar**. A short strike that is in the money at 15:29 can settle out of the money, and the reverse.

**Weekly expiries and expiry day.**

- From 20 Nov 2024, each exchange may list weekly options on **one** benchmark index only (NSE kept NIFTY) ([SEBI circular, 1 Oct 2024](https://www.sebi.gov.in/sebi_data/attachdocs/oct-2024/1727786261636.pdf) `[part]`).
- Contracts expiring on or after 1 Sep 2025 expire on **Tuesday**, not Thursday; monthlies expire on the last Tuesday ([NSE circular 68747](https://nsearchives.nseindia.com/content/circulars/FAOP68747.pdf) `[part]`; [Reuters](https://www.reuters.com/sustainability/boards-policy-regulation/india-markets-regulator-fixes-weekly-derivative-expiry-days-exchanges-source-2025-06-17/) `[part]`). A holiday moves expiry to the previous trading day.

**Lot size.** NIFTY changed from 75 to 65: the last weekly with 75 expired 23 Dec 2025 and the first with 65 expired 6 Jan 2026 ([NSE circular 70616](https://nsearchives.nseindia.com/content/circulars/FAOP70616.pdf) `[part]`). Earlier changes are not checked here. A backtest needs the lot size **per contract**, from the contract master of its date.

**Margin rules from SEBI's Oct 2024 circular.**

- An extra 2% ELM on short options on their expiry day (from 20 Nov 2024).
- No calendar-spread offset for contracts expiring that day (from 1 Feb 2025).
- Premium collected upfront from buyers (from 1 Feb 2025).
- Intraday position-limit checks (from 1 Apr 2025).

**SPAN.** NSE Clearing scans index derivatives at 6σ × √2, capped at 9.3% of the underlying, with a volatility scan of 25% of annualised EWMA volatility (minimum 4%). The calendar spread charge is 1.75% of the far month ([NSE SPAN parameters](https://www.nseindia.com/static/products-services/equity-derivatives-span-risk-parameter-files) `[part]`). The daily `.spn` files make historical SPAN reproducible (marginism above).

**STT.** From 1 Apr 2026: 0.15% of premium on option sales (was 0.10%), and **0.15% of intrinsic value on options exercised at expiry**, paid by the buyer (was 0.125%); futures 0.05% ([NSE STT](https://www.nseindia.com/static/products-services/equity-derivatives-securities-transaction-tax) `[part]`; [BSE notice](https://www.bseindia.com/downloads/UploadDocs/Notices/20260331-7/20260331-7.pdf) `[part]`). Holding a long ITM option to expiry therefore pays a tax that selling it before the close does not. The engine must charge it at settlement, by date.

## What an options-aware engine must model that a stock engine does not

1. **A chain, not a series.** Contracts are listed and expire; the universe at each step is strike × expiry × type. Selection is by delta, strike offset or premium, and **near a 0DTE close select by strike offset, because every delta is 0 or 1** (ZIPLIME).
2. **The forward, not the spot.** ATM and IV should come from the put-call-parity forward of each expiry (Nautilus, ORATS stock price "derived from option prices using put-call parity").
3. **IV and Greeks per step, with a refusal path.** Solve on mid, use the OTM side of each pair (LEAN), and return "no value", never 0 or a default volatility (LEAN's 0 against ZIPLIME's raise).
4. **A bad-quote filter before anything else.** Skip wide markets (ORATS: over 5% of strike or 15% of mid; Option Omega: ignore wide spreads), drop the first noisy minutes (OO starts at 9:32), and avoid the last minutes' quote decay (ORATS: 14 minutes before the close).
5. **Fills as a fraction of the spread, by leg count.** Mark at mid, trade at mid ± a share of the width (75% to 53%), and report results at several shares so the cost sensitivity is visible.
6. **Intra-bar ordering.** One-minute bars cannot say whether stop or target came first (AlgoTest); check stops on sub-minute data where it exists (OO's 1-second mids).
7. **Expiry as an event with the right print.** SPXW: official close at 16:00 ET, 13:00 on half days. SPX: SOQ. NIFTY: 30-minute weighted close. Load expiry times correctly (the Databento midnight-UTC trap).
8. **Exercise costs.** Cash settlement fees and India's STT on exercised intrinsic value.
9. **Margin that knows structures.** Position groups or SPAN scenario arrays, plus expiry-day add-ons (NSE 2% ELM, no calendar offset on expiry day). Capital tied up decides return on margin for short-premium books.
10. **Contract terms that change with the date.** Lot size, expiry weekday, listed weeklies, tax rates: dated tables, never constants.
11. **Nonlinear P&L attribution.** Split P&L into premium, settlement payout and mark-to-market (Goldman, in [papers-tooling](../2026-10-07-research-pipeline/papers-tooling.md)); ORATS sums daily returns rather than compounding them.
12. **Diagnostics that separate "no trade" from "zero edge".** A run that matched no contracts must say so (ORATS).

## What to take for our harness

1. **One cost model, stated and swept.** Default to ORATS's leg-count fractions of the spread (75/66/56/53%), mark at mid, and always report at least two cost levels. The backtester station refuses a run without a cost setting (as the crypto backtester [Algonney](https://algonney.com/research/methodology/backtesting/) `[part]` does: "The engine has no default of its own").
2. **Settle to the official print, by market.** SPXW official close, SPX SOQ, NIFTY 30-minute close; a dated half-day calendar; expiry times fixed at load. Write a test that fails on Databento's midnight-UTC expiry.
3. **IV solver that refuses.** Let's Be Rational via vectorised vollib on the parity forward, OTM side of each pair, NaN plus a counter on failure, never 0.
4. **The ORATS job shape for our MCP backtest tool.** Submit, poll, fetch. Every result carries `effectiveConfig`, diagnostics counters, warnings, data hash and engine version. Copy the tool list of optopsy-mcp (sweep, walk-forward, permutation, FDR) and keep the strategy script sandboxed.
5. **NIFTY via SPAN files and dated tables.** marginism-style SPAN from the daily `.spn`, plus tables for lot size, expiry weekday, ELM add-ons and STT, keyed by date.
6. **Bad-quote and clock rules as named, tested filters.** Wide-market skip, first-minutes skip, near-close quote decay, sub-minute stop checks where data allows.
7. **Pluggable models per concern, LEAN-style.** Price, fill, exercise, assignment and margin are separate interfaces, so the skeptic role can swap one and rerun.
8. **Reproducibility from lambdaclass and bhav.** Pin data by hash; one command reruns every published table and asserts it matches.

**Could not reach or not found:** Stockmock's and Opstra's backtest method docs (not found); Sensibull's own statement on backtesting (only a competitor's claim found); ORATS's settlement price and margin formula (not documented); LEAN's option fill side and Option Omega's margin method (pages read do not say); what vollib does with a price below intrinsic (not checked); the claimed `vbt.options` and `opy` (no primary source). Firecrawl was down and was not used.
