# Plan v3 — nine trading workshops

> Vault copy of the nine-workshop syllabus. Progress, predictions and prior versions remain in D:\second-brain\second-brain\learning\option-structures\. Update that study workspace when a session runs.

**Approved 2026-09-28.** This replaces the 25 unfinished sessions in Plan v2 (archived in the second-brain study workspace) with nine deeper workshops. R1, R2, R3 and T1 remain completed; their results and all predictions stay in the existing ledger. The nine workshops cover the same unfinished syllabus. The 28 September WhatsApp discussion changed the **teaching method**, not the list of required topics.

## What counts as learning

The goal is to read an actual options position from a trader's seat: **what am I exposed to; what changes the value; what could overwhelm the expected profit; what can I actually trade to adjust or exit?** For a lab screen, also ask what the displayed number measures and whether it is executable.

Each workshop uses this sequence:

1. **Teach first.** Start with a real meeting trade, chain snapshot, lab run or execution event. Reconstruct the position and the timeline before asking for a judgment. Explain unfamiliar terms with one worked example at a time.
2. **Build the causal story.** Trace legs and quantities, cashflow, expiry payoff, current Greeks, spot path, IV path, time, execution, and the failure path. Distinguish facts visible in a source from a trader's thesis or our inference.
3. **Drive the relevant lab screen.** Read its controls and units, verify at least one displayed value against source legs or a run record, then identify the data or execution limitation.
4. **Discuss freely.** Lalit can interrupt or ask for a simpler explanation. Keep working through the case before moving to a question. Do not open with a recall quiz.
5. **Check application at the end.** Ask only one or two substantial trading-decision questions per workshop, one question per message, after the material has been taught and discussed. Check each committed prediction against real evidence and log it in PREDICTIONS.md. Work old misses into a relevant case; do not restart basic sign or Taylor drills.
6. **Hand off cleanly.** Record what was covered, what Lalit actually demonstrated, any remaining confusion, and the next action. If a workshop spans chats, keep its status in progress rather than counting another session.

Allow roughly **75–100 minutes** where needed; the number of sessions is a syllabus count, not a timer. Session 6 may take longer because it includes a full backtest audit. Source access or a missing live quote never becomes a made-up result: use a saved case, label it, and leave the unsupported conclusion open.

## Starting point and progress

- **Completed:** R1 (leg signs), R2 (Taylor P&L), R3 (expiry clock), T1 (option chain). Do not reteach these as standalone lessons.
- **Next:** workshop 1, continuing R4. P88 correctly identified the expiry breakevens of the $16 straddle. The previous expected-value forecast question was interrupted and remains **unscored**.
- **Standing application gaps:** vertical Greek retention and deriving spread risk from legs (ledger #37 and #43); forward versus spot when interpreting a screen; bid/ask versus LTP; theta measured over unequal time windows. Revisit these only when they affect an actual decision.
- **Do not add to this syllabus:** today's separate Rahul WhatsApp position. Its detailed observations remain in the vault inbox. It is a model for source-led explanation, not a tenth workshop or a required exercise.
- **Keep deferred:** calendars/term structure, competitor comparison, volga/vanna, and the deeper SpotGamma product tour. The dealer-hedging mechanism and GEX literacy already in v2 remain in workshop 7.

## 1 — Expected move, straddle and the first Structure Chain grid

**Absorbs:** R4 + T2 + M1. **Status:** next / R4 in progress.

Teach in this order:

- Start with the 25 September meeting's near-ATM SPX straddle costing about $16. Separate **expiry payoff** (strike ± premium as breakevens, before costs) from **mark-to-market before expiry** (spot, remaining time and IV can all change the exit value).
- Use the expiry's **forward** to locate ATM, then distinguish three numbers that were previously blurred: the straddle debit, the market's implied **one-sigma** move over a specified horizon, and an observed/realised move. They are related, not interchangeable. Under a simple near-normal approximation, the expected absolute move is about 0.8 times one sigma; use the actual option price and model assumptions when precision matters.
- Turn implied volatility and time into a move scale with sigma proportional to IV × square-root-of-time. Explain 1σ/2σ/3σ as model ranges, not promises or automatic trend labels. Ask what changes when the holding period differs from the expiry.
- Drive Structure Chain's straddle/strangle grid: row strike, column offset, leg direction, per-unit versus per-contract units. Rebuild one cell by summing the corresponding option-chain legs. A displayed LTP sum is a reference cashflow, not an executable combined quote.
- Choose between ATM straddle and wider strangle for a stated view: premium paid, distance to expiry profit, theta cost, gamma/vega exposure, and the required move. Align proposed strikes with the chosen move horizon, then compare with historical day and gap behavior if lab data is available.

**Trader decision to work through:** What move and timing would justify paying for this structure, and what would make you close it before expiry?

**Sources:** [structure-chain](../../domain/structure-chain.md), [option-chain](../../domain/option-chain.md), [volatility](../../domain/volatility.md), [25 Sep recap](../../meetings/25-09-26-recap.txt). **Done when:** Lalit can distinguish breakeven from one sigma and use a real grid cell to support a strike choice.

## 2 — Selling premium: verticals, wings and short-gamma carry

**Absorbs:** R5 + S1 + G1 + G3.

Teach in this order:

- Derive a vertical from its two legs: entry debit/credit, expiry payoff zones, width, maximum gain/loss and breakeven. Use the same strike pair to show why the position's Greeks come from what **differs** between the legs; a structure's name alone does not determine its vega or theta.
- Build an iron condor and an iron fly as paired verticals. Show what the protective wings cap, what premium they cost, where the profit zone sits, and how proximity to a short strike changes the trade.
- Treat short gamma as a business of collecting carry while accepting adverse movement. Trace a quiet session, a steady trend and a sudden candle through delta, gamma, theta and IV. Include hedge cost, spread and gap risk; no win-rate argument alone establishes edge.
- Compare the IV paid/received at entry with the movement that actually occurs over the **same holding window**. Explain why implied-minus-realised can be a source of return, why the path and hedging frequency matter, and why a February regime crossover can reverse a historical seller's advantage.
- Revisit the previously missed vertical retention and risk rules in a real two-leg or four-leg choice, including a near-expiry case. Do not ask for a memorised rank list or routine P&L expansion.

**Trader decision to work through:** When is the credit worth the possible loss, and what warning would make you reduce or exit before a short strike is breached?

**Sources:** [volatility](../../domain/volatility.md), [option-chain](../../domain/option-chain.md), [25 Sep recap](../../meetings/25-09-26-recap.txt). **Done when:** Lalit can derive the position's payoff and explain what market path would make short-gamma carry fail.

## 3 — Buying movement and combining two gamma books

**Absorbs:** G2 + G4.

Teach in this order:

- Price the long-gamma trade as a recurring theta expense. Explain why a cheap premium alone does not prove cheap volatility, and why expiry choice changes the balance of gamma against vega.
- Walk one long straddle through a quiet day, a directional move and a whipsaw. Show the changing option delta and what buying/selling the **underlying or futures** to rebalance does to realised trading P&L. Include spreads and hedge frequency.
- Place a limited-risk long-gamma position beside a short-gamma book. Add the two books' Greeks and show why a small overlay may soften a shock while reducing quiet-market carry. Compare **combined P&L paths**, not merely signs at entry.
- Size the overlay against a concrete bad day and a quiet day. Show what would falsify the idea that "either the move pays or decay pays": both books may lose if the option was expensive, the move happens at the wrong time, IV changes adversely, or execution is poor.
- Connect entry timing to the actual remaining decay window. The short position earns only the decay still available to collect; the long position must earn back its premium and costs before its exit.

**Trader decision to work through:** How much long gamma would you buy, and what event would make you stop paying for it?

**Sources:** [25 Sep recap](../../meetings/25-09-26-recap.txt), [volatility](../../domain/volatility.md). **Done when:** Lalit can describe when the overlay improves the whole book and when it worsens it.

## 4 — Reading skew as a changing market price

**Absorbs:** S2 + T3.

Teach in this order:

- Explain IV as the volatility implied by an **option price**, not a direct forecast or a quantity mechanically forced by a spot move. Use a simple quote repricing to show how an option can rise from delta even while its IV falls, or vice versa.
- Read a smile by expiry and forward-relative moneyness. Compare equal strike distance, equal delta and equal premium as **different** comparisons; do not say a wing became richer without naming the coordinate and timestamp.
- Explain why downside puts often command more IV in risky assets and why another asset can have call skew. Treat demand, hedging and inventory as possible mechanisms, not a guaranteed spot-to-IV rule.
- Drive the Volatility tab: select expiry, read the put and call sides, inspect today's curve against the relevant prior-close overlay, and state **which region** changed. Check quote quality before interpreting a deep wing.
- Translate the surface change into a position view: which legs benefit from IV compression/expansion, where delta and time may dominate, and whether the observed change creates an executable opportunity.

**Trader decision to work through:** Is a proposed skew trade based on an observed relative price change, or only on a story about where spot might move?

**Sources:** [volatility](../../domain/volatility.md), [option-chain](../../domain/option-chain.md). **Done when:** Lalit can make a time-matched, moneyness-matched comparison and separate IV P&L from directional P&L.

## 5 — Ratios, butterflies and the Structure Chain ratio grid

**Absorbs:** S3 + S4 + T4.

Teach in this order:

- Build 1:2 and 1:3 ratios leg by leg. Draw expiry payoff regions and identify the favourable zone, the turn, and the exposed wing. Explain why one buy plus three sells is a **four-lot strategy unit**, not a generic four-lot direction.
- Add the third wing for 1:2:1 and 1:3:2 ratio butterflies. Show how the extra long option changes the far-tail shape, margin need, entry cashflow and sensitivity to skew.
- Compare entry payoff with live risk. A ratio can have a promising expiry tent yet be short vega or short gamma today; the signs can change as spot and time move. Verify any claimed Greek flip with the exact legs and scenario Greeks.
- Drive the Structure Chain ratio controls: quantities and long/short for A/B/C, call and put row strikes, spacing columns, feature selector and units. Rebuild one price cell from the option chain. Distinguish cashflow from P&L and LTP from fillable bid/ask.
- Discuss a **re-ratio**: which leg is changed, what new tail is created or removed, fresh cashflow and margin, and what executable exit would realize the intended gain. Do not assume a profitable "exit" just because gamma is positive.
- Compare at least two structures across the same observed skew and choose which actually expresses the view with acceptable tail and execution risk.

**Trader decision to work through:** Where should the bought and sold strikes sit, what could hurt the far wing, and when would you close or reshape the trade?

**Sources:** [structure-chain](../../domain/structure-chain.md), [option-chain](../../domain/option-chain.md), [25 Sep recap](../../meetings/25-09-26-recap.txt). **Done when:** Lalit can explain an entire ratio cell, its scenario risk and its possible exit without treating the displayed price as realised profit.

## 6 — Why a backtest can win while the live trade loses

**Absorbs:** E1 + E2 + E3 + T6. **Longer workshop; keep one session ID if it spans chats.**

Teach in this order:

- Start at the **current L1 book**: bid, ask, size, midpoint, last trade and spread. Reprice a multi-leg entry and exit at plausible sides of the market. Show why midpoint is a reference and why OI cannot substitute for displayed liquidity.
- Reconstruct the meeting's **9.82 stop → 14.9 fill**: trigger, order type, the available quote, price paid and the later revert. Compare market, limit, delayed and confirmation rules for both missed exits and worse fills; no rule removes risk for free.
- Put the same spike inside a one-minute candle. Explain what a once-per-minute decision can miss, what a tick-level live process sees, and how a configurable cadence changes signals, orders and costs.
- Drive the Strategies page's configuration sections and open a specific Backtest Results run. Trace its parameters to actual Daylog, Trades and Diagnostics records; rebuild one strategy from group and instance records rather than trusting only Overview.
- Audit fills, commissions, slippage assumptions, rejections, position sizing, capital and percentage denominators. Separate a model edge from an artefact of execution or sizing. Name any parameter that the platform currently displays but does not apply, using the vault note as the authority.
- Give a decision on whether the run could support paper trading, a revised backtest, or no action yet, and name the **minimum additional evidence** needed.

**Trader decision to work through:** Would this attractive backtest remain attractive after executable fills and the intraminute path are accounted for?

**Sources:** [strategies](../../domain/strategies.md), [backtest-engine](../../domain/backtest-engine.md), [option-chain](../../domain/option-chain.md), [25 Sep recap](../../meetings/25-09-26-recap.txt). **Done when:** Lalit can trace a run end to end and identify which headline result is supported by trade records and which is not.

## 7 — Open interest, GEX and fast-market hedging

**Absorbs:** T5 + E4.

Teach in this order:

- Read OI as outstanding contracts and volume as trades during a period. Walk through paired buy-to-open/sell-to-open, closing and transfer cases. Explain what OI change and PCR show and why they do not reveal who owns the risk.
- Drive Open Interest: strike, expiry, time, OI and OI-change views. Compare a high-OI strike with its live bid/ask so a concentration is not mistaken for liquidity or directional conviction.
- Build a dealer-gamma scenario from an **assumed** dealer position. If dealers are short gamma, trace the underlying hedge after spot rises or falls and why that hedge can reinforce the move; reverse the position and the hedge response changes.
- Read the lab's GEX flip and walls as model outputs. Identify inputs and sign assumptions before using a level; distinguish observed chain/OI data from inferred dealer inventory. A wall is a scenario to monitor, not a promise of support or resistance.
- Apply the mechanism to the meeting's SPX fast-move-and-revert discussion. Include 0DTE exposure, order withdrawal and other possible causes, and specify what actual flow/quote evidence would support or weaken the dealer explanation.

**Trader decision to work through:** What would you do differently near a claimed gamma level, and what observation would invalidate that use of it?

**Sources:** [open-interest](../../domain/open-interest.md), [25 Sep recap](../../meetings/25-09-26-recap.txt). **Done when:** Lalit can state a dealer-hedging mechanism without presenting inferred positioning as observed fact.

## 8 — Instruments, account risk and the Portfolio tab

**Absorbs:** I1 + I2 + T7.

Teach in this order:

- Compare SPX, NIFTY, Bank NIFTY and BTC on contract unit, multiplier/lot size, strike interval, expiry, market hours, settlement and available liquidity. Use current specifications where available; verify them before numerical sizing.
- Convert a structure's per-unit premium and Greeks into **per strategy unit** money and risk. Distinguish a 1:3 four-lot unit from a four-lot straddle, and show why the same point move has different account impact by instrument.
- Size against maximum loss or a defensible stress loss, drawdown budget and client eligibility. Treat margin as a funding constraint, not the amount the strategy can lose. Work through differently sized client accounts and a smaller second account from the meeting.
- Drive Portfolio: combine backtest runs, read contribution, correlation, concentration and peak margin usage. Check whether an apparently smoother aggregate relies on shared risk, untradeable fills or a misleading size denominator.
- Produce a small allocation table across clients and strategies with units, worst-case/stress loss, funding need and a reason for each allocation.

**Trader decision to work through:** How many complete strategy units can this account hold while surviving the specified bad scenario?

**Sources:** [portfolio](../../domain/portfolio.md), [backtest-engine](../../domain/backtest-engine.md), [25 Sep recap](../../meetings/25-09-26-recap.txt). **Done when:** Lalit can justify an allocation in cash risk rather than just margin or a backtest percentage.

## 9 — Build one trade and replay the 25 September meeting

**Absorbs:** I3 + M2. **Capstone, taught and discussed before any check.**

Teach in this order:

- Walk the 25 September meeting chronologically using its recap and relevant transcript passages. For each trading claim, identify the position or proposed trade, the market view, the exposure, the evidence, and the unresolved assumption. The machine transcript is unreliable in Malayalam stretches; do not turn uncertain wording into a fact.
- Choose one instrument and one strategy already studied. Write the **trading rule**, not just a payoff name: view and invalidation; expiry and strikes; quantity/ratio; entry time and quote condition; hedge rule; profit exit; stop and re-entry; cadence; max account risk; client allocation.
- Map those rules to what the lab can actually configure and backtest. Mark any missing data, inactive parameter or execution feature. Specify the test period, comparison baseline, slippage model and diagnostics needed before trusting performance.
- Run or inspect the closest available backtest, then compare expected and observed behavior. Explain any mismatch by market path, IV, time, quote quality, fills or implementation rather than retrofitting a story.
- Finish by identifying the remaining learning gaps and the next real-data investigation. A gap is recorded as a question to verify, not as a fabricated answer.

**Trader decision to work through:** Would you authorize the trade for a specified client on the evidence available, and what single fact would most change that decision?

**Sources:** [25 Sep recap](../../meetings/25-09-26-recap.txt), [backtest-engine](../../domain/backtest-engine.md), [strategies](../../domain/strategies.md), [portfolio](../../domain/portfolio.md). **Done when:** Lalit can explain the meeting's trading claims and specify a strategy whose entry, risk and exit can be evaluated.

## Coverage check and handoff

| New workshop | Every unfinished v2 ID covered |
|---|---|
| 1 | R4, T2, M1 |
| 2 | R5, S1, G1, G3 |
| 3 | G2, G4 |
| 4 | S2, T3 |
| 5 | S3, S4, T4 |
| 6 | E1, E2, E3, T6 |
| 7 | T5, E4 |
| 8 | I1, I2, T7 |
| 9 | I3, M2 |

**25 of 25 unfinished IDs mapped once.** R1, R2, R3 and T1 remain complete. The prior plan and its dated session notes are in Plan v2 (archived in the second-brain study workspace); prediction history stays in the second-brain prediction ledger. Do not mark a workshop complete because its topics were mentioned: record what Lalit could actually use in a trading decision.
