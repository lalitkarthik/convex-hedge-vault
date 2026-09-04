# Raw research output — do not edit

Agent reports behind the trading-landscape research pass, 2026-08-28.
Kept verbatim as evidence. The synthesised PDF is the deliverable; this is its source.

## Round one — complete (9 agents + critic)
landscape · vol-surface-to-trade · regime-and-strategy · backtest-and-data ·
crypto-strategies · crypto-plumbing · practitioners · income-base-rates · social-sweep
`_critique.md` — completeness critic: gaps, contradictions, unverified claims.

## Round two — 3 of 6 complete (process exited mid-run)
Done: books-attribution-and-video · crypto-options · verify-load-bearing-claims
Not done: india-craft-and-primary-docs · india-tax-and-margin · hedging-rv-sizing

Resume (same session only): runId `wf_bbe90f2e-dcb`
Script: `.claude/projects/D--second-brain-convex-hedge-vault/c7038c05-.../workflows/scripts/trading-research-round-two-wf_bbe90f2e-dcb.js`
A new session must re-run the three missing agents from that script.


## The deliverable

`../trading-research-map.pdf` (75 pp) and its source `../trading-research-map.tex`.
Built with XeLaTeX; aux files stripped with `latexmk -c`.

## Build notes for the PDF
XeLaTeX (pdfLaTeX lacks the rupee glyph). Fonts: Cambria / Segoe UI / Consolas.
`latexmk -xelatex` then `latexmk -c`. Never name the build log `<jobname>.out` —
it collides with hyperref's bookmark file.
