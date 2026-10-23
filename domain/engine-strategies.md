> As of Convex-Hedge-Trading-Engine@06e547fa, 2026-10-23

# Engine strategies — runtime, the strategy instances, simulated broker, alerts

The strategy half of the [trading-engine](trading-engine.md). Canon is
`Trading-Engine/Architecture/Strategy runtime design.md`, `Simulated broker design.md` and
`Alerter design.md`. `Trading-Engine/Guide/Strategies.md` describes the runtime, there is one Guide
page per strategy, and the settings are in `config/*.toml`. `Guide/Changelog.md` dates each change.

## How a strategy runs

- **Strategy vs strategy instance.** A *strategy* is code in the registry (`strategies/registry.py`).
  An *instance* is one configured copy of it, named in the settings file's `[strategies.<name>]`
  section. **Each instance is its own process and its own Compose service** (0031). One slow instance
  never holds up another.
- **Strategies from packages** (since 13 October). Besides the five built-in names, the registry
  takes any strategy an installed package declares through an entry point. A built-in name wins a
  clash. This is how the Research Engine's **node graphs** run in the sandbox (see below).
- **Beats.** An instance decides only on **round wall-clock times** in its market's time zone, every
  `cadence_seconds`, from 1 s to 60 min (0029). It decides only inside its trading calendar's
  session. A late beat fires once, and missed beats are not made up.
- **The card.** At each beat the runtime reads, all at once, the latest values the strategy
  declares it needs, plus its model account. Those values are the nearest expiry within its
  days-to-expiry range, all strikes or a band, and prices, forwards, IV or Greeks. It hands them to
  the strategy as one **strategy market data card** (0033). Derived values come only from the chain
  engine (0034). The card also carries each held option's latest fill and, since 13 October, an
  **account view**: cash, realised and unrealised PnL, fees and the cost of each position.
- **Which forward.** Until 15 October every card carried the regression forward. Since then it
  carries the **ATM forward**, with IV and Greeks worked out on it, and no strategy's rules or
  settings changed ([engine-market-data](engine-market-data.md)).
- **Stale means silent.** Data is stale when the market is closed, the feed is not connected or is
  silent, or chain data is more than 10 s old. An option without both a bid and an ask counts as
  missing. Then **the strategy is not asked**: its state is marked incomplete with plain reasons, and
  no signal goes out. There is one exception: when the only missing prices are for options it
  *holds*, it is still asked, so a time exit always leaves.
- **Output.** Every beat publishes a **strategy state** and a copy of the card it saw. A change of
  mind publishes a **signal**, which names the **whole target position in lots** with a reason (0030)
  and the mid of each leg at decision time, the *signal price* (0041). **A signal is a target, not an
  order.**
- **Restart.** A saved state lets an instance restarted mid-day carry on. An instance whose model
  account vanished reports its positions as unknown and does nothing until the account returns.
- **Controls** work at any hour, within about a second. **Flatten** closes everything and halts the
  instance until it is resumed or the next day. **Pause** stops entries while exits still run.
  **Resume** undoes both. They are commands, never dashboard buttons.
- **Two settings for backtests** (since 13 October): a **cost model** (a preset, `nifty` or
  `spxw-ibkr`, or one given in full) and a **fill-price policy** (mid, or last trade). Both are off
  by default, and **no sandbox instance names a cost model today**. Since 23 October the `nifty`
  preset charges a flat 0.3% tax on premium and no slippage; before, a fill also gave up 0.1%.

## The strategy instances

| Instance | Strategy (registry name) | Market | Rule, in short |
|---|---|---|---|
| `nifty-straddle` | delta-hedged straddle (`delta-hedged-straddle`) | NIFTY, 1 s beats | At 09:17 IST sells 100 lots of the call and the put at the strike nearest the forward, on the nearest weekly expiry. Skips the day if nothing usable by 09:30. **Band** = expected move ÷ 6, where expected move = entry IV ÷ √252 × forward (about 42 pts at 16% IV and 25,000). When net delta ÷ net gamma is past the band, it trades a synthetic forward at the same strike back to zero delta. Closes at 15:35. No stop, no target, no margin check. |
| `sensex-straddle` (since 7 October) | the same | SENSEX on BSE, 1 s beats | The same rules and 100 lots a side, on SENSEX options. |
| `nifty-graph-strangle`, `nifty-graph-straddle` (since 17 October) | node graph (`node-graph`), from the Research Engine package | NIFTY, 60 s beats, 0–5 days to expiry | The Research Engine's `daily_strangle` and `daily_straddle_delta_hedged` graphs, run by its **paper adapter**: the same graph its backtests run. Each trades a fixed 100 lots a side, enters once a day at the first beat from 09:30 and before 15:00 (since 19 October; before, the 09:30 beat only), and closes by its own rule at 15:00 IST. Set `capital` in place of `lots` to size the day from money. |
| `spxw-straddle-low-iv` | long straddle (`long-straddle-low-iv`) | SPXW 0DTE, 5 s beats | Buys the ATM call and put the first time between 09:45 and 15:00 ET that ATM IV is **5% or lower** (it was 7% until #147; 7% is still the code default). At most once a day. Exits at 75% of cost, at 2× cost, or at 15:30. |
| `spxw-inflow-1000`, `spxw-inflow-1130` | inflow strangle (`inflow-three-three`) | SPXW 0DTE, 60 s beats | `spxw-inflow-1000` enters at **09:59 ET since 1 October** (10:00 before); with its 60 s fill delay it fills at about 10:00. `spxw-inflow-1130` enters at 11:29. Spot = today's forward. Each side sells the OTM strike whose mid is highest at or below ½ × 1.1% × 9% × spot. Buys both back at 1.25× the credit, or at 15:30. After a stop it waits a 2-minute **cooldown counted from the stop signal** (#151), then re-enters at most twice, with stops of 1.3× and then 1.4×. |
| `nifty-strangle` | short strangle (`short-strangle`) | NIFTY | Still in the code, but **no settings file runs it** since 2026-09-30. At 11:00 IST it sold the ≤0.2-delta call and put, stopped at 1.25× a leg or half the credit, and exited at 15:00. On a tie between two strikes it took the one further out of the money; since 18 October it takes the lower, the one at-the-money rule every strategy now shares (0156). |

**Node-graph changes since 17 October** (Research Engine releases pinned in the image):

- 18 October: a sized day starts from the session's first ATM forward, not 09:20; reserve days
  count in trading days; each hedge's margin is checked and a hedge over budget is refused.
- 19 October: exits carry the reason from the rule's name, so a profit target shows as a take profit.
- 23 October: a rule that compares an anchor with no value yet counts as not met and waits.

The Research Engine is a separate project. Its Research pages run on the India dashboard
([engine-dashboard](engine-dashboard.md)).

## The simulated broker

- One per engine instance, started with every profile. It **reads signals in order and never skips
  one** (a consumer group with acknowledgements).
- It brings each instance's **model account** to its target **at once, in full, at the mid price,
  all legs or none** (0032). A fill is marked **stale** when it had to use an older mid or the last
  trade. Under the last-trade policy a recent trade is an ordinary fill.
- **Fill delay** per instance (0040). The inflow strangles wait 60 s and then fill at that moment's
  mid. The others fill at once. A newer request replaces one still waiting, and a waiting request
  survives a restart.
- It keeps positions, cash, and realised and unrealised PnL. With no cost model there are **no fees
  and no slippage**. A cost model moves the fill price by its slippage and charges fees from cash;
  realised PnL stays before fees. Each fill records the bid and ask of that moment, and a stop
  records how far past its trigger it was filled.
- **PnL history** (0043): a point every 10 s while the market is open plus one at the close, five
  days, in Redis. On a laptop it is lost if Redis restarts; the cloud machines keep it across the
  nightly stop with a Redis snapshot.
- **The trading journal** (since 6 October, 0064): one SQLite file that only the simulated broker
  writes. It holds every signal, fill, closed trade and 10 s sample, and a **day row** per instance
  at each close (Daily MTM, running total, high and low). A fill is written there before it is
  published. Missed days are rebuilt at the next start. Samples older than 90 days are thinned to
  one a minute, and a copy is taken after each close. The dashboard's PnL curve, Daily MTM and
  History tab read it.
- **In a stepped run** the Research Engine's backtest host asks the broker to drain: fill every
  signal due at the step's prices, without waiting (`Guide/The stepped engine.md`).
- An option held past expiry is kept and marked **NOT SETTLED**. Settlement is not modelled.
- **Open:** the journal keeps the record if the bus is wiped, but the broker does not yet rebuild a
  model account from it. Until it does, a wiped laptop bus still loses the accounts.

## Discord fill alerts — the alerter

One **fill card per signal**, even with several legs (0042), posted through a webhook. The colour
gives the reason: blue entry, green take profit, red stop loss, grey time exit, orange flatten, and
purple for a HEDGE. Each option shows the signal price beside the fill price, plus the bid and ask
and a warning when the price was old. Below come the credit or debit, the total slippage, and the
position afterwards. Delivery follows Discord's rate limits, retries for about ten minutes, and
never posts a card twice except in the narrow moment after Discord accepts it. A replay posts
nothing. Webhook addresses live only in the environment. `engine alerter test-card` posts a sample
marked TEST. **Open:** warning alerts (which events, and who gets mentioned).

Two other senders are not the alerter. On each cloud machine a **watchdog** (since 3 October)
posts to Discord when a part is down, a feed has not connected by 09:10 or a broker is switched.
Since 11 October Grafana on the operations machine sends machine alerts to an **operations
channel** (`Guide/The watchdog.md`, `Guide/The operations machine and alerts.md`).

## What is not here yet

- **No order leaves the engine.** There is no order management system and no risk management
  system. The sandbox's broker is the only broker.
- No margin model in the engine's runtime (the node graphs check hedge margin themselves), no
  settlement, no per-client accounts. Sizes are **base lots** per instance. Fees exist only through a cost model, which no sandbox instance names.
- These are the gaps `delta-exchange-payoff`'s execution design already worked on:
  [engine-lineage](engine-lineage.md). The repo's newer `Architecture/Platform architecture.md`
  places the products and what comes later.

## Drift found on 2026-10-23

- `config/spxw-sandbox.toml` still says the cooldown counts "from the stop's fill". The code, the
  Guide and the Changelog say from the stop signal (#151).
- `Guide/The SPXW inflow strangle.md` says `spxw-inflow-1000` enters at 10:00. The settings have
  said 09:59 since 1 October (commit `fe283825`).
- `Guide/Strategies.md` lists only the five built-in strategies and the five classic instances. It
  does not name `node-graph` or the two graph instances that the India settings run.
- `config/india-sandbox.toml` says a capital-sized graph "waits for the first forward at or after
  09:20". The Changelog of 18 October says it now sizes from the session's first ATM forward.

## Related

[trading-engine](trading-engine.md) · [engine-market-data](engine-market-data.md) ·
[engine-dashboard](engine-dashboard.md) · [strategies](strategies.md) (the terminal's strategies) ·
[trading-engine-decisions](trading-engine-decisions.md)
