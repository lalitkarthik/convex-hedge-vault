# Volatility — `/iv-surface`

Depth note. Two tabs: **Smile** and **IV vs RV**. (The word `VOL` beside the page title is the
page's short name, not a third tab.)

Everything here is fully built — no placeholder controls.

## Smile

Implied volatility plotted across strikes for one expiry at one minute. The x-axis is labelled
twice: by **strike**, and by **offset from the forward**. Measuring moneyness from the forward
rather than spot is the same discipline the [option chain](option-chain.md) applies, and it is what
makes two different expiries comparable at all.

Four comparison curves can be overlaid, all off by default — **prev close**, **day open**,
**prev expiry**, **n-avg** — against the live curve, labelled **primary**. Overlays are how you see
whether today's skew is unusual, which is the only way a smile means anything: a skew is never high
or low on its own, only against its own history.

Observed at NIFTY 10-APR-2026 12:34, front expiry: IV ran from about **18% at the money to ~55% on
the low put wing**, against a spot of 23,998 and a forward of 24,014. That is a steep downside skew
— crash protection is dear, and selling it is what pays for most short-vol books.

## IV vs RV

The most decision-relevant screen on the platform.

It plots **ATM implied volatility** against **realised volatility of the underlying** over a date
range. The gap between the two lines is the variance risk premium — what you are paid for selling
options, or what you overpay for buying them.

**Controls**

| Control | Options |
|---|---|
| Range | start and end date |
| Maturity | `CONST-MAT` · `FRONT` · `USER EXP` |
| Target DTE | a number, e.g. 30 |
| RV estimator | close-close · log return · Parkinson · Garman-Klass · Rogers-Satchell · Yang-Zhang |
| Window | 20 (dropdown) |
| Bar | daily |

Estimators are **checkboxes, not a radio** — several can be drawn at once and compared.

**Constant maturity** holds DTE fixed as time advances by rolling across expiries, so the IV series
stays comparable over months. **Front** follows the nearest expiry instead, which makes the series
sawtooth as each expiry rolls. Constant maturity is what you want for a long study; front is what
you want if you are actually trading the front.

Six estimators exist because they use different information. Close-close sees only closing prices;
Parkinson uses the high-low range; Garman-Klass adds the open and close but assumes no drift;
Rogers-Satchell is the one that is free of drift; Yang-Zhang handles both drift and overnight gaps.
Which to use at which horizon, and the simulation check: [realised-volatility-estimators](realised-volatility-estimators.md). On a gappy index they will disagree, and the disagreement is
itself information.

## The regime change worth studying

NIFTY, constant-maturity 30-DTE ATM IV against 20-day close-close RV, Nov 2025 to Apr 2026:

- **Nov to late Jan** — IV around 10–11%, RV around 7–8%. **IV above RV.** The ordinary state, and
  the reason short-premium strategies exist at all.
- **From mid-Feb** — both climb steeply, and **RV crosses above IV**.
- **Mar to Apr** — RV holds near 25–30% while IV spikes and then falls back to about 17%, leaving
  RV well above IV.

That crossover is the whole risk of selling options in one picture: you are paid a premium for
volatility you expect, and the loss arrives when realised volatility exceeds what was implied.
Every short-vol backtest on this platform that spans February 2026 is being tested against that
event, and any that looks good through it deserves a second look.

The last stretch — IV collapsing to 17% while RV sits near 29% — is the opposite trap: options look
cheap on the tape at exactly the moment the market is still moving.

## How this connects to the rest

- The ATM IV series is the same number the [option chain](option-chain.md) prints in its header.
- Skew read here explains why the far columns of the [structure chain](structure-chain.md) price
  the way they do — put wings are expensive because the smile says so.
- Backtest diagnostics stamp ATM IV on every entry and exit, so a strategy's behaviour can be
  sorted by the vol regime it traded in. See [backtest-engine](backtest-engine.md).

## Open questions

1. Is the RV window in trading days or calendar days? Whichever it is, IV and RV must use the same
   clock. The research also says to match horizons: a 30-DTE IV wants about 21 sessions of RV, not 20
   days by default ([realised-volatility-estimators](realised-volatility-estimators.md)).
2. What does `n-avg` average, and over how many sessions?
3. Is `USER EXP` maturity pinned to the expiry chosen elsewhere, or set independently?
4. Is `BAR` fixed at daily, or are intraday bars intended?
5. Which side's IV feeds the ATM series when the nearest strike sits away from the forward?
