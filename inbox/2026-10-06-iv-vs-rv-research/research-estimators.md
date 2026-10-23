# Realised volatility estimators: formulas, sources and a numerical check

Research note for the implied-versus-realised volatility feature. Written 2026-10-06.

**What this note is.** A list of every credible way to calculate realised volatility (how much a price actually moved), each with its exact formula, what it needs, where it goes wrong, and where the formula was first published. Each formula was checked two ways: against the paper that introduced it, and by a simulation with a known answer (`verify_estimators.py`, in this folder).

**How to read the verification labels.**

- `VERIFIED AGAINST PRIMARY` means the equation was read in the paper itself (or the authors' own copy of it) and the equation or page number is given.
- `UNVERIFIED AGAINST PRIMARY` means the paper could not be reached; what was checked instead is stated.
- "Simulation" refers to the tables in section 14.

## 0. Words and symbols used throughout

- **Volatility** ($\sigma$): the standard deviation of the log return of a price over a stated period. **Variance** ($\sigma^2$) is its square. Every estimator below estimates variance first; volatility is the square root taken at the end.
- **Log return**: $\ln(P_{\text{end}}/P_{\text{start}})$.
- **Drift** ($\mu$): the average log return per period. A steadily trending market has a large drift.
- **Overnight gap** (also "opening jump"): the move from one day's close to the next day's open, when the market is shut.
- **Efficiency**: the variance of the plain close-to-close estimate divided by the variance of the estimator in question, for the same number of days. An efficiency of 5 means the estimator is as accurate with 4 days as close-to-close is with 20.
- **Bias**: the estimator's long-run average minus the true value. An unbiased estimator is right on average.

For day $i$ of a window of $n$ days, with open $O_i$, high $H_i$, low $L_i$, close $C_i$:

$$ o_i = \ln\frac{O_i}{C_{i-1}} \quad\text{(overnight)},\qquad u_i = \ln\frac{H_i}{O_i},\qquad d_i = \ln\frac{L_i}{O_i},\qquad c_i = \ln\frac{C_i}{O_i},\qquad r_i = o_i + c_i = \ln\frac{C_i}{C_{i-1}} $$

So $u_i \ge 0$, $d_i \le 0$, and $u_i - d_i = \ln(H_i/L_i)$ is the day's range. This is the notation of Garman and Klass (1980) and Yang and Zhang (2000).

**Annualising**, for every estimator: multiply the per-period *variance* by the number of periods in a year $A$ (252 for daily bars on a 252-day year), then take the square root: $\sigma_{\text{annual}} = \sqrt{A \cdot \hat\sigma^2_{\text{period}}}$. Section 15 gives the exact factors.

---

## 1. Close-to-close standard deviation

**Formula, mean removed (the textbook sample variance).** Needs $n+1$ closes to give $n$ returns.

$$ \hat\sigma^2_{CC} = \frac{1}{n-1}\sum_{i=1}^{n}\left(r_i - \bar r\right)^2,\qquad \bar r = \frac{1}{n}\sum_{i=1}^{n} r_i $$

**Formula, zero mean.**

$$ \hat\sigma^2_{CC,0} = \frac{1}{n}\sum_{i=1}^{n} r_i^2 $$

- **Data needed:** closes only.
- **Assumptions:** returns are independent with a constant variance over the window. Nothing about gaps or trading hours: the close-to-close return already contains the overnight move.
- **Mean removed or not.**
  - With the mean removed and divisor $n-1$ the variance estimate is unbiased whatever the drift. The price is one lost observation: its variance is $2\sigma^4/(n-1)$.
  - With the mean removed and divisor $n$ (the maximum-likelihood form) the estimate is biased low by the factor $(n-1)/n$: 5% low at $n=20$.
  - With zero mean and divisor $n$ the estimate is unbiased only when the drift is zero. Otherwise it is too high by $\mu^2/\sigma^2$ (drift and volatility both per day). For an index drifting 12% a year at 16% volatility that is about 0.2% of variance, which is nothing. In a short violent trend it is large: simulation Table 4 shows +28% of variance when the drift is half a daily standard deviation per day. Its variance is $2\sigma^4/n$, slightly better than the mean-removed form.
  - Zero mean with divisor $n-1$ (seen in some libraries) is simply biased high by $n/(n-1)$.
- **Small-sample bias of the standard deviation.** The variance estimate is unbiased but its square root is not, because the square root is a concave function. For normal returns

$$ \mathbb{E}[s] = c_4(n)\,\sigma,\qquad c_4(n) = \sqrt{\frac{2}{n-1}}\;\frac{\Gamma\!\left(\frac{n}{2}\right)}{\Gamma\!\left(\frac{n-1}{2}\right)} \approx 1 - \frac{1}{4n} $$

  where $s=\sqrt{\hat\sigma^2_{CC}}$ and $\Gamma$ is the gamma function. $c_4$ is 0.940 for $n=5$, 0.973 for $n=10$, 0.987 for $n=20$, 0.996 for $n=60$. A 20-day volatility therefore reads 1.3% low on average (19.74 when the truth is 20). Dividing $s$ by $c_4(n)$ removes it for normal returns. Simulation Table 5 reproduces these numbers. The same effect applies to the square root of every estimator below, in proportion to how noisy it is.
- **How noisy it is.** The standard error of the volatility is about $\sigma/\sqrt{2n}$: 16% of the value at $n=20$ (20% plus or minus 3.2 points), 9% at $n=60$.
- **Efficiency:** 1 by definition.
- **Source.** Classical statistics. The papers below all print it as their benchmark: Parkinson (1980) section II with $n-1$ and the mean removed, and section V with zero mean; Garman and Klass (1980) as $\hat\sigma_0^2=(C_1-C_0)^2$; Yang and Zhang (2000) eq. (1) with the mean removed and $n-1$. The $c_4$ constant is the standard quality-control constant (source 32). `VERIFIED AGAINST PRIMARY` for the estimator as printed in those three papers; the $c_4$ formula is a textbook result checked by simulation only.
- **Library check.** R's TTR `volatility(calc="close")` computes `sqrt(N) * runSD(r, n-1)`: its `n` counts prices, so it uses $n-1$ returns with divisor $n-2$, which is the formula above with a different meaning of $n$. Its `mean0=TRUE` branch computes `runSum(r^2, n-1) / (n-2)`: $n-1$ squared returns divided by $n-2$, which is biased high by $(n-1)/(n-2)$ (12.5% of variance at its default $n=10$). TTR also defaults to $N=260$ periods a year, not 252.

## 2. Parkinson (1980): the high-low range

$$ \hat\sigma^2_{P} = \frac{1}{4\ln 2}\cdot\frac{1}{n}\sum_{i=1}^{n}\left(\ln\frac{H_i}{L_i}\right)^2 = \frac{1}{4\ln 2}\cdot\frac{1}{n}\sum_{i=1}^{n}(u_i-d_i)^2,\qquad \frac{1}{4\ln 2}=0.3607 $$

- **Data needed:** daily high and low.
- **Assumptions:** the log price is a continuous random walk with **no drift**; it is watched **continuously** (the true high and low are seen); the whole period is traded (**no overnight gap**).
- **Why 4 ln 2.** For a driftless random walk the expected squared range over a period is $4\ln 2$ times the variance.
- **Bias.**
  - Too **high** under drift: a trend widens the range. Simulation Table 4: +3% of variance at a drift of 0.25 daily standard deviations a day, +10% at 0.5, +37% at 1.0.
  - Too **low** when there is an overnight gap: it sees only the session. With a quarter of the variance overnight it returns 75% (Table 1).
  - Too **low** when the high and low come from prices sampled at intervals rather than continuously, because the true extremes fall between samples. Table 3: 7% low with 375 prices a day, 14% low with 75.
- **Efficiency:** Parkinson gives the variance of his estimate as $0.41\,D^2/N$ against $2D^2/N$ for close-to-close, and concludes "$N_x = 5N_l$", that is about 5. The exact figure from his own moment formula is $2/0.4073 = 4.91$. Garman and Klass quote 5.2 for the same estimator, and that 5.2 is what most secondary sources repeat. Simulation: 4.85.
- **Source.** Parkinson, M. (1980), "The Extreme Value Method for Estimating the Variance of the Rate of Return", *Journal of Business* 53(1), 61-65. The equations are not numbered. Section III, p. 62-63: $E[l^2] = (4\ln 2)\,Dt$ and "$D = .393\,(E[l])^2 = .361\,E[l^2]$", then the estimator $D_l = \frac{.361}{n}\sum l_i^2$ (p. 63), with $l=\ln(H/L)$ for a stock (section V, p. 64). `VERIFIED AGAINST PRIMARY` (JSTOR scan hosted at mmquant.net). Garman and Klass eq. (5) prints the same estimator as $(u-d)^2/(4\ln 2)$.
- **Note.** Parkinson also gives a second estimator, $0.393\,(\text{mean range})^2$, which Garman and Klass (footnote 8) set aside as biased. Nobody uses it.
- **Library check.** TTR `calc="parkinson"`: `sqrt(N/(4*n*log(2)) * runSum(log(Hi/Lo)^2, n))`. Matches.

## 3. Garman and Klass (1980)

**The practical form** (their eq. 19a, which the paper recommends as the more practical one):

$$ \hat\sigma^2_{GK} = \frac{1}{n}\sum_{i=1}^{n}\left[\tfrac12\,(u_i-d_i)^2 - (2\ln 2 - 1)\,c_i^2\right],\qquad 2\ln 2-1 = 0.3863 $$

that is, half the squared high-low range minus 0.386 times the squared open-to-close return.

**The exact minimum-variance form** (their eq. 19):

$$ \hat\sigma^2_{4} = 0.511\,(u-d)^2 - 0.019\,\{c\,(u+d) - 2ud\} - 0.383\,c^2 $$

- **Data needed:** daily open, high, low, close.
- **Assumptions:** **zero drift**; continuous monitoring; for eq. (19) and (19a) **no overnight gap** ($f=0$, see below). The paper says in so many words that non-zero drift is ruled out by its model.
- **Other forms in the paper.** The paper numbers its estimators $\hat\sigma_0$ to $\hat\sigma_6$. $f$ is the fraction of the day the market is shut, in variance terms.

| Paper's name | Formula | Efficiency stated |
| --- | --- | --- |
| $\hat\sigma_0^2$ | $(C_1-C_0)^2$, close to close | 1 |
| $\hat\sigma_1^2$, eq. (3) | $\dfrac{(O_1-C_0)^2}{2f}+\dfrac{(C_1-O_1)^2}{2(1-f)}$ | 2 |
| $\hat\sigma_2^2$, eq. (5) | $\dfrac{(u-d)^2}{4\ln 2}$, Parkinson | 5.2 |
| $\hat\sigma_3^2$, eq. (6) | $a\dfrac{(O_1-C_0)^2}{f}+(1-a)\dfrac{(u-d)^2}{(1-f)\,4\ln 2}$, best at $a=0.17$ | 6.2 |
| $\hat\sigma_4^2$, eq. (19) | exact form above | 7.4 |
| $\hat\sigma_5^2$, eq. (19a) | practical form above | about the same |
| $\hat\sigma_6^2$, eq. (20) | $a\dfrac{(O_1-C_0)^2}{f}+(1-a)\dfrac{\hat\sigma_4^2}{1-f}$, best at $a=0.12$ | 8.4 |

  In the paper the prices are already logs, so $(O_1-C_0)$ is $o$ in this note's notation.
- **Bias.** Too high under drift, though less than Parkinson (Table 4: +1.5% at 0.25, +3.6% at 0.5, +13% at 1.0). Too low with an overnight gap (Table 1: 75%). Too low under discrete sampling, and by more than Parkinson (Table 3: 9% low at 375 prices a day, 20% low at 75). The paper's own Table 1 shows the same thing and advises dividing by its tabulated factors.
- **Efficiency:** 7.4 (paper); simulation 7.25 for both forms.
- **It cannot go negative.** Because $|c|\le u-d$, each day's term is at least $(0.5-0.386)(u-d)^2$.
- **Source.** Garman, M. B. and Klass, M. J. (1980), "On the Estimation of Security Price Volatilities from Historical Data", *Journal of Business* 53(1), 67-78, eq. (3), (5), (6), (19), (19a), (20) and Table 1. `VERIFIED AGAINST PRIMARY`, read in the authors' own re-typeset copy hosted by CME Group, which describes itself as an updated version of the journal article. The equation numbers agree with how Yang and Zhang (2000) cite it (they refer to its formula 20). One slip in that copy: after eq. (19) it writes Eff$(\hat\sigma_3^2)\approx 7.4$ where it means $\hat\sigma_4^2$.
- **Library check.** TTR `calc="garman.klass"`: `sqrt(N/n * runSum(.5*log(Hi/Lo)^2 - (2*log(2)-1)*log(Cl/Op)^2, n))`. Matches eq. (19a). Python `volatility-trading` `GarmanKlass.py`: same. Both use the practical form; neither offers eq. (19).

## 4. Rogers and Satchell (1991); Rogers, Satchell and Yoon (1994)

$$ \hat\sigma^2_{RS} = \frac{1}{n}\sum_{i=1}^{n}\left[u_i\,(u_i-c_i) + d_i\,(d_i-c_i)\right] = \frac{1}{n}\sum_{i=1}^{n}\left[\ln\frac{H_i}{O_i}\ln\frac{H_i}{C_i} + \ln\frac{L_i}{O_i}\ln\frac{L_i}{C_i}\right] $$

The two ways of writing it are the same thing, since $u-c=\ln(H/C)$ and $d-c=\ln(L/C)$.

- **Data needed:** daily open, high, low, close.
- **Assumptions:** continuous monitoring and **no overnight gap**. **Drift is allowed**: this is the point of the estimator.
- **Bias.** None under any constant drift (Table 4: within 0.7% at every drift tried). Too low with an overnight gap (Table 1: 75%). Too low under discrete sampling, about as much as Garman-Klass (Table 3).
- **A useful property.** A day that moves in one direction only (open at the low, close at the high) scores zero: the whole move is read as drift.
- **Efficiency.** The paper gives the variance of the one-day estimate as $0.331\,\sigma^4$ at zero drift, against $0.27\,\sigma^4$ for Garman-Klass and $2\sigma^4$ for close-to-close. That is an efficiency of $2/0.331 = 6.0$. Simulation: 5.9.
- **Correction for discrete sampling.** Section 3 of the 1991 paper: if the high and low are the extremes of $N$ equally spaced prices, with $h=1/N$, use the positive root $\hat\sigma_h$ of

$$ \hat\sigma_h^2 = 2b\,\hat\sigma_h^2\,h + 2\,(u-d)\,a\,\hat\sigma_h\sqrt h + u(u-c) + d(d-c),\qquad a=\sqrt{2\pi}\left[\tfrac14-\tfrac{\sqrt2-1}{6}\right]=0.4536,\quad b=\frac{1+\frac{3\pi}{4}}{12}=0.2797 $$

  In simulation (Table 3) this removes most of the shortfall but not all: at 375 prices a day the plain estimate is 9% low and the corrected one 2% low; at 75 prices, 20% low and 4% low.
- **Source.** Rogers, L. C. G. and Satchell, S. E. (1991), "Estimating Variance from High, Low and Closing Prices", *Annals of Applied Probability* 1(4), 504-512: the estimator is eq. (2), its unbiasedness eq. (3), the variances eq. (4), the correction eq. (5). `VERIFIED AGAINST PRIMARY`, read in the authors' typescript on Rogers's own site; the published journal page (Project Euclid) refused automated access, so equation numbers are those of the typescript. Rogers, L. C. G., Satchell, S. E. and Yoon, Y. (1994), "Estimating the volatility of stock prices: a comparison of methods that use high and low prices", *Applied Financial Economics* 4(3), 241-247: eq. (9) restates the estimator as $H(H-S)+L(L-S)$ with $H$, $S$, $L$ the logs of high, close and low over the open, and eq. (8) restates Garman-Klass's exact form. The paper adds an empirical comparison on UK assets and shows the estimator still works when the drift changes over time. `VERIFIED AGAINST PRIMARY` for eq. (8)-(9) and the abstract (scan on Rogers's site); the rest of that scan was not legible to the reader used.
- **Library check.** TTR `calc="rogers.satchell"`: `log(Hi/Cl)*log(Hi/Op) + log(Lo/Cl)*log(Lo/Op)`, averaged over $n$. Matches.

## 5. Yang and Zhang (2000)

$$ \hat\sigma^2_{YZ} = V_O + k\,V_C + (1-k)\,V_{RS} $$

$$ V_O = \frac{1}{n-1}\sum_{i=1}^{n}(o_i-\bar o)^2,\qquad V_C = \frac{1}{n-1}\sum_{i=1}^{n}(c_i-\bar c)^2,\qquad V_{RS} = \frac{1}{n}\sum_{i=1}^{n}\left[u_i(u_i-c_i)+d_i(d_i-c_i)\right] $$

$$ k = \frac{\alpha-1}{\alpha+\dfrac{n+1}{n-1}}\quad\text{with }\alpha=1.34\text{, that is}\quad k=\frac{0.34}{1.34+\dfrac{n+1}{n-1}} $$

- $V_O$ is the sample variance of the overnight returns, $V_C$ the sample variance of the open-to-close returns (both with the mean removed and divisor $n-1$), and $V_{RS}$ the Rogers-Satchell estimate (plain average, divisor $n$).
- $k$ is the weight that makes the combination as accurate as possible. $\alpha$ is the expected square of one day's Rogers-Satchell term divided by $\sigma^4$; it is 1.331 at zero drift and stays below 1.5 at any drift, and the authors recommend setting $\alpha$ to 1.34 in practice (p. 483).
- Values of $k$: 0.120 for $n=5$, 0.133 for $n=10$, 0.139 for $n=20$, 0.143 for $n=60$, tending to 0.145.

- **Data needed:** daily open, high, low, close, for at least two days. It is a multi-day estimator by construction; the paper proves no single-day estimator can be free of both drift and gap.
- **Assumptions:** continuous monitoring. **Drift allowed. Overnight gap allowed.**
- **Bias.** None in any of the four simulated cases (Table 1). Too low under discrete sampling of highs and lows, through its Rogers-Satchell part (the paper's section III says so).
- **The constant in $k$: checked.** The paper's eq. (10) is $k_0 = \dfrac{\alpha-1}{\alpha+\frac{n+1}{n-1}}$ and its conclusion, eq. (18), prints $k_0=\dfrac{0.34}{1.34+\frac{n+1}{n-1}}$. So **0.34 over 1.34 plus $(n+1)/(n-1)$ is right.** The paper's own worked example ($n=10$, $k_0=0.13$) agrees.
- **Efficiency.** Paper's eq. (11): $1/\left(f^2+(1-f)^2k\right)$, where $f$ is the overnight share of variance. The paper reports $f$ between 0.18 and 0.30 for US stocks, takes 0.25 as typical, and gives a typical efficiency of 7.3 for $n=10$, with a peak of 14 at $n=2$. Simulation at $n=20$, $f=0.25$: 7.5, with a sampling error of about 0.3 (eq. 11 gives 7.1).
- **What it gives up against Garman-Klass.** At zero drift the paper finds Garman-Klass (with the overnight term, eq. 4 below) only 8% more accurate at $n=10$ and 3% at large $n$.
- **Source.** Yang, D. and Zhang, Q. (2000), "Drift-Independent Volatility Estimation Based on High, Low, Open, and Close Prices", *Journal of Business* 73(3), 477-491: eq. (7) the estimator, (8) $V_O$, (9) $V_C$, (3) $V_{RS}$, (10) and (18) $k$, (11) efficiency. `VERIFIED AGAINST PRIMARY` (journal PDF hosted at atmif.com).
- **Library and secondary-source check.**

| Source | What it does | Matches the paper? |
| --- | --- | --- |
| R TTR `calc="yang.zhang"` | `k <- (alpha-1)/(alpha+(n+1)/(n-1))`, `alpha = 1.34`; `runVar` (divisor $n-1$) for $V_O$ and $V_C$; Rogers-Satchell with divisor $n$ | Yes |
| Python `qf-lib` `DriftIndependentVolatility` | same, cites the paper's equation numbers | Yes |
| Python `volatility-trading` (jasonstrimpel) `YangZhang.py`, current | $k$ correct, but: uses squared **close-to-close** returns where the paper has open-to-close; takes no mean off either piece; divides all three sums by $n-1$ | **No.** Biased high: +5% of variance with no gap, +9% with a 25% gap, +15% with gap and strong drift (Table 1, "library variant"). It is also no longer drift-independent |
| the same file before its issue #16 | `k = 0.34 / (1 + (window+1)/(window-1))` | **No**, the 1.34 was missing. This changes accuracy slightly, not the average (Table 1 and 2, "wrong k") |
| code copied from it (for example `colinkimball/BinomialOptionsModel`) | same as the current `volatility-trading` file | **No** |
| Rust `scirs2-series` `yang_zhang_volatility` | takes $k$ as an argument, gives 0.34 as its typical value, and documents the formula as $\sigma^2_o + k\sigma^2_c + \sigma^2_{rs}$ | **No.** 0.34 is $\alpha-1$, not $k$ |

## 6. Garman-Klass with the overnight term ("GKYZ")

**The form everybody prints:**

$$ \hat\sigma^2_{GKYZ} = \frac{1}{n}\sum_{i=1}^{n}\left[o_i^2 + \tfrac12\,(u_i-d_i)^2 - (2\ln 2-1)\,c_i^2\right] $$

that is, the practical Garman-Klass term for the session plus the squared overnight return.

**Where it really comes from.** Yang and Zhang (2000), eq. (4), write the Garman-Klass estimator as

$$ V_{GK} = V_O' - 0.383\,V_C' + 1.364\,V_P + 0.019\,V_{RS},\qquad V_O'=\frac1n\sum o_i^2,\quad V_C'=\frac1n\sum c_i^2 $$

where $V_P$ is Parkinson and $V_{RS}$ is Rogers-Satchell, and then point out that this expression does not appear explicitly in Garman and Klass (1980). They obtain it by setting the weight $a$ in Garman and Klass's formula 20 equal to $f$, which makes $f$ drop out. So:

1. The idea of adding an overnight term to the session estimate is **Garman and Klass's own** (their eq. 20, $\hat\sigma_6^2$). Their version needs $f$ and puts a weight $a=0.12$ on the overnight term.
2. The $f$-free version, overnight squared return plus the session estimate, was first written down by **Yang and Zhang** (eq. 4), using Garman-Klass's *exact* coefficients. Algebraically eq. (4) equals $o^2 + \hat\sigma_4^2$ of section 3 (since $c(u+d)-2ud = (u-d)^2 - [u(u-c)+d(d-c)]$ and $0.492\times4\ln2=1.364$).
3. The form with $\tfrac12$ and $(2\ln 2-1)$ is eq. (4) with Garman-Klass's *practical* coefficients (19a) swapped in. It is not printed in either paper. The name "Garman-Klass Yang-Zhang extension" comes from secondary sources: TTR's `gk.yz` cites a 2008 formula page on sitmo.com, and Bennett (2014, p. 243) prints it under that name. Whether Sinclair prints it could not be checked (section 19).

- **Data needed:** daily open, high, low, close and the previous close. Works on a single day.
- **Assumptions:** zero drift; continuous monitoring. **Overnight gap allowed.**
- **Bias.** Handles the gap (Table 1, column C: 0.995). Too high under drift, exactly as Garman-Klass (column B: +3.6%). The overnight term is not mean-removed, so a drifting overnight return adds to it as well.
- **Efficiency.** With a 25% overnight share, 7.9 in simulation against Yang-Zhang's 7.5: slightly more accurate than Yang-Zhang when there is no drift, which is what the Yang-Zhang paper says.
- **The two versions agree in practice.** Simulation: practical 1.036 and exact 1.034 under drift, identical to three decimals otherwise.
- **Source.** `VERIFIED AGAINST PRIMARY`: Yang and Zhang (2000) eq. (4)-(6) and the paragraph after it; Garman and Klass (1980) eq. (20). The practical-coefficient form is verified only against secondary sources and by simulation.
- **Library check.** TTR `calc="gk.yz"`: `log(Op/lag(Cl))^2 + .5*log(Hi/Lo)^2 - (2*log(2)-1)*log(Cl/Op)^2`, averaged over $n$. Matches the practical form.

## 7. Exponentially weighted moving average (RiskMetrics, 1996)

$$ \sigma^2_{t+1|t} = \lambda\,\sigma^2_{t|t-1} + (1-\lambda)\,r_t^2 \qquad\Longleftrightarrow\qquad \sigma^2_{t+1|t} = (1-\lambda)\sum_{j=0}^{\infty}\lambda^{j}\,r_{t-j}^2 $$

- $\sigma^2_{t+1|t}$ is the variance expected for tomorrow given everything up to today; $r_t$ is today's close-to-close log return; $\lambda$ (the decay factor) is 0.94 for daily data and 0.97 for monthly data.
- It is a "current" volatility: yesterday's return has weight 6%, the day before 5.6%, and so on. Nothing drops out of a window, so the figure never jumps when an old shock leaves.
- **Data needed:** closes only.
- **Assumptions:** the mean daily return is zero (the document says so explicitly). No assumption about gaps.
- **Bias.** Unbiased when the drift is zero; too high by $\mu^2/\sigma^2$ otherwise (simulation Table 1: 1.25 under strong drift, exactly as zero-mean close-to-close).
- **Efficiency.** The weights are equivalent to an equal-weighted window of $(1+\lambda)/(1-\lambda) = 32.3$ days when volatility is constant. Simulation Table 2: 1.7 times a 20-day window, as expected. Its purpose is not accuracy under constant volatility but speed when volatility changes.
- **How much history it uses.** The weight on everything older than $K$ days is $\lambda^K$. Solving $\lambda^K$ = tolerance gives $K = \ln(\text{tolerance})/\ln\lambda$. For $\lambda = 0.94$: 74 days at 1%, 112 at 0.1%, 149 at 0.01%. For $\lambda = 0.97$: 151, 227, 302.
- **Starting value.** The document gives no general rule; its worked example starts the recursion at the first squared return.
- **Annualising.** $\sqrt{252\,\sigma^2_{t+1|t}}$. RiskMetrics itself scales one day to one month with $\sqrt{25}=5$.
- **Source.** J.P. Morgan/Reuters (1996), *RiskMetrics Technical Document*, 4th edition, December 1996: recursion eq. [5.3], p. 81, derivation eq. [5.5], p. 82; zero mean section 5.3.1.1, pp. 91-93; decay factors 0.94 and 0.97, section 5.3.2, p. 97, and Table 5.9, p. 100; $K=\ln\Upsilon_L/\ln\lambda$ eq. [5.26], p. 93; the table of days (74, 112, 149, ...) Table 5.7, p. 94; starting value, footnote to Table 5.3, p. 82. `VERIFIED AGAINST PRIMARY` (Part II of the document, university-hosted PDF; Greek letters were lost in text extraction, equation and table numbers are as printed).
- **Practitioner view.** Bennett (2014, p. 237) describes exponentially weighted volatility, with $\lambda$ about 0.9, as rarely used, though possibly useful for indices.

## 8. Realised variance from intraday returns

$$ RV_t = \sum_{j=1}^{M} r_{t,j}^2 $$

where $r_{t,j}$ is the log return over the $j$-th of $M$ equal intervals inside day $t$ (for example $M=75$ five-minute returns in a 375-minute session). Realised volatility is $\sqrt{RV_t}$.

- **Data needed:** intraday bars or ticks.
- **What it converges to.** As the intervals shrink, $RV_t$ converges to the day's **quadratic variation**: the **integrated variance** (the variance of the continuous part of the price path, summed over the day) **plus the sum of the squared jumps**:

$$ RV_t \;\xrightarrow{\;M\to\infty\;}\; \underbrace{\int_{t-1}^{t}\sigma^2(s)\,ds}_{\text{integrated variance}} \;+\; \sum_{\text{jumps in day }t}\kappa_j^2 $$

  So realised variance does not need volatility to be constant within the day, and it counts jumps as volatility.
- **Assumptions.** The price is observed without error (no microstructure noise, section 9) and the intervals cover the period wanted (it says nothing about hours when the market is shut, section 12). No assumption about drift: over 5 minutes the drift is negligible next to the volatility.
- **How accurate one day's figure is.** With no jumps,

$$ \sqrt{M}\,\left(RV_t - IV_t\right) \;\to\; \text{mixed normal with variance } 2\,IQ_t,\qquad IQ_t=\int_{t-1}^{t}\sigma^4(s)\,ds $$

  ($IV$ is integrated variance; $IQ$, integrated quarticity, is the same integral of $\sigma^4$, with the day's length taken as 1). With constant volatility the standard error of one day's realised variance is $\sqrt{2/M}$ of its value: 16% from 75 five-minute returns, 7% from 375 one-minute returns (simulation Table 9: 0.163 and 0.073). A single day of 5-minute realised variance is as accurate as about 75 days of squared daily returns.
- **Bias.** None from drift or from changing volatility. Upward from microstructure noise as sampling gets finer (section 9). Excludes the overnight return (section 12).
- **Annualising.** $\sqrt{252\cdot RV_t}$ for a whole-day figure; see section 15 for a session-only or part-session figure.
- **Sources.**
  - Andersen, T. G. and Bollerslev, T. (1998), "Answering the Skeptics: Yes, Standard Volatility Models Do Provide Accurate Forecasts", *International Economic Review* 39(4), 885-905: the sum of squared intraday returns converges to the day's integrated variance, unnumbered display on p. 897 between eq. (14) and (15); Table 3 shows the measurement error falling as $m$ goes from 1 to 288 returns a day. `VERIFIED AGAINST PRIMARY` (scan of the published article; the display itself is damaged in the scan's text layer and was reconstructed from it and from the Table 3 footnote).
  - Andersen, Bollerslev, Diebold and Labys (2001), "The Distribution of Realized Exchange Rate Volatility", *JASA* 96(453), 42-55: definition eq. (12), convergence to quadratic variation eq. (13), p. 44. `VERIFIED AGAINST PRIMARY` for the equation numbers (published scan); the formula bodies were read in the August 2000 working paper.
  - Andersen, Bollerslev, Diebold and Labys (2003), "Modeling and Forecasting Realized Volatility", *Econometrica* 71(2), 579-625: Proposition 2, eq. (3)-(4), p. 584: the sum of squared returns converges to quadratic variation, which is the continuous part plus the squared jumps; eq. (10), p. 589, the no-jump case. `VERIFIED AGAINST PRIMARY`.
  - Barndorff-Nielsen, O. E. and Shephard, N. (2002), "Econometric analysis of realized volatility and its use in estimating stochastic volatility models", *JRSS B* 64(2), 253-280: definition and the central limit theorem above. Read in the November 2001 Nuffield working paper (definition eq. (7), Theorem 1 eq. (17)-(19)). `UNVERIFIED AGAINST PRIMARY` for the journal's own equation numbers.
- **Library check.** R `highfrequency` `rRVar`: `colSums(q^2)`, no scaling. Matches.

## 9. How often to sample: microstructure noise

**The problem.** An observed price is the true price plus a small error (bid-ask bounce, tick size, stale quotes): $Y_{t_i} = X_{t_i} + \epsilon_{t_i}$. Each return then carries two errors, and their squares add up. With $n$ returns in the day,

$$ \mathbb{E}\big[RV^{(\text{all})}\big] = IV + 2\,n\,\mathbb{E}[\epsilon^2] $$

The noise term grows with the number of returns. Sampled at every tick, realised variance mostly measures the noise, not the volatility. Simulation Table 7 reproduces the formula to three decimals.

**The volatility signature plot.** Plot the average realised variance (over many days) against the sampling frequency. With no noise the line is flat. With noise it rises as sampling gets faster. The frequency where it flattens is the fastest one that is safe. Source: Andersen, Bollerslev, Diebold and Labys (2000), "Great realizations", *Risk* 13(3), 105-108, p. 106. `VERIFIED AGAINST PRIMARY`.

**Why 5 minutes is the default.** It is slow enough that noise is small for liquid instruments and fast enough to give 75 or more returns a day. Liu, Patton and Sheppard (2015) tested it: over 400 realised measures, 31 assets in five asset classes, 11 years. Their conclusion, in the abstract: "it is difficult to significantly beat 5-minute RV". The detail (their section 6): tested against 5-minute realised variance as the benchmark, almost nothing was significantly better for any asset; with no benchmark, a few measures did better, most notably one-minute subsampled realised variance and realised kernels and multi-scale estimators on 1- and 5-second data; for forecasting, 5- or 15-minute truncated realised variance did best. The gains from the sophisticated measures shrank when noise or volatility was higher and outside US markets. `VERIFIED AGAINST PRIMARY` (*Journal of Econometrics* 187(1), 293-311).

**Subsampling and averaging.** A 5-minute grid can start at any of several offsets. Instead of throwing away all but one, compute realised variance on each offset grid and average them. Formally, split the $n+1$ tick observations into $K$ sub-grids, the $k$-th taking every $K$-th observation starting at the $k$-th:

$$ [Y,Y]^{(\text{avg})} = \frac{1}{K}\sum_{k=1}^{K}[Y,Y]^{(k)},\qquad [Y,Y]^{(k)} = \sum_{i}\left(Y_{t_{k+iK}}-Y_{t_{k+(i-1)K}}\right)^2,\qquad \bar n = \frac{n-K+1}{K} $$

$\bar n$ is the average number of returns per sub-grid. Same bias as sparse sampling, $2\bar n\,\mathbb{E}[\epsilon^2]$, but less noisy: simulation Table 7, standard deviation 0.134 against 0.172.

**The two-scales estimator (TSRV).** The all-ticks realised variance is almost pure noise, so it measures the noise. Subtract the right multiple of it from the subsampled average:

$$ \widehat{\langle X,X\rangle} = [Y,Y]^{(\text{avg})} - \frac{\bar n}{n}\,[Y,Y]^{(\text{all})},\qquad \widehat{\langle X,X\rangle}^{(\text{adj})} = \left(1-\frac{\bar n}{n}\right)^{-1}\widehat{\langle X,X\rangle} $$

The second form is the small-sample adjustment. The best number of sub-grids grows as $K = c\,n^{2/3}$. In simulation Table 7 the adjusted two-scales figure is 0.989 where plain 5-minute realised variance is 1.043 and tick realised variance is 1.756. The remaining 1% is an edge effect: offset grids that start late or stop early miss a little of the session, about $(K-1)/n$ of it.

Source: Zhang, L., Mykland, P. A. and Aït-Sahalia, Y. (2005), "A Tale of Two Time Scales: Determining Integrated Volatility With Noisy High-Frequency Data", *JASA* 100(472), 1394-1411: noise bias eq. (5), p. 1395, and eq. (18), p. 1397; subsampled average eq. (32) and $\bar n$ eq. (34), p. 1400; two-scales eq. (55), p. 1402; adjustment eq. (64), p. 1403; $K=cn^{2/3}$ section 1.2.5, p. 1396, with the optimal $c$ in eq. (10). `VERIFIED AGAINST PRIMARY` (published version on the author's Princeton page).

**Realised kernels.** Add to realised variance a weighted sum of the autocovariances of the high-frequency returns, the first $H$ of them, with weights from a smooth kernel function that falls from 1 to 0:

$$ K(X) = \gamma_0 + \sum_{h=1}^{H} k\!\left(\tfrac{h-1}{H}\right)\left(\gamma_h+\gamma_{-h}\right),\qquad \gamma_h = \sum_{j} r_j\,r_{j-h} $$

Noise makes neighbouring returns negatively correlated; the autocovariance terms cancel that. Source: Barndorff-Nielsen, Hansen, Lunde and Shephard (2008), "Designing realized kernels to measure the ex post variation of equity prices in the presence of noise", *Econometrica* 76(6), 1481-1536, eq. (6) of the March 2008 working paper. The paper does not single out one kernel in so many words; its simulations concentrate on the modified Tukey-Hanning kernel. Its companion, "Realised kernels in practice" (*Econometrics Journal* 12, 2009), uses the Parzen kernel in a slightly different form, weights $k(h/(H+1))$, because that guarantees a non-negative result, with bandwidth $H^* = 3.5134\,\xi^{4/5}n^{3/5}$ where $\xi^2$ is the noise variance divided by the square root of integrated quarticity. `UNVERIFIED AGAINST PRIMARY` for the journal versions: both were read as working papers.

**Pre-averaging.** First replace each price by a weighted local average of the $k_n$ prices around it, which shrinks the noise; then sum the squares of the changes in those averages; then subtract a term that removes what noise is left. In the paper's notation, with $\bar Z_i$ the pre-averaged change and $\Delta_i Z$ the raw return:

$$ \widehat C = \frac{\sqrt{\Delta_n}}{\theta\,\psi_2}\sum_i \bar Z_i^{\,2} \;-\; \frac{\psi_1\,\Delta_n}{2\,\theta^2\,\psi_2}\sum_i(\Delta_i Z)^2 $$

with $k_n\sqrt{\Delta_n}\approx\theta$ and, for the usual triangular weights, $\psi_1=1$, $\psi_2=1/12$. Source: Jacod, Li, Mykland, Podolskij and Vetter (2009), "Microstructure noise in the continuous case: the pre-averaging approach", *Stochastic Processes and their Applications* 119, 2249-2276, eq. (3.6), p. 2254. `VERIFIED AGAINST PRIMARY`.

**What this means in practice.** Two-scales, kernels and pre-averaging all reach the best possible rate and all need tick data and a tuning choice. Liu, Patton and Sheppard's result says plain 5-minute realised variance, perhaps subsampled, is hard to beat, so the engine needs the sophisticated ones only if it must sample faster than a few minutes.

**Library check.** R `highfrequency` `rTSCov`: same structure as eq. (55) with the eq. (64) adjustment always on; it counts prices rather than returns as $n$ (so $\bar n$ differs by $1/K$), and defaults to $K=300$ rather than a $n^{2/3}$ rule. `rKernelCov`: the flat-top form of eq. (6), but it defaults to a rectangular kernel with one lag, chooses no bandwidth, and by default rescales each lag by $N/(N-h)$, which is not in the paper.

## 10. Jump-robust measures

**Bipower variation.**

$$ BV_t = \mu_1^{-2}\sum_{j=2}^{M}|r_{t,j}|\,|r_{t,j-1}|,\qquad \mu_1 = \mathbb{E}|Z| = \sqrt{2/\pi} = 0.7979,\qquad \mu_1^{-2} = \frac{\pi}{2} = 1.5708 $$

$Z$ is a standard normal variable; $\mu_1$ is the average size of one. Each term multiplies two neighbouring absolute returns. A jump sits in one return; its neighbour is ordinary and small; so the product stays small and the jump's contribution vanishes as intervals shrink.

- **What it converges to:** the integrated variance alone, without the jumps.
- **What the difference measures:** $RV_t - BV_t$ converges to the sum of the squared jumps in the day. In a finite sample the difference can be negative; it is usual to floor it at zero.
- **Finite-sample correction.** The sum has $M-1$ terms, not $M$. The original paper applies no correction. Later work commonly multiplies by $M/(M-1)$ (this factor was not traced to a primary source here), or by $M/(M-2)$ for the "staggered" version that skips one return between the pair (Andersen, Bollerslev and Diebold 2007, *Review of Economics and Statistics* 89(4), eq. (22), p. 711, read). The simulation applies $M/(M-1)$; at $M=75$ it changes the figure by 1.3%.
- **Bias.** In a finite sample a jump is not fully removed, because the jump times an ordinary neighbour is not zero. Simulation Table 8: with jumps adding 25% to quadratic variation, bipower variation reads 1.09 on 5-minute returns and 1.05 on one-minute returns, against the ideal 1.00.
- **Source.** Barndorff-Nielsen, O. E. and Shephard, N. (2004), "Power and Bipower Variation with Stochastic Volatility and Jumps", *Journal of Financial Econometrics* 2(1), 1-37. Read in the November 2003 working paper: bipower variation eq. (2)-(3), $\mu_r = 2^{r/2}\Gamma\!\left(\tfrac{r+1}{2}\right)/\Gamma\!\left(\tfrac12\right)$ in Theorem 1, the limit and the jump decomposition in Theorem 5 and Remark 4 (eq. 19, 21-22). `UNVERIFIED AGAINST PRIMARY` for the journal's equation numbers. $\mu_1=\sqrt{2/\pi}$ follows from the paper's formula for $\mu_r$ at $r=1$.

**MinRV and MedRV.** Use the smaller of two neighbouring absolute returns, or the middle one of three, in place of the product:

$$ MinRV = \frac{\pi}{\pi-2}\cdot\frac{M}{M-1}\sum_{j=1}^{M-1}\min\!\big(|r_j|,|r_{j+1}|\big)^2,\qquad MedRV = \frac{\pi}{6-4\sqrt3+\pi}\cdot\frac{M}{M-2}\sum_{j=2}^{M-1}\operatorname{med}\!\big(|r_{j-1}|,|r_j|,|r_{j+1}|\big)^2 $$

A jump is discarded outright, not multiplied by a small number, so less of it leaks through: simulation Table 8, 1.03 on 5-minute returns and 1.01 on one-minute returns. Source: Andersen, T. G., Dobrev, D. and Schaumburg, E. (2012), "Jump-robust volatility estimation using nearest neighbor truncation", *Journal of Econometrics* 169(1), 75-93; read as NBER Working Paper 15533, eq. (4). `UNVERIFIED AGAINST PRIMARY` for the journal's equation number; constants and factors are as printed in the working paper.

**Library check.** R `highfrequency`: `rBPCov` is $(\pi/2)\sum|r_j||r_{j+1}|$ with no $M/(M-1)$ factor, as in the original paper. `rMinRVar` and `rMedRVar` match the formulas above exactly, constants and factors included.

## 11. Realised range

$$ RR_t = \frac{1}{4\ln 2}\sum_{j=1}^{M}\left(\ln H_{t,j} - \ln L_{t,j}\right)^2 $$

where $H_{t,j}$ and $L_{t,j}$ are the high and low of the $j$-th intraday bar. It is Parkinson's estimator applied to each intraday bar and added up.

- **Why use it.** The range of a bar uses every tick in it. The variance of the estimate is about 0.4 where realised variance's is 2, for the same number of bars: about five times more precise. Simulation Table 9: realised range on 5-minute bars is as accurate as realised variance on one-minute returns.
- **The catch.** $4\ln 2$ is right only if each bar's high and low are the true continuous extremes. If a bar contains only $m$ observed prices, the divisor must be a smaller constant $\lambda_{2,m}$ (the expected squared range of an $m$-step random walk), which has no formula and is found by simulation; $\lambda_{2,1}=1$ (one return per bar gives plain realised variance) and $\lambda_{2,m}\to 4\ln2 = 2.773$. Simulation Table 9: with five prices per bar and the divisor left at $4\ln 2$ the result is 0.57, which puts $\lambda_{2,5}$ near 1.59.
- **Noise.** Bid-ask bounce widens every bar's range, so the bias from noise is upward and can be severe. Martens and van Dijk scale the realised range by the ratio of the average *daily* range to the average realised range over the previous $q$ days, on the argument that the daily range is almost free of noise.
- **Sources.** Christensen, K. and Podolskij, M. (2007), "Realized range-based estimation of integrated variance", *Journal of Econometrics* 141(2), 323-349: estimator eq. (2.14), central limit theorem with the constant 0.4073 eq. (2.17)-(2.19), pp. 329-331; the discrete version with $\lambda_{2,m}$ eq. (2.26)-(2.29), p. 332. `VERIFIED AGAINST PRIMARY`. Martens, M. and van Dijk, D. (2007), "Measuring volatility with the realized range", *Journal of Econometrics* 138(1), 181-207: read as Econometric Institute Report 2006-10, eq. (2)-(5) and (10)-(11). `UNVERIFIED AGAINST PRIMARY` for the journal's equation numbers.

## 12. Overnight and weekends: a market that is shut most of the day

Intraday realised variance covers the session only. NSE is open 375 minutes of 1,440. The move from close to next open is real risk to an option holder and is in the implied volatility. Three ways to get a whole-day figure. $RV_t$ is the session's realised variance, $o_t$ the overnight return, $r_t$ the close-to-close return.

**1. Add the squared overnight return.**

$$ RV^{\text{day}}_t = o_t^2 + RV_t $$

Right on average. But $o_t^2$ is a one-observation estimate of the overnight variance and is very noisy: in simulation Table 6 it more than doubles the day-to-day noise of the figure (0.368 against 0.163).

**2. Scale the session figure up.**

$$ RV^{\text{day}}_t = \hat\delta\,RV_t,\qquad \hat\delta = \frac{\sum_{t=1}^{n}(r_t-\bar r)^2}{\sum_{t=1}^{n}RV_t} $$

$\hat\delta$ is total close-to-close variance over total session realised variance, measured over a long history. Right on average and no noisier than $RV_t$ itself; but it assumes the overnight variance is always the same multiple of the session's, so a calm session after a large gap is understated.

**3. The best linear combination.**

$$ RV^{\text{day}}_t = \omega_1^{*}\,o_t^2 + \omega_2^{*}\,RV_t,\qquad \omega_1^{*} = (1-\varphi)\frac{\mu_0}{\mu_1},\quad \omega_2^{*} = \varphi\,\frac{\mu_0}{\mu_2},\quad \varphi = \frac{\mu_2^2\,\eta_1^2 - \mu_1\mu_2\,\eta_{12}}{\mu_2^2\,\eta_1^2 + \mu_1^2\,\eta_2^2 - 2\mu_1\mu_2\,\eta_{12}} $$

$\mu_0$ is the average whole-day variance (average of $o_t^2+RV_t$), $\mu_1$ the average of $o_t^2$, $\mu_2$ the average of $RV_t$; $\eta_1^2$ and $\eta_2^2$ are the variances of $o_t^2$ and $RV_t$, $\eta_{12}$ their covariance. The weights keep the average right ($\omega_1\mu_1+\omega_2\mu_2=\mu_0$) and put less weight on the noisy overnight square than its share of variance. Methods 1 and 2 are the special cases $\omega=(1,1)$ and $\omega=(0,\hat\delta)$.

- **Source.** Hansen, P. R. and Lunde, A. (2005), "A realized variance for the whole day based on intermittent high-frequency data", *Journal of Financial Econometrics* 3(4), 525-554. **`UNVERIFIED AGAINST PRIMARY`.** The article is behind a paywall and the SSRN copy refused access. The abstract was read (three estimators studied; the optimal combination can be found even though true variance is unobserved; applied to the 30 Dow Jones stocks over four years). The formulas above are as restated, identically, in three later papers, including Ahoniemi and Lanne (Bank of Finland Discussion Paper 19/2010, eq. 2.2-2.3). Hansen and Lunde's own equation numbers are not confirmed.
- **Evidence on which is best.** Ahoniemi and Lanne (working-paper version of *International Journal of Forecasting* 29(4), 2013) on the S&P 500 index, 1994-2007: the weighted estimator (method 3) is the most accurate overall; ignoring the overnight return, or adding it unweighted, is not recommended. Their estimated weights with a 9:35 opening price were about 0.55 on the overnight square and 1.11 on the session figure (the table's row labels were lost in text extraction and are inferred).
- **How much variance is overnight.** Yang and Zhang (2000): 18% to 30% for US stocks, typical 25%. Ahoniemi and Lanne's S&P 500 figures imply about 20% (derived from their table, not stated by them). Bennett (2014, p. 241): roughly one-sixth of equity volatility falls outside the trading day. No figure for NIFTY was found; it must be measured from our own data, which is what $\hat\delta$ does.
- **Weekends and holidays.** The same three methods apply; the Friday-close-to-Monday-open return is just a larger overnight return. Under method 2, $\hat\delta$ absorbs weekends on average. French and Roll (1986, *Journal of Financial Economics* 17, 5-26; abstract read) established that prices are much more volatile per hour when the exchange is open than when it is shut, which is why a weekend is worth far less than three days of variance and why trading days, not calendar days, are the usual clock (section 15).
- **What practitioners do.** Bennett (2014): for anything compared with a variance swap or hedged at the close, use close-to-close, which contains the overnight move with no adjustment; among range estimators only GKYZ and Yang-Zhang handle the gap (his Figure 142). For intraday realised variance the simple default is method 1; the literature above favours method 3 or 2.
- **The opening price.** Which price counts as the open changes the split. Andersen and Bollerslev (1997, p. 152) drop the first 5-minute S&P 500 return because it carries overnight information. NSE holds a pre-open call auction from 09:00 (orders collected for about 8 minutes, then matched) before continuous trading at 09:15.

## 13. Intraday seasonality: making part of a day comparable

**The pattern.** Volatility is not flat through the session. In equity markets it is high at the open, low around midday and higher again into the close: a U, or a reverse J when the open is much higher than the close. Evidence: Wood, McInish and Ord (1985, *Journal of Finance* 40(3), 723-739) and Harris (1986, *Journal of Financial Economics* 16(1), 99-117) for US stocks; for India, a U-shape in NIFTY futures on one-minute data 2011-2018 (Singh and Gangwar 2018) and a reverse-J in NSE stocks (Agarwalla and Pandey 2012). These four were seen as abstracts or citations only.

**The model.** Andersen and Bollerslev (1997) write the $n$-th of $N$ intraday returns on day $t$ as

$$ R_{t,n} = \mathbb{E}(R_{t,n}) + \frac{\sigma_t\,s_{t,n}\,Z_{t,n}}{N^{1/2}} $$

$\sigma_t$ is the day's volatility, $s_{t,n}$ the seasonal factor for that time of day (averaging one across the day), $Z_{t,n}$ a random shock with unit variance. They estimate $s$ by regressing the log of squared, mean-removed, volatility-standardised returns on a smooth function of the time of day (a "flexible Fourier form": a quadratic in $n$ plus a few sines and cosines plus dummies for special intervals), their eq. (A.1)-(A.4). A return is **deseasonalised** by dividing it by its factor: $\tilde R_{t,n} = R_{t,n}/\hat s_{t,n}$.

**The simple version.** Taylor and Xu (1997) skip the regression: the seasonal variance multiplier for each time-of-day bucket is that bucket's average squared return as a share of the daily total, scaled so the multipliers average one:

$$ \hat s_j^2 = \frac{\text{average squared return in bucket } j}{\text{average squared return over all buckets}} $$

**Making a part-day figure comparable.** No paper was found that states this rule; it follows directly from the model. If the first $k$ of $N$ intervals have been seen,

$$ \widehat{RV}^{\text{full}}_t = \frac{\sum_{n\le k}R_{t,n}^2}{c_k},\qquad c_k = \frac{\sum_{n\le k}s_n^2}{\sum_{n\le N}s_n^2} $$

$c_k$ is the share of a normal day's variance that has usually arrived by interval $k$, estimated as the historical average of (cumulative squared returns to $k$) / (the day's total). Simulation Table 10 confirms it: after 60 of 375 minutes of a U-shaped day, 25% of the variance has arrived, not 16%; scaling by the clock overstates by 58%, scaling by $c_k$ is exact. Equivalently, deseasonalise each return first and then scale by the clock.

- **Caveats.** The shape is not constant: Andersen and Bollerslev (footnote 35) note it turns from U to J on the most volatile days. The profile should be estimated robustly, because a few jump days distort plain averages: Boudt, Croux and Laurent (2011, *Journal of Empirical Finance* 18(2), 353-367) give a weighted-standard-deviation estimator that discards standardised returns whose square exceeds 6.635 (the 99% point of a chi-squared with one degree of freedom) and rescales by 1.081. Expiry days, event days and special sessions have their own shape.
- **Sources.** Andersen, T. G. and Bollerslev, T. (1997), "Intraday periodicity and volatility persistence in financial markets", *Journal of Empirical Finance* 4(2-3), 115-158: eq. (1), p. 125; eq. (7), p. 141; deseasonalising, section 5.1, p. 142; estimation, eq. (A.1)-(A.4), pp. 152-153. `VERIFIED AGAINST PRIMARY` (scan on Bollerslev's Duke page). Taylor, S. J. and Xu, X. (1997), "The incremental volatility information in one million foreign exchange quotations", *Journal of Empirical Finance* 4(4), 317-340: seasonal multipliers eq. (14). Partly verified only: the scan's text was garbled and the exact constants in eq. (14) were reconstructed from the constraint that the multipliers average one. Boudt, Croux and Laurent: working-paper version read, eq. (2.9)-(2.13).


---

## 14. The numerical check

`verify_estimators.py` (numpy only, about a minute to run) simulates a price whose true volatility is known to be exactly 20% a year on a 252-day year, and reports what each estimator returns.

**How the simulation is built.**

- Each trading session is 375 minutes (the NSE session), cut into 1,500 steps of 15 seconds ("ticks"). One-minute bars are 4 ticks; 5-minute bars are 20.
- The true high and low *between* ticks are drawn exactly, from the known law of the maximum of a random walk pinned at both ends. So "continuous" highs and lows in the tables are exact, not an approximation.
- Four main cases, 60,000 days each: **A** no drift, no overnight gap; **B** drift of half a daily standard deviation per day (about 159% a year, a violent trend) and no gap; **C** no drift, 25% of each day's variance overnight; **D** both.
- Side cases: several drift sizes; noise of 2 basis points added to every tick (far more than a liquid index future has; chosen so the effect is visible); one jump a day; a U-shaped session.
- Every figure is **mean estimated variance divided by true variance**. 1.000 is perfect. 1.10 means variance 10% too high, so volatility about 4.9% too high ($\sqrt{1.10}=1.049$), that is 20.98 where the truth is 20.
- The sampling error of a mean over 60,000 days is about 0.006 for close-to-close and less for the others. Case A's close-to-close figure (0.987) is two sampling errors low; that is chance in this seed, and Table 5's third column removes it.

**Output** (`verify_output.txt`):

```text
True volatility 20% a year; 252 days a year; 
60000 simulated days per scenario; session 375 minutes; 1500 ticks a day.
Every figure is  mean estimated variance / true variance  unless it says otherwise.

Table 1. Daily-bar estimators, 20-day windows, true continuous highs and lows
-----------------------------------------------------------------------------
                                             A none        B drift          C gap         D both
Close-to-close, mean removed, n-1             0.987          1.000          0.997          1.008
Close-to-close, zero mean, n                  0.989          1.249          0.999          1.263
Parkinson                                     0.997          1.095          0.749          0.805
Garman-Klass practical (19a)                  1.000          1.036          0.748          0.770
Garman-Klass exact (19)                       1.000          1.034          0.749          0.770
Rogers-Satchell                               1.000          1.001          0.749          0.750
GKYZ practical (o^2 + 19a)                    1.000          1.036          0.995          1.037
GK per Yang-Zhang eq. (4)                     1.000          1.034          0.995          1.036
Yang-Zhang, k from eq. (18)                   0.999          1.000          0.995          1.001
Yang-Zhang, wrong k (0.34/(1+..))             0.998          1.000          0.995          1.001
Yang-Zhang, library variant                   1.051          1.090          1.085          1.145
EWMA lambda 0.94 (zero mean)                  0.990          1.249          0.999          1.263
A: no drift, no overnight gap.  B: drift of 0.5 daily standard deviations a day (about 159% a year).
C: 25% of each day's variance falls overnight.  D: both.

Table 2. Efficiency: variance of the close-to-close estimate / variance of this estimate
----------------------------------------------------------------------------------------
                                           1 day, A          paper     20 days, A     20 days, C
Close-to-close, mean removed, n-1                                           1.000          1.000
Close-to-close, zero mean, n                  1.000            1.0          1.051          1.043
Parkinson                                     4.853     4.91 / 5.2          5.303       (biased)
Garman-Klass practical (19a)                  7.247            7.4          7.862       (biased)
Garman-Klass exact (19)                       7.245            7.4          7.854       (biased)
Rogers-Satchell                               5.875            6.0          6.209       (biased)
GKYZ practical (o^2 + 19a)                                                  7.862          7.907
GK per Yang-Zhang eq. (4)                                                   7.856          7.901
Yang-Zhang, k from eq. (18)                                                 7.384          7.460
Yang-Zhang, wrong k (0.34/(1+..))                                           7.375          7.464
EWMA lambda 0.94 (zero mean)                                                1.673          1.722
'1 day' is the papers' own definition: one day's squared close-to-close return against one day's estimate.
'20 days' compares 20-day windows with the mean-removed close-to-close estimate (n-1 = 19), so the
single-day figures are multiplied by about 20/19 there.
Yang-Zhang k for n=20: 0.1390.  Paper's eq. (11) efficiency 1/(f^2+(1-f)^2 k) with f=0.25: 7.11; with f=0: 7.19.
EWMA theory: (1+lambda)/(1-lambda) = 32.3 effective days against 19, ratio 1.70.

Table 3. Scenario A, highs and lows taken from N equally spaced prices a day
----------------------------------------------------------------------------
                                               N=25           N=75          N=375         N=1500     continuous
Parkinson                                     0.765          0.855          0.930          0.963          0.997
Garman-Klass practical (19a)                  0.679          0.802          0.908          0.953          1.000
Rogers-Satchell                               0.672          0.800          0.908          0.953          1.000
Rogers-Satchell corrected, eq. (5)            0.935          0.958          0.981          0.990            n/a
N=75 is one price every 5 minutes, N=375 every minute, N=1500 every 15 seconds.

Table 4. Bias against drift (drift per day / one day's standard deviation), no gap, continuous highs and lows
-------------------------------------------------------------------------------------------------------------
                                                  0            0.1           0.25            0.5              1              2
Close-to-close, zero mean, n                  0.992          0.998          1.072          1.281          1.979          4.954
Close-to-close, mean removed, n-1             0.993          0.987          1.009          1.022          0.981          1.004
Parkinson                                     1.001          1.006          1.031          1.104          1.370          2.465
Garman-Klass practical (19a)                  1.004          1.010          1.015          1.036          1.134          1.504
Rogers-Satchell                               1.006          1.006          1.003          0.998          0.998          0.993
Yang-Zhang, k from eq. (18)                   1.004          1.003          1.004          1.001          0.996          0.995
0.1 is about 32% a year at 20% volatility; 0.5 is about 159% a year; 1.0 and 2.0 are short violent trends.

Table 5. Close-to-close: the standard deviation is biased low even when the variance is not
-------------------------------------------------------------------------------------------
                                       mean s/sigma    mean s2/var   E[s]/rtE[s2]          c4(n)
n = 5 returns                                 0.933          0.985          0.940          0.940
n = 10 returns                                0.967          0.988          0.973          0.973
n = 20 returns                                0.981          0.987          0.987          0.987
n = 60 returns                                0.990          0.988          0.996          0.996
s = sample standard deviation with n-1.  The third column removes this sample's own luck in the variance
and should equal c4(n) = sqrt(2/(n-1)) * Gamma(n/2) / Gamma((n-1)/2).
Sampling error of a mean variance over 60000 days is about 0.006.

Table 6. Intraday realised variance (RV), no noise
--------------------------------------------------
                                                      ratio
A: RV 1-min / session variance                        1.000
A: RV 5-min / session variance                        1.000
A: RV 5-min / whole-day variance                      1.000
A: (RV 5-min + overnight^2) / whole day               1.000
A: scaled RV 5-min / whole day                        0.989
A:   scale factor used                                0.989
A: sd of daily (RV5 + overnight^2)                    0.163
A: sd of daily scaled RV5                             0.162
A: sd of daily squared c-c return                     1.391
C: RV 1-min / session variance                        1.000
C: RV 5-min / session variance                        0.999
C: RV 5-min / whole-day variance                      0.749
C: (RV 5-min + overnight^2) / whole day               0.996
C: scaled RV 5-min / whole day                        0.999
C:   scale factor used                                1.334
C: sd of daily (RV5 + overnight^2)                    0.368
C: sd of daily scaled RV5                             0.163
C: sd of daily squared c-c return                     1.410
'sd' rows: day-to-day standard deviation of the one-day estimate, in units of the true daily variance.

Table 7. Noise of 2 basis points added to every 15-second price (scenario A otherwise)
--------------------------------------------------------------------------------------
                                                      ratio
RV sampled every 15s                                  1.756
RV sampled every 1m                                   1.189
RV sampled every 5m                                   1.043
RV sampled every 15m                                  1.018
RV sampled every 25m                                  1.009
Subsampled 5-min RV (20 offsets)                      1.027
Two-scales RV, K=20                                   0.940
Two-scales RV, small-sample adjusted                  0.989
sd of daily: RV 5-min                                 0.172
sd of daily: subsampled 5-min RV                      0.134
sd of daily: two-scales adjusted                      0.141
Expected RV bias = 2 * (number of returns) * noise variance: 15s 1.756, 1m 1.189, 5m 1.038, 15m 1.013, 25m 1.008
(A 375-minute session does not divide into 30- or 60-minute bars; 25 minutes is used instead.)

Table 8. One jump a day carrying 25% extra variance (quadratic variation = 1.25, integrated variance = 1.00)
------------------------------------------------------------------------------------------------------------
                                                 with jumps       no jumps
RV, 5m returns                                        1.254          1.000
Bipower variation, 5m returns                         1.091          1.000
MedRV, 5m returns                                     1.034          0.999
MinRV, 5m returns                                     1.032          0.999
RV, 1m returns                                        1.254          1.000
Bipower variation, 1m returns                         1.047          1.001
MedRV, 1m returns                                     1.009          1.000
MinRV, 1m returns                                     1.008          1.001

Table 9. Realised range against realised variance, scenario A, divisor 4 ln 2
-----------------------------------------------------------------------------
                                                           mean    sd of daily
Realised range, 5-min bars, true highs/lows               1.000          0.074
Realised range, bars built from 5 1-min closes            0.572          0.061
RV 5-min                                                  1.000          0.163
RV 1-min                                                  1.000          0.073
Theory for the sd of one day: RV with M returns sqrt(2/M): 5-min 0.163, 1-min 0.073; range with 75 bars sqrt(0.4073/75) = 0.074.

Table 10. U-shaped session (variance at the open and close 4x midday): part-day RV scaled to a full session
-----------------------------------------------------------------------------------------------------------
                                           by clock     by profile   share so far
after 60 of 375 minutes                       1.579          1.005          0.251
after 187 of 375 minutes                      1.005          1.003          0.499

Annualising check: sqrt(252 * mean daily variance) for scenario A close-to-close = 0.1987 (true 0.2000)
```

**What the tables show.**

1. **Every formula recovers 20% where its assumptions hold.** Table 1 column A: the range estimators are all between 0.997 and 1.000; the close-to-close family reads 0.987 to 0.990, which is two sampling errors low and is chance (the same estimators read 1.000, 0.997 and 1.008 in the other columns). The only real miss is the library variant of Yang-Zhang.
2. **Drift** (column B, and Table 4): zero-mean close-to-close and EWMA are 25% too high in variance; Parkinson 10%; Garman-Klass and GKYZ 4%; Rogers-Satchell, Yang-Zhang and mean-removed close-to-close are unaffected. Table 4 shows that at realistic drifts (0.1 of a daily standard deviation, about 32% a year) nothing is off by more than 1%.
3. **Overnight gap** (column C): Parkinson, Garman-Klass and Rogers-Satchell return 0.75, exactly the session's share. GKYZ and Yang-Zhang return 1.00.
4. **Both** (column D): only Yang-Zhang and mean-removed close-to-close stay at 1.00.
5. **Efficiency** (Table 2): Parkinson 4.85, Garman-Klass 7.25, Rogers-Satchell 5.9, against the papers' 4.9 to 5.2, 7.4 and 6.0. Yang-Zhang 7.4 to 7.5 on 20 days. EWMA with 0.94 is worth 1.7 times a 20-day window, as its 32 effective days imply.
6. **Highs and lows from sampled prices** (Table 3): every range estimator reads low. From one-minute prices: Parkinson 7% low in variance, Garman-Klass and Rogers-Satchell 9% low. From 5-minute prices: 14% and 20% low. This matters when daily bars are built from a bar feed rather than taken from the exchange's own day high and low.
7. **Standard deviation bias** (Table 5): matches $c_4(n)$.
8. **Intraday realised variance** (Table 6): recovers the session's variance exactly; misses the overnight quarter in case C; adding the squared overnight return or scaling both fix the average, but scaling gives a daily figure less than half as noisy (0.163 against 0.368).
9. **Noise** (Table 7): realised variance from every tick is 76% too high, from one-minute returns 19%, from 5-minute returns 4%, matching the formula $2 \times \text{(number of returns)} \times \text{noise variance}$. Two-scales removes the bias (0.989; the remaining 1% is an edge effect explained in section 9) and is less noisy than plain 5-minute realised variance.
10. **Jumps** (Table 8): realised variance reports 1.25 (it includes the jump); bipower variation 1.09 on 5-minute returns and 1.05 on one-minute returns; MedRV and MinRV 1.03 and 1.01. The jump-robust measures are robust only approximately at coarse sampling.
11. **Realised range** (Table 9): unbiased with true highs and lows and as accurate from 5-minute bars as realised variance is from one-minute returns; badly low (0.57) if each bar's high and low come from only five prices and the divisor is left at $4\ln 2$.
12. **Part of a day** (Table 10): after the first hour of a U-shaped session, scaling by the clock overstates the day's variance by 58%; scaling by the usual share of variance by that time is right.

---

## 15. Annualising

**The rule.** Variance adds across time; volatility does not. If two periods' returns are independent, the variance of their sum is the sum of their variances. So:

1. Work in variance.
2. Multiply the per-period variance by the number of such periods in a year.
3. Take the square root last.

Never average volatilities across days, and never scale a volatility by a time ratio without the square root: average the variances, then take the root. Averaging volatilities reads low (the same concavity effect as in section 1).

**Which year: 252 or 365.**

- **Trading-day convention.** Daily returns are treated as equal, one per trading day, about 252 a year. Annual variance = 252 times daily variance. This is the convention for realised volatility (Bennett 2014, p. 233). It rests on the fact that prices move far more per hour when the market is open than when it is shut (French and Roll 1986).
- **Calendar convention.** Time runs at the same rate every day, 365 days a year. Annual variance = 365 times daily variance. This is right for a market that never shuts.
- **The two differ by** $\sqrt{365/252} = 1.2035$. Annualising a trading-day volatility with $\sqrt{365}$ overstates it by 20%.
- **Implied volatility is quoted on the calendar convention.** The Cboe VIX measures time to expiry as minutes divided by the minutes in a 365-day year (525,600); so does India VIX (NSE white paper, section 3.1, worked example dividing by 525,600); Deribit's DVOL converts to a daily move with $\sqrt{365}$. Over a whole year the two clocks agree (252 trading days span 365 calendar days). Over a short span that contains a weekend or holiday they do not. Matching the two is the horizon worker's subject; this note only flags it.

**How many trading days there really are.**

| Year | NSE full sessions | NYSE sessions (of which 13:00 early closes) |
| --- | --- | --- |
| 2019 | 244 | 252 (3) |
| 2020 | 250 | 253 (2) |
| 2021 | 247 | 252 (1) |
| 2022 | 247 | 251 (1) |
| 2023 | 245 | 250 (2) |
| 2024 | 246 | 252 (3) |
| 2025 | 248 | 250 (3) |
| 2026 | 246 (if the holiday list stands) | 251 (2) |
| Average | 246.6 | 251.4 |

- NSE counts exclude the one-hour Diwali Muhurat session each year and the two short disaster-recovery test sessions of 2024; they include the full Saturday session of 20 January 2024 and the Budget-day sessions of Saturday 1 February 2025 and Sunday 1 February 2026.
- How verified: NSE holiday circulars were read for 2021, 2022 and 2025; other NSE years were counted from index history and are not circular-verified; 2026 is from secondary copies of the NSE list. NYSE counts follow the exchange's holiday rules and match the number of S&P 500 daily rows for 2019-2025; early-close dates before 2026 are rule-derived.
- India has about 247 sessions a year, not 252. Using 252 for India overstates volatility by $\sqrt{252/247}-1 = 1.0\%$. Small, but it is a constant bias; decide the convention once and state it on the screen.

**Exact factors.** "Variance factor" multiplies the per-period variance; "volatility factor" is its square root and multiplies the per-period volatility.

| What was measured | Variance factor | Volatility factor |
| --- | --- | --- |
| Daily close-to-close, 252-day year | 252 | 15.875 |
| Daily close-to-close, India at 247 sessions | 247 | 15.716 |
| Daily, market open every day (crypto) | 365 | 19.105 |
| One NSE session's realised variance (375 min), session only | 252 | 15.875 |
| NSE 1-minute returns, per-bar variance, session only | 375 x 252 = 94,500 | 307.41 |
| NSE 5-minute returns, session only | 75 x 252 = 18,900 | 137.48 |
| NSE 15-minute returns, session only | 25 x 252 = 6,300 | 79.37 |
| One US session's realised variance (390 min), session only | 252 | 15.875 |
| US 1-minute returns, session only | 390 x 252 = 98,280 | 313.50 |
| US 5-minute returns, session only | 78 x 252 = 19,656 | 140.20 |
| Crypto 1-minute returns | 1,440 x 365 = 525,600 | 724.98 |
| Crypto 5-minute returns | 288 x 365 = 105,120 | 324.22 |
| Crypto hourly returns | 24 x 365 = 8,760 | 93.59 |

**"Session only" matters.** The intraday factors above annualise the variance of the *open session*. They leave out the overnight variance. To get a whole-day figure comparable with close-to-close volatility and with implied volatility, use one of the three methods of section 12 before multiplying by 252:

$$ \sigma^2_{\text{annual}} = 252\times\left(RV_{\text{session}} + o^2\right)\quad\text{or}\quad 252\times\hat\delta\times RV_{\text{session}} $$

If the overnight share of variance is $f$, a session-only figure is low by the factor $\sqrt{1-f}$ in volatility: 0.89 at $f=0.2$, 0.87 at $f=0.25$.

**Part of a session.** Realised variance $RV_{0\to m}$ accumulated over the first $m$ minutes of an $S$-minute session:

$$ \sigma^2_{\text{annual, session only}} = 252\times\frac{RV_{0\to m}}{c_m}\qquad\text{with } c_m = \text{usual share of the session's variance by minute } m $$

Using $c_m = m/S$ (the clock: 375/$m$ for NSE, 390/$m$ for the US) is correct only if volatility is flat through the day, and it is not (section 13, Table 10).

**A rolling intraday window** of $w$ minutes of session time: variance factor $(S/w)\times252$ for session-only annualisation, with the same seasonal caveat unless $w$ is a whole number of sessions.

**Things that change the factor from day to day.**

- **Bar sizes that do not divide the session.** 375 minutes divides evenly into 1, 3, 5, 15, 25 and 75-minute bars, not into 10, 30 or 60. 390 divides into 1, 2, 3, 5, 6, 10, 13, 15, 30, not 60. A "30-minute" series on NSE has a short last bar; counting it as a full bar misstates the factor.
- **Short sessions.** US half days (close 13:00 ET, 210 minutes), the Muhurat hour.
- **Commodities.** MCX trades 09:00 to 23:30 IST (870 minutes), extended to 23:55 (895 minutes) when the US is off daylight saving time, roughly November to March; the session length changes twice a year. CME crude and gold trade nearly 23 hours a day, Sunday evening to Friday (not verified on the exchange's own page).
- **SPX options** trade 09:30 to 16:15 ET, 15 minutes past the stock close, plus an overnight session; the *underlying* index is computed 09:30 to 16:00.
- **Crypto.** 24 hours, 365 days (366 in a leap year). There is no overnight gap and no session, but there is still a daily and weekly rhythm in volatility, so part-day scaling needs a profile there too.

**Sources.** Cboe, *Volatility Index Mathematics Methodology*, section "Time to Expiration"; NSE, *India VIX white paper*, section 3.1; Deribit, DVOL article; NSE market-timings page and holiday circulars; NYSE hours-and-calendars page; Cboe SPX specifications; MCX trading-hours page. Links in the source list.


## 16. Computing it live versus over history

Nothing in this section comes from a single paper; it is engineering consequence of the formulas, with sources named where one exists. Treat it as reasoning to be checked in design.

### Daily-bar estimators (sections 1 to 6)

- **Running value.** Every one of them is an average of a per-day term (or, for close-to-close and Yang-Zhang, a sample variance). Keep the last $n$ days' terms in a fixed-length buffer.
  - Close-to-close with the mean removed needs two running sums, $\sum r$ and $\sum r^2$: variance $= \left(\sum r^2 - (\sum r)^2/n\right)/(n-1)$.
  - Parkinson, Garman-Klass, Rogers-Satchell, GKYZ need one running sum of the day's term.
  - Yang-Zhang needs five: $\sum o$, $\sum o^2$, $\sum c$, $\sum c^2$, $\sum$ Rogers-Satchell term.
  - Adding the newest and subtracting the oldest accumulates rounding error over months. With $n$ at most a few hundred it costs nothing to recompute the sums from the buffer at every update, which removes the problem.
- **History needed at start-up.** $n$ complete daily bars for Parkinson, Garman-Klass, Rogers-Satchell; $n$ bars plus the close before them ($n+1$ bars) for close-to-close, GKYZ and Yang-Zhang. The number is not valid before that. Yang-Zhang needs at least 2 days by construction.
- **A part-finished day.** The newest bar is incomplete until the close. If it is included as if complete, the estimate reads low: the return so far and the range so far are smaller than the day's will be. The shortfall is at most one day's weight, $1/n$ of the variance, largest just after the open. Two clean choices: update only at the close (the number steps once a day), or keep the daily-bar estimate for complete days and show the current day separately from intraday realised variance (below).
- **Bad ticks.** One false print becomes the day's high or low and enters the range estimators squared. It then sits in the window for $n$ days. Close-to-close is immune unless the false print is the close. Prefer the exchange's official daily bar to one built from a raw tick feed, and compare the two.
- **Sampled highs and lows.** If the daily high and low are built from one-minute or 5-minute closes they are too narrow (Table 3). Build them from each bar's own high and low, which come from ticks.
- **The opening price.** GKYZ and Yang-Zhang split the day at the open. An index's first printed value can be stale (built from constituents that have not yet traded), which moves variance from the overnight piece to the session piece. Because both estimators add the two pieces, the total is roughly preserved; Parkinson, Garman-Klass and Rogers-Satchell would instead absorb part of the gap. Decide which price is "the open" (auction price or first trade) and keep it fixed.
- **Missing bars and holidays.** A holiday has no bar; the next close-to-close return spans more calendar time and counts as one observation. Under the trading-day convention (section 15) that is intended.
- **Special sessions.** A one-hour session (the Diwali Muhurat session in India) or a half day (US early closes) produces a full daily bar with a small range. In a 20-day window it pulls every estimator down a little. Flag such days; drop them or merge them into the neighbouring day.

### Intraday realised variance (sections 8 to 11)

- **Running value.** Today's realised variance is a sum that grows by one squared return each time a bar closes: one addition per bar. A rolling window ("the last 60 minutes", "the last 375 trading minutes") adds the newest squared return and drops the oldest. Bipower variation needs the previous bar's absolute return as well; MedRV the previous two.
- **History needed at start-up.** For today's figure: every bar since today's open, back-filled, otherwise the figure is short. For an $n$-day figure: $n$ days of intraday bars (20 days of one-minute NSE bars is 7,500 bars), or stored daily totals. For the time-of-day profile (section 13): several weeks of intraday bars.
- **A part-finished day.** The sum so far covers only the session so far. Three ways to turn it into a comparable number:
  1. Scale by the clock: multiply by (session minutes / minutes elapsed). Wrong whenever volatility is not flat through the day: +58% after the first hour in Table 10.
  2. Scale by the profile: divide by the share of a day's variance that normally arrives by that time (section 13). Right on average (Table 10).
  3. Use a trailing window exactly one session long, reaching back into yesterday. It always contains each time of day once, so it needs no profile. It must say whether the overnight return is inside it.
- **Bad ticks.** A false print followed by a return to the true price gives two huge squared returns. Bar closes are affected only if the false print is the last trade in a bar. Bipower variation, MinRV and MedRV do not protect against this pattern, because the two large returns are next to each other. Filter ticks before building bars.
- **Missing bars.** If returns are taken between consecutive *available* prices, a gap is harmless for realised variance: the longer return's square stands in for the missing ones. Forward-filling prices gives the same total. But the zeros that forward-filling creates pull bipower variation, MinRV and MedRV down.
- **The opening.** Decide whether the first intraday return starts at today's open (the gap is then outside the sum and handled as in section 12) or at yesterday's close (the gap is inside the sum as one very large squared return). The first minutes after the open carry the widest spreads and the most noise.
- **Session length.** Scaling a part day needs the true length of today's session: 375 minutes on NSE, 390 in the US, 210 on a US half day, 60 for Muhurat.

### EWMA (section 7)

- **Running value.** One number, updated once per close: $\sigma^2_t = \lambda\,\sigma^2_{t-1} + (1-\lambda)\,r_t^2$.
- **History needed at start-up.** The weight on everything older than $K$ days is $\lambda^K$. With $\lambda=0.94$: 1% is left after 74 days, 0.1% after 112 days. Seed the recursion with a sample variance and run it over at least 74 days of history before trusting it. The effective sample is $(1+\lambda)/(1-\lambda)=32$ days and the half-life $\ln 0.5/\ln 0.94 = 11.2$ days.
- **A part-finished day.** Updating with today's return so far understates, as for close-to-close. Update at the close.
- **Bad ticks.** A false close enters with weight $1-\lambda = 6\%$ and decays at 6% a day: it is still a third of its first size after 18 days.
- **Drift.** The recursion assumes zero mean; under a strong trend it reads high (Table 1, column B).

## 17. Which estimator for which job

Based on the papers above and on the two practitioner books. Bennett's appendix was read in full; Sinclair's chapter only in excerpts of the first edition (see section 19).

| Estimator | Data needed | Best use | Main weakness |
| --- | --- | --- | --- |
| Close-to-close, mean removed | Closes | Positional windows, 20 to 60 days and longer. The benchmark, and the figure to compare with variance swaps or a book hedged at the close (Bennett p. 240). Best for large samples (Bennett p. 239) | Noisy: about 16% standard error at 20 days. Needs at least 5 observations and ideally 20 or more (Bennett pp. 239-240). Slow to react |
| Close-to-close, zero mean | Closes | Same. Saves one observation; the practitioner default (Bennett p. 234, RiskMetrics) | Reads high in a strong trend (Table 4) |
| Parkinson | High, low | A market with no gap and little drift, when only high and low exist | Ignores the gap; reads high in trends; reads low when highs and lows are sampled. Dominated by Garman-Klass whenever the open and close are available |
| Garman-Klass | Open, high, low, close | A few days to a few weeks on a market with no gap (crypto, near-24-hour futures) | Ignores the gap; mild upward bias in trends; reads low on sampled highs and lows |
| Rogers-Satchell | Open, high, low, close | As Garman-Klass when the market is trending | Ignores the gap; slightly less accurate than Garman-Klass without drift |
| GKYZ | Open, high, low, close, previous close | A few days to a few weeks on a market that shuts overnight; works on one day | Mild upward bias in trends |
| Yang-Zhang | The same, at least 2 days | A few days to a few weeks on a market that shuts overnight (NSE, US). The best range estimator for small samples (Bennett p. 239). The only one free of both drift and gap | Reads low on sampled highs and lows; depends on a clean opening price; its headline efficiency of 14 is a best case |
| EWMA, 0.94 | Closes | A "current" daily volatility that moves smoothly and has no window drop-off | Zero-mean; the decay factor is a convention, not an estimate; a shock lingers for weeks; Bennett (p. 237) calls it rarely used |
| Realised variance, 5-minute, plus the overnight term | Intraday bars, previous close | Intraday monitoring; one-day and few-day realised volatility. One day of it is worth about 75 days of daily squared returns | Needs clean intraday data, a rule for the overnight gap (section 12), and a time-of-day profile for a part day (section 13) |
| Subsampled realised variance, two-scales, kernels, pre-averaging | Ticks or one-second data | Only if sampling faster than a few minutes, or on an illiquid, noisy instrument | Complexity and tuning; gains over 5-minute realised variance are small (Liu, Patton and Sheppard 2015) |
| Bipower variation, MedRV, MinRV | Intraday bars | Splitting a day's move into ordinary volatility and jumps; a figure that is not inflated by one news spike | Jumps leak through at coarse sampling (Table 8); zero returns and bounce-back bad ticks distort them |
| Realised range | Intraday bars with their own high and low | The accuracy of one-minute realised variance from 5-minute bars | The divisor depends on how many ticks are in each bar; noise biases it upward |

**Three practitioner cautions** (Bennett p. 239-241):

1. The efficiency numbers are theoretical maxima for an ideal random walk. On real data the gain is much smaller.
2. Range estimators read low on real data because trading is discrete (Table 3 shows how much).
3. Close-to-close is the definition used by variance swaps, so it is the one to show next to implied volatility when the comparison has to be exact.

**From Sinclair, first edition, as far as read:** Parkinson is about five times as efficient as close-to-close and biased low under discrete sampling and a part-day market; Garman-Klass up to eight times with a worse bias; Rogers-Satchell is the better choice under drift; Yang-Zhang can be 14 times as efficient in some simulations but is no better than close-to-close if opening jumps dominate. His volatility cone (the range of realised volatility seen historically at each window length, against which today's figure is placed) is in his pp. 39-43; how he builds it was not read.

## 18. Where well-known secondary sources and libraries disagree with the papers

| # | Source | What it says | What the paper says | Which is right |
| --- | --- | --- | --- | --- |
| 1 | Bennett (2014), Figure 142, p. 239 | Rogers-Satchell efficiency 8 | Variance $0.331\sigma^4$ against $2\sigma^4$: efficiency 6.0 (Rogers and Satchell 1991, eq. 4). Simulation 5.9 | The paper |
| 2 | Bennett Figure 142; Sinclair | Yang-Zhang efficiency 14 | 14 is the peak, at $n=2$ days and one particular gap size; the "typical" figure in the paper is 7.3 at $n=10$ | Both, read carefully: 14 is a maximum. Simulation at 20 days: 7.5 |
| 3 | Garman and Klass (1980); Bennett; most web pages | Parkinson efficiency 5.2 | Parkinson's own figures give $2/0.41 = 4.9$; the exact value from the moments of the range is 4.91 | 4.9. Simulation 4.85. The difference is immaterial |
| 4 | Bennett p. 242 | Zero-drift close-to-close keeps the divisor $N-1$ | With no mean removed the unbiased divisor is $N$ | $N$. Bennett's form is high by $N/(N-1)$, 5% of variance at 20 days |
| 5 | R TTR `volatility(calc="close", mean0=TRUE)` | Sum of $n-1$ squared returns divided by $n-2$ | As row 4 | High by $(n-1)/(n-2)$: 12.5% of variance at its default $n=10$ |
| 6 | R TTR | Default $N=260$ periods a year | No paper sets this; convention is 252 | Pass $N$ explicitly |
| 7 | Python `volatility-trading` `YangZhang.py` (and copies of it) | Close-to-close squared returns in place of open-to-close; no mean removed; all three sums over $n-1$ | Yang and Zhang eq. (7)-(9) | The paper. The library reads 5% to 15% high in variance (Table 1) and is not drift-independent |
| 8 | The same file before its issue #16 | $k = 0.34/(1+\frac{n+1}{n-1})$ | $k = 0.34/(1.34+\frac{n+1}{n-1})$, eq. (18) | The paper. Fixed in the library since |
| 9 | Rust `scirs2-series` documentation | $k$ "typically 0.34"; formula adds Rogers-Satchell with weight 1 | 0.34 is $\alpha-1$; $k$ is about 0.12 to 0.145; weight on Rogers-Satchell is $1-k$ | The paper |
| 10 | "Garman-Klass Yang-Zhang" as a named estimator (TTR, Bennett p. 243, web pages) | $o^2 + \tfrac12(u-d)^2 - (2\ln2-1)c^2$ | Yang and Zhang eq. (4) has the idea with Garman-Klass's exact coefficients; the half-and-0.386 version is in neither paper | Both forms are sound and agree to within 0.2% in simulation. The name is a later label |
| 11 | R `highfrequency` `rBPCov` | Bipower variation with no $M/(M-1)$ factor | Barndorff-Nielsen and Shephard (2004) also have none | They agree. Papers and code that add the factor differ from both by about $1/M$ |
| 12 | R `highfrequency` `rTSCov` | Counts prices, not returns, as $n$; default $K=300$ | Zhang et al. count returns; $K=cn^{2/3}$ | Immaterial for large $n$; the default $K$ is not a recommendation |
| 13 | R `highfrequency` `rKernelCov` | Defaults: rectangular kernel, one lag, lag terms rescaled by $N/(N-h)$ | Barndorff-Nielsen et al. (2008) use smooth kernels and a chosen bandwidth, no rescaling | The defaults are not the paper's estimator; set the kernel and bandwidth explicitly |
| 14 | The CME-hosted copy of Garman and Klass | After eq. (19): efficiency of "$\hat\sigma_3^2$" is 7.4 | It means $\hat\sigma_4^2$ ($\hat\sigma_3^2$ is 6.2, eq. 6) | A slip in that copy |
| 15 | Sinclair (1st ed.), Table 2.3, as extracted | Parkinson bias 0.92 at 200 transactions | Garman and Klass Table 1: 0.89 at 200, 0.92 at 500 | Probably the paper; Sinclair was seen only as an excerpt, so this is not certain |

One further observation from the simulation, not a disagreement between sources: Rogers and Satchell's correction for sampled highs and lows (their eq. 5) recovers most of the shortfall but not all of it (Table 3), whereas their own small simulation (400 runs) could not tell it from exact.

## 19. What could not be confirmed

1. **Hansen and Lunde (2005).** Primary text not reached. The three whole-day estimators and the optimal weights are taken from three later papers that restate them identically, plus the abstract. Equation numbers, their own estimate of the overnight share for Dow Jones stocks, and their recommendation are unconfirmed.
2. **Sinclair, *Volatility Trading*.** Second edition (2013) not reached. First edition (2008) seen only as excerpts. Unconfirmed: his lists of good and bad points per estimator, his advice on which to use and on sample size, how he builds the volatility cone, and whether he prints a GKYZ formula.
3. **Journal equation numbers** for papers read only as working papers: Barndorff-Nielsen and Shephard (2002) and (2004); Barndorff-Nielsen, Hansen, Lunde and Shephard (2008) and (2009); Andersen, Dobrev and Schaumburg (2012); Martens and van Dijk (2007); Boudt, Croux and Laurent (2011). The formulas themselves were read.
4. **Rogers and Satchell (1991).** Read in the authors' typescript; the journal's own page refused access, so the equation numbers are the typescript's. Rogers, Satchell and Yoon (1994): only the abstract and eq. (1)-(9) were legible.
5. **Garman and Klass (1980).** Read in the authors' updated re-typeset copy, not the 1980 journal pages.
6. **The $M/(M-1)$ factor on bipower variation.** Not traced to a paper.
7. **Taylor and Xu (1997), eq. (14).** Constants reconstructed from a garbled scan.
8. **The part-day scaling rule** ($RV$ so far divided by the usual share). A derivation from Andersen and Bollerslev's model; no paper was found that states it. Confirmed by simulation only.
9. **The $c_4$ constant.** Textbook result, cited from a secondary source; confirmed by simulation.
10. **Overnight share of variance for NIFTY, BANKNIFTY, SENSEX.** No source found. Must be measured.
11. **Ahoniemi and Lanne.** Working paper read, not the published article; table labels inferred.
12. **Evidence on the intraday shape** (Wood, McInish and Ord; Harris; the two Indian studies): abstracts or citations only.
13. **Calendars.** NSE holiday lists for 2019, 2020, 2023 and 2024 were counted from index history, not read from circulars; 2026 is from secondary copies. NYSE early-close dates before 2026 are rule-derived. CME hours were not read on the exchange's own page. MCX circulars were read on mirrors.
14. **Deribit.** No explicit statement of the year length in its option pricing was found; the 365-day basis is inferred from its DVOL article.
15. **The whole of section 16** is engineering reasoning, not sourced findings.
16. **Section 17's recommendations** rest on Bennett and the papers; no study comparing these estimators on Indian index data was looked for.

## 20. Sources

Primary papers. "Read at" is the copy actually read.

1. Parkinson, M. (1980). The Extreme Value Method for Estimating the Variance of the Rate of Return. *Journal of Business* 53(1), 61-65. https://www.jstor.org/stable/2352357 . Read at http://mmquant.net/wp-content/uploads/2016/08/michael_parkinson.pdf
2. Garman, M. B. and Klass, M. J. (1980). On the Estimation of Security Price Volatilities from Historical Data. *Journal of Business* 53(1), 67-78. https://doi.org/10.1086/296072 . Read at https://www.cmegroup.com/trading/fx/files/a_estimation_of_security_price.pdf
3. Rogers, L. C. G. and Satchell, S. E. (1991). Estimating Variance from High, Low and Closing Prices. *Annals of Applied Probability* 1(4), 504-512. https://doi.org/10.1214/aoap/1177005835 . Read at https://www.skokholm.co.uk/wp-content/uploads/2016/01/R_Satchell_HLOC.pdf
4. Rogers, L. C. G., Satchell, S. E. and Yoon, Y. (1994). Estimating the volatility of stock prices: a comparison of methods that use high and low prices. *Applied Financial Economics* 4(3), 241-247. https://doi.org/10.1080/758526905 . Read at https://www.skokholm.co.uk/wp-content/uploads/2016/01/RS_Yoon0.pdf
5. Yang, D. and Zhang, Q. (2000). Drift-Independent Volatility Estimation Based on High, Low, Open, and Close Prices. *Journal of Business* 73(3), 477-491. https://doi.org/10.1086/209650 . Read at https://atmif.com/papers/range.pdf
6. J.P. Morgan/Reuters (1996). *RiskMetrics Technical Document*, 4th edition. Read at http://www.phy.pmf.unizg.hr/~bp/TD4ePt_2.pdf
7. Andersen, T. G. and Bollerslev, T. (1998). Answering the Skeptics: Yes, Standard Volatility Models Do Provide Accurate Forecasts. *International Economic Review* 39(4), 885-905. Read at https://faculty.washington.edu/ezivot/econ589//////AndersenBollerslevIER1998.pdf
8. Andersen, T. G., Bollerslev, T., Diebold, F. X. and Labys, P. (2001). The Distribution of Realized Exchange Rate Volatility. *Journal of the American Statistical Association* 96(453), 42-55. Read at https://public.econ.duke.edu/~boller/Published_Papers/jasa_01.pdf and (working paper) https://finance.martinsewell.com/stylized-facts/volatility/Andersen-etal2001b.pdf
9. Andersen, T. G., Bollerslev, T., Diebold, F. X. and Labys, P. (2003). Modeling and Forecasting Realized Volatility. *Econometrica* 71(2), 579-625. Read at https://www.sas.upenn.edu/~fdiebold/papers/paper43/abdl4.pdf
10. Barndorff-Nielsen, O. E. and Shephard, N. (2002). Econometric analysis of realized volatility and its use in estimating stochastic volatility models. *Journal of the Royal Statistical Society B* 64(2), 253-280. Read (working paper) at https://www.nuff.ox.ac.uk/economics/papers/2001/w4/realised.pdf
11. Andersen, T. G., Bollerslev, T., Diebold, F. X. and Labys, P. (2000). Great realizations. *Risk* 13(3), 105-108. Read at https://public.econ.duke.edu/~boller/Published_Papers/risk_00.pdf
12. Liu, L. Y., Patton, A. J. and Sheppard, K. (2015). Does anything beat 5-minute RV? A comparison of realized measures across multiple asset classes. *Journal of Econometrics* 187(1), 293-311. Read at https://public.econ.duke.edu/~ap172/Liu_Patton_Sheppard_JoE_2015.pdf
13. Zhang, L., Mykland, P. A. and Aït-Sahalia, Y. (2005). A Tale of Two Time Scales: Determining Integrated Volatility With Noisy High-Frequency Data. *Journal of the American Statistical Association* 100(472), 1394-1411. Read at https://www.princeton.edu/~yacine/twoscales.pdf (this address returned "not found" later the same day)
14. Barndorff-Nielsen, O. E., Hansen, P. R., Lunde, A. and Shephard, N. (2008). Designing realized kernels to measure the ex post variation of equity prices in the presence of noise. *Econometrica* 76(6), 1481-1536. Read (working paper) at https://public.econ.duke.edu/~get/browse/courses/201/spr11/DOWNLOADS/WorkingPapers_Now_Published/BNHS-realised3-2008.pdf
15. Barndorff-Nielsen, O. E., Hansen, P. R., Lunde, A. and Shephard, N. (2009). Realized kernels in practice: trades and quotes. *Econometrics Journal* 12(3), C1-C32. Read (preprint) at https://public.econ.duke.edu/~get/browse/courses/201/spr11/DOWNLOADS/MicroStructure/bhls_kernels_practice_08.pdf
16. Jacod, J., Li, Y., Mykland, P. A., Podolskij, M. and Vetter, M. (2009). Microstructure noise in the continuous case: the pre-averaging approach. *Stochastic Processes and their Applications* 119(7), 2249-2276. Read at https://public.econ.duke.edu/~get/browse/courses/201/spr11/DOWNLOADS/MicroStructure/jlmpv_preav_spa_09.pdf
17. Barndorff-Nielsen, O. E. and Shephard, N. (2004). Power and Bipower Variation with Stochastic Volatility and Jumps. *Journal of Financial Econometrics* 2(1), 1-37. Read (working paper) at https://www.nuff.ox.ac.uk/economics/papers/2003/w18/eric.pdf
18. Andersen, T. G., Bollerslev, T. and Diebold, F. X. (2007). Roughing It Up: Including Jump Components in the Measurement, Modeling, and Forecasting of Return Volatility. *Review of Economics and Statistics* 89(4), 701-720. Read at https://public.econ.duke.edu/~boller/Published_Papers/restat_07.pdf
19. Andersen, T. G., Dobrev, D. and Schaumburg, E. (2012). Jump-robust volatility estimation using nearest neighbor truncation. *Journal of Econometrics* 169(1), 75-93. Read (NBER Working Paper 15533) at https://www.nber.org/system/files/working_papers/w15533/w15533.pdf
20. Christensen, K. and Podolskij, M. (2007). Realized range-based estimation of integrated variance. *Journal of Econometrics* 141(2), 323-349. Read at https://public.econ.duke.edu/~get/browse/courses/201/spr11/DOWNLOADS/MicroStructure/cp_range_rv_joe_07.pdf
21. Martens, M. and van Dijk, D. (2007). Measuring volatility with the realized range. *Journal of Econometrics* 138(1), 181-207. Read (Econometric Institute Report 2006-10) at https://repub.eur.nl/pub/7582/ei2006-10.pdf
22. Hansen, P. R. and Lunde, A. (2005). A realized variance for the whole day based on intermittent high-frequency data. *Journal of Financial Econometrics* 3(4), 525-554. https://doi.org/10.1093/jjfinec/nbi028 . Abstract only: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=531422
23. Ahoniemi, K. and Lanne, M. (2010). Realized volatility and overnight returns. Bank of Finland Research Discussion Paper 19/2010 (published as Overnight stock returns and realized volatility, *International Journal of Forecasting* 29(4), 592-604, 2013). Read at https://www.econstor.eu/bitstream/10419/212176/1/bof-rdp2010-019.pdf
24. Andersen, T. G. and Bollerslev, T. (1997). Intraday periodicity and volatility persistence in financial markets. *Journal of Empirical Finance* 4(2-3), 115-158. Read at https://public.econ.duke.edu/~boller/Published_Papers/joef_97.pdf
25. Taylor, S. J. and Xu, X. (1997). The incremental volatility information in one million foreign exchange quotations. *Journal of Empirical Finance* 4(4), 317-340. Read (excerpts) at https://finance.martinsewell.com/stylized-facts/dependence/TaylorXu1997.pdf
26. Boudt, K., Croux, C. and Laurent, S. (2011). Robust estimation of intraweek periodicity in volatility and jump detection. *Journal of Empirical Finance* 18(2), 353-367. Read (working paper) at https://lirias.kuleuven.be/retrieve/95a6deda-7f4d-49f1-8270-55936fb5cc69
27. French, K. R. and Roll, R. (1986). Stock return variances: the arrival of information and the reaction of traders. *Journal of Financial Economics* 17(1), 5-26. Abstract at https://authors.library.caltech.edu/records/y0dmc-gap67
28. Wood, R. A., McInish, T. H. and Ord, J. K. (1985). An investigation of transactions data for NYSE stocks. *Journal of Finance* 40(3), 723-739. https://ideas.repec.org/r/bla/jfinan/v40y1985i3p723-39.html . Harris, L. (1986). A transaction data study of weekly and intradaily patterns in stock returns. *Journal of Financial Economics* 16(1), 99-117. https://ideas.repec.org/a/eee/jfinec/v16y1986i1p99-117.html
29. Singh and Gangwar (2018). MPRA Paper 89689 (NIFTY futures, one-minute data). https://mpra.ub.uni-muenchen.de/89689/ . Agarwalla, S. K. and Pandey, A. (2012). IIM Ahmedabad working paper. https://www.iima.ac.in/publication/whether-cross-listing-stock-specific-and-market-wide-calendar-events-impact-intraday

Practitioner books.

30. Bennett, C. (2014). *Trading Volatility: Trading Volatility, Correlation, Term Structure and Skew*. Appendix A.2, pp. 232-244. https://www.trading-volatility.com/Trading-Volatility.pdf
31. Sinclair, E. (2008; 2nd ed. 2013). *Volatility Trading*. Wiley. Chapter 2. First edition read in excerpts only.

Statistics.

32. "Unbiased estimation of standard deviation", Wikipedia, citing Bolch, B. W. (1968), More on unbiased estimation of the standard deviation, *The American Statistician* 22(3), 27. https://en.wikipedia.org/wiki/Unbiased_estimation_of_standard_deviation

Implementations checked.

33. TTR (R), `volatility()`. https://github.com/joshuaulrich/TTR/blob/master/R/volatility.R
34. volatility-trading (Python), `YangZhang.py` and `GarmanKlass.py`. https://github.com/jasonstrimpel/volatility-trading/tree/master/volatility/models . Issue 16: https://github.com/jasonstrimpel/volatility-trading/issues/16
35. qf-lib (Python), `DriftIndependentVolatility`. https://qf-lib.readthedocs.io/en/latest/_modules/qf_lib/common/utils/volatility/drift_independent_volatility.html
36. scirs2-series (Rust), `yang_zhang_volatility`. https://docs.rs/scirs2-series/latest/scirs2_series/financial/volatility/estimators/fn.yang_zhang_volatility.html
37. highfrequency (R) 1.0.2, `rRVar`, `rBPCov`, `rMinRVar`, `rMedRVar`, `rTSCov`, `rKernelCov`. https://github.com/jonathancornelissen/highfrequency

Exchanges and index methodologies.

38. Cboe, *Volatility Index Mathematics Methodology*. https://cdn.cboe.com/resources/indices/Cboe_Volatility_Index_Mathematics_Methodology.pdf
39. NSE, *India VIX white paper*. https://nsearchives.nseindia.com/web/sites/default/files/inline-files/white_paper_IndiaVIX.pdf
40. Deribit, DVOL article. https://insights.deribit.com/exchange-updates/dvol-deribit-implied-volatility-index/
41. NSE market timings https://www.nseindia.com/market-data/market-timings ; pre-open session https://www.nseindia.com/products-services/equity-market-pre-open ; holidays https://www.nseindia.com/resources/exchange-communication-holidays ; holiday circulars for 2021, 2022, 2025: https://archives.nseindia.com/content/circulars/CMTR46623.pdf , https://archives.nseindia.com/content/circulars/CMTR50560.pdf , https://nsearchives.nseindia.com/content/circulars/CMTR65587.pdf
42. NYSE hours and calendars. https://www.nyse.com/markets/hours-calendars
43. Cboe SPX options specifications. https://www.cboe.com/tradable_products/sp_500/spx_options/specifications/
44. MCX trading hours. https://www.mcxindia.com/market-operations/trading-surveillance
45. BSE index derivatives contract specifications. https://beta.bseindia.com/static/markets/Derivatives/DeriReports/contractindex.aspx


