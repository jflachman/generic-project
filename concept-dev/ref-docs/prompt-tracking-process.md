<!--
  prompt-tracking-process.md
  A portable description of the work-package / prompt-tracking process used in
  the Strategy-Lab Console repo, written so another project can adopt it from
  scratch. Nothing in here is console-specific except where marked
  "adapt this". Extracted 2026-08-21.
-->

# Work packages and prompt tracking — the process

**What this solves.** Once an AI-assisted project is more than a few sessions
old, three questions get expensive to answer:

1. *What should I work on next?* — and why that, not something else.
2. *What was already done, and where is the record of it?*
3. *What was deliberately left out, and is it still left out on purpose?*

The process below answers all three from files in the repo, so that a fresh
session with no memory of prior sessions can pick up correct work by reading
two documents. It costs roughly ten minutes at the end of each session and
removes the "re-derive the backlog from git log" tax at the start of every
one.

It has four moving parts:

- **Work packages** — a themed bundle of related work, with its own directory.
- **Prompts** — one file per runnable session, living inside a package.
- **Build reports** — one file per finished session, beside its prompt.
- **A tracker/history pair** — the live queue, and the closed archive.

---

## 1. Directory layout

```
.notes/                                  ← or wherever your project keeps working notes
├── work/
│   ├── PROMPT-TRACKER.md                ← LIVE work only. "What do I run next."
│   ├── PROMPT-HISTORY.md                ← CLOSED work only. "What was done, where's the record."
│   ├── package001/
│   │   ├── README.md                    ← what this package is and why it exists
│   │   ├── PLAN.md                      ← the measured evidence + phase detail
│   │   ├── DESIGN.md                    ← only if the package introduces a new mechanism
│   │   ├── prompts/
│   │   │   ├── 001-<kebab-case-title>.md
│   │   │   ├── 002-<kebab-case-title>.md
│   │   │   └── 005b-<kebab-case-title>.md   ← suffix letter: see §3
│   │   └── build-reports/
│   │       ├── 001-<kebab-case-title>.md    ← same filename as its prompt
│   │       └── 002-<kebab-case-title>.md
│   ├── package002/
│   └── package003/
├── build-reports/                       ← package-LESS sessions only (see §5)
│   └── <YYYYMMDD>-<title>.md
└── gaps/
    └── <project>-gaps.md                ← deferred scope and follow-ups (see §7)
```

**Numbering.** Packages are `package001`, `package002`, … in the order they
were opened, never renumbered. Prompts are `001`, `002`, … within their
package, also never renumbered. Both numbers are permanent identifiers that
build reports, change logs, and cross-references point at.

**Adapt this:** if your notes directory is gitignored and force-tracked (as
the console's is), every new file under it needs `git add -f` or it silently
never gets committed. Check this once, then state it in your `CLAUDE.md` —
it is the single most common way this process quietly fails.

---

## 2. What a work package is

A package is **a theme, not a sprint**. It bundles work that shares a cause,
a mechanism, or a dependency chain, so the argument for doing it lives in one
place instead of being re-made per session.

Good package boundaries in practice:

- *One mechanism, rolled out across many cases* — "replace nine hand-built
  screens with one generic schema-driven wizard, one case per phase."
- *One triage pass and its consequences* — "close the gaps that another
  package named as blockers."
- *Two unrelated jobs that share a discovery* — "the sync session found both
  of these; they ship together because they came from the same measurement."

A package that would contain exactly one prompt usually should not be a
package — put that prompt in an existing package, or run it as a
package-less session (§5).

### `README.md` — the argument

States, in this order:

- A `<!-- ... -->` header naming the file, its open date, and what triggered
  the package.
- **What this package is** — the purpose in a paragraph, in the reader's
  terms, not the implementer's.
- **The specific items it covers** — usually a table: item, current state,
  what is left and where (which prompt).
- **Any honest scoping call** — the place where a prompt does *less* than its
  title implies, stated explicitly. (Example from the console: "`prompts/002`
  does not close `GAPREQ-006`, and does not claim to" — followed by why, and
  by what to do instead if the reader disagrees.) **Scoping calls belong in
  the README where they can be argued with, never buried in a prompt.**
- **Ordering** — why the prompts run in the order they do, including any
  cross-package dependency.
- **Deliverables** — the file tree the package will contain, with a note on
  anything deliberately absent (e.g. "no `DESIGN.md` — neither prompt
  introduces a new mechanism").

### `PLAN.md` — the evidence

The README argues; the PLAN *measures*. This is where you put the tables of
what you actually found when you looked: which files carry which field, how
many entries the catalog really has, what the current behavior is at which
line number. A prompt written without this is a prompt written from
assumption.

Two rules that keep PLAN.md honest:

- **Date every measurement**, and tell the running session to re-measure
  rather than trust the table. Measured facts rot.
- **Record the finding that invalidated a previous belief**, not just the
  current state. "The 'payoff is zero' note from three weeks ago expired on
  DATE because X" is more valuable than a clean table, because it tells the
  next reader which other beliefs to distrust.

### `DESIGN.md` — only when there is a new mechanism

Skip it when the package only widens, narrows, or repeats existing
mechanisms. Say in the README that you skipped it and why. A package whose
deliverable *is* a design (a mockup-and-pick session) puts the design in the
build report, not here.

---

## 3. What a prompt is

**A prompt is a complete session brief: everything a fresh agent with no
memory needs to do one unit of work correctly, and nothing else.**

The test for a good prompt: hand it to someone who has never seen the
project, with only the repo and the mandatory-reading list, and they produce
the intended result without asking a question you could have anticipated.

### Anatomy

```markdown
<!--
  <Project> | .notes/work/package<NNN>/prompts/<NNN>-<title>.md
  Written <date> by <which session>. <What it closes / why it exists.>
-->

# Package<NNN> / <NNN> — <Imperative title>

## Goal
<Two or three paragraphs. What changes for the user when this is done, and
why it is worth doing. Not a task list.>

---

## 0. Ordering — run this after <other prompt>          ← only when it matters
<Hard gate or soft preference? Say which. If the precondition has NOT been
met, tell the session what to do instead of guessing — usually "say so in the
build report and re-read these files rather than trusting the line numbers
below.">

## 1. The measured state — read this before designing anything
<The evidence table from PLAN.md, restated here so the prompt is
self-contained. Include the measurement date and the instruction to
re-measure.>

## 2. <Any conceptual model the session needs>
<E.g. "three persisted shapes, not one". This is the section that stops a
session from writing a correct-looking fix for a case it did not know
existed.>

## 3. What to build
### 3a. <First concrete change>
### 3b. <Second>
### 3c. <Third — the actual point of the change>
### 3d. Prove it, don't assert it
<How to verify. Name the fixture, the command, the observable result.>

## 4. <Anything the session must construct before it can verify>
<Fixtures, test data, a run that has to happen first. Be explicit about not
overwriting the existing case if the old case is itself the control.>

## 5. Definition of done
<A checklist. Every item observable by someone else.>
```

Sections 0, 2 and 4 are conditional; 1, 3 and 5 are not.

### Prompt-writing rules that earned their place

- **Number is permanent.** If you need to insert work between `005` and
  `006`, use `005b`. The console did exactly this for a follow-up that was
  not a migration phase and deliberately should not consume the number
  `006`. Renumbering breaks every existing reference.
- **Write prompts in batches, from a planning session.** The best prompts
  come out of a session whose whole job was scoping — it has the measurements
  fresh and can write three coherent prompts at once. Prompts written
  hurriedly at the end of a build session are the ones that turn out to be
  wrong.
- **State line numbers and file paths, and mark them as perishable.** They
  save a session real search time and cost nothing when stale, *provided* the
  prompt says "re-read rather than trusting these."
- **A prompt may not silently do less than its title.** If it closes half a
  gap, the title or an early section says so.

---

## 4. The tracker / history pair

This is the part that matters most, and the part most likely to be skipped
when a session is running long.

**The split exists for one reason: the tracker is read at the top of every
session, so it must stay short.** The console ran a single combined file for
two days and it grew past the point of being cheap to read; splitting it
moved thirteen closed rows, a finished package narrative, and a change log
out of the hot path.

### `PROMPT-TRACKER.md` — live work only

Structure:

- **Header** — a one-paragraph statement that this file is the single source
  of truth for "what do I run next", plus an explicit note that closed
  prompts are *not* here and where they went.
- **Scope** — which prompt directories this file tracks, and which historical
  prompt sets it deliberately does not.
- **Status vocabulary** — the table in §4.1 below.
- **§1 Run queue** — one ordered, numbered table of every runnable prompt.
  Columns: `#`, prompt (linked), package, status, **why it sits here**.
  That last column is the whole value of the file; a queue without stated
  reasons gets silently reordered by whoever reads it next.
  Follow the table with:
  - **Hard ordering constraints** — which rows are dependencies (cannot be
    reordered) versus priority (may be re-argued). Name the difference
    explicitly.
  - **Any ordering tradeoff, named rather than hidden.**
  - **Any project-wide sequencing rule and whether it is being deviated
    from.** *(Adapt this: the console has a "build earliest pipeline stage
    first" rule, and the tracker asserts per-queue-state that no deviation is
    in play. Your project's equivalent might be schema-before-UI, or
    migrations-before-features. If you have such a rule, the tracker is where
    it gets audited.)*
- **§2 Open packages and prompts** — per package: a header block with the
  directory, open date and links to README/PLAN/DESIGN, the purpose
  paragraph, a "*Closed: prompts X–Y*" line, and a table of every prompt not
  yet closed plus every planned-but-unwritten phase.
- **§3 Known open items deliberately *not* queued** — items and the reason
  each is not in §1. This section is what stops the same "did we forget
  about X?" conversation recurring monthly. Typical reasons: needs a human
  decision first; blocked on an upstream dependency; belongs to a phase that
  is not written yet.
- **§4 Change log for this file** — dated lines, most useful when they
  record *why the queue changed*, not just that it did.

### `PROMPT-HISTORY.md` — closed work only

Structure:

- **Header** — states this is the archive, and points to the tracker for live
  work. A running count ("as of DATE: N prompts closed across packages …").
- **Where build reports live** — the table in §5 below, plus any historical
  exception. The console's history file carries an explicit note that its
  index spans two locations *by history, not by rule*, because a directory
  listing had once been misread as "these packages have no build reports."
  **Record the misreadings; they recur.**
- **§1 Closed prompts — the full index** — chronological by close date.
  Columns: `#`, closed date, prompt (linked), package, purpose, build report
  (linked). This is the prompt → report index, and it is the answer to "where
  is the record of X."
- **§2 Closed package narratives** — moved across from the tracker's §2 when
  a package's last prompt closes.
- **§3 Resolved items that were once "deliberately not queued"** — moved from
  the tracker's §3 with the resolution recorded.
- **§4 Archived change log** — retired tracker §4 entries.

### 4.1 Status vocabulary

| Status | Meaning |
|---|---|
| `queued` | Written, not yet started. Sitting in the run queue. |
| `in progress` | A session is running it right now. Set **at session start**, before any other work. |
| `closed` | Session ran to completion, end-of-session checklist done, build report exists. **The row moves to `PROMPT-HISTORY.md` §1** and is deleted from the tracker. |
| `no prompt yet` | A phase exists in a package plan, but no prompt file has been written. Not runnable, not in the run queue. |

**`closed` is a transition, not a resting state.** Nothing is ever left in
the tracker wearing a `closed` badge — the row *moves*. This is the rule that
keeps the tracker short without anyone having to periodically prune it.

### 4.2 The session protocol

Every session that runs a prompt does all of this:

**On starting:**
1. Flip the prompt's row in tracker §2 to `in progress`, with the date.
   Leave it in §1 while it runs.

**On finishing:**
2. Write the build report to `package<NNN>/build-reports/`, named after the
   prompt file it answers.
3. Append the prompt's row to `PROMPT-HISTORY.md` §1 with its close date and
   a link to that report.
4. If this closed the package's last open prompt, move the package narrative
   from tracker §2 to history §2. If a tracker §3 item stopped being an open
   question, move it to history §3.
5. **Delete** the row from tracker §1 (renumbering what remains) *and* from
   its package table in §2.
6. Add a line to tracker §4's change log.

**If the session ends without finishing:** skip steps 2–5 entirely. Set the
row back to `queued` with a note, leave it in §1 in its original position,
and still add a §4 change-log line.

**If the session wrote new prompt files:** add their rows (`queued`) to
tracker §2 and place them in §1 with a stated reason.

A session that ran a prompt is **not complete** until both files are updated
and the build report exists.

---

## 5. Build reports

**Every session produces one — no exceptions.** A scoping-only or
decision-only session still reports what was decided and why; that report is
often more valuable than a build report, because decisions are the thing git
history cannot reconstruct.

### Where it goes

| Session type | Path | Naming |
|---|---|---|
| **Ran a package prompt** | `.notes/work/package<NNN>/build-reports/` | mirrors the prompt filename exactly — prompt `003-pine-library-screen.md` → report `003-pine-library-screen.md` |
| **No package** — an upstream sync, a verification sweep, an ad-hoc request | `.notes/build-reports/` | `<YYYYMMDD>-<title>.md` |

Co-location is the point of the first row: a package directory should show
its own complete record — prompt and report side by side — without a lookup.
The central directory is *not* deprecated; it is specifically for
package-less sessions.

**Adopt the co-location rule from day one.** The console adopted it late, so
its report index permanently spans two locations and needs a paragraph
explaining why.

### Report anatomy

```markdown
# Build report — Package<NNN> / <Phase or title>

**Date:** YYYY-MM-DD
**Prompt:** `../prompts/<NNN>-<title>.md`

## What was produced
<Files added/changed, endpoints, components. Concrete.>

## Real findings
<What turned out to be different from what the prompt assumed. This is the
most valuable section in the file — it is what the next prompt-writing
session reads.>

## Verification
<What was run, what passed, what was checked by hand. Include the failures.>

## Deferred / gaps
<Everything left out on purpose, cross-referenced to the gaps file. If
nothing came up, SAY SO explicitly — a silent section is indistinguishable
from a skipped step.>

## Next
<What this unblocks, or what should follow.>
```

The `**Date:**` and `**Prompt:**` lines are load-bearing: they make the
report traceable from either direction, and they are what an audit checks.

---

## 6. Wiring it into the project's agent instructions

The process only works if it is in the file every session reads. Add to your
`CLAUDE.md` (or `AGENTS.md`):

**In the "current work queue" section:**

> `.notes/work/PROMPT-TRACKER.md` is the **single source of truth for which
> prompt to run next** — the **live** work only: open packages, every
> `queued` / `in progress` prompt, and one ordered run queue in its §1. A
> session that runs a prompt marks it `in progress` before starting, and on
> finishing **moves** its row out to `.notes/work/PROMPT-HISTORY.md` rather
> than leaving a `closed` badge behind.
>
> `.notes/work/PROMPT-HISTORY.md` is the **closed-work archive** — the
> prompt → build-report index for every prompt ever closed, plus the
> narratives of fully-closed packages and the archived change log. Read it
> when you need to know what was already done and where the record is; never
> to decide what to run next.

**In the end-of-session checklist:** the build-report step (§5 above) and the
two-work-tracking-files step (§4.2 above), written out in full. Do not
compress them to "update the tracker" — the compressed version gets done
incompletely.

**In the session protocol document**, if you keep one separately: the same
two steps, as the authoritative version, with the checklist in `CLAUDE.md`
pointing at it.

---

## 7. The adjacent files this process assumes

Two more files carry the weight that would otherwise land in the tracker:

- **A gaps log** (`.notes/gaps/<project>-gaps.md`) — deferred scope, behavior
  that diverged from what a mockup or contract assumed, untested paths,
  follow-ups. Every session logs to it or explicitly states in its build
  report that nothing came up. Gap entries get stable ids (`GAP-NNN`) so
  prompts can say "closes `GAP-041`."
- **An upstream-request log**, if your project depends on another repo you
  also control (`.notes/<upstream>/gap-requests.md`). Things the other repo
  must do first, with ids (`GAPREQ-NNN`) and a status (`open` → `resolved` →
  `closed`). The distinction that matters: `resolved` means upstream did its
  half, and something on *your* side is still outstanding. Those leftover
  halves are excellent package material — the console's package005 is exactly
  that.

Both feed the tracker: a gap with a decision attached becomes a queued
prompt; a gap awaiting a human decision sits in tracker §3 with the reason.

---

## 8. Adopting this in a project that already has history

Order that worked:

1. **Inventory first.** List every prompt-like document already in the repo.
   Mark each `closed` or `queued`. Match every closed one to its existing
   report; the gaps you find are real.
2. **Create `PROMPT-TRACKER.md` with both sections** (live and closed), and
   import the run order from wherever it currently lives — usually a
   package `PLAN.md`. Note in the tracker that it *supersedes* that plan's
   ordering table as the live queue, while the plan stays as the written
   argument for why the order is what it is.
3. **Declare which historical prompt sets are out of scope** and say so in
   the tracker's scope note. Old prompt directories that are finished should
   not be back-filled; they just need to be named as deliberately untracked.
4. **Split out `PROMPT-HISTORY.md` when the tracker stops being cheap to
   read** — for the console that was at about thirteen closed rows.
5. **Adopt co-located build reports immediately**, and accept that older
   reports stay where they are with the index pointing at both locations.

Two failure modes to expect:

- **A directory listing misread as missing work.** A package with no
  `build-reports/` subdirectory looks like a package with no reports. Say
  in the history file where each report actually is.
- **The end-of-session steps skipped when a session runs long.** The
  countermeasure is that the steps are in `CLAUDE.md`'s checklist *and* the
  session protocol *and* the tracker's own protocol section. Three copies is
  not redundancy here; it is the only reason it gets done.
