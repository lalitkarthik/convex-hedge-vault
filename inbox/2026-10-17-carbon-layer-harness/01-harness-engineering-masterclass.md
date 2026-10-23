promoted: 2026-10-23
# 01 — Harness Engineering Masterclass

- **Title:** Harness Engineering Masterclass: Technical Deep Dive on how to build Agentic Systems
- **Channel:** The Carbon Layer (speaker: Ankit Desai)
- **Id / link:** `mQfTdNVCOB0` — https://www.youtube.com/watch?v=mQfTdNVCOB0
- **Length:** 28:06
- **Article edition:** https://thecarbonlayer.com/harness-engineering/
- **Source of these notes:** the auto-generated English subtitles, read in full (2026-10-17).

## Core thesis

The model is one part of an agent. The **harness** is the system around the model. It decides what the model sees, what it can do, what it remembers, what work it hands off, how the work is checked, and how the system recovers from failure. When an agent fails, the first question is not "is the model good enough?" but "which harness layer ran out of road?"

## Three things to keep apart

The speaker separates three words before he starts.

- **Model** — the reasoning engine. Prompt in, text out. It knows only its training data and what is in the prompt. When the task data is absent, it guesses; that guess is a **hallucination**.
- **Runtime / agentic loop** — the loop in which the model reasons, acts, observes, and repeats. He cites the OpenAI Agents SDK definition: a model with instructions, tools, and an environment to act in.
- **Harness** — the system around the runtime. This is the subject of the video.

He says the primitive list is his own way to explain the field. It is not an agreed standard.

## The primitives, in the order he builds them

Each primitive solves the limit of the one before it. That "each layer runs out of road" chain is the teaching method of the whole video.

1. **Instructions.** Who the model is, the kind of work, tone, constraints, style, review rules, things not to do. Examples: `AGENTS.md`, `CLAUDE.md`, system prompts, custom instructions, Cursor rules. They move repeated guidance out of the user's head and into the environment. **Limit:** instructions are *passive*. They can say "follow the conventions" but cannot discover them or inspect a file.
2. **Context delivery.** The harness gives the model the material it needs: a file via `@`-reference, a failing test, a stack trace. A model with the source file gives a different answer from a model without it. **Limit:** dumping material in is not context engineering. Long chats and long logs overflow a finite window.
3. **Context management.** The harness decides what enters the model *on this turn*: retrieval (RAG), re-ranking, periodic summaries, **compaction** near the limit, prompt caches, session summaries. Its job is to *protect the model's attention*. Key claim: wrong context can be worse than missing context, because it gives the model a plausible distraction. **Limit:** the agent is still "a talker". It can name the command but cannot run it.
4. **Tool interface.** Tools turn talk into structured action. A tool has a name, a description, an input schema, and often an output schema. The model picks the tool and arguments; that is the model's side of the contract. MCP (Model Context Protocol) sits here as a standard way to expose tools. **Limit:** a tool call still needs a place to run and a trust rule for its output (messy text, partial data, prompt injection in web pages).
5. **Execution environment.** Where a tool call becomes "bounded reality": file-system scope, network, credentials, sandbox, container, dev container, worktree, browser profile, cloud workspace (vendors: Daytona, E2B, Docker sandboxes). The model asks to run a command; the harness decides where it runs, what it sees, what it may change, and whether a human must approve. Trust becomes practical here: do not ask the model to avoid secrets — do not give it secrets. **Limit:** one clean sandbox does not survive a pause, resume, fork, or crash.
6. **Durable state.** "The workbench that survives the current turn": plan files, checkpoints, task state, session summaries, logs, diffs, memory stores. For coding: a branch, a test log, a plan. For research: a source map, extracted quotes, a confidence table. The storage format does not matter; what matters is that progress is *inspectable outside the model's attention*. **Limit:** state preserves work but does not coordinate it.
7. **Orchestration.** The harness decides how work moves: lifecycle hooks, heartbeats, retries, approval gates, human handoff, tool wrapping, step order, task lists, model routing. Claude Code hooks are his main example. "The model is not doing all of that by willpower." **Limit:** one agent has one attention stream; serial branches are slow and crowd the context.
8. **Sub-agents.** The harness splits work into bounded loops: one explores, one reviews the diff, one verifies sources. The parent keeps responsibility to integrate. Two OpenAI SDK patterns: **agents as tools** (a manager calls specialists and keeps control) and **handoff** (the conversation moves to a specialist). A sub-agent is "a model with a narrower job, narrower context, and often narrower tools". He notes that the Pi harness has no built-in sub-agents. **Limit:** the **delegation problem** — each sub-agent invents its own process, so you get **parallel inconsistency**.
9. **Skill layer (skills and procedures).** Reusable procedures for recurring work: how to review a PR, run browser checks, use a repo. Also called slash commands, playbooks, runbooks, recipes. A good skill states when to use it, its inputs, its steps and order, and the preferred tools. It moves "remember to do X" from instructions into a named capability. **Limit:** a procedure is not evidence.
10. **Verification and observability.** Verification asks for receipts: tests, builds, type checks, lint, screenshots, evals. "Looks good to me" is not a verification strategy. Observability is the recorder: traces, tool-call timelines, logs, cost, latency, prompt and tool versions, approval events. The bug is often three tool calls before the final message.
11. **Evolution of the harness.** Failures become infrastructure. He gives a mapping (see Patterns below). This is the agent version of a post-mortem: change the system so the same *class* of failure finds it harder to come back. "The point is to make the next run start from a better place." With this layer, the harness compounds.

Note: in later videos he counts these as **10 primitives** and merges 10 and 11 into one box called **proof and learning**.

## The diagram he draws

He builds one picture layer by layer, then zooms out. To redraw it in Excalidraw:

1. Centre box: **Model**. Arrow in: "prompt". Arrow out: "text".
2. Wrap a loop around the model: **Agentic loop** (reason → act → observe → repeat).
3. Draw the harness as boxes around that loop, added in this order: Instructions, Context delivery, Context management (these three feed arrows *into* the model's input).
4. Tool interface on the model's output side; arrow from model to tools ("call with arguments"), arrow back ("result").
5. Execution environment as a boundary box *around* the tools ("where calls run, what they can touch").
6. Durable state as a store beside the loop, with arrows both ways (save progress / reload).
7. Orchestration as a frame around the whole loop (hooks, retries, approval gates, human handoff).
8. Sub-agents as smaller copies of the loop that branch off the main loop and return results.
9. Skill layer as a library box that feeds procedures to the main agent and to every sub-agent.
10. Verification and observability as a checkpoint after the loop's output plus a recorder line along every arrow.
11. A feedback arrow from observability back to every other box: **evolution** (failures → rules, schemas, gates, tests, memories, skills).

He says the finished picture resembles the published architecture of Claude Code, Codex, and Gemini CLI.

## Patterns and anti-patterns

- **Failure-to-fix mapping (evolution):** repeated context miss → retrieval rule; bad tool result → stricter schema; dangerous command → permission gate; missed edge case → test; recurring correction → memory; repeated workflow → skill.
- **Anti-pattern:** blame the model first.
- **Anti-pattern:** dump all context in.
- **Anti-pattern:** tell the model not to touch secrets instead of withholding them.
- **Anti-pattern:** trust a confident final sentence.
- **Anti-pattern:** let every sub-agent invent its own process.

## Examples and numbers

- Agents named: Codex, Claude Code, Gemini CLI, Pi, OpenClaw (heartbeats), Hermes agent (turns repeated workflows into skills).
- He recalls a harness that ran tests without being asked; he says many people credited that to the model, but the harness prompted it.
- No numeric results in this video.

## Code or repos shown

None. The code companion is video 03 (repo https://github.com/thecarbonlayer/carbon).

## The closing diagnostic

When an agent fails, walk the layers: Instruction missing? Context wrong? Memory stale? Tool schema vague? Wrong environment? State not durable? Orchestration needed? Should it have been delegated? Skill missing? No verification? No trace? Did we learn nothing from the last failure?

## What this means for our options-research harness

1. Write the harness as these named layers so each failure has an address. A bad backtest result gets triaged by layer (wrong data delivered? tool returned stale chain? no verification?), not by "the model is weak".
2. Keep durable state outside the chat: a run directory with the plan, the data manifest, every trial, and the result table. This is the "source map / confidence table" idea applied to research.
3. Treat verification as receipts: a research claim counts only with a reproducible notebook run, a fingerprinted results file, and the trial log (this matches the deflated-Sharpe rule of logging every trial).
4. Give Databento and broker credentials to the harness, never to the model. The execution environment injects keys; the model never sees `.env`.
5. Put recurring research procedures (Bilal's bucket test, the candle i−1 decision rule) into skills, so that every sub-agent runs the same method and we avoid parallel inconsistency.
6. Add the evolution loop from day one: every failure we find becomes a test, a schema rule, or a skill update, logged in the run record.
