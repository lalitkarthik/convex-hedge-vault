promoted: 2026-10-23
# 09 — AI Agent Sandboxing: Layers, Tradeoffs, and Blast Radius

- **Title:** AI Agent Sandboxing: Layers, Tradeoffs, and Blast Radius
- **Channel:** The Carbon Layer (Ankit Desai)
- **Id / link:** `-01_NB4SbBY` — https://www.youtube.com/watch?v=-01_NB4SbBY
- **Length:** 35:59
- **Article edition:** https://thecarbonlayer.com/agent-sandboxing/
- **Source of these notes:** yt-dlp hit HTTP 429; transcript from Firecrawl's YouTube scrape, read in full.

## Core thesis

Once an agent has tools, the prompt is no longer the boundary. "The prompt is an instruction. The boundary is something that still holds when the instruction fails." The sandbox is the part of the harness closest to the **blast radius**: it decides where an action may land. The word "sandbox" hides very different mechanisms; choose the **cheapest boundary that still contains the failure you worry about**.

## Three questions every harness must answer

1. Where does the agent run? 2. What is it allowed to touch? 3. How much can it do before a human or a policy stops it?

## Concepts

- **Intent vs containment.** Intent is what you ask the model to do. Containment is what happens when it tries something else. This video is about containment.
- **Tool calls are an attack surface.** Agent frameworks turn language into tool calls, which become file operations, network requests, shell commands. The danger is often the framework trusting the parsed call too much. Example: the **Microsoft Semantic Kernel** vulnerability — a callable function with loosely constrained arguments let language become a path into host execution. Some tools are "basically a terminal with a friendly name".
- **Approval fatigue.** Approval prompts do not scale as security. After 30 tiny approvals, people click to keep work moving (as with cookie banners and mobile permissions). Anthropic reported that turning on sandboxing in Claude Code cut permission prompts sharply; he reads that as prompts compensating for missing containment. With a good boundary, routine actions run freely and approvals are reserved for actions that cross a boundary: "it reduces the noise so the signal matters again".
- **System call path.** A file read becomes a syscall; the kernel checks process, path, permissions, mount and sandbox policy, then returns a file handle or "no". Sandboxing controls which requests reach the kernel, what the kernel allows, or what world the process believes it lives in.

## The sandbox stack (one file read, `/etc/passwd`, at five layers)

| Layer | Mechanism | What happens to the read | Fits | Cost / caveat |
|---|---|---|---|---|
| 1. Runtime isolation | V8 isolates, WebAssembly (linear memory, host imports) | No file operation exists unless the host provides one — "a room built without doors" | Narrow tasks via a tiny API (transform JSON, plugins) | Too small for a coding agent that needs files, shell, git |
| 2. OS-level sandbox | macOS Seatbelt; Linux bubblewrap (namespaces), Landlock (self-applied path rules, no root), seccomp (syscall filter) | Reaches the real kernel; policy says **permission denied** | Local coding agents: real process, real tools, blocked home dir, SSH keys, cloud config | Only as good as the policy: broad paths, open network, children not covered |
| 3. Containers | Docker: namespaces (mount, PID, network, user) + cgroups | Read may succeed but returns the **container's** file | Internal automation, CI-like tasks, mostly trusted code | **Shared host kernel**; Docker socket mount or `--privileged` punches holes |
| 4. User-space kernel | gVisor (the **Sentry** handles most syscalls) | Request goes to the Sentry, which decides | Untrusted code where micro-VMs feel too heavy | Compatibility edges, syscall overhead |
| 5. Micro-VM | Firecracker on KVM, own guest kernel | Handled by the guest kernel inside a separate small machine | Multi-tenant, user-submitted code, hosted agent platforms | Images, networking, snapshots, cleanup; GPUs harder |

Higher layers isolate more but cost more (startup, images, networking, debugging). The checklist across layers: what exactly is boxed in, what can still leak out, does the boundary follow child processes?

## How to choose

- **Local coding agent:** start with the tool's native sandbox (Codex, Claude Code) and learn its defaults. A slightly weaker boundary that is always on beats a strong one you keep bypassing.
- **Internal trusted automation:** **hardened Docker** — non-root, drop all capabilities, network off unless needed, mount only needed directories, read-only file system, scratch space, "treat the Docker socket like a loaded weapon".
- **User-submitted code:** managed sandboxes, gVisor, or micro-VMs. Self-hosted Firecracker means operating a small virtualization platform; do it deliberately.
- **Two common mistakes:** Docker as a synonym for sandbox; jumping to Firecracker for your own test runner. "Micro-VMs are where I go when the blast radius has to be tenant-sized, not host-sized."

## Five principles that apply at every layer

1. **Start closed** — network off, writes limited, credentials absent by default. Access is earned by configuration, not inherited from the machine.
2. **Treat file system and network as a pair** — secrets + internet = exfiltration path; free writes without internet can still poison code that later runs with more privilege. (He refers to Simon Willison's "lethal trifecta" idea.)
3. **Cover child processes** — shells call package managers, which run scripts, which spawn workers. A sandbox on the first process only is an easy escape.
4. **Choose by blast radius** — a personal agent on one repo is not a SaaS running thousands of users' code.
5. **Make the safe path easy** — if safety needs a long doc, three flags and perfect memory, nobody uses it daily.

## Tools, credentials, and the three boundaries

Treat model-callable functions like **public endpoints**: minimize the tool list, keep contracts narrow, validate arguments at the tool boundary (paths, URLs, SQL fragments, command arguments), prefer structured choices to free strings, avoid general escape hatches. The sandbox is the backstop. **Caveat:** a sandbox limits where code goes, not whether the intended action is safe — a valid production API key used through the official API looks like a normal request. Agent safety has three boundaries: **what the model can call** (tool registry), **what those tools can reach** (credentials), **where execution can touch the system** (sandbox). Pair sandboxing with scoped credentials, explicit registries, audit logs, approval gates, and tight defaults.

**Final model:** an agent harness is "a runtime for delegated action". The follow-up questions when someone says "it runs in a sandbox": What layer? What file-system access? What network access? Do children inherit it? What credentials are present? What happens when the model confidently does the wrong thing?

## Diagram to redraw

1. Vertical stack of five boxes, bottom to top: V8/WASM → OS sandbox → container → gVisor → micro-VM; an arrow up the side labelled "more isolation, more cost".
2. On the left, one request "open /etc/passwd" with five arrows, one into each layer, each labelled with its outcome (no such operation / denied / container's file / Sentry decides / guest kernel's file).
3. A second diagram of three concentric rings around the model: **tool registry** (what actions exist) → **credentials** (what they can reach) → **sandbox** (where execution can cause damage). Approval gate sits on the arrow that crosses the outer ring.

## Code or repos

None shown.

## What this means for our options-research harness

1. Research agents run start-closed: network allowed only to Databento and the broker sandbox endpoints, writes only to the run's scratch directory and results folder, no `.env` in reach (this matches the deny rule already in place).
2. Fetch market data in a harness-side tool that holds the key; the agent gets the data file, never the key. Scope keys to read-only where the vendor allows it.
3. Validate tool arguments: date ranges, symbols and file paths are checked against allow lists before any paid API call.
4. Use the native Claude Code sandbox locally; move to hardened Docker for unattended overnight research jobs.
5. Make sure the sandbox covers child processes — notebooks spawn kernels and backtests spawn workers.
6. Keep approvals for boundary-crossing actions only (paid data pulls above a cost cap, anything touching the trading engine), so the prompts stay meaningful.
