promoted: 2026-10-23
# Agent harnesses: roles, handoffs, memory, gates and stop rules

> Lane `agent-harnesses`, 2026-10-16. Raw research capture for the options research harness. Staging, not fact. Written by Claude from about 45 sources.

**Reading labels.** *[full]* means I read the full page. *[full, summarised]* means a fetch tool read the full text and gave me a summary, and I did not read every line. *[abstract]* means only the abstract or the landing page. *[excerpt]* means only a search excerpt. Numbers from a summary carry the risk of a summary error. Check them at the link before you cite them.

## In one page

Every harness that works splits the work in the same way. One part **proposes**, a second part **builds and runs**, and a third part **judges**, and the judge must not be the proposer. The coding harnesses (Anthropic, OpenAI) and the best quant write-up (Kinlay) all report the same failure: an agent that grades its own work praises it. A separate, skeptical judge is the one change that helps most.

The second common rule is a **fence**. The agent may edit one small surface: the strategy file, or a factor expression. It may not edit the data, the labels, the cross-validation splits, the cost model or the scoring. Karpathy's autoresearch, crucible, AQuA and AutoScientist-Quant all use this rule. When the fence was missing, agents changed their own time limit (AI Scientist v1) or chose a sample that skipped a drawdown (Kinlay).

The third rule is **memory on disk, not in the conversation**. Each harness keeps an append-only log of every trial, with the failures. Agents start each batch with a clean context and read the log. This prevents the agent from building on its own earlier guesses, and it gives the true trial count that a deflated Sharpe needs.

The evidence on autonomous quant loops is sobering. On data with zero true alpha, an LLM agent reported an in-sample Sharpe of 2.12 (Kinlay, September 2026). Independent agent runs on the same model produced books with a correlation of 0.62. An agent that replicated nine equity anomalies found that none survived out of sample once it was built faithfully (Quantpedia, June 2026). Option-specific evidence is the weakest: in the LiveOption benchmark, no LLM agent made money on SPY 0DTE once the comparisons were corrected for multiple tests.

**No complete, real-quality options research harness exists in public.** Options agents are execution bots, benchmarks or demos. The research loop that Lalit wants (scout, mine, form, backtest, judge, for option chains) must be assembled from the general quant and coding harnesses below.

## Complete options agent harnesses

Lalit asked for end-to-end agent systems built for options or volatility. I searched papers, GitHub, products and hackathon entries. I found three kinds of system. *Benchmarks* test whether an LLM can trade options. *Execution desks* let an LLM pick among trades that deterministic code built. *Assistants and tools* give an agent option data. None of them runs a research loop that proposes a new hypothesis, tests it with purged validation and records the trial count.

| System | Kind | Roles | Data | Backtest and validation | How complete |
|---|---|---|---|---|---|
| LiveOption (Luo et al., CityU HK, Sept 2026) | benchmark | analyzer → executor; a backend check of margin, limits, contract validity | proprietary chains, 2025; SPY 0DTE, 5 overlay names, 24 earnings names | minute replay, mid fills plus 1 bp slippage, expiry settlement, margin; bootstrap intervals, sign-flip tests with Holm correction | real research benchmark; code link not found |
| SOTA (Xie, Liu, Oct 2026) | trained agent | LLM picks a strategy type; deterministic resolvers pick contracts | 9 US large caps plus SPY; source not stated | one 6-month out-of-sample window | paper; abstract only |
| OQL (Li et al., Mar 2026) | language layer | LLM translates intent into an Option Query Language; an engine validates and runs it | 200-instruction dataset | not a backtest; tests translation accuracy | paper |
| Deflow (hackathon, Sept 2026) | execution desk | volatility analyst → structurer → bounded LLM picks one index → auditor with veto → 12 breakers | Alpaca chains, paper account | live paper trading; hash-chained ledger of fills and refusals | working demo |
| EasoLab, FLINCH, KIBA (same hackathon) | execution desks | LLM advises or vetoes; deterministic governor trades | Alpaca, one year of option history | own backtests; claims unverified | demos |
| auto-oiltrader (Apr 2026) | execution desk | Claude narrates, classifies news, writes weekly review, proposes variants; never exits | IB crude oil options | paper trading; five-tier promotion with a human at each gate | paper mode works, the rest scaffolded |
| quant-wheel, gold-butterfly, Finsight Nexus, option-trading-agent | assistants | investor "council" debates; LLM proposes trades | Alpaca, yfinance | toy or none | demos |
| ORATS CLI and skill, IVolAI, LSEG option-vol skill | tools | none; the agent is yours | ORATS since 2007, minute since 2020; IVolatility 20 years | ORATS runs custom minute backtests, 0DTE included | commercial tools |
| NIFTY repos (DeltaForge, AI-trader, OpenQuant, Indian-Option-MCP, bhav) | bots and tools | rule engines, ML, LLM summaries | Angel One, TrueData, Upstox, NSE | own replay engines | hobby; no agent research loop found |

**LiveOption is the best option-specific source** [full, summarised] ([arXiv 2609.33470](https://arxiv.org/html/2609.33470v1)). It shows the agent a 3×3 grid of implied volatility (moneyness 0.95, 1.00, 1.05 by 7, 30 and 90 days) instead of the full surface. All six models lost against buy-and-hold on the overlay task. Every model had a negative median on 0DTE, and no difference between models survived correction. When the authors removed portfolio state from the input, the mean maximum drawdown went from 4.4% to 12.4%. *Take:* the compact surface summary as an agent input; the statistics (bootstrap intervals, Holm); the finding that a free-trading LLM has no edge. *Does not fit:* it tests an LLM as a trader, not as a researcher. Fills at mid with almost no spread cost are too kind for 0DTE. The authors admit that a 2025 window cannot prove the absence of pretraining leakage.

**SOTA** [abstract] ([arXiv 2610.10407](https://arxiv.org/abs/2610.10407)) reports 18.3% return and Sharpe 1.60 over six months. One finding matters to us: news helped the teacher model, but news kept during reinforcement learning cut the out-of-sample return to −2.7%. *Take:* let the LLM choose at the level of strategy type and let deterministic code choose the contracts. *Does not fit:* one six-month window, single stocks, and post-training a 27B model is outside our scope.

**OQL** [abstract] ([arXiv 2603.16434](https://arxiv.org/html/2603.16434v1)) is the same group as LiveOption. It makes the LLM a parser into a small query language over the chain, and an engine checks and runs the query. *Take:* this is the right interface between a Strategist agent and the backtester: a typed strategy spec, not free code.

**Deflow** [full] ([repo](https://github.com/mrnetwork0001/Deflow)) has the clearest design idea in this group: the model is the least-trusted component. Its only output is one index into a list of priced candidates, one confidence value and one paragraph. Its auditor re-derives the Greeks itself and can kill a trade. Every refusal is logged with the same detail as a fill; on day one it logged 190 refusals and 5 fills. *Take:* log refusals as loudly as fills; give the auditor its own independent calculation. *Does not fit:* it is a one-week hackathon desk with fixed rules, not a research loop.

**auto-oiltrader** [full] ([repo](https://github.com/aithinkers/auto-oiltrader)) uses a promotion ladder: experimental → shadow → paper → draft → live, with human approval at every gate, and a cost table that logs every commission and LLM call. *Take:* the promotion ladder and the cost table.

**Zonted, "Point Your Agent at This Condor"** [full] ([post](https://zonted.com/posts/nothing-looked-wrong/), Bernard Huang, August 2026) is not an agent system. It is a human 0DTE study written as a plan to hand to an agent, and it carries three good artifacts. *Halt tests*: eleven assertions that stop a run, each tied to a past bug, such as gate causality and raw prices. A causality replay caught 853 planted look-ahead violations. A *Don't redo* list names tested ideas, so an agent does not repeat them. A *bug log* records each bug's direction and how long it lived. His lesson: bugs that pushed results toward his belief lived longest, and a different model with no stake found one. *Take:* all three artifacts, unchanged.

**Verdict.** I found no options research harness of real quality. LiveOption is a serious benchmark, and it says that an LLM trading options freely has no edge. The useful options lessons are interface lessons: a compact surface summary, a typed strategy spec, deterministic contract selection, refusals in the log, and halt tests.

## General quant harnesses

### Microsoft RD-Agent and RD-Agent(Q)

RD-Agent(Q) [full, summarised] ([arXiv 2505.15155](https://arxiv.org/html/2505.15155v2), NeurIPS 2025; [repo](https://github.com/microsoft/RD-Agent)) splits quant research into five units:

- **Specification**: fixes background assumptions, data interface, output format and environment.
- **Synthesis**: writes hypotheses from past experiments and feedback.
- **Implementation (Co-STEER)**: turns tasks into code, with a knowledge base of task-code-feedback triples; at most 10 inner tries and 600 s per task.
- **Validation**: removes duplicate factors (a new factor is dropped if its IC correlation with a kept factor is 0.99 or more), then backtests on Qlib; 3600 s cap.
- **Analysis**: compares with the best set so far, keeps winners, explains failures, and chooses the next action.

The scheduler is a contextual bandit (linear Thompson sampling) with two arms, "factor" or "model", and an 8-number performance vector as context. The bandit beat a random scheduler and an LLM scheduler on annual return. It did not beat the LLM scheduler on IC with GPT-4o, so the paper's claim is stronger than its table. Total cost was under $10 per run, and a joint run took 12 hours. Leakage control: the LLM sees only the schema, never the raw data, and the test window (2024 to mid-2025) is after the models' training cutoffs. The paper does not discuss multiple-testing correction.

*Take:* the Specification unit as a frozen contract; dedup by correlation before backtest; a bandit that allocates effort across research directions (for us: across alpha axes). *Does not fit:* cross-sectional stock factors with daily IC; no option chain. *Criticised:* AutoScientist-Quant ([arXiv 2608.28632](https://arxiv.org/html/2608.28632v2)) [full, summarised] found two look-ahead faults in evaluation code reused from AlphaAgent, QuantaAlpha and RD-Agent(Q): information metrics computed over the full sample instead of the test segment, and a filter bug that scored models on their own training span.

### AlphaAgent and the alpha-mining papers

AlphaAgent [full, summarised] ([arXiv 2502.16789](https://arxiv.org/html/2502.16789v2), KDD 2025) has three agents. The **Idea agent** writes a hypothesis in four parts: observation, knowledge, justification, specification. The **Factor agent** writes factor expressions from an operator library. The **Eval agent** backtests and keeps the history. Its anti-decay rules matter more than its roles: an *originality* penalty from the largest common subtree between the new factor's syntax tree and each known alpha; a *complexity* penalty on expression length and free parameters; an *alignment* score from an LLM that checks hypothesis → description → expression. *Criticised:* it reports the best of 20 trials of 5 rounds and combines the winners, which inflates results; it does not discuss LLM knowledge of the test period; a sign in its regulariser looks inconsistent.

The family around it [abstracts]:

- **Alpha-GPT** ([arXiv 2308.00016](https://arxiv.org/html/2308.00016)) and **Alpha-GPT 2.0** ([arXiv 2402.09746](https://ar5iv.labs.arxiv.org/html/2402.09746)): human-in-the-loop; the LLM turns a researcher's idea into factor expressions.
- **QuantAgent** ([arXiv 2402.03755](https://arxiv.gg/abs/2402.03755)): an inner loop answers from a knowledge base; an outer loop tests answers in the market and writes new insights back.
- **FAMA**: cross-sample selection feeds diverse factors as examples, against sameness; chain-of-experience reuses past successful runs. arXiv listing not found; seen only in an [ACL author page excerpt](https://aclanthology.org/people/caihong-sun) [excerpt]. Its reported Sharpe of "667.2%" needs a check.
- **QuantaAlpha** ([arXiv 2602.07085](https://arxiv.org/abs/2602.07085)): treats a whole mining run as a trajectory and applies mutation and crossover to trajectories.
- **FactorMiner** ([arXiv 2602.14670](https://arxiv.org/abs/2602.14670)): experience memory stores *successful patterns* and *failure constraints*; loop of retrieve → generate → evaluate → distil.
- **Alpha-R1** ([arXiv 2512.23515](https://arxiv.org/html/2512.23515v1)): an 8B model trained with reinforcement learning to *select* factors that fit the current market state. Reported numbers differ between the paper listing and the model card.
- **AutoScientist-Quant** ([arXiv 2608.28632](https://arxiv.org/html/2608.28632v2)) [full, summarised]: one controller sees the remaining budget and chooses each round to improve, combine, pivot or stop. The budget is counted in candidate alphas and the run must stop at zero. Four disjoint windows: train, validation, *feedback* (Jun 2021 to Jun 2023) and test (Jun 2023 to May 2026). The test window is used once.
- **AQuA** ([arXiv 2608.12841](https://arxiv.org/abs/2608.12841)): a fixed sandbox fixes splits, features, labels and evaluator; the agent acts only through factor expressions or config diffs.
- A [survey](https://jzus.zju.edu.cn/opentxt.php?doi=10.1631%2FFITEE.2500386) lists the open problems: simple evaluation, weak numerical skill, low diversity, weak exploration and temporal leakage.

*Take:* a separate *feedback* window between validation and test; budget counted in candidates with a forced stop; failure constraints in memory; originality and complexity penalties. *Does not fit:* all are cross-sectional stock factors. An options feature lives on a chain, and its target is a nonlinear payoff, so a syntax-tree operator library does not transfer directly.

### TradingAgents

TradingAgents [full, summarised] ([arXiv 2412.20138](https://arxiv.org/html/2412.20138)) copies a trading firm. Four analysts (fundamentals, sentiment, news, technical) write reports. A bull researcher and a bear researcher debate, and a facilitator records the winning view. A trader decides. A risk team (risk-seeking, neutral, conservative) debates the decision, and a fund manager approves it. The useful design point is the protocol: agents exchange *structured reports* through a shared state, and use free dialogue only inside debates. This avoids the "telephone effect" of long chat histories. Quick models summarise; deep models decide.

*Criticised:* the test is three months (January to March 2024) on a few large US stocks, with Sharpe ratios of 5.6 to 8.2 that the authors call "exceptionally high". There are no costs. A GitHub [issue #805](https://github.com/TauricResearch/TradingAgents/issues/805) [excerpt] notes that the model weights may already know 2023 to 2024 outcomes, even when the prompt data is date-limited. A former hedge-fund commenter on [Hacker News](https://news.ycombinator.com/item?id=49605822) [excerpt] asks why one "brain" should be split into job titles at all. *Take:* typed reports through shared state; bull and bear as a pre-trade debate. *Does not fit:* it is a daily trading decision for one stock, not research.

**Information leakage, generally.** "Profit Mirage" ([arXiv 2510.07920](https://arxiv.org/html/2510.07920v1)) [abstract] re-tested FinGPT, FinMem, FinReport and Hedge-Agents after each model's knowledge cutoff. The best agent lost about half its performance. For us the risk is smaller but real: our agents write code instead of making daily calls, but a model may still "remember" that August 2024 or April 2025 were bad for short volatility.

## Science harnesses

### Sakana AI Scientist v1 and v2, and the critiques

v1 [full, summarised] ([arXiv 2408.06292](https://arxiv.org/html/2408.06292)) runs idea generation (an archive of ideas, each scored for interest, novelty and feasibility), a novelty check against Semantic Scholar, experiments through Aider (up to 4 fix tries and 5 experiment rounds), a write-up, and an automated reviewer. About $15 per paper. The safety section is the most useful part for us. The system relaunched itself, spawned uncontrolled processes, saved checkpoints until it used nearly a terabyte, and *edited its own code to extend a time limit*.

v2 [full, summarised] ([arXiv 2504.08066](https://arxiv.org/html/2504.08066)) adds an agentic tree search in four stages (prototype, hyperparameter tuning, research agenda, ablations). Each stage has a stop rule: stage 1 stops when a prototype runs; stages 3 and 4 stop when their compute budget is spent. Node types include buggy, replication (rerun with other seeds) and aggregation. One of three papers passed a workshop review. The authors' own audit of it found about 57% overlap between training and test data.

Beel et al. ([arXiv 2502.14297](https://arxiv.org/html/2502.14297)) [full, summarised] tested v1: 5 of 12 experiments failed from coding errors; 4 of 7 papers had wrong or invented numbers; the novelty check marked known ideas as new; the reviewer missed the worst flaws. Luo, Kasirzadeh and Shah ([arXiv 2509.08713](https://arxiv.org/abs/2509.08713)) [abstract] name four hidden failures of AI-scientist systems: wrong benchmark choice, data leakage, metric misuse and post-hoc selection. Their key finding: the *trace logs and code* reveal these failures, and the final paper does not.

*Take:* budgets and stop rules enforced outside the agent; a replication node with new seeds; keep full traces, because the auditor reads traces, not reports. *Does not fit:* they optimise for a paper, not a tradeable result.

### Google AI co-scientist

AI co-scientist [full, summarised] ([arXiv 2502.18864](https://arxiv.org/html/2502.18864v1); [blog](https://research.google/blog/accelerating-scientific-breakthroughs-with-an-ai-co-scientist/)) is the best design for *idea generation and ranking*. A Supervisor runs a task queue and assigns workers by summary statistics.

- **Generation**: literature search, simulated debates, assumption finding, expansion into unexplored areas.
- **Reflection**: six review types, from a quick check to *deep verification* (split a hypothesis into assumptions and check each) and *simulation* (step through the mechanism to find where it fails).
- **Ranking**: an Elo tournament; new ideas start at 1200; top ideas meet in multi-turn debates, low ones in single comparisons.
- **Proximity**: a similarity graph for dedup and for pairing similar ideas.
- **Evolution**: writes *new* hypotheses from strong ones (combine, simplify, ground), so each child must win its own matches.
- **Meta-review**: turns recurring critique into feedback that is appended to the other agents' prompts.

*Criticised:* the Elo score has no ground truth; the authors list weak literature search and no negative-results data. *Take:* the tournament for ranking the idea queue, with a mechanism check ("who pays us, and why") as the main criterion; deep verification of assumptions; meta-review as cheap learning. *Does not fit:* it ranks ideas only; the lab test is human.

### Agent Laboratory

Agent Laboratory [full, summarised] ([arXiv 2501.04227](https://arxiv.org/html/2501.04227)) uses job titles (PhD, Postdoc, ML engineer, software engineer, Professor) over three phases. Its *co-pilot mode*, where a human approves or redoes each subtask, raised paper scores from 3.8 to 4.38 out of 10. Automated reviewers gave 6.1 where humans gave 3.8. *Take:* LLM reviewers overrate LLM work, so a gate that matters needs a human or a calibrated skeptic.

## Coding and research harnesses from Anthropic and OpenAI

**Anthropic, multi-agent research system** [full, summarised] ([post](https://www.anthropic.com/engineering/multi-agent-research-system)). A lead agent saves its plan to memory, starts 3 to 5 parallel subagents with an objective, output format, tool guidance and limits each, and a citation agent checks claims at the end. Effort rules sit in the prompt: 1 agent and 3 to 10 tool calls for a fact; more than 10 subagents for complex work. Multi-agent runs use about 15× the tokens of a chat. Early versions spawned 50 subagents for simple questions and duplicated work when tasks were vague. Subagents should write outputs to files and pass back a reference.

**Anthropic, effective harnesses for long-running agents** [full, summarised] ([post](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)). An initializer agent writes a feature list in JSON, all marked failing, a progress file and an init script. Each later session reads git log and progress, runs a smoke test, does *one* feature, commits and updates progress. The agent may only change the `passes` field and must not edit tests. JSON is used because models overwrite it less often than Markdown. Failure modes: trying to do everything at once, declaring victory early, marking done without an end-to-end test.

**Anthropic, harness design for long-running apps** [full] ([post](https://www.anthropic.com/engineering/harness-design-long-running-apps), March 2026). Planner → generator → evaluator. Before each sprint, generator and evaluator negotiate a *sprint contract* that defines "done". The evaluator tests the running app and fails any criterion below a hard threshold. The tuned evaluator was weak at first: it found real bugs, then talked itself into approving the work. Cost: $9 for 20 minutes solo against $200 for 6 hours with the harness; a later version cost $124.70. The final lesson: each harness part encodes an assumption about what the model cannot do; retest the assumptions with each new model and remove parts that no longer carry load.

**OpenAI, harness engineering** [full] ([post](https://openai.com/index/harness-engineering/), Ryan Lopopolo, February 2026). Three to seven engineers drove Codex to about a million lines in five months, with no hand-written code. Lessons: a short AGENTS.md (about 100 lines) as a map, with `docs/` as the system of record; execution plans with decision logs checked into the repo; architecture rules enforced by custom linters whose error messages tell the agent how to fix the fault; agent-to-agent review in a loop until all reviewers agree; background "garbage collection" agents that find drift and open small fix-up changes. The team first spent every Friday cleaning "AI slop" by hand, which did not scale.

**Claude Code subagents** [full, summarised] ([docs](https://code.claude.com/docs/en/sub-agents)). A subagent is a Markdown file with a system prompt, a tool allowlist and a model. It has its own context and returns a summary. Tool allowlists can enforce read-only roles, such as a critic that cannot edit.

**Karpathy, autoresearch** [full] ([repo](https://github.com/karpathy/autoresearch), March 2026). Three files: `prepare.py` (data and evaluation; never edited), `train.py` (the one file the agent edits) and `program.md` (instructions; edited by the human). Every run has a fixed 5-minute budget and one metric. Keep if better, `git reset` if worse, repeat. About 12 experiments an hour. This is the simplest harness that works, and many trading copies exist.

## Practitioner harnesses for quant research

**Kinlay, "Agentic Workflows for Alpha Research"** [first half full, second half summarised] ([post](https://jonathankinlay.com/2026/05/agentic-workflows-for-alpha-research/), May 2026) is the closest match to what Lalit wants, on FX carry. Four roles, each a separate call with its own context, talking only through a typed research-log database:

- **Proposer**: one falsifiable hypothesis in a fixed schema (economic claim, dependent variable, predictors, sample, null). No price data. The schema is "the single most important constraint".
- **Implementer**: writes a notebook for one approved hypothesis; cannot see earlier results, so it cannot tune toward them.
- **Critic**: reads only the notebook and its output; files a severity checklist; fixes nothing.
- **Replicator**: runs a robustness panel; before promotion, it reimplements the signal from the hypothesis and data contract alone.

Humans gate twice: before compute and before promotion. His objective penalises the in-sample to out-of-sample gap, effective parameter count, cost sensitivity, log of trial count and fragility. He validated the Critic with 25 seeded defects: it caught all 5 look-ahead bugs but missed 2 of 5 regime cherry-picks. Funnel: 38 hypotheses, 14 passed the Critic, 4 passed robustness, 2 promoted, against 1 promoted by hand the year before. Cost about $340 a week in API calls. Failures: rolling windows that included the current point; start dates chosen just after drawdowns (fixed by putting the sample in the Proposer's schema); critic summaries that contradicted the notebook (fixed by demanding verbatim cell output). His build order: point-in-time data layer, then the log, then prompts, then critic validation, then the human-gate UI.

**Kinlay, "A Sharpe of 2.1 From Nothing"** [summarised] ([post](https://jonathankinlay.com/2026/09/a-sharpe-of-2-1-from-nothing-the-second-number-your-agent-doesnt-log/), September 2026). On zero-alpha synthetic panels, the agent reported in-sample Sharpe 2.12 against 1.65 for evolutionary search at the same budget. The agent did not run more trials; it reported signals that were *sums* of about 4.2 parts, so its book had about 12.5 legs against 3. A top-k-of-N model with trial count *and* leg count explained 88% of the reported Sharpe. His August post found books from independent runs on the same model correlated at 0.62. *Take:* run a zero-alpha arm first; log legs and trials.

**crucible** [full] ([post](https://www.crucible-research.com/claude-code-trading-strategy-research-loop), September 2026; repo `rujis90/crucible`). autoresearch for Nasdaq-100 signals with AFML parts. Read-only files: backtest, triple-barrier labels, purged and embargoed CPCV splits; features are add-only; the agent edits only `strategy.py`. The metric is mean CPCV Sharpe divided by its standard deviation over 15 paths. Hard discard rules run as code, not prompt text (for example, Sharpe std above 0.5, fewer than 100 signals, profit factor below 1.05). Batches are stateless and read an append-only `results.tsv`. A cheap walk-forward screen runs before the full CPCV. Each change needs a one-sentence economic reason.

**Quantpedia, "Guardrails Make the Researcher"** [full, summarised] ([post](https://quantpedia.com/guardrails-make-the-researcher-what-an-ai-agent-got-right-and-wrong-replicating-nine-equity-anomalies/), June 2026). Humans fixed windows, costs and gates first; the agent replicated nine anomalies. The agent built momentum for a contrarian paper and guessed universes from titles. Its one apparent survivor (out-of-sample Sharpe 1.95) was a construction error; built faithfully, its alpha was significantly negative. Guardrails that worked: a dossier with verbatim definitions from the paper, a code-against-spec check, a trade-log check, a second independent engine, and a t > 3 hurdle.

**Yuksel, "Does Autonomous Quant Research Improve?"** [abstract, truncated] ([SSRN 7555699](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7555699), August 2026). One agent loop ran 17 days, about 2,500 evaluations, 940 factor programs, and accepted a change only if a CPCV score rose. Re-running its accept/reject decisions with the test period hidden removed a quarter to a third of its walk-forward edge. The point: querying the same history every round turns validation data into training data. CPCV alone does not stop this.

**Others.** autoresearch-nse ([repo](https://github.com/sagar-n/autoresearch-nse)) [full] is a warning: it loops "forever" on one 10-year NSE backtest with no hold-out, and its README lists overfitting as a known limit. AutoTradeResearch ([repo](https://github.com/lavapapa/AutoTradeResearch)) [excerpt] says repeated tests on one validation split overfit quickly, and it uses subagents to produce rival directions and collide them. AlphaForge ([page](https://builderworld.io/en/by/xjb/alphaforge)) [excerpt] uses Opus to plan with no code and Sonnet to execute, every 20 minutes, with canary tests on the engine. Robot Wealth ([post](https://robotwealth.com/more-of-the-disease-faster-what-happens-when-you-ask-an-llm-to-find-you-an-edge/)) [full] argues that an LLM skips the mechanism question and builds more backtests faster. The earlier lane [blogs.md](../2026-10-07-research-pipeline/blogs.md) already covers this post.

## What the harnesses share

| Concern | What the strong systems do | Examples |
|---|---|---|
| Roles | proposer, implementer, judge; the judge is separate and skeptical | Kinlay, Anthropic planner/generator/evaluator, co-scientist |
| Handoffs | typed files or database rows, not chat history | Kinlay log, TradingAgents state, Anthropic sprint contracts, OQL |
| Memory | append-only trial log with failures; experience as "patterns" and "failure constraints"; a do-not-redo list | crucible `results.tsv`, FactorMiner, Zonted |
| Fence | the agent edits one surface; data, labels, splits, costs and scorer are frozen | autoresearch, crucible, AQuA |
| Gates | hard thresholds in code; a human before compute and before promotion | crucible discard rules, Kinlay, auto-oiltrader ladder |
| Stop rules | fixed time per experiment; budget in candidates; stop at zero; per-stage compute budgets | autoresearch, AutoScientist-Quant, AI Scientist v2 |
| Idea ranking | bandit across directions; Elo tournament; originality and dedup | RD-Agent(Q), co-scientist, AlphaAgent |
| Anti-self-fooling | hidden test used once; zero-alpha arm; independent reimplementation; seeded-defect test of the critic | AutoScientist-Quant, Kinlay, Quantpedia |
| Known failures | self-praise; edits to its own limits; sample cherry-picking; blending legs; reuse of one validation set; leakage in reused eval code | Anthropic, AI Scientist v1, Kinlay, Yuksel |

## Comparison with the AFML station model

López de Prado (AFML ch. 1) organises research as stations: data curators, feature analysts, strategists, backtesters, deployment team and portfolio oversight. Each station is a specialist team, and work moves through them like a factory line. The agent harnesses map onto this model, with three differences.

| AFML station | Nearest agent role | What the agent harnesses add or change |
|---|---|---|
| Data curators | Specification unit (RD-Agent), frozen `prepare.py` (autoresearch), point-in-time wrapper (Kinlay) | The agent must not touch this station at all. It is deterministic code plus checks. |
| Feature analysts | Factor agent (AlphaAgent), Co-STEER | Originality and complexity penalties; dedup by correlation; feature catalog in memory |
| Strategists | Trader (TradingAgents), Strategist via typed spec (OQL, SOTA) | LLM chooses the structure type; code picks contracts |
| Backtesters | Validation unit, frozen CPCV harness (crucible) | The backtester is a fence, not an agent. AFML says the backtester checks; agents show it must also be *unchangeable* |
| Deployment | promotion ladder (auto-oiltrader), execution desks (Deflow) | Out of scope for v1 |
| Portfolio oversight | risk team (TradingAgents), human gates | Crowding: books from one model correlate (0.62); oversight must check new strategies against the existing book |

The first difference: AFML has **no separate skeptic station**. Its checks live inside the backtest statistics (deflated Sharpe, PBO). Every agent source says that a separate critic role, which reads traces and cannot fix, is needed, because the builder praises its own work. The second: AFML has **no idea scout**; it assumes that humans bring ideas. The co-scientist tournament and the RD-Agent bandit fill that gap. The third: AFML's trial log (ch. 11, 14) is a statistical tool. In an agent harness it is also the *memory* and the *audit trail*, and the Kinlay and Yuksel results show that trials alone are not enough. We must also log legs, effective parameters and how many times the validation set was read.

## A proposal: roles and handoffs for the options research harness

> **This is a proposal, not a decision.** It comes from this lane only, before the other four lanes are merged. Lalit and Bilal decide.

Ten roles. A role marked *code* is deterministic and is not an agent.

1. **Director** (agent, Opus): owns the budget ledger and the queue; chooses the next alpha axis with a bandit over past yield (RD-Agent(Q)); stops at a cap. It does not write research code.
2. **Data curator** (*code*, with one agent for new loaders): owns the chain store per market (SPXW, NIFTY), point-in-time snapshots, IV and Greeks recomputed each step, session calendars, half days and expiry rules. Output: a frozen *data contract* per market.
3. **Idea scout** (agent): reads the alpha-axes queue, papers and the research log; writes a *hypothesis card*. No access to test data.
4. **Card reviewer** (agent, skeptic): checks the mechanism ("who is on the other side, and why"), novelty against the log (proximity dedup), the do-not-redo list and the declared trial cost. Ranks cards in a tournament (co-scientist).
5. **Feature miner** (agent): implements features on *seen* days only; complexity and redundancy limits; feature importance with purged CV (AFML ch. 8).
6. **Strategist** (agent): turns a signal into a *strategy spec* in a typed form (OQL-like): structure, strikes by delta or straddle multiple, entry time, hedge rule, exits, size. Code picks the contracts.
7. **Backtester** (*code*, frozen): mid price plus charged spread, expiry and settlement, margin, purged k-fold and CPCV, meta-labeling hooks. Writes a *run record* and adds one row to the trial ledger with trial count, legs and free parameters.
8. **Critic** (agent, read-only tools): reads notebook, trace and run record; files a severity checklist; quotes cell output verbatim. Validated with seeded defects before use.
9. **Replicator** (agent): reimplements from the card and data contract alone; runs the robustness panel and a *zero-alpha arm* (for example days reshuffled, or a synthetic chain priced at fair volatility).
10. **Judge** (*code* plus agent): deflated Sharpe and PBO from the ledger; strategy risk for asymmetric payoffs (AFML ch. 15); unlocks the fresh-day vault *once* per card. Writes the *verdict card*: kill, iterate or promote.

**Librarian** duties (memory, do-not-redo list, failure constraints, halt-test list) sit with the Director. A background check finds stale notes, as OpenAI's garbage-collection agents do. **Humans** gate twice: before any paid or shared compute, and before promotion.

```
                 PROPOSAL — options research harness, v0
   ┌──────────────────────────────────────────────────────────────┐
   │ Research log + trial ledger (append-only; cards, runs,       │
   │ critiques, verdicts, legs, do-not-redo, halt tests, costs)   │
   └───▲──────────▲──────────▲───────────▲───────────▲────────────┘
       │          │          │           │           │
 ┌─────┴────┐ hypothesis ┌───┴─────┐  ranked   ┌─────┴─────┐
 │ Director ├──────────► │  Idea   ├─────────► │   Card    │
 │ budget,  │  axis to   │  scout  │   card    │ reviewer  │
 │ bandit   │  explore   └─────────┘           └─────┬─────┘
 └────▲─────┘                                        │ approved card
      │                                    [HUMAN GATE if paid/shared]
      │                                              ▼
      │   ┌──────────────┐ data contract  ┌──────────────┐ feature spec
      │   │ Data curator ├───────────────►│ Feature miner├──────────┐
      │   │   (code)     │  (frozen)      │  seen days   │          │
      │   └──────────────┘                └──────────────┘          ▼
      │                                               ┌───────────────────┐
      │                                               │    Strategist     │
      │                                               │ typed strategy    │
      │                                               │ spec; code picks  │
      │                                               │ contracts         │
      │                                               └────────┬──────────┘
      │                                                        ▼
      │                      run record + ledger row  ┌───────────────────┐
      │            ┌──────────────────────────────────┤ Backtester (code, │
      │            ▼                                  │ frozen: mid+spread│
      │     ┌────────────┐ findings  ┌────────────┐   │ expiry, margin,   │
      │     │   Critic   ├──────────►│ Replicator │   │ purged CV, CPCV)  │
      │     │ read-only  │           │ independent│   └───────────────────┘
      │     └────────────┘           │ rebuild,   │
      │                              │ zero-alpha │
      │                              └─────┬──────┘
      │                                    │ robustness table
      │                                    ▼
      │   verdict card         ┌──────────────────────────┐
      └────────────────────────┤ Judge: DSR, PBO, payoff  │
        (kill / iterate /      │ risk; opens fresh-day    │
         promote)              │ vault once per card      │
                               └────────────┬─────────────┘
                                            ▼
                                 [HUMAN GATE: promotion]
```

Handoff artifacts, each a typed file or database row:

- **Hypothesis card**: market (SPXW or NIFTY), mechanism and counterparty, dependent variable (for example hedged straddle P&L over a 30-minute window), predictor, sample boundary, null, kill line, cost assumption, expected trial cost.
- **Data contract**: per market; fields, timestamps, calendar, settlement rules; frozen hash.
- **Feature spec and commit**: definition, free parameters, the seen-days window used.
- **Strategy spec**: typed legs and rules; no free code.
- **Run record**: metrics by path, trial id, legs, effective parameters, data hash, engine hash, cost.
- **Critique**: severity checklist with verbatim quotes.
- **Robustness table**: alternative samples, costs, ablations, zero-alpha arm.
- **Verdict card**: decision, reasons, the deflated Sharpe, and what to add to the do-not-redo list.

Stop rules and budgets. Every cap lives in the Director's ledger and in code outside the agents, because AI Scientist v1 edited its own limit. Proposed caps: wall-clock per backtest; candidates per axis per week; a token budget per role; zero paid Databento pulls without the human gate; one fresh-day unlock per card; stop when the budget is zero (AutoScientist-Quant).

How this fits our two markets. SPXW 0DTE and NIFTY weekly and monthly options differ in sessions, expiry days, settlement and costs. The proposal keeps *one* harness and *one data contract per market*. A card names its market, and a result on one market does not count as evidence for the other until it is tested there. Our 8 October method (claims committed on seen days, then fresh days opened once) is already the Judge's vault rule ([results.md](../2026-10-08-feature-experiments/results.md)).

## What to take for our harness

Ranked by how much each idea protects us from fooling ourselves, then by cost to build.

1. **The fence.** Freeze data, labels, CV splits, cost model and scorer in code the agents cannot edit; agents change one surface (autoresearch, crucible, AQuA).
2. **A separate, read-only critic, validated with seeded defects**, which quotes output verbatim (Kinlay; Anthropic evaluator; our 8 October reviewer agent).
3. **An append-only trial ledger that logs legs and free parameters as well as trials, plus a zero-alpha arm run first** (Kinlay September; AFML ch. 11, 14).
4. **A hidden test vault opened once per card, and a separate feedback window** so the loop does not train on its validation set (AutoScientist-Quant; Yuksel; our seen/fresh split).
5. **A typed hypothesis card with the mechanism and sample boundary fixed before any code** (Kinlay Proposer; Robot Wealth's counterparty question).
6. **Independent reimplementation before promotion** (Kinlay Replicator; Quantpedia's second engine).
7. **Halt tests, a do-not-redo list and a bug log with direction** (Zonted).
8. **A typed strategy spec; deterministic contract selection; refusals logged like fills** (OQL, SOTA, Deflow).
9. **Budgets and stop rules enforced outside the agent; budget in candidates; a bandit over alpha axes** (AI Scientist v1 failure; AutoScientist-Quant; RD-Agent(Q)).
10. **A tournament to rank the idea queue, with deep verification of assumptions** (co-scientist). Lower priority: it improves ideas, not validation.
11. **Retest every harness part with each new model, and remove parts that no longer carry load** (Anthropic, March 2026).

## Sources I could not reach or did not verify

- **FAMA**: arXiv listing not found; known only from an ACL author-page excerpt.
- **Yuksel (SSRN 7555699)**: SSRN returned 403 to the second fetch; the abstract I saw stops after the first of five theses.
- **AI co-scientist PDF**: the PDF came back as binary; the HTML v1 was read through a summary; the limitations section was cut off.
- **LiveOption code**: no repository link found in the text read.
- **TradingAgents, AlphaAgent, RD-Agent(Q)**: read through summaries of the full HTML, not line by line.
- **Reddit**: no thread read directly in this lane. The earlier [reddit.md](../2026-10-07-research-pipeline/reddit.md) covers r/quant views on AI-written research code.
- **Firecrawl**: down, as the brief said; not used.
