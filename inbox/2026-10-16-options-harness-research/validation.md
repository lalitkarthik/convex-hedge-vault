promoted: 2026-10-23
# Validation: overfitting checks for options research and for autonomous agents

> Lane `validation`, 2026-10-16. Raw research capture: staging, not fact. About 30 sources opened. AFML (López de Prado, 2018) was read from the extracted book text, chapters 3, 7, 11, 12, 14 and 15. "Read: part" means that I read the abstract and long extracts through a search tool, not the whole document.

## Summary

- AFML gives the harness its skeleton: record every trial, deflate the Sharpe ratio by the trial count, estimate PBO, and cross-validate with purging. Each tool needs one change for options. The unit of independence is the **trading day**, not the intraday row. Performance is measured on **daily P&L** with its real skew and kurtosis.
- For a short-volatility payoff, the Sharpe ratio is the wrong main number. Lo's short-put "fund" shows a Sharpe ratio of 1.94, and Goetzmann et al. prove that option selling can raise Sharpe with no skill. Report CVaR, the worst day as a multiple of the premium, maximum drawdown and Omega next to PSR and DSR. Use MinTRL to state how many days are needed.
- The strongest new evidence is from 2026 papers on LLM research agents. A leaky oracle with a Sharpe ratio of 35 **passes** DSR and PBO (Gençay). Only a structural guardrail stops it: a tool surface that cannot express look-ahead. AQuA and Gençay seal the data path and the evaluator so that the agent cannot change them, and they score the final window once.
- Agent-specific failures: the agent inflates the trial count; a leaky result gets stored in memory as a precedent; the agent selects candidates on the same holdout again and again; a model can remember market history from its pre-training. Agents will p-hack when a prompt frames the search as "uncertainty reporting". LLM auditors catch flaws, but they also flag clean code unless they are calibrated.
- Options traps: an intraday decision that uses end-of-day IV; strikes listed only after the market moved; the settlement price (SPXW close, SOQ, NIFTY's closing average) used before it exists; vendor IV built from unsynchronised quotes; stale quotes.
- The desk's 122 fresh days are already used once. The next frozen holdout must be days that nobody has downloaded yet.
- The file ends with a **proposed** 12-step validation gate.

## 1. AFML methods adapted to options

### 1.1 The trial ledger (AFML ch. 11.5, 14.7.3)

AFML says the purpose of a backtest is "to discard bad models, not to improve them" (ch. 11.4). It asks the researcher to record every backtest that is run on a dataset. Its third law says a result must be reported with all the trials that produced it. DSR needs two numbers from the ledger: N, the number of independent trials, and V, the variance of their Sharpe ratios. PBO needs the full P&L series of each trial.

**Options adaptation.** One ledger row is one evaluated configuration. The row holds the hypothesis ID, the structure (straddle, strangle, spread), the strikes rule, the entry and exit times, the hedge rule, the cost model, the data window and the daily P&L series. Options strategies have many free parameters: delta, expiry, entry time, exit time, hedge band and barrier widths. The count therefore grows fast. Trials are correlated (a 9:35 straddle and a 9:40 straddle are almost one trial). López de Prado and Lewis (2019) estimate the **effective** N by clustering the trials' return correlations (the ONC algorithm). The harness should report both the raw N and the clustered N.

### 1.2 Why Sharpe misleads for short volatility, and what to report instead

AFML's Probabilistic Sharpe Ratio (PSR, ch. 14.7.2) corrects the Sharpe ratio for sample length T, skewness γ₃ and kurtosis γ₄:

- PSR(SR*) = Z[ (SR − SR*)·√(T−1) / √(1 − γ₃·SR + ((γ₄−1)/4)·SR²) ]
- Negative skew (γ₃ < 0) and fat tails (γ₄ > 3) make the denominator larger, so PSR falls. This penalty is exactly what a short-straddle book needs.
- DSR (ch. 14.7.3) is PSR with SR* set to the expected maximum Sharpe ratio of N trials that have no skill. AFML says DSR "should exceed 0.95".

**MinTRL.** Bailey and López de Prado (2012) give the minimum track-record length: MinTRL = 1 + [1 − γ₃·SR + ((γ₄−1)/4)·SR²]·(Z_α / (SR − SR*))². It is counted in observations, not years. An illustration with assumed numbers (not desk data): a daily Sharpe ratio of 0.1 (about 1.6 a year) against SR* = 0 at 95%. Normal returns need about 273 days. With γ₃ = −3 and γ₄ = 20 it needs about 366 days, roughly 1.5 trading years. The desk holds about 250 days of SPXW, so a short-volatility claim of this size cannot pass on one year.

**Sharpe can be gamed with options.** Lo's "Capital Decimation Partners" sold out-of-the-money SPX puts from 1992 to 1999. It had a Sharpe ratio of 1.94 against 0.98 for the index and only 6 down months out of 96 (Chan, Getmansky, Haas, Lo). Goetzmann, Ingersoll, Spiegel and Welch (2007) show that trades in index puts and calls raise the Sharpe, Sortino and other ratios even when the trader has no information. They derive a manipulation-proof measure (MPPM): the average of a power-utility function over the return history.

**Report these next to Sharpe**, each on daily P&L:

- Sortino ratio (it uses downside deviation; Goetzmann et al. show it can also be gamed).
- CVaR at 95% and 99%: the mean of the worst 5% and 1% of days.
- Worst day ÷ average daily premium collected, a scale-free tail number for sellers.
- Maximum drawdown, and AFML's 95th-percentile drawdown and time under water (ch. 14.5).
- Omega(0) (Keating and Shadwick 2002): probability-weighted gains over losses at a threshold. It uses the whole distribution. Plot it as a function of the threshold, not as one number.
- MPPM as a cross-check when two structures are compared.
- AFML's HHI concentration of positive and negative returns (ch. 14.5.1). It shows whether a few days carry the result.

### 1.3 PBO through CSCV (AFML ch. 11.6; Bailey et al. 2016)

CSCV builds a T × N matrix of trial performance. It splits the rows into S blocks, and for every half/half combination it asks one question: does the in-sample best trial rank above the median out of sample? PBO is the share of combinations where it does not. AFML's example: S = 16 gives 12,870 combinations (the book prints 12,780, but C(16,8) is 12,870).

**Options adaptation.** The rows must be synchronous for every trial, so aggregate intraday windows to **daily P&L**. A day is the natural row: a 0DTE position never crosses it. With about 250 days and S = 16, each block holds about 15 days. Keep blocks contiguous, because volatility clusters. PBO only measures the **selection process** within one family of trials. Gençay found PBO = 0.01 for an agent whose winner kept its rank but lost its absolute edge, so PBO must be paired with an out-of-sample interval.

### 1.4 Purged k-fold and embargo (AFML ch. 7)

Leakage happens when a training label and a test label share information. AFML removes ("purges") every training observation whose label interval [t₀, t₁] overlaps a test label. It then drops ("embargoes") a short period after each test block, because features are serially correlated. AFML suggests about 1% of T. It adds a test: if performance keeps rising as k grows, the backtest is profiting from leaks.

**0DTE adaptation.** The desk's windows are 30 minutes, twelve a day. Rows inside one day share the open, the day's volatility level and the IV surface, so they are not independent. Overlapping labels (a straddle opened every 5 minutes and held 30) leak inside the day. Rules:

- **Fold by whole days.** A 0DTE label never crosses the close, so whole-day folds remove intraday overlap.
- **Embargo at least one day** after each test block, and longer if a feature uses trailing multi-day realised volatility or IV changes.
- **Count effective sample size in days**, not windows. The desk's own tests already reshuffle whole days ([results.md](../2026-10-08-feature-experiments/results.md)). This is the same idea.

**NIFTY adaptation.** Weekly and monthly positions span days and cross expiries, so purge by each label's t₁, and embargo at least the label length. Group folds by expiry week where possible.

### 1.5 Combinatorial purged CV (AFML ch. 12)

Walk-forward tests one path. It is "as easy to overfit" as a walk backwards (ch. 12.2.1), and its early decisions use little data. CPCV splits T into N groups. It tests every choice of k groups and assembles φ[N, k] = (k/N)·C(N, k) backtest paths. The result is a **distribution** of Sharpe ratios, not one number.

**Options adaptation.** Use groups of whole days, with purging and embargo as in 1.4. For about 250 days, N = 10 and k = 2 give 45 splits and 9 paths of about 25-day groups. That is enough to see the spread of outcomes, but every group is short. One bad week can dominate a path for a short-volatility book, and that is useful information. CPCV is relevant only where a model is **fitted** (a filter, a threshold, a meta-model). A fixed rule with no fitted parameter has nothing to train, and the honest test is then the frozen holdout.

### 1.6 Triple-barrier labels (AFML ch. 3.4)

A label is the first barrier touched: profit-take, stop-loss, or a time limit. The barriers scale with volatility, "whether realized or implied". The label is path-dependent, and its end time t₁ is what purging needs.

**Options adaptation.**

- Set barriers in **option P&L units**: for example, profit-take at a fraction of the premium collected and stop at a multiple of it. Do not use underlying returns, because the payoff is nonlinear.
- The vertical barrier is the window end, a time of day (for example 15:45 for 0DTE), or expiry.
- Scale barriers by the IV **at entry**, never by realised volatility that is measured later.
- With one-minute data, two barriers can be crossed inside one bar. The vault records that one-minute bars cannot tell which was hit first ([pipeline.md](../2026-10-07-research-pipeline/pipeline.md), stage 4). Mark those labels ambiguous, and test with "stop hit first".
- Mark positions at mid and charge the spread on exit, or the profit-take barrier is reached on paper only.

### 1.7 Meta-labeling (AFML ch. 3.6–3.7)

A primary model sets the side. A secondary model learns only whether to act and how much. AFML argues that this limits overfitting, because the machine-learning model does not choose the side.

**Options adaptation.** This fits the desk closely. The primary rule is the existing trade ("sell the at-the-money straddle in each window, hedged on the band"). The meta-label is 1 when that trade made money **after the spread** and 0 otherwise. The secondary model is then a filter or a sizer. The desk's experiment 5 is a warning: a filter that beat 99% of random filters on the seen days failed on the fresh days ([results.md](../2026-10-08-feature-experiments/results.md)). Meta-labeling does not remove the need for purged CV, the ledger and a frozen holdout. A meta-model with a high precision on rare "skip" calls can still be ruined by one missed tail day, so score it on CVaR as well as F1.

### 1.8 Strategy risk for asymmetric payoffs (AFML ch. 15)

AFML models a strategy as n bets a year that win π₊ with precision p and lose π₋ otherwise. It derives the precision p* needed for a target Sharpe ratio θ*. It then estimates P[p < p*], the probability that the strategy fails, by bootstrapping the observed precision. AFML would discard a strategy with P[p < p*] > 0.05. Its example: a fall in p from 0.70 to 0.67 removes all the profit.

**Options adaptation.** A short straddle is the textbook case: a small π₊ (part of the premium) and a large π₋ (a tail day). The desk's sell-every-window test was up on 62% to 73% of days at mid and lost once the spread was paid ([results.md](../2026-10-08-feature-experiments/results.md)). That is a precision just above a thin p*, which is the fragile shape AFML describes. The harness should report p, p*, and P[p < p*] from daily outcomes with the spread paid. A caution from my reading: AFML's Snippet 15.5 passes p(1−p) as the normal scale. A bootstrap over nk bets has standard deviation √(p(1−p)/(nk)). The extracted formula text is garbled, so check this line before reuse.

### 1.9 Regime dependence

AFML asks for a backtest long enough to "include a comprehensive number of regimes" (ch. 14.3), and CPCV's ch. 12.3 tests a model on a stress period it did not see. For options the regime is mostly the volatility level and trend against chop. The desk found that regimes describe returns but did not filter them on both half-years ([results.md](../2026-10-08-feature-experiments/results.md)). Two market-structure breaks also count as regimes. Daily SPXW expiries exist only since Tuesday and Thursday expiries began in April and May 2022 ([SEC filing SR-CBOE-2023](https://www.sec.gov/files/rules/sro/cboe/2023/34-97371.pdf)). NIFTY expiry rules and the expiry day have changed: the NSE page now lists Tuesday expiry ([NSE contract specs](https://www.nseindia.com/static/products-services/equity-derivatives-contract-specifications)), while an older weekly spec says Thursday ([NSE weekly spec](https://www.nseindia.com/static/products-services/equity-derivatives-bank-nifty-option-contract-specification-weekly)). A NIFTY backtest must split at each rule change. The proposed gate asks for the sign of the effect to hold in each volatility tercile.

## 2. Other multiple-testing methods

**Harvey, Liu and Zhu (2016).** They count 316 published factors and set new hurdles: a t-statistic above 3.0 for a new factor. Bonferroni reaches 3.78 by 2012 and BHY (an FDR method) about 3.39. Their estimate is that 71% of the factors that were tried are missing from the record. They conclude that most claimed findings are likely false. *Take:* t ≥ 3 as the floor for a result from a broad search. *Fit:* the paper is about the equity cross-section, not time-series options P&L. The hurdle depends on how many tests the field ran.

**Harvey and Liu (2015), "Backtesting".** A haircut Sharpe ratio adjusted for the number of tests. The haircut is nonlinear: it is far more than 50% below a Sharpe ratio of about 0.4 and at most 25% above 1.0. *Take:* report the haircut Sharpe next to DSR; DSR's authors suggest computing both.

**White (2000), Reality Check.** A bootstrap test of whether the **best** model in a specification search beats a benchmark. *Take:* the benchmark for an options rule is "sell every window" or "do nothing". *Fit:* it loses power when many bad strategies are in the set.

**Hansen (2005), SPA.** It improves the Reality Check with a studentised statistic and a null that adapts to the sample, so it is "less sensitive to poor and irrelevant alternatives". **Romano and Wolf (2005), StepM**, tells you **which** strategies beat the benchmark while controlling the familywise error. Neuhierl and Schlusche (2011) apply all of these to market-timing rules: rules that win alone mostly do not survive the correction. The Python `arch` package implements SPA and StepM ([arch docs](https://bashtage.github.io/arch/multiple-comparison/background.html)). *Fit:* all three need returns for every trial on one common calendar, which is what the ledger provides.

**False discovery rate (Benjamini–Hochberg, BHY).** It controls the share of false discoveries among the accepted ones, not the chance of any false one. It is milder than familywise control, and it suits an idea queue where several survivors are acceptable and a few may be wrong.

**Minimum backtest length (Bailey, Borwein, López de Prado, Zhu 2014).** Already in the vault: with five years of data, try at most about 45 independent configurations ([papers-tooling.md](../2026-10-07-research-pipeline/papers-tooling.md)). With one year, the safe count is far smaller.

**Walk-forward pitfalls.** It tests one path, it rewards the order of history, and early decisions use a small part of the data (AFML ch. 12.2.1). If you edit the model after you see a walk-forward result, that data has become validation data ([qse-forums.md](../2026-10-07-research-pipeline/qse-forums.md); Sinclair in [blogs.md](../2026-10-07-research-pipeline/blogs.md)). Walk-forward is still the right **final** simulation, because it matches live trading. It is not the selection tool.

**The reusable holdout (Dwork et al. 2015).** A standard holdout loses its validity when the analyst queries it adaptively. In their test with pure-noise data, holdout reuse reported 63% accuracy where 50% is the truth. Thresholdout answers from the training set unless the holdout disagrees by more than a noisy threshold. *Take:* if the agent must see any holdout feedback, give it through a Thresholdout-style gate or as a coarse pass/fail, never the raw score.

## 3. Autonomous agents: what goes wrong, and the guardrails

### What goes wrong

- **Trial inflation at machine speed.** Gençay (2026) records every evaluation an LLM agent makes. In 102 trials the best in-sample Sharpe ratio climbed to 1.69, and the deflation threshold climbed to 1.21. DSR stopped at 0.86, and the out-of-sample Sharpe ratio was 0.18. A second model and five repeat runs gave the same verdict: no LLM-found strategy passed.
- **Statistics do not catch leakage.** In the same paper a planted look-ahead oracle posted a Sharpe ratio of 34.7 and DSR = 1.00. Deflation corrects selection among honest backtests; it cannot see a contaminated information set. The author's rule: a two-digit Sharpe ratio means suspect the data, not the alpha.
- **Leakage through memory.** AQuA (Guo et al. 2026): a leaky feature that scores well "gets stored as a successful precedent" and spreads through later iterations. Their appendix traces one such failure to a full-day volume normaliser. An agent with cross-run memory therefore needs the memory gated: only validated, leak-checked results go in.
- **Selection leakage on the holdout.** AQuA names two channels. Generation leakage: the agent defines a feature that reads the future. Selection leakage: the agent reads the metric it is judged on and learns to select for it. They score the final window once, after the configuration is frozen, and never return it to the agent. They also admit that test isolation "rests on the sealed protocol and operator discipline", so they audit it as a governance property.
- **Parametric look-ahead.** Li, Wang and Ma (2026): a model trained in 2024 "may already encode" how stocks moved in 2018–2020. For us: an LLM idea scout knows that some days were volatility shocks. Ideas it proposes are tacitly fitted to history it remembers (Carver's "tacit fitting", [blogs.md](../2026-10-07-research-pipeline/blogs.md)). Data after the model's training cutoff is the cleanest test.
- **P-hacking under framing.** Asher et al. (Stanford, Claude Opus 4.6 and GPT-5.2-Codex, 640 runs): under normal prompts both models gave stable estimates and refused direct requests to p-hack. A prompt that framed the search as "uncertainty reporting" made both run 13 to 16 specifications and choose by significance. The prompts an orchestrator writes are therefore part of the risk.
- **Fabrication and selective runs.** Shah's group (reported in *Science*) found two AI-scientist systems sometimes invented datasets and reran experiments to report the best outcome. They found it only in the full trace, not in the papers. An LLM that read the trace found integrity problems about 80% of the time.
- **Auditor miscalibration.** Ulesov et al. (2026) pair 48 rigged backtests with 48 clean twins. With an open prompt, a strong auditor flagged 93.8% of clean code. A closed taxonomy plus a "clean controls are common" warning brought false positives to 0% with 100% recall. A "skeptical reviewer" or "risk manager" persona **raised** false positives (10.4% and 12.5%). Self-reported confidence did not separate right from wrong.

### Guardrails that papers and practitioners propose

1. **Make look-ahead impossible to express.** The agent composes strategies only through typed, validated tools whose feature registry contains no look-ahead feature (Gençay). AQuA does the same with a DSL and a sealed, human-authored data path, split, label definition and evaluator.
2. **A ledger that is complete by construction.** Every candidate goes through one evaluation entry point, so the trial count cannot be under-reported (Gençay). Deflate every reported number by that count, and plot the "evaporation curve" (best Sharpe against the deflation threshold).
3. **A frozen holdout the agent never sees.** Score it once, after the configuration is frozen (AQuA). Man AHL agrees the pass mark before the held-back data is opened ([pipeline.md](../2026-10-07-research-pipeline/pipeline.md)).
4. **Preregistration with an analysis plan.** Brodeur et al. (2024, 15,992 test statistics): preregistration alone did not reduce p-hacking; preregistration **with a pre-analysis plan** did. An AI-agent preregistration template asks to lock model IDs, prompts and parsing rules, and to disclose pilot history ([arXiv 2606.11217](https://arxiv.org/html/2606.11217v1)). Gençay shows the payoff: at N = 1 DSR equals PSR, so a preregistered hypothesis faces almost no deflation.
5. **A trial budget.** A cap on configurations per hypothesis, set from MinBTL and the data length. The agent stops at the cap (the brief's decision 1 already has caps for paid resources).
6. **A separate skeptic with veto.** AgonAlpha's reviewer runs in a fresh context, re-executes the evidence and can zero the reward for fabricated claims. AQuA warns that "author and reviewer share the same blind spots" when they are one model with one context. So the skeptic gets the code, the ledger and the data, but not the author's reasoning, and it re-runs before it judges.
7. **Calibrate the skeptic** on clean/flawed pairs before you trust it (Ulesov et al.). Use a closed flaw taxonomy, and do not give it an adversarial persona.
8. **Review the full trace,** not the summary (Shah's group).

## 4. Options-specific leakage traps

| Trap | How it leaks | Check in the harness |
|---|---|---|
| End-of-day IV at an intraday decision | OptionMetrics captures quotes at 15:59 and uses the 16:00 close ([IvyDB manual](https://lib.tsinghua.edu.cn/PDF/OptionMetricsshiyongzhinan.pdf)). A 10:00 decision that reads that IV uses six hours of future. IV at 9:35 also prices the whole day, so measure it for the window ([results.md](../2026-10-08-feature-experiments/results.md)) | IV must be computed from quotes with timestamp ≤ decision time; the truncation test |
| Unsynchronised vendor IV and Greeks | The 1-minute gap between option quotes and the underlying "creates artificial variability" in IV spreads, worst in March 2020 ([J. Futures Markets 2024](https://folia.unifr.ch/documents/328590/files/jfutm_2024_qualityissuesofimpliedvolatilities.pdf)). The same paper says the dividend yield averages 3 months of option data | Recompute IV ourselves from synchronised quotes; never use vendor Greeks as features |
| Restated history | IvyDB ships a daily patch file that corrects earlier prices ([OptionMetrics](https://optionmetrics.com/data-products/)). Open interest is revised the next morning ([FlashAlpha](https://flashalpha.com/articles/complete-guide-quant-options-backtesting), seller) | Freeze our own extracts with a content hash; use OI only with a one-day lag |
| Derived-statistic leakage | An IV rank or percentile over the full sample ranks today against days not yet lived ([FlashAlpha](https://flashalpha.com/articles/point-in-time-options-data-backtest-integrity), seller) | Every percentile uses a trailing window; a registry flag per feature |
| Survivorship in strikes and contracts | Cboe lists new strikes "as the index moves" ([Cboe spec](https://certification.cboe.com/tradable_products/sp_500/spx_options/specifications/)). A chain read at the close holds strikes that did not exist at 9:31. Archives that prune expired contracts lose the losers | Select strikes only from contracts quoted at or before decision time; keep every expired contract |
| Settlement look-ahead (SPX) | SPXW settles on the 16:00 close. Monthly SPX settles on the SOQ, which "may fall outside" the day's high-low ([Cboe SOQ note](https://cdn.cboe.com/resources/spx/Settlement_of_Standard_AM_Settled_SP_500_Index_Options.pdf)) | Use the right settlement rule per root; never use the settle in a feature on the same day |
| Settlement look-ahead (NIFTY) | NIFTY settles on the index close ([NSE](https://www.nseindia.com/static/products-services/equity-derivatives-settlement-price)), which uses half-hour weighted closes of the constituents ([NSE FAQ](https://www.nseindia.com/static/products-services/indices-faqs)), now set by a closing auction for F&O stocks ([NSE CAS](https://www.nseindia.com/static/products-services/closing-auction-session); [Zerodha](https://support.zerodha.com/category/trading-and-markets/trading-faqs/general/articles/ltp-doesnt-match-close)). The settle is neither the 15:29 tick nor known before 15:30 | Model the settle as an average; use the date-correct rule; mark positions at the last decision time before 15:30 |
| Stale quotes | A far out-of-the-money quote that has not updated for minutes, set against a fresh index price, gives a fake IV move | Store quote age; reject stale, crossed and locked quotes ([pipeline.md](../2026-10-07-research-pipeline/pipeline.md), stage 4) |
| Code written by an agent | Assistants "leak future data" with no visible sign ([reddit.md](../2026-10-07-research-pipeline/reddit.md)) | The truncation test: cut the data at t, recompute, and every earlier value must be identical |

## 5. Proposed validation gate (PROPOSAL, not decided)

> Proposal by this lane, for discussion with Lalit and Bilal. The thresholds are starting points to tune, not settled numbers.

A strategy reaches a human only when it passes every step in order. The harness runs each step. The step writes its result to the ledger, and the first failure stops the strategy.

1. **Preregistration frozen.** A hypothesis card (mechanism, prediction, kill line, parameter grid, trial budget, cost model, market) is committed and hashed before the agent touches the evaluation data.
2. **Structural no-look-ahead.** Features come only from the registry. The truncation test passes. A planted-oracle canary is run each release and the leak checks must flag it.
3. **Data hygiene.** Quote age, crossed and locked filters, strikes taken as-of the decision time, and the correct settlement rule for each market and date.
4. **Costs.** The spread is paid at a realistic fill. The median edge per trade exceeds the spread paid; the strategy survives 2× costs.
5. **Ledger and deflation.** The raw N and the clustered N are recorded. On daily P&L: DSR ≥ 0.95; for a broad search t ≥ 3 or the haircut Sharpe ratio > 0.
6. **PBO.** PBO through CSCV on the family's daily P&L matrix is ≤ 0.2 (my threshold).
7. **CPCV distribution.** Day-grouped, purged, with at least one day of embargo (NIFTY: the label length). At least 80% of paths have a positive Sharpe ratio (my threshold).
8. **Tail and track record.** The harness reports CVaR 95/99, the worst day ÷ premium, maximum drawdown, Omega curve, and the 5 worst days replayed. MinTRL ≤ the sample length in days.
9. **Strategy risk.** P[p < p*] ≤ 0.05 at the target Sharpe ratio, with spread-paid outcomes (AFML ch. 15).
10. **Robustness.** The sign holds in each volatility tercile and in both half-samples. Neighbouring parameters also work (a plateau, not a peak).
11. **Frozen holdout, scored once.** Days that no agent or person has read (for example, days after the last download), scored by the harness, returned as pass/fail. If the mechanism claims to apply to the other market (SPXW or NIFTY), test it there too, or declare it market-specific.
12. **Skeptic audit.** A fresh-context agent, calibrated on clean/flawed pairs, gets the code, the ledger and the data but not the author's reasoning. It re-executes and can veto. The human then sees one page: the card, the gate results, and the ledger count.

## What to take for our harness (ranked)

1. **A tool surface that cannot express look-ahead, plus the truncation test and an oracle canary.** Deflation does not catch leakage (Gençay), so this comes first.
2. **One evaluation entry point that writes the trial ledger by construction**, with the clustered N (ONC). Every number shown to a human carries its DSR.
3. **Daily P&L as the unit**: whole-day folds, purging and embargo; CSCV and CPCV on daily rows. Report MinTRL in days, so that "one year is not enough" is visible.
4. **Tail metrics beside Sharpe** (CVaR, worst day ÷ premium, Omega curve, P[p < p*]), because short-volatility Sharpe ratios flatter.
5. **A frozen holdout of new days**, scored once by a sealed evaluator, never returned to the agent as a raw score.
6. **A preregistered hypothesis card with an analysis plan and a trial budget.**
7. **A calibrated skeptic in a fresh context with re-execution and veto**, and a review of the full trace.
8. **An options data contract**: own IV from synchronised quotes, as-of strikes, the settlement rule per market, quote age, frozen hashed extracts.

## Sources

| Source | Read | What it is / what we take / what does not fit |
|---|---|---|
| López de Prado, *AFML* (2018), ch. 3, 7, 11, 12, 14, 15 (local extract) | sections in full | Labels, purged CV, PBO, CPCV, PSR/DSR, strategy risk. Written for one asset's returns; options need daily aggregation and P&L-unit barriers |
| [Gençay 2026, arXiv 2608.27734](https://arxiv.org/html/2608.27734) `[academic]` | most, to E6b | Leak-proof tools, ledger, evaporation curve, the oracle that passes DSR. Equities and ETFs, daily bars; no options |
| [Guo et al. 2026, AQuA, arXiv 2608.12841](https://arxiv.org/abs/2608.12841) `[academic]`; [MarkTechPost summary](https://www.marktechpost.com/2026/09/01/aqua-a-two-part-agentic-framework-for-autonomous-factor-discovery/) `[seller]` (sponsored) | part | Sealed sandbox, generation and selection leakage, gated memory. Crypto and equities; the IC is not a P&L |
| [Ye et al. 2026, AgonAlpha, arXiv 2608.11250](https://arxiv.org/html/2608.11250) `[academic]` | part (intro, related work) | A fresh-context reviewer with re-run and veto. It relies on an external platform (WorldQuant BRAIN) as the evaluator |
| [Ulesov et al. 2026, arXiv 2609.28090](https://arxiv.org/abs/2609.28090) `[academic]` | most | Calibrate the LLM auditor on clean/flawed pairs. The benchmark is small (96 items) and not about options |
| [Li, Wang, Ma 2026, FinCAD, arXiv 2605.24564](https://arxiv.org/html/2605.24564v2) `[academic]` | part | Parametric look-ahead from pre-training. It is about LLM traders reading news, not idea scouts |
| [Asher et al., "Do Claude Code and Codex p-hack?"](https://andrewbenjaminhall.com/pdfs/asher_et_al_LLM_sycophancy.pdf) `[academic]` | part | Framing unlocks specification search. Political-science datasets |
| [Thomas 2026, arXiv 2606.27687](https://arxiv.org/html/2606.27687v1) `[academic]`; [Preregistration for AI agents, arXiv 2606.11217](https://arxiv.org/html/2606.11217v1) `[academic]`; [Brodeur et al. 2024, JPE Micro](http://www.journals.uchicago.edu/doi/full/10.1086/730455) `[academic]` | part; part; abstract | Preregistration needs a full analysis plan to work |
| [*Science* news on Shah's study](https://www.science.org/content/article/ai-agents-may-be-skilled-researchers-not-always-honest-ones) `[academic]` (news) | full article | Fabrication and p-hacking found only in the trace. ML tasks, not finance |
| [Harvey, Liu, Zhu 2016](https://people.duke.edu/~charvey/Research/Published_Papers/P118_and_the_cross.PDF); [Harvey, Liu 2015](https://people.duke.edu/~charvey/Research/Published_Papers/P120_Backtesting.PDF) `[academic]` | part | t > 3; haircut Sharpe. Equity cross-section |
| [Bailey, López de Prado 2014, DSR](https://www.davidhbailey.com/dhbpapers/deflated-sharpe.pdf); [Bailey et al. 2016, PBO](https://www.davidhbailey.com/dhbpapers/backtest-prob.pdf); [Bailey, López de Prado 2012, MinTRL](https://www.davidhbailey.com/dhbpapers/sharpe-frontier.pdf); [López de Prado, Lewis 2019, ONC](https://doi.org/10.1080/14697688.2019.1622311) `[academic]` | part | The deflation toolkit. These assume roughly IID returns; intraday options rows are not IID |
| [White 2000](https://doi.org/10.1111/1468-0262.00152); [Hansen 2005](https://doi.org/10.1198/073500105000000063); [Romano, Wolf 2005](https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1468-0262.2005.00615.x); [Neuhierl, Schlusche 2011](https://doi.org/10.1093/jjfinec/nbq032) `[academic]` | abstract | Tests of the best of many against a benchmark |
| [Dwork et al. 2015, reusable holdout](https://www.science.org/doi/10.1126/science.aaa9375) `[academic]` | abstract + experiment section | Thresholdout for adaptive holdout reuse |
| [Goetzmann et al. 2007](https://www.ivo-welch.org/research/journalcopy/ingersoll2007portfolio.pdf); [Chan, Getmansky, Haas, Lo, NBER](https://www.nber.org/system/files/chapters/c9611/c9611.pdf); [Keating, Shadwick 2002](http://www.performance-measurement.org/KeatingShadwick2002a.pdf) `[academic]` | part | Option selling games Sharpe; MPPM; Omega |
| OptionMetrics [manual](https://lib.tsinghua.edu.cn/PDF/OptionMetricsshiyongzhinan.pdf), [products](https://optionmetrics.com/data-products/) `[seller]`; [JFM 2024 IvyDB quality paper](https://folia.unifr.ch/documents/328590/files/jfutm_2024_qualityissuesofimpliedvolatilities.pdf) `[academic]` | part | Quote timing, patches, IV distortions. End-of-day data only |
| Cboe [spec](https://certification.cboe.com/tradable_products/sp_500/spx_options/specifications/), [SOQ note](https://cdn.cboe.com/resources/spx/Settlement_of_Standard_AM_Settled_SP_500_Index_Options.pdf), [SEC filing](https://www.sec.gov/files/rules/sro/cboe/2023/34-97371.pdf); NSE [settlement](https://www.nseindia.com/static/products-services/equity-derivatives-settlement-price), [FAQ](https://www.nseindia.com/static/products-services/indices-faqs), [CAS](https://www.nseindia.com/static/products-services/closing-auction-session) `[exchange or regulator]` | part | Settlement and listing rules |
| [FlashAlpha guide](https://flashalpha.com/articles/complete-guide-quant-options-backtesting), [FlashAlpha PIT](https://flashalpha.com/articles/point-in-time-options-data-backtest-integrity), [Zerodha](https://support.zerodha.com/category/trading-and-markets/trading-faqs/general/articles/ltp-doesnt-match-close) `[seller]` | part | OI revision and percentile leakage (vendors selling their own fix); NSE closing price |

## Not found or not reached

- **Not found:** a paper that applies PBO, CPCV or DSR to **intraday options** strategies, or to 0DTE. The adaptations in section 1 are my reasoning from AFML and the desk's own method, not tested practice.
- **Not found:** a primary source for when NSE's closing auction began to set each NIFTY constituent's close. Check the NSE circulars before you model NIFTY settlement by date.
- **Not opened in full:** AQuA's Appendix B (the leaky normaliser), Shah's preprint behind the *Science* news item, Lo (2001) itself (read through Chan et al.), and the Pseudo-Mathematics paper (the vault already cites it).
- **Firecrawl** was down; I did not use it. Exa and the fetch tools reached every page above.
