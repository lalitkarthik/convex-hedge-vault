> As of delta-exchange-payoff@27a4d89, 2026-09-25

# Design decisions — what was chosen, and what replaced it

**One row per decision.** The canonical text is the record the row points at; this note is the map.
When a decision is replaced, its row moves to *Superseded* with the successor and the date — the old
choice stays visible, because the reason it lost is part of the answer.

Engine records live in `delta-exchange-payoff/docs/design/decisions/`. Terms: `delta-exchange-payoff/CONTEXT.md`.

## The engine's decision records

| # | Question | Chosen | Ticket, date | Standing |
|---|---|---|---|---|
| 0001 | How streams are named | `{event_type}:{VENUE}[:{UNDERLYING}]`; flat envelope, one Redis field per key; payload one JSON object | #58, 2026-09-09 | Stands, except its environment slot (0006) |
| 0002 | Where Redis runs | A container beside the services; persistence off; 2 GiB `maxmemory`, `noeviction`. Named fallback: ElastiCache for Valkey `cache.t4g.medium` | #69, 2026-09-09 | Stands, except the `store` group's start id (0010) |
| 0003 | The connection controller's policy | Five states; a budget of 10 **consecutive** failed reconnects; backoff 1 s doubling to 60 s, no jitter; silence past 45 s cuts the socket | #59, 2026-09-09 | Stands |
| 0004 | Where the bars live | Parquet, hive layout, S3 Standard, one bucket per environment | #67, 2026-09-09 | Stands; the S3 code path is #70, blocked on AWS |
| 0005 | Platform and region | ECS on EC2, `ap-south-1`, public subnet, `host` network mode, every container in one task definition | #68, 2026-09-09 | Stands, except its instance class (0008) |
| 0006 | The environment prefix in stream names | Removed — one local stack, one prod, never a staging | #74, 2026-09-12 | Stands |
| 0007 | The shape of the load | Every Python service compute-bound, one core by its event loop; Redis and `web` memory-bound; nothing disk- or network-bound | #75, 2026-09-12 | Stands; measured by I13 (#79) |
| 0008 | One instance or several | One `c7g.xlarge` (4 vCPU, 8 GiB), `derived` $78.07/month; `feed` reserves a whole vCPU. **Split to T4** when load passes 2.8 cores or `oms` places its first order | #78, 2026-09-12 | Stands |
| 0009 | When to compact | Nightly only, while the store is on local disk | #76, 2026-09-12 | Stands |
| 0010 | The store's crash protocol | Per-stream watermark with an index; checkpoint; flush intent; seal clock (R4, and R4d since #119); replay-gap check every poll (R5) | #63, 2026-09-12 | Stands; amended by #110, #119 |

**Two numbering systems collide.** Research tickets R4, R6 and R7 became records **0005, 0007 and
0008**. Inside record 0010, R1–R8 are *rules*, not records.

**One contradiction, surfaced rather than chosen.** Record 0004 and `CONTEXT.md` write the partition as
`date=/underlying=`; the files on disk are `underlying=BTC/date=2026-09-13/` since #77. The disk is
what the code does.

## Standing decisions made outside a record

| Decision | Made where | Why |
|---|---|---|
| **Split the monolith into services on Redis Streams**, keeping the monolith as the default (`DELTA_BUS` unset) | #57, 2026-09-11 | Change-safety: a new consumer costs producers nothing — the senior's pattern |
| **Redis alone — not Kafka, not both** | [message-buses](../learning-records/message-buses.md), 2026-09-07; kept by #57 | ~1,850 events/s and a handful of readers; Parquet holds history |
| **Ack on receipt; the store flush is the durability boundary** | 0010, #63 | An ack means delivered; a flush means safe |
| **Store flush every 300 s; retention 30 min by age** | #63; `message-bus.md` | A restarted store replays inside retention, so the loss window closes |
| **Publisher batch 50 ms** | I2, #61 | Measured; the hop never enters it while Redis stays beside `feed` |
| **Never forward-fill; `null` is not `0`** | `delta-exchange-payoff/CLAUDE.md` | A padded bar is a fabricated observation |
| **Venue IV and Greeks are reference columns, never inputs** | `delta-exchange-payoff/CLAUDE.md`; `test_no_delta_inputs.py` | The venue's fit lags the book it prices |
| **Every number carries `measured`, `assumed` or `derived`** | `CONTEXT.md` §6 | The tag says where to check when an input moves |
| **One `c7g.xlarge` for now; the next split is T4, not T2** | Owner, 2026-09-13; 0008 | T4 keeps `feed → Redis → store` on one machine |
| **#63 criterion 4 and #79 criterion 1 accept the 2026-09-12 evidence** in place of a full day | Owner, 2026-09-13 | The busiest hour is inside it; no decision would move |
| **IV/RV parked** — #31, #54, #116 | Owner | — |
| **No AI attribution** in commits, trailers or PRs | Owner; `delta-exchange-payoff/CLAUDE.md` | — |
| **A strategy publishes a desired position (Book 1), never an order**; orders are worked out **pooled**, `Book 2 − Book 4 − working`, after a short settling window; a pooled-neutral change rewrites Book 3 as a **reallocation** | `delta-exchange-payoff/docs/design/execution/books.md`; #128, 2026-09-17 | Two strategies wanting opposite things trade nothing; execution stays out of strategy code by construction |
| **The engine's mark is `client_order_id`**; a fill without it is discretionary; reconcile every 10 s and on each fill, a mismatch freezes that contract | `.../execution/books.md`, 2026-09-16 | Delta has no order-source field; positions carry no lineage |
| **One `oms` process** with risk checks and execution as modules; the sandbox is a second instance on venue `PAPER` with the paper broker inside | `.../execution/oms.md`, 2026-09-16 | Change-safety is between strategies, not inside one order's path |
| **Postgres for every state that must outlive a process**; Redis stays a pipe; **working orders live only in the execution module's memory**, rebuilt from the broker's open orders on restart | `.../execution/oms.md`; #128, 2026-09-17 | The senior named in-memory state as his system's gap; the broker is the better record of what is open |
| **Three ids on every envelope**: `decision_id`, `parent_event_id`, `actor`; the trace is a filter over the JSON log files; no event table, no OpenTelemetry, no log server | `.../execution/events-and-tracing.md`; #128, 2026-09-17 | Greg Young's correlation/causation pattern, spelled out; a second copy of the events is a second thing to keep in step |
| **Risk checks reject, never resize**; margin is priced on the **resulting portfolio** and only alerts until measured; a pooled order passes every contributing strategy's limits; loss-limit breach blocks opening orders, allows closes, never auto-flattens | `.../execution/rms.md`; #128, 2026-09-17 | A resized order is a value that stopped meaning what it says; margin is not additive per order |
| **Paper broker first, fills at the touch, fee and slippage 0 by default**; its manual door is a test hook with no route or command; testnet next; never real money in this phase | `.../execution/paper-broker.md`; #128, 2026-09-17 | Owner, 2026-09-16; real manual trades happen on Delta's own app |
| **Execution v1 = limit at touch, cancel and replace; buy legs first, wait, then sells** | `.../execution/oms.md`, 2026-09-16 | Margin; a market order on a thin 0dte wing |

How the work itself is run — tickets, tests, agents, branches — is [team-workflow](team-workflow.md).

## Superseded

| Was | Replaced by | When |
|---|---|---|
| No broker while the engine is one process | The services split on Redis Streams (#57) | 2026-09-11 |
| Flush the bar buffer hourly | Every 300 s, with replay from the last flush (#63) | 2026-09-07 → 09-12 |
| One `m7g.large`, 2 vCPU (0005) | One `c7g.xlarge`, 4 vCPU (0008) — `api`'s viewers could take `feed`'s core | 2026-09-12 |
| An `{env}:` prefix on every stream (0001) | No prefix (0006) | 2026-09-12 |
| Redis `maxmemory 1gb` as shipped by #65 | 2 GiB everywhere — 1 GiB was below the retention #61 measured | 2026-09-12 |
| The `store` group starting where 0002 said | Replay from the last flushed id (0010) | 2026-09-12 |
| A venue level in the partition path | `underlying=/date=` (#77) | 2026-09-12 |
| `/health` returning a literal `ok` | 503 on failure: `store` (#103), `feed` (#108), `discord-alerts` (#115). **`api` still always 200** | 2026-09-12 |
| A bounded reader retry that read only `>` | Pending list read back before `>` (#111) | 2026-09-12 |
| Orders diffed **per strategy**, `Book 1 − Book 3 − working` (#127) | Pooled, `Book 2 − Book 4 − working`, with a settling window and reallocations (#128) | 2026-09-16 → 09-17 |
| A `working_orders` table | Working orders in the execution module's memory, rebuilt from the broker's open orders (#128) | 2026-09-17 |
| `correlation_id` / `causation_id` and an `event_log` table (#127) | `decision_id` / `parent_event_id`, traced over the log files (#128) | 2026-09-17 |
| Margin checked per order, rejecting | Margin of the resulting portfolio, alerting until measured (#128) | 2026-09-17 |
| A manual-order API route and command for the paper broker (#127) | A test hook only (#128) | 2026-09-17 |
| Seal clock pinned only by streams `behind` (R4) | Also held by streams still catching up (R4d, #119) | 2026-09-14 |

## Related

[feed-engine](feed-engine.md) · [bar-store](bar-store.md) · [deployment-and-cost](deployment-and-cost.md) ·
[product-direction](product-direction.md) · [team-workflow](team-workflow.md)
