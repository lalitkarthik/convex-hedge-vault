You are the feature-loop orchestrator. Read `~/.claude/skills/feature-loop/workflow.md` and
`~/.claude/skills/feature-loop/prompts/orchestrator.md`, then start at Startup for feature #265.

Read the hand-off `C:\Users\Acer\AppData\Local\Temp\feature-loop-handoff-orchestrator-iv-vs-rv-20261007-1101.md`
first. Its section "Rules of this repo that replace the feature loop's" and its owner's sections
(Account rule, Parallelism override, Tier rule) override the two files above wherever they
differ; the most important ones are that you open the pull request and never merge it, and that
workers run on accounts `b` and `c` through the account script, never `a`.
