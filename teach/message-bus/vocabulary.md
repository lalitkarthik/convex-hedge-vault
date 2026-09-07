# Vocabulary — message buses, in plain words

Every term used in this workspace, defined before it is used anywhere else.
Nothing here is Convex Hedge-specific, which is why it is not in [GLOSSARY.md](../../GLOSSARY.md).

## The picture to hold

A trading room with **one window** onto the street.

- One person stands at the window. Prices are shouted in from outside, constantly.
  **Their only job is to hear them.** Stop listening for a second and you miss prices —
  worse, the person outside gives up and walks away.
- Two other people need those prices:
  - the **whiteboard writer** rubs out the old price and writes the new one. Only *now*
    matters. Falling behind should mean skipping to the latest, not replaying a backlog.
  - the **ledger keeper** writes down *every* price in a book, forever. Falling behind
    means catching up — a missing entry is a hole in history.
- So the window person hands prices to nobody. They drop each one into **two in-trays**
  and turn straight back to the window.

That is our architecture. The rest of this file names its parts.

## The words

| Word | What it means | In the picture |
|---|---|---|
| **message** | one small piece of data, sent once | one shouted price |
| **producer** | the thing that creates messages | the person at the window |
| **consumer** | a thing that reads messages | whiteboard writer, ledger keeper |
| **queue** | a line of messages waiting to be read | the in-tray |
| **fan-out** | one message copied to several consumers | dropping each price into both trays |
| **topic** / **channel** | a named stream, so consumers take only what they want | separate trays for prices, news, alerts |
| **publish / subscribe** | producer publishes to a topic; consumers subscribe. The producer never learns who listens | shout into the tray; never look up to see who collects |
| **backpressure** | what happens when a consumer is slower than the producer | the in-tray piles up |
| **drop-oldest** | on overflow, discard the *bottom* of the pile | right for the whiteboard: a four-second-old price is worthless, not slightly worse |
| **lossless** | never discard; let the pile grow | required for the ledger |
| **watermark** | a depth at which you start *counting* overflow instead of discarding it | somebody notices the pile before the room fills |
| **stale** | correct once, wrong now | a price still on the whiteboard after the market moved |
| **cache** | a kept copy, so the work is not redone | the whiteboard itself |
| **process** | one running program, with its own memory | one room |
| **in-process** | all inside one program's memory | everyone in the same room |
| **message broker** | a separate program whose only job is carrying messages between programs | a pipe to a different building |
| **serialise / deserialise** | turning an object into bytes to send, and back again | writing the price on paper, then reading it back |
| **durable** | survives the program dying | in the ledger, not just on the whiteboard |
| **replay** | reading old messages again, later | re-reading yesterday's ledger |
| **consumer group** | several readers sharing one stream, each message going to exactly one of them | three clerks splitting one in-tray |
| **at-least-once** | a message may arrive twice, never zero times | the price gets through, possibly shouted twice |
| **exactly-once** | arrives precisely once. Expensive, and rarer than it is claimed | |

## Three levels, not two

A separate **program** is not a separate **machine**. This is the most commonly muddled
point in the whole topic.

| level | example | share memory? | what they need to talk |
|---|---|---|---|
| **1. same program** | our feed, IV solver and bar writer | **yes** | nothing — just memory |
| **2. different programs, one computer** | Chrome and VS Code on one laptop | **no** | something in between |
| **3. different computers or VMs** | engine here, strategy on a server | **no** | something in between, over a network |

**The boundary that forces a bus is 1 → 2.** Going from 2 to 3 changes the distance, not
the need. A Redis bus running entirely on one laptop is still a real bus.

**And a bus is not the only way to cross level 2.** Our own engine and web app are two
separate programs and they talk over **HTTP and a websocket**. For one server and a handful
of browsers that is simpler than a broker and buys the same thing. Reach for a broker when
the traffic is a high-rate stream fanned out to several long-lived consumers, not when it
is request/response.

## The three products, one line each

| | what it is | its instinct |
|---|---|---|
| **Redis** | an in-memory data store that also carries messages | fast and simple; forgets unless told not to |
| **RabbitMQ** | a dedicated broker with rich routing rules | careful delivery — this job reaches exactly one worker |
| **Kafka** | a durable, replayable log of everything that happened | keeps everything for days so anyone can re-read |

**"Which is better" has no answer without a message rate.** That discipline is enforced
throughout this workspace — see [architectures](architectures.md).

## Two Redis words that are not the same thing

| | keeps messages? | if nobody is listening |
|---|---|---|
| **Redis pub/sub** | no | the message is gone, silently |
| **Redis Streams** | yes, up to a trim limit | the message waits to be read |

Which of the two a system uses decides whether it has any durability at all. It is the
first question to ask of any Redis-based design, including the senior's.
