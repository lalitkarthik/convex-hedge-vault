# Jev deep dive: what it is, and how to use it in the options harness

> Lane `jev-deep-dive`, 2026-10-16. Raw research capture: staging, not fact. Follows [jev.md](jev.md) and does not repeat it. Part A is the evidence. Part B is a **PROPOSAL**, not a decision. Lalit and Bilal decide.

Source marks: **[vendor]**, **[third-party tutorial]**, **[independent test]**, **[discussion]**; then **full** (I read the whole page or file) or **excerpt** (a summary, search highlight or part of the page).

---

# Part A: Jev in full

## A1. What TypeSafe ships

Jev is a closed model behind one endpoint, `POST https://api.typesafe.ai/v1/systemone` ([API reference](https://docs.typesafe.ai/api), [vendor, full]). A request holds a `state`, a `model` and a map of `questions`. The response holds one typed answer per question, the `model` that answered, and token `usage`. I read the whole docs site through its `llms-full.txt` export (128 pages): the concept pages, the four primitives, confidence, models, the jaggedness page, the API reference, both SDK references and changelogs, and the prose of the main cookbooks ([docs index](https://docs.typesafe.ai/llms.txt), [vendor, full]).

There are now **four** question types, not three ([primitives](https://docs.typesafe.ai/primitives), [vendor, full]):

| Type | Answer | Limits | Note |
|---|---|---|---|
| Choice | `choice`, `probabilities` over your options, `confidence` | at most 255 options | leans toward the option listed first ([jaggedness](https://docs.typesafe.ai/model-jaggedness/jev-1.13)) |
| Score | `score` (can fall between levels), `legend`, `probabilities`, `confidence` | 2 to 10 ordered levels | do not interpolate a magnitude from `score` |
| Noul | `noul` = P(yes) | no `confidence` field | optional `criteria` {true, false} |
| Box | a bounding box on an image | `jev-1.14.0` only | experimental, behind a header |

The question ID is never sent to the model, so the full question must be in `instructions`. Questions in one request are evaluated in isolation and in parallel; one answer is never context for another. Extra questions cost only their tokens. The vendor's own test batched 13 questions into one call and found it 12.2× cheaper and 10× faster than 13 calls with no change in answers ([parallel questions](https://docs.typesafe.ai/cookbooks/parallel_questions), [vendor, full]).

**Confidence is a statistic of the distribution, not a separate signal** ([confidence](https://docs.typesafe.ai/confidence), [vendor, full]). For a Choice with n options, confidence = (p_max − 1/n)/(1 − 1/n). For a Score it is one minus the mean distance from the top level, scaled by the spread of a uniform distribution. A Noul has none; the docs suggest |2p − 1| if you need one. Because the formulas are exact and every answer returns the full distribution, our code can compute its own measure. The docs also suggest top-probability and the top-to-second ratio.

**There is no native abstain.** "I don't know" is built from three parts: a `none_of_these` option in a Choice, a low-confidence band, and a middle band on a Noul. The code must define what happens in each band before the call.

## A2. Limits, versions, price, access

| Item | Value | Source |
|---|---|---|
| Models | `jev-1.13.0` (stable) and `jev-1.14.0` (14 Oct 2026). Alias `jev-latest` → 1.13.0, `jev-preview` → 1.14.0; `jev-latest` was to move to 1.14 "in a week" | [models](https://docs.typesafe.ai/models), [1.14 post](https://typesafe.ai/blog/jev-1-14) [vendor, full] |
| Deprecation | 60 days' notice for 1.13, 30 for 1.14 (a formal policy is promised) | [1.14 post](https://typesafe.ai/blog/jev-1-14) |
| Context | **64k tokens per request, 32k per question** (state plus one question). Header `TypeSafe-Danger-Zone-Long-Context: true` raises both to 262k, "slower and less accurate" | [models](https://docs.typesafe.ai/models) |
| Request rules | body ≤ 32 MiB; nesting ≤ 64 levels; finite numbers only (send exact quantities and IDs as strings) | [API](https://docs.typesafe.ai/api) |
| Input | text; images are experimental behind `TypeSafe-Danger-Zone-Images: true` ("dreamer-ready", not production) | [images](https://docs.typesafe.ai/images) |
| Language | English first; other languages "not equally well". DEV test: Korean R@1 48.9% vs English 61.5% | [models](https://docs.typesafe.ai/models), [DEV](https://dev.to/aitejiu/benchmarking-jev-what-a-decision-model-can-and-cant-do-in-an-agent-harness-20po) |
| Price | $0.042 per million **input** tokens; output free; prepaid credits that expire after 12 months | [models](https://docs.typesafe.ai/models), [MCA §8](https://typesafe.ai/legal/mca) [vendor, full] |
| Rate limits | per organisation, in tokens/s and requests/s, shown only in the console; `429` and `529` retried by the SDKs with backoff. Numbers: **not found** | [models](https://docs.typesafe.ai/models) |
| Errors | 400 (rules; `max_tokens_exceeded`), 401, 413, 415, 422, 429, 529; SDK default timeout 10 s; `x-typesafe-request-id` header | [API](https://docs.typesafe.ai/api), [SDK exceptions](https://docs.typesafe.ai/sdk/python/api/exceptions) |
| SDKs | Python `typesafe-sdk` 0.7.5 (pydantic `response_model`), JS 0.7.0 (Node 22+) | [Python changelog](https://docs.typesafe.ai/sdk/python/changelog) |

**Access, as of 16 Oct 2026.** The launch on 15 Sep was early access with a waitlist ([launch post](https://typesafe.ai/blog/introducing-system-one-models-and-jev), [vendor, full]). TypeSafe dropped the waitlist on 20 Sep with $5 of credit, paused new signups on 22 Sep under demand, and reopened on 27 Sep **without free credits** ([Jev News timeline](https://jevainews.com/news/typesafe-signups-paused/), [third-party tutorial, excerpt]; it quotes the vendor's X posts). Gateways are separate doors with their own keys and billing: OpenRouter lists `typesafe/jev-1.13` at $0.042/$0, P50 latency 0.16 s, one provider, 262K context, through a separate "Decisions API" ([OpenRouter](https://openrouter.ai/typesafe/jev-1.13), [third-party tutorial, full]); ZenMux lists 1.13 and 1.14 at the same price, one provider, no redundancy ([ZenMux](https://zenmux.ai/typesafe/jev-1.13), [third-party tutorial, excerpt]). Vercel AI Gateway also serves it, reportedly with a zero-data-retention option ([Firecrawl](https://www.firecrawl.dev/blog/what-is-jev), [third-party tutorial, excerpt]).

## A3. Company, founders, method claims

TypeSafe AI is a San Francisco lab. It left stealth on 15 Sep 2026 with a $40M seed led by DCVC ([Wilson Sonsini](https://www.wsgr.com/en/insights/wilson-sonsini-advises-typesafe-ai-on-dollar40-million-seed-round-as-company-emerges-from-stealth.html), [discussion, excerpt]). **Only the CEO is documented as ex-OpenAI**: Diogo Almeida, about 4.5 years at OpenAI, co-author of InstructGPT, earlier at Google Brain. The co-founders are Erik Gafni (CTO) and Sasha Sheng (COO); I did not check their backgrounds ([CEO Insider interview](https://www.ceoinsider.io/interview/diogo-almeida), [Latent Space](https://www.youtube.com/watch?v=cFx9Z3ZXca0), [discussion, excerpt]). A Sequoia page says it joined a later round behind a16z ([Sequoia](https://sequoiacap.com/article/typesafe-the-jevolution), excerpt).

The training method is "RLCD", reinforcement learning for calibrated decisions; probabilities are "optimized against outcomes" ([AI primer](https://docs.typesafe.ai/introduction/machine-learning-primer), [vendor, full]). **No architecture paper, parameter count, reliability diagram, ECE or training cutoff is published.** The launch FAQ says to "put no weight on public benchmarks" and to run your own evals ([launch post](https://typesafe.ai/blog/introducing-system-one-models-and-jev), full). The vendor's "workflow evals" score agreement with the average of two frontier models (GPT-6 Astra and Fable 5.1), not ground truth; the post says this biases the score ([launch post](https://typesafe.ai/blog/introducing-system-one-models-and-jev); [WorkflowEvals repo](https://github.com/typesafe-ai/WorkflowEvals), [vendor, full]). Third parties quote a dashboard figure of 67.8% agreement for Jev against 74.1% for the best comparator ([FoundeReview](https://foundereview.com/r/typesafe.ai/chokt310055), [discussion, excerpt]). The "193.6× faster, 444.6× cheaper" figures come from these workflows, and the vendor calls them "the higher end".

The vendor's one stability test ran a 14-Noul rubric 15 times. The mean per-question standard deviation was 0.0102, lower than every LLM tested, **but one answer moved from 0.43 to 0.53 across the 0.5 line** ([self-consistency cookbook](https://docs.typesafe.ai/cookbooks/consistency_noul_cookbook), [vendor, full]). So Jev is stable, not deterministic. A receipt must store the answer; replaying a call will not reproduce it exactly.

## A4. The vendor's own list of weak points

The [jev-1.13 jaggedness page](https://docs.typesafe.ai/model-jaggedness/jev-1.13) ([vendor, full], reviewed 2 Oct) is the most useful page for us. Jev reads literally. It does not count. It is weak with numbers, hex values and date comparison. It loses accuracy with indirection ("a property of a property") and with large states full of irrelevant detail. It "does not treat [state] as hostile by default"; injected or self-arguing text "can move the answer". It may be confused when `instructions` and `criteria` disagree. It leans toward the first Choice option. Its advice: keep arithmetic and dates in code, send only the fields a question needs, and reorder options to check that an answer is stable.

## A5. Data retention and privacy

- **Training:** the Privacy Policy says TypeSafe "will not train or fine tune" models on Input; the MCA says it will not put Customer Data into a training set without consent ([privacy](https://typesafe.ai/legal/privacy-policy), [MCA §4.1](https://typesafe.ai/legal/mca), [vendor, full]). Jev 1.14 adds an opt-in that lets TypeSafe inspect queries for debugging ([1.14 post](https://typesafe.ai/blog/jev-1-14)). Leave it off.
- **What they keep anyway:** a perpetual right to use Customer Data to derive "Telemetry" (it lists "hashes, summary statistics and classifications, metrics, and learnings") and to monitor abuse. Telemetry may be processed "without restriction" ([MCA §4.1, §4.3](https://typesafe.ai/legal/mca)).
- **Retention:** "as long as reasonably necessary"; no number of days. Zero data retention is for enterprise customers only ([legal](https://docs.typesafe.ai/legal), [DPA](https://typesafe.ai/legal/data-processing), [vendor, full]).
- **Location:** "The Services are hosted in the United States" ([privacy](https://typesafe.ai/legal/privacy-policy)). The subprocessor list is on [trust.typesafe.ai](https://trust.typesafe.ai/subprocessors); it renders in JavaScript and I could not read it.
- **Gateways** add a second processor with its own terms (OpenRouter, Vercel, ZenMux).
- **Two contract terms that matter to us:** the MCA forbids using Output to "train a model to imitate the output of the Services" (§2.3(b)), so distilling Jev's labels into our own classifier is not allowed without TypeSafe's consent. Total liability is capped at the greater of 12 months' fees or $50 (§12).

## A6. Ecosystem: the wire format is now a standard

The `/v1/systemone` request shape spread fast. This changes our data-policy problem, because a local model can answer the same request.

- **Official Claude Code integration:** a skill and plugin, not an MCP server (`claude plugin install typesafe@typesafe-ai`). It helps an agent *write* code that calls Jev ([agent skill](https://docs.typesafe.ai/agent-skill), [vendor, full]). The vendor's advice: put all questions and thresholds in one file so a person can review them.
- **Official adapter:** [`system-one-adapter-python`](https://github.com/typesafe-ai/system-one-adapter-python) ([vendor, full README]) is a drop-in `TypeSafeClient` that sends the same questions to OpenAI, Anthropic or Gemini. It records every attempt for replay. This is our control arm for an A/B test.
- **Local servers:** Ollama has served `/v1/systemone` since 0.35, with decision models `nimble` (9B, Bespoke Labs) and `tev1` (Together) ([Ollama blog](https://ollama.com/blog/ollama-now-supports-jev-style-decision-models), [third-party tutorial, excerpt]), and `kev` (Qwen3.5-based) ([Ollama kev](https://ollama.com/library/kev), excerpt). `vllm-jev` and OpenJev (DiffusionGemma 26B-A4B) speak the same API; the official SDK works if you change `TYPESAFE_BASE_URL` ([vllm-jev](https://github.com/mode-io/vllm-jev), [OpenJev](https://github.com/razorback16/openjev), [third-party tutorial, excerpt]). Some report consistency problems: `kev-0.8b` can change its label under concurrent batches. OpenJev weights are CC BY-NC (non-commercial).
- **Competitors:** OpenAI announced a Decisions API on its Luna model ([The New Stack](https://thenewstack.io/openai-decision-api-luna/), [discussion, excerpt: headline only]). Sean Goedecke argues that most of the speed comes from "prefill, then sample one token", which any LLM with logits can do ([Goedecke](https://www.seangoedecke.com/jev-means-structured-output-is-interesting-again/), [discussion, excerpt]).
- **MCP servers (all community, none official):** `jev-mcp` by the DEV benchmark author, with tools `scan_injection`, `bash_risk`, `rank_candidates` ([PyPI](https://pypi.org/project/jev-mcp/), excerpt); `typesafe-mcp`, 9 read-only tools ([PyPI](https://pypi.org/project/typesafe-mcp/), excerpt); `jev-decision-mcp` on npm and `jev-mcp` on Glama (search results only).
- **"TypeSafe's harness repo" is not TypeSafe's.** `TypeSafeAI/jev-harness` sits in an organisation that describes itself as "an UNOFFICIAL organization made for community repos"; its README says it is independent of the TypeSafe team ([repo](https://github.com/TypeSafeAI/jev-harness), [third-party tutorial, full README]). The official organisation is `typesafe-ai`. Made with Jev attributes the repo to TypeSafe by mistake ([Made with Jev](https://madewithjev.com/jev-agentic-harness), [third-party tutorial, full]).

## A7. Independent evidence

| Source | Type, read | Task | Result | What it means for us |
|---|---|---|---|---|
| [Red Hat](https://developers.redhat.com/articles/2026/10/02/benchmarking-ai-decision-models-against-traditional-guardrails) | independent test, full | balanced prompt-injection and content-safety sets, 9 guardrails | Injection: Jev 86.4% accuracy, **blocked recall 77.9%**; Qwen3.6-35B 89.3%; a 200M DeBERTa classifier 89.0% at 54 ms. Safety: Jev first at 86.2%. Median latency from the UK 348 ms | Jev misses about 1 injection in 5 on a hard set. Not a lone defence |
| [DEV, aitejiu](https://dev.to/aitejiu/benchmarking-jev-what-a-decision-model-can-and-cant-do-in-an-agent-harness-20po) | independent test, full | 10 datasets, 22,500 calls, $2.19 | InjecAgent 100%/100% at 0.10, but **injections hidden inside tool outputs: P 97.1%, R 85.0%, FPR 4.9% at 0.5**; misses were Cyrillic homoglyphs and code disguises. Rerank MRR 0.62→0.84. RouterBench 51%. Who&When AUROC 0.56 | Our pages are the tool-output case, not InjecAgent |
| [jev-benchmark](https://github.com/themsquared/jev-benchmark) | independent test, full README | 60 hand-labelled tool-call risk cases | Jev and Claude Sonnet 5 both 55/60; ECE 0.07 (Jev) vs 0.06; Jev 3.3× faster and 41× cheaper; every wrong answer had hedged confidence; 50 of 60 answers in the 0.9–1.0 bin | Confidence was worth routing on, at n = 60 |
| [Every](https://every.to/vibe-check/mini-vibe-check-typesafe-s-jev-judged-everything-i-ve-written-in-0-7-seconds) | independent test, excerpt | 12 passages, 7 planted writing defects | Jev 6/7, Fable 5.1 7/7; 25× faster, 580× cheaper. Jev missed the same defect in 3 of 3 runs: one that "needed a beat of reasoning" | A misread mechanism will pass a Jev check |
| [Harness](https://www.harness.io/blog/jev-decision-primitive-agent-governance) | independent test, excerpt plus fetch summary | evals, routing, action risk | Decision primitive 7–9× faster than an LLM judge, accuracy mixed. Auto-routing passed more cases but **cost 81% more than always-Sonnet**. Receipts hold the policy version; write paths fail closed, routing fails open | Confirms jev.md on routing |
| [jev-harness](https://github.com/Astro-Han/jev-harness) | independent test, full README | filter every coding-agent tool result | 30-task prototype: Jev-on **25/30 vs 22/30** off (6–0–3 on DeepSWE). TB4 follow-up: **2 vs 5** of 49 pairs, +11.8% tokens; experiment closed | Mixed, not simply negative. Relevance must include the step's intent |
| [moonthetrain](https://moonthetrain.com/lab/jev-does-not-remember-the-past) | independent test, excerpt | 26,000 Polymarket markets | AUC 0.59–0.68 both before and after release; no memory of 2025 events | Not a knowledge source; little sign of look-ahead through memory |
| [jev-alpha-bench](https://metatext.io/decision-models/use-cases/projects/jev-alpha-bench) | independent test, excerpt | 5,000 Nasdaq-100 headlines | rank IC +0.24 on the publication day, **−0.008 one close later**; long-short −18 bps per trade after costs; "cannot read a chart" | Reads news; no tradeable alpha |
| [python.financial](https://python.financial/reviews/jev-trading/) | discussion, excerpt | review of trading projects | a futures bot lost 3.15% in about a day; one HK test got 45% on three classes | no evidence of trading value |
| [HN launch thread](https://news.ycombinator.com/item?id=49717558) (1,989 points, 520 comments) | discussion, top 22 comment threads | — | main objection: "can't hallucinate" means only "can't leave the schema"; it can still be confidently wrong | — |

**Reddit:** no Reddit thread was found by search. Firecrawl says Reddit discussed routing, but gives no links.

## A8. What the evidence says, in one paragraph

Jev is a fast, cheap, stable zero-shot classifier. Its confidence was useful on one small independent set. On narrow, local, textual questions it ties a frontier LLM. It is weaker where the judgment needs a step of reasoning, numbers, dates, cross-step causes, or resistance to adversarial text. The vendor's calibration claim has no published reliability diagram. Its headline speed multiples shrink to about 3–9× in independent one-shot tests; the cost advantage stays large (about 40× and more). The interface is now open: local models answer the same request. So the lasting value for us is the **pattern**, and Jev is one backend for it.

---

# Part B: how to use Jev in our harness — PROPOSAL

> **PROPOSAL.** Nothing here is decided. Thresholds are starting points to recalibrate on our own labels.

## B1. The contract

Keep the rule from [jev.md](jev.md): **the LLM proposes, Jev answers, code decides, every step leaves a receipt.** Four extra rules come from Part A:

1. **Code runs first.** Schema checks, hard caps, allow-lists and exact comparisons run before any Jev call. If code can decide, do not call Jev. If validation fails, do not call Jev (TypeSafeAI/jev-harness rule).
2. **Each decision point has an egress class** (B5). The class picks the backend: hosted Jev, a local `/v1/systemone` model, or the Claude adapter. Every backend uses the same `decide()` code.
3. **Questions and thresholds live in one versioned file.** A question set is frozen under an ID. Any change to wording, options, thresholds or model makes a new `policy_version`.
4. **Pin `jev-1.13.0`** (or 1.14.0 once we have tested it). Never send `jev-latest`, because thresholds tuned on one version do not carry over ([models](https://docs.typesafe.ai/models)).

Every call has a deadline of 2 s (OpenRouter P99 is 0.41 s) and at most two retries. When a call fails, times out or abstains, the fallback is fixed before the call and recorded as a fallback, never as a Jev decision.

## B2. Decision points: accept or reject

| # | Candidate | Verdict | Reason |
|---|---|---|---|
| D1 | Literature rerank and triage (idea scout) | **Accept** | Reranking is its best independent result (DEV MRR 0.62→0.84; vendor CLERC top-10 38%→62%). The texts are public |
| D2 | Injection screening of fetched pages | **Accept, as layer 2 only** | Red Hat recall 78%, tool-output recall 85%; the vendor says adversarial text moves answers. Structure stays layer 1: the scout has no write or spend tools |
| D3 | Tagging cards with one of the 19 axes | **Accept** | Closed-set Choice; Banking77 80% at 77 classes, 93% at confidence ≥ 0.9 |
| D4 | Dedup of cards against the ledger | **Accept, Choice then Noul** | This exact pattern is in the docs (the `potential_duplicate` example). Retrieval stays in code |
| D5 | Card form check | **Accept, form only** | Nouls on whether a field does its job. Whether the mechanism is *true* stays with the reviewer |
| D6 | Gate on tool calls that spend money | **Reject as the gate; accept as a hint** | Caps live in the server code. Jev only flags free-form commands (shell, SQL) that might reach a paid API, so they go to a human |
| D7 | Routing between Opus and a cheaper model | **Reject** | RouterBench 51%; Harness auto-routing cost 81% more than always-Sonnet. Fix the model per role |
| D8 | "Stop or continue" for the Director | **Reject as a decision; accept a loop detector** | Stopping is budget arithmetic (code). Jev may flag "the same failure reason three times", which goes to the Director |
| D9 | Pre-screen before the critic | **Reject** | Skipping the critic needs cross-step judgment (Who&When AUROC 0.56). The run record is typed, so code checks its fields |
| D10 | Labelling ledger rows for the do-not-redo list | **Accept** | Choice over a fixed failure taxonomy from the verdict card's text. Local backend |
| D11 | Critic quote check | **Accept, small** | Code first checks that each quoted cell output exists verbatim. Then one Noul per finding: does the quote support the claim (vendor [citation-check](https://docs.typesafe.ai/cookbooks/citation_check) pattern) |
| D12 | Jev outputs as research features (for example, FOMC or RBI statement tone for the event-vol axis) | **Not a harness use** | Treat it as a feature candidate that goes through the full validation gate. Alpha-bench: the same-day signal is gone by the next close. The training cutoff is unpublished |

**Where Jev must not be used, with evidence:**

- **The critic's verdict and the skeptic audit.** Leakage, wrong embargo and a misread payoff are cross-step judgments. Who&When AUROC was 0.56 (random). Every's missed defect was the one that needed reasoning. The vendor lists indirection as a weak point.
- **Numerical work.** Sharpe, deflated Sharpe, PBO, Greeks, IV, costs, dates, expiry arithmetic. The vendor says "Jev is not a calculator"; it does not count and cannot compare dates. Alpha-bench: it "cannot read a chart".
- **The choice of the next axis.** This is a bandit over the ledger's yield, a quantity across episodes. Difficulty routing gave no signal (51%).
- **Clustering trials for the deflated Sharpe.** The clustered N must come from return correlation in code (AFML ch. 8, 11), not from text similarity. D4 runs only before a card is tested.
- **Any source of market knowledge.** Polymarket AUC was about 0.6 even on famous events.

## B3. Decision-point designs

Notation: `ok` means the code proceeds automatically. The band edges are starting values. "Reviewer" means the card-reviewer agent (Opus).

### D1 — Literature rerank and triage (idea scout)

- **Fork:** after a search returns candidates and before the scout reads full texts. The code builds the shortlist (BM25 or embeddings, top 30). Jev reorders it and tags it.
- **State:** `{"query": <axis text from alpha-axes.md, ≤ 300 tokens>, "paper": {"title", "abstract", "venue", "year"}}`. One request per (query, paper) pair, about 600–900 tokens. No full texts; that keeps every request far below the 32k per-question limit.
- **Questions (one request):**
  - `relevance`, Score: "How directly does `paper.abstract` study the effect described in `query`?" with levels ["unrelated", "same asset class only", "related effect, different market or horizon", "same effect, tested empirically"].
  - `is_options`, Noul: "Does `paper.abstract` study option prices, implied volatility or option returns?"
  - `has_empirical_test`, Noul: "Does `paper.abstract` report a test on historical market data?"
  - `market`, Choice: "Which market does `paper.abstract` study?" with options {us_index_options, india_index_options, other_options, not_options, not_stated}.
- **Policy:** sort by `relevance.score`. Read in full if score ≥ 2 and `is_options` > 0.5. **Fails open:** if Jev fails, keep the BM25 order. No escalation; a wrong order costs reading time only.
- **Code before:** dedup by DOI; drop items already in the research log. **After:** nothing; this step grants nothing.

### D2 — Injection screening of fetched pages (layer 2)

- **Fork:** inside our literature server's `fetch` tool, before the text reaches any agent. Deny Claude Code's own WebFetch to the scout role, so every fetch passes the screen.
- **Code before:** strip scripts, styles and hidden elements; apply Unicode NFKC and a homoglyph map (the DEV misses were Cyrillic homoglyphs); detect the language. Non-English text is quarantined, because Jev is weaker on it. Split the text into chunks of about 2,000 characters.
- **State:** `{"chunk": <text>, "source_url": <domain only>}`.
- **Questions (four orthogonal Nouls per chunk, one request):**
  - `addresses_agent`: "Does `chunk` contain text addressed to an AI system, assistant or agent rather than to a human reader?"
  - `override`: "Does `chunk` ask the reader to ignore, replace or reveal earlier instructions?"
  - `action_request`: "Does `chunk` ask the reader to run a command, call a tool, open a link, or send data somewhere?"
  - `concealed`: "Does `chunk` contain encoded, obfuscated or deliberately hidden text?"
- **Policy:** if any Noul ≥ 0.10 (DEV's operating point), quarantine the page. The scout then receives only the title, the URL and the reason. A human can release the page. **Fails closed:** if Jev fails, quarantine the page. The cost is lost reading, not a breach.
- **What stays true whatever Jev says:** fetched text is data; the scout has no spend, write or shell tools; and the low-score bucket still held 16.6% malicious samples in DEV's test. Jev lowers risk; it does not remove it.

### D3 — Axis tagging (card reviewer)

- **Fork:** a new card enters review. Choice then Noul.
- **State:** `{"card": {"market", "mechanism", "counterparty", "predictor", "dependent_variable"}, "axes": {<id>: <one-line definition from alpha-axes.md>}}`. 19 definitions × about 40 tokens, plus the card, is about 1.5k tokens.
- **Request 1:** `axis`, Choice: "Which axis in `axes` describes the economic mechanism in `card.mechanism`?" with 19 options plus `none_of_these` ("the mechanism fits no listed axis"). Each option's description is an object {covers, not_for}, which follows the vendor's advice for easily confused options (for example, VRP vs jump risk premium, GEX vs vanna and charm).
- **Order check:** the code builds the options in an order seeded by the card ID, and records it. When the top two options are within 0.15, it asks again with the order reversed. If the answer changes, the card escalates.
- **Request 2 (multi-label):** for each axis with probability ≥ 0.15, one Noul: "Is `card.mechanism` an instance of `axis_definition`?" (definition passed in structured `instructions`).
- **Bands:** confidence ≥ 0.6, the order is stable and the top-1 Noul is ≥ 0.8 → tag `ok`. Confidence 0.3–0.6, or an unstable order → the reviewer picks. Top option `none_of_these`, or confidence < 0.3 → mark "possible new axis" and send to the Director, then to a human, since a new axis changes the queue. **Fails open:** the card stays untagged and goes to the reviewer.

### D4 — Dedup against the ledger

- **Code before:** an exact match on structured fields (market, dependent variable, predictor) is a duplicate, decided in code. Otherwise retrieve the 10 nearest past cards with the same market (embeddings over mechanism plus predictor) and **include the cards on the do-not-redo list**.
- **Request 1:** `nearest`, Choice: "Which card in `candidates` tests the same hypothesis as `card`, with the same predictor, the same dependent variable and the same market?" with the 10 card IDs plus `none`. The ranking comes from competition, because isolated Nouls cluster near 0.5 (DEV, v2 skill routing).
- **Request 2:** for the top 3 IDs, four orthogonal Nouls each, with the old card in structured `instructions` as `potential_duplicate`: `same_predictor`, `same_dependent_variable`, `same_horizon`, `same_mechanism`. Each question has the form "Does `card` use the same predictor as `potential_duplicate`?".
- **Combine in code:** a duplicate needs all four ≥ 0.8. A duplicate of a do-not-redo card → reject and give the scout the reason. Any two ≥ 0.8 → "near duplicate", and the reviewer decides between "new trial" and "variant of card N" (the variant link matters later for the trial family). **Fails open:** the card counts as novel and the reviewer still checks it.

### D5 — Card form check

- **Code before:** the JSON schema and non-empty fields; a numeric kill line parses; the sample boundary dates are valid and lie inside the seen-days window. All of this is exact work, so code does it.
- **Questions (one request, Nouls on the card text):**
  - `names_counterparty`: "Does `card.counterparty` name a specific group of market participants and say why they accept the other side?"
  - `kill_line_testable`: "Does `card.kill_line` state a result that a backtest could show to be false?"
  - `null_stated`: "Does `card.null` state what the result would look like if the effect did not exist?"
  - `cost_named`: "Does `card.cost_assumption` say how the bid-ask spread is charged?"
  - `direction_stated`: "Does `card.prediction` say which direction the dependent variable should move?"
- **Policy:** each Noul ≥ 0.8 passes; < 0.2 fails; in between goes to the reviewer. A failure returns the card to the scout with the failing item. **Fails closed:** without a pass, the card does not reach testing, but the reviewer can override, with the override in the receipt.

### D6 — Spend hint (layer 2 behind hard caps)

- **Layer 1 (code, decides):** each server tool declares its cost class in a registry. Paid Databento pulls older than 12 months and company compute are refused unless a human gate token is present.
- **Layer 2 (Jev, hints):** a Claude Code `PreToolUse` hook on `Bash`. Before a shell command runs, two Nouls: `reaches_paid_api` ("Does `command` call a paid data API or download market data from a vendor?") and `uses_shared_compute` ("Does `command` submit work to a shared or remote compute cluster?"). Either ≥ 0.10 → ask the human. **Fails closed** (ask the human). The hook can only add friction; it can never allow something that layer 1 refuses.
- **Lesson from the TypeSafeAI harness:** sweeping the threshold from 0.5 to 0.9 caught no extra bad proposals; it only held back good ones. Tune this threshold as a staffing dial, not a safety dial.

### D8 — Loop detector (Director)

- **State:** the last three verdict cards' `reasons` fields. **Noul:** "Do `verdicts[0].reasons`, `verdicts[1].reasons` and `verdicts[2].reasons` report the same cause of failure?" If ≥ 0.8, raise an escalation note to the Director (Opus), which decides. **Fails open.** The stop itself stays budget arithmetic in code.

### D10 — Do-not-redo labelling

- **State:** the verdict card text (internal, local backend). **Choice** `failure_reason`: {no_effect, killed_by_costs, leak_found, regime_only, data_issue, failed_pbo_or_dsr, failed_holdout, other}, each with {covers, not_for}. **Score** `generality`: "How broadly does the failure in `verdict` apply?" with levels ["this parameter set only", "this card's design", "this axis on this market", "this axis on both markets"].
- **Policy:** confidence ≥ 0.6 → write the label; otherwise the reviewer labels it. **Fails open** (the row stays "unlabelled").

## B4. The receipt (one row per call, in the trial ledger)

Write it in the same transaction as the action it caused. Store the full state in a local content-addressed store and only its hash in the row.

| Field | Content |
|---|---|
| `decision_id`, `ts`, `run_id`, `card_id` | identifiers |
| `role`, `decision_point` | for example `card_reviewer`, `D4_dedup` |
| `policy_version` | for example `D4@v3`: hash of the question set, option order rule, thresholds, combine rule and model ID |
| `backend`, `model_requested`, `model_answered` | `typesafe` / `openrouter` / `local:nimble` / `adapter:claude-…`; `model_answered` is taken from the response |
| `egress_class` | `public`, `internal`, `never` (B5) |
| `state_hash`, `state_ref` | SHA-256 of canonical JSON; path in the local store |
| `option_order` | the order sent for each Choice |
| `answers_raw` | every probability returned |
| `derived` | confidence used, band, the combine result |
| `action` | `ok_pass`, `ok_fail`, `escalate_reviewer`, `escalate_director`, `escalate_human`, `fallback` |
| `fallback_reason` | timeout, 429, 529, 4xx, validation-skipped, unstable-order |
| `latency_ms`, `input_tokens`, `cost_usd`, `request_id` | from the response and the `x-typesafe-request-id` header |
| `shadow` | the same questions answered by the control arm (during the A/B) |
| `outcome_label`, `outcome_by`, `outcome_ts` | filled in later by an audit; the label is what calibration uses |

## B5. Data policy

| Class | What | Backend |
|---|---|---|
| **public** | paper titles, abstracts and full texts; public web pages; the text of alpha-axes.md, which comes from public literature | hosted Jev allowed |
| **internal** | hypothesis cards, verdict-card text, ledger rows, critic findings | **local `/v1/systemone` model only**, unless Bilal approves hosted use in writing |
| **never** | strategy code, run records, results and P&L, parameters, chain data and anything derived from Databento, Dhan or NSE feeds, Greeks and IV values, prompts that contain any of these | no model outside the machine; numbers stay in code anyway |

Reasons: TypeSafe keeps a perpetual right to derive Telemetry "without restriction". Retention has no stated limit. Processing is in the US. ZDR is enterprise-only. A gateway adds a second processor. Our data vendors' licences were not checked for redistribution to a model API, so assume they forbid it. The same `decide()` code runs on either backend (Ollama 0.35+ or vllm-jev with `TYPESAFE_BASE_URL`), so the class decides the backend and the code does not change. The local model needs its own calibration; it is not Jev.

## B6. Integration: where `decide()` lives

| Option | Verdict |
|---|---|
| **A. A library inside our own MCP servers** (trial-ledger, card-review, literature) | **Recommended.** The server's code calls `decide()`; the agent never chooses whether a gate runs. The receipt is written in the same transaction as the ledger row. One file holds all question sets and thresholds |
| B. A Claude Code hook | Use only for tools we do not own: the `PreToolUse` Bash hint (D6). Check the exact hook semantics in the Claude Code docs before relying on it |
| C. A separate Jev MCP server (for example `jev-mcp`) | Reject. It exposes the gate as an optional tool the LLM may skip. Receipts would live apart from the ledger. It is also a third-party binary that holds our key |

In the Astro-Han jev-harness runs, agents `cat`-ed a secrets file and used the gateway key ([jev-harness README](https://github.com/Astro-Han/jev-harness)). Keep the TypeSafe key in the server process, outside the agent's reach.

## B7. Evaluation plan

1. **Labels first.** For each accepted gate, label at least **200 items** (about half pass and half fail), split 60/40 into dev and held-out. Freeze the question set and thresholds on dev, then score held-out once. Tuning on dev is "adaptive development tuning, not held-out calibration", as the TypeSafeAI harness says of its own runs. Today we have few real cards, so start with synthetic good and bad pairs and mark them as synthetic.
2. **How many is enough.** To estimate a gate's error rate to ±5 points at 95% you need about 380 items near p = 0.5. For a rare error, use the rule of three: zero false kills in n good items bounds the rate below 3/n, so n = 150 shows "below 2%". For a reliability diagram, aim for at least 30 items per confidence bin. jev-benchmark's 60 items put 50 in one bin, which made its ECE almost meaningless outside that bin.
3. **Labels from people, not from Opus alone.** A label from an Opus ensemble measures agreement with Opus, as the vendor's own workflow evals do. Lalit labels the held-out set; Opus may label dev.
4. **Shadow mode (two weeks).** Jev answers every decision point, but the current Opus reviewer decides. Log both. Measure agreement, per-band accuracy and the reorder flip rate.
5. **A/B on the funnel.** Randomise by a hash of the card ID. Arm A: the Opus reviewer does every check. Arm B: Jev gates, with Opus only on escalations. Control arm for questions: the same question set through `system-one-adapter` on a Claude model. Metrics: cards → admitted → survivors of each validation-gate step → promoted; **false-kill rate**, from a blinded audit of killed cards (audit 20% of kills; at our volume, auditing the silent lane is cheap); escalation rate; reviewer tokens and wall time per admitted card; total cost. Promotions are too rare to power a test, so judge the arms on admission and survival.
6. **Measure decision and outcome separately** (Harness). A gate can be accurate and still make the funnel worse, as the TB4 run showed.

## B8. Cost estimate for one realistic week

Assumptions: 300 cards, 2,000 abstracts triaged, 200 rerank queries × 30 papers, 1,500 pages fetched (4 chunks each), 5,000 Bash commands, 1,000 ledger rows.

| Point | Requests | Tokens per request | Tokens |
|---|---:|---:|---:|
| D1 triage + rerank | 2,000 + 6,000 | 900 | 7.2M |
| D2 injection | 6,000 | 2,000 | 12.0M |
| D3 + D4 + D5 cards | 300 × 4 | 2,500 | 3.0M |
| D6 Bash hint | 5,000 | 600 | 3.0M |
| D8 + D10 + D11 | 1,600 | 1,200 | 1.9M |
| **Total** | | | **≈ 27M** |

At $0.042/M that is **about $1.15 a week** on hosted Jev. The internal-class points (D3–D5, D8, D10) cost $0 on a local model, apart from the GPU or Mac time. The A/B control arm on a Claude model costs roughly 25–50× more (at Sonnet 5's $2/M input as quoted by jev-benchmark: about $55 plus output). The real cost is labelling time (about 200 items × 6 gates) and building the receipts.

## B9. Lessons that do not depend on Jev

The typed-decision pattern works with any model. Even if we never adopt Jev, we gain these:

1. **Every fork is a named, typed question in one file**, with a frozen version and thresholds. A person can review the whole policy on one page.
2. **Receipts per decision**, joined to the trial ledger, with a policy version and a later outcome label. This lets us measure each gate's precision on our own cards.
3. **Orthogonal Nouls combined in code** and **Choice, then Noul**. These worked on LLMs too: DEV's shell-gate false positives fell from 14.5% to 1.8%.
4. **Abstain is a designed path:** a `none_of_these` option, a middle band, and a fallback fixed before the call and never counted as a win.
5. **Shuffle and re-ask** for order bias, and **audit the silent lane**, the auto-passed and auto-killed items no one reads.
6. **One wire format, many backends:** the TypeSafe SDK runs against Jev, against Ollama or vLLM locally, and against Claude through the official adapter. So egress class, not vendor, decides the backend.

---

## What to take for our harness (ranked)

1. **The `decide()` library inside our own MCP servers**, with question sets and thresholds in one versioned file and a receipt per call in the trial ledger (B4, B6).
2. **The data-policy split by egress class**: hosted Jev for public text only; a local `/v1/systemone` model for cards and ledger text; nothing outside the machine for code, results or chain data (B5).
3. **D1 literature rerank and D2 injection screening**, D2 strictly behind structural isolation and Unicode normalisation.
4. **D3 axis tagging and D4 dedup** with Choice then Noul, order-shuffle checks, and the do-not-redo list in the candidate set.
5. **Shadow mode, then an A/B on the funnel** with the false-kill audit and the Claude-adapter control arm, on ≥ 200 human-labelled items per gate (B7).
6. **Keep Jev out of** the critic, all numbers, the next-axis bandit, trial clustering for the deflated Sharpe, and model routing.
7. **Pin `jev-1.13.0`.** Re-tune before any upgrade.

## Corrections to jev.md

- The context limit is **64k per request and 32k per question**, not "about 32k" for state and questions together; a header raises both to 262k.
- "TypeSafe's harness repo" (`TypeSafeAI/jev-harness`) is an **unofficial community repo**. The slogan is not TypeSafe's.
- The jev-harness A/B is **mixed, not simply negative**: an earlier 30-task run favoured Jev-on (25 vs 22). The TB4 run went the other way, and its author closed the experiment.
- "Injection detection was 100%" holds only for InjecAgent at 0.10. For injections hidden inside tool output, recall was 85%; Red Hat measured 78% blocked recall.
- Access is no longer a waitlist: signups have been open since 27 Sep, with no free credits.
- `jev-1.14.0` exists (14 Oct), and images are experimental. "Text only" is out of date.
- More independent tests exist than "DEV and jev-harness": Red Hat, Every, jev-benchmark, Harness, moonthetrain and jev-alpha-bench.
- Only the CEO is documented as ex-OpenAI.

## Sources not reached

- The HN thread beyond its top 22 comment threads; Reddit (none found).
- The CEO Insider, Latent Space and TechCrunch interviews (excerpts only).
- The WSJ copycat story (paywall); The New Stack piece on OpenAI's Decisions API (headline only).
- [evals.typesafe.ai](https://evals.typesafe.ai) (not opened); the [trust.typesafe.ai](https://trust.typesafe.ai/subprocessors) subprocessor list (JavaScript, not readable).
- OpenRouter's and Vercel's data terms for Jev; the ASSAY calibration report (summary only); the jev-alpha-bench repository (summary only).
- Rate-limit numbers and the training cutoff (not published).
- Licence terms of Databento, Dhan and NSE on sending data to model APIs (not checked).
