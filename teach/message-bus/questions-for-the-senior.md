# Questions for the senior

Five. Each is phrased twice — once as the thing to actually ask, answerable from watching
the system run, and once as what it is really asking. Each changes a conclusion written
down in [architectures](architectures.md) or [the-three-brokers](the-three-brokers.md).

## 1. How many programs do you actually start?

> **Ask:** "When you start the system, how many things do you launch — one, or several?"

A bus only earns its keep between separate programs. If it is all one program, Redis is
sending messages out and straight back in.

| answer | consequence |
|---|---|
| several | the design is sound; copy the pattern when we split |
| one | Redis is optional there; do not copy it blindly |

## 2. Redis Streams or pub/sub?

> **Ask:** "If a strategy crashes and restarts, does it see the messages it missed while it
> was down?"

Better than the technical question because it is observable. `XADD` / `XREADGROUP` means
Streams; `PUBLISH` / `SUBSCRIBE` means pub/sub.

| answer | meaning |
|---|---|
| it catches up | Streams — everything in pass 2 applies |
| it does not | pub/sub: no log, no replay, no acknowledgements, and messages are lost on every restart |

**Follow-up if Streams:** "How far back can you replay — minutes or days?" Nautilus's
default `autotrim_mins` is 30. That decides whether his Redis is a **pipe** or an
**archive**, and people routinely assume the second when it is the first.

## 3. Where do orders and fills actually live?

> **Ask:** "If Redis dies right after a fill comes in, do you still have that fill?"

The one place where losing a message costs money, and the diagram does not show the answer.
Three legitimate answers: Redis with AOF persistence on, a database such as Postgres, or
"we re-read it from the broker."

**No answer is itself the interesting outcome** — a common gap, and this is a polite way to
surface it.

## 4. Was Redis chosen, or did it come with Nautilus?

> **Ask:** "Did you pick Redis deliberately, or is it just what Nautilus uses by default?"

The question pass 1 turned on. Nautilus ships Redis as the built-in backing for external
streams, so there may never have been a comparison.

| answer | consequence |
|---|---|
| came with Nautilus | confirms pass 1; there is no Redis-vs-Kafka debate to have |
| chosen deliberately | **ask what he ruled out and why** — a real constraint from real operation is worth more than everything in pass 2 |

## 5. Where does backtesting get its data?

> **Ask:** "For backtesting, do you replay from Redis, or read stored files?"

The one that matters most for our own next steps. Our conclusion is that a backtest reads
files and never touches a bus, and that our Parquet store already **is** that source. If he
confirms it, backtesting leaves the bus question entirely.

If he replays through Redis, that is worth understanding — it is a harder design than it
sounds, and it would mean his bus is doing a job ours never has to.

---

## The message, ready to send

```
Hey, few questions on the engine architecture — been reading up on
message buses and want to check my understanding against something real.

1. When you start the system, is each box its own process, or is it
   all one process with topic names?

2. Redis Streams or pub/sub? Easier version: if a strategy crashes
   and restarts, does it see the messages it missed while it was down?
   (And if Streams — how far back can you replay, minutes or days?)

3. If Redis dies right after a fill arrives, do you still have that
   fill? Trying to understand where order/fill state actually lives.

4. Did you pick Redis deliberately, or is it just what Nautilus ships
   with? If deliberate — what did you rule out and why?

5. For backtesting, do you replay from Redis or read stored files?

Context: on the Delta side we've got a single process with an in-memory
fan-out and no bus at all, and I'm trying to work out what actually
forces you to need one.
```

**Two notes on asking.** Question 4 returns the most: whatever he rejected an alternative
*for* will be a real operating constraint, worth more than any documentation. And the
closing paragraph is load-bearing — it frames this as learning where the line is rather
than auditing his design, which is how five bare questions from a junior can otherwise read.
