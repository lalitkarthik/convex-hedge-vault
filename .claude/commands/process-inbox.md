---
description: Promote durable capture from the inbox into domain notes and the glossary
---

Promote what is durable out of `inbox/`, and leave the rest where it lies.

1. Read every `inbox/*.md` file whose first line lacks `promoted:`.
2. Sort each item by destination:
   - how something works → `domain/<concept>.md`, creating the note when the concept is new
   - a term worth pinning down → `GLOSSARY.md`
   - something said in a meeting → `meetings/YYYY-MM-DD-<topic>.md`
   - a question still unanswered → the `## Open questions` section of the closest domain note
   - a reminder or passing thought → leave it in the inbox
3. Show the human every proposed promotion as destination plus a one-line summary. Wait for approval.
4. Apply the approved promotions. Add each new domain note to `index.md` with its status.
5. Add `promoted: <today's date>` as the first line of each file you processed, leaving its content untouched.

Done when every inbox file carries a `promoted:` line and `index.md` lists every note under `domain/`.
