---
name: "source-command-vault-lint"
description: "Check vault health — broken links, orphans, oversized notes, stale stamps, inbox overflow"
---

# source-command-vault-lint

Use this skill when the user asks to run the migrated source command `vault-lint`.

## Command Template

Report on the health of this vault. Propose fixes; apply them once the human approves.

Run all eight checks and report each as pass, or as a specific list of offenders:

1. **Broken links** — every relative Markdown link resolves to a file that exists.
2. **Orphans** — every note under `domain/` is reachable from `index.md` or another domain note.
3. **Oversized notes** — flag any note over 200 lines, `AGENTS.md` included, and propose a split. Raw record — `inbox/`, `meetings/`, `research/_raw/` — is exempt.
4. **Inbox backlog** — count files under `inbox/` with no `promoted:` line. Over five means `/process-inbox` is due.
5. **Missing domains** — a topic recurring across inbox files with no `domain/` note is a domain waiting to exist. Name it.
6. **Stale pointers** — every repo path cited in a pointer still exists on disk.
7. **Stale stamps** — for each note opening with `> As of ` + "repo@sha" + date: check whether the files that note cites have changed since that commit, with `git -C <repo> log --oneline <sha>..HEAD -- <cited paths>`. Report each note whose cited files moved on, and how many commits have landed. These notes need re-reading against the code; keep them until then, since a stale map still beats no map.
8. **Uncommitted work** — `git status` is clean and the branch is pushed.

Done when all eight are reported.
