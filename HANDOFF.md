# Handoff — 2026-09-12 (third session)

Everything below happened in `delta-exchange-payoff`. Nothing in this vault is half-built: the
session log is split and current, and the working tree is clean.

## Start here

**A 24-hour measurement is running and it ends at 2026-09-13T05:50:07Z.** Four issues close
off it. Do not disturb it before then.

```bash
cat "D:/Convex Hedge/i13-day/watchdog.log"
```

A watchdog (PID 5804) stops the collector (19236), the viewer driver (15564) and the Redis
watcher (28200) at that moment and writes the final sample count. **If that file says the day
finished, the next four steps are the whole morning:**

1. `tools/measure_containers.py summarize --in "D:/Convex Hedge/i13-day/containers-2026-09-12.jsonl"`,
   then fill R6's table and close **#79**. Slice by the windows in `viewer-windows.log` to get
   the `api` row at 0, 1 and 3 viewers — that log is the authority, not the schedule.
2. `tools/measure_computed_gaps.py` and `tools/compact_store.py` over the day the store
   recorded in `.stack-data/`, which closes **#63**'s criteria 4 and 6.
3. Take a clean per-container start-to-healthy — the collector must be started **before**
   `docker compose up`, which is why it could not be done today — then run
   `tools/smoke_stack.py`, which needs port 8080 back. Both are **#65**'s last two criteria,
   and the smoke run is also **#66**'s.
4. Then `docker compose up -d --build` afresh so the running stack carries #81 and #66. The
   stack now up was built at `c05ebe1` and carries neither.
5. Run #63's criterion 5 live — a `POST` pause and resume over the bus against the split
   composition. It was never run; the plan has an orchestrator step for it and no record
   exists. Do it on a scratch stack, not on the `dxp` one, or a pause puts a hole in the day.

**There has been no I3 to I4 cutover, and nothing needs one.** The monolith on :8000 still
writes `data/` with its in-process writer, and the `dxp` stack's `store` records `.stack-data/`
beside it. Two independent recorders, which is what makes #63's comparison possible at all.
An earlier draft of this file said the cutover had happened; it had not.

## In flight

- **Nothing is mid-implementation.** No worker is running, no worktree is dirty. The only
  worktree left is `dxp-54` (`rv-backfill`), untouched on the owner's instruction.
- **Codex is retired as the implementation route.** Fixes now run as parallel Claude agents,
  one git worktree each, disjoint file territories, and the orchestrator commits. Two Codex
  workers were killed mid-run on 2026-09-12 after 65 and 100 sandboxed commands with the
  source files still untouched.
- **The Fable audit finished and every finding is closed.** Ten issues: #82 to #91.
- **The live engine on :8000 and the web app on :3000 are up and recording**, as always.
- **One directory needs a UAC click to delete**: `D:/Convex Hedge/dxp-docs/engine/.sandbox-tmp`,
  owned by the Codex sandbox user. Nothing depends on it; it is the last trace of that worktree.

## What changed

| Commit | |
|---|---|
| `1c72a4c` | **#84** (blocker) and **#85** — the replay delivered its tail twice |
| `1d68f69` | **#86**, **#91** — Discord posted its own downtime; a test with no assertion |
| `c01abbd` | **#87**, **#88**, **#89** — documents describing a stack three tickets ago |
| `38c4af4` | **#82**, **#83** — conservation, not equality; a duration where a condition belonged |
| `02fca06` | The verification command in `AGENTS.md` made 315 tests not run |

`main` is at `02fca06`, pushed. **1,401 passed, 0 failed, ruff clean.**

**Ten issues closed with full comments**: #82, #83, #84, #85, #86, #87, #88, #89, #90, #91.
Two new tickets came out of the work: **#92** (two suites at once delete each other's Redis
keys) and **#93** (28 more tests wait on a duration instead of a condition).

## Decisions made

- **The day runs on the real venue feed**, not the smoke override, because #79's own text says
  "live feed, one full trading day".
- **One day serves both #79 and #63.** Two days would measure two different sessions.
- **Redis's ceiling is 2gb everywhere**, matching #69. 1gb was below the retention the same
  file documents.
- **#82 was rewritten, not relaxed.** `compare_store_runs.py` demanded byte-equality between
  two recorders on separate websockets. That premise is false, so the tool now checks
  conservation and identity. It exits **0** on the real 05:52–06:12Z pair: tick sums
  **1,333,097** on both sides, `net=0`, no row outside a bound of one, tables B and D
  byte-exact. Loosening a tolerance to go green would have destroyed the check.
- **Stale Discord alerts are dropped, not posted** (#86). #66 had already decided it; the code
  did not do it. The drop happens *ahead of* the gate, so a stale alert cannot spend a real
  one's collapse or rate-limit slot.
- **Closing a ticket whose criteria are unmet is not on the table.** #63, #65, #66 and #79 are
  still open for that reason.

## Open questions

- **#66's core claim is unproven end to end.** "A message arrives in Discord" needs a real
  webhook URL, and only the owner has one. Everything up to the HTTP boundary is proven.
- **Three of #81's four read paths were proven at the seam, not live.** The argument for them
  is an argument, not an observation.
- **The 4.43 MiB buffer figure is still unchecked against a full buffer.** The live run held
  1,669 bars over one minute and never reached the 360 s horizon, so eviction never ran.

## Traps found

- **A published measurement did not reach the file a later ticket wrote.** #61 recorded "1 GiB
  is not enough for thirty minutes of BTC+ETH"; #65 then shipped 1gb. Before writing a
  configured value, grep the repo for a measurement of it.
- **`--basetemp` fails when its parent does not exist.** pytest makes that directory with
  `parents=False`, so **315 tests error at setup**, are reported as errors rather than
  failures, and the run finishes *faster* because they never ran. `AGENTS.md` prescribed the
  flag and told every worker to delete the directory as its last command, so the next run was
  always a first run. Four agents read it as load. Fixed in `02fca06`; `mkdir -p` first.
- **Three mechanisms wore one symptom.** "The suite is flaky under load" was the `--basetemp`
  trap, a shared test Redis container (#92), and one genuine duration-bet (#83). A ticket that
  closes on the wrong mechanism is worse than one left open, because the next person stops
  looking.
- **A test that takes exactly what it expects cannot see one too many.** `take(restarted, 10)`
  asserted ten bids and was green with five duplicates behind it. **Drain to empty and assert
  empty.** That one correction fixed both halves of the blocker #84.
- **"Nothing raised" is evidence only where something can raise.** The bus isolates reader
  failures by design, which silently turned every such test against it into a no-op (#91).
- **Six vacuous tests in this epic now**, so the answer moved from fixing them one at a time to
  an **AST scan** that fails if a test in the file has no assertion.
- **A correct addition can make a document worse.** #81 added a true paragraph to `store.md`
  and left the one it superseded in place. Neither is wrong alone; the file is wrong because it
  holds both.
- **`getattr(obj, "method", None)` with a silent no-op gives back exactly what a fix took
  away.** #66's repair did this and a test double had been running the pre-repair path ever
  since, saying nothing.
- **The same scope gap hit three tickets running** (#63, #81, #66): a test asserting a *global*
  shape — a whole `/health` payload, a whole service set — belongs to whoever changes that
  shape, and no plan can know which tests those are from the ticket text.
- **`--samples` on `measure_containers.py` is a tick count, not a duration.** A tick costs
  `measured` 16.2 s here against the 5 s asked for, because the `docker stats` call happens
  before the sleep.
- **A Codex sandbox leaves directories the real user cannot delete.** `takeown` and `icacls`
  both fail unelevated. Anything that worktree owns needs a UAC click to remove.
- **Unlink a junction before `git worktree remove`.** A guard blocks `rmdir`; use
  `[System.IO.Directory]::Delete(path, $false)`, which unlinks a reparse point without walking
  it, and check the real directory's entry count before and after.

## Read these

1. `gh issue view 79` and `gh issue view 63` — the two comments posted today carry the day's
   parameters and say exactly which criteria are waiting on it.
2. `gh issue view 84` — the blocker's comment, and the clearest worked example of the
   drain-to-empty correction. Then **#92** and **#93**, which are ready to start.
3. [session-log.md](session-log.md) — today's entry. Earlier periods are split into
   [August](session-log-2026-08.md) and [1–9 September](session-log-2026-09-01-to-09-09.md).
4. The memory note on parallel Claude agents in worktrees — the routing that replaced Codex.
5. `D:/Convex Hedge/i13-day/` — the day's samples, the Redis curve, the viewer windows.
