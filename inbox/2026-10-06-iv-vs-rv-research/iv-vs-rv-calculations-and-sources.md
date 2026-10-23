promoted: 2026-10-23
# IV vs RV: the calculations and where each comes from

For the meeting on 7 October 2026. Part 1 is the intraday calculation as built (PR #306). Part 2 is the positional calculation as researched, not built. Each step names the source and the exact place in it.

How far to trust the source pins: research agents read the papers and reported the equation and page numbers; I checked the formulas against those reports and reran the simulation. Not every link was opened by a person. Where a paper could not be read in the original, it says so.

## In one minute

- **IV** comes out of option prices: what the market expects the index to move, per year.
- **RV** comes out of the index's own prices: what it actually moved, scaled to the same per-year figure.
- **Intraday:** RV is the sum of squared one-minute returns since the open, scaled up to a full day by how much of a day's movement usually happens by that time, then to a year with 252.
- **Positional:** RV is a daily-candle estimator (Yang-Zhang by default) over N days, set against an IV that always means "the next N days".

---

## Part 1: intraday (built)

### Step 1. Returns from one-minute candles

The chain engine already builds a one-minute candle of the index. Take the log return from each candle's close to the next.

```
r_j = ln( close_j / close_(j-1) )        the first return starts from the first candle's first price
```

A minute with no candle is not filled in; the next return spans the hole.

### Step 2. Realised variance: add up the squared returns

```
RV(open to now) = r_1^2 + r_2^2 + ... + r_M^2
```

Squaring stops ups and downs cancelling, and makes large moves count more.

**Source.** This is the standard "realised variance" estimator.

| Paper | Exact place | What it says |
|---|---|---|
| Andersen and Bollerslev (1998), "Answering the Skeptics", *International Economic Review* 39(4) | p. 897, the unnumbered formula between eq. (14) and (15); Table 3 | The sum of squared returns within the day converges to the day's true variance; the error falls as returns per day go from 1 to 288 |
| Andersen, Bollerslev, Diebold and Labys (2001), *JASA* 96 | eq. (12) definition, eq. (13) convergence, p. 44 | Defines realised volatility this way |
| Andersen, Bollerslev, Diebold and Labys (2003), *Econometrica* 71(2) | Proposition 2, eq. (3)-(4), p. 584 | The sum converges to the smooth variance plus the squared jumps |

Links: [1998](https://faculty.washington.edu/ezivot/econ589//////AndersenBollerslevIER1998.pdf) · [2001](https://public.econ.duke.edu/~boller/Published_Papers/jasa_01.pdf) · [2003](https://www.sas.upenn.edu/~fdiebold/papers/paper43/abdl4.pdf)

### Step 3. Two sampling intervals: 1 minute and 5 minutes

The same sum is also taken on five-minute returns (the last close at or before each five-minute mark from the open). One minute uses the most information. Five minutes is the check against noise, and the default for SPXW, whose level is an implied forward and not a traded index.

**Source.**

| Paper | Exact place | What it says |
|---|---|---|
| Liu, Patton and Sheppard (2015), "Does anything beat 5-minute RV?", *Journal of Econometrics* 187(1) | Abstract p. 293; section 6 p. 309 | Across many assets, little beats plain five-minute realised variance |
| Andersen, Bollerslev, Diebold and Labys (2000), "Great realizations", *Risk* 13(3) | p. 106 | The "signature plot": sampling too finely inflates the figure through price noise |
| Our simulation | Research note section 5, noise table | With 2 basis points of tick noise, RV read 19% high at 1 minute and 4% high at 5 minutes |

Links: [Liu et al.](https://public.econ.duke.edu/~ap172/Liu_Patton_Sheppard_JoE_2015.pdf) · [Great realizations](https://public.econ.duke.edu/~boller/Published_Papers/risk_00.pdf)

### Step 4. Scale part of a day up to a whole day

By 11:00 only part of the day's movement has happened, and the first hour is always the busiest. So we do not scale by the clock. From the stored sessions (up to 30) the engine learns the usual share of a day's movement in each 15-minute bucket, and divides by the share that has usually happened by now.

```
full-day variance estimate = RV(open to now) / share(open to now)
```

With fewer than five stored sessions the page shows "building history" and draws no RV line.

**Source.**

| Source | Exact place | What it says |
|---|---|---|
| Andersen and Bollerslev (1997), "Intraday periodicity and volatility persistence", *Journal of Empirical Finance* 4 | eq. (1) p. 125; eq. (7) p. 141; appendix eq. (A.1)-(A.4) pp. 152-153 | Volatility follows a repeating U-shape through the day, which must be removed before intraday figures are compared |
| Our simulation | Research note section 5, part-day table | After 60 of 375 minutes, scaling by the clock read 58% high (1.579); scaling by the usual share read right (1.005) |

**Our own step, say so plainly:** the papers establish the U-shape. The exact rule "divide by the usual share so far" is our derivation from their model. No paper was found that states it; it is confirmed by our simulation only.

Link: [1997](https://public.econ.duke.edu/~boller/Published_Papers/joef_97.pdf)

### Step 5. Scale a day to a year

```
RV (yearly) = sqrt( 252 x full-day variance estimate )
```

252 trading days, each session counted as one day. This is the same count of time the engine uses to compute IV, so the two lines share a scale. Variance adds across time; volatility does not, which is why the scaling is done on variance and the square root is taken last.

**Source.** The engine's own convention (its trading-days-per-year constant, used for IV). The same 252-day annualising is in Cboe's realised volatility index method: [Cboe RVOL methodology](https://cdn.cboe.com/resources/indices/documents/RVOL_Methodology.pdf).

### Step 6. The IV side

- IV per strike: the Black-76 model on the forward, already in the engine.
- At-the-money IV: the skew's value at the forward, a straight line between the two strikes either side of it (decision 0076).
- One value per minute: the latest at or before the minute's end.

**Source.** Existing engine behaviour, not new work: the vault note "Implied forwards, volatility and Greeks" and its decisions.

### Step 7. The three numbers

| Number | Formula | Where it comes from |
|---|---|---|
| Gap | IV minus RV, in volatility points | The variance risk premium. AlgoTest uses exactly "VRP = IV − RV" ([blog](https://algotest.in/blog/iv-vs-rv-and-trading-edge-with-vrp/)). Carr and Wu (2009) define it on variance with the opposite sign |
| Pace | (RV ÷ IV) squared | Our own figure. It equals realised variance so far over the variance IV budgeted for this part of the day. It rests on the hedged-option result that profit follows realised minus implied variance: Bossu, Strasser and Guichard (2005), section 2.1, Eq. 4 and 5 ([link](http://docs.sbossu.com/bossu-strasser-guichard-varswap.pdf)); Carr and Madan (1998), eq. (9) |
| Move against straddle | Absolute move since the morning reading ÷ the at-the-money straddle's price that morning | The straddle is the market's price for the move: straddle ≈ 0.8 × forward × IV × √time. Brenner and Subrahmanyam (1988) is the usual citation but could not be reached; we derived it from Black-76 and checked it numerically. Bennett prints the 0.4 form for one option at p. 44 ([book](https://www.trading-volatility.com/Trading-Volatility.pdf)) |

The morning reading is taken five minutes after the open.

### Worked example (made-up numbers)

```
11:00, 105 one-minute returns so far
Sum of squared returns                 = 0.0000120
Usual share of a day's movement by 11:00 = 0.40
Full-day variance estimate             = 0.0000120 / 0.40      = 0.0000300
Yearly variance                        = 0.0000300 x 252       = 0.00756
RV                                     = sqrt(0.00756)         = 8.7%

IV of the chosen expiry                = 12.0%
Gap                                    = 12.0 - 8.7            = 3.3 points
Pace                                   = (8.7 / 12.0)^2        = 0.52   (52% of the budgeted movement used)
Move against straddle                  = 62 points / 118 points = 0.53
```

### Choices that are ours, not a paper's

- The 15-minute bucket, the five-session minimum, and the "complete session" test (first candle within two minutes of the open, nine in ten minutes present).
- The live RV covers the session only. The opening gap is shown separately. An option several days from expiry also prices the nights, so its IV sits a little above session-only RV by construction.
- Pace, as a named figure.

---

## Part 2: positional (researched, not built)

### The rule: same length on both sides

A 30-day IV goes against a 30-day RV; a 7-day IV against a 7-day RV.

| Source | Exact place |
|---|---|
| AlgoTest VRP tool docs | "Best Practices: Match Time Horizons. 30 d IV ↔ 30 d RV, 7 d IV ↔ 7 d RV" ([link](https://docs.algotest.in/clicktrade/strategy-builder/vrp-analysis-tool/)) |
| Bennett, *Trading Volatility* | p. 234 ([book](https://www.trading-volatility.com/Trading-Volatility.pdf)) |
| Montréal Exchange, "Trading Volatility Using Historical Volatility Cones", describing Burghardt and Lane (1990) | The passage on comparing 1-month implied with 1-month historical ([link](https://www.m-x.ca/f_publications_en/cone_vol_en.pdf)). The 1990 article itself was not read |

### RV from daily candles

```
o = ln(O_i/C_(i-1))   u = ln(H_i/O_i)   d = ln(L_i/O_i)   c = ln(C_i/O_i)   r = o + c

Close-to-close    var = 1/(n-1) x sum (r_i - mean r)^2
Parkinson         var = 1/(4 n ln2) x sum (u_i - d_i)^2
Garman-Klass      var = 1/n x sum [ 0.5 (u_i - d_i)^2 - (2 ln2 - 1) c_i^2 ]
Rogers-Satchell   var = 1/n x sum [ u_i (u_i - c_i) + d_i (d_i - c_i) ]
Yang-Zhang        var = V_o + k V_c + (1-k) V_rs,   k = 0.34 / (1.34 + (n+1)/(n-1))
RV (yearly)       = sqrt(252 x var)
```

| Estimator | Paper | Exact place | Read in |
|---|---|---|---|
| Parkinson | Parkinson (1980), *Journal of Business* 53(1) | Unnumbered equations pp. 62-64; the 0.361 constant on p. 63 | JSTOR scan ([link](http://mmquant.net/wp-content/uploads/2016/08/michael_parkinson.pdf)) |
| Garman-Klass | Garman and Klass (1980), *Journal of Business* 53(1) | eq. (19a) is the practical form above; eq. (19) the exact one | The authors' re-typeset copy hosted by CME, not the journal pages ([link](https://www.cmegroup.com/trading/fx/files/a_estimation_of_security_price.pdf)) |
| Rogers-Satchell | Rogers and Satchell (1991), *Annals of Applied Probability* 1(4) | eq. (2)-(5) | The authors' typescript; numbering is the typescript's ([link](https://www.skokholm.co.uk/wp-content/uploads/2016/01/R_Satchell_HLOC.pdf)) |
| Yang-Zhang | Yang and Zhang (2000), *Journal of Business* 73(3) | eq. (7) the estimator, (8) V_o, (9) V_c, (3) V_rs, (10) and (18) the weight k, (11) efficiency | The journal's pages ([link](https://atmif.com/papers/range.pdf)) |

Why Yang-Zhang is the default (our simulation, research note section 5): with a quarter of the movement overnight, Parkinson, Garman-Klass and Rogers-Satchell all read 25% low; Yang-Zhang stayed within 0.5%. It was also about 7 times as accurate as close-to-close over 20 days.

### The IV side: constant maturity

Blend the two expiries either side of the target, on total variance:

```
s* = sqrt( (1/T*) x [ T1 s1^2 (T2 - T*)/(T2 - T1)  +  T2 s2^2 (T* - T1)/(T2 - T1) ] )
example: 24 days at 12% and 31 days at 13%  ->  30 days at 12.89%
```

| Source | Exact place |
|---|---|
| Cboe, *Volatility Index Mathematics Methodology* | Section "(b) Constant Maturity Term"; the same step is "Step 3" of the VIX white paper ([link](https://cdn.cboe.com/resources/indices/Cboe_Volatility_Index_Mathematics_Methodology.pdf)). Checked by recomputing the white paper's worked example: 13.686 against the printed 13.69 |
| NSE, India VIX white paper | Uses the same step on near-month and next-month NIFTY options to reach 30 calendar days ([link](https://nsearchives.nseindia.com/web/sites/default/files/inline-files/white_paper_IndiaVIX.pdf)) |
| AlgoTest VRP tool docs | "Constant Maturity: 7 d, 21 d, 30 d, or 90 d" |

### Trailing, and "what followed"

- Trailing: RV of the N days before each date. Answers "are options priced above how the market has been moving?"
- What followed: the same RV line shifted back by N days so it sits under the IV that forecast it. Answers "was the forecast right?"

| Source | Exact place |
|---|---|
| AlgoTest VRP tool docs | "Lag RV: Aligns prediction dates (IV) with outcome dates (RV)" |
| Quantsapp classroom | "FRV data series leads by 20 days, as compared to HV" ([link](https://web.quantsapp.com/quantsapp-classroom/Volatility/futures-realized-volatility-&-stock-trading)) |
| Carr and Wu (2009), "Variance Risk Premiums", *Review of Financial Studies* 22(3) | eq. (1), (2) and section 4.1, read in the 2004 draft ([listing](https://ideas.repec.org/a/oup/rfinst/v22y2009i3p1311-1341..html)) |

### What positional needs that we do not have

- Past daily index candles: about two years (500 rows per underlying) for a year of chart plus rank and percentile.
- Options further out than the feed takes today: about 14 days out for a 7-day IV, about 45 for a 30-day IV. Only the two expiries either side of the target, and only strikes near the forward.
- The IV line can only begin the day recording starts.

---

## What was not confirmed

- **The part-day scaling rule** (Step 4) is our derivation, backed by simulation, not by a paper that states it.
- **Brenner and Subrahmanyam (1988)** could not be reached; the straddle approximation was derived and checked by us.
- **Garman-Klass and Rogers-Satchell** were read in the authors' own copies, not the journal pages.
- **Burghardt and Lane (1990)** was read only through the Montréal Exchange paper.
- **Carr and Wu** was read in the 2004 working draft.
- **AlgoTest's "Integrated" estimator** and its sampling options are not documented publicly.
- **NIFTY's overnight share of movement** has no published figure; the engine's daily rows will measure it.
- **The Indian session length:** the research assumed 375 minutes, while options have closed at 15:40 since 3 August 2026. The profile is learned from stored sessions, so it adapts either way.

Full detail: `Trading-Engine/Research/Implied against realised volatility.md` on `feature/iv-vs-rv` (PR #306), sections 2, 3, 4.5, 5, 7 and 8.
