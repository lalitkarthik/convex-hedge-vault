# Product direction — what Convex Hedge asked for

What the senior asked to be built, promoted from the August meetings and traced to the work that
answers it. **Every ask is *stated*, with its meeting** — none was a signed-off requirement, and the
recaps record that timelines and final requirements stayed unresolved. Raw record: `meetings/`.

## The platform

- **`app.convexhedge.ai` is an in-house backtesting terminal** (since 2026-10-11 at `research.` and
  `lab.convexhedge.ai`; `app.` is now the trading engine), released as a beta with features added
  gradually; one GitHub branch per feature across production and main. The beta excludes a market the
  recap transcribes as "XPX" — meaning unconfirmed. *24-08.* Mapped in [platform-map](platform-map.md).
- **Front end and back end kept apart**: the interface renders, the back end fetches and computes. *19-08.*
- **An authentication page** for the website. *20-08.*
- **A backtesting-engine application**: strategy templates from a user's own logic, trade-by-trade
  review. Participants may own strategies and share income from successful deployments. *24-08.*

## The options maths

| Ask | Meeting | Where it stands |
|---|---|---|
| Implied forward from a put-call-parity regression across strikes; ≥3 valid strikes, direct calculation as fallback | 20-08 | `delta-exchange-payoff` measured four forward methods: `docs/forward.md` |
| A spot/forward toggle on payoff charts | 20-08 | *Not traced* |
| Days to expiry on 375 trading minutes a day and 252 days a year, counting the rest of today | 20-08 | Index options only — crypto trades around the clock. *Not traced* in `payoff-project` |
| Credit, debit and ratio spreads; iron condor and iron fly; spline-smoothed payoff curves | 20-08 | `payoff-project/docs/calculations.md` for what exists |
| IV by Newton-Raphson; review a closed-form method; validate against five-point regression and online calculators | 20-08 | `delta-exchange-payoff` compares four solvers: `docs/implied-vol.md` |
| Compare Black-Scholes on spot against on forward, live | 20-08 | `delta-exchange-payoff/docs/greeks.md` |
| ATM/ITM/OTM classification by distance from the ATM strike | 19-08 | *Not traced* |

## Analytics the senior wants next

- **P&L attribution by Greek** — delta, gamma, theta, vega, vanna — with a Taylor expansion, so a loss
  on a quiet day can be traced to its source. A Taylor-expansion field on the dashboard. *24-08.*
- **An intraday study**: ATM IV from the first to the last of ~375 minutes, ΔIV against Δspot, and a
  regression decomposition — then productise it as a back end, estimated at two to three days. *24-08.*
- **An interactive payoff view** driven by time, IV, spot and the Greeks. *24-08.*
- **Live Greeks on every tick for NIFTY, SPX, and possibly Delta Exchange crypto options.** *20-08.*
  **This is the ask [feed-engine](feed-engine.md) answers**, for Delta crypto: our own IV and Greeks,
  computed off the websocket, beside the venue's.
- **Backtest ideas for US markets.** *24-08.*

## How the engine fits the direction

- **The senior's stack is feed, Redis, execution, strategies, a terminal** — separate programs on Redis
  Streams ([what-the-senior-said](../teach/message-bus/what-the-senior-said.md)). The engine's split
  (#57) copies that shape and leaves costed slots for `oms` and `strategy`.
- **Backtests read stored files, never the bus**, so the [bar store](bar-store.md) is what a backtest of
  crypto options would stand on.

## Open questions

- What "XPX" is, and when it joins the beta.
- Whether the terminal's backtests will ever read our Parquet store, or only their own data.
- Who owns the P&L attribution back end, and in which repo.
- Timelines — the 24-08 meeting ended with them unresolved.

## Related

[design-decisions](design-decisions.md) · [team-workflow](team-workflow.md) · [platform-map](platform-map.md) ·
[option-chain](option-chain.md) · [volatility](volatility.md)
