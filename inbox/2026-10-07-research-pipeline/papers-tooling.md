promoted: 2026-10-23
> Lane papers-tooling, 39 sources read, 2026-10-07

# Papers and tooling: how practitioners research a strategy

Two workers wrote this report. The first read S1 to S30; the second re-read S30 in full and read S31 to S39. Seven sources were read only in part. Each finding drawn from them carries the mark: S8 (through someone else's notes), S11, S21, S35, S37 (through a fetch summary), S34 (passage extraction from a 317-page book) and S36 (talk abstract only).

## Summary

1. The papers disagree on where ideas should come from. Arnott-Harvey-Markowitz say theory must come first. López de Prado and Man's Jamil Baz say data can lead, provided the result is tested afterwards on data that was not used to find it. For options, the strongest source of ideas is someone forced to trade: end users who must buy puts, or structured-product hedging (Gârleanu-Pedersen-Poteshman, Bennett, Sinclair).
2. Screening ratios are real practice: implied minus historical vol (Goyal-Saretto), implied minus realised correlation, forward vol spreads (Goldman), skew scaled by the square root of time (Bennett). All of these are starting points, not tested edges.
3. Notebooks: trading firms use them for research and treat that code as disposable (Jane Street). Code that lasts goes into a tested library. Netflix and Cookiecutter give the clearest rules for when code moves out of a notebook.
4. The serious public options research repos (Vilkov 0DTE, OpenSourceAP, hkalager) use **scripts plus a module and a single entry point, not notebooks**. Public options notebooks (Goldman gs-quant, QuantConnect) are demos and sales material, and they contain no step that could kill the idea.
5. The most useful single tooling pattern is a parameter cell plus an immutable output notebook per run (papermill at Netflix, Notebooker at Man Group). Every run is then counted, and that count is the number of trials the multiple-testing papers ask for.
6. How much to discount a backtest is disputed. Harvey-Liu call the flat 50% haircut "a serious mistake". CFM say a factor of about 2 "seems to be the industry standard". On whether most findings are false, Harvey-Liu-Zhu say most are; Chen and Jensen-Kelly-Pedersen say most are true.
7. A process from inside a fund (Man AHL, 2015): write down the data split, the method and the expected result before testing; keep a record of every idea tried; count how many ideas die at each stage; trade each new strategy with the firm's own capital for 2-3 months first.
8. Options-specific traps found in this lane: stale and closing quotes, prices in the data not recorded at the same time (Goyal-Saretto, Cboe's 15:45 snapshot), a units error in the cost line that reversed a peer-reviewed 0DTE result (Vilkov), and Sharpe-based checks that under-penalise short-skew books (Harvey-Liu).
9. Nothing in this lane says how many ideas die in options research, or how long one options idea takes.

## 1. Where hypotheses come from

**Theory first, and the warning against stories made up after the fact.** A hypothesis written after seeing the data is a red flag. All data use is mining in some degree. — [Arnott, Harvey, Markowitz](https://www.smallake.kr/wp-content/uploads/2023/04/SSRN-id3275654.pdf), 2018/2019. "Any suspicion that the hypothesis was developed after looking at the data is an obvious red flag." `[academic]` `[general, not options]`

**Theory buys a lower bar.** A factor with a theory behind it needs less statistical evidence than one found by search. — [Harvey, Liu, Zhu](https://www.nber.org/system/files/working_papers/w20592/w20592.pdf), 2016. "A factor derived from a theory should have a lower hurdle" `[academic]` `[general, not options]`. Harvey adds that a single-test p-value only "makes sense if researchers are strongly motivated by an economic theory" ([Harvey & Liu](https://people.duke.edu/~charvey/Research/Published_Papers/P120_Backtesting.PDF), 2015). `[academic]`

**Disagreement: data first.** López de Prado lets the data find features first and builds the theory afterwards; the backtest only checks the result. — [López de Prado](https://www.garp.org/hubfs/Whitepapers/a1Z1W0000054x6lUAA.pdf), 2018. "feature importance is a research tool, and backtesting is not." `[named practitioner]` `[general, not options]`. At Man, Baz agrees that data mining used correctly "can stumble across things without needing the theoretical prior". Harvey answers: "Theory is flexible, so theory alone is not enough" ([Man AHL board](https://www.man.com/insights/overfitting-and-its-impact-on-the-investor), 31 May 2015). `[named practitioner]` `[general, not options]`

**Who is forced to trade (options).** Dealers cannot hedge perfectly, so end-user demand moves option prices. This gives the "who pays and why" behind index put richness and the skew. — [Gârleanu, Pedersen, Poteshman](https://www.nber.org/system/files/working_papers/w11843/w11843.pdf), 2005/2009. "end users are net long index options, especially out-of-money puts" `[academic]`

**Flow imbalance as the stated precondition (options).** Bennett states what an edge needs: a source of imbalance that misprices risk, with structured-product flow and hedging demand as the examples. — [Bennett, *Trading Volatility*](https://www.trading-volatility.com/Trading-Volatility.pdf), 2014, *read by passage extraction, not in full*. "a source of imbalance in the markets (eg, structured product flow or regulatory demand for hedging)" `[named practitioner]`

**Risk premium or inefficiency (options).** Sinclair classes every edge as a risk premium, which can persist, or an inefficiency, which decays: an inefficiency's half-life is 6 months to 5 years. Behavioural stories serve as a checklist that justifies a pattern the data already showed. — [Sinclair, *Positional Option Trading*, via Abdelmessih's notes](https://notion.moontowermeta.com/positional-option-trading-by-sinclair), 2020, *read through someone else's notes; book not opened*. An inefficiency lasts "only until other people notice it". `[named practitioner]`

**Desk edge was in the data (options).** Sinclair says the 1980s vol-arbitrage edge came from collecting and processing data, not from the model. — same notes, *read through someone else's notes*. The edge "was in data collection and processing". `[named practitioner]`

**Screening implied against historical vol (options).** Sort stocks on historical minus implied vol. The motivation came first, from known facts: vol mean-reverts and option traders overreact. — [Goyal & Saretto](https://docs.lib.purdue.edu/cgi/viewcontent.cgi?article=1054&context=ciberwp), 2008/2009. "valuable information contained in the cross-section of implied volatilities which is disregarded by option traders" `[academic]`

**Screening with rules of thumb (options).** Bennett gives desk benchmarks: implied correlation trades about 5 points above realised, VIX futures 1-2 points above ATM-forward implied, and skew compared across maturities after multiplying by the square root of maturity. — [Bennett](https://www.trading-volatility.com/Trading-Volatility.pdf), 2014, *passage extraction*. "the levels of correlation sold are typically c5pts above realised correlation." `[named practitioner]`

**A forward-vol screen as the idea (options).** Goldman's notebook starts from the forward vol spread between SX5E and SPX implied by today's surfaces, then proposes the trade. — [gs-quant notebook](https://github.com/goldmansachs/gs-quant/blob/master/gs_quant/content/events/00_gsquant_meets_markets/01_ideas_for_risk_re_rating/eq_sx5e_spx_vol_spread_trade.ipynb), c. 2020. "The analysis shows a projected narrowing of vol spread" `[named practitioner]` `[seller]` (GS sells Marquee analytics)

**Screening tools packaged.** A popular repo turns Sinclair's realised-vol estimators into cones, percentiles and z-scores. It screens only realised vol; it does not compare with implied vol. — [jasonstrimpel/volatility-trading](https://github.com/jasonstrimpel/volatility-trading), last push Oct 2024. "A complete set of volatility estimators based on Euan Sinclair's Volatility Trading" `[seller]` (Python course)

**Published papers as a source, with decay.** Out-of-sample decay of published predictors measured near the original test is 20-36%; decay far from it reflects economic change. — [Chen](https://arxiv.org/pdf/2206.15365), v10 Nov 2025. "the decay is consistently less than 36%" `[academic]` `[general, not options]`

**Warned against: vendor demo ideas.** QuantConnect's research tutorial states its idea and then assumes it is true. — [QuantConnect/Research](https://github.com/QuantConnect/Research), read 2026-10-07. "in this example we will assume it holds." `[seller]` `[general, not options]`

## 2. From idea to testable statement

**Pre-register.** Write down the economic foundation, the hypotheses, data, tests and robustness checks before you look at the data. — [Harvey, Presidential Address](https://people.duke.edu/~charvey/Research/Published_Papers/P131_The_scientific_outlook.pdf), Aug 2017. "Before looking at the data, establish a research framework" `[academic]` `[general, not options]`

**Pre-registration inside a fund.** After studying backtest-overfitting research, Man AHL made researchers write their plan down in advance. — [Man AHL board](https://www.man.com/insights/overfitting-and-its-impact-on-the-investor), 2015. "You now have to write down the data partitioning and the methodology and expectations." `[named practitioner]` `[general, not options]`

**A checklist form.** Exhibit 2 of the backtesting protocol is a seven-part checklist. It requires a logical foundation and a falsifiable claim, and it can serve as a review form. — [Arnott et al.](https://www.smallake.kr/wp-content/uploads/2023/04/SSRN-id3275654.pdf), 2019. "Refrain from tweaking the model" `[academic]` `[general, not options]`

**Name the payer (options).** A hypothesis template follows from demand-based pricing. It names the end user, the intermediary who takes the other side, and the unhedgeable risk that intermediary is paid for. — [Gârleanu, Pedersen, Poteshman](https://www.nber.org/system/files/working_papers/w11843/w11843.pdf), 2005. "skew is heavily influenced by supply and demand factors" (desk quote the paper opens with). `[academic]`

**State what cannot be proven (options).** With no model of expected option returns, an abnormal return can never be shown to be mispricing rather than a risk premium. — [Goyal & Saretto](https://docs.lib.purdue.edu/cgi/viewcontent.cgi?article=1054&context=ciberwp), 2008. "The joint hypothesis problem is especially acute" `[academic]`

**Test against the simplest alternative with the same return (options).** Israelov compares put protection with a plain cut in equity exposure that earned the same return. He then simulates first without a vol premium and then with one, to separate two causes. — [Israelov, AQR](https://www.aqr.com/-/media/AQR/Documents/Journal-Articles/Pathetic-Protection-JAI-Wint19.pdf), Winter 2019. "comparing the drawdown characteristics of a protected strategy to another strategy that has 130% higher average returns" `[named practitioner]`

**Sinclair's four steps (options).** Identify the edge, choose the structure that captures it, size it, and "be aware of what you don't know". — [notes on Sinclair](https://notion.moontowermeta.com/positional-option-trading-by-sinclair), 2020, *read through someone else's notes*. "Be aware of what you don't know" `[named practitioner]`

**Committee bar relative to the book.** At CFM the review checks risk-reward, rebalancing frequency, maximum drawdown and correlation with existing strategies. The bar is a Sharpe ratio on what the strategy adds to the current book, not a stand-alone Sharpe. — [Rej, Seager, Bouchaud](https://arxiv.org/pdf/1902.01802), Feb 2019. "assume no improvement" `[named practitioner]` `[general, not options]`

**The slogan version.** Two Sigma's co-founder describes the cycle without detail. — [Siegel, Two Sigma](https://www.twosigma.com/insights/wsj-op-ed-by-david-siegel-investing-and-the-scientific-method), 14 Jun 2017, *read through a fetch summary*. "the formulation of carefully crafted hypotheses, followed by a recurring process of measurement, learning, and adjustment" `[named practitioner]` `[general, not options]`

## 3. Data

**Concrete option-quote filters (options).** Goyal-Saretto drop quotes that break arbitrage bounds, quotes with ask below bid, a zero bid, or a spread below one tick, and stale quotes (bid and ask unchanged from the previous day, or zero volume). They keep one near-ATM next-month contract per stock (moneyness 0.975-1.025). — [Goyal & Saretto](https://docs.lib.purdue.edu/cgi/viewcontent.cgi?article=1054&context=ciberwp), 2008. "To further ameliorate microstructure biases" (reason for forming portfolios on Tuesday, not Monday). `[academic]`

**Prices not recorded at the same time (options).** OptionMetrics Ivy DB records option and stock prices at different times, which breaks put-call parity checks. — same paper (footnote citing Battalio-Schultz 2006). "violations of the put-call parity relation" `[academic]`

**The vendor's own answer: a 15:45 snapshot (options).** Cboe sells NBBO snapshots at 15:45 ET and at the close, and says 15:45 better represents liquidity. IV and Greeks are a paid add-on, and the page does not say how they are computed. — [Cboe DataShop](https://datashop.cboe.com/option-quotes-end-of-day-with-calcs), undated, read 2026-10-07, *read through a fetch summary*. "considered a more accurate representation of market liquidity compared to end-of-day" `[seller]` (Cboe sells the data)

**Which strikes to keep (options).** When fitting a surface, desks drop strikes by a fixed moneyness band or by requiring a non-zero bid. Implied event jumps are computed only for near-dated expiries, because the bid-offer swamps far-dated ones. — [Bennett](https://www.trading-volatility.com/Trading-Volatility.pdf), 2014, *passage extraction*. "only use strikes between 80% and 120%) or by insisting on a bid price above zero" `[named practitioner]`

**The realised-vol window is a choice (options).** Bennett says the look-back length is not a trivial choice, that a one-off jump should be excluded, and that daily data beats weekly. — same, *passage extraction*. "Choosing the historical volatility number of days is not a trivial choice." `[named practitioner]`

**A units error in the cost column (options, 0DTE).** In Vilkov's package the spread was a fraction of spot and the return was in percent of spot, so the half-spread was charged at 1/100 of its size. The fix removed every positive net Sharpe. An outside replicator found it after reproducing the published table to four decimals. — [vilkovgr/0dte-strategies](https://github.com/vilkovgr/0dte-strategies), Aug 2026. "the correction reverses the sign of the net-of-cost conclusions" `[academic]`

**Three tiers of data access (options).** Vilkov ships derived Parquet panels; a rebuild needs paid vendor APIs (Massive, ThetaData); raw Cboe bars are "proprietary and not redistributed". hkalager's study needs paid WRDS subscriptions to OptionMetrics, CRSP and CUSIP. — [Vilkov](https://github.com/vilkovgr/0dte-strategies), Aug 2026; [hkalager/optionm](https://github.com/hkalager/optionm), Jun 2022. "you need an active subscription with WRDS" `[academic]` / `[unknown]`

**Whole chain, not your filtered subset (options).** QuantConnect's daily option-universe history returns every contract, so the user's own filter must be re-applied in research. — [QuantConnect docs](https://www.quantconnect.com/docs/v2/research-environment/datasets/equity-options/universes), read 2026-10-07, *read through a fetch summary*. "returns the entire Option chain for each trading day" `[seller]`

**Who holds what (options).** Testing demand-based pricing needs position data by participant type; open interest alone cannot give the dealer's sign. — [Gârleanu, Pedersen, Poteshman](https://www.nber.org/system/files/working_papers/w11843/w11843.pdf), 2005. "end users are net long index options" `[academic]`. (Price of such data: see `research/_raw/social-sweep.md`, not repeated.)

**Raw data is never edited.** Treat raw files as immutable and build everything else from them as a pipeline. — [Cookiecutter Data Science](https://cookiecutter-data-science.drivendata.org/opinions/), undated, read 2026-10-07. "raw data must be treated as immutable" `[unknown]` (open-source template from a data-science consultancy) `[general, not options]`

**Cleaning choices are p-hacking tools.** Dropping outliers, scaling and the choice of controls are where results get tuned; fix the sample and the winsorisation before the model. — [Harvey 2017](https://people.duke.edu/~charvey/Research/Published_Papers/P131_The_scientific_outlook.pdf); [Arnott et al. 2019](https://www.smallake.kr/wp-content/uploads/2023/04/SSRN-id3275654.pdf). "the model should explain all data" `[academic]` `[general, not options]`

**Errors that look like correct numbers.** Jane Street's ML lead says numerical code fails softly in pandas: the numbers come out slightly wrong and nobody notices. — [Signals and Threads ep. 5](https://signalsandthreads.com/python-ocaml-and-machine-learning/), 7 Oct 2020. "in this kind of soft way" `[named practitioner]`

Cost of data: nothing priced in this lane beyond the WRDS and vendor-API requirements above.

## 4. Notebooks

### Exploration only, or the full study?

**Trading firm: research only, and disposable.** At Jane Street, Python notebooks are for research. Anything that must last weeks or months is written in OCaml, and research code is fitted to today's data on purpose. — [Signals and Threads ep. 5](https://signalsandthreads.com/python-ocaml-and-machine-learning/), 7 Oct 2020. "Building trading systems in Python is not the best idea." `[named practitioner]` `[general, not options]`

**Data platform: the whole life-cycle.** Netflix runs notebooks from exploration through scheduled production jobs, with parameterised templates. — [Netflix, Beyond Interactive](https://netflixtechblog.com/notebook-innovation-591ee3221233), 16 Aug 2018. "run an experiment with different coefficients and summarize the results" `[named practitioner]` `[general, not finance]`

**Notebooks for everything (disagrees with Grus).** nbdev writes library modules, tests and docs from the notebooks themselves. — [Jeremy Howard, nbdev](https://hackernoon.com/test-nj2k3t7d), 5 Dec 2019, *read through a fetch summary; wording near-verbatim*. "work in notebooks without compromise for the entire life-cycle" `[named practitioner]` `[general, not finance]`

**A quant fund invests in notebooks.** Two Sigma built its own notebook (Beaker) and rebuilt it as Jupyter extensions for time series and research publication. — [Greenwood, JupyterCon](https://conferences.oreilly.com/jupyter/jup-ny-2017/public/schedule/detail/60072.html), 24 Aug 2017, *abstract only*. "time series plotting and processing, research publication" `[named practitioner]` `[general, not options]`

**Research notebook, then a separate backtest file.** QuantConnect tells users to test the hypothesis in a Jupyter research environment first; the backtest is a separate algorithm, and shared code lives once in the project's .py files. — [QuantConnect docs](https://www.quantconnect.com/docs/v2/research-environment/key-concepts/getting-started), *read through a fetch summary*. "we recommend testing your hypothesis in the Research Environment." `[seller]`

### How a research notebook is laid out

**A bank's published options notebook (options).** Goldman's "Systematic Selling" has six parts: (1) a summary with linked contents; (2) a session cell; (3) build the portfolio (sell one 1m10y straddle per day); (4) price it historically; (5) split P&L into premium, expiry payout and mark-to-market, then plot; (6) a one-line verdict. The library version is written into the notebook. — [gs-quant, 3-Systematic Selling](https://github.com/goldmansachs/gs-quant/blob/master/gs_quant/content/made_with_gs_quant/3-Systematic%20Selling.ipynb), c. 2020. "since beginning of 2019 this has mostly been a losing strategy" `[named practitioner]` `[seller]`

**Four-part trade-idea notebook (options).** Analyse the vol spread → trade idea and backtest → compare the strategy with the spread → price and Greeks. — [gs-quant vol spread notebook](https://github.com/goldmansachs/gs-quant/blob/master/gs_quant/content/events/00_gsquant_meets_markets/01_ideas_for_risk_re_rating/eq_sx5e_spx_vol_spread_trade.ipynb), c. 2020. "formulate a trade idea, analyze a trading strategy backtest and calculate spot price and greeks" `[named practitioner]` `[seller]`. Neither GS notebook has costs, an out-of-sample test or a kill condition.

**Folder and file layout.** `notebooks/exploratory/` for first passes and `notebooks/reports/` for polished work; names like `0.3-bull-visualize-distributions.ipynb` (step, owner, topic); the project is an installed package imported with `%autoreload 2`; preprocessing lives in `<module>/data/make_dataset.py`. — [Cookiecutter Data Science](https://cookiecutter-data-science.drivendata.org/opinions/), read 2026-10-07. "contains initial explorations" `[unknown]` `[general, not finance]`

**Keep it linear and short.** Netflix's three rules are: low branching, library functions in libraries, short and simple. — [Netflix, Scheduling Notebooks](https://netflixtechblog.com/scheduling-notebooks-348e6c14cfd6), 27 Aug 2018. "Low Branching Factor: Keep your notebooks fairly linear" `[named practitioner]` `[general, not finance]`

**Notebook as lab journal.** Write the reasoning down as you go, dead ends included; divide the notebook into clear steps and tell a story. — [Rule et al., Ten Simple Rules](https://arxiv.org/pdf/1810.08055), 2019. "document all your explorations, even (or perhaps especially) those that led to dead ends!" `[academic]` `[general, not finance]`

### What moves into a library, and when

**The trigger signs.** Move code out when you copy old notebooks to start new ones, paste functions between notebooks, or write classes inside a notebook. — [Cookiecutter Data Science](https://cookiecutter-data-science.drivendata.org/opinions/). "Classic signs that you are ready to move from a notebook to source code include duplicating old notebooks" `[unknown]` `[general, not finance]`

**Tests belong to the library, not the notebook.** Complex reusable functions go to a unit-tested package in the same repo; notebooks are not tested as code. — [Netflix](https://netflixtechblog.com/scheduling-notebooks-348e6c14cfd6), 2018. "we're not using notebooks as code libraries" `[named practitioner]` `[general, not finance]`

**Reused once → a module.** Wrap copy-pasted cells in a function; if another notebook needs it, make a module with unit tests. — [Rule et al.](https://arxiv.org/pdf/1810.08055), 2019. "consider turning it into a module, package, or library" `[academic]` `[general, not finance]`

**Grus's target layout.** A pinned environment, a parameterisable `load_data.py` and `model.py` with docs and unit tests, and a `run_experiment.py` that reproduces the result exactly. — [Grus, I Don't Like Notebooks](https://docs.google.com/presentation/d/1n2RlMdmv1p25Xy5thJUhkKGvjtV-dkAIsUXP-AL4ffI), 24 Aug 2018. "replicates exactly the original result" `[named practitioner]` `[general, not finance]`

**Parity test when code moves (options).** Goldman replaced a hand-built notebook backtest with a generic engine and kept both, plotting "Original series" against "Generic backtester". — [gs-quant Systematic Selling](https://github.com/goldmansachs/gs-quant/blob/master/gs_quant/content/made_with_gs_quant/3-Systematic%20Selling.ipynb). "we have built a generic backtesting framework to support the same flexibility with significantly less code" `[named practitioner]` `[seller]`. Jane Street does the same at handover: the exported model carries sample input and output values, which production must reproduce exactly ([Signals and Threads](https://signalsandthreads.com/python-ocaml-and-machine-learning/), 2020). `[named practitioner]`

### Reproducibility

**One immutable output notebook per run.** Tag a `parameters` cell; papermill injects run values and writes a new output notebook holding code, outputs and logs. — [Netflix](https://netflixtechblog.com/notebook-innovation-591ee3221233), 2018; [papermill](https://github.com/nteract/papermill), read 2026-10-07. "becomes an immutable record of that execution, containing the code, output, and logs" `[named practitioner]` `[general, not finance]`

**A quant fund's version.** Man Group's Notebooker reviews notebooks as Jupytext `.py` diffs, runs them as papermill templates "10s or 100s" of times, stores every result in MongoDB searchable by parameter, and deploys by merging into a `production` branch. — [Man Group, Notebooker](https://www.man.com/technology/notebooker), 15 Sep 2020. "often the hard work put into the code within a Jupyter Notebook is lost" `[named practitioner]` `[general, not options]`

**Text notebooks for review.** Jupytext pairs `.ipynb` with a `# %%` percent-format `.py`; you commit the `.py`. — [Jupytext README](https://github.com/jupytext/jupytext), read 2026-10-07. "Text notebooks are well suited for version control." `[unknown]` `[general, not finance]`

**How bad it is in public.** Of 863,878 GitHub notebooks they tried to run, a quarter ran and 4% reproduced. The paper's eight practices include pinning versions, keeping imports at the top, using relative paths, and re-running top to bottom before every commit. — [Pimentel et al.](https://leomurta.github.io/papers/pimentel2019a.pdf), MSR 2019. "only 24.11% executed without errors and only 4.03% produced the same results." `[academic]` `[general, not finance]`

### Public repos that hold real research, and how they are laid out

| Repo | Options? | Notebooks? | Layout |
|---|---|---|---|
| [vilkovgr/0dte-strategies](https://github.com/vilkovgr/0dte-strategies) | yes, SPXW 0DTE | none | `code/ingest/` one adapter per vendor; `config.py` for paths; `analysis/` one script per table; `run_replication.py` single entry; `tests/reference/` ground truth + parity test; `docs/manifests/` claim → code; `KNOWN-ISSUES.md` |
| [OpenSourceAP/CrossSection](https://github.com/OpenSourceAP/CrossSection) | no | none | `Signals/` one file per signal; `Portfolios/Code/` numbered R scripts run by `master.R`; `Shipping/` with an old-vs-new release check; placebo signals |
| [hkalager/optionm](https://github.com/hkalager/optionm) | yes, single stocks | none | one module class; methods `step1_crsp` → `step2_proc` → `analyse_buy/sell`; horizon as a parameter; figures per horizon |
| [jasonstrimpel/volatility-trading](https://github.com/jasonstrimpel/volatility-trading) | vol screening | none | package, one file per estimator, `tests/` CSVs |
| [goldmansachs/gs-quant content](https://github.com/goldmansachs/gs-quant/tree/master/gs_quant/content) | yes | all | numbered notebooks per case study and per asset-class screen |
| [QuantConnect/Research](https://github.com/QuantConnect/Research) | no | all | tutorial notebooks; idea assumed, not tested |

What the table shows: the repos whose results others have checked use scripts, no notebooks. The notebook repos are demos. Chen-Zimmermann on why their code is split into stages: "We separate the code so you can choose which parts you want to run." ([OpenSourceAP README](https://github.com/OpenSourceAP/CrossSection)) `[academic]` `[general, not options]`

### The case against notebooks

**Hidden state, from outside finance.** Grus: "notebooks have tons of hidden state that's easy to screw up and difficult to reason about" ([slides](https://docs.google.com/presentation/d/1n2RlMdmv1p25Xy5thJUhkKGvjtV-dkAIsUXP-AL4ffI), 2018). He also argues that poorly factored code is bad science. `[named practitioner]`

**Hidden state, from inside a trading firm.** Minsky: "you can look at a notebook, and you have no guarantee that it's in a consistent state" ([Signals and Threads](https://signalsandthreads.com/python-ocaml-and-machine-learning/), 2020). Mazare: if a restart from scratch does not reach the same conclusion, "it's actually annoying". `[named practitioner]`

**Where the two sides meet.** Grus does not object to markdown and inline plots, only to notebooks as the place code lives. Netflix and Man Group keep notebooks but move tests and reusable code into libraries. Nobody in this lane defends untested logic living only in a notebook.

## 5. The backtest

**Price costs at the full spread and report the drop (options).** Goyal-Saretto's long-short straddle return falls from 22.5% to 7.5% a month when options trade at the quoted spread; they also discuss margin as a limit on whether the trade can be run at all. — [Goyal & Saretto](https://docs.lib.purdue.edu/cgi/viewcontent.cgi?article=1054&context=ciberwp), 2008. "returns are reduced from 22.5% to 7.5% per month" `[academic]`

**Cost-line units are where a 0DTE result died (options).** A cost charged at 1/100 of its size survived peer review. Only a check on units exposed it: the implied dollar spread was smaller than the minimum tick. — [Vilkov](https://github.com/vilkovgr/0dte-strategies), Aug 2026. "no strategy or basket retains a positive net Sharpe ratio." `[academic]`

**Split the P&L before judging it (options).** Goldman splits a short-straddle strip into premium, expiry payout and mark-to-market, because premium against payout alone hides the risk. — [gs-quant Systematic Selling](https://github.com/goldmansachs/gs-quant/blob/master/gs_quant/content/made_with_gs_quant/3-Systematic%20Selling.ipynb), c. 2020. "doesn't speak to the volatility of this strategy" `[named practitioner]` `[seller]`

**Hedging with implied vol makes delta-hedged P&L depend on direction (options).** Delta-hedged P&L depends on the path and on the hedge frequency. If the delta uses implied vol rather than the vol still to be realised, the return depends on which way the market moves. — [Bennett](https://www.trading-volatility.com/Trading-Volatility.pdf), 2014, *passage extraction*. "returns are dependent on the direction of equity markets" `[named practitioner]`

**Use a public index when you lack a fill model (options).** Israelov tests a real protection strategy through the Cboe 5% Put Protection Index (PPUT), regressing 21-day overlapping returns with Newey-West t-statistics. — [Israelov](https://www.aqr.com/-/media/AQR/Documents/Journal-Articles/Pathetic-Protection-JAI-Wint19.pdf), 2019. "to deal with nonsynchronicity" `[named practitioner]`

**Sharpe-based checks miss short-skew books (options).** Harvey-Liu note that a high Sharpe can come from an option-like payoff with negative skew, so their haircut under-penalises premium selling. — [Harvey & Liu](https://people.duke.edu/~charvey/Research/Published_Papers/P120_Backtesting.PDF), 2015. "an option-like strategy with high ex ante negative skew" `[academic]`

Event-driven against vectorised engines, fill models, and margin modelling: nothing found in this lane beyond the above. Goldman's generic engine uses triggers and actions (`PeriodicTrigger`, `AddTradeAction`), which is event-style; earlier notes cover QuantConnect fills.

## 6. Checks against fooling yourself

**How big a haircut: disagreement.** Harvey-Liu say the haircut must depend on the number of tests and is not linear (Sharpe 0.75 after 200 tests becomes 0.32). — [Harvey & Liu](https://people.duke.edu/~charvey/Research/Published_Papers/P120_Backtesting.PDF), 2015. "it is a serious mistake to use the usual 50% haircut." `[academic]`. CFM find a factor of about 2 for typical Sharpes — [Rej, Seager, Bouchaud](https://arxiv.org/pdf/1902.01802), 2019. "in line with our experience and seems to be the industry standard" `[named practitioner]`. Both `[general, not options]`.

**Count your trials.** Without N you cannot judge overfitting. With 5 years of data, try at most about 45 configurations. — [Bailey, Borwein, López de Prado, Zhu](https://www.ams.org/notices/201405/rnoti-p458.pdf), May 2014. "if only five years of data are available, no more than forty-five independent model configurations should be tried." `[academic]` `[general, not options]`

**Research by backtest is the error.** Rerunning backtests until one looks good gives a false strategy after about 20 tries at 5%. — [López de Prado](https://www.garp.org/hubfs/Whitepapers/a1Z1W0000054x6lUAA.pdf), 2018. "imperative to control for the number of trials" `[named practitioner]` `[general, not options]`

**Walk-forward: disagreement.** López de Prado says walk-forward tests one path and is as easy to overfit as walking backward; he proposes combinatorial purged cross-validation (CPCV: many train/test splits, with training samples that overlap the test window in time removed). — same. "as easy to overfit" `[named practitioner]`. Arnott et al. warn that reusing out-of-sample data "is overfitting" and that the only true OOS is live trading ([2019](https://www.smallake.kr/wp-content/uploads/2023/04/SSRN-id3275654.pdf)). `[academic]` Both `[general, not options]`.

**Are most findings false? Disagreement.** — [Harvey, Liu, Zhu](https://www.nber.org/system/files/working_papers/w20592/w20592.pdf), 2016: "we argue that most claimed research findings in financial economics are likely false." `[academic]` — [Jensen, Kelly, Pedersen](https://www.nber.org/system/files/working_papers/w28432/w28432.pdf), 2021: evidence is "strengthened (not weakened) by the large number of observed factors." `[academic]` `[named practitioner]` — [Chen](https://arxiv.org/pdf/2206.15365), 2025: false discovery rate at most 25%, likely at most 9%. "consistently less than 36%" (OOS decay) `[academic]`. All `[general, not options]`.

**Selection at the committee, not just at the desk.** If 100 researchers each test one idea honestly and only the best reports, the firm is still fooled: a Sharpe of 0.6 over 23 years has p = 0.002 alone, but p = 0.15 as the best of 100. — [Roulston & Hand, Winton](https://www.portfolioconstruction.com.au/obj/articles_perspectives/PortfolioConstruction-Forum_Winton_Blinded-by-optimism.pdf), 22 Aug 2016. "force researchers to publish the results of all their studies" `[named practitioner]` `[general, not options]`

**The "improve until it passes" loop.** At CFM, a strategy that misses the bar is dissected and improved until it passes; the improvement fits the noise. — [Rej, Seager, Bouchaud](https://arxiv.org/pdf/1902.01802), 2019. "The performance enhancement simply comes from 'improving' the noise realization." `[named practitioner]` `[general, not options]`

**Parameter heat maps, fake data, outlier trimming.** — [Man AHL board](https://www.man.com/insights/overfitting-and-its-impact-on-the-investor), 2015. "If your parameter choice is an isolated point sticking out, then this is a red flag" (Harvey) `[named practitioner]` `[academic]` `[general, not options]`. Puchtler and Buchmann (ex-CERN) suggest adding noise or fake data first and touching real data last.

**Overfit or decayed: test both sides.** If a strategy fails both before and after its fitting window, suspect overfitting, not arbitrage. If many strategies break on one date, suspect a regime change; if only one breaks, suspect overfitting. — [Winton](https://www.portfolioconstruction.com.au/obj/articles_perspectives/PortfolioConstruction-Forum_Winton_Blinded-by-optimism.pdf), 2016; [Man AHL](https://www.man.com/insights/overfitting-and-its-impact-on-the-investor), 2015 (Ledford). "If you have a range of strategies, and you see the same breaking point" `[named practitioner]` `[general, not options]`

**Disagreement: hunter, not scientist (options).** Sinclair says to stop tuning windows once an effect holds across horizons and countries. — [notes on Sinclair](https://notion.moontowermeta.com/positional-option-trading-by-sinclair), 2020, *read through someone else's notes*. "a trader is a hunter rather than a scientist" `[named practitioner]`. This cuts against the trial-counting school above. Both camps agree that a robust effect should not hinge on one parameter value.

**Review by others catches what tests miss (options).** An outside replicator found Vilkov's units bug; Chen-Zimmermann carry placebo signals and a built-in comparison with Harvey-Liu-Zhu. — [Vilkov](https://github.com/vilkovgr/0dte-strategies), 2026; [OpenSourceAP](https://github.com/OpenSourceAP/CrossSection). "the correction reverses the sign" `[academic]`

**When the effect is rare, t > 3 is not enough.** — [Harvey 2017](https://people.duke.edu/~charvey/Research/Published_Papers/P131_The_scientific_outlook.pdf). "if the effect being studied is rare, even t > 3 will produce a large number of false positives." `[academic]` `[general, not options]`. Man's "SR" (not named on the page) doubts that a t of 3 rather than 2 has been shown to raise investor returns.

## 7. From a passed test to real money

**Live trading is the only true out-of-sample; do not tweak.** — [Arnott et al.](https://www.smallake.kr/wp-content/uploads/2023/04/SSRN-id3275654.pdf), 2019. "the only true out of sample is the live trading experience" `[academic]` `[general, not options]`

**Test trading with own capital, 2-3 months.** Too short to prove anything statistically, but it has caught research and implementation errors. A large early drawdown is the warning: 20% in three months does not fit an expected Sharpe of 3. — [Man AHL board](https://www.man.com/insights/overfitting-and-its-impact-on-the-investor), 2015. "all strategies are first traded with the firm's capital." `[named practitioner]` `[general, not options]`

**Parity before go-live.** Production must reproduce the research model's sample outputs exactly before it trades. — [Signals and Threads ep. 5](https://signalsandthreads.com/python-ocaml-and-machine-learning/), 2020. The export carries the weights "as well as some sample values". `[named practitioner]` `[general, not options]`

**When to stop.** Set the stop-out from the strategy's own expected drawdown; recovery takes about three times as long as the loss took to build. If returns are assumed IID normal, good managers get fired. — [Bailey & López de Prado](https://escholarship.org/content/qt758637dr/qt758637dr.pdf), Dec 2015. "On average, the recovery spans three times the period involved in accumulating the maximum quantile loss." `[academic]` `[named practitioner]` `[general, not options]`. For short-option books the IID-normal assumption fails in both directions (inference from S3 and S28, not a source claim).

**Expect decay.** Published effects shrink 20-36% out of sample even when true. — [Chen](https://arxiv.org/pdf/2206.15365), 2025. "These numbers suggest that at least 36% of discoveries are true." `[academic]` `[general, not options]`

**Hypothetical vs live.** Winton cites ETF and CTA studies where backtested performance did not match live results. — [Roulston & Hand](https://www.portfolioconstruction.com.au/obj/articles_perspectives/PortfolioConstruction-Forum_Winton_Blinded-by-optimism.pdf), 2016. "Blinded by optimism" (title) `[named practitioner]` `[general, not options]`

**What professionals fear in live options books (options).** Sinclair says it is "meta risks": contract spec changes, index changes, counterparties, fraud. — [notes on Sinclair](https://notion.moontowermeta.com/positional-option-trading-by-sinclair), *read through someone else's notes*. "meta risks" `[named practitioner]`

Paper trading and a method for comparing live results with the backtest: nothing options-specific found in this lane.

## 8. Records and killing ideas

**Keep a record of everything tried; track the rejection rate.** — [Man AHL board](https://www.man.com/insights/overfitting-and-its-impact-on-the-investor), 2015. "we do keep a record of the things we try" (Sargaison); Baz: count how many ideas die in research, in review and in test trading. `[named practitioner]` `[general, not options]`

**Do not punish a good test that failed.** Punishing a failed test drives data mining. — same (Harvey). "The second researcher should not be punished just because the finding was negative." `[academic]` `[general, not options]`. Arnott et al. agree that "most experiments will fail" and that a firm should reward good science, not good results ([2019](https://www.smallake.kr/wp-content/uploads/2023/04/SSRN-id3275654.pdf)).

**Report all results.** — [Harvey 2017](https://people.duke.edu/~charvey/Research/Published_Papers/P131_The_scientific_outlook.pdf). "Report all results, not just a selection of significant results" `[academic]` `[general, not options]`

**Log dead ends in the notebook itself.** — [Rule et al.](https://arxiv.org/pdf/1810.08055), 2019. "Document the Process, Not Just the Results" `[academic]` `[general, not finance]`. The papermill/Notebooker output notebook ([Netflix](https://netflixtechblog.com/notebook-innovation-591ee3221233); [Man](https://www.man.com/technology/notebooker)) is a record of each run that cannot be edited afterwards.

**Error log and null results in public (options).** Vilkov's `KNOWN-ISSUES.md` records the bug and its fix; hkalager's README leads with its null result. — [hkalager/optionm](https://github.com/hkalager/optionm), 2022. "This is an exploratory study with no profitable strategy in sight." `[unknown]`

**Records defend against self-deception (options).** — [notes on Sinclair](https://notion.moontowermeta.com/positional-option-trading-by-sinclair), *read through someone else's notes*. "Few of these investors who keep records will see that they are failing" `[named practitioner]`

**How long an idea takes.** López de Prado describes the failure mode of asking each PhD to produce a strategy within six months; he says to divide the work into an assembly line of specialists instead. — [López de Prado](https://www.garp.org/hubfs/Whitepapers/a1Z1W0000054x6lUAA.pdf), 2018. "demand that each of them produce an investment strategy within six months" `[named practitioner]` `[general, not options]`. Sinclair's half-life for an inefficiency, 6 months to 5 years, bounds how long a found edge is worth having (*via notes*).

**How many ideas die.** No firm in this lane gives a number. The nearest are the statistical ones: 20 random strategies give one with t > 2 (Arnott), and about 20 reruns of a backtest give one false pass at 5% (López de Prado).

## Hypothesis sources, ranked

Counts are sources in this lane that name the route as a real source of ideas; practitioners are those labelled `[named practitioner]`.

| Source of ideas | Sources naming it (practitioners) | Strongest link |
|---|---|---|
| Economic theory or a stated rationale first | 7 (3) | [Arnott, Harvey, Markowitz](https://www.smallake.kr/wp-content/uploads/2023/04/SSRN-id3275654.pdf) |
| Market structure: who is forced to trade (hedgers, structured products, put buyers) | 3 (2) | [Gârleanu, Pedersen, Poteshman](https://www.nber.org/system/files/working_papers/w11843/w11843.pdf) |
| Screening ratios: IV vs HV, implied vs realised correlation, forward vol, skew/√T | 5 (3) | [Goyal & Saretto](https://docs.lib.purdue.edu/cgi/viewcontent.cgi?article=1054&context=ciberwp) |
| Published papers, with expected decay | 5 (2) | [Chen 2025](https://arxiv.org/pdf/2206.15365) |
| Data mining / feature importance, then theory | 3 (2) — disputed | [López de Prado](https://www.garp.org/hubfs/Whitepapers/a1Z1W0000054x6lUAA.pdf) |
| Behavioural stories, used as a checklist after the data | 2 (1) | [Sinclair via Abdelmessih](https://notion.moontowermeta.com/positional-option-trading-by-sinclair) |
| Desk experience / better data handling | 2 (1) | same |
| Vendor or bank demo notebooks (warned against as evidence) | 3 (1) | [QuantConnect/Research](https://github.com/QuantConnect/Research) |

## Ten sources worth reading in full

1. [Arnott, Harvey, Markowitz — A Backtesting Protocol](https://www.smallake.kr/wp-content/uploads/2023/04/SSRN-id3275654.pdf) — Research Affiliates / Duke. Its seven-part checklist can be used as a review form for each study.
2. [Man AHL — Overfitting and Its Impact on the Investor](https://www.man.com/insights/overfitting-and-its-impact-on-the-investor) — Man AHL CIO and board. A fund describing its own records, written plans and test trading.
3. [Vilkov — 0dte-strategies, README and KNOWN-ISSUES](https://github.com/vilkovgr/0dte-strategies) — Frankfurt School. The best public layout of an options study, and a cost bug that reversed its result.
4. [Goyal & Saretto](https://docs.lib.purdue.edu/cgi/viewcontent.cgi?article=1054&context=ciberwp) — Purdue/Arizona State academics. The IV-vs-HV screen turned into a test, with concrete option-data filters and costs.
5. [Gârleanu, Pedersen, Poteshman](https://www.nber.org/system/files/working_papers/w11843/w11843.pdf) — NYU/AQR. How to ask "who pays the premium and why" for index options.
6. [Israelov — Pathetic Protection](https://www.aqr.com/-/media/AQR/Documents/Journal-Articles/Pathetic-Protection-JAI-Wint19.pdf) — AQR. A model of testing a claim against the simplest alternative with the same return.
7. [Roulston & Hand — Blinded by optimism](https://www.portfolioconstruction.com.au/obj/articles_perspectives/PortfolioConstruction-Forum_Winton_Blinded-by-optimism.pdf) — Winton. Why an honest researcher still fools the firm.
8. [Netflix — Scheduling Notebooks](https://netflixtechblog.com/scheduling-notebooks-348e6c14cfd6) — Netflix data platform. The clearest rules on what stays in a notebook and what moves to a library.
9. [Cookiecutter Data Science — Opinions](https://cookiecutter-data-science.drivendata.org/opinions/) — DrivenData. Folder layout, naming, and the signs that code should leave the notebook.
10. [Signals and Threads ep. 5 transcript](https://signalsandthreads.com/python-ocaml-and-machine-learning/) — Jane Street. How a trading firm separates disposable research notebooks from code that lasts.

## Could not open

| Link | Reason |
|---|---|
| Muravyev & Pearson, "Options Trading Costs Are Lower than You Think" (RFS 2020), SSRN 2580548 | SSRN download returned 403; no author-hosted copy found; a forum-hosted copy was not used because its legality is unclear |
| Bakshi & Kapadia, "Delta-Hedged Gains and the Negative Market Volatility Risk Premium" (RFS 2003) | Paywalled at OUP; no legal free copy found |
| Natenberg, *Option Volatility and Pricing* (McGraw-Hill 2015) | No legal full text found; not searched further. Nothing from it is cited |
| Sinclair, *Positional Option Trading* (Wiley 2020) | Book not opened; read only through Abdelmessih's notes (S8), marked on each finding |
| Bennett, *Trading Volatility*, direct PDF | A JavaScript challenge blocked direct download; read by passage extraction from the first part of the PDF only (S34) |
| Siegel, "Quants' Best Strategy Is From the 17th Century", WSJ 2017 | WSJ paywall; only Two Sigma's summary page read (S35) |
| Greenwood, "From Beaker to BeakerX" slides and video, JupyterCon 2017 | Not found; abstract only (S36) |
| Winton's original paper behind the FT 2014 "meta-overfitting" item | Not located; the 2016 reprint (S26) was read instead |
| Two Sigma and G-Research descriptions of research tooling | Nothing found: Two Sigma's site has slogan-level pages only; G-Research's news page (https://www.gresearch.com/news/) lists Arrow and Parquet posts but nothing on research process |
| hkalager/optionm Wiki | Not opened; README and code tree only |

## Appendix: working log

### S1. Arnott, Harvey, Markowitz — A Backtesting Protocol in the Era of Machine Learning (2018/2019)
https://www.smallake.kr/wp-content/uploads/2023/04/SSRN-id3275654.pdf (SSRN 3275654), full text read. [academic] (Arnott runs Research Affiliates, so also practitioner). [general, not options]
- Q1: hypothesis must exist before data; ex-post stories are flagged. "Any suspicion that the hypothesis was developed after looking at the data is an obvious red flag."
- Q1: data mining is unavoidable; "We are all data miners, even if only by living through a particular history".
- Q2: hypothesis needs a logical foundation and falsifiability; exploratory approach from medicine is "dangerous" in finance because no fresh OOS.
- Q6: track every strategy tried and their correlations; 20 random strategies give one t>2. Parallel-universe problem: one pre-chosen test is still one of many possible.
- Q3: sample period fixed ex ante; winsorisation level and transforms chosen before the model; "the model should explain all data".
- Q6: "the only true out of sample is the live trading experience"; iterated OOS "is overfitting".
- Q7: "Refrain from tweaking the model" when live underperforms the backtest.
- Q8: culture: "most experiments will fail"; reward good science, not good results; watch delegated research (assistants please the boss).
- Exhibit 2 is a 7-section checklist usable as a review form.

### S2. López de Prado — The 10 Reasons Most Machine Learning Funds Fail (JPM 2018; working paper Jan 2018)
https://www.garp.org/hubfs/Whitepapers/a1Z1W0000054x6lUAA.pdf, full text read. [named practitioner] (then at Guggenheim; later AQR, ADIA) + [academic] (LBNL). [general, not options]
- Q1, disagrees with S1: data can come before theory. "ML models do replace theory, they guide it" (sic; meaning: they guide it). Find the features that matter, then build a theory and test it on independent data.
- Q8/Q4: "Sisyphus paradigm" — one PhD building a whole strategy alone in six months ends in a false positive or a crowded factor. Successful firms run a "meta-strategy" assembly line: data curation, features, execution simulator, backtesting each owned by a specialist.
- Q6: Pitfall #2 "Research through backtesting": rerunning backtests until one looks good; "about 20 such iterations" give a false strategy at 5%. "feature importance is a research tool, and backtesting is not."
- Q6, disagrees with common walk-forward practice: walk-forward tests one path and is "as easy to overfit" as walk-backward; proposes combinatorial purged cross-validation (CPCV) to get a distribution of Sharpe ratios. Purging/embargo remove training labels that overlap test labels in time.
- Q6: without the number of trials I you cannot compute FWER, FDR or PBO; "imperative to control for the number of trials".

### S3. Harvey & Liu — Backtesting (JPM, Fall 2015)
https://people.duke.edu/~charvey/Research/Published_Papers/P120_Backtesting.PDF, full text read (first half closely, method sections skimmed). [academic] (Harvey: Duke, ex-editor JF, adviser to Man Group). [general, not options]
- Q6: the industry rule of thumb is to cut a backtested Sharpe by 50%; "it is a serious mistake to use the usual 50% haircut." The right haircut depends on the number of tests and is nonlinear: marginal Sharpe ratios are cut hard, very high ones only a little.
- Q6 worked number: 20 years monthly, Sharpe 0.75; after 200 tests the adjusted Sharpe is 0.32 (about 60% haircut). With N=10 tests, a p of 0.05 becomes about 0.40.
- Q6 options caveat, in the authors' own words: a high Sharpe "could be the results of non-normal returns, for instance, an option-like strategy with high ex ante negative skew." So the method under-penalises short-premium books.
- Q1: a single-test p-value only "makes sense if researchers are strongly motivated by an economic theory".
- Methods offered: Bonferroni, Holm (both FWER), BHY (FDR); authors publish a program to vary inputs.

### S4. Bailey, Borwein, López de Prado, Zhu — Pseudo-Mathematics and Financial Charlatanism (Notices of the AMS, May 2014)
https://www.ams.org/notices/201405/rnoti-p458.pdf, full text read. [academic] (López de Prado also practitioner). [general, not options]
- Q6: Minimum Backtest Length. "if only five years of data are available, no more than forty-five independent model configurations should be tried." With a two-year backtest, seven configurations already give an expected best in-sample Sharpe of 1 with zero out of sample.
- Q6/Q8: "a backtest which does not report the number of trials N ... makes it impossible to assess the risk of overfitting." The hold-out method alone cannot fix this because it ignores how many trials were made.
- Q6: when returns have memory (mean reversion, crowding, regime turns) overfitting does not just fail to help OOS, it makes OOS worse ("compensation effects").
- Side lead from the FT write-up of this paper (https://www.carmamaths.org/resources/jon/FTbackfit.pdf, FT 2014, read): Winton Capital warned of "meta-overfitting" because only the best-fitting strategies are sent up to the approval committee. Winton paper itself not read.

### S5. Harvey, Liu, Zhu — ...and the Cross-Section of Expected Returns (RFS 2016; NBER w20592)
https://www.nber.org/system/files/working_papers/w20592/w20592.pdf, read abstract, introduction and the publication-bias section; tables skimmed. [academic]. [general, not options]
- Q6: 316 published factors; a new factor needs t > 3.0, not 2.0. "we argue that most claimed research findings in financial economics are likely false."
- Q1: "A factor derived from a theory should have a lower hurdle than a factor discovered from a purely empirical exercise." Theory buys you a lower bar.
- Q8: publication bias: replication studies are hard to publish, so failed tests are hidden ("hidden tests").

### S6. Jensen, Kelly, Pedersen — Is There a Replication Crisis in Finance? (NBER w28432, 2021; JF 2023)
https://www.nber.org/system/files/working_papers/w28432/w28432.pdf, read abstract, introduction and figure 1 discussion. [academic] + [named practitioner] (Kelly and Pedersen at AQR). [general, not options]
- Q6, disagrees with S5: using a Bayesian model on 153 factors in 93 countries, most factors replicate, cluster into 13 themes, and work out of sample; their evidence is "strengthened (not weakened) by the large number of observed factors."
- Q6: "a non-trivial minority of factors fail to replicate ... much less disastrous than some people suggest." Their fix is not a higher t-bar but shrinkage toward a prior plus grouping related factors.
- Q4: code and data are public (github.com/bkelly-lab/GlobalFactor) — a reproducibility model.

### S7. Harvey — Presidential Address: The Scientific Outlook in Financial Economics (JF, Aug 2017)
https://people.duke.edu/~charvey/Research/Published_Papers/P131_The_scientific_outlook.pdf, read abstract, sections on p-hacking and section IX in full. [academic]. [general, not options]
- Q2 (pre-registration): "Before looking at the data, establish a research framework that includes: economic foundation, hypotheses to be tested, data collection methods" ... tests, statistics, reporting plan and robustness checks. Points to osf.io pre-registration and CONSORT-style checklists.
- Q6: "if the effect being studied is rare, even t > 3 will produce a large number of false positives." Offers the minimum Bayes factor, which combines the p-value with prior odds.
- Q3/Q6: lists the p-hacker's tools: dropping outliers, scaling, choice of controls, estimation method.
- Q8: "Report all results, not just a selection of significant results"; replicate a surprising result on new data before believing it.

### S8. Sinclair — Positional Option Trading (Wiley 2020), read through Kris Abdelmessih's chapter notes
https://notion.moontowermeta.com/positional-option-trading-by-sinclair (notes page, all toggles expanded, read in full). The book itself was NOT opened; these are Abdelmessih's notes, part quotation, part paraphrase. [named practitioner] x2 (Sinclair: Bluefin, Hull; Abdelmessih: SIG, Parallax). OPTIONS.
- Process in four steps, from the introduction: identify the edge; choose the structure that monetises it; size it; "Be aware of what you don't know".
- Q1: every edge is classed as a **risk premium** (someone pays for insurance; can persist) or an **inefficiency** (the market has not noticed; lasts "only until other people notice it"). Differentiating them "can be challenging". Alpha decay half-life for inefficiencies: 6 months to 5 years.
- Q1: ranked edge list with confidence levels. Level 3: term-structure roll, vol on value vs growth stocks, post-earnings drift. Level 2: "renting the straddle", overnight/weekend variance, FOMC event vol premium, options long vol-of-vol overpriced. Level 1: pre-earnings run-up fade, pre-earnings drift.
- Q1: behavioural stories may serve "as part of a checklist for why an inefficiency might exist"; "The data suggests the trade, but the psychological reason gives a theoretical justification" (paraphrase of Sinclair in the notes).
- Q1/Q3: the 1980s vol-arb edge "was in data collection and processing", not in the model.
- Q6/Q1: "a trader is a hunter rather than a scientist": do not fuss over 40- vs 45-day windows once a phenomenon is robust across horizons and countries. This sits against the parameter-hunting that S1-S4 warn about, from the other side.
- Q6: macro data gives "a small number of data points that occur a lot of times", so history is less informative than it looks.
- Q8: "Few of these investors who keep records will see that they are failing" (Sinclair quotation in the notes) — record keeping is the defence against self-deception.
- Q7: "meta risks" (contract spec changes, index changes, counterparty, fraud) are what professionals fear most, not market risk.

### S9. Goyal & Saretto — Cross-Section of Option Returns and Volatility (Purdue CIBER WP 2008; JFE 2009)
https://docs.lib.purdue.edu/cgi/viewcontent.cgi?article=1054&context=ciberwp, full working paper read (intro, data, cost sections closely). [academic]. OPTIONS.
- Q1 (the screening-ratio route): the paper IS the IV-vs-realised screen: sort stocks on 12-month historical vol minus ATM implied vol; long straddles where HV >> IV, short where HV << IV. Motivation given first from known facts: vol mean reverts, and option traders overreact (Stein 1989, Poteshman 2001). "there is valuable information contained in the cross-section of implied volatilities which is disregarded by option traders."
- Q3, concrete option-data filters (OptionMetrics Ivy DB, 1996-2005): drop prices that violate arbitrage bounds; drop ask < bid, zero bid, spread below one tick; drop a quote if both bid and ask equal the previous day's or volume is zero (stale/non-trading). Keep one near-ATM, next-month contract per stock (moneyness 0.975-1.025).
- Q3: Ivy DB records option and stock prices at different times, which breaks put-call parity tests (footnote citing Battalio and Schultz 2006).
- Q5: portfolios are formed on the Tuesday after expiry, not Monday, "To further ameliorate microstructure biases" (closing-quote effects).
- Q5: costs cut returns; long-short straddle return falls to 7.5% per month if traded at the full quoted spread; they cite effective/quoted spread ratios below 0.5 from other studies. Margin is discussed as a feasibility limit.
- Q2: "The joint hypothesis problem is especially acute ... no models for expected option returns", so an abnormal return can never be proven to be mispricing rather than risk.

### S10. Joel Grus — I Don't Like Notebooks (JupyterCon, 24 Aug 2018), slides with speaker notes
https://docs.google.com/presentation/d/1n2RlMdmv1p25Xy5thJUhkKGvjtV-dkAIsUXP-AL4ffI (text export read, about two-thirds). [named practitioner] (research engineer, Allen Institute for AI; ex-Google SWE). [general, not finance]
- Q4 case against: "notebooks have tons of hidden state that's easy to screw up and difficult to reason about" (his #1 complaint): cells run out of order, an edited cell not re-run.
- Q4: notebooks discourage modularity and tests: "how do you write tests for code that's in a notebook? not easily". "notebooks are a recipe for poorly factored code" and "poorly factored code is bad science".
- Q4, what he wants instead (concrete layout): a requirements.txt or Docker image; "clean, parameterizable load_data.py and model.py" with docs and unit tests; parameters and data paths set from outside; a run_experiment.py that "replicates exactly the original result".
- Q4: nbconvert to .py "still mixes 'library' code and 'execution' code".
- What he likes: markdown between code, inline plots. He does not object to notebooks for display, only as the place code lives.

### S11. Jeremy Howard — nbdev: use Jupyter Notebooks for everything (fast.ai, 5 Dec 2019; mirror on Hackernoon)
https://hackernoon.com/test-nj2k3t7d (read via fetch summary; quotes below are as returned, treat wording as near-verbatim). [named practitioner] (fast.ai founder; ex-president of Kaggle). [general, not finance]
- Q4 case FOR, disagrees with S10: aim is to "work in notebooks without compromise for the entire life-cycle". Exploration is development; the notebook keeps the charts, explanations and dead ends as documentation.
- Q4 mechanics: cells marked "#export" are written out as normal Python modules; "Tests are written directly in notebooks" and a command-line tool runs all notebooks' tests in parallel; docs are generated from the same notebooks; a merge driver resolves git conflicts in cell outputs; CI template on GitHub Actions.
- So the library still exists — it is generated from the notebook rather than written beside it.

### S12. Netflix (Ufford, Pacer, Seal, Kelley) — Beyond Interactive: Notebook Innovation at Netflix (16 Aug 2018)
https://netflixtechblog.com/notebook-innovation-591ee3221233, full text read. [named practitioner] (Netflix data platform engineers). [general, not finance]
- Q4: notebooks used for the whole life-cycle, not only exploration: data access, parameterised templates, and scheduled production runs.
- Q4 reproducibility mechanism: when a notebook is scheduled, a copy becomes the "source notebook"; each run creates a new "output notebook" that "becomes an immutable record of that execution, containing the code, output, and logs".
- Q4: parameterised notebook use by a data scientist: "run an experiment with different coefficients and summarize the results" (papermill runs many parameter sets concurrently and collects metrics).
- Q4: what lives outside the notebook: "a Python library that consolidates access to platform APIs"; one shared container image with fixed libraries and kernels.
- Q4 problem they hit: shared live notebooks were overwritten by colleagues, so read-only sharing (Commuter) was built.

### S13. Netflix (Seal, Kelley, Ufford) — Part 2: Scheduling Notebooks at Netflix (27 Aug 2018)
https://netflixtechblog.com/scheduling-notebooks-348e6c14cfd6, opened; relevant passages extracted verbatim (not every paragraph read). [named practitioner]. [general, not finance]
- Q4, the clearest "what moves to a library" rule found: "we're not using notebooks as code libraries and consequently aren't pressing for unit level tests on our notebooks, as those should be encapsulated by the underlying libraries."
- Their three notebook rules: "Low Branching Factor: Keep your notebooks fairly linear"; "Library Functions in Libraries": complex, reusable functions go to a unit-tested package in the same git repo; "Short and Simple is Better".
- Trigger for moving code out: "If a notebook becomes too complex to easily test, we have the local repository into which we can consolidate code".
- Q4 reproducibility: notebooks in git, tested with papermill before promotion, output notebook "provides the executed code, the outputs and logs from each code cell, and a repeatable template". A failed run is debugged by opening the output notebook "with our exact failed runtime parameterizations".

### S14. Man Group (Jon Bannister) — Notebooker: From Jupyter Notebook to a reproducible report in a jiffy (15 Sep 2020)
https://www.man.com/technology/notebooker, full text read; repo https://github.com/man-group/notebooker. [named practitioner] (Head of Data Platform Engineering, Man Group). Trading firm, but the tool is for reports, not alpha research. [general, not options]
- Q4: the problem stated by a quant fund: "often the hard work put into the code within a Jupyter Notebook is lost" — either a developer rewrites it as a report, or it "become[s] stale on the user's hard drive". Hard parts: "code review, testability, re-usability, execution, and browsing of results".
- Q4 review: notebooks are converted .ipynb -> .py with Jupytext so diffs can be reviewed; regression tests via a pytest-based CLI.
- Q4 reproducibility: a papermill parameters cell turns one notebook into a template run "10s or 100s" of times; every run's result stored in MongoDB, searchable by parameter, with stable URLs.
- Deploy = jupytext to .py, commit, merge into a `production` branch. Used internally since late 2018 for dashboards, reporting and "portfolio drilldowns".

### S15. Jane Street, Signals and Threads ep. 5 — Python, OCaml, and Machine Learning (Ron Minsky with Laurent Mazare, 7 Oct 2020), transcript
https://signalsandthreads.com/python-ocaml-and-machine-learning/, transcript read (long passages on notebooks extracted verbatim). [named practitioner] (Mazare: ML researcher at Jane Street, ex-DeepMind; Minsky: head of tech at Jane Street). Trading firm. (Podcast, but in this lane for the tooling content.)
- Q4: at Jane Street, Python notebooks are for research ("mostly for research purposes"), OCaml for anything that must last: "when things are there to last ... multiple weeks, or months, then OCaml is very neat." "Building trading systems in Python is not the best idea."
- Q4, research code is disposable on purpose: in a notebook "you actually want it to work on your data rather than on any potential data"; code "you get information from and then maybe never run again".
- Q4 hidden state, from inside a trading firm (agrees with S10): "you can look at a notebook, and you have no guarantee that it's in a consistent state ... nerve-wracking" (Minsky). Mazare: if you cannot restart from scratch and reach the same conclusion, "it's actually annoying".
- Q4 research-to-production handover: when a Python model is reimplemented in OCaml, the export includes the weights "as well as some sample values"; production must reproduce those exact outputs before it goes live — a parity test.
- Q3/Q4: pandas has "very weird corner cases"; errors in numerical code fail "in this kind of soft way" — the numbers are slightly wrong and nobody notices. Traders still check numbers fast in Excel.

### S16. Pimentel, Murta, Braganholo, Freire — A Large-scale Study about Quality and Reproducibility of Jupyter Notebooks (MSR 2019)
https://leomurta.github.io/papers/pimentel2019a.pdf, read abstract, method, and section V (best practices) in full. [academic]. [general, not finance]
- Q4 hard number: 1,159,166 GitHub notebooks; of 863,878 attempted runs, "only 24.11% executed without errors and only 4.03% produced the same results."
- Q4: most notebooks never move code into modules or tests; the bottom of a notebook is the least executed and least documented part.
- Q4 eight practices: short file names; check the bottom of the notebook; "Abstract code into functions, classes, and modules and test them"; pin versions in requirements files; test in a clean environment; imports at the top; relative data paths; "Re-run notebooks top to bottom before committing."

### S17. Rule, Birmingham, et al. — Ten Simple Rules for Writing and Sharing Computational Analyses in Jupyter Notebooks (PLOS Comp Bio 2019; arXiv 1810.08055)
https://arxiv.org/pdf/1810.08055, full text read. [academic]. [general, not finance]
- Q4/Q8, notebook as lab journal: Rule 2 "Document the Process, Not Just the Results" — "document all your explorations, even (or perhaps especially) those that led to dead ends!" Write the reasoning at the time; later you forget why you chose a parameter.
- Q4 when to move code out: Rule 4 "Modularize Code": instead of copy-paste-tweak cells, wrap in a function; if reused in another notebook, "consider turning it into a module, package, or library" with unit tests.
- Other rules: tell a story for an audience; divide into clear steps; record dependencies; version control; build a pipeline (Rule 7: notebook steps become a parameterised pipeline); share data; make notebooks readable, runnable, explorable.

### S18. DrivenData — Cookiecutter Data Science, "Opinions" page (v2 docs, undated; checked 2026-10-07)
https://cookiecutter-data-science.drivendata.org/opinions/, relevant sections quoted verbatim. [seller]? No — open-source template from DrivenData (a data-science consultancy). Label [unknown, credible open source]. [general, not finance]
- Q4 layout: `notebooks/exploratory/` "contains initial explorations", `notebooks/reports/` "is more polished work" exported to HTML. Naming `<step>-<ghuser>-<description>.ipynb`, e.g. `0.3-bull-visualize-distributions.ipynb`, so order and owner are visible.
- Q4 the move-out rule, most concrete found: "Classic signs that you are ready to move from a notebook to source code include duplicating old notebooks to start new ones, copy/pasting functions between notebooks, and creating object-oriented classes within notebooks."
- Q4 mechanics: project is an installed Python package; notebooks import it with `%load_ext autoreload` / `%autoreload 2`; preprocessing goes to `<module>/data/make_dataset.py`, notebooks read from `data/interim/`.
- Q3: "raw data must be treated as immutable ... never okay to change it in place"; analysis is a DAG from raw to processed.

### S19. Jupytext README (Marc Wouts and maintainers; current main branch, read 2026-10-07)
https://github.com/jupytext/jupytext (README read in full to the CLI section). [named practitioner] (open-source tool; Wouts was a quant at a bank when he wrote it — not verified this session, so treat as [unknown]). [general, not finance]
- Q4 tool: saves a notebook as plain `.py` in the "percent" format (`# %%` marks a cell, `# %% [markdown]` a text cell). "Text notebooks are well suited for version control. You can also edit or refactor them in an IDE."
- Q4 paired notebooks: keep `.ipynb` (with outputs) and `.py` (inputs only) in sync; commit the `.py` for review. One `jupytext.toml` with `formats = "ipynb,py:percent"` pairs a whole folder.
- This is the mechanism Man Group uses for review before deploy (S14).

### S20. papermill README and docs (nteract; read 2026-10-07)
https://github.com/nteract/papermill — read below. [general, not finance]
- Q4 mechanics: tag one cell `parameters` (holds defaults); papermill injects a cell `injected-parameters` after it with run values; `pm.execute_notebook('input.ipynb', 'output.ipynb', parameters=dict(...))` or CLI `papermill in.ipynb out.ipynb -p alpha 0.6` or `-f parameters.yaml`. Each run writes a new output notebook, so the parameters of every run are kept inside its output.
- "an *opinionated* approach ... based on our experiences using notebooks at scale in data pipelines" (Netflix origin, S12-S13).
- Relevance: for a parameter sweep, the honest count of trials (S2, S4) is the number of output notebooks.

### S21. QuantConnect docs — Research Environment: Getting Started, and Equity Options universe history (read 2026-10-07)
https://www.quantconnect.com/docs/v2/research-environment/key-concepts/getting-started and https://www.quantconnect.com/docs/v2/research-environment/datasets/equity-options/universes, read via fetch summaries. [seller] (QuantConnect sells cloud compute and data). OPTIONS (the second page).
- Q4: "Before you run backtests, we recommend testing your hypothesis in the Research Environment." Research = Jupyter with a `QuantBook` object (`qb = QuantBook()`, `qb.add_equity("SPY")`, `qb.history(...)`); the backtest is a separate algorithm file. Code in the project's .py files can be imported into the notebook, so shared logic lives once.
- Q3 options: `qb.option_history(symbol, start, end, Resolution.MINUTE)` gives chain history; a separate daily `OptionUniverse` history gives Greeks and IV per contract. Caveat stated: the daily universe call "returns the entire Option chain for each trading day, not the subset of contracts that pass your universe filter."
- Earlier note (backtest-and-data A3) already covers QuantConnect's fill-model and IV caveats; not repeated.

### S22. QuantConnect/Research GitHub repo — "Research 2 Production" notebook series (read 2026-10-07)
https://github.com/QuantConnect/Research, README and `Research2Production/Python/01 Mean Reversion.ipynb` read cell by cell. [seller] (QuantConnect). [general, not options]
- Q4 example of a vendor tutorial notebook: one markdown cell states the idea, one code cell builds the signal. The idea is not tested: "There are a number of ways to test for mean-reversion, but in this example we will assume it holds." Useful as a counter-example of the layout: hypothesis stated, never falsified, no costs, no out-of-sample.

### S23. Vilkov — 0dte-strategies replication package (README, KNOWN-ISSUES.md and file tree, last updated Aug 2026)
https://github.com/vilkovgr/0dte-strategies, README, KNOWN-ISSUES.md and full file list read. [academic] (Frankfurt School). OPTIONS (SPXW 0DTE, Sep 2016 - Jan 2026).
- This VERIFIES the claim that the earlier critique (_critique.md 2.1) flagged as unverified. README: "the correction reverses the sign of the net-of-cost conclusions: no strategy or basket retains a positive net Sharpe ratio." Cause in KNOWN-ISSUES: the spread column `bas` was a fraction of spot, the return column `reth_und` was percent of spot, and code subtracted one from the other, so the half-spread was charged at 1/100 size (0.022 bp vs 2.2 bp). A second scale error mislabelled turnover. Found by an outside replicator (gex.live) who first reproduced the published table "to four decimal places".
- Q4 layout of a real options research project (no notebooks at all): `code/ingest/` (one adapter per data vendor: Massive, ThetaData), `code/build_data.py`, `code/config.py` (all paths), `code/analysis/` with "One script per table/figure family", `code/run_replication.py` (single entry point), `data/` derived Parquet panels, `output/tables|figures`, `tests/reference/` ground-truth tables and `tests/test_replication.py` parity test, `tools/doctor.py` health check, `docs/manifests/` mapping each paper claim and exhibit to code, `KNOWN-ISSUES.md` as an error log.
- Q3: three data tiers: shipped derived panels; rebuild from vendor API (paid); raw Cboe bars "proprietary and not redistributed".
- Q6/Q8 lesson: a unit-scale bug in the cost line survived peer review and replication-to-four-decimals; only a units sanity check (implied dollar spread of $0.013 would be below the minimum tick) exposed it. The repo also names its own checks: clustered inference with multiple-hypothesis testing, structural break 2022, OOS protocol, tail-risk diagnostics.

### S24. Chen & Zimmermann — OpenSourceAP/CrossSection repo (README and tree, read 2026-10-07)
https://github.com/OpenSourceAP/CrossSection, README and file tree read. [academic] (Chen: Federal Reserve Board; Zimmermann: Cologne). [general, not options]
- Q4 layout of a large research codebase (~15,000 lines, 200+ signals): three stages in three folders — `Signals/` (download from WRDS, one file per signal, e.g. `Predictors/BrandInvest.py`), `Portfolios/Code/` (numbered R scripts `00_SettingsAndTools.R`, `10_DownloadCRSP.R`, `20_PredictorPorts.R` ... run by `master.R`), `Shipping/Code/` (packaging, `4_old_vs_new_check.R` compares a new release against the old one). Numbered scripts run in order; no notebooks.
- Q6: the repo carries `Placebos` (signals that should not work) and `Docs/Comparison_to_HLZ.csv` — a built-in check of their replications against Harvey-Liu-Zhu's list.
- Q4: credentials in `.env`, outputs in separate data folders, so a stage can be skipped by downloading its output.

### S25. Andrew Y. Chen — Most claimed statistical findings in cross-sectional return predictability are likely true (arXiv 2206.15365 v10, Nov 2025)
https://arxiv.org/pdf/2206.15365, abstract, introduction and OOS-reconciliation section read. [academic] (Federal Reserve Board). [general, not options]
- Q6, disagrees with S5 (HLZ "most ... likely false"): false discovery rate is at most 25% in eight of nine prior studies, and a tighter bound gives at most 9%. Reason: "randomly selecting accounting ratios produces statistically significant predictability far more often than would occur if there were no predictability."
- Q6/Q7 decay numbers: out-of-sample decay measured close to the original test is 20% (Chen-Zimmermann), 26% (McLean-Pontiff), 36% (Jacobs-Müller); far-away OOS decay reflects economic change (crowding, IT, retail), not false discovery.
- Read with care: "true" here means the in-sample effect is real, not that it survives costs or trades after publication. For an options desk the dispute matters less than the shared point: count tests, and expect a published edge to shrink by a quarter to a third or more.
- Replication code public: github.com/chenandrewy/mostly-true.

### S26. Roulston & Hand (Winton Capital) — Blinded by optimism (PortfolioConstruction Forum reprint, 22 Aug 2016; Winton paper c. 2013)
https://www.portfolioconstruction.com.au/obj/articles_perspectives/PortfolioConstruction-Forum_Winton_Blinded-by-optimism.pdf, full text read. [named practitioner] (Winton Capital research; Hand is also an Imperial College statistician). [general, not options]
- Q6/Q8 "meta-overfitting": each of 100 researchers can test one idea honestly, yet "if only the one researcher who found the highest level of predictability reported their results to management", the firm is fooled. Selection happens at the approval committee, not only at the desk.
- Q6 worked number: a Sharpe of 0.6 over 23 years has p = 0.002 against random strategies, but p = 0.15 if it was the best of 100.
- Q6 test for overfitting vs decay: a seasonal strategy fitted on 1980-2004 failed both before 1980 and after 2004; failure on both sides points to overfitting rather than "arbitraged away".
- Q8 fix: "force researchers to publish the results of all their studies", as with pre-registered clinical trials; Occam's razor; cross-validation.
- Q7: cites studies where hypothetical (backtest) performance of ETFs and CTAs did not match their live results.

### S27. Rej, Seager, Bouchaud (Capital Fund Management) — How should you discount your backtest PnL? (arXiv 1902.01802, Feb 2019)
https://arxiv.org/pdf/1902.01802, full text read (5 pages). [named practitioner] (CFM researchers; Bouchaud is CFM chairman). [general, not options]
- Q6, the overfitting mechanism described from inside a fund: when a strategy the team believes in misses the committee's Sharpe bar, it is "dissected into elementary building blocks" and "improved" until it passes. "The performance enhancement simply comes from 'improving' the noise realization." Base case: "assume no improvement".
- Q6 numbers: to be 99.9% sure a Sharpe of 0.5 is not noise needs 43 years of data. For typical CTA Sharpes of 0.3-0.5 their model gives a discount factor of about 2, "in line with our experience and seems to be the industry standard". This agrees with the 50% rule of thumb that S3 calls a mistake — a direct disagreement.
- Q2/Q7: the committee checks risk-reward, rebalancing frequency, backtest max drawdown and correlation to existing strategies; the bar is a residual Sharpe threshold against the current book, not a stand-alone Sharpe.

### S28. Bailey & López de Prado — Stop-outs under serial correlation and "the triple penance rule" (J. of Risk 18(2), Dec 2015)
https://escholarship.org/content/qt758637dr/qt758637dr.pdf, abstract and introduction read; derivations skimmed. [academic] + [named practitioner] (LdP then at Guggenheim). [general, not options]
- Q7 (when to stop a live strategy): set the stop-out from the strategy's own expected drawdown, not a round number. "On average, the recovery spans three times the period involved in accumulating the maximum quantile loss."
- Q7: firms "may be firing more than three times the number of skillful portfolio managers" than intended because they assume IID normal returns. For a short-option book, returns are not IID normal (S3's skew caveat), so a naive drawdown stop is miscalibrated in both directions.
- Q7: higher-Sharpe managers get looser stop rules, and the paper justifies that.

### S29. Gârleanu, Pedersen, Poteshman — Demand-Based Option Pricing (NBER w11843, 2005; RFS 2009)
https://www.nber.org/system/files/working_papers/w11843/w11843.pdf, abstract, introduction and empirical summary read. [academic] (Pedersen also AQR). OPTIONS.
- Q1 (market structure / who is forced to trade) — the academic basis of the "who pays and why" question for index options: dealers cannot hedge perfectly, so end-user demand moves prices. "end users are net long index options, especially out-of-money puts, which helps explain their apparent expensiveness and the smirk."
- Q2 template for a hypothesis: name the end user (forced or fundamental demand), the intermediary who takes the other side, and the unhedgeable risk the intermediary is paid for. Demand in one option raises its price in proportion to the variance of its unhedgeable part, and other options' prices in proportion to covariance.
- Q3: the evidence needs position data by participant type (dealers vs customers vs firm proprietary) — the CBOE open-close style data that earlier notes say costs ~$17k/month; OI alone cannot sign dealer positions.
- Opens with a desk quote: "[Option implied volatility] skew is heavily influenced by supply and demand factors" (Gray, Dresdner Kleinwort Benson) — practitioner intuition turned into a testable model.

### S30. Israelov (AQR) — Pathetic Protection: The Elusive Benefits of Protective Puts (J. Alternative Investments 21(3), Winter 2019)
https://www.aqr.com/-/media/AQR/Documents/Journal-Articles/Pathetic-Protection-JAI-Wint19.pdf (linked from https://www.aqr.com/Insights/Research/White-Papers/Pathetic-Protection-The-Elusive-Benefits-of-Protective-Puts). The earlier worker read only the landing page; re-read in full by the second worker (sections 1-2 closely, simulation sections skimmed). [named practitioner] (Israelov, principal at AQR). OPTIONS.
- Q2 method worth copying: test a claim ("puts protect against drawdowns") against the simplest alternative with the SAME realised return — a static cut in equity exposure. "comparing the drawdown characteristics of a protected strategy to another strategy that has 130% higher average returns can lead to incorrect conclusions."
- Q2/Q5: the benchmark is matched by construction: 36.5% SPX + 63.5% cash gave the same 2.5% excess return as the Cboe 5% Put Protection Index (PPUT), Jul 1986 - May 2016. Divesting had better peak-to-trough drawdowns 97% of the time on the shortest windows and 100% on windows over about half a year.
- Q3/Q5: uses a public Cboe benchmark index as the "real-world implementable" strategy, so no own fill model is needed; regressions on 21-day overlapping returns with Newey-West t-stats "to deal with nonsynchronicity".
- Q2/Q6: separates two causes by simulation: first with no vol premium (path dependence alone), then with a premium added. Result: "Put options are only effective in reducing drawdowns in the unusual circumstance that options are priced with no volatility risk premium and equity drawdowns precisely coincide with the option holding period."
- Q8: states its own limits ("out of the scope of this article": non-lognormal prices, stochastic vol premia) instead of claiming a general result; puts do win against one-day crashes.

### S31. Goldman Sachs — gs-quant `content/` folder and the "3-Systematic Selling" notebook (repo pushed 2026-10-01; notebook written c. 2020)
https://github.com/goldmansachs/gs-quant/tree/master/gs_quant/content, README read, folder tree listed, `made_with_gs_quant/3-Systematic Selling.ipynb` read cell by cell (25 cells). [named practitioner] (Goldman Sachs Marquee quant team; individual authors not named). Also [seller]: the notebooks need a GS Marquee client login and sell GS analytics. OPTIONS (swaption straddles).
- Q4 layout of a bank's published research notebook: (1) summary cell stating the study and a linked table of contents; (2) session/authentication; (3) "Create portfolio" (one sold 1m10y straddle per day); (4) "Evaluate portfolio historically"; (5) "Putting it all together" — split P&L into premium received, paid at expiry, and mark-to-market; (6) a one-line conclusion: "since beginning of 2019 this has mostly been a losing strategy". The library version used is written into the notebook ("produced using gs-quant version 0.8.102").
- Q4 what moved to a library, visible inside one notebook: the hand-built backtest (loops, futures, a `get_p` helper) was later replaced by a "generic backtesting framework" (`GenericEngine`, `PeriodicTrigger`, `AddTradeAction`). The notebook keeps both and plots "Original series" against "Generic backtester" for cash, mark-to-market and total — a parity test of library against notebook.
- Q5: the P&L is split into premium, expiry payout and MTM because "looking at only premium collected and amount paid out doesn't speak to the volatility of this strategy". No costs, no delta hedge in this edition ("Look out for future publications where I will build on this strategy with added delta hedging").
- Repo layout: `made_with_gs_quant/` numbered case studies (`1-Navigating Rates` ... `15-...`); `reports_and_screens/00_fx/0000_vol_screen.ipynb`, `0001_vol_calendar_screen`, `0005_vol_skew`, `02_rates/0001_vol_moneyness_screen` — screens kept as numbered notebooks per asset class; `events/` notebooks per client event.

### S32. Goldman Sachs — gs-quant "eq_sx5e_spx_vol_spread_trade" notebook (events/00_gsquant_meets_markets, c. Nov 2020)
https://github.com/goldmansachs/gs-quant/blob/master/gs_quant/content/events/00_gsquant_meets_markets/01_ideas_for_risk_re_rating/eq_sx5e_spx_vol_spread_trade.ipynb, all 16 cells read. [named practitioner] (GS) + [seller]. OPTIONS.
- Q1 a screen-first idea: start from a chart of 1y-forward 2y implied vol spread SX5E vs SPX (2014-2020), plus the "roll-up" implied by today's surface; "The analysis shows a projected narrowing of vol spread". The forward curve in the surface is itself the hypothesis source.
- Q4 four-part layout stated up front: "Analyze Vol Spread" -> "Trade Idea & Backtest" -> "Compare Performance" -> "Price & Greeks". The analysis function (`forward_vol_spread`) is defined in the notebook; pricing and backtests come from the library.
- Q2/Q6 gap: no kill condition, no out-of-sample, no costs; the disclaimer says "it is not a recommendation" and terms are "indicative". A sales-research notebook, not a falsification test — a useful contrast to S23 and S30.

### S33. jasonstrimpel/volatility-trading ("volest") — volatility estimators after Sinclair's *Volatility Trading* (1,957 stars, last push Oct 2024)
https://github.com/jasonstrimpel/volatility-trading, README and full file tree read. [seller] (the author sells the "Getting Started With Python for Quant Finance" course; the README carries an Amazon affiliate link). OPTIONS (vol screening).
- Q1 the screening-ratio route turned into a library: six realised-vol estimators (close-to-close, Parkinson, Garman-Klass, Rogers-Satchell, Yang-Zhang, Hodges-Tompkins) plus skew, kurtosis, correlation, each plotted as "Probability cones", rolling quantiles, rolling extremes, z-scores, and a ratio/regression "against arbitrary comparable"; output is a PDF "term sheet".
- Q4 layout: a package, not notebooks — `volatility/models/<Estimator>.py`, one file per estimator; `volest.py` drives; `tests/` holds two CSVs (JPM, BENCH). The README says the data feed broke when Yahoo changed its API, so data loading was made pluggable ("specify your own data").
- Caveat: it screens realised vol only; nothing compares it with implied vol or tests a trade.

### S34. Colin Bennett — *Trading Volatility: Trading Volatility, Correlation, Term Structure and Skew* (self-published 2014), free PDF from the author's own site
https://www.trading-volatility.com/Trading-Volatility.pdf (linked from https://www.trading-volatility.com/downloads.html, "Download Trading Volatility"). READ BY PASSAGE EXTRACTION: a tool pulled verbatim passages on how trades are judged from the first part of the 317-page PDF; the book was NOT read front to back, and later chapters may be missing from what was seen. [named practitioner] (Bennett: Head of Quantitative and Derivative Strategy at Santander; earlier Barclays Capital, Dresdner Kleinwort, Eurex — per a search snippet, not verified this session). OPTIONS.
- Q1 hypothesis from forced flow: an edge needs "a source of imbalance in the markets (eg, structured product flow or regulatory demand for hedging), causing a mispricing of risk". "Excessive demand for volatility products has historically caused implied volatility to be overpriced." Skew overpricing "can be considered to be a result of excessive demand for downside put options, potentially caused by hedging."
- Q1 screening ratios with rules of thumb: implied correlation sold "typically c5pts above realised correlation"; VIX futures "should be only c1-2pts above ATMf implied volatility, but during 2012 they were c5-6pts above"; skew compared across maturities by multiplying by square root of maturity; "a trader needs to evaluate the richness or cheapness of skew across different strikes".
- Q1/Q3 choice of the realised window: "Choosing the historical volatility number of days is not a trivial choice"; exclude a recent one-off jump; prefer daily to weekly data; Yang-Zhang and other OHLC estimators trade efficiency against bias.
- Q3: surface fitting drops strikes "via a fixed rule (ie, only use strikes between 80% and 120%) or by insisting on a bid price above zero"; implied event jumps are only computed for near-dated events because far-dated ones are "untradeable taking bid-offer spreads into account".
- Q5: delta-hedged P&L is path dependent and depends on hedge frequency and on the vol used for delta: using implied rather than remaining realised vol "means returns are dependent on the direction of equity markets".
- Nothing seen on backtest method, out-of-sample tests, records or killing ideas: in the passages seen, the book is about instruments and pricing, not research process.

### S35. David Siegel (Two Sigma co-founder) — WSJ op-ed "Investing and the Scientific Method" (14 Jun 2017), Two Sigma reprint page
https://www.twosigma.com/insights/wsj-op-ed-by-david-siegel-investing-and-the-scientific-method, read via a fetch summary of a short page; the full WSJ article is paywalled and was not read. [named practitioner]. [general, not options]
- Q1/Q2: the process is "the formulation of carefully crafted hypotheses, followed by a recurring process of measurement, learning, and adjustment." More data and compute need more discipline, not less.
- Thin: no description of tooling, notebooks, or how ideas die. Two Sigma's public material on its research process is at this slogan level.

### S36. Matt Greenwood (Two Sigma) — "From Beaker to BeakerX", JupyterCon NY, 24 Aug 2017 (talk abstract)
https://conferences.oreilly.com/jupyter/jup-ny-2017/public/schedule/detail/60072.html, abstract read; no slides or video opened. [named practitioner] (Two Sigma, leads BeakerX). [general, not options]
- Q4: a quant fund built its own notebook first (Beaker, c. 2012) and in 2016 rebuilt it as Jupyter extensions: "polyglot data science, time series plotting and processing, research publication, and integration with Apache Spark". Signal only: a large systematic fund chose to invest in notebooks rather than replace them. Nothing on layout or what moves into libraries.

### S37. Cboe DataShop — "Option EOD Summary" / Option Quotes End of Day with Calcs product page (undated; read 2026-10-07)
https://datashop.cboe.com/option-quotes-end-of-day-with-calcs, read via fetch summary. [seller] (Cboe sells the data). OPTIONS.
- Q3: two snapshots a day, "one at 15:45 U.S. Eastern and another at end-of-day"; NBBO bid/ask and size in each; OHLC, volume, VWAP and open interest at end of day. Why 15:45: it is "considered a more accurate representation of market liquidity compared to end-of-day". IV and Greeks are sold as an add-on at 15:45 only; the page gives no model, rate, dividend or American-exercise method. History from January 2012.
- Use: a study on closing quotes inherits the closing-quote problem that Goyal-Saretto (S9) avoided by forming portfolios on Tuesdays; the vendor's own answer is a 15:45 snapshot.

### S38. Man AHL Academic Advisory Board — "Overfitting and Its Impact on the Investor" (Man Institute, 31 May 2015)
https://www.man.com/insights/overfitting-and-its-impact-on-the-investor, full text read. [named practitioner] (Sargaison, CIO Man AHL; Granger, Ledford, Baz, Furdak, Puchtler, Buchmann) + [academic] (Harvey, Barberis, Shephard). One speaker appears only as "SR" and is not named on the page. [general, not options]
- Q6/Q2: after reading the probability-of-backtest-overfitting work, AHL made partitioning a written step: "You now have to write down the data partitioning and the methodology and expectations." (Sargaison) — pre-registration inside a fund.
- Q8: "we do keep a record of the things we try" (Sargaison). Baz names a "rejection rate": count how many ideas die in initial research, in review, and in test trading.
- Q7: "all strategies are first traded with the firm's capital"; test trading lasts "2-3 months", which Granger says "is not enough time to demonstrate any kind of statistical significance", yet it has caught research and implementation mistakes; a 20% drawdown in three months is inconsistent with an assumed Sharpe of 3.
- Q6 checks named: parameter "heat maps" — "If your parameter choice is an isolated point sticking out, then this is a red flag" (Harvey); add noise or fake data and see whether the effect behaves (Puchtler, Buchmann, from CERN practice); trim outliers; model confidence sets; independent review.
- Q6 overfitting vs decay: if many strategies break at the same date it is likely a regime change; if only one breaks, overfitting is more likely (Ledford). Agrees with S26's two-sided test.
- Q8 culture: a well-run test that fails "should not be punished"; punishing it "will lead to potentially extreme data mining" (Harvey). Disagreement: "SR" doubts that a t-stat of 3 instead of 2 has been shown to improve investor returns.

### S39. Arman Hassanniakalager — hkalager/optionm repo (OptionMetrics buy/sell-side study, last push Jun 2022)
https://github.com/hkalager/optionm, README and file tree read; the Wiki was not opened. [unknown] (the GitHub profile names him and a consultancy; his academic post was not verified this session). OPTIONS.
- Q4 layout of a small options study with no notebooks: `optionm_module.py` holds one class whose methods are the pipeline steps — `step1_crsp()` (pull OptionMetrics matched to CRSP via 8-character CUSIP), `step2_proc()` (realised-vol proxies), `analyse_buy()`, `analyse_sell()` — parameterised by `study_period` and `horizon` (10 to 730 days); `helper_codes.py`; `requirements.txt`; figures saved per horizon (`buy_ret_h30.png` ... `h365`).
- Q8: the README opens with "This is an exploratory study with no profitable strategy in sight." — a null result published with its code.
- Q3: replication needs paid WRDS access to OptionMetrics, CRSP and CUSIP; only common stocks (share codes 10, 11) on NYSE/NASDAQ.
