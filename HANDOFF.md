# Handoff — 2026-10-23

The vault was linted and cleaned today (see the 23 October entry in [session-log.md](session-log.md)).
The previous handoff, of 17 October, is in git history at `f27fbd7`; everything in it that still
holds is below or in the notes it names.

## Start here

Read [index.md](index.md). Every domain note is listed there with its status. For the research work
of October, start at [options-research-harness](domain/options-research-harness.md),
[feature-testing](domain/feature-testing.md) and [databento](domain/databento.md).

## In flight, by repo

- **`options-research-harness`** (Lalit's private repo). Design, build order, feature-loop setup and
  the F1 spec are merged (PRs #1–#4). **PR #5** (Carbon Layer notes, shared working rules, the
  repo's own `docs/handoff.md`) is open and mergeable. **F1 waits on the senior's agreement** to
  the spec; no tickets and no code until then. A friend may continue it with his own Claude.
- **`convex-hedge-strategy`** (Meghav's). PRs #29–#31 are merged. The local branch
  `feature/anomaly-studies` holds **16 commits that are not pushed** (volatility, smile and
  IV-against-tilt anomaly studies). The vault has no record of that work beyond this line. The
  local `main` holds licensed Databento files: never push it.
- **`Backtest-Engine`** (Bilal's). The 12 October lab-run thread: see
  [handoff-2026-10-12](inbox/2026-10-12-ratio-over-the-day/handoff-2026-10-12.md). Local branch
  `feature/spxw-straddle-after-bucket`.
- **`Convex-Hedge-Trading-Engine`**. The Zerodha data feed is merged into `main`. The local
  checkout is on `feature/zerodha-data-feed` with an untracked `.codex/` and `AGENTS.md`.

## Open questions

- Does the senior agree the harness lives in Lalit's personal repo until it is moved (decision
  0006)?
- The two pass bars in `convex-hedge-strategy` disagree (`IMPLEMENTING.md` against the workflow
  page); the senior should be told.
- Is `convex-hedge-strategy` allowed to hold Databento files on GitHub `main`? Its workflow page
  says `data/` is never committed.
- **This vault is a public GitHub repo** (`lalitkarthik/convex-hedge-vault`). It holds notes about
  company repos. Confirm with the senior that this is acceptable, or make the repo private.

## Traps

- **"jev"** is TypeSafe AI's decision model, not "dev-style harness engineering". Ask when a term is
  unfamiliar.
- **Run Databento downloads from `D:\Convex Hedge\convex-hedge-strategy`**, where `.env` lives, not
  from the vault. Data older than twelve months is not free ([databento](domain/databento.md)).
- **The local `convex-hedge-strategy` can be behind GitHub**: pull before copying code.
- **The senior's edge dashboards default to a look-ahead regime** ("dominant regime" uses the
  outcome week). Reuse their charts, never that label.
- **Page builders for the 8 October findings pages live only in
  `%TEMP%\spxw-feature-experiments-kit\`**, and the pages themselves are git-ignored. Copy the kit
  somewhere durable before `%TEMP%` is cleaned.
- Agent and tooling traps are in [team-workflow](domain/team-workflow.md), under *Headless workers*.
