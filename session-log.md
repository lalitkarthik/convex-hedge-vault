# Session log

Append-only. Newest entry at the bottom. One block per session: what was decided, and what is still open.

<!-- Entry shape:

## 2026-08-19

**Decided:** ...
**Open:** ...

-->

**Earlier entries are split by period**, because this file reached 304 lines against the
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

Split the same way when this file next outgrows the bound: the closed period moves to its own
file, the live entries stay here.

## 2026-09-24 — the 20 September design review, and Meghav's revision (#128)

**Landed before the review:** `delta-exchange-payoff` #128 (Meghav, merged 2026-09-17) revised the
execution pages: pooled diffing from Book 2 with a settling window, reallocation without orders,
working orders in the execution module's memory with no table, portfolio-level margin that alerts,
tracing ids renamed `decision_id` / `parent_event_id`, `event_log` dropped, manual orders a test hook.

**Asked at the 20 September review (raw notes, not yet promoted):** Redis retention 30 → 5 min, per
feed, which forces the store's 300 s flush down too; market hours per venue and instrument in the
adapter, and a connection controller that follows them; per-instrument multiplier and lot size;
per-adapter subscription lists (SPXW only from Databento, a data vendor, not a broker); a signal
card for slippage research, never read by execution; strategy state in a per-strategy Postgres table
as JSONB with checkpoints; Postgres reached only through the bus; **working orders persisted**, which
reverses #128; reconciliation that re-fires cancelled orders behind a loop guard; Bilal to write
Book 3 documentation by 2026-09-25 and consider a recovery fallback beyond the strategy tag; choose
the execution broker; add authentication; implement test-first after the docs.

**Open:** whether "Postgres only through the bus" covers the OMS; the "outside venue/exchange
folder" note; the 8:00–9:00 window; SPX 0DTE 16:00 and 1DTE 16:30 ET to verify against Cboe. The 18
ClickUp tasks are drafted as a CSV and not yet in ClickUp, because the connector is not connected.
The design pages are not yet edited for any of this; that waits for the next meeting and Bilal's
Book 3 section.

## 2026-09-25 — the 25 September meeting, the vault cleaned, and Codex set up as tutor

**Recorded:** the 20 September review and the 25 September meeting are now raw record in
[meetings/](meetings/) — `20-09-26-recap.txt`, `25-09-26-recap.txt`, `25-09-26-transcript.txt`. Not
yet promoted into `domain/`.

**Asked on 25 September (raw, not yet promoted):** one common OMS serving several brokers, clients,
fund-manager books and venues. Clients **subscribe** to strategies by risk appetite and capital, so
Book 1 and Book 2 differ per client, and orders are placed per client in **strategy units** (a
straddle is 1 lot per leg; a 1:3 ratio is a 4-lot unit). Risk management per client. The
backtest-to-live gap on SPX was put down to one-minute backtest decisions against tick-level live
ones, 0DTE spikes of $10–15 that recover inside a minute, and market orders on stops (stop 9.82,
filled 14.9); the decision cadence must be **configurable** (one minute down to seconds). Execution
must route the same positions to several brokers and serve manual traders. Strategy side: a
long-gamma overlay on the short-gamma book, asset-specific skew, ratios and ratio butterflies,
sigma-band analysis of gap days. Rahul implements and backtests a strategy for a week; Bilal builds
strategy constructs. **Lalit's order: per-client OMS changes first, then strategy work.**

**Cleaned:** `design-decisions` updated for #128 (pooled diffing, working orders in memory,
`decision_id` / `parent_event_id`, portfolio margin, manual door as a test hook), with five rows moved
to *Superseded*. Five engine notes restamped at `27a4d89`; only #126 (component-named logs,
throughput records) touched code since, and `service-health` now says so. This log split at
2026-09-16.

**Decided: Codex tutors, Claude plans and builds.** `AGENTS.md` now gives Codex a tutor's role in
this vault, with its own write area, `teach/`. General options theory stays in the existing
`second-brain/learning/option-structures` workspace, which already covers ratios (sessions 16–17)
and long-versus-short gamma judgment (31–32). A new `teach/execution-design/` workspace covers
Convex Hedge's own design. Claude promotes durable results into `domain/`.

**Open:** the per-client OMS design (subscriptions, units, per-client books and risk); whether the
20 September changes and the 25 September ones are folded in together; the 20 September questions
still unanswered (Postgres via the bus for the OMS too, the venue folder, the 8:00–9:00 window).
