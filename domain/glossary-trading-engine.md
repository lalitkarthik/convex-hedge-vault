> As of Convex-Hedge-Trading-Engine@06e547fa, 2026-10-23

# Glossary — the trading engine

Split from [GLOSSARY](../GLOSSARY.md). **Canon is the repo's `CONTEXT.md`**: 1,075 terms (463 on
2026-10-01), each a page in `Trading-Engine/Glossary/`. This note holds only the terms the vault's
engine notes use. For collisions with the terminal's or feed engine's words, see GLOSSARY's *Collisions*.

## The engine as a whole

**Trading engine**: Convex Hedge's engine that runs strategies, watches market data and, later,
places orders. The map is [trading-engine](trading-engine.md).

**Engine instance**: One complete, independent copy of the engine: its own Redis, feeds, parts and
strategies, started from one **settings file** (TOML in `config/`). _Avoid_: stack, deployment.

**Compose profile**: The Compose switch that picks the feed: `live-us-databento`, `live-india-fyers`,
`replay`, and since October `live-india-upstox` and `live-india-zerodha` (three on 2026-10-01).

**Sandbox / Live trading**: Paper trading on live data with the simulated broker, and trading real
money. Only the sandbox exists. The platform's newer word for the sandbox is **Paper Trading**.

**Part**: One process of an instance in its own container, such as the chain engine or the alerter.
_Avoid_: service, which is the feed engine's word.

**Heartbeat file**: A file each part touches from its own work loop, about once a second. Docker
calls the part unhealthy when the file is older than 30 seconds, so a stuck loop shows.

**Layer map / Market Core**: The file that puts every part in one of three layers: Market Core (bus,
feeds, chain engine), Market Watch (dashboard, console) and company products (strategies, broker,
alerter). A test refuses any import from a higher layer, an **upward import**.

**Release tag**: `engine-` and a date on a merge commit, such as `engine-2026.10.23`; the version.

## The platform

**Product / Side**: Research, Market Watch and Live Trading, each offered on two sides, in-house and clients.

**Market Watch**: The product for watching chains, volatility and Greeks; the first product for
clients. **Pilot**: its first free, invited release to clients, from 2026-10-15. Planned as one
instance per client; since 2026-10-11 the clients share one market.

**Research Engine**: The second repository, `Convex-Hedge-Research-Engine`, holding the Strategy SDK
and the backtest host. It depends on the engine; the engine never imports it.

**Oracle**: The old backtest engine, frozen as the answer sheet. The Research host must match it on
its twenty strategies before it is retired. This vault calls that program the terminal.

**Node graph / Legacy strategy**: A strategy drawn as nodes from a fixed vocabulary, the end state
for every strategy; and one written by hand in Python, kept until redrawn. **Echo**, the AI
strategy builder in the Research product, writes node graphs onto a canvas.

**Tenancy / Track 1**: One system serving many users with each user's data kept apart; and the work
that builds it, after the pilot.

**User session**: The running work for one person in the multi-user dashboard. It starts at the
first connection and stops 30 minutes after the last page closes.

**Internal account / Clients account**: The AWS account for the company's machines (India, SPXW,
operations, the terminal's lab) and the one for everything clients use (the pilot, the router).

## Data

**Bus client**: The only code that knows stream names. Every part reaches Redis through it.

**Feed adapter**: A process that connects to one source and publishes raw data in five **message
kinds**: quote, trade, instrument definition, feed status and statistic.

**Broker feed / Selected broker**: A feed in the settings that reads Indian prices from a broker,
Fyers, Upstox or Zerodha; and the one of them that publishes now, switched on the Broker page.

**Daily-login broker**: A broker that needs a person's login every trading day: Fyers and Zerodha.
Upstox uses a one-year **Analytics token** instead.

**Record store**: Small named facts with lifetimes beside the bus streams: day's token, selected broker.

**Sampled top of book**: Databento's book at the end of each second in which it changed. The default
quote. The alternative is **every-change mode**.

**Latest value**: The newest message per key, kept seven days beside each stream. A late starter
reads it once. Strategies read only these.

**Market / Market prefix**: In Track 1, one broker plus one broker account, named by its market id;
every bus key of that market carries it as a prefix. The glossary page still gives the first
meaning, "a place, usually an exchange". An empty prefix gives the company instances' keys.

**Market host / Market worker**: The program that runs one worker per market through the trading
day, and the worker itself: one market's feed and chain engine. The pilot uses them; India and SPXW
do not.

**Chain engine / Derived data engine**: The part that works out forwards, IV and Greeks per expiry,
since 2026-10-03 also skew, gamma exposure and candles, since 2026-10-07 realised volatility. Both
names are in use; the glossary page for the second still says "not built yet".

**ATM forward**: An expiry's forward from put-call parity at the at-the-money strike, discount
factor one. **The only forward since 2026-10-15** (decision 0132).

**Implied forward**: An expiry's forward price; until 2026-10-15 a line fitted through every strike,
the **regression forward**, from mids and last trades, now retired. **Implied index level**: the
nearest expiry's forward, standing in for an index level the vendor does not carry.

**Chain event / Chain snapshot**: A small recorded message saying an expiry was recomputed, and the
large numbered picture of every strike, kept in keyed state and never recorded.

**Lineage**: The bus ids and times that tie a derived message back to the raw event that caused it.

**Recording / Replay**: The exact copy of the bus in one `.jsonl.zst` file per run, and the adapter
that plays it back as if it were live. The recorder runs on laptops only; the cloud records nothing.

**History store**: The SQLite file where the chain engine keeps what must outlast a restart: index
candles, OI history, smile snapshots and volatility readings.

**Saved view**: The dashboard's last full picture of one market, kept on its own disk and shown,
marked as saved, after Redis loses its data.

**Strike window**: The strikes around the money that one person's page receives, 5 to 50 each side
or all. The chain engine still works out every strike.

**Trading calendar**: The files per exchange and year giving trading days and hours. Time to expiry
counts only open-market time, 252 days to the year.

## Strategies

**Strategy / Strategy instance**: The code, named in the **strategy registry**, and one configured
copy of it with its own name, market, cadence, size and settings.

**Beat / Decision cadence**: A round wall-clock time at which an instance decides, and the spacing
of those times, from 1 s to 60 min.

**Strategy market data card**: Everything an instance declared it needs, read all at once at a
beat: prices, forwards, IV, Greeks and its account.

**Strategy state / Strategy signal**: What the instance thought at a beat, published every beat, and
the **target position** it wants, published only on a change of mind, with a reason.

**Signal price**: The mid of each leg when the strategy decided. The fill card compares it with the
fill price.

**Base lots**: The unit size of an instance. Every target is a multiple of it.

**Flatten / Pause / Resume**: Controls given as commands. Flatten closes everything and halts;
pause stops entries while exits still run; resume undoes both.

**Cooldown**: The wait after a stop before a re-entry, two minutes in the inflow strangle, counted
from the stop signal.

**Paper adapter / Intended book**: The class from the Research Engine that runs a node graph as an
engine strategy instance; and the positions the graph believes it holds, returned as its target.

**Stepped run / Backtest host**: The engine's own parts driven one data step at a time in one
process, with no Redis; and the Research Engine program that drives such a run over past data.

## Broker and alerts

**Simulated broker**: The part that fills every instance's model account, at the mid by default.

**Model account**: One pretend account per strategy instance: positions, cash, and realised and
unrealised PnL before charges.

**Fill delay**: The per-instance wait before the simulated broker fills. The fill uses the mid at
the end of the wait.

**Fill-price policy**: Which price a simulated fill tries first: the mid (the default) or a recent
last trade.

**Cost model / Cost preset / Fees total**: The rule for slippage, taxes and fees on every fill,
opt-in per instance; a ready-made one by name, "nifty" or "spxw-ibkr"; and the fees paid, kept
beside the gross PnL.

**Stale fill**: A fill that had to use an older mid or the last trade.

**PnL history**: A stream per instance of PnL samples, five days of them in Redis and also on disk
in the trading journal, which feeds the dashboard's curve.

**Trading journal / Day row / Daily MTM**: The simulated broker's SQLite record of every signal,
fill, closed trade and PnL sample; one summary per instance per trading day; and that day's PnL
measured from the previous close.

**Client portfolio / Client account**: A named set of strategy instances on one engine instance;
and a customer's account at a broker, which will follow one portfolio at its own multiple.

**Alerter / Fill card**: The part that posts to Discord, and its one card per signal.

**Watchdog**: A five-minute check during market hours, in the cloud, that posts problems such as a
part down or a missed broker login to Discord.

## Access

**Role**: What a person or agent may do on one market: viewer, trader, poweruser, or admin for the
whole site. Each role includes the ones below it. **Deny by default**: no role means no access.

**Control list / Controller**: Before roles (2026-10-04 → 10-18), the emails allowed to switch the
broker and log in, and a person on that list. Replaced by roles on the company dashboards (0151).

**Market path**: The `/india` or `/spxw` part of `trade.convexhedge.ai` that picks the market.

## Related

[GLOSSARY](../GLOSSARY.md) · [glossary-feed-engine](glossary-feed-engine.md) · [trading-engine](trading-engine.md) · [trading-engine-decisions-platform](trading-engine-decisions-platform.md)
