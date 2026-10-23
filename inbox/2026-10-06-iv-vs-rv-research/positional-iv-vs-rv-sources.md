# Positional IV vs RV: findings and sources

## The two open questions

1. **Past prices.** Back-fill daily index data from a broker, or keep our own candles for longer?
2. **30-day IV.** We subscribe only to expiries 0 to 7 days out (0 to 1 for SPXW), so no 30-day IV can be built. Subscribe to further expiries, use India VIX, or stay with weekly IV?

## 1. How positional RV is calculated

- **Method:** take daily candles over a window, apply an estimator, scale by √252.
- **Window:** match it to the IV's horizon. A one-month IV sits against one-month RV, about 21 trading days.
  - Montréal Exchange, "Trading Volatility Using Historical Volatility Cones", describing Burghardt and Lane 1990: https://www.m-x.ca/f_publications_en/cone_vol_en.pdf
  - Bennett, *Trading Volatility*, p. 234: https://www.trading-volatility.com/Trading-Volatility.pdf
- **Estimator:** Yang-Zhang handles both overnight gaps and trends. In our simulation the simpler range methods (Parkinson, Garman-Klass, Rogers-Satchell) read 25% low when a quarter of the movement was overnight; Yang-Zhang stayed within 0.5%.
  - Yang and Zhang 2000, eq. 7 to 11 and 18: https://atmif.com/papers/range.pdf
  - Parkinson 1980: http://mmquant.net/wp-content/uploads/2016/08/michael_parkinson.pdf
  - Garman and Klass 1980 (authors' re-typeset copy): https://www.cmegroup.com/trading/fx/files/a_estimation_of_security_price.pdf
  - Rogers and Satchell 1991 (authors' typescript): https://www.skokholm.co.uk/wp-content/uploads/2016/01/R_Satchell_HLOC.pdf
- **Standard reference calculation:** 21 trading days, 252 a year, mean taken as zero.
  - Cboe Realized Volatility Index methodology: https://cdn.cboe.com/resources/indices/documents/RVOL_Methodology.pdf (Cboe retired these indices in January 2025; the document still defines the calculation.)

### The formulas

```
r_i = ln(C_i / C_(i-1))        volatility = sqrt(252 * var)

Close-to-close    var = 1/(n-1) * sum (r_i - mean r)^2
Parkinson         var = 1/(4 n ln2) * sum ln(H_i/L_i)^2
Garman-Klass      var = 1/n * sum [ 0.5 ln(H_i/L_i)^2 - (2 ln2 - 1) ln(C_i/O_i)^2 ]
Rogers-Satchell   var = 1/n * sum [ ln(H_i/C_i) ln(H_i/O_i) + ln(L_i/C_i) ln(L_i/O_i) ]
Yang-Zhang        var = var_overnight + k * var_open_to_close + (1-k) * var_RS
                  k = 0.34 / (1.34 + (n+1)/(n-1))
```

### What this means for the back-fill question

A 21-day RV needs 21 daily candles plus the close before them. Keeping our own candles for longer only works from today forward. A chart with months of past RV needs past daily prices from somewhere else. This is reasoning from the formulas, not a quoted source.

What the engine has today: one-minute index candles for the last 30 sessions, stored since 30 September 2026; no daily candle; no back-fill. The Fyers adapter fetches option candles only and Upstox has no candle mode.

## 2. Which IV is used for 30 days

| Approach | How | Who uses it | Source |
|---|---|---|---|
| Constant-maturity ATM IV | Blend the two expiries either side of 30 days, by total variance | AlgoTest (7, 21, 30 or 90 days), Market Chameleon (IV30) | Cboe VIX methodology, "Constant Maturity Term": https://cdn.cboe.com/resources/indices/Cboe_Volatility_Index_Mathematics_Methodology.pdf ; AlgoTest: https://docs.algotest.in/clicktrade/strategy-builder/vrp-analysis-tool/ |
| VIX-style index | Uses the whole strip of out-of-the-money options, no pricing model | Cboe VIX, India VIX | NSE India VIX white paper: https://nsearchives.nseindia.com/web/sites/default/files/inline-files/white_paper_IndiaVIX.pdf |
| Nearest monthly expiry | Take the expiry 30 or more days out as it is | Barchart (second-hand) | None read directly |

The blending formula, for two expiries at times T1 < T* < T2 with variances s1² and s2²:

```
s* = sqrt( (1/T*) * [ T1*s1² * (T2 - T*)/(T2 - T1)  +  T2*s2² * (T* - T1)/(T2 - T1) ] )
```

Checked by recomputing the Cboe white paper's worked example: the formula gives 13.686, the paper prints 13.69.

Two facts about India VIX:

- It is built from near-month and next-month NIFTY options, counts time in calendar minutes, and rolls with 3 trading days left.
- It reads higher than ATM IV whenever there is a skew, because it includes the far strikes. So "India VIX minus RV" overstates what a straddle seller earns. Source: Demeterfi, Derman, Kamal and Zou, "More Than You Ever Wanted to Know About Volatility Swaps", Goldman Sachs 1999, eq. 31 (read from a saved copy, no link recorded).
- There is no SENSEX equivalent that the engine takes in, and the engine has no India VIX or VIX feed.

## 3. Two ways to line the two up

- **Trailing:** IV on a date against RV over the days before it. Different periods; answers "are options priced above how the market has been moving?" Available on the day.
- **What followed:** IV on a date against RV over the days after it. Same period; answers "was the forecast right?" Available only once the period is over, so it needs saved IV history.

## 4. How Indian products present it

- **AlgoTest:** IV and RV at the same horizon, four RV estimators, and a switch that shifts RV to sit under the IV that forecast it.
  - https://docs.algotest.in/clicktrade/strategy-builder/vrp-analysis-tool/
  - https://algotest.in/blog/iv-vs-rv-and-trading-edge-with-vrp/
- **Quantsapp:** RV shifted forward 20 days by default; IV rank and percentile over 250 days.
  - https://web.quantsapp.com/quantsapp-classroom/Volatility/futures-realized-volatility-&-stock-trading
  - https://web.quantsapp.com/quantsapp-classroom/Volatility/IV-With-IVR-&-IVP
- **Opstra:** IV, HV and a spread line on daily candles. Methods not documented.
  - https://www.definedgesecurities.com/user-manuals/opstra-user-guide/
- **Sensibull:** nearest-expiry ATM IV with an IV percentile; no RV shown.
  - https://blog.sensibull.com/2018/11/25/how-high-is-high-the-iv-percentile/
- **Fyers:** no public IV-vs-RV view. Its Options Analytics screen charts ATM IV for one expiry against price and the ATM straddle.

Definitions, since products mix the names:

- **IV rank** = (today's IV − lowest in the lookback) ÷ (highest − lowest) × 100.
- **IV percentile** = share of days in the lookback on which IV was below today's.
- Market Chameleon's "% Rank" is a percentile; tastylive says its IV Rank is sometimes called IV Percentile.

## 5. How big the gap usually is

- **S&P 500, 1996 to 2003:** realised 18.8 against ATM implied 21.3, in volatility points. Carr and Wu, "Variance Risk Premiums": https://ideas.repec.org/a/oup/rfinst/v22y2009i3p1311-1341..html (figures from the 2004 draft; the published paper uses a longer sample).
- **Indices generally:** implied runs 1 to 2 points above what is then realised. Bennett, p. 15.
- **NIFTY, August 2022 to March 2026:** implied minus realised averaged +1.2 points and was positive on 75% of days. Agarwal, SSRN: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6530119 . Low trust: one author, not peer-reviewed, abstract only.

## 6. What was not confirmed

- Burghardt and Lane 1990 (the volatility cone) was read only through the Montréal Exchange paper.
- Garman-Klass and Rogers-Satchell were read in the authors' own copies, not the journal pages.
- Opstra's IV and HV methods, and Sensibull's percentile lookback, are not public.
- No peer-reviewed figure exists for the NIFTY gap or for NIFTY's overnight share of movement.
- NSE and BSE expiry-day rules came from news reports, not the circulars.

## Open these four first

1. AlgoTest VRP tool docs: the closest existing product to what we would build.
2. NSE India VIX white paper: how NSE builds a 30-day figure.
3. Cboe VIX methodology: the blending formula.
4. Yang and Zhang 2000: the RV estimator.
