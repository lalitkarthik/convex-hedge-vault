> As of Convex-Hedge-Trading-Engine@06e547fa, 2026-10-23

# Trading engine — the system we build on

**`Convex-Hedge-Trading-Engine`** at `D:\Convex Hedge\Convex-Hedge-Trading-Engine`, written by
Bilal Sagar Razak. GitHub: `Convex-Hedge-Private-Limited/`, moved from `bilal-sagar-razak/` on
2026-10-10 (decision 0093); old issue links keep the first address. **From 2026-10-01 it is the
engine all our work targets and the most recent design.** It reworks what `delta-exchange-payoff`
designed and has built far more: [engine-lineage](engine-lineage.md).

It is Convex Hedge's trading engine. It runs several strategies at once, watches live market data,
works out forwards, volatility and Greeks, decides what to trade, and will send orders to brokers.
It runs in two modes. **Live** trading uses real money. The **sandbox** paper-trades the same live
data with a simulated broker; the platform's newer word for it is *Paper Trading*. **Today only the
sandbox exists: no order reaches any market.** The order path is a later build from scratch inside
this engine (decision 0087).

## From one engine to a platform

Since 2026-10-10 the engine is the base of a platform of **three products on two sides**, in-house
and clients (decision 0086). `Trading-Engine/Architecture/Platform architecture.md` draws it.

| Product | What a person gets | In-house | Clients |
|---|---|---|---|
| Research | Strategies as **node graphs**, backtests, the AI builder **Echo** | In use, internal users only | Later |
| Market Watch | Live option chains, volatility, Greeks, the analytics pages | In use | The **pilot**, from 2026-10-15 |
| Live trading | Strategies trading real money through the person's broker | Later | Last |

**Research** lives in a second repository, `Convex-Hedge-Research-Engine`, which depends on the
engine and is never imported by it (decision 0109). It holds the Strategy SDK and the backtest host.
Its node graphs run in the India sandbox through a *paper adapter*, and its Research pages plug into
the company dashboard. The engine image pins one Research Engine commit (`pins/python.txt`).

**The Market Watch pilot** gives invited clients the market pages, free, for NIFTY and SENSEX. It
was first one engine instance per client (0098). Since 2026-10-11 all clients share one market fed
by the company's Upstox token (0104), and since 2026-10-13 one multi-user dashboard serves every
person as a *user session* (0122, 0126). A router signs clients in with Amazon Cognito.

The order of work is the pilot, then the move to three AWS accounts, then **Track 1, tenancy**: one
engine serving many user sessions, each fed by the person's own broker login (0090, 0095, 0097).
The Research track runs beside Track 1 (0108). Decisions 0086 onward are mapped in
[trading-engine-decisions-platform](trading-engine-decisions-platform.md).

## Not the terminal

The engine's docs call the program that was at `app.convexhedge.ai` "the Backtest engine", and its dashboard
copies that program's look. This vault calls it the terminal ([platform-map](platform-map.md),
[backtest-engine](backtest-engine.md)). The engine's docs now also call the frozen old backtest
engine the **Oracle**: the Research host must match it on its twenty strategies before it is
retired. **The address moved, so there is no collision.** Decision 0099 gives `app.convexhedge.ai` to
the pilot's router, and on 2026-10-11 the terminal left it for `research.convexhedge.ai` (external
beta users) and `lab.convexhedge.ai` (in-house). Source: `Backtest-Engine` commit `fa06b175` and its
glossary page `Convex-Hedge/Glossary/Live environment.md`; see [backtest-lab](backtest-lab.md).

## Markets and feeds

| # | Market | Source | Built |
|---|---|---|---|
| 1 | SPXW (weekly S&P 500 options) | Databento, live or downloaded files | Yes |
| 2 | NIFTY | Fyers, Upstox or Zerodha; the **selected broker** picks one in seconds | Yes |
| 3 | SENSEX | The same three brokers, in the same process as NIFTY | Yes |
| 4 | Bitcoin options | not chosen | No date. This is where `delta-exchange-payoff` fits |
| 5 | MCX options | not chosen | No date |

Fyers and Zerodha need a person's login each morning; Upstox uses a one-year read-only token
(0045). Zerodha joined the shared India instance and the cloud on 2026-10-08 (0076), but has never
been connected to Zerodha itself: no key has been bought. For clients the broker logins arrive in
the order Zerodha, Upstox, Fyers, then IIFL and Dhan (0090, 0096). Detail:
[engine-market-data](engine-market-data.md).

## What runs — one engine instance

An **engine instance** is one Redis and one container per part, started by Docker Compose from
`compose.yaml` and one TOML settings file in `config/` (`spxw-sandbox`, `india-sandbox`, one per
Indian broker, replays). The cloud adds `compose.cloud.yaml`. Five
**profiles** pick the feed: `live-us-databento`, `live-india-fyers`, `live-india-upstox`,
`live-india-zerodha` and `replay`. In the cloud the India profile runs all three Indian adapters.

| Part | Does | Code (`src/convex_trading_engine/`) |
|---|---|---|
| `redis` | The bus. Port bound to localhost; no persistence on a laptop, a snapshot across the nightly stop in the cloud (0052) | `bus/` |
| `datafeed`, `datafeed-fyers`, `-upstox`, `-zerodha`, `replay` | Feed adapters: raw quotes, trades, definitions, feed status, statistics | `datafeed/adapters/` |
| `chain` | Chain engine: the ATM forward, IV, Greeks, skew, GEX, realised volatility | `chain/` |
| `recorder` | Every message to one `.jsonl.zst` file per run. Laptops only | `recording/` |
| `console` | Text view of the top of book. Laptops only | `console/` |
| `dashboard` | Web pages on `127.0.0.1:8080`, under `/spxw` or `/india`; no login on a laptop, Google sign-in in the cloud | `dashboard/`, `trading_pages/`, `frontend/` |
| `strategy-<name>` | One container per strategy instance | `strategies/` |
| `sim-broker` | Fills each instance's model account, keeps the trading journal | `sim_broker/`, `journal/` |
| `alerter` | One Discord card per fill | `alerter/` |
| `watchdog` | Five-minute checks, problems to Discord. India cloud machine and pilot only | `watchdog/` |

Lasting data sits in SQLite files on the instance's `history` volume: the history store, the
trading journal and the client portfolios. Every part proves it is alive with a **heartbeat file**
(0074) and can serve a metrics page for Prometheus. The pilot adds a market host, a router and a
shared market (`markets/`, `pilot/`). Access roles live in `roles/`, the AWS helpers in `cloud/`,
and the pilot's PostHog events in `analytics/`.

Strategy instances today: on India, the delta-hedged straddle on NIFTY and on SENSEX, and two NIFTY
node graphs from the Research Engine (a strangle and a straddle). On SPXW, the low-volatility
straddle and the inflow strangle at 10:00 and 11:30. The halves are
[engine-strategies](engine-strategies.md) and [engine-dashboard](engine-dashboard.md).

## Where it runs

Laptop and cloud run the same engine; only settings change (0002). The cloud is AWS in Mumbai, in
three accounts: management, internal and clients (0092). The India and SPXW machines sit in the
**internal account** since 2026-10-11. Each is one EC2 machine running the Compose stack on a
market-hours schedule (0051). Since 2026-10-18 all four machines are ARM64 Graviton (0146–0149).
The team opens `trade.convexhedge.ai/india` and `/spxw` with Google sign-in. A **role** per market,
viewer to admin, decides what each person sees and does (0151–0155). The pilot machine sits in the
**clients account**. An operations machine runs Grafana and alerts. Guide: `Running on AWS.md`.

## Status, 2026-10-23

**Merged, 2026-10-01 → 10-08:** the Upstox and Zerodha feeds; the analytics tabs (#150); AWS India
hosting; dashboard sign-in and the Broker page; client portfolios and daily history; the structure
editor; the SENSEX straddle; implied against realised volatility; the ATM forward.

**Merged, 2026-10-10 → 10-18:** the platform plan; the Market Watch pilot and its shared market;
the AWS account move; the dashboard and front-end split into products; user sessions in one
engine; engine seams for the backtest host; the regression forward retired (2026-10-15, 0132); the
chain picker and structure presets; dashboard plug-ins; Research Engine graphs in the India
sandbox; Graviton machines; market roles; second-order Greeks.

**Since 2026-10-19** main takes mostly Research Engine pins: the Research pages, the Strategy
builder, Echo and the strategy canvas, internal users only. The "nifty" cost preset charges no
slippage since 2026-10-23. Releases are tagged `engine-<date>`, latest `engine-2026.10.23` (0133).

**Open problems:** Fyers refuses the India subscription, "symbol count exceeds limit 100" (#635);
the portfolio backup fails on the India machine (#636); a straddle process uses 40% of a core (#279).
**Next, not designed:** the execution engine (order and risk management), real orders, Track 1's
control plane and dashboard shell, the client broker logins, the Bitcoin and MCX markets.

**History, 2026-10-01:** twelve features had merged in five days (2026-09-26 → 09-30). Feature
#150 was in flight with decisions 0045–0050 on its branch; it merged 2026-10-03. The live checks
then listed as open were closed: #86 as *wontfix* (2026-09-30, the strangle gave way to the
straddle), #144 on 2026-10-03, #119 on 2026-10-05.

## Where the answers live (the repo's own docs are canon)

| Question | Open |
|---|---|
| Any term | `CONTEXT.md` (index, 1,075 terms) → `Trading-Engine/Glossary/<Term>.md` |
| The engine's shape, and what is open | `Trading-Engine/Architecture/Overall architecture.md` |
| The products, accounts and tracks | `Trading-Engine/Architecture/Platform architecture.md`, `Project overview.md` |
| One part's design | `Trading-Engine/Architecture/<Part> design.md` (adds *Live trading pages design*) |
| Why something is so | `Trading-Engine/Decisions/0001`–`0156`; mapped in [trading-engine-decisions](trading-engine-decisions.md) and [trading-engine-decisions-platform](trading-engine-decisions-platform.md) |
| What it does today | `Trading-Engine/Guide/What the engine does.md`, then one page per part |
| What changed, when | `Trading-Engine/Guide/Changelog.md` (98 rows) |
| One feature's scope | `Trading-Engine/Specs/`, `Research/`, `Tickets/` |
| How to run it | `README.md`; cloud: `Guide/Running on AWS.md`, `Deploying to the cloud.md` |
| How work is built | `CLAUDE.md` and `Trading-Engine/Workflow/How a feature gets built.md` |
| The layers and products in the code | `Guide/The layer rule.md`, `src/convex_trading_engine/layers.toml` |
| Code structure | the local graph, [code-graphs](code-graphs.md) |

The docs are an Obsidian vault for a reader who neither codes nor trades; the Guide holds merged behaviour only.

## How work is built there

Grill, research, grill again, spec issue, ticket sub-issues in **waves**, an implementation plan.
An unattended Opus orchestrator runs at most three Opus implementers in worktrees and opens one PR
per feature; the user merges. Sessions run in Herdr and hand off at 60% context; since October they
address the user in Simplified Technical English. We run it without Herdr: [team-workflow](team-workflow.md).

## Drift found

**Found 2026-10-01, re-checked 2026-10-23:**

- `README.md` *Status* still says "Design stage". **Still wrong.** `Project overview.md` is now right.
- Specs of merged features still read "implemented, awaiting merge". **Still so**, for 21 specs;
  some wait for a person's live check (PR #640 marks Market roles live).
- `Overall architecture.md` *What is decided* still stops at 0011, and *What is still open* still
  lists the AWS setup, which 0051 and 0092 decided.

**New on 2026-10-23** (decision-record drift is in the two decision maps):

- `What the engine does.md` says the engine runs on crypto options "today". No crypto adapter exists.
- `Guide/The Zerodha adapter.md` says in three places that Zerodha is not in the cloud. Its own later
  section, decision 0076 and `compose.cloud.yaml` say it is. Tickets #252 and #253, its live
  check, are closed as deferred, but the adapter has never met Zerodha.
- Glossary `Pilot.md` and `Market.md` keep their first meanings: one instance per client, and "a
  place, usually an exchange". Decisions 0104 and 0120 changed both.
- Glossary `Derived data engine.md` says "not built yet", while the chain engine has worked out GEX
  and skew since 2026-10-03 and realised volatility since 2026-10-07.

## Open questions for us

- Where Bitcoin options enter: a Delta Exchange feed adapter reusing `delta-exchange-payoff`'s
  websocket and Greeks work, or a fresh one. The engine has no date for it.
- The execution design: 0087 makes the order path a from-scratch build for many clients. Whether
  `delta-exchange-payoff/docs/design/execution/` informs it is not decided ([engine-lineage](engine-lineage.md)).
- Which database: the engine now keeps SQLite files per purpose and roles in DynamoDB. The overall
  database is still listed as open.

## Related

[engine-lineage](engine-lineage.md) · [trading-engine-decisions](trading-engine-decisions.md) ·
[trading-engine-decisions-platform](trading-engine-decisions-platform.md) · [engine-market-data](engine-market-data.md) ·
[engine-strategies](engine-strategies.md) · [engine-dashboard](engine-dashboard.md) · [code-graphs](code-graphs.md) ·
[glossary-trading-engine](glossary-trading-engine.md) · [GLOSSARY](../GLOSSARY.md)
