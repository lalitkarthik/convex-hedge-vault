# Mission: Convex Hedge's trading engine, understood from a trader's seat

## Why

Lalit builds Convex Hedge's engine and will trade on it. The design for its trading half (strategy
worker, order management, risk checks, paper broker) was written fast, reviewed twice, and is about
to change again for per-client accounts. Building the next version well needs the current one
understood completely: every part, why it exists, and what goes wrong in money if it is missing.

## Success looks like

- Given a scenario (a strategy changes its mind, a person trades by hand, the engine restarts
  mid-order), Lalit can say what every book shows and what the engine sends next, **before** reading
  the page, and be right.
- For each part of the design, Lalit can name the trading problem it solves in one sentence.
- Lalit can read a new meeting's asks and say which part of the design each one changes.
- The feed engine underneath (feed, bus, store) is understood well enough to say what a restart of
  each loses.

## Out of scope

- General options theory: Greeks, structures, skew, gamma trading. That is
  `D:\second-brain\second-brain\learning\option-structures\`.
- Writing the design. Claude and Lalit do that in the engine repository; this workspace only studies it.
