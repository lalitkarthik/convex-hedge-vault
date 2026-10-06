# Long-gamma research brief: SPXW 0DTE, minute quotes, 127 days

## 1. Method

**Start from a mechanism, not a correlation scan.** The academic papers that hold up say first who is mispricing what and why, and only then test it. Examples: Muravyev and Ni argue that options are priced as if variance arrived evenly by the clock ([SSRN 2820264](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2820264)). Baltussen et al. argue that short-gamma hedgers must trade with the trend ([JFE 2021](https://pure.eur.nl/en/publications/hedging-demand-and-market-intraday-momentum/)). Scanning features for correlation with 127 days will find false positives. The current Greek-ratio plots are circular. Theta/gamma, vega/theta and delta/gamma are fixed functions of implied vol, time and moneyness. Plotting them against ATM implied vol plots implied vol against itself. Rolling and lead-lag correlations of these trending series then produce spurious patterns.

**Target variable.** The standard target is the delta-hedged option gain over a fixed window. This goes back to Bakshi and Kapadia (2003, RFS) (not verified). Vilkov reports strategy P&L as a percentage of the underlying, net of half-spread plus slippage ([0DTE Trading Rules, GitHub annotated paper](https://github.com/vilkovgr/0dte-strategies/blob/main/docs/paper/paper-annotated.md)). For us, the target should be:

- buy the ATM straddle at the ask at time A;
- hedge with the synthetic forward using the desk's band rule, paying the quoted spreads;
- sell at the bid at time B, or settle;
- record P&L divided by spot, and separately the window's realised variance minus implied variance.

**Guards against false discovery.**
- **Harvey, Liu and Zhu:** after decades of data mining, a new factor needs t > 3.0, not 2.0 ([RFS 2016, SSRN 2513152](https://papers.ssrn.com/abstract=2513152)).
- **Bailey and López de Prado, deflated Sharpe ratio:** corrects the Sharpe ratio for the number of trials and for skew and kurtosis. The same paper gives a minimum track record length ([SSRN 2460551](https://papers.ssrn.com/abstract=2460551)).
- **Probability of backtest overfitting** (Bailey, Borwein, López de Prado, Zhu): combinatorially symmetric cross-validation over all variants tried ([SSRN 2326253](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253), not verified).
- **Walk-forward testing:** Vilkov's conditional rules re-fit on a rolling 252-day window and are scored only out of sample ([GitHub](https://github.com/vilkovgr/0dte-strategies/blob/main/docs/paper/paper-annotated.md)).

**How many days you need.** The Sharpe-ratio standard error is from Lo (2002) and Mertens (2002), as used in Bailey and López de Prado ([PSR explainer](https://portfoliooptimizer.io/blog/the-probabilistic-sharpe-ratio-bias-adjustment-confidence-intervals-hypothesis-testing-and-minimum-track-record-length/)):

SE(SR) ≈ √[(1 − γ₃·SR + (γ₄−1)/4·SR²) / (T−1)], with SR the daily Sharpe ratio, γ₃ skew and γ₄ kurtosis.

This gives the minimum days T ≈ 1 + (1 − γ₃·SR + (γ₄−1)/4·SR²)·(z/SR)².

Worked numbers (my arithmetic):
- **Smallest detectable Sharpe with T = 127.** Under normal returns, significance at z = 1.96 needs a daily SR of 1.96/√127 = 0.174. That is an annualised Sharpe of **2.76**. At the Harvey-Liu-Zhu bar of t = 3, it is **4.2**.
- **Days needed for an annualised Sharpe of 1.** Daily SR is 0.063, so normal returns need about 970 days. A short straddle with γ₃ = −3 and γ₄ = 20 needs about 1,170 days. A long straddle with γ₃ = +3 needs about 800 days.
- **Effective sample size.** Many entry minutes per day are not independent. The effective sample is about 127 days, and event days are only about 4 FOMC, 6 CPI and 6 payroll days (not verified). Treat the 127 days as a place to find hypotheses. Confirming them needs data the desk does not have yet.

## 2. When is long gamma paid, intraday?

**Day against night.** Muravyev and Ni, SPX delta-hedged options, 2004–2013 ([CXO summary](https://www.cxoadvisory.com/equity-options/intraday-versus-overnight-option-returns/), [JFE](https://ideas.repec.org/a/eee/jfinec/v136y2020i1p219-238.html)):
- the total is −0.7% per day: −1.0% close-to-open and **+0.3% open-to-close**;
- intraday gains concentrate in the afternoon;
- options under 3 weeks: −2.6% overnight, +0.07% intraday;
- the overnight strategy is "limited due to bid-ask spreads".

Their mechanism is that options are priced as if noon and midnight carried equal risk, while daytime risk is about 2.5 times higher ([SUFE summary](https://academicnewsletter.sufe.edu.cn/info/355741)).

Follow-ups:
- Jones and Shemesh find option returns are much lower over non-trading periods, mostly weekends ([JF 2018](https://ideas.repec.org/a/bla/jfinan/v73y2018i2p861-900.html)).
- NIFTY replicates the pattern: sellers earn overnight and lose intraday ([Bhat, Pandey, Rao, JFM 2024](https://ideas.repec.org/a/wly/jfutmk/v44y2024i8p1320-1337.html)).
- A blog says the split reproduces on SPXW through 2025 at bid/ask ([FirmTape](https://firmtape.com/research/what-the-0dte-literature-claims), unreviewed).

**What this means for us.** A 0DTE contract has no night. The night-premium mechanism therefore does not transfer directly. What does transfer is the clock-time against variance-time mismatch inside the session.

**0DTE studies.**

| Study | Sample | Finding |
|---|---|---|
| Vilkov | 09/2016–01/2026 ([SSRN 4641356](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4641356), [GitHub](https://github.com/vilkovgr/0dte-strategies/blob/main/docs/paper/paper-annotated.md)) | 0DTE VRP is positive and significant but tiny: median from 10:00 to close ≈ **0.0011% of underlying**. ATM–OTM long options lose on average. Short OTM wins in up to 75% of days. Realised skewness explains P&L more than variance. |
| Almeida and Hizmeri | ([Tinbergen abstract](https://tinbergen.nl/event/2025/11/06/13089/0dte-asset-pricing)) | High VRP, mostly **upside** risk. Strategy profits held through 2022 and faded after daily expiries began. |
| Chong | 2020–2024 ([SSRN 4933153](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4933153)) | 0DTE options are "expensive but not mispriced" after costs. |
| Beckmeyer, Branger, Gayda | 02/2021–02/2023 ([SSRN 4404704](https://ssrn.com/abstract=4404704)) | Retail lost $184k per day on average, rising to **$358k per day** after May 2022. |
| Bandi, Fusari, Renò | ([SSRN 4503344](https://econbiz.de/Record/0dte-option-pricing-bandi-federico/10014348685)) | A short-time expansion that prices the 0DTE smile. It is a pricing model; I found no trading result in it. |
| Dim, Eraker, Vilkov | 2024 ([summary](https://harbourfrontquant.substack.com/p/the-rise-of-0dte-options-cause-for)) | High 0DTE open-interest gamma goes with **lower** intraday vol. No propagation. |
| Adams et al. | ([SSRN 5641974](https://quantpedia.com/do-sp500-0dtes-options-increase-market-volatility/)) | About **−60 bp annualised** vol on 0DTE days. Stronger order-flow reversals and weaker momentum. |
| Cboe | May 2025 ([Cboe](https://www.cboe.com/insights/posts/0-dt-es-decoded-positioning-trends-and-market-impact)) | Customer flow is "extremely balanced". Market-maker hedging is at most 0.2% of SPX liquidity. |
| FlashAlpha (blog with data) | 193 Wednesdays, 07/2022–04/2026 ([link](https://flashalpha.com/articles/are-0dte-straddles-overpriced-193-spy-sessions-data-study)) | Median realised/implied move 0.589 against a fair value of 0.674, so about 13% rich. The close stayed inside 1σ 71% of the time against 68.3%. |

I could not identify the Adams, Fontaine and Ornthanalai paper exactly. The SSRN 5641974 paper by "Adams et al." is the likely match (not verified).

**Scheduled-event days.**
- Wright, weekly options the night before the event: VRP is "large and significantly positive, especially for FOMC days". Event straddles are over-priced on average ([NBER w28306](https://www.nber.org/papers/w28306)).
- Pre-FOMC 0DTE implied uncertainty builds from 10:00 to 14:00 and forecasts realised vol after the announcement, not before it ([Song, SSRN 7412318](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7412318), abstract only).
- FOMC 0DTE straddles price about 2× neighbouring weeks, and the market "largely respected" that ([FlashAlpha](https://flashalpha.com/articles/are-0dte-straddles-overpriced-193-spy-sessions-data-study)).
- CPI against this: SPX 1-day straddles were overpriced on only 4 of 12 CPI reports, against a norm of about 60% ([Nasdaq](https://www.nasdaq.com/articles/ndx-straddle-buyers-love-cpi-day-volatility), not verified).

**Intraday VRP and the U-shape.** Realised variance is U-shaped across the session, with a midday lull. About 70% of daily variance falls in session hours ([Moontower](https://moontowermeta.com/pricing-0dtes/)). If quotes decay time value by the clock, midday options are rich and last-hour options are cheap. Moontower gives one worked example. I found no peer-reviewed curve of 0DTE VRP by minute. There is a paper on VIX1D's mechanical "overnight bias" ([FRL 2024](https://www.sciencedirect.com/science/article/pii/S1544612324002162), not opened). **We can measure this curve ourselves. It is the most direct test available.**

**Intraday momentum.**
- Gao, Han, Li, Zhou, SPY 1993–2013: the first half-hour return predicts the last half-hour. It is stronger on volatile and news days ([JFE 2018](https://profiles.wustl.edu/en/publications/market-intraday-momentum/)).
- Baltussen et al., 60+ futures 1974–2020: the effect is tied to short-gamma hedging demand ([JFE 2021](https://pure.eur.nl/en/publications/hedging-demand-and-market-intraday-momentum/)).
- After 2022: Adams et al. find dealers are net long gamma from rolled positions, which mutes momentum. Zarattini, Aziz and Barbon report a net Sharpe of 1.33 for 2007–early 2024 from a breakout trend rule on SPY ([SSRN 4824172](https://ssrn.com/abstract=4824172)). The evidence is mixed. Momentum is weaker on average but survives in breakout form.

**Evidence against long gamma.** Every 0DTE study above finds implied above realised on average. Long ATM options lose on average, and retail buyers lose heavily. The one consistent long-gamma result, Muravyev and Ni's positive intraday returns, is gross of spreads, comes from multi-day options and predates 2014.

## 3. Features we can build

| Feature | Evidence | Note |
|---|---|---|
| Time of day | **Strong** | Muravyev and Ni; U-shape |
| Prior-days RV, HAR forecast against straddle-implied | **Strong** for forecasting RV, **weak** for RV − IV | Corsi HAR (not verified). Low against high RV split is reported as the biggest conditioner, with after-cost Sharpe 0.40–0.47 against 0.00–0.08, via a secondary source ([FirmTape](https://firmtape.com/research/what-the-0dte-literature-claims)) |
| First-30-min RV against implied | **Moderate** | Vol clustering is strong. Morning vol signals carry t = 5.6 and R² 2.6%, 2006–2022, using VVIX ([Hizmeri](https://tinbergen.nl/event/2025/11/20/13054/early-birds-get-the-vol-morning-volatility-uncertainty-and-variance-risk-premium)) |
| Overnight gap | **Weak** | Enters through the first half-hour return (Gao et al.) |
| ATM IV level | **Weak** | VIX-tercile heterogeneity, statistically weak (Vilkov) |
| IV change after the open | **Weak** | By analogy with the VVIX timing result |
| Skew level and change | **Weak** | Realised skew drives P&L, but predicting it is open (Vilkov) |
| Event calendar | **Strong** for RV, **mixed** for RV − IV | Wright; Song |
| Day of week | **Folklore** | Mostly the event calendar in disguise |
| Greek ratios | **None beyond IV and time** | Identities |

**Features needing data we lack:**
- **Open-interest gamma:** documented but modest. A 2026 thesis finds the hedging channel adds no QLIKE improvement ([Princeton](https://theses-dissertations.princeton.edu/entities/publication/61115cd1-cb09-4a8b-9230-ff488fc2a386)).
- **VIX1D:** largely the same information as our 0DTE implied vol.
- **Volume and order flow:** reversals in Adams et al., and the retail-flow papers. Probably the most valuable missing input.

## 4. Long-gamma strategy shapes

**Gamma scalping with a band.** The Whalley–Wilmott band is optimal under proportional costs, with half-width growing in cost and gamma as a cube root. Zakamouline adds fixed costs ([Zakamouline](https://econwpa.ub.uni-muenchen.de/econ-wp/fin/papers/0311/0311009.pdf); [W–W 1997](https://ideas.repec.org/a/bla/mathfi/v7y1997i3p307-324.html)). Sinclair's books cover the practitioner side (not verified).

The key point is that hedged P&L ≈ ½Γ·Σ(ΔS between re-hedges)². The band therefore picks the scale at which variance is harvested:
- **Tight band:** pays if the price mean-reverts at that scale (variance ratio < 1).
- **Wide band, or letting delta run:** pays in a trend.

So the band choice is a bet on trend against mean reversion ([practitioner discussion](https://www.elitetrader.com/et/threads/managing-deltas-hedging-frequency.326612/post-4753555), weak source). It ties to dealer positioning: long-gamma dealers produce reversals and short-gamma dealers produce momentum. What kills it is spread cost on each re-hedge and midday chop paid against theta.

**Unhedged straddle or strangle with a time stop.**
- It is held to the close and pays only if |move| > premium (≈0.8σ).
- Fair odds of that are about 42%. At FlashAlpha's 13% overpricing, my arithmetic gives about 36%.
- Pay-off is strongly right-skewed. Vilkov finds negative median P&L and insignificant means.
- What kills it is the VRP plus the spread.

**Long wings financed by a short body, or backspreads.** The evidence is against this:
- OTM 0DTE options are rich, especially calls (Almeida and Hizmeri).
- Call ratio spreads are "unattractive".
- Put ratio spreads, the opposite shape (short wing), earn a net Sharpe of 0.93 out of sample ([Vilkov](https://github.com/vilkovgr/0dte-strategies/blob/main/docs/paper/paper-annotated.md)).

**Long straddle after the morning crush.** Folklore. Profitable Option Alpha users sell at about 10:15 and close after noon ([Option Alpha](https://optionalpha.com/blog/0dte-options-strategy-performance); survivor-selected). This hints at a cheap afternoon but proves nothing.

**Event-morning straddle.** Wright finds event VRP positive, so it loses on average. CPI may be the exception. Song suggests timing should end before the release, because implied uncertainty peaks at 14:00 on FOMC days.

## 5. Short gamma, briefly

**Conditioners:**
- enter after the open (about 10:00–10:15);
- skip high-RV regimes and event days;
- prefer low-VIX for call-side and high-VIX for put-side structures;
- use a logistic model on 10:00 signals: net straddle or strangle Sharpe 0.39, iron fly −0.20 ([Vilkov](https://github.com/vilkovgr/0dte-strategies/blob/main/docs/paper/paper-annotated.md)).

Option Alpha win rates are 72% for iron flies and 63% for condors, from a survivor-biased sample.

**Tail:**
- Vilkov's 1% expected shortfall is 0.58–1.58% of the underlying per day.
- On 9 April 2025, the 10:00 straddle priced a 3.51% move. SPY closed **+8.72%**, about 2.5× the implied move ([FlashAlpha](https://flashalpha.com/articles/are-0dte-straddles-overpriced-193-spy-sessions-data-study)).

## 6. NIFTY

**VRP.** It is positive and priced, from synthetic variance swaps ([Sankar et al. 2020](https://ideas.repec.org/a/eee/reveco/v70y2020icp321-334.html)). It is earned overnight, and short NIFTY options lose intraday ([Bhat et al. 2024](https://ideas.repec.org/a/wly/jfutmk/v44y2024i8p1320-1337.html)). A 1-minute study covers 887 days, 2022–2026 ([Agarwal, SSRN 6530119](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6530119), abstract only).

**Expiry day.**
- 59% of index-option turnover was on expiry day in FY26, down from 70% in FY25.
- 87.7% of individual traders lost money ([SEBI FY26 via Finnovate](https://www.finnovate.in/learn/blog/sebi-fno-trader-losses-fy26-individual-derivatives)).
- SEBI's July 2025 Jane Street order describes expiry-day index pushing ([Oxford blog](https://blogs.law.ox.ac.uk/oblb/blog-post/2025/07/jane-street-and-expiry-day-trap-unpacking-sebis-crackdown-algorithmic)).
- Weekly expiry is now a single NIFTY weekly on Tuesday (not verified).

**Costs from 1 April 2026** ([Zerodha](https://zerodha.com/charges); [5paisa](https://www.5paisa.com/news/stt-hike-on-fo-to-take-effect-from-april-1-amid-rising-options-activity)):

| Item | Charge |
|---|---|
| STT on options | 0.15% of premium on the sell side; 0.15% of intrinsic value if exercised |
| STT on futures | **0.05% of notional on the sell side** |
| NSE options charge | 0.0355% of premium |
| Stamp duty | 0.003% |
| GST | 18% on fees |

Each futures hedge sale costs 0.05% of notional, about 12 index points at NIFTY 25,000 (my arithmetic; level not verified). That is a large share of an expiry-day ATM straddle. **Futures-hedged scalping is close to uneconomic. Hedge with option legs, where STT applies only to premium, and close before expiry rather than paying STT on exercise.**

## Five hypotheses to test, ranked

1. On all non-event days, a long hedged ATM straddle from 14:30 to 16:00 earns more than its spread cost, because quotes run time value down by the clock while realised variance spikes in the last hour (Muravyev–Ni afternoon gains, U-shape).
2. On days when 09:30–10:00 realised variance from minute forwards exceeds the 10:00 implied variance rate by a set threshold, a long hedged ATM straddle from 10:00 to 16:00 earns more than its spread cost, because intraday vol clusters and quotes under-react to the morning.
3. On days when the 10:00 straddle-implied variance is below a HAR forecast scaled to the rest of the session, a long hedged ATM straddle from 10:00 to 16:00 earns more than its spread cost, because implied vol lags shifts in the realised-vol regime.
4. On days when the first-hour variance ratio of minute returns is above 1, a long ATM straddle from 10:30 to 16:00 hedged with a wide band of half the implied move earns more than its spread cost, because trending days pay long gamma at coarse scales and tight bands give that up.
5. On non-event days, a short hedged ATM straddle from 11:30 to 13:30 earns more than its spread cost, because clock-time decay overprices the midday variance lull. This is the mirror image of hypothesis 1 and a check on it.
