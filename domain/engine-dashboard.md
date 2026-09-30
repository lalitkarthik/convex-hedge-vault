> As of Convex-Hedge-Trading-Engine@b47d8ee, 2026-10-01

# Engine dashboard — what the team sees

The screens of the [trading-engine](trading-engine.md). Canon is
`Trading-Engine/Architecture/Dashboard design.md` and `Trading-Engine/Guide/The dashboard.md`.

## How it is built

- A Next.js app in TypeScript, under `frontend/`, **served as static files** by the Python
  `dashboard` part (0019). It uses pnpm and Node 24, and its checks are Vitest and a typecheck.
- The page gets live data over one **websocket** from the part (`ws://…/socket`). The part reads
  the bus and never writes to it. Shared sample socket messages in
  `tests/dashboard/socket-messages.json` are checked by both the Python and the Vitest tests.
- It is reachable **only from the same machine** (`127.0.0.1:8080`) and has **no login**.
- **It copies the look of Convex Hedge's terminal**, which the repo calls "the Backtest engine"
  (0035). It is dark only (0037), in its own font (0036), with amber for anything clickable, green
  calls and red puts. Only in-the-money cells are tinted (0039). Small ▲/▼ **change markers** show
  which way a figure moved (0038).

## Pages today

| Page | What it shows |
|---|---|
| **Option chain** | Every strike of the chosen root and expiry, calls and puts mirrored around the strike. A column picker offers twelve columns, eight by default: OI, bid and ask with sizes, last, IV and delta per strike. The top shows the index level, the implied index level, both forwards, the discount factor, trading-day DTE and ATM IV. ATM follows each expiry's own forward. Rupee figures are grouped in lakh and crore. One status word covers all feeds: LIVE, STALE, CLOSED and so on. |
| **Strategies** | A grid of cards, one per strategy instance. Each shows a status badge, data freshness, total PnL valued live, today's change, a sparkline, open legs and the age of its last beat. Filters are kept in the page address, and a strip on top gives spot and today's PnL per currency. **Rupees and dollars are never added together.** |
| **Strategy details** | Addressed by a query parameter (0044). It has an Overview (PnL figures, cash, open positions, the day's closed trades) beside a **total-PnL curve** in 1D and 5D ranges. Below are signals and fills, where a signal highlights the fills it produced. The **decision snapshot** shows the market data the strategy saw at a chosen beat, narrowed to its legs, with its state card. A *Full chain ↗* link opens the whole snapshot. Then the log. |

## In flight — feature #150, *Dashboard analytics tabs*

These pages live on `feature/dashboard-analytics-tabs`, with tickets #155–#162. They are the same
screens our terminal notes describe, now live:

| Code | Page | Vault note on the terminal's version |
|---|---|---|
| STC | Structure chain: straddle/strangle grid and ratio spreads (1:3:2 by default), price or net Greeks | [structure-chain](structure-chain.md) |
| SMI | IV smile: put IV below the forward, call IV above; tiles for 25Δ skew, risk reversal, butterfly, slope, skew rank | [volatility](volatility.md) |
| GEX | Gamma exposure by strike, with walls and gamma flip | [open-interest](open-interest.md) |
| GXC | Spot + GEX: index candles with the day's levels drawn over them | [open-interest](open-interest.md) |

Decisions on the branch, not yet on `main`:

- **0045** — the structure chain is worked out in the dashboard.
- **0046** — GEX and skew come from the derived data engine.
- **0047** — that engine keeps its history in **SQLite on a named Docker volume**.
- **0048** — every chart uses **Apache ECharts**, and the PnL curve moves to it.
- **0049** — the gamma flip is found from the GEX profile.
- **0050** — GEX is measured **per 1% move, with dealers long calls and short puts**.

The last one is the dealer-positioning assumption [RESOURCES](../RESOURCES.md) lists as a gap.

## Still open (from the design page)

- A login, and reaching the dashboard from outside the machine, such as on AWS. The likely path is
  Next.js's own server.
- Whether several engine instances share one dashboard.
- Later pages: orders, broker positions, margin and balance, and the logs of each part. Logs today
  go only to each container's own output.
- A full history of fills, states and signals that survives a restart. That waits for the database.

## Related

[trading-engine](trading-engine.md) · [engine-strategies](engine-strategies.md) ·
[platform-map](platform-map.md) · [option-chain](option-chain.md)
