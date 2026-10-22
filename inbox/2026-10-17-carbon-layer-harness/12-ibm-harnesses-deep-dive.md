# 12 — Harnesses in AI: A Deep Dive (Tejas Kumar, IBM)

- **Title:** Harnesses in AI: A Deep Dive – Tejas Kumar, IBM
- **Channel:** AI Engineer (conference talk; not part of the Carbon Layer series)
- **Id / link:** `C_GG5g38vLU` — https://www.youtube.com/watch?v=C_GG5g38vLU
- **Length:** 20:26
- **Official talk page:** https://ai.engineer/talks/C_GG5g38vLU-ai-agent-harnesses
- **Source of these notes:** English subtitles, read in full.

## Core thesis

We rent black-box models: limited context, no control over what is served. The reason for a harness is **reliability**: the agent does what it should, whatever the model underneath. A harness is "everything around the model that gives it grounding in reality" — it ties a non-deterministic model to a stable, deterministic environment you control. His demo never changes the prompt; only the harness changes, and a 2023-era model (GPT-3.5 Turbo) goes from lying to succeeding.

## Concepts

- **Two meanings of "harness".** In ML: a test suite and runner for model outputs. In AI engineering: the **agent harness**. The talk is about the second.
- **The metaphor.** A climber's harness anchors to the mountain; a dog's harness stops the dog from running off. The harness anchors the agent to something stable.
- **Components of an agent harness:**
  - **Tool registry** (read, write, bash…). Tools follow the OpenAI SDK shape: name, description, parameters, execute.
  - **Model** (some harnesses let you choose).
  - **Context management primitives** (almost every harness compacts its own context).
  - **Guardrails** (for example max steps; exceed it and kill the run).
  - **Agent loop** — but the harness is *not* just the loop; it is the stuff around the loop, possibly "a loop around your agent loop".
  - **Verify step** (lint, tests; check that nothing broke).
- **Do not prompt harder.** When an agent fails, the reflex is to edit the prompt. He fixes everything in code instead.
- **Deterministic verification from the trace.** The verifier reads the tool-call history the loop has been recording, not the model's claim.
- **Harness-side actions with secrets.** The harness, not the model, performs sensitive steps (login) using secrets the model never sees.
- **The rented black box** (added 2026-10-17 from the transcript). A provider could serve a different model under the same name, and you would not know. The model is a variable you do not control; the harness is the part you do. This is why the series fingerprints the model id on every run (videos 08, 10, 11).
- **Composable guardrails.** Each guardrail is a small function; a helper combines them, and the harness pushes guardrail metadata (for example context size) into the trace.
- **Harness messages in the loop.** After a harness-side action, the harness appends its own message to the conversation so the model knows the state changed ("the harness logged you in").
- **Dynamic, on-the-fly harnesses** (his forecast). 2025 was "the year of agents", 2026 "the year of harnesses"; he hopes 2027 brings agents that generate their own harness before a task — "plan mode on steroids".

## The demo, step by step (the architecture he builds)

Task: a browser agent goes to Hacker News and upvotes the first post. Prompt is fixed and never edited.

1. **Bare loop.** `index` creates a Playwright browser session (plain Playwright, not the MCP), tools bound to that session, a context with a minimal system prompt and the task, and `runLoop`: `while (true)` call the model; if it says stop, return; else push events into a **trace** list. **Result:** hits the login page, crashes, and **claims success** — it clicked upvote and never checked.
2. **Guardrails.** `maxIterations` (6 steps) and `maxMessages` (compress when too many). Composable guardrail functions. Naive compressor: keep system prompt + user prompt + last two messages, drop the middle. Context size pushed into the trace.
3. **Refactor into `runHarness`.** Move the logic out of `index` (now about 19 lines). Nothing new; it now has a name.
4. **Verify step + max attempts.** `runHarness` becomes an outer loop of at most 3 attempts around `runHarnessAttempt`. A deterministic `verifySuccessfulUpvote` reads the trace: success only if an upvote click truly succeeded; fail early if the auto-login tool reported failure, or if the browser is on the login URL and auto-login never ran. **Result:** still fails, but **stops lying**. "Step one to solving a problem is admitting you have one."
5. **Login handler.** Runs every loop iteration just before the trace push. Checks the browser URL; if not the login page, does nothing (cheap). If it is, the harness fills credentials (from an environment variable) and submits the form, then pushes a message: "I'm the harness, I logged in." **Result:** logs in and upvotes; succeeded after 6 iterations; verified by hand on Hacker News.

To redraw: an inner **agent loop** (model ↔ tools ↔ browser) inside an outer **attempt loop** (max 3). On the inner loop's edges: **guardrails** (max steps, context compressor), a **login handler** hook reading browser URL and holding **secrets**, and a **trace** store receiving every event. After each attempt, a **verifier** reads the trace and returns pass / fail → retry or stop.

## Examples and numbers

- GPT-3.5 Turbo on purpose, to show a harness lifting an old model.
- Guardrails: 6 max iterations; 3 max attempts.
- IBM's **OpenRAG**: open-source enterprise RAG over Teams calls, PDFs and invoices, with "a hell of a harness" for security on siloed data.
- Advice: use cheap or free models (Qwen, GPT-OSS) with a great harness.

## Code and repos

Slides on GitHub (link not given in the description); talk page above.

## What this means for our options-research harness

1. The verifier must read the trace and the files, not the agent's summary. "Backtest done" counts only if the trace shows the run command and the results file exists with the expected columns.
2. Put deterministic handlers in the harness for known obstacles: Databento 422 on holidays and 504 on price calls get a harness-side retry/skip rule, not a prompt line.
3. Credentials stay in harness handlers; the model gets a message saying the step was done.
4. Wrap the agent loop in an outer attempt loop with a hard cap and an honest failure report.
5. Test the harness with a cheap model first: if a weak model succeeds inside it, a strong one will be more robust.
