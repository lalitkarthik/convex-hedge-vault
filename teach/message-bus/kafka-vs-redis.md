# Kafka against Redis Streams, and what a migration would mean

Follows [the-three-brokers](the-three-brokers.md). Written because the senior is
considering Kafka — see [the-disk-bloat](the-disk-bloat.md) for why his stated reason is
probably the wrong one.

---

## First: pub/sub and Streams are not the same feature

Both live inside Redis and are routinely confused.

| | **pub/sub** | **Streams** |
|---|---|---|
| what it is | a live broadcast | an append-only log |
| stored? | **no** | yes, until trimmed |
| nobody listening | message **vanishes, silently** | it waits |
| listener reconnects | sees only what comes next | catches up from where it stopped |
| acknowledgements | none | yes, with a pending list |
| delivery | at-most-once | at-least-once |
| commands | `PUBLISH` / `SUBSCRIBE` | `XADD` / `XREADGROUP` / `XACK` |

Pub/sub is a radio broadcast — if the radio was off, that is that. Streams is a recording.

For a trading system pub/sub is almost always wrong: a strategy that restarts and silently
misses what happened while it was down is a bug nobody can see. **He uses Streams.**

---

## Kafka against Streams — same shape, different structure

Redis's own docs concede the shape: consumer groups are "basically what Kafka (TM) does."
So the differences are structural, not conceptual.

### 1. Where the data lives — this causes all the others

| | |
|---|---|
| **Redis Streams** | in **memory**; disk is a backup |
| **Kafka** | on **disk**; memory is a cache |

### 2. How progress is tracked — the deepest difference

**Redis tracks every message individually.** Unacknowledged entries sit in the pending list
by name, so entry 7 can be acked while 5 and 6 are outstanding.

**Kafka tracks one number** — the consumer group's **offset**. "Processed up to 4,812."

| | Redis pending list | Kafka offset |
|---|---|---|
| granularity | per message | **one number** |
| ack 7 but not 5? | yes | **no** — past it or not |
| cost when a consumer stalls | the list grows, in RAM | **nothing** — the number stops moving |
| "how far behind?" | count the pending list | subtract two numbers |

**This is why Kafka shrugs at a slow consumer and Redis does not.** Redis gives finer
per-message control; Kafka gives a consumer that can fall a day behind for free.

### 3. Partitions, and what they charge

Redis Streams: one stream, one total order.

Kafka: a topic is split into **partitions**. That buys scale and charges twice —
**ordering holds only within a partition**, and **partition count caps parallelism** (four
partitions means a fifth consumer in the group sits idle).

At his 1 message/second, partitions are pure overhead.

### 4. Retention

| | |
|---|---|
| **Redis** | `MAXLEN` (count) or `MINID` (age) — **and you must set it** |
| **Kafka** | `retention.ms` / `retention.bytes`, with a default (typically 7 days) |

Kafka also has **log compaction** — keep only the latest message per key, forever. Useful
for "current state of every contract". Redis Streams has no equivalent.

### 5. Operational cost

Redis is one process, already running. Kafka is a cluster — brokers plus coordination,
tuning and monitoring. **For a small team this is usually the deciding factor**, not any
technical row above.

### The table

| | Redis Streams | Kafka |
|---|---|---|
| lives in | memory | disk |
| progress tracked by | per-message pending list | one offset number |
| ordering | total, one stream | per partition only |
| parallelism cap | consumers per group | **partition count** |
| retention | you must set it | default ~7 days, plus compaction |
| slow consumer costs | RAM; trimming may delete unread | nothing |
| running it | one process | a cluster |
| sweet spot | < ~500k msg/s, simplicity matters | millions/s, many readers, days of history |

---

## What a migration would actually look like

| his Redis Streams | Kafka equivalent | direct? |
|---|---|---|
| a stream (`md.option_quotes`) | a **topic** | yes |
| `XADD` | **produce** | yes |
| consumer group | **consumer group** | yes |
| `XREADGROUP` | **poll** | yes |
| `XACK` | **commit offset** | per-message becomes one number |
| pending list (PEL) | *nothing* — offsets replace it | **no** |
| `XAUTOCLAIM` | **rebalancing**, done for you | **no** |
| `MAXLEN` / `MINID` | `retention.bytes` / `retention.ms` | yes |
| entry ID `<ms>-<n>` | **offset**, a plain number per partition | roughly |
| — | **partitions** | Redis has none |
| — | **log compaction** | Redis has none |

**Mostly mechanical.** Two places it is not:

1. **Acknowledgement changes shape.** Any logic that acks out of order must be redesigned.
2. **Crash recovery changes owner.** `XAUTOCLAIM` becomes Kafka's automatic rebalancing —
   less code, less control.

**And one cost that is easy to miss:** Nautilus ships Redis as its built-in backing for
external streams. Kafka means writing and maintaining that transport, or finding another
route. That is real work, and it is independent of every technical argument above.
