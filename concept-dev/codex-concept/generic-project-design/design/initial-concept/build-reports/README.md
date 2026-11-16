<!--
  generic-project-design | design/initial-concept/build-reports/README.md
-->

# Build reports — template design sessions

One report per session, **without exception** — including sessions that
produce only decisions. The console corpus is emphatic about this
(*"a scoping-only or decision-only session still reports what was decided and
why"*), and its 66 reports are the reason a six-week-old choice can still be
traced to the session that made it.

**Naming:** `YYYYMMDD-<slug>.md`, where `<slug>` matches the prompt file name
minus its numeric prefix.

## Shape

```markdown
---
date: YYYY-MM-DD
prompt: prompts/NNN-<slug>.md
decides: [D-NN, ...]
---

# YYYYMMDD — <title>

## What this session did
## Decisions made        ← with the reasoning, not just the outcome
## What was measured     ← real numbers, and how they were obtained
## What changed on disk  ← file by file
## What was deliberately left out
## Gaps / follow-ups     ← or "none, explicitly"
## Next
```

The last two sections are the ones that get skipped and the ones that matter
most later. "No gaps found" must be stated, never left implicit — otherwise a
silent section and an unexamined one are indistinguishable.

## Reports

| Date | Session | Report |
|---|---|---|
| 2026-08-18 | Initial concept — directory structure, console inventory, open questions | [20260818-initial-concept.md](20260818-initial-concept.md) |
