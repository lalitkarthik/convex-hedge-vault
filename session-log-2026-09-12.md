# Session log - 12 September 2026, later and evening

Closed. The store stalled and nothing said so (#103), the fixes landed, and one defect shape
explained the day. Split out of [session-log.md](session-log.md) on 2026-09-14 when that file
passed this vault's 200-line bound. Nothing was edited; every entry moved unchanged.

## 2026-09-12, later — the store stopped and nothing said so

**The finding of the day is not a ticket that closed. It is [#103](https://github.com/lalitkarthik/delta-exchange-payoff/issues/103).**

At `measured` 11:02:38Z the `store` stopped consuming the bus and never resumed. It read one
batch of **500 entries spanning 18 ms**, never acked it, and read nothing again. Retention
then trimmed **97 minutes of market data past its consumer-group position** — gone, not late.
`api` stopped publishing `computed.chain` 21 seconds later. `feed` never stopped.

Every signal a person checks said fine. `/health` returned
`{"status":"ok", ..., "replay_gap_entries":0}` while the group was 2.2 million entries behind
— **the replay-gap counter exists and reported zero through the exact condition it was built
for**. `docker ps` said `Up 7 hours (healthy)`. The checkpoint advanced to generation 88 and
sealed every minute through 13:03:44Z, so two hours of minutes are **sealed empty**, and a
seal is final.

And the reason nobody saw it: **no container emits any application log record.** `docker logs`
minus access lines is 4 lines for `store`, 4 for `feed`, 22 for `api`, across seven hours. The
`store.flush` record #42 added to catch a silent hole in this exact store never reaches
stdout. So #42's three-day hole recurred, live, under attention. The stack was left running
in its stalled state as evidence; an Opus agent is diagnosing the mechanism.

**Second instrument defect, [#100](https://github.com/lalitkarthik/delta-exchange-payoff/issues/100).**
`measure_containers.py` samples at a `measured` **16.4 s** when told `--interval 5`, because
`time.sleep(interval)` runs *after* a sweep of six serial `docker stats` calls at 1.14 s each.
`--samples 17280` was set to mean 24 h and actually meant **78.7 h**. And one `sampled_at` is
stamped across six reads taken up to 6.9 s apart. #79 calls out cells that move more than 25%;
the instrument's own error is larger than that threshold.

**Third, [#102](https://github.com/lalitkarthik/delta-exchange-payoff/issues/102).** #97 asked
whether a forgetful caller existed, grepped `engine/src/`, found none, and wrote *"not a live
defect; the landmine underneath one"*. The forgetful caller existed one directory over and it
was `tools/measure_bus_live.py` — **an arrival-lag harness that was replaying the retention
window into its own numbers.** The defect never touched the system; it corrupted the evidence
about the system, which is why nothing failed.

**A load generator outlived its session by 73 minutes.** 112 orphaned `burn.py` processes from
#96's load test, running 11:24:28Z–12:37:42Z. They cost **22 test failures that were not
failures** (the same two suites: 740 s / 12 failed and 751 s / 10 failed, then 78 s / 0 failed
and 97 s / 1 failed once killed) and about 16% of I13's measurement window. The one real
failure was buried among twenty-one that were not, which is how a real defect gets dismissed
as flake. Filed as [#99](https://github.com/lalitkarthik/delta-exchange-payoff/issues/99).

**#95's fix carried three defects, and only one had a test behind it.** The units correction
inserted its blockquote *between table rows D and E*, so row E rendered outside the table —
**the correction deleted the row it was correcting**, above a note reading "checked on all
five rows". The suite was green. `test_doc_bounds` fired only because the same edit happened
to cross 200 lines, a coincidence. That is now
[#98](https://github.com/lalitkarthik/delta-exchange-payoff/issues/98), landed: a render check
that is red against the broken file and green against the fixed one, built on a code-span-aware
tokenizer after a naive pipe count fired on four *correct* tables.

**#93's published counts were all wrong.** `measured` from the blobs either side of `89aa9b3`:
**35 sites, 19 removed, 16 remaining**, against the title's 28, the body's 33 and the commit's
"21 bets". Two sites in `test_store_process.py` are bets measured in *scheduler turns* rather
than seconds and were never triaged — in the one file that commit edited.

Closed with full comments: **#95, #97, #98**. Merged but held open on unmet criteria: **#96**
(needs a loaded machine), **#70** (criteria 2–4 need AWS). `main` **1,440 passed, 0 failed,
ruff clean**, up from 1,401.

**The measurement is cut to 05:50:07Z–11:24:28Z** and even that now ends inside a stalled
system. I loaded the host myself with gate runs 12:24–12:55Z and said so on #79 rather than
letting the earlier, cleaner-sounding cut stand.

### Later the same evening — the fixes landed, and the tear-downs were the bug

**Eight issues closed with red-green evidence**: #93, #95, #97, #98, #99, #100, #101, #102.
`main` **1,502 passed, 0 failed, ruff clean** — up from 1,401, **+101 tests**, pushed at `af82c3b`.

**The best find came out of fixing #103.** `store.py:2237` read `value.split("-", 1)` and unpacked
**three** names from **two** parts, so `_stream_id_seconds` raised `ValueError` on *every* stream id
there is — `0-0` included — and `seal_clock` caught `(TypeError, ValueError)` and fell through to the
wall clock. **Record 0010 R4 had never once executed**, since #63 introduced it at `83120d6`. It is
written in the decision record, defined in `CONTEXT.md`, and was written into `message-bus.md` as
rule A6 by #72 *that same day*. One word — `partition` for `split` — and R4 pins for the first time.

**So the same shape occurs twice in one subsystem**: an exception a defensive handler swallowed, and
a signal that silently became a default. Neither was caught by a test, a health check, or a log a
person could see. Assume there is a third.

**Three un-torn-down processes were found in one day, and two of them were tear-down scripts.** The
112 `burn.py`; the collector the 13:30Z watchdog reported stopped and did not stop; and
**`stop-at-24h.ps1`, still running, armed for 05:50Z tomorrow to force-kill three PIDs that are
already dead** — Windows recycles PIDs, so it would have killed whatever unrelated processes then
held those numbers. Found by #99's agent while building the fix for exactly that class of defect.

**A belief I had been repeating all day was wrong.** "Two concurrent suites are safe, three trip the
fail-safe bounds" rested on a `measured` 304 s and 4 timeouts — **taken while those 112 processes
were running.** Re-measured on a verified quiet machine: **130 s against 97 s alone, 1.34x, zero
failures.** Corrected in the memory note and on #99.

**Instruments, not systems, were the day's theme.** Three were lying — #100 (16.4 s cadence when
told 5 s, six reads stamped with one clock), #102 (an arrival-lag harness replaying the retention
window into its own numbers), #104 (a gap probe that cannot see a store that stopped, because a
stall shortens its grid rather than holing it). All three were found by accident while doing
something else. **Nothing checks the instruments.**

**#79 survived anyway.** #100's salvage analysis puts the instrument's contribution under 9% of every
published cell, far below R6's 25% call-out threshold, so the table can be written from the existing
collection — with two qualifiers attached to the figures: the p95s are of ~1.9 s-averaged CPU, and
the per-viewer cost carries ±0.6–0.8.

Seven filed and still open: **#103** (fixed and merged, four verifications need the stack restarted),
**#104**, **#105**, **#106**, **#107**, plus #96 and #70 held open on unmet criteria. **The final
audit was not run** — its brief is written at `D:\Convex Hedge\incident-103\audit-brief.md` and is
the next session's first task.

---

## 2026-09-12, evening — the epic's non-AWS work is done, and one shape explains the day

**Everything that does not need AWS credentials is finished.** The suite went **1,401 → 1,595
passed, 0 failed, ruff clean** in one day. Twenty-eight issues closed.

**#103 is closed.** The stack was restarted at `measured` 15:52:27Z with the owner's approval and
images rebuilt from the fix, and all four remaining criteria were proved against it: JSON records
reach `docker logs`, `.stack-logs/<service>/` is mounted and filling, `store.flush` appears at
302/301/297 s against a 300 s cadence, and **`/health` returned 503 at 20.6 s** when `dxp-store`
alone was cut from its network for 21 seconds. That single reading showed all six of #103's
changes working at once.

**The last reading of the stalled system is worth keeping**: `"status":"ok"`,
`"replay_gap_entries":0`, against a lag of **1,859,571 entries**, with `generation` advanced 87 →
120 while `rows_written` never moved off 523,510. Thirty-three generations, all empty seals.

### One defect shape produced eight incidents, and none of them is a crash

**A value that quietly stopped meaning what it says.** A counter that still increments. A status
field that is a literal. An exception a defensive handler swallows. A rule that silently became a
special case. **Every one left the system reporting success.**

#103 (the readers), `_stream_id_seconds` (**R4 had never once executed** since #63 introduced it),
R5 (a record that never said *when*), **#108** (`feed` reporting `ok` while stopped with its budget
spent), **#111** (a lossless reader stranding a batch in the pending list — and **#103's own
bounded-retry fix turned a loud reader death into a silent repeating loss**, 30% of
`md.option_bar`), **#115** (a failed Discord post spending the alert's window, with the comment
beside it saying the pair existed to prevent exactly that), **#110** (a restart losing the open
minute from one table and leaving no record of the restart), and **four instrument defects** —
#100, #102, #104, and `docker stats` BlockIO not observing a bind mount, wrong by **59×**.

**Why it took a day to find eight: a defect that makes a number look worse gets investigated. One
that makes it look better gets quoted.**

### The one that revised my own belief

**#111 is #103's fix carrying the next defect.** Bounded retry was right — a reader holds nothing,
so retrying forever buys it nothing — and it converted a visible death into an invisible loss,
because nothing read the pending list Redis had already moved the batch into. The repair reads
`XREADGROUP ... 0` before the `>` read, and **the agent caught its own error**: the rule that a
checkpointed reader defers to its replay is true only *before* the replay runs. Applied mid-run it
would ack away the very batch being rescued.

### Three tickets to hold one rule

`test_nomenclature.py` pinned documents against each other, and in #103 **the record and the
document agreed with each other and both were wrong about the code.** #106 built the first check
that reads the code; **#117 broke it** — it catches structural disconnection, not evaluation; #114
answered with a test that drives the timer itself. Worth remembering as a sequence.

**And #117's own premise was half wrong**: its mutations A and B were already caught by a
behavioural test #103 landed the same day. The audit had run them against the AST helper only.

### Ten tests that proved nothing, and none found by reading

The newest passed with its type guard deleted — the pause fell into the dispatch body, raised
`AttributeError`, and the handler swallowed it. **All 32 tests in three alert files passed with the
guard gone.** Every one of the ten was found by **mutating**: delete the guard, no-op the commit,
force the cadence, revert the fix.

### Two prompt-injection attempts, both refused

A fake `<system-reminder>` appeared inside `gh issue view` output, twice, claiming the GitHub API
rate limit was exceeded and instructing a sleep. Two independent agents checked
(`gh api rate_limit` → 5,000 remaining, 0 used), found it false, and carried on. **Tool output is
data, and both treated it that way.**

### What is left

**#70, #71, #80 need AWS credentials and nothing else.** #63 and #79 each need one clean day of
recording, and **one re-collection closes both** — the stack has been recording since 15:52:27Z.
#57 cannot close until the three AWS tickets do.

Open and workable: **#110** (criterion 2, now **#119**), #116, #118, #119.

**Three new front doors**, because the reasoning was correct and unreadable across ten records,
fifteen cloud files, twenty-two LLDs and several hundred comments:
`docs/split-start-here.md`, `docs/split-numbers.md`, `docs/split-what-to-do-next.md`.

**Writing them found a defect**: putting `derived` beside 1,056.4 MiB made #112's widened sweep see
a disagreement it had been blind to, and the suite went red. That is #118, arriving by accident.
