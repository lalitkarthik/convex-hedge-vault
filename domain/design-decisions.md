> As of delta-exchange-payoff@fce8d39, 2026-10-01

# Design decisions — what was chosen, and what replaced it

**One row per decision.** The canonical text is the record the row points at; this note is the map.
When a decision is replaced, its row moves to *Superseded* with the successor and the date — the old
choice stays visible, because the reason it lost is part of the answer.

Engine records live in `delta-exchange-payoff/docs/design/decisions/`. Terms: `delta-exchange-payoff/CONTEXT.md`.

**Since 2026-10-01 the current engine is `Convex-Hedge-Trading-Engine`.** Its 44 records are mapped in
[trading-engine-decisions](trading-engine-decisions.md); the rows below are `delta-exchange-payoff`'s, kept as
history and as the prior design for execution. How the two line up: [engine-lineage](engine-lineage.md).

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
| **Store flush every 300 s; retention 30 min by age** — *built*. The execution design (#129) plans 60 s flushes to S3, 5 min retention per feed, a store that refuses retention under 3 × flush, and Redis AOF every second; **design only, no code** | #63; `message-bus.md`; `.../execution/message-bus.md` | A restarted store replays inside retention, so the loss window closes |
| **Publisher batch 50 ms** | I2, #61 | Measured; the hop never enters it while Redis stays beside `feed` |
| **Never forward-fill; `null` is not `0`** | `delta-exchange-payoff/CLAUDE.md` | A padded bar is a fabricated observation |
| **Venue IV and Greeks are reference columns, never inputs** | `delta-exchange-payoff/CLAUDE.md`; `test_no_delta_inputs.py` | The venue's fit lags the book it prices |
| **Every number carries `measured`, `assumed` or `derived`** | `CONTEXT.md` §6 | The tag says where to check when an input moves |
| **One `c7g.xlarge` for now; the next split is T4, not T2** | Owner, 2026-09-13; 0008 | T4 keeps `feed → Redis → store` on one machine |
| **#63 criterion 4 and #79 criterion 1 accept the 2026-09-12 evidence** in place of a full day | Owner, 2026-09-13 | The busiest hour is inside it; no decision would move |
| **IV/RV parked** — #31, #54, #116 (`delta-exchange-payoff` only; the trading engine built its IV vs RV page — #306, reworked by #558, live 2026-10-17) | Owner | — |
| **No AI attribution** in commits, trailers or PRs | Owner; `delta-exchange-payoff/CLAUDE.md` | — |
| **A strategy publishes a target in strategy units, never an order**; a client's Book 1 = target × that client's units; orders are worked out **pooled within one client**, `Book 2 − Book 4 − working`, after a short settling window; a pooled-neutral change rewrites Book 3 as a **reallocation** | `delta-exchange-payoff/docs/design/execution/books.md`, `clients.md`; #128, 2026-09-17; #130, 2026-09-28 | Two strategies wanting opposite things trade nothing; the strategy decides the shape, the client the size |
| **The engine's mark is `client_order_id`**; a fill without it is discretionary; reconcile every 10 s and on each fill; reconciliation **adopts the broker's record and repairs**: at most 3 re-fires per contract per decision after a cancel, at most 2 Book 4 repairs per contract per day, then the contract freezes; Book 6 never causes an order | `.../execution/books.md`; #129, 2026-09-28 | Delta has no order-source field; the 20 September ask for a reconciliation that re-fires |
| **One OMS per client** (`oms-<client>`, one broker account each, configured by `clients/<id>.yaml`), with risk checks and execution as modules; **nothing crosses clients**; the sandbox is **paper clients**, each with its own paper broker; `oms:* kill` is the firm-wide kill | `.../execution/clients.md`, `oms.md`; #130, 2026-09-28 | The 25 September ask: clients subscribe to strategies by risk appetite and capital |
| **Postgres for every state that must outlive a process, reached only through the bus**: a **persistence service** is its only client, idempotent by `event_id`, and answers restore requests; the OMS has no database connection and publishes each order's record before sending it; **working orders live only in memory**, rebuilt from the broker's open orders | `.../execution/message-bus.md`, `oms.md`; #128, 2026-09-17; #129, 2026-09-28 | The senior named in-memory state as his system's gap; one writer to Postgres |
| **Strategy state is checkpointed** (`strategy_checkpoints`, JSONB with `schema_version`), restored over the bus before the first evaluation; a **signal card** is recorded at every decision for slippage research, never read by the order path | `.../execution/strategy-worker.md`; #129, 2026-09-28 | The 20 September asks: state as JSONB over the bus, signal cards |
| **Data adapters and broker adapters are always separate**, even for one company; market hours from `pandas_market_calendars` (NSE, BSE, Cboe), checked each morning against the broker; a `venues/` folder holds one file per venue | `.../execution/data-feed.md`; #129, 2026-09-28 | A closed market must not look like a dead feed |
| **Three ids on every envelope**: `decision_id`, `parent_event_id`, `actor`; the trace is a filter over the JSON log files; no event table, no OpenTelemetry, no log server | `.../execution/events-and-tracing.md`; #128, 2026-09-17 | Greg Young's correlation/causation pattern, spelled out; a second copy of the events is a second thing to keep in step |
| **Risk checks reject, never resize**, and are **client-wise**; strategy limits are in units with per-client overrides; check 2's ceiling is the client's **allocation cap**; margin is priced on the **resulting portfolio** and only alerts until measured; loss-limit breach blocks opening orders, allows closes, never auto-flattens | `.../execution/rms.md`; #128, 2026-09-17; #130, 2026-09-28 | A resized order is a value that stopped meaning what it says; margin is not additive per order |
| **Paper broker first, fills at the touch, fee and slippage 0 by default**; its manual door is a test hook with no route or command; testnet next; never real money in this phase | `.../execution/paper-broker.md`; #128, 2026-09-17 | Owner, 2026-09-16; real manual trades happen on Delta's own app |
| **Execution v1 = limit at touch, cancel and replace; buy legs first, wait, then sells** | `.../execution/oms.md`, 2026-09-16 | Margin; a market order on a thin 0dte wing |

How the work itself is run — tickets, tests, agents, branches — is [team-workflow](team-workflow.md).

## Research decisions — October 2026

Feature tests ([feature-testing](feature-testing.md)), volatility ([realised-volatility-estimators](realised-volatility-estimators.md)),
long gamma ([long-gamma-research](long-gamma-research.md)), Bilal's lab ([backtest-lab](backtest-lab.md)) and the
harness ([options-research-harness](options-research-harness.md)). Harness records are in
`options-research-harness/docs/design/decisions/` and its `grilling-log.md` (Q-numbers).

| Decision | Made where | Why |
|---|---|---|
| **Test a feature with Bilal's bucket test**: 30-minute windows, short-straddle log return, buckets, compare distributions | Bilal, 2026-10-07; `inbox/2026-10-07-feature-testing/meeting.md` | Shape and tails matter more than the mean; a passing feature becomes a filter on the live strategy |
| **Test on windows that do not overlap, reshuffle whole days, write each claim before opening fresh days** | Claude, 2026-10-08; `results.md` — waits for Bilal's word | Rolling windows overstate significance |
| **Read IV at the window's start; price the same contracts at its end** | Claude, 2026-10-08; `results.md` — pending | A forecast must be known at entry; a new at-the-money pair is not an earnable return |
| **Leave half days out until the strategy repo's loader handles them** | 2026-10-08; `results.md` | The loader counts every day to 16:00 |
| **Intraday RV = sum of squared 5-minute returns, scaled by a time-of-day profile** | Trading engine record 0075, PR #306, 2026-10-07 | Clock scaling reads 58% high after the first hour |
| **Positional RV defaults to Yang-Zhang over a window matched to the IV horizon** — researched, not built | 2026-10-07; `handoff-positional-iv-vs-rv.md` | The only estimator free of both gap and drift |
| **Backtests decide on candle i−1 and trade on candle i; returns on a fixed 150,000 per lot; no compounding** | Bilal, 2026-10-12; `handoff-2026-10-12.md` | No forward bias; comparable returns |
| **Long-gamma research: mechanism first, one target, three hedge rules, the tests corrected together** | 2026-10-07; `long-gamma-research/plan.md` | 127 days can only find hypotheses |
| **The harness lives in Lalit's private repo** `options-research-harness`; company code may be copied in; the senior moves it later | Harness 0006, 2026-10-17 | Lalit's call; Bilal not yet asked |
| **SPXW 0DTE only; NIFTY parked** | Harness Q13, 2026-10-17 | One market end to end first |
| **Code owns the steps; agents judge only inside a step** | Harness 0001, 2026-10-17 | No supervising model in the control path |
| **A frozen layer outside agent control** (data, labels, splits, cost model, pass bar) | Harness 0002, 2026-10-17 | Leakage passes DSR and PBO, so the guard must be structural |
| **`Backtest-Engine`'s maths is canonical** (405-minute clock) | Harness 0003, Q35, 2026-10-17 | One maths; IV on different clocks does not compare |
| **Forward holdout**: days after 2026-09-30, sealed, opened once, pass or fail | Harness 0004, Q41, 2026-10-17 | Free, unseen, grows about 21 days a month |
| **The harness changes only through pull requests a person merges** | Harness 0005, 2026-10-17 | Every change explainable and reversible |
| **Only the free held year; no paid data** | Harness Q37, 2026-10-17; Q47, 2026-10-19 | The 2024–25 year costs money; the senior may add data later |
| **Pass bar = the workflow page's**: one variant, chosen on the train half, read once on the test half | Harness Q34, 2026-10-17 | Stops picking the winner on the test half |
| **First gate builds steps 1–5 and 11**; DSR, PBO, CPCV, tails and robustness come later | Harness `evals.md`, 2026-10-17 | Thresholds need calibrated evals first |
| **Build order F1 ledger → F2 tools → F0 frozen layer → F3 meta-harness** | Harness Q46, PR #2, 2026-10-19 | The frozen layer guards against agents, and none exist before F3 |
| **Records are hash-chained JSON Lines in a git-ignored `records/`; the ledger is a rebuilt view; HTML pages** | Harness 0007, Q48–Q52, 2026-10-21 | An edit or deletion shows as a break in the chain |
| **The engine adapter waits for the senior's MCP server** | Harness Q40, 2026-10-17 | No interface exists yet |


## Superseded

| Was | Replaced by | When |
|---|---|---|
| `delta-exchange-payoff` as the engine this vault builds on | `Convex-Hedge-Trading-Engine`, the most recent design ([trading-engine](trading-engine.md)) | 2026-10-01 |
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
| Reconciliation that only freezes a mismatched contract | Adopt the broker's record and repair, bounded, then freeze (#129) | 2026-09-28 |
| One `oms` process for the engine; the sandbox as a second instance on venue `PAPER` | One OMS per client; paper clients (#130) | 2026-09-28 |
| Book 1 as a strategy's desired lots; pooling across the engine | Target × client units; pooling inside one client (#130) | 2026-09-28 |
| Engine-wise risk checks | Client-wise, strategy limits in units, an allocation cap (#130) | 2026-09-28 |
| Stream names `{type}:{VENUE}` for strategy output | By owner: feed by venue, strategy by market, OMS by client (#130) | 2026-09-28 |
| Seal clock pinned only by streams `behind` (R4) | Also held by streams still catching up (R4d, #119) | 2026-09-14 |
| Harness holdout: the 2024-07-01 to 2025-06-30 year, sealed (Q23) | The forward holdout, days after 2026-09-30 (Q41, decision 0004); the old year costs money | 2026-10-17 |
| Harness build order F0 to F8, frozen layer first (Q39) | F1 ledger → F2 tools → F0 → F3 (Q46, PR #2) | 2026-10-19 |

## Related

[trading-engine-decisions](trading-engine-decisions.md) · [feed-engine](feed-engine.md) · [bar-store](bar-store.md) · [deployment-and-cost](deployment-and-cost.md) ·
[product-direction](product-direction.md) · [team-workflow](team-workflow.md)
