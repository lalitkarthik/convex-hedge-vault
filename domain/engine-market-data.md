> As of Convex-Hedge-Trading-Engine@b47d8ee, 2026-10-01

# Engine market data — bus, feeds, chain engine, recordings

The data half of the [trading-engine](trading-engine.md). Canon is
`Trading-Engine/Architecture/Message bus design.md`, `Data feed engine design.md` and
`Chain engine design.md`. User-facing behaviour is in `Trading-Engine/Guide/`.

## The bus

**Redis Streams, one Redis per engine instance**, reached only through the shared **bus client**
(0003, 0004). The old version floor was Redis 6.2. It is now **Redis 7.4 or Valkey 9**, because
each latest value needs to expire on its own.

- **One stream per message kind**, under a category prefix: market data, chain, strategy, fill.
  Only the bus client knows the stream names. Raw data and worked-out data never share a category (0021).
- **One header on every message**: kind, layout version, source, instrument id, exchange time,
  receive time, publish time and a sequence number per source. Times are UTC nanoseconds. Prices
  are fixed-point numbers. The bus gives each message an id, and every log line that touches the
  message carries it.
- **Short memory**: ten minutes per stream by default, with a window per category. Nothing goes to
  disk. The **recording** is the permanent copy.
- **Latest value of every key**, kept seven days (0020). A part that starts late reads this snapshot
  once and then the live stream. **A strategy reads only latest values, never a stream.**
- **Keyed state beside the streams** (0026). Large pictures such as the numbered **chain snapshot**
  live there: one entry per expiry, and old versions are kept ten seconds. A record store holds
  small facts that must outlast a restart. A **PnL history** stream per strategy instance is
  written only by the simulated broker.
- **Two reading rules.** A market-data reader keeps only the **newest message per instrument** when
  it falls behind, and counts what it skipped. Feed status is kept per feed. A statistic is kept per
  instrument and per statistic type. **In-order reading** uses a consumer group with
  acknowledgements, as the simulated broker does for signals. A message trimmed away before its
  acknowledgement is reported, never skipped silently.

## Feed adapters — raw data only

A family of adapters, one process each, built on a shared **data feed manager**. An adapter
translates the source's names into the engine's own **instrument id**, which carries the product
root because SPX and SPXW share expiries (0006). **It never calculates anything** (0008). It
publishes five kinds of message: quote, trade, instrument definition, feed status and statistic.

| Adapter | Source | Notes |
|---|---|---|
| Databento | SPXW from OPRA, live or from downloaded `.dbn.zst` files (file mode) | Default quote is the **sampled top of book**, the book at the end of each changed second (0011). Every change is a switch. Subscribes by option symbol. |
| Fyers | NIFTY (NSE) and SENSEX (BSE), one process, one login (0016) | A person logs in each morning after 06:30 IST (0014). The adapter decodes the socket itself (0015). The index level is published as a trade with no size (0018). **Candle mode** rebuilds a past day (0017). |
| Replay | A recording | To every other part, replay is indistinguishable from live. It refuses a live instance. |
| Synthetic | Invented prices | Used for demos and tests. |

**Subscriptions** use a days-to-expiry filter, set per feed. SPXW defaults to today and tomorrow;
India's example keeps 0 to 7 days. Adapters resubscribe at each trading day without a restart.
**Feed status** is one of connected, degraded, stale, disconnected or closed. Stale means silent
past a gap of a few seconds during a session. Outside a session the status is closed. **A gap is
never backfilled.**

**Daily statistics** are open interest each morning plus eight after-close figures, which arrive
in two passes at about 16:23 and 17:45 New York. They are **republished with the definitions**,
because the bus forgets after ten minutes (0013).

**Times.** A Databento sampled quote is timed at the end of its second (0027). That superseded 0012,
which had patched only the records with no exchange time. A Fyers tick with no exchange time still
takes its receive time and is counted. Recordings made before 2026-09-28 carry the older quote times.

## The chain engine

It is one process in every profile. **On every quote or trade it recomputes that option's whole
expiry** (0025). Bursts are coalesced.

- **Implied forward and discount factor, twice**: once from mid prices and once from last trades,
  from at least three strikes of the current session. Strikes whose spread is over 30% of the mid
  are left out of the mid fit. An implausible fitted discount factor falls back to 1, marked.
- **IV from the out-of-the-money option only** (0028), whatever its spread. A strike with no usable
  price gets a reason, never a guessed number.
- **Five Greeks** for every call and put. **The Greeks take the forward as the spot level** (0022).
- **Time to expiry counts open-market time only**: trading days, 252 to the year, from calendar
  files per exchange and year for Cboe, NSE and BSE (0023). Early closes and Muhurat trading count
  as closed. A missing year stops the engine with a clear message.
- **Implied index level**: the nearest expiry's mid forward, published as a stand-in for the S&P 500
  level that Databento does not carry.
- It publishes a small **chain event** (recorded, carries its lineage, 0024) and a numbered **chain
  snapshot** of every strike (keyed state, never recorded).
- **Speed:** one SPXW expiry recomputes in about 5 ms at the 99th percentile on a full day. A full
  Indian day and a full every-change day are still to be measured.
- **Becoming the derived data engine** in feature #150: GEX, its levels, skew figures and
  one-minute index candles, with a SQLite history (0046, 0047, on the branch).

## Recording and replay

The recorder writes **every message, in order, to one `.jsonl.zst` file per run** (0010). It records
the market data, strategy and fill categories by default. Chain data is recorded as events only,
and a replay leaves it out unless a setting asks for it. **A replay never republishes recorded
strategy decisions or fills**: the strategies and the broker work afresh. Below a free-disk floor
(10 GB by default) the recorder pauses, loudly.

**Sizes:** about 300 MB a day for two SPXW expiries sampled, and 8–11 GB every-change. The
acceptance day, 2026-09-25, produced 5,591,253 messages in about 280 s. The whole procedure is in
`README.md`, *Acceptance on a real trading day*.

**Tests run on recordings.** `fixtures/` holds one busy real SPXW second and two invented NIFTY
seconds. `tests/end_to_end/` replays them through a real Redis. No test needs a vendor or a secret.

## Still open (from the design pages)

- Retention in the every-change mode on a busy Monday. The rule is to drop to five minutes above 2 GB
  of Redis memory, or to narrow the strike band if publishing cannot keep up.
- A holiday calendar per market for the feeds. The chain engine already has calendars.
- Which source serves Bitcoin options and MCX options.
- How Redis runs on AWS: a container, or the managed service.
- The rules for changing message fields once parts depend on them.

## Related

[trading-engine](trading-engine.md) · [engine-strategies](engine-strategies.md) ·
[engine-lineage](engine-lineage.md) · [volatility](volatility.md) · [option-chain](option-chain.md)
