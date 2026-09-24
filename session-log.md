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

Split the same way when this file next outgrows the bound: the closed period moves to its own
file, the live entries stay here.

## 2026-09-13 to 09-14 — closing the last non-AWS tickets, and the vault learns the engine

**Decided: #63 and #79 close on an amended criterion** — the owner's call, option 1 of three. Both
asked for "one full day" of recording. #79's 5h12m window already holds the busiest hour (07:00Z)
and seven days show no session structure. #63's 348 clean minutes with zero interior misses bound
the computed-bars miss rate below `derived` ~0.9% at 95% (3/348), against 19.1% before #23's fix;
a full day would tighten that to ~0.2% and change no decision. Rejected: a faster-than-live
replay, because `loadgen.py` only raises CPU load and speed would distort both measurements.

**Decided: the order.** #119 and #118 first, in two worktrees. Then merge, one gate on `main`, and
close #110 with #119. Then #120's rebuild, so the seal-clock fix ships in the same restart that
proves it live. Then #63 and #79. **#63 depends on #119** — its restart criterion is exactly the
minute #110 lost. #79 depends only on #118, which re-tags its figures.

**Decided: the future split is T4, not T2.** The owner proposed `feed` + Redis on one instance and
`store`, `api`, `web` on the other. Record 0008 costed that as T2 ($84.46) and rejected it: `store`
on the far side puts the lossless path across the network and makes the second instance's
replacement race Redis's 30 minutes. T4 moves `store` beside Redis for $73.22. The instance for now
stays one `c7g.xlarge`, confirmed by the owner.

**RAM is measured, not only reserved.** Seven containers `measured` ~1.23 GiB mean, Redis 761.8 MiB
of it. Worst case `derived` ~3.1 GiB of 8. The 8.25 GB of reservations predate the measurement.

**The vault now carries the engine.** Four domain notes — [feed-engine](domain/feed-engine.md),
[bar-store](domain/bar-store.md), [service-health](domain/service-health.md),
[deployment-and-cost](domain/deployment-and-cost.md) — and the learning record
[silent-success](learning-records/silent-success.md). `HANDOFF.md` (a 2026-09-12 watchdog plan) and
an empty `domain.md` removed; `AGENTS.md` is now a pointer to `CLAUDE.md`; the Codex-only
`.agents/` command copies removed with Codex retired.

**Owner's instruction: keep the agent count down.** One agent per concern; the rest inline.

**Open:**
- #119 may conclude there is no safe release valve, and argue for keeping the window plus the
  `store.empty_generation` alarm. That answer needs the owner before #119 or #110 closes.
- A read-only audit of `delta-exchange-payoff`'s HLD, LLDs and front doors against the code is
  running. `docs/split-what-to-do-next.md` is already known stale: it lists #107, #108, #109,
  #111 and #117 as open.
- Whether #8, the historical vol surface, falls under the IV/RV pause. #1, #6 and #7 look built
  and have no closing evidence.
- AWS credentials for #70, #71, #80. IV/RV still parked: #31, #54, #116.

### Later, 2026-09-14 — six closed, two found live, and the vault committed

**Closed with evidence:** #118, #119, #110 (its criterion 2 was #119), #120, #79 (amended).
`main` gated at **1,610 passed, 0 failed** with Docker up — the first run of #119 on a real Redis,
since both agents ran without Docker. One gate on a very long `--basetemp` path failed two tests
that passed alone and on the re-run; recorded, not explained.

**#120's rebuild:** `bar-buffer` pending stayed 0 across 9,639 entries, against 59,146 stranded
before. **None of the 59,146 was recovered** — Redis has no persistence and the stack had been down
since 2026-09-12 18:06Z. The first flush after start wrote all four tables, so #119's release valve
worked live on empty streams.

**#63 was taken live and did not close.** A hard kill at 19:28:30Z lost nothing in any table
(criterion 3, met). A pause at 19:18:07Z kept the open minute in `quote-bars` only — `reference-bars`
and `spot-bars` lost it though 507 frames each arrived at 19:18:04.7Z: **#121**. An earlier kill at
19:04 left `computed-bars` without 19:04, but `computed.chain` held no publish for that minute and
the monolith's own recording had it: the api's minute pass skipped, silently — **#122**. Not
reproduced by the 19:28 kill. **Decided by the owner:** #63 stays open on criterion 5 until #121;
#122 is a ticket whose first step is a per-pass record; #110 gets a comment and stays closed.

**What this revised.** The live 15:56 loss on 2026-09-12 was diagnosed store-side and #119's test
reproduces that mechanism. Today's 19:04 loss had the same picture and an upstream cause. Whether
15:56 had one too cannot be checked — its entries were trimmed. **Two recorders on two paths were
the only witness**: the monolith's `data/` showed the source was fine where neither service could.

**Also decided:** no Claude attribution anywhere in `delta-exchange-payoff`. `origin/main` and all
four other remote branches carry none; 13 stale local pre-rewrite branches still do and are unpushed.

**Open:** #121, #122, #63. AWS for #70, #71, #80. IV/RV parked. #1, #6–#8 untriaged.

**Correction, 2026-09-14.** The RAM figures in this period's first entry were divided by 1,000, not
1,024. Seven containers sum to `derived` **1,226.7 MiB = 1.20 GiB** mean (not ~1.23) and
**1,356.5 MiB = 1.32 GiB** as a sum of p95s (not ~1.36); the worst case with Redis at its 2 GiB
ceiling is ~3.0 GiB of 8 (not ~3.1). CPU is `derived` 1.14 cores mean and 1.91 as a sum of p95s;
there is no 1.36-core figure. `domain/deployment-and-cost.md` corrected in place.

### Later, 2026-09-14 — the vault made reusable

**Decided:** the vault's purpose is written down ([MISSION.md](MISSION.md)) — the memory of the work, so a
fresh session answers *what runs, what was chosen, what is broken, what is next* from `index.md`.
Every design choice is now one row in [design-decisions](domain/design-decisions.md), with a *Superseded*
table (ten replaced choices, from "no broker while one process" to R4's seal clock). The August meetings,
never promoted, became [product-direction](domain/product-direction.md) — each ask traced or marked *not
traced* — and [team-workflow](domain/team-workflow.md). `teach/message-bus` is archived with a banner.
**Figures now live in the repo and conclusions here**: the per-container and constants tables were
replaced by pointers after a copied RAM figure proved wrong. `CLAUDE.md` and `/vault-lint` exempt raw
record from the size bound. **Kept, deliberately:** `research/_raw/` and the `.tex` (the evidence behind the
PDF's claims) and the closed session logs (append-only history), both labelled *Archive* in the index.

**Also:** every service stopped on the owner's instruction — the `dxp` stack, `:8000` and `:3000`. The 13
stale local branches with old Claude trailers deleted; GitHub's contributors API lists no Claude, so the
sidebar entry is GitHub's cache.

**Open:** what "XPX" is; whether `/codex-route` still stands; the *not traced* meeting asks.

## 2026-09-16 — the execution half designed: strategy worker, OMS, RMS, paper broker

**Decided, after three grilling rounds with the owner (all recommendations taken):** the contracts
for the right half of the senior's diagram, written as eight reader-facing pages in
`delta-exchange-payoff/docs/design/execution/` (branch `docs/execution-design`), each with a mermaid
diagram, and as eight new rows in [design-decisions](domain/design-decisions.md). The headline
choices: a strategy publishes a desired position and never an order; orders are diffed **per
strategy** (a deviation from the senior's pooled diagram, to be confirmed with him); the engine's mark
is `client_order_id`, so a fill without one is discretionary and Book 6 is derived; reconciliation
every 10 s freezes a mismatched contract; one `oms` process with risk and execution as modules, the
sandbox a second instance on venue `PAPER`; Postgres for all state that outlives a process; three
tracing ids on every envelope; risk checks reject and never resize; paper broker first, fills at the
touch, never real money in this phase. The books picture: [assets/oms-books.png](assets/oms-books.png).

**Facts established:** Delta's API has no order-source field and positions carry no lineage, so
`client_order_id` is the only mark; there is no pre-trade margin estimate; the India testnet has its
own base address and keys; daily options settle 12:00 UTC (17:30 IST) and auto-close.

**The senior's standing instructions, recorded:** "build first, fix later" — no audits now, the broad
machine first with logging that backtracks; converge on a design document with detailed flowcharts
before any spec or tickets; write for a reader who has never seen the project.

**Open:** the per-strategy-versus-pooled deviation; one-sided stop re-entry semantics; margin model
for Delta; whether the live `oms` sits dormant in compose. Then `/setup-matt-pocock-skills`,
`to-spec`, `to-tickets`. The excalidraw pack waits on gstack being installed on this machine.

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
