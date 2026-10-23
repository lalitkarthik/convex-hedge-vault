promoted: 2026-10-23
# Harness engineering — merged principles

The principles and ideology of The Carbon Layer's harness series (videos 01–11) and the IBM talk (video 12), merged and deduplicated. Each principle names its source videos. Numbers are stable: other notes may cite "P14". Terms are defined in [glossary](glossary.md); the master picture is in [diagram-spec](diagram-spec.md).

## A. What a harness is

**P1. Engineer the harness, not the model.** The model is one component. The harness decides what it sees, what it can do, what it remembers, how work is checked, and how the system recovers. When an agent fails, ask which layer ran out of road before you blame the model. (01, 03, 12)

**P2. The model is stateless and frozen.** Memory, agency, and improvement all live in software around the model. Even "self-improvement" changes the harness, not the weights. (02, 03, 04)

**P3. Add a layer only when you can show the failure that needs it.** Each primitive answers the limit of the one before it. Build it, break it on purpose, fix it, then demo it. (01, 03, 05)

**P4. Reliability is the goal; a strong harness lifts a weak model.** The model you rent is a black box you do not control. A good harness lets a cheap or weak model do the job, and a weak test model exposes harness gaps that a strong model hides. (08, 10, 12)

**P5. Look at what actually reached the model.** Read the real window, the real trace, and the real files before you tune anything. The first look usually surprises. (04, 06, 08)

## B. Context and memory

**P6. Protect the model's attention.** Wrong context can be worse than missing context, because it gives the model a plausible distraction. Dumping material in is not context engineering. (01, 06)

**P7. Manage context with four moves, each with a cost.** Select (what goes in, and where it sits), compress (lossy, and itself a model call), write (park it on disk), isolate (a sub-task in its own window, at a coordination cost). (03, 06)

**P8. Freeze a stable prefix and move only the tail.** Identity, instructions and tools stay fixed so the prompt cache holds; reshuffling early context every turn is correct but slow and costly. (06)

**P9. Compaction is a design surface, not a default.** Choose its trigger and its prompt. A good summary keeps the goal, the locked decisions, progress, key facts, and the next step. (03, 06, 12)

**P10. Never drop overflow blindly.** A head-only cut loses the end of a log. Keep head and tail, or offload the full bytes to a file and pass a reference. A bigger limit is a bigger bucket, not a fix. (02, 03, 11)

**P11. Memory is context assembly over time.** Durable stores hold state; a context builder retrieves, ranks, resolves and assembles a slice each turn. Keep the four types apart: working, episodic, semantic, procedural. (04)

**P12. Conflicts are state problems, not retrieval problems.** Resolve by time: the newer fact becomes current, the older one stays as history. Similarity search alone cannot tell then from now. (04)

**P13. Forgetting is hygiene.** Old items may stay but must not outrank current ones. Every fact needs a date; every procedure needs an owner, a review date, and a deprecation path. (04, 07)

**P14. A bigger window is a bigger desk, not memory.** It will not find the right session, tell which fact is current, or retire a runbook. (04, 06)

## C. Action and boundaries

**P15. The model chooses; the harness decides how, where, and whether.** The model picks a tool and arguments. The harness validates, gates, places, runs, and records the call. (01, 03)

**P16. The prompt states intent; containment lives in the harness.** A boundary must still hold when the instruction fails. "Read-only" in a system prompt is a request. (03, 09, 10)

**P17. Never grant beats deny, and deny beats ask.** Withhold a capability or a secret rather than forbid its use. Infrastructure that never grants is strictly stronger than a rule that denies. (01, 09, 10, 12)

**P18. Start closed.** No network, scoped writes, no credentials by default. Access is earned by configuration, not inherited from the machine. (03, 09)

**P19. Treat model-callable tools like public endpoints.** Keep the list short and the contracts narrow, validate arguments at the boundary, prefer structured choices to free strings, and avoid general escape hatches. (08, 09)

**P20. Choose the cheapest boundary that contains the failure you fear.** Pick the sandbox layer by blast radius. Treat file system and network as a pair, and make the boundary cover child processes. (03, 09)

**P21. Approvals are scarce on purpose.** With good containment, routine work runs freely and approvals mark only boundary-crossing actions. With no approver wired up, a gated call fails closed. (03, 09)

**P22. Authority only narrows as it moves down.** An organisation ceiling, then the role, then the task; each worker gets its own environment (writable for the implementer, read-only for reviewers, no repo for the consolidator). (05, 10)

**P23. Sensitive steps run harness-side.** The harness holds credentials and performs the login or the paid call; the model gets a message that the step is done. (01, 09, 12)

**P24. The harness owns every resource it creates.** Separate model behaviour from storage policy. Harness files live in per-run scratch space, outside the project, deleted at run end on the failure path too. (05, 11)

**P25. A new boundary needs an explicit capability across it, matched to the route the model takes.** Do not widen a root to reach one directory. Give an adapter per tool the model actually uses, rather than an instruction that depends on compliance. (11)

## D. Work, coordination and procedure

**P26. Keep progress outside the model's attention.** Plans, checkpoints, logs, diffs and session records live on disk where people and code can inspect them. (01, 03, 05)

**P27. Hand off through files, not transcripts.** Research writes a findings file, planning writes a plan file, and implementation starts in a fresh window seeded by the plan. Review the plan, where a mistake is cheapest. (06)

**P28. Code owns transitions; models judge inside steps.** Sequencing, joins, caps, gates, retries, failure paths and terminal states are code. A model may decide what kind of task it faces; code decides what happens next. (05, 10)

**P29. Bounds belong in code, not prompts.** Timeouts, attempt limits, cost caps, revision rounds and max steps are enforced by the runtime. Containment without detection still gives most of the value. (05, 10, 12)

**P30. Delegate to buy capacity and isolation, and pay for coordination.** A sub-agent gets a narrower job, context and tool set, and returns its reply, not its transcript. Give every sub-agent the same skill so they do not each invent a process. (01, 03, 06, 07)

**P31. A skill captures the repeatable part of an expert's procedure.** Give it a trigger and a non-trigger, load it progressively, and make one only when the task repeats, the procedure matters, mistakes are expensive, and the right path is not obvious. Eval it against a no-skill baseline; own, prune and deprecate it like code. (07, 03)

**P32. Workers are versioned packages with a hashed effective configuration.** Then any run can be traced to the exact model, instructions, tools and limits that produced it. (05, 10)

**P33. Observation and control are different capabilities.** Seeing a wrong tool call does not let you pause, steer or cancel it; build the control path on purpose. One append-only event stream feeds every view. (03, 05, 10)

## E. Proof

**P34. "Done" is a fact only with receipts.** Tests, builds, exit codes, files and screenshots count; a confident final sentence does not. (01, 03, 12)

**P35. Stop asking the model what it did.** Read the outcome from ground truth (git, the file system, the trace) after the worker exits. Not needing the claim is a higher level of trust than validating it. (10, 12)

**P36. A check is only as strong as what it executes.** A review that only reads files is a reading. An exit code is worth only as much as what the tests load. Require verification to touch the changed files. (10)

**P37. Enforce output contracts.** One machine-readable block per answer, validated against a declared shape; a failed validation is a failed attempt inside a fixed budget. (08, 10)

**P38. Grade with code first.** Compute gold answers with the same deterministic functions the tools use. Keep the LLM judge to a small remit and calibrate it against human labels before you trust it. (08)

**P39. Measure the kind of wrong.** Count confident-wrong answers apart from abstentions, and engineer toward the safe failure. (08)

**P40. Repeat, and compare per task.** Record pass fractions over several runs, report pass@k and pass^k, split by category, and never judge by the aggregate alone. (02, 08, 11)

**P41. Fingerprint every run and rerun on any change.** Harness commit, loop commit, model, configuration, dataset and environment go into each results file. A mismatch means a new baseline. Behaviour can drift from layers you did not touch. (02, 08, 11)

**P42. Instrument while you build.** Traces with tool tiers and empty/error labels cost little at build time and a lot to retrofit. Emit once, send to many sinks. (03, 08, 10)

## F. Evolution

**P43. Failures become infrastructure.** Route each failure class to its proper home: a retrieval rule, a stricter schema, a permission gate, a test, a memory, or a skill. (01, 07)

**P44. Classify the fix before you make it.** A missing fact goes to memory; a plumbing failure goes to the harness; a failure everywhere points at the model. (02)

**P45. Mine clusters, not single slips.** Group failures that share a provable cause and set flaky noise aside, then look at the noise again later. (02)

**P46. Hold out what the fixer never sees.** Keep graders and answer keys away from the editor and fingerprint them. Retire held-out tasks over time, because selection leaks them. (02)

**P47. Accept only improvements that cost nothing elsewhere.** At least as good on held-in and held-out, strictly better on one, checked per task, then confirmed in paired runs against a fresh baseline. (02, 11)

**P48. Declare the editable surface, and widen it from numbers to behaviours.** All green is necessary, not sufficient: ask whether the change fixes the class of failure or one bounded case. (02, 11)

**P49. Every change is explainable, staged, human-merged and reversible.** Boundaries, evidence, isolation and promotion come from the delivery system around the loop; rollback is a normal operation. (02, 11)

**P50. The loop is the easy part.** A scheduler can run the loop, but only engineering makes its evidence trustworthy. The loop exposes missing engineering; it does not remove it. (11)

## Ideology in one paragraph

Assume the model is a capable but unreliable black box you cannot change. Put everything you can make deterministic into code around it: boundaries, bounds, transitions, storage, and proof. Leave the model only the judgment that needs it, and give it the narrowest context, tools and authority that the judgment requires. Make every run inspectable and fingerprinted, so that each failure has an address and each fix can be measured, reviewed and undone. As one line from the IBM talk puts it: "Step one to solving a problem is admitting you have one."

## Where the series disagrees with itself or with the IBM talk

**Inside the series**

1. **How many primitives.** Video 01 builds eleven layers. From video 07 on he counts ten, merging verification/observability and evolution into "proof and learning".
2. **The order of primitives.** Video 01 orders by the request path (context management third, tools fourth, execution environment fifth). Video 03 builds tools before context management, and the sandbox and durable state after skills. Both are defensible; the numbers differ between notes.
3. **Is the loop inside the harness?** Video 01 separates the runtime (agentic loop) from the harness. Video 03 puts the loop inside the harness package (agent = model + harness + UI).
4. **The first self-improvement PR.** Video 02 presents the 4,000 → 12,000 change as the loop's first real success. Video 11 rejects the same PR as a bigger bucket that keeps the structural failure. The acceptance rule of video 02 was therefore not sufficient on its own.
5. **Scratch files.** Video 06 recommends writing scratch and plan files to disk as a context move. Video 11 shows that harness-written files in the workspace leak secrets and contaminate later runs; they need per-run, harness-owned scratch space.
6. **Fixing by instruction.** Videos 01 and 07 call instructions passive, and video 11 refuses to fix reachability with an instruction because correctness would depend on compliance. Yet both fix loops in video 08 were paragraphs in `AGENTS.md`, and they worked. The reconciling rule is P44: missing knowledge suits instructions or memory; plumbing does not.
7. **Self-grading.** Video 02 separates the proposer from the patient and the grader from the editor. Video 08 lets the same local model judge its own answers, accepted only after hand-label calibration (kappa 1.0).
8. **What counts as verified.** Video 03's verifier accepts an exit 0 found in the transcript. Video 10 shows a green `pytest` that never imported the server and moves to deriving results from git and requiring that verification touch changed files.
9. **Revision cap.** Video 05 designs one controlled revision. Video 10 shows that a cap of one ships the final revision unreviewed, and proposes about five rounds or a gate that requires review.
10. **Approval gates.** Video 03 gates every bash call and write. Video 09 argues that frequent approvals cause fatigue and should be kept for boundary-crossing actions once a sandbox is on.
11. **Supervisor agents.** Video 01 treats sub-agents and agents-as-tools as a primitive. Videos 05 and 10 argue that coordination between agents belongs in external code, with a supervisor allowed only inside a step.

**Between the series and the IBM talk (12)**

1. **Prompts.** IBM never edits the prompt and treats prompt changes as the wrong reflex. The series counts instructions as a harness layer, puts prompt edits at the safest rung of Weng's ladder (02), and used `AGENTS.md` edits as its fixes in video 08.
2. **Retry on a failed check.** IBM wraps the loop in up to three whole attempts after a failed verification. Video 10 says a gate failure on fabricated work must stop the run, because a retry or resume replays the same bad result; retries belong to contract failures, and resume beats restart.
3. **Source of truth for verification.** IBM verifies from the trace of tool calls. Video 10 goes one level further: the trace still records the agent's own actions, so derive the outcome from external ground truth (git) where possible.
4. **Who builds the harness.** IBM hopes for agents that generate their own harness before each task. The series changes the harness only inside a declared editable surface, measured on held-out tasks, and merged by a human (02, 11).
5. **Where the harness boundary sits.** IBM includes the model and the loop in the list of harness components. The series (01) keeps the model, the runtime and the harness as three separate words.
6. **Compression.** IBM's compressor keeps the first two messages and the last two and drops the middle, which it admits is naive. The series keeps head and tail with a summary of the middle, and treats compaction as a lossy model call with its own design (03, 06).
