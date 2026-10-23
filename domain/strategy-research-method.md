# Strategy research method — from an idea to real money, and where ideas come from

This note states how practitioners research an options strategy, and how to search for a new
edge, as one method. It merges two research sweeps: six lanes on the research *process*
(7 October, about 210 sources) and five lanes on new SPXW same-day hypotheses (8–9 October, about
157 sources). It is a method, not a list of strategies. Meghav's studies and their findings are
mapped in [strategy-research](strategy-research.md); the harness that automates this method is
[options-research-harness](options-research-harness.md).

**How far to trust it.** Few quotes were checked; the strongest options voices on Reddit are
anonymous; Sinclair, Longmore and Abdelmessih count as one school. Evidence on going live is thin.

## The pipeline in eight stages

![The research pipeline in eight stages](../inbox/2026-10-07-research-pipeline/pipeline.png)

### 1. Find an idea

The most common origin is a **participant who must trade and does not care about the price**:
index funds, call-selling funds, structured-product hedgers, put-selling programmes, retail option
buyers. Next come watching the screen and explaining your own profit and loss. Papers and ratio
screens come after those. Almost no experienced source recommends indicator libraries, retail
videos or ideas a language model generates.

**A ratio tells you where to look, never what to trade.** Abdelmessih reduces a chain to four
comparisons, each set against other assets and against its own history:

- the straddle: implied against realised volatility;
- the vertical spread: skew;
- the strangle: the price of the tails;
- the time spread: term structure.

Traps named by practitioners: high implied volatility alone is no reason to sell; VIX minus
realised is the wrong comparison (compare at-the-money implied with realised); implied volatility
forecasts the *next* period, so compare it with what came after.

Sort every idea at once into a **risk premium** (someone pays for insurance; it can last; trade it
carefully for a long time) or an **inefficiency** (nobody has noticed yet; it ends when others
notice; trade it hard for a short time).

### 2. Write the claim before any test

Before opening data, write:

- **who pays, and why they will keep paying**;
- **where the effect must appear and where it must not** (side predictions you did not tune);
- **the number that ends the idea**, and the cost model and the out-of-sample definition with it;
- **what is unpleasant about the edge** (if nothing is, a larger firm already has it).

For options, state the trade as a relative claim, find the effect before choosing the structure,
and compare it with the simplest alternative that has the same return. Pre-registration works only
with a full analysis plan; registration alone did not reduce p-hacking in a large study.

### 3. Run the cheapest test that could kill it

A backtest holds many arbitrary choices, so a good one proves little. First ask what simple data
would show if the idea were true, and if it were false; plot everything and average by bucket.
Express the edge and the bid-ask width in the same unit: an edge of 0.2 volatility points cannot be
collected through a market 0.5 points wide. Before modelling a trade, **price the window**: compare
the distribution of index moves over the window with what the options implied at its start.

### 4. Build clean data

Use real quotes, never prices rebuilt from VIX and a model. Remove hard errors first: zero bids,
crossed or locked quotes, stale quotes. Match the clock of the option and the index. Take the
forward from the options by put-call parity; it is also a data check. Keep raw data unchanged.
Select strikes only from contracts that existed at the decision time, and keep every expired one.
Distrust a result that is too good: a two-digit Sharpe ratio means suspect the data.

### 5. Run the costed backtest

- **Never fill at mid.** One vendor charges 75% of the spread for one leg, falling to about 53% for four.
- **Count the hedge**, and split the profit by Greek. If you cannot explain it, add nothing.
- **Enter on every qualifying day**, so one start date does not decide the result.
- **Check units.** A published 0DTE study charged the spread at a hundredth of its size; after the
  fix, nothing stayed profitable after costs.
- **Settle on the official print**, not the last bar.
- One-minute bars cannot tell whether a stop or a target was hit first.

Trust the difference between two runs on one engine more than the level of either.

### 6. Try to break the result

- **Neighbours.** A real effect works at nearby settings; one that works at 9:20 and not at 9:30 is luck.
- **Data you have seen is used up.** Any choice made after seeing a result is a fit; a held-back
  sample works once.
- **Count every trial, and count them as independent ones.** Correlated variants are fewer trials
  than they look; trial correction is treated in [options-research-harness](options-research-harness.md).
- **Test where you know the answer**: run the method on simulated prices with no edge, and compare a
  timed rule with random entries of the same count and holding time.
- **Check for future data**: cut the data at a past date and recompute; earlier values must not move.
- **Have someone else read it**, with the pass mark agreed before the held-back data is opened.
- For short-option strategies, **report tails beside the Sharpe ratio**, which flatters rare large losses.

### 7. Paper trade or trade one lot

Compare live results with the backtest **as distributions**, not trade by trade. Replay each live
day through the backtest and explain every gap. Do not tweak after a month live; stop also if live
runs well *above* the backtest.

### 8. Size up, watch, stop

Size follows understanding. Write the stop rule before the first trade, from the strategy's own
expected drawdown. Edges decay, partly because trading them improves the price.
How the desk's bucket test fits stages 3 and 6: [feature-testing](feature-testing.md).

## The research log and the notebook

**Most ideas die.** Reported rates run from nine in ten to 4 survivors of 600, but the lanes found
no solid number; the nine-in-ten figure is one anonymous researcher's. People who last keep a
record of what was tried, on which data, and why it died, grouped by the kind of failure, with a
daily P&L series per dead idea so a new idea can be compared with old ones. A failed idea is not
adjusted until it passes. Measure progress by the growth of the falsified list.

**Notebooks are for exploration and the final report.** Code used twice moves into a tested library;
the notebook calls it and stays linear. Restart and run all before sharing; save an output notebook
per run. Read every line an AI assistant writes: assistants leak future data with no visible sign.

## Where a new edge may come from

The 8 October sweep looked for hypotheses with a mechanism that nobody has tested on SPXW 0DTE.
It found two main places, and no source had tested any of its top eight candidates for profit.

**The clock.** The session holds fixed times when a group must trade or news must arrive: the
closing auction from 15:50 (imbalances published, and every expiring SPXW contract settles on the
official close), the 10:00 releases, the Friday close before the weekend, the third-Friday
settlement open, the last business day of the month. Studies of same-day options often start at
10:00 and stop at 15:40 because spreads are wide, so **the open and the close are untested by
everyone**: literature gaps sit where studies chose not to look.

**The shape of recent moves, not their size.** Implied volatility already follows recent realised
volatility. The literature says the *sign* of recent moves and the share of one *jump* forecast
differently from total volatility.

### The hypothesis card

A hypothesis always has a mechanism: someone forced to trade, or a reason a price is set wrongly,
at a known time. A pattern with no mechanism is not a hypothesis. Each card holds:

1. **Name**; 2. **Mechanism** (who, why, when, and the effect on prices); 3. **Prediction** (one
measurable statement with a sign); 4. **Kill line**; 5. **Data needed**, and whether it is held;
6. **Evidence**, each source labelled (academic, exchange or regulator, fund document, named
practitioner, anonymous, seller); 7. **Already tested?**; 8. **Why it may fail**, the spread included.

### How to search

- **Size a flow from primary documents** (prospectus, holdings filings, index rules), convert it to
  contracts and compare it with daily volume before believing it. Same-day income funds turned out
  tiny against the market.
- **A directional flow reaches a straddle seller only through the hedge**; size it against hedge cost.
- **Re-test any effect transferred from another market or horizon.** Its sign can flip between index
  and single stocks, and a daily result may not hold at 30 minutes.
- **Look for rule and venue breaks** inside the sample as natural experiments (a settlement change,
  a retail rule change).
- **Test any new signal against trailing realised volatility**, which implied volatility already tracks.
- **Fix the event set before opening the data**, write a rival hypothesis into the same test, and
  correct for the number of buckets or windows looked at.
- **Keep a "known and taken" list** of documented effects, and a "what stopped working" list, so
  nobody proposes them as new ([read-first](../inbox/2026-10-08-alpha-search/read-first.md)).
- **Forums are good for mechanisms** from people who quoted the other side, and for disputes that
  point straight at a test. **They are bad for results**: unstated fills, unfinished journals, and
  sellers. Practitioner and seller results are unverified by default.
- **Rare events need years**: twelve third Fridays a year cannot be decided on one year of quotes.
- **A pattern noticed after opening the data uses up that data**; such cards are leads for new days.

## Where practitioners disagree

| Question | One side | Other side |
|---|---|---|
| Reason first, or data first? | Reason first (Harvey, Longmore, Carver) | Data may lead if tested afterwards (López de Prado) |
| Correct for the number of trials? | Always (Bailey, Harvey, López de Prado) | Carver prefers a backtest of every idea ever tried; Hoffstein says a missed edge costs more |
| Is walk-forward out-of-sample? | Yes, with enough data | No: once you edit after seeing it, it is used |
| Paper trading | Run paper beside live first | Trade one lot instead (Sinclair) |
| When do costs enter? | After the effect is understood | Before any backtest; for hedged options they may decide the result |

## Open questions

- Which of the clock candidates can the held year decide, and which need earlier, paid years?
- Who earns in the last 25 minutes? The lanes predict opposite signs; that is the test.
- What is a fair trial count for a family of correlated 0DTE variants: raw, clustered, or by theme?
- No source showed an options research notebook end to end; the notebook advice rests on forums.

## Sources

- [How practitioners research a strategy](../inbox/2026-10-07-research-pipeline/pipeline.md) and its
  lanes: [reddit](../inbox/2026-10-07-research-pipeline/reddit.md),
  [forums](../inbox/2026-10-07-research-pipeline/qse-forums.md),
  [blogs](../inbox/2026-10-07-research-pipeline/blogs.md),
  [papers and tooling](../inbox/2026-10-07-research-pipeline/papers-tooling.md),
  [podcasts](../inbox/2026-10-07-research-pipeline/podcasts.md),
  [YouTube](../inbox/2026-10-07-research-pipeline/youtube.md)
- [New hypotheses for SPXW same-day options](../inbox/2026-10-08-alpha-search/read-first.md) and its
  lanes: [frontier](../inbox/2026-10-08-alpha-search/frontier.md),
  [flows](../inbox/2026-10-08-alpha-search/flows.md),
  [transfer](../inbox/2026-10-08-alpha-search/transfer.md),
  [forums](../inbox/2026-10-08-alpha-search/forums.md),
  [own data](../inbox/2026-10-08-alpha-search/own-data.md)
- [Validation lane](../inbox/2026-10-16-options-harness-research/validation.md),
  [alpha axes](../inbox/2026-10-16-options-harness-research/alpha-axes.md)
