> As of delta-exchange-payoff@7783a4b, 2026-09-14

# Bar store — sealing, flushing, replay

The `store` service of the [feed engine](feed-engine.md): the only writer of the one-minute bar
tables, and the data a backtest would read. Terms resolve to `delta-exchange-payoff/CONTEXT.md` §3.

## The four tables

| Table | Folded from | Holds |
|---|---|---|
| `quote-bars` | `md.option_quote` — top of book | one row per contract per minute |
| `reference-bars` | `md.option_reference` — the venue's ticker, its IV and Greeks as columns | the same |
| `computed-bars` | `computed.chain` — **our** IV, Greeks and forward, published by `api` | the same |
| `spot-bars` | `md.index_quote` | one row per underlying per minute |

Hive layout: `<table>/underlying=BTC/date=2026-09-12/…`. No venue level (#77). Files are named
by minute and **generation**, e.g. `20260912T155600Z-g00000123.parquet`, so two processes cannot
collide on one name.

## Two steps, two words

**A bar is sealed, then flushed.** Never "saved" or "written".

1. **Seal** — close a minute's bucket; nothing more can enter it. **A seal is final.**
2. **Store flush** — write sealed bars to Parquet, every **300 s**. This, and nothing before it,
   is the durability boundary. An ack is not.

A bar keeps the extremes and destroys the path. **A minute with no arrivals produces no row**;
nothing is forward-filled.

## Crash and restart — record 0010

Before the split a crash lost up to five minutes of buffer. On the bus, Redis keeps 30 minutes
whether or not anyone acked, so a restarted store asks for everything after the last entry it
**flushed**.

| Part | What it is |
|---|---|
| watermark | Per stream: the entry id last flushed, plus its logical index |
| checkpoint | `<root>/_store-checkpoint.json` — the watermarks and each aggregator's seal point |
| flush intent | `<root>/_store-flush-intent.json` — written before the Parquet, deleted after the checkpoint |
| seal clock (R4, R4d) | `min(wall clock, time inside the last id of any stream still behind, time inside the last drained id of any stream still catching up)` — so a replay does not seal ahead of what it has read |
| replay gap (R5) | Group position older than the stream's oldest entry: data existed and is gone. **Checked every 10 s**, not only at start-up (#103) |

**Ack means delivered. Flushed means safe.** They are different facts.

**Every start-up now writes a `store.checkpoint` record with `replayed_from`** (#110). Before
that, a clean replay logged nothing, and a lost minute left only a file name as evidence.

## The restart loss window — closed by #119

**Before the fix**, a restarted store sealed on **every** drain pass, including empty ones during
replay. A seal at `minute_end + grace` refused the rest of that minute in any table whose grace was
that short or less:

| Seal pass at | Tables that lost the minute open at the restart |
|---|---|
| `minute_end + 0.0 … 1.9` s | none |
| `minute_end + 2.0 … 7.9` s | `computed-bars` alone (grace 2.0 s) |
| `minute_end + 8.0` s and after | all four (ticker grace 8.0 s) |

It happened live at 15:56 on 2026-09-12 (#110). **Equalising the graces moved the boundary; it
would not have removed it.**

**The fix (#119, `b3358ea`):** the seal clock also holds at the drained position of every stream
not yet shown caught up by a **short** `>` read (`RedisSubscription.caught_up_at`). The hard part
was the **release valve**: release needs one read, not a new entry, so a quiet, never-written or
trimmed stream releases within one pass. Only a reader that never completes a pass holds the clock,
and that reader is already a loud 503. All six offsets now lose nothing, in a test.

**Proven live on 2026-09-13**: `docker kill -s KILL` at 19:28:30Z, mid-minute and mid-interval; 19:24–19:32
on disk once in all four tables, 0 duplicate keys. An earlier kill at 19:04 lost `computed-bars` 19:04,
but the api never published that minute (#122) — the store folded all it was given.

## Pause — a known loss, #121

A pause at 19:18:07Z kept the open minute (19:18) in `quote-bars` only. `reference-bars` and `spot-bars`
lost it, though 507 ticker and index frames arrived at 19:18:04.7Z, and nothing counted it.
`docs/recording-contract.md` promises that minute is written on resume. **Until #121 lands, a paused
recording can drop the minute it was paused in, in three of four tables.**

## What the recordings show

- **Duplicates: none, ever.** 0 minutes in more than one flush file and 0 duplicate
  `(symbol, minute)` keys across the 2026-09-12 partition, all four tables (#63).
- **Losses: three kinds in one day, every one sealed empty.** 97 minutes trimmed unread (#103), one
  minute at a replay seam (#110), ten minutes with the venue socket down (#108).
- **Computed-bars sampling miss** (#23's race): `measured` **19.1%** (214 of 1,118 minutes) on the
  monolith before the fix; **0 interior misses in 348 minutes** on the split store. The two misses
  that day sit on store discontinuities. `derived`: zero in 348 bounds the rate below ~0.9% at 95%.
- **Compaction** on a real day: 280 files → 4, 568,001 rows, 29.44 → 25.11 MiB, every hole kept
  (`measured`, #63). Nightly only, while the store is on local disk (record 0009).
- **Disk:** `measured` 1.49 KB/s written by `store`, BTC alone. `docker stats` reported 25.4 B/s —
  it does not see a bind mount (#79).

## Where it is going

- **S3 Standard, one bucket per environment** (record 0004). The code path lands with #70;
  criteria 2–4 need AWS credentials.
- Recording pause and resume travel as a `control.command`; a pause commits a generation (#109).

## Pointers

- Design: `delta-exchange-payoff/docs/design/lld/store.md`, `lld/store-replay.md`, `lld/store-health.md`
- Protocol and argument: `delta-exchange-payoff/docs/design/decisions/0010-store-replay.md`
- Front door for storage: `delta-exchange-payoff/docs/storage-start-here.md`
- The restart seam test: `delta-exchange-payoff/engine/tests/test_store_restart_seam.py`
- Tools: `tools/measure_computed_gaps.py`, `tools/compact_store.py`

## Related

[feed-engine](feed-engine.md) · [service-health](service-health.md) ·
[silent-success](../learning-records/silent-success.md) — why every loss above looked like success
