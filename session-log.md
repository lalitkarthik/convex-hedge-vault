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

Split the same way when this file next outgrows the bound: the closed period moves to its own
file, the live entries stay here.

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
