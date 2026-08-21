# Session log

Append-only. Newest entry at the bottom. One block per session: what was decided, and what is still open.

<!-- Entry shape:

## 2026-08-19

**Decided:** …
**Open:** …

-->

## 2026-08-21

**Decided:** Breadth-first, then depth. Phase 1 maps the whole terminal; Phase 2 takes one surface
at a time — option chain, structure chain, strategies — with the Greeks as the lens across all
three rather than as a fourth pass. Phase 3 opens teach workspaces only when the jargon stops
making sense.

**Decided:** Teach workspaces split by subject, not by tool. Portable options knowledge (Greeks,
vol, pricing) goes to `D:\second-brain\second-brain\learning\<topic>\`. Convex Hedge's own system
goes to `teach/<topic>/` in this vault.

**Decided:** `payoff-project` stays out of the vault for now. Its existence is noted; what to
promote gets chosen later, by hand.

**Decided:** Access to the terminal is by Google SSO in a browser pane the human signs into.
Read-only throughout — no rerunning, no deleting, no saving.

**Done:** Phase 1 breadth pass over all six surfaces. Wrote [platform-map](domain/platform-map.md)
and seeded [GLOSSARY.md](GLOSSARY.md) with the terminal's vocabulary.

**Open — resolve in the depth passes:**

1. **What is Echo?** A strategy source alongside Registry, with a `NOT VALIDATED` state and an
   external owner. Who or what authors one, and what validation means, is unknown.
2. **Margin does not reconcile.** `expiryday_long_strangle` reports `AVG MARGIN / DAY ₹646` while
   each trade pays roughly ₹75,000 in premium for long options. Long premium is paid in full, so
   ₹646 is not a margin figure that makes sense. Either margin means something specific here, or it
   is wrong.
3. **46% of orders are rejected.** 84 of 182 on that same run. Probably the `min_entry_premium`
   filter refusing entries, but unconfirmed — and if so, a rejected order is a normal outcome
   rather than an error, which changes how the number should be read.
4. **Returns below −100% are a sizing artifact, not a P&L bug.** Per-leg arithmetic checks out
   exactly. The engine sizes 200 lots regardless of the account being exhausted and reports against
   the fixed anchor. Worth knowing which runs are capital-constrained before trusting any headline
   return.
5. **Greeks go blank on far-OTM strikes.** Quotes exist, Greeks show dashes. Presumably the IV
   solve fails below some premium — confirm the threshold and whether it silently affects
   structures built out there.
6. **Premium sign convention is opposite to `payoff-project`.** The terminal shows a long straddle
   as negative net premium; `payoff-project` treats a debit as positive. Confirm the terminal's rule
   before reading any Structure Chain number.
7. **`/oi` never loaded.** GEX and OI both unseen.
8. **MISSION.md is still placeholders.** It should say what this vault is for before it steers
   anything.
9. **Vault root still half-looks like a teach workspace** — `RESOURCES.md`, `NOTES.md`,
   `learning-records/`, `assets/` are files the teach skill expects in *its* directory. Decide
   whether they are vault-level or leftovers.
10. **The `teach` skill is not enabled.** Cached under `mattpocock-skills/skills/productivity/`
    but that group is switched off, so Phase 3 cannot start.
