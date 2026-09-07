# Five sessions, in order

Built after the senior's answers ([what-the-senior-said](what-the-senior-said.md)) because
every one of them landed on a concept that had not been taught yet.

**How to use this.** One session at a time. Watch the videos first, then read the note, then
answer the check question out loud without looking. If the check question is hard, the
session is not finished — say so and it gets re-taught rather than moved past.

**On the videos.** Each was found by search and matched on topic; none has been watched
end to end. If one is bad, say so and it gets replaced.

---

## Session 1 — Programs, and why he starts five things

**His answer this explains:** *"Feed, redis, execution, strategies and trading terminal…
the rest are started with a single script."*

**Concepts:** program vs process · process vs thread · why separate memory forces a
messenger · a script launching three programs is still three programs.

**Watch**
- [Process vs Thread — ByteByteGo](https://www.youtube.com/watch?v=4rLW7zg21gI) (~5 min) —
  the clearest statement of why one process cannot touch another's memory.
- [Processes vs Threads in 90 seconds](https://www.youtube.com/watch?v=7yjKlebrECQ) — the
  house-and-roommates picture, if the first is too fast.

**Then read:** [vocabulary](vocabulary.md), "Three levels, not two".

**Check:** his five components run on one laptop. Why do they still need Redis to talk?

---

## Session 2 — Event-driven architecture, and why a bus exists

**His answer this explains:** *"better for a microservice architecture … we can add multiple
strategies without affecting the current one."*

**Concepts:** request/response vs event-driven · publisher, broker, consumer · fan-out ·
loose coupling · **independent deployability — the actual reason** · eventual consistency ·
at-least-once and why consumers must be idempotent.

**Watch**
- [Event-Driven Architecture in 7 minutes — Alex Hyett](https://www.youtube.com/watch?v=gOuAqRaDdHA)
  — the closest match to his exact argument, including the drawbacks.
- [Pub/Sub from scratch — one event, five systems](https://www.youtube.com/watch?v=8rrNvaWTn9c)
  (~3 min) — why adding a consumer costs the producer nothing. This *is* his "add a strategy
  without affecting the others".
- [Messaging & Event Streaming: queues, streams, pub/sub](https://www.youtube.com/watch?v=KSmXNaUtPp4)
  — the fullest single explanation of the three shapes.

**Then read:** [architectures](architectures.md), "The senior's".

**Check:** a bus made his system 798x slower per message. Why is it still the right call
for him and the wrong one for us?

---

## Session 3 — Redis Streams, specifically

**His answer this explains:** *"Redis streams (which is persistent)."*

**Concepts:** append-only log · entry IDs · `XADD` / `XREAD` / `XREADGROUP` · consumer
groups · the Pending Entries List · `XACK` · `XCLAIM` / `XAUTOCLAIM` · trimming with
`MAXLEN ~` and `MINID` · **why `XACK` does not free memory**.

**Watch**
- [Pub-Sub vs Message Queue vs Broker](https://www.youtube.com/watch?v=Fki3eW4eevs) — sorts
  the three layers people mix up: pattern, product, guarantee.
- [Understanding Redis Streams](https://www.youtube.com/watch?v=rBlnHJZKD_M) — on topic;
  quality unverified.

**Then read:** [the-three-brokers](the-three-brokers.md), then
[the-spike](the-spike.md). Redis's own Streams page is the authority and is worth the hour.

**Check:** a consumer reads an entry and acknowledges it. Is the entry gone from Redis?

---

## Session 4 — State, restarts, and what actually dies

**His answer this explains:** *"redis volumes … fills taken from IBKR to retrace it"* and
*"state variables in each process die with a process restart."*

**Concepts:** in-memory state vs persisted state · Docker volumes · RDB snapshots vs AOF ·
`appendfsync` (`always` / `everysec` / `no`) · **reconciliation — rebuilding truth from the
venue** · why the broker, not the bus, is the source of truth about a fill.

**Watch:** no single good video was found for this one. The material is
Redis's own persistence page, which is unusually readable, plus the eventual-consistency
section of the Alex Hyett video from session 2.

**Then read:** [caching](caching.md), then [what-the-senior-said](what-the-senior-said.md) §3.

**Check:** his Redis dies and loses everything. Which of his data is actually gone forever,
and which can he rebuild — and from where?

---

## Session 5 — The disk problem, and whether Kafka fixes it

**His answer this explains:** *"disk bloating issue with redis in docker desktop which we
need to clean manually daily or thrice a week."*

**Concepts:** unbounded streams · AOF growth · **dynamically expanding virtual disks that
never shrink** · `fstrim` then compact · Kafka's retention model and why it writes *more*
to disk.

**Read rather than watch** — this one is documented in issue threads, which are better than
any video on it:
- [Reclaiming disk space from WSL2 and Docker Desktop](https://erfi.dev/guides/wsl2-disk-reclaim/)
  — why deleting inside the guest does not shrink the host file, and the trim-then-compact order.
- [docker/desktop#375](https://github.com/docker/desktop/issues/375) — a real Docker Desktop
  leak, 7.5–25 GB of stale ISO blobs, invisible to `docker system prune`.
- [WSL#4699](https://github.com/microsoft/WSL/issues/4699) — the original "WSL2 should
  release disk space" thread.

**Then read:** [the-disk-bloat](the-disk-bloat.md), which carries the five-step diagnosis.

**Check:** he switches to Kafka tomorrow, in the same Docker Desktop. Does the disk problem
go away?

---

## After the five

The remaining open work is ours, not his: re-measure the recompute pass against the live
engine ([caching](caching.md)), and decide whether the five-minute flush lands. Neither
needs any more theory.
