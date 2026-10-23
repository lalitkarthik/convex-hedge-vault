# Handover: intraday IV vs RV (for whoever continues it)

Written 12 October 2026. State gathered from `origin/main` that day, not from memory.

- **Repo:** `Convex-Hedge-Private-Limited/Convex-Hedge-Trading-Engine` (it moved from `bilal-sagar-razak/…`; the old address redirects).
- **Where the feature is:** merged to `main` on 12 October 2026 as PR #306 (merge commit `fc53142`), feature issue #265, tickets #266 to #274.
- **Read first:** the repo's `CLAUDE.md` (every behaviour change goes through its feature flow: branch, spec, tickets, PR that a person merges; docs live in the vault folder `Trading-Engine/`).
- **Decision numbers 0073 to 0078 now exist twice or three times on `main`** (other features took the same numbers). Find this feature's records by title, not number; the titles are quoted below.

## 1. What the page computes, in order

```
r_j        = ln(price_j / price_(j-1))         prices: the first candle's first price, then candle closes
RV_raw     = sum of r_j^2                       over a stretch: since the open, or the last 15 / 30 / 60 minutes
share      = usual share of a session's movement that falls in that stretch (the time-of-day profile)
RV_yearly  = sqrt( 252 * RV_raw / share )

gap        = IV - RV_yearly(since the open)
pace       = ( RV_yearly(since the open) / IV )^2
move/straddle = | level now - level at the morning reading | / straddle price at the morning reading
opening gap   = ln( today's first price / previous session's last close )
```

- Two sampling intervals: 1 minute (every candle) and 5 minutes (the last close at or before each five-minute mark from the open). SPXW uses 5 by default.
- A minute with no candle is never filled in; the next return spans the hole.
- A figure that cannot be worked out is `None` everywhere (message, store, page), never zero.
- IV is the skew's at-the-money value: a straight line between the two strikes either side of the forward.
- The morning reading is the first reading five minutes after the open.

## 2. Where it lives in the code

| What | Where |
|---|---|
| The maths, pure functions | `src/convex_trading_engine/chain/realised.py`: `realised_variance`, `is_complete`, `time_of_day_profile`, `Profile.share` / `share_of`, `yearly_volatility`, `opening_gap`, `implied_realised_gap`, `pace`, `move_against_straddle` |
| One reading per minute, the daily rows | `chain/readings.py`: `_profile` (builds the profile), `_reading` (applies it), the daily-row code further down |
| Engine wiring | `chain/engine.py` |
| Store tables | `chain/history.py`: `volatility_minutes`, `implied_minutes` (30 sessions), `volatility_days`, `implied_days` (kept for good) |
| Message and stream | `VolatilityReading` / `ExpiryReading` in `messages/models.py`; stream `chain.volatility_reading` |
| Settings | `class Volatility` in `settings/models.py`, block `[chain.volatility]` in each `config/*.toml` |
| Dashboard server | `dashboard/volatility.py` |
| Page | `frontend/src/dashboard/ivRv.ts`, `ivRvFigures.ts` and their tests, `protocol.ts`; route `/iv-rv/` |
| IV (Black-76) | `chain/volatility.py`; at-the-money value in `chain/skew.py` (`_at_forward`) |
| Tests | `tests/chain/test_realised.py`, `test_volatility_readings.py`, `test_volatility_implied.py`, `test_history_volatility.py`; frontend `ivRv.test.ts`, `ivRvPage.test.tsx` |
| Docs | `Trading-Engine/Guide/The IV vs RV page.md`; `Trading-Engine/Research/Implied against realised volatility.md` (every formula with its source); `Trading-Engine/Specs/Implied against realised volatility.md` |

Settings and their defaults (`[chain.volatility]`):

| Setting | Default | Meaning |
|---|---|---|
| `window_minutes` | 15, 30, 60 | Rolling windows |
| `sampling_minutes` | 1, 5 | Sampling intervals |
| `default_sampling_minutes` | `{SPXW = 5}` | Which interval the three numbers use, per root (1 if not listed) |
| `bucket_minutes` | 15 | Length of a profile bucket |
| `min_sessions` | 5 | Complete sessions needed before the profile stops "building history" |
| `first_candle_limit_minutes` | 2 | A session is complete only if its first candle starts within this of the open |
| `minutes_present_share` | 0.9 | …and at least this share of its minutes have a candle |
| `morning_reading_minutes` | 5 | When the morning reading is taken |
| `reading_sessions` | 30 | Sessions of per-minute rows kept |

## 3. The "five sessions" rule

- The first hour of a session is always busier than the middle. If part of a day were scaled up by the clock, every morning would look wild.
- So the engine learns a **time-of-day profile**: for each 15-minute bucket, the average share of a session's realised variance that falls in it, taken over the stored sessions (up to the 30 kept).
- A stored session counts only if it is **complete** (first candle within 2 minutes of the open, at least 9 minutes in 10 present), has the same length as today's session, and moved at all.
- With fewer than `min_sessions` (5) usable sessions the profile is **building**: `Profile.share` returns `None`, so every yearly figure is `None`, and the page shows "Building history: n of 5 sessions stored". Raw variance is still computed and stored.
- Code: `time_of_day_profile` and `Profile` in `realised.py`; called from `_profile` in `readings.py`.
- Record: "A part-day figure is scaled by the usual share of a day's movement, not by the clock" (decision 0075 of this feature).

Where this came from, said plainly: the U-shape of volatility through the day is well documented (Andersen and Bollerslev 1997, eq. (1) p. 125 and eq. (7) p. 141). The rule "divide by the usual share so far" is our own derivation; no paper was found that states it. In our simulation, after 60 of 375 minutes, scaling by the clock read 58% high (1.579) and scaling by the share read right (1.005).

## 4. Going back to plain ("normal") annualising

Plain annualising scales by the clock:

```
RV_yearly = sqrt( 252 * RV_raw * session_minutes / stretch_minutes )
```

That is the same as the current formula with `share = stretch_minutes / session_minutes`. So the change is small.

**The one place to change.** `yearly_volatility(variance, share)` already does `sqrt(252 * variance / share)`. Only the share needs to become the clock share. Two ways:

1. **Flat profile (smallest change).** In `readings.py`, `_profile` returns a `Profile` whose buckets each carry `bucket length / session minutes`, with `building=False`. `Profile.share_of` then returns exactly `stretch minutes / session minutes`, because it already interpolates in a straight line inside a bucket. Nothing else in the engine, the store, the message or the page has to change.
2. **A setting.** Add `scaling = "profile" | "clock"` to `class Volatility`, and choose the flat profile when it is `"clock"`. This keeps both and lets an instance switch. It costs more: the block is in every `config/*.toml`, and `tests/settings/test_chain_settings.py` pins each file's values.

A middle path, if the only complaint is the wait: keep the profile, but **use the clock share while the profile is building** instead of returning `None`, and keep `profile_building = true` so the page can mark the figure as rough. That is a change inside `Profile.share` (or where `_reading` calls `share_of`) plus the page's notice text.

**What changes for the person looking at the page.**

- RV appears from the first minutes of the first day. The "Building history" notice goes away (it is driven by `profile_building`).
- RV since the open reads high all morning and settles through the day; a rolling window reads high at the open and close and low at midday. Against a flat IV line this looks like a signal and is only the time of day.
- Gap and pace inherit that: pace above 1 most mornings.

**What else must be updated with it.**

- Tests that expect `None` while building or expect profile-scaled values: `tests/chain/test_realised.py`, `tests/chain/test_volatility_readings.py`, `tests/chain/test_volatility_implied.py`; the shared sample messages `tests/dashboard/socket-messages.json` (the "building history" case) and the frontend tests that read it (`ivRv.test.ts`, `ivRvPage.test.tsx`).
- Docs: `Guide/The IV vs RV page.md`, the glossary pages "Time-of-day profile" and "Building history", a new decision record that replaces "A part-day figure is scaled by the usual share…", and a changelog row.
- **Stored history mixes two scalings.** Rows written before the change hold profile-scaled volatility, rows after hold clock-scaled. The raw variance is stored beside every yearly figure (per-minute rows and daily rows), so old rows can be recomputed, or the page can recompute from raw variance. Decide which, and say so in the decision record. The daily rows are kept for good, so this matters.

## 5. Formulas

### Black-76 (the engine's implied volatility model; Black-Scholes on the forward)

```
call = D * ( F * N(d1) - K * N(d2) )
put  = D * ( K * N(-d2) - F * N(-d1) )
d1   = ( ln(F/K) + 0.5 * s^2 * T ) / ( s * sqrt(T) )
d2   = d1 - s * sqrt(T)
```

- `F` forward for the expiry (from put-call parity in the chain engine), `K` strike, `D` discount factor, `s` volatility, `N` the standard normal distribution function.
- `T` is in **trading time**: open-market time to the expiry, each session one day, divided by 252 (`time_to_expiry` in `trading_calendar/calendars.py`). Nights and weekends carry no time.
- Black-Scholes on spot is the same thing with `F = S * exp((r - q) * T)` and `D = exp(-r * T)`. The engine never prices on spot.
- Implied volatility is solved per strike from the **out-of-the-money** option's price only: Newton-Raphson with a bisection fallback, volatility kept between 0.001 and 10, price tolerance 1e-6, at most 50 iterations (`implied_volatility`, `_search` in `chain/volatility.py`).
- At-the-money IV for this feature: a straight line in strike between the two strikes bracketing the forward (`_at_forward` in `chain/skew.py`). Two other at-the-money definitions exist elsewhere in the engine (nearest strike on the chain header; call-put average in the strategies), so the header and this page can show different numbers.
- Straddle as a move: `straddle ≈ 0.8 * F * s * sqrt(T)`. The page's straddle is the call mid plus the put mid at the strike nearest the forward.

### Parkinson and the other range estimators (daily candles; not used intraday)

```
u = ln(H/O)   d = ln(L/O)   c = ln(C/O)   o = ln(O / previous C)   r = o + c

Parkinson         var = 1/(4 n ln2) * sum ( ln(H_i/L_i) )^2            1/(4 ln2) = 0.3607
Garman-Klass      var = 1/n * sum [ 0.5 (u_i - d_i)^2 - (2 ln2 - 1) c_i^2 ]     2 ln2 - 1 = 0.3863
Rogers-Satchell   var = 1/n * sum [ u_i (u_i - c_i) + d_i (d_i - c_i) ]
Yang-Zhang        var = V_o + k V_c + (1-k) V_rs
                  V_o, V_c: sample variances (divisor n-1) of o and c;  V_rs: Rogers-Satchell
                  k = 0.34 / (1.34 + (n+1)/(n-1))
Close-to-close    var = 1/(n-1) * sum ( r_i - mean r )^2
yearly volatility = sqrt( 252 * var )
```

Sources: Parkinson (1980) pp. 62-64; Garman and Klass (1980) eq. (19a); Rogers and Satchell (1991) eq. (2)-(5); Yang and Zhang (2000) eq. (7)-(11) and (18). Links and what was read are in the research note, section 2.

### Parkinson inside the day ("realised range"), if someone wants to try it

```
RV_range = 1/(4 ln2) * sum over the candles of ( ln(H_j / L_j) )^2
```

Why it was left out (decision "Realised volatility within the day is the sum of squared returns at one- and five-minute sampling"):

- It assumes each candle's high and low are the true extremes. Our one-minute candle is built from index levels that arrive about once a second, and the Indian feeds send a level only when it changes. The sampled range understates the true one.
- Simulation, research note section 5: with 75 sampled prices per candle Parkinson read about 15% low and Garman-Klass about 20% low; with 5 prices per candle and the divisor left at 4 ln 2 a range figure read 43% low. With perfect highs and lows on five-minute candles it was only as accurate as one-minute squared returns, so nothing is gained.
- The bias depends on how often ticks arrive, so it would differ by broker and by time of day. A correction exists that replaces 4 ln 2 with a constant for the number of prices per candle (Christensen and Podolskij 2007; see the research note, section 2.11, for the equations). It needs the tick count per candle, which the stored candle does not carry.
- Yang-Zhang cannot be used for "today so far": it needs at least two days and exists to handle the overnight gap.

## 6. Open items I know of

No open GitHub issue mentioned this feature when I searched on 12 October. These came up while building and checking it:

1. **RV has never been seen with real data.** Locally on a replay the page showed IV updating and "Building history: 0 of 5". Whether the deployed instances now show RV lines after the merge has not been checked.
2. **Two at-the-money IVs on one screen.** On the replay the header showed 14.96% (nearest strike, live) and the page's tile 13.89% (skew at the forward, last closed minute).
3. **Session-only RV against an IV that prices nights.** An option several days from expiry includes overnight moves; the live RV does not, so IV sits a little above RV by construction. The opening gap is shown separately and stored daily, so the overnight share can be measured later.
4. **Narrow width:** the chart legend overlaps the chart at about 480 pixels wide.
5. **Indian session length.** The research assumed 375 minutes; options have closed at 15:40 since 3 August 2026. Ticket #269 was asked to record what a real session shows on `Trading-Engine/Architecture/Chain engine design.md`; I have not read what it wrote.
6. **Positional (over weeks)** is not built. Notes are in `handoff-positional-iv-vs-rv.md` and `positional-iv-vs-rv-sources.md` beside this file.

## 7. Running and checking

```
uv sync
uv run pytest tests/chain/test_realised.py tests/chain/test_volatility_readings.py
uv run mypy src tests
uv run ruff check . && uv run ruff format --check .
```

- Frontend, inside `frontend/`: `pnpm typecheck`, `pnpm lint`, `pnpm test` (on the Windows machine this was written on, `pnpm` was not on the path and `corepack pnpm` was used).
- The full suite needs Docker. On Windows about 75 tests fail for reasons that have nothing to do with this feature (path separators, line endings, missing Unix calls); GitHub's checks are the clean signal.
- To see the page locally: a replay instance (`README.md`, "Replay a recording") and open `/iv-rv/`. A fresh store has no past sessions, so expect "Building history".

## 8. What I did not verify

- I read `realised.py` in full and the profile and annualising parts of `readings.py`. I did not read the rest of the feature's code line by line, and I did not run the tests on `main` after the merge.
- The source page and equation numbers were reported by research agents; the formulas were checked against their reports and against a simulation, but not every paper was opened by a person.
- Section 4 is a plan from reading the code, not a change I made or tested.
