# The spike — our fan-out against Redis Streams, measured

Part of [the-three-brokers](the-three-brokers.md). Terms in [vocabulary](vocabulary.md).

## Setup

Redis 7.4.11 in Docker on this laptop, port 6399; the real 136-frame `ob_l2` capture;
our own `FanOut` class, not a stand-in. Reproduce with
`delta-exchange-payoff/tools/measure_bus.py`.

**Read this caveat before quoting any absolute number.** Docker Desktop on Windows routes
localhost through a WSL2 VM, so every Redis call pays a port-forward hop. Native Linux
Redis over loopback or a unix socket is typically several times faster. **The ratios and
the batching lesson transfer; the microsecond figures do not.**

### One message, end to end (publish until the consumer holds it)

| transport | median | p95 | p99 |
|---|---|---|---|
| in-process `FanOut` | **1.8 µs** | 2.1 µs | 3.0 µs |
| Redis Streams, unpipelined round trip | **1,436 µs** | 1,665 µs | 2,035 µs |

**798x**, per message.

### What the producer alone pays

The round trip above includes the read. A feed handler only pays for the write, so that is
the number that decides whether it keeps up:

| | median | p95 | at 1,323 frames/s | ceiling |
|---|---|---|---|---|
| `FanOut.publish` (2 consumers) | **1.6 µs** | 1.8 µs | **0.21% of a core** | ~625,000/s |
| `XADD`, one per frame | **623 µs** | 776 µs | **82.4% of a core** | **~1,605/s** |

**That last cell is the finding.** Written the obvious way — one `XADD` per frame — Redis
would consume 82% of a core at our rate and top out at ~1,605 frames/s against a live feed
already delivering ~1,323. It would *just* survive, with nothing left for a busy market.

Pipelined it is a different machine entirely:

| | rate |
|---|---|
| in-process `FanOut`, 2 consumers | **407,670 /s** |
| Redis Streams, pipelined write | 53,942 /s |
| Redis Streams, batched read | 54,917 /s |

**So Redis is fast enough only if you batch** — 34x headroom pipelined, 1.2x headroom not.
And batching a live feed means deliberately adding latency, which is the thing the feed
exists to avoid. That trade has to be made knowingly.

### The same numbers at the senior's rate

At **1 Hz**, `XADD` at 623 µs costs **0.06% of a core**. Free. Same transport, same
machine, opposite verdict — which is exactly why this workspace refuses any claim about a
broker without a rate attached.

### When the consumer falls behind — 10,000 published, capacity 1,000

| | held | lost | is the loss visible? |
|---|---|---|---|
| `FanOut`, drop-oldest | 1,000 | 9,000 | **yes** — `dropped` counts every one |
| `FanOut`, lossless | 10,000 | **0** | **yes** — 9,000 over-capacity offers counted |
| Redis Stream, `MAXLEN 1000` | 1,000 | 9,000 | **no** — trimmed away, unreadable, nothing says so |

**This is the predicted failure, reproduced.** Redis discards exactly as much as the lossy
policy does, and unlike our fan-out it keeps no count. A reader that was behind cannot tell
a quiet market from 9,000 vanished frames.

Redis 8.2 added consumer-group-aware trimming, which addresses this — but it has to be
chosen, and the naive `MAXLEN` above is what a first implementation writes.

### What the spike settles

1. **Redis is not too slow for us** — pipelined it has 34x headroom at our rate.
2. **But it is 798x the cost of what we do now, to move data to where it already is.**
   The argument against it was never speed; it is that there is no boundary to cross.
3. **The silent-loss failure is real and reproducible**, and it lands on the one consumer
   that must not lose anything.

