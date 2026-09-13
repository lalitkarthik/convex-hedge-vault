# Convex Hedge Resources

Trusted sources for this vault. Annotate every entry with what it covers and when to reach for it.

## Knowledge

**app.convexhedge.ai** — the terminal itself. Google SSO, authorised accounts only, currently
v0.1 · Phase 1. Historical NIFTY and SPXW option data, replayed minute by minute. The primary
source for everything in [domain/](domain/); mapped in [platform-map](domain/platform-map.md).
Reach for it when a question is about what Convex Hedge's own system does. Read-only in this vault's
workflow — no rerunning, no deleting, no saving.

**`payoff-project`** — `D:\Convex Hedge\payoff-project`. Independent reimplementation of option
payoff and Greek maths, built to be understood rather than used. Reach for it when a number on the
terminal needs checking against something you derived yourself.

- `CONTEXT.md` — vocabulary, and the reasoning behind each choice
- `docs/calculations.md` — the maths
- `docs/data-quality.md` — data traps
- `docs/adr/` — decisions

Its vocabulary disagrees with the terminal's in two places; both are recorded in
[platform-map](domain/platform-map.md) rather than reconciled.

**`delta-exchange-payoff`** — `D:\Convex Hedge\delta-exchange-payoff`, GitHub
`lalitkarthik/delta-exchange-payoff`. Our live crypto option analytics engine, and the system this
vault is here to improve. Reach for it for anything about the feed, the bus, the bar store, health
or deployment; the vault's map is [feed-engine](domain/feed-engine.md). **The GitHub issues are its
state of record** and win over any document, this vault included.

- `CONTEXT.md` — every term; read first
- `docs/split-start-here.md` — what runs and what was chosen
- `docs/design/hld.md`, `docs/design/lld/` — the design, one LLD per component
- `docs/design/decisions/` — records 0001–0010
- `docs/split-numbers.md` — every measured figure with its run

**Convex Hedge platform repo** — _access pending._ Will supersede inference about how the engine
works. The strategy pages expose Python source, so some engine structure is already visible;
anything read there is theirs and stays out of this repo as a pointer only.

## Wisdom (Communities)

_Empty._

## Gaps

Areas the mission needs where no good source is known yet.

- **Their conventions, as people state them rather than as the UI implies.** Echo, validation,
  what margin means per unit, what regime was meant to hold, why some parameters are decorative.
  Every open question at the foot of a `domain/` note is one of these. They need a person, not a
  screen.
- **Indian index options market structure** — lot size history, expiry calendar changes, settlement
  mechanics. The terminal applies these correctly without explaining them.
- **Dealer gamma positioning** — the assumptions behind any GEX model, and how often they fail.
  Needed before [open-interest](domain/open-interest.md)'s walls can be used rather than noted.
