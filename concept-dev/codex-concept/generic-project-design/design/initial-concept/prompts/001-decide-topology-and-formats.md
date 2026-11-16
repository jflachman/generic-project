---
id: 001
title: Decide topology, state location, sync, and the format rules
status: closed
depends_on: []
decides: [D-01, D-02, D-03, D-04, D-05, D-09, D-10, D-11]
touches:
  - ../../../docs/two-repo-governance-and-dev-design.md
  - design/initial-concept/docs/06-open-questions.md
  - design/initial-concept/docs/05-proposed-structure.md
---

<!--
  generic-project-design | design/initial-concept/prompts/001-decide-topology-and-formats.md
-->

# 001 — Decide topology, state location, sync, and the format rules

## Goal

Answer the eight load-bearing open questions listed in this file's
`decides:` front matter, in conversation with the researcher, and write each
answer back into [`../docs/06-open-questions.md`](../docs/06-open-questions.md)
in place with a date. Then update
[`../docs/05-proposed-structure.md`](../docs/05-proposed-structure.md) so the
proposed tree reflects what was decided.

**This is a decision session. It writes no scaffold.**

## What this session is NOT

- **Not populating `generic/` or `generic-dev/`.** That is prompt `003`, and
  it is gated on the check suite (prompt `002`) existing first — see
  [`../docs/06-open-questions.md`](../docs/06-open-questions.md) D-12.
- **Not writing `init.sh`.** Instantiation mechanics are settled enough in
  [`../docs/07-instantiation-checklist.md`](../docs/07-instantiation-checklist.md)
  to defer.
- **Not re-deciding what is already measured.** The seven failures in
  [`../docs/03-what-broke-measured.md`](../docs/03-what-broke-measured.md)
  are facts about a real repo. Argue with the *response* to them, not the
  measurements.

## Mandatory reading

1. [`../README.md`](../README.md) — the concept and its three core questions
2. [`../../../docs/two-repo-governance-and-dev-design.md`](../../../docs/two-repo-governance-and-dev-design.md) — the current high-level intent to preserve
3. [`../docs/03-what-broke-measured.md`](../docs/03-what-broke-measured.md) — read in full; it is the evidence base
4. [`../docs/05-proposed-structure.md`](../docs/05-proposed-structure.md) — the proposal being argued with
5. [`../docs/06-open-questions.md`](../docs/06-open-questions.md) — the agenda
6. [`../docs/04-file-formats-for-ai-readers.md`](../docs/04-file-formats-for-ai-readers.md) — only §3 and §5 are needed for D-09/D-10/D-11

Do **not** read `02-console-approaches-inventory.md` in full unless a
specific mechanism is under discussion — it is reference, not agenda.

## Preconditions

None. This is the first session.

## Deliverables

1. D-01 … D-05, D-09 … D-11 each marked `decided` (or explicitly `deferred`
   with the reason) in `06-open-questions.md`, dated.
2. `05-proposed-structure.md` updated to match the accepted design. Keep
   decisions traceable, but do not leave contradictory amendment blocks that
   make the final governance meaning ambiguous. The current accepted tree and
   rules should read as the canonical answer.
3. If any answer creates new work, add a prompt file and put it in the
   tracker.

## Close-out

Build report at `../build-reports/YYYYMMDD-decide-topology-and-formats.md`.
Mark this prompt `closed` in the front matter and in
[`../PROMPT-TRACKER.md`](../PROMPT-TRACKER.md), and remove it from the
ordered queue.
