# What the senior said — answers, decoded

Asked and answered 2026-09-07. Questions from [questions-for-the-senior](questions-for-the-senior.md).
This replaces `assumed` with `stated` throughout the workspace.

---

## 1. How many programs do you start?

> "Feed, redis, execution, strategies and trading terminal. In this redis and trading
> terminal are done independently. The rest are started with a single script."

**Five components, and they are separate programs.** One script launches three of them;
Redis runs on its own (a container), and the trading terminal is IBKR TWS, a desktop
application he starts by hand.

**A script that launches three programs is still three programs.** Being started together
says nothing about running together — they have separate memory and cannot share a queue.

**So his Redis is load-bearing, not decoration.** Pass 1's first branch is settled: his
design is the sound one, and the pattern is worth copying when we split.

## 2. Streams or pub/sub?

> "Redis streams (which is persistent)"

**Streams.** So everything in [the-three-brokers](the-three-brokers.md) applies to his
system: an append-only log, consumer groups, a pending list, acknowledgements, replay.

One care point on the word *persistent*: a Stream is durable **against a reader being
absent**, which pub/sub is not. Durability **against Redis dying** is a separate setting —
which is what question 3 was really asking, and he answered it separately and correctly.

## 3. If Redis dies right after a fill, do you still have it?

> "There are redis volumes linked to it. If the redis dies we have fills taken from IBKR to
> retrace it."

**Two layers, and the second is the one that matters.**

- **Docker volumes** — storage that outlives the container, so a container restart does not
  wipe the data.
- **Reconciliation from IBKR** — he re-reads fills from the broker to rebuild the truth.

**The second is the real answer, and it is the right one.** The broker is the source of
truth about what was traded; Redis is a copy. A system that can rebuild its state from the
venue does not depend on its message bus being durable. That is what `recon` on his diagram
meant, and it is a stronger design than any persistence setting.

## 4. Was Redis chosen, or did it come with Nautilus?

> "I had used redis before. Nautilus was used for event driven architecture style and the
> protocols or standards used in it"

**We were wrong, and this is the correction.** [architectures](architectures.md) inferred
that Redis probably arrived with Nautilus, because Nautilus ships Redis as its built-in
backing for external streams. That inference was reasonable and it was **not what
happened**.

**Two independent choices:**

| choice | reason |
|---|---|
| **Redis** | prior experience with it |
| **Nautilus** | its event-driven architecture style, and the conventions it brings |

The Nautilus finding still stands as a fact about Nautilus — its internal bus is
in-process, Redis backs only external streams. It was simply the wrong explanation for
*his* choice.

**Worth noting what he did not say:** he did not say he compared Redis against Kafka. He
reached for what he knew. That is an ordinary and defensible way to choose, and it means
there is still no Redis-versus-Kafka comparison behind this architecture.

## 5. Backtesting — Redis or files?

> "Not from redis but from stored files"

**Confirms [caching](caching.md).** A backtest reads files; it never touches a bus. Our
Parquet store already is that source, and backtesting leaves the bus question entirely.

---

## What he added, unprompted — the two most useful parts

### Why the bus exists at all

> "Its better for a microservice architecture with Message Bus and event driven
> architecture because we can add multiple strategies without affecting the current one."

**That is the reason, stated plainly: independent deployability.** Adding a fourth strategy
must not require touching, retesting or restarting the first three. A bus buys that, because
a new subscriber costs the publisher nothing.

It is worth being precise that this is an argument about **change**, not about speed. A bus
does not make the system faster — [the-spike](the-spike.md) measured it 798x slower per
message. It makes the system *safe to change in pieces*.

### The gap he named himself

> "But still there is a small coupling in the architecture as the state variables in each
> process dies with a process restart or crash (which has to be made persistent going
> forward)."

**This is the same gap [caching](caching.md) found in our system, in his.** In-memory state
dies with the process. He has identified it and has not fixed it yet.

Two things follow. It is not a defect unique to either system — it is what "in-memory"
means. And **his fix and ours are different sizes**: he has several processes whose state
must be shared and restored, which is genuinely Redis-shaped work; we have one process whose
only unrecoverable state is a buffer, which a shorter flush interval fixes.

---

## The one thing to push back on

> "I am also looking for alternative to redis streams like kafka as there is a disk bloating
> issue with redis in docker desktop which we need to clean manually daily or thrice a week."

**Changing broker is unlikely to fix this, and may make it worse.** See
[the-disk-bloat](the-disk-bloat.md) — diagnose before switching.
