---
id: 004
title: Build instantiation tooling
status: queued
depends_on: [003]
decides: []
touches:
  - generic/
  - generic-dev/
  - generic-project-design/design/initial-concept/docs/
---

<!--
  generic-project-design | design/initial-concept/prompts/004-build-instantiation-tooling.md
-->

# 004 — Build instantiation tooling

## Goal

Create the first mechanical instantiation path for copying this template into
a real project family without interpreting project-specific prose by hand.

## Mandatory reading

1. [`../docs/07-instantiation-checklist.md`](../docs/07-instantiation-checklist.md)
2. [`../docs/05-proposed-structure.md`](../docs/05-proposed-structure.md)
3. Prompt `003`'s build report
4. `generic/scripts/README.md`

## Preconditions

Prompt `003` is closed, D-14 is decided, and `check-governance` passes against
the real `generic/` and `generic-dev/` scaffold.

## Deliverables

1. Add a template manifest or equivalent token contract for `generic`,
   `generic-dev`, and `generic-project`.
2. Add a local instantiation script or documented command path that copies the
   parent template, deletes `generic-project-design/`, renames both child
   repositories, and replaces placeholder tokens.
3. Include dry-run or fixture coverage where practical.
4. Run `check-governance` after any scaffold changes.
5. Build report at `../build-reports/YYYYMMDD-build-instantiation-tooling.md`.

## Close-out

Update the tracker at both ends and leave the next prompt queued or explicitly
state that the initial design sequence is complete.
