## Account rule (the owner's, set 2026-10-04; it replaces every earlier account rule and overrides the skill wherever they differ)

`ACCT` is `node "C:/Users/Acer/AppData/Local/Temp/feature-loop-acct.mjs"`. Use it wherever the
skill says `CX pick`; never run `CX pick` and never pass `--account a`.

- **Accounts:** `b` and `c` only. Never `a`. `max` only when `b` and `c` are both spent.
- **No limit per account:** any number of sessions may run on one account at the same time.
- **Starting a worker** (implementer, fixer, flow checker, your successor):
  `ACC="$(ACCT pick <run-name>)"`. It prints `b`, `c` or `max`, spreading workers over the
  accounts. Then `CX run … --account "$ACC"`.
- **Before every `CX send <name>`:** run `ACCT assign <name>`. It moves that worker's record to
  an allowed, unspent account and prints the account.
- **`ACCT pick` prints `max`:** `b` and `c` are both spent, and the owner allows `max` then.
  The **Usage limit** rule is unchanged: a worker that hits the limit on `max` means every
  account is spent, so take the stop, with the resume command using
  `--account "$(node "C:/Users/Acer/AppData/Local/Temp/feature-loop-acct.mjs" pick <run-name>)"`.
- `ACCT status` shows what runs where.
- Copy this whole "Account rule" section, word for word, into every hand-off you write and into
  your successor's prompt file, so it holds for the rest of the build.

## Parallelism override (the owner's; it overrides the skill wherever they differ)

The one-implementer-while-Docker-runs cap is off for this build: start the whole frontier at once
(the wave rule only). Copy this section, word for word, into every hand-off and successor prompt
you write, next to the Account rule.

## Tier rule (the owner's, set 2026-10-04; it replaces the tier table in workflow.md's Models rule)

The number of areas a ticket touches does not set its tier.

| Tier | Model / effort | The ticket |
| --- | --- | --- |
| `sonnet-high` | Sonnet high | is tightly scoped and leaves no design choice open: the ticket and the spec already say what to build, and the code has a pattern to follow |
| `opus-medium` | Opus medium | everything else |
| `opus-high` | Opus high | leaves a design choice open, or involves concurrency, a data migration, auth or money |

Copy this section into every hand-off and successor prompt you write, next to the Account rule.
