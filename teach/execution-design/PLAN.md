# Plan — sixteen sessions

Written **2026-09-25**. Sessions are **~45 minutes, 3–5 committed predictions each**, one question
per message. Every session is grounded in a named section of a real document.

**The source is the design as merged in `delta-exchange-payoff` #128 (2026-09-17)**, under
`D:\Convex Hedge\delta-exchange-payoff\docs\design\execution\`. The 20 and 25 September meetings
asked for changes that are not yet in those pages. Block C studies them only once they are written in.

## Block A — the trading half, as designed

| # | Session | The one idea | Read | Status |
|---|---|---|---|---|
| 1 | **The pieces** | A strategy states a wish; the OMS turns wishes into orders; risk says yes or no; a broker fills. Six rules hold it together | `00-overview.md`; `operations.md` "What runs where" | |
| 2 | **Books I — what a book is** | A book is signed lots per contract. Desired against actual. Six books plus working orders, and who writes each | `books.md` to "Why Book 6 is derived" | |
| 3 | **Books II — the gap** | Orders = Book 2 − Book 4 − working. Why working is subtracted; why the sum is pooled; the settling window | `books.md` "How orders are worked out" | |
| 4 | **Books III — reallocation and Book 3's tag problem** | When wishes swap and the sum does not move, no order is sent and Book 3 is rewritten. One pooled order can only name one strategy | `books.md` "When the pooled book does not move", "How Book 3 is filled in" | |
| 5 | **Books IV — the check that catches a double fire** | Reconciliation every ten seconds: two identities per contract; a mismatch freezes one contract. The person-trades-by-hand case | `books.md` "The check that catches a double fire" | |
| 6 | **An order's life** | Intent, sent, acked, filled, replaced, cancelled. Limit at the touch with cancel and replace; why no market orders | `oms.md` "The order lifecycle" | |
| 7 | **Legging** | Buys first, wait, then sells, because margin. What a half-filled condor actually is | `oms.md` "Legging: buys first" | |
| 8 | **The strategy worker and the sample condor** | Logic only. Entering means waiting for Book 3. The state machine and the counters a crash must not lose | `strategy-worker.md` | |
| 9 | **The six risk checks** | Yes or no, never smaller. Why margin is priced on the whole portfolio, and why it only alerts for now | `rms.md` | |
| 10 | **The paper broker** | Fill at the touch, never mid. Instant fills without a special case. What it ignores: size | `paper-broker.md` | |
| 11 | **Tracing** | Three labels on every event; following a fill back to its decision | `events-and-tracing.md` | |
| 12 | **Operations** | Commands, the kill switch, what each restart loses, the build order | `operations.md` | |

## Block B — the feed engine underneath

| # | Session | The one idea | Read | Status |
|---|---|---|---|---|
| 13 | **Feed, bus, store** | One connection to the venue; the bus lets readers go at their own speed; drop-oldest against lossless | `domain/feed-engine.md`; `final-design/architecture.md`, `message-bus.md` | |
| 14 | **Sealing, flushing, replay** | A bar is sealed, then flushed. What a store restart loses, and why retention must outlast the flush interval | `domain/bar-store.md` | |

## Block C — the changes, once written into the design

| # | Session | The one idea | Read | Status |
|---|---|---|---|---|
| 15 | **The 20 September review** | Persisted working orders, state over the bus, reconciliation that repairs, signal cards, market hours per instrument | the revised pages; `meetings/20-09-26-recap.txt` | Waiting on the pages |
| 16 | **Per-client OMS** | Clients subscribe to strategies; orders in strategy units; books and risk per client; routing one position to several brokers | the revised pages; `meetings/25-09-26-recap.txt` | Waiting on the pages |

## What a prediction looks like here

> Book 2 wants +1 of the 58000 put. Book 4 holds +1. Working is 0. A person then buys 1 more of the
> same put on Delta's app. Before you look: what do Book 5 and Book 6 show, and does the engine send
> an order?

Commit to the numbers first; then check against `books.md`'s worked case.

## Trader's-seat question for every session

What trading problem does this part solve, and what would it cost in money if it were missing?
