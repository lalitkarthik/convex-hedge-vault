# Round Two — Verification of Round One's Load-Bearing Claims

Seven claims, seven verdicts. Where I could not reach a primary document I say so. Two claims survive intact, three are refuted or materially wrong, one is confirmed with a wording correction that matters, and one (the SVI residual) resolves in a way neither round-one agent stated.

---

## 1. THE CORRECTION NOTICE — **CONFIRMED**, with one wording discrepancy that cuts against round one

**Repository:** `vilkovgr/0dte-strategies` — https://github.com/vilkovgr/0dte-strategies
**Notice:** https://github.com/vilkovgr/0dte-strategies/blob/main/KNOWN-ISSUES.md
**Paper:** Vilkov, *0DTE Trading Rules: Tail Risk, Implementation, and Tactical Timing*, https://ssrn.com/abstract=4641356

I pulled the raw `README.md` and `KNOWN-ISSUES.md`, not the rendered page. The README banner reads **verbatim**:

> **Correction, August 2026.** A transaction-cost unit-scale error caused the bid-ask half-spread to be charged at 1/100 of its true size (about 0.022 bp instead of 2.2 bp). The code is fixed in this commit, and the correction reverses the sign of the net-of-cost conclusions: no strategy or basket retains a positive net Sharpe ratio. Gross results are also affected. Read **KNOWN-ISSUES.md** before using any number from this package. Found by gex.live.

**The discrepancy.** `KNOWN-ISSUES.md` states the same result more carefully: *"**No structure retains a materially positive net Sharpe ratio.**"* Its own table does not support the README's absolute claim:

| Structure | SR mid | SR net (before) | SR net (after) |
|---|---|---|---|
| Put Ratio Spread | +1.06 | +0.84 | **−0.61** |
| Risk Reversal | +0.65 | +0.44 | **+0.10** |
| Bear Put Spread | +0.48 | +0.30 | **−0.73** |
| Strangle/Straddle | −0.27 | −0.51 | **−0.97** |
| Iron Butterfly/Condor | −0.56 | −0.96 | **−2.67** |

Risk Reversal survives at **+0.10**, not negative. Round one repeated the README's stronger sentence. Use the KNOWN-ISSUES wording.

**The mechanism, exactly.** The panel mixes scales: `bas`, `mid`, `tv` are *fractions* of spot (`(ask-bid)/active_underlying_price`); `reth_und`, `reth` are *percent* of spot (`(payoff-mid)*100`). The cost line `pnl_ba = pnl_mid - half_spread_cost` subtracted a fraction from a percent, while the flat `- 0.005` (0.5 bp) fee was correctly scaled. Entry turnover for a two-leg strangle goes from an apparent 0.24 bp to a true **24 bp**.

**The part round one missed, and it is the most transferable lesson.** The notice's own scope note:

> Note that gross columns also move, because the binary target `y = 1{pnl_net > 0}` depends on the cost. Correcting the cost relabels the training data, so the classifier learns a different — and weaker — signal. Anyone rescaling the cost only at the evaluation step, without also rebuilding the target, will get a more favorable number than the one reported here.

Also flagged: `compute_conditional_model_zoo.py` and `derive_binary_decision_summary.py` use a flat `--net-cost 0.005` that **excludes the half-spread entirely** — "those 'net' figures understate realistic cost by roughly 5x and should be read as an upper bound." That is a modelling choice, not a bug, and it is still in the repo.

There is a second, earlier correction (2026-05, reported by Victor Yoong, [issue #1](https://github.com/vilkovgr/0dte-strategies/issues/1)): `dir_pnl_net = sign * pnl_net` flipped the sign of costs on short days, *adding* the spread to PnL.

**Tests passed:** (1) runnable code ✓ (2) explicit cost model ✓ (4) names its own failure modes — **counts double** ✓✓ (5) reproducible ✓. This is now the strongest single artefact in the entire two-round corpus, and it is strongest *because* it is a retraction.

**Caveat:** the Git LFS budget is exceeded, so the data panels cannot be fetched; `data/conditional_oos_protocol_predictions.parquet` is stale; the paper PDF still carries the uncorrected numbers.

**If false:** nothing — it is confirmed. **What actually changes:** the general prior. A cost bug of exactly two orders of magnitude survived peer review, an SSRN posting and a public replication package, and was caught by an outside replicator reproducing a table to four decimals. Treat *every* published 0DTE net-Sharpe as unproven until the cost line is read. Round one's conclusion stands; its quotation of it did not.

---

## 2. LRS AND US OPTIONS — **REFUTED.** The US is a source of technique, not a venue.

Round one's implied permissiveness is wrong, and the secondary sources everyone cites are *also* wrong, in a way that matters.

**Primary documents opened:**

**(a) RBI Master Direction — LRS**, FED Master Direction No. 7/2015-16, updated 06 Sep 2024 — https://www.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=10192

Para 5, verbatim:
> All other transactions which are otherwise not permissible under FEMA and those in the nature of remittance for margins or margin calls to overseas exchanges/ overseas counterparty are not allowed under the Scheme.

Para 6(iii), the exhaustive list of permissible **capital account** transactions, verbatim:
> acquisition of immovable property abroad, Overseas Direct Investment (ODI) and Overseas Portfolio Investment (OPI), in accordance with the provisions contained in Foreign Exchange Management (Overseas Investment) Rules, 2022, Foreign Exchange Management (Overseas Investment) Regulations, 2022 and Foreign Exchange Management (Overseas Investment) Directions, 2022

**(b) FEM (Overseas Investment) Directions, 2022**, A.P. (DIR Series) Circular No. 12, 22 Aug 2022 — this is the clause that decides it. Definition (ix), verbatim:

> **"Overseas Portfolio Investment (OPI)"** means investment, other than ODI, in foreign securities. The following is further provided:
> a) OPI shall not be made in:
>  i. any unlisted debt instruments; or
>  ii. any security which is issued by a person resident in India who is not in an IFSC; or
>  **iii. any derivatives unless otherwise permitted by Reserve Bank; or**
>  iv. any commodities including Bullion Depository Receipts (BDRs).

And (f): *"Resident individuals may make OPI within the overall limit for Liberalised Remittance Scheme (LRS) in terms of schedule III of the OI Rules."*

**The chain closes without a gap.** LRS capital-account permission runs only through OPI/ODI. OPI expressly excludes derivatives. A US-listed option is a derivative. Therefore a resident individual has **no LRS route to a US-listed option — long or short.** Long options do not escape via the "no margin needed" argument: the margin prohibition in para 5 is a *separate*, independent bar that kills short options; the OPI carve-out kills long ones too.

**(c) A correction to the received wisdom.** I downloaded the full RBI LRS FAQ (https://www.rbi.org.in/scripts/FAQView.aspx?Id=115) and grepped it. The strings **"derivative" and "option" appear zero times.** Q2's actual prohibition list is:

> - Remittance for any purpose specifically prohibited under Schedule-I … or any item restricted under Schedule II of FEM (Current Account Transactions) Rules, 2000.
> - Remittance from India for margins or margin calls to overseas exchanges / overseas counterparty.
> - Remittances for purchase of FCCBs issued by Indian companies in the overseas secondary market.
> - **Remittance for trading in foreign exchange abroad.**
> - Capital account remittances … to FATF "non-cooperative countries and territories" …
> - Remittances … to those individuals and entities identified as posing significant risk of committing acts of terrorism …
> - Gifting by a resident to another resident, in foreign currency, for the credit of the latter's foreign currency account held abroad under LRS.

Multiple advisory sites quote the RBI FAQ as saying *"Remittance under the Scheme is not available for margin trading or derivative transactions."* **That sentence is not in the FAQ.** The right answer is the same, but it comes from the OI Directions, not the FAQ. If he ever argues this with a bank's AD desk, cite definition (ix)(a)(iii) of the OI Directions — quoting a sentence that does not exist will lose the argument.

**(d) GIFT City / IFSC.** RBI/2024-25/49, A.P. (DIR Series) Circular No. 15, 10 July 2024 — https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=12699 — widened IFSC remittance to *all permissible purposes under LRS*, for (i) availing financial services/products under the IFSCA Act 2019 within IFSCs, and (ii) all current or capital account transactions in any other foreign jurisdiction through an FCA held in IFSC.

**"All permissible purposes under LRS" is the load-bearing phrase, and it imports the same OPI carve-out.** IFSC does not create a derivatives permission; it relocates the account. NSE International Exchange's Global Access platform states directly that derivatives and crypto are excluded "due to regulatory restrictions under LRS norms" — equities, ETFs and select debt only. That is the operator's own reading of the same clause, and it matches mine.

**What I could not verify:** I could not retrieve an RBI document that says in terms "a resident individual may not trade overseas exchange-traded options." No such sentence appears to exist. The conclusion is a three-step derivation from primary text, not a single quotable prohibition — which is precisely why the secondary sources invent one. I also could not reach the India INX circular text (PDF extracted to encoded data) or the RBI circular PDF on rbidocs (CAPTCHA-gated); I used the rbi.org.in HTML notification page instead, which is the same primary instrument.

**Edge case, unresolved and worth a CA's opinion, not mine:** funds *already* held abroad and never remitted under LRS (e.g. earned as a US-resident before returning to India) sit outside the LRS remittance question but inside FEMA's residency net. Round one did not raise it; I flag it as genuinely open rather than answer it.

**If this verdict is false** — i.e. if RBI has "otherwise permitted" some derivative class — his opportunity set widens enormously and SPX/SPY becomes his primary research venue with the deepest available data. **Because it is true:** US options are technique only. Everything he builds must clear on NSE, or on a domestically-registered crypto venue. That is a hard constraint on the entire research programme and should be stated at the top of his plan, not in a footnote.

---

## 3. DELTA EXCHANGE INDIA / DERIBIT — **PARTIALLY CONFIRMED, PARTIALLY UNRESOLVABLE.** I could not verify the depth claim and will not launder someone else's snapshot as my own.

**FIU-IND registration: CONFIRMED at first-party level only.** Delta Exchange India is operated by **Excelium Technologies Private Limited**, FIU-IND Reporting Entity registration **VA00041101**. Source: Delta's own compliance page, https://www.delta.exchange/support/solutions?articleId=80001177929.

**Honest negative:** **FIU-IND does not publish a public, searchable register of VDA SP registrations.** I tried `fiuindia.gov.in/files/Reporting_Entity/list_of_registered_reporting_entities.html` (request rejected) and the FIU root. The only independent corroboration is aggregate: the Ministry of Finance told the Lok Sabha that 47 VDA SPs were registered as of December 2024, and the FY2024-25 figure is 49 (45 domestic, 4 offshore). **The registration number is a self-declaration that I could not independently confirm against a government register, because no such public register exists.** Round one presented it as established fact. It is credible but unverified, and he should know the difference.

**Order-book depth: UNRESOLVABLE this session.** `api.india.delta.exchange` and `api.delta.exchange` both returned `HTTP 000` (connection failure) on six attempts across two hosts and two tool paths. A snapshot file left in the shared scratchpad by a sibling agent contains 1,024 option tickers over BTC/ETH/**XAUT**, aggregating ~$486M BTC option OI notional and ~$1.1bn 24h turnover, with a median relative bid-ask of **1.7%** (p25 1.3%, p75 3.5%) and 123/621 BTC strikes at zero OI. **The presence of XAUT strongly suggests this is the global venue, not the India entity** — Delta India lists BTC and ETH. I am not going to report those numbers as Delta India's depth. They are unattributable.

**What he should do instead, and it takes ten minutes:** hit `https://api.india.delta.exchange/v2/tickers?contract_types=call_options,put_options` from his own machine and compute, per expiry: count of strikes with non-zero 24h volume, `(ask-bid)/mid` at each strike, and `bid_size`/`ask_size` in contract-value terms. The 1.7% median spread figure above — even if it is the *global* venue, which is deeper — should be read against the Vilkov result: 2.2 bp of half-spread was enough to invert every 0DTE Sharpe on SPX. A 170 bp spread is roughly **seventy-seven times** that. Any crypto-options strategy that trades more than a few times a month is dead on arrival at that spread, and this is the single number he should compute before writing any crypto code at all.

**Deribit: CONFIRMED available, with a caveat neither agent raised.** Deribit's Restricted Jurisdictions page (last updated **19 March 2026**) lists: Belarus, Canada, Central African Republic, Congo, Cuba, Guam, Iran, Iraq, Japan, DPRK, Libya, Myanmar, Panama (retail spot only), Puerto Rico, Russian Federation, American Samoa, Somalia, South Sudan, Sudan, Syria, sanctioned regions of Ukraine, UAE (retail spot only), UK (retail not allowed), United States, US Virgin Islands, Yemen. **India is not on the list.** Deribit does not restrict Indian residents.

The India-side question is separate. Deribit was **not** among the nine offshore VDA SPs served FIU-IND compliance show-cause notices on 28 December 2023 (Binance, Kucoin, Huobi, Kraken, Gate.io, Bittrex, Bitstamp, MEXC Global, Bitfinex) — PIB press release PRID 1991372 — and it does **not** appear in the 25-name March 2026 MeitY blocking list. So: Deribit does not block him, and India has not blocked Deribit. **But Deribit is not FIU-IND registered**, which means using it does not carry the PMLA protection Delta India's registration provides, and the FIU has demonstrated twice that it adds names to the blocking list without warning. Round one's framing of Delta as "possibly the only domestically-registered crypto options venue available to him" is **correct as stated** and remains the safer venue for anything he intends to run for more than a quarter.

**Note:** I could not open the PIB pages directly (403 on both `PressReleasePage.aspx` and `PressReseDetail.aspx`); the nine names come from search-result text citing that release, not from the release itself. Flagging this rather than implying I read it.

---

## 4. SECTION 115BBH SAME-ASSET NETTING — **CONFIRMED: transaction-level. No netting.** And the section number he is using is obsolete.

**First: 115BBH no longer exists.** The Income-tax Act, 2025 replaced the 1961 Act. The successor is **Section 194, Table Sl. No. 4**, expressly mapped in the marginal note *"[Ss. 115B, 115BB, 115BBF, 115BBG, 115BBH and 115BBJ of the 1961 Act]"*. I read this in the Income-tax Act, 2025 as amended by Finance Act 2026. Any filing or memo he writes should cite s.194 Table Sl. No. 4, not 115BBH.

**The operative text**, verbatim, Sl. No. 4 (any person; income from transfer of any VDA; 30%), conditions:

> (a) No deduction in respect of any expenditure (other than cost of acquisition, if any) or allowance or **set off of any loss shall be allowed** to the assessee under any provision of this Act **in computing the income referred to in column C**; and
> (b) no set off of loss from transfer of the virtual digital asset computed herein shall be allowed against income computed under **any provision** of this Act to the assessee and such loss shall not be allowed to be carried forward to succeeding tax years.

Two independent bars. Condition (a) forbids set-off *in computing the VDA income itself* — that is what kills same-asset netting. Condition (b) then forbids set-off against anything else. Note (b) says "any provision", not "any **other** provision"; the narrowing word is absent, which is exactly what closes the inter-VDA route.

**Three converging confirmations:**

1. **Ministerial statement.** Pankaj Chaudhary, MoS Finance, answering Karti P. Chidambaram in the Lok Sabha on 21 March 2022: *"loss from the transfer of Virtual Digital Assets (VDA) will not be allowed to be set off against the income arising from transfer of another VDA."* This is the government's own reading, given in Parliament, and it addresses the same-asset question **directly**. *(Caveat: sansad.in returned HTTP 500 on every URL pattern I tried for AU2800; this quotation is from search-result text of that answer, not from the PDF. I could not open the primary.)*

2. **The enforcement mechanism, which is the strongest evidence and which I did open.** CBDT e-Filing **ITR-2 Validation Rules, AY 2025-26, v1.0** — https://www.incometax.gov.in/iec/foportal/sites/default/files/2025-07/CBDT__e-Filing_ITR%202_Validation%20Rules_AY%202025-26_V1.0.pdf — Rule 201 and Rule 202:

   > 201. In Schedule VDA, value at Sl. No. 7 should be equal to Sl. No. 6 − Sl. No. 5
   > 202. In Schedule VDA, value at **'Total (Sum of all Positive Incomes of Capital Gain in Col. 7)'** should be equal to sum of col. 7 if head of income is selected as Capital Gain in col. 4

   The total field on the notified form is *literally labelled* "sum of all **positive** incomes". Rule 202 requires that total to equal the plain sum of column 7 — which can only hold if every row is non-negative. **The filing utility structurally cannot accept a negative row.** Reporting is transaction-wise. This is not an interpretation; it is what the software enforces.

3. **Statutory text**, above.

**Consequences, since this is resolved rather than open.** He must budget on **gross winning transactions**, not net P&L. A crypto options book that turns over frequently and finishes the year flat still generates a 30% liability on the sum of its winners, plus 1% TDS per transaction on the sell side. For a market-making or high-turnover strategy the effective tax rate on *economic* profit is unbounded — a strategy with a genuine positive edge can be tax-negative. **This does not merely reduce crypto returns; it changes which strategies are admissible.** It rules out anything with a high winner-count-to-net-P&L ratio, which is most of what he would naturally build with an SVI surface. Round one treated this as a rate question. It is a strategy-selection constraint, and it argues for concentrating his effort on NSE, where normal set-off rules apply.

**If the netting reading were wrong** (i.e. same-asset netting allowed), high-turnover crypto strategies come back into scope and the crypto leg of his programme becomes worth building. It is not wrong.

---

## 5. DEALER POSITIONING FROM OPEN INTEREST — **REFUTED as stated, but the failure opens a better door.** This is the most useful finding in the set after item 7.

Round one asserted dealer-positioning proxies are computable from OI plus a Black-Scholes gamma map. **The stated method is unidentified, and on NIFTY its standard sign convention is contradicted by NSE's own published data.**

### The identifying assumption, made explicit

The SqueezeMetrics GEX construction (white paper, March 2016, rev. 2017) computes per strike `Spot² × Γ × OI`, **call OI positive, put OI negative**. That sign convention is not a fact about the market; it is an assumption that **dealers are long every call and short every put** — equivalently, that customers sell all calls and buy all puts. OI is unsigned: every contract has a long and a short, and the exchange publishes only the total. **Nothing in an OI file distinguishes a dealer's long from a customer's long.** The convention requires, to be true:

1. Every option has a delta-hedging intermediary on one side;
2. Retail/institutional customer flow is systematically *long puts* (protection buying) and *short calls* (covered-call and overwriting programmes);
3. Net inventory is well approximated by cumulative OI rather than by signed flow.

In US index options, (2) is a defensible stylised fact grounded in the protection-buying bid. **It is the assumption that carries all the weight, and it is empirical, not structural.** Studies that actually identify dealer sign — Ni, Pearson, Poteshman and White on option trading's impact on underlying prices; Baltussen et al. on hedging demand and intraday momentum — use **signed order-flow data** (CBOE/ISE Open-Close, which flags buy-to-open vs sell-to-open), not open interest. That is the honest state of the art: sign comes from flow data, not OI.

### On NIFTY the assumption is not merely unproven — it is contradicted, and I have the primary file

**NSE publishes signed participant-category option positions daily.** This is `fao_participant_oi_DDMMYYYY.csv` in the NSE archives — e.g. https://nsearchives.nseindia.com/content/nsccl/fao_participant_oi_27082026.csv. Columns include **Option Index Call Long, Option Index Put Long, Option Index Call Short, Option Index Put Short**, by Client Type (Client, DII, FII, Pro). **There is no US equivalent at this granularity, freely published, daily.** Round one did not mention it. It is the single most valuable primary document in this round.

I downloaded three consecutive days and computed net positions (contracts):

| Date | Participant | Net calls | Net puts |
|---|---|---|---|
| 25 Aug 2026 | Client | +94,693 | **−604,022** |
| | FII | −198,430 | +549,436 |
| | Pro | +99,801 | +24,124 |
| 26 Aug 2026 | Client | +191,071 | **−663,004** |
| | FII | −235,885 | +555,751 |
| | Pro | +40,908 | +75,274 |
| 27 Aug 2026 | Client | +289,153 | **−760,983** |
| | FII | −265,856 | +626,360 |
| | Pro | −27,622 | +101,109 |

**Read the put column.** The SqueezeMetrics convention requires customers to be *net long puts*. On NIFTY, clients are net **short** puts by 600k–760k contracts, consistently and growing, while FIIs are net **long** puts and net **short** calls. The retail put leg has **the opposite sign to the US stylised fact.** Applying the standard GEX sign convention to NIFTY does not merely lack evidence — it inverts the sign of the dominant leg. Round one's "implementable framework" would have produced a gamma map with a systematically wrong sign on puts.

**Limitations of this file, stated plainly.** It is (a) aggregated across all strikes and all expiries, so it cannot build a per-strike gamma map on its own; (b) aggregated across all index options, not NIFTY alone; (c) daily EOD, not intraday; (d) "Pro" is proprietary trading members, a proxy for market makers but not identical to them. So it does **not** hand him dealer gamma. What it does is **falsify the sign assumption and give him a daily aggregate constraint** that any per-strike attribution scheme must reproduce. That is a real research instrument: fit whatever strike-level sign model he likes, then check that its aggregate matches this file. That test is free, daily, and nobody in either round proposed it.

### Has anyone shown out-of-sample value for GEX on NIFTY?

**No. This is a genuine "nobody has published on this."** I searched for peer-reviewed or replicable NIFTY-specific GEX work and found only commercial dashboards (Draconic, Vtrender, StockMojo, QuintalMind) — all of which **auto-reject** on the paid-funnel and no-cost-model criteria, and none of which disclose their sign assumption. The academic literature is entirely S&P 500.

The two items on the sign question worth his time, both S&P 500:

- **Chilingarian, *The Sign of Dealer Gamma: A Reproducible, Auditable Framework for Computing S&P 500 GEX*** — https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7131778. Formalises the sign question as a three-model taxonomy, ratifies the SqueezeMetrics OI proxy as an explicit written contract rather than a fact, fixes the aggregation formula and unit scale, distinguishes the portfolio gamma-flip root from the per-strike approximation, and identifies a reproducible software failure ("the masking test") by which sign inversions survive in production GEX code. **Tests: (1) framework is specified to be reproducible, (4) names its own failure modes — counts double, (5) reproducible on obtainable data.** *Caveat: SSRN returned 403; I have the abstract from search metadata, not the paper. He has IIT KGP access — he should open it himself before relying on it, and it is US-only, so its value to him is the sign taxonomy, not the results.*
- A pre-registered SPY backtest over 1,972 days (2018–2026) reporting that GEX/DEX/VEX/CHEX add little **after controlling for VIX and ATM IV** — the honest negative, and the correct null for anything he builds.

**If round one's claim were true**, he would have a cheap positioning signal from data he already has. **Because it is false**, the work is: (i) treat the sign as a parameter to be estimated, not assumed; (ii) use the NSE participant file as the aggregate identifying constraint; (iii) benchmark any GEX-style measure against VIX/ATM-IV controls before believing it. That is a harder project than round one implied, and a more defensible one.

---

## 6. THE SEBI STATISTIC — **CONFIRMED as to the numbers. REFUTED as to the strategy inference. And the figures are now superseded.**

### The FY25 numbers are exactly right

From the SEBI note itself (July 2025), Section C, para 18, verbatim:

> The study indicates that the net losses of individual traders widened by 41% to ₹1,05,603 crore in FY25 from ₹74,812 crore in FY24 (after accounting for transaction costs). Further, the percentage of traders making losses in EDS remained broadly unchanged at 91% from earlier study done by SEBI.

Table 11, verbatim: FY22 −40,824 / 42.7 lakh / 90.2% / −95,517 · FY23 −65,747 / 58.4 / 91.7% / −1,12,677 · FY24 −74,812 / 86.3 / 91.1% / −86,728 · **FY25 −1,05,603 / 96.0 / 91.0% / −1,10,069**. Sample: top 13 brokers, ~96 lakh unique traders of ~107 lakh market-wide.

### What it actually measures — narrower than the headline

**Realised, squared-off P&L, net of transaction costs, at PAN level, for individual traders** (resident individuals, HUFs, NRIs, sole proprietorships) at a **broker sample**, not the whole market. Open positions at year end are excluded. The category-level analysis (Section 4 of the 2026 study) is *gross* P&L on contracts expiring in the window, **before** transaction costs — a different number from the headline, and the two are routinely conflated in press coverage.

### The strategy inference is unsupported. Flatly.

Round one inferred "a large share is naive short vol." **The study cannot support that and does not attempt to.** I grepped the full text of the current study for `option buyer`, `option writer`, `short vol`, `straddle`, `strangle`, `naked`, `directional`, `strategy`. Six hits in 91 pages, none about strategy composition. The methodology section's **Table 3, "Data Fields and Sub-Categories Used in the Analysis"**, lists the complete categorisation: Product Category (Index Options, Stock Options, Index Futures, Stock Futures), Age, Income, Gender, Tier of city — plus turnover, portfolio size, trading frequency, experience, new-vs-regular, historical performance. **There is no direction field. No long/short. No buy/write. No strategy field.** The data are P&L and turnover by PAN; the sign of the position is never in the dataset.

SEBI states its own limits: *"The analysis is descriptive and does not establish cause-and-effect relationships."*

Anyone claiming the SEBI study shows retail is short vol is reading in something that is not there. It is compatible with retail being short vol, long vol, or directionally random — the study cannot distinguish them. **Ironically, the file from item 5 can**: NSE's participant-wise OI shows clients net short puts and mildly net long calls, which is *evidence* of a short-put tilt. That is the right source for that claim. The SEBI study is not.

### The figures are now stale — this is the practical finding

**SEBI, *Profitability of Individual Traders in the Equity Derivatives Segment (FY25–FY26)*, Patankar & Rath, Department of Economic and Policy Analysis, August 2026, 91pp.** Broker sample expanded 13 → 15, covering ~90% of individual traders. Headline changes:

- **FY25 net loss revised upward: ₹1.06 lakh crore → ₹1.12 lakh crore.** The number round one used is superseded.
- FY25 loss-maker share stated precisely as **90.9%**, FY26 **87.7%** (−3.2pp).
- FY26 aggregate net losses **₹91,685 crore**, down 18%; but average loss per person **rose** 2% to ₹1.17 lakh.
- Active individual traders **fell 18%**, 106.2 → 87.5 lakh — the first YoY decline since FY16. New entries −40%.
- **Options accounted for 92% of aggregate individual losses**; 93% of individuals traded **only** options.
- **23% of traders account for ~90% of total losses.**
- Loss incidence in options 87.7% vs futures 66.0%.
- **99% of FPI and proprietary profits came from "algo entities."** Top 10 prop entities took ~75% of the PROP category's gross profits.
- **Expiry-day concentration, directly relevant to him:** FY25 — 70% of index-option turnover on the expiry day itself (0DTE), 80% within 1DTE, 98% within 7DTE. FY26 — moderated to **59% / 75% / 97%**. Only 3% of turnover in contracts with >7 days to expiry; **1% beyond ten days.**

**That last block is the actionable content**, and neither round-one agent surfaced it. His SVI surface has, in practice, **one to two usable maturity points**. Beyond ~7 days there is essentially no NIFTY index-option liquidity. A term-structure strategy on NIFTY has almost nothing to trade. This should reshape what he builds before he writes a line of code — and it connects directly to item 7.

**Tests passed:** (2) explicitly nets transaction costs ✓ (3) regulator with direct access to PAN-level clearing data ✓ (5) reproducible in the sense that the aggregate inputs are published ✓. **Caveat:** broker-sample based, revised retrospectively (as FY25 was), descriptive only, and it tells him nothing whatever about *which* strategies lose.

---

## 7. THE RESIDUAL CONTRADICTION — **Both agents are partly right. Both stated the wrong mechanism. I settled it on real NIFTY data.**

This is the question that decides whether his SVI codebase contains a trade. I ran the adjudication rather than arguing it, using the NSE F&O bhavcopy for **27 August 2026** (NIFTY spot 24,090.85), 1,590 NIFTY option lines across 18 expiries.

### Agent B's "artefact" claim is CONFIRMED — but not for the reason given

Agent B blamed tick quantization, zero bids, and settlement prices from a fitted surface. **The settlement-price mechanism is real and large. The tick-quantization mechanism is quantitatively wrong in the range that matters.**

**Finding 1 — half the chain does not trade.** 821 of 1,590 NIFTY option lines (**51.6%**) had **zero volume** on the day. Per near expiry: 26–28% zero-volume even in the front three expiries.

**Finding 2 — untraded settlement prices are model output, and it is visible in the last digit.** NSE option ticks are Rs 0.05, so any genuine trade price lies on the 5-paise grid. Testing that grid:

| | n | settlement on the Rs 0.05 grid | ClsPric ≠ SttlmPric |
|---|---|---|---|
| Traded (vol > 0) | 769 | **90.5%** | 12% |
| Untraded (vol = 0) | 821 | **20.6%** | **100%** |

**79.4% of untraded settlement prices are off the tick grid entirely** — they cannot be observed prices. Examples: `NIFTY2691523550PE` close 133.00, settle **125.87**, vol 0. `NIFTY2690125900PE` close 1500.00, settle **1787.67**, vol 0. NSE Clearing confirms the method in principle: Black-Scholes with an assumed volatility is used to price contracts not traded, and the base price of newly introduced option contracts is "the theoretical value … based on the Black-Scholes model."

**Finding 3 — the imputation signature, which is the decisive exhibit.** On the 29 Sep 2026 expiry (T = 33d), four consecutive call strikes with **zero volume**:

| Strike | Volume | Settle | Implied vol |
|---|---|---|---|
| 25600 | 4,703 | 11.95 | **11.22%** |
| 25850 | **0** | 52.48 | 17.30% |
| 26100 | **0** | 34.02 | 17.21% |
| 26350 | **0** | 21.49 | 17.13% |
| 26600 | 162 | 3.55 | **14.11%** |
| 26850 | **0** | 7.93 | 17.00% |

The zero-volume strikes return **17.30, 17.21, 17.13, 17.00** — a near-constant, monotone, near-flat vol sequence — sitting **5–6 vol points above** their traded neighbours at 25600 and 26600. That is not a smile. **That is a flat-vol model writing its own answer into the data**, and it is exactly the failure agent B described. Fit SVI to a chain containing those rows and you will fit NSE's constant-volatility assumption in the wings and then discover a "residual" that is your own model disagreeing with theirs.

### Agent A's "residual is the surviving signal" claim is REFUTED as stated, but the tick objection against it fails

I computed, for every OTM strike, the IV uncertainty implied by **half a tick** (Rs 0.025) via `ΔIV = 0.025 / vega`:

**5-day expiry (1 Sep 2026), across the whole wing |k| ≤ 0.12:** half-tick IV uncertainty runs **0.00 to 0.17 vol points**. At k = −0.091 (22000 PE, settle 0.80, volume 64,558) it is **0.09** vol points against an IV of 28.66%. At k = +0.121 (27200 CE, settle 0.45, volume 22,247) it is **0.17** vol points against an IV of 34.96%.

Across that same wing the IV ranges from **6.4% to 33%**. **A half-tick is under 0.5% of the structure being measured.** Tick quantization is *not* what makes wing IVs unreliable in the liquid range. Agent B's stated mechanism is wrong on the numbers; the right mechanism is imputation and absent volume. Also note: **zero contracts settled at or below Rs 0.05** on the front expiry — the "zero bid" concern does not bind at EOD either.

But agent A is still refuted, for a different reason: **a residual measured against a surface fitted to a chain that is half imputed is not a market signal.** The signal and the contaminant are not separable at EOD.

### The adjudication, and the protocol that makes it testable

**His SVI codebase is infrastructure, not a trade — as currently fed.** It becomes a candidate trade only under filters that neither agent specified. Concretely:

**Quote-quality filters (all mandatory, all falsifiable):**
1. **Drop every strike with zero traded volume in the bar.** This alone removes ~52% of the EOD chain and all of the imputation signature.
2. **Never fit to `SttlmPric` or `ClsPric`.** Both are contaminated for untraded strikes; `ClsPric` is additionally stale. Fit to **intraday two-sided quotes** — which is precisely what his incoming minute-wise data provides and what the EOD bhavcopy structurally cannot.
3. **Require a two-sided quote with bid > 0** and a relative spread below a pre-registered threshold — set it from the data, not from taste.
4. **Screen on the tick grid as a cheap integrity check:** any "price" off the 5-paise grid in an intraday feed is imputed or erroneous. This is a free, decisive filter and it should run permanently.

**Moneyness and maturity range:**
5. **|log-moneyness| ≤ ~0.10 on the front weekly**, widened only where measured volume supports it. Beyond that, volume collapses (27200 CE: 22,247 contracts; 26600 CE: 1,645) and quote-driven IV noise grows non-linearly.
6. **Maturity: the front one or two expiries only.** Per SEBI FY26, 97% of index-option turnover is within 7 days of expiry and **1% beyond ten days**. There is no NIFTY term structure to trade. Any calendar or term-structure residual strategy is untradeable on this venue — that is a hard finding, and it kills a whole class of ideas cheaply.

**Error-bar construction — the part that decides everything:**
7. The error bar must be **the quoted bid-ask mapped into vol space** (`ΔIV = half-spread / vega`), **not** the half-tick. My computation shows the half-tick is 0.00–0.17 vol points; the *quoted spread* in the wings will be one to two orders of magnitude larger, and it is the quantity that determines whether a residual is real and, separately, whether it is capturable. Compute both; report both.
8. **Add a vega-weighted fit-uncertainty term.** An SVI slice fitted to n quotes has parameter uncertainty; the residual at strike k must be compared against the *combined* quote uncertainty and fit uncertainty at k, not against quote uncertainty alone. Round one's framing of "residual versus error bar" omitted the second term entirely, which is how a fitted-surface artefact gets mistaken for signal.

**The falsification test — pre-register it before looking:**

> **The residual is signal if, and only if, the sign of today's residual at strike k predicts the sign of tomorrow's change in that strike's mid-IV, out of sample, after subtracting the round-trip half-spread at that strike, on strikes that passed filters 1–6.**

Three specific ways it dies, and he should check each:
- **It reverses.** The residual predicts *mean reversion of the fit*, not of the market — i.e. it forecasts its own next-period recalibration. Test by re-fitting with a different SVI parameterisation (raw vs SVI-JW) and checking the residual survives. If it is parameterisation-dependent, it is an artefact of his own model.
- **It is real but uncapturable.** The residual is smaller than the half-spread at every strike where it is statistically distinguishable from zero. **This is the modal outcome, and it is exactly what Vilkov's correction turned out to be** — the entire 0DTE result set inverted on a cost term two orders of magnitude smaller than a NIFTY wing spread. He should expect this and design to detect it early rather than discovering it after six months.
- **It is a liquidity proxy.** The residual is largest precisely where volume is lowest, meaning he has rediscovered the illiquidity premium. Test by regressing residual magnitude on contemporaneous volume and spread; if those two regressors absorb it, there is nothing left.

**What changes on the answer.** If the residual survives all three, his existing SVI/SSVI work is the core of a trade and everything else is plumbing. If it does not, the codebase is still worth having — as the surface that prices and risk-manages positions he takes for other reasons — but it is **not** the alpha, and he should stop treating it as such. **On the evidence available at EOD, I cannot resolve this, and neither could either round-one agent: the question is genuinely intraday-only.** His incoming minute-wise NIFTY data is the correct and possibly the only instrument. That is the good news — the decisive experiment is one he can actually run, in weeks, and the pre-registered falsification above is the whole specification.

---

## Summary of verdicts

| # | Claim | Verdict |
|---|---|---|
| 1 | Vilkov 0DTE correction notice | **CONFIRMED** — but "no *materially* positive net Sharpe"; Risk Reversal survives at +0.10 |
| 2 | LRS permits US-listed options | **REFUTED** — OI Directions 2022 def. (ix)(a)(iii) excludes derivatives from OPI; IFSC does not cure it |
| 3 | Delta Exchange India registration / depth | **Registration: first-party only** (no public FIU register exists). **Depth: UNRESOLVABLE** — API unreachable. Deribit: not restricted, not registered |
| 4 | 115BBH same-asset netting | **CONFIRMED transaction-level.** Also: now s.194 Table Sl. No. 4, Income-tax Act 2025 |
| 5 | Dealer positioning from OI | **REFUTED** — sign unidentified; NSE participant data shows clients net **short** puts, inverting the US convention. No NIFTY GEX study exists |
| 6 | SEBI FY25 statistic | **Numbers CONFIRMED. Strategy inference REFUTED** (no direction field exists). **Superseded** by SEBI Aug 2026: FY25 revised to ₹1.12 lakh crore |
| 7 | SVI residual vs artefact | **Split.** Artefact confirmed via *imputed settlement prices* (79.4% of untraded settles off the tick grid), not tick quantization (≤0.17 vol pts, <0.5% of signal). Testable only intraday |

## Highest-value new primary sources found this round

1. **NSE participant-wise open interest**, daily, signed by category — `https://nsearchives.nseindia.com/content/nsccl/fao_participant_oi_DDMMYYYY.csv`. Free, daily, no US equivalent at this granularity. Refutes the GEX sign convention on NIFTY and gives an aggregate constraint for any strike-level attribution model. *Tests: (2) real positions not modelled, (3) exchange-generated, (5) trivially obtainable.*
2. **`vilkovgr/0dte-strategies` KNOWN-ISSUES.md** — the best-documented cost-scale failure in the public options literature, including the target-relabelling trap. *Tests: (1)(2)(4)✕2(5).*
3. **SEBI, *Profitability of Individual Traders in the EDS (FY25–FY26)*, August 2026** — supersedes the FY25 figures and contains the 0DTE/1DTE/7DTE turnover concentration that bounds his tradeable maturity set. *Tests: (2)(3)(5).*
4. **FEM (Overseas Investment) Directions, 2022, definition (ix)** — the single clause that decides the US-venue question, and the one every secondary source paraphrases wrongly.
5. **CBDT ITR-2 Validation Rules AY 2025-26, Rules 201–202** — the VDA netting question answered by what the filing utility structurally enforces rather than by interpretation.

## What I could not verify, stated plainly

- **Delta Exchange India order-book depth** — API returned `HTTP 000` on six attempts. A scratchpad snapshot of ambiguous provenance (contains XAUT, suggesting the global venue) shows a **1.7% median relative spread**; I decline to attribute it to Delta India. He must measure this himself, and it is the highest-priority ten minutes of work in the crypto leg.
- **FIU-IND registration register** — no public searchable register exists. Delta's VA00041101 is a self-declaration corroborated only by aggregate counts in Parliament answers.
- **Lok Sabha AU2800 of 21.03.2022** — sansad.in returned HTTP 500 on every URL pattern. The ministerial quotation is from search-result text of that answer, not the PDF.
- **PIB releases PRID 1991372** — 403 on both URL forms. The nine-name list is from citing sources, not the release.
- **SSRN 7131778 (Chilingarian)** — 403. Abstract only. He has IIT KGP access and should open it himself.
- **NCL Consolidated Circular, F&O segment, Part B Item 4** — the exact option settlement-price formula. The NCL Settlement FAQ cross-references it for currency and commodity segments but not equity derivatives. **My empirical tick-grid test (79.4% of untraded settlements off the 5-paise grid, 100% differing from close) is stronger evidence than the circular text would have been**, so I stopped chasing it — but the formula itself remains unread.