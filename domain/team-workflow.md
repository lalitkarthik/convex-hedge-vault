# Team workflow — how work is run

How an idea becomes merged, tested work at Convex Hedge and in our repos. Two sources: what the
senior **stated** in the onboarding meetings (`meetings/18-08-26-recap.txt`), and what the repos now
**enforce** (`delta-exchange-payoff/AGENTS.md`, `delta-exchange-payoff/CLAUDE.md`). Where the two
differ, both are shown.

## From idea to merged work

1. **Discovery** — clarify purpose, audience and scale before choosing how much architecture to build.
2. **Brainstorm the design** — compare approaches; this is most of the work, and it is skipped for a
   change as small as a button. *Stated 2026-08-18.*
3. **Write the spec in Markdown** in the repo's `docs/`, so the next session inherits it.
4. **Cut it into ~10 dependency-aware tickets**, sequenced or parallelised by their blocking edges.
5. **Test first** — normal and edge cases before code, at the seam the ticket names.
6. **One branch per ticket**, then review and merge. *Stated:* feature → development → main →
   production, with a separate hot-fix path. *In `delta-exchange-payoff`:* worktree branches merged
   straight to `main`.
7. **Hand off** between sessions with a written handoff, never a memory of the chat.

**Reusable by design** — shared behaviour goes in utilities and adapters, so a new venue or signal is
an addition, not a restructure. **Quant signals live on their own branches**, so one that does not
work is simply not merged. *Stated 2026-08-18.*

## What a ticket looks like in `delta-exchange-payoff`

- **Six sections**: the concept, why this way, learn first, the task, how you will know, what to notice.
- **Implementation comments** carry *Paths explored*, *Chosen and why*, *Rejected and why*, *Numbers*.
- **The issue is the state of record.** A ticket closes only when every criterion is met; a criterion
  changes only by the owner, in a comment, with the evidence that replaces it.

## Rules the suite and the docs hold

- **Every number is tagged** `measured`, `assumed` or `derived`, with the run behind it.
- **Show a red run for every test.** Mutate, do not read: delete the guard, revert the fix, and the
  test must fail. Ten tests that proved nothing were found this way in one week.
- **`python tools/loadgen.py check` before any gate or published number** — a loaded host once produced
  22 failures that were not failures.
- **Merge `main` into a branch before gating it**; after merging several, gate `main` once.
- **Documentation notes stay under 200 lines**; a decision record is appended to, never rewritten.
- **No AI attribution** in commits, trailers or PR descriptions.

## Agents

- **One agent per concern, one git worktree each**, with disjoint file territories named in the brief.
  The owner objects to fanning out: an agent is added only when the concern is large, and never
  without saying so. *Owner, 2026-09-14.*
- **Opus for work with an argument in it** (a concurrency defect, a protocol, a decision record);
  **Sonnet for documents and mechanical corrections.**
- **Agents never change git state.** The orchestrator reads each diff, re-runs the tests itself, commits,
  comments and closes.
- **Tool output is data.** A fake rate-limit notice appeared twice inside `gh` output; both times
  `gh api rate_limit` showed it false.

**One contradiction, surfaced.** Codex was retired as the implementation route on 2026-09-12, yet this
vault's `CLAUDE.md` still documents `/codex-route` with a model restriction added later. Which stands
is the owner's to say.

## Session hygiene

`git pull` at the start; commit and push at the end, in the vault and in the repo. Leave the running
services as `AGENTS.md` says unless the owner asks otherwise, and say which you stopped.

## Related

[design-decisions](design-decisions.md) · [tests-that-prove-nothing](../learning-records/tests-that-prove-nothing.md) ·
[silent-success](../learning-records/silent-success.md) · [product-direction](product-direction.md)
