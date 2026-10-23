# Session log

Append-only. Newest entry at the bottom. One block per session: what was decided, and what is still open.

<!-- Entry shape:

## 2026-08-19

**Decided:** ...
**Open:** ...

-->

**Earlier entries are split by period**, because this file reached 304 lines (and again 392 on 2026-10-23) against the
vault's 200-line bound:

- [session-log-2026-08.md](session-log-2026-08.md) - the terminal survey and the six depth passes
- [session-log-2026-09-01-to-09-09.md](session-log-2026-09-01-to-09-09.md) - Engine Feed
  Management, the services epic designed, and its first week
- [session-log-2026-09-10-to-09-12.md](session-log-2026-09-10-to-09-12.md) - the
  senior's review folded into #57, and the audit's findings fixed and closed
- [session-log-2026-09-12.md](session-log-2026-09-12.md) - the store stalled and nothing said
  so, the fixes landed, and the defect shape behind eight incidents
- [session-log-2026-09-13-to-09-16.md](session-log-2026-09-13-to-09-16.md) - the last
  non-AWS tickets closed, the vault made reusable, and the execution half designed
- [session-log-2026-09-24-to-10-01.md](session-log-2026-09-24-to-10-01.md) - the 20 September
  review and #128, the 25 and 30 September meetings, and the trading engine adopted
- [session-log-2026-10-05-to-10-08.md](session-log-2026-10-05-to-10-08.md) - market observation
  begun, long-gamma research planned and tested, and the feature experiments built

Split the same way when this file next outgrows the bound: the closed period moves to its own
file, the live entries stay here.

## 2026-10-15 to 2026-10-17 — the options research harness, from the book to a design grilling

**15 to 17 October: the options research harness, from the book to a design grilling.** Bilal asked
Lalit and Meghav to read López de Prado's *Advances in Financial Machine Learning* and to build a
faster research pipeline by connecting MCP servers. Six research lanes went into
[inbox/2026-10-16-options-harness-research/](inbox/2026-10-16-options-harness-research/findings.html):
agent harnesses, options backtesters, alpha axes, validation, MCP tools and Jev. Lalit is learning
harness engineering from The Carbon Layer's playlist; study notes on all twelve videos, with a
glossary and the principles, are in
[inbox/2026-10-17-carbon-layer-harness/](inbox/2026-10-17-carbon-layer-harness/00-index.md). Facts
about our code, data, docs and the senior's dashboards are in
[inbox/2026-10-17-harness-planning-facts.md](inbox/2026-10-17-harness-planning-facts.md).

Decisions from the grilling so far:

- The harness lives in a private repo on Lalit's own GitHub, `options-research-harness`, cloned to
  `D:\Convex Hedge\options-research-harness`. Company code may be copied into it; the senior moves
  it into the organisation later. Python, matching `convex-hedge-strategy`.
- SPXW 0DTE only for now.
- The harness improves itself as in video 02: weakness mining, an editable surface, held-in and
  held-out tasks, an acceptance rule, and a PR that a human merges. It never writes to the frozen
  layer (data, labels, splits, cost model, scoring).
- Agents follow videos 05 and 10: code owns the steps between tasks and the limits; specialist
  agent packages judge inside a step; results are read from files and git, never from an agent's
  report; each step returns one JSON block checked against a schema.
- Logs follow the IBM talk and video 10: one append-only event file per run, rendered into a report
  a person can read, with trial cards and a ledger index built from it.
- An evaluation harness tests the research harness (video 08); its detailed design waits.
- Feature combination is in the design and is built after single features are screened.
- The specialist roles from the research stay, including a strategist who must give each feature an
  economic story.
- Ideas come from forums (Elite Trader, r/thetagang, r/options, r/quant, Quant StackExchange, a few
  volatility Substacks), as leads only.
- One backtester interface, local first; the engine adapter waits for the senior's MCP, which is
  not built yet. Our run record matches the engine's outputs.
- The context pack comes from the findings in the `convex-hedge-strategy` notebooks.
- Regimes: high against low volatility is one example only. The research looks at every axis that
  can condition a result, each known at decision time, with lines drawn on the train half.
- Pass bar: the workflow page's version (one variant, picked on the train half).
- Backtest-Engine's maths is the canonical version (its 405-minute clock).
- Docs: feature-loop's `docs/design/` layout, written in plain, good English for a new reader, with
  Excalidraw diagrams and the playlist's terms.
- Build order F0 to F8, as proposed in the grilling.
- The 2024-07-01 to 2025-06-30 data is the sealed holdout. Lalit believes it is free; the ledger shows
  older days cost about $0.02 to $0.07 each. Lalit runs the download.

**Open:** Lalit asked to slow down and finish the playlist first, so the grilling is paused. Still to
settle: the evaluation harness in detail; the data download and its cost; whether the harness may
re-check results that came from the convex_strategy clock.

## 2026-10-19 to 2026-10-22 — harness: build order, setup, F1 spec, hand-over

**Decisions** (full reasoning in `options-research-harness`, `docs/design/grilling-log.md`):
- Design PR #1 merged. Build order changed to F1 ledger → F2 tools → F0 frozen layer → F3
  meta-harness (Q46, PR #2): the frozen layer guards against agents, and none exist before F3.
- The tools are built and tested on the free year we hold (Q47); the senior may get more data.
- Feature-loop setup merged (PR #3). F1 slice grilled (Q48–Q52, decision 0007): records in a
  git-ignored `records/` folder inside the main checkout, hash-chained JSON Lines, ledger rebuilt
  from `trial_recorded` events, `harness demo` and `harness build-views`, HTML pages. Spec merged
  as docs PR #4; no tickets and no build until the senior agrees.
- The Carbon Layer study notes are now committed here and copied into the harness repo at
  `docs/research/carbon-layer/`, so a second person's Claude reads the same terms.

**Open:** a friend continues the harness with his own Claude (handoff at the repo's
`docs/handoff.md`). His Claude does not have Lalit's `feature-loop` skill or memory notes.

## 2026-10-23 — vault lint, inbox processed, stale notes refreshed

**Linted** all eight checks. Pointers and orphans passed. Fixed: one broken link (the 12 October
handoff to `sources/`); this log split at 392 lines into
[24 September – 1 October](session-log-2026-09-24-to-10-01.md) and
[5–8 October](session-log-2026-10-05-to-10-08.md); every inbox file now carries `promoted:`.

**Promoted** (the owner said to do all of it without asking): nine new domain notes —
[feature-testing](domain/feature-testing.md), [realised-volatility-estimators](domain/realised-volatility-estimators.md),
[long-gamma-research](domain/long-gamma-research.md), [backtest-lab](domain/backtest-lab.md),
[databento](domain/databento.md), [strategy-research-method](domain/strategy-research-method.md),
[options-research-harness](domain/options-research-harness.md), [agent-harness-design](domain/agent-harness-design.md),
[glossary-research](domain/glossary-research.md) — plus [trading-engine-decisions-platform](domain/trading-engine-decisions-platform.md),
split from the decisions map. The terminal notes took the September lab readings (seven surfaces,
MID prices on SPX, the ratio grid's formula, the DIVERSIFICATION tab). Twenty-two research and harness
rows went into [design-decisions](domain/design-decisions.md).

**Restamped** against `origin/main`: the seven trading-engine notes at `06e547fa` (2,056 commits since
`b47d8ee`), [strategy-research](domain/strategy-research.md) and notebook-facts at `292f816`.

**Found:**
- **The terminal moved.** Since 2026-10-11 it is `research.convexhedge.ai` (beta users) and
  `lab.convexhedge.ai` (in-house); `app.convexhedge.ai` is the trading engine's pilot. The terminal's
  code is Bilal's `Backtest-Engine` repo, so the "platform repo, access pending" line in CLAUDE.md is
  now that repo.
- **The harness holdout changed.** The 15–17 October entry above names 2024-07-01 to 2025-06-30 as
  the sealed holdout. The harness repo replaced it on 2026-10-17 with a forward holdout (days after
  2026-09-30; decision 0004), because the old year costs money.
- **The feature experiments are on GitHub `main`** (`cc8b0ef`), not only on a local branch.
- **Unrecorded work:** 16 local commits on `convex-hedge-strategy` `feature/anomaly-studies`, not
  pushed, and the 9–14 October sessions have no entry here.
- **This vault is a public GitHub repo.** The three 8 October findings pages and the 17 October
  harness planning facts are git-ignored for that reason.

**Decided (owner, same day):** push everything, the findings pages and the planning facts included;
the owner will make the vault private later. Only `sources/` stays git-ignored, as CLAUDE.md says.

**Open:** the
30 September asks are not yet traced into a domain note; the drift lists in
[trading-engine](domain/trading-engine.md) and [engine-strategies](domain/engine-strategies.md) are for
the engine's owners.
