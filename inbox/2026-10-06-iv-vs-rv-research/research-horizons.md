promoted: 2026-10-23
# Matching implied and realised volatility fairly: intraday and positional horizons

Research note for the implied-versus-realised volatility feature. Written 2026-10-06.

**What this note is.** It answers one question: when a chart puts implied volatility (IV) next to realised volatility (RV), which IV figure and which RV figure belong together, for a trader who holds for minutes or hours and for one who holds for days or weeks. It does not repeat the RV estimator formulas (see `research-estimators.md`) or the survey of existing products (see `research-dashboards.md`, which also defines IV rank, IV percentile, the volatility cone and the expected move). It refers to both.

**Verification labels.**

- `VERIFIED AGAINST PRIMARY` — the equation or sentence was read in the paper or the publisher's own document. Two sub-cases, stated each time:
  - *(text read)*: read directly in the extracted text of the PDF held in `src/`.
  - *(tool quote)*: the PDF was read through a web extraction tool that returned the equation and its number. Equation numbers are reliable; page numbers from this route are approximate.
- `UNVERIFIED AGAINST PRIMARY` — the primary could not be reached. What was checked instead is stated.
- *Derived here* — arithmetic or reasoning done in this note from verified inputs. Treat as reasoning to be checked in design.

**Words used.**

- **Variance** is volatility squared. **Total variance** to a date is annual variance times the time left in years, $w = \sigma^2 T$. It is the quantity an option price actually fixes; the quoted volatility is total variance divided by a chosen clock.
- **ATM** means at the money: the strike equal to the forward price $F$.
- **Delta hedging**: trading the underlying so the position does not gain or lose from a small price move. **Gamma** ($\Gamma$) is how fast that hedge has to change. **Dollar gamma** is $\Gamma S^2$.
- **Variance swap rate**: the fixed variance a variance swap buyer pays in exchange for the realised variance. It equals the expected variance under option-market pricing.
- **Session**: one exchange trading day (375 minutes on NSE, 390 on the US cash market).
- **The engine's clock**: time to expiry counted in sessions over 252, each session one day, the night carrying no time of its own.

---

## 1. What exactly is being compared

IV is a price-implied forecast of variance over the option's *remaining* life. Trailing RV is a measurement of the *past*. People make three different comparisons and they answer different questions.

### 1a. IV now against trailing RV

$$ VRP_t \equiv IV_t - RV_t $$

where $IV_t$ is the option-implied expected variance over $[t, t+1]$ and $RV_t$ is the variance realised over $[t-1, t]$. `VERIFIED AGAINST PRIMARY` *(text read)*: Bollerslev, Tauchen and Zhou, eq. (22) and the sentence before it [2]. They use the squared VIX for $IV_t$ and the sum of 78 five-minute squared returns per day plus the squared close-to-open return for $RV_t$ [2].

- **Answers:** is the market pricing more movement ahead than we have just had?
- **Strength:** both numbers are known at time $t$. The authors say so: "$IV_t$ and $RV_t$, and therefore $VRP_t$, are directly observable at time t" [2].
- **Weakness:** it compares two different periods. It is only fair if the recent past is a good guide to the near future.
- **Size (S&P 500, monthly, January 1990 to December 2007):** mean implied variance 33.23, mean realised 14.93, gap 18.30, in monthly percent squared [2]. *Derived here:* that is about 20.0 against 13.4 in annual volatility points ($\sqrt{33.23 \times 12}$ and $\sqrt{14.93 \times 12}$).

### 1b. IV on a past day against the RV that then followed (the ex-post premium)

$$ RP_{t,T} \equiv RV_{t,T} - SW_{t,T}, \qquad LRP_{t,T} \equiv \ln\!\left(\frac{RV_{t,T}}{SW_{t,T}}\right), \qquad SW_{t,T} = E^{Q}_t\!\left[RV_{t,T}\right] $$

$SW_{t,T}$ is the variance swap rate fixed at $t$; $RV_{t,T}$ is the variance realised from $t$ to $T$. `VERIFIED AGAINST PRIMARY` *(text read)*: Carr and Wu, eq. (1), (2) and section 4.1, in the May 2004 working-paper draft of the 2009 article [1]. Equation numbers in the journal version may differ.

Their realised side, matched to a 30-calendar-day swap rate, is

$$ RV_{t,t+30} = \frac{365}{30}\sum_{i=1}^{30}\left(\frac{F_{t+i,t+30}-F_{t+i-1,t+30}}{F_{t+i-1,t+30}}\right)^{2} $$

`VERIFIED AGAINST PRIMARY` *(text read)*: eq. (51) [1]. Note three choices: calendar days on both sides, returns of the *forward* not the spot, and no mean removed.

- **Answers:** did option sellers get paid? This is the only comparison that measures the premium actually earned.
- **Weakness:** the answer for today's IV is not known until expiry. On a chart the last $T-t$ days are empty.
- **Sign warning:** Carr and Wu write realised minus implied (negative on average). Bollerslev, Tauchen and Zhou write implied minus realised (positive on average). A chart must say which.
- **Size (S&P 500, 4 January 1996 to 28 February 2003, 1,779 days, 30-day horizon):** mean realised 18.82, mean variance swap rate 24.41, mean ATM implied 21.28, all in volatility points (Table 4). Mean of $100 \times (RV - SW)$ is −2.279; mean $\ln(RV/SW)$ is −0.594 with a t-statistic of −9.48 (Table 5) [1]. These are the draft's figures; the published article uses a longer sample.

The same premium seen from a hedged option position: Bakshi and Kapadia define the **delta-hedged gain**

$$ \Pi_{t,t+\tau} \equiv C_{t+\tau} - C_t - \int_t^{t+\tau}\Delta_u\,dS_u - \int_t^{t+\tau} r\left(C_u - \Delta_u S_u\right)du $$

and show that with continuous hedging $E_t(\Pi_{t,t+\tau}) = \int_t^{t+\tau} E_t\!\left(\lambda_u \frac{\partial C_u}{\partial \sigma_u}\right)du$, where $\lambda$ is the price of volatility risk; it is zero if volatility risk is not priced, and discrete hedging adds only a bias of order $1/N$. `VERIFIED AGAINST PRIMARY` *(tool quote)*: eq. (1), eq. (6) for the discrete version and Proposition 1 [3]. For S&P 500 options, 1988 to 1995, ATM 30-day calls hedged daily to expiry lost $0.47 on average (t = −2.34) [3].

### 1c. IV now against a forecast of RV

$$ EVRP_t \equiv IV_t - E_t\!\left(RV_{t+1}\right) $$

`VERIFIED AGAINST PRIMARY` *(text read)*: Bollerslev, Tauchen and Zhou, text after eq. (22) and section 5 [2]. They forecast with the HAR-RV model (section 6 below).

- **Answers:** the fair question — implied future against expected future.
- **Weakness:** the answer now depends on a model.
- **How much it adds:** in their sample the correlation between $EVRP$ and the simple $VRP$ of 1a is 0.85 (footnote 30) [2]. Trailing RV already carries most of the information.

### What the practitioner books add

- Bennett: "The implied volatility of options is on average 1-2pts above the volatility realised over the life of the option", larger for indices than single stocks (p. 15) [12]. `VERIFIED AGAINST PRIMARY` *(tool quote)*.
- Sinclair (*Volatility Trading*, *Positional Option Trading*) and Natenberg (*Option Volatility and Pricing*) could not be reached. Nothing in this note rests on them. `UNVERIFIED AGAINST PRIMARY`.

---

## 2. Why the gap matters to a hedged option position

### The formula

Sell a claim at implied volatility $\sigma_h$ and delta hedge it with the Black model delta computed at $\sigma_h$, while the true instantaneous volatility is $\sigma_t$. The seller's profit at the end of the hedge, $T'$, is

$$ P\&L = \int_T^{T'} e^{r(T'-t)}\,\frac{F_t^2}{2}\,\frac{\partial^2 V}{\partial F^2}(F_t,t;\sigma_h)\,\left(\sigma_h^2-\sigma_t^2\right)dt $$

`VERIFIED AGAINST PRIMARY` *(text read)*: Carr and Madan, "Towards a Theory of Volatility Trading", eq. (9), with the sentence "the instantaneous P&L from delta-hedging it … is … the difference between the hedge variance rate and the realized variance rate, weighted by half the dollar gamma" [4]. For the buyer the sign flips: realised minus implied.

The discrete, daily version:

$$ \text{Daily P\&L} = \tfrac12\,\Gamma S^2\left[\left(\frac{\Delta S}{S}\right)^2 - \sigma^2\,\Delta t\right], \qquad \text{Final P\&L} = \tfrac12\sum_{t=0}^{n}\gamma_t\left[r_t^2 - \sigma^2\,\Delta t\right] $$

with $r_t$ the return over step $t$ and $\gamma_t = \Gamma_t S_t^2$ the dollar gamma. `VERIFIED AGAINST PRIMARY` *(tool quote)*: Bossu, Strasser and Guichard, section 2.1, Eq. 4 and Eq. 5, built from Eq. 3, $\Theta \approx -\tfrac12 \Gamma S^2 \sigma^2$ [5]. The same balance is Demeterfi, Derman, Kamal and Zou, EQ 12: $\Theta + \tfrac12 \Gamma S^2\sigma^2 = 0$ *(text read)* [7].

A third statement: hedging at implied volatility $\tilde\sigma$ when actual volatility is $\sigma$, the mark-to-market profit over $dt$ is $\tfrac12(\sigma^2-\tilde\sigma^2)S^2\Gamma^i\,dt$ and the total is $\tfrac12(\sigma^2-\tilde\sigma^2)\int_{t_0}^{T}e^{-r(t-t_0)}S^2\Gamma^i\,dt$: "always positive, but highly path dependent". Hedging at the actual volatility instead locks in a known total, $V^a - V^i$, but "on a mark-to-market basis you could lose before you gain". `VERIFIED AGAINST PRIMARY` *(tool quote)*, with a caveat: read in Wilmott's lecture slides of the same title [6]; the journal article (Ahmad and Wilmott, *Wilmott* magazine, 2005) is behind a login, so its equation numbers are not confirmed.

### What it implies about which RV to watch

1. **The RV that pays is measured at the hedging frequency.** $r_t$ in the sum is the return between two hedges. A position hedged every five minutes earns five-minute realised variance. A position hedged at each close earns close-to-close variance. A chart of daily-bar RV says little about a position hedged intraday on a day that swings and closes flat.
2. **Over the life of the position, forward from entry.** The sum runs from entry to exit. A trailing window that ends at entry is a forecast input, not the thing earned.
3. **Weighted by dollar gamma, not equally.** Movement when the price is near the strike and expiry is close counts far more. Equal-weighted RV can sit below IV while a short-gamma position still loses. Bossu et al. note that even with returns drawn at exactly $\sigma$, Eq. 5 "does not become nil", an effect "mostly due to discrete hedging" [5].
4. **Variance, not volatility.** The bracket is a difference of variances. The natural unit of the gap is variance; a gap in volatility points is an approximation that works near the strike level (section 3e).
5. **Overnight counts only if it is held.** A position opened and closed inside a session never sees the overnight gap. A position held over nights does.

*Derived here.* For the engine's delta-hedged long straddle the scoreboard is therefore: realised variance since entry at the hedge interval, against the implied variance paid at entry, both for the same stretch of time. Trailing RV is context.

---

## 3. Which implied figure

### 3a. ATM implied volatility of one expiry

- **What it is.** The volatility that makes the model price of the ATM option equal its market price. In the engine: Black-76 on the forward, trading-day clock.
- **Strengths.** It is the volatility of the instrument actually traded (the straddle). It needs one strike. It is available now for every subscribed expiry.
- **Weaknesses.**
  - Its horizon shrinks every day and jumps when the series rolls, so a time series of "front-expiry IV" is a sawtooth, not one quantity.
  - It ignores the skew. It sits close to the volatility swap rate, below the variance swap rate: Carr and Wu use the interpolated ATM IV "as an approximation for the volatility swap rate", and their S&P 500 means are 21.28 (ATM) against 24.41 (variance swap) [1].
  - In the last hours of an option's life the ATM strike changes with every tick and the price is small relative to the bid-ask spread, so the figure is unstable.

### 3b. Constant-maturity IV by interpolating total variance

Take two expiries with times $T_1 < T^* < T_2$ and variances $\sigma_1^2, \sigma_2^2$. Interpolate *total variance* linearly in time, then convert back:

$$ \sigma^{*} = \sqrt{\frac{1}{T^*}\left[T_1\sigma_1^2\,\frac{T_2-T^*}{T_2-T_1} + T_2\sigma_2^2\,\frac{T^*-T_1}{T_2-T_1}\right]} $$

The Cboe form, for a 30-day target, with $N$ counting minutes:

$$ VIX = 100\times\sqrt{\left\{T_1\sigma_1^2\left[\frac{N_{T_2}-N_{30}}{N_{T_2}-N_{T_1}}\right]+T_2\sigma_2^2\left[\frac{N_{30}-N_{T_1}}{N_{T_2}-N_{T_1}}\right]\right\}\times\frac{N_{365}}{N_{30}}} $$

`VERIFIED AGAINST PRIMARY` *(text read, and recomputed)*: Cboe VIX white paper, Step 3 [9]; the same formula with a general constant-maturity term $N_{CM}$ is in the Cboe mathematics methodology, section "(b) Constant Maturity Term" [8]. The symbols were partly lost in text extraction, so the structure was confirmed by recomputing the white paper's worked example ($T_1 = 0.0683486$, $\sigma_1^2 = 0.0184629$, $N_{T_1} = 35{,}924$, $T_2 = 0.0882686$, $\sigma_2^2 = 0.018821$, $N_{T_2} = 46{,}394$): the formula above gives 13.686, the paper prints 13.69.

- **Strengths.** One fixed horizon every day, so the series is comparable through time and can be set against a fixed RV window.
- **Weaknesses.**
  - It needs an expiry on each side of the target. Carr and Wu "do not extrapolate" [1].
  - Linear in *which* clock? Cboe uses calendar minutes. If a weekend or an event sits between the two expiries, variance does not arrive evenly in calendar time and the interpolated figure is off (section 5d).
  - **For the engine today:** feeds cover 0 to 7 days in India and 0 to 1 day for SPXW. No 30-day figure can be built. In India a 0-to-7-day window usually holds a single weekly expiry, so even a short constant maturity cannot be bracketed. For SPXW the same-day and next-day expiries could give a one-day figure in the style of VIX1D (section 5d).

### 3c. A model-free, VIX-style figure

For one expiry:

$$ \sigma^2 = \frac{2}{T}\sum_i \frac{\Delta K_i}{K_i^2}\,e^{RT}\,Q(K_i) \;-\; \frac{1}{T}\left[\frac{F}{K_0}-1\right]^2 $$

$Q(K_i)$ is the mid price of the out-of-the-money option at strike $K_i$ (put below $K_0$, call above, the average of both at $K_0$); $K_0$ is the first strike at or below the forward $F$; $\Delta K_i$ is half the distance between the strikes either side. `VERIFIED AGAINST PRIMARY` *(text read)*: Cboe white paper, "The generalized formula" [9]; Cboe mathematics methodology, formula (1) [8]. It is the discrete form of the variance swap replication: Carr and Wu, eq. (5), $E^Q_t[RV_{t,T}] = \frac{2}{T-t}\int_0^\infty \frac{\Theta_t(K,T)}{B_t(T)K^2}dK + \varepsilon$ [1]; Cboe cites Demeterfi et al. [7] for it.

**Time in VIX:** $T = \{M_{\text{current day}} + M_{\text{settlement day}} + M_{\text{other days}}\} / \text{minutes in a year}$, with 525,600 minutes in a 365-day year: calendar time to the minute *(text read)* [8][9].

**India VIX** uses the same formula with these changes *(text read)* [10]:

- near-month and next-month NIFTY options, bracketing "a 30-day calendar period";
- the forward is "the latest available price of NIFTY future contract" of that expiry, not a put-call parity forward;
- the rate is NSE MIBOR (30 or 90 days);
- time is minutes to the 3:30 pm close over 525,600; the worked example gives $T_1 = \{510 + 930 + 11{,}520\}/525{,}600 = 0.02466$;
- missing or wide quotes are filled with a natural cubic spline;
- with 3 trading days left it rolls to the next and far month.

- **Strengths.** No pricing model. It includes the skew. It is the exact counterpart of realised *variance*: it is what a variance swap would pay against.
- **Weaknesses.**
  - It needs a wide strip of reliable quotes. With few strikes or wide spreads it is biased (truncation and coarse strike spacing; Demeterfi et al. section "Imperfect Hedges" [7]).
  - It is a variance figure, higher than ATM volatility whenever there is a skew. With a skew linear in strike of slope $b$, $K_{var} \approx \sigma_0^2(1+3Tb^2)$: Demeterfi et al. EQ 31 *(text read)* [7]; the same rule appears in Bossu et al. as $K_{var} \approx \sigma_{ATMF}\sqrt{1+3T\times skew^2}$ *(tool quote)* [5]. So "VIX-style IV minus RV" overstates the edge of an ATM straddle seller: part of the gap is the price of the wings.
  - India VIX is a 30-calendar-day, monthly-expiry figure. It is not the implied volatility of a weekly NIFTY option and should not sit opposite a weekly option's RV.

### 3d. The ATM straddle price as an implied move

For a call and a put struck at the forward, Black-76 gives $C = P = e^{-rT}F\left[2N\!\left(\tfrac{\sigma\sqrt T}{2}\right)-1\right]$. Using $N(x) \approx \tfrac12 + \tfrac{x}{\sqrt{2\pi}}$ for small $x$:

$$ C \approx \frac{1}{\sqrt{2\pi}}\,F\sigma\sqrt{T}\,e^{-rT} \approx 0.4\,F\sigma\sqrt T, \qquad \text{Straddle} = C+P \approx \sqrt{\frac{2}{\pi}}\,F\sigma\sqrt{T}\,e^{-rT} \approx 0.8\,F\sigma\sqrt T $$

$$ \sigma \approx \sqrt{\frac{2\pi}{T}}\,\frac{C}{F} = \sqrt{\frac{\pi}{2T}}\,\frac{\text{Straddle}}{F} $$

- **Source.** Brenner and Subrahmanyam (1988), *Financial Analysts Journal* 44(5), 80–83 [11]. `UNVERIFIED AGAINST PRIMARY`: the article is paywalled. Checked instead: (i) the derivation above from Black-76; (ii) *derived here*, a numerical comparison with the exact formula — the error is 0.002% for 12% volatility with 7 sessions left, 0.01% for 20% and 30 days, 0.12% for 60% and 30 days, 4% for 100% and one year; (iii) Bennett prints "ATM call price ≈ 0.4 × σ × √T" (p. 44) *(tool quote)* [12].
- **What it means.** *Derived here:* a straddle struck at $K$ pays $|F_T - K|$, so the undiscounted ATM straddle price *is* the market's expected absolute move to expiry, with no model at all. For a normal distribution the mean absolute move is $\sqrt{2/\pi} \approx 0.80$ of one standard deviation. So:
  - the straddle price belongs opposite the realised *absolute move* $|F_T - F_0|$;
  - the one-standard-deviation band $F\sigma\sqrt T$ is 1.25 times the straddle;
  - the engine's band "IV divided by root 252" is a one-standard-deviation move for one session, not the straddle's break-even.
- **Strengths.** A price, in index points, that a trader can act on. No day-count convention enters: the clock argument disappears.
- **Weaknesses.** One realised move is a very noisy sample; it takes many expiries to judge. It is only "ATM" at the moment it is struck.

### 3e. Volatility figures against variance figures

- The square root is concave, so the average of volatilities is below the root of the average variance (Jensen's inequality). A volatility swap struck at $K_{vol}$ is approximated by variance: $\sigma_R - K_{vol} \approx \frac{1}{2K_{vol}}\left(\sigma_R^2 - K_{vol}^2\right)$, and the difference between the two payoffs is the **convexity bias** $\frac{1}{2K_{vol}}\left(\sigma_R - K_{vol}\right)^2$. `VERIFIED AGAINST PRIMARY` *(text read)*: Demeterfi et al. EQ 43, EQ 44 and the text under Figure 11 [7].
- Bennett: "The square root of the variance strike is always above volatility swaps (and ATMf implied as volatility swaps ≈ ATMf implied)" (p. 52) *(tool quote)* [12].
- **Where it matters for the chart.**
  - Pair like with like: VIX-style implied variance with realised variance; ATM IV with realised volatility.
  - When averaging over days, average variances and take the root at the end.
  - A gap in volatility points and a gap in variance points rank days differently when the level changes. A 2-point gap at 10% volatility is $12^2 - 10^2 = 44$ variance points; at 30% it is 124.

---

## 4. Positional horizon (days to weeks)

### 4a. Match the RV window to the option's days to expiry

- The rule, from the Montréal Exchange's write-up of Burghardt and Lane: "implied volatilities of options with 1 month to expiry are compared with 1-month historical volatilities, while implied volatilities of options with 3 months to expiry are compared with 3-month historical volatilities" *(text read)* [13].
- Bennett: "Some investors believe the best number of days of historical volatility to look at is the same as the implied volatility of interest" (p. 234) *(tool quote)* [12].
- So an option with $n$ sessions left sits opposite RV over $n$ sessions: the last $n$ for comparison 1a, the next $n$ for comparison 1b.
- **The short-window problem.** *Derived here* (standard result; see the efficiency discussion in `research-estimators.md`): the standard error of a volatility estimated from $n$ daily returns is about $\sigma/\sqrt{2n}$. That is 32% of the level for $n=5$ and 15% for $n=21$. A five-day close-to-close RV is too noisy to set against a weekly option. For horizons of 1 to 7 sessions the RV must be built from intraday returns (hundreds of observations per session), with the overnight gaps added.

### 4b. Trading days against calendar days, on both sides

- Total variance is fixed by the option price. The quoted volatility depends on the clock: $\sigma_{cal}^2 T_{cal} = \sigma_{trd}^2 T_{trd}$, so $\sigma_{cal} = \sigma_{trd}\sqrt{T_{trd}/T_{cal}}$.
- *Derived here*, the ratio $\sigma_{cal}/\sigma_{trd}$ for the same option price:

| Situation | Calendar time | Trading time | Ratio |
| --- | --- | --- | --- |
| 1 calendar day, 1 session | 1/365 | 1/252 | 1.20 |
| Friday close to Monday close | 3/365 | 1/252 | 0.69 |
| 4 calendar days, 2 sessions | 4/365 | 2/252 | 0.85 |
| 7 calendar days, 5 sessions | 7/365 | 5/252 | 1.02 |
| 30 calendar days, 21 sessions | 30/365 | 21/252 | 1.01 |

- At a month the choice hardly matters. Inside a week it moves the figure by up to 30%, and the size depends on the day of the week.
- **Conventions in the sources.** Carr and Wu: 365/30 on both sides [1]. Cboe VIX and India VIX: calendar minutes over 525,600 [8][10]. Cboe's realised volatility indices: 252, mean set to zero *(text read)* [27]. Bossu et al.'s variance swap term sheet: 252 [5]. So "VIX against 252-day RV" already mixes clocks, harmlessly at 30 days.
- **Rule.** Annualise RV with the same clock the IV was solved with. Or compare total variance (or the expected move in points) and skip annualising altogether.
- **The engine.** IV uses sessions over 252. RV must therefore be annualised by 252 sessions per year, and a multi-day RV must include the overnight gaps, because the option's price includes them even though the clock gives them no time.

### 4c. The volatility cone

Defined in `research-dashboards.md` section 5.3. Burghardt and Lane (1990), "How to Tell if Options Are Cheap", *Journal of Portfolio Management*: `UNVERIFIED AGAINST PRIMARY` (paywalled); read through the Montréal Exchange paper [13]. Its use here: it answers "is this IV high *for its maturity*" by placing IV inside the historical spread of RV for a window of the same length. Two cautions:

- The bands come from overlapping windows (4e), so they look smoother and more certain than they are.
- It needs long history. Thirty sessions hold only 26 overlapping five-session windows and about 6 independent ones. A cone cannot be built from the engine's present data.

### 4d. IV rank and IV percentile

Defined in `research-dashboards.md` sections 5.1 and 5.2. They compare IV with its own past, not with RV. They need about a year of stored IV. For a single expiry they are distorted by the sawtooth of 3a: a 2-day option and a 6-day option are not the same quantity. They only make sense on a constant-maturity series.

### 4e. Overlapping windows

- A daily series of a 30-day ex-post premium shares 29 of 30 days between neighbours. It is strongly autocorrelated by construction.
- Carr and Wu handle it with Newey-West standard errors "with a lag of 30 days" for the overlapping daily series, and six lags for non-overlapping monthly series *(text read)* [1]. Bollerslev, Tauchen and Zhou warn that "overlapping multi-period return regressions need to be interpreted with great caution" [2].
- **For the chart.** The number of independent observations is roughly the number of days divided by the window. One bad week appears as a long run of bad daily points. Any statistic shown (hit rate, average premium) should be computed on non-overlapping windows, for example one per expiry.

### 4f. Typical size of the premium for index options

| Market | Figure | Source |
| --- | --- | --- |
| S&P 500, 30 days, 1996–2003 | realised 18.82, variance swap 24.41, ATM 21.28 volatility points; $\ln(RV/SW)$ mean −0.594 | Carr and Wu, Tables 4 and 5 [1] *(text read)* |
| S&P 500, monthly, 1990–2007 | implied variance 33.23, realised 14.93 (monthly percent squared) | Bollerslev, Tauchen and Zhou [2] *(text read)* |
| S&P 500 options, 1988–1995 | ATM 30-day calls, delta hedged daily: −$0.47 on average | Bakshi and Kapadia [3] *(tool quote)* |
| Indices generally | implied 1–2 points above the volatility realised over the option's life | Bennett p. 15 [12] *(tool quote)* |
| NIFTY 50, August 2022 – March 2026 | ATM Black-76 IV minus Yang-Zhang RV: mean +1.208 points, positive on 74.9% of 887 days, mean −4.63 points in early 2026 | Agarwal, SSRN abstract [25] |

The NIFTY row is **low trust**: a single-author, non-peer-reviewed working paper, abstract only. No peer-reviewed figure for the NIFTY premium was found. The premium is an average with a fat left tail; all sources agree it is not earned steadily.

---

## 5. Intraday horizon (minutes to one session)

### 5a. Turning IV into an expected move for the rest of the day

$$ \text{one-standard-deviation move} = F\,\sigma\,\sqrt{\tau}, \qquad \text{expected absolute move} \approx 0.8\,F\,\sigma\,\sqrt{\tau} $$

$\tau$ is the time left in years **in the same clock $\sigma$ was solved with**. If the clock is "variance time" (5d), then for the rest of today

$$ \tau = \frac{1 - c(t)}{252} $$

where $c(t)$ is the usual share of a session's variance that has arrived by time $t$. For a same-day expiry the cleanest figure is the ATM straddle itself (3d): it is the implied absolute move to the close and needs no clock.

Bennett's rule of thumb: "Historical volatility roughly equal to 16 × percentage daily move" (p. 42) *(tool quote)* [12], that is $\sqrt{252} \approx 15.9$.

### 5b. Comparing it with what has happened so far today

- Realised variance so far: the sum of squared one-minute (or five-minute) log returns since the open, $RV_{0\to t} = \sum r_i^2$ (`research-estimators.md`, intraday sections).
- The implied budget for the whole session, taken at the open from the same-day option: $\sigma_{open}^2/252$ in the engine's clock.
- *Derived here.* A fair "pace" figure is

$$ \text{pace}(t) = \frac{RV_{0\to t}}{c(t)\cdot \sigma_{open}^2/252} $$

  Above 1, the day is moving more than was priced for this time of day. Dividing by $c(t)$ and not by the clock fraction is essential (5c).
- For the remaining part: implied variance still to come, from the current straddle, against the usual remaining share $1-c(t)$ of a normal day's variance.
- Also compare moves directly: realised $|F_t - F_{open}|$ against the straddle at the open.

### 5c. Variance time against clock time

**The U-shape.** Volatility is higher at the open and the close than at midday.

- Equities: Andersen and Bollerslev cite "the well-documented U-shape for equity market volatility; see e.g., Wood, McInish and Ord (1985) and Harris (1986)" *(text read; NBER working paper 5752)* [22]. Their 1997 *Journal of Empirical Finance* paper, which models the periodic component directly, could not be fetched: `UNVERIFIED AGAINST PRIMARY` [22].
- SPX options: "the volatility of the underlying is expected to be higher at the beginning and at the end of the trading day"; Bandi, Fusari and Renò therefore take their option cross-sections at 10:30 *(tool quote, section 5.2)* [16].
- NIFTY: Singh and Gangwar, NIFTY futures 2011 to August 2018, Table 1 *(text read)* [21]. Hourly-equivalent volatility (%): 9:15–10:00 0.3496; 10–11 0.2380; 11–12 0.2248; 12–13 0.2460; 13–14 0.2850; 14–15 0.3268; 15:00–15:30 0.2799. *Derived here* from that row (squaring and weighting by minutes):

| By this time | Share of session variance arrived | Share of clock elapsed |
| --- | --- | --- |
| 10:00 | 18.8% | 12% |
| 11:00 | 30.5% | 28% |
| 12:00 | 40.9% | 44% |
| 13:00 | 53.3% | 60% |
| 14:00 | 70.0% | 76% |
| 15:00 | 91.9% | 92% |

  The first 45 minutes carry about one and a half times their clock share; 14:00–15:00 carries 21.9% against 16%. The engine should measure its own profile from its own candles; this table is an older sample on the future, not the index.

- Consequence, from the simulation in `research-estimators.md` (Table 10): scaling the first hour's RV to a full day by the clock overstates by 58%.

**Overnight against in-session.**

- S&P 500: "about 29.4% of daily variance occurs during the hours the market is closed", rising from about 21% to nearly 40% over 1996 to mid-2017. `UNVERIFIED AGAINST PRIMARY`: this is the abstract of a Peking University seminar, "The Weekly Rhythm of Volatility", seen only as a search extract; the page returned 404 on a direct read [24].
- A warning on method: measured with the *cash* index's own open, the non-trading share is only 2.83% for the S&P 500 (ratio $r_o^2/(r_o^2+RV)$, 14-year sample) [23]. The cash index's first print is stale, built from stocks that have not yet traded, so the overnight move shows up in the first minutes of the session instead. Seen through a search extract of the manuscript: treat as `UNVERIFIED AGAINST PRIMARY`.
- A working paper using E-mini futures through the night reports overnight realised variance *larger* than intraday for 2003–2019 (Table 1 of [30], *text read*); its table units are ambiguous and it is not used here beyond showing that estimates vary widely with method.
- NIFTY: **no published split was found.** Measure it from the engine's own data. NSE's pre-open auction means the 9:15 index value does reflect the overnight move, unlike the US cash index.

**Events.** A scheduled event adds a known extra lump of variance on one day. Bennett backs the implied event move out of two expiries:

$$ \sigma_{Jump} = \sqrt{\sigma^2_{\text{Expiry after jump}}\,T - \sigma^2_{\text{Diffusive}}\,(T-1)} $$

`VERIFIED AGAINST PRIMARY` *(tool quote)*: Bennett p. 180, $T$ in trading days to the expiry after the event [12]. A trailing RV window with no event in it is not a fair opposite for an IV that spans one (and the reverse).

### 5d. The market maker's variance calendar

The idea: give every stretch of time a weight equal to the variance it usually carries, and measure time to expiry as the sum of the weights left.

$$ \tau_{var}(t,T) = \frac{\sum_{k \in (t,T]} \omega_k}{\sum_{k \in \text{one year}} \omega_k}, \qquad \sigma_{var}^2 = \frac{w(t,T)}{\tau_{var}(t,T)} $$

- $\omega_k$: a weight per intraday bucket (the U-shape profile), a weight for each night, a weight for each weekend, a multiplier for each event day, a reduced weight for holidays and half sessions.
- An IV quoted on this clock stays flat when nothing has changed. On any other clock it drifts mechanically.
- **Primary evidence that exchanges do this.** Cboe's one-day index: "The calculation of the VIX1D Index uses business years and business minutes – this is a different increment than the VIX Index, which uses calendar years and calendar minutes", over a "405-minute trading day", with the weight shifting through the day from the same-day to the next-day expiry *(read from Cboe's own article)* [19]. The official VIX1D methodology PDF refused the request, so the exact formula is `UNVERIFIED AGAINST PRIMARY`.
- **What a crude version costs.** Albers and Kestner find that VIX1D "consistently rise[s] during trading hours and … fall[s] overnight", a bias that "stems from the index's calculation methodology, particularly the use of business time and dynamic weighting of next-term options, which include overnight variance risk premiums" *(abstract only)* [20].
- **The engine has the same convention and will show the same bias.** *Derived here.* Let $V_s$ be a session's variance, $V_o$ a night's, and $w = V_o/(V_s+V_o)$. With time counted as sessions over 252 and nothing for the night:
  - a same-day option at the open covers one session and no night: its IV squared is $252\,V_s$;
  - an option with $n$ sessions and $n-1$ nights left has IV squared $252\left(V_s + \tfrac{n-1}{n}V_o\right)$.
  - With $w = 0.25$ and a truly flat market, the engine's IV reads 0.87 of the long-run level for a same-day option, 0.94 for two sessions, 0.97 for five. The same-day figure is lower by convention, not by information.
  - Across each night the next expiry's IV steps down (variance has gone, no time has passed) and it creeps up through the session.
- **Within the session.** *Derived here*, assuming the engine counts time evenly inside a session and using the NIFTY profile above: a same-day option whose total variance follows the usual profile shows a clock-time IV of 0.96 of its opening value at 10:00, 0.98 at 11:00, 1.03 at noon, 1.08 at 13:00, 1.12 at 14:00 and 1.01 at 15:00. A 12% swing in IV with no change in the market's view.
- Gatheral (*The Volatility Surface*) and Sinclair on variance time and event weights: books not reachable. `UNVERIFIED AGAINST PRIMARY`.

### 5e. What goes wrong when a short-dated IV is annualised by calendar time

*Derived here.* The option price fixes total variance. Dividing by a calendar-time $T$ that counts nights and weekends as fully as trading hours inflates the volatility of anything expiring soon.

| Option | Calendar time | Session time | Calendar-clock IV ÷ session-clock IV |
| --- | --- | --- | --- |
| SPX same-day, any time of day | hours left / 8,760 | (hours left / 6.5) / 252 | 2.31 |
| NSE same-day, any time of day | minutes left / 525,600 | (minutes left / 375) / 252 | 2.36 |
| SPX expiring tomorrow, seen at 10:00 | 30 h / 8,760 | (6/6.5 + 1) / 252 | 1.49 |
| 7 calendar days, 5 sessions | 7/365 | 5/252 | 1.02 |

- A same-day option worth "12%" on the session clock prints "28%" on the calendar clock. The term structure from same-day to weekly looks steeply inverted for no reason.
- The factor changes with the day of the week and jumps over weekends and holidays.
- Any RV set against it must be annualised the same way, which nobody does. This is the most common way a same-day IV-versus-RV chart lies.

### 5f. What the same-day-expiry research measures

- **Scale.** "Daily transaction volume in 0DTE SPX options is now over 43% of overall daily option volume"; sample 2 January 2014 to 11 May 2023 *(tool quote)* [16].
- **A same-day premium, defined.** Almeida, Freire and Hizmeri: $VRP_{t,T} = V^{Q}_{t,T} - RV_{t,T}$, where $V^Q$ is the model-free implied variance from the same-day options at time $t$ and $RV_{t,T}$ is the sum of one-minute squared log returns from $t$ to the close $T$ **on the previous day**; $t$ runs from 10:00 to 14:00 in half-hour steps, so horizons of 6 down to 2 hours (sections 2.6, 3.1, 3.5) *(tool quote)* [17]. This is comparison 1a moved inside the day: same time-of-day window, one day back. It removes the U-shape problem without a profile.
- **Size.** "The annualized 0DTE $VRP_{t,T}$ varies from 1.54% to 2.95%" across times of day; the upside part is 0.96% to 1.97%, the downside part 0.58% to 0.99%; SPXW, 6 January 2012 to 18 March 2025 (Table 1) *(tool quote; the annualising factor is not stated)* [17].
- **Can it be collected?** Vilkov: "A positive 0DTE variance risk premium exists, but at same-day horizons its economic magnitude is small and difficult to monetize after realistic frictions"; profit distributions are "dominated by tail risk rather than by stable mean carry"; sample September 2016 to 2 February 2026 *(abstract only; the paper's formulas were not reachable)* [18].

---

## 6. Forecasting RV as the fair comparison (short)

**HAR-RV (Corsi 2009).** Today's forecast is a weighted sum of yesterday's RV, the last week's average and the last month's average.

$$ RV^{(d)}_{t+1d} = c + \beta^{(d)}RV^{(d)}_t + \beta^{(w)}RV^{(w)}_t + \beta^{(m)}RV^{(m)}_t + \omega_{t+1d} $$

$$ RV^{(w)}_t = \tfrac15\left(RV^{(d)}_t + RV^{(d)}_{t-1d} + \dots + RV^{(d)}_{t-4d}\right), \qquad RV^{(m)}_t = \tfrac1{22}\left(RV^{(d)}_t + \dots + RV^{(d)}_{t-21d}\right) $$

`VERIFIED AGAINST PRIMARY` *(tool quote)*: Corsi, eq. (8) and the aggregate definitions before it [14]; restated as eq. (6) in Hansen and Lunde's survey *(text read)* [15]. Corsi presents it "for the realized volatility (i.e., the square-root transformation of the variance)"; analogous models exist for variance and log variance. Estimated by ordinary least squares with Newey-West errors. S&P 500 futures, January 1990 to July 2007: $c = 0.781$, $\beta^{(d)} = 0.372$, $\beta^{(w)} = 0.343$, $\beta^{(m)} = 0.224$ (Table 2) [14]. It needs 22 sessions of daily RV to produce one forecast and several hundred to estimate the weights.

**EWMA.** $\sigma_t^2 = \lambda\sigma_{t-1}^2 + (1-\lambda)r_t^2$. One parameter, no estimation; RiskMetrics uses $\lambda = 0.94$ for daily data. It reacts quickly but its forecast is flat for every horizon: it cannot say that a spike will fade. Formula and start-up needs are in `research-estimators.md`. `UNVERIFIED AGAINST PRIMARY` (RiskMetrics Technical Document, 1996, not fetched).

**GARCH(1,1).** $\sigma_{t+1}^2 = \omega + \alpha r_t^2 + \beta\sigma_t^2$. It adds a long-run level $V_L = \omega/(1-\alpha-\beta)$ that forecasts return to: $E_t[\sigma^2_{t+k}] = V_L + (\alpha+\beta)^{k-1}(\sigma^2_{t+1}-V_L)$. The average of that path over the option's life is the figure to set against IV. It needs years of daily returns to estimate. `UNVERIFIED AGAINST PRIMARY` (Bollerslev 1986 not fetched; standard textbook form).

**Is a simple forecast worth showing?** Not in a first version.

- Trailing RV is already most of the story: correlation 0.85 between the forecast-based and the trailing premium [2].
- The engine keeps 30 sessions. That is enough to *run* a HAR forecast but not to *estimate* one, and Corsi's published weights are for another market and another unit.
- A forecast adds a model the reader must trust. Show trailing RV at two or three windows first; they bracket what a HAR forecast would say.

---

## 7. Each market's quirks

**NSE index options (NIFTY; SENSEX on BSE).**

- Session 9:15 to 15:30, 375 minutes (the hour bands of [21] confirm it); a pre-open auction before 9:15.
- Weekly expiry: NIFTY on Tuesday for contracts expiring on or after 1 September 2025; SENSEX on Thursday; BANKNIFTY weekly options discontinued in November 2024. News reports of exchange circulars; the circulars themselves were not read [28]. Confirm against the engine's instrument master.
- So within 0 to 7 days there is normally one weekly expiry per index: no bracketing pair for a constant maturity.
- Expiry day: the front option's ATM IV is unstable in the last hour and the series then rolls, so the IV line jumps to the next expiry's level and horizon. Show days to expiry beside the IV.
- India VIX is 30 calendar days from monthly expiries (3c). It is a different horizon and a different kind of figure from a weekly ATM IV. The engine has no India VIX feed.

**SPX same-day expiries (SPXW).**

- PM-settled: "'weekly' SPX options are deemed to expire at the close of trading (i.e., 4:00 p.m. ET)" *(text read)* [9].
- The engine has no spot feed; the level is the front expiry's implied forward. *Derived here:* RV from that series contains quote noise from the options used to build it. One-minute sampling will read high; five-minute sampling is safer (`research-estimators.md`, noise table). At the open the forward can be unreliable until option quotes settle.
- With only 0-to-1-day expiries, the IV is always a same-day or next-day figure. Opposite it belongs session RV, not a 20-day or 30-day window.
- The US cash index's stale open (5c) does not affect a forward built from options, which is an advantage.

**Crypto.**

- Trades all hours: no overnight gap, no session. Annualise with 365 days: Volmex's realised indices use "A = 365/n … assuming 365 calendar days per year" *(text read)* [26].
- Deribit's DVOL is a 30-day, model-free figure (outline in `research-dashboards.md` section 5.8). Opposite it belongs 30-day RV on a 365-day year.
- Calendar time and variance time are close but not equal: weekends and time of day still differ. Not quantified here. `UNVERIFIED`.

**Commodity options on futures.**

- The underlying is one specific futures contract, so Black-76 on the future is exact in form.
- RV must be computed on that same contract. A continuous rolled series has a false return on each roll day.
- Volatility of a future tends to rise as it nears delivery (the Samuelson effect), so trailing RV understates what the option faces late in the contract's life. `UNVERIFIED AGAINST PRIMARY` (Samuelson 1965 and Black 1976 not fetched).
- Sessions are long and the option often expires before its future. Both need the instrument master.

---

## 8. Synthesis

### 8a. Who needs which pairing

| Trader | IV figure | RV figure (estimator, bar, window) | How the two are aligned | The one number |
| --- | --- | --- | --- | --- |
| **Intraday scalper or gamma trader** (holds minutes to hours, delta hedged) | ATM IV of the expiry actually held, turned into implied variance for the stretch held | Sum of squared log returns at the hedge interval: one-minute bars for NIFTY and SENSEX, five-minute for the SPX forward. Windows: since entry, since the open, and a rolling one-session window | Same clock (sessions over 252). Session only on both sides: no overnight. Part-day figures scaled by the time-of-day profile, never by the clock | **Pace**: realised variance since the open ÷ implied variance budgeted for that part of the day (5b). Above 1 favours long gamma |
| **Same-day expiry seller** | ATM straddle price at entry, in index points: the implied absolute move to the close. Also its implied variance | Realised absolute move from entry to the close, and realised variance (one-minute or five-minute) from entry to the close | Same start time, same end (expiry). No annualising at all. History kept per entry time of day | **Realised move ÷ straddle** for today, and its record over past expiries for the same entry time |
| **Weekly positional** (1 to 7 sessions) | ATM IV of the held expiry, with its sessions to expiry $n$ shown | Intraday realised variance summed over the last $n$ sessions **plus the squared overnight gaps**, annualised by $252/n$. Not five daily closes | Window length equals sessions to expiry. Overnight on both sides. Same 252 clock. For the earned premium, RV runs *forward* from the entry date | **IV − RV** in volatility points for the matched window, with the variance ratio $RV^2/IV^2$ beside it |
| **Monthly positional** | 30-day constant-maturity IV by total-variance interpolation, or a VIX-style figure | 21- or 22-session Yang-Zhang or close-to-close RV (`research-estimators.md`) | Fixed 30-calendar-day horizon on both sides; one clock; ex-post RV shifted back 21 sessions to sit under the IV it answers | **Variance risk premium** $IV^2 - RV^2$, with its percentile over a year. Not buildable today |

### 8b. Mistakes that make an IV-versus-RV chart lie

1. **Windows that do not match.** A 30-day RV under a 3-day option. *Avoid:* RV window equals sessions to expiry; print both.
2. **Two clocks.** Calendar-time IV against 252-day RV. Inside a week the error reaches 30% and changes with the weekday (4b). *Avoid:* one clock on both sides, or compare total variance or points.
3. **Calendar-annualising a same-day option.** Inflates IV about 2.3 times (5e). *Avoid:* session clock, or show the straddle in points.
4. **Overnight on one side only.** Session-only RV against an IV that prices the nights reads RV low by the overnight share. In the engine's clock the reverse also bites: a same-day IV has no night in it and reads lower than a weekly IV by convention (5d). *Avoid:* same-day IV with session RV; multi-day IV with RV that includes the gaps; never one line across the two.
5. **Scaling a part day by the clock.** After the first hour it overstates by about 58%. *Avoid:* the time-of-day profile, or a trailing window exactly one session long.
6. **Reading clock-time IV drift as news.** A same-day IV on an even clock moves about ±10% through a normal day (5d). *Avoid:* show implied variance remaining or the straddle, or use variance time.
7. **The sawtooth.** One expiry's IV changes horizon daily and jumps at the roll. *Avoid:* show days to expiry; do not compute rank or percentile on it.
8. **The ex-post premium drawn on the wrong date.** RV for the life of an option belongs under the day the IV was quoted. Drawn at the end date it looks like IV lags. *Avoid:* shift it, and leave the last $n$ days blank.
9. **Trailing RV mistaken for what was earned.** The position earns forward RV at the hedge frequency, weighted by dollar gamma (section 2). *Avoid:* label trailing RV as context; show realised-since-entry separately.
10. **Volatility against variance.** A VIX-style figure against ATM-style RV, or averaging volatilities. The VIX-style figure is higher through the skew alone (24.41 against 21.28 in [1]). *Avoid:* pair like with like; average variances.
11. **The straddle read as one standard deviation.** It is the mean absolute move, 0.8 of it. *Avoid:* label the band; the engine's IV-over-root-252 band is one standard deviation.
12. **Too few points.** Five daily returns give a volatility with a 32% standard error. *Avoid:* intraday RV for short windows.
13. **Noise read as volatility.** One-minute RV on a synthetic forward (SPX) or a thin future reads high. *Avoid:* five-minute sampling or a noise-robust estimator (`research-estimators.md`).
14. **Overlap read as evidence.** A daily series of a 21-day premium is one observation per month, not per day. *Avoid:* statistics on non-overlapping windows, one per expiry.
15. **Events on one side.** IV spans a scheduled event; the trailing window does not (or the reverse). *Avoid:* mark event days; later, event weights.
16. **Stale opens and odd sessions.** The US cash index's first print; a forward built from unsettled option quotes; Muhurat or half sessions counted as full days. *Avoid:* start the day's RV after quotes settle and say so; flag special sessions.
17. **A different underlying.** IV on a forward or a future, RV on spot or on a rolled series. *Avoid:* RV on the same series the IV is solved against.
18. **A sign left unstated.** Implied minus realised or the reverse. *Avoid:* say it in the axis label.

### 8c. Recommendation for a first version

**Build now** (everything here uses data the engine already has):

1. **IV side.** For NIFTY, SENSEX and SPXW, the ATM IV of each subscribed expiry, as already computed (Black-76, sessions over 252), shown with its sessions to expiry. Beside it the ATM straddle in points as the implied move to expiry.
2. **RV side, from the stored one-minute candles.**
   - Today so far: sum of squared returns since the open (one-minute for India, five-minute for the SPX forward).
   - A rolling window exactly one session long.
   - For each $n$ from 1 to 7: realised variance over the last $n$ sessions including the squared overnight gaps, annualised by $252/n$. Thirty stored sessions are enough.
3. **Alignment rules, fixed in code.** One clock (252 sessions). Same-day IV against session-only RV. Multi-day IV against RV with gaps. Window equals sessions to expiry.
4. **Three summary numbers.**
   - Live, intraday: the **pace** figure of 5b, using a time-of-day profile measured from the stored sessions (median across days; thirty sessions is thin, so smooth it into buckets of 15 to 30 minutes).
   - Positional: **IV − RV** in volatility points for the matched window.
   - Same-day: **realised move ÷ straddle** at fixed entry times, logged per expiry day.
5. **Start recording history now.** At fixed times each session store: ATM IV and straddle per expiry, the day's session RV, the overnight gap, and the time-of-day profile. Rank, percentile, cone and the ex-post premium all need history, and there is no back-fill. Every week not recorded is a week missing from them.
6. **Label the existing band.** The delta-hedged straddle's "IV divided by root 252" band is a one-standard-deviation move for a full session on the engine's clock. Say so, and show the straddle (0.8 of it) as the break-even.

**Leave for later, and why.**

| Item | Why not now |
| --- | --- |
| 30-day constant-maturity IV, VIX-style figure, variance risk premium in the textbook sense | Needs expiries beyond 7 days (India) and 1 day (SPXW) to be subscribed |
| IV rank, IV percentile | Need about a year of stored IV on a constant maturity |
| Volatility cone | Needs long RV history; 30 sessions give about 6 independent weekly windows |
| India VIX and VIX overlays | No feed; and they are the wrong horizon for weekly and same-day options |
| Variance-time clock with night, weekend and event weights | The right fix for 5d and 5e, but a change to how IV itself is computed; needs its own design and measured overnight shares |
| HAR, EWMA or GARCH forecast | Cannot be estimated on 30 sessions; adds little over trailing RV at first |
| Gamma-weighted realised variance per position | Belongs with position reporting, not a market chart |
| Crypto and commodities | No live chains yet; each needs its own clock and underlying rules (section 7) |

---

## 9. What could not be confirmed

- **Brenner and Subrahmanyam (1988)**: article not read. The 0.4 and 0.8 factors are derived and numerically checked here and confirmed by Bennett.
- **Ahmad and Wilmott (2005)**: the journal article is behind a login. Formulas read in Wilmott's lecture slides of the same title.
- **Burghardt and Lane (1990)**: not read; the cone is described through the Montréal Exchange paper.
- **Andersen and Bollerslev (1997), *Journal of Empirical Finance***: not read; the U-shape statement is from their NBER paper 5752.
- **Sinclair, Natenberg, Gatheral**: books not reachable. Nothing rests on them. The variance-calendar section rests on Cboe's VIX1D article, Bennett's event formula and reasoning.
- **Cboe VIX1D methodology PDF**: refused; only Cboe's article and one paper's abstract were read. The exact weighting formula is unconfirmed.
- **Overnight share of variance.** S&P 500: 29.4% from a seminar abstract seen as a search extract; 2.83% by a cash-open method from a search extract. NIFTY and SENSEX: nothing found. Measure in-house.
- **NIFTY premium size**: one low-trust working paper abstract.
- **Vilkov, "0DTE Trading Rules"**: abstract only. **Albers and Kestner**: abstract only.
- **Carr and Wu**: the 2004 working-paper draft was read, not the 2009 journal text; equation numbers and sample statistics may differ.
- **Page numbers** for Bossu et al., Bennett and Almeida et al. came through an extraction tool; equation numbers and quotes are reliable, pages approximate.
- **NSE and BSE expiry-day rules**: from news reports, not the circulars.
- **GARCH, EWMA, Samuelson effect, Black-76**: textbook forms, primaries not fetched.
- **The engine's clock inside a session** was assumed to run evenly. The size of the within-day drift in 5d depends on that.
- **Almeida et al.'s annualising factor** for the same-day premium is not stated in what was read.

---

## Sources

1. P. Carr and L. Wu, "Variance Risk Premia", working-paper draft dated 27 May 2004 (`src/carrwu_b.pdf`); published as "Variance Risk Premiums", *Review of Financial Studies* 22(3), 2009, 1311–1341. https://ideas.repec.org/a/oup/rfinst/v22y2009i3p1311-1341..html
2. T. Bollerslev, G. Tauchen and H. Zhou, "Expected Stock Returns and Variance Risk Premia", CREATES Research Paper 2008-48 (`src/btz.pdf`); published in *Review of Financial Studies* 22(11), 2009.
3. G. Bakshi and N. Kapadia, "Delta-Hedged Gains and the Negative Market Volatility Risk Premium", *Review of Financial Studies* 16(2), 2003, 527–566. Author's copy: https://people.umass.edu/nkapadia/Research/rfsfinw.pdf
4. P. Carr and D. Madan, "Towards a Theory of Volatility Trading", version of 16 December 1997 (`src/carrmadan.pdf`); published in R. Jarrow (ed.), *Volatility*, Risk Books, 1998.
5. S. Bossu, E. Strasser and R. Guichard, "Just What You Need to Know About Variance Swaps", JPMorgan Equity Derivatives, May 2005. http://docs.sbossu.com/bossu-strasser-guichard-varswap.pdf
6. P. Wilmott, lecture slides "Which Free Lunch Would You Like Today, Sir? Delta hedging, volatility arbitrage and optimal portfolios" (2005): http://cfile23.uf.tistory.com/attach/116600154C6A63BE55B403 . The article (R. Ahmad and P. Wilmott, *Wilmott* magazine, 2005) is listed at https://www.wilmott.com/which-free-lunch-would-you-like-today-sir-delta-hedging-volatility-arbitrage-and-optimal-portfolios-riaz-ahmad-and-paul-wilmott/ (login required).
7. K. Demeterfi, E. Derman, M. Kamal and J. Zou, "More Than You Ever Wanted to Know About Volatility Swaps", Goldman Sachs Quantitative Strategies Research Notes, March 1999 (`src/ddkz.pdf`).
8. Cboe, "Cboe Volatility Index Mathematics Methodology" (`src/cboevix.txt`). https://cdn.cboe.com/resources/indices/Cboe_Volatility_Index_Mathematics_Methodology.pdf
9. Cboe, "Cboe Volatility Index" white paper, 2019 (`src/asx_vixwp.pdf`).
10. NSE, "India VIX" white paper (`src/indiavix.txt`). https://archives.nseindia.com/content/indices/white_paper_IndiaVIX.pdf
11. M. Brenner and M. Subrahmanyam, "A Simple Formula to Compute the Implied Standard Deviation", *Financial Analysts Journal* 44(5), 1988, 80–83. https://www.tandfonline.com/doi/abs/10.2469/faj.v44.n5.80 (not reachable)
12. C. Bennett, *Trading Volatility: Trading Volatility, Correlation, Term Structure and Skew*, 2014. https://www.trading-volatility.com/Trading-Volatility.pdf
13. Montréal Exchange, "Trading Volatility Using Historical Volatility Cones" (`src/mx_cone.pdf`). https://www.m-x.ca/f_publications_en/cone_vol_en.pdf . Describes G. Burghardt and M. Lane, "How to Tell if Options Are Cheap", *Journal of Portfolio Management*, Winter 1990 (not reached).
14. F. Corsi, "A Simple Approximate Long-Memory Model of Realized Volatility", *Journal of Financial Econometrics* 7(2), 2009, 174–196. https://statmath.wu.ac.at/~hauser/LVs/FinEtricsQF/References/Corsi2009JFinEtrics_LMmodelRealizedVola.pdf
15. P. R. Hansen and A. Lunde, "Forecasting Volatility using High Frequency Data" (`src/hl11.pdf`), section 5.3.
16. F. Bandi, N. Fusari and R. Renò, "0DTE Option Pricing", draft of 15 March 2024. https://portal.northernfinanceassociation.org/viewp.php?n=2240145012
17. C. Almeida, G. Freire and R. Hizmeri, "0DTE Asset Pricing", working paper. https://www.fma.org/assets/docs/Derivatives2025/Almeida.pdf
18. G. Vilkov, "0DTE Trading Rules", SSRN 4641356 (abstract). https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4641356
19. S. Doar, "What the VIX and VIX1D Indices Attempt to Measure and How They Differ", Cboe Insights, 24 April 2023. https://www.cboe.com/insights/posts/what-the-vix-and-vix-1-d-indices-attempt-to-measure-and-how-they-differ
20. S. Albers and L. Kestner, "The daily rise and fall of the VIX1D: causes and solutions of its overnight bias", *Finance Research Letters*, 2024 (abstract). https://doi.org/10.1016/j.frl.2024.105186
21. R. Singh and R. Gangwar, "A Temporal Analysis of Intraday Volatility of Nifty Futures on the National Stock Exchange", MPRA Paper 89689, 2018 (`src/mpra89689.pdf`). https://mpra.ub.uni-muenchen.de/89689/1/MPRA_paper_89689.pdf
22. T. Andersen and T. Bollerslev, "Heterogeneous Information Arrivals and Return Volatility Dynamics", NBER Working Paper 5752 (`src/ab97.pdf`). Their "Intraday periodicity and volatility persistence in financial markets", *Journal of Empirical Finance* 4, 1997, 115–158, https://www.sciencedirect.com/science/article/pii/S0927539897000042 , was not reached.
23. Manuscript JFEC-2013-084, "On Setting Day-Ahead Equity Trading Risk Limits: VaR Prediction at Market Close or Open?", City Research Online (search extract only; authors not confirmed here). https://openaccess.city.ac.uk/id/eprint/12655/1/Manuscript_JFEC-2013-084.pdf
24. Peking University seminar notice, "The Weekly Rhythm of Volatility" (search extract only; direct read returned 404). https://econ.pku.edu.cn/ltjz/335073.htm
25. Y. Agarwal, "The Variance Risk Premium in Nifty 50: A Structural Anatomy Across Nine Empirical Filters", SSRN 6530119, April 2026 (abstract). https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6530119
26. K. G. Babaoglu, "Volmex Realized Volatility Indices", Volmex Labs, 30 June 2025 (`src/volmex_rv.txt`). https://volmex.finance/papers/Volmex-Realized-Volatility-Indices.pdf
27. Cboe, "Cboe Realized Volatility Index Series Methodology" (`src/rvol.txt`). https://cdn.cboe.com/resources/indices/documents/RVOL_Methodology.pdf
28. News reports of expiry-day changes: Business Standard, "Bye, Thursday Nifty expiry! New NSE derivatives expiry start next Tuesday", August 2025, https://www.business-standard.com/amp/markets/news/nse-bids-adieu-to-thursday-expiry-as-dates-swap-come-into-effect-explained-125082800635_1.html ; News On AIR, "NSE to discontinue weekly index derivatives for Bank Nifty, Nifty Midcap Select, Nifty Financial Services", https://newsonair.gov.in/nse-to-discontinue-weekly-index-derivatives-for-bank-nifty-nifty-midcap-select-nifty-financial-services
29. Sibling notes in this folder: `research-estimators.md` (RV formulas and the simulation) and `research-dashboards.md` (product survey and definitions).
30. F. Liang, L. Du and Z. Huang, "Option Pricing with Overnight and Intraday Volatility", Peking University working paper E2022025, December 2022 (`src/pku.pdf`).

---

DONE
Summary line 1: A fair IV-versus-RV comparison needs the same horizon, the same clock and the same treatment of the overnight gap on both sides; the delta-hedged profit is half dollar gamma times realised minus implied variance at the hedge frequency over the position's life (Carr and Madan eq. 9; Bossu et al. Eq. 5).
Summary line 2: Intraday and same-day traders should compare the straddle or implied session variance with realised variance and move since the open, scaled by a time-of-day profile; weekly traders the held expiry's ATM IV with intraday-built RV over the same number of sessions including gaps; a 30-day constant-maturity or VIX-style figure cannot be built from the engine's feeds today.
Summary line 3: First version: nearest-expiry ATM IV and straddle against one-minute-candle RV on the engine's 252-session clock, three summary numbers (pace, IV minus RV, realised move over straddle), and start recording history now; rank, percentile, cone, forecasts and a variance-time clock come later.
Left unverified: Brenner-Subrahmanyam 1988 (derived and checked numerically instead); Ahmad-Wilmott article (lecture slides read); Burghardt-Lane 1990; Andersen-Bollerslev 1997 JEF; Sinclair, Natenberg, Gatheral; Cboe VIX1D methodology formula; overnight variance share for S&P 500 (search extracts only) and for NIFTY (none found); NIFTY premium size (one low-trust abstract); Vilkov and Albers-Kestner (abstracts only); Carr-Wu journal text (2004 draft read); NSE/BSE expiry rules (news only); GARCH, EWMA, Samuelson, Black-76 primaries; the engine's within-session clock assumption.
