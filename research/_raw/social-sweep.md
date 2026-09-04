# UNVERIFIED — CURRENT-CHATTER LAYER (30 days to 2026-08-28)

**Everything below is chatter, not evidence. Nothing here has passed the 5-test source filter. This is a routing list: names, repos, tools and — most importantly — complaints, to be sent to independent verification.**

## Method and what failed

- `last30days` skill: **invoked, ran, produced garbage.** First-run setup was incomplete, no X/Twitter auth, no yt-dlp, Reddit rate-limited (HTTP 429) after 6 items, and its deterministic planner keyword-collided on "options" — top-ranked clusters were E-Paper displays, Logitech Options+, and Lenovo BIOS options. Engine footer: `Reddit: 6 threads | HN: 6 stories | X: 0 | YouTube: 0`. Unusable.
- Fallback used: **GitHub REST search API** (star counts and `pushed_at` are live, verified), **HN Algolia API**, **arctic-shift Reddit archive** (r/quant, r/algotrading, r/options, r/thetagang, r/quantfinance, r/defi, r/CryptoCurrency), plus WebSearch. Reddit's own JSON endpoint is blocked from this host.
- **X and YouTube were not swept at all.** No credentials. This is a real hole — see the crypto gap below.

---

## 1. Active GitHub repos (star counts and last push verified live via API, 2026-08-28)

### Vol surface / SVI
| Stars | Last push | Repo | What it actually does |
|---|---|---|---|
| 33 | 2026-08-23 | `volsurf-rs/volsurf` | Vol surface library in Rust. Created 2026-02, still moving. The only "production-quality" claim in the surface space that isn't a notebook. |
| 16 | 2026-06-01 | `adityatomar15/options-market-making` | C++20 MM engine: SVI surface, lock-free SPSC queues, delta hedging, real-time PnL attribution. **The most directly relevant repo found** — it puts SVI inside an execution loop rather than a plot. |
| 12 | 2026-05-14 | `XanderRobbins/Arbitrage-Free-Volatility-Surface` | SVI + Heston, arbitrage-free constraints. |
| — | — | `arkonique/ssvi`, `chi-gamma/SVI_and_SSVI_Volatility_Surface_fitting`, `JackJacquier/SSVI` | SSVI calibration + parameter conversion. `JackJacquier` is Jacquier of Gatheral–Jacquier — author-of-record repo. |
| 134 | 2026-06-09 | `Dagalon/PyStochasticVolatility` | SV simulation toolkit (rough vol adjacent). |
| 91 | 2026-08-18 | `khakhasshi/OptionWorkstation` | Options replay + vol analytics + guarded paper trading. Created 2026-07-23, 91 stars in a month — **fast star accretion on a brand-new account is itself a flag worth checking.** |

You have already implemented SVI/SSVI, so the calibration repos are redundant to you. The two worth actually opening are `adityatomar15/options-market-making` (surface → quoting → hedge, which is the gap in your curriculum) and `volsurf-rs/volsurf` (if you ever want the surface off the Python hot path for minute-wise data).

### Backtesting infrastructure
| Stars | Last push | Repo | Note |
|---|---|---|---|
| 27,998 | 2026-08-28 | `nautechsystems/nautilus_trader` | Rust core, nanosecond event-driven, 114 open issues. Named repeatedly by practitioners as the thing you graduate *to*. |
| 1,463 | 2026-06-30 | `goldspanlabs/optopsy` | Options-specific research/backtest library. Stalled two months. |
| 264 | 2026-07-28 | `lambdaclass/options_portfolio_backtester` | Strategy sweeps, tail-risk hedge analysis, signal timing. |
| **26** | **2026-07-19** | **`rajmaurya0904/bhav`** | **"Open-source NSE options backtesting engine, built for Upstox historical data. Realistic Indian cost model, deterministic Parquet outputs."** Created 2026-07-04. The single most on-target repo for your NIFTY minute data — an explicit Indian cost model is exactly what the auto-reject rule looks for. Tiny, brand-new, one author, zero issues. **Route this to hard verification: read the cost model before trusting a line of it.** |

### Regime detection
The whole space is thin and recent. Best of a weak field: `CameronScarpati/lob-regime-scanner` (14★, 2026-08-21) — Gaussian HMM over crypto order books, 30+ features, C++/pybind11 LOB engine. Also `kratu/wess_hmm` (Wasserstein + HMM), `AlgoVaultLabs/crypto-quant-signal-mcp` (funding-rate arb + regime, 6★). Nothing here has scale. Everything is HMM-on-features; see the complaint section for why practitioners say this class fails.

### Crypto
`ccxt` (43.8k) and `crypto-chassis/ccapi` (732★, header-only C++, 2026-08-07) are the plumbing everyone actually uses. **A GitHub search for crypto implied-volatility / Deribit repos returned essentially nothing usable** — the crypto options analytics layer is not on public GitHub in any serious form.

---

## 2. Tools people report actually running

- **Nautilus Trader** — the recurring "official validation and live engine" answer.
- **VectorBT / VectorBT Pro** — used as a *screening* layer only. `u/quant-king`: "VectorBT Pro for initial idea validation, Nautilus for official validation and live engine." Slippage/fill modelling in vectorbt is widely described as simplified.
- **Self-built engines** — a striking number. `u/Apprehensive-Soup864` claims a GPU C++ tick-level engine (~850M ticks, 5–7y futures, 100M parameter combos, broker fill emulation) and says "I would not trust anything less now, seeing how things actually backtest out vs. some approximation." `u/Life-Succotash-7053`: "i spend 3 months building my own... robust engine but at huge time as cost."
- **quantstats** (`ranaroussi`) for metrics.
- **CBOE Open-Close Volume Summary** — named as the *only* dataset with participant tags for real GEX; **~$17k/month**. Cited as the reason every free/cheap GEX product is structurally wrong.
- Retail tier that keeps appearing and should be ignored: optionstrat, optionsprofitcalculator, thinkorswim, portfoliovisualizer, TradingView backtester.

---

## 3. RECURRING COMPLAINTS AND FAILURE REPORTS — the highest-value output here

**a) GEX / gamma-exposure is being publicly demolished.** r/options, "GEX is a scam please dont waste your time" (128 pts, 133 comments) and a companion study, "On the predictive power of GEX/Max pain vs a Martingale for SPX 0DTE" (39 comments). The study's finding, as summarised in-thread: spot itself beats GEX and max-pain as a predictor. `u/Sharaku_US`: "I have GEX, DEX, VEX, CEX data from September of last year and I can clearly tell you none of the Greeks have any predictive value." `u/WhoStoleMyMartini` gives the mechanism: most services compute GEX from **open interest with no participant tags**, so the dealer-positioning sign is guessed. If any part of your terminal is heading toward dealer-gamma levels, this is the current state of the argument.

**b) Volatility risk premium in SPX 0DTE is real but "razor thin."** Same author (`u/Fit_Equal6932`) ran tick-level ATM IV for SPX 0DTE, CBOE VIX-methodology rates, June 2025–July 2026, 280 trading days, realized vol sampled per minute: **~3–4 vol points of premium, strongly regime-dependent, with extended runs where it is absent.** Median index move ~0.4%. This is the most methodologically serious retail work found in the window and the method transfers directly to NIFTY minute data. **Route this person and this study to verification** — it is unverified chatter, but it is the right shape.

**c) Regime switching "sounds good but disappoints."** r/algotrading thread of that exact title. `u/MarkGarcia2008`: "One needs a way to detect a regime switch *before* it happens. And if I could do that — I'd be rich." Treat the entire HMM regime-detection repo cluster above as suspect on this basis: they detect regimes in-sample, after the fact.

**d) Slippage and latency are where backtests die, and most tools cannot see latency.** `u/EveryLengthiness183`: "The biggest thing you need to correctly model in your backtesting is **latency**. The time you get your signal > time you place your trade > time the exchange receives your order is often significantly longer than you think. **Most backtesting tools lack visibility to this.**" `u/CoughRock` models adversarial fills: long fills at the *high ask* of the next candle, short at the *lowest bid*, with a penalty above 1% of that candle's volume. `u/stratcore` argues execution must be a **separate state machine** from signal — snapshot bid/ask/spread/size at signal time, submit marketable limits with a max price and participation cap, track New/PartiallyFilled/Filled explicitly.

**e) Look-ahead leakage is the most-confessed failure.** "Note to self: Eye watering returns = look ahead error." The cheapest diagnostic offered, `u/hypertradeworx`: "shift every feature forward one bar and rerun. If the edge survives, the leak is in the **label** rather than the features — with xgboost usually a rolling stat that touches the same bars the forward return is built from."

**f) Overfitting: the trade-count trap.** `u/Zestyclose-Eagle1809`: "One month of forward testing... it's a **trade count** question not a time one. If it's 15 or 20, that tells you almost nothing, a broken system passes 20 trades regularly. If it's 200, that's different. **How many versions did you build to get to this one?**" `u/AlgorithmicFIRE` gives two curve-fit tells: high parameter sensitivity under 5–10% input noise, and per-trade gain where mean is good but **median is not** (a few huge winners carrying a pile of losers). CPCV and walk-forward named as the standard; `u/VettaQ`: "Walk-forward with realistic costs: fill model, fees, slippage, bar-close vs intrabar entries. **Most 'great' equity curves die here first.**"

**g) Individual-name option markets are too thin to trade** (r/thetagang, "Why are option markets so thin on individual stocks", 44 comments) — relevant if you generalise beyond index.

**h) Sizing, not strategy, is the reported killer.** "What I've learned after 2 years of selling options": +30% to −20% on deposits, author attributes it to oversizing to 2–3x account value on assignment. `u/Stablecoin_news`: "Most people diagnose a bad exit as a strategy problem when it was actually a position size that made clear thinking impossible."

**i) Spurious structure gets debunked in-thread.** "Why are there price-dependent volatility contractions on SPY?" — top answer `u/axehind`: "mainly an artifact of plotting a non-stationary price level against a regime-dependent return series." A clean example of the community catching a chart artifact.

---

## 4. Named individuals worth routing to independent verification

All pseudonymous — this is the weakest category and none pass test (3) as stated.
- **`u/Fit_Equal6932`** (r/options, r/thetagang) — tick-level SPX 0DTE IV construction, VIX-methodology rates, 280-day VRP study. Highest priority. Also the sharpest critic of GEX vendors in the same threads.
- **`u/Sharaku_US`** — claims a year of GEX/DEX/VEX/CEX data with a null result. Worth asking for the data.
- **`u/EveryLengthiness183`, `u/stratcore`, `u/CoughRock`** — execution/latency/fill modelling specifics.
- **`u/Apprehensive-Soup864`** — GPU tick-level backtester claim; unverified and unusually large. Treat sceptically.
- **`rajmaurya0904`** (bhav, NSE cost model), **`adityatomar15`** (SVI market maker), **`volsurf-rs`** maintainers — repo authors, verifiable through code rather than claims.
- **Jacquier** (`JackJacquier/SSVI`) — the only non-anonymous, institutionally verifiable name in the sweep, and you already know the work.

---

## 5. Coordinated / shill patterns — flagged

1. **GEX-service astroturf.** `u/Fit_Equal6932`, on being downvoted for a null result: "All the downvotes gel very well with all the posts we see these days on this sub for a new gex service. **Everyone without an edge has pivoted to using AI coding assistants to build and sell a 'service'.**" Multiple separate GEX-platform threads in the same 30 days. Treat every new gamma/GEX dashboard in this window as marketing until proven otherwise.
2. **LLM-generated "I built a thing / here's what I learned" posts.** The r/algotrading "self-hosted quant scoring engine" post drew `u/arbitrageME`: "lol... absolute AI output"; `u/johannthegoatman`: "It's not anti-AI, it's anti-AI *writing your post*." The author admitted AI assistance. The post's own body concedes "some tiers use a **simulated AI-accuracy ceiling**" — i.e. parts of the backtest are synthetic. Auto-reject.
3. **The NIFTY/BankNifty 0-star repo flood.** A GitHub search sorted by recency returns page after page of freshly-pushed **zero-star** NIFTY/BankNifty repos — `nifty-option-radar`, `nifty-options-scanner`, `oi-analysis-dashboard`, `ict-nifty-options-strategy`, `banknifty-predictor`, `Jacob-XGBoost-Classifier`, `deltaforge` — nearly all pushed within the last 48 hours, none with a stated cost model. This is the most crowded and lowest-quality corner of the entire sweep. `bhav` (26★, explicit Indian cost model) is the only one that looks different, and even that is one author, seven weeks old.
4. **Marketing-shaped r/thetagang content** — "1% Weekly Returns from Options Week 25", daily "trades I took today" posts, "$3,423 in realized premium". Win-rate marketing; auto-reject per your filter.

---

## 6. Honest negatives about this sweep

- **Hacker News is dead on this topic.** Algolia search over the window returns nothing above single-digit points — one "Bloomberg terminal for Claude Code" Show HN at 6 points, 0 comments. HN is not a source for vol/quant in 2026.
- **r/quantfinance is pure careers noise** — interview prep, spring weeks, "how do I break into quant". Zero technical content this window. Drop it from any future sweep.
- **Crypto quant chatter did not show up on Reddit at all.** r/CryptoCurrency and r/defi returned nothing on vol, options, or systematic strategy above 3 points; the only options-adjacent item was a Solana options protocol promo post. Given your 40% crypto weighting, this is a **coverage failure, not a finding**: crypto vol discussion lives on X, Discord and Telegram, and X was not swept because no credentials were available. **Re-run the crypto leg with X access before drawing any conclusion.**
- **No cost model was stated anywhere in this chatter layer except `bhav`'s claim and the fill heuristics in the slippage thread.** Under your own filter, that means almost nothing here would survive to a recommendation as-is. Which is the correct outcome for a chatter agent: this is a routing list, not a reading list.