# Pass 1 — three architectures, side by side

Terms used here are defined in [vocabulary](vocabulary.md). Read that first.

**What this pass answers:** whether the senior *chose* Redis, and whether our having no
message broker is a gap or a decision. Both turned out to be answerable from source.

---

## The one-sentence version of each

| | |
|---|---|
| **Ours** — `delta-exchange-payoff` | One process. A websocket reader publishes into two in-memory queues; one drives the screen, one writes bars to disk. No broker. |
| **The senior's** | Several components around a Redis bus carrying five topic groups, with IBKR TWS split into a data client and an execution client, and a dashboard reading over SSE. |
| **Nautilus Trader**, which his engine is built on | An **in-process** message bus, with Redis as an *optional* backing used only when messages must leave the node. |

---

## Ours

Code truth lives in the repo. Pointers, not copies:

> The fan-out and its two policies: `delta-exchange-payoff/engine/src/deltapayoff/fanout.py`
> The wiring of the whole process: `delta-exchange-payoff/engine/src/deltapayoff/main.py`

```
Delta Exchange
     |  one websocket, two channels
     v
  DeltaFeed  --publishes-->  FanOut  -->  ChainStream  (lossy, drop-oldest)
                             in-process      |  newest frame per contract,
                             two queues      |  recomputed every 100 ms,
                                             |  serves /chain and /ws/chain
                                        -->  BarWriter  (lossless + watermark)
                                                every frame, one-minute bars,
                                                hive Parquet on disk
```

The numbers that decide everything downstream:

| what | value | tag |
|---|---|---|
| `ob_l2` refresh, per contract | 508 ms | `measured` — `tools/measure_feed.py` |
| `ticker` refresh, per contract | 5,001 ms | `measured`, same run |
| frames arriving | ~1,323 / second | `measured` |
| bandwidth | ~82 KB/s | `measured` |
| contracts listed | 688 | `measured`, 2026-09-04 handoff |
| chain recompute pass | ~10 ms, every 100 ms | `measured` |

**There is no broker, and that is written down as a decision rather than left implied.**
`fanout.py` records the reasoning: OpenAlgo fans out over ZeroMQ because it serves 36
brokers and many users across separate processes; we have one venue, one user and 82 KB/s.
A broker would cost a deployment step, a failure mode and a serialise round trip per
message, and buy nothing.

The part worth keeping in mind: **the seam sits exactly where OpenAlgo puts the bus.**
Putting a real broker in later replaces what is behind the seam without rewriting the
producer or the consumers.

**The one genuinely hard-won piece of design here is the per-consumer overflow policy.**
Drop-oldest is right for the screen and *wrong* for the bar writer — not because a dropped
tick leaves a hole, but because drops happen under load, load is when price moves fastest,
so drop-oldest **systematically shaves the highs and the lows**: a bias, not noise, and
nothing in the output says so. So the writer subscribes losslessly and its queue ceiling
becomes a watermark that counts rather than discards.

Carry that forward: **how a system behaves when a consumer falls behind is a correctness
question, not a performance one.** It is the axis pass 2 compares the three brokers on.

---

## The senior's

`assumed` throughout — read from one screenshot, not from his repo.

```
IBKR TWS (market data) --> chain-feed --publish 1 Hz--+
                                                      v
             +---------- REDIS, five topic groups ----------+
             | market-data . control . signals . execution . ops |
             +----------------------------------------------+
                 ^            ^              ^            ^
            strategies    execution      dashboard     ops/recon
            (three)       --> IBKR TWS   reader -> SSE
                              (trading)
```

Topics on the diagram: `md.option_quotes`, `md.underlying`, `clock`, `heartbeats`,
`targets`, `orders.status`, `fills`, `exec.positions`, `alerts`, `recon`, `risk`,
`broker.positions`.

**The number that matters: `chain-feed` publishes at 1 Hz.** One message a second, against
our ~1,323. Any claim that a bus is cheap or expensive has to say at which of those.

Two things his design does that ours does not, and both are the reason a bus exists:

1. **Separate concerns are separate components** — three strategies, an execution client, a
   dashboard. Components that are separate processes cannot share an in-memory queue.
2. **Two IBKR connections, deliberately split** — one for market data, one for trading. A
   slow or stuck execution path cannot then stall the data path. Same instinct as our
   "the socket reader must never run inside a consumer", solved at a different scale.

---

## Nautilus Trader's own design — the finding

`measured` from the project's own documentation, read 2026-09-07:

- The MessageBus "facilitates inter-component communication through publish/subscribe,
  request/response, and command/event messaging patterns. It supports **optional** external
  backing, such as Redis, to handle live transport for **external** streams."
  — `docs/concepts/architecture.md`
- "Redis is the built-in backing for these messages, requiring a minimum version of **6.2**
  for stream trimming." — `docs/concepts/message_bus.md`. Stream trimming means **Redis
  Streams**, not pub/sub.
- Config carries `streams_prefix`, `external_streams`, `stream_per_topic`, a `types_filter`
  choosing *which* message types cross the boundary at all, and `autotrim_mins: 30`.
- The Cache "maintains trading state in memory — instruments, accounts, orders, positions"
  with `tick_capacity: 10_000`, `bar_capacity: 10_000`, `save_market_data: false` by
  default, and **optional** Redis persistence buffered at `buffer_interval_ms: 100`.

**Three consequences.**

1. **Nautilus's bus is in-process, like ours.** Redis appears only at the node boundary.
   So the senior most likely did not weigh Redis against Kafka — he chose Nautilus, and
   Redis is what Nautilus ships. Pass 2 must not argue against a decision nobody made.
2. **His bus is probably not a permanent log.** `autotrim_mins: 30` keeps half an hour.
   That is a very different thing from Kafka, and it means "Redis gives you replay" is
   true only for the last 30 minutes unless the default was changed.
3. **Nautilus's Cache is our `ChainStream`, generalised** — in-memory current state plus a
   bounded ring of recent data. We arrived at the same shape independently, which is mild
   evidence the shape is right.

---

## Where that leaves the question

**Ours is not missing a bus. It has one consumer boundary, and it is inside one process.**
A broker is for crossing a process boundary. Until a second process needs the frames, a
broker is a serialise round trip that buys nothing — which is what `fanout.py` already says.

The honest form of the open question is therefore **not** "Redis, RabbitMQ or Kafka?" but:

> What would have to become true for us to need a second process?

Pass 2 compares the three anyway — because the comparison is the learning, and because the
answer should be ready before the day the trigger fires rather than after.

## Still open

- **Are his five boxes separate OS processes, or one process with topic names?** Decides
  whether his Redis is load-bearing or decorative.
- **Redis Streams or Redis pub/sub?** Decides whether his bus has any durability.
- Whether his `autotrim` is at the Nautilus default of 30 minutes.

Three questions, five minutes of his time, and they sharpen everything in pass 2.
