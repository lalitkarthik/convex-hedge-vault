> As of Convex-Hedge-Trading-Engine@06e547fa, 2026-10-23

# Trading engine decisions — the map, 0001 to 0085

Split from [design-decisions](design-decisions.md), which holds our own choices and the
`delta-exchange-payoff` records. **Canon is each record in `Trading-Engine/Decisions/`.** Every
record gives the situation, the choice, the options considered and the consequences. This note is
the map: one row per record, with the gist in a few words. Records 0086 to 0156, the platform era
from 2026-10-10, are in the successor note
[trading-engine-decisions-platform](trading-engine-decisions-platform.md).

The records are numbered in the order they were locked in. Records are *accepted* unless the row
says **superseded** or **amended**. **Numbers repeat:** parallel feature branches each took the next
free number, so 0045–0048 and 0073–0078 each name two or three records. A record is therefore
named by number and title, and the rows below give both.

## Foundations, 2026-09-26

| # | Decision | Gist |
|---|---|---|
| 0001 | AWS is the cloud provider | Cloud hosting on AWS; the setup came in 0051 and 0092 |
| 0002 | The engine runs the same way locally and in the cloud | Where it runs changes settings, never behaviour |
| 0003 | Components talk through a message bus | No part calls another directly |
| 0004 | Redis Streams is the message bus | One Redis per engine instance |
| 0005 | Every part runs as its own process in a container | One image; the start command picks the part |
| 0006 | The engine names instruments itself | Adapters translate at the edge; the id carries the product root |
| 0007 | Python is the language of the engine | 3.12, `uv`, strict mypy, ruff |
| 0008 | Feed adapters publish raw market data only | Anything worked out is a separate part and category |
| 0009 | Secrets reach the engine only through environment variables | Never in files, logs or the vault. **Amended by 0057** for the day's broker token |
| 0010 | Recordings are compressed newline-delimited JSON | An exact copy of the bus, one file per run |
| 0011 | Quotes are sampled once a second by default | 8.3 M records a day instead of 283 M; every-change is a switch |

## Data feeds and the bus, 2026-09-27 → 09-28

| # | Decision | Gist |
|---|---|---|
| 0012 | A sampled quote without an exchange time takes its receive time | **Superseded by 0027** |
| 0013 | Daily statistics are republished with the definitions | The bus forgets after 10 min, so OI would vanish otherwise |
| 0014 | A person logs in to Fyers every trading day | Fyers' April 2026 rules; the token dies at 06:30 IST. **Amended by 0057**: the login is on the Broker page |
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
| 0025 | The chain engine recomputes a whole expiry on every event | About 5 ms p99 per SPXW expiry. A recompute floor came with 0073 |
| 0026 | Streams carry small events and large pictures live in keyed state | The chain snapshot is keyed state, never recorded |
| 0027 | A sampled quote is timed at the end of its second | Not the contract's last trade time |
| 0028 | Volatility comes only from the out-of-the-money option | No IV from an ITM price, whatever the spread |

## Strategies, broker, dashboard look, 2026-09-29 → 09-30

| # | Decision | Gist |
|---|---|---|
| 0029 | Strategies decide on a wall-clock cadence | Round beats in the market's time zone, 1 s to 60 min |
| 0030 | A strategy signal is a target position | The whole position in lots, never an order |
| 0031 | Each strategy instance runs as its own process | One slow instance never holds up another |
| 0032 | The simulated broker fills the model account at the mid price | At once, in full, all legs or none. **Amended by 0040** |
| 0033 | A strategy reads its whole card at each decision | All inputs read at once, from latest values |
| 0034 | Derived values come from the chain engine | Strategies do not compute their own IV or Greeks |
| 0035 | The dashboard copies the look of the backtest engine | That is Convex Hedge's terminal, [platform-map](platform-map.md) |
| 0036 | The dashboard carries its own font files | Served by the dashboard itself; the fonts changed in 0105 |
| 0037 | The dashboard has only a dark look | The light look was removed |
| 0038 | A change marker shows which way a figure moved | ▲/▼ that fade over about a second |
| 0039 | Only in-the-money cells are tinted | OTM cells are plain |
| 0040 | Simulated fills can wait a set delay per strategy instance | 60 s for the inflow strangles |
| 0041 | A strategy signal carries the price of each leg | The *signal price*, used for slippage on the fill card |
| 0042 | The alerter posts one card per signal through a webhook | Discord; one card even for several legs |
| 0043 | The simulated broker keeps the PnL history | In Redis, five days, a point every 10 s. **Superseded in part by 0064**: also on disk |
| 0044 | A strategy's page is addressed by a query parameter | `/strategies/view?instance=<name>`; filters too |

## Indian brokers, 2026-10-01 → 10-08

| # | Decision | Gist |
|---|---|---|
| 0045 | The Upstox adapter logs in with a one-year Analytics token | No morning login for Upstox |
| 0046 | The Upstox adapter reads the live connection with a generated reader | Generated from Upstox's message description; certificate check on |
| 0047 | An Upstox quote takes the broker's message time | Counted on the statistics line |
| 0048 | An engine instance runs one Indian feed | **Superseded by 0056** |
| 0056 | One Indian instance runs both feeds and the selected broker picks one | A record-store fact; the switch takes seconds, nothing restarts |
| 0066 | Zerodha's personal-use rule goes to the firm before a key is bought | Bilal rules on it; no key bought yet |
| 0067 | A person signs in to Zerodha each morning | Button on the Broker page; a command as fallback |
| 0068 | The Zerodha adapter reads the live connection itself and keeps the best bid and ask | Written from Zerodha's byte table; no library |
| 0069 | A Zerodha quote takes the exchange time | Receive time when Zerodha sends none, counted |
| 0070 | Settings and the Broker page take any number of Indian brokers | One rule over every broker feed; first named is default |
| 0071 | Zerodha stays out of the shared Indian instance until its live check | **Superseded in part by 0076** |
| 0076 | Zerodha joins the shared Indian instance in the cloud | Beside Fyers and Upstox; Fyers stays the default |

## Cloud hosting and sign-in, 2026-10-01 → 10-07

| # | Decision | Gist |
|---|---|---|
| 0051 | The India instance runs on one scheduled EC2 machine | Compose on EC2 in Mumbai, 08:45–16:15 IST, no recorder, Terraform. Later moved by 0092 and 0146–0149 |
| 0052 | Redis keeps a snapshot across the nightly stop | Cloud only; laptops keep nothing on disk |
| 0053 | The load balancer signs dashboard visitors in with company Google accounts | **Superseded by 0055** |
| 0054 | The day's Fyers token reaches AWS by a token push | **Superseded by 0057**; still a fallback |
| 0055 | The dashboard signs visitors in with company Google accounts itself | Seven-day cookie; a control list may act. **Superseded in part by 0151** (roles) |
| 0057 | The day's Fyers token is handed to the adapter through the record store | The Broker page swaps the code for the token; no restart |
| 0074 | Every part proves it is alive with a heartbeat file | Touched from the work loop; Docker checks its age, 30 s |

## Derived data and volatility, 2026-09-30 → 10-08

| # | Decision | Gist |
|---|---|---|
| 0046 | Gamma exposure and skew figures come from the derived data engine | The chain engine publishes them |
| 0047 | The derived data engine keeps its history in SQLite on a named volume | One writer; seven nightly copies kept |
| 0049 | The gamma flip is found from the gamma exposure profile | About sixty imagined levels; nearest crossing to spot |
| 0050 | Gamma exposure is measured per one percent move with dealers long calls and short puts | Calls positive, puts negative |
| 0059 | Resistance sits above spot and support below | **Superseded by 0082** |
| 0060 | Open interest history is kept in the history store | Once a minute per strike shown |
| 0073 | Realised volatility is worked out in the chain engine from its own one-minute candles | The dashboard only displays |
| 0073 | The ATM forward is a third flavour worked out by the chain engine | **Superseded by 0132**: the ATM forward is the only forward |
| 0073 | The chain engine waits a recompute floor between pictures of one expiry | 0.1 s by default; 0025 otherwise stands |
| 0074 | Realised volatility within the day is the sum of squared returns at one- and five-minute sampling | **Amended by 0131**: windows counted in samples |
| 0075 | A part-day figure is scaled by the usual share of a day's movement, not by the clock | A time-of-day profile from stored sessions; amended 2026-10-12 (provisional figures) |
| 0076 | The implied volatility set against realised volatility is the skew's, read at the forward | ATM IV between the two strikes around the forward |
| 0077 | Volatility readings are kept by the minute for 30 sessions and by the day for good | Four new kinds of history row |
| 0078 | The first version compares implied against realised volatility within the day only | **Superseded by 0140 and 0141** |
| 0079 | Skew rank is a percentile of the expiry's own minute readings over a lookback window | 5M to 2D, trading time only |
| 0080 | The chain engine saves a smile snapshot every minute in the history store | Every expiry; skew slopes to six decimals |
| 0081 | Risk reversal and butterfly follow the market's standard definitions | Delta points 25, 10, 5, 1; nothing guessed past the strikes |
| 0082 | Resistance and support levels are chosen by the sign of gamma exposure | R1 the call wall, S1 the put wall |

## Dashboard pages, 2026-09-30 → 10-08

| # | Decision | Gist |
|---|---|---|
| 0045 | The structure chain is worked out by the dashboard | Summed in the browser from chain rows |
| 0048 | The dashboard draws every chart with Apache ECharts | **Superseded by 0058** |
| 0058 | The dashboard draws every chart with Lightweight Charts | Version 5, one shared chart frame |
| 0072 | The structure editor works out the payoff in the browser | From the chain rows it already has |
| 0074 | The forward method is a browser choice that never reaches the strategies | **Superseded by 0132** |
| 0075 | Page settings are remembered in the browser | For the company's pages; Market Watch moved to the server in 0124 |
| 0077 | The option chain no longer picks legs | Buy and Sell move to the structure builder |
| 0078 | The structure editor becomes the structure builder | `/structure-builder/`; old address forwarded |
| 0083 | The GEX page becomes the Open Interest page | Tabs OI, OI CHANGE, GEX |
| 0084 | Pages open on the ATM forward by default | **Superseded by 0132** |
| 0085 | The dashboard reads only the forward methods its pages show | **Superseded by 0132** |

## Strategy records and client portfolios, 2026-10-05

| # | Decision | Gist |
|---|---|---|
| 0061 | A client account follows one client portfolio | Members at their own size; a client account takes every member's trades at its multiple |
| 0062 | Client portfolios are kept in SQLite on the engine's volume | Soft delete; stale writes refused |
| 0063 | Anyone signed in may create and edit client portfolios | **Superseded in part by 0151**: trader role or above |
| 0064 | The simulated broker keeps a trading journal in SQLite | Signals, fills, trades, day rows kept for good; 10 s samples 90 days |
| 0065 | Daily figures are marked to market from the previous close | *Daily MTM* on cards, Live tab and day rows |

## History of this note

On 2026-10-01 this note mapped 0001–0044 and said that 0045–0050 sat on the branch
`feature/dashboard-analytics-tabs` (feature #150). That feature merged on 2026-10-03; its records
are in the tables above. Every other record above merged to `main` with its feature, and no branch
holds an unmerged record as of 2026-10-23.

## Record drift found on 2026-10-23

`About decisions.md` says a changed decision gets a new record that says so. The new records say
so, but some older ones carry no back-link: 0009 and 0014 (amended by 0057), 0025 (floor in 0073),
0051 (moved by 0092 and 0146–0149), 0035 and 0036 (fonts in 0105). The platform-era cases are in
the successor note.

## Not decided yet (from `Overall architecture.md`)

Open as of 2026-10-23: the database, and what to store in it; whether instances share a database
and a dashboard; which broker or terminal serves which market for orders; how a same-machine
terminal (Trader Workstation) works in the cloud; what counts as an alert. **The execution engine
(OMS and RMS) has no design page yet.** On 2026-10-01 the AWS hosting setup was also open; 0051 and
0092 decided it, though the page still lists it.

## Related

[trading-engine](trading-engine.md) · [trading-engine-decisions-platform](trading-engine-decisions-platform.md) ·
[design-decisions](design-decisions.md) · [engine-lineage](engine-lineage.md)
