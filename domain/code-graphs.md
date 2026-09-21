# Code graphs for Convex Hedge

Pointers to the Graphify code graphs. The graphs are generated, not written, so they live outside this vault, one standalone Obsidian vault per repo, backed up in the private repo `lalitkarthik/code-graph-vaults`. Built 2026-09-21; each row shows the commit it was built from, so staleness is visible.

| Repo | Source | Built from | Notes | Graph vault |
|---|---|---|---|---|
| delta-exchange-payoff | `/d/Convex Hedge/delta-exchange-payoff` | `docs/execution-design` @ `54d7764` | 6489 | `D:\second-brain\graph-vaults\delta-exchange-payoff` |
| payoff-project | `/d/Convex Hedge/payoff-project` | `main` @ `92f1710` | 1138 | `D:\second-brain\graph-vaults\payoff-project` |

## How to use them

- **Overview:** open `_graph/graph.html` inside the graph vault in a browser, or read `_graph/GRAPH_REPORT.md` (hubs, clusters, surprising links).
- **Browse:** in Obsidian, "Open folder as vault" on the graph vault. One note per function, class or file. Obsidian links do not cross vaults, so this note is the bridge.
- **Ask, from inside the source repo:** `graphify affected "Name"` (what a change could break), `graphify explain "Name"`, `graphify path "A" "B"`. Local and free.
- **Refresh after big changes:** `D:\second-brain\graph-vaults\map-repo.sh <repo-path> <name>`. Free without `--label`; `--label` names clusters with an LLM and spends Claude tokens.

## Limits

- The graph is built by parsing code. It cannot see behaviour wired up at runtime, such as event buses or dependency injection. Use it to find where to look, then read the real file.
- Links tagged INFERRED are leads, not facts.
- Nothing from Graphify is ever committed to the company repos: `graphify-out/` and `.claudeignore` are hidden with the local-only `.git/info/exclude`.
- Only `delta-exchange-payoff` has named clusters (that naming cost about 245k Claude tokens on 2026-09-21). The rest use "Community N".
