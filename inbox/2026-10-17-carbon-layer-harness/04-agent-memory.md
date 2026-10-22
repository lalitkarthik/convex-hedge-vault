# 04 — AI Agent Memory Masterclass

- **Title:** AI Agent Memory Masterclass | How Agents Remember and Forget
- **Channel:** The Carbon Layer (Ankit Desai)
- **Id / link:** `PxuMqeIqCEo` — https://www.youtube.com/watch?v=PxuMqeIqCEo
- **Length:** 27:18
- **Article edition:** https://thecarbonlayer.com/agent-memory-architecture/ (13-slide deck linked there)
- **Source of these notes:** yt-dlp hit HTTP 429 twice; the transcript came through Firecrawl's YouTube scrape and was read in full, cross-checked with the article edition.

## Core thesis

The model remembers nothing across sessions; its weights do not change. Whatever feels like memory is the harness deciding what to **keep, recall, update, and forget**. "Memory is context assembly over time": durable stores hold state, a context builder assembles a slice each turn, and the model acts only on what reaches the window. The hard part is not storage but the decisions about storing, retrieving, ranking, resolving conflicts, and retiring.

## Running example (CrikIT issue #9)

CrikIT is his cricket-league app. The request: pick up issue #9 (a player profile shows the old club after a membership change), assigned to "Buddy Bean Town", using "the same approval-gated Codex workflow as last time". The gate: Codex implements only after someone comments `@codex implement` under a written proposal; until then it stays in read-only investigation. Project rules: read the getting-started doc first; work only inside two named folders. Getting this right means lining up the request, past history, project facts and workflow before touching anything.

## Concepts

- **Memory as a harness primitive.** Memory decides what state survives long enough to shape the next action. It is where context management and durable state meet.
- **Memory vs RAG.** RAG asks what external knowledge to retrieve for this answer. Memory asks what state should survive across turns, sessions, users and workflows.
- **The session boundary.** Inside one chat the model "remembers" because the earlier message is still in the window. A new session has nothing; a good guess is still a guess.
- The four-type split comes from cognitive science, mapped to language agents by the **CoALA** paper (https://arxiv.org/abs/2309.02427).

### The four memory types

1. **Working memory** — the active context window this turn: latest message, prior replies, instructions, files, tool results. It runs on a budget. A 200k or 1M window is a bigger working-memory budget, not persistence. It breaks two ways: **it ends** (session gone) and **it fills up** (everything competes; "emptying the whole filing cabinet onto the desk to find one sticky note").
2. **Episodic memory** — what happened, with a **when**: a specific investigation or session. Usually logs stamped with time and session ID. Storage can be simple (Markdown, SQLite with full-text search); vector DBs help when keyword search is brittle; a **temporal knowledge graph** tracks when each fact was true. Three tests: can it find the event, recover the right slice, and tell old state from current state? **Limit:** it tells you what happened, not what is true now.
3. **Semantic memory** — standing facts that "float free" of time: user facts, project conventions, current state; the layer `AGENTS.md` / `CLAUDE.md` occupy. Stored as key-value or Markdown notes. **Cost:** maintenance — facts go stale and conflict (issue was "open, not approved", later "approved"); preferences stored as absolutes ("keep answers short") fight later requests. Three chores: what to save, update, retire.
4. **Procedural memory** — how work gets done: runbooks, checklists, skills. "Implementation requires approval" is semantic; "here is the approval-gated sequence" is procedural. It lives in **tool schemas** (a schema can force an issue number, approval comment ID, branch name), **skill files / runbooks**, and **orchestration code** (workflow graphs, loops, approval gates). People call it tools or automation, not memory. It goes stale too, and a stale procedure followed confidently makes the system worse.

### Assembly

- **Filing cabinet and desk.** Durable stores are the cabinet; working memory is the desk; the model only works at the desk.
- **Context builder** — the harness part that retrieves, ranks, resolves, and assembles the prompt each turn. The model does not browse stores unless given tools.
- **Product check:** Hermes exposes session search, memory files, and skills — almost one-to-one with episodic, semantic, procedural. Letta, Mem0, Zep Graphiti, LangChain long-term memory draw the same lines differently. Ask which job a product's memory actually does.

### Failures and forgetting

- **The interesting failures are conflicts.** A weak system treats them as a *retrieval* problem (grab something similar). A strong one treats them as a *state* problem (what was true then, what is true now, which procedure governs). "Just give it a vector database" cannot see that the issue moved from non-qualifying to qualifying.
- **Forgetting is hygiene, not loss.** Old memories may stay; they must not outrank what is true now. Per type: working → selection; episodic → compression; semantic → conflict resolution; procedural → maintenance.
- **Four strategies:** **temporal decay** (older items lose priority unless pinned, recently used, or tied to policy); **contradiction handling** (new fact updates current state, old one kept as history); **compression** (sessions → summaries → facts → procedures); **manual curation** (rules, approval gates, onboarding, production checks need an owner).
- **The big-window argument.** A bigger window adds working memory but will not find the right session, tell which fact is current, or retire a runbook. "Move the mess into a bigger room."

## Diagram to redraw (his Fig. 02 and Fig. 03)

1. Left column, three stacked stores: **Episodic** (what happened — session DB), **Semantic** (what is true — fact store / memory files), **Procedural** (how to act — skills, tool schemas, orchestration code). Also documents/files.
2. Arrows from each store into a middle box **Context builder** with four steps: retrieve → rank → resolve → assemble.
3. Arrow from the builder into **Working memory (the active context window)**.
4. Arrow into **Model**, which may call tools and observe results, then responds. Caption: stores do nothing until a slice reaches the window.
5. Conflict inset: two cards "THEN: open, not approved" and "NOW: `@codex implement` present" both feed the builder; "rank by similarity" sees equals; "resolve by timing" lets NOW outrank THEN.
6. Forgetting inset (Fig. 04): "everything ever saved" → decay, compress, curate, resolve → "current facts, summarized recent sessions, owned runbooks".

## Examples and numbers

- Window sizes cited: 200k and 1M tokens. No experimental numbers in this video.

## Five questions for any agent

1. What is in working memory now (what did the model actually see)? 2. Which past session matters, and can the agent find it? 3. Which facts are current, and how are they updated? 4. Which workflow applies, and where is it encoded (tools, skills, orchestration)? 5. What should be forgotten, how does old state lose priority, who owns the procedures?
"If you cannot answer those, you probably have scattered state."

## Code or repos

None shown.

## What this means for our options-research harness

1. Split research memory into the four types: episodic = the trial log and run records (with timestamps); semantic = canonical facts (contract specs, holiday calendar, cost model) in `domain/` notes; procedural = skills for the research methods.
2. Every semantic fact carries an as-of date, so the builder resolves by timing (for example "Databento last-12-months is free" as of a date). This matches the vault rule of `As of <repo>@<sha>`.
3. Treat conflicts as state problems: when a new backtest contradicts an old note, update the current fact and keep the old one as history, never side by side as equals.
4. Give procedures an owner and a review date; a stale data-loader procedure (half days) is a real risk.
5. Do not count on a bigger window. Keep a session-search tool over past research runs instead of replaying transcripts.
