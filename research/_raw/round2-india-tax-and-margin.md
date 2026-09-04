# The Full Indian Arithmetic: F&O vs VDA, and Margin as a Simulable Object

**Everything below is computed from primary documents I opened in this session.** Where I could not reach the primary document I say so in the source line rather than substituting a blog. Live market data used throughout is NSE's own 28-Aug-2026 files.

**One correction up front that changes the premise:** the Income-tax Act, 2025 (Act 30 of 2025) commenced 1 Apr 2026 **and** the Finance Act, 2026 (assent 30 Mar 2026) raised derivative STT again — options 0.10% → **0.15%**, futures 0.02% → **0.05%**, exercise 0.125% → **0.15%**, all w.e.f. 1 Apr 2026. Round one's Oct-2024 STT numbers are one revision stale. Every arithmetic figure below uses the current rates.

---

## PART 0 — THE SOURCE SET

### 0.1 Income-tax Act, 2025 — official Gazette text (Act 30 of 2025)
**URL:** `https://egazette.gov.in/WriteReadData/2025/265620.pdf` (572 pp; mirrored byte-identical at `https://resource.cdn.icai.org/87647dtc-aps2139-inceome-tax-act-2025.pdf`)
**Gives him:** every section number he needs, in the operative Act, not a summary. Presidential assent 21 Aug 2025; commencement 1 Apr 2026.
**Tests passed:** (3) the enacting authority itself; (5) reproducible — it is the law; (4) it names its own boundaries (each set-off section states exactly what it does *not* permit).
**Caveat:** this is the as-enacted gazette. The Department's "as amended by Finance Act 2026" PDF (`https://www.incometaxindia.gov.in/documents/d/guest/income_tax_act_2025_as_amended_by_fa_act_2026-pdf`) returns **HTTP 403 to non-browser clients** — I could not open it. I closed that gap instead by reading the Finance Bill 2026's own amendment clauses (below) and confirming that **ss. 66(31), 66(33), 108–113, 121, 194 and 393(1) Table Sl.8(vi) are untouched** by FA 2026. FA 2026 amends s.66 only at clause (4) (definitions of commodities transaction tax), and s.58 only by omitting s.58(11)(a)(i).

### 0.2 Finance Bill / Act 2026
**URL:** `https://www.indiabudget.gov.in/doc/Finance_Bill.pdf` (Bill No. 3 of 2026)
**Gives him:** Clause 143 — the operative STT amendment, verbatim: *"In the Finance (No.2) Act, 2004, in section 98, in the Table, against serial number 4, — (i) against entry (a)… for '0.1 per cent.', '0.15 per cent.'; (ii) against entry (b)… for '0.125 per cent.', '0.15 per cent.'; (iii) against entry (c)… for '0.02 per cent.', '0.05 per cent.'"* Also the full arrangement-of-clauses list of which ITA-2025 sections FA 2026 touched.
**Tests:** (3), (5).
**Caveat:** it is the Bill as introduced. The enacted position is confirmed independently by NSE's tax circular (0.4) which cites assent on 30 Mar 2026.

### 0.3 NSE Clearing — Securities Transaction Tax (mechanics)
**URL:** `https://www.nseclearing.in/clearing-settlement/equity-derivatives/securities-transaction-tax` (updated 01/08/2025)
**Gives him, verbatim:** *"STT is applicable on all sell transactions for both futures and option contracts. For the purpose of STT, each futures trade is valued at the actual traded price and option trade is valued at premium. In case of final exercise of an option contract, STT is levied on intrinsic value if the option contract is in-the-money on the day of expiry."* Plus the **STT report file spec** he can parse: `F_STT01_DDMMYYYY.CSV` in `/FAOFTP/F/REPORTS`, record types 10/20/30/40 — type 30 gives per-client, per-contract taxable sell value split futures/options; type 40 gives exercise quantity, exercise value, taxable exercise value.
**Tests:** (2) it *is* the cost specification; (3) the CC that levies it; (5).
**Caveat:** the rate table is on the NSE (not NSE Clearing) page; this page carries only the method.

### 0.4 NSE rate table + NSE tax circular NSE/FATAX/73524
**URLs:** `https://www.nseindia.com/static/products-services/equity-derivatives-securities-transaction-tax` (updated 01/04/2026) and `https://nsearchives.nseindia.com/content/circulars/FATAX73524.pdf` (31 Mar 2026)
**The table, exactly:**

| Sl | Taxable securities transaction | Rate w.e.f. 1-Apr-2026 | Rate upto 31-Mar-2026 | Payable by | Value on which levied |
|---|---|---|---|---|---|
| 4(a) | Sale of an option in securities | **0.15%** | 0.10% | **Seller** | option premium |
| 4(b) | Sale of an option in securities, where option is exercised | **0.15%** | 0.125% | **Purchaser** | **intrinsic value** = settlement price − strike |
| 4(c) | Sale of a futures in securities | **0.05%** | 0.02% | **Seller** | actual traded price |
| 3 | Sale of equity share settled otherwise than by delivery | 0.025% | 0.025% | Seller | trade value |
| 1/2 | Delivery-based purchase / sale of equity share | 0.1% each | 0.1% | Purchaser / Seller | trade value |

**Tests:** (2) doubly; (3); (5).
**Caveat:** none — this is the definitive levy table and the circular names the enacting statute and assent date.

### 0.5 NSE/FATAX/41919, 20 Aug 2019 — the exercise-base change
**URL:** `https://nsearchives.nseindia.com/content/circulars/FA64232.pdf` (identical text also archived as the 2019 FATAX circular)
**Gives him:** *"With effect from September 1, 2019 where option is exercised, STT at the prescribed rate shall be levied on the 'intrinsic value' instead of the settlement price as at present."*
**Why it matters:** this is the document that kills the folklore. See §A.6.

### 0.6 NSE/FA/73061, 27 Feb 2026 — transaction charges
**URL:** `https://nsearchives.nseindia.com/content/circulars/FA73061.pdf`, effective **1 Mar 2026**

| Segment | Transaction charge | IPFT | Total, each side |
|---|---|---|---|
| Cash market | ₹306.99/cr | ₹0.01/cr | **₹307 per crore** |
| Equity futures | ₹182.99/cr | ₹0.01/cr | **₹183 per crore** of traded value |
| Equity options (**on premium**) | ₹3,552.99/cr | ₹0.01/cr | **₹3,553 per crore** of premium |

**Tests:** (2), (3), (5). **Caveat:** these are charges to the *trading member*; your broker may or may not pass through exactly.

### 0.7 SEBI Master Circular for Stock Exchanges & Clearing Corporations, **Chapter 5 — Exchange Traded Derivatives** (213 pp)
**Gives him:** the complete, literal SPAN specification India runs — the 16-scenario table, PSR/VSR definitions, ELM rates, calendar-spread treatment, expiry-day tail-risk add-on, liquid-asset composition, and the peak-margin verification framework with its phased 25/50/75/100% adoption. This is §D's backbone.
**Tests:** (2), (3), (4) — it explicitly enumerates where each margin stops covering risk; (5).
**Caveat:** the copy I read is the consolidated chapter; individual measures cite their originating circulars in footnotes (e.g. SEBI/HO/MRD2/DCAP/CIR/P/2020/27 for ELM and PSR floors, SEBI/HO/MRD2/DCAP/CIR/P/2020/127 for peak margin) and those are the citations to use.

### 0.8 NSE Clearing FAQ — Risk Management
**URL:** `https://www.nseclearing.in/sites/default/files/2025-01/NCL%20-%20FAQ%20RISK%20MANAGEMENT.pdf` (26 pp)
**Gives him the operational facts the Master Circular omits:** SPAN file run times, the exact ELM ladder, the additional-margin triggers, and — crucially for a backtester — *"The computation of the margin requirement of SPAN+ELM (both intra-day and EOD) … shall be based on the **fixed Beginning of Day (BOD) margin parameters**."*
**Tests:** (2), (3), (4) — it states the penalty formula for getting it wrong; (5).
**Caveat:** an FAQ, not a rulebook; it summarises circulars it does not always name.

### 0.9 ICAI Guidance Note on Tax Audit under Section 44AB (Revised 2025), 589 pp
**Gives him:** ¶5.11 — the only authoritative statement of how derivative *turnover* is computed. See §A.4.
**Tests:** (3) written by the profession that signs the audit report; (4) it explicitly bounds its own applicability; (5).
**Caveat:** it is a Guidance Note, not law, and it says so: *"the method of computation of turnover/gross receipts provided here is solely for the purpose of determining applicability of section 44AB and does not alter the treatment of such transactions for income."*

### 0.10 Live NSE data files (all anonymously downloadable, all machine-readable)

| File | URL pattern | What it gives |
|---|---|---|
| Market lot | `https://nsearchives.nseindia.com/content/fo/fo_mktlots.csv` | current lot size per underlying per expiry month |
| Daily volatility | `https://nsearchives.nseindia.com/archives/nsccl/volt/FOVOLT_DDMMYYYY.csv` | EWMA daily & annualised vol, underlying and futures, per symbol — **the exact σ that feeds PSR and VSR** |
| UDiFF F&O bhavcopy | `https://nsearchives.nseindia.com/content/fo/BhavCopy_NSE_FO_0_0_0_YYYYMMDD_F_0000.csv.zip` | OHLC, settlement price, OI, lot size, underlying price, per contract |
| Settlement prices | `https://nsearchives.nseindia.com/archives/nsccl/sett/FOSett_prce_DDMMYYYY.csv` | the number that determines exercise-STT intrinsic value |
| Collateral haircuts | `.../content/equities/APPSEC_COLLVAL_DDMMYYYY.csv`, `.../archives/fo/mf_haircut/MF_VAR_DDMMYYYY.csv` | haircuts for the non-cash half of margin |
| Circular index (JSON) | `https://www.nseindia.com/api/circulars?fromDate=DD-MM-YYYY&toDate=DD-MM-YYYY` | every circular with a direct PDF link — how I found the STT and lot-size circulars |

Requires a cookie bootstrap (`GET https://www.nseindia.com/` first) and a browser User-Agent; nothing else.
**Tests:** (1) machine-consumable; (2); (3); (5).
**Caveat:** the FOVOLT vol is a *daily EWMA with λ implied by* `sqrt(0.995·D² + 0.005·C²)` — the header states the formula, so the recursion is exactly reproducible, but it is the **underlying's** realised vol, not the option-implied surface.

---

## PART A — NSE INDEX F&O TAX TREATMENT, FROM THE STATUTE

Section numbers below are **Income-tax Act, 2025**. The 1961-Act equivalent is given in brackets once.

### A.1 Non-speculative status — s.66(31) read with s.66(33) [old s.43(5)(d)]

s.66(31) defines "speculative transaction" as settlement otherwise than by actual delivery, **"other than the following transactions:— (a) a specified derivative transaction as defined in clause (33)"**.

s.66(33): a *specified derivative transaction* means any transaction in respect of trading in derivatives referred to in **s.2(ac) SCRA 1956**, provided it is
- (a) carried out **(i)** through a SEBI-registered stock broker or intermediary, or **(ii)** by banks or mutual funds, **electronically on screen-based systems of a recognised stock exchange**; and
- (b) supported by a **time-stamped contract note** stating **(i)** the unique client identity number and **(ii)** the PAN.

**Note what is *not* required:** unlike the commodity-derivative limb of the same clause, the equity-derivative limb does **not** condition non-speculative status on the transaction being chargeable to STT. Screen-based + broker + time-stamped contract note with UCC and PAN is the whole test.

**Consequence:** NIFTY/BANKNIFTY futures and options are **business income under "Profits and gains of business or profession"**, not speculation business, not capital gains.

s.26(3) is the companion: *"Where speculative transactions carried on by an assessee are of such nature to constitute a business, the business … shall be deemed to be distinct and separate from any other business."* Since exchange-traded index F&O is carved out of s.66(31), it never enters that ring-fence. **Intraday cash-equity trading does** — and it is a separate, worse regime (§A.3).

### A.2 Expense deductibility

- **s.34(1)** [old s.37(1)]: any expenditure not capital, not personal, **"laid out or expended wholly and exclusively for the purposes of the business"** is allowed. Brokerage, exchange transaction charges, IPFT, GST on those, data feeds, VPS/colocation, terminal charges, internet, depreciation on the trading rig, interest on borrowed trading capital — all deductible in computing PGBP.
- **s.32(1)(k)** [old s.36(1)(xv)]: **STT itself is deductible**, provided (i) the taxable securities transactions are entered into in the course of the business, and (ii) the income from them is included under PGBP. Both hold for an F&O business.
- **Contrast, s.72(3)(b):** STT is expressly **not** deductible when computing capital gains. So the moment you are classified as an investor rather than a business, your largest cost stops being deductible.

### A.3 Set-off and carry-forward — the full ladder

| Provision | Rule |
|---|---|
| **s.108(1)** [old 70] | Loss from one source set off against income from any other source **under the same head**. So a losing NIFTY book nets against a winning BANKNIFTY book, and against any other business income, automatically. |
| **s.109(1)** [old 71] | Business loss set off against income under **any other head, including "Capital gains"** — **except** s.109(1)(a): *"loss under the head 'Profits and gains of business or profession' shall not be set off against income assessable under the head 'Salaries'."* |
| **s.109(2)** | Capital-gains loss can **never** go against another head. (Asymmetric: business loss → capital gains is allowed; the reverse is not.) |
| **s.112(1)–(2)** [old 72] | Unabsorbed business loss carried forward, set off **only against profits of any business or profession**, for **not more than eight tax years**. |
| **s.113** [old 73] | Speculation loss (intraday cash equity) set off **only against speculation profits**, carry-forward **four tax years**. |
| **s.121** [old 80] | *"no loss which has not been determined in pursuance of a return filed under section 263(1) shall be carried forward and set off under section 111(1) or 112(1) or 113(2) or 114(2) or 115(2)."* **File by the due date or the loss is gone permanently.** |
| **s.263(1)(c) Table** | Due date: audited person or partner of an audited firm → **31 October**; any other assessee → **31 July**; transfer-pricing cases → 30 November. |

**The salary carve-out is the live constraint for him.** A salaried quant with an F&O book cannot use trading losses against salary in the loss year. He can use them against interest, rent, capital gains, or other business income; otherwise they wait up to eight years for trading profits.

### A.4 Turnover computation for derivatives, and the audit thresholds

**ICAI Guidance Note (Revised 2025), ¶5.11(b)** — the operative text:

> *(i) The total of favourable and unfavourable differences in case of squared off transactions shall be taken as turnover.
> (ii) **Premium received on sale of options is also to be included in turnover.** However, where the premium received is included for determining net profit for transactions, then such net profit should not be separately included.
> (iii) In respect of any reverse trades entered, the difference thereon, should also form part of the turnover.
> (iv) In case of an open position as at the end of the financial year …, the turnover … should be considered in the financial year when the transaction has been actually squared off.
> (v) In case of delivery based settlement in a derivatives transaction, the difference between the trade price and the settlement price shall be considered as turnover.*

**This matters enormously to an option seller.** Turnover ≈ Σ|per-trade P&L| **plus** the gross premium written. A book selling 8 NIFTY straddles a week (real prices, §D) writes ₹47.8 lakh of premium a year before a single rupee of P&L is counted. Scale it 3× and you are at ₹1.5 crore of "turnover" on a ₹25 lakh account.

**s.63 — tax audit** [old s.44AB]:
- s.63(1) Table Sl.1(a): audit required if **total sales, turnover or gross receipts exceed ₹1 crore**;
- **s.63(1)(b): substituted to ₹10 crore** where (i) cash *receipts* ≤ 5% of aggregate receipts **and** (ii) cash *payments* ≤ 5% of aggregate payments. A trader whose entire flow is bank-to-broker satisfies both. **His effective audit threshold is ₹10 crore, not ₹1 crore.** (s.63(5)(b): a non-account-payee cheque counts as cash.)
- s.63(1) Table Sl.2: audit *also* required if he opts out of presumptive taxation and declares profits **lower than** the deemed profits.
- s.63(5)(a): audit report due **one month before** the s.263(1) due date, i.e. **30 September**.

### A.5 The presumptive-taxation trap — s.58 [old s.44AD]

- **s.58(2) Table Sl.1:** an *eligible assessee* with turnover ≤ **₹2 crore** (or ≤ **₹3 crore** where cash receipts ≤ 5%) may declare deemed profits of **6% of turnover received by banking/online mode + 8% of the rest**, or actual profit, **whichever is higher**.
- **s.58(11)(a):** *eligible assessee* = resident individual / HUF / non-LLP firm who does not carry on a specified profession, does not earn commission or brokerage, and carries on no agency business. **A proprietary derivatives trader is eligible.** (FA 2026 clause 32 deleted the further condition in s.58(11)(a)(i).)
- **s.58(4):** *"Any loss, allowance or deduction allowable under the provisions of this Act shall not be allowed against the income computed in the manner specified in sub-section (2)."* No costs, no depreciation, no carry-forward set-off.
- **s.58(3):** if you claim actual profits **lower** than the deemed figure **and** your total income exceeds the exemption limit, you **must** keep books (s.62) **and** get audited (s.63).
- **s.58(7) — the trap proper:** *"Where an eligible assessee declares profit … as per sub-section (2) … and he declares profit for any of the **five** tax years succeeding such tax year in contravention …, he shall not be eligible to claim the benefit of the provisions of this section for **five tax years** subsequent to the tax year in which the profit has not been declared."*
- **s.58(8):** once s.58(7) bites and total income exceeds the exemption limit, **books + audit become compulsory**.
- **s.408(2):** a presumptive assessee pays **the whole advance tax by 15 March** (single instalment).

**Why this is a trap for an options seller specifically.** Turnover under the ICAI method includes written premium, which bears no relation to profit. Declare 6% of a ₹2 crore turnover and you have declared ₹12 lakh of income on a book that may have lost money. Decline to declare it in a later year — as any honest loss year forces you to — and s.58(7) locks you out of s.58 for five years while s.58(8) forces audit. It is a one-way door.

### A.6 STT: premium vs intrinsic-value-at-exercise — **the folklore is now false, and the primary documents say exactly when it died**

Three regimes, from the primary record:

1. **Before 1 Sep 2019.** s.98 entry 4(b) levied 0.125% on the **settlement price × quantity** — the *full notional* of the exercised option. A NIFTY 24,200 call ₹50 in-the-money at a 24,250 settlement attracted STT of 0.125% × 24,250 × 65 ≈ **₹1,970 on a contract worth ₹3,250**. That is the massacre everyone remembers, and it was real.
2. **1 Sep 2019 – 31 Mar 2026.** NSE/FATAX/41919 (20 Aug 2019): Finance (No.2) Act 2019 changed the value of the 4(b) transaction to **"the difference between the settlement price and the strike price"** — intrinsic value. The base collapsed by ~500×. A rate gap remained: exercise 0.125% vs sale 0.10% (0.0625% before Oct 2024) — so letting an ITM long expire cost 25%–100% more STT than selling it.
3. **From 1 Apr 2026.** Finance Act 2026 set **both entries to 0.15%**. Sale of an option: 0.15% of **premium**, paid by the seller. Exercise: 0.15% of **intrinsic value**, paid by the **purchaser**.

**The arithmetic that follows, and it inverts the standard advice:**

At expiry an ITM option's market price ≥ its intrinsic value (equal only at the bell). So for the holder of a long ITM option:

- Sell it in the market → STT = 0.15% × **premium** × qty, and premium = intrinsic + residual time value.
- Let it be exercised → STT = 0.15% × **intrinsic** × qty.

**Exercise is now weakly cheaper on STT than sale, and strictly cheaper whenever any time value remains.** The "always square off before expiry to dodge exercise STT" rule is a 2019-era artefact. What still argues for squaring off is *settlement-price risk* (the exercise base is the closing-half-hour VWAP-derived settlement price, not your fill) and the **delivery-margin ladder** for stock derivatives (§D.7) — not STT.

**The one asymmetry that survives:** exercise STT falls on the **purchaser**, who paid no STT on entry. A long ITM position therefore carries a 15 bp exit tax on intrinsic that a naive P&L model omits entirely. On a synthetic long built from a deep ITM call — long 22,000 CE with NIFTY at 24,176, intrinsic 2,176 — that is 0.15% × 2,176 × 65 = **₹212 per lot**, every expiry, forever, on a 1.35% of notional position.

### A.7 Advance tax — ss.403–408, 424, 425

- **s.404:** advance tax payable if the amount is **₹10,000 or more**. F&O business income has no TDS against it, so effectively 100% of the liability must be prepaid.
- **s.408(1) Table:** ≥15% by **15 Jun**, ≥45% by **15 Sep**, ≥75% by **15 Dec**, 100% by **15 Mar**. (Presumptive assessees: 100% by 15 Mar, s.408(2).)
- **s.424** [old 234B]: if advance tax paid < **90% of assessed tax**, simple interest **1% per month** from 1 April following the tax year until determination.
- **s.425** [old 234C]: shortfall against each instalment threshold carries **3%** per period (Sl.1: 15% due by 15 Jun, etc.).

**The structural problem this creates for a trading book, and no blog states it:** you must estimate the *whole year's* P&L by 15 June to get the first instalment right. A book that makes its money in Q4 overpays; a book that gives back Q1 profits in Q4 has prepaid tax on income that no longer exists and gets it back as a refund a year later. **Advance tax converts a volatile P&L into a working-capital problem.** The s.109(1)(a) salary carve-out compounds it: a salaried trader cannot even net a Q3 trading loss against salary already taxed at source.

### A.8 The complete cost stack, per round trip

Using the Feb-2026 charges, Apr-2026 STT, and NIFTY lot 65:

**Index options** (per ₹1 of one-way premium turnover):

| Component | Rate | bps of one-way premium |
|---|---|---|
| STT (sell leg only) | 0.15% of premium | **15.00** |
| Exchange txn + IPFT, both sides | ₹3,553/cr × 2 | **7.11** |
| GST @18% on exchange charges | — | **1.28** |
| Stamp duty (buy leg) | 0.003% of premium *(unverified — see §0 negatives)* | 0.30 |
| SEBI turnover fee *(unverified)* | ~₹10/cr × 2 | 0.02 |
| **Regulatory total, round trip** | | **≈ 23.7 bps of premium** |
| Brokerage | broker-specific; ₹20/order is the discount-broker standard | + |

Pre-1-Apr-2026 the same stack was ≈ 18.7 bps. **The Finance Act 2026 raised the option round-trip floor by 27%.**

**Index futures** (per ₹1 of notional):

| Component | bps of notional, round trip |
|---|---|
| STT 0.05%, sell leg only | **5.00** |
| Exchange ₹183/cr × 2 | **3.66** |
| GST @18% | **0.66** |
| Stamp 0.002% (buy) *(unverified)* | 0.20 |
| **Total** | **≈ 9.5 bps** |

Pre-Apr-2026: ≈ 6.5 bps. **Futures round-trip cost rose 46%.**

**The consequence he actually needs.** A short NIFTY weekly straddle collects ₹11,495 per lot on ₹15,71,417 of notional (real 28-Aug-26 prices). One full round trip of that notional in futures costs 9.5 bps × ₹15,71,417 = **₹1,493 — 13.0% of the premium collected.** Delta-hedging that straddle with total hedge turnover of 2× position notional over its life burns **26% of the premium**. Three round trips of notional and the trade is a coin-flip before you have priced a single Greek. **The Finance Act 2026 futures STT hike is, functionally, a tax on delta-hedging.**

---

## PART B — THE VDA REGIME, CURRENT SECTION NUMBERING

### B.1 The charge — s.194(1), Table Sl. No. 4

Not s.115BBH any more. The operative provision is **s.194(1) of the Income-tax Act, 2025, Table serial number 4**, reproduced verbatim from the Gazette:

| A (Sl) | B (Person) | C (Income) | D (Rate) | E (Conditions) |
|---|---|---|---|---|
| 4 | Any person | Any income from the transfer of any virtual digital asset | **30%** | **(a)** No deduction in respect of any expenditure (**other than cost of acquisition, if any**) or allowance **or set off of any loss** shall be allowed to the assessee under any provision of this Act in computing the income referred to in column C; and **(b)** no set off of loss from transfer of the virtual digital asset computed herein shall be allowed against income computed under any provision of this Act to the assessee and such loss shall **not be allowed to be carried forward** to succeeding tax years. |

Plus **s.194(2)(n):** *"for the purposes of sub-section (1) (Table: Sl. No. 4), the term 'transfer' as defined in section 2(109), shall apply to any virtual digital asset, whether capital asset or not."* — the provision that stops you re-characterising a trading book as business income.

VDA itself is defined at **s.2(111)**. Effective rate with 4% health & education cess: **31.2%**, plus surcharge where applicable.

**Two independent prohibitions.** Column E(a) blocks netting *inside* the computation. Column E(b) blocks netting *outside* it and blocks carry-forward. Together they are the statutory basis for the transaction-level application your sibling agent established — the words are there in the Act.

### B.2 The withholding — s.393(1), Table Sl. No. 8(vi)

Not s.194S any more. From the Gazette:

> **8(vi)** *Any sum by way of consideration for transfer of a virtual digital asset.* — Payer: **Any person**. — **Rate: 1%**. — **Threshold limit: Nil.**

Exemptions sit in **s.393(4) Table Sl. No. 12**: ₹50,000 for a specified individual/HUF (turnover ≤ ₹1 crore business / ₹50 lakh profession, or no PGBP income); **₹10,000 for everybody else**.

**Note 6 to s.393(1)** handles in-kind consideration: where the consideration *"is in exchange of another virtual digital asset"*, or is wholly or partly in kind and the cash part is insufficient, **the payer must ensure the tax has been paid before releasing the consideration.** Crypto-for-crypto legs are inside the net.

**FA 2026 confirmation:** clause 72 amends s.393 only at sub-section (1) Sl.3 Note 3, sub-section (4) Sl.7, and sub-sections (6)–(7). **Sl. No. 8(vi) is untouched — 1% stands.**

### B.3 The genuine open question I could not close

**s.393(1) Sl.8(vi) taxes "consideration for transfer of a virtual digital asset."** A cash-settled perpetual or option on a VDA is not, on the face of the words, a transfer *of* a VDA. Whether 1% TDS attaches to VDA **derivatives** is not answered by the statutory text and I found no CBDT circular resolving it in this session. **I am flagging this as unresolved rather than asserting either answer.** The arithmetic in Part C is therefore run twice: with and without TDS. The no-loss-offset half of the regime applies regardless, because s.194(1) Sl.4 column C is "any income from the transfer of any virtual digital asset" and s.194(2)(n) extends "transfer" beyond capital assets.

---

## PART C — THE TWO REGIMES SIDE BY SIDE

This is the core. Same strategy, same gross edge, same turnover.

### C.1 The general result: what gross edge each regime demands

Let one round trip have P&L $X$ with mean $\mu$ and standard deviation $\sigma$. Define the **per-trade information ratio** $r = \mu/\sigma$.

**F&O regime.** Tax is levied on the *net* of the year, all costs deduct (s.34, s.32(1)(k)), losses set off across sources and heads (ss.108–109) and carry forward eight years (s.112). Tax is therefore **linear and symmetric** in P&L:

$$\text{after-tax} = (G - C)(1 - t)$$

**Break-even gross edge is exactly the cost stack, $G = C$.** The tax rate scales the outcome; it does not move the break-even point.

**VDA regime.** Tax is levied per transaction on the positive part only, with no cost deduction:

$$\text{after-tax per trade} = \mu - 0.312 \cdot \mathbb{E}[\max(X,0)] = \mu - 0.312\big(\mu\,\Phi(r) + \sigma\,\varphi(r)\big)$$

Setting this to zero and solving numerically:

$$\boxed{r^\* = 0.1491}$$

**A trade must carry a per-trade information ratio of 0.149 before the VDA regime lets you keep a rupee.** Equivalently, required *annualised* Sharpe just to break even is $0.1491\sqrt{N}$:

| Trades per year $N$ | Annual Sharpe needed to break even under VDA |
|---|---|
| 250 | **2.4** |
| 1,000 | **4.7** |
| 5,000 | **10.5** |
| 20,000 | **21.1** |
| 50,000 | **33.3** |

The corresponding number under the F&O regime is **0**.

**Effective tax as a fraction of gross edge**, which is the number that actually communicates it:

| Per-trade $r$ | VDA tax, as % of gross edge |
|---|---|
| 0.02 | **638%** |
| 0.05 | **265%** |
| 0.10 | **141%** |
| 0.20 | **79%** |
| 0.50 | **44%** |
| 1.00 | 34% |
| 2.00 | 31% |

Only at $r \gtrsim 1$ does the 31.2% headline rate approximate reality. **Every delta-neutral options strategy lives at $r$ between 0.02 and 0.3.** In that band the VDA regime is not a 30% tax; it is a 79%–640% tax.

### C.2 Worked case 1 — a low-turnover short-vol book (the favourable case for VDA)

Real inputs: NIFTY 28-Aug-2026 close **24,175.65**, lot **65**, notional/lot **₹15,71,417**. One 24,200 weekly straddle collects **₹11,495 per lot** (CE 104.75 + PE 72.10, ×65).

Book: ₹25,00,000 equity, 8 lots, one cycle per week, 52 cycles. Outcome shape 72% win +₹40,000 / 28% lose −₹63,000 → mean **₹11,160**, sd **₹46,247**, **r = 0.241** (a genuinely good short-vol book; annual Sharpe 1.74).

| | **NSE F&O** | **VDA** |
|---|---|---|
| Gross annual edge | ₹5,80,320 | ₹5,80,320 |
| Tax base | net of the year, after costs | **₹14,97,600** — the sum of winners only |
| Tax @31.2% | ₹1,81,060 | **₹4,67,251** |
| **Net** | **₹3,99,260 (16.0% of equity)** | **₹1,13,069 (4.5% of equity)** |
| 1% TDS withheld in-year | n/a | ₹47,819 = **42% of the year's net profit**, locked until refund |

**Same strategy, same edge, same turnover. The VDA regime keeps 28% of what the F&O regime keeps** — and this is the *flattering* case, because turnover is only 1.9× equity.

### C.3 Worked case 2 — a high-turnover delta-neutral book (where it breaks)

Same ₹25,00,000 equity. 5,000 round trips a year (20/day × 250 days), ₹5,00,000 notional each → **₹250 crore annual turnover = 1,000× equity**. Per-trade edge 2 bps of notional (₹100), per-trade vol 40 bps (₹2,000) → **r = 0.050**. Gross edge ₹5,00,000.

| | **NSE F&O** | **VDA** |
|---|---|---|
| Gross edge | ₹5,00,000 | ₹5,00,000 |
| Regulatory costs (23.7 bps of premium, premium = 1.2% of notional) | −₹71,100, **deductible** | −₹71,100, **not deductible** |
| Tax | ₹1,33,817 | $0.312 \times 5000 \times \mathbb{E}[\max(X,0)]$ where $\mathbb{E}[\max]=₹849.8$ → **₹13,24,255** |
| **Net before TDS** | **+₹2,95,083 (+11.8% of equity)** | **−₹8,24,255 (−33.0% of equity)** |
| 1% TDS on transfers | n/a | **₹2,50,00,000 = 10× the entire equity** |

The tax alone converts a +20% gross book into a −33% net book. **The TDS makes it un-fundable before the tax question is even reached.**

### C.4 Where exactly it breaks — the two thresholds, stated plainly

**Threshold 1 — no-loss-offset. Independent of turnover.** The book dies when the per-trade information ratio falls below **0.149**. No amount of size, leverage or capital fixes this; it is a property of the P&L *shape*, and it is scale-invariant.

**Threshold 2 — 1% TDS. Purely a turnover threshold.** Let $e$ be gross edge as a fraction of transfer consideration. TDS withheld in the year is $0.01 \times T$; gross edge is $e \times T$. So:

$$\frac{\text{TDS}}{\text{gross edge}} = \frac{0.01}{e}$$

| Gross edge, bps of turnover | TDS as % of gross edge |
|---|---|
| 200 bps | 50% |
| **100 bps** | **100% — the break point** |
| 50 bps | 200% |
| 25 bps | 400% |
| 10 bps | 1,000% |
| 5 bps | 2,000% |
| 1 bp | 10,000% |

**The book breaks the moment gross edge falls below 1% of turnover.** Market-making, basis capture, funding-rate harvesting, gamma scalping and every other delta-neutral strategy earns 1–30 bps of turnover. **They break by a factor of 3× to 100× on the withholding alone**, before any tax is assessed. The TDS is refundable, which means the loss is not the money — it is the *carry on the money* plus the fact that the cash is gone from the account while the position needs margin.

Stated as a capital constraint: **TDS withholding equals 100% of equity when annual sell-side turnover reaches 100× equity.** For ₹25 lakh of equity that is ₹25 crore of transfers — roughly ten trading days of a modest intraday book.

### C.5 What this implies about which venue is worth building for

Stated as arithmetic, not opinion:

1. **The F&O regime is tax-transparent to strategy design.** Break-even gross edge = the cost stack, full stop. The tax rate changes how much you keep; it never changes *whether* an edge is worth trading. You can therefore design, backtest and size a strategy against a pure cost model and add tax afterwards as a scalar. **That is what makes a research programme possible at all.**

2. **The VDA regime is not tax-transparent — it is a strategy filter.** Because the tax base is $\mathbb{E}[\max(X,0)]$ rather than $\mathbb{E}[X]$, the tax changes the *ranking* of strategies. It penalises high-frequency, low-per-trade-IR, high-hit-rate strategies most, which is exactly the class of delta-neutral options strategies. It penalises short-premium books specifically and severely: you pay 31.2% on every one of the many small wins and receive nothing back on the few large losses. **The regime is close to maximally hostile to precisely the strategies he is training to build.**

3. **The comparison is not "India vs offshore."** Per the settled sibling finding, LRS does not fund an overseas margin account, so the realistic choice set is *NSE index F&O* versus *Indian-domiciled VDA venues*. On the arithmetic above there is no contest for a systematic delta-neutral programme.

4. **The concrete implication.** Build the research stack, the execution stack, the margin simulator and the cost model **against NSE index derivatives**. Treat crypto as a source of *data and technique* — 24/7 tick data, a real perpetuals microstructure, an implied surface with no lot-size floor — and as a place to validate models, not as a P&L venue, unless and until either (a) the strategy's per-trade IR exceeds ~0.15 with a wide margin, or (b) the regime changes. The identical model class, run on the identical data, is worth 3.5× more per rupee of equity on NSE in the low-turnover case and is the difference between +11.8% and −33% in the high-turnover case.

5. **And know what NSE costs you.** The F&O regime is transparent but not cheap and it got 27%/46% dearer on 1 Apr 2026. The break-even gross edge on an options round trip is **23.7 bps of premium**; on a futures round trip **9.5 bps of notional**. Delta-hedging is now the single largest controllable cost line in a short-premium book.

---

## PART D — MARGIN AS A SIMULABLE OBJECT

### D.1 PRISM — what it is, from NSE Clearing's own words

From `https://www.nseclearing.in/risk-management/equity-derivatives/violations` (updated 09/03/2026):

> *"**PRISM (Parallel Risk Management System)** is the real-time position monitoring and risk management system for the Futures and Options market segment at NSE CLEARING. The risk of each trading and clearing member is monitored on a real-time basis and alerts/disablement messages are generated if the member crosses the set limits."*

PRISM is the **monitoring and disablement layer**. **SPAN** is the *margin computation* inside it. NSE Clearing licenses SPAN from CME (the site carries the trademark notice). PRISM applies SPAN's output in real time and pulls the trading facility when limits break — see §D.6.

### D.2 The initial-margin model, exactly as specified

From SEBI Master Circular Chapter 5, §2.2 (index options) and §1.2.5 (index futures), and the NSE Clearing SPAN Risk Parameters page (updated 20/06/2025):

**Price Scan Range (PSR)** — index derivatives:
> *Six standard deviations (6σ) scaled up by √2, subject to at least **9.3%** of the underlying price.*
(17.7% for index options with residual maturity > 9 months; 14.2% for stock derivatives.)

The √2 is the **MPOR scaling**: SEBI requires exchanges to estimate an MPOR of at least 2 days and *"the revised MPOR shall be given effect by way of scaling up the PSR used for computing the Worst Scenario Loss."*

**Volatility Scan Range (VSR)** — index: *25% of annualised EWMA volatility, subject to minimum 4%* (10% minimum for stock derivatives).

**The 16 scenarios** (Master Circular ¶2.2.2.1.1), reproduced exactly — this is the whole model:

| # | Price move (× PSR) | Vol move (× VSR) | Fraction of loss |
|---|---|---|---|
| 1–2 | 0 | +1 / −1 | 100% |
| 3–6 | ±1/3 | +1 / −1 | 100% |
| 7–10 | ±2/3 | +1 / −1 | 100% |
| 11–14 | ±1 | +1 / −1 | 100% |
| **15–16** | **±2** | **0** | **35%** |

Worst Scenario Loss = max loss across the 16 (scenarios 15/16 at 35% weight). Permitted pricing models: **Black-Scholes, Binomial, Merton, Adesi-Whaley** (¶2.2.2.1.4). All futures maturities on the same index are assumed to move by the same amount (¶2.2.2.1.3).

**There is no separate short-option minimum charge** for index options (¶2.2.1.2, footnote to SEBI/HO/MRD2/DCAP/CIR/P/2020/27).

**Initial Margin = SPAN worst-scenario loss + calendar-spread charge + margin on consolidated crystallised obligations + delivery margins.** Netted at individual client level; **grossed at TM/CM level with no set-off between clients**.

### D.3 Extreme Loss Margin — the second, non-portfolio layer

From the NSE Clearing Margins page and NCL Risk FAQ Q12:

| Position | ELM |
|---|---|
| Index futures, gross open | **2% of notional** |
| Short index options | **2% of notional** |
| Short index options, deep OTM (>10% OTM vs prev close) | **3%** |
| Short index options, residual maturity > 9 months | **5%** |
| Stock futures | 3.5% |
| Short stock options (deep OTM >30%) | 3.5% (5.25%) |
| Calendar spread in futures | ELM on **one third** of the far-month leg |
| **On the day of options expiry** | **additional 2%** on all short index options open at start of day **and** on short options initiated during the day that expire that day |

The expiry-day add-on comes from **SEBI/HO/MRD/TPD-1/P/CIR/2024/132 ¶5.6**, effective 20 Nov 2024. Notional for a short option = *the value of the underlying index* × lot, at last available closing price — **not the premium**.

**The critical structural fact for a spread trader:** ELM is levied on **short option contracts**, netted at client level per contract. **Long options do not reduce it.** SPAN is portfolio-based; ELM is not. This is why buying wings collapses your SPAN and barely touches your total margin (§D.5).

### D.4 Portfolio margining across legs of a spread

- **Within an expiry:** full portfolio treatment. The 16 scenarios are applied to the whole portfolio's value, so a long leg's gain in a scenario offsets a short leg's loss.
- **Across expiries (calendar spread):** *"The margin for calendar spread would be the same as specified for the index futures contracts. However, the margin shall be calculated on the basis of **delta** of the portfolio in each month"* (¶2.2.2.3). **Calendar Spread Charge for index derivatives = 1.75% of the far-month contract** (2.2% for stock derivatives). It is charged **in addition to** the Worst Scenario Loss.
- **On expiry day, calendar-spread benefit is withdrawn.** SEBI/2024/132 ¶5.2.2, effective 1 Feb 2025: *"On the day of expiry, the worst scenario loss … shall be calculated separately for contracts expiring on the given day and for the rest of the contracts."* NSE Clearing's page states it as: *index calendar spread positions get calendar-spread treatment only till **expiry−1 day**.*
- **Net Option Value:** current market value of the option × quantity (positive long, negative short) is added to Liquid Net Worth — so short option MTM is deducted from available collateral continuously, and long option value is credited.
- **Cross-margining across correlated indices** is subject to full revocation at the start of the first expiring index (SEBI/2024/132 ¶5.2.1).

### D.5 The numbers — computed from the published parameters and real 28-Aug-2026 prices

I implemented the 16-scenario model above against the actual F&O bhavcopy. Inputs, all from NSE files that day:

- Underlying **24,175.65**; lot **65**; **notional per lot ₹15,71,417**
- FOVOLT: NIFTY applicable daily vol **0.847876%**, annualised **16.1986%**
- 6σ√2 = **7.19%** → **the 9.3% floor binds** → **PSR = 2,248.3 points**
- VSR = max(25% × 16.1986%, 4%) = **4.05 vol points**
- Forward from put-call parity at the ATM strike; Black-76; IVs backed out per contract

| Position (1 lot) | Premium | SPAN WSL | ELM | **Initial margin** | % of notional |
|---|---|---|---|---|---|
| Weekly ATM 24200 short straddle, 4 DTE | ₹11,495 | ₹1,36,769 | ₹62,857 | **₹1,99,625** | 12.70% |
| Weekly ~1σ short strangle 24600C/23750P, 4 DTE | ₹718 | ₹1,21,546 | ₹62,857 | **₹1,84,402** | 11.73% |
| Monthly ATM 24200 short straddle, 32 DTE | ₹36,189 | ₹1,19,923 | ₹62,857 | **₹1,82,780** | 11.63% |
| Monthly short strangle 25200C/23200P, 32 DTE | ₹3,916 | ₹89,198 | ₹62,857 | **₹1,52,055** | 9.68% |
| **0DTE ATM short straddle** (+ expiry-day ELM) | ₹11,495 | ₹1,36,769 | **₹1,25,713** | **₹2,62,482** | **16.70%** |
| 0DTE short strangle (+ expiry-day ELM) | ₹718 | ₹1,21,546 | ₹1,25,713 | **₹2,47,259** | 15.73% |
| Iron condor: 24200 straddle vs 24700C/23700P wings | ₹11,008 | **₹21,492** | ₹62,857 | **₹84,349** | 5.37% |

**Verdict on round one's figures:**

- **"₹1.5–2 lakh per lot for a NIFTY short strangle" — CORRECT, and still correct.** ₹1.52 lakh (monthly) to ₹1.84 lakh (weekly). But it is correct for a *different reason* than round one supposed: the lot is now **65, not 75**, and the notional is ₹15.71 lakh.
- **"₹3–3.25 lakh for a 0DTE short straddle" — NOW ~15% TOO HIGH. The current figure is ₹2.62 lakh.** The old figure was right at lot 75: ₹2,62,482 × 75/65 = **₹3,02,864**. Round one was quoting a pre-28-Oct-2025 lot size. **NSE/FAOP/70616 (3 Oct 2025) revised NIFTY 75 → 65** effective 28 Oct 2025 EOD, per SEBI/HO/MRD-PoD2/CIR/P/2024/00181.

**Three non-obvious results worth keeping:**

1. **SPAN margin for a short option is almost time-insensitive.** The 0DTE and 4-DTE straddles show the *same* ₹1,36,769 worst-scenario loss. With a 9.3% price scan, intrinsic dominates the scenario valuation regardless of time to expiry. **The entire 0DTE margin uplift — ₹62,857, or 24% — is the expiry-day ELM, nothing else.**
2. **Buying wings collapses SPAN by 84% and total margin by only 58%,** because ELM does not net across contracts. The iron condor's margin is 75% ELM. Any margin-efficiency work on defined-risk structures must optimise against ELM, not against SPAN.
3. **The 9.3% PSR floor was binding on 28 Aug 2026** (6σ√2 = 7.19%). It has been binding for most of the last several years in NIFTY. **In calm markets Indian index option margin is not a VaR number at all — it is a flat 9.3% + 2% administrative floor.** Margin therefore does *not* fall when vol falls, which is precisely when a short-premium book wants leverage. Model it as a floor, not as a risk measure.

### D.6 Intraday recomputation, peak margin, and forced liquidation

**SPAN file cadence — NCL Risk FAQ Q2:** *"SPAN files, with updated parameters, shall be based on the prices at **11:00 hrs, 12:30 hrs, 14:00 hrs, 15:30 hrs, EOD and BOD** and shall be run shortly thereafter."* Six files a day, equity derivatives. (Currency: nine. Commodity: at intervals not exceeding two hours.)

**But — and this is the single most useful fact in this section for a backtester — NCL Risk FAQ Q61:**

> *"The computation of the margin requirement of SPAN+ELM (both, **intra-day and EOD**) for the Equity Derivatives … shall be based on the **fixed Beginning of Day (BOD) margin parameters** and would include all SPAN margin parameters as well as ELM requirements."*

**Your intraday margin path is fully reconstructible from the BOD parameters plus the intraday price path.** You do not need the intraday SPAN files to simulate the intraday margin requirement — you need one parameter set per day and a tick series. That is what makes a margin-aware backtest feasible.

**Peak margin — SEBI Master Circular ¶14.3.2 (from SEBI/HO/MRD2/DCAP/CIR/P/2020/127, 20 Jul 2020):**
- CCs send **a minimum of 4 client-wise margin snapshots per day**, taken randomly within pre-defined windows.
- File **MG-12/13** carries both the EOD margin requirement and the **peak** across snapshots.
- The member compares EOD obligation vs EOD collateral **and** peak obligation vs peak collateral; **the higher of the two shortfalls is penalised**.
- Phase-in reached 100% of peak.
- **Penalty (NCL FAQ Q62): 0.50%** if shortage < ₹1 lakh **and** < 10% of applicable margin; **1.00%** if ≥ ₹1 lakh **or** ≥ 10% — **per client, per segment, per day.** Non-reporting = non-collection.
- Reporting deadline: **T+5** (NCL FAQ Q58).

**A backtest must simulate peak margin, not EOD margin.** A strategy that ends the day flat but peaks at 3× margin mid-session has a real, penalised requirement it never shows on the closing book. Simulate at least 4 random intraday snapshots and take the max.

**Forced liquidation — this is an event, and here is the trigger ladder (NSE Clearing Violations page):**
- TM total margin (IM + ELM) is computed **real-time** against TM effective collateral.
- Warning at **70%, 80%, 90%** utilisation.
- **At 100% utilisation the trading facility is withdrawn.** Not a margin call — the terminal stops.
- CM violation: margin liability exceeds effective deposit less minimum liquid net worth, *"at any time, including during trading hours."*
- On failure to restore, NSE Clearing may *"close out forthwith or any time thereafter … by placing at the Exchange, counter orders in respect of the outstanding position … **without any notice**."*

**Simulate it as:** a hard state transition when running margin ÷ collateral crosses 1.0 — no new orders, and existing positions liquidated at market by a counterparty who does not care about your exit price. Not a slippage haircut; a regime change. For a short-gamma book this is the mechanism by which a −4σ day becomes a −12σ P&L.

**Position limits are now monitored intraday too** (SEBI/2024/132 ¶5.3, effective 1 Apr 2025), on a minimum of 4 random snapshots, on a **Future-Equivalent (delta)** basis. NSE/SURV/70553 (30 Sep 2025) **Annexure 2 publishes the Black-Scholes delta formula the exchange uses**, and NSE/SURV/75524 (31 Jul 2026) updates the time-to-expiry convention to the **15:40 derivatives close on expiry day** on account of the new Closing Auction Session. The exchange's own delta convention is published and therefore reproducible — use theirs, not yours.

### D.7 Other margin components a backtest must carry

From NCL Risk FAQ Q23–Q26:

- **Margin on consolidated crystallised obligation.** Intraday: net payable across premium payable/receivable + futures crystallised P&L at weighted-average trade prices. EOD: futures MTM + option premium + exercise/assignment + futures final settlement. If net payable, it is blocked as margin. **This replaced net-buy-premium, intraday crystallised losses, assignment margin and futures final-settlement margin.**
- **Delivery margin** (stock derivatives): from **E−4**, on the lower of potential deliverable positions or ITM long option positions, at cash-segment margin rates, laddered **10% at E−4, 25% at E−3, 45% at E−2, 70% at E−1**. Index derivatives are cash-settled and escape this.
- **Additional margin on extreme scenarios** — Q26(ii)(a): applicable on *"client positions in extreme scenario of **20% market fall and 17.74% market rise**"*, and (b) on *"clients having net loss of ₹25 crores and more."* **This is a second, wider stress test sitting behind the 9.3% PSR, and it targets exactly the naked-short-option book.**
- **Cash collection of option value** — Q26(iii): mandatory on index contracts ≤9 months whose strike is **≥20% away** from the index close, ≥30% for 9m–2y, ≥40% for anything. Deep-OTM shorts require *cash*, not collateral.
- **Concentration margin** on long-dated (>9 month) short option positions ≥20% of an expiry's short side, ≥₹500 crore notional: 1.50%/2.25%/3.00% of notional by slab, **blocked from the cash component**.

### D.8 The cash / cash-equivalent requirement

**SEBI Master Circular ¶1.2.2.1:**
> *"At least **50% of the total liquid assets** shall be in the form of **cash equivalents** viz. cash, bank guarantee, fixed deposits, central govt. securities (T-bills and G-Secs)."*

NSE Clearing's Margins page restates it at member level: *"At least 50% of the Effective Deposits should be in the form of cash."* Cash component = cash, BG, FDR, T-bills, dated G-Secs. Non-cash = pledged demat securities with haircuts (haircut file published daily, §0.10). Money-market, overnight and G-Sec mutual fund units count toward the cash component at **5% haircut (overnight growth plans)** / **10% (others)**, marked daily.

**The arithmetic that follows.** To carry a ₹1,84,402 short strangle you must hold **at least ₹92,201 in cash or cash-equivalent** that earns T-bill yield at best. The other half can be pledged equity or funds, post-haircut. **The true funding cost of an Indian options book is therefore roughly (50% × repo-ish) + (50% × the opportunity cost of a haircut-reduced pledge)** — and that belongs in the cost model alongside the 23.7 bps.

**Honest limitation:** the 50% rule I verified is stated at **clearing-member / effective-deposit level** in both the SEBI Master Circular and NSE Clearing's pages. The identical 50:50 requirement is applied down to the client by brokers, but **I did not reach the primary SEBI circular that imposes it at client level** in this session and I am not going to assert it from a broker page.

### D.9 Verified negative: you cannot download the SPAN risk-parameter file anonymously

I tried, in this session:
- `https://nsearchives.nseindia.com/archives/nsccl/span/nsccl.YYYYMMDD.sN.spn` — **404** (all of s1–s6, both date formats, `.zip` variants, `/content/` and `/archives/` prefixes)
- `https://www.nseindia.com/api/daily-reports?key=…` and `merged-daily-reports?key=favDerivatives` — the derivatives daily-report manifest returns nine files (bhavcopies, settlement prices, ban list, haircuts) and **no SPAN file**
- I fetched and parsed the raw HTML of `https://www.nseindia.com/static/products-services/equity-derivatives-span-risk-parameter-files` — despite the page title, its body contains **only the PSR/VSR/calendar-spread parameter table**, no file links, no API call, no iframe.

**Where the file actually is.** NSE Clearing's PC-SPAN page (updated 16/11/2021) documents the workflow: register at CME Group, download **PC-SPAN (free)** from *Portfolio & Risk → CORE Margin Calculator → Download Center → Software*, then *"copy the risk parameter file and the position file in C:/Span4/Data"*. The `.spn` file itself is distributed to **members via the NSE Clearing extranet**, directory `faoftp/faocommon` (the same directory named in NSE/FAOP/64625 and NSE/FAOP/70616 for contract masters). NSE Clearing also launched an **NMASS-Margins module with API access** during 2026 (NCL/CMPT/72539, 30 Jan 2026, F&O; NCL/CMPT/75155, 10 Jul 2026, SLB) — again member-authenticated.

**What this means practically, and it is good news:** he does not need the `.spn` file. Everything in it that matters for index derivatives is either (a) a published constant (PSR floor 9.3%, VSR 25%/4% floor, calendar spread 1.75%, ELM 2%/3%/5% + 2% expiry-day) or (b) in a public daily file (FOVOLT for σ, fo_mktlots.csv for lot, bhavcopy for prices). **The table in §D.5 was produced entirely from public files and published parameters.** The residual gap versus the official number is NSE's exact option-pricing model choice and its scenario-contract-value discretisation — expect single-digit-percent deviation, not order-of-magnitude.

---

## HONEST NEGATIVES AND UNVERIFIED ITEMS

Stated explicitly, per the brief:

1. **SEBI turnover fee** — I could not retrieve the fee schedule. SEBI replaced the Stock Brokers Regulations 1992 with the **SEBI (Stock Brokers) Regulations, 2026** (8 Jan 2026, `https://www.sebi.gov.in/legal/regulations/jan-2026/securities-and-exchange-board-of-india-stock-brokers-regulations-2026_98974.html`), and that page serves its text via a JS call I could not resolve without a browser. **The ~₹10 per crore figure in §A.8 is unverified.** It is 0.02 bps and does not move any conclusion.
2. **Stamp duty** — I could not open the Indian Stamp Act 1899 Schedule I as amended (indiacode.nic.in and legislative.gov.in both 404'd on the act PDF; egazette search unavailable). **The 0.003% options / 0.002% futures figures in §A.8 are unverified.** Combined ~0.3 bps; again does not move a conclusion. If he wants these nailed, the primary document is the Finance Act 2019 (Act 7 of 2019), Chapter IV Part I, plus the Indian Stamp (Collection of Stamp-Duty through Stock Exchanges, Clearing Corporations and Depositories) Rules, 2019.
3. **GST on brokerage** — I did not open the CGST rate notification. **18% is stated from general knowledge and is unverified against the primary notification** in this session.
4. **VDA TDS on derivatives** — genuinely unresolved in the statutory text (§B.3). Not a research failure; a gap in the law.
5. **Client-level 50% cash rule** — verified at clearing-member level only (§D.8).
6. **ITA 2025 "as amended by FA 2026"** — the Department's consolidated PDF is 403-blocked to non-browser clients. I closed the gap by reading FA 2026's amendment clauses directly and confirming none of the load-bearing sections were touched, but he should re-verify from that PDF in a browser before relying on it.
7. **Nobody has published a public, runnable Indian SPAN implementation that reads NSE's own risk-parameter file.** I looked; the parameter file is member-gated and every public "SPAN calculator" I could reach is broker-affiliated (auto-reject under the filter). **The §D.5 implementation — 16 scenarios, PSR floor, VSR, Black-76 on the parity forward, ELM ladder with expiry-day add-on, driven by FOVOLT + fo_mktlots + bhavcopy — appears to be a gap worth filling and is about 60 lines of Python.** That is a genuinely publishable artefact and a better use of a week than reading another paper.