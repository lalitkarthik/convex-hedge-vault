# Handoff: orchestrator for feature #265 (Implied against realised volatility)

**Predecessor:** the planning session (no Herdr on this machine; nothing to close)
**Branch / cwd:** `feature/iv-vs-rv` in `D:\Convex Hedge\Convex-Hedge-Trading-Engine.worktrees\feature-iv-vs-rv`
**State file:** `TMP/feature-loop-iv-vs-rv.json` (create it at Startup)
**Model and flags to use:** `--model opus --effort medium`, started through `cx run`

## Where things are

- Feature issue: #265. Its comment
  https://github.com/bilal-sagar-razak/Convex-Hedge-Trading-Engine/issues/265#issuecomment-6031613330
  holds the `## Implementation plan` and a `## Clarifications for implementers` section that
  binds every ticket; give it to every implementer and reviewer.
- Tickets to build: #266, #267, #268 (wave 1); #269, #271 (wave 2); #270, #272 (wave 3); #273,
  #274 (wave 4). Board page: `Trading-Engine/Tickets/Implied against realised volatility.md`.
- Spec page: `Trading-Engine/Specs/Implied against realised volatility.md` (its Assumptions list
  is also at the end of issue #265). Research, with every formula and its source:
  `Trading-Engine/Research/Implied against realised volatility.md` (long; read section 2.8, 4.5
  and 5 only when a ticket needs them). Decisions: 0073 to 0078 in `Trading-Engine/Decisions/`.

## Done so far

- Planning: grill, research, spec, tickets, waves, approved by the user on 2026-10-07.
- `origin/main` merged into the feature branch on 2026-10-07 and the branch pushed
  (`0acd2e4`), so it starts level with `main`.
- Docker Desktop was started by the planning session just before launch; check it answers
  (`docker info`) before the first test run, and wait for it if it is still starting.

## In progress right now

- Nothing. No worker has been started.

## Not started

- Every ticket. Wave 1 (#266, #267, #268) has no blockers.

## Rules of this repo that replace the feature loop's

This repo is not set up for the feature loop and must stay that way. Use the loop
(`workflow.md`, `prompts/orchestrator.md`) as the engine, and apply these in place of whatever
the loop says on the same point. Where neither covers something, the repo's checked-in
`CLAUDE.md` decides.

1. **No loop files in the repo.** Never run `/feature-loop setup`. `CLAUDE.md` has no
   feature-loop section, so skip Startup's `{{` check. This checkout is a worktree of the
   feature branch and its tree is clean.
2. **Worktrees.** This checkout is itself a worktree, so do not derive the ticket worktree path
   from `git rev-parse --show-toplevel`. Every ticket worktree is
   `D:\Convex Hedge\Convex-Hedge-Trading-Engine.worktrees\ticket-<n>`, on branch
   `ticket/<n>-<ticket slug>` cut from `feature/iv-vs-rv`. The worktrees `ticket-250` and
   `ticket-251` there, and the main checkout `D:\Convex Hedge\Convex-Hedge-Trading-Engine` on
   `feature/zerodha-data-feed`, belong to another feature: never touch them.
3. **Commands** come from the Stack table in `CLAUDE.md`: set up a worktree with `uv sync`;
   type check `uv run mypy src tests`; lint `uv run ruff check . && uv run ruff format --check .`;
   one test file `uv run pytest tests/<path>`; full suite `uv run pytest` (needs Docker running).
   Tickets that touch `frontend/` or the shared sample-messages file (#271, #272, #273) also run
   `pnpm --dir frontend install` once, then `pnpm --dir frontend typecheck`,
   `pnpm --dir frontend lint` and `pnpm --dir frontend test`. `frontend/AGENTS.md` says this
   Next.js version has breaking changes: tell those workers to read it first.
4. **The full suite on this Windows machine** takes 25 to 40 minutes and has about 75 failures
   and 2 errors that come from Windows, not from any ticket: `tests/hosting/test_machine_start_up.py`
   (41), `tests/watchdog/test_watchdog_command.py` (14), `tests/cloud/test_cloud_commands.py` (14),
   `tests/hosting/test_core_has_no_aws.py` (3), `tests/chain/test_history_backup.py` (2 errors),
   plus load-sensitive ones (`tests/chain/test_volatility.py` timing,
   `tests/dashboard/test_dashboard_web.py`). `uv run mypy src tests` reports one error for the
   same reason (`tests/chain/test_history_backup.py`, `os.geteuid`). Run the suite in the
   background with its whole output sent to a file in the temp directory, and judge a run by
   comparing its failures against this list by test file: only a failure outside it, or in the
   ticket's own area, is the ticket's. Tell implementers the same. A
   `tests/dashboard/test_dashboard_web.py` failure is the ticket's own for #271.
5. **Paperwork lives in the vault,** never in `docs/specs/` or a root `CHANGELOG.md`. Wherever
   the loop names `docs/specs/<slug>.md`, use
   `Trading-Engine/Specs/Implied against realised volatility.md`, in the implementer prompt and
   the reviewer prompt as well. Vault pages follow
   `Trading-Engine/Workflow/Rules for writing in this vault.md` (or, if that page is absent, the
   "Documentation rules" of `CLAUDE.md`): plain language, no code, a glossary page and a
   `CONTEXT.md` line for every new term. Two tickets that each add a `CONTEXT.md` line merge by
   keeping both lines.
6. **After every closed ticket** update the board page
   `Trading-Engine/Tickets/Implied against realised volatility.md` (status, a dated note) and
   commit it on the feature branch (`CLAUDE.md`, Phase B, loop step 6).
7. **Parallelism:** as much as the dependency graph allows (the user's standing instruction).
   Start every open ticket the moment all its blockers are closed, whatever its wave number and
   however many implementers are already running; there is no cap. The blocked-by edges already
   keep tickets that share code apart. Do not drop to one because Docker is running: the suite
   needs Docker, so it always is.
8. **Wave 1** runs two tickets inside the chain engine package: #266 owns a new calculation
   module and its tests; #268 owns the history store module and its tests. Neither edits the
   engine's main module. If one reports it must change a module the other owns, run them one
   after the other.
9. **The message shape is the contract.** #267 defines the volatility reading exactly as the
   spec's "The message" and "What is stored" paragraphs list it. #266, #268, #269 and #271 are
   written against that list. If an implementer finds the spec's list cannot be met as written,
   it asks; you answer from the spec and the clarifications comment, and post any new
   clarification on #265 so the other tickets see it.
10. **Secrets.** Sessions on this machine cannot read or edit `.env` or `.env.*` files, the
    example file included. Never try another way round. No ticket needs a broker key.
11. **Finish, in place of the loop's steps 3, 6 and 7:**
    - Docs as `CLAUDE.md` Phase B "Finish" step 1 says: spec page status "implemented, awaiting
      merge"; Guide pages in the product-manual tone (`Guide/The chain engine.md`, which says it
      "publishes six things"; `Guide/The dashboard.md`, whose analytics section counts its pages;
      `Guide/The message bus.md`; `Guide/Settings and secrets.md`; a new page for the IV vs RV
      page if the dashboard page's section would grow too long); an entry at the top of
      `Guide/Changelog.md`; glossary pages for new terms. Commit.
    - The user-flow check runs once, on a replay instance (`config/india-replay.toml`). Walk:
      the sidebar shows "IV vs RV" after "IV Smile"; the page opens for NIFTY and for SENSEX;
      the expiry, rolling-window and sampling controls respond; readings arrive as the replay
      runs. On a fresh history store fewer than five sessions exist, so the expected state is
      "building history" with its count: that is a pass, not a failure. A flow that needs five
      stored sessions or a live broker is `SKIPPED`, not failed; the engine and socket tests
      cover it.
    - Open the PR with a plain-language summary, the ticket list, links to issue #265 and the
      Guide pages, and how it was tested. Repeat the issue's "For review by Bilal before merge"
      list in the PR body. Comment the PR link on #265.
    - **Never merge the PR and never run Phase C.** A person merges. This holds even when
      everything is green.
12. **No attribution.** Commit messages and PR bodies carry no `Co-Authored-By` trailer, no
    "Generated with Claude Code" line and no session link.

## Account rule (the owner's, set 2026-10-04; it replaces every earlier account rule and overrides the skill wherever they differ)

`ACCT` is `node "C:/Users/Acer/AppData/Local/Temp/feature-loop-acct.mjs"`. Use it wherever the
skill says `CX pick`; never run `CX pick` and never pass `--account a`.

- **Accounts:** `b` and `c` only. Never `a`. `max` only when `b` and `c` are both spent.
- **No limit per account:** any number of sessions may run on one account at the same time.
- **Starting a worker** (implementer, fixer, flow checker, your successor):
  `ACC="$(ACCT pick <run-name>)"`. It prints `b`, `c` or `max`, spreading workers over the
  accounts. Then `CX run … --account "$ACC"`.
- **Before every `CX send <name>`:** run `ACCT assign <name>`. It moves that worker's record to
  an allowed, unspent account and prints the account.
- **`ACCT pick` prints `max`:** `b` and `c` are both spent, and the owner allows `max` then.
  The **Usage limit** rule is unchanged: a worker that hits the limit on `max` means every
  account is spent, so take the stop, with the resume command using
  `--account "$(node "C:/Users/Acer/AppData/Local/Temp/feature-loop-acct.mjs" pick <run-name>)"`.
- `ACCT status` shows what runs where.
- Copy this whole "Account rule" section, word for word, into every hand-off you write and into
  your successor's prompt file, so it holds for the rest of the build.

## Parallelism override (the owner's; it overrides the skill wherever they differ)

The one-implementer-while-Docker-runs cap is off for this build: start the whole frontier at once
(the wave rule only). Copy this section, word for word, into every hand-off and successor prompt
you write, next to the Account rule.

## Tier rule (the owner's, set 2026-10-04; it replaces the tier table in workflow.md's Models rule)

The number of areas a ticket touches does not set its tier.

| Tier | Model / effort | The ticket |
| --- | --- | --- |
| `sonnet-high` | Sonnet high | is tightly scoped and leaves no design choice open: the ticket and the spec already say what to build, and the code has a pattern to follow |
| `opus-medium` | Opus medium | everything else |
| `opus-high` | Opus high | leaves a design choice open, or involves concurrency, a data migration, auth or money |

Copy this section into every hand-off and successor prompt you write, next to the Account rule.

## Open questions and problems

- Whether the Indian index level keeps changing between 15:30 and 15:40 is unknown; #269 is asked
  to look at a recorded Indian session and write what it finds on the Architecture page.
- Positional (a 30-day comparison) is out of scope; two questions about it are open with Bilal
  and are recorded in the spec. No ticket depends on them.

## Next action

Startup, from `prompts/orchestrator.md`, for feature #265; then start wave 1 (#266, #267, #268)
together.

## Suggested skills

- `/mattpocock-skills:code-review`, `/mattpocock-skills:resolving-merge-conflicts`
