> As of delta-exchange-payoff@7783a4b, 2026-09-14

# Service health — what each check can see

How to tell whether the [feed engine](feed-engine.md) is working. **The short answer: ask Redis,
not the process.** Every serious incident so far was a service reporting success while it failed.

## Do this first — 1 minute

```bash
docker exec dxp-redis redis-cli XINFO GROUPS md.option_quote:DELTA:BTC
```

- A group whose `last-delivered-id` is **older than the stream's oldest entry** has already lost
  data. Exact, no threshold.
- `pending` that **rises** is a reader stranding entries (#111). `lag 0` does not rule it out.
- Then check the newest `.parquet` generation under `.stack-data/`. **A store writing checkpoints
  and no Parquet is stalled, not quiet.**

## What each `/health` detects

`measured` 2026-09-12 from inside each container. **Read the last column first.**

| Service | On failure | Detects | Cannot see |
|---|---|---|---|
| `feed` | **503** | stopped, paused, spent budget, silence past 135 s, dead bus reader, dead flusher | whether `store` keeps up |
| `store` | **503** | reader liveness and give-up, task exits, trimmed watermarks, lag, monitor staleness | **a dead producer** — lag stays 0 when nothing arrives |
| `discord-alerts` | **503** | consumer not running, last post failed | — |
| `api` | **always 200** | the feed's state, mirrored off the bus | a spent budget; its own bus reader; its bar buffer |
| proxy | never | nginx is running | every upstream being down |
| `web` | non-2xx | the page renders | whether data flows |
| Redis | non-PONG | the server answers | memory, evictions, stream depth |

**Three of seven still cannot fail, and `api`'s is the one a person checks.** That is the first
improvement candidate below.

**A 503 from `discord-alerts` or `feed` after a rebuild is not a regression** — those paths are
new (#108, #115) and mean exactly what they say.

## The incident that shaped this — #103

At 11:02:38Z on 2026-09-12 `store` read one batch of 500 entries, never acked it, and never read
again. Retention trimmed **97 minutes** past its position. For two hours:

- `/health` said `{"status":"ok", "replay_gap_entries":0}` with the group 2.2 million entries behind
- `docker ps` said `Up 7 hours (healthy)`
- the checkpoint kept advancing, **sealing two hours of minutes empty**
- no container emitted a single application log record

The fix made `/health` a readiness check that returns 503, made the gap check continuous, and
routed JSON logs to `docker logs` and `.stack-logs/<service>/`. **Its bounded-retry change then
produced the next silent loss, #111** — 30.8% of `md.option_bar` stranded in `api`'s pending list.

## Logs and alerts worth knowing

| Record or code | Means |
|---|---|
| `store.flush` | a generation was committed; expect one every ~300 s |
| `store.checkpoint` | start-up: what was replayed (`replayed_from`) and sealed (#110) |
| `store.empty_generation` | a generation with zero rows in every table — a loss or a dead feed (#110) |
| `store.replay_gap` | the group was trimmed past; data is gone (#103) |
| `store.consumer_lag` | lag passed 100,000 entries (#103) |
| `store.flush_failed` | Parquet or checkpoint write failed (#107) |

Health payload fields to read first on `store`: `readers` (`alive`, `gave_up`, `behind`),
`consumer_lag`, `replay_gap_streams`, `flush_errors`, **`bus_checked_seconds_ago`** — the field that
would have made #103 visible in its first minute.

## Improvement candidates

Each is a gap the table above already shows. Two became tickets on 2026-09-14.

0. **Counters that exist and cannot be read (#121, #122).** The api's minute pass counts its
   errors and skips in `recompute_errors` and `minute_pass_skipped`, on no route and in no log; the
   store has no counter at all for a refused or discarded tick. Both live losses on 2026-09-13
   were found only by reading Parquet and `XRANGE`.
1. **`api`'s `/health` cannot fail.** It is always 200 and cannot see its own reader or bar buffer.
   Its bus readers also time out on a 2 s socket timeout 6–10 times a minute (#122), and it says nothing.
2. **Nothing detects a dead producer from the consumer side.** Only `feed`'s own 135 s silence rule does.
3. **No alarm reads `XPENDING` growth.** #111 ran for hours with `lag 0`.
4. **Redis's health is a PONG.** Memory against the 2 GiB `noeviction` ceiling is unwatched.
5. **The proxy's check passes with every upstream down.**

## Pointers

- Every route's detection, measured: `delta-exchange-payoff/docs/split-numbers.md` §6
- Store's own view: `delta-exchange-payoff/docs/design/lld/store-health.md`
- Readers and their stall: `delta-exchange-payoff/docs/design/lld/bus-reader.md`, `lld/bus-reader-stall.md`
- Log catalogue: `delta-exchange-payoff/docs/design/lld/logging-catalogue.md`
- Alerts: `delta-exchange-payoff/docs/design/lld/discord-alerts.md`
- The instruments and their four defects: `delta-exchange-payoff/docs/design/instruments.md`

## Related

[silent-success](../learning-records/silent-success.md) — the shape behind every row above ·
[bar-store](bar-store.md) · [deployment-and-cost](deployment-and-cost.md) — the alarms prod will carry
