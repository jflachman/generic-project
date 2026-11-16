<!--
  generic-project-design | design/initial-concept/docs/06-open-questions.md
  The working agenda. Answers get written back into the table cells, dated,
  the way strategy-lab-console's PLAN.md decision tables do (see 02 §C3).
-->

# 06 — Open questions

Fourteen decisions. Each has options, lean, and accepted answer when decided.
The first four are load-bearing — the tree in
[`05-proposed-structure.md`](05-proposed-structure.md) changes shape
depending on the answers. The rest are tuning.

Status values: `open` · `decided` · `deferred` · `dissolved`.

---

## Topology

### D-01 — Does a single-product family need the parent folder? · `decided`

| Option | |
|---|---|
| Always | Uniform; costs one wrapper folder for a one-repo project |
| Only for families of 2+ | Less nesting when it buys nothing |

**Decision, 2026-08-19: always use a parent container.** The `-dev` sibling
means there are never fewer than two repos, so the parent always groups
something. Use `<family>-suite/` for real projects when the family name is
known. The parent is a filesystem container, not a git repo, and is never
published.

### D-02 — Is `-dev` the right suffix? · `decided`

Alternatives: `-ai`, `-notes`, `-build`, `-coord`. Cost of changing later
scales with the number of repos and every cross-reference in both corpora.
**Decision, 2026-08-19: keep `-dev`.** The suffix is short, sorts adjacent to
the product repo, and is already the intended convention. Pay for the possible
ambiguity with the first line of `<project>-dev/README.md`: it must state
that the repo contains no application code and is the AI-coordination corpus,
not a development branch, environment, or fork.

### D-03 — Which repo holds current state? · `decided`

| Option | Trade |
|---|---|
| All state in `-dev/` | Clean churn separation; a GitHub visitor to `<project>/` cannot tell what works |
| All state in `<project>/` | State commits with the code that changed it; reimports the 339 KB bloat risk |
| **Split: generated `STATUS.md` (cap ~80 lines) in `<project>/`, full history in `-dev/`** | Two places, but only one is authored |

**Decision, 2026-08-19: split current state.** `<project>/STATUS.md` is a
small generated consumer-facing snapshot with links only and a hard line cap.
Full session history, package state, build reports, and detailed work status
live in `<project>-dev/`. The product repo must not contain authored mutable
session history.

### D-04 — What is the sync mechanism across the repo boundary? · `decided`

The split creates exactly the boundary that rotted six weeks in the console
([`03`](03-what-broke-measured.md) §7). Options: a `SYNC.yml` pin plus a
check script; git submodules; a CI job in each repo that verifies the other's
last-known ref; or nothing (accept drift).

**Decision, 2026-08-19: use `SYNC.yml` plus a check script.** Any mirrored or
duplicated cross-repo artifact must ship with an upstream path/ref/date entry
and a machine check in the same change that creates the mirror. Do not use
submodules for the baseline template; they solve pinning but add operational
friction to ordinary sessions.

### D-05 — How is family-shared material handled? · `decided`

The protocol, format rules, and lint script are identical across
`<project>-dev` repos in a family; today each of strategy-lab / console /
charts carries its own drifting copy.

Options: per-project copies (simple, drifts), a `<family>-suite-dev/` shared
repo (one source, another sync boundary), a submodule, or a published package
the check script installs.

**Decision, 2026-08-19: per-project copies with a version stamp and drift
check.** Each instantiated project carries its own protocol, format rules, and
check suite. A `TEMPLATE_VERSION` or equivalent manifest records the template
version, and `check-governance` flags divergence from the expected family
version when that reference exists. Revisit a shared repo or package only
after there are at least three active projects with repeated shared updates.

---

## Size and rot

### D-06 — Does the constitution contain zero mutable state? · `decided`

**Decision, 2026-08-20: yes, and enforce it.** `CLAUDE.md` and `AGENTS.md`
contain only stable constitution text and pointers. They must not contain
"current phase", active status, work queues, session history, or equivalent
mutable state. `check-governance` enforces this with the
`mutable-state-in-constitution` and `relative-links` checks.

### D-07 — What are the actual budget numbers? · `decided`

**Decision, 2026-08-20: start strict and encode the numbers as data.** Hot
files are capped at 200 lines and 20,000 bytes. Warm governance files are
capped at 500 lines and 80,000 bytes. Cold files are uncapped but must be
indexed. No `##` section may exceed 150 lines unless it contains a `###`
subheading. Sync pins must be checked within 45 days. These values live in
`generic/scripts/governance-budgets.json`, not as literals in checker code.

### D-08 — What triggers rotation, and where does content go? · `decided`

**Decision, 2026-08-20: use all three triggers by content type.** State
rotates on a schedule into `state/YYYY-QN.md`. Issue records rotate by status:
closed or superseded records move to `archive/` when retention is still
needed. Other governed files rotate or split when `check-governance` budget
or section checks fail. Every move appends to `archive/MANIFEST.yml` so
archiving remains retention, not deletion.

---

## Formats

### D-09 — Do issue logs become one YAML record per file? · `decided`

**Decision, 2026-08-19: yes, with typed issue records.** Gaps, deferred
items, bugs, and upstream requests are separate one-file YAML records under
`issues/`, with prefixes `GAP`, `DEF`, `BUG`, and `REQ`. Generated indexes
provide active, blocked, planned, verified, and closed views. Long
explanatory prose belongs in fields only when needed, not in one growing
markdown log.

### D-10 — Which files are generated, and how is hand-editing prevented? · `decided`

Proposed generated set: `QUEUE.md`, `STATUS.md`, the capability and routing
markdown views, the gap index, the build-report index.

**Decision, 2026-08-19: generate all six baseline views.** `QUEUE.md`,
`STATUS.md`, capability markdown views, routing markdown views, gap indexes,
and the build-report index are generated. Each generated file must carry a
`DO NOT EDIT - generated from ...` banner, and `check-governance` must fail
when regeneration would produce a diff.

### D-11 — What is the front-matter schema set? · `decided`

Needed for: prompt, build report, gap record, ADR, unit contract, work
package. Keep the field sets small and boring, and validate them in the lint
script — a schema nobody validates is a comment.

**Decision, 2026-08-19: define small validated schemas for each governed
record type.** Required schemas: prompt, build report, issue record, ADR,
spec, contract, unit contract, and work package. Prompt front matter includes
`touches: [paths]` so the generated queue can flag likely collisions.
Markdown files use YAML front matter for queryable metadata and prose bodies
for rationale. YAML record files use schema-validated keys only. A schema that
is not enforced by `check-governance` is not part of the governance contract.

### D-12 — What exactly does the check suite cover, and where does it run? · `decided`

**Decision, 2026-08-20: cover every baseline check in
[`05`](05-proposed-structure.md) §5 and run it locally at session close, then
in CI once the scaffold exists.** The first executable form is
`generic/scripts/check-governance.py`, with a PowerShell wrapper at
`generic/scripts/check-governance.ps1`. Each check is independently runnable,
and the test fixture proves the suite fails non-zero before there is a real
scaffold to validate.

---

## Process

### D-13 — Is there exactly one queue, and is it generated? · `decided`

**Decision, 2026-08-20: yes to both.** `QUEUE.md` is the only ordered run
queue and is generated from prompt front matter. Other files may point to it
but must not contain competing queue content. The design project's
hand-maintained `PROMPT-TRACKER.md` remains a dogfooding bridge only until
the scaffold generation session replaces it with the generated queue.

### D-14 — How does a session learn all this, given two repos? · `decided`

An agent starts in one working directory. Both repos must be mounted, and the
constitution in `<project>/CLAUDE.md` must point into `<project>-dev/` for
the protocol and queue. Options: a workspace file mounting both; a
`.claude/settings.json` with the sibling path; a symlink; or a
`<project>-dev/CLAUDE.md` that mirrors the pointer for sessions started on
that side.

**Decision, 2026-08-20: both repos carry a small `CLAUDE.md` that points at
the other, and both repos must be mounted as siblings in the same parent
workspace.** Sessions that start in `generic/` read `generic/CLAUDE.md`, which
points to `../generic-dev/PROTOCOL.md` and `../generic-dev/QUEUE.md`.
Sessions that start in `generic-dev/` read `generic-dev/CLAUDE.md`, which
points back to `../generic/CLAUDE.md`. Do not use a symlink for the baseline
template, and do not reproduce the `.claudeignore` line `**/.notes/` or any
equivalent exclusion for the coordination corpus.

---

## How to use this file

Answer in place, in the section, with a date — do not open a second document.
When an answer dissolves a later question, strike the question through and
say what dissolved it rather than deleting it (the console's `D-F` row is the
model). Then record the session in `../build-reports/`.
