---
description: Check vault health — broken links, orphans, oversized notes, inbox overflow
---

Report on the health of this vault. Propose fixes; apply them once the human approves.

Run all seven checks and report each as pass, or as a specific list of offenders:

1. **Broken links** — every relative Markdown link resolves to a file that exists.
2. **Orphans** — every note under `domain/` is reachable from `index.md` or another domain note.
3. **Oversized notes** — flag any note over 200 lines, `CLAUDE.md` included, and propose a split.
4. **Inbox backlog** — count files under `inbox/` with no `promoted:` line. Over five means `/process-inbox` is due.
5. **Missing domains** — a topic recurring across inbox files with no `domain/` note is a domain waiting to exist. Name it.
6. **Stale pointers** — every repo path cited in a pointer still exists on disk.
7. **Uncommitted work** — `git status` is clean and the branch is pushed.

Done when all seven are reported.
