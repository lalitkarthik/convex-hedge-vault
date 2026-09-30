> As of Convex-Hedge-Trading-Engine@b47d8ee, 2026-10-01

# Trading engine — the system we build on

**`Convex-Hedge-Trading-Engine`** at `D:\Convex Hedge\Convex-Hedge-Trading-Engine`, GitHub
`bilal-sagar-razak/Convex-Hedge-Trading-Engine`, written by Bilal Sagar Razak. **From 2026-10-01 it
is the engine all our work targets and the most recent design.** It reworks what
`delta-exchange-payoff` designed, carries the same core ideas into more markets, and has
already built far more. [engine-lineage](engine-lineage.md) sets out what carried over and what changed.

It is Convex Hedge's trading engine. It runs several strategies at once, watches live market data,
decides what to trade, and will send orders to brokers. It runs in two modes. **Live** trading uses
real money. The **sandbox** paper-trades the same live data with a simulated broker. **Today only
the sandbox exists: no order reaches any market.**

**Not the terminal.** The engine's own docs call `app.convexhedge.ai` "the Backtest engine", and its
dashboard deliberately copies that program's look. This vault calls it the terminal
([platform-map](platform-map.md)).

## Markets, in build order

| # | Market | Source | Built |
|---|---|---|---|
| 1 | SPXW (weekly S&P 500 options) | Databento, live or downloaded files | Yes |
| 2 | NIFTY | Fyers broker feed, one morning login a day | Yes |
| 3 | SENSEX | Fyers, same process as NIFTY | Yes |
| 4 | Bitcoin options | not chosen | No. This is where `delta-exchange-payoff` fits |
| 5 | MCX options | not chosen | No |

## What runs — one engine instance

An **engine instance** is one Redis and one container per part, started by Docker Compose from
`compose.yaml` and one TOML settings file in `config/`. Two sandboxes exist: `spxw-sandbox` (US) and
`india-sandbox`. A **profile** picks the feed: `live-us-databento`, `live-india-fyers` or `replay`.

| Part | Does | Code (`src/convex_trading_engine/`) |
|---|---|---|
| `redis` | The bus. Persistence off, port bound to localhost | `bus/` |
| `datafeed`, `datafeed-fyers`, `replay` | Feed adapters: raw quotes, trades, definitions, feed status, statistics | `datafeed/adapters/` |
| `chain` | Chain engine: forward, IV, Greeks per expiry on every event | `chain/` |
| `recorder` | Every message to one `.jsonl.zst` file per run | `recording/` |
| `console` | Text view of the top of book | `console/` |
| `dashboard` | Web page on `127.0.0.1:8080`, no login | `dashboard/` + `frontend/` |
| `strategy-<name>` | One container per strategy instance | `strategies/` |
| `sim-broker` | Fills every instance's model account at the mid | `sim_broker/` |
| `alerter` | One Discord card per fill | `alerter/` |

Detail: the data half is [engine-market-data](engine-market-data.md). The strategy half is
[engine-strategies](engine-strategies.md). The screens are [engine-dashboard](engine-dashboard.md).

## Status, 2026-10-01

**Merged, 2026-09-26 → 09-30** (twelve features in five days; PR list on GitHub):
bus and data feed; open interest and daily statistics; Fyers feed; dashboard option chain; chain
engine (forwards, IV, Greeks); dashboard redesign; change markers; strategy portfolio; SPXW
strategies; Discord fill alerts; NIFTY delta-hedged straddle; strategy details pages.

**Merged but a person's live check is still open:** #86 (strategy portfolio, India), #119 (SPXW
strategies on a US day) and #144 (strategy details pages, both sandboxes).

**In flight:** feature #150, *Dashboard analytics tabs*, on `feature/dashboard-analytics-tabs`. It
adds four pages (structure chain, IV smile with skew, GEX by strike, spot with GEX levels). The chain
engine becomes the **derived data engine**, and the first lasting history arrives as a SQLite file.
Tickets are #155–#162. Decisions 0045–0050 exist only on that branch.

**Next, not designed:** the execution engine (order management and risk management), the database,
real orders, warning alerts, AWS hosting, and a login for the dashboard.

## Where the answers live (the repo's own docs are canon)

| Question | Open |
|---|---|
| Any term | `CONTEXT.md` (index, 463 terms) → `Trading-Engine/Glossary/<Term>.md` |
| The shape, and what is open | `Trading-Engine/Architecture/Overall architecture.md` |
| One part's design | `Trading-Engine/Architecture/<Part> design.md` (bus, data feed, chain, strategy runtime, simulated broker, alerter, dashboard) |
| Why something is so | `Trading-Engine/Decisions/0001`–`0044`; mapped in [trading-engine-decisions](trading-engine-decisions.md) |
| What it does today | `Trading-Engine/Guide/` — `What the engine does.md`, then one page per part and strategy |
| What changed, when | `Trading-Engine/Guide/Changelog.md` |
| One feature's scope | `Trading-Engine/Specs/`, `Research/`, `Tickets/` (one page each per feature) |
| How to run it | `README.md`: Compose, Fyers morning login, replay, the acceptance day |
| How work is built | `CLAUDE.md` and `Trading-Engine/Workflow/How a feature gets built.md` |
| Code structure | the local graph, [code-graphs](code-graphs.md) |

The repo's docs are an Obsidian vault written for a reader who neither codes nor trades. Every
term has its own page, and the Guide describes only merged behaviour.

## How work is built there

The flow is grill, research, grill again, spec issue, ticket sub-issues in **waves**, then an
implementation plan. An unattended Opus orchestrator runs at most three Opus implementers, each in
its own worktree, merges each ticket, code-reviews it, and opens one PR per feature. The user merges.
Every session runs inside Herdr and hands off at 60% context (`scripts/claude/context-guard.py`).
On this machine Herdr, `python3` and `jq` break that recipe as written, so we run it without Herdr:
[team-workflow](team-workflow.md).

## Drift found on 2026-10-01

- `README.md` *Status* and `Architecture/Project overview.md` *Where things stand* still say
  "design stage, no engine code". The Guide and the Changelog show twelve merged features.
- Specs for five merged features still read "implemented, awaiting merge". Those PRs are merged; the
  status seems to wait for the live check.
- `Overall architecture.md` *What is decided* stops at record 0011, while the records run to 0044.

## Open questions for us

- Where Bitcoin options enter: a Delta Exchange feed adapter reusing `delta-exchange-payoff`'s
  websocket and Greeks work, or a fresh one.
- Whether the execution design in `delta-exchange-payoff/docs/design/execution/` (books, pooled
  diffing, per-client OMS) is the starting point for this engine's execution engine. See
  [engine-lineage](engine-lineage.md).
- Which database: the analytics feature brings SQLite for derived history (0047, on its branch). The
  overall database is still open.

## Related

[engine-lineage](engine-lineage.md) · [trading-engine-decisions](trading-engine-decisions.md) ·
[engine-market-data](engine-market-data.md) · [engine-strategies](engine-strategies.md) ·
[engine-dashboard](engine-dashboard.md) · [code-graphs](code-graphs.md) · [GLOSSARY](../GLOSSARY.md)
