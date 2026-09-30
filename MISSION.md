# Mission: Convex Hedge

**This vault is the memory of the work.** A new session — a person, or Claude — should be able to
answer *what runs, what was chosen and why, what is broken, and what is next* from here, without
reading old chats. It holds understanding and decisions; the code repos hold the code.

## What it is for

1. **Understand Convex Hedge's terminal and its data** well enough to build on it —
   [platform-map](domain/platform-map.md) and the terminal notes.
2. **Build and improve the trading engine**, `Convex-Hedge-Trading-Engine`, the current design
   since 2026-10-01: feed, bus, chain, strategies, execution — [trading-engine](domain/trading-engine.md).
   Our earlier engine, `delta-exchange-payoff`, is history and prior design — [engine-lineage](domain/engine-lineage.md).
3. **Keep every design choice, its reason, and what replaced it, in one place** —
   [design-decisions](domain/design-decisions.md).
4. **Trace what the company asked for** in meetings to the work that answers it —
   [product-direction](domain/product-direction.md).
5. **Keep what was learned, so it is not relearned** — [learning-records/](learning-records/).

## Success looks like

- A fresh session gets from [index.md](index.md) to a correct answer on *what runs, what was chosen,
  what is broken, what is next* in under ten minutes.
- Every design choice has one row in [design-decisions](domain/design-decisions.md), a pointer to its
  record, and its successor once replaced.
- **No figure lives only here.** Each number a note quotes can be found in the repo file it points at;
  conclusions live here, evidence lives there.
- Every meeting ask is either traced to work or marked *not traced*.
- `/vault-lint` passes, and the vault is committed and pushed at the end of every session.

## Constraints

- **Their proprietary code and data stay out.** Pointers only; documents they hand over go in
  `sources/`, which git ignores.
- **The GitHub issues are the state of record** for tickets. This vault points at them and never
  replaces them.
- **Raw record is append-only** — `inbox/`, `meetings/`. It becomes fact only once promoted.
- **Notes stay under 200 lines**, one topic each. Supersede, never rename.
- **Owner's standing instructions**: no AI attribution in any commit or PR; IV/RV work is parked.

## Out of scope

- Code, build steps and run commands — those are each repo's `AGENTS.md` and `CLAUDE.md`.
- Ticket status beyond a pointer — GitHub.
- Teaching a topic step by step — that is a `teach/<topic>/` workspace, not this file.
- Market data, trade records, or anything that is advice about money.

## How to use it

| When | Do |
|---|---|
| Starting a session | `git pull`, then read [index.md](index.md) |
| A concept becomes clear | One `domain/` note; stamp it `> As of <repo>@<sha>, <date>` if it cites code; link it from `index.md` |
| A decision is made or replaced | A row in [design-decisions](domain/design-decisions.md); the old one moves to *Superseded* |
| A meeting happens | A file in `meetings/`; promote what is durable with `/process-inbox` |
| A lesson is learned the hard way | A `learning-records/` entry, dated |
| Ending a session | Append [session-log.md](session-log.md), run `/vault-lint`, commit, push |
