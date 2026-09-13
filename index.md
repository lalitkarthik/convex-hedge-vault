# Convex Hedge — front door

Understand Convex Hedge's options-trading platform and its data well enough to build on it — and
improve our own live engine, which is part of that system.

Read this first, then open only what you need.

## Domains — the terminal (Convex Hedge's backtesting platform)

<!-- one line per domain note: link — what it covers — status (solid / partial / stub) -->

- [platform-map](domain/platform-map.md) — the six surfaces of app.convexhedge.ai, what each is for, what v0.1 has not built, and where its vocabulary collides with `payoff-project` — **solid**
- [option-chain](domain/option-chain.md) — the chain screen: the snapshot model, forward per expiry, all eleven columns, what DTE does to the Greeks, and the data traps — **solid**
- [structure-chain](domain/structure-chain.md) — the straddle/strangle grid and ratio spreads: how a cell is built, the sign convention, and why the Greek views do not work yet — **solid**
- [volatility](domain/volatility.md) — smile and skew, IV against realised vol, the six estimators, and the Feb 2026 regime change — **solid**
- [open-interest](domain/open-interest.md) — OI by strike, PCR, OI change, and the GEX gamma flip with its call and put walls — **solid**
- [strategies](domain/strategies.md) — what a strategy is made of, how hedging is specified, and the parameters that silently do nothing — **solid**
- [backtest-engine](domain/backtest-engine.md) — runs, the four report tabs, per-run parameter JSON, cost models, and which numbers not to trust — **solid**
- [portfolio](domain/portfolio.md) — combining runs into a book: correlation, the no-diversification baseline, and why there is no per-unit track — **solid**

## Domains — our feed engine (`delta-exchange-payoff`)

- [feed-engine](domain/feed-engine.md) — **start here for the engine**: the seven services on a Redis Streams bus, how data moves, what the split promises and does not, the constants, and where each truth lives — **solid, 2026-09-14**
- [bar-store](domain/bar-store.md) — the four tables, seal then flush, the crash-and-replay protocol, the one known loss window (#119), and what the recordings show — **solid, 2026-09-14**
- [service-health](domain/service-health.md) — what each `/health` can and cannot detect, the #103 incident, the logs and alarms, and five improvement candidates — **solid, 2026-09-14**
- [deployment-and-cost](domain/deployment-and-cost.md) — one `c7g.xlarge` on ECS, CPU and RAM measured, T1/T2/T4 costed, the split threshold and the hop — **solid, nothing built yet**

## Learning records — what I understand, in order

- [message-buses](learning-records/message-buses.md) — why a bus exists at all, the three brokers
  measured, Redis Streams' mechanics and its one trap, state sorted by recoverability — **2026-09-07**
- [tests-that-prove-nothing](learning-records/tests-that-prove-nothing.md) — six green tests that
  verified nothing, the five checks that find them, and three mechanisms wearing "flaky" — **2026-09-12**
- [silent-success](learning-records/silent-success.md) — the engine's recurring defect: a value that
  stopped meaning what it says, eight instances, and the five questions that found them — **2026-09-12**

## Workspace

- [MISSION.md](MISSION.md) — what I am learning here, and why
- [GLOSSARY.md](GLOSSARY.md) — canonical terms: the terminal's, the engine's, and where they collide
- [RESOURCES.md](RESOURCES.md) — trusted sources
- [NOTES.md](NOTES.md) — working scratch for the teach skill
- [teach/message-bus](teach/message-bus/plan.md) — message buses and caching against the senior's
  Nautilus + Redis engine. His answers: [what-the-senior-said](teach/message-bus/what-the-senior-said.md);
  teaching order: [sessions](teach/message-bus/sessions.md) — **solid**
- [session-log.md](session-log.md) — decisions and open questions, current period. Closed periods:
  [August](session-log-2026-08.md) · [1–9 September](session-log-2026-09-01-to-09-09.md) ·
  [10–12 September](session-log-2026-09-10-to-09-12.md) · [12 September, evening](session-log-2026-09-12.md)

## Research

- [trading-research-map.pdf](research/trading-research-map.pdf) — the field outside Convex Hedge: 25 trading and quant fields triaged, the Indian cost/tax/margin arithmetic computed from primary documents, crypto measured against live APIs, and eleven unpublished questions worth answering. Source `.tex` alongside it; raw agent reports in [research/_raw/](research/_raw/) — **2026-08-29**

## Capture

- [inbox/](inbox/) — daily capture, staging only
- [meetings/](meetings/) — dated record of what was said
- [sources/](sources/) — their documents, kept off GitHub

## Code repos

Listed in the contract, [CLAUDE.md](CLAUDE.md). **Their own documentation is the canonical answer
for anything inside them** — this vault maps to it and never copies it.

- `payoff-project` — payoff diagrams and Greek maths for option structures, reimplemented to be
  understood. Front door `payoff-project/CONTEXT.md`.
- `delta-exchange-payoff` — the feed engine. Front doors, in order: `delta-exchange-payoff/CONTEXT.md`
  (every term), `delta-exchange-payoff/docs/split-start-here.md` (what runs and what was chosen),
  `delta-exchange-payoff/docs/maths-start-here.md` (forward, IV, Greeks),
  `delta-exchange-payoff/docs/storage-start-here.md` (what is kept). Epic #57. The vault's map of it
  is [feed-engine](domain/feed-engine.md).
