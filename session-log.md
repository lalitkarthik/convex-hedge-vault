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

## 2026-10-01 — the trading engine becomes the engine we build on

**Decided (owner):** `Convex-Hedge-Trading-Engine` (`bilal-sagar-razak/…`, cloned to
`D:\Convex Hedge\Convex-Hedge-Trading-Engine`) is the most recent design and the target of all work
from now on. `delta-exchange-payoff` becomes history and prior design.

**Mapped** at `b47d8ee`: [trading-engine](domain/trading-engine.md) (front door),
[engine-market-data](domain/engine-market-data.md), [engine-strategies](domain/engine-strategies.md),
[engine-dashboard](domain/engine-dashboard.md), [trading-engine-decisions](domain/trading-engine-decisions.md)
(0001–0044) and [engine-lineage](domain/engine-lineage.md), which sets the two engines side by side
and checks the 20/25 September asks against both. The four `delta-exchange-payoff` notes carry a
*Superseded by* line. GLOSSARY was split into two engine glossaries, and its collisions are now
three-way. The MISSION, RESOURCES, team-workflow, code-graphs and CLAUDE.md repo list are updated.

**Graph:** a code-only Graphify graph (319 files, no tokens), in the repo's `graphify-out/`, which
`.git/info/exclude` keeps out of git.

**Found in the repo:** twelve features merged from 26 to 30 September. Live checks #86, #119 and #144
are still open for a person. Feature #150 (analytics tabs: STC, SMI, GEX, GXC; SQLite history;
ECharts) is in flight. Drift: the README status and the project overview still say "no code".
Five merged specs read "awaiting merge". The config comment on the cooldown predates #151.

**Open:** whether the execution engine starts from `delta-exchange-payoff`'s execution pages; where
Bitcoin options (Delta Exchange) enters; which database; whether `teach/execution-design` is rebuilt
on the trading engine.

## 2026-10-01 — the 30 September meeting recorded

**Recorded, not promoted:** [meetings/](meetings/) now holds `30-09-26-recap.txt` (the assistant's
summary plus a marked reading of both transcripts), `30-09-26-transcript.txt` (English rendering)
and `30-09-26-transcript-malayalam.txt`.

**Asked (raw):** build an **Upstox feed adapter** through the engine's own workflow; each person and
each client brings their own broker login for Indian data; watch the live market daily; study how
IV behaves per underlying and per days to expiry; pull 6–12 months of history and the 0DTE
one-minute data; find a generic statistical check for a signal; a short-gamma skeleton with Rahul.
One client links to several engine instances and subscribes to strategy events.

**Checked on 2026-10-01:** Fyers' API and market data are free; Upstox's APIs and websockets are
free; Zerodha's Kite Connect with live data is ₹500 a month per key. The engine already has a
Fyers adapter and none for Upstox or Zerodha.

**Open:** the names of the statistical tests (not captured); why the Discord link was given
(probably the fill-card channel); whether a Databento key was handed over; **whether the engine was
built from scratch or from our `docs/design`** — the transcript reads as scratch, while
[trading-engine](domain/trading-engine.md) and CLAUDE.md say it builds on `delta-exchange-payoff`.

## 2026-10-01 — Upstox first

**Decided (owner):** observe the Indian market through **Upstox**, where an account already exists,
instead of opening a Fyers account. That makes the Upstox feed adapter the first feature we build in
the trading engine.

**Started:** local branch `feature/upstox-data-feed` in `Convex-Hedge-Trading-Engine` (not pushed),
and the research note `Trading-Engine/Research/Upstox data feed.md` (uncommitted, 36 sources).
Its main findings: a free one-year read-only **Analytics token** removes the daily login; the feed is
snapshots, not tick-by-tick, and gives no exchange time for quotes or open interest; NIFTY and
SENSEX at 0–7 days (854 contracts on 1 October) fit one connection; the official library is unsafe
for a long-running reader.

**Open:** the ten decisions listed at the foot of that note, before the spec.


## 2026-10-05 — market observation planned, the live dashboard mapped

**Decided (owner):** observe the live market every trading day, **India and the US in parallel**, one
sitting per market, Claude teaching from the deployed dashboard. First US sitting tonight, first
India sitting on 6 October. The plan is [teach/market-observation](teach/market-observation/PLAN.md):
a fixed sweep of readings, the day so far, one page in depth, a dated record, and a running table,
[normal-ranges](teach/market-observation/normal-ranges.md). A review after ten sittings per market
promotes what held up into `domain/`.

**Mapped:** `india.convexhedge.ai` walked page by page at 15:09–15:14 IST;
[engine-dashboard](domain/engine-dashboard.md) rewritten at `59c1083` (seven pages, Google sign-in,
the Broker page, what each page keeps over time). `convex-hedge-strategy` (Meghav) cloned to
`D:\Convex Hedge\convex-hedge-strategy` and mapped in [strategy-research](domain/strategy-research.md)
at `4bcf653`; it is now a linked repo in CLAUDE.md.

**Found:** each address answers 503 outside its own session. The India badge reads STALE while
Fyers is connected, because the unselected Upstox feed counts as disconnected. Only Spot + GEX, the
smile's open and close curves, and the strategy details pages hold a day's history; the rest are
live snapshots.

**Open:** the two sitting times (defaults 10:00 and 20:00 IST); three readings not yet explained
(two ATM IV figures that differ, the step in NIFTY's IV at the forward, SENSEX's discount factor of
0.9757); whether `spxw.convexhedge.ai` needs its own sign-in; `Convex-Hedge-Trading-Engine` notes
other than the dashboard are still stamped `b47d8ee` while `main` is at `59c1083`.

## 2026-10-05 — US observation, sitting 1

[Record](teach/market-observation/days/2026-10-05-us.md). SPXW 0DTE, 10:45–11:29 ET. Page of the
day: header and option chain. Facts A1–A3 shown; five paper structures opened at 10:47 ET.

**Found:** opening ATM IV about 7.1% against the notebook's 8.0%, 5.2% by 11:30, skew unchanged.
On a same-day expiry the chain's theta equals the time value left (Claude's inference). The
dashboard changed at about 10:50 ET: GEX and Spot + GEX have new layouts and a printed levels table.

**Open:** [engine-dashboard](domain/engine-dashboard.md) is out of date on those two pages and was
not edited; S1's jump from 7,700 to 7,750 at the change; the strategy page losing its morning; the
62-second gap between `spxw-inflow-1000`'s signal and its fills. Sitting 2 settles today's five
structures and closes out A1–A3 from today's candles.

