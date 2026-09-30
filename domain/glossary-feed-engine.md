# Glossary — the `delta-exchange-payoff` feed engine

> Split from [GLOSSARY](../GLOSSARY.md) on 2026-10-01, when the [trading-engine](trading-engine.md) became the
> engine we build on. These are the earlier engine's terms, kept because its notes and its execution
> design still use them.

Canon for these is `delta-exchange-payoff/CONTEXT.md`; this section holds only the terms vault notes
use. The map is [feed-engine](feed-engine.md).

**Split mode / Monolith**: The seven-service composition over Redis (`DELTA_BUS=redis`), and the
default single process with an in-process bus.

**Stream / Consumer group**: A stream is one Redis key of entries; a consumer group is one service's
place in it. Never used for each other.

**Lossless / Drop-oldest**: A subscription that reads through a group and drops nothing (`store`),
and one that keeps only the newest and counts what it skipped (the chain cache).

**Retention**: Thirty minutes, by age. What a restarted `store` can still recover.

**Seal**: Closing a minute's bucket. Final — a minute sealed while its data is unread is lost.

**Store flush**: Writing sealed bars to Parquet every 300 s; the only durability boundary.
_Avoid_: save, write, persist

**Watermark / Checkpoint / Generation**: The last flushed entry per stream; the file holding the
watermarks; the number in a flush file's name. See [bar-store](bar-store.md).

**Ladder**: The chain as the screen shows it, rows ascending by strike.

**Computed chain**: Our own IV, Greeks and forward, beside the venue's reference figures.

**`measured` / `assumed` / `derived`**: The provenance tag every number carries — observed in a named
run, chosen by a person, or computed from the other two. One origin each, never re-tagged.

**Instance**: One EC2 machine. _Avoid_: box, node.

**Book (execution design)**: A table of signed lots per contract — a position snapshot, never prices
or orders. Six are named: desired per strategy (1), desired pooled (2), actual per strategy (3),
actual engine (4), actual broker (5, the truth), discretionary (6, derived as 5 − 4). Canon:
`delta-exchange-payoff/CONTEXT.md` §8 and `docs/design/execution/books.md`.

**Strategy set**: Every strategy process currently running. _Avoid_: portfolio — see Collisions.

## Related

[GLOSSARY](../GLOSSARY.md) · [glossary-trading-engine](glossary-trading-engine.md) · [feed-engine](feed-engine.md)
