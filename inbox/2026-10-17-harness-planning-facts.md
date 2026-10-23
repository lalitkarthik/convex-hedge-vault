promoted: 2026-10-23
# Harness planning facts — 2026-10-17

> Raw capture, not canon. Read-only fact-finding for the options research harness (SPXW 0DTE first).
> As of `convex-hedge-strategy` local branch `feature/anomaly-studies`@a5a5fa3 and remote `origin/main`@b4b174d (read through `gh api`, not fetched), 2026-10-17.

**Important first fact.** The local checkout of `convex-hedge-strategy` is behind GitHub. Local `origin/main` is `cc8b0ef` (last fetch 2026-10-12). GitHub `main` is `b4b174d`. The folders `hypothesis/` and `hyp_test_notebooks/`, which `sources/Strategy research workflow.md` names, exist **only on GitHub `main`**. No local branch holds them. I read them through `gh api` (read-only) into my scratchpad. I did not fetch or pull. Paths below say "remote main" when the file is only on GitHub.

## 1. Deterministic maths code to reuse

All paths in this section are in `convex-hedge-strategy` unless named. Language is Python 3.12 throughout. "Local" = the checkout at `D:\Convex Hedge\convex-hedge-strategy` (branch `feature/anomaly-studies`). "Remote main" = GitHub `main`@b4b174d. The core modules (`chain/`, `quotes/`, `smile/`, `features/buckets.py`, `features/windows.py`) are the same in both.

**Python and libraries** (`pyproject.toml`; `.python-version` = `3.12`):
- `requires-python = ">=3.12,<3.13"`
- runtime: `matplotlib>=3.11.2`, `numpy>=2.0`, `pandas>=2.2`, `plotly>=7.1.0`, `pyarrow>=17`, `scipy>=1.14`
- dev: `ipykernel`, `mypy` (strict), `nbconvert`, `nbformat`, `pandas-stubs`, `py-vollib>=1.0.12` (test-only IV reference), `pytest`, `ruff`
- package: `src/convex_strategy` (hatchling); tests under `tests/` mirror the package; `uv` manages the env.

### 1.1 Implied forward / put-call parity
- `src/convex_strategy/chain/forward.py` — `fit_forward(strikes, calls, puts, *, T, widths=None) -> ForwardFit` (L69–107), `ForwardFit` dataclass (L57). Weighted least squares of `C(K) − P(K) = D(F − K)` across strikes; weights = 1/combined spread. Fallback ladder: `parity_fit` → `parity_fit_unit_discount` → `single_strike_parity` → `none`. Constants: `MIN_PAIRS = 5`, `MAX_RATE = 0.30`, `MAX_DISCOUNT_ERROR = 0.05`; with 1 trading day or less left, the discount is always taken as 1 (L44–50).
- Called by `chain/build.py` `build_chain()` (L41). Only strikes with both spreads at most `MAX_SPREAD_SHARE = 0.30` of mid enter the fit; `MIN_PRICE_STEP = 0.05`.
- Tests: `tests/chain/test_forward.py`, `tests/chain/test_build.py`.
- The header says it was "Copied from `convex-hedge-payoff/src/payoff/forward.py`".
- **Other copies:** `payoff-project/src/payoff/forward.py` (the original); `Convex-Hedge-Trading-Engine/src/convex_trading_engine/chain/forward.py` `fit_forward` (`MAX_DISCOUNT = 1.05`); `Backtest-Engine/src/chain/forward.py` `compute_implied_forwards` (L82), `_regress_pcp` (L35); `delta-exchange-payoff/engine/src/deltapayoff/forward.py`.
- **Disagreement:** Backtest-Engine falls back to `F = K + exp(r*T)(C − P)` "with the static risk-free rate" (forward.py header L9–12). The strategy repo falls back to D = 1 and never trusts a fitted rate on the expiry day.

### 1.2 IV solver
- `src/convex_strategy/chain/pricing.py` — `implied_vol(price, forward, strike, T, discount, *, is_call, max_sweeps)` (L195–257): vectorised Newton–Raphson on raw vega, a bisection rescue (`_bisect`, L175) for rows whose vega collapsed, a moneyness-aware seed `_seed` (L161, Brenner–Subrahmanyam near the money). It raises on a price it cannot solve. There is no IV at T = 0.
- `black76_price` (L40). Time: `years_to_expiry(minutes_left) = minutes/390/252` (L27–30); `SESSION_MINUTES = 390` (L23).
- `chain/build.py`: one IV per strike from the **out-of-the-money option only** (the call at or above the forward, the put below). The price is the quote mid, only where both bid and ask exist that minute. Nothing is carried forward (header L1–10).
- Tests: `tests/chain/test_pricing.py` (py-vollib is the reference).
- **Other copies:** `delta-exchange-payoff/engine/src/deltapayoff/solvers.py` (`implied_vol_newton` L125, `implied_vol_brent` L248, `implied_vol_householder` L384, `solve_chain_vectorised` L482; tests `engine/tests/test_solvers.py`); `Backtest-Engine/src/chain/greeks.py` (`implied_volatility` L192, `implied_volatility_otm` L342: Newton with a `brentq` fallback on [1e-4, 5.0]); `Convex-Hedge-Trading-Engine/src/convex_trading_engine/chain/volatility.py` `implied_volatility` (L151).
- **Disagreement on the clock:** the strategy repo uses a 390-minute session (pricing.py L23–25: "The trading engine counts 405; see issue #2 before moving an implied volatility level between the two"). `Backtest-Engine/src/chain/dte.py` uses the CBOE 6.75 h session (9:30–16:15) with the SPXW cutoff at 16:00. An expiry day is then 0.962963 of a session, and 0.037 trading days of time value remain at 16:00 (dte.py L7, L83, L133). IV levels from the two repos are not directly comparable.

### 1.3 Greeks
- `src/convex_strategy/chain/pricing.py` `black76_greeks(...)` (L80): price, delta, gamma, vega, theta, rho. Conventions (docstring): delta and gamma against the forward, **not discounted**; vega per vol point, discounted; rho per 1%; **theta = one-trading-day repricing**, not the analytic derivative. Stored in `data/derived/chain/<day>.parquet` columns `call_delta, put_delta, gamma, vega, call_theta, put_theta, call_rho, put_rho`.
- **A second theta in the same repo:** `descriptive/positions.py` (header L17–20) and remote `features/sizing.py` `Day.greeks` use the Black-76 identity per minute, `0.5·iv²·F²·gamma / MINUTES_PER_YEAR`, because "The chain's stored theta is not used: it reprices one session later, which on expiry day is all the time value left." A harness must use the per-minute identity for 0DTE, not the chain column.
- Straddle Greeks at the forward: `smile/fixed_delta.py` `at_the_money()` (L87–129): `straddle_gamma = 2·gamma`, `straddle_vega`, `straddle_theta`.
- Tests: `tests/chain/test_pricing.py`, `tests/smile/test_fixed_delta.py`, `tests/descriptive/test_positions.py`.
- **Other copies:** `Backtest-Engine/src/chain/greeks.py` `bs_greeks` (L80; also vanna, volga, charm; theta = one-trading-day finite difference; delta `N(d1)` undiscounted, which agrees with the strategy repo); `delta-exchange-payoff/engine/src/deltapayoff/greeks.py`, `black76.py`, `black_scholes.py` (tests `test_greeks.py`, `test_black76.py`); `Convex-Hedge-Trading-Engine/.../chain/volatility.py` `Greeks` (L83), `black76` (L130).

### 1.4 Realised volatility (each estimator)

| Estimator | Where | Formula | Tests |
|---|---|---|---|
| Close-to-close, demeaned | `features/windows.py` `realised(level, start, end, step=1)` L82–98 | `std(ddof=1)` of `step`-minute log returns of the forward × √(MINUTES_PER_YEAR/step); empty below 80% of returns (`MIN_SHARE = 0.8`) | `tests/features/test_windows.py` |
| Root mean square, not demeaned | `smile/insights.py` `realised_vol(returns, step, from_left, to_left)` L64–74; `log_returns()` L48 | √(Σr² / years covered) per day | `tests/smile/test_insights.py` |
| Parkinson (day) | `descriptive/study.py` L143–144, column `range_vol` | `ln(H/L)/√(4 ln2 · OPEN_LEFT/MINUTES_PER_YEAR)` | `tests/descriptive/test_daily.py` |
| Parkinson (window) | remote `hyp_test_notebooks/_iv_parkinson.py` `parkinson(level, start, end)` L12–17 | √(ln(H/L)²/(4 ln2) · MINUTES_PER_YEAR/(start−end)); empty below 80% of minutes | none |
| HAR-style forecast | `descriptive/hedged_study.py` `iv_less_har()` L165–179 | mean of yesterday, 5-day and 22-day RV | `tests/descriptive/test_hedged_study.py` |
| Variance ratio (5m/1m) | `descriptive/hedged_study.py` `variance_ratio()` L182–203 | Σ(5-min r)² / Σ(1-min r)² | same |
| Multi-session span | `features/week.py` `realised_span()` L200 | — | `tests/features/test_week.py` |

- `MINUTES_PER_YEAR = 390 × 252` in `smile/insights.py`.
- **Disagreement:** `windows.realised` subtracts the mean (sample std); `insights.realised_vol` does not (RMS). They differ when a window trends. The 5-minute variant (`RV_STEP = 5`, windows.py L58) is "decision 0013".
- **Other repo:** `delta-exchange-payoff/engine/src/deltapayoff/realised_vol.py` has `log_return_vol` L97, `simple_return_vol` L109, `parkinson` L161, `garman_klass` L176, `rogers_satchell` L197, `scale_to_window` L218, `rolling` L370 (tests `engine/tests/test_realised_vol.py`). It drops returns that span a gap and reports how many it kept. Garman–Klass and Rogers–Satchell exist **only** in dxp.

### 1.5 IV − RV
- `features/windows.py` `with_features()` L236–288: `gap_{prev,same}[_5m] = iv_start − rv`, `pace = iv/rv`, `vr = (rv/iv)²`, `iv_change`, `var_window`, `iv_window` (the variance charged for the window alone, from IV at start and end; it describes only), `vr_window`. `_prev` is known at the window start. `_same` is not (same-period information).
- `descriptive/hedged_study.py` `early_vol_over_iv()` L156 (RV of the 9:35 half-hour / IV at 10:00) and `iv_less_har()` L165.
- Tests: `tests/features/test_windows.py`, `tests/descriptive/test_hedged_study.py`.

### 1.6 Smile and skew
- `smile/fixed_delta.py` `fixed_delta_smile(strikes)` L37: IV read at deltas `DELTAS = (5,10,15,20,25,30,40,50)` per side, by linear interpolation in delta; no extrapolation. `at_the_money(strikes)` L87: `atm_iv`, `implied_move = F·IV·√years`, `straddle` mid.
- Skew = put IV − call IV at the same delta: `smile/study.py` `study_day()` L54; `descriptive/study.py` `opening_skew()` L68–75 (25-delta at 9:35).
- `smile/stats.py`: `bucket_of`, `daily_values`, `bands`, `rank_among_other_days`. `smile/charts.py`: heatmaps, smile fan, day slider.
- Remote only: `notebooks/_credit_spread_skew.py` `skews()` L28 (`iv_skew_25/10`, `put_skew`, `call_skew`); `notebooks/_straddle_regimes.py` `_skews()` L28.
- Local only (branch `feature/anomaly-studies`): `features/sheets.py` `smile_minutes()` L158, `features/anomaly_smile.py`, `features/term.py` (term slope against the next expiry).
- Tests: `tests/smile/*`. Other repos: `delta-exchange-payoff/engine/src/deltapayoff/smile.py`; `Convex-Hedge-Trading-Engine/.../chain/skew.py`.

### 1.7 Straddle and window P&L
- `descriptive/positions.py` `pick_strikes(reading, target)` L53, `follow(...)` L66 (fill at the next minute; hedge = −delta of the earlier minute, at no cost), `hold_day()` L157, `breakeven_move()` L43.
- `features/windows.py` `window_day()` L167: 30-minute windows (`WINDOW = 30`, `STARTS` 9:35 to 15:05, `ROLLING` every minute). Seller's return as a share of premium, mid and spread forms, three hedges (none, every minute, a band of 1/6 or 1/2 of the implied move).
- `descriptive/hedged.py` `hedge_day()` L202, `_band_hedges` L130; local `features/bands.py` `band_hedges()` L149.
- Remote only: `features/sizing.py` `Day` class (L47; `strike_at`, `quotes`, `greeks`, `metric`), `window_starts(length)` L42, `LENGTHS = (5,10,15,30,60)`, `simulate`, `simulate_held`; `features/exit_rule.py` (`sell_once` L89, `run_day` L152, `closing_level` L81). `hypothesis/IMPLEMENTING.md` L51–66 lists these as "Readers to reuse (do not rewrite these)" and gives `long_trade()` (L70–88) as the standard fill.
- Local only: `features/structures.py` (`follow_legs` L67, iron fly and condor), `features/term.py`.
- Tests: `tests/descriptive/test_positions.py`, `test_hedged.py`, `tests/features/test_windows.py`, `test_bands.py`, `test_structures.py`; remote `tests/features/test_sizing.py`, `test_exit_rule.py`.

### 1.8 The bucket method and its tests
- `features/buckets.py` (the same file local and remote):
  - `edges(values, groups=GROUPS)` L37 and `assign(values, cuts)` L43: lines drawn on one sample (train) and applied to another. **`GROUPS = 4` (quartiles, "decision 0018"). No quintile code found.**
  - `cards(returns, bucket)` L54: windows, share, median, mean, win rate, profit factor, std, IQR, p05, tail mean, worst.
  - `compare(table, feature, returns, bucket, reshuffles=2000, seed=20261008)` L118–173: **day-reshuffle p-value** (the returns of one day are set against the features of another, slot for slot). Four statistics (`STATISTICS` L107): Spearman rank correlation, Kruskal–Wallis (centres), Brown–Forsythe/Levene (widths), **two-sample KS of top bucket against bottom bucket only**. It also reports "time of day alone" (the mean of the reshuffles).
  - `correct(p)` L176: Benjamini–Hochberg via `scipy.stats.false_discovery_control(method="bh")`.
  - Tests: `tests/features/test_buckets.py`.
- **Anderson–Darling** and **pairwise KS with Holm** are only in remote `hyp_test_notebooks/_metric_predicts_next_window.py` `tests()` L68–117: `stats.anderson_ksamp(groups)` L88 (comment "p capped to [0.001, 0.25]"); pairwise `ks_2samp` with a hand-written Holm, L82–86; pooled, per-day and time-of-day-adjusted Spearman, L90–96. No tests.
- `descriptive/hypothesis.py`: `reshuffled_p()` L83 (ordinary or block reshuffle, `SEED = 20261003`, `RESHUFFLES = 10_000`), `sign_test` L71, `rank_row` L151, `groups_row` (Kruskal–Wallis, or Mann–Whitney for two groups) L171, `spread_row` L197, `friedman_row` L221, `correct()` L244 (BH **and** Benjamini–Yekutieli). Tests `tests/descriptive/test_hypothesis.py`.
- Remote `notebooks/_straddle_regimes.py`: `bh()` L115, `kruskal_table()` L120, `wilson()` L135, `auc()` L142, `fit_logit()` L150, `block_ci(..., seed=20261015)` L169.
- Local `features/bands.py` `flip_p()` L426 (sign flip by day), `paired()` L442; `features/anomalies.py` `contrast()` L143 (day reshuffle).
- **Disagreements:** three seeds (20261003 in hypothesis.py, 20261008 in buckets.py, 20261015 in the workflow and IMPLEMENTING.md L18). The workflow says "quartiles or quintiles … Anderson-Darling … Kolmogorov-Smirnov pair by pair". The library does quartiles, KS top-against-bottom only, and no AD. Workflow step 3 is fully implemented only in the remote notebook helper.

### 1.9 Benjamini–Hochberg
Four copies, all through `scipy.stats.false_discovery_control`: `features/buckets.py` `correct` L176; `descriptive/hypothesis.py` `correct` L244 (BH + BY); remote `notebooks/_straddle_regimes.py` `bh` L115; `descriptive/hedged_study.py` `seventeen()` L308–319 (threshold `BAR` L87). Tested in `test_buckets.py` and `test_hypothesis.py`.

### 1.10 Results card: Sharpe, drawdown, Calmar
- **No library function exists.** The card is a code snippet in remote `hypothesis/IMPLEMENTING.md` L103–117, `card(daily, trades)`: Sharpe = mean/sd·√252 (no risk-free rate); `max DD = -(running - running.cummax().clip(lower=0)).min()` (the peak is floored at 0); Calmar = mean·252/DD; total % of 150k = `100*daily.sum()*100/150_000`; `p (mean > 0)` = one-sided `ttest_1samp`.
- The same formulas are in remote `scripts/long_straddle_after_wild_metric_window.py` L79–89. Each `hyp_test_notebooks/_*.py` helper re-implements its own card. No tests.
- **Disagreement:** `Backtest-Engine/src/analytics/summary.py` L19–22 and L140–155: Sharpe = (avg_daily − rf/252)/std·√252 (it subtracts a risk-free rate), plus Sortino; `_max_drawdown` L95; `run_metrics.py` `_max_drawdown_pct` L121, `TRADING_DAYS = 252` L47. Tests `Backtest-Engine/tests/analytics/test_summary_metrics_parity.py`, `test_metrics_parity.py`.

### 1.11 Half-day handling
- `features/windows.py` `closes_early(day, root)` L69–79, `EARLY_CLOSE = 30` L65: a day whose forward stops more than 30 minutes before 16:00 closed early. Docstring: "The chain maths counts every day's time to expiry to 16:00. On a day that closes at 13:00 that is wrong by three hours, and so is every implied volatility and Greek of that day."
- Build scripts drop and name such days: `scripts/build_windows.py` L13, `build_bands.py` L11, `build_smile_minutes.py` L11, `build_structures.py` L11, `build_term.py` L76; `features/week.py` `clear_of_early_closes()` L132.
- `quotes/loader.py` `load_day()` always counts `minutes_left` to 16:00 (`EXPIRY_TIME = time(16, 0)`), so half days get wrong IVs upstream. `data/history/derived/chain/2025-11-28.parquet` and `2025-12-24.parquet` exist with that wrong clock.
- IMPLEMENTING.md L33: "249 days, 2025-10-01 to 2026-09-30, early-close days already removed" (251 days on disk − 2 half days).
- **Disagreement:** `quotes/loader.py` L22 `HOLDOUT_START = date(2026, 8, 19)` refuses days on or after 19 Aug 2026 unless `include_holdout=True`. The current workflow splits train and test at 2026-04-01 and reads all of the test half. The loader's hold-out is left over from an earlier design.

## 2. Hypothesis workflow in the code

All files in this section are on **remote main only** (`MeghavPradeep/convex-hedge-strategy`@b4b174d). Status lines are dated 2026-10-15 and 2026-10-16.

### 2.1 File format and naming (as written)
- `hypothesis/README.md` L3–7: a hypothesis is "any testable claim about the market": a trading rule or a relationship. One file = one hypothesis, which may cover a family. Family members "differ only in a window length, a threshold, a lookback or one swapped metric, and each member's result is reported in its own row" (L11–13).
- Folders (README L15–19): `testing/` (every hypothesis starts here; untested or mixed evidence), `failure/` ("Shown not to work beyond reasonable doubt. The file stays so nobody tests it again by accident."), `success/` (a statistically significant effect of any kind that could be used).
- Names in `testing/` (README L42–47): `untested--<name>.md`, or `tested-r<N>--<name>.md` after N rounds. A file moved to `success/` or `failure/` drops the prefix. Names are kebab-case.
- Round records (README L47): every file in `testing/` has a `## Testing rounds` section that lists each round with the date, the notebook, the variants run and the key numbers. In practice each round is a `### Round N (YYYY-MM-DD): <what changed>` subsection.
- Status line: `**Status:** testing — tested 2 rounds (2026-10-16)`; `**Status:** success (2026-10-15, after round 1; relationship claim)`; `**Status:** failure (2026-10-15)`. IMPLEMENTING.md L146: move with `git mv` and update the Status line with the date.
- Notebooks (IMPLEMENTING.md L12): "One notebook per hypothesis file: `hyp_test_notebooks/hypothesis_<file name, with underscores>.ipynb`." Shared builders are `hyp_test_notebooks/_<topic>.py`. In practice, several older notebooks do not follow the `hypothesis_` prefix (for example `sell_late_day_pin_fly.ipynb`, `put_side_bias_and_risk_reversal.ipynb`).
- Results (IMPLEMENTING.md L15–17): "The notebook is the evidence; the file is the record." Copy the final tables into the file; name the notebook and the number of variants. Run end to end first with `uv run jupyter nbconvert --to notebook --execute --inplace hyp_test_notebooks/<name>.ipynb` (L21).
- Seed `20261015` for any bootstrap (L18). Public data such as FOMC dates: `hypothesis/data/fomc-days.csv`.

### 2.2 Shared rules (README L21–33, IMPLEMENTING.md)
- No look-ahead: decide on minutes up to the decision minute; fill at the next minute's quote.
- Prices: README says "Fills are at the mid." The workflow page (section 3) adds the spread-paid form whenever it could change the verdict. Recent files report both MID and SPREAD.
- Returns: dollars / fixed 150,000, summed, never compounded; multiplier 100.
- Instrument: one ATM SPXW 0DTE straddle (strike nearest the forward), unhedged unless the file says otherwise. Delta-hedged variant at the mid, free (IMPLEMENTING.md L92–96).
- Train 2025-10-01 to 2026-03-31; test 2026-04-01 to 2026-09-30 (`SPLIT = 2026-04-01`, IMPLEMENTING.md L34). 249 days; train 123, test 126 (from the pin-fly file).
- Same-period rule (README L35–40): any reading that uses information from the outcome period goes to `failure/` "however significant it is".
- Results card: IMPLEMENTING.md L98–120 (see 1.10). Report for train and test separately for every variant; apply `correct` (BH) to test-half p-values across the family.
- Relationship claims (IMPLEMENTING.md L122–129): the statistic is named in advance, reported on both halves with p-values corrected across the family, standard errors across days not minutes, and a check with the time-of-day pattern removed.

### 2.3 Pass bar — two versions that disagree
- **IMPLEMENTING.md L131–140 (the code repo):**
  - `success/`: "At least one variant has a test-half corrected p below 0.05 **and** a positive mean on the train half. Or the file's named statistic … is significant after correction on **both** halves."
  - `failure/`: same-period information; or every variant has test-half mean ≤ 0 **and** the train half agrees (no variant with corrected p below 0.10); or the file's own "What would kill it" condition is met.
  - Otherwise stays in `testing/`. "Choosing the best variant on the test half is not allowed: pick on the train half, then read its test row once."
- **`sources/Strategy research workflow.md` section 2 (dated 2026-10-17, newer):** a strategy is judged on **one** variant only, the one with the best Sharpe on the train half; it succeeds when its test-half mean is positive, significant after correction, **and** it still makes money with the spread paid; a filter must also beat the same trade without the signal.
- The two disagree. IMPLEMENTING.md's "at least one variant" rule lets a variant pass that was not the train pick. The pin-fly file (round 2) shows the conflict: "One variant (condor 15:00, L=60, >1.0) meets the letter of the success rule … But … it was not picked on train. It stays in `testing/`."

### 2.4 Current hypotheses by folder (titles only; 24 files)
**testing/ (14)**
- `tested-r1--buy-after-a-quiet-open.md` — Buy the straddle after a quiet opening range
- `tested-r1--buy-after-put-skew-spike.md` — Buy the straddle after a jump in put skew
- `tested-r1--buy-into-the-close.md` — Buy the straddle late in the day, into the close
- `tested-r1--buy-the-opening-burst.md` — Buy the straddle at the open and sell it within the first hour
- `tested-r1--buy-when-implied-variance-is-below-realised.md` — Buy the straddle when implied variance is below recent realised variance
- `tested-r1--buy-when-straddle-is-cheap-against-implied-move.md` — Buy the straddle when its price is cheap against the implied move
- `tested-r1--iv-minus-parkinson-rv-predicts-next-window.md` — IV minus Parkinson RV of a window predicts the straddle return of the next window
- `tested-r1--metric-at-window-start-predicts-straddle-return.md` — The metric known at a window's start predicts the seller's straddle return over the window
- `tested-r1--opening-range-fade-and-intraday-momentum.md` — Opening-range fade (H8) and intraday momentum (H9)
- `tested-r1--put-side-bias-and-risk-reversal.md` — Put-side bias and risk reversals (H6) and put-heavy iron flies (H7) (Status: "Not committed.")
- `tested-r1--sell-after-iv-spikes.md` — Sell a fresh 0DTE straddle or fly right after an intraday IV spike
- `tested-r1--sell-morning-straddle-with-exits-and-filters.md` — Sell the morning straddle, with move exits and two filters
- `tested-r1--sell-open-iron-condor-with-stops.md` — Sell a short-delta iron condor at the open, with a stop
- `tested-r2--sell-late-day-pin-fly.md` — Sell a late-day iron fly or iron condor (the pin)

**success/ (4, all relationship claims)**
- `intraday-mean-reversion-of-put-skew.md` — Put skew mean-reverts within the day
- `intraday-mean-reversion-of-straddle-price-against-implied-move.md` — The straddle's price against the implied move mean-reverts within minutes
- `intraday-mean-reversion-of-the-index.md` — The index mean-reverts slightly over 5 to 30 minutes
- `realised-volatility-persists-and-iv-follows-it.md` — Realised volatility persists between windows, and implied volatility already follows it

**failure/ (6)**
- `buy-after-wild-metric-window.md` — Buy the straddle after a wild window of delta² / (2 gamma) over theta
- `buy-before-scheduled-macro-releases.md` — Buy the straddle before a scheduled macro release
- `buy-when-iv-and-rv-decouple.md` — Buy the straddle when IV and RV stop moving together
- `buy-when-iv-jumps-before-the-index-moves.md` — Buy the straddle when IV jumps before the index has moved
- `sell-put-skew-spikes-with-hedged-risk-reversal.md` — Sell put-skew spikes with a delta-hedged 25-delta risk reversal
- `window-iv-minus-rv-explains-its-own-straddle-return.md` — The IV − RV gap of a window explains the straddle's return over that same window (same-period rule)

`hyp_test_notebooks/` holds 20 notebooks and 14 `_*.py` helpers (list in remote tree; for example `hypothesis_intraday_mean_reversion_of_put_skew.ipynb`, `_metric_predicts_next_window.py`, `_put_skew.py`, `_straddle_ratio.py`).

### 2.5 Template: exact section headings of one file
`hypothesis/testing/tested-r2--sell-late-day-pin-fly.md` (157 lines):
```
# Sell a late-day iron fly or iron condor (the pin)
**Status:** testing — tested 2 rounds (2026-10-16)
## Hypothesis
## Mechanism
## Who is on the other side
## Rules
## Family
## What would kill it
## Results
## Testing rounds
### Round 1 (2026-10-15)
### Round 2 (2026-10-16): IV-rich filter
## Verdict
```
- `## Family` states the count used for BH ("4 entries × 3 structures = 12 hold variants, plus 2 move-exit variants = 14, plus the baseline … = 15 rows in each BH correction").
- `## Results` names the notebook and helper, day counts per half, the MID and SPREAD definitions, a table with columns `Days traded | Mean | Sharpe | Calmar | Max DD | Worst | Total % | $/trade | p corr`, and a **Sanity** paragraph that works one trade by hand.
- Other files add `## Implementation` (instructions for the implementer), `## When to move it`, `## Evidence so far`, `## What is still in doubt`, `## Pass bar (fixed in advance)`, `## Sanity checks`. Relationship claims use `## Claim` in place of `## Hypothesis`.

## 3. Data held

### 3.1 What is on disk (local, `D:\Convex Hedge\convex-hedge-strategy\data\`)

| Folder | Content | Schema / columns | Range | Days | Size |
|---|---|---|---|---|---|
| `SPXW/` | same-day SPXW quotes + definitions, `spxw-<day>-cbbo-1m-expiry-<day>.parquet` and `spxw-<day>-definition.parquet` | Databento OPRA `cbbo-1m`: `ts_event, rtype, publisher_id, instrument_id, side, price, size, flags, bid_px_00, ask_px_00, bid_sz_00, ask_sz_00, bid_pb_00, ask_pb_00, symbol, ts_recv`; `definition`: 40+ columns incl. `instrument_id, raw_symbol, instrument_class, strike_price, expiration, contract_multiplier` | 2026-03-31 to 2026-09-30 | 127 | 414 MB |
| `history/SPXW/` | same layout | same | 2025-10-01 to 2026-03-30 | 124 | 327 MB |
| `week-ahead/SPXW/` | `spxw-<day>-cbbo-1m-week-ahead.parquet`: expiries 1 to 7 calendar days out, strikes within 5% of the day's ATM | `cbbo-1m` | 2025-10-02 to 2026-09-30 | 249 | 1.3 GB |
| `ES/es-ohlcv-1m.parquet` | ES front-month (`ES.v.0`), all hours | `ohlcv-1m`: `open, high, low, close, volume, symbol, ts_event` | 2024-04-01 00:00 to 2026-09-30 23:59 UTC | 886,751 bars | 14 MB |
| `derived/` and `history/derived/` | built tables: `chain/<day>` (minute × strike: `ts, minutes_left, strike, call_bid, call_ask, put_bid, put_ask, forward, years, iv, otm_right, call_delta, put_delta, gamma, vega, call_theta, put_theta, call_rho, put_rho`), `minutes/<day>`, `descriptive/`, `features/` (`windows`, `windows_rolling`, `window_minutes`, `sessions`, `week_readings`, `bands*`, `smile_minutes`, `structures`, `term`), `smile/` | — | same days | 127 + 124 | 372 MB + 254 MB |

- Example day 2026-04-01: 199,041 quote rows, 536 instruments, stamps 13:31 to 20:02 UTC.
- Same-day total: **251 days** on disk, 2025-10-01 to 2026-09-30. Two are half days (2025-11-28, 2025-12-24); the studies use **249**.
- Holidays recorded in the ledger `no_data`: 2025-11-27, 2025-12-25, 2026-01-01, 2026-01-19, 2026-02-16; also `week 2026-08-25`.
- `data/SPXW/` and `data/ES/` are tracked in git on the local branch (`git ls-files data` lists them). On GitHub `main`, `data/history/SPXW/` (124 cbbo files), `data/derived/`, `data/week-ahead/` are also committed. This contradicts the workflow page ("Market data | `data/`, never committed").
- **Second copy, engine format:** `D:\Convex Hedge\Backtest-Engine-data-spike\Data\` (1.2 GB): `greeks_v7/asset=SPXW/date=<day>/expiry=<day>/greeks.parquet` for **251 days**, 2025-10-01 to 2026-09-30, and `index/asset=SPXW/index.parquet` (1.3 MB). This is the Backtest-Engine's hive layout (its chain clock is 405 minutes, see 1.2). The main `Backtest-Engine` checkout has no `Data/` folder. `Backtest-Engine-data-spike` is a worktree at `2a839e7d` (2026-10-12).

**Nothing is held for 2024-07-01 to 2025-06-30 for SPXW options.** Only the ES futures one-minute bars cover that range. The range has 261 weekdays; my count of NYSE holidays (11, including the 2025-01-09 day of mourning) gives about 250 sessions, of which 3 are half days (2024-07-03, 2024-11-29, 2024-12-24). This count is mine, not from the repo.

### 3.2 The downloader: `scripts/databento_download.py` (354 lines; tracked on remote main, 14,262 bytes both sides)
- Run line (docstring L3–5): `uv run --env-file .env --with databento python scripts/databento_download.py`. The key comes from `.env`, so **Lalit must start any real run** (deny rule).
- Arguments (L327–338):
  - `--only {es,history,week}` — one part; default runs `history` then `week`.
  - `--max-usd FLOAT` — default `300.0`; "stop before this total".
  - `--dry-run` — "make no request".
  - `--since YYYY-MM-DD` — default `2025-10-01` (`HISTORY_START`).
  - `--workers INT` — default 3.
- **There is no end-date argument.** `HISTORY_END = date(2026, 3, 30)` is a constant (L54). `download_history` (L276–285) asks for every weekday from `--since` to 2026-03-30, newest first, and skips days whose definition file exists or that are in `no_data`.
- **Dry run** (`dry_run()` L313–320): prints the number of weekdays from `--since` to 2026-03-30 and the week-ahead contract count for about six sample days on disk. **It prints no price.** There is no estimate-only mode.
- **Cost cap**: every request is priced first with `client.metadata.get_cost(...)` (L100–103). The run raises `Budget` and prints `STOPPED: …` before the total would pass `--max-usd` (L104–111). The total is the **whole ledger sum** (`spent`, L88–90) plus requests in flight, so the cap must include the $3.44 already spent.
- Files are written whole or not at all (`.part` then rename, L166–171); a file on disk is never asked for again; prices go into `data/databento-ledger.json`.
- Holidays answer HTTP 422 "could not be resolved" and are recorded in `no_data` (L255–260).

### 3.3 Commands for 2024-07-01 to 2025-06-30 (not run)
- **(a) Estimate.** No command gives a dollar estimate. The nearest:
  - `uv run python scripts/databento_download.py --dry-run --since 2024-07-01` — no key needed, no request; prints the weekday count only (it will report the span to 2026-03-30).
  - A priced probe that stops at the first paid request: `uv run --env-file .env --with databento python scripts/databento_download.py --only history --since 2024-07-01 --max-usd 3.45 --workers 1`. With $3.44 in the ledger, the first day that costs more than $0.01 stops the run, and the `STOPPED` line prints that day's price. A day cheaper than $0.01 is downloaded before the stop. Lalit must run it.
  - A true range estimate needs a small new script that calls `metadata.get_cost` for each day. Not present.
- **(b) Download.** `uv run --env-file .env --with databento python scripts/databento_download.py --only history --since 2024-07-01 --max-usd <cap>`. Because `HISTORY_END` is fixed, this also asks for **2025-07-01 to 2025-09-30** (66 more weekdays) and writes into `data/history/SPXW/`. To stop at 2025-06-30, the constant at L54 (or a new `--until` flag) must change. Drop `--only history` to also fetch week-ahead quotes for each new day.

### 3.4 Prices for data older than 12 months
- The code says nothing about the 12-month rule. It prices every request at run time.
- The ledger shows the rule in effect (downloads of 7–8 Oct 2026): every same-day and definition file from 2025-10-06 onward cost **$0.00**. The three oldest days, then just over 12 months old, cost: `same-day 2025-10-01` $0.0233, `2025-10-02` $0.0227, `2025-10-03` $0.0292; `week 2025-10-02` $0.0639, `week 2025-10-03` $0.0669. Definition files cost $0.00 even for those days. ES 2.5 years cost $3.24. Ledger total $3.443.
- `data/databento-download.log` last lines: "STOPPED: week 2025-10-01 costs $0.07; $3.44 is spent and the limit is $3.50."
- Extrapolation (mine, not in the repo): at about $0.025 per same-day file, 250 sessions ≈ $6; week-ahead at about $0.065 per day ≈ $16. Older 2024 days have fewer strikes, so the real figure may be lower or higher. Memory note: Lalit said the account has a spending limit; ask before any run that could pass a few dollars.

## 4. dxp docs format (`delta-exchange-payoff/docs/`, `main`@fce8d39)

### 4.1 Page types
| Type | Files | Pattern |
|---|---|---|
| Start-here pages | `maths-start-here.md` (263 lines), `storage-start-here.md` (199), `split-start-here.md` (122) | Open with a runnable command ("Print all three for a live chain, right now:" + `curl …`) or "**Read this before you read any other document about the services.**" Then a quoted "Reference doc." block that names where the evidence lives. Numbered parts as `# 1 · The forward`, each with `## What it is`, `## The identity it rests on`, `## What we run`, `## The trap — …`. Ends with `## Word list` and `## The three rules that stop a wrong number looking right`. |
| Contracts | `chain-contract.md`, `live-chain-contract.md`, `historical-chain-contract.md`, `smile-contract.md`, `bars-contract.md`, `recording-contract.md` | `# The \`/chain\` contract`, then one paragraph: "The interface between the engine and the web app. Both are built against this file, so it is fixed before either exists. Change it by changing this file first." Sibling links. One `##` per route (`## \`GET /chain?underlying=BTC&expiry=04-09-2026\``), `### A leg` field tables, `## Rules that are not negotiable`, `## Errors`. |
| Research / verdict pages (root) | `forward.md`, `implied-vol.md`, `greeks.md`, `iv-vs-rv.md`, `index-history.md`, `delta-api-scope.md`, `settlement.md`, `ingestion.md`, `storage.md` | Title is the finding ("Four forwards, and what the chain says about them"); first line is **`**Verdict: …**`** with the key number in bold. |
| `design/` (94 files) | `hld.md`, `hld-evidence.md`, `events.md`, `instruments.md`; `lld/*.md` (one per module, "— low-level design"); `cloud/*.md` with `*-numbers.md` twins; `execution/00-overview.md` + one page per part; `decisions/000N-*.md` (ADRs); `research/000N[a-c]-*.md` (evidence per decision, plus raw `.log`/`.json`) | Design phase pages: "Everything here is a **decision, not a description**: none of it is built yet." |
| `final-design/` (15 files) | `index.md`, `overview.md`, `getting-started.md`, `glossary.md`, `architecture.md`, `data-flow.md`, `events.md`, `message-bus.md`, `adapters.md`, `adding-an-adapter.md`, `data-store.md`, `logging.md`, `deployment.md`, `configuration.md`, `api-reference.md` | Newcomer register. `index.md` has a table "If you are... / Read, in this order" and a "What is on each page" table in three groups. |
| Handoff | `handoff.md` ("# Handoff — 2026-09-17") | `## Start here`, `## In flight`, `## What changed this session`, `## Decisions made`, `## Open questions`, `## Traps found`, `## Read these`. |
| Split notes | `split-start-here.md`, `split-numbers.md`, `split-what-to-do-next.md` | "start here" / "numbers" (evidence only) / "what to do next" (open tickets only; "The GitHub issues are the state of record"). |
| Specs | `superpowers/specs/2026-09-0N-<name>-design.md` (4 files) | Dated, one contract each, cut into tickets. |
| Superseded legacy | `architecture.md` | Top line `> Superseded by [design/hld.md](design/hld.md) and [design/events.md](design/events.md).` |

### 4.2 Front matter and heading pattern
- **No YAML front matter** on any page under `dxp/docs/` (checked: no file starts with `---`). This differs from the Strategy-Research vault, whose pages open with `type: / status: / updated:` YAML (for example `sources/Strategy research workflow.md`).
- One `#` title per page (start-here pages use extra `#` for numbered parts). The opening is bold labelled lines, not a summary heading:
  - final-design and execution pages: `**What this page contains.** …` then `**How to read it.** …` (`final-design/overview.md` L3–10; `design/execution/00-overview.md` L3–9).
  - decision records: `# 0001 — Stream naming and payload format`, then `**Status** decided, #58, 2026-09-09. **Supersedes** nothing. **Fills** [...]. **Evidence** [...]`, then `## The question`, `## The options`, `## The decision`, `## Why, in the criteria's order`, `## Rejected, and why`, `## What would change this decision`. Partial supersession is a quoted line at the top.
  - research pages: `**Verdict: …**` first.

### 4.3 Writing rules
- dxp has **no separate style-guide file** under `docs/`. The rules are in `AGENTS.md`:
  - L10: "The words this repository uses are `CONTEXT.md`. Look a term up there before you write it."
  - L86–132: "**Documentation notes stay under 200 lines.** Split rather than overflow, unless named exempt below with a reason", with a measured exemption list; `engine/tests/test_doc_render.py` parses every Markdown file under `docs/`, and `test_doc_bounds.py` checks the bound.
  - L144: "Numbers are tagged `measured`, `assumed` or `derived`, with the run that produced them. Never quote a figure from a doc as if you observed it." (`split-numbers.md` L3 repeats it.)
- `design/execution/00-overview.md` L82–91 "The rules every page follows" are design rules, not writing rules.
- The house writing guide that dxp's later pages follow is the feature-loop skill's `prompts/docs-style.md` (section 5): the two opening lines, **Status.** on design pages, bold terms that resolve to `CONTEXT.md`, mermaid diagrams, fixed table columns, a closing **Reading order**, and no secrets or attribution lines.
- Memory "Write for a newcomer": design pages use the final-design register.

### 4.4 Diagrams
- **No Excalidraw, SVG or PNG** in `dxp/docs/` or in any dxp branch (`git ls-tree -r` over every ref finds none).
- Diagrams are **Mermaid code blocks** inside the page: all nine `design/execution/*.md` pages have one or two ```` ```mermaid ```` blocks (for example `00-overview.md` "## The whole machine, in one picture").
- `final-design/architecture.md` L22–68 uses a plain-text box drawing in a bare ```` ``` ```` block ("DELTA EXCHANGE (the venue, on the internet)" with `|` arrows). `maths-start-here.md` L21–31 uses a small text block (`1. FORWARD ← from prices`).
- The Trading-Engine repo also has no `.excalidraw` files. Excalidraw output exists only as the gstack `diagram` skill's ability (source + `.excalidraw` + SVG + PNG); no repo uses it yet.

### 4.5 How docs link to code
- Backticked repo-relative paths: `` `engine/src/deltapayoff/controller.py` `` (`design/lld/commands.md` L7–8, `design/lld/chain-cache.md` L3).
- File plus line range in backticks: `` (`store.py:376-382`) `` (`design/decisions/0009-compaction-cadence.md` L45), `` `controller.py:662-674` `` (`design/lld/reconnect.md` L175), `` `main.py:1282` ``.
- Relative Markdown links to code: `[`engine/src/deltapayoff/store.py`](../../../engine/src/deltapayoff/store.py)`, `[`engine/tests/test_cloud_numbers.py`](../../engine/tests/test_cloud_numbers.py)`.
- Commits and issues inline: "Landed by #37", "`4209ec2` (#54)", "**passes as of `2725da7`**".
- Docs to docs: relative links only (`[chain-contract.md](chain-contract.md)`, `[Glossary](../../final-design/glossary.md)`).

### 4.6 Two skeletons

**A. Design page (final-design / execution register)**
````markdown
# The execution half: overview

**What this page contains.** A picture of the whole system once it can trade, a description of each
new part, and the rules that every other page in this folder follows.

**How to read it.** Read the first two sections, then follow the reading order at the bottom. Words
in **bold** on first use are defined where they appear, and again in [Glossary](../../final-design/glossary.md).

## The whole machine, in one picture
```mermaid
flowchart LR
  A["Strategy worker"] --> B["OMS"]
```
What to notice: …

## The new parts, one at a time
| Part | What it does | What it deliberately does not do |
## The rules every page follows
1. **A strategy publishes a position in units, never an order.** … [books.md](books.md).
## Reading order
1. [books.md](books.md) — …
## To review
## What is out of scope, on purpose
````

**B. Research / verdict page**
````markdown
# Implied volatility: two models, four solvers, four forwards

**Verdict: the solver does not matter and the forward does.** Across 295 solved strikes on
eight expiries, the four solvers agree to **2.5e-05 vol points** … (`measured`, run …)

## What was compared
## Method                      <- links to `engine/src/deltapayoff/solvers.py` and the test file
## Results                     <- tables; every number tagged measured / assumed / derived
## The trap
## What this changes           <- decision link: design/decisions/000N-….md
````

## 5. The feature-loop skill (`C:\Users\Acer\.claude\skills\feature-loop\`)

Files: `SKILL.md` (112 lines), `workflow.md` (201), `herdr.md`, `prompts/` (`audit`, `auditor`, `design`, `docs-style`, `flow-check`, `gaps`, `grill`, `handoff`, `implementer`, `orchestrator`, `waves`), `scripts/` (`context-guard.py`, `dashboard.mjs`, a test), `templates/` (`claude-md-section.md`, `docs-agents/{domain,handoff,issue-tracker,triage-labels}.md`, `settings.json`). Modes (SKILL.md L5): `setup | design | plan | orchestrate <feature issue> | gaps | audit [<feature issue>] | dashboard`. `disable-model-invocation: true` — only the user can start it.

### 5.1 `setup` (SKILL.md L21–59) — prepare a repo; safe to re-run
1. Detect the stack and fill `{{SETUP_WORKTREE}}`, `{{TYPECHECK}}`, `{{LINT}}`, `{{ONE_TEST}}` (with `<path>`), `{{FULL_SUITE}}`, `{{RUN_APP}}`, `{{APP_URL}}` (`none` without a web UI), `{{REPO}}`. Ask the user once for unknowns.
2. Append `templates/claude-md-section.md` to `CLAUDE.md` between `<!-- feature-loop:start -->` and `<!-- feature-loop:end -->` (commands table + docs-layout table).
3. Copy, keeping existing files: `docs/agents/*.md` (domain, handoff, issue-tracker, triage-labels); `scripts/claude/context-guard.py` (harness-owned, overwritten when different); `.claude/settings.json` (two context-guard hooks + `attribution` blanked); add `.claude/worktrees/` and `.playwright-cli/` to `.gitignore`.
4. GitHub labels: `feature`, `ticket`, `in-progress`, `ready-for-agent`, `ready-for-human`, `needs-info`, `needs-triage`, `wontfix`, `audit`.
5. Run Matt Pocock's `setup-matt-pocock-skills` (adds an `## Agent skills` block to `CLAUDE.md`, or to `AGENTS.md` only when no `CLAUDE.md` exists — it "Never create[s] `AGENTS.md` when `CLAUDE.md` already exists").
- **AGENTS.md is not created or required by feature-loop.** It appears only through step 5's rule.

### 5.2 `design` (SKILL.md L61–70; `prompts/design.md`) — the whole product, user present
- Branch `docs/design-<yyyymmdd>`; ends with PR "Design: <product>". Writes **no spec, ticket or code**.
- Creates `docs/design/`: `00-overview.md` (opening lines, **Status.**, one paragraph, one mermaid picture of every part, parts table, numbered rules, **Reading order**), one page per part, `grilling-log.md` (`## Round <n>: <topic>` + `# | Question | Decision | Why`, `Q#` never renumbered, a `flowchart LR` of rounds), `decisions/NNNN-<slug>.md` for HARD-TO-CHANGE decisions, `build-order.md` (feature table `# | Feature | Contains | Done when` + dependency flowchart + a "Parked, built on demand" table), `research-gaps.md` (via `gaps`); research notes `docs/research/<topic>.md`; terms into `CONTEXT.md` as `**Term** — definition.`
- Steps: 1 Start (extend an existing design; for an existing product with no design, first describe what is built), 2 Shape (two or three candidate shapes, user picks), 3 Grill in rounds, 4 Research, 5 Write pages, 6 Feature list, 7 Gaps, 8 Approve and open the PR.

### 5.3 `plan` — Phase A, user present (`workflow.md` L12–74)
1. **Branch** `feature/<slug>` off `main` (or a worktree `../<repo>.worktrees/feature-<slug>`).
2. **Design check.** With `docs/design/`, run **Slice mode** of `prompts/grill.md` (reads `00-overview.md`, `build-order.md`, `grilling-log.md`, `decisions/`, `research-gaps.md`; recommends the earliest unbuilt step with no spec and no `feature` issue; flags open RESEARCH/SPIKE gaps) and append the round to `grilling-log.md`. Without a design and with more than one feature ahead, it recommends `/feature-loop design` first.
3. **Grill** (no design route): rounds written to `docs/specs/<slug>.md` (`Status: planned` first line) as `# | Question | Decision | Why`; terms to `CONTEXT.md`; decisions to the decisions folder.
4. **Research** with `/mattpocock-skills:research` → `docs/research/<slug>.md` (docs-style format, mermaid where there is a flow).
5. **Grill again** until the frontier is empty.
6. **Spec** with Pocock `to-spec`: a GitHub issue labelled `feature` + `ready-for-agent`, opening with a "Plain-language summary", ending with **Assumptions**; the same spec in `docs/specs/<slug>.md` in house format with at least one mermaid diagram; committed on the feature branch.
7. **Tickets** with Pocock `to-tickets`: sub-issues labelled `ticket` + `ready-for-agent`, native blocked-by edges, plain-language summary first.
8. **Waves** (`prompts/waves.md`): name each ticket's areas (modules or directories), apply the wave rule, post `## Implementation plan` (`| Wave | Ticket | Areas | Blocked by |`) on the feature issue.
9. **Approval**: one message with spec link + wave table; one approval starts the build and lets it merge into `main` itself.
10. **Launch**: write the orchestrator hand-off (`prompts/handoff.md`, format `docs/agents/handoff.md`) and run `node ~/.claude/accounts/cx.mjs run --detach yes --name orch-<slug> --cwd "$PWD" --model opus --effort medium --prompt-file TMP/feature-loop-orch-<slug>.md`; start the dashboard (`scripts/dashboard.mjs --detach`, `http://127.0.0.1:8765`).

### 5.4 `orchestrate <feature issue>` — Phase B, unattended (`prompts/orchestrator.md`)
- Normally started by `plan`; typed only to resume. Startup (L29–45): resume from `TMP/feature-loop-<slug>.json` or a hand-off; read the feature issue and its `## Implementation plan` comment, every ticket, `docs/specs/<slug>.md`, and the `CLAUDE.md` section; **check** it is on `feature/<slug>`, the tree is clean, and the `CLAUDE.md` section has no `{{` left — otherwise stop.
- One `cx run` worker per ticket in its own worktree (tiers `sonnet-high` / `opus-medium` / `opus-high`), reviewer subagents `fl-opus-medium` / `fl-opus-high`, one flow check in the running app, one PR per feature, auto-merge when every ticket is closed, the suite is green and the flow check passed. Only 1 implementer while Docker runs. Phase C cleans branches after the merge.
- Context budget: hand off at 40%, never past 45% (`context-guard.py` hook).

### 5.5 What a repo needs before `plan` can run
- A git repo with a `main` branch and a GitHub remote (`gh` works; labels exist). Issues, sub-issues and blocked-by edges are on GitHub.
- `/feature-loop setup` done: the `CLAUDE.md` marker section with **every** `{{…}}` filled (the orchestrator refuses otherwise), `docs/agents/` files, `.claude/settings.json` hooks, `scripts/claude/context-guard.py`.
- `CONTEXT.md` at the root (created on first term if missing; "A missing file means nothing has been recorded yet").
- Strongly recommended for a multi-feature product: `docs/design/` from `/feature-loop design` (with `build-order.md`), then `/feature-loop gaps` before the first plan.
- Pocock skills installed (`research`, `to-spec`, `to-tickets`, `setup-matt-pocock-skills`); `~/.claude/accounts/cx.mjs` for workers.

### 5.6 State of the target repos
- `convex-hedge-strategy` has `docs/agents/` (domain, handoff, issue-tracker, triage-labels) and a context-guard hook (`python3 "$CLAUDE_PROJECT_DIR/scripts/claude/context-guard.py"`), but **no `feature-loop` marker section** in `CLAUDE.md`. Its `CLAUDE.md` holds an older inline workflow (`## The feature workflow` L130, Phase A/B/C, `## Herdr recipes` L318) and `## Documentation rules (the vault)` L271. A new harness repo would need `setup` (and `design`) first.
- `Backtest-Engine/CLAUDE.md` has no marker section either.

## 6. The two dashboards (`sources/hypernova_edge_dashboard.html`, `sources/nova_edge_dashboard.html`)

### 6.1 What they are
- Both files have 965 lines. Lines 1–335 and 339–965 are **identical** except the name ("Hypernova Edge" against "Nova Edge"). Line 337 `chartData` (about 4.0 MB), line 338 `perfData` (about 0.46 MB) and line 339 `distData` (30 KB) hold the data. Plotly 2.27.0 from CDN.
- Title (L5): "Combined Regime Analysis - Hypernova Edge". H1 (L234): "Hypernova Edge - Regime Analysis Dashboard". Subtitle (L235): "Combined Volatility + Trend Regime Analysis across 90 Feature Combinations".
- **What they study:** the weekly P&L of two of the desk's live strategies, "Hypernova Edge" and "Nova Edge", split by a market regime. The HTML does not say what the strategies trade. `sources/07-10-26-images.md` says the page is Bilal's (`Quant/Markov-Models/Model_Validation/Alpha_Validation/Combined_Strategy/Reports/hypernova_edge_dashboard.html`) and that "the strategy is a trend strategy". The 7 Oct recap mentions "short straddles and short iron flies, presets". About 53–60 trades a week in every regime.
- Data: 263 weekly rows, 2021-01-01 to 2026-01-21. `pnl_pct` is weekly P&L in percent. `cumulative_pnl` is the **simple sum** of weekly P&L (checked). `log_cumulative` is Σ ln(1 + r/100) (compounded; checked on the first row). `drawdown` is weekly, from the simple-sum curve.
- Default combination (L955–959): `vol_yz`, `hurst`, window 50, daily, `dominant_regime`. Hypernova at that setting: mean weekly 1.77%, sd 2.21%, worst week −6.92%, best +7.42%, total 464%, worst drawdown −8.0%. Nova: mean 1.05%, sd 1.19%, worst −3.34%, total 276%.
- The regime labels are **identical in both files** (checked for all 180 combinations). The regime is a property of the market, not of the strategy. Only the P&L differs.
- The 7 Oct screenshot numbers (regime 0: 148.4%, 79 weeks) do not match the default view of this file (regime 0: 80.2%, 50 weeks). The screenshot used another selection or an older build.

### 6.2 Controls (L237–258)
- Volatility model (6): `vol_simple`, `vol_log`, `vol_parkinson`, `vol_rs` (Rogers–Satchell), `vol_yz` (Yang–Zhang), `vol_garch`.
- Trend model (3): `hurst`, `efficiency_ratio`, `durbin_watson`.
- Window (5): 10, 20, 50, 100, 200 bars. Combination key `getComboName` (L364–366): `${vol}_${window}__${trend}_${window}` — the vol and trend windows are always equal. 6 × 3 × 5 = **90 combinations**.
- Timeframe (2): Daily, Hourly — the bars the regime is computed on. The weekly P&L is the same for both (checked).
- Regime approach (2): **Starting Regime** (the regime at the start of the week) and **Dominant Regime** (the regime that holds most of the week).
- Regime background checkboxes and a date range filter (affect only the cumulative chart).

### 6.3 Every chart and table
1. **Metric cards**, one per regime (L533–558): total P&L %, weeks, win rate, profit factor, max drawdown %, number of drawdown periods, total trades, average trades a week.
2. **"Regime Distribution"** donut chart (L560–583): share of weeks in each regime.
3. **"Total PnL % by Regime"** bar chart (L585–607).
4. **"Log Cumulative Returns with Drawdown Overlay"** (L661–803): the log cumulative line, the drawdown on a reversed second axis, and the regime of each week as a coloured background band (opacity 0.15); side notes "Regime: n DD".
5. **"Win Rate by Regime"** bar chart (L610–625).
6. **"Avg Win vs Avg Loss by Regime"** grouped bars (L627–658).
7. **"Return Distribution (PDF) by Regime"**: four Gaussian-KDE density curves of weekly P&L, one per regime (L805–880), with a dashed line at 0 and a "Mean / Median" note. Bandwidth = Silverman, 1.06·σ·n^(−1/5) (L443); σ is the population std (L457–462).
- **There is no statistical test** on the page: no p-value, no confidence interval, no comparison between regimes, no train/test split.

### 6.4 How the regimes are split
- Four regimes (L260–276, L348–353): 0 Low Vol + Choppy, 1 Low Vol + Trending, 2 High Vol + Choppy, 3 High Vol + Trending. `-1` = undefined (first week).
- **Measure:** high or low volatility from the chosen volatility estimator over the chosen window of daily or hourly bars; trending or choppy from Hurst exponent, Kaufman efficiency ratio or Durbin–Watson over the same window.
- **Threshold: not in the file.** The labels arrive pre-computed in `chartData[...].starting_regime` and `.dominant_regime`; the JavaScript only colours and groups them. Evidence from the data:
  - The share of high-vol weeks varies by model from 0% to 100% (for example daily `vol_parkinson` and `vol_rs` at window 100 = 100%, at window 200 = 0%; daily `vol_yz` 45–51%; hourly `vol_yz` window 100 and 200 = 100%). So the cut is **not** a median of the series being cut. A fixed level, or a cut set on a different scale, fits the 0% and 100% cases.
  - `vol_garch` gives the same 45.4% high-vol share (daily) and 42.0% (hourly) at every window, while its labels differ between windows in 131 of 263 weeks.
  - With a 200-bar window, a regime is already defined in the second week (2021-01-08). So either data before 2021 was used to warm up, or the whole sample was used.
- **Known at decision time?**
  - `dominant_regime`: **no.** It is the regime that held most of the week whose P&L it explains. This is same-period information (look-ahead). It is the page's **default** (L959).
  - `starting_regime`: possibly, if it uses only bars closed before the week's first trade. The file does not show this.
  - The threshold: unknown. If it was set on the whole 2021–2026 sample (for example a full-sample quantile, or one GARCH fit over all data), every label carries look-ahead.

### 6.5 How the page judges a feature
By eye: does the strategy's P&L curve, total, win rate, average win/loss and weekly P&L density **differ between regimes**? The meeting framing (7 Oct transcript L445–448, garbled): "Are the return distribution characteristics different. That is when regimes changed … When you have three buckets, let's say four buckets. If two distributions are different, you can easily say they are distinct regimes." Bilal read the weekly tails (about −6% in high vol, −2% to −4% in low vol) and the profit factor per regime. No test of difference is computed.

### 6.6 Metrics on the page
Per regime: `n_weeks`, `total_trades`, `avg_trades_weekly`, `total_pnl_pct`, `avg_weekly_pnl_pct`, `win_rate` (share of winning weeks), `avg_win_pnl_pct`, `avg_loss_pnl_pct`, `profit_factor`, `max_drawdown`, `n_drawdown_periods`. Overall: log cumulative return and drawdown series. No Sharpe, no Calmar.

### 6.7 What looks like look-ahead or over-fitting
1. **Dominant regime** (the default) uses the outcome week's own data — the same-period rule of our workflow sends this to `failure/`.
2. **Unstated threshold** that may be full-sample (and GARCH fitted once on all data).
3. **Warm-up**: 200-bar regimes defined from week 2.
4. **360 views** (90 combinations × 2 timeframes × 2 approaches) and a free date filter, with no correction for multiple testing and no hold-out. The best-looking view will look good by chance.
5. Weekly regimes on a strategy that trades about 55 times a week mix many decisions into one label.

### 6.8 Ideas to reuse in the harness
- **Regime-coloured equity curve with a drawdown overlay** (chart 4). Best single picture of "where does the strategy make and lose money".
- **Per-regime density of the outcome** (chart 7) beside our bucket cards — the visual of the Kruskal–Wallis / Anderson–Darling question.
- **Two-axis regime** (volatility × trend/efficiency) as a 2×2 bucket. We already compute `efficiency` (`features/windows.py` L101) and RV.
- **Per-regime card** with profit factor, avg win / avg loss, drawdown periods — add to our results card.
- **One page, one selector per feature/estimator/window** so a reviewer can flip through variants — but the harness must print the **number of variants** and the BH-corrected p-value on the page, and must offer only `starting`-style (decision-time) labels with thresholds drawn on the train half.

## 7. The senior's MCP for the engine (Backtest-Engine)

`D:\Convex Hedge\Backtest-Engine`, branch `feature/spxw-straddle-after-bucket`@b17841a8. GitHub `Convex-Hedge-Private-Limited/Backtest-Engine` (older links point at `bilal-sagar-razak/Backtest-Engine`).

### 7.1 Is there an MCP server? **Not built. Planned only as "the future MCP server".**
- No `.md` file in `docs/`, `wiki/`, `sdd/`, `PROJECT.md` or `GAPS.md` mentions MCP (case-insensitive search).
- Code mentions, all as a future consumer:
  - `src/engine/nodes/catalog.py` L1–5: "``nodes.catalog()`` — the machine-readable export of the node vocabulary. Catalog-as-code (#454): the SINGLE source of truth for the painter's AST mapping, Echo's prompts and tools, the future MCP server and the validation gate's guardrails."
  - `src/engine/nodes/__init__.py` L5: "Echo/MCP discovering which constructor fits which node".
  - `tests/engine/nodes/test_declarations.py` L616 ("#600: the catalog is the vocabulary Echo, the MCP server and the docs read") and L650 ("It crosses process boundaries — the painter, Echo prompts, a future MCP server"; the test asserts the catalog round-trips through `json`).
- GitHub issues (read with `gh issue list --search MCP`):
  - **#437 OPEN** "Strategy Graph v2 — wayfinder map": "The protocol doubles as the Echo/MCP discovery surface — standardized utilities help in creating MCPs and better understanding for Echo (Q6b)."
  - **#454 CLOSED** "Node protocol — typed per-node utility functions": "Echo/MCP discovery: how the protocol surfaces itself — function registry, typed schemas per node type".
  - **#455 OPEN** "Echo Agent v2 rebuild — wayfinder map": a rebuilt Echo agent "on a LangGraph turn loop (hybrid shape) with OpenRouter as the model-access layer, targeting the Strategy Graph v2 node protocol and its MCP/discovery surface". (#445 CLOSED: "Decision: adopt LangGraph for the Echo agent?"; branch `origin/research/langgraph-echo-agent`.)
- So the plan is: the MCP server would expose `nodes.catalog()` (node types, constructors, render specs, `capabilities` per asset, `engine_reserved_params`, `engine_policies`, `deferred`) so an agent can **compose strategies** from typed protocol functions. Nothing yet describes MCP tools for launching or reading backtests.
- **Echo** (the in-product LLM agent) already exists: `src/echo/` (`agent/`, `painter/`, `schemas/`, `storage/`, `reverb/`), wiki `wiki/high-level/echo.md`, `wiki/low-level/echo-agent.md`, `echo-painter.md`, `echo-storage.md`, `echo-validation.md`. Endpoints `POST /api/echo/build` (`src/api/echo/build.py:36`), `POST /api/echo/save` (`src/api/echo/actions.py:177`), `GET /api/echo/source/{strategy_uid}`.

### 7.2 The interface a later backtest call would use (what exists today)
- **CLI:** `run_backtest.py` → output in `runs_pq/<strategy_uid>/<run_id>/`. Flags (L84–140): `--strategy` (default `straddle`), `--start` (default 2024-04-01), `--end` (inclusive, default 2026-04-01), `--capital` (default 10,000,000), `--asset` (default NIFTY; `SPXW` for us), `--sizing-pct` / `--sizing-units`. Example in its docstring: `.venv/bin/python run_backtest.py --strategy daily_strangle --start 2024-04-01 --end 2025-12-31`.
- **HTTP:** `POST /api/jobs` (`src/api/routes/jobs.py` L253) with `LaunchRequest` (L133–150): `strategy_uid`, `source` (`"registry"` | `"store"`), `asset` (default `"NIFTY"`), `start`, `end`, `capital` (10,000,000), `params` (dict), `name`. Auth: session identity plus a membership check (`can_access`); `AUTH_DEV_BYPASS=true` skips auth locally. Poll `GET /api/jobs/{job_id}` (L1007). Workers report back with `POST /internal/jobs/{job_id}/complete` (L1041; carries `meta`, `verdict`, `cost`) or `/fail`. Rerun: `POST /api/runs/{run_id}/rerun` (L789). Name preview: `POST /api/jobs/name-preview` (L199).
- **Results:** `GET /api/runs`, `/api/runs/{id}/meta`, `/views/overview`, `/views/trades`, `/views/day-log`, `/views/day/{day}` (`wiki/high-level/api-server.md`). On disk (`wiki/low-level/run-output.md` L31–45): `daily.parquet` (`date, n_trades, pnl_capital, return_capital, equity_capital, daily_mtm, …`), `trades.parquet`, `signals_orders.parquet` (with `bid_at_fill`, `ask_at_fill`, `slippage_cost`, `charges`), `open_positions.parquet`, `signal_snapshots.parquet` (`forward, atm_iv, regime_flags, …`), `signal_leg_snapshots.parquet` (`iv, delta, gamma, vega, theta`), `meta.json` (`strategy_uid, strategy_version, params, start_date, end_date, cost_config, greeks_version, dte_window, …`).
- Summary metrics: `src/analytics/summary.py` (Sharpe with risk-free, Sortino, max drawdown; see 1.10).

### 7.3 How a strategy is registered and launched
- **Registry:** `src/api/strategy_registry.py` — "filesystem auto-discovery of the strategy folders". It imports every module under `strategies/` (research) and `strategies/live/` (live) and records each concrete subclass of `StrategyBase` with `cls`, `default_params()`, `params_schema()`, `description` (`DESCRIPTION` or module docstring), `module_path`. Canonical name = **module file stem** (`daily_straddle`), plus hand-kept `_SHORT_ALIASES` (`straddle`, `strangle`, `iron_condor`, …). `STRATEGY_REGISTRY_SCOPE=live` serves only `strategies/live/`; unset serves all (L64–68, `_roots()` L165). Collisions on `UNIQUE_ID` raise (L321). Functions: `get_strategy(name)` L359, `list_names()` L370, `reload_strategies()` L339.
- **Contract** (`wiki/high-level/strategies.md` §5, L1594–1630; `src/engine/signals/strategy.py`): class attributes `UNIQUE_ID` (L54), `VERSION` (L55), `SIGNAL_TAGS` (L56), **`ASSETS`** (L62, required, e.g. `frozenset({"SPXW"})`), optional `DTE_WINDOW` (L80; the five SPXW 0DTE strategies use `DteWindow(0.0, 1.0)`). Hooks: `setup(params)`, `prepare(bars, chain)`, `structures()`, `max_loss_per_unit(lot_size)`, `hedger()`, **`on_candle(ctx)`** (abstract; returns one `Signal` or `None`), `on_fill(fill)`. Classmethods `default_params()` and `params_schema()` give the dashboard its editable settings. Since #547 a strategy may instead be a **protocol strategy** (`GraphStrategy`) declaring `START` / `RULES` / `HEDGES` as data.
- **Timing rule** (docstring of `strategies/spxw_0dte_straddle_after_bucket.py`): "The engine hands `on_candle` the chain of the bar BEFORE the bar it decides on, and fills on the deciding bar at that bar's mid." This matches our "decide at minute i−1, fill at i" rule.
- **Settings:** per-strategy `params` (merged over `default_params()`), sizing through `src.api.sizing_params.apply_sizing` (`sizing_pct`, `sizing_units` are `engine_reserved_params`), asset checked by `assert_asset_declared` (`jobs.py:153`).
- **SPXW strategies already registered:** `spxw_0dte_iron_condor`, `spxw_0dte_long_straddle_low_iv`, `spxw_0dte_premium_condor`, `spxw_0dte_put_spread`, `spxw_0dte_strangle`, and on this branch `spxw_0dte_straddle_after_bucket` (the bucket-method straddle: 30-minute windows 09:35–15:35, ratio = (Δc+Δp)²/(2(Γc+Γp)) over earned theta, three bucket lines, six `rule` modes; it notes the chain's clock is 252 × 405 minutes, not 390 × 252).

## 8. SPXW 0DTE dynamics already found (the context pack)

Sample unless stated: 249 days, 2025-10-01 to 2026-09-30; **train** = 123 days before 2026-04-01 ("fresh" in older notebooks), **test** = 126 days from 2026-04-01 ("seen" days; the older studies used 97 or 127 of them). The index is the put-call-parity forward. "Both halves" = significant with the same sign on train and test after BH correction. Hypothesis files are on GitHub `main` only.

### 8.1 Confirmed on both halves (the four `success/` files)

| # | Finding | Source | Key numbers | Both halves | Status |
|---|---|---|---|---|---|
| D1 | **The index mean-reverts slightly over 15–30 minutes.** | `hypothesis/success/intraday-mean-reversion-of-the-index.md` (Results); notebook `hyp_test_notebooks/hypothesis_intraday_mean_reversion_of_the_index.ipynb` | Lag-1 autocorrelation of consecutive h-minute log-forward changes, per-day mean. 30 min: train −0.062 (t −2.41, BH p 0.027), test −0.065 (t −2.65, BH p 0.018). 15 min: train −0.070 (p 0.003), test −0.037 (p 0.083). 5 min: train −0.003 (p 0.84), test −0.062 (p <0.001). Variance ratio (median) 0.93/0.84/0.75 train, 0.94/0.83/0.76 test. AR(1) half-life of day-demeaned level: 43 min train, 46 min test. Same with bid-only, ask-only forward and with time of day removed. | yes at 30 min; 15 min test weak; 5 min unstable | confirmed (relationship). "About 6% of a 30-minute move comes back in the next 30 minutes." |
| D2 | **Put skew mean-reverts within the day (at fixed delta).** | `hypothesis/success/intraday-mean-reversion-of-put-skew.md`; `hyp_test_notebooks/hypothesis_intraday_mean_reversion_of_put_skew.ipynb` (helper `_put_skew.py`) | skew25 (25Δ put IV − 25Δ call IV) lag-1 ac, train / test: 5 min −0.231 / −0.193; 15 min −0.254 / −0.216; 30 min −0.237 / −0.213. skew10: 30 min −0.267 / −0.225. 75–93% of days below 0. All 12 BH p < 0.0001. VR at 30 min ≈ 0.16–0.22. Half-life (pooled AR(1), 5-min): 22–30 min. Bid/ask-only IV (first-order approximation) same. | yes | confirmed (relationship). **Caveat:** at the strikes actually traded it did not hold on test (D10). |
| D3 | **The straddle price over the implied move mean-reverts within minutes.** | `hypothesis/success/intraday-mean-reversion-of-straddle-price-against-implied-move.md`; notebook `hyp_test_notebooks/hypothesis_intraday_mean_reversion_of_straddle_price_against_implied_move.ipynb` | Mid, lag-1 ac train / test: 5 min −0.314 / −0.344; 15 min −0.279 / −0.307; 30 min −0.285 / −0.301; all BH p < 0.0001; 76–91% of days below 0. VR at 30 min 0.07–0.08. Bid-only −0.36 to −0.44; ask-only −0.17 to −0.30. Half-life: mid 11.5 / 11.2 min; bid-only 4.3 / 4.4; ask-only 24 / 21. | yes | confirmed (relationship). Part may be forward/interpolation noise; time of day not removed. The trade on it (D14) shows no significant profit. |
| D4 | **Realised volatility persists between 30-minute windows, and IV already follows it.** | `hypothesis/success/realised-volatility-persists-and-iv-follows-it.md`, citing Experiment 3 of `notebooks/spxw_feature_iv_rv.ipynb` | corr(RV window k, RV window k+1): seen 0.75, fresh 0.85. corr(IV at start, trailing RV): seen 0.79, fresh 0.86. | yes ("both significant") | confirmed fact, "not a trade": RV is forecastable but IV has moved to match it. |

### 8.2 Facts from the trading tests (mechanism statistics inside `testing/` and `failure/` files)

| # | Finding | Source | Key numbers | Both halves | Status |
|---|---|---|---|---|---|
| D5 | **The opening moves much less than the options charge for it.** | `hypothesis/testing/tested-r1--buy-the-opening-burst.md`, "Mechanism: RV² over the window against the variance charged for the window alone" | Pooled RV² / charged variance, train / test: 9:31→9:45 0.42 / 0.42; 9:31→10:00 0.50 / 0.60; 9:31→10:30 0.75 / 0.74; 9:35→9:45 0.37 / 0.35; 9:35→10:30 0.78 / 0.77. Many windows dropped because var_window ≤ 0 (IV rose; 23–36 of ~120). | yes (all < 1) | descriptive mechanism on both halves; buying the open loses. |
| D6 | **The last hour realises less than it is priced.** | `hypothesis/testing/tested-r1--buy-into-the-close.md` L78–85 | RV (decision→close) / ATM IV², median (mean), train / test: 15:00 0.75 (0.94) / 0.65 (0.76); 15:15 0.72 (0.90) / 0.65 (0.76); 15:30 0.68 (0.85) / 0.70 (0.81); 15:45 0.63 (0.73) / 0.65 (0.80). | yes (all < 1) | descriptive on both halves; 14 of 16 buyer variants lose on test. |
| D7 | **After an IV jump on a quiet index, the next hour moves less than the new IV prices.** | `hypothesis/failure/buy-when-iv-jumps-before-the-index-moves.md` (Verdict) | RV next 60 min / IV at entry: median 0.86–0.92 on test; all 9 buyer variants lose on both halves; lowest BH p 0.996. | yes | failure (buyer loses). |
| D8 | **Seller baseline (sell ATM straddle at 10:00, hold to expiry) flips sign between halves.** | `hypothesis/testing/tested-r1--sell-morning-straddle-with-exits-and-filters.md` L53–60 | Train MID mean −0.18 pts/day, Sharpe −0.09, worst day −189.4, max DD 305.8; test MID +0.98, Sharpe 0.75, worst −72.2. SPREAD: −0.37 / +0.82. BH p 0.84–0.93. The pin-fly file repeats "−0.18 to +0.98". | no (flips) | descriptive: regime. Train = index falling, test = index rising (workflow §5). |
| D9 | **Rest-of-day RV² is below IV² at entry on most days.** | `hypothesis/testing/tested-r1--buy-after-a-quiet-open.md`, "Mechanism: rest-of-day RV² minus IV² at entry" | Median RV² − IV² (yearly variance) ≈ −0.0006 to −0.0012 on signal and other days, both halves; quiet-open days not different (Mann-Whitney p 0.42–0.75). | yes (negative) | descriptive (variance risk premium, rest of day). |
| D10 | **Skew "reversion" at fixed delta is not reversion at fixed strikes.** | `hypothesis/failure/sell-put-skew-spikes-with-hedged-risk-reversal.md` (Verdict) | Test half: after signals the strike IV gap widened (+0.07 vol points vs control; Wilcoxon p 1.0, Mann-Whitney p 1.0). Hedged cards positive at mid for all 24 variants, but 0–1 of 24 keep a positive test mean with the spread paid. | no | failure. Mid-price profits disappear with the spread (the "both sides win at the mid" warning). |
| D11 | **A window's own IV − RV explains its own straddle return** (same-period; not usable). | `hypothesis/failure/window-iv-minus-rv-explains-its-own-straddle-return.md` | significant, but uses RV of the outcome window | — | failure by the same-period rule. |
| D12 | **IV − Parkinson RV of window k against the seller's return in window k+1:** bucket tests unstable; within-day rank correlation negative on both halves at every length (not pre-registered). | `hypothesis/testing/tested-r1--iv-minus-parkinson-rv-predicts-next-window.md` (Verdict); helper `hyp_test_notebooks/_iv_parkinson.py` | 60-min test AD p 0.016; KW and AD not both < 0.05 on both halves at any length; best bucket differs (train Q4, test Q3). | partly | testing; within-day rank effect needs its own pre-registered test. |
| D13 | **The Greek metric (Δ²/(2Γ) over theta earned) known at a window's start ranks the seller's return within the day.** | `hypothesis/testing/tested-r1--metric-at-window-start-predicts-straddle-return.md` (Verdict); helper `_metric_predicts_next_window.py` | Across-day, time-of-day-adjusted Spearman significant after BH on both halves at 15, 30 and 60 min; ρ 0.05–0.18. Pooled correlation and bucket means: nothing usable; Q4 vs rest and Q1 vs rest not significant. | yes for the named statistic (chosen after a previous round) | testing; effect small, within-day only. |
| D14 | **Cheap straddle vs implied move (z-score) as a buy signal:** almost every test mean slightly positive, lowest BH p 0.48; 7–21 trades a day; spread would very likely remove it. | `hypothesis/testing/tested-r1--buy-when-straddle-is-cheap-against-implied-move.md` | as stated | no significance | testing. |
| D15 | **Buying volatility has not worked** under any trigger tested (quiet open, open burst, into the close, IV jump, IV < RV, macro days, wild metric window, IV/RV decoupling, put-skew spike). | the nine buyer files in `testing/` and `failure/`; `buy-before-scheduled-macro-releases.md` (8 FOMC statement days, 7 minutes days: minutes days lose at every exit on both halves) | e.g. IV<RV: 19 of 24 test rows lose, all 12 unhedged rows lose on both halves; wild metric window: all 10 variants negative Sharpe at mid | yes (consistently ≤ 0 or insignificant) | failure / leaning failure. |
| D16 | **Late-day pin (iron fly/condor 14:30–15:30):** train flat to negative, test positive (best BH p 0.053); entry spread 2–7% of credit; IV-rich filter (IV/RV_L > 1 or > train median 1.13–1.49) does not help. | `hypothesis/testing/tested-r2--sell-late-day-pin-fly.md` | chosen fly10 14:45 move-exit k=1: test 0.59 pts/day mid, 0.20 spread | no (flips) | testing; "looks like regime". |
| D17 | **Put-side bias:** 10-delta put spread positive on test at mid (BH p 0.035) but not with spread (0.070); P&L tracks index drift (train down, test up). Put-heavy iron flies (H7) fail. Opening-range fade H8 stays; intraday momentum H9 fails (no relation on train, slope p 0.18–0.33). | `hypothesis/testing/tested-r1--put-side-bias-and-risk-reversal.md`; `tested-r1--opening-range-fade-and-intraday-momentum.md` | as stated | no | testing / failure. |
| D18 | **Selling right after an IV spike adds nothing over selling at every 5-minute step** (SIGNAL − UNCOND test mean −0.064, p 0.79); short 30-min sales earn at the mid and lose with the spread. | `hypothesis/testing/tested-r1--sell-after-iv-spikes.md` | 29 of 60 variants beat their unconditional twin on test | no | testing. |

### 8.3 Findings from the notebooks, by topic

Notation: **S** = seen days 2026-03-31 to 09-30 (127 days; 126 with a 9:35 chain; S97 = first 97). **F** = fresh days 2025-10-01 to 2026-03-30 (122 days, half days removed). Figures written "S/F". Status: **C** = confirmed, significant on both halves; **1H** = one half only (or only one half tested); **D** = descriptive only, no test; **SP** = same-period reading (describes, cannot trade). "main" = notebook on GitHub `main` only; "local" = on local branches only (`feature/feature-experiments`, `feature/four-comparisons`, `feature/anomaly-studies`); otherwise in both. Cell numbers `c<n>` are code-cell indices of the notebook (0-based, all cells counted). The anomaly notebooks were written after both halves had been read, so all their findings are D even where p-values print.

**Time of day**

| # | Finding | Source | Numbers | Status |
|---|---|---|---|---|
| D19 | RV is highest at the open, lowest mid-afternoon, and rises again at the close. | `notebooks/spxw_descriptive_stats.ipynb` c14; `spxw_smile_study.ipynb` c26; `spxw_feature_regimes.ipynb` c3 | Median half-hour RV 9.66% at 9:35 → 4.57–4.71% 14:00–15:00 → 6.02% at 15:30 (S). Usual RV 0.109 at 9:35 → 0.045 at 15:05 (S). Pooled RV 14.7% at 9:30, 8–10% from 11:00 (S97). | D |
| D20 | ATM IV falls from the open to early afternoon, then rises into the close (to-the-close IV). | `spxw_descriptive_stats.ipynb` c54, c40; `spxw_smile_study.ipynb` c10; `spxw_iv_two_halves.ipynb` c5 (main) | Median 8.00% at 9:35 → 6.33% at 14:00 → 7.54% at 15:30; 7.5 / 8.5 / 10.0 / 14.3% at 15:30 / 15:45 / 15:55 / 15:59 (S). Last-hour median above earlier hours in both quarters of S. | D |
| D21 | Movement runs ahead of time decay after 11:30. | `spxw_hedged_straddle.ipynb` c5 | Share of day's movement vs share of time value: 9:35 13.4% vs 26.8%; 15:30 5.2% vs 1.2%; from 11:30 movement leads in 9 of 9 windows (S). | D |
| D22 | Highs and lows cluster at the open and the close. | `spxw_descriptive_stats.ipynb` c18 | High set in the 9:35 window on 24 days, low on 40; 15:30 window high 21, low 13; quietest window 14:00 (6 days) (S). | D |
| D23 | The opening window charges a much higher window-only IV than the IV to the close. | `spxw_feature_iv_rv.ipynb` c27, c34 (main) | 9:35 window IV 13.9% / 17.9% vs 8.0% / 10.2% to the close (S/F). | C (against stated ranges); SP (needs IV at window end) |
| D24 | Plain RV > IV-to-close in most opening windows and few closing ones — an artefact of comparing a window with IV to the close. | `spxw_feature_iv_rv.ipynb` c34 (main) | RV > IV in 85% / 94% of 9:35 windows; 9% / 7% at 15:05. | D (notebook calls it an artefact) |
| D25 | Window variance ratio (RV² / variance charged for that window alone) is below 1 at every time of day by median; pooled over the day ≈ 1. | `spxw_feature_iv_rv.ipynb` c27, c34 (main) | Median 0.53–0.75 (S), 0.56–0.80 (F); share above 1: 17–28% / 20–34%; pooled whole day 1.01 / 1.02 (5-min RV 1.04 / 0.92). By hour pooled 0.77–1.21 / 0.80–1.60; only 9:35 below 1 on both (0.77 / 0.80). | C on ranges; SP |
| D26 | Actual move over implied move falls through the day. | `spxw_smile_study.ipynb` c28, c32 | RMS ratio 1.01 at 9:30 → 0.90 at 13:30 → 0.83 at 15:30; median ratio 0.75 at 10:00 → 0.56 at 14:00; days beyond implied 31.96% → 18.56% (S97). | D |
| D27 | IV drifts up late in the session. | `spxw_anomaly_vol.ipynb` c46 (local) | Median IV change +0.0042 at 14:35, +0.0063 at 15:05 (S); +0.0032 / +0.0128 (F). | D |
| D28 | Charm (clock's share of delta change) grows towards the close. | `spxw_feature_greeks.ipynb` c21, c22, c27 (main) | Re-struck pair: market 0.934/0.939, clock 0.016/0.015, IV 0.050/0.046; clock 0.005 at 9:35 → 0.048 / 4.3% at 15:05. 9:35 straddle held: clock 0.032/0.033, 15:00 hour 0.093/0.101. | C (against stated ranges) |
| D29 | Premium decays to about half by 13:35. | `spxw_anomaly_vol.ipynb` c31–32 (local) | Median premium at 13:35 = 0.47 / 0.48 of 9:35 premium; days keeping ≥ 0.9: 4/127 and 6/122. | D |

**IV level and behaviour**

| # | Finding | Source | Numbers | Status |
|---|---|---|---|---|
| D30 | Opening IV and implied move levels. | `spxw_descriptive_stats.ipynb` c28 | IV at 9:35 median 8.00% (4.53–17.51%); implied move median 38.12 points = 0.50% of the index (S). | D |
| D31 | Opening IV predicts the day's range (not its direction). | `spxw_descriptive_stats.ipynb` c30, c44, c38, c46; `spxw_greek_ratios.ipynb` c23 (main) | Spearman +0.55 (N6); range by IV quartile 0.50 / 0.66 / 0.82 / 0.97% (N7); OLS slope 0.0898, R² 0.274, p 3.2e-10. IV group → return KW p 0.755; skew group → return p 0.221. | 1H (S only), tested |
| D32 | IV follows yesterday's RV. | `spxw_descriptive_stats.ipynb` c36 | Spearman +0.58 with yesterday's RV (N9); +0.46 with yesterday's range (S). | 1H, tested |
| D33 | Index falls ↔ IV rises (spot-vol slope), asymmetric. | `spxw_feature_greeks.ipynb` c29 (main); `spxw_smile_study.ipynb` c36; `spxw_anomaly_link.ipynb` c18 (local) | Slope all moves −1.24 / −1.59; down moves −3.05 / −3.04; up moves +0.39 / −0.18 (vol points per 1%); rank corr −0.24 / −0.36. S97: return vs IV change −0.513 (−3.17 vol pts per 1%). Forward return vs IV change −0.456 / −0.643. | C (same-window relation; SP for trading) |
| D34 | After a large fall IV gives some back; not after a rise. | `spxw_smile_study.ipynb` c38 | −0.199 after a large fall (BH p 0.0317); after a rise p 0.23 (S97). | 1H |
| D35 | IV regime differs within S: Jul–Sep lower and fatter-tailed than Apr–Jun. | `spxw_iv_two_halves.ipynb` c3, c9 (main) | Per-minute mean 8.79 → 6.91; kurtosis 1.85 → 11.76; daily mean median 7.93 → 6.12 (KS, MW p 0.0000); intraday sd 1.10 vs 1.16 (p 0.58); skew25 0.0098 → 0.0068. F IV is higher than S (9:35 ATM IV 0.102 vs 0.080, `spxw_feature_smile.ipynb` c18). | D (S quarters only) |
| D36 | Hedge with the spot-vol slope reduces hedged variance. | `spxw_feature_greeks.ipynb` c30 (main) | −4.4% (S), −9.7% (F, using the S slope −1.236). | C |

**RV behaviour**

| # | Finding | Source | Numbers | Status |
|---|---|---|---|---|
| D37 | 1-minute returns: fat-tailed, no lag-1 correlation at 1 min. | `spxw_smile_study.ipynb` c24; `spxw_descriptive_stats.ipynb` c20 | SD 3.15 bp; 1.65% of minutes beyond 3 SD; excess kurtosis 12.1; lag corr +0.020 (S97). Lag-1 rank corr median −0.00 (1 min), −0.05 (5 min, t-test p 0.0000, N1), −0.04 (10 min) (S). | D / 1H (N1) |
| D38 | RV persists across windows (ranks, time of day removed). | `spxw_feature_iv_rv.ipynb` c22 (main); `spxw_anomaly_vol.ipynb` c43–44 (local) | Rank corr 1-min RV 0.753 / 0.846; 5-min 0.497 / 0.647; above usual after above usual 80–84%. Log-RV AR coefficient 0.780 / 0.859 (half-life 2.8 / 4.6 windows). | C (= D4) |
| D39 | 1-min vs 5-min RV. | `spxw_feature_iv_rv.ipynb` c8 | Ratio median 1.06 (middle half 0.88–1.29); rank corr 0.85; median IV 0.0694, RV1 0.0675, RV5 0.0615 (S). | D |
| D40 | Daily range facts. | `spxw_descriptive_stats.ipynb` c6, c10, c12, c22 | Abs open-to-close median 0.34%; range median 0.72% (0.26–3.18%); range/net move median 2.00; Parkinson/RV median 0.89; today's range vs yesterday's +0.28 (N2); vs overnight gap +0.17 (BH 0.086 only) (S). | D / 1H |
| D41 | Nights are a third to half of a week's movement. | `spxw_week_iv_rv.ipynb` c5, c9 | 47% (S) / 37% (F) of all movement; median week 35% / 33%. | D both |

**IV against RV (variance risk premium)**

| # | Finding | Source | Numbers | Status |
|---|---|---|---|---|
| D42 | At the open IV is above trailing RV most days. | `spxw_descriptive_stats.ipynb` c42 | IV − RV median +0.97 vol points, worst −16.48; IV/RV median 1.14; IV > RV on 78/126 days; signed-rank p 0.0019 (N10) (S). | 1H, tested |
| D43 | The day closes inside one implied move most days. | `spxw_descriptive_stats.ipynb` c32 | Move / implied move median 0.63; inside on 92/126 (73%); never beyond intraday on 58/126; range / implied median 1.33 (S). | 1H (reference "badly chosen", c79) |
| D44 | Over 7 days and 1 day ahead, realised variance is below implied. | `spxw_week_iv_rv.ipynb` c9, c18 | 7-day pooled RV/IV variance 0.87 / 0.95 (no nights 0.51 / 0.62); next day 0.95 / 0.94; IV above outcome on 70% / 52% of days (failed on F). Highest-charge bucket lowest ratio 0.89 / 0.82 (lead only). IV forecasts next-week RV better than last week's RV (0.49 vs 0.22; 0.54 vs 0.27). | C (pooled ratios) |
| D45 | IV tracks recent RV; the IV−RV gap itself barely persists. | `spxw_feature_iv_rv.ipynb` c22, c24 (main) | IV vs RV before 0.790 / 0.855; gap persistence 1-min 0.336 / 0.349, 5-min 0.156 / 0.163 ("about half is quote noise"). Next-window RV explained: IV 0.575 / 0.706, trailing RV 0.567 / 0.716, both 0.638 / 0.766. | C (measurement) |
| D46 | Same-window gap strongly describes the seller's return (unusable). | `spxw_feature_iv_rv.ipynb` c12, c15, c36 (main); `spxw_straddle_iv_rv_regime_backtest.ipynb` c3, c5 (main) | Rank corr hedged-every-minute / band-paid / unhedged 0.598 / 0.456 / 0.330 (S), 0.529 / 0.378 / 0.234 (F); lowest-gap bucket wins 34% vs 88% top (F). Own-window IV−Parkinson KW p 0.000 both; next window p 0.053 / 0.570. | C but SP |
| D47 | Trailing gap → next window: weak, F only, gone after costs. | `spxw_feature_iv_rv.ipynb` c20 (main) | Hedged 0.150 vs TOD 0.148 (S, nothing); 0.110 vs 0.059, p 0.027 (F); spread-paid p 0.22 / 0.09. | 1H |
| D48 | IV² − RV² at the window start ranks the size of the next 5–15 minute move (higher premium → smaller move). | `spxw_feature_iv_rv.ipynb` c48 (main) | Within day, TOD out: 5 min −0.086 / −0.080 (p 0.000); 15 min −0.056 (p 0.007) / −0.071 (p 0.000); 30 and 60 min not significant. Same statistic vs seller's hedged return: raw significant both, TOD-removed 0.075 (F, p 0.016) / 0.020 (S, p 0.58). | C at 5 and 15 min (move size); 1H for return |
| D49 | IV and RV variability. | `spxw_feature_iv_rv.ipynb` c40 (main) | corr(IV, RV) 0.727 (60-min), 0.614 (5-min); sd IV 0.036 / 0.035; sd RV 0.051 / 0.062 (all 249). | D |

**Skew and smile**

| # | Finding | Source | Numbers | Status |
|---|---|---|---|---|
| D50 | Smile shape: put wing rich, call wing below ATM, flattening into the close. | `spxw_smile_study.ipynb` c51; `spxw_credit_spread_skew.ipynb` c9 (main) | 25Δ put IV 1.11 × ATM (1.09–1.14); 5Δ put 1.44; 25Δ call 0.94; 5Δ call 1.15 by 13:30 (S97). iv_skew_10 median 3.04 at 10:00 → 1.53 at 14:30; iv_skew_25 median 1.11 (both halves). | D |
| D51 | Tilt (put minus call at ±25Δ, local definition) is positive almost always and falls through the day; wings ratio > 1. | `spxw_feature_smile.ipynb` c18, c20, c6 (local) | Tilt > 0 in 97% / 98% of windows; median 0.0132 → 0.0040 (S), 0.0202 → 0.0069 (F) 9:35 → 15:05. Wings > 1 in 99% / 98%; range 0.99–1.12. Tilt ≤ 0 mostly at 14:35–15:05 (15.0% / 11.5% of 15:05 windows) (`spxw_anomaly_smile.ipynb` c12–16). | D both |
| D52 | Tilt and wings persist; tilt moves with IV level. | `spxw_feature_smile.ipynb` c19; `spxw_anomaly_smile.ipynb` c70–83; `spxw_anomaly_link.ipynb` c8–16 (local) | Tilt rank next window 0.70 / 0.78, next day 0.27 / 0.27; tilt AR 0.778 / 0.816 (half-life 2.8 / 3.4 windows); tilt with ATM IV +0.50 / +0.30; wings with ATM IV −0.46 / −0.65. IV-change vs tilt-change rank corr +0.272 / +0.201 (BH 0.009 both). | D (both halves agree) |
| D53 | Put skew mean-reverts at fixed delta, but not at fixed strikes. | = D2, D10 | — | C / failure |
| D54 | Richer wing at entry → worse credit spread held to expiry. | `spxw_credit_spread_skew.ipynb` c17 (main) | Put spread vs put_skew_10 within-day −0.163 / −0.110; call spread vs call_skew_10 −0.115 / −0.136 (pooled −0.38 / −0.37); BH < 0.05 on both; TOD explains about ⅔ of pooled strength. Credit as share of width: put 9.7%, call 13.8%; win rate 84–86%, worst −100%. | C |
| D55 | Skew level and skew change do not predict direction or straddle return. | `spxw_descriptive_stats.ipynb` c38 (P5 p 0.22); `spxw_credit_spread_skew.ipynb` c17 (prior-30-min skew change: none on both); `spxw_feature_smile.ipynb` c33–37 (A2, A4 not findings) | as stated | NS |

**Bid-ask spread as a share of price**

| # | Finding | Source | Numbers | Status |
|---|---|---|---|---|
| D56 | Spread given up, % of mid, by structure. | `spxw_descriptive_stats.ipynb` c60 | Straddle 0.50%, 25Δ strangle 1.02%, 10Δ strangle 1.55% (S, median). | D |
| D57 | Spread share rises through the day and in the wings. | `Strategy-Research/Guide/SPXW 0DTE smile study.md` L98–100; `spxw_feature_term.ipynb` c17 (local); `spxw_straddle_return_regimes.ipynb` c23 (main) | 5Δ options 5–9% of price in the morning, > 20% after 15:30; ATM about 1%. Straddle spread share 0.0100 at 9:35 → 0.0219 at 14:35 while points fall 0.30 → 0.20 (S). spread_share decile Q1-share 8% → 38% (ρ 0.988). | D |
| D58 | Round-trip cost per 30-min window ≈ 2% of premium; it removes the mid-price edge. | `spxw_feature_regimes.ipynb` c5 (main); `spxw_feature_smile.ipynb` c12, c15 (local) | Options 0.29 / 0.35 points a window, hedges 0.13 / 0.16; median premium 19.1 / 21.4. Straddle spread cost per window 0.0158 / 0.0180 of premium. | D both |
| D59 | Quotes thin out late: the morning strike often has no two-sided quote. | `Strategy-Research/Research/Hedged straddle results.md` L32 | No two-sided quote on about 1 day in 7 at 15:30 and half the days at 15:50. | D |

**Mean reversion, persistence and regimes**

| # | Finding | Source | Numbers | Status |
|---|---|---|---|---|
| D60 | Index, skew and straddle/implied-move mean reversion. | = D1, D2, D3 | — | C |
| D61 | Greek-metric regimes (Δ²/(2Γ) over theta, quartiles) last about one window. | `spxw_metric_regime_durations.ipynb` c2–c16 (main) | 5-min spells mean 6.7–7.1 min, median 5; 71–75% last one window. Excess over chance at 5 min: calm +5.6% / +4.3% (p 0.001), wild +2.8% / +3.1% (p ≤ 0.007); at 30 min nothing (p 0.54–0.97). Regime 4 does not predict the next window (Welch p 0.16–0.70). | C (5-min calm/wild, tiny) |
| D62 | The metric persists only a little between 10-minute windows. | `spxw_feature_greeks.ipynb` c16 (main) | Log corr +0.051 [0.021, 0.081] (S), +0.072 [0.032, 0.106] (F); fades to +0.011 at 30 min; R² 0.006. | C but tiny |
| D63 | Long-straddle "great" windows and short-straddle "great" windows do not persist. | `spxw_straddle_return_regimes.ipynb` c32 (main) | Daily Q5-share autocorr −0.023 (p 0.61); Q1 −0.018 (p 0.57); within day P(Q5→Q5) 0.187 vs 0.198 (p 0.76). | NS |
| D64 | Vol × direction regimes of the window itself describe the seller's return; regimes known at the start do not. | `spxw_feature_regimes.ipynb` c8, c9, c13 (main) | Own window, unhedged mean: low vol + choppy +11.5% / +10.2%; high vol + trending −13.9% / −13.9%; choppy pays about 10% whatever the vol; p < 0.001. Known-at-start regimes: S lead failed on F. | C but SP / NS |
| D65 | Efficiency of the day so far points the same way on both halves (straighter day → better hedged seller). | `spxw_feature_regimes.ipynb` c16 (main) | Straightest bucket +1.9% (S) / +1.3% (F); p 0.36 / 0.88. | lead, NS |
| D66 | Slope of the term structure barely reverts within a day. | `spxw_feature_term.ipynb` c34–35 (local) | AR 0.970 / 0.973 (half-life ≈ 23–25 windows); 77% / 76% of variance between days. | C (claim killed on both) |

**Seller's and buyer's returns**

| # | Finding | Source | Numbers | Status |
|---|---|---|---|---|
| D67 | Selling every 30-min window earns at the mid on both halves and loses once the spread is paid. | `spxw_feature_regimes.ipynb` c5, c6 (main) | Mid totals unhedged / hedged-every-minute / band: +376.6 / +293.4 / +273.0 points (S), +183.2 / +136.2 / +288.5 (F); days up 66–73%. Spread paid: unhedged −61.4 / −328.3; band −358.5 / −464.5. | C |
| D68 | Hedging cuts the seller's tail. | `spxw_feature_regimes.ipynb` c5 (main); `spxw_feature_band.ipynb` c16, c19 (local) | Worst day F: −57.5 unhedged, −25.9 hedged, −31.3 band. Held to close (S): band mean 0.0647, width 0.2207, worst −1.705; hedged every minute mean 0.0926, worst −1.399; unhedged mean 0.0758, worst −4.962 (share of premium). | D both |
| D69 | Hedged short straddle held from 9:36 wins on most days but a few days give back most of it. | `spxw_descriptive_stats.ipynb` c62, c66, c72 | Median day +2.45 points (84/126 up), worst −23.71; ten worst days −141.5 vs total +194.4. Median day earned 13.68 time value, lost 13.87 to movement. Re-sold each half-hour: median above 0 in 13/13 windows; average day positive in 10 windows at mid, 5 with spread. | 1H, tested (N13–N15) |
| D70 | The long straddle loses most windows and most days. | `spxw_straddle_return_regimes.ipynb` c9 (main); `spxw_descriptive_stats.ipynb` c76; `spxw_feature_iv_rv.ipynb` c46 (main) | 30-min long wins 29.6% of windows, median −0.0597, best +4.40; by TOD median −0.050 (9:35) → −0.131 (15:05). Held from 9:32 to expiry: median −14.0%, mean +1.6%, up 41% (248 days). S: median −21.98% at the ask, lost on 79/126 days. | D |
| D71 | Seller and buyer entry grid (hold to close / 60 min), S. | `spxw_hedged_straddle.ipynb` c8, c10, c19 | Seller medians +0.77 to +3.13 (to close), buyer −3.75 to −1.47; 60-min seller −0.01 to +1.84. 14:30 band-hedged buyer up on 26/112 days (p 1.1e-8, against its idea). H2–H5 NS. | D / 1H |
| D72 | Weekly short straddle (unhedged) disagrees between halves. | `spxw_week_iv_rv.ipynb` c15 | Mean +0.2% vs +24.9%; worst −193% / −142%. | killed |
| D73 | Windows where IV rose during the window are nearly always seller losses. | `spxw_feature_iv_rv.ipynb` c29 (main); `spxw_anomaly_vol.ipynb` c9–12 (local) | 161 / 175 windows; hedged seller median −0.120 / −0.099; win 1.2% / 1.1%. High-gap windows that still lose: IV rose in 80/88 and 72/79; nothing known at the start separates them (smallest p 0.24 / 0.14). | C but SP |
| D74 | Windows ending beyond one implied move are rare and bad for the seller. | `spxw_feature_greeks.ipynb` c26 (main) | 36 / 52 windows (2.4% / 3.6%); hedged median −0.178 / −0.102; win 22.2% / 19.2%; 11% / 22% of 15:05 windows. | D both; SP |

**Predictability from readings known at decision time**

| # | Finding | Source | Numbers | Status |
|---|---|---|---|---|
| D75 | Nothing known at the start picks the long straddle's best windows; the short's best windows are picked only by time of day. | `spxw_straddle_return_regimes.ipynb` c29, c35 (main) | Train → test once: Q5 AUC 0.504 (0.465–0.540) vs slot-only 0.496; Q1 AUC 0.714 vs slot-only 0.715; same at 15 and 60 min. Raw survivors after TOD removed (ε²): iv_rv 0.0135, metric_prev 0.013, iv_chg15 0.008. | C (null) |
| D76 | Direction is not predictable from gap, yesterday, first half-hour, or 15:30 return. | `spxw_descriptive_stats.ipynb` c8, c16 | P6 gap→day 0.090 (p 0.32); P9 p 0.89; P7 first→last half-hour 0.130 (p 0.15); P8 −0.018 (p 0.85) (S). | NS |
| D77 | Greek metric of the previous window does not predict the next window's return. | `spxw_straddle_delta_gamma_theta_regime_backtest.ipynb` c3 (main); `spxw_feature_greeks.ipynb` c12 (main) | ρ +0.02 / −0.02; bucket means flat (0.025 / 0.004 / 0.020 / 0.011 S). Same window ρ −0.78 (SP). | NS (but see D13 within-day rank) |
| D78 | Filters and rules chosen on one period do not carry to the next. | `spxw_straddle_metric_window_and_sizing_backtest.ipynb` c5, c9; `spxw_straddle_iv_rv_regime_backtest.ipynb` c11 (main); `spxw_feature_regimes.ipynb` c18 (main) | Sharpe rank Val → Te −0.24; all filters vs hold NS (Wilcoxon 0.36–0.91); regime filter rule beaten by 67% of random filters on F. | NS |
| D79 | News days: Fed days have wide ranges; scheduled-release days otherwise not different. | `spxw_descriptive_stats.ipynb` c24; `Guide/SPXW 0DTE descriptive statistics.md` L133 | Fed days (4) median range 1.59% vs 0.72%; 15 news days 0.52% vs 0.72% (N5 p 0.31); weekday ANOVA p 0.69 (S). Negative term slope only on Fed days in S (`spxw_feature_term.ipynb` c20). | D / NS |
| D80 | Term structure is upward sloping; next-expiry IV above same-day. | `spxw_week_iv_rv.ipynb` c6; `spxw_feature_term.ipynb` c20, c22 (local) | Median ATM IV same day → 1 → 5 sessions: 7.6 / 9.6 / 11.7% (S), 9.6 / 11.5 / 13.1% (F); slope median 0.20 → 0.48 (S) 9:35 → 14:35; slope vs today's IV −0.58 / −0.41. | C (held on both) |

### 8.4 Count
**80 findings** (D1–D80): 18 from hypothesis files (D1–D18) and 62 from the notebooks (D19–D80). Of these, about 30 hold on both halves (C), about 14 are one-half-only or tested on S only, about 25 are descriptive, and 10 are null results worth keeping (NS). Several C findings are same-period (D23, D25, D33, D46, D64, D73) and describe only. The **tradable-at-decision-time facts confirmed on both halves** are: D1, D2 (fixed delta only), D3, D4/D38, D44, D45, D48 (move size), D54, D61, D62, D80, plus the null results D75 and D67's spread-paid loss.

Sources not covered: notebook outputs truncated in the dumps are marked "not printed" by the readers and left out; the literature figures in `Strategy-Research/Research/*.md` (for example VRP 2016–2026, 0.59 median move/implied) are outside sources, not tests in this repo.

## 9. Not found

- Quintile bucket code (only quartiles, `GROUPS = 4`).
- Anderson–Darling or pairwise KS in the library (only in a remote notebook helper).
- A results-card function (only a snippet in `IMPLEMENTING.md`).
- A downloader estimate-only mode or an end-date flag.
- The regime threshold of the two dashboards.
- An MCP server for Backtest-Engine (planned only as "the future MCP server").
- Excalidraw diagrams in any repo.
- `hypothesis/` and `hyp_test_notebooks/` in any local checkout (GitHub `main` only).
