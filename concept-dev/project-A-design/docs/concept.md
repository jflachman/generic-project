<!--
  project-A-design | docs/concept.md
-->

# Concept — a three-repo template for AI-led, multi-project development

Status: draft concept, for discussion
Scope: the reusable `project-A` / `project-A.ai` / `project-A.gov` template,
and the family structure that lets several such triads work together
Date: 2026-08-20

This document proposes the shape of the new template. It builds on
`codex-concept/`, a two-repo design (`generic` + `generic-dev`) built in a
prior session, and keeps what that design validated: small indexed files,
prose-for-reasoning/data-for-records, generated views, and a check suite
that enforces the rules instead of trusting them. It changes the topology
from two repos to three, and adds two things the prior design never had to
address: several related projects sharing a family, and several distinct AI
roles operating with separation of duties instead of one implicit agent.

---

## 1. The three repos, and why a third one

| Repo | Holds | Analogous to (prior design) |
|---|---|---|
| `project-A` | The running artifact: source, tests, Docker/deploy config, CI that builds and ships it. | `generic/`, minus governance |
| `project-A.ai` | The collaboration corpus: session protocol, work packages, prompts, build reports, issues, design exploration, agent roles, audits. | `generic-dev/` |
| `project-A.gov` | The authoritative record: ADRs, specs, contracts, interfaces, unit/capability inventory, architecture decisions. | `generic/governance/`, pulled out |

The prior design deliberately kept governance *inside* the product repo,
reasoning that ADRs and contracts are "consumer-facing truth" a product
repo's own visitor needs. That reasoning still holds for a single project.
It stops holding once a family has several inter-related projects that all
need to *read* each other's governance without touching each other's code —
`project-A.gov` becomes the thing `project-B` depends on, not
`project-A`'s source tree. Separating governance into its own repo makes
that dependency explicit and independently versioned, at the cost of a
second sync boundary (§6).

**The rule that decides which repo anything goes in:**

> `.gov` holds the current accepted answer to a design question.
> `.ai` holds the process of getting to that answer, and the bookkeeping
> around it.
> `project-A` holds what actually runs.

Ask three questions, in order:

1. *Is this the decided, current truth — the thing another project or a
   future session should trust without re-deriving it?* → `.gov`
2. *Is this evidence of how the work happened, or work still in flight —
   a prompt, a build report, a mockup, an issue, an audit?* → `.ai`
3. *Is this code, a test, a Dockerfile, or something CI runs?* → `project-A`

Worked cases:

| Artifact | Repo | Reason |
|---|---|---|
| Source code, tests, CI pipelines | `project-A` | Runs. |
| Generated `STATUS.md` | `project-A` | Consumer-facing snapshot; capped, generated. |
| ADRs, specs, contracts, unit/capability inventory | `project-A.gov` | Decided truth another project or session depends on. |
| `INTERFACE.md` | `project-A.gov` | It **is** a contract — the allowed surface for other projects. See §5. |
| Mockup variants, design exploration | `project-A.ai` | Not truth until a direction is picked. |
| An ADR draft, before acceptance | `project-A.ai` | Same reasoning — promoted into `.gov` on acceptance (§4). |
| Work packages, prompts, build reports | `project-A.ai` | Session bookkeeping. |
| Gaps, bugs, deferred items, enhancement requests | `project-A.ai` | Typed work tracking, not decided truth. |
| Agent role assignment (`roles.yml`) | `project-A.ai` | Governs collaboration, not the product. |
| Cross-project audit reports | `project-A.ai` | Evidence, not truth — findings get filed as issues, not treated as governance. |

---

## 2. The family: several projects, one workspace

A family is several related implementation projects — a backend, a
console, a visualization tool — that each get the full triad, sitting as
siblings under one parent folder:

```
<family>-workspace/                 ← container only. No .git. Never published.
├── ml-lab/                         ← repo (implementation)
├── ml-lab.ai/                      ← repo (collaboration)
├── ml-lab.gov/                     ← repo (governance)
├── ml-console/                     ← repo
├── ml-console.ai/                  ← repo
├── ml-console.gov/                 ← repo
├── ml-vis/                         ← repo
├── ml-vis.ai/                      ← repo
└── ml-vis.gov/                     ← repo
```

Nine independent GitHub repos, one parent folder. The developer works
almost exclusively in the three `.ai` repos; the AI creates and maintains
almost everything in the corresponding `.gov` and implementation repos.

**A project may depend on another project's governance, never on its
implementation or coordination.** `ml-console` may read `ml-lab.gov` to
learn `ml-lab`'s interface. Nothing outside `ml-lab.ai` writes to
`ml-lab.ai`, and nothing outside `ml-lab` writes to `ml-lab`'s source —
except through the cross-project issue protocol in §7, which is explicitly
the one sanctioned side-channel.

Naming note: GitHub allows dots in repository names (a name may not literally
*end* in `.git`, which none of these do). This is called out only as a
practical footnote, not a design risk.

Whether the family container should stay flat (as drawn above) once it
holds many projects, or nest one level per project
(`ml-lab/{ml-lab, ml-lab.ai, ml-lab.gov}/`), is **D-04** in
[`open-questions.md`](open-questions.md).

---

## 3. What each repo contains

This is a first-pass shape, not an exhaustive schema — enough to anchor the
next round of design, in the spirit of the prior template's own staged
approach (topology first, exhaustive tree later).

### `project-A/` — the implementation repo

```
project-A/
├── CLAUDE.md / AGENTS.md      ← short constitution. Zero mutable state. Points into .ai and .gov
├── README.md                  ← for humans arriving from GitHub
├── STATUS.md                  ← GENERATED consumer snapshot, capped, links only
├── src/  tests/  deploy/
└── scripts/
    └── check-governance.*     ← now validates across all three repos, see §8
```

No `governance/` directory here at all — that content now lives one repo
over. `CLAUDE.md` replaces what used to be a governance table of contents
with two pointers: "the decided rules are in `../project-A.gov/`, the
current queue is in `../project-A.ai/QUEUE.md`."

### `project-A.gov/` — the governance repo

```
project-A.gov/
├── README.md                  ← what this repo is: decided truth only. No code, no work tracking, no history log
├── CLAUDE.md / AGENTS.md      ← governance-authoring rules only
├── INDEX.md                   ← map of every governance area below
├── adr/
│   ├── INDEX.md
│   └── ADR-NNN-<slug>.md
├── specs/
│   ├── INDEX.md
│   └── SPEC-NNN-<slug>.md
├── contracts/
│   ├── INDEX.md
│   ├── SYNC.yml               ← pins for contracts THIS project mirrors from elsewhere
│   └── <contract>.md
├── interfaces/
│   └── INTERFACE.md           ← how OTHER projects may use this one. See §5
├── units/                     ← one contract per module/service/screen
│   ├── INDEX.md
│   ├── _TEMPLATE.md
│   └── UNIT-NNN-<slug>.md
├── architecture/
│   ├── INDEX.md
│   └── <topic>.md
├── capabilities.yml
└── ai-reference/
    ├── routing.yml            ← topic/function → the ONE file to load
    └── routing.md             ← generated view
└── changelog/                 ← see §6.3
```

### `project-A.ai/` — the collaboration repo

```
project-A.ai/
├── README.md                  ← FIRST LINE: no application code, no governance authority
├── PROTOCOL.md                ← the session protocol
├── QUEUE.md                   ← GENERATED, single run queue
├── roles.yml                  ← the agent-role assignment config, see §9
├── work/
│   └── NNN-<slug>/
│       ├── package.yml
│       ├── README.md          ← the argument: why this package exists
│       ├── PLAN.md            ← the measured evidence
│       ├── DESIGN.md          ← only when the package introduces a new mechanism
│       └── prompts/
│           └── NNN-<slug>.md
├── build-reports/
│   ├── INDEX.md
│   └── YYYYMMDD-<slug>.md
├── issues/                    ← see §7
│   ├── README.md
│   ├── INDEX.md
│   ├── gaps/            + completed/
│   ├── bugs/             + completed/
│   ├── deferred/         + completed/
│   ├── enhancement-requests/ + completed/
│   └── external-requests/    + resolved/  + closed/
├── design/
│   ├── INDEX.md
│   ├── concepts/               ← exploratory reasoning, ADR/architecture drafts pre-acceptance
│   └── mockups/<unit>/         ← variants + a workflow narrative each
├── audits/                     ← see §10
│   ├── INDEX.md
│   └── YYYYMMDD-<slug>.md
├── state/
│   ├── INDEX.md
│   └── YYYY-QN.md
├── archive/
│   └── MANIFEST.yml
└── agent/
    ├── conventions.yml
    ├── buglog.yml
    └── do-not-repeat.yml
```

---

## 4. Promotion: how something becomes governance

Nothing is written directly into `.gov` from a blank page. The path is
always: raised in `.ai` → decided → promoted.

1. An idea, a mockup direction, or an ADR argument is drafted in
   `project-A.ai/design/concepts/` or `.../design/mockups/`.
2. The developer (or, for smaller calls, the Liaison role — §9) picks a
   direction. This is a real wait-for-approval point, not a formality.
3. The Governance Author role writes or updates the corresponding file in
   `project-A.gov/` — an ADR, a spec, a unit contract — and the record
   points back at the `.ai` draft that produced it (a relative cross-repo
   link plus commit ref, not a copy).
4. The `.ai` draft is marked accepted/superseded in place; it is not
   deleted. It is the argument; the `.gov` file is the ruling.

This is the same mockup-gate mechanism proven in
`ref-docs/VIBE_SESSION_PROTOCOL.md` §4, generalized from screens to any
governance decision, and retargeted from `governance/screens/` to
`project-A.gov/units/`.

---

## 5. `INTERFACE.md` — the contract for other projects

Lives at `project-A.gov/interfaces/INTERFACE.md`, because it *is* a
contract — the same reasoning that puts other contracts in `.gov`.

Structure:

```markdown
# INTERFACE — how other projects may use project-A

## General method
<How consumers are expected to interface: HTTP API? imported library?
CLI? Which is preferred, which is merely possible, which is forbidden
(e.g. "never read this project's database directly").>

## Consumers
### ml-console
<What ml-console specifically calls, since when, which contract/spec
governs it, anything ml-console must not do.>

### ml-vis
<Same shape, independent section.>
```

Each interfacing project gets its own section, owned by *this* project
(only `project-A.gov` maintainers edit `INTERFACE.md` — a consumer proposes
a change via the issue protocol in §7, it doesn't edit the file itself).
The general-method section stays short and stable; per-consumer sections
are where drift would actually show up, so they're the part worth
re-reading whenever a consumer's own governance changes.

Whether `project-A/README.md` should carry a duplicate pointer sentence
("see `../project-A.gov/interfaces/INTERFACE.md`") for GitHub visitors who
never clone `.gov` is **D-08**.

---

## 6. Governance structure, bloat prevention, and "memory"

Everything the prior design concluded about file formats, tiering, and
bloat still applies — it is a property of the corpus, not of which repo
holds it. Restated briefly, then extended for the two things that are new:
a governance repo of its own, and a family of repos.

### 6.1 File formats — unchanged from the prior design

> **Prose explains. Data enumerates.**

| Role | Format |
|---|---|
| Constitutions, protocols, architecture narrative | Markdown |
| ADRs, specs, contracts, unit governance, `INTERFACE.md` | Markdown + YAML front matter (`id`, `status`, `date`, `updated`, `supersedes`) |
| Prompts, build reports | Markdown + YAML front matter |
| Issue records (gaps, bugs, deferred, enhancement/external requests) | One YAML record per file |
| Queues, indexes, capability/routing views | Generated Markdown |
| Agent role config, sync pins, archive manifest | YAML |
| Machine catalogs, lockfiles | JSON |
| XML | Never as storage. Only as attention-delimiters inside a prompt fed to a model. |

### 6.2 Tiering — unchanged, now applied per repo

| Tier | Read | Budget | Where it shows up |
|---|---|---|---|
| Hot | Every session, in full | ≤200 lines | `CLAUDE.md`, `PROTOCOL.md`, `QUEUE.md`, `STATUS.md` |
| Warm | When the session touches that area | ≤500 lines | a unit contract, an ADR, an active `PLAN.md` |
| Cold | Only when named | indexed, uncapped | build reports, issue records, `state/` history |
| Archive | Effectively never | manifest only | superseded ADRs, closed work packages, resolved audits |

### 6.3 The changelog question — resolved as one mirrored folder

The developer's brief proposed two ideas that both worked in isolation: a
"sister file" changelog per document, and folder-based separation so
`check-governance` and casual readers never trip over history mixed into
current truth. The synthesis: **one `changelog/` folder per governance
repo, mirroring record ids, not document trees.**

```
project-A.gov/
├── adr/ADR-004-cache-invalidation.md      ← current truth only
├── specs/SPEC-012-ingest-schema.md
└── changelog/
    ├── ADR-004.md                          ← why it changed, when, from what
    └── SPEC-012.md
```

One folder to ignore by default, one folder an AI opens only when a session
genuinely needs the history of a specific record (front matter has
`supersedes`/`replaced_by` for the mechanical trail; `changelog/<ID>.md` is
where the *prose* reasoning for a change lives, out of the hot path). This
is **D-09**.

### 6.4 Efficient access: indexes first, RAG/MCP deferred

The brief asks directly whether governance access should be via RAG, MCP,
or something else. Recommendation: **neither, for a single project or a
small family, because the corpus is designed not to need them.**

- The tiering and per-area `INDEX.md`/`routing.yml` files already solve
  "find the 2–3 relevant files without loading the corpus" deterministically
  — a lookup, not a retrieval problem. RAG solves fuzzy retrieval over a
  corpus too large to index by hand; this corpus is deliberately kept small
  and indexed specifically so it never becomes that corpus.
- RAG has a real cost this design is structured to avoid: embeddings go
  stale the moment a file updates, which reintroduces exactly the kind of
  silent drift the whole check-suite philosophy exists to prevent.
- All repos in a family are mounted as siblings on disk (carried forward
  from the two-repo design's own D-14). A session in `ml-console.ai` can
  read `ml-lab.gov/interfaces/INTERFACE.md` directly, by relative path — no
  server needed for local, same-workspace access.
- **MCP earns its place in one specific spot, not as a general governance
  front-end:** the cross-project issue protocol (§7) requires an agent
  working in one project's `.ai` repo to update *another* project's `.ai`
  repo. That is a real access-boundary problem worth solving with a small
  service rather than raw multi-repo git credentials handed to every agent.
  See §7 and **D-02**.
- Revisit RAG (for "has any project in this family solved X before"
  cross-family search) and a general governance-query MCP server only once
  a family is large enough that indexes stop being sufficient — the same
  threshold logic the prior design used for shared tooling. This is **D-05**.

---

## 7. Issues, and the cross-project request protocol

`project-A.ai/issues/` holds five record types, one file per record, YAML,
each folder carrying a `completed/` (or `resolved/`/`closed/`) subfolder so
a listing never has to be cross-referenced against a status field to know
if it's live:

| Type | Prefix | Meaning | Folder | Origin |
|---|---|---|---|---|
| Gap | `GAP` | A needed capability/contract/design answer is missing. | `gaps/` | local |
| Bug | `BUG` | Existing accepted behavior is broken. | `bugs/` | local |
| Deferred | `DEF` | Valid work intentionally left out of current scope. | `deferred/` | local |
| Enhancement request | `ENH` | Another project is asking *this* project for something. | `enhancement-requests/` | external → local |
| External request | `REQ` | This project is asking *another* project for something. | `external-requests/` | local → external |

`ENH` and `REQ` are two ends of the same conversation, filed in two
different `.ai` repos. Every `REQ` this project opens against `ml-lab`
should have a matching `ENH` sitting in `ml-lab.ai/issues/enhancement-requests/`
— they are meant to be near-duplicates by design, not two independent
records.

### 7.1 Shared record shape

```yaml
id: ENH-014
type: enhancement-request
status: open
severity: medium
requested_by: ml-console          # only on ENH
requested_of: ml-lab              # only on REQ
summary: Expose per-symbol volatility as a queryable field
created: 2026-08-20
updated: 2026-08-20
links:
  external_request: ../../ml-console.ai/issues/external-requests/REQ-031.yml
  governance: ../gov/specs/SPEC-009-volatility.md   # once planned
```

### 7.2 Status vocabulary

```
open           written, not yet planned
queued         planned, a work package/prompt will close it
in_progress    a session is actively working it
resolved       (REQ only) the target project says its half is done — requester must verify
closed         verified done, or (ENH) target project finished it and moved the file
rejected       will not be done, with a reason
```

### 7.3 The close protocol

When a project closes an `ENH` it owns:

1. Do the work (through the normal work-package/prompt flow — an `ENH`
   becomes governed the same way any other decision does, per §4).
2. Move `enhancement-requests/ENH-014.yml` → `enhancement-requests/completed/`.
3. Update `enhancement-requests/INDEX.md`: status `closed`, linked build
   report / commit.
4. **Update the requester's record**: in `ml-console.ai/issues/external-requests/`,
   set `REQ-031` status to `resolved`, add a link to the `ENH-014` build
   report, and move the file to `external-requests/resolved/`.
5. Later — on the requester's own cadence, not synchronously — a session in
   `ml-console.ai` reviews everything in `external-requests/resolved/`,
   confirms the result actually satisfies the request, and either:
   - moves it to `external-requests/closed/`, or
   - reopens it (`status: open`, a note explaining the gap, moved back out
     of `resolved/`).

Step 4 is the one mechanical wrinkle: it requires write access into a
*different* project's `.ai` repo. Doing this as a direct git write from
whichever agent happens to be running is the simplest option and the
weakest boundary — it means every implementer-role agent effectively has
push access to every other project's coordination repo. The alternative is
routing step 4 through a pull request or an issue comment on the target
repo, reviewed the normal way. This tradeoff is **D-02**.

---

## 8. The check suite, extended across three repos

Everything the prior design's check suite verified still applies; it now
also has to reason about repo *boundaries*, not just files:

| Check | New because of |
|---|---|
| Every relative cross-repo link resolves (`../project-A.gov/...` from `.ai`, and back) | three repos instead of one governance tree |
| `project-A` carries a governance pin (commit/tag of `project-A.gov` it was built against) and it's fresh | governance moved out of the product repo |
| No governance content exists inside `project-A` (the check should fail loudly if it creeps back in) | prevents the exact regression this redesign is fixing |
| Every `ENH` has a matching `REQ` in the named project (or is flagged orphaned) | the two-sided request protocol in §7 |
| Issue folder + prefix + status agree, including `completed/`/`resolved/`/`closed/` placement | five issue types now, not four |
| `roles.yml` — every role referenced by a build report or a PR actually exists in the config | separation-of-duties is only real if it's checked |
| PR approver identity ≠ PR author identity, when `roles.yml` declares `independence_from` | see §9 |

This should run per-repo where the check is local, and as a family-level
job where the check spans repos (link resolution, the governance pin, the
`ENH`/`REQ` pairing).

---

## 9. Agent roles and separation of duties

The brief asks for several distinct AI functions instead of one implicit
agent, with which-does-what managed in config rather than convention. This
section proposes the shape of that config; it is intentionally not
exhaustive about triggers/scheduling, which belongs in a later, narrower
design pass.

### 9.1 Roles

| Role | Does | Primarily works in |
|---|---|---|
| **Liaison** | The developer-facing collaborator. Turns conversation into work packages and prompts. First point of contact. | `.ai` |
| **Governance Author** | Drafts/updates `.gov` records from accepted decisions (§4). | `.gov`, reads `.ai` |
| **Governance Reviewer** | Periodically reviews `.gov` for staleness, budget violations, contradictions. Independent identity from the Author. | `.gov` |
| **Implementer** | Writes code/tests in `project-A` against current governance. | `project-A` |
| **PR Reviewer** | Reviews and approves the Implementer's pull requests. Independent identity from the Implementer. | `project-A` |
| **Auditor** | Periodic cross-project sweep of gov + impl + coordination; produces an audit report. | all three, read-only |
| **Second Auditor** | Reads the Auditor's report, verifies independently, and is the one that actually files `GAP`/`BUG`/`DEF` records from confirmed findings. | all three |

The Auditor/Second-Auditor split matters for the same reason the
PR-author/PR-reviewer split does: the role that *notices* a problem and the
role that *records* it as an actionable issue should not be the same
session, or an auditor's blind spot becomes a blind spot in the backlog
too.

### 9.2 `roles.yml`, sketch

```yaml
roles:
  liaison:
    repos: [project-A.ai]
  governance-author:
    repos: [project-A.gov]
    reads: [project-A.ai]
  governance-reviewer:
    repos: [project-A.gov]
    independence_from: [governance-author]
    schedule: monthly
  implementer:
    repos: [project-A]
    reads: [project-A.gov, project-A.ai]
  pr-reviewer:
    repos: [project-A]
    independence_from: [implementer]
  auditor:
    repos: [project-A, project-A.ai, project-A.gov]
    schedule: monthly
  second-auditor:
    repos: [project-A, project-A.ai, project-A.gov]
    reads_reports_from: [auditor]
    independence_from: [auditor]
```

`independence_from` is the load-bearing field: it's not decoration if
`check-governance` (or CI) can actually reject a PR where the approving
identity matches the authoring identity for a role pair that declares
independence. Whether that's enforced by distinct GitHub bot
identities/tokens per role, or procedurally (same credentials, logged role
per action), is **D-03**.

Whether `roles.yml` is per-project or shared once-per-family is **D-11**.

---

## 10. Periodic audits

`project-A.ai/audits/YYYYMMDD-<slug>.md` — the Auditor's output. Format:
what was checked, what was found, explicitly stated when nothing was found
(a silent section reads as a skipped step, same rule as build reports).
Findings are *not* governance and are not directly actionable — the Second
Auditor reads the audit, independently verifies each finding, and is the
one who opens the corresponding `GAP`/`BUG`/`DEF` record. This keeps the
audit report itself immutable evidence rather than a second, competing
issue queue.

Cadence (schedule-based vs. milestone-triggered) is **D-10**.

---

## 11. The `.ai` repo's operating workflows

Carried forward close to verbatim from `ref-docs/prompt-tracking-process.md`
and `ref-docs/VIBE_SESSION_PROTOCOL.md` — both road-tested in a real
project, not re-derived here:

- **Work packages** bundle related work with a stated argument
  (`README.md`), measured evidence (`PLAN.md`), and — only when a new
  mechanism is introduced — a `DESIGN.md`.
- **Prompts** are complete, self-contained session briefs, numbered
  permanently within their package (`005b` for an inserted follow-up, never
  a renumber).
- **The queue.** The prior design's own conclusion (D-13, generated
  `QUEUE.md`) and the console's road-tested mechanism (a hand-maintained
  `PROMPT-TRACKER.md`/`PROMPT-HISTORY.md` split) solve the same problem two
  ways. The synthesis proposed here: **generate `QUEUE.md` from prompt
  front matter, and give that front matter a `queue_reason` field** — this
  gets the drift-proofing of "never hand-maintained" *and* the console's
  most valuable column, the stated reason a row sits where it does. Closed
  rows are generated out of the live queue, not hand-deleted; a generated
  `QUEUE_HISTORY.md` (or the `build-reports/INDEX.md`) is the closed-work
  view. Confirm this reconciliation as **D-07**.
- **End-of-session checklist**, every prompt session, no exceptions:
  1. Write the build report (`work/<package>/build-reports/<same-name-as-prompt>.md`).
  2. Confirm the follow-on prompt(s) are current — re-check line numbers and
     assumptions rather than trusting what was written when the package was
     planned.
  3. Regenerate `QUEUE.md` and any touched indexes.
  4. Log any gap/bug/deferred item found, or state explicitly that nothing
     came up.
  5. If the session touched governance, confirm the Governance Author step
     (§4) happened — a prompt is not closed with an undecided promotion
     pending.
- **Code review / commit / PR / approve / merge automation.** Git
  operations happen in the repo they target (`project-A` or
  `project-A.gov`); they are *orchestrated from* `.ai`, and the `.ai` build
  report is the audit trail tying a work-package session to the commits and
  PRs it produced. The PR Reviewer role (§9) is the one that approves —
  never the Implementer role, when `roles.yml` declares that pair
  independent.
- **Design collaboration** (functionality and mockups) uses the mockup gate
  from §4: 2–3 real variants, a workflow narrative per variant anchored to
  a concrete task, present-and-wait-for-direction before any governance or
  code changes.
- **Skills management across projects.** Claude Code skills used in more
  than one project's `.ai` repo start as per-project copies with a version
  stamp, checked for drift the same way the prior design handled
  family-shared tooling (its D-05) — not a shared package or submodule
  until there is real, repeated multi-project churn to justify one. This is
  **D-06**.

---

## 12. What carries forward unchanged, and what's genuinely new

| Area | Status |
|---|---|
| File-format rules (§6.1), tiering (§6.2), "no amendments, update in place" | Carried forward unchanged. |
| Prompt/build-report/work-package mechanics | Carried forward from `ref-docs/`, road-tested. |
| Mockup gate | Carried forward, retargeted to `.gov/units/`. |
| Check-suite philosophy | Carried forward, scope extended to span repo boundaries (§8). |
| Governance repo of its own | **New.** Was inside the product repo; now `.gov`. |
| Multi-project family structure | **New.** Prior design scoped to one project. |
| Explicit multi-agent roles with separation of duties | **New.** Prior design assumed one implicit agent. |
| Cross-project issue protocol (`ENH`/`REQ` pairing) | **New**, generalizes the prior design's single-direction `upstream/REQ`. |
| Periodic audit + second-auditor verification | **New.** |
| `INTERFACE.md` | **New**, though it plays the role a "contract" already played in the prior design. |

---

Open questions raised throughout this document (marked **D-NN**) are
collected, with options and a recommended lean, in
[`open-questions.md`](open-questions.md).
