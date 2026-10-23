> Lane alpha-axes, 2026-10-16. Raw research capture: staging, not fact. 19 axes, about 55 sources opened.

# Options alpha axes: the harness's seed idea queue

## How to read this page

An **axis** is one independent reason an options position makes money. Each axis below is written as a card that the harness can put straight into its queue: a hypothesis, the person who loses money to us and why, the evidence, the features and data it needs, a test, how SPXW 0DTE and NIFTY differ, and what is known about decay. The 28 SPXW hypothesis cards in [read-first](../2026-10-08-alpha-search/read-first.md) are mostly *instances* of these axes at a clock time; this page names the axes and points to those cards rather than repeating them.

**Read marks.** [A] = abstract only. [E] = long extracts of the full text through search (tables, method, conclusions), not the whole paper. [F] = read in full. No source on this page was read in full; every number comes from an abstract or a long extract. Sources already logged in the vault are cited by pointer and were not re-opened.

**The standard test (the bucket method).** Every card uses the method of [results](../2026-10-08-feature-experiments/results.md), so only the parts that change are written per card:

- Window: 30 minutes. SPXW: twelve a day from 9:35 New York. NIFTY: twelve a day from 9:20 to 15:20 India time.
- Position: an at-the-money (ATM) straddle sold at the window start, bought back at the end, priced at mid.
- Labels: (L1) seller's return hedged every minute, per unit premium; (L2) unhedged seller's return; (L3) realised over charged variance of the window; (L4) the desk's band hedge with the spread paid. L4 is the only label that decides.
- Feature: known at the window start, cut into quintiles on the *seen* half of days.
- P-value: reshuffle whole days. Write the claim and the kill line, commit, then open the *fresh* half once.
- Kill line, unless the card says otherwise: the top-minus-bottom quintile difference in L4 has the wrong sign or is inside the reshuffled band on either half.

Two numbers frame everything. On SPXW, the median window realises 0.6 of the variance charged but the pooled ratio is 1.01 to 1.02, and over one day or one week realised variance is 5% to 13% below implied ([results](../2026-10-08-feature-experiments/results.md), findings 4, 10, 11). So an axis that only says "options are dear" adds nothing inside the 0DTE day. It must say *when* or *which* options are dear.

## The axes

### 1. Variance risk premium (VRP), unconditional and conditional

**Hypothesis.** Implied variance exceeds expected realised variance; selling it pays on average, more when volatility is high.
**Who loses and why.** Hedgers who pay to insure against variance shocks; the premium is a risk premium, not an error ([Bakshi and Kapadia 2003](https://doi.org/10.1093/rfs/hhg002) [A]: delta-hedged index calls lose money, more so at high volatility).
**Evidence.** Most of the premium is for large jumps: Bollerslev and Todorov put "more than half" of the VRP on jump-tail risk, S&P 500 1990 to 2008 ([JF 2011](https://public.econ.duke.edu/~boller/Published_Papers/jf_11.pdf) [E]). It sits at the shortest maturity: one-month variance claims have an annual Sharpe of about −1.3, claims three months and longer are not priced ([Dew-Becker et al.](https://www.dew-becker.org/documents/price_of_variance_risk.pdf) [E]). Inside the 0DTE day it is tiny (Vilkov; Almeida et al., in [read-first](../2026-10-08-alpha-search/read-first.md) "Known and taken"). NIFTY: priced but eaten by normal costs except for low-cost writers ([Garg and Vipul, JFM 2015](https://ideas.repec.org/a/wly/jfutmk/v35y2015i9p795-812.html) [A]); priced despite heavy retail, and only past *continuous* variance forecasts variance-swap returns, jumps do not ([Sankar et al. 2020](https://ideas.repec.org/a/eee/reveco/v70y2020icp321-334.html) [A]); a delta-hedged NIFTY seller conditioned on VRP percentile shows net Sharpe 2.37 with a premium that shrank after the November 2024 reforms ([John 2026, ResearchGate](https://www.researchgate.net/publication/411779323_Harvesting_the_Volatility_Risk_Premium_in_Nifty_Index_Options_Out-_of-Sample_Evidence_and_the_Post-2024_Regulatory_Regime_Break) [A], one author, not refereed; treat as weak).
**Features.** IV−RV gap; IV level; IV percentile; jump share of recent RV.
**Data.** One-minute chain quotes; index one-minute bars.
**Test.** Standard. Condition on IV level (Bakshi–Kapadia predicts a bigger premium at high IV) rather than on the trailing gap, which the desk killed as a signal.
**SPXW vs NIFTY.** SPXW 0DTE: near zero inside the day. NIFTY weekly: premium exists and the holding period of days is the natural unit.
**Decay.** The 0DTE mispricing "dissipates after the daily availability of 0DTEs" ([Almeida et al., FMA 2025](https://www.fma.org/assets/docs/Derivatives2025/Almeida.pdf) [E]). NIFTY: compressed after Nov 2024 (John 2026).

### 2. The non-trading-period premium (overnight and weekend)

**Hypothesis.** The seller earns the premium mostly when the market is closed, and gives some back while it is open.
**Who loses.** Holders who cannot hedge overnight pay to be insured across the gap; pricers who count closed hours as trading time overcharge ([Jones and Shemesh 2018](https://faculty.marshall.usc.edu/Christopher-Jones/pdf/jones_shemesh_2018_jf.pdf), in vault).
**Evidence.** SPX: delta-hedged returns negative overnight, positive intraday (Muravyev and Ni, in vault). NIFTY 2017 to 2020: short NIFTY options earn significantly overnight and lose intraday; the VRP is "mainly a reward for overnight risk" ([Bhat, Pandey, Rao, JFM 2024](https://doi.org/10.1002/fut.22512) [E]). NIFTY overnight volatility was about 59% of intraday in that sample (same source).
**Features.** Close-to-open variance share; overnight implied variance (1DTE minus 0DTE at the close); GIFT Nifty move overnight (NSE IX trades 06:30–15:40 and 16:35–02:45 IST, [Hindu BusinessLine 2023](https://www.thehindubusinessline.com/markets/gift-nifty-is-a-signal-to-global-financial-markets-that-ifsc-is-now-in-the-game/article67037300.ece) [E]).
**Data.** Close and open chain snapshots; GIFT Nifty bars for NIFTY.
**Test.** Label: straddle sold at 15:25 (NIFTY) or 15:55 (SPXW 1DTE), bought 15 minutes after the next open. Bucket on the overnight implied share and on day of week. One trade a day, so years are needed.
**SPXW vs NIFTY.** Stronger candidate for NIFTY: no night session in India and the desk holds NIFTY weeklies over days. SPXW 0DTE never holds overnight; the 1DTE does.
**Decay.** The US overnight equity drift ended around 2021 (NY Fed, in vault); the option premium was not tested after 2020 on NIFTY.

### 3. The variance clock: intraday theta and its shape

**Hypothesis.** The market's rate of time decay through the day differs from the rate at which variance actually arrives, at known clock times.
**Physics.** For an ATM straddle, premium ≈ 0.8·S·σ·√τ, so theta per minute ≈ premium/(2τ): decay accelerates as 1/√τ in clock time. If the market prices on a variance clock V(t), theta at minute t is proportional to the variance expected in that minute, σ²(t). So the theta curve *reveals* the intraday variance curve the market assumes.
**Who loses.** A seller who charges a smooth clock through a known burst (10:00 releases, 14:00 FOMC, 15:50 imbalances), or a buyer who pays for variance in a dead hour.
**Evidence.** Much of the zig-zag in the 0–7 day IV term structure is a mismeasured clock; a clock calibrated to intraday E-mini variance is smoothest on 96% of days, calendar time never ([Bondarenko 2026](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6705119) [A]). DAX intraday variance is U-shaped with spikes at release times ([Sundkvist](https://helda.helsinki.fi/server/api/core/bitstreams/be70e561-a909-466a-9a94-b505355b5f99/content) [E]). Practitioner pricers already weight time by expected variance ([SpiderRock docs](https://docs.spiderrockconnect.com/docs/Documentation/PlatformFeatures/Analytics/VolTimeCalc/) [E]). Against this, the desk found the window ratio flat through the day once each window is charged for itself (finding 4): on average the clock is right.
**Features.** Implied local variance per minute (change in ATM straddle at fixed spot, or the forward variance between adjacent expiries); realised variance per clock bucket over the last 20 days; event-calendar dummies.
**Data.** One-minute 0DTE and 1DTE quotes (held); release calendars (free).
**Test.** Standard, but bucket on "implied local variance ÷ trailing realised for this clock bucket". Holding period 5 to 30 minutes around fixed times. Overlaps read-first cards 1, 2, 10.
**SPXW vs NIFTY.** SPXW: daily 0DTE, so 250 days a year of clock data. NIFTY: 0DTE only on Tuesday (NSE moved all expiries to Tuesday from 1 Sep 2025, [Indian Express](https://indianexpress.com/article/business/market/nse-shift-weekly-derivatives-expiry-tuesday-bse-thursday-10072638/) [E]); the clock question is about the 15:00-to-settlement window and the August 2026 closing-auction change (read-first card 12).
**Decay.** Not known; Bondarenko is from 2026.

### 4. Event volatility (FOMC, CPI, payrolls; Union Budget, RBI)

**Hypothesis.** Options sold before a scheduled release and bought after it earn the event premium, net of the jump.
**Who loses.** Hedgers buying protection into a known date; retail buying straddles into a story.
**Evidence.** US: in vault — FOMC VRP (Johannes, Kaeck, Seeger), CPI/FOMC/payrolls/GDP priced and most others not (Londono and Samadi), 71% of FOMC priced variance at the statement (Song). Single stocks: earnings jumps are large, time-varying and informative for future volatility ([Dubinsky et al., RFS 2019](https://doi.org/10.1093/rfs/hhy060) [A]). India: India VIX rises before scheduled releases and normalises after ([Shaikh and Padhi 2013](https://journals.sagepub.com/doi/10.1177/0973801013500168) [A]); only RBI policy days move India VIX, other releases do not ([Srinivasan 2017](https://www.scirp.net/pdf/tel_2017041708591130.pdf) [E]). Union Budget: Bank Nifty IV rose from 31.7% to 43.4% in the five days before and fell to 30.5% at the budget close, five-year average ([Upstox](https://upstox.com/news/market-news/trading/budget-2025-how-to-trade-options-leading-up-to-the-budget-day/article-142620/) [E], a broker, [seller]). A practitioner event study of 42 NIFTY events found RBI and FOMC "crush" near a fair-pricing baseline once a weekday placebo is removed, and all 3 Budgets overpriced, realised/implied move 0.74%/1.75% ([LinkedIn post, Sep 2026](https://www.linkedin.com/posts/kaushikkumar3_volatility-eventrisk-nse-activity-7508537645052944384-hc-N) [E], [unknown]).
**Features.** Event implied move (straddle before minus straddle after, in variance); last event's realised/implied; weekday control.
**Data.** Calendars (free); quotes around each event.
**Test.** Event study, not quintiles: label is L1 from the last pre-event minute to 30 minutes after. Compare with the same weekday and clock time on non-event days (the placebo above is the key control). Rare: about 8 FOMC, 12 CPI, 6 RBI, 1 Budget a year.
**SPXW vs NIFTY.** SPXW: many events, intraday release times known to the minute. NIFTY: RBI at 10:00 IST, Budget around 11:00 on 1 February; US events land overnight for NIFTY, so they belong to axis 2.
**Decay.** Pre-FOMC drift ended in 2016 (Song, in vault). No decay data for India.

### 5. Skew premium and skew dynamics

**Hypothesis.** OTM puts (index) carry a premium beyond the leverage effect; selling the skew against variance earns little extra, so the skew is a *form* of the VRP, not a separate axis.
**Who loses.** End users who are net long index options, especially OTM puts; dealers charge for the unhedgeable part ([Gârleanu, Pedersen, Poteshman, RFS 2009](https://www.nber.org/papers/w11843) [A]). Index IV changes follow public put buying pressure ([Bollen and Whaley, JF 2004](https://doi.org/10.1111/j.1540-6261.2004.00647.x) [A]).
**Evidence.** About 42% of the one-month implied skew is risk premium; strategies that capture skew and hedge variance "earn an insignificant risk premium" ([Kozhan, Neuberger, Schneider, RFS 2013](https://openaccess.city.ac.uk/id/eprint/15209/1/RFS%20Skew%20Risk%20Premium%20with%20Kozhan%20and%20Schneider.pdf) [E]). 0DTE: the premium is for *upside* risk (Almeida et al. [E]); Vilkov finds downside (vault). NIFTY: put IV above call IV across strikes and maturities, 2004–2014 ([Narain et al.](https://ideas.repec.org/a/eme/jamrpp/jamr-09-2015-0062.html) [A]); a smile-adjusted Black model fits and IV forecasts volatility; the IV risk premium is higher for Indian single-stock options than abroad ([Jain, Varma, Agarwalla, JFM 2019](https://doi.org/10.1002/fut.21971) [A]).
**Features.** 25-delta risk reversal (RR25); RR25 divided by ATM IV; smile slope at fixed standardised moneyness; spot-vol beta (the desk measured slope −3).
**Data.** One-minute quotes across strikes (held for SPXW).
**Test.** Label: return of a delta-hedged risk reversal (short 25-delta put, long 25-delta call) per window, plus L1. Bucket on RR25 z-score against the same minute over 20 days. Kill if the RR return vanishes after hedging variance exposure (the KNS result).
**SPXW vs NIFTY.** SPXW: test which wing is dear (read-first card 7). NIFTY: retail buys cheap OTM options on both sides; the expiry-day wing may be dear on both sides at once.
**Decay.** Not found.

### 6. Term structure and calendars

**Hypothesis.** The slope of implied variance across expiries prices variance risk, not future variance; an inverted curve pays buyers.
**Evidence.** The second principal component of the VIX curve predicts returns of variance swaps, VIX futures and straddles at all maturities ([Johnson, JFQA 2017](https://doi.org/10.1017/s0022109017000825) [A]). Only the front claim is priced (Dew-Becker et al., axis 1). 0DTE against 1DTE: disputed (read-first card 9). NIFTY: current-month IV significantly above next and far month, 2004–2014 (Narain et al. [A]).
**Who loses.** Buyers of front-expiry protection in stress.
**Features.** Forward variance between adjacent expiries; front/next IV ratio; slope z-score.
**Data.** Quotes of two or more expiries (held: SPXW 0–7 days within 5% of spot).
**Test.** Label: gamma- or vega-matched calendar return over the window and to the front expiry; bucket on slope. Use the stochastic clock of axis 3 when computing forward variance, or the slope is noise (Bondarenko).
**SPXW vs NIFTY.** SPXW: daily ladder, so slopes exist every day. NIFTY: one weekly plus the monthly; a weekly-versus-monthly calendar held to the weekly expiry is the natural trade.
**Decay.** Not found.

### 7. Realised-volatility forecasting (HAR and its extensions) against IV

**Hypothesis.** A better forecast of realised variance than the options' own forecast tells which windows are cheap or dear.
**Evidence.** HAR-RV regresses RV on its daily, weekly and monthly averages ([Corsi 2009](https://ideas.repec.org/a/oup/jfinec/v7y2009i2p174-196.html) [A]). IV carries information beyond HAR and its jump split in stocks, bonds and FX ([Busch, Christensen, Nielsen](https://repec.econ.au.dk/repec/creates/rp/07/rp07_09.pdf) [E]); HAR with IV beats every HAR without IV across 10 indices, and overnight returns help further ([Kambouroudis et al., JFM 2021](https://doi.org/10.1002/fut.22241) [E]); HAR wins at one day, VRP-adjusted IV at one month ([Kourtis et al., JFM 2016](https://doi.org/10.1002/fut.21792) [E]). High IV goes with daily reversal, so IV is a biased forecast of long-horizon variance ([Jones, Pyun, Wang](https://faculty.marshall.usc.edu/Christopher-Jones/pdf/jones_pyun_wang_2016.pdf) [E]). The desk: IV already tracks recent RV (0.79–0.86).
**Who loses.** Nobody in particular; this axis is a *tool* for every other axis.
**Features.** HAR terms in clock-bucket units; signed semivariance; jump share; overnight return; IV. The feature is the forecast residual: HAR-IV forecast minus charged variance.
**Data.** One-minute index bars (held).
**Test.** Fit on the seen half only; bucket on the residual.
**SPXW vs NIFTY.** Same method; NIFTY needs the GIFT Nifty overnight term.
**Decay.** Not relevant; the risk is that the residual is just noise in IV.

### 8. Dealer gamma exposure (GEX), pinning and squeezes

**Hypothesis.** When hedgers are net long gamma, realised variance is lower and moves reverse; when net short, moves continue.
**Evidence.** Stock volatility falls with the net gamma of likely hedgers; about 12% of daily absolute stock return is hedge rebalancing ([Pearson, Poteshman, White](https://www.ou.edu/dam/price/Finance/CFS/paper/pdf/pearsonPoteshmanWhite.pdf) [E]; published as Ni et al., RFS 2021). 0DTE market-maker gamma is mostly positive; the maximum effect is +3.3 vol points a day and +6.4 for one 30-minute period ([Amaya et al., Cboe](https://cdn.cboe.com/resources/education/research_publications/gammasqueezes.pdf) [E]). Positive gamma strengthens reversal, negative gamma momentum ([Dim, Eraker, Vilkov](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4692190) [A]). 0DTE days lower index volatility by 60–90 bp ([Adams, Fontaine, Ornthanalai](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4881008) [A]). S&P futures pinned on serial expiries 1992–2009, cash-settled SPX shows anti-pinning ([Golez and Jackwerth](https://kops.uni-konstanz.de/server/api/core/bitstreams/b9492112-cab3-4217-a7d0-d2c4f5ba7825/content) [E]).
**Who loses.** A seller who ignores a negative-gamma regime; a buyer who pays for moves in a pinned book.
**Features.** Signed GEX from trades (who opened what), not from open interest alone; distance to the largest-gamma strike; GEX × time to close.
**Data.** Open interest by strike; better, signed trade flow (Cboe Open-Close, OPRA conditions). **Not held.** NIFTY: NSE publishes daily participant-wise open interest for clients, proprietary traders, FIIs and DIIs (not opened here; check).
**Test.** Standard, label L3 first (the mechanism is about realised variance), then L4.
**SPXW vs NIFTY.** SPXW: well documented, but the effect is a few vol points. NIFTY: no study found; the SEBI order against Jane Street shows the opposite case, a large participant moving the index to suit its options on expiry days (axis 11).
**Decay.** Flow-gamma sign reversed in 2025 (Singh, in vault).

### 9. Vanna and charm flows near expiry

**Hypothesis.** As time passes (charm) and IV falls (vanna), hedgers' deltas change and they must trade the index in a predictable direction late in the day or into monthly expiry.
**Evidence.** Academic: S&P 100 stocks earn high returns over option-expiration weeks, linked to hedgers reducing short-stock hedges and falling IV ([Stivers and Sun](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1571786) [A]). For the index intraday: **no academic test found.** Vendor only: Volland claims charm "yields a significant edge" on 0DTE ([DeLorenzo, SSRN 2023](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4669282) [A], [seller]). The desk: charm causes under 2% of a re-struck straddle's delta change (finding 8).
**Features.** Aggregate charm and vanna of the 0DTE book (signed); IV change since the open × aggregate vanna.
**Data.** Signed open interest or flow: **not held**.
**Test.** Label L4 and index return from 14:00 to 15:50; bucket on signed charm notional.
**SPXW vs NIFTY.** SPXW 0DTE has the gamma concentration; NIFTY only on Tuesday.
**Decay.** Unknown; the axis is crowded in retail commentary.

### 10. Retail flow in 0DTE and in Indian weeklies

**Hypothesis.** Retail buys short-dated OTM options at prices above fair value and loses the difference to sellers and market makers.
**Evidence.** US: in vault (Beckmeyer et al. $241,000 a day; Bogousslavsky and Muravyev −4.6% per 0DTE trade). India: 91.1% of individuals lost money in F&O in FY24; options losses were ₹77,800 crore; proprietary traders and FPIs made gross profits of about ₹33,000 crore and ₹28,000 crore, 96–97% of it by algorithmic entities ([SEBI study, Sep 2024](https://www.sebi.gov.in/sebi_data/attachdocs/sep-2024/1727085659479.pdf) [E]). FY25: net individual losses ₹1,05,603 crore, 91% loss-makers; unique traders fell from 61.4 to 42.7 lakh between Q1 and Q4 after the November 2024 measures ([SEBI, Jul 2025](https://www.sebi.gov.in/sebi_data/attachdocs/jul-2025/1751900271726.pdf) [E]).
**Who loses.** Retail option buyers, through overpayment, spread and their own timing.
**Features.** Time of day; premium level (cheap far-OTM); expiry day; Monday after a rally; retail share proxies (small-lot trade share).
**Data.** Trades with size, or exchange participant data. **Not held** for either market.
**Test.** Label: delta-hedged return of far-OTM (5–15 delta) options sold at entry times when retail is active, versus ATM; holding to expiry and per window.
**SPXW vs NIFTY.** NIFTY is the stronger case: retail dominates, the regulator measures the losses, and the 1 Oct 2024 circular cut weekly expiries to one benchmark per exchange, tripled lot size (NIFTY 25 → 75) and added 2% tail margin on expiry day ([SEBI circular](https://www.sebi.gov.in/sebi_data/attachdocs/oct-2024/1727786261636.pdf) [E]; [NSE lot sizes](https://nsearchives.nseindia.com/content/circulars/FAOP64625.pdf) [E]).
**Decay.** Shrinking by regulation in India. Costs rose too: from 1 Apr 2026 STT is 0.15% of premium on option sales and 0.05% on futures sales ([NSE STT page](https://www.nseindia.com/static/products-services/equity-derivatives-securities-transaction-tax) [E]); a futures-hedged NIFTY seller pays the futures rate on every hedge sale.

### 11. Expiry-day structural flow and settlement (India focus)

**Hypothesis.** On expiry day, a small number of large participants and forced closes push the index into settlement; the settlement window carries more risk than the chain prices.
**Evidence.** SEBI's interim order: one group made ₹43,289 crore in index options January 2023 to March 2025 while losing ₹7,687 crore in futures and cash; on 17 Jan 2024 it bought ₹4,370 crore of Bank Nifty constituents from 9:15 to 11:47 while building bearish options, then sold from 11:49 ([SEBI order](https://www.sebi.gov.in/sebi_data/attachdocs/jul-2025/1751584518593.pdf) [E]). A second pattern, "extended marking the close", was found on NIFTY in May 2025 (same). Brokers force-close intraday positions after 15:20 by algorithm (SEBI Sep 2024 study [E]). Settlement moved to a closing auction on 3 Aug 2026 (read-first card 12).
**Who loses.** Retail holding options into expiry against a participant who can move the index.
**Features.** Morning cash-futures flow against option flow; distance to max open-interest strikes after 14:00; 15:20 forced close window.
**Data.** NIFTY minute quotes, cash index; participant data not held.
**Test.** Label L3 for 14:30–settlement on expiry Tuesdays against non-expiry days; split before and after 3 Aug 2026.
**SPXW vs NIFTY.** NIFTY only. SPXW has a deep auction and many expiries a week (read-first card 1 is the SPXW analogue).
**Decay.** Regulator is closing it actively; treat as a risk axis as much as an alpha axis.

### 12. Jump risk premium

**Hypothesis.** OTM options price jumps larger than those that occur; the premium for small moves is near zero.
**Evidence.** Fear of rare events is more than half the VRP and about 5% of the equity premium in absolute terms (Bollerslev and Todorov [E]); in 0DTE the premium sits in large jumps (Chong and Todorov, in vault). Index co-jump insurance earns Sharpe 0.85 when sold through dispersion ([AEA 2020 paper](https://www.aeaweb.org/conference/2020/preliminary/paper/8fAi7DtY) [E]). NIFTY: realised jumps do not predict variance-swap returns (Sankar et al. [A]).
**Features.** Implied jump intensity from deep OTM wings; jump share of recent RV; butterfly prices in the tails.
**Data.** Wing quotes (held for SPXW within the 0DTE chain).
**Test.** Label: delta-hedged return of short 5-delta strangle vs short ATM straddle per unit vega; holding period to expiry. Use AFML ch. 15 (strategy risk for asymmetric payoffs): the sample needs enough crash days.
**SPXW vs NIFTY.** Both; NIFTY's overnight gap (axis 2) is the main jump channel.
**Decay.** Not found.

### 13. Volatility-of-volatility premium

**Hypothesis.** Vol-of-vol is priced separately from vol; high vol-of-vol predicts lower delta-hedged option gains for the buyer.
**Evidence.** VIX and VVIX are only weakly related; both negatively predict delta-hedged S&P 500 option gains ([Huang, Schlag, Shaliastovich, Thimme, JFQA 2019](https://www.econstor.eu/bitstream/10419/178991/1/102338860X.pdf) [E]). Morning VVIX predicts next-day variance returns (Bevilacqua and Hizmeri, in vault). Smile convexity near ATM reflects vol-of-vol (Bandi, Fusari, Renò, in vault [E]).
**Features.** ATM smile curvature; realised vol of the 1-minute ATM IV series; India VIX realised volatility for NIFTY.
**Data.** Held (curvature from chain quotes).
**Test.** Standard, bucket on curvature z-score; label L1 next window and next day.
**SPXW vs NIFTY.** Both. No VVIX equivalent in India; compute it.
**Decay.** Not found.

### 14. Dispersion and the correlation premium

**Hypothesis.** Index options are dear against their constituents because investors pay to hedge correlation spikes.
**Evidence.** Priced correlation risk with high alpha, but it "cannot be exploited with realistic trading frictions" ([Driessen, Maenhout, Vilkov, JF 2009](https://doi.org/10.1111/j.1540-6261.2009.01467.x) [A]); Swedish evidence: Sharpe falls to 0.20 after the full spread ([Jokela](https://aaltodoc.aalto.fi/server/api/core/bitstreams/3079087f-5d08-44d9-9caf-e9eeedcbe1ed/content) [E]).
**Data.** Single-stock option chains: **not held**; NIFTY stock options are monthly only (SEBI May 2025 circular [E] via [this PDF](https://www.sebi.gov.in/sebi_data/attachdocs/may-2025/1748266377271.pdf)).
**SPXW vs NIFTY.** Neither fits an intraday desk. Park it.

### 15. Put-call parity, the box rate and the financing basis

**Hypothesis.** Deviations from parity carry information about order flow; the box rate is the true financing cost.
**Evidence.** SPX box rates sit about 35–40 bp above Treasuries, minute by minute, with R² near 1 ([van Binsbergen, Diamond, Grotteria, JFE 2022](https://www.nber.org/papers/w26138) [E]): parity holds tightly for SPX. Single stocks: expensive calls over puts predict +50 bp a week, a predictability that "decreases over the sample period" ([Cremers and Weinbaum, JFQA 2010](https://doi.org/10.1017/s002210901000013x) [A]). NIFTY: frequent put-call-futures violations even after costs that "vanish quickly"; puts overpriced more often ([Vipul, JFM 2008](https://doi.org/10.1002/fut.20325) [A]); violations tied to short-sale limits ([Gupta and Jithendranathan](http://hdl.handle.net/10072/40293) [E]).
**Features.** Implied forward (parity) minus futures; implied rate minus box rate; call-minus-put IV at the same strike.
**Data.** Implied forward held; futures not held.
**Test.** Label: next-window index return (directional) and L4 of the band hedge using synthetic versus futures hedge.
**SPXW vs NIFTY.** SPXW: a cost input (use the parity forward for Greeks), not alpha. NIFTY: hedging through the synthetic future instead of the future may save STT and margin; a cost axis worth a test.
**Decay.** Strong.

### 16. Open-interest signals: max pain and the put-call ratio

**Max pain.** The claim: price converges to the strike where option holders lose most. For small, illiquid stocks there is a reversal that overlaps expiry ([Filippou, Garcia-Ares, Zapatero, SSRN 2022](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4140487) [A]). For indices: on 1,146 graded snapshots, 40.6% ended closer to max pain and the median distance widened from 2.3% to 2.8% ([Quant Data, 2026](https://quantdata.uk/research/does-max-pain-pin) [E], [seller]); FirmTape replicated pinning on 1,072 SPX sessions and says the popular effect is not supported ([FirmTape](https://firmtape.com/learn/max-pain) [E], [seller]). The academic finding is strike *clustering* in stocks, 16.5 bp per expiry (Ni, Pearson, Poteshman, in vault), and anti-pinning for cash-settled SPX (Golez and Jackwerth).
**Put-call ratio.** The predictive PCR is built from *non-public* open-buy volume; the source of predictability is private information, not inefficiency ([Pan and Poteshman, RFS 2006](https://www.mit.edu/~junpan/volume.pdf) [E]). Index net put buying predicts weekly S&P 500 returns, best explained by retail protection buying ([Chordia et al., Mgmt Sci 2021](https://pubsonline.informs.org/doi/10.1287/mnsc.2019.3529) [A]). On 1,027 days of 0DTE, a gamma-weighted opening PCR predicts a higher chance of a falling hour, but a trading rule on it earns nothing out of sample, before or after costs ([Maurer and Müller, SSRN 2026](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7339718) [A]).
**Verdict.** Max pain: myth at index level. Public PCR: a risk descriptor, not alpha. Keep one test of each only as a negative control for the harness's skeptic.

### 17. Greek-ratio features, and what they measure

**Derivation.** With zero rates the Black–Scholes equation hedged of delta is Θ = −½σ²S²Γ, exact ([Thuztra notes](https://learn.thuztra.com/reference/greeks-for-a-live-position) [E]; [Sterling, Oct 2026](https://julianrsterling.com/articles/gamma-theta-break-even-move/) [E], with the financing correction). Three consequences:

- 2|Θ|/Γ = σ²S², the implied variance rate in price units. The gamma-theta breakeven move √(2|Θ|dt/Γ) = σS√dt is one implied standard deviation. **No information beyond IV.**
- For an ATM straddle, |Θ|/premium ≈ 1/(2τ) and ΓS²/premium ≈ 1/(σ²τ): ratios of Greeks per unit premium are functions of the clock and σ√τ only. Their *deviation* from these values measures the smile and the market's clock (axis 3), nothing else.
- For a straddle struck at K, Δ/Γ ≈ S−K (desk finding 7). So Δ²/(2Γ|Θ|h) ≈ (S−K)²/(σ²S²h) for elapsed time h: the squared *end-point* move since the strike over the implied variance for that time. The hedged P&L instead sums squared *increments* along the path: ½ΓS²Σ(r²−σ²dt) (Bakshi and Kapadia [A]).

So Δ²/(2Γθ) divided by (RV/IV)² is the window's **variance ratio**, end-point variance over path variance, the statistic of [Lo and MacKinlay, RFS 1988](https://doi.org/10.1093/rfs/1.1.41) [A]. It is above 1 when the window trended and below 1 when it chopped. That is why it explains the unhedged seller (−0.78) better than the variance ratio does, and why the two correlate only 0.3. **Published basis:** none for the ratio by name; its pieces are standard. Practitioner "gamma/theta ratio" pages ([greeks.live](https://learn.greeks.live/area/gamma-theta-ratio/) [E]) treat it as a free signal; at ATM it is not.
**Testable hypothesis.** Trendiness persists inside the day (intraday momentum, in vault: Gao et al., Baltussen et al.; FirmTape says flat 2022–2026). Prediction: the trailing 60-minute variance ratio sorts L2 of the next window. This is the desk's open lead "how straight the day has run" (read-first card 27). Test it once as the variance ratio, not as a Greek ratio.

### 18. Demand pressure and option supply (end users, overwriters)

**Hypothesis.** Predictable buying or selling by funds moves IV at known times and reverses.
**Evidence.** Demand pressure explains index option expensiveness and skew (Gârleanu et al. [A]). Single-stock option returns are highly negative on the third-Friday and next-Monday rollover days of covered-call writers, and rollover days carry half of 18 option-return anomalies ([Garcia-Ares, FMA 2025](https://www.fma.org/assets/docs/Derivatives2025/GarciaAres.pdf) [E]). Index call overwriting by income funds is small (vault: under $1bn in daily-call funds).
**Test.** Label: change in call IV at fixed moneyness around fund roll times; L1 of straddle across rollover Mondays. SPXW: monthly roll of large buy-write funds. NIFTY: not found.

### 19. Option-return momentum

**Evidence.** Monthly ATM straddle returns on single stocks persist over 6–36 months with no reversal; near zero after the full spread for liquid names ([Heston et al., JF 2023](http://faculty.marshall.usc.edu/Christopher-Jones/pdf/opmom.pdf) [E]). The desk found no persistence of the trailing gap inside the day. Cross-sectional and monthly; does not fit one index intraday. Low priority.

## Ranking by market

Expected strength combines the evidence, whether the edge survives our costs, and whether we hold the data. "Rank 1" is the first item the harness should test.

| Rank | SPXW 0DTE | Why | NIFTY weekly/monthly | Why |
|---|---|---|---|---|
| 1 | Variance clock at fixed burst times (3, 4) | Mechanism with a minute; data held; Song and Bondarenko | Non-trading-period premium (2) | Refereed NIFTY evidence; no night session; desk holds over days |
| 2 | Event vol, FOMC/CPI (4) | Documented premium; resolves at a known minute | VRP conditional on level, weekly horizon (1) | Priced in India; survives low costs; compressing |
| 3 | 1DTE overnight and weekend premium (2) | One-day realised 5–13% under implied (desk); Jones–Shemesh | Retail flow on expiry Tuesday, far-OTM (10, 11) | SEBI measures who loses; algos take 96–97% of prop/FPI profit |
| 4 | Jump premium in the wings, which wing (5, 12) | Premium in large moves; papers disagree on the wing | Event vol: Budget and RBI (4) | Clear dates; small n; Budget overpriced in a weak source |
| 5 | Dealer gamma as a variance regime (8) | Well documented, but a few vol points and data not held | Term structure, weekly against monthly (6) | Front-only premium (Dew-Becker); NIFTY front IV higher |
| 6 | Trendiness / variance ratio (17) | Desk lead; cheap to test | Skew and put demand (5) | Put IV above call IV; premium higher than abroad |
| 7 | Vol-of-vol (13) | Priced in S&P; proxy held | Synthetic vs futures hedge cost (15) | STT 0.05% on futures sales; a cost edge, not alpha |
| 8 | Skew dynamics, RR25 (5) | KNS says it collapses into VRP | Settlement window after 3 Aug 2026 (11) | Clean break; regulator may revert |
| 9 | HAR residual (7) | A tool; IV already subsumes most | HAR with GIFT Nifty overnight term (7) | Same |
| 10 | Vanna/charm (9), retail flow (10) | No academic test; data not held | GEX, vanna/charm (8, 9) | No study found |

## What the evidence calls myths

- **Max pain at index level.** Graded tests find no pull; the real effect is stock strike clustering and, for cash-settled SPX, anti-pinning (axis 16).
- **Public put-call ratio as a timing signal.** Predictability comes from non-public open-buy flow; the one 0DTE test finds a risk signal with no out-of-sample profit (axis 16).
- **Greek ratios as new information.** At the money they reduce to IV and the clock; Δ²/(2Γθ) is a variance ratio in disguise (axis 17).
- **"Options are always dear" inside the 0DTE day.** Pooled ratio 1.01–1.02 on the desk's year; Vilkov's premium is tiny (axis 1).
- **The trailing IV−RV gap as a signal.** Killed on the desk's fresh days (results, finding 2).
- **Dispersion as a retail-size or intraday edge.** Priced but not exploitable after frictions (axis 14).
- **Parity violations as SPX alpha.** SPX parity holds to near R² = 1; old NIFTY violations needed short sales institutions could not make (axis 15).
- **Vanna and charm "drive the market".** No academic test found; vendor claims only; charm is under 2% of a re-struck straddle's delta change (axis 9).

## What to take for our harness

1. **Seed the queue with these 19 axes as typed cards** (hypothesis, loser, features, data, label, holding period, kill line, market). The idea scout adds instances (a clock time, an event type) under an axis; the skeptic rejects a new card that is an instance of a killed axis.
2. **One feature library, shared by all axes:** IV−RV, RR25, term slope, smile curvature, implied local variance per clock bucket, HAR-IV residual, variance ratio, event and weekday dummies, overnight share. Most ratios people propose reduce to these; the feature miner must check that first (axis 17).
3. **A data gate per card.** Cards that need open interest, signed flow or futures (8, 9, 10, 14, 15) wait in a "needs data" lane with the vendor named, under the paid-data cap.
4. **Fixed controls.** Every event test carries the weekday-and-clock placebo; every 0DTE test reports the pooled ratio beside the median.
5. **Negative controls for the auditor.** Max pain and public PCR run once each; if the harness finds an edge there, suspect the harness.
6. **NIFTY first tests:** overnight premium (2), conditional weekly VRP (1), expiry-Tuesday far-OTM premium (10), all with STT at the April 2026 rates.
7. **SPXW first tests:** variance clock at 10:00, 14:00 and 15:50 (3), and the 1DTE overnight premium (2), both on data held.

## Could not reach or not found

- No academic test of vanna or charm flows on index returns was found.
- No study of dealer gamma or open-interest signals on NIFTY was found.
- NSE participant-wise open interest page: not opened; whether it splits options by strike is not known.
- JSTOR copies of Driessen et al. and Bollen–Whaley returned a challenge page; abstracts read instead.
- Bondarenko 2026, Maurer–Müller 2026 and Adams et al. were read as abstracts only; their numbers above are from the abstracts.
