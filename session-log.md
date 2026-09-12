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

Split the same way when this file next outgrows the bound: the closed period moves to its own
file, the live entries stay here.


**The senior's review, folded into the epic, 2026-09-12.** Six things came out of the
meeting and each is now a decision in #57 and a ticket under it, grilled to a shared
understanding first. Stream names lose the environment slot — one local, one prod, never a
shared Redis, so `{env}:` protected nothing; record 0001 gains a successor rather than a
rewrite, and I11 (#74) lands before I3 so the split builds on the final grammar. The store
partitions `underlying/date`, no venue level; I12 (#77) moves the 4,812 files once, engine
stopped at a flush boundary, between I3 and I4 and before anything reaches S3. Two research
tickets replace an adjective with a table: R6 (#75) derives a per-service load profile from
the monolith's `measured` numbers with `oms` and `strategy` as `assumed` rows — the senior
named services that do not exist, and a topology with no slot for them is redone the day
they arrive — and R7 (#78) costs one box against several on that profile, confirming or
superseding 0005 while #68 stays closed. The inter-instance hop is answered `derived` for
the five real services — same AZ, three orders below a one-second refresh — and left open
for `oms`, where a millisecond may matter. R8 (#76) settles compaction on the go against
at the close with a measurement, having established that Parquet cannot append and the
only thing keeping the open day out of the compactor is a non-atomic flush. D1 (#72) is now
the single source of truth he asked for — action-first, Simplified Technical English, a
`CONTEXT.md` for the vocabulary. I13 (#79) and I14 (#80) are the "re-cost after #65" and
"measure the hop after access" promises, made tickets. `to-tickets` was followed by hand:
numbered breakdown approved before publishing, native blocking edges, blockers first.
Frontier is now I11, R6, R8 in parallel; #62 waits on #74. Owed: `epic.md` was 233 lines
before this and is longer now; it mirrors an issue that wins, and should become a pointer
or be split.

**First run of the Codex route, 2026-09-12.** Six tickets closed in `delta-exchange-payoff`:
#73 (not planned), R6 #75, R8 #76, I11 #74, R7 #78 and I3 #62 (`b4d5fce`). Research went to
Opus; implementation to Codex Luna max, planned first by Sol medium read-only, gated by
Claude, reviewed by Sonnet — every Codex run passed on its first attempt, no escalation.
Answers worth keeping: R7 keeps one box but a `c7g.xlarge`; R8 keeps nightly compaction for
local disk. I3's live check killed `feed` for 14.8 s and the ladder came back 0.59 s after
it did. Sandbox traps found and written into `~/.claude/skills/codex-route/SKILL.md`: the
first command after a reboot fails once; the sandbox user can write neither `%TEMP%` nor any
directory the real user made, so its temp tree is `.sandbox-tmp/`. In flight: I12 #77 (store
layout migration) and the I5 #64 plan. Owed: nightly compaction has never run on this
machine; this log is past the 200-line bound and should be split.

**The rest of that run, 2026-09-12.** Four more tickets landed: I3 #62 (the feed as its own
process), I12 #77 (the store's underlying-first layout, including a live migration of 5,098
files with the engine stopped 133 s at a flush boundary), I5 #64 (the api learns the feed's
state from the bus and commands it over the bus), and #54 (realised volatility read from a
backfilled index series). Two blockers were caught before they could cost anything, each by a
different check: the store migration tool had no `__main__` block, so run as a command it
printed nothing, moved nothing and exited 0 while 1,120 tests passed — found by a trial
migration on a copy of real data, not by the suite or the review; and a failure partway
through its delete phase would have stranded the migration unresumable — found by the review,
which reproduced it. Both fixed in one repair round. I4 #63 was not built: its planner refused,
naming seven unsettled design questions, so an Opus pass settled them in decision
`0010-store-replay.md` and the owner answered five judgment calls, one of which became a new
ticket, #81. Method notes worth keeping: two tickets whose files are disjoint ran at once in
separate git worktrees; and when the Codex 5-hour window reached 91%, the routing rule moved
#54's implementation to Claude without ceremony, which is the behaviour the rule was written
for.

**The day-long measurement, and four tests that proved nothing, 2026-09-12 (second session).**
The day #79 and #63 both need was started first, because it is the only thing on the critical
path that wall clock alone can finish: the Compose stack rebuilt from `main` after #63 landed,
brought up on the **real venue feed** at 05:49:32Z, all six containers healthy including
`dxp-store`, which had never started before because `store_main.py` did not exist when #65 was
gated. Setting it up found three things the run would otherwise have been spoiled by. Redis was
capped at **1gb under `noeviction`**, and at its ceiling Redis refuses writes -- so the stack
was configured to stall itself at steady state and take both tickets with it. The number was
not new: **#61 had already published** "1 GiB is not enough for thirty minutes of BTC+ETH and
#69's 2gb is", and had raised its own container mid-run. #65 then shipped the value that
finding rejects. Fixed live with `CONFIG SET` and in the file (`49c23c5`); the steady state is
now `measured` **758.6 MB for one underlying**, flat once the trim engages, which puts the
second underlying at **+39%** and independently corroborates the older "ETH costs +55% on
message rate" result. Second, the day would have answered only one third of R6's `api` row,
which is costed "at 0, 1 and 3 viewers" -- a driver now holds each count through the proxy a
browser uses. Third, `--samples` is a **tick count, not a duration**, and a tick costs
`measured` 16.2 s here against the 5 s asked for, so 17,280 ticks is 77 hours; a watchdog
enforces the day instead. That one was my own arithmetic, caught by reading the file rather
than the flag.

**#81 and #66 landed** (`f2fd905`, `ed7b538`), with #81's live half proven on a scratch split
stack: `/smile` answered minute 07:55:00Z while the store root held **zero Parquet files**, so
the minute could not have come from disk because there was no disk to come from. Honest limit:
one of four read paths was proven live, and two bugs in my own script cost the other three.
#81 is closed. **#63, #65, #79 and #66 stay open**, each on criteria that need either the
running day or the owner -- the smoke test cannot bind port 8080 while the day holds it, and
only he has the Discord webhook. Ticking those boxes today would have been a lie.

**The theme of the day was tests that pass while proving nothing, and it is now four.** A
compose test asserted `"1gb" in blocks["redis"]` against a block that includes its own
comments, so it was satisfied by prose, never read the configuration, and **passed unchanged
when I moved the real ceiling to 2gb**. It had been vacuous since the day it was written.
Before it: `migrate_store.py` with no `__main__`, `smoke_stack.py` discarding its argv, and
`fakeredis` hiding the `behind` defect. **Three of the four were found by running something
rather than reading it.** Two more of the same family surfaced: `BarBuffer.attach`'s docstring
promised a lossless subscription while one branch defaulted to drop-oldest, pinned by a test
asserting *a fake's call kwargs*; and #66's repair -- which exists because the gate spent an
occurrence Discord never saw -- reached its own fix through `getattr(..., None)`, so a gate
missing the method reverts to the defect **silently**. Removing that fallback immediately
exposed a test double that had been running the pre-repair path ever since (`4a22022`).

Three things worth carrying. **A gate checks rules; a review checks reasoning** -- #66's gate
was green and the review found the real defect. **The same scope gap hit three tickets running**
(#63, #81, #66): a test that asserts a *global* shape belongs to whoever changes that shape,
and no plan can know which tests those are from the ticket text; the fix is to make such tests
derive their expectations rather than repeat them. And **a published measurement did not reach
the file a later ticket wrote** -- the finding existed, in this repository, with a number.
`AGENTS.md` had drifted three ways at once and is corrected (`6e20870`); its suite count sat
162 tests low, so its own tripwire could not have tripped. Filed from findings: **#82** (two
recorders on separate sockets agree by conservation, not equality -- tick sums identical at
1,333,097 on both sides) and **#83** (the suite is green only when the machine is idle; 30
`time.sleep` call sites, and #50 was the same shape). A first-ever Fable audit of the whole
epic is running. Owed: the day lands 2026-09-13T05:50Z and four issues close off it.

## 2026-09-12 (third session) — the audit's findings, fixed and closed

Codex is retired as the implementation route. Two Codex workers had reached 65 and 100
sandboxed commands and were still writing red tests with the source file untouched; both were
killed, their partial diffs salvaged, and the work handed to **four Claude agents running in
parallel, one git worktree each, disjoint file territories**. All four landed. That is the
model now — see the memory note, not this file, for how to set it up.

**Ten issues closed with full comments**: #82, #83, #84, #85, #86, #87, #88, #89, #90, #91.
`main` is at `02fca06`, pushed, **1,401 passed, 0 failed, ruff clean**.

**#84 is the one that mattered.** It is #63's own "none duplicated" acceptance criterion, and
#63 shipped believing it held. `XREAD` takes a start and no end, so `_replay` handed the writer
every entry past the group's `last-delivered-id`, which the live `>` read then delivered again:
15 delivered for 10 distinct on fakeredis, 14 on real Redis, and a position index of **20
against an `entries-added` of 15** — an index larger than the stream has entries, which is what
the *next* restart's gap arithmetic is computed from. The test that let it ship ended with
`take(restarted, 10)` and asserted ten bids, never that the queue was then empty. **Drain to
empty and assert empty** is the correction, and it was the fix for both halves.

**Three different mechanisms were all being called "the suite is flaky".** Only one was #83.
The second is the trap worth remembering: pytest creates the `--basetemp` directory with
`parents=False`, so `--basetemp=X/basetemp` fails outright when `X` does not exist — **315
tests error at setup, are reported as errors rather than failures, and the run finishes
faster because they never ran**. `AGENTS.md` prescribed that flag *and* told every worker to
delete the directory as its last command, guaranteeing the next run was always a first run.
Four agents read it as load and moved on. Fixed in `02fca06`. The third is a shared test Redis
container, filed as **#92**; the remaining 28 duration-bets are **#93**.

**#82 now exits 0 on the real pair** (05:52–06:12Z, `data` against `.stack-data`): tick sums
1,333,097 both sides, `net=0`, no row outside a bound of one, tables B and D byte-exact. The
556 `right_only` rows were never a store defect. Widening the tolerance would have destroyed
the only thing the check was for.

Two more of the green-while-proving-nothing family, taking the count to **six**: a rejoin test
with **no assertion at all** (#91) — unfalsifiable because the bus deliberately isolates reader
failures — and #84's pair above. The answer this time was an **AST scan** that fails if any
test in the file has no assertion. Six in one epic says the one-at-a-time repairs are not
keeping up.

Owed: the 24-hour run lands **2026-09-13T05:50Z** and four issues close off it. One directory,
`dxp-docs/engine/.sandbox-tmp`, cannot be deleted without a UAC click — the Codex sandbox user
owns it.
