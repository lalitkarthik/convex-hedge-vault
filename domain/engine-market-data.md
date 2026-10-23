> As of Convex-Hedge-Trading-Engine@06e547fa, 2026-10-23

# Engine market data — bus, feeds, chain engine, recordings

The data half of the [trading-engine](trading-engine.md). Canon is
`Trading-Engine/Architecture/Message bus design.md`, `Data feed engine design.md` and
`Chain engine design.md`. User-facing behaviour is in `Trading-Engine/Guide/`: `The message bus.md`,
`Market data feeds.md`, one page per adapter, `The chain engine.md`, `The forward method.md` and
`Recording and replay.md`. What changed, and when, is in `Trading-Engine/Guide/Changelog.md`.

**Decision numbers repeat in this repo** (0045–0048, 0073, 0132 and others each name two or three
records). This note gives the title with the number where two records share it.

## The bus

**Redis Streams, one Redis per engine instance**, reached only through the shared **bus client**
(0003, 0004). The version floor is **Redis 7.4 or Valkey 9**, because each latest value needs to
expire on its own. (It was Redis 6.2 before the latest values came.)

- **One stream per message kind**, under a category prefix: market data, chain, strategy, fill.
  Only the bus client knows the stream names. Raw data and worked-out data never share a category (0021).
- **One header on every message**: kind, layout version, source, instrument id, exchange time,
  receive time, publish time and a sequence number per source. Times are UTC nanoseconds. Prices
  are fixed-point numbers. The bus gives each message an id, and every log line that touches the
  message carries it.
- **Short memory**: ten minutes per stream by default, with a window per category. The
  **recording** is the permanent copy of the messages.
- **What reaches disk.** On a laptop Redis keeps nothing on disk. **On the cloud machines Redis
  writes a snapshot at the nightly stop and reads it back each morning**, so model accounts, the
  five-day PnL history, the broker's place and the alerter's records carry over. Prices are not
  kept (`Guide/Running on AWS.md`). The bus design page still says Redis "writes nothing to disk".
- **Latest value of every key**, kept seven days (0020). A part that starts late reads this snapshot
  once and then the live stream. **A strategy reads only latest values, never a stream.**
- **Keyed state beside the streams** (0026). Large pictures such as the numbered **chain snapshot**
  live there: one entry per expiry, and old versions are kept ten seconds. A record store holds
  small facts that must outlast a restart, such as the selected broker. A **PnL history** stream
  per strategy instance is written only by the simulated broker.
- **Two reading rules.** A market-data reader keeps only the **newest message per instrument** when
  it falls behind, and counts what it skipped. Feed status is kept per feed. A statistic is kept per
  instrument and per statistic type, and a **previous close** also per session it serves (0135).
  **In-order reading** uses a consumer group with acknowledgements, as the simulated broker does for
  signals. A message trimmed away before its acknowledgement is reported, never skipped silently.
- **One bus, several markets** (since 13 October, 0120). A settings file can give a part a
  **market id**; every Redis name then carries that market's prefix. The pilot uses this. The
  company's India and SPXW instances, the recorder and the research tools run with no prefix.
- **Cheaper reading** (since 7 October). Each part decodes with a decoder prepared once per message
  kind, about 5.5 times cheaper, and drops superseded messages before it decodes them. Since
  14 October a dashboard that meets a message it cannot read logs it and skips it.
- **The pilot's Redis** (since 18 October): a 1 GB memory limit inside a 1.5 GB container. At the
  limit it refuses writes and deletes nothing. A pilot deploy no longer replaces Redis.

## Feed adapters — raw data only

A family of adapters, one process each, built on a shared **data feed manager**. An adapter
translates the source's names into the engine's own **instrument id**, which carries the product
root because SPX and SPXW share expiries (0006). **It never calculates anything** (0008). It
publishes quotes, trades, instrument definitions, feed status and statistics.

| Adapter | Source | Notes |
|---|---|---|
| Databento | SPXW from OPRA, live or from downloaded `.dbn.zst` files (file mode) | Default quote is the **sampled top of book**, the book at the end of each changed second (0011). Every change is a switch. Subscribes by option symbol. At start it fetches the previous session's closes from the historical service. |
| Fyers | NIFTY (NSE) and SENSEX (BSE), one process, one login (0016) | A person logs in each morning after 06:30 IST, now usually with one click on the Broker page (0014). The adapter decodes the socket itself (0015). The index level is published as a trade with no size (0018). **Candle mode** rebuilds a past day (0017). |
| Upstox (since 1 October) | NIFTY and SENSEX | A one-year read-only Analytics token, so no morning login (0045 Upstox). Upstox sends a whole record per instrument about once a second; the adapter publishes only what moved. A quote takes Upstox's message time (0047 Upstox). No candle mode. |
| Zerodha (since 6 October) | NIFTY and SENSEX, through Kite Connect | A person logs in each morning, after 07:35 IST (0067). In the cloud India instance since 8 October (0076 Zerodha). **No live check on record**: #253 (live check) and #252 (a real captured minute) were closed as deferred on 6 October, the Guide still waits for both, and the test minute is hand-built. |
| Replay | A recording | To every other part, replay is indistinguishable from live. It refuses a live instance. |
| Synthetic | Invented prices | Used for demos and tests. |

**The previous close** (since 15 October, 0135) is a new statistic kind from all four live feeds:
the close of the session before, **stamped for the session it serves**, so Thursday's close before a
Friday holiday serves Monday. The dashboard measures every day change from it. Older parts cannot
read the kind, so **every part of an instance must be deployed together**.

**Several Indian feeds, one selected broker.** From 1 to 4 October an instance ran one Indian feed,
chosen by Compose profile (0048 one Indian feed). Since 4 October one India instance runs every
named feed and the **selected broker**, kept in the record store, decides which one publishes
(0056, which superseded that 0048). A **publishing lease** stops two feeds publishing at once; a
switch pauses prices for a few seconds and restarts nothing. The cloud India settings name Fyers,
then Upstox, then Zerodha; Fyers is selected until someone chooses. A poweruser or admin switches on
the Broker page ([engine-dashboard](engine-dashboard.md)).

**The pilot's shared market** (since 11 October) uses one Upstox feed for every client. Since
14 October it follows every NIFTY and SENSEX expiry of the next **30 days** (it was 7): about 2,700
contracts, near Upstox's 3,000 per connection. Past that, the adapter drops the furthest expiries
and logs which.

**Subscriptions** use a days-to-expiry filter, set per feed. SPXW defaults to today and tomorrow;
India's example keeps 0 to 7 days. Adapters resubscribe at each trading day without a restart.
**Feed status** is one of connected, degraded, stale, disconnected or closed. Stale means silent
past a gap of a few seconds during a session. Outside a session the status is closed. **A gap is
never backfilled.** A feed that is not the selected broker reports disconnected, with the reason
"another broker is selected".

**Daily statistics** are open interest each morning plus eight after-close figures, which arrive
in two passes at about 16:23 and 17:45 New York. They are **republished with the definitions**,
because the bus forgets after ten minutes (0013). The Indian feeds send open interest as it changes.

**Times.** A Databento sampled quote is timed at the end of its second (0027). That superseded 0012,
which had patched only the records with no exchange time. A Fyers tick with no exchange time still
takes its receive time and is counted. Zerodha times are whole seconds. Recordings made before
2026-09-28 carry the older quote times.

## The chain engine

It is one process in every profile. **On every quote or trade it recomputes that option's whole
expiry** (0025), at most once per **recompute floor** of 0.1 s (since 7 October, 0073 recompute
floor). Prices inside the floor are gathered into one chain event; a quiet market publishes nothing.

- **One forward per expiry: the ATM forward** (since 15 October, 0132 ATM forward only). Among the
  strikes whose call and put both have a usable mid in the current session, with a spread of at
  most 30% of the mid, take the strike where call minus put is smallest. Forward = strike + (call −
  put), with the **discount factor taken as one**. If that pair was quoted more than 60 s apart, the
  next strike is used and marked "next strike". With no usable pair the expiry has no forward and
  its figures stay blank.
- **History of the forward.** Until 15 October the engine fitted a **regression forward** twice,
  from mids and from last trades, over at least three strikes, with a fitted discount factor that
  fell back to 1 when implausible. On 7 October the ATM forward came in beside it as a dashboard
  switch (0073 ATM forward). On 15 October the regression forward was retired; every strategy has
  traded on the ATM forward since. Old fields still read as **retired fields**.
- **IV from the out-of-the-money option only** (0028), by Black-76 against the forward, between
  0.1% and 1,000% a year. A strike with no usable price gets a reason, never a guessed number.
- **Greeks.** Five for every call and put, taking the forward as the level (0022). Since
  18 October also **vanna, volga and charm** (0156), in the chain snapshot for the Research Engine
  only; no card or page shows them. The same change gave every strategy one at-the-money pick (the
  strike nearest the forward, the lower on a tie) and one 252-day year.
- **Time to expiry counts open-market time only**: trading days, 252 to the year, from calendar
  files per exchange and year (0023). NSE and BSE close at 15:40 IST since 3 August 2026 (15:30
  before). Early closes and Muhurat trading count as closed. Files exist for Cboe 2026–2027 and NSE
  and BSE 2026 only, and **a missing year stops the engine** with a clear message.
- **Implied index level**: the nearest expiry's forward, a stand-in for the S&P 500 level that
  Databento does not carry. The dashboard calls it IMPLIED SPOT.
- It publishes a small **chain event** (recorded, carries its lineage, 0024) and a numbered **chain
  snapshot** of every strike (keyed state, never recorded).
- **Speed.** As of 1 October: about 5 ms at the 99th percentile for one SPXW expiry on a full day.
  On the India capture of 7 October (Upstox, mid-session) it was about 7% busy, and the slowest one
  in a hundred chain events came about 21 ms after its price, against limits of 10% and 100 ms.
  Retiring the regression forward brought 7% to 5.2%. A cloud core is about 2.2 times slower.

**The derived figures** came with feature #150, *Dashboard analytics tabs*, merged 3 October. The
branch called the chain engine the "derived data engine"; the name in the Guide stays chain engine.
It now also builds one-minute index candles, gamma exposure with R1–R4, S1–S4 and the flip (dealers
assumed long calls and short puts, 0050), skew figures, open interest by the minute, a smile
snapshot every minute (since 8 October) and a **volatility reading** per root per closed minute
(merged 11 October), with seven realised-volatility methods since 16 October
([realised-volatility-estimators](realised-volatility-estimators.md)). None of these is on a
strategy's card yet.

**The history store** keeps them: one SQLite file on a named Docker volume (0047 SQLite), one per
market. Candles, levels and minute readings keep 30 sessions; daily readings are kept for good;
smile snapshots sit in a second file for ten sessions. After each close the engine copies the store
and keeps the newest seven copies. A history begins on the first day the chain engine ran.

## Recording and replay

The recorder writes **every message, in order, to one `.jsonl.zst` file per run** (0010). It records
the market data, strategy and fill categories by default. Chain data is recorded as events only,
and a replay leaves it out unless a setting asks for it. **A replay never republishes recorded
strategy decisions or fills**: the strategies and the broker work afresh. Below a free-disk floor
(10 GB by default) the recorder pauses, loudly.

**The recorder runs on laptops only.** The cloud machines record nothing. Since 7 October a capture
tool copies a running bus, laptop or cloud (through port forwarding), into a bus capture, without
changing the bus.

**Sizes:** about 300 MB a day for two SPXW expiries sampled, and 8–11 GB every-change. The
acceptance day, 2026-09-25, produced 5,591,253 messages in about 280 s. The whole procedure is in
`README.md`, *Acceptance on a real trading day*.

**Tests run on recordings.** `fixtures/` holds one busy real SPXW second, two invented NIFTY seconds
and a synthetic demo. `tests/end_to_end/` replays them through a real Redis, and now also covers the
Upstox and Zerodha feeds, a broker switch, an India chain replay, the Compose profiles and a stepped
day. No test needs a vendor or a secret.

**The stepped engine** (since 13 October). The chain engine, simulated broker, trading journal and
strategy runner can run one minute at a time in one process, on a simulated clock, with an
in-memory bus. The Research Engine's backtest host drives it, so a backtest uses the live code
(`Guide/The stepped engine.md`).

## Still open (from the design pages)

- Retention in the every-change mode on a busy Monday. The rule is to drop to five minutes above 2 GB
  of Redis memory, or to narrow the strike band if publishing cannot keep up.
- A holiday calendar per market for the feeds. The feeds read a calendar only to stamp the previous
  close; on a holiday they still show stale, not closed.
- Which source serves Bitcoin options and MCX options.
- How Redis runs on AWS. The design page still lists it as open. In practice each machine runs Redis
  as a container with a nightly snapshot.
- The rules for changing message fields once parts depend on them. The previous close showed the
  cost: the whole stack must deploy together.
- Zerodha's live check, and Upstox's answers outside market hours and to a cancelled token.
- A full recorded Indian day and an Indian open, to confirm the chain engine's speed targets.
- Whether NIFTY and SENSEX index levels still move between 15:30 and 15:40.

## Related

[trading-engine](trading-engine.md) · [engine-strategies](engine-strategies.md) ·
[engine-dashboard](engine-dashboard.md) · [engine-lineage](engine-lineage.md) ·
[volatility](volatility.md) · [option-chain](option-chain.md) ·
[realised-volatility-estimators](realised-volatility-estimators.md)
