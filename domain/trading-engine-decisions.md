> As of Convex-Hedge-Trading-Engine@b47d8ee, 2026-10-01

# Trading engine decisions — the map

Split from [design-decisions](design-decisions.md), which holds our own choices and the
`delta-exchange-payoff` records. **Canon is each record in `Trading-Engine/Decisions/`.** Every
record gives the situation, the choice, the options considered and the consequences. This note
is the map: one row per record, with the gist in a few words.

All records are *accepted* except 0012. The records are numbered in the order they were locked in.

## Foundations, 2026-09-26

| # | Decision | Gist |
|---|---|---|
| 0001 | AWS is the cloud provider | Cloud hosting on AWS; the setup there is still open |
| 0002 | The engine runs the same way locally and in the cloud | Where it runs changes settings, never behaviour |
| 0003 | Components talk through a message bus | No part calls another directly |
| 0004 | Redis Streams is the message bus | One Redis per engine instance |
| 0005 | Every part runs as its own process in a container | One image; the start command picks the part |
| 0006 | The engine names instruments itself | Adapters translate at the edge; the id carries the product root |
| 0007 | Python is the language of the engine | 3.12, `uv`, strict mypy, ruff |
| 0008 | Feed adapters publish raw market data only | Anything worked out is a separate part and category |
| 0009 | Secrets reach the engine only through environment variables | Never in files, logs or the vault |
| 0010 | Recordings are compressed newline-delimited JSON | An exact copy of the bus, one file per run |
| 0011 | Quotes are sampled once a second by default | 8.3 M records a day instead of 283 M; every-change is a switch |

## Data feeds and the bus, 2026-09-27 → 09-28

| # | Decision | Gist |
|---|---|---|
| 0012 | A sampled quote without an exchange time takes its receive time | **Superseded by 0027** |
| 0013 | Daily statistics are republished with the definitions | The bus forgets after 10 min, so OI would vanish otherwise |
| 0014 | A person logs in to Fyers every trading day | Fyers' April 2026 rules; the token dies at 06:30 IST |
| 0015 | The Fyers adapter decodes the data socket itself | The official library drops OI and does not resubscribe |
| 0016 | One Fyers process serves both Indian index markets | One live connection per app, up to 5,000 instruments |
| 0017 | Candle mode publishes candles as flagged trades | A past Indian day, rebuilt from the broker's candles |
| 0018 | The index level is published as a trade with no size | On the underlying's own id, flagged as an index level |
| 0019 | The dashboard front end is TypeScript on Next.js, served as static files | The Python part serves it |
| 0020 | The bus keeps the latest value of every key | Seven days, so late starters are complete; needs Redis 7.4 |

## The chain engine, 2026-09-28

| # | Decision | Gist |
|---|---|---|
| 0021 | Values worked out from the option chain have their own category | Raw and derived never share a stream |
| 0022 | The Greeks treat the forward as the spot level | Theta is value lost per trading day |
| 0023 | Trading calendars are kept as files in the engine | Per exchange and year; a missing year stops the chain engine |
| 0024 | Every worked-out message carries its lineage | The bus id of its cause and of the raw event at the start of the chain |
| 0025 | The chain engine recomputes a whole expiry on every event | About 5 ms p99 per SPXW expiry |
| 0026 | Streams carry small events and large pictures live in keyed state | The chain snapshot is keyed state, never recorded |
| 0027 | A sampled quote is timed at the end of its second | Not the contract's last trade time |
| 0028 | Volatility comes only from the out-of-the-money option | No IV from an ITM price, whatever the spread |

## Strategies, broker, dashboard look, 2026-09-29 → 09-30

| # | Decision | Gist |
|---|---|---|
| 0029 | Strategies decide on a wall-clock cadence | Round beats in the market's time zone, 1 s to 60 min |
| 0030 | A strategy signal is a target position | The whole position in lots, never an order |
| 0031 | Each strategy instance runs as its own process | One slow instance never holds up another |
| 0032 | The simulated broker fills the model account at the mid price | At once, in full, all legs or none |
| 0033 | A strategy reads its whole card at each decision | All inputs read at once, from latest values |
| 0034 | Derived values come from the chain engine | Strategies do not compute their own IV or Greeks |
| 0035 | The dashboard copies the look of the backtest engine | That is Convex Hedge's terminal, [platform-map](platform-map.md) |
| 0036 | The dashboard carries its own font files | Served by the dashboard itself |
| 0037 | The dashboard has only a dark look | The light look was removed |
| 0038 | A change marker shows which way a figure moved | ▲/▼ that fade over about a second |
| 0039 | Only in-the-money cells are tinted | OTM cells are plain |
| 0040 | Simulated fills can wait a set delay per strategy instance | 60 s for the inflow strangles |
| 0041 | A strategy signal carries the price of each leg | The *signal price*, used for slippage on the fill card |
| 0042 | The alerter posts one card per signal through a webhook | Discord; one card even for several legs |
| 0043 | The simulated broker keeps the PnL history | In Redis, five days, a point every 10 s |
| 0044 | A strategy's page is addressed by a query parameter | `/strategies/view?instance=<name>`; filters too |

## On a branch, not yet merged — feature #150

Records 0045–0050 are on `feature/dashboard-analytics-tabs`. They cover the structure chain in the
dashboard, GEX and skew in the derived data engine, a **SQLite history on a named volume**,
**Apache ECharts**, the gamma flip from the GEX profile, and GEX **per 1% move with dealers long
calls and short puts**. See [engine-dashboard](engine-dashboard.md). Move them into the tables
above when the feature merges.

## Not decided yet (from `Overall architecture.md`)

These are open: the database, and what to store in it; whether instances share a database and a
dashboard; which broker or terminal serves which market; how a same-machine terminal
(Trader Workstation) works in the cloud; what counts as an alert; and the AWS hosting setup,
including how Redis runs there. **The execution engine (OMS and RMS) has no design page yet.**

## Related

[trading-engine](trading-engine.md) · [design-decisions](design-decisions.md) ·
[engine-lineage](engine-lineage.md)
