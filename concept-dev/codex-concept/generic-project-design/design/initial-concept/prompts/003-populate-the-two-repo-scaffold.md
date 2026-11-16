---
id: 003
title: Populate the two-repo scaffold under checker control
status: closed
depends_on: [002]
decides: [D-14]
touches:
  - generic/
  - generic-dev/
  - generic-project-design/design/initial-concept/docs/
---

<!--
  generic-project-design | design/initial-concept/prompts/003-populate-the-two-repo-scaffold.md
-->

# 003 — Populate the two-repo scaffold under checker control

## Goal

Create the first real `generic/` and `generic-dev/` scaffold from the accepted
structure, with `check-governance` running against the scaffold before close.
Close or explicitly defer D-14.

## Mandatory reading

1. [`../docs/05-proposed-structure.md`](../docs/05-proposed-structure.md) —
   accepted tree, schemas, checks, and tier budgets
2. [`../docs/06-open-questions.md`](../docs/06-open-questions.md) D-14
3. [`../../../docs/two-repo-governance-and-dev-design.md`](../../../docs/two-repo-governance-and-dev-design.md)
4. Prompt `002`'s build report and `generic/scripts/README.md`

## Preconditions

Prompt `002` is closed, D-06 through D-08 and D-12 through D-13 are decided,
and `python -m unittest discover -s generic/scripts/tests` passes.

## Deliverables

1. Populate the accepted product and dev repo trees without adding real
   project-specific code.
2. Generate baseline indexes, `QUEUE.md`, `STATUS.md`, capability/routing
   views, and build-report indexes.
3. Run `check-governance` against `generic/` and `generic-dev/` and fix any
   violations.
4. Decide or defer D-14 in `06-open-questions.md`.
5. Build report at `../build-reports/YYYYMMDD-populate-the-two-repo-scaffold.md`.

## Close-out

Update the tracker at both ends and leave the next prompt queued.
