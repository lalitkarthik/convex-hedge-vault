> As of Convex-Hedge-Trading-Engine@59c1083, 2026-10-05

# Engine dashboard — what the team sees

The screens of the [trading-engine](trading-engine.md), now deployed for the team. Canon is
`Trading-Engine/Guide/The dashboard.md`, `Trading-Engine/Guide/Signing in and the Broker page.md`
and `Trading-Engine/Architecture/Dashboard design.md`. This note maps the screens and says what
each one keeps over time; the guide holds every detail.

## Where it runs

| Address | Market | Roots seen | Open when |
|---|---|---|---|
| `india.convexhedge.ai` | India, INR · IST | NIFTY, SENSEX | Indian session, 09:15–15:30 IST |
| `spxw.convexhedge.ai` | US, USD · ET | SPXW | US session, 09:30–16:00 ET (19:00–01:30 IST until 1 November 2026, then an hour later) |

- Each address is one engine instance with its own dashboard. Sign-in is by an authorised Google
  account.
- **Outside its session an address answers `503 Service Temporarily Unavailable`** (seen on
  `spxw` at 15:14 IST on 5 October). Observation has to happen while the market is open.
- The page is laid out for a computer screen. The guide says there is no phone layout.

## The seven pages

Five pages share the top two lines: asset, index level (SPOT), implied index level, units, the
status badge, then expiry, DTE in trading days, both forwards, DF, ATM IV and the strike count.

| Page | Path | What it shows | What it keeps over time |
|---|---|---|---|
| **Option chain** | `/` | Every strike, calls left and puts right. Twelve columns, eight by default: OI, theta, gamma, delta, IV, bid, ask, last. | Nothing. A live snapshot. |
| **Structure chain** | `/structure-chain/` | Two tabs. *Straddle / strangle*: a grid by strike and offset. *Ratio spreads*: three legs, 1 long : 3 short : 2 long by default, separate call and put grids. Either shows net premium or net delta, gamma, vega, theta; bought or sold; per unit or per contract. | Nothing. A live snapshot. |
| **IV smile** | `/smile/` | IV across strikes, put IV below the forward and call IV above. Tiles: 25Δ put skew, risk reversal, butterfly, skew slope, skew rank. | **Today's open curve** (white, dotted) and **yesterday's close curve** (teal, dotted). The **skew rank** takes one reading per expiry a day, at 14:30 IST or 15:00 ET, and needs twenty. |
| **Spot + GEX** | `/spot-gex/` | Index candles (1, 5 or 15 minutes) with the call wall R1 (red), the put wall S1 (green) and the gamma flip (purple) drawn as step lines, and net GEX per strike as sideways amber bars. | **The whole session minute by minute, and the last five sessions.** The one page that shows a day evolving. |
| **GEX** | `/gex/` | Three bars per strike: calls (green), puts (red), net (amber). Lines for R1–R4, S1–S4, the index and the gamma flip. A strip gives NET and FLIP. This expiry or all expiries. | Nothing. A live snapshot. |
| **Strategies** | `/strategies/` | One card per strategy instance: status, total PnL, today's change, a sparkline, open legs, age of the last beat. | Each instance's details page keeps a PnL curve (1D, 5D), the day's signals and fills, and a decision snapshot per beat. |
| **Broker** | `/broker/` | India only. Which broker feeds the prices (Fyers or Upstox), who chose it and when. Only the control list can switch. | — |

## What was live on 5 October 2026, 15:09–15:14 IST

- **Chains:** NIFTY 06-OCT (244 strikes, 1.07 DTE) and SENSEX 08-OCT (199 strikes, 3.07 DTE).
  One expiry per root, so the smile's *+2 EXPIRIES* and *+3 EXPIRIES* buttons add nothing yet.
- **Feed:** Fyers selected and connected; Upstox disconnected, with a token valid to 2027-10-04.
- **Strategy:** one instance, `nifty-straddle` (`delta-hedged-straddle`), short 100 lots each of the
  22,550 call and put, entered at 09:17, re-hedged sixteen times by shifting lots between the legs.
- **Skew rank:** *building history (1/20)*.

The readings themselves are in [teach/market-observation](../teach/market-observation/PLAN.md).

## Things that read wrongly at first sight

- **STALE does not mean the prices are old here.** The badge turns STALE when any feed is
  degraded, stale or disconnected. In India the unselected broker's feed is always disconnected,
  so the badge read STALE while Fyers was connected and prices moved every second. Click the
  badge to see each feed. *This is our reading of the guide's rule against what the page showed.*
- **Level colours swap between the two GEX pages.** On GEX, resistance is green and support red.
  On Spot + GEX, R1 is red and S1 green.
- **The implied index level may come from another expiry** than the one on screen: it is the
  nearest expiry's forward.
- **SPXW has no real index level.** No feed sends it, so SPOT shows a dash and the candles follow
  the implied level.
- **SPXW open interest is a morning figure**, counted once before the open. Its GEX leaves out
  today's trading. India's is recounted through the day (*"Open interest as of 15:10"*).
- **GEX rests on one assumption** (decision 0050): dealers are long the calls and short the puts.
  It is the dealer-positioning gap [RESOURCES](../RESOURCES.md) lists.
- **History starts when the chain engine first ran.** Candles, levels, the open and close curves
  and the skew readings are empty before that.

## Not explained yet

- The summary strip's ATM IV and the smile strip's ATM IV differed at the same moment
  (13.66% against 13.97%).
- NIFTY's IV steps down at the forward: 15.37% at 22,500 and 13.29% at 22,550. The put side and
  the call side do not meet.
- DF read 0.9985–0.9994 for NIFTY at one day and **0.9757 for SENSEX at three days**. A discount
  factor that far from one over three days is not an interest rate.

## Related

[trading-engine](trading-engine.md) · [engine-strategies](engine-strategies.md) ·
[structure-chain](structure-chain.md) · [volatility](volatility.md) ·
[open-interest](open-interest.md) · [strategy-research](strategy-research.md)
