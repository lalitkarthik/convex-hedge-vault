# 11 — The Engineering Behind a Self-Improving AI Agent

- **Title:** The Engineering Behind a Self-Improving AI Agent
- **Channel:** The Carbon Layer (Ankit Desai)
- **Id / link:** `qDJIEodb2tk` — https://www.youtube.com/watch?v=qDJIEodb2tk
- **Length:** 24:50
- **Article edition:** not linked in the video description.
- **Source of these notes:** auto-generated English subtitles (`en-orig`), read in full on 2026-10-17. Raw file stays in the session scratch folder.
- **Watch order note:** this is the sequel to video 02. It also uses the fingerprinting idea from video 08. Watch 02 and 08 first.

## Core thesis

The first pull request from the self-improvement loop (video 02) raised Carbon's tool-output limit from 4,000 to 12,000 characters. Every test passed. He rejected it, because a bigger bucket fixes one bounded case and keeps the same structural failure. The real fix was to widen the **editable surface** from one number to a set of named **strategies**. That one decision forced a chain of ordinary engineering: file lifecycle, secret leakage, a new boundary, a second access route, redone tests, and reproducible runs. The loop runs itself; the trust in its output must be engineered around it.

## Concepts, named as he names them

**The clamp problem.** A tool returned about 11,800 characters. Carbon's clamp kept the first 4,000 and dropped the rest. The answer sat beyond the cut, so the model never saw it. The tool had the data; the harness removed it before it reached the desk. This is a harness failure, not a model failure.

**Bucket size versus overflow handling.** Raising the limit to 12,000 made all the tests pass only because the longest test output was under 12,000. An answer at character 13,000 would fail again. The change was small, readable and reversible, which is good. But it moved the threshold and left the overflow rule (drop the tail) the same.

**Editable surface beyond raw numbers.** Instead of one knob (`max item characters`), the loop gets a schema with a choice of named strategies. The loop then selects a behaviour instead of tuning a number or editing arbitrary code.

**The three output strategies.**

- **Clamp** — keep the first N characters. The original behaviour.
- **Head and tail** — keep the same budget but split it, for example 2,000 from the start and 2,000 from the end.
- **Offload** — write the complete output to a file and give the model a compact reference to it. The model then decides which part to read.

**The lifecycle design question.** A file creates duties that did not exist under the clamp. Who creates it, what is it called, who may read it, how much is exposed, who deletes it, and can another run see it? A small strategy change became a lifecycle design problem.

**First attempt: offload folder inside the project.** He put the files in a hidden offload folder in the working directory, which is also the project directory. Both `bash` and `read_file` could reach it easily. The costs: the files persist in the workspace next to real work, later runs may read them as stray context, and no component owns the cleanup.

**The security test.** A test plants a fake secret shaped like an API key inside a tool output. After the run, it scans the workspace for those bytes. The bytes survived in the offload file. The secret had already entered the model's context, so Carbon did not cause the first exposure. But the offload strategy created a **second persistent surface**: a copy on disk that outlives the run.

**Separate model behaviour from storage policy.** Reading the tool output is model behaviour. Where the bytes are stored, and for how long, is a harness decision. Storage needs an owner and a lifetime that do not depend on what the model does.

**Second attempt: per-run scratch space.** Each run gets one private scratch directory when it starts. Offloaded outputs go there. The harness removes the directory when the run ends, on the failure path too. Now the store has a clear owner and a clear lifecycle.

**The reachability problem (blast radius versus reachability).** Carbon's normal tools are rooted in the project directory on purpose, to limit blast radius. The scratch directory is outside that root, so the agent's tools cannot see it. Moving the file out fixed contamination but made the artifact hard to reach. A new boundary needs an **explicit capability** across it, not a wider root.

**Logical reference (first adapter).** `read_file` accepts a stable logical name for the scratch store. It resolves the name inside the current run only and enforces the scratch boundary. The transcript stays portable because it never holds a machine-specific temp path.

**32 bash attempts, zero `read_file` calls.** In the confirmation run, the model tried to reach the scratch file 32 times, always through `bash`, never through `read_file`. Bash treated the logical name as a literal path, failed, retried, and spent the budget. Recovery was zero. The count is inflated by retries, but the signal is clear.

**Support the route the model takes.** He could have told the model to use `read_file`. Then correctness would depend on tool compliance, and compliance differs by model. Bash already has good retrieval tools (grep, sed, awk, jq), and this model prefers it. So the runtime should serve that route.

**One store, two adapters (the bash adapter).** One isolated store and one cleanup policy, both owned by the harness. Two legitimate access routes: `read_file` resolves the logical reference; `bash` reaches the same bytes through an environment variable that the runtime sets. The path is a runtime alias, so it is not baked into configuration or transcripts.

**Clean comparison.** Same model, same candidate, one runtime capability changed. Before the bash adapter: 0 of 10 tests recovered the answer. After: bash was used 18 times, `read_file` still zero times, and all 10 recovered the answer.

**Two counts, kept separate.** The **recovery** count comes from five test cases that check whether the model pulled the answer out of the offloaded file. The **paired confirmation** is a separate gate: it reruns the candidate against a fresh baseline, ten runs side by side, and the candidate must win on all of them with no regression anywhere.

**Propose, validate, confirm, accept.** The promotion process he used for this change.

**Tests that baked in the first implementation.** The old tests assumed the clamp. They had to be redone, and each test case now declares which strategy it intends to exercise.

**The ordinary engineering behind one setting.** None of it is new to software engineers:

- explicit interfaces and least privilege for each setting the loop may pick;
- refactoring, and **configuration validation**;
- the **strategy pattern**, with each strategy modular and selectable through the config file or an SDK parameter; users can add their own;
- **behaviour-focused testing** (system-level runs on real examples), plus unit, integration, **boundary** and **mutation** testing;
- Claude Code sessions paired with Codex as reviewer, which caught many issues;
- **reproducible experiments** through fingerprinting (see Examples);
- **per-feature regression checks**, staged releases, and review.

**Four properties the loop cannot provide on its own.** These come from the delivery system around the loop, not from the loop.

- **Boundaries** — the loop knows exactly what it may change and which state is protected.
- **Evidence** — when a behaviour moves, you can trace it to the change that caused it.
- **Isolation** — every run starts clean, gets private scratch space, and is torn down at the end.
- **Promotion** — nothing lands without confirmation runs, a human review, and a rollback path.

**The loop is the easy part.** He sums it up as: "Cron job can run the loop, but it cannot make the evidence trustworthy." The loop did not remove engineering. It kept showing where engineering was missing. The editable surface keeps moving as the harness becomes more configurable.

**Observe, analyze, improve, evaluate.** The working cycle he recommends, including separate review sessions to second-guess his own reasoning.

## The architecture, step by step (for Excalidraw)

Draw two nested regions: Carbon's run on the left, the refinery loop wrapped around it.

1. **Tool call** box → arrow "raw output (about 11.8k chars)" → **Output strategy selector** (diamond). Label the diamond "editable surface: clamp | head_tail | offload (schema-validated config)".
2. From the diamond, three arrows:
   - "clamp" → **Context window** with label "first N chars";
   - "head_tail" → **Context window** with label "head + tail";
   - "offload" → **Run scratch store** (cylinder) with label "full bytes", and a second arrow → **Context window** with label "compact reference".
3. Draw a dashed box **Project root boundary** around the workspace and the project tools. Put the **Run scratch store** outside this box.
4. **Run lifecycle (harness)** box above the scratch store. Arrow "create on run start" → store. Arrow "delete on run end, success or failure" → store.
5. **Model** next to the context window. From the model, two arrows towards the store:
   - **read_file adapter** (resolves the logical reference, enforces the scratch boundary);
   - **bash adapter** (environment variable alias set at runtime).
   Both arrows end at the same store. Label: "one store, two routes".
6. Red side box **Security probe**: arrow "plant fake key in tool output" → tool call; arrow "scan disk after run" → workspace. Annotate the first design: "offload in workspace → leak found".
7. Outer region **Refinery loop**: **Propose** (pick a strategy) → **Validate** (5 recovery cases) → **Confirm** (10 paired runs against a fresh baseline) → **Accept** (pull request) → **Human review** → back to Carbon's config.
8. **Fingerprint gate** on the arrow into Validate and Confirm: "Carbon sha, refinery sha, model, environment; mismatch → reject or rebase".
9. Label the four edges of the outer region: Boundaries (top, at the editable surface), Evidence (at the fingerprint gate), Isolation (at the scratch store), Promotion (at human review, with a "rollback" arrow back).

## Primitives, patterns and anti-patterns

- **Primitives touched:** context management (what reaches the window), execution environment (project root, scratch boundary), durable state (scratch store lifecycle), tool interface (two adapters), proof and learning (fingerprints, paired confirmation, the refinery loop).
- **Pattern:** expose behaviours, not numbers, on the editable surface.
- **Pattern:** the harness owns every file it creates, with cleanup on the failure path.
- **Pattern:** a canary secret plus a disk scan after each run.
- **Pattern:** one store, several adapters, matched to the tools each model actually uses.
- **Pattern:** change one runtime capability at a time for a clean comparison.
- **Pattern:** a targeted test count and a paired confirmation count, reported separately.
- **Anti-pattern:** accept a change because all tests pass when it only moves a threshold.
- **Anti-pattern:** put harness-created files inside the project workspace.
- **Anti-pattern:** widen the tool root to reach one new directory.
- **Anti-pattern:** fix a reachability gap with an instruction to the model.
- **Anti-pattern:** keep tests that encode the old implementation.
- **Anti-pattern:** trust the simple loop diagram; it hides most of the work.

## Examples and numbers

- Tool output about 11,800 characters; clamp at 4,000; first PR raised it to 12,000.
- Head-and-tail example: 2,000 + 2,000 within the same 4,000 budget.
- Logical-reference run: 32 bash attempts, 0 `read_file` calls, 0 recoveries.
- Bash-adapter run: 18 bash calls, 0 `read_file`, 10 of 10 recovered (from 0 of 10).
- Recovery cases: 0/5 → 5/5. Paired confirmation: 0/10 → 10/10 against a fresh baseline.
- Fingerprint fields: Carbon repo hash, refinery repo hash, model name, run environment. Any mismatch → treat as new or rebase.
- He reran the baseline six times for this one setting. All runs used a local model on his own machine, which was slow.
- Next video plan: benchmark Carbon, and compare it with Pi under the same model and configuration.

## Code or repos

- Carbon (the harness): https://github.com/thecarbonlayer/carbon
- Refinery (the self-improvement loop): https://github.com/thecarbonlayer/refinery
- The rejected first PR: https://github.com/thecarbonlayer/carbon/pull/1

## What this means for our options-research harness

1. Treat large tool outputs (option chains, Databento pulls, backtest logs) with the **offload** strategy: the full file goes to run scratch space, and the model gets a reference plus a short summary. Make output handling a named strategy on our editable surface, not one size limit.
2. Keep two stores apart. **Run scratch** belongs to one run and is deleted at its end, also on failure. **Research artifacts** (results files, findings pages) are promoted out of scratch on purpose, with lineage. Nothing lands in the repo by accident.
3. Add a canary test: plant a fake Databento-shaped key (`db-` plus 29 characters) in a tool output and scan the disk after the run. This extends the `.env` deny rule to copies the harness makes.
4. Serve the route the agent uses. If our agents read data with pandas or bash, expose the scratch path through an environment variable as well as a read tool. Do not rely on a prompt line that says "use read_file".
5. Fingerprint every backtest and eval run: engine commit, harness commit, model id, data snapshot hash, environment. Refuse to compare runs whose fingerprints differ.
6. Report two numbers for any harness change: the targeted test count and a paired confirmation against a fresh baseline with no per-task regression.
7. Before we accept "all green", ask whether the change fixes the class of failure or one bounded case. Widening a data window to dodge a holiday gap is a bigger bucket; fixing the half-day loader is the structural fix.
8. Use the four properties as the acceptance checklist for any self-improving research loop: boundaries, evidence, isolation, promotion.
