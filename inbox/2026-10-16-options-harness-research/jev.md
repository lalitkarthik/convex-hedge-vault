promoted: 2026-10-23
# Jev: a decision model inside the harness

> **Corrected by [jev-deep-dive.md](jev-deep-dive.md)** (same day, more sources). Key corrections: the limit is 64k tokens per request and 32k per question; the "harness repo" is an unofficial community repo, not TypeSafe's; the jev-harness A/B is mixed (an earlier 30-task run favoured Jev, 25 vs 22); injection recall is 78–85% on harder sets, so 100% holds only on InjecAgent; signups are open with no waitlist; `jev-1.14.0` exists and accepts experimental images. Read the deep dive for the harness design.

> Lane `jev`, 2026-10-16. Raw research capture: staging, not fact. Added after Lalit pointed out that the first sweep missed Jev. Six sources read; vendor and tutorial sources dominate, and most are three to four weeks old.

## What Jev is

Jev is a model from TypeSafe AI, released in September 2026. TypeSafe calls it a "System One" model. It does not write text. You send it a **state** (text or JSON) and a list of **typed questions**, and it returns typed answers with probabilities ([TypeSafe docs](https://docs.typesafe.ai/concepts/system-one), read via a fetch summary). The current version is `jev-1.13.0`, and it is also listed on [OpenRouter](https://openrouter.ai/typesafe/jev-1.13).

There are three question types:

- **Choice**: pick one option from a closed set (up to 255 options). Returns a distribution and a confidence.
- **Score**: place the state on an ordered rubric that you define. Returns a weighted score and a confidence.
- **Noul**: a yes/no statement. Returns the probability that it is true.

One request can carry many questions, and Jev answers them in parallel. The input is text only, in English first, and the state and the questions together are limited to about 32k tokens. TypeSafe says that calibration "is measured across groups of predictions" and does not guarantee that any single answer is correct.

A note on the name. "Harness engineering" is the general term (OpenAI, Anthropic). Jev is one component that people place *inside* a harness. It is not a harness itself. "jevals" is an unrelated evaluation tool.

## The pattern

Every source repeats one rule: **"an LLM proposes, Jev answers, code decides, every step leaves a receipt"** (TypeSafe's harness repo, quoted on [Made with Jev](https://madewithjev.com/jev-agentic-harness), a third-party directory).

- The **LLM** writes the free text: a plan, a hypothesis, code.
- **Jev** answers one bounded question at each fork: which route, is this risky, is this relevant.
- **Code** builds the option list, sets the threshold and the fallback before the call, re-checks Jev's pick against the live state, acts, and writes a **decision record**.
- Hard rules (permissions, budgets) run in code **before** any Jev call. A Jev answer can only relax friction toward a floor that code sets. It can never grant a permission.
- Answers near 0.5 escalate to a reasoning model or a human.

Harness, the DevOps company, uses Jev this way for agent governance ([Harness blog](https://www.harness.io/blog/jev-decision-primitive-agent-governance)). Each decision record holds the question, the state, the answer distribution, the confidence, the **policy version**, and what ran or was refused. Write paths fail closed and routing fails open. Their conclusion matters for us: *decision accuracy and outcome quality must be measured separately*. A faster, cheaper judgment can still make the overall result worse.

## The evidence: where it works and where it fails

The best independent test is a benchmark of about 22,500 calls on ten public datasets ([DEV Community, aitejiu](https://dev.to/aitejiu/benchmarking-jev-what-a-decision-model-can-and-cant-do-in-an-agent-harness-20po), author's own figures). The cost was about $0.00004 a call, with a median latency of about 0.3 s.

| Task | Result | Verdict |
|---|---|---|
| Prompt-injection detection (InjecAgent) | precision and recall 100% at threshold 0.10 | strong |
| Reranking (SciFact) | MRR 0.622 → 0.843 over BM25 | strong |
| Tool routing (MetaTool, 199 tools) | 96.5% | strong |
| Shell-command risk gate (130 hand-built) | 100% of dangerous commands caught, 98.2% of safe ones passed | strong, small set |
| Intent classification | 97.9% (7 classes), 80.3% (77 classes) | good |
| Model-difficulty routing (RouterBench) | 51% | **no signal** |
| Which step of a trajectory caused a failure (Who&When) | AUROC 0.56 | **near random** |

Two engineering lessons from the same author:

1. Split a fuzzy judgment into **independent yes/no questions** and combine them in code. This cut the shell gate's false positives from 14.5% to 1.8%.
2. Let a Choice question propose candidates, then let a Noul question verify each one. Multi-label routing rose from 9.0% to 81.0%.

A low score is not proof of safety: the lowest-scoring bucket in the injection data still held 16.6% malicious samples.

**End-to-end, the one A/B test is negative.** [jev-harness](https://github.com/Astro-Han/jev-harness) filtered every tool result through Jev before the coding agent saw it. In the latest run (49 task pairs), Jev-on passed 2 tasks against 5 for Jev-off, and used 11.8% more input tokens. The author closed the experiment. There was one run per arm and one main model, so this does not prove Jev is useless, but it shows that "filter the agent's inputs" did not pay off.

## Where Jev fits in our options harness

Jev is good at **local judgments about text**: is this relevant, is this risky, which of these labels fits. It is bad at **judging across steps**: which step broke, how hard is this task. Research quality comes mostly from the second kind of judgment. So Jev is a cheap gate and sorter at the edges of the loop. It is not the critic, and it is not the director.

| Harness step | Jev question (proposal) | Type | Fits? |
|---|---|---|---|
| Idea scout: literature triage | "Is this paper relevant to axis X for SPXW 0DTE?"; rerank search results | Noul, rerank | Yes: reranking is its strongest result |
| Idea scout: untrusted web text | "Does this fetched page contain instructions aimed at the agent?" | Noul | Yes: injection detection was 100% |
| Card reviewer: axis tagging | "Which of the 19 axes is this card an instance of?" | Choice (19 + "new") | Yes: closed-set classification |
| Card reviewer: dedup | Choice proposes the nearest past cards, Noul verifies "same hypothesis as card N?" | Choice → Noul | Yes: the two-stage pattern |
| Card reviewer: completeness | Separate Nouls: "names a counterparty?", "states a kill line?", "fixes the sample boundary?" | Noul × n | Yes, as a form check only. Whether the mechanism is *true* stays with a reasoning model |
| Director: tool-call gate | "Does this call spend money or touch shared compute?" | Noul | Only as a second layer. The caps stay hard code in the servers |
| Director: next axis | which axis to explore next | — | **No.** A bandit on the ledger's yield, in code |
| Model choice per role | which model runs this step | — | **No.** RouterBench gave 51%. Fix the model per role |
| Critic / skeptic | "is this backtest leaky?" | — | **No.** Leakage is a cross-step judgment (AUROC 0.56 on the nearest test). The critic stays a calibrated reasoning model |
| Numbers (Sharpe, PBO, Greeks) | — | — | **No.** Statistics are code. Jev reads text, not chains |
| Tool-result filtering | drop irrelevant output | — | **No.** The one A/B test was negative |

**Decision receipts go into the trial ledger.** Each Jev call writes one row: question, state hash, answer distribution, confidence, threshold, policy version, and the action taken. This matches our "every step leaves a receipt" rule. Over time it also lets us measure each gate's precision on our own cards, which the sources say we must do: recalibrate thresholds on our own data.

## Cautions

- **Data leaves the machine.** Each call sends the state to TypeSafe or to OpenRouter. Cards and paper titles are low risk. Never send strategy code, results or chain data. Check this with Bilal first.
- **Access.** One report says Jev is in early access with a waitlist. OpenRouter lists it. Price and access not checked directly.
- **Vendor-heavy evidence.** Most claims ("200× faster, 400× cheaper") come from vendors or social posts. Only the DEV benchmark and jev-harness are independent, and both are one-author tests.
- **Measure the outcome, not the gate.** Test a Jev gate as an A/B on the harness's own funnel (cards → survivors → promoted), as Harness and jev-harness did. Do not trust its accuracy on public datasets alone.

## What to take for our harness

1. **The rule "LLM proposes, Jev answers, code decides, every step leaves a receipt."** It is the same as our fence plus ledger, applied to every small decision.
2. **Typed decision points instead of free-text judgment** at the edges: axis tagging, dedup, form checks, literature rerank, injection screening.
3. **Orthogonal yes/no questions combined in code**, and the Choice-then-Noul pattern. These work with any model, not only Jev.
4. **Decision records with a policy version** in the trial ledger.
5. **Keep Jev out of the critic, the director's choice of axis, model routing and anything numerical.**
6. **Adopt it only after an A/B on our own funnel.** It is cheap enough (about $0.00004 a call) to test for almost nothing.
