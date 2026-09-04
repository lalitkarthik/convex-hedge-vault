# The Gated Practitioner List

Verification standard used below: **V** = confirmed this session against at least one source independent of the person's own marketing page. **S** = self-reported / repeated by promo-adjacent outlets only. **U** = could not verify.

---

## 1. The six seed candidates — audited

### Imran Lakha (Options Insight) — background **VERIFIED**, outlet **AUTO-REJECTED**
- **CV**: Maths + LSE → Credit Suisse First Boston → **Citigroup, Head of European Index Options** → **Bank of America, head of European options desk** → macro PM at BlueCrest. Founded Options Insight 2018. **V** — consistent across Real Vision's contributor page, Finance Unlocked's expert page, and Finnotes, none of which he controls. This is the cleanest CV of the six.
- **Auto-reject trigger**: the primary funnel is a paid membership plus "The Ultimate Options Course" (`join.options-insight.com/the-ultimate-options-course`). That is an explicit disqualifier in your filter regardless of how good the CV is.
- **What survives**: his free weekly vol commentary and podcast/Real Vision appearances are usable as *market colour* — where the vol-of-vol is, what the dealer community is positioned in, how a sell-side index-vol book actually thinks about skew and implied correlation. He does not publish code, does not state fills, does not publish P&L. Use him for vocabulary and desk intuition, never as a source of a testable claim.
- **URL**: https://options-insight.com/insights (free posts), https://www.realvision.com/contributors/imran-lakha
- **Caveat**: the free tier does *not* stand alone as an education — it is deliberately incomplete.

### Cem Karsan (Kai Volatility) — background **MOSTLY VERIFIED, one claim does not check out**
- **CV**: Rice 1999 (Economics/Public Policy/English, honours), Kellogg MBA 2005. Worked under John Mulheren at Bear Wagner Specialists; founded **Precision Capital Management** (2005), an SPX vol-arb market-making firm. Founded **Aegea Capital Management, April 2011**, which was later renamed **Kai Volatility Advisors** — an **NFA-registered CTA**. NFA registration is the strongest single verification available here: it is a regulator record, not a bio. **V**
- **Where the claim does not check out**: the widely circulated "**32 years of exchange trading experience**" / "27 years as a market maker" figures are arithmetically impossible against a 1999 undergraduate degree. Those numbers appear to be firm-level aggregates (the Aegea team page language) that migrated into his personal bio via speaker directories. His real book is roughly 2000→present, which is still ~25 years. Treat the "32 years" line as marketing drift, not fraud — but note that he has never corrected it.
- **Good for**: the mechanical, flow-based half of index vol — vanna/charm decay into monthly OPEX, dealer gamma positioning, why the SPX vol surface has a structural supply of upside calls and structural demand for puts. This is the one framework in the retail-visible world that is genuinely *implementable* on your minute data: dealer-positioning proxies are computable from open interest + a Black-Scholes gamma map, and the OPEX-window effects are testable directly.
- **Ignore**: his macro/political forecasting and the "everything is fourth-turning liquidity" narrative layer. It is unfalsifiable and unrelated to the part of his work that has edge.
- **Free material stands alone?** Yes — he has no course. He sells a fund. His free output (X, Alpha Exchange, Mutiny Fund, Real Vision) is the whole public product.
- **Honest negative**: the dealer-gamma/vanna trade is now **crowded**. GEX dashboards are a retail commodity. The framework's explanatory value survived; its naive tradeable edge largely did not. Test the OPEX effect on your own NIFTY minute data before assuming it transfers — Indian expiries are weekly and the dealer structure is completely different (no comparable structural call-overwriting supply).
- **Filter tests passed**: (3) yes, (4) partially — he does discuss when the framework fails, e.g. in vol-of-vol regimes. Fails (1), (2), (5).

### Kris Sidial (Ambrus Group) — **VERIFIED, and the most useful of the six for you**
- **CV**: Co-CIO, The Ambrus Group (founded 2018, vol-arb/tail-risk). Prior: **exotic derivatives desk at Bank of Montreal**, prop trading at Xanthus Capital and Chimera Securities; started under CBOE trader Robert Kanter. **V** — corroborated by Dean Curnutt (Alpha Exchange), Mutiny Fund, Benzinga speaker records, and HFM/HedgeWeek/HedgeFundJournal awards, all independent of Ambrus's own site.
- **The "University of Pennsylvania" line is U** — it appears only in aggregator profiles and I could not confirm it. Ignore it; his desk record is what matters and that is solid.
- **Good for**: the microstructure of *how a tail hedge actually fills*. He is unusually explicit about liquidity, the cost of carry on convexity, and specifically about **the fragility of the options market plumbing** — his repeated public argument that the market-maker ecosystem is thinner than it looks and that a liquidity gap is the real tail. That is test (4) and he passes it hard: he names where his own trade fails (a slow grind-down bleeds him out; he needs discontinuity).
- **Ignore**: nothing much. He does not run a course. He occasionally over-eggs the fragility thesis.
- **Free material stands alone?** Yes. There is no paid product for retail.
- **Filter tests**: (3), (4)×2 — passes cleanly. Fails (1), (2), (5).

### Dan Sheridan — background **SELF-REPORTED ONLY**, outlet **AUTO-REJECTED**
- **CV claim**: 22-year CBOE market maker with Mercury Trading (the Najarian firm), left the pits 2004, trained Pete Najarian. **S** — every restatement (MoneyShow, InvestorPlace, Yelp) traces back to bios he supplied. The Mercury Trading / Najarian association is plausible and widely repeated but I found no independent primary record. Not disproven; just not independently verified.
- **Auto-reject trigger**: Sheridan Mentoring / Sheridan Risk Management is a paid mentoring business. That is the funnel.
- **Honest note**: his free CBOE-era webinars on calendars and butterflies are pedagogically decent and pre-date the current course business, but they are 2010s-vintage, cost-free in every sense including the modelled ones, and contain no reproducible testing. He is the closest US analogue to the Ravish class — better credentialed, same commercial structure.

### SMB Capital options desk — **REJECT; the implied pedigree is weaker than presented**
- **What actually checks out**: Seth Freudberg, Wharton BS 1981, then **property & casualty insurance — CEO of United National Group from 1987** — left insurance in **2006** and has traded options since. **V**, and it materially contradicts the impression SMB's marketing creates. He is not an ex-market-maker or ex-desk trader; he is a career insurance executive who became an options trader at ~47. Mike Bellafiore and Steve Spencer are equities prop, not options.
- **Auto-reject trigger**: the options desk's public output is a funnel into paid mentoring / "Options Fast Track". Every free YouTube video terminates in a class registration.
- **Blunt version**: SMB's options content is a course business wearing a prop firm's clothes. The prop firm is real; the options *desk* is substantially the education product. Skip entirely.

### tastylive / Tom Sosnoff — background **VERIFIED**, outlet **AUTO-REJECTED TWICE**
- **CV**: genuine and large. CBOE market maker ~20 years, original OEX pit trader, co-founded thinkorswim 1999 (sold to TD Ameritrade, $750m), founded tastytrade 2011 and tastyworks 2017 (sold to IG Group, ~$1.1bn). **V** — Wikipedia, SIFMA, CME OpenMarkets, MarketsWiki, John Lothian News.
- **Auto-reject 1**: tastylive is the media arm of a **broker**. Order flow is literally the business model — this is the exact case your filter names.
- **Auto-reject 2**: their "studies" are the marketing. Documented failures to reproduce their backtests exist (Elite Trader threads on replication mismatches), and the standard criticism — that they present anecdote and selective sampling in place of formal testing — is fair. Their signature claims (sell 45 DTE, manage winners at 50%, 16-delta strangles, high IV rank entry) are presented with cost models that flatter the strategy and sample periods that are almost entirely post-2011 US equity bull market.
- **Use for one thing only**: vocabulary and the *mechanics* of managing a short-premium book (rolling, assignment, margin). Then go test every quantitative claim yourself. Do not treat a single tastylive number as an input.

**Score on the seeds: two survive the filter as sources (Karsan, Sidial). One survives as background colour only (Lakha). Three are rejected.**

---

## 2. Tier 1 — the ones actually worth your reading time

### Euan Sinclair — the single highest-value name on this list for you
- **CV**: PhD theoretical physics (Bristol); ~25 years professional options trading; risk manager / strategy design at **Bluefin Trading**; partner, Talton Capital. **V** via Risk.net contributor record, SSRN co-authorship with **Blair Hull** (of Hull Trading — that co-authorship is itself a credential), and Bluefin.
- **Concretely gives you**: free SSRN papers that are directly implementable — *The Risk-Reversal Premium* (with Hull), *The Skewness and Kurtosis of European Options and the Implications for Trade Sizing*, *Volatility Estimation via First Exit Times*, *Alternative Risk Measures and Stock Selection*. The trade-sizing paper is the one to read first: it connects the third and fourth moments of the option's own return distribution to position sizing, which is exactly the gap between your SVI/SSVI work and an actual position.
- **Why he clears the filter**: he passes (2), (3), (4) and (5). Test (4) doubly — he is the only widely-read options author who systematically documents *where premium selling stops working*, why most retail vol edges are cost-annihilated, and how to distinguish a real variance risk premium from a survivorship artefact.
- **Ignore**: nothing, but note his focus is US equity/index and single-stock. Transfer the method, not the parameters.
- **Free stands alone?** The SSRN papers do. The books (*Volatility Trading*, *Option Trading*, *Positional Option Trading*) are paid — get them through IIT KGP; Wiley is standard in institutional library packages.
- **URLs**: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3968542 (Risk-Reversal Premium), https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2956161 (skew/kurtosis and sizing), https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3904792 (first-exit-time vol estimation)
- **Caveat**: some of the SSRN work is a decade old and the specific premia have decayed. The estimators and the sizing framework have not.

### Kris Abdelmessih — *Moontower*
- **CV**: **SIG** (Susquehanna) trainee → market maker across several option pits → **Parallax**, running a relative-value commodities vol book. ~20 years. Cornell BA Econ 1996–2000. **V** via Alpha Exchange and Flirting-with-Models-adjacent podcast records, independent of his own site.
- **Concretely gives you**: the best free writing anywhere on *thinking in payoff space* — how a market maker actually decomposes a structure into vega/gamma/skew exposures and prices the residual. Practical pieces on why "income" is a category error, how to reason about wide markets and fill quality, and how edge is really measured against your own cost of capital and hedging friction.
- **Filter tests**: (3) yes, (4) yes and doubly — he is explicit and repeated about which retail vol ideas are simply the bid-ask spread in disguise. Some posts include spreadsheets/notebooks, so (1) partially.
- **Ignore**: the lifestyle/parenting/personal-finance posts. Maybe 40% of the Substack.
- **Free stands alone?** Yes. moontower.ai is a separate paid tool; the writing does not gate behind it.
- **URL**: https://moontower.substack.com
- **Caveat**: he writes for intuition, not rigour. Almost nothing there is a finished, testable specification — you have to convert his intuitions into hypotheses yourself. For you that is the right division of labour.

### Benn Eifert — QVR Advisors — **read him, and read what just happened to him**
- **CV**: PhD Economics (UC Berkeley), BA Stanford; taught in Berkeley Haas MFE; Head of Quantitative Research and derivatives trader on the **Wells Fargo prop desk** (which became Overland Advisors); co-founder/co-PM of Mariner Coria; started as an EM macroeconomist at the World Bank. Co-founded QVR 2017. **V** — Google Scholar profile, Bloomberg, Hedgeweek, EQDerivatives.
- **Concretely gives you**: years of free, technically precise threads on structured product flows, dispersion, the mechanics of how bank vol supply distorts surfaces, and — most usefully — sustained public demolition of retail "options income" strategies (his "selling options for passive income" zorb-ball post is the canonical version).
- **The essential caveat, and it is a big one**: **QVR's multi-strategy fund lost ~30% between January and April 2026 and is winding down**, from a ~$1.6bn peak, with the management business up for sale (Bloomberg, Hedgeweek, May 2026). This does not invalidate his analysis, but it is the most instructive single fact on this list: the most technically credentialled, most cost-aware, most failure-mode-literate vol manager in the retail-visible world still blew up. Read his back catalogue *and* read the blow-up as the empirical footnote. Do not treat anyone's process as proof of survivability.
- **Free stands alone?** Yes — X/Twitter and podcast appearances, no course, no signal service.
- **URL**: https://www.qvradvisors.com/media, and his X account.

### Dean Curnutt — *Alpha Exchange* podcast
- **What it gives you**: long-form interviews with people who actually run vol books (Sidial, Abdelmessih, and dozens of sell-side derivatives heads). Free, no course, no signals. The interviews routinely go into position sizing, liquidity, and what broke.
- **Verification**: **S/V** — Curnutt's own background (Banc of America Securities equity derivatives strategy, Macro Risk Advisors) I did not independently verify this session. The *guests* are independently verifiable, which is the load-bearing part.
- **Caveat**: it is a podcast. Zero code, zero reproducibility. Treat as a sourcing channel for names, not as a source.

---

## 3. Crypto (40% weight) — where the free, data-backed material actually is

### Greg Magadini — Amberdata Derivatives blog
- **CV**: prop trader at **Chopper Trading** and **DRW** in Chicago; co-founder and CEO of **Genesis Volatility**, acquired by Amberdata in 2022; now Director of Derivatives at Amberdata. ~15 years. **V** — the Genesis Volatility acquisition is a matter of record, DRW/Chopper are checkable, and cryptonews/Derive interviews corroborate independently of Amberdata's own copy.
- **Concretely gives you**: the closest thing to free institutional crypto vol research — BTC/ETH term structure, skew dynamics, realised-vs-implied spreads, option flow decomposition, with actual charts off Amberdata's own tick data. Directly relevant to your later crypto leg: Deribit's surface behaves nothing like SPX, and this is where that difference is documented rather than asserted.
- **Filter tests**: (2) partially — he discusses execution and liquidity concretely; (3) yes; (5) yes — Amberdata's underlying data is purchasable and Deribit's public API gives you most of it free.
- **Ignore**: the Amberdata product marketing wrapped around the research. Also note one podcast title in his promotional orbit is "$50k into $1.3 million" — that is exactly the win-rate marketing your filter rejects. It's a podcast host's framing, not his own output, but it's a flag: the research is good, the surrounding promotion occasionally isn't.
- **URL**: https://blog.amberdata.io/author/greg-magadini
- **Caveat**: it is vendor-published research. The conclusion is never "and therefore you don't need our data."

### Block Scholes × Deribit Insights — weekly crypto derivatives analytics
- **What it gives you**: a free, weekly, quantitatively serious recap of BTC/ETH vol surfaces, term structure, perp funding and futures basis — published on Deribit Insights and Block Scholes' own resource centre. Block Scholes' team is ex-Bloomberg/Goldman/Credit Suisse quants (**S** — firm-level claim on their own site; I could not verify individual CVs).
- **Why it's in**: (5) unambiguously — everything they show is reproducible against Deribit's free public API, which is the single most important property for you. You can rebuild their surface and check them.
- **Ignore / caveat**: Deribit is the **venue**. This is exchange-adjacent content and it will never tell you that crypto options are too expensive to trade. Treat their vol levels as data and their conclusions as marketing. Cross-check against Amberdata.
- **URLs**: https://insights.deribit.com/, https://www.blockscholes.com/research

---

## 4. Open-source authors — where the code *is* the contribution

- **`py_vollib` / `vollib`** — https://github.com/vollib/py_vollib. Wraps **Peter Jäckel's "Let's Be Rational"** for Black/BS/BSM implied vol and Greeks. Jäckel's algorithm is the reference implementation; if your IV inversion disagrees with this, you are wrong. Passes (1) and (5). **Caveat**: European only, no American exercise, and the maintenance cadence is slow.
- **`fast-vollib`** — https://github.com/raeidsaqur/fast-vollib, paper at arXiv 2604.27210. Drop-in `py_vollib`-compatible API with PyTorch/JAX backends and a CUDA fused Triton kernel for batched IV. **This is the one that matters for minute-wise NIFTY data**: full-chain IV inversion across every minute of every strike is the bottleneck you are about to hit, and this removes it. Passes (1) and (5). **Caveat**: new, small user base, and you should validate it against `py_vollib` on a reference grid before trusting it.
- **`optopsy`** — https://github.com/goldspanlabs/optopsy. Filter-composition options backtester: build a strategy out of DTE/delta/width filters. Passes (1). **Caveat, and it's the disqualifying one for naive use**: the cost model is thin. If you use it, you must supply your own fill assumption — mid is a fantasy on Indian weekly options away from ATM. Use it as a data-plumbing skeleton, not as a P&L authority.
- **`jugaad-data`** — https://github.com/jugaad-py/jugaad-data. NSE bhavcopy, historical, derivatives and option chain, built against the **current** NSE site. Passes (1) and (5). **Caveat**: `nsepy` (the more famous library) is built against the deprecated NSE site and will die; prefer jugaad-data. All NSE scraping libraries are one site redesign from breaking — do not build infrastructure that assumes they persist.
- **`marketcalls/openengine` and `openalgo`** — https://github.com/marketcalls/openengine. Event-driven Indian-market backtest engine with a live-execution path, and the associated portfolio backtester explicitly models **transaction costs, rebalancing drift bands, benchmarks and robustness checks** with QuantStats tearsheets. Passes (1), (2), (5). This is the strongest Indian open-source item I found. **Caveat**: broker-integration-shaped (Zerodha-centric), and I did not verify the maintainer's trading background — treat it as infrastructure, not as strategy advice.
- **`breeze-historical-options`** — https://github.com/madmay247/breeze-historical-options. Second-level historical Indian options data via the ICICI Breeze API. Directly relevant if your minute data has gaps you need to fill. **Caveat**: broker API, rate-limited, and ICICI's historical depth is inconsistent across strikes.

---

## 5. Indian-market practitioners — the honest answer

**Almost nobody survives this filter. I am not going to lower the bar to manufacture entries.**

What I checked and rejected:

- **Sensibull / Abid Hassan** — CV is real and decent (derivatives at STCI, ICICI, IIFL; NIT Calicut + IIM Ahmedabad; served on SEBI's hedge fund committee — **V**). But the "ex-Goldman" claim that circulates does **not** check out; I found no Goldman association. Rejected anyway on a structural ground: Sensibull is a broker-integrated platform distributed through Zerodha and others. Order flow is the business model.
- **Zerodha Varsity** — genuinely the best-written free options primer in India, and it is still an auto-reject under your own rule: broker-affiliated education where order flow is the business. It is also below your level.
- **QuantInsti / `blog.quantinsti.com`** — the blog has free, runnable Python and the parent firm is real (**iRage**, a genuine HFT firm; Rajib Ranjan Borah ex-Optiver, IIM Calcutta; Dr Gaurav Raizada PhD IIT Bombay in financial econometrics — **V**). But QuantInsti exists as the educational arm funnelling into the paid EPAT programme. Auto-reject. The blog code is occasionally useful as a snippet source; the conclusions are not.
- **Quantsapp / Shubham Agarwal** — CMT/CFA/CQF/CFTe, trading F&O since 2002 (**V** at the certification level, **S** for the trading record). Product platform with a subscription. No published cost model, no reproducible research.
- **AlgoTest, StockMock, Opstra, NiftyTrader, optionbacktesting.in** — free tiers of paid backtesters. Several *do* let you set slippage and brokerage, which is more than most US retail content offers. But they are closed-box: you cannot inspect the fill logic, so nothing produced there is reproducible. Use them for a five-minute sanity check on an idea, never for a result you would size on.
- **Graviton, Dolat, iRage, Estee** — real, serious Indian quant firms with verifiable people. **They publish nothing.** That is the whole problem: the competent Indian options community is entirely inside prop firms and does not write.

**Two Indian sources that do pass, and they are not people:**

1. **SEBI's annual study on individual traders in equity derivatives** — https://www.sebi.gov.in (press releases, Sep 2024 for FY22–24; the FY26 edition released Aug 2026). Concretely: **87.7% of individual traders lost money in FY26**, aggregate net losses ~₹91,685 crore, **~₹25,000 crore of transaction costs in one year** (~₹1 lakh crore cumulative FY22–FY26), **~92% of aggregate individual losses came from options**, **~97% of traders were predominantly option buyers**, and **~99% of prop/FPI profits were earned by algo entities**. Passes (2) — it is the only Indian document that states the true all-in cost drag — and (5). This is your prior. It tells you precisely who is on the other side of your fills and what the toll booth costs.
   **Caveat**: it is regulator aggregate data with a policy agenda; it tells you the population loses, not why any individual strategy fails.
2. **Ajay Shah and Susan Thomas / XKDR Forum** — https://www.xkdr.org, https://www.mayin.org/ajayshah. Shah and Thomas did the foundational quantitative work on **Indian market microstructure and index construction** (including the NSE-era design work) and publish free, technically serious research plus the Leap Blog. **V** — Google Scholar, SSRN, published book with Michael Gorham. This is the only place you will find rigorous treatment of Indian market microstructure — liquidity, impact cost, index mechanics — written by people who built the institutions.
   **Caveat**: it is policy and microstructure economics, not a trading strategy, and much of the derivatives-specific work is from the late 1990s–2000s. Read it for how NIFTY liquidity and impact cost are actually structured, not for a signal.

**The blunt conclusion**: there is no Indian equivalent of Sinclair or Abdelmessih. Given you will hold minute-wise NIFTY/Sensex data and can model costs against SEBI's published aggregates, the honest recommendation is to import technique from the US/crypto names above and become the missing Indian source yourself, rather than to keep searching for one.

---

## 6. The "Options With Ravish" class — and its honest replacements

Confirmed excluded, along with its entire category (paid course funnel + broker sponsorship + "verified performance" whose trade-level detail is hidden). The tell is generalisable: **any claimed track record whose per-trade fills you cannot inspect is not a track record.** Dan Sheridan, SMB's options desk, and most of the Indian "option selling" YouTube ecosystem are the same object at different production budgets.

For the same subject matter — **double calendars, income structures, delta-neutral premium selling** — here is what to read instead:

| Topic | Honest source | Why |
|---|---|---|
| Whether premium selling has an edge at all, and how to size it | Euan Sinclair, *Positional Option Trading* + the SSRN skew/kurtosis sizing paper | The only treatment that starts from "here is the cost of being wrong about the fourth moment" rather than from a win rate |
| Double calendars / diagonals | There is no good dedicated free source, and that is informative. The correct framing is **forward variance and term-structure slope**, which you already have from Gatheral/SSVI. A double calendar is a bet on the forward vol between two expiries plus a short skew position — price it as such and the folklore evaporates | Nobody teaching calendars as a "range play" is pricing the forward vol |
| Delta-neutral short vol — the failure modes | Kris Sidial (liquidity gaps, why the hedge doesn't fill), Benn Eifert (why the structural short is a levered carry trade), and **the QVR wind-down itself** | Test (4), triple-sourced |
| VRP harvesting with an explicit cost model and code | Robot Wealth free blog + GitHub (https://robotwealth.com, and their public repos) — Kris Longmore, real systematic trader, publishes VIX-basis and vol-risk-premium work with costs modelled | Passes (1), (2), (5). **But**: the primary funnel is a paid bootcamp, so under a mechanical reading of your filter it is an auto-reject. I am flagging it rather than smuggling it in — the free blog and GitHub genuinely stand alone and you can judge |
| The actual net cost of doing this in India | SEBI FY26 study | ₹25,000 crore/year of transaction costs is the number every Indian income-strategy backtest omits |

---

## 7. What I could not verify — stated plainly

- **Kris Sidial's University of Pennsylvania education** — aggregator-only. Ignore it.
- **Dan Sheridan's 22 years / Mercury Trading** — self-reported, repeated by promo-adjacent outlets, not disproven.
- **Dean Curnutt's own sell-side CV** — not checked this session.
- **Block Scholes' individual quant CVs** — firm-level claim only.
- **Corey Hoffstein / Newfound Research** (free research, *Flirting with Models*, publishes replication code and is unusually honest about strategy decay) — I did **not** verify this session and am listing him only as a lead worth checking, not as a passed entry.
- **The maintainer background behind `openengine`/`openalgo`** — unverified. The code's cost modelling is the reason it is listed, not the author.

---

## PAID — worth considering later

Listed separately, never mixed above. Get all three through IIT Kharagpur's library before paying.

1. **Euan Sinclair — *Positional Option Trading* (Wiley)**. The one book on this list with no free equivalent. Covers position sizing under non-normal option returns, the real economics of the variance risk premium, and an unusually long treatment of why most published option edges are cost artefacts. If you buy one thing, this.
2. **Euan Sinclair — *Volatility Trading* (Wiley, 2nd ed.)**. Volatility estimation, forecasting, and hedging error. Overlaps your SVI work but from the P&L side rather than the surface-fitting side.
3. **Imran Lakha — Options Insight membership**. Only if you later want ongoing sell-side index-vol flow colour. It teaches you how a desk talks, not how to test anything. Low priority for you; you can get 80% of it free from Alpha Exchange and Karsan.

**Not recommended at any price**: SMB's options programmes, Sheridan Mentoring, and anything in the Indian option-selling course market.