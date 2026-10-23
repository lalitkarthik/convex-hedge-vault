> As of Convex-Hedge-Trading-Engine@06e547fa, 2026-10-23

# Trading engine decisions — the map, 0086 to 0156

The successor of [trading-engine-decisions](trading-engine-decisions.md), which maps 0001 to 0085.
It was split off on 2026-10-23 because one map of 156 records would pass this vault's 200-line
bound. **Canon is each record in `Trading-Engine/Decisions/`.** This note gives one row per record
with the gist in a few words.

These records start on 2026-10-10, when the engine became the base of a platform: three products,
two sides, clients, the Research Engine and the cloud accounts. `Architecture/Platform
architecture.md` draws that platform. Records are *accepted* unless the row says otherwise.
**Numbers repeat** here too (0108, 0109, 0129–0134, 0139), because parallel feature branches each
took the next free number. Name a record by number and title.

## The platform plan, 2026-10-10

| # | Decision | Gist |
|---|---|---|
| 0086 | Three products on two sides | Research, Market Watch, Live Trading; in-house and clients |
| 0087 | The Execution Engine repository stays out of the platform | The order path is a later build from scratch inside the engine |
| 0088 | The strategy SDK is a protocol and node graphs are the end state | Python strategies are *legacy*, migrated later |
| 0089 | Market core and Market Watch start as packages inside the Trading Engine | Own repositories at the end of Track 1 |
| 0090 | Each client's market data comes from their own broker login | Zerodha, Upstox, Fyers, then IIFL, then Dhan; static IP only for orders |
| 0091 | Two environments only until clients are live | Internal production and client production |
| 0092 | Three AWS accounts, management, internal and clients | All in Mumbai; two organizational units |
| 0093 | The GitHub organization owns the repositories | `Convex-Hedge-Private-Limited`, free plan |
| 0094 | The web shell is the existing app behind CloudFront with Cognito sign-in | Google or a one-time code; no passwords |
| 0095 | The user session is the unit of scale | About 2% of a core per Market Watch session; settings on the server |
| 0096 | Partner requests go to every broker now | Until approval, each client makes their own broker app |
| 0097 | The pilot comes first, then the accounts move, then tenancy | Changed in part by 0108 (Research in parallel) |

## The Market Watch pilot, 2026-10-10 → 10-16

| # | Decision | Gist |
|---|---|---|
| 0098 | The pilot runs one engine instance per client | 15 invited clients, free, NIFTY and SENSEX. Replaced in effect by 0104 and 0126 |
| 0099 | One address for the pilot with a router in front | `app.convexhedge.ai`, Cognito sign-in, email to instance |
| 0100 | The pilot runs in the clients account behind the existing load balancer | First a t3.2xlarge. Resized by 0108 and 0148 |
| 0101 | Product analytics with PostHog and Clarity from the pilot's first day | Client instances only; typed text masked |
| 0102 | Machine health with Prometheus and Grafana on the pilot machine | Metrics page in every part; five alerts to Discord |
| 0103 | The pilot's invite and remove commands call AWS from the pilot machine | A narrow exception to the laptop-only rule of 0054 |
| 0104 | The pilot's clients share one market data feed while they all use one Upstox token | One bus, feed, chain engine and watchdog; a dashboard each |
| 0108 | The pilot machine is a t3.xlarge | About half the price |
| 0125 | Clients never see a bare error page and the pilot deploys outside market hours | Restarting and busy pages; reconnect with jitter |
| 0126 | The pilot moves to user sessions in one switch | All clients at once after the close; a week's way back |
| 0129 | The pilot market carries every expiry of the next 30 days | At most 3,000 instruments, nearest expiries first |
| 0134 | Pilot clients are signed out at midnight | 00:00 IST, every session ends |
| 0145 | The pilot's privacy policy is a public page on the router | `app.convexhedge.ai/privacy` |

## Track 1, part 1: user sessions in one engine, 2026-10-13 → 10-14

| # | Decision | Gist |
|---|---|---|
| 0120 | A market is one broker account and its keys carry a market prefix | Empty prefix gives today's keys; a Redis user per market |
| 0121 | A market host runs one worker per market for the whole trading day | Feed and chain engine per worker; 08:45 IST start; restart limit |
| 0122 | One multi-user dashboard holds every user session | Session ends 30 min after the last page. Amended 2026-10-14: the strike window is the person's choice |
| 0123 | A person's id is their Cognito id with Google linked at the first sign-in | The router passes the id |
| 0124 | Page settings and paper trades live on the server for each person | SQLite user settings store; idempotency keys |
| 0127 | The history rebuild from a client's own login belongs to the broker key form | Ten days, marked rebuilt; later |

## Products inside one repository, 2026-10-12 → 10-14

| # | Decision | Gist |
|---|---|---|
| 0106 | The Live Trading pages are a plug-in of Market Watch | One page slot; the trading dashboard command fills it |
| 0107 | One image carries a Market Watch export and a company export until the repository split | Two front-end builds in one image |
| 0130 | Dashboard plug-ins are found through an entry point and chosen in the settings file | Refuses to start on a missing or clashing plug-in |
| 0131 | Outside packages come in through reviewed pin lists, and only company packages are trusted | Exact versions; build stops on anything unlisted |
| 0132 | A page package has one mount route in both exports | Such as `/research/` |
| 0133 | The engine version follows its release tag | `engine-` and the date, such as 2026.10.15 |

## The Research track, 2026-10-12 → 10-13

| # | Decision | Gist |
|---|---|---|
| 0108 | The Research track runs in parallel with Track 1 | Backtest on the engine, Research pages, Two hosts |
| 0109 | The Research Engine is a new repository that depends on the Trading engine | SDK and backtest host; the engine never imports it |
| 0110 | Node graphs from the start, in the Oracle's cell format | The two existing graphs run unchanged |
| 0111 | A node graph returns a target position through an intended book | The host fills it and reports real positions back |
| 0112 | The paper adapter lives in the Research Engine and is found through an entry point | Settings name `node-graph` with a graph path |
| 0113 | Backtest periods come from the DTE window and run in parallel with fixed capital | Nothing compounds |
| 0114 | Margin and costs are host-owned, formula in the backtest and broker API in paper | A parity report comes with "Two hosts" |
| 0115 | The backtest reads the Oracle's bars from S3, with real quotes where present | NIFTY first |
| 0116 | A beat sees only earlier data, and a fill lands at the close of a later step | Delay *n* fills at the close of step *t+n−1* |
| 0117 | Node-graph strategies read the ATM forward as their level on every host | No index level in graphs |
| 0118 | No data purchase and no cloud recorder yet | The Oracle's one-minute bars for now |
| 0119 | Fees are booked beside gross profit and loss, and a cost model is opt-in per instance | Net is realised minus fees |

## Dashboard and analytics, 2026-10-11 → 10-17

| # | Decision | Gist |
|---|---|---|
| 0105 | The dashboard uses Neue Montreal for words and Inter for numbers | Both served by the dashboard |
| 0109 | Range methods are shown beside squared returns for comparison | Parkinson, Rogers-Satchell, day range |
| 0128 | The structure builder has its own chain picker | The option chain still picks nothing |
| 0129 | Structure presets return as Sensibull's set | 34 shapes in four groups |
| 0130 | The payoff chart's standard deviation comes from at-the-money volatility and time | Forward × ATM IV × √(year share) |
| 0131 | A rolling window is counted in samples, not minutes | 5 to 200 samples; amends 0074 |
| 0132 | The ATM forward is the only forward | Regression fit retired 2026-10-15; supersedes 0073, 0074, 0084, 0085 |
| 0132 | The Structure Builder opens on a full-page Ready-made gallery | Cards with filters and search |
| 0133 | The chart pages share one toolbar with an indicator picker | Indicators drawn; choices change the maths |
| 0134 | Prices carry the day change from the previous close | Signed amount and percentage |
| 0135 | The previous close travels on the bus as a statistic for the session it serves | Fallback to the history store for an index |
| 0136 | The page frame has one top bar and one control strip | Top-bar part withdrawn 2026-10-15; the control strip stands |
| 0137 | Dashboard text comes from four size tokens with an 11 pixel floor | 11, 12, 14, 20 px |
| 0138 | The dashboard lays itself out by the width of the page area | Wide from 1200 px, medium from 860 px |
| 0139 | Every realised method runs on the sampled candles at the chosen sampling and window | 20-day close-to-close line removed |
| 0139 | The dashboard keeps a saved view of each market | SQLite on the dashboard's disk; shown after Redis loses data |
| 0140 | A rolling window reaches back into the stored sessions | Newest 30 sessions |
| 0141 | The overnight return counts, and the time-of-day profile gets a night bucket | Year stays 252 days |
| 0142 | Garman-Klass and Yang-Zhang join the picker, and a candle's range is widened, not floored | Seven methods |
| 0143 | The close-to-close line is the textbook figure, scaled by samples per year | Never provisional |
| 0144 | The tiles, the gap and the pace follow the toolbar | Worked out in the browser |
| 0156 | The chain engine publishes vanna, volga and charm, and the trading year and ATM strike pick have one definition | Oracle units; not on the strategy card yet |

## Graviton machines, 2026-10-17

| # | Decision | Gist |
|---|---|---|
| 0146 | The engine image holds both processor kinds during the Graviton move, then ARM64 only | One multi-platform tag |
| 0147 | A Graviton move is a machine swap, and the old machine stays stopped for seven days | Snapshot, new machine, copy, move the address |
| 0148 | A machine's size comes from its cost per user | Pilot on t4g.large; India on t4g.xlarge after a replay test |
| 0149 | India and the pilot move first, and the orchestrator does the swaps outside market hours | Never 08:30–16:00 IST on an Indian trading day |

## Access and roles, 2026-10-17 → 10-18

| # | Decision | Gist |
|---|---|---|
| 0150 | The pilot dashboard gets its cloud identity from a keys folder that the machine renews | Every 30 min, read-only to the dashboard |
| 0151 | Each person has one role per market, on a fixed ladder from viewer to admin | Viewer, trader, poweruser; admin for the whole site. Supersedes in part 0055 and 0063 |
| 0152 | Roles live in a DynamoDB table in the internal account, read fresh on every request | No cache; SQLite on a laptop |
| 0153 | Both markets share one address, trade.convexhedge.ai, with a path per market | `/india` and `/spxw`; one sign-in covers both |
| 0154 | Any Google account may sign in, but only a role lets it in | Deny by default |
| 0155 | The access check is ready for agents, and every change is recorded | Agent accounts; an append-only access record |

## Record drift found on 2026-10-23

Some older records changed in effect without a back-link to the record that changed them: 0098
(0104, 0126), 0100 (0108, 0148), 0097 (0108). The new records name what they change.

## Still open (from `Platform architecture.md`)

The control plane's design: how a user session starts, how broker tokens are kept and refreshed,
how a full machine refuses the next session. Market Core's boundary as a package. The regulatory
questions on client data and client orders, which wait for the broker partnerships. Sandboxes and
release gates once clients are live. The Backtest Engine's move to the internal account and the
split of Research into a client product. The move of legacy strategies to node graphs.

## Related

[trading-engine](trading-engine.md) · [trading-engine-decisions](trading-engine-decisions.md) ·
[engine-lineage](engine-lineage.md) · [design-decisions](design-decisions.md)
