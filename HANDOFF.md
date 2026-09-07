# Handoff — 2026-09-07

Vault session. All work landed in [teach/message-bus/](teach/message-bus/plan.md) and
[learning-records/message-buses.md](learning-records/message-buses.md). A second agent is
working in `delta-exchange-payoff` on the volatility screens — **stay out of `engine/src`
and `web/` there unless told otherwise.**

## Start here

Settle the one open measurement. The engine is up, so this takes ten minutes:

```bash
cd "D:/Convex Hedge/delta-exchange-payoff/engine" && ./.venv/Scripts/python.exe -c "import time,sys; sys.path.insert(0,'src')"
```

`stream.py` records that a full `recompute_dirty()` pass over every listed expiry is
"~10 ms". `measured` this session on the 69-row fixture: **7.25 ms for ONE expiry**, and
**eight are listed live**. 8 × 7 ms ≈ 56 ms against a 100 ms tick would be over half a core,
not the ~10% the comment implies. The fixture may not be representative — that is why it is
tagged `assumed` in [caching.md](teach/message-bus/caching.md) rather than claimed.

Measure it against the running engine. It either closes the flag or finds a live problem.

## In flight

- **Both servers are running.** Engine PID **25748** on 8000 (`/health` returns ok, eight
  expiries listed); web on 3000 via `bun run dev`, HTTP 200. Started this session at ~09:45Z.
- **`tools/measure_bus.py` is untracked** in `delta-exchange-payoff`. It is the spike from
  this session and it is reproducible; commit it there or delete it, but do not leave it
  drifting.
- **Nothing half-built in the vault.** Working tree clean, `master`, pushed.

## What changed this session

Five commits, all pushed to `master`:

| | |
|---|---|
| `6350113` | Pass 1 — our architecture, his, and Nautilus's own |
| `e5969b3` | The spike — 798x, and the silent loss reproduced |
| `03c273d` | Pass 3 — the cache cannot be stale; the gap is durability |
| `f55f857` | The senior's answers, and the correction they force |
| `df91ff5` | The learning record |
| `7474869` | Kafka against Redis Streams, and the migration mapping |

Also: five teaching sessions delivered, each closed by a check question answered unaided.
`teach/` and `learning-records/` were both empty before this session.

## Decisions made

- **No broker while we are one process; Redis alone if we ever split** —
  [plan.md](teach/message-bus/plan.md), "Where the answer stands".
- **The senior's Redis was chosen, not inherited from Nautilus** — corrects pass 1's
  inference. [what-the-senior-said.md](teach/message-bus/what-the-senior-said.md) §4.
- **His disk problem is probably not Redis** and Kafka would likely worsen it —
  [the-disk-bloat.md](teach/message-bus/the-disk-bloat.md), with a five-step diagnosis.
- **We need no caching we do not already have; the real gap is durability** —
  [caching.md](teach/message-bus/caching.md).

## Open questions

- **The recompute discrepancy above.** `assumed` until measured live.
- **Session 4 has no video.** None found that was any good; taught cold instead. If a good
  one turns up, [sessions.md](teach/message-bus/sessions.md) should carry it.
- **The disk diagnosis is the senior's to run**, not ours — steps 1 and 2 of
  [the-disk-bloat.md](teach/message-bus/the-disk-bloat.md) take one minute and settle it.
- **The store has a three-day hole**, 2026-09-04 09:38Z to 2026-09-07 ~09:45Z. Not
  recoverable. 782,870 quote-bar rows on disk now.

## Traps found

- **This machine's two clocks disagree by three days.** WSL `date` said 2026-09-04 while
  Windows said 2026-09-07. Vault notes were stamped wrong and corrected. **Trust
  `Get-Date`, not `date`.**
- **I stated a number I had never measured.** Claimed a flush costs "hundreds of
  milliseconds" and derived a backlog from it; `measured` 37.7 ms for all four tables —
  wrong by five times, in the alarming direction. Recorded in
  [the-three-brokers.md](teach/message-bus/the-three-brokers.md) rather than quietly fixed.
- **I told the user the flush was still hourly and uncommitted. It is not.** The other agent
  landed #16; `store.py:135` reads `FLUSH_SECONDS = 300.0` and the running engine is
  verifiably writing every five minutes (files at 15:22, 15:27, 15:32, 15:37, 15:42 local).
  **Re-read state before reporting it; do not carry the morning's picture into the evening.**
- **A `FanOut` throughput test hung forever** because it awaited 20,000 items from a
  drop-oldest queue capped at 1,000. Fixed by making both subscriptions lossless — the test
  measures transport, not policy.
- **Docker's daemon must be started by the human.** Redis for the spike:
  `docker run -d --name X -p 6399:6379 redis:7-alpine`. Remove the container afterwards.

## Read these

1. [teach/message-bus/plan.md](teach/message-bus/plan.md) — the map. Everything else hangs off it.
2. [learning-records/message-buses.md](learning-records/message-buses.md) — the durable answer, if you only read one.
3. [teach/message-bus/what-the-senior-said.md](teach/message-bus/what-the-senior-said.md) — what is now `stated` rather than `assumed`.
4. [teach/message-bus/the-disk-bloat.md](teach/message-bus/the-disk-bloat.md) — the only live problem, and it is his.
5. `handoff-delta-exchange-payoff-2026-09-03-evening.md` in `%TEMP%` — its **"How he engages"** section still governs. Unchanged and still the most important thing in any of these files.
