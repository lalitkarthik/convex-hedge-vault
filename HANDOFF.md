# Handoff — 2026-10-07 (evening)

Two repos are involved: this vault, and `D:\Convex Hedge\convex-hedge-strategy` (`MeghavPradeep/convex-hedge-strategy`).

## Start here

Read [test-plan.md](inbox/2026-10-07-feature-testing/test-plan.md), then get Lalit's yes on its section 3, step 1: Bilal's table (Gap, Pace, variance ratio against straddle and forward returns) on the 127 days already on disk. It needs no new data. Nothing is built yet and nothing is approved.

## In flight

- **Databento download: failed, blocked on Lalit.** He ran it at 21:55. The first request, a free price call, returned `401 auth_authentication_failed`. Verified: `data/databento-ledger.json` is empty, no file was downloaded, nothing was spent. To unblock: check `D:\Convex Hedge\convex-hedge-strategy\.env` holds one line `DATABENTO_API_KEY=<key>` with no quotes or spaces, and that the key is active in the Databento portal. Then run:

  ```bash
  uv run --directory "D:/Convex Hedge/convex-hedge-strategy" --env-file .env --with databento python scripts/databento_download.py 2>&1 | tee "D:/Convex Hedge/convex-hedge-strategy/data/databento-download.log"
  ```

- **`scripts/databento_download.py`** is untracked in the strategy repo, on `main`. Ruff-clean. Its requests to Databento have never succeeded, so treat them as untested. Contract selection was tested offline (`--dry-run`).
- **Feature experiments**: seven proposed, none started. Lalit has not chosen.
- **Strategy repo, not ours**: `notebooks/spxw_hedged_straddle.ipynb` shows as modified (Lalit had it open). PR #24 (theta/vega chart) is Meghav's and open. Issue #28 (ten-day Greek ratios) was opened at 17:26 today; no branch or worktree exists for it.
- **No worker or background script is running.** Accounts a, b and c all read `ok` at 21:56.
- **Carried from the morning handoff, untouched today**: lessons 2 to 16 of the long-gamma teaching (lesson 2 is the breakeven move; list in [plan.md](inbox/2026-10-07-long-gamma-research/plan.md)); the three readings of the skipped-hedge rule on [issue #20](https://github.com/MeghavPradeep/convex-hedge-strategy/issues/20#issuecomment-6032875176); the one-page summary for the seniors.
- **Vault**: `inbox/2026-10-06-iv-vs-rv-research/` is untracked and predates this session. Left alone.

## What changed this session

- `2771a61`: the practitioner research. Six lane reports and [pipeline.md](inbox/2026-10-07-research-pipeline/pipeline.md) with its flowchart; 212 sources.
- This commit: [meeting.md](inbox/2026-10-07-feature-testing/meeting.md), [test-plan.md](inbox/2026-10-07-feature-testing/test-plan.md), [inbox/2026-10-07.md](inbox/2026-10-07.md), today's recap and transcript in `meetings/`, a session-log entry.
- Not pushed, by rule: `sources/07-10-26-sheet.png`, `sources/07-10-26-dashboard.webp`, `sources/07-10-26-images.md` (every number on Bilal's two screenshots).

## Decisions made

- Lalit: download all three data parts without a price check; Claude added one $300 total limit (`--max-usd`). Parts and folders: section 5 of [test-plan.md](inbox/2026-10-07-feature-testing/test-plan.md).
- Claude: new days stay out of `data/SPXW/`. Reason in [inbox/2026-10-07.md](inbox/2026-10-07.md).
- Lalit: the research lanes were finished on the max account from saved notes, with no second reading.
- No comparison of the research with the 7 October hedged straddle study was written.

## Open questions

- **For Bilal**: the points marked *read* in [meeting.md](inbox/2026-10-07-feature-testing/meeting.md), most of all whether IV is read at the start or the end of the window, and whether the straddle is hedged inside the 30 minutes.
- **For Lalit**: the choices in section 1 of test-plan.md are Claude's proposals, none confirmed. Which experiments to build first.
- **Issue #28 against the download.** #28 wants contracts about ten days before expiry; the week-ahead part stops at seven. Decide whether to widen it before paying twice.
- *Assumed:* the 401 is a problem with the key's text or status. Claude cannot read `.env`, so this is not checked.
- *Unchecked:* the cost of the download. The rough guess of under $100 has no quote behind it.
- The YouTube research lane is short: 13 talks of 25 to 30, five by one person.
- Vault canon is still stale ([strategy-research](domain/strategy-research.md) at `4bcf653`); [session-log.md](session-log.md) is over the 200-line bound.

## Traps found

- **A deny rule blocks Claude from any command that names `.env`.** Do not work around it. Lalit starts key-using scripts himself.
- **TaskStop does not kill a waiting script on Windows.** Two "stopped" launchers still fired and tripled the workers on one account. Check `ps` after stopping; make launchers run once.
- **A Bash heredoc holding backticks fails and can leave an empty file**; a worker was started on one. Write prompt files with the file tool.
- **Bilal's 9:17 start is the Indian clock.** SPXW opens at 9:30 New York; the repo's opening reading is 9:35.
- **Rolling one-minute windows overlap by 29 of 30 minutes.** A plain ANOVA on them will look far too significant.

## Read these

1. [test-plan.md](inbox/2026-10-07-feature-testing/test-plan.md) — the test, the features, the order of work, the data.
2. [meeting.md](inbox/2026-10-07-feature-testing/meeting.md) — what the seniors said, with each point marked clear or read.
3. `sources/07-10-26-images.md` — the two screenshots in full (local only).
4. [pipeline.md](inbox/2026-10-07-research-pipeline/pipeline.md) — how practitioners research a strategy.
5. `convex-hedge-strategy/scripts/databento_download.py` — its docstring states what is downloaded and where.
6. Memory notes: `teach-dont-quiz`, `explanation-style-paragraphs-ste`, `taskstop-leaves-the-script-running`, `env-files-are-denied`.
