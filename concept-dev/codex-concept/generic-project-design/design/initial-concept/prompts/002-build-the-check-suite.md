---
id: 002
title: Build the governance check suite before any scaffold exists
status: closed
depends_on: [001]
decides: [D-06, D-07, D-08, D-12, D-13]
touches:
  - generic/scripts/
---

<!--
  generic-project-design | design/initial-concept/prompts/002-build-the-check-suite.md
-->

# 002 — Build the governance check suite before any scaffold exists

## Goal

Confirm or decide D-06, D-07, D-08, D-12, and D-13, then write
`check-governance` — the executable form of every invariant in
[`../docs/05-proposed-structure.md`](../docs/05-proposed-structure.md) §5 —
and prove it runs, before there is a project for it to check.

Building the checker first is deliberate and is the central bet of this whole
template: **[`../docs/03-what-broke-measured.md`](../docs/03-what-broke-measured.md)
concludes that six of seven measured failures were rules that existed in prose
and nowhere else.** Writing the checker first also forces the front-matter
schemas (D-11) to be concrete rather than aspirational.

## What this session is NOT

- **Not populating the scaffold.** The checker is written against the
  *decided* tree, and run against fixtures.
- **Not a CI setup session.** Wire the workflow file if it is cheap; the
  deliverable is a script that runs locally and exits non-zero correctly.
- **Not a linter for source code.** This checks the governance corpus only.

## Mandatory reading

1. [`../docs/05-proposed-structure.md`](../docs/05-proposed-structure.md) §5 and §6 — the baseline checks and the tier budgets
2. [`../docs/06-open-questions.md`](../docs/06-open-questions.md) D-06 … D-08, D-12, D-13 — the decisions this prompt must close or explicitly defer
3. [`../../../docs/two-repo-governance-and-dev-design.md`](../../../docs/two-repo-governance-and-dev-design.md) — the index, update, and generated-view expectations
4. Prompt `001`'s build report — topology and schema decisions are authoritative over the proposal docs

## Preconditions

Prompt `001` is `closed` and its decisions are written into
`06-open-questions.md`. **If D-03 or D-11 is still `open`, stop** — the
checker cannot validate a schema that does not exist yet.

The accepted structure must also preserve the direction in
[`../../../docs/two-repo-governance-and-dev-design.md`](../../../docs/two-repo-governance-and-dev-design.md):
indexes are required, generated status/queue files are not hand-authored, and
governance files are updated to their current accepted meaning rather than by
ambiguous amendment-only sections.
The accepted structure also uses `issues/` rather than a broad `gaps/` bucket:
`GAP`, `DEF`, `BUG`, and `REQ` records share a schema style but keep distinct
meanings.

## Deliverables

1. `check-governance` with the baseline checks, each independently runnable
   and each with a fixture that makes it fail.
2. Budget numbers from D-07 encoded as data, not literals in code.
3. A short `README` documenting each check and, for each, **the measured
   failure it exists to prevent** — the "rules with a scar" mechanism from
   [`../docs/02-console-approaches-inventory.md`](../docs/02-console-approaches-inventory.md) §B5.
4. Exit-code contract documented, so the session-close step can call it.
5. A fixture or test that proves amendment-only governance drift is rejected
   when it leaves contradictory active meanings in one file.
6. A fixture or test that proves issue records fail when their `type`, id
   prefix, and folder disagree.

## Close-out

Build report at `../build-reports/YYYYMMDD-build-the-check-suite.md`.
Update the tracker at both ends.
