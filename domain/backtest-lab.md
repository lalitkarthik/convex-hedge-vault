> As of Backtest-Engine@b17841a8, 2026-10-23
> (the local checkout, on branch `feature/spxw-straddle-after-bucket`, one merge behind `origin/main`
> at `0aebd67d`, which holds PR 659)

# Backtest lab — Bilal's `Backtest-Engine` and the ratio-over-the-day runs

`Backtest-Engine` (`Convex-Hedge-Private-Limited/Backtest-Engine`, cloned to
`D:\Convex Hedge\Backtest-Engine`) is the company's options backtester. Bilal gave Lalit write access
on 12 October 2026, and the first strategy from this vault's research went into it that day. This
note holds Bilal's rules for any backtest, how a strategy reaches the lab, the strategy built, and
what its first runs showed. **The repo's own pages are canon:** `PROJECT.md`, `CONTEXT.md`, `wiki/`,
and the strategy file's docstring.

## Two names, kept apart

- **`Backtest-Engine`** (this note) is the **repo**: the engine, its strategy registry and its
  dashboard.
- **[backtest-engine](backtest-engine.md)** is the vault's note on the **terminal's `/backtest`
  page**, read from the screen while the terminal sat at `app.convexhedge.ai`.

They are not unrelated. The repo's `PROJECT.md` describes three faces — the engine, a terminal-style
dashboard with runs, chains, IV surfaces and structure pricing, and *Echo*, an AI agent that writes a
strategy from chat. That is the terminal the vault mapped. Its addresses changed on 11 October 2026:

| Address | What it serves now |
|---|---|
| `lab.convexhedge.ai` | the in-house copy, every registry strategy — **the lab** |
| `research.convexhedge.ai` | the copy for external beta users (was `app.` until 11 October) |
| `app.convexhedge.ai` | the **trading engine**, not the backtester |

## Bilal's rules for any backtest

Set in the group chat on 12 October 2026 for the delta²/gamma-over-theta backtests:

- **No forward bias: decide on candle i−1, trade on candle i.** The engine already does this: it hands
  a strategy the previous bar's chain and fills on the current bar at that bar's mid.
- **Returns as a share of a fixed 150,000 for one lot** of straddle selling.
- **Add returns arithmetically** for total profit and the profit curve. No compounding.
- **"A registry strategy for all four conditions"**: the four conditions are the four buckets of the
  window before (confirmed by Lalit).

## How a strategy reaches the lab

- A strategy is **one file in `strategies/`**; its file stem is its registry id.
- It reaches the lab only through a **PR merged to `main`**, which deploys by itself. The lab's
  "New strategy" form cannot take a finished file.
- **CI has no market data**, so golden tests and other market-data tests never run there.
- The engine can run locally on our own quotes ([databento](databento.md)), but that tree has one
  expiry a day and an index made from put-call parity. **Local numbers are a rehearsal**; a full year
  takes about 9 GB and 8 minutes.

## Two facts of the engine that change a result

- **Its clock.** The chain counts a year as 252 sessions of **405 minutes** (the SPXW options session,
  09:30 to 16:15), so one minute is 1 ÷ (252 × 405) of a year. The research repo and the trading engine
  count time differently. The harness design took this engine's clock as canonical.
- **Its settlement.** A leg still open after the last bar closes at its own **mid in the day's last
  chain**, time value included, tagged `EXPIRY`. The research repo settles at intrinsic value against
  the 16:00 index. A study must not mix the two.

## The first strategy: `spxw_0dte_straddle_after_bucket`

Built from the [bucket test](feature-testing.md) and merged as PR 659 on 12 October 2026, without a
spec issue and without Bilal's review. Its feature is the **window ratio**, the Greek ratio Δ²/Γ over
Θ measured on a 30- or 60-minute window from 09:35 to 15:35 ET:

- **locked** = (Δ_call + Δ_put)² ÷ (2 × (Γ_call + Γ_put)), at the window's end, for the ATM pair
  picked at its start;
- **earned** = Σ ½ × IV² × F² × Γ × one minute, summed over the window for both legs;
- **ratio** = locked ÷ earned. Above 1 the seller lost the window; below 1 the seller earned.

Three lines cut the ratio into four buckets. Six rules trade on them, all on one lot and no hedge:
**next_window** (sell for the next window after a chosen bucket), **hold** (one straddle all day, the
baseline), **in_or_out** and **in_or_out_held** (step out after a large bucket, back in after a quiet
one), **scaled** (size 1, ¾, ½, 0 by bucket) and **short_or_long** (buy the straddle after bucket 4,
sell otherwise). On a year of real quotes, the baseline's sale price, buy-back price and result
matched the research table in 2,707 of 2,727 straddles.

## What the ratio-over-the-day runs found

Four lab runs drew the bucket lines on SPXW same-day straddles, 1 July 2025 to 7 October 2026, 316
sessions ([ratio-over-the-day.html](../inbox/2026-10-12-ratio-over-the-day/ratio-over-the-day.html)):

- **The ratio is largest in the first 90 minutes and falls through the day.** With 30-minute windows
  the median is 0.97 in the first window and 0.33 in the last one stored.
- **Two causes.** The move part (locked) is largest at the open and about half as large from late
  morning. The theta earned per window grows all day and about doubles by 15:00.
- **So the bucket is partly a clock.** One set of lines serves the whole day, and a first window falls
  in bucket 4 in 41% of cases against 16% for a 14:35 window.
- **Every time of day is skewed to the right**: the mean is 2 to 3.5 times the median.
- Both halves of the data and both window lengths agree in direction. No significance test was run.
- The day's last window is missing: this rule stores a ratio only when a trade follows it.

## Status

- **Merged and deployed:** PR 659. The lab has run it: the four line runs above.
- **Not done:** the 24 test runs on the second half of the data — each rule at 30 and 60 minutes,
  against `hold`. Untouched since 12 October, as of the 17 October handoff.
- **Local rehearsal:** 17 runs on our own second-half data. Treat as a rehearsal; `hold` was not run,
  so no rule has yet been set against the baseline.
- **Not built, on Lalit's word:** the delta hedge on the desk's band.

## Open questions

1. **For Bilal:** PR 659 skipped the spec and ticket flow and was merged without his review. Does he
   want a spec issue, a Guide page, and the `wiki/` strategy counts updated?
2. **For Lalit:** the split dates — proposed 1 July 2025 to 15 February 2026 for the lines, 16
   February to 7 October 2026 for the test. Unconfirmed.
3. **Should the bucket lines depend on the time of day?** One set of lines makes bucket 4 mostly a
   morning bucket. A rule may be trading the clock, not the ratio.
4. How is a run's signal snapshots downloaded from the lab, to draw lines from it?
5. *Assumed, unchecked:* the lab form shows the new settings and sizes a run at one unit on 150,000;
   fees on `scaled`'s fractional fills; half days, where no buy-back bar comes and the engine settles.
6. Does any day-long rule beat `hold` after costs?

## Sources

- [handoff-2026-10-12.md](../inbox/2026-10-12-ratio-over-the-day/handoff-2026-10-12.md) — the session, rules, traps, open items
- [ratio-over-the-day.html](../inbox/2026-10-12-ratio-over-the-day/ratio-over-the-day.html) — the lab runs' ratios by time of day
- Repo: `strategies/spxw_0dte_straddle_after_bucket.py` (its docstring), PR 659, `PROJECT.md`,
  `Convex-Hedge/Guide/Changelog.md` (the address change)
- Local rehearsal: `D:\Convex Hedge\Backtest-Engine-data-spike\.scratch\spike\results\results.md`

## Related

[feature-testing](feature-testing.md) · [backtest-engine](backtest-engine.md) ·
[long-gamma-research](long-gamma-research.md) · [strategy-research](strategy-research.md) ·
[platform-map](platform-map.md)
