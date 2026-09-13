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
