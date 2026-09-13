> As of delta-exchange-payoff@7783a4b, 2026-09-14

# Feed engine — our live crypto option analytics

**`delta-exchange-payoff`** at `D:\Convex Hedge\delta-exchange-payoff`. A live engine over Delta
Exchange India: it holds one websocket, computes **our own** forward, implied vol and Greeks beside
the venue's, and records one-minute bars to Parquet. It is the system this vault is here to improve.

**Not the terminal.** [platform-map](platform-map.md) is Convex Hedge's backtesting terminal —
history replayed minute by minute. This engine is live. They share the vocabulary of a chain, a leg
and an expiry; where words collide, [GLOSSARY](../GLOSSARY.md) records both.

## Why it is shaped like this

The senior's execution engine is **feed, Redis, execution, strategies and a trading terminal**, as
separate programs on Redis Streams ([what-the-senior-said](../teach/message-bus/what-the-senior-said.md)).
His stated reason is change-safety: a new strategy must not touch the running ones. The split copies
that pattern, and leaves named, costed slots for `oms` and `strategy`, which are **not built**.

**Backtests read stored files, never the bus** — so the [bar store](bar-store.md) is the part a
backtest would stand on.

## What runs

The engine was one process. **Since 2026-09-12 it is seven containers on a Redis Streams bus** (epic #57).

| Service | Does | Entry point |
|---|---|---|
| `feed` | The only process that contacts the venue. Adapter, controller, supervisor, publisher | `feed_main.py` |
| `store` | Only writer of the four bar tables. Reads losslessly, seals, flushes Parquet | `store_main.py` |
| `api` | Ladder, REST routes, `/ws/chain`. Solves our IV and Greeks. No venue socket | `main.py` |
| `web` | Next.js page. Renders, computes nothing | `web/` |
| proxy | `nginx:alpine`, one origin on host port 8080 | `proxy/nginx.conf` |
| Redis | The bus. No persistence, 2 GiB ceiling, `noeviction` | `compose.yml` |
| `discord-alerts` | Reads the `alert` stream only, posts to a webhook | `alert_main.py` |

**Two compositions, both supported.** `DELTA_BUS` unset is the **monolith** — one process, an
in-process fan-out, serving `:8000` with `web` on `:3000`. `DELTA_BUS=redis` is **split mode**, the
table above, started with `docker compose -p dxp up -d`.

## How data moves

- `feed` publishes `md.option_quote`, `md.option_reference`, `md.index_quote` to streams named
  `{event_type}:{VENUE}[:{UNDERLYING}]`, in 50 ms pipelined batches, trimmed by age.
- `store` reads them **losslessly** in its own consumer group and folds bars.
- `api` reads them **drop-oldest** into the chain cache, solves, and publishes `computed.chain`,
  which `store` folds into `computed-bars`.
- `store` publishes each sealed bar as `md.option_bar`; `api`'s `bar-buffer` group holds the
  not-yet-flushed right edge for the history routes.
- `feed.connection` and `heartbeat` carry the connection state to `api` and the badge.
- Commands (`pause`, `resume`, `reconnect`, recording) travel as `control.command`.

Ten event types, catalogued in `delta-exchange-payoff/docs/design/events.md`.

## What the split promises, and what it does not

| Promises | Does not promise |
|---|---|
| A new consumer costs producers nothing | **A seal is final** — a minute sealed while its data is unread is lost |
| A restarted `store` loses nothing inside retention — it replays from the last **flushed** entry, not the last acked | **Retention is 30 minutes** — a store stopped longer loses the difference |
| A minute with no arrivals produces no row — never forward-filled | **An alert is not durable** — a failed post is gone, now logged |

## The constants that govern it

**The table, with the file each value lives in, is `delta-exchange-payoff/docs/split-start-here.md` §4.**
The three that shape every design question: **retention 30 minutes** by age, a **store flush every
300 s**, and a **50 ms publisher batch**. Why each was chosen: [design-decisions](design-decisions.md).

## Where the truth lives — read in this order

1. `delta-exchange-payoff/CONTEXT.md` — every term. Canon for the engine, as this vault's glossary is for the terminal
2. `delta-exchange-payoff/docs/split-start-here.md` — what runs, what was chosen, one line per decision
3. `delta-exchange-payoff/docs/design/hld.md` — the parts and the traffic; one LLD per component under `docs/design/lld/` (index: `lld/index.md`)
4. `delta-exchange-payoff/docs/design/cloud/message-bus.md` and `.../data-feed-engine.md` — the two assembled design documents
5. `delta-exchange-payoff/docs/split-numbers.md` — every measured figure with its run
6. `delta-exchange-payoff/docs/design/decisions/` — records 0001–0010, one question each

The maths is a separate front door: `delta-exchange-payoff/docs/maths-start-here.md`.
Storage: `delta-exchange-payoff/docs/storage-start-here.md`.

## Status, 2026-09-14

- **Done:** everything in #57 that does not need AWS. **#118, #119 and #110 closed 2026-09-14.**
  Suite 1,610 passed at `7783a4b`, with Docker up.
- **Also closed 2026-09-14:** #120 (the stack runs `7783a4b`), #79 (on the owner's amended criterion).
- **Open, found live 2026-09-13:** #121 — a pause loses the open minute from `reference-bars` and
  `spot-bars`; #122 — the api's minute pass skipped a minute of `computed.chain`, silently.
- **#63** stays open on criterion 5 until #121 lands; a hard kill at 19:28:30Z proved criterion 3 live.
  See [session-log](../session-log.md).
- **Blocked on AWS credentials:** #70 (store to S3), #71 (deploy prod), #80 (measure the hop). #57 closes after them.
- **Parked by the owner:** IV/RV — #31, #54, #116.

## Related

- [bar-store](bar-store.md) — sealing, flushing, replay, and the one known loss window
- [service-health](service-health.md) — what each `/health` can and cannot see, and how to ask Redis instead
- [deployment-and-cost](deployment-and-cost.md) — the instance, RAM, cost, and the next topology
- [silent-success](../learning-records/silent-success.md) — the defect shape this engine keeps producing
- [message-buses](../learning-records/message-buses.md) — why a bus, and Redis Streams' mechanics
- [tests-that-prove-nothing](../learning-records/tests-that-prove-nothing.md) — how its suite was made honest
