# Silent success — a value that stopped meaning what it says

**Learned 2026-09-12**, in `delta-exchange-payoff`, from eight incidents in one day. The system it
happened in: [feed-engine](../domain/feed-engine.md).

## The shape

**Not a crash. A value that quietly stopped meaning what it says** — and left the system reporting
success. A counter that still increments. A status field that is a literal. An exception a
defensive handler swallows. A rule that silently became a special case.

**Why it survives: a defect that makes a number look worse gets investigated. One that makes it
look better gets quoted.**

## The eight

| # | What reported success | What was true |
|---|---|---|
| #103 | `/health` `ok`, `replay_gap_entries: 0`, `docker ps` healthy | `store` had stopped reading; 97 minutes trimmed unread |
| `_stream_id_seconds` | `seal_clock` returned a time | it raised on every stream id and fell through to the wall clock — **record 0010 R4 had never once executed** |
| R5 | a replay-gap counter existed | it was computed once at start-up, never while running |
| #108 | `feed` `{"status":"ok"}` | adapter stopped, budget spent, nothing published for 583 s |
| #111 | `lag 0`, `skipped: 0` | a lossless reader stranding ~30% of `md.option_bar` in the pending list — **created by #103's own fix** |
| #115 | `post_alert` returned `True` | the Discord post failed, and spent the alert's 300 s window |
| #110 | a clean restart, no log line | the open minute was gone from `computed-bars` |
| instruments | four tools reporting numbers | #100 16.4 s cadence told 5 s; #102 replayed retention into its own lag; #104 a stall scored 8× better than health; `docker stats` disk wrong by 59× |

## The five questions that found them

1. **Ask the dependency, not the process.** `XINFO GROUPS` tells you what `/health` cannot.
2. **Ask what has never executed.** `git log -S <symbol>` against the tests that claim to cover it.
3. **Ask where a denominator comes from** — the data, or the request. A stall shortens a span
   rather than holing it.
4. **Ask what a counter reads if the thing it counts never happens.** Usually zero, which reads
   the same as healthy.
5. **When an A/B comes out clean, ask what else differs between the arms.**

## What I now believe

- **A fix can carry the next defect.** #103's bounded retry was right, and it turned a loud death
  into a silent loss. Re-ask the five questions of every fix, not only of every bug.
- **Two documents agreeing proves nothing about the code.** In #103 the decision record and the
  design document agreed with each other and were both wrong. Only a check that reads the code
  can see that (#106) — and even that one caught structure, not evaluation (#117).
- **Instruments need the same suspicion as the system.** Nothing checked them; all four erred
  in the flattering direction.
- **Correct and dead can look identical.** A generation sealed with zero rows is correct when
  the venue is silent and a loss when the store is — so the alarm names it and a person judges.

## Where it is applied

- In the suite: [tests-that-prove-nothing](tests-that-prove-nothing.md) — mutate, do not read.
- In operations: [service-health](../domain/service-health.md) — what each check cannot see.
- In the code repo: `delta-exchange-payoff/docs/split-what-to-do-next.md`, "The one thing to carry forward".
