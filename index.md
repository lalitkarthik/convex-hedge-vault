# Convex Hedge — front door

Understand Convex Hedge's options-trading platform and its data well enough to build on it — and
build the **trading engine**, `Convex-Hedge-Trading-Engine`, which since 2026-10-01 is the engine all
work targets and the most recent design. **What this vault is for, and how to use
it: [MISSION.md](MISSION.md).**

## Start here

1. [trading-engine](domain/trading-engine.md) — the engine we build on: what runs, what is built, what is next, where its docs answer
2. [engine-lineage](domain/engine-lineage.md) — what carried over from `delta-exchange-payoff`, what changed, what the meetings asked
3. [design-decisions](domain/design-decisions.md), [trading-engine-decisions](domain/trading-engine-decisions.md) and [trading-engine-decisions-platform](domain/trading-engine-decisions-platform.md) — every choice, why, and what replaced what
4. [platform-map](domain/platform-map.md) — Convex Hedge's terminal, surface by surface
5. [product-direction](domain/product-direction.md) — what the company asked for, traced to the work
6. [options-research-harness](domain/options-research-harness.md) and [feature-testing](domain/feature-testing.md) — the October research: how a strategy idea is tested, and the harness being built to do it

## Domains — the terminal (Convex Hedge's backtesting platform)

<!-- one line per domain note: link — what it covers — status (solid / partial / stub) -->

The code is Bilal's `Backtest-Engine` repo; since 2026-10-11 the terminal is at `research.` and
`lab.convexhedge.ai`. These notes were read off the screen in August and September.

- [platform-map](domain/platform-map.md) — the seven surfaces of the terminal (`research.` and `lab.convexhedge.ai`; `app.` until 11 October), what v0.1 has not built, and where its vocabulary collides with `payoff-project` — **solid**
- [option-chain](domain/option-chain.md) — the chain screen: snapshot model, forward per expiry, the eleven columns, DTE and the Greeks, data traps — **solid**
- [structure-chain](domain/structure-chain.md) — the straddle/strangle grid and ratio spreads: how a cell is built, the sign convention — **solid**
- [volatility](domain/volatility.md) — smile and skew, IV against realised vol, the six estimators, the Feb 2026 regime change — **solid**
- [open-interest](domain/open-interest.md) — OI by strike, PCR, OI change, the GEX gamma flip and its walls — **solid**
- [strategies](domain/strategies.md) — what a strategy is made of, hedging, and the parameters that silently do nothing — **solid**
- [backtest-engine](domain/backtest-engine.md) — runs, the four report tabs, cost models, which numbers not to trust — **solid**
- [portfolio](domain/portfolio.md) — combining runs into a book, and why there is no per-unit track — **solid**

## Domains — the trading engine (`Convex-Hedge-Trading-Engine`, current)

- [trading-engine](domain/trading-engine.md) — the front door: products and pilot, markets and brokers, the parts of one instance, where it runs, status to 23 Oct, where the repo's docs answer, drift — **solid, 2026-10-23**
- [engine-market-data](domain/engine-market-data.md) — the bus (cloud snapshot, market prefix, previous close), feeds (Databento, Fyers, Upstox, Zerodha, replay, synthetic) under one selected broker, the chain engine on the ATM forward with its history store, recording, capture and the stepped engine — **solid, 2026-10-23**
- [engine-strategies](domain/engine-strategies.md) — beats and cards, seven sandbox instances (NIFTY/SENSEX straddles, two NIFTY node graphs, three SPXW), cost models, the simulated broker and its trading journal, Discord fill cards — **solid, 2026-10-23**
- [engine-dashboard](domain/engine-dashboard.md) — `trade.convexhedge.ai/india` and `/spxw`: market roles, each page and what it keeps, the 5 October readings and what since explained them — **solid, 2026-10-23**
- [strategy-research](domain/strategy-research.md) — Meghav's `convex-hedge-strategy`: front doors, a year of data, the SPXW yardstick, the hedged straddle study and the hypothesis folder — **solid, 2026-10-23**
- [trading-engine-decisions](domain/trading-engine-decisions.md) — records 0001–0085 by phase, superseded and amended marked, duplicate numbers explained, what is still undecided — **solid, 2026-10-23**
- [trading-engine-decisions-platform](domain/trading-engine-decisions-platform.md) — records 0086–0156: platform plan, pilot, Track 1, Research track, Graviton, roles — **solid, 2026-10-23**
- [engine-lineage](domain/engine-lineage.md) — `delta-exchange-payoff` against the trading engine after the platform turn, and the 20/25 September asks against both — **solid, 2026-10-23**
- **Execution engine (OMS, RMS, real orders)** — the trading engine's next features; no design page there yet. The prior design is `delta-exchange-payoff`'s, below — **not designed**

## Domains — research (October 2026)

How a strategy idea is tested on SPXW 0DTE data, and the agent harness being built to do it at scale.
Research terms: [glossary-research](domain/glossary-research.md).

- [feature-testing](domain/feature-testing.md) — Bilal's bucket test: what a feature is, the test made exact, what counts as evidence, and the 8 October SPXW results (works as a description, not as a signal; costs decide; Greek ratios; nights; smile) — **solid, 2026-10-23**
- [realised-volatility-estimators](domain/realised-volatility-estimators.md) — the six estimators and intraday squared returns, which one at which horizon, the simulation check, chart mistakes, and where the trading engine builds it — **solid, 2026-10-23**
- [long-gamma-research](domain/long-gamma-research.md) — why the desk wants long gamma, the literature's answer, the 7 October plan, and the result (no idea passed; H1 went the wrong way) — **solid, 2026-10-23**
- [backtest-lab](domain/backtest-lab.md) — Bilal's `Backtest-Engine` repo and lab: his rules, how a strategy reaches the lab, the window-ratio strategy, the ratio-over-the-day findings, the 24 runs still to do — **partial, 2026-10-23**
- [databento](domain/databento.md) — our SPXW option data: what we hold, what it costs (the last year is free), how the API behaves, the downloader and its traps — **solid, 2026-10-23**
- [strategy-research-method](domain/strategy-research-method.md) — how practitioners take an idea to real money in eight stages, the research log, notebooks, and how to search for a new SPXW 0DTE edge with a hypothesis card — **solid, 2026-10-23**
- [options-research-harness](domain/options-research-harness.md) — agents that research SPXW 0DTE under a frozen layer: the layers, the rules, the held year and forward holdout, the trial ledger and deflated Sharpe, the gate, build order F1→F2→F0→F3, status — **partial, 2026-10-23** (designed, not built)
- [agent-harness-design](domain/agent-harness-design.md) — transferable principles from The Carbon Layer series and the harness research: context, memory, skills, sandboxing, meta-harness, evals, self-improvement, MCP tool design — **solid, 2026-10-23**

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

- [design-decisions](domain/design-decisions.md) — our own choices, `delta-exchange-payoff`'s ten records and execution-design rows, the October research and harness decisions, and the superseded table — **solid, 2026-10-23**
- [product-direction](domain/product-direction.md) — the senior's asks from the August meetings, each traced or marked *not traced* — **partial**
- [team-workflow](domain/team-workflow.md) — idea to merged work: specs, tickets, tests, branches, agents, and what headless workers taught (1–17 October) — **solid, 2026-10-23**

## Learning records — what was learned, in order

- [message-buses](learning-records/message-buses.md) — why a bus exists, the three brokers measured, Redis Streams' one trap — **2026-09-07**, partly superseded by the split
- [tests-that-prove-nothing](learning-records/tests-that-prove-nothing.md) — green tests that verified nothing, and the checks that find them — **2026-09-12**
- [silent-success](learning-records/silent-success.md) — a value that stopped meaning what it says: eight instances, five questions — **2026-09-12**

## Workspace

- [MISSION.md](MISSION.md) — why this vault exists, what success looks like, how to use it
- [GLOSSARY.md](GLOSSARY.md) — canonical terms: the terminal's, and where the three systems collide; engine terms split into [glossary-trading-engine](domain/glossary-trading-engine.md) and [glossary-feed-engine](domain/glossary-feed-engine.md), research terms into [glossary-research](domain/glossary-research.md)
- [RESOURCES.md](RESOURCES.md) — trusted sources and when to reach for each
- [NOTES.md](NOTES.md) — threads no ticket or note tracks yet
- [session-log.md](session-log.md) — the current period's decisions and open questions
- [AGENTS.md](AGENTS.md) — the rules Codex followed as tutor (what it may write, how it teaches); Claude tutors since 2026-09-30

## Study — Claude tutors and builds (since 2026-09-30)

- [teach/market-observation](teach/market-observation/PLAN.md) — one sitting per market per trading day on the live dashboard, India and the US; the running table is [normal-ranges](teach/market-observation/normal-ranges.md); the notebook facts repeated against live days are in [notebook-facts](teach/market-observation/notebook-facts.md); the five paper structures opened each sitting are in [structures-book](teach/market-observation/structures-book.md). **Starts 2026-10-05 (US), 2026-10-06 (India)**
- [teach/execution-design](teach/execution-design/PLAN.md) — Convex Hedge's execution design and the feed engine under it, from a trader's seat. Sixteen sessions; **none run yet**. Built on `delta-exchange-payoff`, so it predates the trading engine — revisit before running it
- General options theory — Greeks, structures, ratios, gamma, skew — lives outside this vault in
  `second-brain/learning/option-structures/`: plan v2, 29 sessions from 2026-09-25, opening with a rebuild of the faded basics

## Archive — history, not canon

Read these to learn how a decision was reached; cite the notes above for what stands.

- [teach/message-bus](teach/message-bus/plan.md) — the buses-and-caching workspace that led to "Redis alone"; archived 2026-09-14
- Session logs, closed periods: [August](session-log-2026-08.md) · [1–9 September](session-log-2026-09-01-to-09-09.md) ·
  [10–12 September](session-log-2026-09-10-to-09-12.md) · [12 September, evening](session-log-2026-09-12.md) ·
  [13–16 September](session-log-2026-09-13-to-09-16.md) · [24 September – 1 October](session-log-2026-09-24-to-10-01.md) ·
  [5–8 October](session-log-2026-10-05-to-10-08.md)
- [trading-research-map.pdf](research/trading-research-map.pdf) — the field outside Convex Hedge: 25 fields triaged, Indian cost/tax/margin arithmetic, crypto measured against live APIs — **2026-08-29**. The `.tex` source sits beside it; [research/_raw/](research/_raw/) holds the agent reports behind each claim — open only to verify one

## Capture — raw record

- [inbox/](inbox/) — daily capture, staging only. Every file processed by 2026-10-23 carries a `promoted:` line.
- [meetings/](meetings/) — onboarding and daily meetings, 17–24 August 2026, promoted into [product-direction](domain/product-direction.md) and [team-workflow](domain/team-workflow.md); the design review of **20 September** and the meeting of **25 September**, their asks traced in [engine-lineage](domain/engine-lineage.md); the **30 September** asks recorded in the [session log](session-log-2026-09-24-to-10-01.md) and not yet traced; the **7 October** meet written up in [meeting.md](inbox/2026-10-07-feature-testing/meeting.md) and promoted into [feature-testing](domain/feature-testing.md)
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
- `Backtest-Engine` — Bilal's backtester: the terminal's engine, dashboard and Echo. Front doors: `PROJECT.md`,
  `CONTEXT.md`, `GAPS.md` (known problems), `wiki/00-overview.md`, `Convex-Hedge/` (its docs vault). Map: [backtest-lab](domain/backtest-lab.md).
- `options-research-harness` — Lalit's private repo for the research harness. Front doors: `CONTEXT.md`,
  `docs/reading-guide.md`, `docs/design/00-overview.md`, `docs/handoff.md`. Map: [options-research-harness](domain/options-research-harness.md).
- `delta-exchange-payoff` — the earlier feed engine. Front doors: `delta-exchange-payoff/CONTEXT.md` (every term),
  `delta-exchange-payoff/docs/split-start-here.md` (what runs and what was chosen),
  `delta-exchange-payoff/docs/split-what-to-do-next.md` (open work), `delta-exchange-payoff/docs/maths-start-here.md`
  (forward, IV, Greeks), `delta-exchange-payoff/docs/storage-start-here.md` (what is kept). Epic #57.

- [code-graphs](domain/code-graphs.md) — which repos have a local Graphify code graph (all three), the commit each was built from, and how Claude uses and refreshes them
