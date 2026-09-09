# Convex Hedge vault

Personal knowledge vault for Convex Hedge. Plain Markdown, read by Obsidian and by Claude Code.

**Start by reading [index.md](index.md)** — the front door. It lists every domain and its status. Open only the notes it points you to.

## What lives here

Knowledge with no home in a code repository: meeting notes, domain understanding, open questions, learning records.

Code truth lives in the code repos and stays there. Reference it with a **pointer** — repo name plus file path — so one copy exists and it cannot drift:

> Data caveats: `payoff-project/docs/data-quality.md`

Linked repos:

- `payoff-project` — payoff diagrams for option structures, at `D:\Convex Hedge\payoff-project`
- `delta-exchange-payoff` — live crypto option analytics over Delta Exchange India, at
  `D:\Convex Hedge\delta-exchange-payoff`
- _Platform repo — access pending._

## Note types

| Where | Holds | Written by |
|---|---|---|
| `inbox/YYYY-MM-DD.md` | Raw daily capture. Staging, not fact. | Human, appended |
| `meetings/` | Dated record of what was said. | Human, appended |
| `sources/` | Their documents, as handed to you. Git-ignores everything inside; never pushed. | Human drops files in |
| `domain/` | One concept per file — the canonical answer. | Human and Claude, on request |
| `index.md` | Curated links and status. A map, never content. | Claude keeps current |
| `GLOSSARY.md` | Canonical terms for Convex Hedge. | Claude, updated in place |
| `MISSION.md`, `RESOURCES.md`, `NOTES.md`, `learning-records/` | Why this vault exists, its sources, and what you now understand. | Human and Claude |
| `teach/<topic>/` | One teach-skill workspace per topic about their system. Never the vault root. | teach skill |
| `session-log.md` | Decisions and open questions. | Claude, appended each session |

## Rules

**Treat `inbox/` and `meetings/` as append-only raw record.** State their contents as fact only after promotion — see `/process-inbox`.

**Cite `domain/`, `GLOSSARY.md`, and `learning-records/` as canon.** Where two of them disagree, surface the contradiction rather than choosing silently.

**Create files only when asked, and keep the folder layout as it stands.**

**Supersede instead of renaming.** Links address files by path, so a rename breaks every link into that note. Replace a note by writing its successor and adding `> Superseded by [successor](domain/successor.md)` at the top of the original.

**Link with relative Markdown links** — `[greeks](domain/greeks.md)`. They resolve in every tool and fail loudly.

**Name files in kebab-case. Hold each note to one topic and under 200 lines**, this file included. Split a note that outgrows the bound.

**Keep Convex Hedge proprietary code and data out of this repo — notes and pointers only.** This vault is a personal repo; their code lives in their repos. Documents they hand you belong in `sources/`, which git ignores.

## Git is the sync layer

`git pull` at session start; commit and push at the end. Obsidian Sync and sync plugins stay off — concurrent writers lose edits silently.

## Commands

- `/process-inbox` — promote durable capture into `domain/` and the glossary
- `/vault-lint` — check links, orphans, note size, inbox overflow
- `/codex-route` — run a published ticket through Codex, gated by Claude. Global skill at `~/.claude/skills/codex-route/`; each linked code repo carries its own `AGENTS.md`. Not used in this vault — implementation happens in the code repos.
