> As of delta-exchange-payoff@7783a4b, 2026-09-14

# Deployment and cost — where the engine will run

Where the [feed engine](feed-engine.md) goes in AWS, what it costs, and when to split it. Prices
are `derived`, ap-south-1, AWS Price List Bulk API read 2026-09-12, all-in (instance, 30 GB gp3,
one IPv4). **Nothing here is built** — #71 deploys it and needs AWS credentials.

## The decision

**ECS on EC2, one `c7g.xlarge` (Graviton3, 4 vCPU, 8 GiB), `host` network mode, public subnet,
ap-south-1 — `derived` $78.07 a month.** Confirmed by the owner on 2026-09-13. Records 0005 and 0008.

- **Why ECS on EC2:** restarts and records dead containers and holds desired state, for $0. EKS adds
  $73.00/month and a yearly upgrade. Fargate bills reservations, which the instance overcommits.
- **Why a public subnet:** a NAT gateway would cost `derived` $165.00/month at 2,216.5 GB inbound.
- **Why 4 vCPU and not 2:** `feed` reserves a whole vCPU (1,024 CPU units) so `api`'s viewers can
  never starve it. A starved `feed` leaves holes in the bars.
- **Why Mumbai:** cheapest of four regions priced, in-country for a future NSE adapter. Delta's origin
  is **AWS Tokyo** behind CloudFront `BOM78`, so a region buys only the client-to-edge leg.

## CPU and RAM, `measured`

I13 (#79), 2026-09-12T05:50:07Z–11:02:38Z, 5h12m, at `derived` 0.86× of normal load, BTC only.

| Container | CPU, cores (mean) | RAM mean | RAM p95 |
|---|---|---|---|
| `feed` | 0.3592 | 97.1 MiB | 105.8 MiB |
| `store` | 0.3048 | 113.0 MiB | 183.4 MiB |
| `api` | 0.3045 | 80.2 MiB | 81.5 MiB |
| `web` (idle, no viewers) | 0.0388 | 110.6 MiB | 112.5 MiB |
| Redis | 0.0706 | 761.8 MiB | 802.9 MiB |
| proxy | 0.0109 | 17.1 MiB | 17.7 MiB |
| `discord-alerts` (separate 10-min run) | 0.0463 | 46.9 MiB | 52.7 MiB |

- **Total CPU `derived` 1.1351 cores** across seven — two runs in one sum. The six-container
  total is `derived` 1.0888, re-tagged at all five sites by #118. Redis's earlier 1,056.4 MiB is `measured` (I2's run).
- **Total RAM `derived` ~1.23 GiB mean, ~1.36 GiB at p95.**
- **Worst case `derived` ~3.1 GiB of 8:** Redis full at its 2 GiB ceiling, services at p95, ~0.5 GiB
  for the OS and ECS agent. **Memory does not bind at 1×.** At 10× Redis alone is `derived` 10.269 GiB, so it does.
- **The reservations sum to 8.25 GB** (`compute.md` §4) against 8 GiB — sized before measurement.
  They could be lowered; nothing has decided that.
- **CPU binds, not memory.** Every Python service is one event loop, one core at most (record 0007).

## The next topology, and when

**Split when the instance passes 2.8 cores (70% of 4 vCPU) or `oms` places its first order through
the bus.** Measured load is 1.09 cores, 41% of the threshold.

| | Instance A | Instance B | $/mo 1× | Lossless path | If B dies |
|---|---|---|---|---|---|
| **T1, today** | everything, `c7g.xlarge` | — | **$78.07** | loopback | everything stops |
| T2 | `feed` + Redis, `c7g.large` | `store` + `api` + `web`, `c7g.large` | $84.46 | **crosses the network** | B must be replaced inside Redis's 30 min or bars are lost |
| **T4, next** | `feed` + `store` + Redis, `m7g.large` | `api` + `web` + proxy + alerts, `c7g.medium` | **$73.22** | loopback | **nothing lost**, only the screens |
| T3 | one instance per service | | $128.07 | two hops | 16 alarms, ~3.5 h/month |

**The owner proposed T2 on 2026-09-13; the records choose T4.** The difference is where `store` sits:
T4 keeps `feed → Redis → store` on one machine, so losing instance B costs the screens and no data.
T4's `c7g.medium` passes the fit rule with one viewer; a second viewer on the largest ladder needs
`c7g.large`. `oms` goes on A beside Redis, `strategy` on B beside `api`.

**At 10×:** T1 is one `c7g.4xlarge`–`c7g.8xlarge`, $295.72–582.39; T4 $373.79–732.08.

## What a split adds

- **Latency:** the same-AZ hop is `derived` ≤ 1 ms round trip — under 0.1% of `api`'s one-second
  ladder push. `feed`'s 50 ms batch is untouched because Redis stays beside it. **Never measured**:
  that is #80, and its p99.9 is the number to read, not the median.
- **Cost traps:** same-AZ traffic is free **on private addresses only**. Across AZs, or via a public
  IP, $0.01/GB each way — `derived` +$31.44/month for T4.
- **Work:** ~1.5 h/month against ~50 min. A second AMI, placement constraints, Redis on a fixed
  private IP behind a password and a security-group rule, per-instance alarms.

## Open

- **`oms` latency** — whether an order path can spend a same-AZ hop is undecided (record 0008).
- **`m7g.large` at $48.94** — I13's 1.09 cores crossed record 0008's "≤ 1.4 cores" trigger. The class
  is **not** reopened: headroom, not the total, rejected it, and p95s sum to 1.767 cores, 88% of 2 vCPU.
- **Redis fallback** if a criterion moves: ElastiCache for Valkey `cache.t4g.medium`, `derived` $47.30/month.

## Pointers

- The table and arithmetic: `delta-exchange-payoff/docs/design/cloud/compute-topology.md`
- Sizing, ops list, load profile: `delta-exchange-payoff/docs/design/cloud/compute.md`
- Measured per container: `delta-exchange-payoff/docs/design/research/0007a-container-measurement.md`
- Decisions: `delta-exchange-payoff/docs/design/decisions/0005-compute-and-region.md`, `0008-topology.md`, `0002-redis-hosting.md`
- What someone with credentials runs: `gh issue view 70` in `delta-exchange-payoff`, closing comment

## Related

[feed-engine](feed-engine.md) · [service-health](service-health.md) · [bar-store](bar-store.md)
