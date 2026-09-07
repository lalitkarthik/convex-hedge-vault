# The disk bloat — diagnose before switching brokers

The senior reports Redis in Docker Desktop growing until it has to be cleaned by hand,
daily to three times a week, and is considering Kafka because of it.

**Switching broker is unlikely to fix this, and Kafka would probably make it worse.** There
are three candidate causes and only one of them is Redis's fault. They are cheap to tell
apart, and the answer decides whether any migration is warranted at all.

---

## Why Kafka is the wrong instinct here

**Kafka's entire design is to keep data on disk for a configured retention period.** Redis
Streams hold data in memory and write to disk only as a persistence side-effect. Swapping
an in-memory log for a disk-first log, to solve a disk problem, is backwards.

And it would still run in the same Docker Desktop, so cause 3 below would follow it across
unchanged.

## The three candidates

### 1. Streams are never trimmed — Redis's fault, and the easy fix

A Redis Stream is an append-only log that **grows forever unless told not to**. If `XADD`
carries no `MAXLEN` and no `XTRIM` job runs, every message ever published is still there.

The fix is one argument:

```
XADD mystream MAXLEN ~ 100000 * field value      # cap by count
XTRIM mystream MINID ~ <timestamp-id>            # or cap by age, Redis 6.2+
```

The `~` matters: approximate trimming removes whole internal nodes rather than counting
exactly, and is far cheaper on a hot path.

**Nautilus exposes this as `autotrim_mins`, default 30.** If his config sets it, or if he
publishes outside Nautilus without a cap, that alone explains unbounded growth.

**Related trap worth naming:** `XACK` does *not* free memory. Acknowledging removes an
entry from the group's pending list; the entry stays in the stream until trimmed. A system
that acks diligently and never trims grows exactly as fast as one that does neither.

### 2. AOF persistence growing — partly Redis's, and configurable

With `appendonly yes`, Redis logs every write to disk. The file is rewritten in the
background when it gets large, but the rewrite threshold is a setting, and a high write rate
against a small threshold means constant rewriting and a large working set.

If durability is really coming from **reconciliation against IBKR** — which is what he said
in [what-the-senior-said](what-the-senior-said.md) — then AOF may be buying very little and
its cost is worth re-examining.

### 3. The Docker Desktop VHDX never shrinks — not Redis's fault at all

**This is the most likely cause and it has nothing to do with which broker is used.**

Docker Desktop on Windows stores everything inside a dynamically expanding virtual disk
(`docker_data.vhdx`). It grows when the guest writes and **never gives space back**, because
deleting a file inside the Linux guest only updates guest metadata — the host file keeps
every block it ever allocated.

So: Redis trims its stream, the space is free *inside* the container, and the Windows file
is exactly as large as it was. That matches "we clean it manually two or three times a week"
almost exactly.

The reclaim needs two steps, in order, and skipping the first is why most attempts fail:

1. `fstrim` inside the guest, so freed blocks are marked as discarded
2. then compact the VHDX from Windows (`Optimize-VHD -Mode Full`, or `diskpart` →
   `compact vdisk` on Windows Home)

There is also a **documented Docker Desktop leak** unrelated to any container: stale ISO
blobs accumulating under `isocache` across updates, reported at 7.5 GB to 25 GB, invisible
to `docker system prune` — [docker/desktop#375](https://github.com/docker/desktop/issues/375).
Worth ruling out before blaming Redis at all.

---

## The diagnosis — twenty minutes, and it settles the question

Run in this order and the answer falls out:

| step | command | what it tells you |
|---|---|---|
| 1 | `docker system df` | how much Docker *thinks* it is using |
| 2 | compare that to the size of `docker_data.vhdx` on disk | a large gap means **cause 3** |
| 3 | `redis-cli XLEN <stream>` for each stream | millions of entries means **cause 1** |
| 4 | `redis-cli INFO memory` | how much Redis itself actually holds |
| 5 | `ls -la` the AOF directory in the volume | a large AOF means **cause 2** |

**If step 2 shows the gap, no broker change fixes it.** If step 3 shows unbounded streams,
the fix is `MAXLEN ~` and takes one line.

## What to say to him

Ask the diagnostic question rather than the conclusion:

> "Before switching — is the growth inside Redis, or is it the Docker VHDX not shrinking?
> `docker system df` against the actual `docker_data.vhdx` size will say. If it's the VHDX,
> Kafka lands in the same Docker Desktop and keeps more on disk by design."

**And one genuinely good reason to look at Kafka anyway**, unrelated to disk: he named
independent deployability as why the bus exists, and Kafka's retention model suits a system
where several consumers replay history at their own pace. That is an argument worth having
on its own terms — just not as a disk-space fix.
