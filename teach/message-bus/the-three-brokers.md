# Pass 2 — Redis, RabbitMQ and Kafka, compared

Terms in [vocabulary](vocabulary.md). Why the comparison is shaped this way: [architectures](architectures.md).

Every claim here is from the project's own documentation, read 2026-09-07. No blog
comparisons — the standing pattern is that **every source gives a good design and a bad
number**, and that genre is nothing but numbers, none of them from our workload.

---

## The one question that splits them

**When a message has been read, what happens to it?**

That single question produces three different products.

| | picture | when a message is read |
|---|---|---|
| **RabbitMQ** | a post office | delivered to one recipient, signed for, **gone** |
| **Kafka** | a newspaper archive | stays on the shelf until its retention expires |
| **Redis Streams** | the same archive, on a whiteboard | stays, until trimmed away — and the board is finite |

## What each one says about itself

**RabbitMQ.** A positive acknowledgement instructs RabbitMQ "to record a message as
delivered and can be discarded." Unacked deliveries are "automatically requeued when the
channel (or connection) on which the delivery happened is closed", so consumers "must be
prepared to handle redeliveries" — **at-least-once**.

Its brake is `prefetch`: it "defines the max number of unacknowledged deliveries that are
permitted on a channel. When the number reaches the configured count, RabbitMQ will stop
delivering more messages on the channel until at least one of the outstanding ones is
acknowledged." Recommended 100–300.

**Kafka.** "Events are not deleted after consumption. Instead, you define for how long
Kafka should retain your events through a per-topic configuration setting, after which old
events will be discarded." Events "can be read as often as needed".

A topic "is spread over a number of buckets" — partitions. Ordering holds **within** a
partition: "any consumer of a given topic-partition will always read that partition's
events in exactly the same order as they were written." Across partitions there is no
global order. Events with the same key land in the same partition, which is how key-level
ordering is bought.

**Redis Streams.** "An append-only log", entries keyed `<millisecondsTime>-<sequence>`,
strictly increasing. Consumer groups exist and Redis says plainly what they are:
"This is basically what Kafka (TM) does with consumer groups." Unacknowledged entries sit
in a **Pending Entries List** until `XACK`; `XCLAIM` / `XAUTOCLAIM` recover a dead
consumer's work — **at-least-once**, same as RabbitMQ.

Size is capped by trimming: `MAXLEN` on `XADD`, or `XTRIM`, exact or approximate (`~`).
Nautilus's default is `autotrim_mins: 30` — half an hour of history.

---

## The comparison, one row per axis

| axis | RabbitMQ | Kafka | Redis Streams |
|---|---|---|---|
| **shape** | queue | durable partitioned log on disk | append-only log in memory |
| **read destroys?** | yes, on ack | no | no |
| **delivery** | at-least-once | at-least-once | at-least-once |
| **ordering** | per queue | per partition only | per stream |
| **replay** | no — it's gone | yes, to the retention limit | yes, to the trim limit |
| **fan-out model** | exchanges route to queues | partitions; consumer groups | consumer groups |
| **parallelism cap** | consumers per queue | **partition count** | consumers per group |
| **when a consumer lags** | broker **stops sending** (prefetch) | lag grows; data safe on disk | entries pile up in RAM; **trimming can delete what was never read** |
| **lives where** | its own broker process | its own cluster (+ coordination) | inside Redis |
| **best at** | "this work must get done, once" | "keep the history, everyone reads it" | "fast, recent, in-memory" |
| **bad at** | replay, and re-reading history | per-message routing; small deployments | anything that must outlive the trim window |
| **latency at 1 Hz** | to be measured | to be measured | to be measured |
| **latency at ~1,323/s** | to be measured | to be measured | to be measured |

---

## Falling behind — and the number I asserted before measuring it

**First, the rate, because it is routinely misread.** `ob_l2` refreshes every 508 ms **per
contract**, and 688 contracts are listed. A departure board with 688 staggered rows:

> 688 × ~2/s = ~1,376/s, `measured` at ~1,323/s — **one frame every 0.76 ms**

Not one every 500 ms. That factor of 688 is the whole difference.

**Second, the disk. An earlier draft of this note said a flush costs "hundreds of
milliseconds" and derived ~260 backlogged frames from it. That input was `assumed`, never
measured, and it was wrong by about five times.** Measured on this machine, 2026-09-07,
minimum of five runs, rewriting the real hourly files:

| table | rows | size | write |
|---|---|---|---|
| quote-bars | 41,280 | 1.14 MB | 12.9 ms |
| reference-bars | 41,280 | 3.72 MB | 12.8 ms |
| computed-bars | 33,488 | 1.19 MB | 8.0 ms |
| spot-bars | 60 | — | 3.9 ms |
| **all four** | | | **37.7 ms** |

At 577,920 rows — 14x a real hourly file — the quote-bars write is still only 54.0 ms, so
it scales better than linearly.

> 37.7 ms ÷ 0.76 ms = **~50 frames arrive during a full flush** (`derived`)

**So disk is not our bottleneck**, and the flush runs on a worker thread rather than the
event loop anyway. The lossless policy is still right, but as *insurance* — against a load
spike, a slower disk elsewhere, or a future consumer that genuinely is slow — not because
every flush guarantees a backlog.

**The reason insurance is worth buying is that the backlog would be deepest at exactly the
wrong moment.** Message rate is not constant —
when the underlying moves hard every contract reprices at once. So the queue is longest
precisely when price is moving fastest, which is precisely when the minute's high and low
occur, which is precisely what the bars exist to record. Discarding a backlog therefore
does not lose random data; it loses the extremes, systematically, and the output file looks
entirely normal.

Hence the two policies already in `fanout.py`:

| consumer | falls behind | policy | why |
|---|---|---|---|
| `ChainStream` (screen) | rarely, briefly | **drop oldest** | a four-second-old price is worthless, not slightly worse |
| `BarWriter` (bars) | ~50 frames per flush; more under a spike | **lossless**, depth counted | dropping shaves the highs and lows out of history, invisibly |

**And everything in this process is sequential.** One `asyncio` event loop, one thread, so
only one piece of our code runs at any instant — the socket reader, the solver and the
aggregator take turns rather than running together. A long turn anywhere stops the socket
reader, the OS receive buffer fills, and Delta closes the connection. That is why the disk
write is pushed to a worker thread, and it is the reason "concurrent" and "parallel" must
not be muddled when reasoning about this engine.

So the question is never *whether* a consumer falls behind. It is: **one consumer is
allowed to fall behind and lose things; the other falls behind constantly and must lose
nothing.** Any broker we adopt has to serve the second one.

## The row that matters most to us

**When a consumer falls behind.** This project already learned the hard way that it is a
**correctness** question, not a performance one: drops happen under load, load is when
price moves fastest, so drop-oldest systematically shaves the highs and the lows out of the
bars — a bias, not noise, with nothing in the output to say so. That is why `BarWriter`
subscribes losslessly and its ceiling is a watermark that **counts** rather than discards.

Against that requirement:

- **RabbitMQ** is safe and *loud* — it slows the whole system down rather than losing
  anything. You cannot fail to notice.
- **Kafka** is safe and *visible* — nothing is lost, and consumer lag is a number you can
  watch.
- **Redis Streams** is the dangerous one for this specific job. A slow consumer plus
  trimming can silently drop entries nobody read. Redis 8.2's consumer-group-aware trimming
  helps, but it has to be chosen; the naive `MAXLEN` does not protect a lagging reader.

**So if we ever put a broker behind our fan-out seam, the bar-writing path is the one that
decides which broker — and it is the path Redis Streams serves worst by default.**

---

## What this does *not* yet answer

Latency and sustained rate, at our numbers rather than someone's blog. That is the spike:
replay real decoded frames through (a) our in-process fan-out and (b) Redis Streams on
localhost, at 1 Hz and at ~1,323/s, recording round-trip latency, maximum sustained rate,
CPU, and behaviour when the consumer is deliberately slowed.

**Blocked on a runtime.** No Redis on this machine — Docker Desktop's daemon is not
running, WSL Ubuntu has no `redis-server`, and its `sudo` wants a password. Either will do;
neither can be arranged without the human.

## Still open

Unchanged from pass 1, and each still changes a conclusion here:

1. Are the senior's five boxes separate OS processes, or one process with topic names?
2. Redis **Streams** or Redis **pub/sub**? Pub/sub has none of the above — no log, no
   replay, no pending list. If it is pub/sub, this whole table describes something he is
   not using.
3. Is `autotrim` left at the Nautilus default of 30 minutes?
