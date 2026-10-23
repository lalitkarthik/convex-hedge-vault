> As of Convex-Hedge-Trading-Engine@06e547fa, 2026-10-23

# Engine dashboard — what the team sees

The screens of the [trading-engine](trading-engine.md), deployed for the team. Canon is
`Trading-Engine/Guide/The dashboard.md`, `Trading-Engine/Guide/Signing in and the Broker page.md`,
`Trading-Engine/Guide/Market roles and access.md` and `Trading-Engine/Architecture/Dashboard
design.md`. Pages with their own Guide page: `The structure builder.md`, `The IV vs RV page.md`,
`Live and History tabs.md`, `Client portfolios.md`. This note maps the screens and says what each
one keeps over time; the Guide holds every detail.

## Where it runs

**One address since 18 October: `trade.convexhedge.ai`**, with one market path each (0153). One
sign-in covers both, and a person with a role on both markets gets a market switch in the header.
Each path is one engine instance on its own machine, with its own dashboard.

| Path | Market | Roots | Machine on (weekdays) | Market open |
|---|---|---|---|---|
| `/india` | India, INR · IST | NIFTY, SENSEX | 08:45–16:15 IST | 09:15–15:40 IST (15:30 before 3 August 2026) |
| `/spxw` | US, USD · ET | SPXW | 09:00–16:15 ET | 09:30–16:15 ET; 0DTE options stop at 16:00, which is 01:30 IST until 1 November 2026, then 02:30 |

- **Earlier addresses, now history.** India opened at `trading.convexhedge.ai` (3 October), then
  `india.convexhedge.ai` and `spxw.convexhedge.ai` (4 October). Both were removed on 18 October.
- **Outside the machine's hours the address answers `503`.** We saw it on `spxw` at 15:14 IST on
  5 October. AWS can also refuse a start: on 19 October SPXW showed 503 until a person started it
  at 09:33 ET. Since then extra start checks run (India 09:13, 09:28, 09:43, 09:58 IST; SPXW 09:12,
  09:27, 09:42 ET). The machines also start on market holidays.
- **A saved view** (since 16 October, 0139). When the machine is up but the bus is empty, for
  example after a Redis restart, the pages show the last saved figures with an amber band and the
  badge MARKET CLOSED · SAVED or SAVED VIEW FROM, never LIVE.
- Laid out for a computer or a tablet. On a narrow page nothing is cut off, but there is no phone
  layout.

## Who gets in — roles (since 18 October, 0151–0155)

**Any Google account may sign in, but only a role lets it in** (deny by default). Each person holds
one role per market on a fixed ladder; each role can do all that the role below it can.

| Role | Adds |
|---|---|
| Viewer | The analysis pages, own Profile, own settings and paper trades |
| Trader | Strategies, strategy details, Portfolios, the Structure builder; may change client portfolios |
| Poweruser | The Broker page (India); pages the dashboard does not name, such as Research |
| Admin | The Admin page. One role for the whole site |

Admins grant roles by email on the **Admin page** (a pending grant until the first sign-in) and can
make **agent accounts** for a coming MCP server. Every role change, broker switch, broker login and
portfolio change goes into an **access record** that only grows. Two first admins sit in the
settings files. Roles live in DynamoDB in the cloud. *History:* from 4 to 18 October only company
Google accounts could sign in; anyone signed in was a viewer, and people on a **control list** were
controllers who could also act.

## The pages

Every page sits in one frame: a thin top strip with the market clock, a sidebar with the person
block at its foot, and a title bar. Since 15 October the chain and chart pages share one **control
strip**: asset, spot with its day change, implied spot with its day change, expiry, DTE in trading
days, FWD (the ATM forward) with its day change, ATM strike, ATM IV and the strike window. It
replaced two lines that also showed both forwards, the discount factor and the strike count.

| Page | Path / code | What it shows | What it keeps over time |
|---|---|---|---|
| **Option chain** | `/`, CHN | Every strike, calls left and puts right. Fourteen columns a side, eight by default (OI, theta, gamma, delta, IV, bid, ask, last). Optional CHG and CHG % from the previous close (since 15 October). | Nothing. A live snapshot. |
| **Spot** | SPT (was *Spot + GEX*, renamed 5 October) | Index candles (1, 5 or 15 min) with R1 (call wall, green), S1 (put wall, red) and the gamma flip (purple) as step lines; GEX, OI and OI CHG as sideways profiles. | **Today minute by minute and the last five sessions in view**; the store keeps 30. The one page that shows a day evolving. |
| **Structure chain** | STC | *Straddle / strangle* grid by strike and offset; *Ratio spreads*, 1 long : 3 short : 2 long by default, with separate call and put grids. Net premium or net Greeks, bought or sold, per unit or per contract. | Nothing. A live snapshot. |
| **Structure builder** | STB (was *Structure editor*, 6–8 October) | Build a multi-leg structure from a chain picker or 34 ready-made shapes; payoff chart and figures; **paper trades** followed on a Trades tab, beside every strategy's live trade, read-only. | Paper trades, kept on the server per person (since 13 October). No order is sent. |
| **IV smile** | SMI | IV across strikes against the ATM forward. A skew grid at 25, 10, 5 and 1 delta (put skew, call skew, risk reversal, butterfly) with slopes. Next expiries and an earlier smile (OPEN by default) are indicators. These replaced the skew tiles and the fixed open and previous-close curves on 8 October. | A smile snapshot every minute for ten sessions. **Skew rank** = percentile of the expiry's own minute readings over a lookback, 5M to 2D, 1D by default. |
| **IV vs RV** | IVR (merged 11 October) | ATM IV against realised volatility since the open and over a rolling window counted in samples; seven RV methods; tiles for gap, pace, move against the straddle, opening gap. | A reading a minute for 30 sessions and a row a day for good. "Building history" until five sessions are stored. |
| **Open Interest** | `/open-interest`, OI (replaced the GEX page, 8 October) | Tabs OI, OI CHANGE and GEX by strike; strike filter (15 a side by default); an expiry checklist added strike by strike. | Open interest by the minute, for the change windows. |
| **Strategies** | STR | One card per strategy instance: status, Daily MTM, running total, sparkline, open legs, age of the last beat. Each opens a details page with a **Live** tab and a **History** tab, which replaced the 1D / 5D curve picker on 6 October. | The trading journal: every day's row, signals, fills and trades. Decision snapshots and the log are kept in memory only. |
| **Portfolios** | PRT (since 6 October) | Client portfolios: named bundles of strategy instances, figures added together. | The same journal, member by member. |
| **Broker** | BRK, India only | Which broker feeds the prices (Fyers, Upstox or Zerodha), who chose it and when, each feed's state and login. A poweruser switches and logs in. | Each switch and login in the access record. |
| **Research** | `/research/`, India | The Research Engine's plug-in pages: backtest runs and the Strategy builder, with the Echo assistant since 22 October. Internal users only. | In the Research Engine, not here. |
| **Admin**, **Profile** | — | Roles and the access record; a person's own settings. | The access record. |

Strategies, Portfolios and the strategy pages are the **Live trading pages**: only the company's
dashboards have them. `config/spxw-sandbox.toml` loads no plug-in, so SPXW shows no Research page.

**The status badge** reads LIVE, DEGRADED, MARKET CLOSED, **DATA IS LATE SINCE** a time, or one of
CONNECTING, RECONNECTING, BUSY, NO ACCESS and the saved-view words. Until 13 October the late state
read **STALE**. Clicking the badge lists every feed.

## The Market Watch pilot (not the team's dashboard)

A separate machine serves invited clients at `app.convexhedge.ai`, from one shared Upstox feed, one
multi-user dashboard and up to 400 open sessions. Clients see the market pages only: no Broker,
Strategies, Portfolios or Research page. Roles do not apply there (`Guide/The Market Watch
pilot.md`).

## What was live on 5 October 2026, 15:09–15:14 IST (history)

Read on the dashboard as it then stood, at `india.convexhedge.ai`.

- **Chains:** NIFTY 06-OCT (244 strikes, 1.07 DTE) and SENSEX 08-OCT (199 strikes, 3.07 DTE).
  One expiry per root, so the smile's *+2 EXPIRIES* and *+3 EXPIRIES* buttons added nothing.
- **Feed:** Fyers selected and connected; Upstox disconnected, with a token valid to 2027-10-04.
- **Strategy:** one instance, `nifty-straddle` (`delta-hedged-straddle`), short 100 lots each of the
  22,550 call and put, entered at 09:17, re-hedged sixteen times by shifting lots between the legs.
- **Skew rank:** *building history (1/20)*. It then took one reading per expiry a day, at 14:30 IST
  or 15:00 ET, and needed twenty; the minute-reading rule replaced it on 8 October.

The readings themselves are in [teach/market-observation](../teach/market-observation/PLAN.md).

## Things that read wrongly at first sight

- **The badge can say late while prices move.** On 5 October it read STALE while Fyers was
  connected: the badge counts every feed, and in India the unselected broker's feed reports
  disconnected. The word is now DATA IS LATE SINCE, and the code (`frontend/src/dashboard/badge.ts`)
  still counts every disconnected feed, so the same reading should recur. *Not re-observed.* Click
  the badge to see each feed.
- **Level colours.** Since 8 October R is green and S red on every page, and levels are chosen by
  the sign of GEX (R1 the call wall, S1 the put wall), so R can sit below the index. *History:* on
  5 October GEX drew resistance green and Spot + GEX drew R1 red; levels stored before 8 October
  used the old rule (by side of the index), so Spot lines can jump there.
- **Risk reversal changed sign on 8 October.** It is now call IV less put IV, and the butterfly is
  half its old size. Older notes and screenshots used the other convention.
- **Implied spot may come from another expiry** than the one on screen: it is the nearest
  expiry's forward.
- **SPXW has no real index level.** No feed sends it, so SPOT shows a dash and the candles follow
  the implied level. SPXW candles on the ATM forward start on 7 October 2026.
- **SPXW open interest is a morning figure**, counted once before the open. Its GEX leaves out
  today's trading, and OI CHANGE offers only PREV. India's is recounted through the day.
- **GEX rests on one assumption** (decision 0050): dealers are long the calls and short the puts.
  It is the dealer-positioning gap [RESOURCES](../RESOURCES.md) lists.
- **History starts when the chain engine first ran.** Candles, levels, smiles and readings are empty
  before that; nothing is filled in from a broker.

## Explained since 5 October

- *The two ATM IVs differed* (13.66% against 13.97%). Since 7 October the strip shows the chain
  engine's own figure read at the forward, the same as the smile page.
- *NIFTY's IV stepped down at the forward* (15.37% at 22,500, 13.29% at 22,550). That step came
  from the regression forward. The ATM forward has no step at the money, and since 15 October it
  is the only forward.
- *DF read 0.9757 for SENSEX at three days.* That was the regression fit's discount factor. Since
  15 October the discount factor is taken as one and the strip no longer shows it.

## Drift found on 2026-10-23

- `Guide/The dashboard.md` opens with "eight pages" and says people on the control list switch the
  broker; the sidebar has nine to eleven entries, and roles replaced the control list on 18 October.
- `Guide/Signing in and the Broker page.md` says the cloud India instance names Fyers and Upstox
  only; the India settings name Zerodha too (decision 0076 Zerodha).
- `Guide/Dashboard plug-ins.md` says no settings file names a plug-in; India's names `research`.
- `Architecture/Dashboard design.md` still lists a login and outside access as open.

## Related

[trading-engine](trading-engine.md) · [engine-strategies](engine-strategies.md) ·
[engine-market-data](engine-market-data.md) · [structure-chain](structure-chain.md) ·
[volatility](volatility.md) · [open-interest](open-interest.md) ·
[strategy-research](strategy-research.md)
