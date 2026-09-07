# Message buses and caching — the plan

**Why this exists.** The senior's execution engine runs on Nautilus Trader with Redis as its
message bus. He asked for RabbitMQ, Redis and Kafka to be understood and compared, and for
the caching question to be answered. This workspace is that learning, done as three passes.

**Started** 2026-09-07.

## Read in this order

1. [vocabulary](vocabulary.md) — every term, defined before use. Start here.
2. [architectures](architectures.md) — **pass 1, done.** Ours, his, and Nautilus's own.
3. [the-three-brokers](the-three-brokers.md) — **pass 2, done.** The three, on their own docs.
   [the-spike](the-spike.md) — **run 2026-09-07.** Our fan-out against Redis Streams, measured.
4. [questions-for-the-senior](questions-for-the-senior.md) — five questions, each with the
   plain-words version to actually ask, and a ready-to-send message.
5. [caching](caching.md) — **pass 3, done.** The four caches, measured, and the gap.

The spike ran on Redis 7.4.11 in Docker, port 6399, against the real frame capture. It
**strengthened** the recommendation below rather than changing it: Redis is fast enough at
our rate *if pipelined*, 798x our current per-message cost, and reproduces the silent-loss
failure exactly as predicted.

## What was settled before starting

| decision | answer |
|---|---|
| Where it lives | this workspace, plus a durable note in [learning-records/](../../learning-records/) when it concludes |
| Does it end in a decision? | **Yes** — whether to put a broker behind our fan-out seam |
| Is Nautilus in scope? | Yes, and first. It reframed the question — see pass 1 |
| How we learn | primary docs only, plus **one measured spike** on Redis Streams |
| Caching scope | all four senses of the word, under one framework |
| The senior's diagram | treated as intent, every inference tagged `assumed` |
| Drill ledger | no |

## The rule this workspace is held to

**No claim about a broker without a message rate attached.** He publishes at 1 Hz; our feed
delivers ~1,323 frames a second. A bus that is free at his rate is not automatically free at
ours, and one we would need at ours may be pure overhead at his. Every number is tagged
`measured`, `assumed` or `derived` with the run that produced it.

## Pass 2 — the plan, so it can be argued with before it is written

**The columns**, applied identically to Redis, RabbitMQ and Kafka so none gets a home
advantage: delivery guarantee; ordering; persistence and replay; the fan-out model
(consumer groups vs exchanges vs partitions); backpressure and slow-consumer behaviour;
measured latency at both rates; operational cost; **and what each is bad at**.

The last column is mandatory. The fastest way to tell three brokers apart is what each
one's own documentation admits it is wrong for, and it is the column every comparison
online leaves out.

**The spike.** Replay real decoded frames through (a) our in-process fan-out and (b) Redis
Streams on localhost. Record per-message round-trip latency, sustained maximum rate, CPU,
and — the axis that actually bit this project — **what each does when the consumer falls
behind**. Run it at both 1 Hz and ~1,323/s.

## Pass 3 — the four caches

Done: [caching](caching.md). Headline — we need no caching we do not already have. Our
computed chain is invalidated by **arrival, not by time**, so it cannot serve a stale
answer; the history reads are 6.8 ms and want no cache; and the real gap is **durability**,
whose cheapest fix is flushing every five minutes rather than a new dependency.

## Where the answer stands, before pass 3

**Recommendation, if we ever cross a process boundary: Redis alone. Not Kafka, not both.**

- **Backtesting is not a bus question.** A bus carries live messages between running
  programs; a backtest reads stored files. Our Parquet store already **is** that source.
- **Four kinds of traffic**, and Redis serves all four: prices (thousands/second, each one
  disposable); decisions (a few a day, each one money); current state (a fact looked up,
  not a message); history (files, not a bus).
- **Redis is more durable than its reputation.** `appendfsync everysec` loses at most one
  second; `appendfsync always` is "very very slow, very safe" — and *slow does not matter
  for order events, because they happen a few times a day*. The safest setting is
  affordable on exactly the traffic that needs it.
- **Kafka's three strengths do not bite here.** Millions of messages/second (we have
  1,323), days of retention for many independent readers (we have two readers and Parquet),
  cluster-scale throughput (one laptop).
- **Two brokers is the worst option.** Two things to install, watch and debug, serving one
  process boundary.
- **The strongest available evidence:** the senior runs a real execution engine placing real
  orders on Redis alone.

**One boring alternative worth naming:** orders and fills often belong in a **database
table**, not a broker at all — you want to *query* them ("what is my position?"), not stream
them. Nautilus supports Postgres alongside Redis for this.

**Revisit only when:** several independent readers need the same stream over days, or Redis
measurably cannot keep up. Neither is close.
