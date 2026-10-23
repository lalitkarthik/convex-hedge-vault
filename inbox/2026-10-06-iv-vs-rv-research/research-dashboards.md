promoted: 2026-10-23
# How existing products show implied volatility against realised volatility

Research note for the Convex Hedge IV-vs-RV dashboard feature. Written 6 October 2026.
Scope: what each product plots and what it calls things. RV formulas in depth and horizon-matching
theory are covered by other notes; here they appear only as far as each product states them.

## How to read this note

- **Implied volatility (IV)** is the yearly price swing that option prices imply, given as a percentage.
  It looks forward.
- **Realised volatility (RV)**, also called **historical volatility (HV)**, is the yearly price swing the
  underlying actually showed over a past window. It looks backward.
- **ATM** (at the money) means the option strike closest to the current price.
- **Expiry** is the date an option ends. The **front expiry** is the nearest one.
- **Constant maturity** means a figure always measured for the same number of days ahead (say 30),
  made by blending the two expiries either side of that point. **Interpolation** is that blending.
- **Annualisation** turns a daily swing into a yearly one by multiplying by the square root of the
  number of periods in a year: 252 if you count trading days, 365 if you count calendar days.
- **Trailing RV** is plotted on the day the window ends ("the last 20 days, shown today").
  **Forward-shifted RV** is plotted on the day the window starts, so it sits next to the IV that tried
  to forecast it.
- **Primary source** means the product's own documentation. Where a fact comes only from a search-engine
  summary or a third party, the note says so with "(secondary)". Where nothing public exists, it says
  **not documented**.

A practical limit: this machine's DNS failed for parts of the session. Barchart's pages render only in a
browser and could not be read directly, Schwab and SpotGamma returned "forbidden", and the Opstra
volatility video sits behind a login. Facts for those products are marked secondary.

---

## 1. Product by product

### 1.1 Fyers (India) — the team's reference

Full screen description is in section 6. Summary:

- **Which IV.** Option chain: one IV per strike and expiry, taken from the out-of-the-money (OTM) option
  and computed against the futures price, shown on both the call and the put side [1]. Options
  Analytics: an **ATM IV** chart for a chosen expiry, whose ATM strike moves as the price moves [2].
  Not constant maturity, not a VIX-style index.
- **Which RV.** None. No public Fyers page mentions historical or realised volatility, IV rank or IV
  percentile [2][3][4][5].
- **Layout.** ATM IV line over time, with underlying price, ATM strike and ATM straddle value
  (ATM call price plus ATM put price) on the same chart [2]. A separate multi-strike IV chart [3].
- **Intraday.** Yes. Resolutions 1, 5, 15, 30 minutes and 1 hour (secondary: search summary of the same
  help article) [2]. The FIA insights panel refreshes every 60 seconds [6].
- **Derived numbers.** None of IV rank, IV percentile or IV–RV. FIA insights mentions "market-implied
  move information", without a formula [6].
- **Controls.** Underlying, expiry, range, resolution [2].
- **API.** The option-chain API did not return IV as of May 2025; Fyers staff said it would come in
  "upcoming enhancements" [7].

### 1.2 Sensibull (India; also powers the option chain on Zerodha Kite)

- **Which IV.** Black-76 model on futures prices (Black-76 is the Black-Scholes variant for options on
  futures). One OTM-derived IV per strike, applied to call and put [8]. Charts show the **ATM strike IV**.
  In automatic mode the nearest expiry is used, but **on expiry day the chart switches to the next
  expiry**, "because IV values grow very large when there are only a few hours left to expiry" [9].
- **Which RV.** Not documented. Sensibull's IVP article mentions "mean HV" only in passing [10].
- **Layout.** ATM IV line chart; live (intraday) charts were announced in January 2023 [9]. Before that a
  user reported IV charts were end-of-day only (2020) [11].
- **Derived numbers.** **IVP (IV percentile):** "the percentage of time that the IV in the past has been
  lower than current IV", 0 to 100, high above 80, low below 20 [10]. A Sensibull staff member said it is
  "the standard IV percentile plus some level of proprietary stuff … to reduce noise" [12]. Lookback is
  not stated by Sensibull; a 250-day ATM-IV lookback appears only in secondary summaries. Sensibull warns
  IVP "is not reliable for next month's options" [9].
- **Controls.** Expiry (manual or auto), strike [9].

### 1.3 Opstra by Definedge (India)

- **Which IV.** Not documented (strike, expiry or constant maturity not stated) [13][14].
- **Which RV.** "Historical Volatility"; window and estimator not documented [13][14].
- **Layout.** "Daily candlestick charts on the EOD timeframe along with line charts of IV, Historical
  Volatility, and IV-RV spread. It has an intraday line chart as well." [13][14] So: price candles, IV and
  HV as two lines, plus a spread line. A training video on the IV–RV spread exists but is behind a login [15].
- **Other views.** Volatility surface and heatmap of OTM IV across four expiries; a volatility-skew table
  with "VS Percentile"; an options dashboard listing IV, IVR and IVP for every F&O stock with a
  "High IVP" filter [14].
- **Intraday.** EOD and intraday IV charts [16].
- **Definitions of IVR/IVP.** Not documented.

### 1.4 Quantsapp (India)

- **Which IV.** Not documented in public pages. Its embeddable IV chart shows "historical IV plotted with
  Future Prices & key range-based data like IV Rank & Percentile" [17].
- **Which RV.** **FRV, "future realized volatility"**: the standard deviation of returns over the 20 days
  *after* the date. "FRV data series leads by 20 days, as compared to HV." [18] This is the only Indian
  product found that plots **forward-shifted RV** by default.
- **Layout.** Lines; Nifty in orange, FRV in blue [18].
- **Derived numbers.** **IVR** = (current IV − IV low) / (IV high − IV low) × 100 over 250 trading days.
  **IVP** = (days IV was lower than today / 250) × 100 [19].

### 1.5 AlgoTest (India) — VRP Analysis Tool

- **Which IV.** Constant-maturity IV at 7, 21, 30 or 90 days, chosen by the user [20].
- **Which RV.** Window matched to the IV horizon (30-day IV pairs with 30-day RV). Estimators offered:
  "Integrated" (recommended), Parkinson, Garman-Klass, Yang-Zhang [20]. (Parkinson, Garman-Klass and
  Yang-Zhang are range-based estimators that use the day's high and low as well as the close.)
- **Layout.** Two lines on one time axis, IV blue and RV red; plus a table of how often VRP was positive
  or negative and its average, bucketed by IV percentile (0–10, 10–20 … 90–100) [20][21].
- **Shift.** A **"Lag RV" toggle** that "aligns prediction dates (IV) with outcome dates (RV)" [20].
- **Derived numbers.** **VRP = IV − RV**, in volatility points [21].
- **Controls.** Underlying (NIFTY, BANKNIFTY…), IV maturity, RV window, estimator, lag toggle [20].

### 1.6 StockMojo (India; found while searching, not on the brief)

- NIFTY "IV, HV, RV" chart that refreshes every minute in market hours; HV range default 1 month;
  IVP/IVR lookback default 252 sessions; IVR is placed between the 52-week low (0%) and high (100%) [22].
  It treats **HV** (past window) and **RV** ("what price is doing right now") as separate lines [22].
  Which IV strike/expiry: not documented.

### 1.7 Zerodha, Upstox, Dhan, StockMock

- Zerodha's Kite option chain is powered by Sensibull (secondary) [23]; see 1.2. Streak: nothing found.
- Upstox, Dhan, StockMock: **not documented**. No public help page describing an IV-vs-HV chart was found.

### 1.8 NSE India VIX

- **Which IV.** A VIX-style **model-free** index: a weighted strip of OTM NIFTY option prices, not an ATM IV.
  Uses best bid-ask quotes of **near and next month** NIFTY options; "expected market volatility over the
  next 30 calendar days" [24]. Details in section 5.
- **Which RV.** None published by NSE.

### 1.9 TradingView

- **Built-in "Historical Volatility".** TradingView's help page gives only a concept description (dispersion
  of returns, "often … standard deviation"); it states no window or annualisation [25]. The built-in's
  defaults could not be confirmed from a primary source (see the unconfirmed list).
- **Popular community script, "IV vs Realised Volatility (VIX/HV Comparator)".** IV comes from a
  user-chosen volatility index (CBOE:VIX for SPX, NSEINDIA:INDIAVIX for Nifty). HV over a chosen number of
  bars (example 20), annualised with user-set trading days per year and hours per day. Orange IV line,
  aqua HV line, fill green when IV > HV and red when HV > IV; optional sub-panel with the IV/HV ratio and
  guide lines at 1.2 and 0.8; a label showing IV, HV and the difference [26]. Note it compares a
  **30-day model-free index** with a **trailing N-bar HV** — the horizons match only if N is about 21
  trading days.

### 1.10 Market Chameleon (US)

- **Which IV.** **IV30**: "30-day constant maturity Implied Volatility" [27][28].
- **Which RV.** **HV20** (20 trading days) and **HV52wk** (one year) [28]. Its learning page describes
  both close-to-close and an OHLC (Yang-Zhang) estimator [29]; which one feeds HV20 is not stated.
- **Layout.** IV30 against HV20 on one time chart [27]; IV term-structure view on the same IV page [30];
  rankings tables [28].
- **Derived numbers — note the naming.** "**IV30 % Rank**" is defined as "the number of days out of the
  past year that had a LOWER 30-day implied volatility than the current value", which is what most
  products call **IV percentile**. "**IV30 52-Week Position**" is where IV sits between the 52-week high
  and low, which most products call **IV rank** [28].

### 1.11 Barchart (US) — secondary only (pages need a browser)

- **Which IV.** "the average implied volatility (IV) of the nearest monthly options contract that is 30-days
  out or more" (secondary) [31]. Barchart also publishes an "IV Index", a weighted average of near-the-money
  IVs that "straddle constant maturities" (secondary) [31].
- **Which RV.** 30-day historic volatility (secondary) [31].
- **Layout.** "IV vs HV" column = 30-day IV minus 30-day HV; an "Implied Volatility vs Realized Volatility"
  screener ranks symbols by the IV/HV ratio (secondary) [31][32]; a volatility term-structure chart [31].
- **Derived numbers.** **IV Rank**: ATM average IV relative to its 1-year high and low. **IV Percentile**:
  "the percentage of days where implied volatility closed below the current ATM IV over the past 1-year"
  (secondary, search-engine extract of Barchart's page) [33].

### 1.12 ORATS (US)

- **Which IV.** `iv30d` and siblings: "constant maturity implied volatility … calculated by measuring the
  two expirations around the day to be measured" (30, 60, 90 days, 6 months, 1 year). Also **ex-earnings
  IV**, with "earnings effects taken out" [34].
- **Which RV.** `orHv` (1, 5, 10, 20, 60-day…): "calculated from intraday open-high-low-close stock price
  market information"; `clsHv`: close-to-close; both also published **ex-earnings**, with "the day of and
  day after earnings taken out" [34][35].
- **Derived numbers.** `ivHvXernRatio` = ex-earnings 30-day IV ÷ 20-observation HV [34][36]. **IV
  percentile**: sort all observations and place today's reading in the list (worked example in the docs)
  [34]. Forward implied vol between two dates; implied earnings move [34]. IV rank: field exists
  (`ivRank1m`, `ivRank1y`), definition not found in the page read.
- **Layout.** Data-first (API and research tables); chart layout not documented.

### 1.13 IVolatility (US)

- **Which IV.** **IVX (IV Index)**: four ATM options per expiry, weighted by delta and vega, "normalized
  to fixed tenors (30, 60, 90, 120, 150, 180 days) using a linear interpolation by the squared root of
  time"; call, put and mean versions [37][38].
- **Which RV.** Close-to-close HV; Parkinson and Garman-Klass are also described in its education pages
  [37][39].
- **Layout.** 30-day IVX and HV as two lines on one chart; the text notes IVX moves tend to
  anticipate HV by about a month [38].

### 1.14 Cboe (US)

- **IV.** VIX: model-free, 30-day constant maturity from SPX and weekly SPXW options, published about
  every 15 seconds [40][41]. Outline in section 5.
- **RV indices (now ceased).** Cboe Realized Volatility Index series: **RVOL** (21 trading days),
  **RVOL3M** (63), **RVOL6M** (126), **RVOL12M** (252). Price is an implied spot from put-call parity at
  4:00 p.m. ET; daily log returns; **mean set to zero**; annualised with **√252**; one closing value a day
  [42]. Cboe **ceased these indices from 27 January 2025** [43].

### 1.15 Interactive Brokers (TWS)

- **Which IV.** "The IB 30-day volatility is the at-market volatility estimated for a maturity thirty
  calendar days forward of the current trading day, and is based on option prices from two consecutive
  expiration months." [44]
- **Which RV.** "30-day historical volatility (currently for stocks)" [44]; estimator not documented.
- **Layout.** Volatility Lab, Implied Volatility tab: IV history for all expiries, Volatility Profile
  ("the Historical and Implied readings of volatility side-by-side, over time"), multi-expiry skew,
  time-lapse skew. The plot "defaults to the 30-day reading of both implied and historical volatility
  plotted against the share price" [45].
- **Derived numbers.** IV Percentile, IV Rank, HV Percentile, HV Rank, each for **13, 26 and 52 weeks**
  [46]. Definitions in section 5.

### 1.16 thinkorswim (Schwab) — secondary only

- Shows "IV Percentile" and "HV Percentile" on the Today's Options Statistics sub-tab (secondary; Schwab
  page refused access) [47]. Community sources claim the platform's "IV Percentile" is computed as a
  range position (that is, what others call rank) — **unconfirmed** [48].

### 1.17 tastytrade / tastylive

- **Which IV.** "IV Index", described as a VIX-style IV for one underlying (secondary) [49].
- **Derived numbers.** **IV Rank**: where current IV sits in its past-year range; example: range 30–60,
  current 45, rank 50% [50]. tastylive itself says "IVR … may at times also be referred to as IV
  Percentile" [50]. RV display: not documented.
- **Expected move**: IV-based and straddle-based formulas (section 5) [51][52].

### 1.18 OptionStrat

- Shows IV rank and IV percentile in its builder (secondary) [53]. Definitions and any HV display:
  **not documented**.

### 1.19 SpotGamma (same-day / 0DTE)

- **"Implied 1-Day Move"**: a proprietary one-standard-deviation range for the next day, "not a simple
  formula derived from implied volatility" but based on historical datasets; SpotGamma reports SPX
  closing inside it on 76% of days (secondary: support page refused direct access) [54]. No documented
  intraday implied-versus-realised move chart was found.

### 1.20 Deribit (crypto)

- **Which IV.** **DVOL**: 30-day, VIX-style, from the two expiries either side of 30 days, with a
  one-hour EMA smoothing (outline in section 5) [55].
- **Which RV.** API endpoint `public/get_historical_volatility` returns timestamp–value pairs; the docs
  give no window, sampling or annualisation [56]. **Not documented.**

### 1.21 Amberdata (crypto)

- **Which IV.** ATM IV at constant maturities 7, 30, 60, 90 and 180 days to expiry [57].
- **Which RV.** "close-to-close realized volatility using hourly data" for **7-day and 30-day** windows
  [57]. Annualisation not stated.
- **Layout.** Implied-vs-realised endpoint and a volatility-cones page [57][58].

### 1.22 Laevitas (crypto)

- Charts: historical ATM IV, realised volatility, "Implied Volatility vs Realized Volatility", ATM IV term
  structure and time-lapse term structure, IV term structure by strike and by delta, volatility cone [59].
- **RV**: "Annualised standard deviation of daily (log) returns calculated from a data set over a
  specified fixed period of time" [60].
- **Cone**: credits Burghardt; example table with windows 7D to 365D, 25th/50th/75th percentiles and a
  "Current" column [61]. History length and IV overlay not stated.

### 1.23 Volmex (crypto)

- **IV.** BVIV / EVIV: 30-day forward-looking, model-free (variance-swap replication), consolidated across
  venues, exponentially smoothed [62][63].
- **RV.** **VRV indices** (e.g. BVRV30D, BVRV7D): daily non-overlapping log returns, sum of squares
  (zero mean), annualised with **365/n** (calendar days) [64]. A separate family uses an EWMA of
  one-minute squared returns, refreshed every minute [65].
- Layout: index pages per series; a dedicated IV-vs-RV chart was not found.

### 1.24 Greeks.live, Velo, Delta Exchange

- **Not documented.** Greeks.live posts commentary quoting "1-week realized volatility" against
  "month-end implied volatility" (secondary) [66] — itself an example of a horizon mismatch.

---

## 2. Comparison table

"ND" = not documented. "Sec." = secondary source only.

| Product | IV used | RV used (estimator, window, annualisation) | Layout | RV timing | Intraday | Derived numbers | Controls |
|---|---|---|---|---|---|---|---|
| Fyers | ATM IV of chosen expiry; strike floats | none | ATM IV + price + ATM strike + straddle on one chart; multi-strike IV | — | 1m–1h | none (implied-move text in FIA) | expiry, range, resolution |
| Sensibull | ATM IV, nearest expiry, next expiry on expiry day; Black-76 | ND | ATM IV line; IVP badge | — | yes since 2023 | IVP (proprietary smoothing) | expiry, strike |
| Opstra | ND | "HV", ND | candles + IV, HV, IV–RV spread lines; surface; skew table | trailing (assumed) | yes | IVR, IVP, VS percentile | ND |
| Quantsapp | ND | FRV: SD of next 20 days | lines, FRV shifted 20 days | **forward** | ND | IVR, IVP (250 days) | ND |
| AlgoTest | constant maturity 7/21/30/90d | Integrated / Parkinson / GK / YZ, window = IV horizon | two lines + VRP-by-IVP table | **lag toggle** | ND | VRP = IV − RV | underlying, maturity, estimator, lag |
| StockMojo | ND | HV and RV, HV default 1 month | IV, HV, RV lines | trailing | 1-minute refresh | IVP, IVR (252) | HV range, IVP range |
| India VIX | model-free 30 calendar days | — | index line | — | real time | — | — |
| TradingView script | user-chosen VIX index | N-bar close-to-close, user annualisation | two lines, coloured fill, ratio sub-panel | trailing | any bar size | IV−HV, IV/HV | all |
| Market Chameleon | IV30 constant maturity | HV20, HV52wk; C-C or YZ ND | lines; term structure; tables | trailing | ND | "% Rank" (= percentile), "52-Week Position" (= rank) | ND |
| Barchart (sec.) | nearest monthly ≥30 days | 30-day HV | screener tables, term structure | trailing | ND | IVR, IVP, IV−HV, IV/HV | ND |
| ORATS | iv30d etc., ex-earnings too | intraday OHLC and C-C, ex-earnings, 1–60+ days | data/API | trailing | ND | IV/HV ratio, IVP, forward IV, earnings move | API fields |
| IVolatility | IVX 30–180d, sqrt-time interpolation | C-C HV | IVX and HV lines | trailing | IVX intraday | ND | tenor |
| Cboe | VIX | RVOL 21/63/126/252 td, zero mean, √252 (ceased 2025) | separate indices | trailing | VIX ~15 s | — | — |
| IBKR | 30-day at-market IV, two expiries | 30-day HV, ND | Volatility Profile side by side; vs share price | trailing | ND | IVR, IVP, HVR, HVP (13/26/52 wk) | period |
| thinkorswim (sec.) | ND | ND | statistics tab | — | ND | "IV Percentile", "HV Percentile" | ND |
| tastytrade | IV Index (sec.) | ND | chain header | — | ND | IVR (also called IVP by tastylive), expected move | ND |
| SpotGamma (sec.) | proprietary | — | key-level number | — | daily | Implied 1-Day Move | — |
| Deribit | DVOL | API values, ND | index chart | ND | 1 s raw, EMA | — | — |
| Amberdata | ATM 7/30/60/90/180d | C-C on hourly data, 7d/30d | endpoint + cones | trailing | hourly | ND | tenor |
| Laevitas | ATM IV, term structure | SD of daily log returns | IV vs RV, cone, term structure | trailing | ND | ND | ND |
| Volmex | BVIV/EVIV 30d model-free | VRV daily, zero mean, 365/n; EWMA 1-min variant | index pages | trailing | 1-min (EWMA RV) | — | — |

---

## 3. Layout patterns

### Pattern A — two lines on one time axis (IV and RV)

Used by Opstra, Market Chameleon, IBKR Volatility Profile, IVolatility, AlgoTest, Laevitas, the
TradingView script [13][27][45][38][20][59][26].

- Good: shows regime and history at a glance; easy to read the gap.
- Bad: the gap is read by eye; two lines on different horizons look comparable when they are not;
  with trailing RV the "gap" mixes forecast and outcome from different periods.

### Pattern B — the gap as its own line (spread or ratio), often in a lower panel

Opstra's IV–RV spread, ORATS' IV/HV ratio, Barchart's IV vs HV and IV/HV screener, the TradingView
script's ratio panel [13][34][31][26].

- Good: one number to watch, easy to put bands on (the script uses 1.2 and 0.8 [26]).
- Bad: a ratio exaggerates when RV is tiny; a spread in volatility points is not the same as a variance
  premium (see section 5); neither shows whether both are high or both low.

### Pattern C — a rank or percentile badge, or a screener table

Sensibull IVP, tastytrade IVR, Barchart, Market Chameleon rankings, IBKR columns, Opstra dashboard
[10][50][33][28][46][14].

- Good: compact; good for scanning many underlyings.
- Bad: names conflict between products (section 4.2); a percentile of IV alone says nothing about RV.

### Pattern D — volatility cone with current IV overlaid, and term-structure views

Laevitas, Amberdata, the Montreal Exchange note on Burghardt and Lane [61][58][67]; term structure at
Market Chameleon, Barchart, Laevitas, IBKR [30][31][59][45].

- Good: matches horizons by construction; shows whether IV at each maturity is high for that horizon.
- Bad: a snapshot, not a time series; needs years of history; RV percentiles are wide at short horizons.

### Pattern E — intraday ATM IV with price and straddle (no RV)

Fyers Options Analytics, Sensibull live charts [2][9].

- Good: what a same-day trader watches: IV moving with price, straddle decay through the session.
- Bad: no realised comparison at all; ATM strike switches and expiry rolls create jumps.

### Who needs which

- **Watching intraday (incl. NIFTY/SENSEX weekly expiry day, SPX 0DTE).** Pattern E plus an *intraday*
  realised measure on the same clock (examples: Volmex's minute-level EWMA RV [65], Amberdata's
  hourly-based RV [57]), and the day's implied move against the move so far. Daily-close HV is of no use
  inside the session.
- **Holding for weeks.** Pattern A with matched horizons, Pattern B as a lower panel, a forward-shift
  ("lag") option like Quantsapp and AlgoTest to check past forecasts [18][20], Pattern C for context,
  and Pattern D to judge each maturity.

---

## 4. Common mistakes and misleading presentations

1. **Horizon mismatch.** Comparing 30-day IV with 10- or 20-day HV, or month-end IV with 1-week RV
   (Greeks.live commentary [66]). The Montreal Exchange note names this the main weakness of the
   simple IV-vs-HV comparison and says 1-month IV should meet 1-month HV, 3-month meet 3-month [67].
   AlgoTest forces the match [20]; Market Chameleon pairs IV30 with HV20 [27].
2. **Rank and percentile swapped.** Market Chameleon's "% Rank" is a percentile; its "52-Week Position"
   is a rank [28]. tastylive says its IVR may be called IV Percentile [50]. thinkorswim is reported to
   do the same (unconfirmed) [48]. Always show the formula on hover.
3. **Front-expiry sawtooth at roll.** An ATM IV of a fixed expiry jumps when the expiry rolls, and
   explodes in the last hours of expiry day. Sensibull switches to the next expiry on expiry day for this
   reason [9]; Fyers' ATM IV chart follows the selected expiry [2]. Constant-maturity IV (ORATS,
   IVolatility, IBKR, Market Chameleon, AlgoTest) avoids it [34][37][44][27][20].
4. **ATM strike switching.** A floating ATM strike jumps between strikes with different IVs (skew), so
   part of the line's movement is strike change, not volatility change. Fyers plots the ATM strike on
   the chart so this can be seen [2].
5. **Calendar versus trading days.** India VIX and Cboe VIX count minutes in a 365-day year [24][41];
   Cboe RVOL and the Montreal note annualise with 252 [42][67]; Volmex RV uses 365 [64]. Mixing them
   shifts a figure by √(365/252) ≈ 1.20, about 20%.
6. **Event inside IV but not yet in RV.** IV ahead of earnings, budgets, policy days or elections
   carries the event; trailing RV does not. ORATS publishes ex-earnings IV and HV for this [34].
7. **Trailing RV drawn as if it scored the forecast.** Trailing RV on day *t* measures the past; IV on day
   *t* forecasts the future. Only a forward shift compares forecast with outcome (Quantsapp FRV,
   AlgoTest lag) [18][20]. IVolatility notes IVX tends to lead HV by about a month [38].
8. **Model-free index treated as ATM IV.** VIX, India VIX, DVOL and BVIV weight a whole strip of OTM
   options [41][24][55][62]; an ATM IV uses one strike. *(Inference: with a downward-sloping skew a
   model-free index usually reads above ATM IV, so the two should not share a line unlabelled.)*
9. **Underlying used for IV.** Sensibull uses futures with Black-76 and contrasts this with NSE's fixed
   10% rate on spot [8]; Fyers also uses the futures price [1]. Two products can show different IVs for
   the same option.
10. **Zero mean versus sample mean in RV.** Cboe RVOL and Volmex VRV set the mean to zero [42][64]; the
    Montreal note subtracts the mean [67]. Small difference, but enough for a reconciliation failure.
11. **Spread in vol points called a variance premium.** Carr and Wu define the premium on *variance*,
    and as realised minus implied [68]; AlgoTest defines VRP as IV − RV in volatility points [21]. State
    sign and units.

---

## 5. Exact definitions

### 5.1 IV rank

- Formula: (current IV − lowest IV in lookback) ÷ (highest − lowest) × 100.
- Quantsapp: 250 trading days [19]. tastylive: past year [50]. IBKR: "where the implied volatility ranks
  between the selected period's high and low", 13/26/52 weeks [46]. Barchart: ATM average IV vs 1-year
  high and low (secondary) [33]. Market Chameleon calls this "52-Week Position" [28].

### 5.2 IV percentile

- Formula: share of days in the lookback with IV below today's.
- Quantsapp: (days lower ÷ 250) × 100 [19]. IBKR: "the percentage of days with implied volatility closing
  below the current implied volatility over the selected period" [46]. ORATS: rank today's value in the
  sorted list (their example gives 5/8 = 62.5%) [34]. Sensibull: "percentage of time that the IV in the
  past has been lower than current IV", plus proprietary smoothing [10][12]. Market Chameleon calls this
  "IV30 % Rank" [28].
- IBKR's published HV Percentile text says "historical volatility closing below the current implied
  volatility" [46] — probably a typo for "current historical volatility"; do not copy it.

### 5.3 Volatility cone (Burghardt and Lane, 1990)

- Source: G. Burghardt and M. Lane, "How to Tell if Options Are Cheap", *Journal of Portfolio
  Management*, Winter 1990 [67][69].
- Build: for several horizons (the Montreal example uses 1, 3, 6, 9, 12 months), compute rolling
  historical volatilities over history; for each horizon plot the maximum, minimum and middle values (or
  percentiles) against horizon. Short horizons give a wide spread, long horizons a narrow one, hence the
  cone. Then overlay current IV at the matching time to expiry, "typically … from at-the-money options".
  The Montreal example annualises with √252 [67]. Laevitas uses 7 to 365 days and 25/50/75th percentiles [61].

### 5.4 Variance risk premium

- Carr and Wu (2009): the difference between realised variance and the variance swap rate (the
  risk-neutral expected variance, replicated by a portfolio of options) [68]. In their sign convention
  it is usually negative.
- Product usage: AlgoTest "VRP = IV − RV" in volatility points [21]. ORATS uses an IV/HV ratio [34].

### 5.5 Expected move from IV

- One standard deviation over N days: price × (IV ÷ 100) × √(N ÷ 365) with calendar days, or
  √(N ÷ 252) with trading days (secondary: tastylive episode summary) [51].
- One day: the same with N = 1 (√(1/365) ≈ 1/19.1; √(1/252) ≈ 1/15.9).
- Straddle shortcut for events: 85% of the front-month ATM straddle, or (ATM straddle + first OTM
  strangle) ÷ 2 [52].
- SpotGamma's "Implied 1-Day Move" is proprietary, not this formula (secondary) [54].

### 5.6 India VIX (outline)

From NSE's white paper [24]:
- Options: OTM calls above and OTM puts below the ATM strike K0 of **near and next month** NIFTY options,
  bid-ask midpoints; strikes with spread above 30% of mid, or missing, are filled by a **natural cubic
  spline**.
- Forward: latest traded NIFTY futures price of each expiry month. K0 = strike just below it.
- Rate: NSE MIBOR of the relevant tenor (30 or 90 days).
- Time: minutes to expiry ÷ 525,600 (minutes in a 365-day year).
- Each month's variance by the Cboe VIX formula, then interpolated to 30 days (N30 = 43,200 minutes).
- Roll: with **3 trading days** left to near expiry it moves to next and far month.
- Caveat: the white paper's worked example uses old NIFTY levels; NSE's current page still describes near
  and next-month options [24]. Whether weekly expiries are now used was not confirmed.

### 5.7 Cboe VIX (outline)

From Cboe's methodology documents [40][41]:
- Universe: AM-settled SPX and PM-settled weekly SPXW options, excluding SPXW expiring the same day as
  SPX standard options.
- "Bracket method" with a 30-day constant maturity: a near term at or under 30 days and a next term
  after it.
- Forward from put-call parity at the strike with the smallest call–put price difference; K0 at or just
  below it; strikes included until two consecutive zero bids.
- Rates from US Treasury constant-maturity yields with a cubic spline.
- Variance per term from option prices weighted by 1/K²; interpolate in minutes to 30 days; ×365/30;
  square root; ×100.
- Published about four times a minute (every 15 seconds) [40].

### 5.8 Deribit DVOL (outline)

From Deribit's DVOL article [55]:
- Take the two expiries closest to 30 days, one each side; ignore instruments under one hour old.
- Price from order-book bid/ask; if the spread is too wide, use last-minute trades, else the mark price
  from a minute ago.
- Drop ITM options and far-OTM options with delta below 5%.
- Variance-swap formula per expiry; time-weighted interpolation to 30 days gives a raw value every
  second; DVOL = exponential moving average of the last 240 raw points.

---

## 6. Fyers in detail — what the reference screen actually shows

Everything here is from Fyers' public help centre and notices.

**Where it lives.** "Options → Analytics" on Fyers Web and App [70]. The app path for IV is "Options >
Tools > Analytics > Implied Volatility"; on web "Options > Analytics > Implied Volatility" [3]. Fyers
describes the area as putting "Open Interest, IV, Max Pain, and Futures data" together in one view [70].

**The analytics menu** (help-centre category list) [71]:
Futures Volume; Symbol vs Futures; Futures OI; Straddle/Strangle; Auto ATM Straddle; Multi-Strike IV;
ATM IV Chart; Time vs OI; Trending OI; Multi Strike OI; Historical PCR and Max Pain; OI Change; OI Drops;
OI Spurts; OI Interpretation.

**ATM IV Chart** [2] (help article last updated 25 September 2026):
- Shows "changes in At-The-Money (ATM) Implied Volatility (IV) alongside the underlying price over time".
- Series and tooltip fields: **ATM IV, Price, ATM Strike, ATM Straddle, timestamp**.
- "ATM strike updates automatically as the underlying price moves" — no manual strike choice.
- Controls: **Range, Resolution, Expiry**. Resolutions 1, 5, 15, 30 minutes, 1 hour (secondary
  extract of the same article).
- Analysis only; no order placement.
- No HV, RV, India VIX, IV rank or IV percentile.

**Multi-Strike IV** [3]: "compare how IV changes across multiple option strikes over time for a selected
underlying and expiry"; uses: ATM and OTM IV behaviour, skew changes, IV expansion or compression. Tips
mention adjusting resolution, narrowing the time window and reducing the number of strikes.

**Auto ATM Straddle** [72]: ATM call + ATM put premium over time with underlying price and **VWAP**
(volume-weighted average price) as a reference line; strike auto-adjusts; listed under "Combined Charts"
on web.

**Straddle/Strangle** [73]: user-chosen call and put strikes, several strategies compared, with spot and
VWAP, and Buy/Sell actions.

**Option chain** [1][4][5]: columns LTP, Bid/Ask, Volume, OI, OI Chg, Delta, Gamma, Theta, Vega, **IV**,
ITM Prob, Intrinsic Value, Time Value, Breakeven, plus PCR and Max Pain. One IV per strike from the OTM
side, against futures. Price, Greeks and Straddle views. IV and Greeks "may not refresh during weekends,
holidays, or after market hours".

**FIA Insights** [6]: swipeable cards, including "market-implied move information"; shortcuts to "OI, OI
Change, Max Pain, ATM IV, Multi Strike OI, and Multi Strike IV"; refreshes every 60 seconds.

**What this means for us.** Publicly, Fyers is an **intraday ATM-IV and straddle dashboard**, not an
IV-versus-RV dashboard. Names worth reusing: "ATM IV", "ATM Strike", "ATM Straddle", "Multi-Strike IV",
"Range", "Resolution", "Expiry". If the team remembers an IV-vs-HV view on Fyers, it is either behind
login or from another product (Opstra and AlgoTest are the Indian products that publicly document one).

---

## Sources

1. Fyers, "Why do the Call and Put options show the same IV in FYERS?" https://support.fyers.in/portal/en/kb/articles/why-do-the-call-and-put-options-show-the-same-iv-in-fyers
2. Fyers, "What is the ATM IV Chart in Options Analytics?" https://support.fyers.in/portal/en/kb/articles/what-is-the-atm-iv-chart-in-options-analytics
3. Fyers, "What is Multi-Strike IV in Options Analytics?" https://support.fyers.in/portal/en/kb/articles/what-is-multi-strike-iv-in-options-analytics
4. Fyers, "What do the different columns in the FYERS Options Chain mean?" https://support.fyers.in/portal/en/kb/articles/what-do-the-different-columns-in-the-fyers-options-chain-mean
5. Fyers, "Why is data missing or not updating in the FYERS Options Chain?" https://support.fyers.in/portal/en/kb/articles/why-is-data-missing-or-not-updating-in-the-fyers-options-chain
6. Fyers, "How can I use FIA Insights for options analysis on the FYERS App?" https://support.fyers.in/portal/en/kb/articles/how-can-i-use-fia-insights-for-options-analysis-on-the-fyers-app
7. Fyers Community, "When or how can I get IV data in option chain API?" (May 2025) https://fyers.in/community/questions-5gz5j8db/post/option-chain-api-Y5Tk5kdZLxPj9P6
8. Sensibull, "Why is the IV on NSE website different from Sensibull's IV?" https://sensibull.freshdesk.com/support/solutions/articles/43000115287-why-is-the-iv-on-nse-website-different-from-sensibull-s-iv-
9. Sensibull Blog, "Live Options Charts & Multi Straddle-Strangle Charts" (Jan 2023) https://blog.sensibull.com/2023/01/13/live-options-charts-multi-straddle-strangle-charts/
10. Sensibull Blog, "How high is high? The IV percentile" (Nov 2018) https://blog.sensibull.com/2018/11/25/how-high-is-high-the-iv-percentile/
11. Trading Q&A, "Live Options Straddle and IV chart" (Oct 2020) https://tradingqna.com/t/live-options-straddle-and-iv-chart/93105
12. Trading Q&A, "What is IV percentile in sensibull?" (Sensibull reply, Jul 2018) https://tradingqna.com/t/what-is-iv-percentile-in-sensibull/42148
13. Definedge, "OPSTRA Options Trading Terminal User Guide" https://www.definedgesecurities.com/user-manuals/opstra-user-guide/
14. Definedge, "New Feature Releases in OPSTRA Mobile App" https://www.definedgesecurities.com/new-features/new-feature-releases-in-opstra-mobile-app/
15. Definedge Insight, "Learn how to Trade Options by tracking IV & RV spread | E06" (login) https://insight.definedgesecurities.com/product-user-guide/opstra-analytics-and-trading-terminal/learn-how-to-trade-options-by-tracking-iv-rv-spread-episode-6/
16. Definedge, Opstra FAQs https://www.definedgesecurities.com/faqs/opstra/
17. Quantsapp, iframe docs, "Implied Volatility (IV) chart" https://iframe-doc.quantsapp.com/products/implied-volatility-iv-chart
18. Quantsapp Classroom, "Futures realized volatility & stock trading" https://web.quantsapp.com/quantsapp-classroom/Volatility/futures-realized-volatility-&-stock-trading
19. Quantsapp Classroom, "IV with IVR & IVP" https://web.quantsapp.com/quantsapp-classroom/Volatility/IV-With-IVR-&-IVP
20. AlgoTest Docs, "VRP Analysis Tool" https://docs.algotest.in/clicktrade/strategy-builder/vrp-analysis-tool/
21. AlgoTest Blog, "IV vs RV and trading edge with VRP" https://algotest.in/blog/iv-vs-rv-and-trading-edge-with-vrp/
22. StockMojo, "NIFTY IV, HV, RV Chart" https://stockmojo.in/iv-chart/nifty
23. Equities India, "Sensibull review" (secondary) https://equitiesindia.com/tools-directory/sensibull-review
24. NSE, India VIX white paper https://archives.nseindia.com/content/indices/white_paper_IndiaVIX.pdf and NSE India VIX page https://www.nseindia.com/products-services/indices-indiavix-index
25. TradingView Help, "Historical Volatility" https://www.tradingview.com/support/solutions/43000589145-historical-volatility/
26. TradingView, "IV vs Realised Volatility (VIX/HV Comparator)" by amitlall https://www.tradingview.com/script/K3wR3gOD-IV-vs-Realised-Volatility-VIX-HV-Comparator/
27. Market Chameleon, "Implied Volatility vs Historical Volatility Charting" https://marketchameleon.com/Instructional-Stock-and-Options-Trading-Videos/609/Implied-Volatility-vs-Historical-Volatility-Charting-Comparing-Vol-Trends
28. Market Chameleon, "Implied Volatility Rankings" https://marketchameleon.com/volReports/VolatilityRankings
29. Market Chameleon, "Learn: Volatility" https://marketchameleon.com/Learn/Volatility
30. Market Chameleon, "SPY Implied Volatility (IV) vs Historical Volatility (HV)" https://marketchameleon.com/Overview/SPY/IV/
31. Barchart, "Implied Volatility vs. Realized Volatility" and volatility pages (secondary, via search extracts) https://www.barchart.com/options/implied-volatility-range ; https://www.barchart.com/stocks/quotes/$SPX/volatility-charts
32. Barchart (Canada mirror), implied volatility range https://www.barchart.com/ca/options/implied-volatility-range
33. Barchart, "IV Rank and IV Percentile" (secondary, via search extract) https://www.barchart.com/options/iv-rank-percentile
34. ORATS, "Core Research" data definitions https://orats.com/docs/core-research
35. ORATS Blog, "Our special historical volatility calculation at ORATS" https://orats.com/blog/our-special-historical-volatility-calculation-at-orats
36. ORATS Blog, "Trading when implied is a specific amount over realized volatility" https://blog.orats.com/trading-when-implied-is-a-specific-amount-over-realized-volatility
37. IVolatility, "IV INDEX…IVX" https://www.ivolatility.com/info/ivxm_desc.html
38. IVolatility Education, "Implied Volatility Index (IV Index)" http://www.ivolatility.com/education/implied-volatility-index/
39. IVolatility Help, "Ways to estimate volatility" https://www.ivolatility.com/help/5.html
40. Cboe, "Volatility Index Methodology: Cboe Volatility Index" https://cdn.cboe.com/resources/indices/Volatility_Index_Methodology_Cboe_Volatility_Index.pdf
41. Cboe, "Cboe Volatility Index Mathematics Methodology" https://cdn.cboe.com/resources/indices/Cboe_Volatility_Index_Mathematics_Methodology.pdf
42. Cboe, "Cboe Realized Volatility Index Series Methodology" (v2.0, Aug 2024) https://cdn.cboe.com/resources/indices/documents/RVOL_Methodology.pdf
43. Cboe, "Consultation Results Regarding the Cessation of the RVOL and EVZ Indices" (Jan 2025) https://cdn.cboe.com/resources/release_notes/2025/20250113_Consultation-Results-Regarding-the-Cessation-of-the-RVOL-and-EVZ-Indices.pdf
44. Interactive Brokers, TWS API tick types https://interactivebrokers.github.io/tws-api/tick_types.html
45. Interactive Brokers, TWS guide "Volatility" https://ibkrguides.com/traderworkstation/volatility.htm
46. FinanceFeeds, "Interactive Brokers adds Implied Volatility Percentile and Rank data points to TWS" (Nov 2018, quoting IB) https://financefeeds.com/interactive-brokers-adds-implied-volatility-percentileand-rank-data-points-tws-platform/
47. Schwab, "Using Implied Volatility Percentiles" (secondary; access refused) https://www.schwab.com/learn/story/using-implied-volatility-percentiles
48. Scribd, "IVR IVP ThinkScript" (community, unconfirmed) https://www.scribd.com/document/469378291/IVR-IVP-ThinkScript
49. tastylive, "Implied Volatility, IV Index and IVR" (episode, secondary) https://www.tastylive.com/shows/options-trading-concepts-live/episodes/implied-volatility-iv-index-and-ivr-02-05-2024
50. tastylive, "Revisiting IV Rank" (Aug 2015) https://www.tastylive.com/news-insights/revisiting-iv-rank
51. tastylive, "Calculating expected moves: calendar vs trading days" (episode, secondary) https://www.tastylive.com/shows/options-jive/episodes/calculating-expected-moves-calendar-vs-trading-days-04-06-2016
52. tastylive, "Calculating Expected Move" https://www.tastylive.com/definitions/calculating-expected-move
53. Search extract naming OptionStrat's IVR/IVP display (secondary) via https://www.moomoo.com/us/learn/detail-implied-volatility-rank-and-percentile-117201-240514161
54. SpotGamma Support, Implied 1-Day Move (secondary; access refused) https://support.spotgamma.com/hc/en-us/articles/15297901147923
55. Deribit Insights, "DVOL – Deribit Implied Volatility Index" https://insights.deribit.com/exchange-updates/dvol-deribit-implied-volatility-index/
56. Deribit API, "public/get_historical_volatility" https://docs.deribit.com/api-reference/market-data/public-get_historical_volatility
57. Amberdata Docs, "Implied vs Realized" https://docs.amberdata.io/data-dictionary/analytics/derivatives/implied-realized
58. Amberdata Docs, "Volatility Cones" https://docs.amberdata.io/docs/volatility-cones-1
59. Laevitas User Guide index https://guide.laevitas.ch/llms.txt and "Implied Volatility vs Realized Volatility" https://guide.laevitas.ch/laevitas-metrics/implied-volatility-vs-realized-volatility.md
60. Laevitas User Guide, "Realized Volatility" https://guide.laevitas.ch/concepts/realized-volatility.md
61. Laevitas User Guide, "Volatility Cone" https://guide.laevitas.ch/laevitas-metrics/volatility-cone.md
62. Volmex, "BVIV" https://volmex.finance/indices/bviv
63. Volmex, "BVIV-US paper" https://volmex.finance/papers/BVIV-US-paper.pdf
64. Volmex, "Volmex Realized Volatility Indices" (June 2025) https://volmex.finance/papers/Volmex-Realized-Volatility-Indices.pdf
65. Volmex, Docs https://volmex.finance/docs
66. Blockchain.news flash item quoting @GreeksLive (secondary) https://blockchain.news/flashnews/BTC%20implied%20volatility
67. Montréal Exchange, "Trading Volatility Using Historical Volatility Cones" https://www.m-x.ca/f_publications_en/cone_vol_en.pdf
68. P. Carr and L. Wu, "Variance Risk Premiums", *Review of Financial Studies* 22(3), 2009, 1311–1341 https://ideas.repec.org/a/oup/rfinst/v22y2009i3p1311-1341..html
69. LuxAlgo, "Volatility Cones" (citation of Burghardt and Lane 1990) https://www.luxalgo.com/library/concept/volatility-cones/
70. Fyers, "Options Analytics is now live" (notice; search extract, page returned 404 on direct fetch) https://fyers.in/notice-board/options-analytics-is-now-live/ and Fyers Community, "All-New Options Platform on FYERS" https://fyers.in/community/blogs-gdppin8d/post/introducing-the-new-options-platform-on-fyers-YGlhXLn9XGxraJZ
71. Fyers Help Centre, Options Analytics category https://support.fyers.in/portal/en/kb/platforms-tools/options/analytics
72. Fyers, "What is Auto ATM Straddle in Options Analytics?" https://support.fyers.in/portal/en/kb/articles/what-is-auto-atm-straddle-in-options-analytics
73. Fyers, "What is Straddle/Strangle in Options Analytics?" https://support.fyers.in/portal/en/kb/articles/what-is-straddle-strangle-in-options-analytics
