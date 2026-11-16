---
id: 20260819-decide-topology-and-formats
prompt: 001-decide-topology-and-formats
date: 2026-08-19
status: closed
validated:
  - required-docs-read
  - decisions-written
  - structure-updated
---

# Build Report: Decide Topology and Formats

## Summary

Prompt `001` was run as a decision session. It closed D-01 through D-05 and
D-09 through D-11, updated the accepted project/dev structure, and preserved
the newer requirement that governance files should be updated to current
accepted meaning rather than accumulating ambiguous amendment-only sections.

## Decisions Closed

| Decision | Result |
|---|---|
| D-01 | Always use a parent container, normally `<family>-suite/`; the parent is not a git repo. |
| D-02 | Keep the `-dev` suffix and require the first line of `<project>-dev/README.md` to define what the repo is not. |
| D-03 | Split current state: generated capped `STATUS.md` in the product repo, detailed state/history in the dev repo. |
| D-04 | Use `SYNC.yml` plus a machine check for cross-repo mirrors; do not use submodules in the baseline template. |
| D-05 | Use per-project copies of shared material with template version stamping and drift checks. |
| D-09 | Store gaps as one YAML record per file, with generated indexes. |
| D-10 | Generate the baseline views: `QUEUE.md`, `STATUS.md`, capability views, routing views, gap indexes, and build-report indexes. |
| D-11 | Validate small schemas for prompts, build reports, gaps, ADRs, specs, contracts, unit contracts, and work packages. Prompts declare `touches`. |

## Files Changed

- `docs/06-open-questions.md`: wrote accepted answers for D-01 through D-05
  and D-09 through D-11.
- `docs/05-proposed-structure.md`: converted the document from a proposal to
  the accepted baseline structure, added indexes, added specs, added schema
  expectations, and updated the check-suite list.
- `prompts/002-build-the-check-suite.md`: updated section references after
  the accepted-structure renumbering.
- `PROMPT-TRACKER.md`: prompt `001` was marked in progress at session start
  and closed at session end.

## Validation

- Read the mandatory concept, evidence, structure, open-question, format, and
  design-brief documents before deciding.
- Searched the touched prompt/docs for stale `open`, `Status: proposal`, and
  amendment-oriented wording in the decided areas.
- Confirmed prompt `002` now points at the accepted check-suite and budget
  sections.

## Follow-Up

Prompt `002` is now the next runnable prompt. It should decide or confirm
D-06, D-07, D-08, D-12, and D-13, then build the governance check suite
against fixtures.
