# Message buses, caching, and what our architecture actually is

**Learned 2026-09-07.** Workspace and evidence: [teach/message-bus/](../teach/message-bus/plan.md).
Taught in five sessions built from the senior's own answers, each closed by answering a
check question unaided.

---

## The one idea everything hangs off

**A message bus exists to cross the wall between separate processes. Nothing else.**

Two processes on the same laptop cannot share memory — the hardware forbids it. So data
between them must be turned into bytes, sent through something both can reach, and rebuilt.
That "something" is the bus.

Consequences that follow directly:

- **"One program" is not "one process."** A program can spawn children; a script can launch
  three programs. Being started together says nothing about running together.
- **Separate machines are not the point.** The wall is between processes, not computers.
- **Topics are labels on messages, not architecture.** We already use them — `ob_l2` and
  `ticker` are Delta's topic names — with no broker anywhere.

## What a bus actually buys, stated correctly

**Change-safety, not speed.** `measured`: a Redis Streams round trip is **798x** our
in-process hand-off (1,436 µs against 1.8 µs).

The senior pays that knowingly, for **independent deployability** — adding a fourth strategy
without touching, retesting or restarting the first three. Direct calls fail three ways: the
caller must know every recipient, one slow consumer stalls the rest, and crashes spread.
Publishing to a topic removes all three.

**Event-driven is a pattern; a broker is a product.** We have the pattern without the
product — our fan-out already decouples its consumers. So "decoupling" was never a reason to
add Redis; we had it already.

## Ours, and why it needs no broker

One process: websocket reader → in-memory fan-out → two consumers (live chain screen, and
the one-minute bar writer). Everything is `asyncio` on one thread, so parts take turns
rather than running together — which is why the disk write is exiled to a worker thread.

`measured`: ~1,323 frames/second — **one every 0.76 ms**, because `ob_l2` refreshes every
508 ms **per contract** and 688 are listed. Not "every 500 ms"; that factor of 688 is the
single most-misread number in the project.

**Adding a broker today would pay a toll to cross a wall we do not have.**

## The three brokers, in one line each

| | shape | when read |
|---|---|---|
| **RabbitMQ** | a queue — a post office | delivered, acked, **gone** |
| **Kafka** | a durable log — an archive | kept until retention expires |
| **Redis Streams** | the same log, in memory | kept until **trimmed** |

Redis's own docs: consumer groups are "basically what Kafka (TM) does."

**The axis that actually matters is what happens when a consumer falls behind**, because
that is a correctness question, not a performance one. `measured`, 10,000 published into
capacity 1,000: our lossy policy dropped 9,000 and **counted every one**; our lossless
policy held all 10,000 and counted the over-capacity offers; a Redis stream at `MAXLEN 1000`
trimmed 9,000 away **with nothing recording that it had**.

## Redis Streams — the mechanics, and the trap

- Append-only log; IDs are `<millisecond>-<counter>` and only increase.
- **Reading does not delete.** That is what separates a log from a queue.
- **Different consumer groups each receive everything; consumers inside one group split the
  work.** Same commands — the group name decides which behaviour you get.
- Unacknowledged entries sit in a **pending list** and are redelivered after a crash.
- **`XACK` frees no memory.** It means "*my group* is finished", and it cannot mean delete,
  because another group may not have read the entry yet. **Only `XTRIM` deletes** —
  `MAXLEN ~ N` by count or `MINID ~ <id>` by age.

**"Persistent" and "kept" are different words.** Streams are durable against a *reader*
being absent; durability against *Redis* dying is a separate disk setting.

## State: sort it by how you would get it back

| kind | example | fix |
|---|---|---|
| refills itself | latest quote per contract | none — a new one lands in 508 ms |
| recomputable | our IV and Greeks | none — `measured` 6 ms to rebuild |
| **unrecoverable** | our unflushed bars; his strategies' working state | **must be written somewhere** |

**Only the third row is a problem**, and this is what makes the whole question tractable.

**Reconciliation beats persistence.** The senior's best answer was that fills are recovered
from IBKR, not from Redis. The venue is the authority; a copy being lost is survivable.
Persistence protects against losing data, reconciliation against data being *wrong* — the
failure that costs money and cannot be seen by looking.

**Ask of anything that matters: who is the authority on this fact? If it is not you, you can
rebuild.**

## Caching: ours is right, for a better reason than most

`measured`: building a chain 5.383 ms, solving IV **and all five Greeks** 0.719 ms, a cache
hit 0.0004 ms against a 6.073 ms miss — worth ~15,000x per read. **Assembling the chain
costs seven times the mathematics**, which is the opposite of the intuition.

**The design worth copying: invalidation by arrival, not by time.** A frame marks its expiry
dirty and a read of a dirty key recomputes before answering, so **the cache cannot serve a
stale answer** — not "rarely does", cannot. A TTL buys a window in which the cache is
knowingly wrong; on a price screen that window is the bug.

## The standing decision

**No broker while we are one process. If we ever split: Redis alone, not Kafka, not both.**
Kafka's strengths — millions of messages a second, days of retention for many independent
readers — do not bite at 1,323/s with two readers and Parquet holding history. Revisit only
when several readers need the same stream over days, or Redis measurably cannot keep up.

**Our real gap is durability, not caching**, and its cheapest fix is flushing every five
minutes rather than hourly — one constant, not a dependency.

## Two things I got wrong, recorded because the pattern is the point

1. **I inferred the senior's Redis came bundled with Nautilus.** Reasonable — Nautilus does
   ship it — and wrong. He chose Redis from prior experience and Nautilus for its
   event-driven style. Two independent decisions.
2. **I asserted a flush costs "hundreds of milliseconds" and derived a backlog from it.**
   `measured`: 37.7 ms for all four tables. Wrong by five times, in the alarming direction.

Both are the project's standing pattern — *every source gives a good design and a bad
number* — and the second one was caught only because the number was questioned.
