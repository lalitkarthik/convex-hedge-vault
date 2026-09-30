> As of Convex-Hedge-Trading-Engine@b47d8ee, 2026-10-01

# Engine strategies — runtime, the four strategies, simulated broker, alerts

The strategy half of the [trading-engine](trading-engine.md). Canon is
`Trading-Engine/Architecture/Strategy runtime design.md`, `Simulated broker design.md` and
`Alerter design.md`. There is one Guide page per strategy in `Trading-Engine/Guide/`, and the
settings are in `config/*.toml`.

## How a strategy runs

- **Strategy vs strategy instance.** A *strategy* is code in the registry (`strategies/registry.py`).
  An *instance* is one configured copy of it, named in the settings file's `[strategies.<name>]`
  section. **Each instance is its own process and its own Compose service** (0031). One slow instance
  never holds up another.
- **Beats.** An instance decides only on **round wall-clock times** in its market's time zone, every
  `cadence_seconds`, from 1 s to 60 min (0029). It decides only inside its trading calendar's
  session. A late beat fires once, and missed beats are not made up.
- **The card.** At each beat the runtime reads, all at once, the latest values the strategy
  declares it needs, plus its model account. Those values are the nearest expiry within its
  days-to-expiry range, all strikes or a band, and prices, forwards, IV or Greeks. It hands them to
  the strategy as one **strategy market data card** (0033). Derived values come only from the chain
  engine (0034).
- **Stale means silent.** Data is stale when the market is closed, the feed is not connected or is
  silent, or chain data is more than 10 s old. An option without both a bid and an ask counts as
  missing. Then **the strategy is not asked**: its state is marked incomplete with plain reasons, and
  no signal goes out. There is one exception: when the only missing prices are for options it
  *holds*, it is still asked, so a time exit always leaves.
- **Output.** Every beat publishes a **strategy state**. A change of mind publishes a **signal**,
  which names the **whole target position in lots** with a reason (0030) and the mid of each leg at
  decision time, the *signal price* (0041). **A signal is a target, not an order.**
- **Restart.** A saved state lets an instance restarted mid-day carry on. An instance whose model
  account vanished reports its positions as unknown and does nothing until the account returns.
- **Controls** work at any hour, within about a second. **Flatten** closes everything and halts the
  instance until it is resumed or the next day. **Pause** stops entries while exits still run.
  **Resume** undoes both. They are commands, never dashboard buttons.

## The four strategies

| Instance | Strategy (registry name) | Market | Rule, in short |
|---|---|---|---|
| `nifty-straddle` | delta-hedged straddle (`delta-hedged-straddle`) | NIFTY, 1 s beats | At 09:17 IST sells 100 lots of the call and the put at the strike nearest the forward, on the nearest weekly expiry. Skips the day if nothing usable by 09:30. **Band** = expected move ÷ 6, where expected move = entry IV ÷ √252 × forward (about 42 pts at 16% IV and 25,000). When net delta ÷ net gamma is past the band, it trades a synthetic forward at the same strike back to zero delta. Closes at 15:35. No stop, no target, no margin check. |
| `spxw-straddle-low-iv` | long straddle (`long-straddle-low-iv`) | SPXW 0DTE, 5 s beats | Buys the ATM call and put the first time between 09:45 and 15:00 ET that ATM IV is **5% or lower** (it was 7% until #147). At most once a day. Exits at 75% of cost, at 2× cost, or at 15:30. |
| `spxw-inflow-1000`, `spxw-inflow-1130` | inflow strangle (`inflow-three-three`) | SPXW 0DTE, 60 s beats | Enters at 10:00 and at 11:29 ET. Spot = today's forward. Each side sells the OTM strike whose mid is highest at or below ½ × 1.1% × 9% × spot. Buys both back at 1.25× the credit, or at 15:30. After a stop it waits a 2-minute **cooldown counted from the stop signal** (#151), then re-enters at most twice, with stops of 1.3× and then 1.4×. |
| `nifty-strangle` | short strangle (`short_strangle.py`) | NIFTY | Still in the code, but **no settings file runs it** since 2026-09-30. At 11:00 IST it sold the ≤0.2-delta call and put, stopped at 1.25× a leg or half the credit, and exited at 15:00. |

**Drift:** the comment in `config/spxw-sandbox.toml` still says the cooldown counts "from the stop's
fill". The code and the Changelog say from the signal (#151).

## The simulated broker

- One per engine instance, started with every profile. It **reads signals in order and never skips
  one** (a consumer group with acknowledgements).
- It brings each instance's **model account** to its target **at once, in full, at the mid price,
  all legs or none** (0032). A fill is marked **stale** when it had to use an older mid or the last
  trade.
- **Fill delay** per instance (0040). The inflow strangles wait 60 s and then fill at that moment's
  mid. The others fill at once. A newer request replaces one still waiting, and a waiting request
  survives a restart.
- It keeps positions, cash, and realised and unrealised PnL **before charges**. There are no fees
  and no slippage model. Each fill records the bid and ask of that moment, and a stop records how
  far past its trigger it was filled.
- **PnL history** (0043): a point every 10 s while the market is open plus one at the close, five
  days, in Redis. It is lost only if Redis restarts.
- An option held past expiry is kept and marked **NOT SETTLED**. Settlement is not modelled.
- **Open:** keeping accounts safe if the bus is wiped. That waits for the database.

## Discord fill alerts — the alerter

One **fill card per signal**, even with several legs (0042), posted through a webhook. The colour
gives the reason: blue entry, green take profit, red stop loss, grey time exit, orange flatten, and
purple for a HEDGE. Each option shows the signal price beside the fill price, plus the bid and ask
and a warning when the price was old. Below come the credit or debit, the total slippage, and the
position afterwards. Delivery follows Discord's rate limits, retries for about ten minutes, and
never posts a card twice except in the narrow moment after Discord accepts it. A replay posts
nothing. Webhook addresses live only in the environment. `engine alerter test-card` posts a sample
marked TEST. **Open:** warning alerts (which events, and who gets mentioned).

## What is not here yet

- **No order leaves the engine.** There is no order management system and no risk management
  system. The sandbox's broker is the only broker.
- No fees, no margin, no settlement, no per-client accounts. Sizes are **base lots** per instance.
- These are the gaps `delta-exchange-payoff`'s execution design already worked on:
  [engine-lineage](engine-lineage.md).

## Related

[trading-engine](trading-engine.md) · [engine-market-data](engine-market-data.md) ·
[engine-dashboard](engine-dashboard.md) · [strategies](strategies.md) (the terminal's strategies) ·
[trading-engine-decisions](trading-engine-decisions.md)
