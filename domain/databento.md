> As of convex-hedge-strategy@292f816, 2026-10-23

# Databento — where our SPXW option data comes from

Databento is a market-data vendor, not a broker. It is the one source of US option history we
hold, and it is the trading engine's live SPXW feed (see
[engine-market-data](engine-market-data.md)). It does not carry NIFTY or any Indian market, so
every study that rests on it is a US-only result.

## What we take from it

**OPRA `cbbo-1m`** is the main schema: the consolidated best bid and offer across the US option
exchanges, sampled once a minute, with sizes. One-minute consolidated quotes go back to April 2013.
A **definition** file per day maps each `instrument_id` to its strike, expiry, class and multiplier;
without it a quote file cannot be read.

**ES futures `ohlcv-1m`** bars (front month, all hours) are the only data we hold that covers the
nights and the year before our option history.

What is on disk, and where, is listed in the strategy repo's data table
(`convex-hedge-strategy/CLAUDE.md`) and in
[harness-planning-facts](../inbox/2026-10-17-harness-planning-facts.md) section 3. In short: 251
same-day SPXW sessions from 2025-10-01 to 2026-09-30 (249 used — two are half days), 249 days of
week-ahead quotes, and ES bars from April 2024. **Nothing is held for SPXW options from 2024-07-01
to 2025-06-30.** That year was first chosen as the harness's sealed holdout and dropped on
2026-10-17 because it costs money: the harness holds out the trading days after 2026-09-30 instead,
which arrive free (decision 0004; see [options-research-harness](options-research-harness.md)).

## What it costs

**The last twelve months are free on our plan.** Every same-day and definition file inside twelve
months priced at $0.00. Days just older than a year cost about $0.02–0.03 for a same-day file and
about $0.06–0.07 for a week-ahead file; definition files stay free. The whole ledger to 8 October
was $3.44, of which $3.24 was 2.5 years of ES bars.

**Billing is on Databento's own record size**, so the size of our Parquet files says nothing about
the price. Price every request first: the metadata price call is free. The account has a spending
limit; ask the owner before a run that could pass a few dollars.

## How the API behaves

- **A market holiday answers HTTP 422** ("none of the symbols could be resolved"), not an empty
  file. The downloader records it under `no_data`.
- **The free price call can time out with HTTP 504.** It needs the same retry as the download call.
- **2,000 symbols per request** at most.
- **Three requests at once ran three times faster** with no refusal: 0.44 minutes a day against 1.4.
- **A key starts with `db-`.** A key pasted without that prefix fails with 401 on the first call
  (7 October). Keys live in `.env`, which Claude's commands may not name, so Lalit starts any run
  that needs one.

## The downloader

`convex-hedge-strategy/scripts/databento_download.py` prices every request before it makes it,
stops before a dollar cap (`--max-usd`, counted over the whole ledger, so the cap must include what
is already spent), writes each file whole or not at all, never asks for a file twice, and logs
prices to `data/databento-ledger.json`. It has no end-date argument and no estimate-only mode.

**New history goes to `data/history/SPXW/`, never `data/SPXW/`.** The loader lists every day with
a definition file, so older days dropped into `data/SPXW/` would change every 127-day study on its
next rebuild. `CONVEX_STRATEGY_DATA` points the loader at another root.

## Traps

- **Half days break the strategy repo's clock.** `src/convex_strategy/quotes/loader.py` counts every day to 16:00;
  2025-11-28 and 2025-12-24 closed at 13:00. Exclude or handle them before pricing time decay.
- **The files are licensed.** Raw quotes stay local. Do not push them to a public repo — this vault
  is public — and keep rendered pages that embed the data out of it too.
- **Two copies exist.** The strategy repo's Parquet files, and a Backtest-Engine copy built from
  them in that engine's own layout (`D:\Convex Hedge\Backtest-Engine-data-spike\Data\`).

## Open questions

1. The strategy repo's workflow page says market data under `data/` is never committed, yet
   `main` on GitHub holds `data/history/SPXW/`, `data/derived/` and `data/week-ahead/`. Which is
   intended? Is that repo private, and does the licence allow it?
2. What would the 2024-07-01 to 2025-06-30 year cost, if the senior wants more data? The ledger
   suggests about $6 for same-day files and $16 for week-ahead; older days have fewer strikes, so
   this is an estimate only.
3. Where does Indian history come from, given Databento has none?

## Sources

[2026-10-07](../inbox/2026-10-07.md) · [2026-10-08](../inbox/2026-10-08.md) ·
[harness-planning-facts](../inbox/2026-10-17-harness-planning-facts.md) section 3 ·
[feature test plan](../inbox/2026-10-07-feature-testing/test-plan.md)
