> As of Convex-Hedge-Trading-Engine@06e547fa and delta-exchange-payoff@fce8d39, 2026-10-23

# Engine lineage — from `delta-exchange-payoff` to the trading engine

**Since 2026-10-01 the [trading-engine](trading-engine.md) is the current design, and the target of
all new work.** `delta-exchange-payoff` ([feed-engine](feed-engine.md)) came first. It was one
crypto venue, bars in Parquet, and an execution design that was never built. The trading engine
keeps its core ideas, widens them to several markets, and has built the strategy half in the
sandbox. Since 2026-10-10 it is also the base of a platform with clients. This note keeps what each
engine chose side by side, so no decision is lost in the move. `delta-exchange-payoff` has not
moved since `fce8d39`; every change below is on the trading engine's side.

## What carried over

| Idea | `delta-exchange-payoff` | Trading engine |
|---|---|---|
| Separate programs on a Redis Streams bus | Seven services, epic #57 | Every part a container: 0003, 0004, 0005 |
| Change-safety: a new strategy never touches the running ones | The senior's stated reason | One process per strategy instance: 0031 |
| **A strategy states a position, never an order** | Book 1, the desired position | The signal is a **target position**: 0030. Node graphs keep an *intended book* and return it as the target: 0111 |
| Our own forward, IV and Greeks; the venue's are reference only | `CLAUDE.md` rule, `test_no_delta_inputs.py` | The chain engine computes them; strategies take derived values only from it: 0034. Since 2026-10-15 one forward, the ATM forward: 0132 |
| Newest-only reading for market data, lossless reading for the one that must not lose | The chain cache drops oldest; `store` reads losslessly | The newest-per-instrument rule; in-order reading with acknowledgements for signals |
| Never fabricate a value | "Never forward-fill; `null` is not `0`" | A missing price shows a dash; stale data means the strategy is not asked; a figure with too little history is marked *provisional* or *incomplete* |
| Secrets in the environment only | `.env` | 0009; in the cloud, SSM Parameter Store. A daily broker token is the one exception: it goes through the record store (0057, 0067) |
| AWS in Mumbai | ECS on EC2, `ap-south-1` (0005, 0008 there) | EC2 in `ap-south-1` running Docker Compose, one machine per market, on a market-hours schedule (0051); Graviton since 2026-10-18 (0146) |
| Payoff arithmetic | `engine/src/deltapayoff/payoff.py`, `docs/payoff-contract.md` | Cited as a source in the engine's research for the structure editor (`Trading-Engine/Research/Structure editor and payoff chart.md`) |

## What changed

| Topic | `delta-exchange-payoff` | Trading engine |
|---|---|---|
| Markets | BTC options on Delta Exchange India | SPXW, NIFTY, SENSEX built; **Bitcoin options and MCX on the list, no date** |
| Market data sources | One venue websocket | Databento for SPXW; three Indian brokers, Fyers, Upstox and Zerodha, with a *selected broker* switch (0056, 0070, 0076) |
| Permanent record | One-minute bars in Parquet; a store with seal, flush and watermarks ([bar-store](bar-store.md)) | **Recordings**, an exact copy of the bus as `.jsonl.zst`, on laptops only (0118). Derived history in SQLite: candles, smiles, OI, volatility readings (0047, 0060, 0077, 0080). No bars. The Research Engine's backtests read the Oracle's Parquet bars from S3 (0115) |
| Bus memory | 30 min by age, 2 GiB `maxmemory` | 10 min per category, plus **latest values** kept 7 days (0020); a Redis snapshot across the nightly stop in the cloud (0052) |
| Stream naming | `{event_type}:{VENUE}[:{UNDERLYING}]` | Category prefixes, hidden inside the bus client; a **market prefix** in front for each broker account on a shared bus (0120) |
| Quote rate | Every websocket message | **Sampled once a second** by default (0011) |
| Decision timing | Not built | **Wall-clock beats**, configurable from 1 s to 60 min (0029). A backtest beat sees only earlier data (0116) |
| Paper trading | Paper clients, each with its own paper broker inside its OMS; fills at the touch | A **simulated broker** part; fills at the **mid**, with an optional **fill delay** (0032, 0040). Since 2026-10-13 an optional cost model and fill-price policy per instance (0119) |
| Orders | One OMS per client; pooled `Book 2 − Book 4 − working` within a client; limit at touch, cancel and replace | **No orders yet.** The broker brings each model account straight to its target. The order path is a later from-scratch build (0087) |
| Tracing | `decision_id`, `parent_event_id`, `actor` over JSON log files | A bus message id in every log line; **lineage** on every derived message (0024) |
| Durable state | Postgres through the bus, one persistence service writing it; strategy checkpoints as JSONB | **SQLite files per purpose**, each with one writer, on the instance's volume: history store (0047), trading journal (0064), client portfolios (0062), saved view (0139), user settings (0124). Roles in DynamoDB (0152). The overall database is still listed as open |
| Health | `/health` per service; #103 showed it green while nothing worked ([service-health](service-health.md)) | A **heartbeat file** touched from each part's own work loop, so a stuck loop fails the check (0074); a five-minute **watchdog** (India cloud, pilot); metrics pages for Prometheus and Grafana (0102); feed status on the bus and data-freshness badges |
| Alerts | `discord-alerts` service | The **alerter**: one fill card per signal (0042). Problems: the watchdog, and Grafana alerts to an operations channel |
| Clients | Paper clients, per-client OMS, subscriptions in units | **Client portfolios**: a client account will follow one portfolio at its own multiple (0061). Market Watch clients as *user sessions*, one per person (0095, 0122) |
| Access | Not designed | Google sign-in and a **role per market**, viewer to admin (0151–0155); Cognito for pilot clients (0094, 0099) |
| Repository | Personal repository | The company's GitHub organisation (0093); Research in a second repository, `Convex-Hedge-Research-Engine` (0109) |
| Workflow | GitHub tickets, Claude agents in worktrees | A spec issue and ticket waves, an orchestrator with at most three implementers, one PR per feature |

**History.** On 2026-10-01 this table said "the database is undecided", "SQLite history coming
(0047, on a branch)" and "AWS (0001); the setup is open". The SQLite stores merged from 2026-10-03,
and the AWS setup was decided by 0051 (2026-10-01) and 0092 (2026-10-10).

## What `delta-exchange-payoff` designed that the trading engine has not yet

The execution half. It is in `delta-exchange-payoff/docs/design/execution/`, eleven pages after
#129 and #130, and is summarised in [design-decisions](design-decisions.md):

- the six **books** and **pooled** diffing, with reallocations;
- `client_order_id` as the engine's mark, with discretionary fills and reconciliation every 10 s;
- **risk checks that reject, never resize**; margin priced on the resulting portfolio;
- **one OMS per client**, subscriptions in units, per-client risk (#130);
- execution v1: limit at the touch, cancel and replace, buy legs first.

The trading engine's later features are exactly this: an order management system, a risk
management system and real orders. **Since 2026-10-10 decision 0087 says the order path is built
from scratch inside the engine, designed for many clients from the start, with the brokers' and the
exchange's rules.** The record sets aside a separate *Execution Engine* repository, which it
describes as an older order path for one account on one machine. It does not name
`delta-exchange-payoff`, whose execution design was never built and was per-client. No engine page
cites our execution pages. Whether they inform the new order path is still **not decided**. The
execution engine has no design page yet.

Two neighbours of execution are now decided on the engine side: margin and costs belong to the
host, by formula in a backtest and from the broker's API in paper trading (0114), and fees are
booked beside gross profit and loss (0119).

## The meeting asks, against the trading engine

These asks are raw record in [meetings/](../meetings/) and not yet promoted.

| Asked | Where it stands in the trading engine, 2026-10-23 |
|---|---|
| Configurable decision cadence (25 Sep) | **Answered**: `cadence_seconds`, 1 s to 60 min (0029) |
| Signal cards (20 Sep) | **Partly**: one fill card per signal, showing the signal price against the fill price (0041, 0042) |
| Per-instrument trading hours (20 Sep) | **Partly**: calendar files per exchange and year (0023), and sessions per market in settings |
| Backtest-to-live gap on SPX (25 Sep) | **Measured, not closed**: fill delay, slippage and stop overshoot are recorded. The Research track's third feature, "Two hosts", plans a *parity report* between backtest and paper (0108, 0114) |
| Per-client OMS, subscriptions, units (25 Sep) | **Partly designed**: a client account will follow one client portfolio at its own multiple (0061). No client account trades yet; sizes are base lots per instance |
| One OMS routing to several brokers (25 Sep) | **Not yet**: brokers serve data only. Client brokers are ordered Zerodha, Upstox, Fyers, IIFL, Dhan (0090); orders come with Live trading |
| Persist working orders; reconciliation that re-fires (20 Sep) | **Not yet**: there are no orders |

On 2026-10-01 the per-client row read "Not yet: there are no client accounts". Client portfolios
(0061, 2026-10-05) moved it to *partly designed*.

## Related

[trading-engine](trading-engine.md) · [trading-engine-decisions](trading-engine-decisions.md) ·
[trading-engine-decisions-platform](trading-engine-decisions-platform.md) ·
[design-decisions](design-decisions.md) · [feed-engine](feed-engine.md) ·
[product-direction](product-direction.md)
