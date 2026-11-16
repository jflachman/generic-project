<!--
  generic-project-design | design/initial-concept/docs/03-what-broke-measured.md
  All figures measured in /workspaces/strategy-lab-console on 2026-08-18.
-->

# 03 — What broke, measured

Seven failures in a repo whose *ideas* are sound. Each is a design
requirement for the template, stated as such at the end of the section.

---

## 1. The always-read state file became the largest document in the project

`governance/UI_STATE.md` — **339 KB, 4,556 lines**. It is item 2 of the
mandatory reading order, so it is nominally read *every session*.

Worse than the size is the shape:

| Metric | Value |
|---|---|
| `##` headings in the whole file | 6 |
| `###` headings in the whole file | **0** |
| Lines under the single `## Current phase` heading | **3,777** (lines 16–3792) |

Nearly 3,800 lines with no internal structure — sessions appended prose to a
running paragraph for six weeks. It cannot be skimmed, sectioned, diffed
usefully, or partially loaded.

**Requirement:** a file that every session *writes* must never also be a file
every session *reads in full*. Append targets and read targets are different
files. See D-06.

## 2. "Lightweight contracts" grew past the code they govern

`governance/screens/_TEMPLATE.md` instructs: *"Keep it short — this is a
lightweight contract, not a strategylab-style slice document."*

| File | Size |
|---|---|
| `_TEMPLATE.md` | 2.8 KB |
| `run_panel.md` | **147 KB** |
| `config_studio.md` | **140 KB** |
| `data_explorer.md` | 55 KB |

Two contracts are **50×** their own template. The instruction to stay short
was present, in the file being copied, and lost every time.

**Requirement:** a size rule that is only prose is decoration. It needs a
number and a check that fails. See D-07.

## 3. Append-only logs were never rotated

| File | Size | Lines |
|---|---|---|
| `.notes/gaps/console-gaps.md` | **181 KB** | 2,935 |
| `.notes/strategy-lab/gap-requests.md` | 70 KB | — |
| `.notes/strategy-lab/gaps-closed.md` | 65 KB | — |

The third file is the encouraging part: `gap-requests.md` hit the same wall
and was split (*"2055 → 1090 lines; 7 closed entries moved to
`gaps-closed.md` with a summary table + do-not-read note left behind"*). The
fix works. It was applied **once, reactively, to one of the two logs** — the
larger one is untouched.

**Requirement:** rotation is a scheduled, triggered operation with a stated
threshold, not something noticed when a file becomes annoying. See D-08.

## 4. The constitution went stale because it contained mutable state

`CLAUDE.md` §"Current phase" says: *"Setup / scaffolding."*
Ten screen contracts are marked `built`.

The same section directs every session to read two files:

> *"lives in `governance/STATE.md` … and `.notes/build-reports/IMPLEMENTATION_HISTORY.md`. Do not duplicate that history here; read it directly."*

**Neither file exists.** And `VIBE_SESSION_PROTOCOL.md` line 202 says so
outright: *"this repo has no `governance/STATE.md`/`IMPLEMENTATION_HISTORY.md`"*.

So the two documents every session must read contradict each other, and the
first one sends every session to two missing paths.

**Requirement:** the constitution contains **zero mutable state** — no phase,
no status, no "current work". It may contain *pointers*, and every pointer
must be link-checked mechanically. See D-06, D-12.

## 5. There were three competing answers to "what do I do next"

As of this morning: `.wolf/STATUS.md`'s next-quest block,
`UI_STATE.md`'s "Current work queue" (line 3907), and
`package004/PLAN.md` §1. Each was written by a different session, each was
sincere, and they were not guaranteed to agree.

Fixed today by `PROMPT-TRACKER.md`, which one of them now defers to. The
generalization is what matters.

**Requirement:** exactly one queue, named in the constitution as *the* queue,
with every other location holding a pointer to it and no content. See D-13.

## 6. The coordination corpus was not version-controlled

`.notes/` appears in `.gitignore` (line 5) **and** `.claudeignore`
(`**/.notes/`).

| | Count |
|---|---|
| Files under `.notes/` on disk | 463 |
| Tracked in git | 194 |
| **Untracked** | **269** |

Every tracked file needed an explicit `git add -f` — a step a session must
remember, forever, or the work silently exists on one machine only. This is
recorded as standing knowledge in the agent's own memory (*"new files under
`.notes/` need `git add -f` to show up at all"*), which is the tell: a
structural defect had to be papered over with agent memory.

**Requirement:** this is the reason for the `<project>-dev/` repo. Nothing in
the coordination corpus is ignored anywhere, ever.

## 7. A cross-repo mirror rotted six weeks with no signal

`governance/contracts/workspace_artifact_contract/` mirrors an upstream
contract. On 2026-08-18 a sync session found **11 of 18 files stale, six
weeks old**. There was no recorded upstream commit, no script, and no check.
The contract's own README §9 states a pinning obligation the console did not
honour.

The drift was found *by accident*, while a different prompt was verifying an
unrelated precondition.

**Requirement:** any mirrored or duplicated content ships with a sync record
(upstream ref + date) and a one-command check, **in the same change that
creates the mirror**. This applies directly to the `<project>` ↔
`<project>-dev` split, which creates exactly this class of boundary. See
D-04.

---

## The pattern underneath all seven

Six of the seven are the same failure: **a rule with no enforcement, in a
corpus whose only reader is an agent optimizing for the current task.**

- "Keep it short" — no check → 147 KB.
- "Do not duplicate history here" — no check → duplicated and stale.
- "Read the mirror's §9 pinning obligation" — no check → six weeks stale.
- "`git add -f`" — no check → 269 files lost.

The console's *documents* are unusually well written. That is the point: good
prose is not the control. **The template's differentiator must be that its
invariants are executable** — a lint script, a link checker, a size budget, a
sync check, run in CI and in the session-close step, so that violating a rule
fails loudly instead of accumulating quietly.

See [`06-open-questions.md`](06-open-questions.md) D-12 for what that check
suite should cover.
