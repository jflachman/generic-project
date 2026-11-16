<!--
  generic-project-design | design/initial-concept/docs/05-proposed-structure.md
-->

# 05 — Accepted structure for `<project>/` and `<project>-dev/`

**Status: accepted baseline as of 2026-08-19.** This is the canonical
structure for the first scaffold build. Every choice here traces to a
measured failure in
[`03-what-broke-measured.md`](03-what-broke-measured.md) or a mechanism worth
keeping from [`02-console-approaches-inventory.md`](02-console-approaches-inventory.md).

---

## 1. The rule that decides which repo anything goes in

> **`<project>/` holds what a *consumer* of the project needs.**
> **`<project>-dev/` holds what a *builder* of it needs.**

It resolves the real cases cleanly:

- A contract another repo mirrors → consumer-facing → `<project>/`.
- An ADR that explains why the API is shaped this way → consumer → `<project>/`.
- A build report, a prompt, an issue record, a mockup → builder → `<project>-dev/`.
- The session protocol → builder → `<project>-dev/`.

Current state is split by role. `<project>/STATUS.md` is a small generated
consumer-facing snapshot with links only and a hard line cap. Full session
history, package state, build reports, and detailed work status live in
`<project>-dev/`.

---

## 2. `<project>/` — the product repo

```
<project>/
├── CLAUDE.md                  ← constitution. Hard cap ~200 lines. ZERO mutable state
├── AGENTS.md                  ← thin pointer for non-Claude agents; no second copy of the rules
├── README.md                  ← for humans arriving from GitHub
├── STATUS.md                  ← GENERATED. What exists today, links only. Cap ~80 lines
├── governance/
│   ├── INDEX.md               ← generated/readable map of governance files
│   ├── adr/                   ← ADR-NNN-<slug>.md, YAML front matter (id/status/date/supersedes)
│   │   └── INDEX.md           ← generated ADR index
│   ├── specs/                 ← SPEC-NNN-<slug>.md, YAML front matter
│   │   └── INDEX.md           ← generated spec index
│   ├── contracts/             ← interfaces other repos may depend on
│   │   ├── INDEX.md           ← generated contract index
│   │   └── SYNC.yml           ← upstream ref + date for every mirrored contract  (D-04)
│   ├── units/                 ← one contract per screen/module/service, from _TEMPLATE.md
│   │   ├── INDEX.md           ← generated unit index
│   │   └── _TEMPLATE.md       ← includes the "must never do" section
│   ├── capabilities.yml       ← the closed taxonomy; generated .md view
│   └── ai-reference/
│       └── routing.yml        ← function/topic → the ONE doc to load. Generated .md view
├── src/  tests/  deploy/      ← ordinary project shape
└── scripts/
    └── check-governance.*     ← the lint suite. See §5
```

Notes on the deltas from the console:

- **`governance/screens/` → `governance/units/`.** "Screen" is UI-specific;
  the template must serve a library or service too. The *mechanism* — one
  contract per unit, from a template, with a "must never" section — is the
  part worth keeping.
- **`ai-reference/` moves under `governance/`.** In the console it is a
  top-level directory holding one 24 KB file, and its status relative to
  governance is ambiguous. It is governance: it is the retrieval policy.
- **`SYNC.yml` exists from day one**, not after the first six-week rot.
- **Indexes exist from day one** so an AI session can discover the small
  files it needs without loading the whole governance corpus.

## 3. `<project>-dev/` — the coordination repo

```
<project>-dev/
├── README.md                  ← FIRST LINE defines what this repo is not (see 01 §2)
├── PROTOCOL.md                ← the session protocol (the VIBE_SESSION_PROTOCOL descendant)
├── QUEUE.md                   ← GENERATED. The one ordered run queue     (D-13)
├── work/
│   └── <NNN>-<slug>/          ← one work package
│       ├── package.yml        ← id, title, purpose, status, depends_on
│       ├── README.md          ← why this package exists
│       ├── DESIGN.md          ← optional — omit when the package's deliverable IS a design
│       ├── PLAN.md            ← phases + the decision table (D-A…) with answers written back
│       └── prompts/
│           └── NNN-<slug>.md  ← YAML front matter drives QUEUE.md
├── build-reports/
│   ├── INDEX.md               ← GENERATED
│   └── YYYYMMDD-<slug>.md     ← one per session, without exception
├── issues/
│   ├── README.md              ← type rules and routing: local, deferred, bug, upstream
│   ├── INDEX.md               ← GENERATED
│   ├── gaps/GAP-NNN.yml       ← missing or underspecified capability/contract/design
│   ├── deferred/DEF-NNN.yml   ← intentional out-of-scope work
│   ├── bugs/BUG-NNN.yml       ← accepted behavior is broken
│   └── upstream/REQ-NNN.yml   ← another project/repo/template must change first
├── design/
│   ├── INDEX.md               ← generated or maintained map of active design artifacts
│   ├── mockups/<unit>/        ← variants + a workflow narrative each
│   └── concepts/              ← exploratory; marked historical when superseded
├── state/
│   ├── INDEX.md               ← generated map of current/cold state files
│   └── YYYY-QN.md             ← session history, rotated by quarter. Cold by default
├── archive/
│   └── MANIFEST.yml           ← what was archived, when, why, and where it came from
└── agent/                     ← agent-operational memory (the .wolf/ descendant)
    ├── do-not-repeat.yml
    ├── buglog.yml
    └── conventions.yml
```

Notes:

- **`issues/` is one record per file**, per
  [`04-file-formats-for-ai-readers.md`](04-file-formats-for-ai-readers.md)
  §5. This is the direct fix for a 181 KB flat log, without letting "gap"
  become a catch-all for bugs and deferred work.
- **`state/` is rotated by quarter and cold by default** — the fix for a
  3,777-line unstructured section that every session was told to read.
- **`QUEUE.md` is generated** from prompt front matter, so three competing
  queues become structurally impossible.
- **`archive/MANIFEST.yml`** answers your "retain it without cluttering"
  requirement: content moves, a one-line pointer with the reason stays.
- **Prompt front matter declares `touches: [paths]`** so the queue can flag
  likely work collisions before two sessions edit the same governance area.

## 4. File formats and schemas

Accepted rules from D-09 through D-11:

| Role | Format |
|---|---|
| Constitutions, protocols, design docs | Markdown |
| ADRs, specs, contracts, unit governance | Markdown with YAML front matter |
| Prompts and build reports | Markdown with YAML front matter |
| Queues, status views, indexes | Generated Markdown |
| Issue records, package metadata, sync pins | YAML |
| Machine outputs and generated catalogs | JSON |

Markdown bodies carry rationale. YAML front matter and YAML records carry
facts that need to be queried, sorted, counted, filtered, or validated. XML is
allowed as an in-prompt delimiter pattern, not as a governance storage format.

Required validated schemas:

| Record type | Required fields |
|---|---|
| Prompt | `id`, `title`, `status`, `depends_on`, `touches` |
| Build report | `id` or `session`, `prompt`, `date`, `status`, `validated` |
| Issue | `id`, `type`, `status`, `severity`, `scope`, `found_in`, `summary`, `created`, `updated` |
| ADR | `id`, `status`, `date`, `updated`, `supersedes` |
| Spec | `id`, `status`, `date`, `updated`, `unit_or_scope` |
| Contract | `id`, `status`, `date`, `updated`, `owners`, `sync_required` |
| Unit contract | `id`, `status`, `date`, `updated`, `unit_type` |
| Work package | `id`, `title`, `purpose`, `status`, `depends_on` |

Issue record prefixes and folders must agree:

| Type | Prefix | Folder |
|---|---|---|
| Gap | `GAP` | `issues/gaps/` |
| Deferred item | `DEF` | `issues/deferred/` |
| Bug | `BUG` | `issues/bugs/` |
| Upstream request | `REQ` | `issues/upstream/` |

Governance files are updated to their current accepted meaning. Do not append
amendment-only sections that leave contradictory active meanings in place.
Traceability lives in front matter, supersession fields, archived records, and
build reports.

## 5. The check suite — the actual differentiator

Everything above is a rule, and
[`03-what-broke-measured.md`](03-what-broke-measured.md) concludes that rules
without enforcement rot. `scripts/check-governance.*` runs in CI **and** in
the session-close step, and fails on:

| Check | Catches |
|---|---|
| Line/byte budget per tier (hot / warm / cold) | 147 KB "lightweight" contracts, 339 KB state |
| Every relative link resolves | `CLAUDE.md` pointing at two files that do not exist |
| No `##` section exceeds N lines without `###` | the 3,777-line paragraph |
| Front matter and YAML records present and schema-valid | records drifting back into prose |
| Generated files match their source | hand-edited queues; disagreeing views |
| `SYNC.yml` entry per mirrored path, age under threshold | six-week silent contract rot |
| Nothing in the dev repo is git-ignored | 269 lost files |
| Every closed prompt has a build report | silent session closes |
| Required indexes exist and generated indexes are current | AI sessions loading too much context or stale views |
| No contradictory active amendment sections | ambiguous final governance meaning |
| Issue type, prefix, and folder agree | bugs, gaps, deferred work, and upstream requests collapsing into one vague log |

**If only one thing survives this whole design, make it this table.** It is
the difference between a template and a folder of good intentions.

## 6. Tiers, so budgets mean something

| Tier | Read | Budget | Examples |
|---|---|---|---|
| **Hot** | Every session, in full | ≤ 200 lines | `CLAUDE.md`, `PROTOCOL.md`, `QUEUE.md`, `STATUS.md` |
| **Warm** | When the session touches that area | ≤ 500 lines | a unit contract, an ADR, an active `PLAN.md` |
| **Cold** | Only when explicitly named | no cap, but indexed | build reports, issue records, state history |
| **Archive** | Effectively never; recoverable | manifest only | superseded designs, closed packages |

The console's mandatory reading order is a good mechanism aimed at the hot
tier. It failed because two of its six items were *not* hot files — they were
cold files that had never been split out. Sorting every document into a tier
on creation is what makes the reading order enforceable.

## 7. What is deliberately NOT proposed

- **No `.notes/` directory.** Its entire contents become `<project>-dev/`.
  Keeping a leading-dot directory would re-invite the ignore-file problem.
- **No third repo for design.** See [`01`](01-naming-and-repo-topology.md) §3.
- **No monorepo.** The two repos have different audiences, different churn
  rates, and different clone-weight tolerances.
- **No format decision for prompts and reports beyond front matter.** Their
  bodies are prose and should stay prose.
