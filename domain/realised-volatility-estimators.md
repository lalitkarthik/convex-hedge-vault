> As of Convex-Hedge-Trading-Engine@06e547fa, 2026-10-23

# Realised volatility estimators — which one, at which horizon

Realised volatility (RV) is never observed. It is estimated from prices, and each estimator uses
different information: closes only, the high-low range, the open, the overnight gap, or every minute
of the session. This note says which estimator fits which horizon, why, and how a simulation with a
known answer checked them. **The papers' formulas and the simulation tables stay in the research
files and the repos; this note keeps the conclusions.**

The terminal's IV vs RV screen offers six estimators as checkboxes ([volatility](volatility.md)). The
trading engine has its own IV vs RV page, built from this research. Both need the same rules.

## The estimators in one table

For day *i*: o = ln(O/C₋₁) the overnight gap, u = ln(H/O), d = ln(L/O), c = ln(C/O), r = o + c.

| Estimator | Uses | Handles the gap | Handles drift | Accuracy against close-to-close |
|---|---|---|---|---|
| Close-to-close, mean removed | closes | yes (inside r) | yes | 1 (the benchmark) |
| Close-to-close, zero mean | closes | yes | no — reads high in a strong trend | about 1 |
| Parkinson | high, low | **no** | no | about 5 |
| Garman-Klass | open, high, low, close | **no** | no | about 7.4 |
| Rogers-Satchell | open, high, low, close | **no** | yes | about 6 |
| Yang-Zhang | the same plus the previous close, n ≥ 2 | yes | yes | about 7.4 over 20 days |
| Sum of squared intraday returns | 1- or 5-minute closes | only if the night is added | yes | one day ≈ 75 days of daily returns |

**Accuracy** (the papers call it efficiency) is how many days of close-to-close one estimator is worth
per day. An efficiency of 5 means 4 days do the work of 20. These are best cases for a perfect random
walk; real data gives less.

**Annualise in variance, take the root last:** σ = √(A × variance per period), with A = 252 for daily
bars, 252 × 390 for US one-minute bars, 252 × 375 for NSE. Never average volatilities. India has about
247 sessions a year; using 252 there overstates volatility by about 1%, a constant bias to state once.

## What the simulation showed

`verify_estimators.py` simulated a price with a known 20% volatility over 60,000 days per case, with
true continuous highs and lows ([verify_output.txt](../inbox/2026-10-06-iv-vs-rv-research/verify_output.txt)).
Every result is estimated over true variance; 1.00 is right.

- **The overnight gap breaks the range estimators.** With a quarter of each day's variance overnight,
  Parkinson, Garman-Klass and Rogers-Satchell all read about 0.75. Yang-Zhang read 1.00.
- **Drift breaks the zero-mean forms.** At a drift of half a daily standard deviation a day,
  zero-mean close-to-close read 1.25 and Parkinson 1.10. Rogers-Satchell and Yang-Zhang read 1.00.
- **Sampled highs and lows read low.** Built from one-minute prices, Parkinson read 0.93 and
  Garman-Klass 0.91; from five-minute prices, 0.86 and 0.80. A candle built from a few prices
  understates its true range.
- **Noise inflates fine sampling.** With 2 basis points of price noise, intraday RV read 1.19 at one
  minute and 1.04 at five minutes. This is why five minutes is the default for a noisy series such as
  the SPX implied forward.
- **A part day scaled by the clock lies.** On a U-shaped day, the first hour's RV scaled to a full
  session by the clock read 1.58. Scaled by the usual share of a day's movement so far, it read 1.00.
- **A popular Python Yang-Zhang** (`volatility-trading`) reads 5% to 15% high. Its terms are not the
  paper's. Copy the formula from Yang and Zhang (2000), not from a library.

## Which estimator at which horizon

The rule under every row: **set IV against RV over the same stretch, on the same clock, with the
night counted on both sides or on neither.**

| Horizon | IV side | RV side | Why |
|---|---|---|---|
| Inside one session (minutes to hours) | ATM IV of the expiry held, turned into the variance it budgets for that stretch | Sum of squared returns — one minute for NIFTY and SENSEX, five minutes for the SPX forward — scaled by a **time-of-day profile**, never by the clock | Hundreds of returns a day; the profile removes the U-shape |
| Same-day expiry | The ATM straddle at entry, in points | The absolute move from entry to the close | No clock and no annualising needed; the straddle is the implied mean move, about 0.8 of one standard deviation |
| One to seven sessions | ATM IV of the held expiry, with its sessions left | Intraday RV summed over the last *n* sessions **plus the squared overnight gaps**, annualised by 252/*n* | Five daily returns give a standard error near 32%; the option's price includes the nights |
| A month | Constant-maturity 30-day IV, blended on total variance between the two expiries either side | Yang-Zhang or close-to-close over 21 sessions | Daily bars are enough; Yang-Zhang is the only range estimator free of both gap and drift |

**Close-to-close stays the reference** whenever the comparison must match a variance swap or a book
hedged at the close: it holds the night with no adjustment, and it is what the published realised
indices use. **Garman-Klass and Parkinson suit a market with no gap**, such as crypto or near-24-hour
futures.

**The night is large.** In the published US work it is 18% to 30% of a day's variance. On SPXW the
feature experiments found **the nights are a third of a week's movement**
([feature-testing](feature-testing.md)). No published figure exists for NIFTY or SENSEX; it must be
measured from stored sessions.

## Mistakes that make an IV-against-RV chart lie

From the eighteen in the horizons research, the ones that bite first:

1. **Windows that do not match** — a 20-day RV under a 3-day option.
2. **Two clocks** — calendar-time IV against 252-day RV. Inside a week the error reaches 30% and
   changes with the weekday. A same-day option on the calendar clock reads about 2.3 times too high.
3. **The night on one side only.** Session-only RV against a multi-day IV reads RV low by the
   overnight share.
4. **A part day scaled by the clock** — 58% high after the first hour.
5. **Trailing RV read as what was earned.** Trailing RV is context. The ex-post premium needs RV over
   the days *after* the IV, drawn under the date the IV was quoted.
6. **Overlap read as evidence.** A daily series of a 21-day premium is about one independent reading
   a month.
7. **A sign or a unit left unstated.** Gap in volatility points is IV − RV; Carr and Wu's premium is
   on variance with the opposite sign.

## Where it is built

- **The trading engine's IV vs RV page** (`/iv-rv/`, PR #306, merged 12 October 2026) computes the
  intraday side: squared returns at one and five minutes, a 15-minute time-of-day profile learned
  from up to 30 stored sessions (no figure until five complete sessions exist), Gap, Pace and the
  move against the straddle. Canon: `Trading-Engine/Guide/The IV vs RV page.md` and
  `Trading-Engine/Research/Implied against realised volatility.md`.
- **Since then the page was reworked.** Range methods (decision 0109) and the *Realised volatility
  rework* (issue #558, live 17 October 2026) run all seven methods on the sampled candles, let a
  window reach back into stored sessions, count the overnight return with a night bucket in the
  profile, and add Garman-Klass and Yang-Zhang. Canon: `Trading-Engine/Specs/Realised volatility
  rework.md` and its research note. **This replaces the 12 October handoff's statement that range
  estimators were left out inside the day.**
- **The positional view (days to weeks) is not built.** It needs past daily index prices and expiries
  further out than the feed takes: about 14 days for a 7-day IV, about 45 for a 30-day IV.
- **The research repo** has its own calculation page: `convex-hedge-strategy`,
  `Strategy-Research/Guide/Implied against realised volatility calculations.md`.

## Open questions

1. **For Bilal:** back-fill past daily index prices from a broker, or let the store build its own?
2. **For Bilal:** the longer IV — further expiries blended to constant maturity, India VIX, or weekly
   only? India VIX reads above ATM IV wherever there is a skew, so "India VIX − RV" overstates what a
   straddle seller earns.
3. What is the overnight share of variance for NIFTY and SENSEX? The engine's daily rows can measure it.
4. Two at-the-money IVs show on one engine screen: the header's nearest-strike IV and the page's
   skew-at-the-forward IV. Should they be one?
5. The Indian session length: the research assumed 375 minutes; Indian options have closed at 15:40
   since 3 August 2026. The profile adapts, but the assumption is unconfirmed.
6. The part-day scaling rule is derived from Andersen and Bollerslev's model and confirmed only by
   simulation. No paper states it.

## Sources

- [research-estimators.md](../inbox/2026-10-06-iv-vs-rv-research/research-estimators.md) — every formula, its source, the simulation
- [research-horizons.md](../inbox/2026-10-06-iv-vs-rv-research/research-horizons.md) — which IV against which RV
- [research-dashboards.md](../inbox/2026-10-06-iv-vs-rv-research/research-dashboards.md) — how 24 products show it
- [iv-vs-rv-calculations-and-sources.md](../inbox/2026-10-06-iv-vs-rv-research/iv-vs-rv-calculations-and-sources.md) — the calculation, step by step, for the 7 October meet
- [positional-iv-vs-rv-sources.md](../inbox/2026-10-06-iv-vs-rv-research/positional-iv-vs-rv-sources.md) — the positional findings
- [handover-intraday-iv-vs-rv.md](../inbox/2026-10-06-iv-vs-rv-research/handover-intraday-iv-vs-rv.md),
  [handoff-positional-iv-vs-rv.md](../inbox/2026-10-06-iv-vs-rv-research/handoff-positional-iv-vs-rv.md) — state of the engine feature
- [verify_estimators.py](../inbox/2026-10-06-iv-vs-rv-research/verify_estimators.py),
  [verify_output.txt](../inbox/2026-10-06-iv-vs-rv-research/verify_output.txt) — the simulation

## Related

[volatility](volatility.md) · [feature-testing](feature-testing.md) · [trading-engine](trading-engine.md) ·
[engine-dashboard](engine-dashboard.md)
