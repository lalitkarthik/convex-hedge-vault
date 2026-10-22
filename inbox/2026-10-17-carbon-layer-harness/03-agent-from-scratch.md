# 03 — Building an AI Agent From Scratch in Python

- **Title:** Building an AI Agent From Scratch in Python – One Primitive at a Time
- **Channel:** The Carbon Layer (Ankit Desai)
- **Id / link:** `oUBgqzcV1qw` — https://www.youtube.com/watch?v=oUBgqzcV1qw
- **Length:** 34:11
- **Article edition:** https://thecarbonlayer.com/building-an-agent-from-scratch/
- **Source of these notes:** English subtitles, read in full.

## Core thesis

**An agent = a model + a harness + a UI.** The model is a stateless reasoning engine behind one API call. The UI is only how a human reaches it. Everything that makes it *feel* like an agent lives in the harness. The video turns each primitive from video 01 into code, one chapter (and one git tag) per primitive, about 2,500 lines of Python in total. The model's weights never change; the harness turns the model into an agent.

## Build rules he sets up front

- **Three packages, one-way arrows:** UI → harness → model. The core never knows a screen exists. A new model provider is "drop in a file" (a pattern he credits to Pi).
- **OpenTelemetry instead of a home-made logger**, so traces can go anywhere (TUI today, Jaeger tomorrow).
- **Chapter rhythm:** build the primitive → break it to show why it is needed → fix it → demo on a real model. "The previous layer wasn't wrong, it just wasn't finished."
- Model used: Gemma 4 26B (A4B) served locally by LM Studio; providers swappable (LM Studio, Ollama, OpenRouter, a fake provider for tests).

## The chapters (each a primitive and its failure)

Order note (added 2026-10-17): the build order here differs from the primitive numbering in video 01. Tools (ch 5) come before context management (ch 6), and the sandbox (ch 8) and durable state (ch 9) come after skills (ch 7). The build follows what breaks first in code; video 01 follows the request path. See [principles](principles.md), "Where the series disagrees".

| Ch | Primitive | What the code adds | The gap that motivates the next chapter |
|---|---|---|---|
| 0 | Setup | Three packages, git tags ch0–ch14, `uv run demo`, `uv run agent` | — |
| 1 | Bare model | `Agent.send` = one chat call, no message list | It forgets your name on the next call: the API is **stateless** |
| 2 | History | `self.messages` list; append user, send all, append reply (3 lines) | "The single most important idea": the harness replays history. But no standing personality |
| 3 | Instructions | System prompt + auto-loaded `AGENTS.md`; a **workspace** directory the agent owns | A path is only a string; the agent cannot read the file |
| 4 | Context delivery | `@path` references scanned, read from disk, injected before the question (raw, whole file) | It can read but cannot act |
| 5 | Tools | Tool = **function + schema** in a registry; loop capped at 6 steps; file tools scoped to the workspace; bash in a sandbox (Docker, else subprocess); **approval gate** for bash and writes | Every call and result piles into a finite window |
| 6 | Context management | The four moves named (select, compress, write, isolate); builds **compress**: summarize the middle, keep **head and tail**; `clamp` caps every item at max characters | It re-derives the same procedures every time |
| 7 | Skills | `skill.md` folders with name + description front matter; **progressive disclosure** (only descriptions in the prompt; body read on demand with `read_file`) | Untrusted code still runs on your machine |
| 8 | Sandboxing & security | **Start closed**: no network, scoped file system, no credentials; Docker non-root, capabilities dropped, read-only FS, memory and process caps; `read_file` fenced to the workspace; verifier env scrubbed. Compaction now triggers on model-reported tokens | Kill the process and the conversation is gone |
| 9 | Durable state & memory | `memory.py`: sessions as **JSONL**, one message per line, load at start, save each turn; **episodic search** = plain keyword search across stored sessions (borrowed from Hermes) | A turn is one opaque loop; you cannot hook, gate or see its steps |
| 10 | Planning / orchestration | `orchestrator.py` control plane: the **model plans steps as JSON, the harness drives them** (gate, execute, retry); `/plan` command; agent loop unchanged | All steps share one context window |
| 11 | Sub-agents | `subagents.py`: fresh agent, own context and tools, returns the **reply, not the transcript**; tools `delegate` and `fan_out` (parallel) | "Done" is still a sentence, not a fact |
| 12 | Verification | Harness watches the transcript and refuses "done" until a real passing run (exit 0) appears; command read from a *Testing* section of `AGENTS.md`; gate arms only when the turn wrote a code file (by extension) | When a run breaks, the cause is usually earlier than where it shows |
| 13 | Observability | Tracer with spans for model calls, tool calls (with arguments and results), plan and verify steps; tokens, latency, cost from a pricing table (local = free); **one emit, many sinks** (UI, JSONL, console, OTel collector) using OTel GenAI conventions | Only a REPL to see it |
| 14 | Real UI | Textual TUI: conversation left, live trace right; approval gate as a modal with a unified diff; runs the same agent in a worker thread on a **git worktree** | — |

## Key principles stated

- "The model decides what to call, but the harness decides how and then actually runs it."
- "The prompt is intent, not containment." The boundary lives in the harness.
- Approvals are scarce on purpose; with no approver wired up, a gated call fails closed.
- Sandbox ladder chosen by **blast radius**: OS sandbox → container → user-space kernel → micro-VM.
- Context isolation is a feature.
- "A good UI is a consumer of events, not an owner of them."
- Done is a fact only with receipts.

## The architecture to redraw

1. Three stacked layers: **UI** (top) → **Harness** (middle, large) → **Model** (bottom). Arrows point down only.
2. Inside the harness, a central **agent loop** box holding the **message list**.
3. Inputs into the message list: system prompt, `AGENTS.md`, skill descriptions, `@file` contents, compacted summary.
4. Loop → **tool registry** → (approval gate) → **sandbox** (Docker / subprocess) → result back to the message list.
5. **Compaction** box on the message list (head + summary + tail) and **clamp** on each tool result.
6. **Session store** (JSONL on disk) with save/load arrows and a **search_sessions** tool.
7. **Orchestrator** above the loop: plan JSON → gate → execute → retry, calling the loop per step.
8. **Sub-agent** boxes off the loop via `delegate` / `fan_out`, returning one reply each.
9. **Verifier** after the loop: reads transcript, requires exit 0 from the Testing command.
10. **Tracer** alongside everything → event seam → sinks (TUI pane, JSONL, console, OTel).

## Code and repo

- https://github.com/thecarbonlayer/carbon (renamed from `gemma`); tags `ch0`–`ch14`; `main` has the TUI (`uv run tui`).

## What this means for our options-research harness

1. Copy the one-way package rule: research UI/notebooks → harness → model adapters. Model choice (Opus, Sonnet) becomes a one-file swap.
2. Use the "build, break, fix" rhythm as our test plan: for each primitive we add, first write the failing case that shows why it is needed.
3. Clamp every tool output (Databento pulls, option chains, backtest logs) and prefer head + tail over head only, so the last rows of a chain or log are never lost (see video 02).
4. Arm the verification gate by output type: if a turn wrote a strategy file or notebook, "done" requires the backtest command to exit 0 and a results file to exist.
5. Emit one OpenTelemetry trace per research run with token cost per call; a local JSONL sink is enough to start.
6. Run each research task on its own git worktree, as the TUI does, so the main checkout stays clean.
