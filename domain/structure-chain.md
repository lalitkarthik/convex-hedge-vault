# Structure chain — `/structure-chain`

Depth note. Prices a whole family of multi-leg structures at one minute, as a grid rather than a
list. Built entirely out of [option-chain](option-chain.md) quotes, so read that first.

## The two tabs

**Straddle / Strangle.** Rows are strikes, columns are offsets. The cell at row `K`, column `D` is:

> `call(K + D) + put(K − D)`

Verified against the chain at NIFTY 10-APR-2026 10:30 — strike 24,000 call LTP 164.30 plus put LTP
141.75 gives 306.05, exactly the `D=0` cell; and 137.40 + 119.30 = 256.70, exactly the `D=50` cell.
The `D=0` column is therefore a straddle by construction, and every wider column a strangle.

**Ratio Spreads.** Three legs — A, B, C — each independently long or short, defaulting to
long / short / long, which is a butterfly. Call and put axes are configured separately (min, step,
column count) and drawn as two grids, rows being the anchor strike and columns the wing width.

On 2026-09-26 the view showed leg A `1 LONG`, leg B `3 SHORT`, leg C `2 LONG` (NIFTY 10-APR-2026
10:30:59, 13-APR expiry). A cell reconciles exactly with the chain's LTPs. For a call row `K` and
column `d` the legs are `K`, `K + d`, `K + 2d`; for a put row they are `K`, `K − d`, `K − 2d`:

- call, row 24,000, column 250: −1 × 164.30 + 3 × 61.50 − 2 × 18.55 = −16.90
- put, row 24,000, column 250: −1 × 141.75 + 3 × 59.35 − 2 × 24.65 = −13.00

The sign is the LTP cashflow, not P&L, and LTP carries no bid/ask cost.

**The desk's own ratios are a different shape.** Rahul's call ratio (28 September) is two strikes:
buy 1 call at a higher strike, sell 6 at an even higher strike — a short call ratio that is short
vega, gains theta while the market stays below the short strikes, and loses if it runs through them.
Do not read the lab's three-leg `1 / 3 / 2` grid as that trade.

## Grid geometry

Four inputs shape the straddle/strangle grid: **offset min**, **step**, **columns**, **rows ±ATM**.
Columns run from the minimum in steps; rows extend that many strikes either side of the money.
Defaults observed: 0, 50, 5 columns, 10 rows each side — a 21×5 grid.

## Sign and basis

**Direction toggles LONG / SHORT and flips every sign.** A long straddle at 24,000 shows −306.05;
short shows +306.05. The sign is **cashflow**: negative is money out, positive is money in.

**Ratio Spreads keep the same cashflow sign — and colour it.** On the NIFTY 10-APR-2026 10:30:59
ratio grid, negative cells (such as −16.90) are green and positive ones (18.20) neutral. The grid's
label is `CALL NET PRICE · PER UNIT · LTP`. Green is money paid out at the current price, not a
profit and not an edge.

> This is the opposite of `payoff-project`, where Net Premium is positive for a debit. Same number,
> opposite sign. Check which convention you are in before comparing anything.

**SPX prices are mids since September.** By 2026-09-30 the SPX Structure Chain labels prices
**MID ($)**. SPX 25-Sep-2026 09:31: the 7,710 straddle −25.90 = call mid 13.80 + put mid 12.10, and
the D=10 (−17.20) and D=25 (−8.75) cells reconcile to chain mids too. The LTP caveats below are the
NIFTY grid's.

**Basis toggles PER UNIT / PER CONTRACT**, and per-contract is simply per-unit × the multiplier
(306.05 → 19,893.25 at ×65). Nothing else changes.

## What this screen cannot do yet

**The FEATURE selector is not built.** It offers PRICE · IV · Δ · Γ · Ν · ΔOI, but only **PRICE**
works. The other five are marked `cursor-not-allowed` with `title="Coming soon"` in v0.1, on both
tabs.

This matters more than a missing button usually would. The obvious reading of this screen — that it
shows how each structure carries the Greeks — is the reading it does not yet support. It prices
structures; it does not yet expose their risk.

**So the Greeks of a structure have to be built, not read.** Three routes, and they are worth
knowing apart:

1. Add up the per-leg Greeks by hand from [option-chain](option-chain.md), remembering that a short
   leg flips every sign.
2. Compute them independently — which is exactly what `payoff-project` already does. The terminal's
   gap and that project's purpose line up unusually well.
3. Wait for the feature.

Note also that ΔOI, one of the greyed options here, **is** live on
[open-interest](open-interest.md) as an OI-change view. The capability exists; it just is not
wired into this grid.

## Inherited data caveats

Because every cell is a sum of two LTPs, everything true of the chain is true here and less
visible:

- **Stale legs are invisible once summed.** A cell built from a strike that last traded hours ago
  looks exactly like a cell built from two fresh quotes. There is no staleness marker.
- **Wide offsets are the least trustworthy columns.** They reach furthest out of the money, where
  quotes are thinnest — so the far-right of the grid is where prices are worst, and it is also
  where the cheapest-looking structures sit.
- **No bid/ask means no spread.** Nothing on this screen tells you what a structure would actually
  cost to trade. Two legs each crossing a wide spread can turn a printed edge into a loss.

## A reading worth keeping

At 1.8 DTE the cheapest straddle sat at **24,050** (303.15) rather than at 24,000 (306.05), though
24,000 is nearer the forward of 24,021.96. Minimum premium and nearest-the-forward are not the same
strike — skew and stale quotes both push them apart.

## Snapshot count differs from the chain

The chain reported **414** minutes for 10-APR-2026; this screen reports **376** for the same day,
as does [open-interest](open-interest.md). The chain is counting something the other two are not.
Unresolved — see the open questions.

## Open questions

1. Why 376 minutes here against 414 on the chain, for the same asset and date?
2. Are the FEATURE views unbuilt in the UI only, or is structure-level Greek aggregation missing
   from the engine as well?
3. Does the grid skip a cell when a leg has no quote, or silently price the pair anyway?
4. In Ratio Spreads, what sets leg B's quantity? On 2026-09-26 the view showed 1 / 3 / 2 (A long,
   B short, C long); whether that is a fixed default or a saved choice is not known.
