# Pass 3 — what caching we actually need

Terms in [vocabulary](vocabulary.md). The bus half is [the-three-brokers](the-three-brokers.md).

Four different things wear the word "cache" here. One question separates them cleanly:

> **What goes stale, how fast, and who notices?**

---

## The four

| | what it holds | built? |
|---|---|---|
| **1. Latest frame per contract** | newest `ticker` and `ob_l2` frame per symbol | yes — `ChainStream._ticker` / `._book` |
| **2. The computed chain** | our solved IV and Greeks per `(underlying, expiry)` | yes — `ChainStream._computed` |
| **3. Stored-history reads** | a day of bars off Parquet | **no** — `smile.py` reads disk every request |
| **4. Surviving a restart** | anything at all | **no** — everything above dies with the process |

---

## 1. Latest frame per contract

**What goes stale:** nothing, by definition. It holds only the newest frame per symbol, so
"stale" is not a state it can be in — the newest frame *is* the truth.

**Who notices:** nobody, and that is the point. This is why `ChainStream` can subscribe
lossy: a dropped older frame is exactly what the cache would have overwritten anyway.

**The one real subtlety** is that `ticker` and `ob_l2` are kept in *separate* dictionaries
rather than merged on arrival, and layered only when a chain is built. They refresh at
508 ms and 5,001 ms; merging on arrival would let the slower channel overwrite fields the
faster one had just refreshed.

## 2. The computed chain — the interesting one

`measured` 2026-09-07 on the 69-row 04-09-2026 fixture, median of 200 runs:

| | |
|---|---|
| build the raw chain from frames | **5.383 ms** |
| enrich it — IV **and** all five Greeks | **0.719 ms** |
| `chain()` **cache hit** | **0.0004 ms** |
| `chain()` **cache miss** | **6.073 ms** |
| the cache is worth | **~15,000x per read** |

**Two things worth keeping.**

**First, the expensive part is assembling the chain, not the mathematics.** 5.4 ms to build
against 0.7 ms to solve every volatility and every Greek. The intuition — that inverting
Black-76 is where the time goes — is wrong at this scale by a factor of seven.

**Second, and this is the design worth copying: the cache is invalidated by *arrival*, not
by time.** There is no TTL. A frame landing marks its `(underlying, expiry)` dirty, and
`chain()` recomputes synchronously when the key it is asked for is dirty.

> So **the cache cannot serve a stale answer**. Not "rarely does" — cannot. Freshness is a
> property of the read path, not of how recently a timer ran.

The 100 ms loop then computes once for every reader rather than once per reader, and bounds
staleness for a screen nobody is currently watching. `stream.py` states it exactly: *"It is
an optimisation, not the mechanism."*

That distinction is the whole answer to "what caching do we need". **Time-based expiry — the
thing most people reach for — buys a window in which the cache is knowingly wrong.** For a
price screen that window is the bug.

### A number to re-measure

`stream.py` records that "a full pass over every listed expiry is ~10 ms". `measured`, one
expiry with 69 rows took **7.25 ms**. Eight expiries are listed live. Those two do not
reconcile — 8 × 7 ms is ~56 ms per pass against a 100 ms tick, which would be over half a
core rather than the ~10% the comment implies.

The fixture may not be representative and the live path may be warmer. **`assumed` either
way until measured against the running engine** — but it is exactly the shape of thing this
project keeps finding: a good design carrying a bad number.

## 3. Stored-history reads — no cache, and probably right

`smile.py` reads Parquet on every request. `measured` by the smile work: one minute for one
expiry 4.5 ms, the whole day — 540 minutes, 18,676 rows — 6.8 ms, because Parquet prunes by
partition and by column so the fixed cost dominates.

**A cache in front of a 6.8 ms read that is already served once per screen load would be
pure complexity.** The right move was the one taken: return the whole day in one response so
scrubbing is an array index rather than a network round trip.

**What would change this:** the five-minute flush multiplies the current day's file count by
twelve, and the re-read cost is `derived` at ~88 ms until someone measures it. If that lands
near 88 ms, an in-process cache of the current day becomes worth considering — and
compaction, which returns the day to one file, is the cheaper fix.

## 4. Surviving a restart — the real gap, and it bit today

Every cache above lives in the process. When the engine dies, all of it dies:

- the latest frame per contract — harmless, refills in ~508 ms
- the computed chain — harmless, rebuilds in 6 ms
- **whatever bars are buffered and not yet flushed — gone, unrecoverably**

That last one has now cost real data three times: 2h52m to a closed laptop, ~62 minutes to
a teardown, and again on 2026-09-07 when the engine stopped and nobody noticed for hours.

**This is the one place a Redis-shaped answer genuinely earns its keep** — and note that it
is not the bus. Nautilus uses Redis exactly this way: its `Cache` holds instruments,
accounts, orders and positions in memory with **optional** Redis persistence, buffered at
`buffer_interval_ms: 100`, restored on startup before reconciliation.

**But it is not our cheapest answer.** Flushing every five minutes — already coded on
[#16](https://github.com/lalitkarthik/delta-exchange-payoff/issues/16) — cuts the loss
window from sixty minutes to five for the price of one constant. Adding Redis to fix
durability would be the most expensive possible version of a five-line change.

---

## The answer to "what caching do we need"

**None that we do not already have.** Concretely:

1. **Keep invalidating by arrival, never by time.** It is why our cache cannot be stale, and
   it is the single most valuable thing in this note.
2. **Do not cache the history reads.** 6.8 ms served once per screen load. Re-measure after
   the five-minute flush lands, and reach for compaction before a cache.
3. **The gap is durability, not caching** — and the fix is flushing more often, not a new
   dependency.
4. **Re-measure the full recompute pass** against the live engine. If it really is ~56 ms
   per 100 ms tick, that is a live problem wearing a comment that says otherwise.

**Redis would be the answer to a question we do not yet have**: state shared between
separate programs that must survive one of them restarting. The day there is a second
program, revisit — with [questions-for-the-senior](questions-for-the-senior.md) answered by
then, because his engine already lives in that world.
