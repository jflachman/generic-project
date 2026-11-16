<!--
  project-A-design | README.md
-->

# project-A-design — the design conversation for the three-repo template

**This folder is a container for a design conversation, not a template and not
a repository.** It has no `.git` of its own. It exists so this session's
concept work sits next to the prior generation (`codex-concept/`) and the
future scaffold (`claude-concept/`) on disk.

## Relationship to the other top-level folders

| Folder | Role |
|---|---|
| `codex-concept/` | The **previous generation** of this design — a two-repo template (`generic/` + `generic-dev/`), built with Codex. Treated here as prior art: several of its conclusions (file-format rules, tiering, the check-suite philosophy, the prompt/build-report process) carry forward unchanged. Others (governance living inside the product repo, single-project scope, one implicit agent) are being revisited. |
| `project-A-design/` (this folder) | **The new design conversation**, for the three-repo template: `project-A`, `project-A.ai`, `project-A.gov`. |
| `claude-concept/` | Where the actual `project-A` / `project-A.ai` / `project-A.gov` scaffold will be built, once enough of this conversation is settled. Empty today, on purpose. |
| `ref-docs/` | Road-tested process documents from a real project (Strategy-Lab Console), extracted as portable reference. Not written for this effort, but several mechanisms here — the prompt-tracker/history split, the vibe-session protocol — are adopted almost directly. |

## Start here

[`docs/concept.md`](docs/concept.md) — the concept document: repo topology,
the purpose of each repo, governance structure and bloat prevention, the
`.ai` repo's operating workflows, and the multi-agent-role architecture.

[`docs/open-questions.md`](docs/open-questions.md) — the working agenda.
Genuine decisions that shape the design, each with options and a recommended
lean, left open for the developer to answer. Mirrors the pattern that worked
in `codex-concept/generic-project-design/design/initial-concept/docs/06-open-questions.md`.

## Status

Draft, 2026-08-20. First pass — written to give the developer something
concrete to react to before the next round of design work.
