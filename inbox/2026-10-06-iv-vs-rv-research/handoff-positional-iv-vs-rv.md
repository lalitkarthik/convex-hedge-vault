# Handoff — 2026-10-07 — positional IV vs RV (the "over weeks" view)

Repo: `D:\Convex Hedge\Convex-Hedge-Trading-Engine` (GitHub `bilal-sagar-razak/Convex-Hedge-Trading-Engine`). Read its `CLAUDE.md` first; the user's feature loop (`~/.claude/skills/feature-loop/`) drives planning and builds, the repo's rules decide what lands. This file lives in the user's personal vault on purpose: the repo keeps hand-offs out, and the user asked for it not to be in the temp folder.

## Start here

Run `gh pr view 306 --repo bilal-sagar-razak/Convex-Hedge-Trading-Engine --json state,mergeable -q '.state+" "+.mergeable'`.

- `MERGED`: do Phase C of the repo's `CLAUDE.md` for `feature/iv-vs-rv` (worktree `D:\Convex Hedge\Convex-Hedge-Trading-Engine.worktrees\feature-iv-vs-rv`), then start Phase A for the positional feature on a new branch from `main` (suggested slug `iv-vs-rv-positional`).
- `OPEN`: the positional feature depends on what #306 adds (the daily rows below). Branch from `feature/iv-vs-rv`, not `main`, or wait for the merge. If `mergeable` is `CONFLICTING`, merge `origin/main` in; the conflict so far has only ever been `Trading-Engine/Guide/Changelog.md` (keep both rows).

Then ask the user what Bilal said at the meeting on the evening of 7 October about the two open questions below. Planning cannot finish without them.

## In flight

- **PR #306** (`feature/iv-vs-rv`, head `442aff4`): open, mergeable, all four GitHub checks passed. Waiting on Bilal. Never merge it yourself.
- **Worktree** `…worktrees\feature-iv-vs-rv`: clean, pushed. Remove only after the merge.
- **PR #261** (Zerodha data feed) is another feature of the user's, open in the main checkout. Leave it alone.
- **Nothing is running.** The orchestrator ended cleanly at 17:08 on 7 October; the local replay instance is down; ticket worktrees are gone.

## What changed this session

Intraday feature, issue #265, tickets #266 to #274, all closed, in PR #306. Verified on the branch by listing the code, not read line by line:

- Chain engine modules `realised.py`, `readings.py`, `volatility.py`; message `VolatilityReading` (with `ExpiryReading`) on stream `chain.volatility_reading`; settings block `Volatility`.
- History store tables `volatility_minutes` and `implied_minutes` (kept 30 sessions), and **`volatility_days` and `implied_days` (kept for good)**. The daily tables hold, per underlying and day, the session's first, highest, lowest and last level, the opening gap and the session's realised variance; per expiry and day, the morning IV, straddle and level. Check the exact columns in the history module before relying on this list.
- Dashboard page `/iv-rv/` ("IV vs RV", after "IV Smile"); Guide page `Trading-Engine/Guide/The IV vs RV page.md`.
- Vault: research note, spec, ticket board (all named `Implied against realised volatility`), decisions 0073 to 0078.
- Preview with sample numbers, including a mock of the positional view: https://claude.ai/artifact/LrkGwtAoYgkJHWauG7kJKS (private until the user shares it).

Seen running locally on a replay: the page loads, the IV line and tile update each minute, RV shows "Building history: 0 of 5 sessions" as designed. The RV lines have never been seen with real data by anyone; that needs five stored sessions on a live instance.

## Decisions made (reasoning lives at the link)

- Intraday first, positional later: decision 0078; Bilal's message of 7 October ("start with intraday first, then research on the calculation of positional").
- RV is worked out in the chain engine, the dashboard only displays: 0073 (rests on 0034, 0045, 0046, 0047).
- The IV set against RV is the skew's, read at the forward: 0076.
- Part-day RV is scaled by a time-of-day profile, 252 trading days a year: 0075.
- Per-minute rows 30 sessions, daily rows for good: 0077.
- A screen to watch only; NIFTY, SENSEX, SPXW only; no formula review before the build, Bilal reviews the PR: spec page, "Questions and decisions" and Assumptions.
- Workers run on accounts `b` and `c` only, never `a`: the owner's rule in `%TEMP%\feature-loop-account-rule.md`, copied to `launch-pattern/` beside this file (copy it into any orchestrator hand-off).

## What positional needs (settled by the research unless marked)

**Pairing.** N-day IV against N-day RV, same clock on both sides. Two alignments: trailing (RV of the days before each date) and "what followed" (RV shifted back by N so it sits under the IV that forecast it; AlgoTest calls this "Lag RV"). Research note sections 7.1 and 7.3.

**RV on daily candles**, annualised with 252, Yang-Zhang as the default (research note section 2, sources and equation numbers there; simulation in section 5):

```
o = ln(O_i/C_(i-1))   u = ln(H_i/O_i)   d = ln(L_i/O_i)   c = ln(C_i/O_i)   r = o + c

Close-to-close    var = 1/(n-1) * sum (r_i - mean r)^2
Parkinson         var = 1/(4 n ln2) * sum (u_i - d_i)^2
Garman-Klass      var = 1/n * sum [ 0.5 (u_i - d_i)^2 - (2 ln2 - 1) c_i^2 ]
Rogers-Satchell   var = 1/n * sum [ u_i (u_i - c_i) + d_i (d_i - c_i) ]
Yang-Zhang        var = V_o + k V_c + (1-k) V_rs
                  V_o, V_c = sample variances (divisor n-1) of o and c;  V_rs = Rogers-Satchell
                  k = 0.34 / (1.34 + (n+1)/(n-1))
volatility = sqrt(252 * var)
```

Parkinson, Garman-Klass and Rogers-Satchell ignore the overnight gap and read 25% low when a quarter of the movement is overnight. Yang-Zhang needs n of at least 2 and the close before the window. Do not copy the Python `volatility-trading` Yang-Zhang; it reads 5 to 15% high (section 6).

**Constant-maturity IV**, by straight-line blending of total variance between the two expiries either side of the target (section 8.2, checked against the Cboe worked example):

```
s* = sqrt( (1/T*) * [ T1*s1^2*(T2-T*)/(T2-T1) + T2*s2^2*(T*-T1)/(T2-T1) ] )      T1 <= T* <= T2
example: 24 days at 12% and 31 days at 13% -> 30 days at 12.89%
```

No extrapolation: an expiry is needed on each side of the target. The engine counts time in trading days over 252, so blend in that clock and pair "30 days" with 21 sessions of RV.

**How much RV data** (my reasoning from the formulas, told to the user on 7 October, not a sourced finding):

- One point needs the lookback plus one earlier close: 22 daily candles for 30 days, 6 for 7 days.
- A chart of H sessions needs H plus the lookback. A year on screen is about 275 daily candles per underlying.
- IV rank, percentile and the cone use about 250 trading days by convention; two years (about 500 rows per underlying) covers that with a year of chart behind it. Daily candles are tiny, so two years costs nothing to store.
- A 7-day RV on daily candles rests on 5 returns and has a standard error near 32%. Build it from the engine's own one-minute candles instead (5 sessions plus the gaps), which needs no back-fill.
- From the day #306 is deployed, `volatility_days` builds daily candles by itself. Back-fill is only for the days before that.

**How far forward to subscribe for IV** (my reasoning; confirm against the instrument master):

- 7-day figure: this week's and next week's expiry. Feed filter `dte_max` from 7 to about 14.
- 30-day figure: an expiry at or before 30 calendar days and one at or after. With weekly expiries that means out to about 37 days; allow 45 so a holiday-shifted expiry still brackets. India today: `dte_max = 7`. SPXW today: `dte_max = 1`.
- Do not subscribe whole chains that far out. Only the two bracketing expiries are needed, and only a band of strikes round the forward, because the at-the-money IV is read between the two strikes either side of it. The SPXW settings already warn that two expiries can outrun the feed, so the positional feature needs a feed filter of the kind "these expiries, at-the-money band only".
- The IV line starts the day recording starts. Past IV cannot be rebuilt without buying historical option data.

## Open questions

1. **For Bilal: past prices.** Back-fill daily index candles from a broker, or let the store build up? Asked 6 October, not answered.
2. **For Bilal: the longer IV.** Further expiries blended to a constant maturity, or India VIX, or weekly only? Not answered. Worth offering the 7-day version as the cheap first step. India VIX covers NIFTY only, has no feed in the engine, and reads above at-the-money IV because it includes the far strikes.
3. **Not researched:** each broker's historical-candle limits (Fyers fetches option candles only today, Upstox has no candle mode, Zerodha is unmerged); which expiries NSE and BSE list beyond a week; the load of far SPXW expiries.
4. **Calendars:** only NSE and BSE 2026 and Cboe 2026 to 2027 exist, and a missing year stops the engine. A back-fill of earlier years needs earlier calendars or a rule that does not use them.
5. **Session length:** the research assumed 375 minutes; Indian options have closed at 15:40 since 3 August 2026. Ticket #269 was asked to write what a recorded session shows on `Trading-Engine/Architecture/Chain engine design.md`. I have not read what it wrote.
6. **Two at-the-money IVs on one screen:** on the replay the header strip showed 14.96% (nearest strike, live) while the page's tile showed 13.89% (skew at the forward, last closed minute). Unifying them was left out of scope; expect the question.
7. **Small bug seen, not ticketed:** at a narrow width the IV vs RV chart's legend overlaps the chart.

## Traps found

- **The desktop app kills builds.** A `cx run --detach` orchestrator, its workers and the dashboard are children of the Claude desktop app and die when it restarts (it happened at 13:00 on 7 October and cost about 90 minutes). Start the orchestrator under a watchdog outside the app from the first launch: see the memory note `launch-builds-outside-the-desktop-app` and `launch-pattern/feature-loop-orch-watch-iv-vs-rv.mjs` beside this file.
- **Accounts.** `cx status` said `b` was ok while its login had expired; ping an account before relying on it. Leave `cx` routing off: the owner's account script does the picking. Two builds at once drain `b` and `c` in about four hours.
- **Headless research workers** that follow the research skill hand the job to a background agent and exit with nothing written. Tell them to work in the foreground.
- **`pnpm` is not on PATH** in the Bash tool; use `corepack pnpm` inside `frontend/`.
- **Windows-only reds, not regressions:** two frontend tests (`look.test.ts` path separators, the NOTICE text line endings), Prettier on line endings, and about 73 failures and 2 errors in the Python suite (list in the memory note `full-suite-on-this-windows-machine`). GitHub's checks are the clean signal.
- **The feature-loop dashboard serves one project root.** Port 8765 may belong to another build; start a second with `--port 8766`.
- **What worked:** fixing the message shape in the spec first let three foundation tickets run at once; nine tickets closed in about six hours of wall clock. Review sent back #269 twice and #267 and #271 once each.

## Read these, in order

1. `positional-iv-vs-rv-sources.md` (beside this file): the positional findings with every source link. The user may have edited it since I wrote it.
2. Repo vault, `Trading-Engine/Research/Implied against realised volatility.md`: sections 2 (estimators), 7.3 (days to weeks), 8 (which implied figure), "How others have built this" (AlgoTest, Quantsapp, Opstra), "What could not be confirmed".
3. `Trading-Engine/Specs/Implied against realised volatility.md`: "Deliberately left out" and the Assumptions list.
4. AlgoTest's VRP tool, the layout the user wants to follow: https://docs.algotest.in/clicktrade/strategy-builder/vrp-analysis-tool/
5. `launch-pattern/` (beside this file): copies of this build's orchestrator hand-off, its launch prompt, the watchdog script and the owner's account rule, kept here because the originals sit in the temp folder. Use them as the pattern for the next launch, and check `%TEMP%\feature-loop-account-rule.md` for a newer account rule first.
6. The raw research drafts and the simulation script beside this file, only if a formula needs re-checking.
