# Convex Hedge — front door

Understand Convex Hedge's options-trading platform and its data well enough to build on it — and
build the **trading engine**, `Convex-Hedge-Trading-Engine`, which since 2026-10-01 is the engine all
work targets and the most recent design. **What this vault is for, and how to use
it: [MISSION.md](MISSION.md).**

## Start here

1. [trading-engine](domain/trading-engine.md) — the engine we build on: what runs, what is built, what is next, where its docs answer
2. [engine-lineage](domain/engine-lineage.md) — what carried over from `delta-exchange-payoff`, what changed, what the meetings asked
3. [design-decisions](domain/design-decisions.md) and [trading-engine-decisions](domain/trading-engine-decisions.md) — every choice, why, and what replaced what
4. [platform-map](domain/platform-map.md) — Convex Hedge's terminal, surface by surface
5. [product-direction](domain/product-direction.md) — what the company asked for, traced to the work

## Domains — the terminal (Convex Hedge's backtesting platform)

<!-- one line per domain note: link — what it covers — status (solid / partial / stub) -->

- [platform-map](domain/platform-map.md) — the six surfaces of app.convexhedge.ai, what v0.1 has not built, and where its vocabulary collides with `payoff-project` — **solid**
- [option-chain](domain/option-chain.md) — the chain screen: snapshot model, forward per expiry, the eleven columns, DTE and the Greeks, data traps — **solid**
- [structure-chain](domain/structure-chain.md) — the straddle/strangle grid and ratio spreads: how a cell is built, the sign convention — **solid**
- [volatility](domain/volatility.md) — smile and skew, IV against realised vol, the six estimators, the Feb 2026 regime change — **solid**
- [open-interest](domain/open-interest.md) — OI by strike, PCR, OI change, the GEX gamma flip and its walls — **solid**
- [strategies](domain/strategies.md) — what a strategy is made of, hedging, and the parameters that silently do nothing — **solid**
- [backtest-engine](domain/backtest-engine.md) — runs, the four report tabs, cost models, which numbers not to trust — **solid**
- [portfolio](domain/portfolio.md) — combining runs into a book, and why there is no per-unit track — **solid**

## Domains — the trading engine (`Convex-Hedge-Trading-Engine`, current)

- [trading-engine](domain/trading-engine.md) — the front door: markets, the parts of one engine instance, status, where the repo's docs answer each question, drift found — **solid, 2026-10-01**
- [engine-market-data](domain/engine-market-data.md) — the bus, feed adapters (Databento, Fyers, replay), the chain engine, recording and replay — **solid, 2026-10-01**
- [engine-strategies](domain/engine-strategies.md) — beats and cards, the four strategies, the simulated broker, Discord fill cards — **solid, 2026-10-01**
- [engine-dashboard](domain/engine-dashboard.md) — the deployed dashboard at `india.` and `spxw.convexhedge.ai`: seven pages, what each keeps over time, what reads wrongly at first sight — **solid, 2026-10-05**
- [strategy-research](domain/strategy-research.md) — Meghav's `convex-hedge-strategy`: where its pages answer, and the SPXW yardstick for live watching — **solid, 2026-10-05**
- [trading-engine-decisions](domain/trading-engine-decisions.md) — records 0001–0044 grouped by phase, 0045–0050 on a branch, what is still undecided — **solid, 2026-10-01**
- [engine-lineage](domain/engine-lineage.md) — `delta-exchange-payoff` against the trading engine, and the 20/25 September asks against both — **solid, 2026-10-01**
- **Execution engine (OMS, RMS, real orders)** — the trading engine's next features; no design page there yet. The prior design is `delta-exchange-payoff`'s, below — **not designed**

## Earlier engine — `delta-exchange-payoff` (history and prior design)

Superseded as the engine we build on, 2026-10-01. Kept because its execution design is the most
worked-out answer to what the trading engine builds next.


- [feed-engine](domain/feed-engine.md) — seven services on a Redis Streams bus, how data moves, the promises and non-promises, status — **solid, 2026-09-25**
- [bar-store](domain/bar-store.md) — the four tables, seal then flush, crash and replay, the pause loss (#121), what the recordings show — **solid, 2026-09-25**
- [service-health](domain/service-health.md) — what each `/health` can and cannot detect, the #103 incident, component-named logs (#126), improvement candidates — **solid, 2026-09-25**
- [deployment-and-cost](domain/deployment-and-cost.md) — one `c7g.xlarge` on ECS, CPU and RAM, T1/T2/T4, the split threshold and the hop — **solid, nothing built**
- **Execution half — strategy worker, OMS, RMS, paper broker** — designed 2026-09-16, revised by #128 on 09-17, not built. Changes asked on 20 and 25 September are not yet in it. Canon is
  `delta-exchange-payoff/docs/design/execution/00-overview.md`; the decisions are rows in [design-decisions](domain/design-decisions.md);
  the books picture is [assets/oms-books.png](assets/oms-books.png) — **decided, nothing built**

## Across both

- [design-decisions](domain/design-decisions.md) — our own choices, `delta-exchange-payoff`'s ten records and execution-design rows, and the superseded table — **solid, 2026-10-01**
- [product-direction](domain/product-direction.md) — the senior's asks from the August meetings, each traced or marked *not traced* — **partial**
- [team-workflow](domain/team-workflow.md) — idea to merged work: specs, tickets, tests, branches, agents — **solid**

## Learning records — what was learned, in order

- [message-buses](learning-records/message-buses.md) — why a bus exists, the three brokers measured, Redis Streams' one trap — **2026-09-07**, partly superseded by the split
- [tests-that-prove-nothing](learning-records/tests-that-prove-nothing.md) — green tests that verified nothing, and the checks that find them — **2026-09-12**
- [silent-success](learning-records/silent-success.md) — a value that stopped meaning what it says: eight instances, five questions — **2026-09-12**

## Workspace

- [MISSION.md](MISSION.md) — why this vault exists, what success looks like, how to use it
- [GLOSSARY.md](GLOSSARY.md) — canonical terms: the terminal's, and where the three systems collide; engine terms split into [glossary-trading-engine](domain/glossary-trading-engine.md) and [glossary-feed-engine](domain/glossary-feed-engine.md)
- [RESOURCES.md](RESOURCES.md) — trusted sources and when to reach for each
- [NOTES.md](NOTES.md) — threads no ticket or note tracks yet
- [session-log.md](session-log.md) — the current period's decisions and open questions
- [AGENTS.md](AGENTS.md) — the rules Codex followed as tutor (what it may write, how it teaches); Claude tutors since 2026-09-30

## Study — Claude tutors and builds (since 2026-09-30)

- [teach/market-observation](teach/market-observation/PLAN.md) — one sitting per market per trading day on the live dashboard, India and the US; the running table is [normal-ranges](teach/market-observation/normal-ranges.md). **Starts 2026-10-05 (US), 2026-10-06 (India)**
- [teach/execution-design](teach/execution-design/PLAN.md) — Convex Hedge's execution design and the feed engine under it, from a trader's seat. Sixteen sessions; **none run yet**. Built on `delta-exchange-payoff`, so it predates the trading engine — revisit before running it
- General options theory — Greeks, structures, ratios, gamma, skew — lives outside this vault in
  `second-brain/learning/option-structures/`: plan v2, 29 sessions from 2026-09-25, opening with a rebuild of the faded basics

## Archive — history, not canon

Read these to learn how a decision was reached; cite the notes above for what stands.

- [teach/message-bus](teach/message-bus/plan.md) — the buses-and-caching workspace that led to "Redis alone"; archived 2026-09-14
- Session logs, closed periods: [August](session-log-2026-08.md) · [1–9 September](session-log-2026-09-01-to-09-09.md) ·
  [10–12 September](session-log-2026-09-10-to-09-12.md) · [12 September, evening](session-log-2026-09-12.md)
- [trading-research-map.pdf](research/trading-research-map.pdf) — the field outside Convex Hedge: 25 fields triaged, Indian cost/tax/margin arithmetic, crypto measured against live APIs — **2026-08-29**. The `.tex` source sits beside it; [research/_raw/](research/_raw/) holds the agent reports behind each claim — open only to verify one

## Capture — raw record

- [inbox/](inbox/) — daily capture, staging only
- [meetings/](meetings/) — onboarding and daily meetings, 17–24 August 2026, promoted into [product-direction](domain/product-direction.md) and [team-workflow](domain/team-workflow.md); the design review of **20 September** and the meetings of **25 and 30 September**, **not yet promoted**
- [sources/](sources/) — their documents, kept off GitHub

## Code repos

Listed in the contract, [CLAUDE.md](CLAUDE.md). **Their own documentation is the canonical answer for
anything inside them** — this vault maps to it and never copies it.

- `payoff-project` — payoff diagrams and Greek maths for option structures. Front door `payoff-project/CONTEXT.md`.
- `Convex-Hedge-Trading-Engine` — **the engine we build on.** Front doors: `CONTEXT.md` (every term),
  `Trading-Engine/Home.md` (its docs vault), `Trading-Engine/Guide/What the engine does.md`,
  `Trading-Engine/Guide/Changelog.md`, `README.md` (running it). Map: [trading-engine](domain/trading-engine.md).
- `convex-hedge-strategy` — Meghav's strategy research. Front doors: `Strategy-Research/Home.md`,
  `Strategy-Research/Guide/SPXW 0DTE descriptive statistics.md`, `CONTEXT.md`. Map: [strategy-research](domain/strategy-research.md).
- `delta-exchange-payoff` — the earlier feed engine. Front doors: `delta-exchange-payoff/CONTEXT.md` (every term),
  `delta-exchange-payoff/docs/split-start-here.md` (what runs and what was chosen),
  `delta-exchange-payoff/docs/split-what-to-do-next.md` (open work), `delta-exchange-payoff/docs/maths-start-here.md`
  (forward, IV, Greeks), `delta-exchange-payoff/docs/storage-start-here.md` (what is kept). Epic #57.

- [code-graphs](domain/code-graphs.md) — which repos have a local Graphify code graph (all three), the commit each was built from, and how Claude uses and refreshes them
