# Brief — options research harness, inspiration sweep (2026-10-16)

Raw research capture. Staging, not fact.

## Goal

Lalit is collecting inspiration to design an **agent harness for options research**: a complete workflow in which AI agents (Claude, driven through MCP servers and tools) find ideas, mine features, form strategies, backtest them and judge whether a result is real. Bilal Razak (Convex Hedge) set the direction on 2026-10-15: read López de Prado, *Advances in Financial Machine Learning* (AFML, 2018), and build a faster research pipeline by connecting MCP servers.

This sweep collects ideas only. Nothing is built yet.

## Settled decisions (grilling, 2026-10-15/16)

1. **Autonomy:** the harness runs the full research loop alone. Full autonomy on free data and local runs; hard budget caps on anything paid or shared (Databento pulls older than 12 months, company lab compute); the agent stops at a cap.
2. **Markets:** SPXW 0DTE (US, European, cash-settled) and longer-dated NIFTY options (India, weekly and monthly). Their dynamics differ; the harness must handle both.
3. **Options, not stocks:** the data unit is the chain (strike × expiry × time); IV and Greeks recomputed each step; price at mid and charge the spread as cost; expiry and settlement; margin; nonlinear payoffs (labels, risk statistics). Early exercise out of scope for v1. Mostly intraday strategies.
4. **Many alpha axes, not only straddles:** IV vs RV, skew, term structure, gamma/dealer positioning, Greek ratios such as Δ²/(2Γθ), event vol, intraday decay, and more.
5. **Harness engineering in the dev sense** (corrected 2026-10-16: Lalit's "jev" meant TypeSafe AI's Jev decision model; see `jev.md`): a complete workflow with named roles (idea scout, feature miner, strategist, backtester, skeptic/auditor…) and fixed handoffs, like a coding harness (Claude Code subagents, a planner/implementer/reviewer/auditor loop), not tools glued together.
6. **AFML ideas to carry:** research as a factory of stations (ch. 1); record every trial, deflated Sharpe, PBO (ch. 11, 14); purged k-fold and embargo (ch. 7); combinatorial purged CV (ch. 12); meta-labeling (ch. 3); feature importance (ch. 8); strategy risk for asymmetric payoffs (ch. 15).

## Lanes (one file each)

| File | Lane |
|---|---|
| `agent-harnesses.md` | How agent research and coding harnesses split work into roles, handoffs, memory, gates, stop rules, budgets |
| `options-backtesters.md` | Open-source options backtest engines: chain model, fills, Greeks/IV, expiry, margin; NIFTY tooling |
| `alpha-axes.md` | Catalog of options alpha axes, each as a testable hypothesis — the harness's seed idea queue |
| `validation.md` | Overfitting and validation for options research and for autonomous agents |
| `mcp-and-tools.md` | Existing finance/data MCP servers and tools; what we must write ourselves |
| `jev.md` | TypeSafe AI's Jev decision model: where typed decisions fit in the loop (added after the sweep) |
| `jev-deep-dive.md` | Jev in full, plus the proposed design of Jev decision points in our harness |

## Rules for every lane file

- Write for Lalit: short concept-first paragraphs, quantitative undergraduate level, Simplified Technical English. Bullets only for lists, formulas, assumptions.
- Every claim carries a source link (paper, repo, doc, post). Mark what you read in full versus what you saw in a summary or abstract. Say "not found" rather than guessing.
- For each source: what it is, what idea we can take, and what does not fit options or our two markets.
- End with **"What to take for our harness"** — a ranked short list.
- Notes and links only. Copy no large code blocks; no Convex Hedge proprietary code.
- Keep the file under about 350 lines.

## Context in this vault (read before searching, so you do not repeat it)

- `inbox/2026-10-07-research-pipeline/pipeline.md` — how practitioners research a strategy; six source lanes already done.
- `inbox/2026-10-08-alpha-search/` — earlier alpha search (read `_brief.md` and `read-first.md`).
- `inbox/2026-10-08-feature-experiments/results.md` — our feature tests on SPXW 0DTE (bucket method).
- `inbox/2026-10-06-iv-vs-rv-research/` — IV vs RV research.
