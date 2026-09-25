# Convex Hedge — front door

Understand Convex Hedge's options-trading platform and its data well enough to build on it — and
improve our own live engine, which is part of that system. **What this vault is for, and how to use
it: [MISSION.md](MISSION.md).**

## Start here

1. [design-decisions](domain/design-decisions.md) — every choice, why, and what replaced what
2. [feed-engine](domain/feed-engine.md) — our engine: what runs, how data moves, what is open
3. [platform-map](domain/platform-map.md) — Convex Hedge's terminal, surface by surface
4. [product-direction](domain/product-direction.md) — what the company asked for, traced to the work

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

## Domains — our feed engine (`delta-exchange-payoff`)

- [feed-engine](domain/feed-engine.md) — seven services on a Redis Streams bus, how data moves, the promises and non-promises, status — **solid, 2026-09-25**
- [bar-store](domain/bar-store.md) — the four tables, seal then flush, crash and replay, the pause loss (#121), what the recordings show — **solid, 2026-09-25**
- [service-health](domain/service-health.md) — what each `/health` can and cannot detect, the #103 incident, component-named logs (#126), improvement candidates — **solid, 2026-09-25**
- [deployment-and-cost](domain/deployment-and-cost.md) — one `c7g.xlarge` on ECS, CPU and RAM, T1/T2/T4, the split threshold and the hop — **solid, nothing built**
- **Execution half — strategy worker, OMS, RMS, paper broker** — designed 2026-09-16, revised by #128 on 09-17, not built. Changes asked on 20 and 25 September are not yet in it. Canon is
  `delta-exchange-payoff/docs/design/execution/00-overview.md`; the decisions are rows in [design-decisions](domain/design-decisions.md);
  the books picture is [assets/oms-books.png](assets/oms-books.png) — **decided, nothing built**

## Across both

- [design-decisions](domain/design-decisions.md) — the ten engine records, standing decisions, the execution-design rows, and the superseded table — **solid, 2026-09-25**
- [product-direction](domain/product-direction.md) — the senior's asks from the August meetings, each traced or marked *not traced* — **partial**
- [team-workflow](domain/team-workflow.md) — idea to merged work: specs, tickets, tests, branches, agents — **solid**

## Learning records — what was learned, in order

- [message-buses](learning-records/message-buses.md) — why a bus exists, the three brokers measured, Redis Streams' one trap — **2026-09-07**, partly superseded by the split
- [tests-that-prove-nothing](learning-records/tests-that-prove-nothing.md) — green tests that verified nothing, and the checks that find them — **2026-09-12**
- [silent-success](learning-records/silent-success.md) — a value that stopped meaning what it says: eight instances, five questions — **2026-09-12**

## Workspace

- [MISSION.md](MISSION.md) — why this vault exists, what success looks like, how to use it
- [GLOSSARY.md](GLOSSARY.md) — canonical terms: the terminal's, the engine's, and where they collide
- [RESOURCES.md](RESOURCES.md) — trusted sources and when to reach for each
- [NOTES.md](NOTES.md) — threads no ticket or note tracks yet
- [session-log.md](session-log.md) — the current period's decisions and open questions
- [AGENTS.md](AGENTS.md) — **Codex is the tutor here**: what it may write, where the material lives, how it teaches

## Study — Codex tutors, Claude builds

- [teach/execution-design](teach/execution-design/PLAN.md) — Convex Hedge's execution design and the feed engine under it, from a trader's seat. Sixteen sessions; **none run yet**
- General options theory — Greeks, structures, ratios, gamma, skew — lives outside this vault in
  `second-brain/learning/option-structures/`: 52 sessions, 1–13 and 19–21 done as of 2026-09-08

## Archive — history, not canon

Read these to learn how a decision was reached; cite the notes above for what stands.

- [teach/message-bus](teach/message-bus/plan.md) — the buses-and-caching workspace that led to "Redis alone"; archived 2026-09-14
- Session logs, closed periods: [August](session-log-2026-08.md) · [1–9 September](session-log-2026-09-01-to-09-09.md) ·
  [10–12 September](session-log-2026-09-10-to-09-12.md) · [12 September, evening](session-log-2026-09-12.md)
- [trading-research-map.pdf](research/trading-research-map.pdf) — the field outside Convex Hedge: 25 fields triaged, Indian cost/tax/margin arithmetic, crypto measured against live APIs — **2026-08-29**. The `.tex` source sits beside it; [research/_raw/](research/_raw/) holds the agent reports behind each claim — open only to verify one

## Capture — raw record

- [inbox/](inbox/) — daily capture, staging only
- [meetings/](meetings/) — onboarding and daily meetings, 17–24 August 2026, promoted into [product-direction](domain/product-direction.md) and [team-workflow](domain/team-workflow.md); the design review of **20 September** and the meeting of **25 September**, **not yet promoted**
- [sources/](sources/) — their documents, kept off GitHub

## Code repos

Listed in the contract, [CLAUDE.md](CLAUDE.md). **Their own documentation is the canonical answer for
anything inside them** — this vault maps to it and never copies it.

- `payoff-project` — payoff diagrams and Greek maths for option structures. Front door `payoff-project/CONTEXT.md`.
- `delta-exchange-payoff` — the feed engine. Front doors: `delta-exchange-payoff/CONTEXT.md` (every term),
  `delta-exchange-payoff/docs/split-start-here.md` (what runs and what was chosen),
  `delta-exchange-payoff/docs/split-what-to-do-next.md` (open work), `delta-exchange-payoff/docs/maths-start-here.md`
  (forward, IV, Greeks), `delta-exchange-payoff/docs/storage-start-here.md` (what is kept). Epic #57.

- [code-graphs.md](domain/code-graphs.md): which repos have a local Graphify code graph, the commit each was built from, and how Claude uses and refreshes them.
