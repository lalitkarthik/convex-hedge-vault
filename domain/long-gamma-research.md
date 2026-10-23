> As of convex-hedge-strategy@292f816, 2026-10-23

# Long-gamma research on SPXW 0DTE

The desk's strategies are almost all **short gamma**: they sell options and earn the premium on
most days. The senior asked for at least one **long-gamma** strategy — one that buys options and
earns when the market moves more than was priced. This note holds the question, what the literature
says, how it was tested on 7 October 2026, and the result. **The study's own Guide page and notebook
are canon for every figure.**

## Where a hedged straddle's money comes from

A straddle bought and hedged back to zero delta earns from movement and pays the clock:

- Hedged result ≈ ½Γ × Σ (move between hedges)², less the theta paid.
- Θ per unit of time = ½Γσ²F², so the buyer breaks even when realised variance equals implied.
- So **Θ ÷ Γ, vega ÷ Θ and Δ ÷ Γ are implied volatility and the clock in other units.** Plotting them
  against ATM IV plots IV against itself. They are units, not signals.

The buyer wins when realised variance beats implied over the stretch held. Every 0DTE study read
finds implied above realised on average, so the plain buyer loses on most days and wins on a few
large ones.

## What the literature says

The literature report was written by a research run; its sources were then opened by hand, which
changed two points (below).

- **Start from a mechanism, not a correlation scan.** Say who is forced to trade and why that leaves
  the straddle mispriced. With 127 days, a scan finds false positives.
- **Clock time against variance time** is the one mechanism that transfers to 0DTE. Options run time
  value off by the clock, while movement arrives in a U-shape through the day. Muravyev and Ni found
  delta-hedged SPX options gain inside the day, mostly in the afternoon — but in multi-day options,
  before costs, before 2014.
- **0DTE implied is rich on average but by little.** Vilkov finds the same-day premium positive but
  hard to collect after costs; profits are driven by tails. *Checked by hand: Vilkov's 0DTE study is
  unhedged.*
- **The hedge band is a bet on scale.** A tight band pays when prices revert; a wide band pays in a
  trend. The cost of each re-hedge decides how wide is wise (Whalley and Wilmott). *Checked by hand:
  their band formula could not be confirmed from the abstract.*
- **Long wings over a short body are rich** on 0DTE, especially calls. The literature is against
  that shape.
- **Sample size limits what can be proved.** With 127 days, only an annualised Sharpe ratio near 2.8
  can be told from zero. A Sharpe of 1 needs roughly 800 to 1,200 days, depending on skew.
- **NIFTY is different.** Sellers there earn overnight and lose inside the day. Since April 2026, a
  futures hedge sale pays 0.05% of notional in transaction tax, so futures-hedged scalping is close
  to uneconomic; hedge with option legs instead.

## The plan, decided on 7 October

Nineteen decisions in three rounds ([plan](../inbox/2026-10-07-long-gamma-research/plan.md)). The ones
that shape the result:

- **Done** means a strategy in the engine's shape — entry, structure, hedge rule, exit — with one page
  of evidence. A tested idea that failed, with its reason, also counts.
- **One target:** the result of a hedged ATM straddle after the spread. The straddle keeps its entry
  strike until the window ends.
- **Three hedge rules side by side:** every minute; the desk's band (delta ÷ gamma past one sixth of
  the implied move left); a wide band (half the implied move).
- **Each result twice:** at the mid, and with the spread paid.
- **No tuned thresholds.** Days are sorted into four equal groups by the feature and the trend across
  groups is tested on ranks and medians.
- **Five hypotheses, each with a source,** joined to the repo's existing twelve tests and corrected
  as seventeen.
- **Every result reads "SPXW, intraday, 0DTE".** Nothing is assumed to carry to NIFTY.

## The five hypotheses and the result

The target table (PR #26) and the study (PR #27) were both merged on 7 October 2026. The notebook is
`notebooks/spxw_hedged_straddle.ipynb`.

| # | Idea | Result on 127 days |
|---|---|---|
| H1 | The hedged buyer is paid in the last 90 minutes | **A finding against itself:** the 14:30 buyer lost on 86 of 112 days |
| H2 | A busy first half-hour helps the buyer from 10:00 | Not a finding |
| H3 | IV below a realised-volatility forecast helps the buyer | Not a finding |
| H4 | A trending morning favours a wide hedge band | Not a finding |
| H5 | The hedged seller is paid over midday | Not a finding |

**No long-gamma idea passed.** The baseline agrees: the hedged long straddle bought at 9:36 and hedged
every minute at no cost won on 42 of 126 days and summed to −214 points, while its ten best days
summed to +140. The clock chart shows time value running off faster than movement before 11:30, and
the other way round from 11:30 to the close — yet the afternoon buyer still lost.

By the plan's own definition this is a done result: tested ideas that failed, each with its reason.

## Contradictions with later work

- **"Time of day is the one lead"** (the plan's facts). The plan read IV above realised volatility on
  33% of days at 9:35 and 87% at 15:00. The feature experiments of 8 October showed this is an effect
  of the comparison: IV at 9:35 prices the whole day. Set each window against what the options charged
  *for that window* and the ratio is flat through the day ([feature-testing](feature-testing.md),
  finding 4). The morning lead for the buyer is therefore weaker than the plan assumed.
- **"No new download now"** (decisions 6 and 16). Superseded the next day: 122 fresh days were bought
  on 8 October for the feature experiments ([databento](databento.md)). The five hypotheses have not
  been re-run on them.
- **The desk's backtest tool.** The plan meant to prove a rule there on days after 30 September 2026.
  Its date range is now known: the lab holds SPXW from 1 July 2025 to 7 October 2026
  ([backtest-lab](backtest-lab.md)).

## Status

- Feature 1 (target table) and feature 2 (the five-hypothesis study) are merged in
  `convex-hedge-strategy`. No long-gamma strategy exists.
- Lesson 1 of the sixteen teaching items is taught; lessons 2 to 16 are not.
- The only long side tried since is the `short_or_long` rule in the backtest lab, which buys the
  straddle after a window with a large move ([backtest-lab](backtest-lab.md)).

## Open questions

1. A sixth candidate — long from 9:35 for the first hour — was the strongest lead in hand on 7
   October and has no source. After the per-window finding above, is it still a lead?
2. Three readings of the skipped-hedge rule on issue #20 wait for Lalit's word.
3. Do the five hypotheses change on the 122 fresh days?
4. Five-minute returns reverse slightly (median lag correlation −0.05). Is that real, or noise in the
   implied forward? It would favour the desk's tight band on the short side.
5. Is there a long-gamma mechanism outside clock-versus-variance time — event days, or the
   short-gamma hedging flow that drives intraday momentum — that the SPXW data can test?

## Sources

- [plan.md](../inbox/2026-10-07-long-gamma-research/plan.md) — nineteen decisions, facts, five hypotheses, the teaching list
- [literature-report.md](../inbox/2026-10-07-long-gamma-research/literature-report.md) — the research run's brief
- [session-log](../session-log.md), entries of 7 October 2026 — the build and the result
- Repo: `convex-hedge-strategy`, `Strategy-Research/Guide/SPXW 0DTE hedged straddle study.md` and
  `Hedged straddle results table.md`; decisions 0020 to 0022

## Related

[strategy-research](strategy-research.md) · [feature-testing](feature-testing.md) ·
[backtest-lab](backtest-lab.md) · [strategies](strategies.md)
