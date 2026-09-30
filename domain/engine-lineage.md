> As of Convex-Hedge-Trading-Engine@b47d8ee and delta-exchange-payoff@fce8d39, 2026-10-01

# Engine lineage — from `delta-exchange-payoff` to the trading engine

**Since 2026-10-01 the [trading-engine](trading-engine.md) is the current design, and the target of
all new work.** `delta-exchange-payoff` ([feed-engine](feed-engine.md)) came first. It was one
crypto venue, bars in Parquet, and an execution design that was never built. The trading engine
keeps its core ideas, widens them to several markets, and has built the strategy half in the
sandbox. This note keeps what each engine chose side by side, so no decision is lost in the move.

## What carried over

| Idea | `delta-exchange-payoff` | Trading engine |
|---|---|---|
| Separate programs on a Redis Streams bus | Seven services, epic #57 | Every part a container: 0003, 0004, 0005 |
| Change-safety: a new strategy never touches the running ones | The senior's stated reason | One process per strategy instance: 0031 |
| **A strategy states a position, never an order** | Book 1, the desired position | The signal is a **target position**: 0030 |
| Our own forward, IV and Greeks; the venue's are reference only | `CLAUDE.md` rule, `test_no_delta_inputs.py` | The chain engine computes them; strategies take derived values only from it: 0034 |
| Newest-only reading for market data, lossless reading for the one that must not lose | The chain cache drops oldest; `store` reads losslessly | The newest-per-instrument rule; in-order reading with acknowledgements for signals |
| Never fabricate a value | "Never forward-fill; `null` is not `0`" | A missing price shows a dash; stale data means the strategy is not asked |
| Secrets in the environment only | `.env` | 0009 |
| AWS | ECS on EC2, `ap-south-1` (0005, 0008 there) | AWS (0001); the setup is open |

## What changed

| Topic | `delta-exchange-payoff` | Trading engine |
|---|---|---|
| Markets | BTC options on Delta Exchange India | SPXW, NIFTY, SENSEX built; **Bitcoin options fourth, not started** |
| Permanent record | One-minute bars in Parquet; a store with seal, flush and watermarks ([bar-store](bar-store.md)) | **Recordings**, an exact copy of the bus as `.jsonl.zst`. No bars. SQLite history coming for derived figures (0047, on a branch) |
| Bus memory | 30 min by age, 2 GiB `maxmemory` | 10 min per category, plus **latest values** kept 7 days (0020) |
| Stream naming | `{event_type}:{VENUE}[:{UNDERLYING}]` | Category prefixes, hidden inside the bus client |
| Quote rate | Every websocket message | **Sampled once a second** by default (0011) |
| Decision timing | Not built | **Wall-clock beats**, configurable from 1 s to 60 min (0029) |
| Paper trading | Paper clients, each with its own paper broker inside its OMS; fills at the touch | A **simulated broker** part; fills at the **mid**, with an optional **fill delay** (0032, 0040) |
| Orders | One OMS per client; pooled `Book 2 − Book 4 − working` within a client; limit at touch, cancel and replace | **No orders yet.** The broker brings each model account straight to its target |
| Tracing | `decision_id`, `parent_event_id`, `actor` over JSON log files | A bus message id in every log line; **lineage** on every derived message (0024) |
| Durable state | Postgres through the bus, one persistence service writing it; strategy checkpoints as JSONB | Redis latest values and record stores; **the database is undecided** |
| Health | `/health` per service; #103 showed it green while nothing worked ([service-health](service-health.md)) | Feed status on the bus, a statistics line every 10 s, data-freshness badges on the dashboard |
| Alerts | `discord-alerts` service | The **alerter**: one fill card per signal (0042) |
| Workflow | GitHub tickets, Claude agents in worktrees | A spec issue and ticket waves, an orchestrator with at most three implementers, one PR per feature |

## What `delta-exchange-payoff` designed that the trading engine has not yet

The execution half. It is in `delta-exchange-payoff/docs/design/execution/`, eleven pages after
#129 and #130, and is summarised in [design-decisions](design-decisions.md):

- the six **books** and **pooled** diffing, with reallocations;
- `client_order_id` as the engine's mark, with discretionary fills and reconciliation every 10 s;
- **risk checks that reject, never resize**; margin priced on the resulting portfolio;
- **one OMS per client**, subscriptions in units, per-client risk (#130);
- execution v1: limit at the touch, cancel and replace, buy legs first.

The trading engine's next features are exactly this: an order management system, a risk management
system and real orders. Whether that work starts from these pages is **not decided**. The execution
engine has no design page there yet.

## The meeting asks, against the trading engine

These asks are raw record in [meetings/](../meetings/) and not yet promoted.

| Asked | Where it stands in the trading engine |
|---|---|
| Configurable decision cadence (25 Sep) | **Answered**: `cadence_seconds`, 1 s to 60 min (0029) |
| Signal cards (20 Sep) | **Partly**: one fill card per signal, showing the signal price against the fill price (0041, 0042) |
| Per-instrument trading hours (20 Sep) | **Partly**: calendar files per exchange and year (0023), and sessions per market in settings |
| Backtest-to-live gap on SPX (25 Sep) | **Measured, not closed**: fill delay, slippage and how far past its trigger a stop filled are all recorded |
| Per-client OMS, subscriptions, units (25 Sep) | **Not yet**: sizes are base lots per strategy instance; there are no client accounts |
| One OMS routing to several brokers (25 Sep) | **Not yet**: which broker serves which market is open |
| Persist working orders; reconciliation that re-fires (20 Sep) | **Not yet**: there are no orders |

## Related

[trading-engine](trading-engine.md) · [trading-engine-decisions](trading-engine-decisions.md) ·
[design-decisions](design-decisions.md) · [feed-engine](feed-engine.md) ·
[product-direction](product-direction.md)
