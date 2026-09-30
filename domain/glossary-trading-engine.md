> As of Convex-Hedge-Trading-Engine@b47d8ee, 2026-10-01

# Glossary — the trading engine

Split from [GLOSSARY](../GLOSSARY.md). **Canon is the repo's `CONTEXT.md`**, which indexes 463
terms, each a plain-language page in `Trading-Engine/Glossary/`. This note holds only the terms the
vault's engine notes use. Where they collide with the terminal's or the feed engine's words, see
GLOSSARY's *Collisions*.

## The engine as a whole

**Trading engine**: Convex Hedge's engine that runs strategies, watches market data and, later,
places orders. The map is [trading-engine](trading-engine.md).

**Engine instance**: One complete, independent copy of the engine: its own Redis, feeds, parts and
strategies, started from one **settings file** (TOML in `config/`). _Avoid_: stack, deployment.

**Compose profile**: The Docker Compose switch that picks an instance's feed: `live-us-databento`,
`live-india-fyers` or `replay`.

**Sandbox / Live trading**: Paper trading on live data with the simulated broker, and trading real
money. Only the sandbox exists.

**Part**: One process of an instance in its own container, such as the chain engine or the alerter.
_Avoid_: service, which is the feed engine's word.

## Data

**Bus client**: The only code that knows stream names. Every part reaches Redis through it.

**Feed adapter**: A process that connects to one source and publishes raw data in five **message
kinds**: quote, trade, instrument definition, feed status and statistic.

**Sampled top of book**: Databento's book at the end of each second in which it changed. The default
quote. The alternative is **every-change mode**.

**Latest value**: The newest message per key, kept seven days beside each stream. A late starter
reads it once. Strategies read only these.

**Chain engine / Derived data engine**: The part that works out forwards, IV and Greeks per expiry.
It is being renamed the derived data engine as it gains GEX, skew and candles (#150).

**Implied forward**: An expiry's forward price, fitted from calls and puts twice, from mids and from
last trades. **Implied index level**: the nearest expiry's mid forward, standing in for an index
level the vendor does not carry.

**Chain event / Chain snapshot**: A small recorded message saying an expiry was recomputed, and the
large numbered picture of every strike, kept in keyed state and never recorded.

**Lineage**: The bus ids and times that tie a derived message back to the raw event that caused it.

**Recording / Replay**: The exact copy of the bus in one `.jsonl.zst` file per run, and the adapter
that plays it back as if it were live.

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

## Broker and alerts

**Simulated broker**: The part that fills every instance's model account at the mid.

**Model account**: One pretend account per strategy instance: positions, cash, and realised and
unrealised PnL before charges.

**Fill delay**: The per-instance wait before the simulated broker fills. The fill uses the mid at
the end of the wait.

**Stale fill**: A fill that had to use an older mid or the last trade.

**PnL history**: A stream per instance of PnL samples, five days of them, which feeds the dashboard's
curve.

**Alerter / Fill card**: The part that posts to Discord, and its one card per signal.

## Related

[GLOSSARY](../GLOSSARY.md) · [glossary-feed-engine](glossary-feed-engine.md) ·
[trading-engine](trading-engine.md)
