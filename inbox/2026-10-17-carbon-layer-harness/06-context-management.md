promoted: 2026-10-23
# 06 — Context Management Masterclass

- **Title:** Context Management masterclass
- **Channel:** The Carbon Layer (Ankit Desai)
- **Id / link:** `mM_Wxemh3lU` — https://www.youtube.com/watch?v=mM_Wxemh3lU
- **Length:** 35:38
- **Article edition:** https://thecarbonlayer.com/context-management/
- **Source of these notes:** English subtitles, read in full.

## Core thesis

"Your agent didn't get dumber. Its window got messy." Context management is the primitive that decides what reaches the model on each turn. Its job is to protect a finite attention budget. He breaks it into **four moves — select, compress, write, isolate** — and adds a fifth concern that most talks skip: **prompt-cache stability**. The universal habit: look at what actually reaches the model.

## The running bug (StreamIt)

An agent debugged StreamIt, an app that streams a cricket match from a phone over WebRTC to a Node server that re-encodes with FFmpeg and pushes to YouTube. Symptom: choppy low-resolution video and garbled audio on cellular. The ticket linked Docker logs, an earlier session, and a design document. Around turn 40 the agent reopened a file it had edited, proposed a fix it had ruled out, and contradicted an agreed decision. Same model, same weights, same settings. The window had filled with logs, half-read files and tool output.

## Four ways long context goes bad (Drew Breunig)

- **Poisoning** — a wrong fact or bad tool result enters and is referenced as true.
- **Distraction** — the context is so long the model leans on it instead of its training.
- **Confusion** — irrelevant material in the window degrades the answer.
- **Clash** — facts in the window contradict each other.

StreamIt had distraction (a log of thousands of lines) and clash (the design doc said frames were already normalized to 1080p; the deployed code did not do that, and the agent trusted the doc).

## Where it sits (boundaries)

- Primitive 3 in his stack: after context delivery, before tools.
- **Not RAG.** RAG asks what knowledge exists that could be pulled in. Context management decides what goes into *this* prompt *this* turn.
- **Not memory.** Memory is what survives between runs.
- His one-liner: delivery is what is reachable; memory is what sticks around; context management is what makes it onto the desk for this turn.

## The naive approach

Put everything in. Windows are large (hundreds of thousands of tokens; up to a million). It can work on short tasks. It fails on **long-horizon tasks**, and you pay for every token on every turn.

## The four moves (Lance Martin, LangChain), in the order they bite

1. **Select** — pull the slice this turn needs. Selection must itself be cheap and approximate (embeddings, recency/relevance ranking, search index, scannable descriptions). **Tool selection** breaks down as the tool set grows (Lance's rough figures: trouble in the tens, real failures near a hundred; he warns not to quote these exactly). Mature harnesses **retrieve tools** like documents. **Selection across time**: Codex and Claude Code isolate sessions; Hermes stores every session in SQLite with FTS5 and gives the model a `session_search` tool. **Position matters**: "lost in the middle" — models use the start and end of a long context reliably and the middle poorly. Selection is two decisions: what goes in, and where it sits.
2. **Compress** — summarize running history, trim what is no longer load-bearing. A good compaction keeps: the **goal**, **constraints and decisions** locked in, **progress** (done / blocked), **key files and facts**, and the **next step** — "what you would write a teammate before a vacation". Two hidden costs: it is **lossy** (it can flatten the smoking gun — resolution oscillating 1280×720 ↔ 904×508 and hundreds of restarts — into "video quality is unstable"), and it is itself an **LLM call** (compacting too often spends tokens to save tokens and breaks momentum). The trigger and the compaction prompt are **design surfaces, not defaults to inherit**.
3. **Write** — move what you cannot afford to lose *out of the conversation* into a scratch file on disk. A compaction cannot delete what was never in the window. **Dex Horthy (HumanLayer)**: write a research file (files and line numbers) and a plan file before code; run each implementation step in a fresh window seeded by the plan; he reports staying under 40% of the window. Boundary: a scratch note for this task is context management; a note meant for future runs is memory.
4. **Isolate** — give a sub-task its own context and bring back only the result. Searching the huge Docker log is a sub-agent job; it returns "226 restarts, here is the resolution collapse sequence". Isolation buys **total capacity** (five windows hold more than one) and costs **coordination** (which hands off to orchestration).

## The prompt-cache cost

Providers cache the prompt **prefix**; an identical prefix is discounted (he says up to 90%). Changing something early invalidates every token after it. So every re-select, re-rank or compress may blow the cache. "A harness that reshuffles context every turn can be correct and still slow and expensive." Rule: **freeze a stable prefix** (identity, instructions, tools) and let only the tail move.

## Codex vs Hermes

| | Codex ("discipline at the door") | Hermes ("flexible window with reach-back") |
|---|---|---|
| Select | Walks `AGENTS.md` from cwd to repo root within a byte budget; no cross-session recall | `session_search` over all past sessions (SQLite + FTS5) |
| Compress | Hard caps per item: no item over 10k tokens; items that may cross 1k tokens flagged; skills budgeted at 2% of window; configurable auto-compaction limit and custom compaction prompt | Checks before each turn; compresses at a threshold (default 50% of window, can be 70–80%); protects first and last messages; rebuilds the whole prompt |
| Cache | Rules: build context incrementally, do not rewrite history, avoid cache misses | System prompt built once per session; late memory injected into the user message so the prefix stays frozen |

Both share: bounded assembly, a stable cached prefix, and progressive disclosure. Claude Code (used for StreamIt) lets you toggle auto-compaction and give a one-time focus, but not move the threshold.

## Observability

You cannot tune selection or compression blind. Look at a context readout; the first look usually surprises (half the window a forgotten log, three copies of a note, a 20-turn-old tool result). Tracing tools that speak OpenTelemetry (LangFuse, LangSmith) capture the full prompt, messages and tools per call.

## His workflow: research → plan → implement

Close to Dex's **intentional compaction**. Research writes a one-page findings file. Plan writes the intended changes to a plan file; you review the plan, where a misunderstanding costs "one comment instead of a day". Implement runs in a fresh window from the plan. Research sub-agents should write findings to a file so the next agent reads the file, not the transcript.

## Diagram to redraw

1. Left: **sources** — ticket, logs, design doc, repo files, past sessions, tool results.
2. Arrow into a funnel labelled **Select** (ranker, tool retrieval, session search) — output: a slice.
3. Slice placed into the **context window** drawn as a bar: **stable prefix** (identity, instructions, tools; marked "cached") on the left, **moving tail** (selected material, recent turns) on the right; mark the middle "lost in the middle".
4. **Compress** box acting on the history inside the window, with protected head and tail.
5. **Write** arrow from the window to a **scratch file / research file / plan file** on disk, and a reload arrow back.
6. **Isolate** arrow from the window to a **sub-agent window**; only a short result returns.
7. **Observability** probe reading the window's actual payload.

## Diagnostic at the end

When an agent goes dumb mid-task, walk the moves: Select (did it have the right thing, or was it buried?), Compress (did the summary drop a key detail?), Write (did it lose work it should have parked?), Isolate (did one giant context drown a sub-task?). Under all four: could I see the window? StreamIt was select + compress; the fix was to send the log to a sub-agent that wrote findings to a file.

## What this means for our options-research harness

1. Never put a raw option chain or tick log in the main window. A sub-agent reads it and returns a summary table; the full file stays on disk with a path.
2. Freeze the prefix of every research agent (role, rules, tool list) and append only at the tail, so long sessions stay cheap.
3. Write our own compaction prompt that always keeps: hypothesis, data window, cost assumptions, trials run so far, decisions, next step.
4. Adopt research → plan → implement as the default for every strategy study, each phase writing a file (matches the vault's inbox pattern).
5. Retrieve tools per task rather than registering every MCP tool on every call once the research tool set grows past a dozen.
6. Add a "context readout" to the trace: tokens per section per call.
