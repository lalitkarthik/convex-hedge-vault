promoted: 2026-10-23
# MCP servers and tools for an options research harness

> Lane report, 2026-10-16. Raw research capture: staging, not fact. Nothing here is promoted to `domain/`.
> Question: which existing MCP servers and agent tools can the harness reuse, and what must we write ourselves?

## How to read this page

An MCP server is a program that gives an agent a set of named tools. The agent calls a tool with arguments and receives a result. This page asks, for each server that exists, three things: does it hold option chains (full chain, history, Greeks), who maintains it, and what does it cost us in money and risk.

Each source carries a reading label:

- **Full**: I read the page itself.
- **Fetch**: a fetch tool read the page and gave me a summary; I did not see every line.
- **Excerpt**: I saw only search-engine extracts of the page.

GitHub stars and the last push date come from the GitHub API on 2026-10-16. Keys appear only as environment variable names. Where I write "not checked", I did not look; where I write "not found", I looked and found nothing.

The short answer: **no existing server serves historical option chains from our own files, and none records trials.** The data vendors and brokers now ship official servers, but they serve their own live or historical APIs. The research core (our chain data, features, backtests, trial ledger) we must write. Literature, notebooks, SQL and memory we can reuse.

## 1. Data servers: US

| Server | Maintainer | Chain support | Cost | Activity | Read |
|---|---|---|---|---|---|
| [dbn-go-mcp-data / -meta](https://github.com/NimbleMarkets/dbn-go/blob/main/cmd/dbn-go-mcp-data/README.md) (Databento) | Community (NimbleMarkets) | No OPRA quote schema in `fetch_range` | Databento billing | 43 stars, push 2026-05-04 | Fetch |
| [databento-mcp-server](https://github.com/Nice-Wolf-Studio/databento-mcp-server) | Community | ES/NQ futures focus | Databento billing | 10 stars, 2025-11-25 | Excerpt |
| [mcp_massive](https://github.com/massive-com/mcp_massive/) (Polygon, now Massive) | Official | Chain snapshot with Greeks; history by REST | Massive plan, not checked | 398 stars, 2026-10-08 | Excerpt |
| [Theta Terminal v3 MCP](https://www.thetadata.net/docs/Mcp/Getting-Started.html) | Official, inside the terminal | Full chain, history, Greeks, 0DTE | Subscription, not checked | Closed source | Excerpt |
| [ORATS CLI + MCP](https://orats.com/ai-agents) | Official | Smoothed IV surface, 1-min since Aug 2020, EOD since 2007, intraday backtester incl. 0DTE | $199–$899/month, Tools APIs $99–$299 extra ([pricing](https://orats.com/data-api)) | Closed source | Excerpt |
| [alpha_vantage_mcp](https://github.com/alphavantage/alpha_vantage_mcp) | Official | `HISTORICAL_OPTIONS`: daily chain, 15+ years, Greeks | Free tier; premium for real-time | 220 stars, 2026-10-03 | Excerpt |
| [FMP MCP](https://site.financialmodelingprep.com/developer/docs/mcp-server) | Official, hosted | Not found (stock data) | FMP plan | Hosted | Excerpt |
| [Tradier MCP](https://docs.tradier.com/docs/tradier-mcp) | Official, hosted | Current chain; Greeks come from ORATS | Brokerage account | Hosted | Excerpt |
| [IBKR AI integration](https://www.interactivebrokers.com/en/trading/ai-integrations.php) | Official, hosted at `api.ibkr.com/v1/api/mcp-public` | Option chains, account data | Free with account | Hosted | Excerpt |
| [tastytrade-mcp](https://developer.tastytrade.com/docs/sdks-and-tools/mcp-server/) | Official, self-hosted | Chains, live Greeks over DXLink | Brokerage account | 30 stars, 2026-10-12 | Excerpt |
| [tasty-agent](https://github.com/ferdousbhai/tasty-agent) | Community | Live Greeks, a GEX tool | Brokerage account | 87 stars, 2026-10-04 | Excerpt |
| [alpaca-mcp-server](https://github.com/alpacahq/alpaca-mcp-server/) | Official | Chain snapshot with Greeks and IV; historical option bars and trades | Free paper account | 1,022 stars, 2026-10-12 | Excerpt |
| Cboe DataShop / LiveVol | — | **No MCP server found.** LiveVol has an OAuth REST API ([docs](https://api.livevol.com/v1/docs/)) | Points tiers | — | Excerpt |

**Databento.** Databento publishes no MCP server; its GitHub organisation lists client libraries only ([org](https://github.com/orgs/databento/repositories), Excerpt). The best community server, `dbn-go-mcp-data`, has a good shape: free discovery tools (`list_datasets`, `list_schemas`, `get_cost`), one billed tool (`fetch_range`) that caches Parquet, and `query_cache`, which runs DuckDB SQL over the cache. It has a `--max-cost` flag per query (default $1) and a `--read-only` flag that removes `fetch_range`. It prefers a key file (`DATABENTO_API_KEY_FILE`) to an environment variable. But its `fetch_range` accepts only OHLCV, trades, mbp-1, tbbo, imbalance and statistics. **It does not list `cbbo-1m` or `definition`, the two schemas our SPXW work uses.** So it cannot fetch our data as it stands. Take its shape; do not take the server.

**Theta Data** is the closest to what we need from a vendor. Its MCP server starts with the Theta Terminal and listens on `127.0.0.1:25503` ([Claude page](https://www.thetadata.net/claude), Excerpt). Its Greeks endpoints take `strike=*` for every strike of one expiry, solve IV at the NBBO mid, and use real time to expiry down to one hour for 0DTE ([Greeks article](https://www.thetadata.net/docs/Articles/Data-And-Requests/Option-Greeks.html), Excerpt). Multi-day Greeks requests are limited to one month ([all Greeks](https://www.thetadata.net/docs/operations/option_history_greeks_all.html), Excerpt). It would be a second source to check our own IV and Greeks against. It needs a paid subscription and Java 21; I did not check the price.

**ORATS** sells the computed answer: a smoothed IV surface, forecasts, and an intraday backtester API that accepts 0DTE jobs. Its underlying price is derived from options by put-call parity and is "not a replacement for real stock prices" ([data API](https://orats.com/data-api), Excerpt). Useful as an outside benchmark. It does not fit as the harness core: the agent would test ideas on a vendor's engine whose fills and cost model we cannot read.

**Brokers** (IBKR, Tradier, tastytrade, Alpaca) serve live chains and accounts. None serves SPXW quote history at one-minute depth for research. All except IBKR can place orders; IBKR's server only drafts "instructions" that a human must submit ([ORATS on IBKR](https://orats.com/blog/agentic-options-research-with-the-ibkr-ai-integration), Excerpt). The harness does not trade, so these are out of v1. The security ideas transfer (section 7).

**Security notes.** FMP's documented connection URL carries the key as a query parameter (`?apikey=`), which leaks into logs; it now also offers OAuth ([mcp.so listing](https://mcp.so/servers/fmp), Excerpt). Alpaca defaults to paper trading (`ALPACA_PAPER_TRADE=true`) and can hide tool groups (`ALPACA_TOOLSETS`). tastytrade has `TASTYTRADE_READ_ONLY=1` and `MAX_ORDER_NOTIONAL_USD`.

## 2. Data servers: India

| Server | Maintainer | Chain support | Cost | Activity | Read |
|---|---|---|---|---|---|
| [kite-mcp-server](https://github.com/zerodha/kite-mcp-server) (Zerodha) | Official; hosted at `mcp.kite.trade/mcp` | Quotes, OHLC, historical candles, instrument search; **no option-chain tool** | Free hosted with an account; self-host needs Kite Connect | 324 stars, 2026-09-10 | Excerpt |
| [Upstox MCP](https://upstox.com/developer/api-documentation/mcp-integration/) | Official, hosted | **Account data only** (holdings, orders, funds, positions) ([overview](https://upstox.com/developer/api-documentation/api-overview)) | Free with account | 0 stars, 2026-08-19 | Excerpt |
| Dhan native MCP ([docs](https://docs.dhanhq.co/)) | Official | Option chain with Greeks; tool list not found | Data Plan needed for data APIs | Not checked | Excerpt |
| [dhanhq-mcp](https://github.com/shubhamtaywade82/dhanhq-mcp) | Community | Chain, IV rank, `expired_options_data.get` | Dhan Data Plan | 0 stars, 2026-07-08 | Excerpt |
| [Fyers MCP](https://fyers.in/api-docs/ai/mcp/) | Official, hosted | Historical candles and option chains, 38 tools | Free with account | Hosted | Excerpt |
| [angel-one-mcp](https://github.com/ameernoufil/angel-one-mcp) | Community | OI, Greeks, PCR | Free with account | 0 stars, 2026-05-22 | Excerpt |
| [Indian-Option-MCP](https://github.com/devag7/Indian-Option-MCP), [NseKit-MCP](https://github.com/Prasad1612/NseKit-MCP), [nse-bse-mcp](https://playbooks.com/mcp/bshada/nse-bse-mcp) | Community | Live NSE chain by reading nseindia.com endpoints | Free | 14 / 6 / 13 stars | Excerpt |
| [OptionAlgo](https://optionalgo.in/ai-connector) | Commercial, hosted, read-only | Live NIFTY chain with Greeks, GEX, dealer flow | Free tier | Hosted | Excerpt |

**The useful find for NIFTY history is not an MCP server; it is Dhan's expired options API.** It gives five years of minute data for expired index and stock options, "on rolling basis": strikes are named relative to spot (ATM, up to ATM±10 for index options near expiry), with OHLC, IV, volume, OI and spot, up to 30 days per call ([Dhan docs](https://dhanhq.co/docs/v2/expired-options-data/), Excerpt). That answers the problem the 7 Oct pipeline page reported: brokers drop expired contracts ([pipeline.md](../2026-10-07-research-pipeline/pipeline.md), stage 4). It does not fit perfectly: a strike named "ATM+3" changes contract as spot moves, so a held position must be rebuilt from contract IDs, and strikes beyond ATM±10 are absent. I did not check the Data Plan price, nor whether bid and ask are present (the field list shows OHLC, not quotes).

**Kite and Upstox official servers are not research servers.** Kite's hosted server removes trading tools for safety; a self-hosted copy can drop tools with `EXCLUDED_TOOLS` (variables `KITE_API_KEY`, `KITE_API_SECRET`). It has no option-chain tool, so the agent would build a chain from `search_instruments` plus `get_quotes`. Upstox's official server reads the account only; option chains with Greeks exist in its REST API ([chain API](https://upstox.com/developer/api-documentation/get-pc-option-chain), Excerpt).

**NSE scrapers are fragile.** They call nseindia.com's website endpoints, which close after 15:30 IST (Indian-Option-MCP switches to a fallback endpoint then). I did not read NSE's terms of use; check them before any automated capture.

**Security.** Angel One servers take the account MPIN and the TOTP secret as environment variables (`ANGEL_PASSWORD`, `ANGEL_TOTP_SECRET`). That gives a local process full login power. Do not run them.

## 3. Crypto options

| Server | Maintainer | Chain support | Activity | Read |
|---|---|---|---|---|
| [delta-exchange-mcp](https://github.com/delta-exchange/delta-exchange-mcp) | Official, Delta Exchange India | 14 public tools with no key: tickers, order book, candles, OI, `get_options_chain` | 15 stars, pushed 2026-10-16 | Excerpt |
| [deribit-mcp](https://github.com/schoeffeljp/deribit-mcp) | Community | Chain with Greeks, `get_volatility_surface`, `find_options_by_delta`, DVOL | 3 stars, 2026-03-23 | Excerpt |

The Delta Exchange server matters because `delta-exchange-payoff`, our earlier repo, runs on that exchange. It is local stdio and read-only by default; trading registers only with `DELTA_MCP_MODE=trade`. Its own docs warn that a Trading key means "no rehearsal, no size cap and no confirmation step" ([docs](https://mcp.delta.exchange/docs), Excerpt). Every mutation is written to an audit log under `~/.delta-exchange-mcp/audit/`. Crypto is not one of the two harness markets, so this is a later lane.

## 4. Backtest and quant servers

**QuantConnect** ([key concepts](https://www.quantconnect.com/docs/v2/ai-assistance/mcp-server/key-concepts), Fetch; [repo](https://github.com/QuantConnect/mcp-server), 79 stars, 2026-05-07). Official, about 64 tools in groups: projects, files, compile, backtests, optimisation, live trading, cloud Jupyter, object store, datasets, skills, notifications. Its backtest pattern is the one to copy: `create_backtest` returns an ID, and the tool description tells the agent not to poll, because the result arrives later as a message. QuantConnect calls its agent servers "a harness for quant finance". Its data has SPXW minute quotes since January 2012 (AlgoSeek, OPRA-derived), at $0.15 per ticker-day file for local download ([dataset](https://www.quantconnect.com/docs/v2/writing-algorithms/datasets/algoseek/us-index-options), [download](https://www.quantconnect.com/docs/v2/lean-cli/datasets/quantconnect/index-options), Excerpt). The remote server needs a paid agent node. What does not fit: the strategy must be a LEAN algorithm, the fill model is LEAN's, NSE options data was not found, and the server carries live-trading and SMS tools that the harness must never see.

**vectorbt PRO MCP** ([page](https://vectorbt.pro/features/ai/mcp-server/), Excerpt). Commercial. Documentation search, source reading, skills, and `run_code` in a persistent Jupyter kernel (stdio only). vectorbt works on price arrays; it has no option-chain model.

**cloudQuant/backtrader-mcp** ([repo](https://github.com/cloudQuant/backtrader-mcp), 1 star, 2026-09-20, Excerpt). Tiny, but the best design found for a backtest server. It turns CSV files into immutable datasets, keeps strategies as reviewed drafts, and runs them in a bounded subprocess through `prepare_strategy_run` → `start_strategy_run` → `get_run_status` → `get_run_result`, with `cancel_strategy_run`, `list_jobs` and bounded `get_run_logs`. A start needs a run-plan ID, a signed run token, an approval ID and an idempotency key. It exposes no brokers, no credentials and no arbitrary Python. It says plainly that its SDK lacks the Tasks extension, so it built its own job tools.

**Others.** [kukapay/backtrader-mcp](https://github.com/kukapay/backtrader-mcp) runs agent-written strategy code with `exec` in one `run_backtest` tool, crypto only: a pattern to avoid. [marketcalls/vectorbt-backtesting-skills](https://github.com/marketcalls/vectorbt-backtesting-skills) (209 stars) is a skill pack, not a server; it has an Indian F&O cost model and SEBI lot sizes from December 2025, worth reading for the NIFTY cost model. [BacktestLoop](https://backtestloop.com/) and [Manifold-BT](https://www.manifoldbt.com/mcp) are commercial platforms; Manifold-BT's server serves only its documentation, so code and data stay local.

No open-source options backtest engine with an MCP server was found.

## 5. Notebook, compute and SQL servers

| Server | Maintainer | What it gives | Activity | Read |
|---|---|---|---|---|
| [jupyter-mcp-server](https://github.com/datalayer/jupyter-mcp-server/) | Datalayer | Read, insert, edit, execute cells; `execute_code`; sandbox variants (Docker, Modal, E2B…) | 1,304 stars, 2026-10-16 | Excerpt |
| [mcp-server-motherduck](https://github.com/motherduckdb/mcp-server-motherduck/) | MotherDuck, official | DuckDB SQL on a local file or MotherDuck | 530 stars, 2026-10-07 | Excerpt |
| [postgres-mcp](https://github.com/crystaldba/postgres-mcp) (Postgres MCP Pro) | Crystal DBA | Nine tools; `--access-mode=restricted` | 3,403 stars, 2026-08-17 | Excerpt |
| [mcp-run-python](https://github.com/pydantic/mcp-run-python) | Pydantic | **Archived** | — | Excerpt |
| [e2b-dev/mcp-server](https://hub.docker.com/r/mcp/e2b) | E2B | `run_code`; **repo archived** (GitHub API) | — | Excerpt |

**Jupyter.** The Datalayer server runs execution on the Jupyter server, so a long computation survives the end of the agent session ([reference](https://jupyter-mcp-server.datalayer.tech/mcp/reference/), Excerpt). Cells can be addressed by a stable cell ID, not only by position. The risk is the one the pipeline page names: cells run in any order, so the notebook can differ from a clean run ([pipeline.md](../2026-10-07-research-pipeline/pipeline.md), "Notebooks"). Use it for the final report notebook, run top to bottom; keep research logic in tested modules.

**DuckDB.** The local MotherDuck server opens a DuckDB file read-only by default and caps output (`--max-rows` 1024, `--max-chars` 50,000, optional `--query-timeout`). Its own README warns that read-only mode "alone is not sufficient" for third-party access, because DuckDB can still read the local filesystem. Run it in a container with only the data folder mounted.

**Postgres.** The reference Postgres server is archived. A secondary source reports that Datadog Security Labs escaped its read-only mode with `COMMIT` followed by any statement, in August 2025 ([Hikmah blog](https://hikmahtechnologies.com/blog/postgres-mcp-server/), Excerpt; I did not read the Datadog post). Postgres MCP Pro parses SQL with `pglast` and rejects `COMMIT`; its default mode is `unrestricted`. The blog's advice is right for us: the read-only guarantee must come from the database role (`SELECT` grants, `default_transaction_read_only`, `statement_timeout`), with the server's mode as an extra layer.

**Python sandbox.** Both popular sandbox servers are archived. Pydantic says there is "no safe way" to run Python in Pyodide with reasonable latency. For the harness, run our own code in a container we control.

## 6. Experiment tracking, literature and memory

**MLflow** (official, inside [mlflow/mlflow](https://mlflow.org/docs/latest/genai/mcp/), Excerpt). `mlflow mcp run` starts it. `MLFLOW_MCP_TOOLS` picks tool groups: `genai` (26 tools), `ml` (experiments, runs, models, deployments; 32 tools), or `all` (45) ([cookbook](https://mlflow.org/cookbook/mlflow-mcp-server/), Excerpt). It is free and local. Its toolsets include delete tools, so it cannot be the trial ledger: an agent could delete its failed trials. It can be a read-only mirror of the ledger.

**Weights & Biases** ([repo](https://github.com/wandb/wandb-mcp-server), official, 71 stars, 2026-10-16, Excerpt). Hosted at `mcp.withwandb.com`, or self-hosted. `WANDB_MCP_ACCESS_MODE=read-only` removes write tools. The data lives in W&B's cloud, so company research results would leave our machines. Not needed if we run MLflow.

**DVC.** No official MCP server found. A community server wraps DVC, MLflow and Git ([mlops-mcp-server](https://github.com/anant-patankar/mlops-mcp-server), 1 star). DVC is still useful from the command line to version the Databento files ([experiments guide](https://doc.dvc.org/user-guide/experiment-management), Excerpt).

**Literature.**

- [arxiv-mcp-server](https://github.com/blazickjp/arxiv-mcp-server) (3,221 stars, 2026-10-08, Excerpt; README read in part). Local; reads papers one LaTeX section at a time, exports BibTeX, keeps topic watches on disk. Install from PyPI (`uvx arxiv-mcp-server`); an unrelated npm package has the same name.
- [paper-search-mcp](https://github.com/openags/paper-search-mcp) (2,850 stars, 2026-10-02, Excerpt). 20+ sources including Semantic Scholar, OpenAlex, RePEc and **SSRN** (discovery through OpenAlex metadata, best-effort public PDFs, no bypass of login). It also offers optional Sci-Hub workflows: keep those off.
- SSRN itself has no API or MCP server found. Jina's hosted `search_ssrn` is a search wrapper ([Glama](https://glama.ai/mcp/servers/jina-ai/MCP/tools/search_ssrn), Excerpt).

**Memory.**

- [Official memory server](https://github.com/modelcontextprotocol/servers/blob/main/src/memory/README.md) (Excerpt): entities, relations and observations in one JSONL file, with a lock for concurrent writers.
- [Graphiti MCP](https://github.com/getzep/graphiti/blob/main/mcp%5Fserver/README.md) (31,815 stars, Excerpt): a temporal graph in which each fact has a validity window, and old facts are invalidated, not deleted. It needs Neo4j or FalkorDB and an LLM key for extraction.
- [basic-memory](https://github.com/basicmachines-co/basic-memory) (4,245 stars, AGPL, Excerpt): Markdown notes with wikilinks, Obsidian-compatible, local-first; tools carry read-only and destructive hints.

For the harness, "what was tried" must live in the trial ledger, as exact rows. A fuzzy memory server is for context, such as "Bilal wants the bucket method". Basic-memory fits this vault's format best. Graphiti's validity windows fit facts like "lot size is 75 from date X", but that belongs in a data table.

## 7. MCP design patterns for this harness

The current specification is **2026-07-28** ([spec](https://modelcontextprotocol.io/specification/latest), Full). Two changes from 2025-11-25 matter here. The protocol core is stateless: every request carries its own `_meta`, and there is no session. Tasks moved out of the core into an official extension ([changelog](https://modelcontextprotocol.io/specification/2026-07-28/changelog), Excerpt).

**Long jobs (a backtest).** The Tasks extension, `io.modelcontextprotocol/tasks`, lets a server answer `tools/call` with a task handle (`resultType: "task"`, a `taskId`, `ttlMs`, `pollIntervalMs`) instead of a result ([Tasks spec](https://tasks.extensions.modelcontextprotocol.io/specification/2026-07-28/tasks), Excerpt). The client polls `tasks/get` until status is `completed`, `failed` or `cancelled`; `input_required` means the server needs an answer, given through `tasks/update`. Three rules are useful to us. The server must not return the handle until `tasks/get` can find it (durable creation). A tool result with `isError: true` is a `completed` task, not a `failed` one. Clients should store task IDs durably so that polling resumes after a restart. Client support is the problem: the [client matrix](https://modelcontextprotocol.io/extensions/client-matrix) shows no Tasks column in what I saw, and [canimcp](https://canimcp.dev/feature/tasks.get/) lists Claude Code's support as unknown (both Excerpt). So the backtest server must also expose plain tools (`submit`, `status`, `result`, `cancel`), as cloudQuant's server does, and add Tasks when Claude Code supports it.

**Large data.** A tool result can hold a `resource_link` (a URI plus name and MIME type) that the client fetches only if needed, and `structuredContent` that conforms to a declared `outputSchema` ([tools spec](https://modelcontextprotocol.io/specification/2026-07-28/server/tools), Full). So a chain query returns a handle, a short summary (rows, time range, missing minutes) and a link to a Parquet file, never the rows. Two servers show the follow-up: Massive stores a result as a SQL table (`store_as`) for later `query_data` calls, and dbn-go caches Parquet and answers SQL with a row cap. The spec's guidance on stateful tools says the same: return an explicit, opaque handle (UUIDv4), state its lifetime in the tool description, and return a clear error when it has expired.

**Budget and permission on the server side.** The prompt is not a control; the server is. Patterns found:

- Separate free and billed tools, and give the billed one a hard cap (dbn-go `--max-cost`, `--read-only`).
- Register write tools only when a flag is set (Delta `DELTA_MCP_MODE=trade`, W&B `read-only`, Kite `EXCLUDED_TOOLS`, Alpaca `ALPACA_TOOLSETS`).
- Caps per call (tastytrade `MAX_ORDER_NOTIONAL_USD`, Deribit `DERIBIT_MAX_NOTIONAL_USD`).
- Let the credential be the boundary (MotherDuck read-scaling token, Postgres read-only role, Delta Read Data key).
- The tool list "MAY vary by the authorization presented on the request" ([tools spec](https://modelcontextprotocol.io/specification/2026-07-28/server/tools)). So the skeptic role can get a token that sees only read tools.
- A tool can answer `input_required` with an elicitation form, which asks the human before it continues (multi round-trip requests, same page). For our settled decision 1 the server refuses at the cap with `isError: true` and a clear message; asking a human to raise a cap is optional.
- The spec says servers MUST rate-limit tool calls and clients SHOULD log tool usage for audit.

**Every tool call as a trial record.** No server found does this. Two layers will do it. First, inside our servers: each call that touches data or runs a backtest writes one row to the ledger before it returns (inputs, data hash, code commit, result hash, cost), and the ledger has no delete or update tool. Second, a backstop in the client: Claude Code hooks see every MCP call as `mcp__<server>__<tool>`, a `PreToolUse` hook can block a call (exit code 2), and `PostToolUse` can log it ([hooks docs](https://code.claude.com/docs/en/hooks), Fetch, first 100k characters only). The hook catches calls a server forgot to record. MCP's own logging utility sends messages to the client; it is not a durable store.

**Local security.** The official guide's rule: treat a third-party local server "as untrusted code with exactly the privileges you hand it" ([local server security](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/local-server-security.md), Full). It means: pin versions (`uvx` pins only the top package; a container digest pins all), run third-party servers in a container with only the needed folder mounted, give each server its own narrow key through per-server config, deny network where none is needed, and read each tool description, because descriptions are instructions the model reads (tool poisoning) and can change after approval. It adds that every server shares the model's context, so a bad one can steer the use of the others. Keep the roster small.

## 8. Proposed server map for our harness — PROPOSAL

> **This is a proposal for discussion, not a decision.** Tool names are illustrative. Nothing is built.

Reuse (pinned, in containers, read-only where possible):

| Server | Role in harness | Settings |
|---|---|---|
| arxiv-mcp-server | Idea scout: papers | Local storage path in the research folder |
| paper-search-mcp | Idea scout: SSRN, Semantic Scholar, RePEc | Sci-Hub off; `SEMANTIC_SCHOLAR_API_KEY` optional |
| mcp-server-motherduck | Ad hoc SQL over our Parquet, phase 1 only | Read-only, data folder mounted, `--max-rows`, `--query-timeout` |
| jupyter-mcp-server | Report notebook, run top to bottom | Docker sandbox variant; no secrets in the container |
| MLflow MCP (`ml` group) | Read-only view of runs, if we mirror the ledger to MLflow | Read access only |
| basic-memory (or plain vault files) | Context memory for agents | Points at a harness notes folder, not the vault root |
| Kite MCP (hosted) | Live NIFTY quotes for a daily chain capture, later | Hosted copy has no trading tools |
| delta-exchange-mcp | Later crypto lane | No key, or Read Data key only |

Optional paid cross-checks, not v1: Theta Data (recompute check of our SPXW IV and Greeks), ORATS (outside benchmark), QuantConnect (second engine on SPXW; strip live and notification tools).

Write ourselves:

**1. `chain-data` — SPXW over our Databento files.** Reads the OPRA `cbbo-1m` and `definition` files we already hold; the downloader and its cost ledger are `convex-hedge-strategy/scripts/databento_download.py` and `data/databento-ledger.json` (per the 8 Oct capture). Tools:

- `list_sessions(start, end)` — trading days held, with half days flagged
- `get_chain(date, time, expiry, strike_window)` → handle + summary + Parquet link
- `get_surface(handle)` — IV and Greeks recomputed at mid, forward from put-call parity
- `data_quality(date)` — crossed, locked, stale and zero-bid quotes, missing minutes
- `query(handle, sql, max_rows)` — DuckDB over a handle
- `estimate_pull(range)` (free) and `pull(range)` (billed; hard cap read from the ledger; `$0` inside 12 months, refused above the cap)

**2. `nifty-data` — NIFTY weekly and monthly.** Tools:

- `list_expiries(underlying, start, end)` — the expiry calendar by date
- `lot_size(underlying, date)` and `holidays(year)`
- `get_rolling_options(underlying, expiry_flag, strike_offset, side, start, end)` — Dhan expired options (key `DHAN_ACCESS_TOKEN`, with `DHAN_CLIENT_ID`)
- `capture_chain(underlying)` — daily snapshot from a live source into our own store, so we stop depending on brokers for history
- `get_chain(date, time, expiry)` and `data_quality(date)`, as in `chain-data`

**3. `feature-lab` — the feature library.** Tools:

- `list_features()`, `describe_feature(name)` — definition, inputs, the time each value is known
- `compute_feature(name, handle, params)` → handle
- `bucket_test(feature, target, handle)` — Bilal's bucket method, day-level reshuffle p-value
- `feature_importance(handle, method)` — MDI, MDA, SFI (AFML ch. 8)
- `propose_feature(spec)` — writes a draft with tests for human review; never registers itself

**4. `backtest-lab` — runs and splits.** Tools:

- `prepare_run(strategy, params, dataset, cost_model, fill_model)` → plan ID, checked against budget
- `start_run(plan_id, idempotency_key)` → job ID (a Task when the client supports it)
- `run_status(job_id)`, `run_result(job_id)` (summary + resource links), `cancel_run(job_id)`
- `make_splits(dataset, method, k, embargo)` — purged k-fold, CPCV (AFML ch. 7, 12)
- `compare_runs(run_ids)` — the difference between two runs on one engine
- Server-side caps: concurrent jobs, wall time, and company lab compute

**5. `trial-ledger` — append-only record of every trial.** Tools:

- `open_study(hypothesis, payer, kill_line, data_split)` — the claim written before data is opened
- `record_trial(study_id, run_id, …)` — called by the other servers, not by agents
- `list_trials(study_id)`, `count_trials(study_id)`
- `deflated_sharpe(study_id)`, `pbo(study_id)` (AFML ch. 11, 14)
- `budget_status()` — spend so far against each cap
- `close_study(study_id, verdict, reason)`
- No delete or update tool; each row carries the hash of the row before it

Each of the five servers gets a read-only token profile for the skeptic role.

## What to take for our harness

1. **Write `trial-ledger` first.** Nothing found records trials; the AFML statistics (deflated Sharpe, PBO) depend on an honest count, so the ledger must be append-only and fed by the servers.
2. **Write `chain-data` over our own Databento files.** No server reads `cbbo-1m`; dbn-go's shape (free discovery, one billed tool with a hard cap, Parquet cache, SQL with a row cap) is the model.
3. **Copy cloudQuant's run lifecycle for `backtest-lab`**: immutable datasets, prepare → start → status → result, idempotency keys, no arbitrary code. Add the Tasks extension later; Claude Code support is unknown.
4. **Put NIFTY history on Dhan's expired options API** in our own `nifty-data` server, and start a daily chain capture now; check the Data Plan price and whether quotes (bid, ask) exist.
5. **Return handles and resource links, never rows.** Use `structuredContent` with an `outputSchema` for summaries.
6. **Enforce limits in servers and credentials, not prompts**: tool lists by token role, caps per call, read-only roles, a `PreToolUse` hook as backstop.
7. **Reuse arxiv-mcp-server and paper-search-mcp** for the idea scout, with Sci-Hub off.
8. **Run every third-party server pinned and in a container**, and keep the roster small.

## Sources I could not reach or did not read

- Firecrawl was down; not used, as the brief said.
- Dhan's native MCP tool list: not found on the docs page I saw.
- Prices not checked: Theta Data, Massive, Dhan Data Plan, Kite Connect.
- Datadog Security Labs' Postgres post: seen only through a secondary blog.
- Claude Code hooks page: read to 100k of 270k characters; the `PostToolUse` input schema was not confirmed.
- NSE terms of use for automated access: not read.
- Whether Claude Code supports the MCP Tasks extension: not found; listed as unknown.
