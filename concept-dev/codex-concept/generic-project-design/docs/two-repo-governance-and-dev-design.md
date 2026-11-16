# Two-Repo Governance and Development Design

Status: design brief  
Scope: the reusable `generic` / `generic-dev` project template  
Date: 2026-08-19

This document captures the intended shape of the generic software development
template. The template is meant to be copied for a new project, with
`generic` replaced by the real project name.

## Purpose

The template creates two repositories:

| Repository | Purpose |
|---|---|
| `generic/` | The product repository. It holds source code, tests, durable governance, specs, ADRs, contracts, and generated high-level status that a project consumer or maintainer needs. |
| `generic-dev/` | The development coordination repository. It holds AI collaboration material: design conversations, work packages, prompt plans, vibe sessions, mockups, build reports, issue records, queues, and operational state. |

The working directory `generic-project-design/` is only for designing this
template. It should not ship into instantiated projects.

## Placement Rule

Use this rule when deciding where a file belongs:

> Put consumer-facing truth in `generic/`. Put builder coordination in
> `generic-dev/`.

Examples:

| Artifact | Location | Reason |
|---|---|---|
| Source code and tests | `generic/` | Product behavior. |
| ADRs | `generic/governance/adr/` | Durable design decisions that explain the product. |
| Specs and contracts | `generic/governance/specs/`, `generic/governance/contracts/` | Product interfaces and expected behavior. |
| Generated status summary | `generic/STATUS.md` | Consumer-facing snapshot, but generated and capped. |
| Work packages | `generic-dev/work/` | Builder coordination. |
| Prompt files | `generic-dev/work/<package>/prompts/` | AI execution instructions. |
| Build reports | `generic-dev/build-reports/` | Session evidence and close-out records. |
| Mockups and design explorations | `generic-dev/design/` | Builder/design iteration, not product truth until accepted into governance. |
| Gaps, deferred items, bugs, and upstream requests | `generic-dev/issues/` | Typed work tracking with one shared record pattern. |
| Vibe session protocol | `generic-dev/PROTOCOL.md` | Builder workflow. |

## Governance Structure

The product repo should keep governance small, indexed, and enforceable:

```text
generic/
├── CLAUDE.md
├── AGENTS.md
├── STATUS.md
├── governance/
│   ├── INDEX.md
│   ├── adr/
│   │   ├── INDEX.md
│   │   └── ADR-001-<slug>.md
│   ├── specs/
│   │   ├── INDEX.md
│   │   └── SPEC-001-<slug>.md
│   ├── contracts/
│   │   ├── INDEX.md
│   │   ├── SYNC.yml
│   │   └── <contract>.md
│   ├── units/
│   │   ├── INDEX.md
│   │   └── UNIT-001-<slug>.md
│   ├── capabilities.yml
│   └── ai-reference/
│       ├── routing.yml
│       └── routing.md
├── src/
├── tests/
└── scripts/
    └── check-governance
```

Recommended rules:

- `CLAUDE.md` and `AGENTS.md` are short constitutions and pointers. They must
  not contain mutable state, active queues, or session history.
- `STATUS.md` is generated from governance and dev records. It should be a
  compact current snapshot, not an authored history file.
- Each governance area has an `INDEX.md` or generated index so an AI session
  can discover relevant small files without loading the whole corpus.
- ADRs, specs, contracts, and unit files are updated in place when the
  accepted meaning changes. Do not add amendment sections that leave two
  competing interpretations in the same file.
- Historical context belongs in front matter fields, build reports, superseded
  links, or archived records, not in ambiguous appended prose.

## Development Coordination Structure

The dev repo should make AI collaboration explicit and auditable:

```text
generic-dev/
├── README.md
├── PROTOCOL.md
├── QUEUE.md
├── work/
│   └── 001-<slug>/
│       ├── package.yml
│       ├── README.md
│       ├── PLAN.md
│       └── prompts/
│           └── 001-<slug>.md
├── build-reports/
│   ├── INDEX.md
│   └── YYYYMMDD-<slug>.md
├── issues/
│   ├── INDEX.md
│   ├── gaps/
│   │   └── GAP-001.yml
│   ├── deferred/
│   │   └── DEF-001.yml
│   ├── bugs/
│   │   └── BUG-001.yml
│   └── upstream/
│       └── REQ-001.yml
├── design/
│   ├── INDEX.md
│   ├── architecture/
│   ├── mockups/
│   └── concepts/
├── state/
│   ├── INDEX.md
│   └── 2026-Q3.md
├── archive/
│   └── MANIFEST.yml
└── agent/
    ├── conventions.yml
    ├── buglog.yml
    └── do-not-repeat.yml
```

Recommended rules:

- `QUEUE.md` is generated from prompt front matter and is the only ordered
  run queue.
- A work package contains the plan, decisions, prompts, and package-local
  context for a bounded effort.
- Every AI prompt session closes with a build report, even if the session was
  design-only or scoping-only.
- State is split by time period or topic and indexed. Do not let a single
  status file become the permanent session-history sink.
- Issues are one record per file, split by meaning: gaps, deferred items,
  bugs, and upstream requests. Generated indexes provide active, blocked,
  planned, verified, and closed views.

## Issue Taxonomy

Use one shared record style, but keep the meanings distinct:

| Type | Prefix | Meaning |
|---|---|---|
| Gap | `GAP` | A needed capability, contract, design answer, or implementation surface is missing or underspecified. |
| Deferred item | `DEF` | Valid known work is intentionally left out of the current scope. |
| Bug | `BUG` | Existing accepted behavior is broken. |
| Upstream request | `REQ` | Another project, repo, dependency, or template must change before this project can finish the work. |

Recommended shared fields:

```yaml
id: BUG-001
type: bug
status: open
severity: high
scope: local
found_in: build-reports/20260819-example.md
summary: Generated queue omits blocked prompts
blocks:
  - work/002-check-suite
created: 2026-08-19
updated: 2026-08-19
links:
  governance: governance/contracts/queue-generation.md
  report: build-reports/20260819-example.md
```

Recommended statuses:

```text
open
accepted
in_progress
blocked
deferred
implemented
verified
closed
rejected
```

Cross-project enhancement requests use `issues/upstream/REQ-NNN.yml`. The
requesting project's dev repo records the request; the target project accepts,
rejects, or implements it through its own governance and prompt flow.

## File Format Rules

Choose formats by job, not by whether the reader is human or AI.

| File role | Recommended format |
|---|---|
| Constitutions, protocols, design docs | Markdown |
| ADRs, specs, contracts, unit governance | Markdown with YAML front matter |
| Prompts and build reports | Markdown with YAML front matter |
| Queues, status views, indexes | Generated Markdown |
| Issue records, package metadata, sync pins | YAML |
| Machine outputs, generated catalogs, lockfiles | JSON |
| Prompt delimiters inside a prompt | XML-style tags are allowed |
| Governance storage files | Avoid XML |

Core rule:

> Prose explains. Data enumerates.

Use Markdown where rationale matters. Use YAML or JSON when records must be
filtered, counted, sorted, validated, or generated into indexes.

## Indexing Rules

Indexes are mandatory because the governance corpus is primarily read by AI
sessions that need a minimal context window.

Each major directory should expose one of these:

- `INDEX.md` for human- and AI-readable navigation.
- `INDEX.yml` when the index is primarily consumed by tooling.
- Generated `*.md` views from YAML records where a readable summary is useful.

Indexes should answer:

- What records exist?
- Which records are active, in progress, blocked, complete, superseded, or
  archived?
- Which files should an AI read for a given unit, feature, ADR, contract, or
  work package?
- Which generated views must not be hand-edited?

## Update Policy

Governance files should reflect the current accepted truth.

When a decision changes:

- Update the existing ADR, spec, contract, or unit file in place.
- Update front matter fields such as `status`, `updated`, `supersedes`, or
  `replaced_by`.
- Preserve important rationale in the body only when it helps interpret the
  current decision.
- Move stale or superseded detail to archive records when retention matters.
- Record session-level evidence in a build report.

Avoid amendment-only updates that append new sections while leaving old
sections authoritative. That pattern makes the final governance meaning
ambiguous for both humans and AI.

## Vibe Coding Workflow

Vibe coding is allowed, but it still runs through governance.

Expected flow:

1. Capture the intent in `generic-dev` as a prompt, package note, design note,
   or session brief.
2. Identify which governance files in `generic` must change.
3. Update governance first: ADRs, specs, contracts, units, capabilities,
   routing, or status sources.
4. Generate or modify code, mockups, tests, or design artifacts.
5. Run the relevant check suite.
6. Write a build report that states what changed, what was validated, and what
   remains open.
7. Regenerate indexes, queues, and status views.

For mockups and exploratory design, the accepted result should be promoted
into governance only when it becomes a product decision. Exploratory variants
stay in `generic-dev/design/`.

## Check Suite Expectations

The template should ship with a governance check suite before the scaffold is
treated as stable. The suite should validate:

- Required indexes exist.
- Required front matter and YAML records exist and match schema.
- Generated files are current.
- Relative links resolve.
- Hot files stay within line budgets.
- No mutable state appears in constitutions.
- Mirrored contracts have `SYNC.yml` entries.
- Every closed prompt has a build report.
- Issue records use the correct prefix/type/folder combination.
- Dev coordination files are not excluded by ignore rules.

This keeps the template from becoming a set of unenforced conventions.

## Instantiation Contract

When copying the template to a new project:

1. Copy the parent template directory.
2. Delete `generic-project-design/`.
3. Rename `generic/` to `<project>/`.
4. Rename `generic-dev/` to `<project>-dev/`.
5. Replace placeholder tokens such as `generic`, `generic-dev`, and
   `generic-project` with the new project names.
6. Initialize and publish the two repositories separately.
7. Run `check-governance` before the first real development session.

The template should be designed so this replacement is mechanical and does
not require interpreting project-specific prose.
