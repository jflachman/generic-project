<!--
  project-A-design | docs/open-questions.md
  The working agenda. Answer in place, in the section, with a date — the
  same pattern that worked in codex-concept's own
  design/initial-concept/docs/06-open-questions.md.
-->

# Open questions

Eleven decisions raised in [`concept.md`](concept.md). Each has options and
a recommended lean, marked `open`. Answer in place with a date when decided;
if an answer makes a later question moot, strike it through and say why
rather than deleting it.

Status values: `open` · `decided` · `deferred` · `dissolved`.

---

## Topology

### D-04 — Does the family container stay flat, or nest per project? · `open`

Referenced in concept.md §2.

| Option | Trade |
|---|---|
| Flat (`ml-lab/`, `ml-lab.ai/`, `ml-lab.gov/`, `ml-console/`, ... all siblings) | Matches the brief exactly; simple for 2–3 projects; nine-plus siblings gets visually noisy past that |
| Nested (`ml-lab/{ml-lab, ml-lab.ai, ml-lab.gov}/`) | Groups a project's triad visually; adds one directory level everywhere, and the outer folder name now collides with the inner one the same way the prior design's D-01 warned about |

**Lean: flat**, matching the brief, revisited only if a family grows past
roughly 4–5 projects and the sibling list becomes hard to scan.

---

## Cross-project mechanics

### D-02 — How does closing an `ENH` write to another project's `REQ`? · `open`

Referenced in concept.md §6.4 and §7.3.

| Option | Trade |
|---|---|
| Direct git write from whichever agent closes the `ENH` | Simplest to implement; means every such agent has effective push access to every other project's `.ai` repo — a wide, implicit trust boundary |
| Pull request against the target `.ai` repo, reviewed normally | Matches how the rest of this design treats cross-repo change (nothing writes to another project without going through its own review); adds latency to what is otherwise a fast bookkeeping update |
| A small mediating service (MCP or otherwise) that both `.ai` repos trust for exactly this handshake | Narrow, purpose-built trust boundary instead of full git credentials; is new infrastructure to build and operate |

**Lean: PR-based for now**, since it reuses machinery this design already
needs (§8, §9) rather than introducing new infrastructure before there's a
second real project to test it against. Revisit the mediating-service
option once the PR-based version proves too slow in practice.

### D-05 — When does RAG or a governance-query MCP server earn its place? · `open`

Referenced in concept.md §6.4.

**Lean:** neither for a single project or small family — the tiered,
indexed corpus is designed specifically to make retrieval a lookup, not a
search problem (§6.4's full argument). Revisit once a family is large
enough that "has any project here already solved X" stops being answerable
by routing tables — no specific project count proposed yet; **needs the
developer's sense of what "large enough" means for this family**, since it
depends on how many projects are actually planned.

---

## Roles and separation of duties

### D-03 — How strictly is role independence enforced? · `open`

Referenced in concept.md §9.2.

| Option | Trade |
|---|---|
| Distinct GitHub bot identities/tokens per role | Real, verifiable separation — a PR literally cannot be self-approved; more credentials to provision and rotate per project |
| Same credentials, distinct sessions, role logged per action | Much simpler to stand up; the separation is a convention `check-governance` can audit after the fact, not something GitHub itself prevents |

**Lean: start procedural** (log the acting role, audit after the fact),
move to distinct identities for the pairs that matter most
(Implementer/PR-Reviewer first) once the family has enough real PR volume
to make self-approval a live risk rather than a theoretical one.

### D-11 — Is `roles.yml` per-project or family-wide? · `open`

Referenced in concept.md §9.2.

| Option | Trade |
|---|---|
| Per-project (`project-A.ai/roles.yml`) | A project can have a different bench of agents/roles than its siblings; drifts the way any per-project copy drifts (same shape as D-06) |
| One family-wide config, referenced by every `.ai` repo | One source of truth for "who does what"; needs a location that isn't any single project's repo — possibly the family workspace folder itself, which today is deliberately not a repo |

**Lean: per-project to start**, since the workspace container is
deliberately not a git repo today and family-wide config would need one.
Revisit alongside D-05/D-06 if drift becomes a real problem.

---

## Process mechanics

### D-07 — Generated `QUEUE.md` with a `queue_reason` field, replacing the tracker/history split? · `open`

Referenced in concept.md §11.

The road-tested `PROMPT-TRACKER.md`/`PROMPT-HISTORY.md` split
(`ref-docs/prompt-tracking-process.md`) and the prior design's generated
`QUEUE.md` (its D-13) both work, and solve the same problem. concept.md §11
proposes combining them: generate the queue, but carry the tracker's most
valuable column (the stated reason a row is ordered where it is) as prompt
front matter.

**Lean: adopt the combined version**, since it keeps the drift-proofing
property (a queue that's generated can't have three competing copies) while
keeping the one thing the hand-maintained version proved worth having.
Confirm before this becomes the template default — it's untested in this
exact form.

### D-06 — Skills sharing: per-project copies, or a shared package? · `open`

Referenced in concept.md §11.

**Lean: per-project copies with a version stamp**, mirroring the prior
design's D-05 resolution for shared tooling generally. Revisit once there
are at least three active projects with repeated shared-skill updates.

### D-10 — Audit cadence: scheduled or milestone-triggered? · `open`

Referenced in concept.md §10.

| Option | Trade |
|---|---|
| Fixed schedule (e.g. monthly) | Predictable, easy to automate; may fire when nothing has changed, or miss a burst of risky work between cycles |
| Milestone-triggered (before a release, after a large work package closes) | Audits land when they're most useful; needs something to reliably trigger it |

**Lean:** no lean yet — this is closer to a developer preference than an
architectural tradeoff. Needs the developer's input directly.

---

## Governance shape

### D-08 — Does `project-A/README.md` duplicate a pointer to `INTERFACE.md`? · `open`

Referenced in concept.md §5.

**Lean: yes, one sentence, no content duplication** — the same move the
prior design used for the two-repo boundary (`CLAUDE.md` pointing across
repos rather than restating anything). A GitHub visitor to `project-A`
should not have to already know `.gov` exists.

### D-09 — Changelog shape: mirrored `changelog/` folder, sister files, or per-area history folders? · `decided, 2026-08-20`

Referenced in concept.md §6.3. Resolved in the concept document itself: one
`changelog/` folder per governance repo, files named by record id
(`changelog/ADR-004.md`), not mirroring the document tree. Recorded here so
the decision has a place to live if it needs revisiting, not because it's
still open.

---

## How to use this file

Same convention as the prior design: answer in place, in the section, with
a date. When an answer dissolves a later question, strike the question
through rather than deleting it, and say what dissolved it. Record the
session that answers these in `project-A.ai/build-reports/` once that repo
exists — for now, in whatever session log this conversation is using.
