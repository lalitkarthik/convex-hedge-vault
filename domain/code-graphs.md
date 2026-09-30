# Code graphs for Convex Hedge

Each repo below has a local Graphify code graph in its own `graphify-out/` folder. Claude queries it; there is nothing to open or maintain by hand. The graph folder is hidden from git with the repo's local-only `.git/info/exclude`, so it never reaches the company repo. (Standalone Obsidian graph vaults were tried on 2026-09-21 and dropped as not useful.)

| Repo | Path | Graph built from |
|---|---|---|
| delta-exchange-payoff | `D:\Convex Hedge\delta-exchange-payoff` | `docs/execution-design` @ `54d7764`, 2026-09-21 |
| payoff-project | `D:\Convex Hedge\payoff-project` | `main` @ `92f1710`, 2026-09-21 |
| Convex-Hedge-Trading-Engine | `D:\Convex Hedge\Convex-Hedge-Trading-Engine` | `main` @ `b47d8ee`, 2026-10-01. Code only (src, frontend, tests, scripts); its `Trading-Engine/` docs vault is not in the graph |

## How to use

- Ask Claude from inside the repo: "what could break if I change X?" or "give me a tour of this repo". It runs `graphify affected "X"`, `graphify explain "X"` or reads `graphify-out/GRAPH_REPORT.md`, then confirms in the real file.
- To look yourself: open `graphify-out/graph.html` in a browser.
- Refresh after big changes: `graphify update .` inside the repo. Local and free. Never run `graphify cluster-only` without `--no-label`; naming clusters spends Claude tokens.

The trading engine's graph covers `src/`, `frontend/`, `tests/` and `scripts/`: 319 files, 222 communities
left unnamed. Its central nodes are `InMemoryBus`, `BusClient`, `CardSnapshot`, `EngineSettings` and
`TargetPosition`. Its 586 Markdown docs were left out on purpose, because they are read directly
([trading-engine](trading-engine.md) maps them). Refresh with `graphify update .` inside the repo.

## Limits

- The graph comes from parsing code. It cannot see behaviour wired up at runtime, such as event buses. Use it to find where to look, then read the file.
- Links tagged INFERRED are leads, not facts.
