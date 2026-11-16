---
date: 2026-08-18
prompt: none — direct researcher request
decides: []
---

<!--
  generic-project-design | design/initial-concept/build-reports/20260818-initial-concept.md
-->

# 20260818 — Initial concept

## What this session did

Created `/workspaces/generic-project/` with its three folders, and wrote the
initial concept for a reusable two-repo project template for AI-led
development. No decisions were made — the deliverable is the agenda plus the
evidence to decide against.

## What was measured

All figures taken from `/workspaces/strategy-lab-console` on 2026-08-18 by
direct inspection, not recall:

| Finding | Measurement |
|---|---|
| `governance/UI_STATE.md` | 339 KB, 4,556 lines, 6 `##`, **0 `###`**; 3,777 lines under one heading |
| `governance/screens/run_panel.md` | 147 KB — **50×** its own `_TEMPLATE.md`, which says "keep it short" |
| `governance/screens/config_studio.md` | 140 KB |
| `.notes/gaps/console-gaps.md` | 181 KB, 2,935 lines, flat append-only |
| `.notes/` version control | 194 of 463 files tracked; `.notes/` in **both** `.gitignore` and `.claudeignore` |
| `CLAUDE.md` drift | "Current phase: Setup / scaffolding" vs 10 screen contracts marked `built`; directs every session to `governance/STATE.md` and `.notes/build-reports/IMPLEMENTATION_HISTORY.md`, **neither of which exists** — and `VIBE_SESSION_PROTOCOL.md:202` says so outright |
| Competing "what's next" pointers | 3 (`.wolf/STATUS.md`, `UI_STATE.md:3907`, `package004/PLAN.md` §1) |
| Contract mirror | 11 of 18 files 6 weeks stale, no sync record, found by accident |
| Format overhead, 3 records | md-table 90% · YAML 100% · JSON 123% · XML 141% |

The last row is the basis for the claim that format choice should not be
driven by token cost — the spread is too small to matter next to a 181 KB
file being loaded at all.

## Decisions made

**None, deliberately.** Fourteen are staged in
[`../docs/06-open-questions.md`](../docs/06-open-questions.md) with options
and a lean on each. Prompt `001` runs them.

## What changed on disk

```
/workspaces/generic-project/
├── README.md                                  ← the parent container's purpose
├── generic/README.md                          ← placeholder, intentionally empty repo
├── generic-dev/README.md                      ← placeholder, intentionally empty repo
└── generic-project-design/
    ├── README.md
    └── design/initial-concept/
        ├── README.md                          ← the concept + reading order
        ├── PROMPT-TRACKER.md                  ← dogfoods the tracker mechanism
        ├── docs/01-naming-and-repo-topology.md
        ├── docs/02-console-approaches-inventory.md
        ├── docs/03-what-broke-measured.md
        ├── docs/04-file-formats-for-ai-readers.md
        ├── docs/05-proposed-structure.md
        ├── docs/06-open-questions.md
        ├── docs/07-instantiation-checklist.md
        ├── prompts/README.md
        ├── prompts/001-decide-topology-and-formats.md
        ├── prompts/002-build-the-check-suite.md
        └── build-reports/README.md + this file
```

Nothing in `/workspaces/strategy-lab-console` was modified by this session.

## What was deliberately left out

- **`generic/` and `generic-dev/` are empty** (README placeholder only).
  Populating them would prejudge D-01…D-04.
- **No `init.sh` or `template.yml`.** The token contract is specified in
  `docs/07`; writing the script before the tree is decided would be writing
  it twice.
- **Directories are `generic/` / `generic-dev/`, not `{{PROJECT}}/`.** As
  requested. `docs/07` §1 flags the conversion to token-form names as part of
  the session that populates them, and explains why bare-word substitution is
  the main instantiation risk.
- **No opinion recorded on whether `strategy-lab-console` should be
  retrofitted.** It is a live project; that is a separate call.

## Gaps / follow-ups

1. **The 17-mechanism inventory in `docs/02` is not prioritised beyond a
   top-five.** If the scaffold gets large, that list is where to cut.
2. **D-05 (family-shared material) has no good answer yet.** The lean —
   per-project copies plus a version stamp — is the least-bad option, not a
   satisfying one. Worth revisiting at 3+ projects.
3. **`docs/04` §5's front-matter pattern is asserted from one working
   example** (the agent-memory directory). It has not been tried at
   project-corpus scale. Prompt `002` is where it either holds or does not.
4. **Nothing here is under version control yet.** `/workspaces/generic-project`
   has no `.git`, by design — but that means this concept currently has the
   same durability problem the concept itself is about. Worth a `git init` on
   `generic-project-design/` early even though it is never published.

## Next

Prompt `001` — decide topology, state location, sync, and format rules.
