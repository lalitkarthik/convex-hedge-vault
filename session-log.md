# Session log

Append-only. Newest entry at the bottom. One block per session: what was decided, and what is still open.

<!-- Entry shape:

## 2026-08-19

**Decided:** …
**Open:** …

-->

## 2026-08-21

**Decided:** Breadth-first, then depth. Phase 1 maps the whole terminal; Phase 2 takes one surface
at a time — option chain, structure chain, strategies — with the Greeks as the lens across all
three rather than as a fourth pass. Phase 3 opens teach workspaces only when the jargon stops
making sense.

**Decided:** Teach workspaces split by subject, not by tool. Portable options knowledge (Greeks,
vol, pricing) goes to `D:\second-brain\second-brain\learning\<topic>\`. Convex Hedge's own system
goes to `teach/<topic>/` in this vault.

**Decided:** `payoff-project` stays out of the vault for now. Its existence is noted; what to
promote gets chosen later, by hand.

**Decided:** Access to the terminal is by Google SSO in a browser pane the human signs into.
Read-only throughout — no rerunning, no deleting, no saving.

**Done:** Phase 1 breadth pass over all six surfaces. Wrote [platform-map](domain/platform-map.md)
and seeded [GLOSSARY.md](GLOSSARY.md) with the terminal's vocabulary.

**Open — resolve in the depth passes:**

1. **What is Echo?** A strategy source alongside Registry, with a `NOT VALIDATED` state and an
   external owner. Who or what authors one, and what validation means, is unknown.
2. **Margin does not reconcile.** `expiryday_long_strangle` reports `AVG MARGIN / DAY ₹646` while
   each trade pays roughly ₹75,000 in premium for long options. Long premium is paid in full, so
   ₹646 is not a margin figure that makes sense. Either margin means something specific here, or it
   is wrong.
3. **46% of orders are rejected.** 84 of 182 on that same run. Probably the `min_entry_premium`
   filter refusing entries, but unconfirmed — and if so, a rejected order is a normal outcome
   rather than an error, which changes how the number should be read.
4. **Returns below −100% are a sizing artifact, not a P&L bug.** Per-leg arithmetic checks out
   exactly. The engine sizes 200 lots regardless of the account being exhausted and reports against
   the fixed anchor. Worth knowing which runs are capital-constrained before trusting any headline
   return.
5. **Greeks go blank on far-OTM strikes.** Quotes exist, Greeks show dashes. Presumably the IV
   solve fails below some premium — confirm the threshold and whether it silently affects
   structures built out there.
6. **Premium sign convention is opposite to `payoff-project`.** The terminal shows a long straddle
   as negative net premium; `payoff-project` treats a debit as positive. Confirm the terminal's rule
   before reading any Structure Chain number.
7. **`/oi` never loaded.** GEX and OI both unseen.
8. **MISSION.md is still placeholders.** It should say what this vault is for before it steers
   anything.
9. **Vault root still half-looks like a teach workspace** — `RESOURCES.md`, `NOTES.md`,
   `learning-records/`, `assets/` are files the teach skill expects in *its* directory. Decide
   whether they are vault-level or leftovers.
10. **The `teach` skill is not enabled.** Cached under `mattpocock-skills/skills/productivity/`
    but that group is switched off, so Phase 3 cannot start.

**Depth pass 1 of 6 — option chain.** Wrote [option-chain](domain/option-chain.md).

Cadence confirmed: map all six surfaces first, teach afterwards. Sequential, no parallel agents —
the six screens share one browser session whose asset/date/minute are global, and the surfaces have
a learning dependency order (the structure grid is built out of chain quotes). Teaching will run in
chat rather than through the `teach` skill, but each session still ends with a learning record,
routed by subject: portable options knowledge to `second-brain\learning\`, Convex Hedge's own
system to `teach/` here.

Because teaching now comes after all six passes, session seven should open with retrieval on
surfaces one and two rather than assuming they survived the gap.

Resolved from the depth pass: **#5 is answered in part** — the Greeks blank out because the IV
solve fails, and the deeper cause is that LTP is a last-traded price with no bid/ask, going stale
and non-monotonic on illiquid strikes. The exact rejection rule is still open.

New open questions, chain-specific, listed at the foot of
[option-chain](domain/option-chain.md): the IV-solve rejection rule, how the per-strike IV is
fitted given calls and puts agree exactly, whether the contract multiplier is stored or inferred,
what `VOL` counts, and whether the 414 minutes are a fixed grid.

Worth carrying into the structure-chain pass: the far-expiry forward sat 1,150 points above spot
and was fitted from an 11-strike chain. Row count is the tell for whether a forward can be trusted,
and every structure built at that expiry inherits the doubt.

**Depth passes 2–6, run in one sweep.** Wrote [structure-chain](domain/structure-chain.md),
[volatility](domain/volatility.md), [open-interest](domain/open-interest.md),
[strategies](domain/strategies.md), [backtest-engine](domain/backtest-engine.md). Filled in
[RESOURCES.md](RESOURCES.md) and extended [GLOSSARY.md](GLOSSARY.md).

**Corrected in [platform-map](domain/platform-map.md):** the breadth pass claimed the Structure
Chain FEATURE toggle repaints the grid as any Greek. It does not — only PRICE is built; IV, Δ, Γ,
Ν and ΔOI are disabled placeholders marked "Coming soon". The breadth pass also counted three tabs
on the volatility page where there are two. Both fixed.

**Open questions resolved:**

- **#6, premium sign** — settled. The Structure Chain signs by cashflow: LONG negative, SHORT
  positive. Opposite to `payoff-project`, where a debit is positive.
- **#7, `/oi`** — mapped. Both OI and GEX are fully built.
- **#4, sub-−100% returns** — confirmed a sizing-and-anchor artifact, not a P&L error, with the
  per-leg arithmetic checked exactly.

**Still open and needing a person, not a screen:** #1 Echo, #2 margin per unit, #3 rejected orders,
#8 MISSION.md, #9 vault root layout, #10 the `teach` skill being disabled.

**New, and the most consequential thing found:** some strategy parameters are decorative. On
`daily_straddle_delta_hedged` only `capital` is read; `entry_time`, `exit_time`, `delta_band`,
`tolerance` and `default_dte` display as tunable and are hard-coded in the source, which says so in
its own docstrings. A parameter sweep over those fields would return identical results that look
like a finding. Which other strategies do this is unchecked, and checking it comes before any
parameter study.

**Also new:** the `regime` field is empty on every diagnostics row; margin per unit does not
reconcile between long and short books; the chain reports 414 minutes for a date where the
structure chain and OI report 376.

**Their source code stays theirs.** Strategy pages expose Python. Structure and behaviour are
recorded here in our own words; no code was copied, per [CLAUDE.md](CLAUDE.md).

**Best single teaching artefact found:** the IV vs RV chart. NIFTY constant-maturity 30-DTE IV
against 20-day realised vol shows IV above RV through to late January, then RV crossing above from
mid-February and staying there — the entire case for and against selling premium, in one picture.

**Study session 19 completed, 2026-09-07.** Option-chain data quality: put-call-parity residuals
flagged two mismatched deep-ITM rows, but only by comparison with the chain's residual baseline;
they could not identify which leg was stale. Confirmed the three related screen limits: LTP is a
historical print rather than a current quote, blank IV means a leg has no usable Greeks, and a
one-sided row can simply mean its missing contract never traded. Portable learning record:
`second-brain/learning/option-structures/learning-records/0010-parity-residuals-need-a-baseline.md`.

**Study session 20 completed, 2026-09-08.** IV-surface reading: moneyness is measured from the
selected expiry's forward, not spot. On the live NIFTY surface, the deep 23,000 put wing sat above
previous-close IV (30.3% versus 28.6%), while primary IV was below previous close near ATM. The
curve's shape must therefore be compared by region and against history. Portable learning record:
`second-brain/learning/option-structures/learning-records/0011-moneyness-is-relative-to-forward.md`.

**Study session 21 completed, 2026-09-08.** Open-interest reading: OI is the stock of outstanding
contracts, volume counts trades, and OI change marks net position creation or closure. On NIFTY's
live five-minute view at 09:21:59, the largest positive put OI change was 23,800 and the largest
positive call OI change was 24,000. Neither establishes trade direction: every OI increase creates
a new long and short together. Portable learning record:
`second-brain/learning/option-structures/learning-records/0012-oi-is-paired-position-creation.md`.

**Engine Feed Management shipped, 2026-09-08.** All thirteen tickets of
`delta-exchange-payoff` #33 are on `main` at `9266230` — broker adapters behind a protocol,
canonical events, a connection controller and supervisor, `/health` that reports the feed,
a badge, pause/resume/reconnect, structured logging, ETH recorded, compute that follows the
page, the historical chain and the contract chart. Suite went 576 → **996 passing**, ruff,
`tsc`, web guards and `next build` all clean. Design lives beside the code:
`delta-exchange-payoff/docs/design/hld.md`, `events.md`, and eleven LLDs under
`docs/design/lld/`.

Four defects were found and fixed as their own issues rather than folded in: a null spot
rendered the ladder backwards (#47); the live chain never opened its websocket at all, a
deadlock that passed `tsc` and `next build` (#49); a load-flaky test plus 21 siblings of the
same shape (#50); and #39's own review round, which caught measurement tools silently
reporting full windows they had not observed.

Three numbers were corrected rather than inherited. The BTC feed comment claiming ~600 msg/s
had **never been run** — BTC alone is `measured` 1,095.1 msg/s, BTC+ETH 1,693.6, so ETH costs
+55% and not a doubling. The 7.25 ms fixture solve was wrong by 35% per expiry and 3x on the
pass: live it is `measured` 9.790 ms and a full pass 175 ms, which means the old hot loop
**could not finish inside its own 100 ms tick** and ran at roughly 275 ms and ~64% of a core.
And `reconnect_after` = 45 s survived a `measured` 3,610 s hour by **0.215 s**, which is no
margin at all and is the first thing worth re-measuring.

**Services epic designed, 2026-09-09.** A grilling session over three rounds settled the
split of `delta-exchange-payoff` into four services on a Redis Streams bus — `feed`,
`store`, `api`, `web` — with Redis as a thirty-minute pipe, trimmed by age, no persistence,
and the store replaying from its last flushed minute so the five-minute loss window closes.
Currency lands as two instrument fields and a `-USD` symbol suffix. **No AWS service is
decided**: durable store, compute and region, and Redis hosting are research tickets against
five ordered criteria — invariants, ops burden, cost at 1x and 10x, path to OMS and NSE,
latency — and run after the local split and after cloud access arrives. The spec is
`delta-exchange-payoff` **#57**, mirrored at `docs/design/cloud/epic.md`; sixteen tickets
**#58–#73** in dependency order, R1 naming first, I10 staging last. Opus for research,
controller, bus policy and schemas; Sonnet for mechanical work; never Fable on a ticket.
Work runs one ticket at a time, findings mirrored into each issue so he can study the last
while the next runs. Two reversals worth recording: he chose currency *in* the symbol over
my recommendation of fields only, and I had overstated the cost — the canonical string is
derived, never stored, so the blast radius is code and tests, not data. Both servers were
down all session; nothing recorded since 2026-09-09T00:02Z.

**Seven tickets landed, 2026-09-09, second half.** After #57 was published the day ran
research in parallel with the local split, on his reversal of "cloud last" — the
comparisons never needed the Compose stack, only the sizing inputs, and those existed.
Closed in `delta-exchange-payoff`: **#58** naming (`{env}:{event_type}:{VENUE}:{UNDERLYING}`,
envelope flat, JSON `payload`, colon between sections per Redis's own convention — a
correction to the epic's spelling); **#69** Redis as a container beside the services,
persistence off, `noeviction`, 2 GB, MemoryDB rejected because its durability cannot be
turned off; **#67** the bars stay Parquet on S3 Standard compacted nightly — Timescale is
not on RDS and Timestream LiveAnalytics is closed to new customers, and uncompacted the
same reads cost 288x in requests; **#68** ECS on one `m7g.large` in Mumbai, host networking,
no NAT gateway — inbound market data through a NAT would cost more than the compute;
**#60** currency fields and the `-USD` symbol suffix, live on the engine; **#61** Redis
Streams behind the bus seam, `DELTA_BUS=redis`, 50 ms batches, `measured` 1,056.4 MiB at
thirty minutes against #58's `derived` 1,051.5. **#59** the controller adopted one rule
from Nautilus — silence past `reconnect_after` now cuts the socket and redials — and stays
open for a six-hour tagged quiet-gap run due 2026-09-09T19:03Z (00:33 IST), PID 28432.
The engine was restarted twice at flush boundaries and lost nothing. A study prompt for
reading a ticket back with ChatGPT is at `delta-exchange-payoff/docs/study-with-chatgpt.md`.
Two things owed: `hld.md` is 219 lines against a 200 bound, and every cloud decision
carries "re-cost after #65" and "measure the network hop once access arrives".

**Codex enters the ticket loop, 2026-09-09 evening.** Implementation moves to Codex;
judgment, review and the gate stay with Claude. A ChatGPT-written routing plan he brought
was checked against `~/.codex/models_cache.json` and largely did not survive: the real
ladder is Astra > Sol > Terra > Luna, Sol is described as a workhorse rather than a scarce
top tier, and Astra — the most capable model on the plan — went unmentioned entirely; its
per-window message figures and several of its citations could not be verified. He chose
Luna at `max` first, Sol medium then Sol high on gate failure, never Astra, which would
empty the window in minutes. His own idea carried the design: Codex writes `rate_limits`
into its session rollout after every turn, so the orchestrator reads the 5-hour and weekly
windows for free and switches wholly to Claude at 92% used *before* dispatching. That
removes the break-even — expected cost becomes `12 − 7p` against a baseline of 12, so the
arrangement is never worse than doing the work on Claude, only better by however often
Codex succeeds. Research tickets stay with Opus: there is no gate for a decision record,
and a plausible-but-wrong conclusion feeds the epic uncaught for days; Codex is used inside
them only to gather evidence read-only. The `learning` label means he learns from the
ticket, not that it is research — an Opus pass writes "What I learned" from the finished
diff, whoever implemented it. The routing lives at `~/.claude/skills/codex-route/`, global
so every repo and every vault created later inherits it; the one per-repo file is a root
`AGENTS.md`, now written for `delta-exchange-payoff`. `measured` against `codex-cli
0.153.4`: `-c model_reasoning_effort=max` does reach the model and the rollout records it,
though the model misreported its own effort as "high" when asked — trust the rollout, not
the answer; `--approve-for-me` cannot be combined with `-s`; Codex refuses to run outside a
trusted git directory. Still `assumed`: that an unattended `workspace-write` run does not
stall on an approval, so the first one is to be watched rather than slept through. Owed:
the repo's `CLAUDE.md` documents `.venv/bin/` and `bun`, neither of which exists on this
machine.
