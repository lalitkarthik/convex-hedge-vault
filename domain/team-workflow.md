# Team workflow — how work is run

How an idea becomes merged, tested work at Convex Hedge and in our repos. Two sources: what the
senior **stated** in the onboarding meetings (`meetings/18-08-26-recap.txt`), and what the repos now
**enforce** (`delta-exchange-payoff/AGENTS.md` and `CLAUDE.md`, and since 2026-10-01
`Convex-Hedge-Trading-Engine/CLAUDE.md`). Where the two
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

## How the trading engine builds a feature

Canon is `Convex-Hedge-Trading-Engine/CLAUDE.md`, with the plain version in
`Trading-Engine/Workflow/How a feature gets built.md`. Every behaviour change goes through three phases.

- **A, plan (with the user):** a `feature/<slug>` branch; grill; research, saved to `Trading-Engine/Research/`;
  grill again; a spec issue labelled `feature` plus a vault spec page; ticket sub-issues labelled `ticket`,
  with native *blocked by* edges; an implementation plan of **waves**, where no two tickets in a wave touch
  the same area; then a handoff.
- **B, build (unattended):** an Opus orchestrator runs at most **three** Opus implementers, each in its own
  worktree on `ticket/<n>-<slug>`. It merges each ticket with `--no-ff`, code-reviews it (two rounds at
  most), runs the typecheck and the full suite, and closes the ticket or parks it `ready-for-human`. At the
  end it writes the Guide pages and the Changelog, then opens **one PR per feature**.
- **C, after the user merges:** every branch of the feature is deleted, locally and on GitHub.
- **Context budget:** a hook warns at 50% and hands off at 60%, to a successor session named `-2`, `-3`.
- **Docs rules:** plain language; every term gets a Glossary page and a `CONTEXT.md` line; the Guide
  describes merged behaviour only; secrets never appear in the docs.

**On this machine** the recipes assume Herdr, `python3` and `jq`. Here `python3` is the Store alias and
`jq` is missing, so we run the same flow without Herdr: the main session orchestrates, and implementers
are Agent calls in worktrees, capped at two while the stack runs.

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

### Headless workers — learned building the Upstox feed and the research lanes (1–8 October)

- **A headless `claude -p` worker ends when it stops replying.** One that starts its tests in the
  background and waits is cut off mid-ticket. Its prompt says: run every command in the foreground,
  never end the turn to wait, and leave the full suite to the orchestrator after the merge.
- **A skill can lead the prompt.** `/mattpocock-skills:implement` as the first words of a headless
  worker's prompt loads the skill on the Pro accounts.
- **Account budget, measured.** A Pro account lasts about an hour of Opus implementer work, then
  five hours until reset. Two Opus-high web-reading workers drained one in 12 to 50 minutes.
  Synthesis-only workers on the max account finished two lanes in about 15 minutes.
- **A worker cut off by the limit usually leaves one complete commit.** Check it (typecheck, lint,
  the ticket's tests), merge, and let the review find what is unfinished, rather than restart.
- **`cx send` resumes on the account in the run record.** A worker cut off on a spent account cannot
  move to another; start a fresh worker pointed at the notes file instead.
- **`cx.mjs` misses "You've hit your session limit"** (its pattern wants "hit your limit"), exits 1
  instead of 10, and leaves the account unmarked. Mark it spent by hand in
  `~/.claude/accounts/state.json` until the script is fixed.
- **Reviews find real faults when told what to attack** — "the worker was cut off, look for anything
  unfinished", "try to make the secret land in the capture". A reviewer that **mutates the code**
  finds what reading does not: 19 of 33 seeded mistakes passed the first test suite on 8 October.
- **A hung pytest holds the worktree's `.venv`**, so `git worktree remove` fails with "Invalid
  argument" on Windows. Look for processes under the worktree path first.
- **Overlapping tickets.** Starting the next ticket before its blocker closed worked when only review
  fixes were pending (bring the fix commits into the new branch). It failed for two tickets that
  edit the same module.
- **Draft the Guide and glossary beside the build** only with a list of every statement that rests
  on unbuilt tickets; a second pass against the finished code found about a dozen of 44 wrong.
- **A wall-clock test is load-sensitive.** In the trading engine,
  `tests/chain/test_volatility.py::test_an_expiry_of_three_hundred_strikes_takes_well_under_a_few_milliseconds`
  failed three runs in six at about 40% CPU. Loosen or mark it before trusting a red run.
- **Background agents die with the session.** Two were lost on an app restart (17 October). Tell a
  long agent to write its report section by section, so partial work survives.
- **Tool gaps on this machine.** `yt-dlp` hits HTTP 429 on many videos; Firecrawl's YouTube scrape
  works. The `/diagram` skill cannot render (no bundle, no browse binary); draw with a repo script
  (matplotlib, Mermaid) and export PNGs with headless Edge (`msedge --headless=new --screenshot`).
- **No route links Claude Code to ChatGPT Go** (no connectors, no API). A ChatGPT Project with the
  vault's Markdown uploaded is the working route.

**Codex's role.** Retired as the implementation route on 2026-09-12, and made the **tutor** on
2026-09-25 ([AGENTS.md](../AGENTS.md)). **Since 2026-09-30 Claude tutors as well as builds**, at the
owner's word.

## Session hygiene

`git pull` at the start; commit and push at the end, in the vault and in the repo. Leave the running
services as `AGENTS.md` says unless the owner asks otherwise, and say which you stopped.

## Related

[design-decisions](design-decisions.md) · [tests-that-prove-nothing](../learning-records/tests-that-prove-nothing.md) ·
[silent-success](../learning-records/silent-success.md) · [product-direction](product-direction.md) ·
[trading-engine](trading-engine.md)
