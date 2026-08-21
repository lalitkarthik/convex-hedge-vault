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
- [backtest-engine](domain/backtest-engine.md) — runs, the four report tabs, cost models, and which numbers not to trust — **solid**

## Workspace

- [MISSION.md](MISSION.md) — what I am learning here, and why
- [GLOSSARY.md](GLOSSARY.md) — canonical terms for Convex Hedge
- [RESOURCES.md](RESOURCES.md) — trusted sources
- [NOTES.md](NOTES.md) — working scratch for the teach skill
- [learning-records/](learning-records/) — what I understand, in order
- [teach/](teach/) — teach-skill workspaces, one folder per topic
- [session-log.md](session-log.md) — decisions and open questions

## Capture

- [inbox/](inbox/) — daily capture, staging only
- [meetings/](meetings/) — dated record of what was said
- [sources/](sources/) — their documents, kept off GitHub

## Code repos

Listed in the contract, [CLAUDE.md](CLAUDE.md).
