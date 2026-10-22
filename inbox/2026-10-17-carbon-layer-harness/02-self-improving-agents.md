# 02 — Self-Improving AI Agents: Evolving the Harness, Not the Model

- **Title:** Self-Improving AI Agents | Evolving the Harness, Not the Model
- **Channel:** The Carbon Layer (Ankit Desai)
- **Id / link:** `KoDohnhLpJM` — https://www.youtube.com/watch?v=KoDohnhLpJM
- **Length:** 35:19
- **Article edition:** https://thecarbonlayer.com/self-evolving-harness/
- **Source of these notes:** auto-generated English subtitles, read in full.
- **Watch order note:** this video assumes video 03 (the agent built from scratch). Watch 03 first.

## Core thesis

"Self-improving AI" can mean a model that retrains itself. This video means a narrower and safer thing: a loop that improves the **harness** and leaves the frozen model alone. A second, stronger model watches the agent fail, proposes a harness change inside a declared **editable surface**, and the change is measured against hidden tests before a human merges it. Every improvement is a change you can read, test, and undo.

## Concepts and principles

- **Frozen model.** The weights do not change. All improvement happens in the software around the model.
- **Loop engineering.** Lilian Weng's name for the practice. He notes others use the term too (Peter Steinberger, Boris at Anthropic).
- **The five-level ladder (Weng).** Safest at the bottom, riskiest at the top; each level contains the ones below.
  1. Improve the prompt (system prompt, `AGENTS.md`).
  2. Improve the context (material fed in).
  3. Improve the workflow (the steps the agent takes).
  4. Improve the harness code. **This video works at level 4.**
  5. Improve the thing that does the improving (meta level).
- **Weakness mining (Self-Harness paper).** Run the agent normally, let it fail, then ask whether failures share one real cause. Group only failures with a provable shared cause. A single flaky slip does not count.
- **Cluster.** A group of failures with one shared cause. The rest of the pipeline works on clusters.
- **Choose the right kind of fix (AReaL paper).** A missing plain fact → put it in **memory** (cheapest). A failure in tool routing, reading results, or guardrails → **harness edit**. A failure that shows up everywhere whatever you do → touch the **model**.
- **Miners vs regression guards** (his own terms). Miners are tasks you expect to fail because you found a gap; they feed mining. Regression guards are tasks you expect to pass; they complain loudly if a fix breaks something else. You need both.
- **Held-in vs held-out** (Self-Harness). Held-in tasks are shown to the fixer. Held-out tasks are hidden from it. The hidden pile is the only defence against a fix that games the visible test.
- **Pass fraction, not pass/fail.** Small quantized models are not consistent. Run each task several times and record a fraction (2/3). Compare by averaging fractions, not by majority.
- **Acceptance rule** (Self-Harness). A candidate must be at least as good on both held-in and held-out, and strictly better on at least one. Better in one place and worse in another → reject. No partial credit.
- **Explain or drift** (AReaL). A self-evolving system that cannot explain what changed is not evolving; it is drifting.
- **Rollback is first class** (AReaL). Undoing a change must be a normal operation, not an emergency.
- **Editable surface.** A short, named, versioned list of what the improver may change. Everything outside stays untouchable.
- **Separate proposer from patient** (his variation). The paper uses one model to diagnose itself. He keeps the small local model (Gemma) frozen and uses a stronger external model to diagnose and propose, because a small model cannot see past its own blind spot.
- **Capability mismatch** (his term). A strong proposer can suggest something too clever for the weak patient to follow.
- **Keep the grader away from the editor.** If tests sit near what is edited, the editor can "cheat efficiently" by editing the test.
- **Traces, not just scores** (AReaL). Every run is recorded in full — every tool call and reply — stamped with the agent commit and the config version.
- **Safe, audited, staged deployment** (AReaL phrase). Each change carries its own promotion path, reviewed before it ships.
- **Held-out leakage.** Using the hidden pile to choose between candidates leaks information into the winner. Over many iterations the hidden pile stops being hidden. Fix: retire and replace held-out tasks from time to time.

## The architecture (the improvement loop)

Draw as a loop with a human gate at the exit:

1. **Agent (frozen model + harness)** runs the **test suite** (13 tasks, 4 groups) several times per task.
2. Runs write **full traces** (tool calls, replies, commit, config version) to a **run store**.
3. **Weakness mining** reads the traces and groups repeated failures into a **cluster**; flaky noise is set aside.
4. **Fix-type decision:** memory vs harness vs model. Here: harness.
5. **Proposer model** (external, stronger) reads the held-in failing trace and writes candidate edits *only* to the **editable surface** (one JSON config file), each with a risk note.
6. **Candidate runner:** applies one candidate to the working copy (marked `dirty: true` with a fingerprint), runs the *full* suite, then reverts. A rejected candidate never becomes a commit.
7. **Acceptance rule** compares per-task pass fractions on held-in and held-out against the baseline.
8. Winner → **pull request** on a separate branch with a per-task table.
9. **Human review** (merge or not). Arrow back to step 1 for the next iteration.

Side boxes: the **grader and answer keys** live in a separate area the proposer never sees; the answer-key files are **fingerprinted** so editing them fails the task.

## How he built the loop

He built the improver the same way as the agent: one AI session read and synthesized the three sources; a separate session with none of that context reviewed it adversarially; other sessions built the config file and the runner. Each received a self-contained brief "instead of a shoulder tap".

## Examples and numbers

- **The failure:** a question whose answer sits near the end of a long log file. The harness **clamp** function (six lines) keeps the head up to a limit and drops the rest. The model said honestly that the log was truncated and it could not answer. An honest model points the bug at the plumbing.
- **Editable surface:** knobs collected from 5 files into 1 file — 35 lines, 11 values, 1 version number.
- **Adversarial review** found 5 problems in the checks before any live run, including: a test a do-nothing agent could pass; nothing stopping a fix from rewriting the answer key.
- **Suite:** 13 tasks in 4 groups — long-session information loss; claims of success it cannot prove; leaks; tool use instead of guessing. Each task grounded in a real past failure. 3–5 tries each; 49 separate runs per candidate.
- **Baseline:** all green except two tasks: A2 (held-in) failed 3/3, A4 (held-out) failed 5/5 — one cluster.
- **Dry-run bug:** one test compared against the *live* editable value, so the best fix would have errored. The measuring stick was coupled to what it measured. He pinned it and re-recorded the baseline.
- **Candidates:** 4,000 → 8,000 chars: near miss (the answer starts at char 8,690). 4,000 → 12,000: fixed, no cost elsewhere; replies took under 2 s instead of about 19 s. Third candidate: broke a previously always-passing task (empty replies after over a minute) while a flaky task ticked up by about the same — the aggregate barely moved. Only per-task inspection caught it.
- **Result:** PR #1, "max item characters 4,000 → 12,000", left open, not merged.
- **Honest limit:** the fix only made the bucket bigger. A better fix (keep head *and* tail, as compaction already does) is code, outside the editable surface.

## What he plans next (added 2026-10-17 from the transcript; video 11 carries out item 1)

He names three gaps in this first version rather than hide them.

1. **Widen the editable surface beyond values**, so the loop can propose a strategy for a failure class, not only a bigger number. Video 11 does exactly this and rejects PR #1.
2. **Look harder at the flaky tasks** that mining set aside as noise. More attempts may reveal a second real cluster under the noise floor.
3. **Widen the suite beyond failures he has already met.** The suite tests only what his own use exposed. A wider view of where the harness should improve, plus a matching editable surface, widens what the loop can find.

The improvement loop's first PR stays open, not merged; in video 11 he states that he rejected it.

## Code and repos

- Carbon (the harness): https://github.com/thecarbonlayer/carbon — PR #1: https://github.com/thecarbonlayer/carbon/pull/1
- Refinery (the self-improving loop): https://github.com/thecarbonlayer/refinery
- AReaL paper: https://arxiv.org/abs/2607.01120
- Self-Harness paper: https://arxiv.org/abs/2606.09498
- Lilian Weng, "Harness Engineering for Self-Improvement": https://lilianweng.github.io/posts/2026-07-04-harness/

## His checklist for any "self-improving" claim

A real failure found in logs → grouped with failures of the same cause → separated from noise → tested on work the fixer never saw → fixed inside a named editable surface → checked against every task → protected against gaming its own test → landed as a PR that waits for a person.

## What this means for our options-research harness

1. This is the same problem as strategy overfitting. Held-in / held-out is our in-sample / out-of-sample split, and "held-out leakage" is the same effect that deflated Sharpe corrects for. Use the same discipline for harness changes as for strategy changes.
2. Declare an editable surface for the research harness (for example `harness-config.json`: data windows, cost model knobs, tool output limits). Agents may only propose changes there.
3. Keep graders and answer keys (fixture results, reference P&L files) outside the agent's workspace and fingerprint them.
4. Record pass *fractions* over repeated runs and compare per task, never only the total.
5. Each accepted change ships as a PR with a per-task table and waits for Lalit or Bilal. No automatic merge.
6. Before fixing, classify the failure: missing fact → memory note; plumbing → harness; everywhere → model choice.
