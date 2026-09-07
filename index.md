# Convex Hedge — front door

Understand Convex Hedge's options-trading platform and its data well enough to build on it.

Read this first, then open only what you need.

## Domains

<!-- one line per domain note: link — what it covers — status (solid / partial / stub) -->

- [platform-map](domain/platform-map.md) — the six surfaces of app.convexhedge.ai, what each is for, what v0.1 has not built, and where its vocabulary collides with `payoff-project` — **solid**
- [option-chain](domain/option-chain.md) — the chain screen: the snapshot model, forward per expiry, all eleven columns, what DTE does to the Greeks, and the data traps — **solid**
- [structure-chain](domain/structure-chain.md) — the straddle/strangle grid and ratio spreads: how a cell is built, the sign convention, and why the Greek views do not work yet — **solid**
- [volatility](domain/volatility.md) — smile and skew, IV against realised vol, the six estimators, and the Feb 2026 regime change — **solid**
- [open-interest](domain/open-interest.md) — OI by strike, PCR, OI change, and the GEX gamma flip with its call and put walls — **solid**
- [strategies](domain/strategies.md) — what a strategy is made of, how hedging is specified, and the parameters that silently do nothing — **solid**
- [backtest-engine](domain/backtest-engine.md) — runs, the four report tabs, per-run parameter JSON, cost models, and which numbers not to trust — **solid**
- [portfolio](domain/portfolio.md) — combining runs into a book: correlation, the no-diversification baseline, and why there is no per-unit track — **solid**

## Workspace

- [MISSION.md](MISSION.md) — what I am learning here, and why
- [GLOSSARY.md](GLOSSARY.md) — canonical terms for Convex Hedge
- [RESOURCES.md](RESOURCES.md) — trusted sources
- [NOTES.md](NOTES.md) — working scratch for the teach skill
- [learning-records/](learning-records/) — what I understand, in order
  - [message-buses](learning-records/message-buses.md) — why a bus exists at all, the three
    brokers measured, Redis Streams' mechanics and its one trap, state sorted by
    recoverability, and why our cache cannot go stale — **2026-09-07**
- [teach/](teach/) — teach-skill workspaces, one folder per topic
  - [message-bus](teach/message-bus/plan.md) — message buses and caching: our in-process fan-out
    against the senior's Nautilus + Redis engine, RabbitMQ vs Redis vs Kafka measured, and the
    four caches. His answers are in [what-the-senior-said](teach/message-bus/what-the-senior-said.md);
    the teaching order is [sessions](teach/message-bus/sessions.md) — **solid**
- [session-log.md](session-log.md) — decisions and open questions

## Research

- [trading-research-map.pdf](research/trading-research-map.pdf) — the field outside Convex Hedge: 25 trading and quant fields triaged, the Indian cost/tax/margin arithmetic computed from primary documents, crypto measured against live APIs, and eleven unpublished questions worth answering. Source `.tex` alongside it; raw agent reports in [research/_raw/](research/_raw/) — **2026-08-29**

## Capture

- [inbox/](inbox/) — daily capture, staging only
- [meetings/](meetings/) — dated record of what was said
- [sources/](sources/) — their documents, kept off GitHub

## Code repos

Listed in the contract, [CLAUDE.md](CLAUDE.md). Their own documentation is the canonical answer
for anything inside them — this is a map to it, never a copy of it.

- `payoff-project` — payoff diagrams for option structures.
- `delta-exchange-payoff` — live crypto option analytics over Delta Exchange India: our own
  implied volatility and Greeks computed off the websocket while the venue's own figures travel
  beside them, and a one-minute bar store. Two front doors, both written to be read first:
  `docs/maths-start-here.md` for how the forward, the IV and the Greeks are each computed, and
  `docs/storage-start-here.md` for what is kept and where. The evidence behind them is in
  `docs/forward.md`, `docs/implied-vol.md`, `docs/settlement.md`, `docs/ingestion.md`,
  `docs/storage.md` and the published interface in `docs/chain-contract.md` — **2026-09-04**
