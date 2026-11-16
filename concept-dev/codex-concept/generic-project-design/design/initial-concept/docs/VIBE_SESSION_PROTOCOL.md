<!--
  Strategy-Lab Console | VIBE_SESSION_PROTOCOL.md
-->

# Vibe Session Protocol

**Purpose:** You (the researcher) describe a small piece of capability in
plain language. Claude Code turns that into governance updates and working
code in one session, without you having to write a spec by hand and
without Claude Code re-reading strategylab's full governance corpus every
time. This document is what Claude Code follows when a session starts.

This is a deliberately scaled-down mirror of strategylab's own
`AGENTS.md` discipline — same shape (read first, propose, implement, close
out), much smaller footprint, because the console's scope per session is
always one screen and one or two BFF endpoints, never a pipeline stage.

---

## How you start a session

Just describe what you want, at whatever size feels natural. Examples:

> "Add a table view screen for feature datasets — let me sort and filter
> columns and see basic stats per column."

> "On the Config Studio screen, add a warning banner if the researcher
> tries to save a config whose manifest pin doesn't match what's on
> disk."

> "Wrap `run_exit_sweep()` as a Run Panel option under Backtest, with the
> ability to pick which exit profiles to include."

You don't need to specify governance, endpoints, or file structure — that's
what the protocol below produces.

---

## What Claude Code does, in order

### 1. Read the minimal set

- `CLAUDE.md`
- `governance/UI_STATE.md`
- `.notes/work/PROMPT-TRACKER.md` — §1 is the ordered run queue across all
  work packages; it says which prompt is next and which are already
  `closed`. **If this session is running one of its prompts, mark that row
  `in progress` before doing anything else.**
- `ai-reference/ui-dev-reference.md`
- The relevant screen contract in `governance/screens/` (if one exists)

Nothing from strategylab's own governance yet.

### 2. Classify the request

State out loud which of the 16 categories in `governance/UI_CAPABILITIES.md`
this falls under. If it doesn't fit cleanly, say so before proceeding —
don't force-fit it.

### 3. Locate or draft the screen contract

- If `governance/screens/<screen>.md` exists, check the request against
  it: does it fit within "strategylab functions called" and "what this
  screen must never do," or does the contract need amending?
- If no contract exists yet, copy `governance/screens/_TEMPLATE.md` and
  fill in what's known so far — this can be minimal on the first pass and
  filled in further as the session progresses.

### 4. Mockup gate — required before building any new screen, wizard, tool, or editor

Skip this step if the request is a small addition to a screen that's
already built (e.g. "add a warning banner to Config Studio" — see the
examples in "How you start a session"). It applies whenever
`governance/UI_STATE.md`'s Screen status table (or `UI_TOOLBOX.md`, for a
tool/wizard smaller than a full screen) shows the thing being asked for as
not yet implemented.

- Draft **2–3 distinct mockup variants** as static HTML in
  `.notes/design/mockups/`, following the existing visual language
  (`N_screen_name.html`, next available number). Distinct means a real
  difference in layout or interaction approach, not color tweaks. If the
  capability genuinely has only one sane approach, one mockup plus a
  one-line note on why the others weren't worth drawing is enough — don't
  manufacture false variety.
- For each variant, write a short **researcher-workflow narrative**: the
  concrete pipeline task the researcher is trying to get done, and how
  they'd move through this specific mockup to do it. Not an abstract
  description of the UI — a walkthrough anchored to a real task (e.g. "the
  researcher just noticed `features_v2` is stale and wants to know which
  upstream artifact moved").
- Present the mockups and narratives to the researcher and get a direction
  before writing the screen contract or any frontend code. This is a real
  wait-for-approval point, same as step 6 below.
- Once a direction is picked, record it in the screen contract
  (`governance/screens/<screen>.md`) or `UI_TOOLBOX.md` entry — which
  mockup/approach was chosen and why — so the reasoning survives past this
  session.

The goal throughout is that the researcher is never confused by
strategylab's underlying complexity — favor the mockup variant that hides
pipeline mechanics behind a task the researcher already understands, over
one that mirrors strategylab's internal model more literally.

### 5. Identify the access path first, then the boundary

Per `ADR-UI-001`, ask this before anything else: **does the request only
need to display something that's already sitting in `{workspace}`, or does
it need to write, validate, or execute?**

- **Display only → Path 1.** No `strategylab-service` endpoint needed.
  Read the relevant `governance/contracts/workspace_artifact_contract/
  manifests/*.md` spec (never a strategylab ADR or slice contract) and
  implement it as a client-side read against the read-only mount. This is
  the default for most requests — check here before reaching for Path 2
  out of habit.
- **Write, validate, or execute → Path 2.** Name the strategylab
  function(s) `strategylab-service` will call. Pull **only** the
  routing-table entry in `ai-reference/ui-dev-reference.md` for that
  function — if it points to a specific strategylab `ai-reference/*.md`
  file or per-function doc, read only that one file.
- If the capability would require strategylab to do something it doesn't
  currently support (not just a new way to reach existing behavior), stop
  and flag it — that's a strategylab-side gap, not a console session. See
  `ADR-UI-001`, "what requires a new ADR, not just an implementation
  session." The same applies if Path 1 would need to read something the
  workspace artifact contract doesn't document — that's a
  contract-extension request against strategylab (`ADR-080` §8), not a
  console-side workaround.
  - **File the gap, don't quietly build around it or quietly drop it:**
    add an entry to `.notes/strategy-lab/gap-requests.md` (stable
    `GAPREQ-NNN` id, what's needed, what it blocks, what's checked to
    confirm it's a real gap) and mark the blocked capability **deferred**
    in the screen contract and `governance/UI_STATE.md`, pointing back at
    the id. strategy-lab changes happen on the researcher's own periodic
    cadence, separate from the console session that found the gap — see
    the process section at the top of that file. Once a `GAPREQ-NNN`
    lands upstream, a future session re-checks the real new function
    shape before un-deferring anything, same discipline as every other
    "verify against the real function" rule in this project.

### 6. Propose structure, wait for approval

Before writing code, state:
- The endpoint(s) being added or changed (method, path, request/response
  shape).
- The frontend component(s) being added or changed.
- Any screen contract changes.

Wait for a go-ahead, the same way strategylab implementation sessions wait
for approval on module structure before coding.

If this session's proposal includes an order across more than one config
type or pipeline stage (a phased work-package plan, a migration rollout,
a "what's next" recommendation), that order defaults to real pipeline
order per `CLAUDE.md`'s sequencing rule and `PIPELINE_DATA_MODEL.md` §2 —
earliest stage first, Backtest last. State the proposed order explicitly
as part of this step so the researcher can catch a bad default before
work starts, and call out plainly if the proposal deviates from pipeline
order for a stated engineering reason (e.g. build the simplest case
first to de-risk a shared mechanism) rather than silently reordering.

If this session's proposal includes an order across more than one config
type or pipeline stage (a phased work-package plan, a migration rollout,
a "what's next" recommendation), that order defaults to real pipeline
order per `CLAUDE.md`'s sequencing rule and `PIPELINE_DATA_MODEL.md` §2 —
earliest stage first, Backtest last. State the proposed order explicitly
as part of this step so the researcher can catch a bad default before
work starts, and call out plainly if the proposal deviates from pipeline
order for a stated engineering reason (e.g. build the simplest case
first to de-risk a shared mechanism) rather than silently reordering.

### 7. Implement incrementally

One endpoint or component at a time, with tests, before moving to the
next — mirrors strategylab's "one module at a time" rule. When this
slice's function reads a file an earlier slice's function wrote (or vice
versa), verification must include running the *other* slice's real code
path against this slice's real output at least once, not just this
slice's own isolated verification — a Save/Run file-path mismatch across
two sessions sat unnoticed for 9 days before this check existed
(`GAP-CONSOLE-011`/`GAP-CONSOLE-014`).

### 8. Close the session

Update, in this order:
1. `governance/UI_STATE.md` — what was built, test status.
2. The screen contract touched (or newly created).
3. `governance/UI_CAPABILITIES.md`, only if a new category or a materially
   new definition was needed.
4. `ai-reference/ui-dev-reference.md`'s routing table, only if a new
   strategylab function was newly wrapped.
5. **Create a build report** at
   `.notes/build-reports/<YYYYMMDD>-<prompt-title>.md` (kebab-case,
   `<prompt-title>` matching the session's prompt file name minus any
   numeric prefix, or a short slug if the session had no prompt file).
   Every session gets one, regardless of size — a scoping-only session
   still reports what was decided and why; a build session reports what
   was implemented, tested, and verified. Follow the shape of an existing
   report in `.notes/build-reports/` (e.g.
   `20260723-catalog-reusable-browser-build.md` for a full build,
   `20260722-phase-b-scoping-catchup.md` for a scoping-only session) —
   this repo has no `governance/STATE.md`/`IMPLEMENTATION_HISTORY.md`, so
   "what changed" always lives in `governance/UI_STATE.md` plus this
   report, not a separate history file.
6. **Update `.notes/work/PROMPT-TRACKER.md`** if this session ran a prompt
   from `.notes/work/package*/prompts/`: flip its §2 row from
   `in progress` to `closed` with the date and a link to the build report
   from step 5, then **delete its row from the §1 run queue and renumber
   the rows that remain**. If the session ended without finishing, set the
   row back to `queued` with a note and leave it in place in §1. If the
   session wrote new prompt files, add their rows (`queued`) and place
   them in §1. Add a line to the file's §4 change log either way.
7. **Log any deferred functionality or gaps found this session** to
   `.notes/gaps/console-gaps.md`, per `.notes/gaps/README.md`'s process —
   anything deliberately left out of scope, a real behavior discovered
   that diverges from what a mockup/contract assumed, an untested code
   path, or a follow-up worth a future session's attention. If a session
   finds nothing worth logging, say so explicitly in the build report
   rather than skipping this step silently. Capabilities blocked on
   strategylab itself still go in `.notes/strategy-lab/gap-requests.md`
   (step 5's process above), not here — see `.notes/gaps/README.md` for
   exactly which directory a given finding belongs in.

A session is not complete until step 8 is done, the same standing rule
strategylab applies to its own implementation sessions.

---

## Guardrails that apply regardless of session size

These come directly from `ADR-UI-001` and `ADR-UI-002` and are restated
here because they're easy to forget in a fast, small session:

- Every workspace write goes through a real strategylab function, called
  from `strategylab-service`. No exceptions, no "just this once, it's
  faster."
- Every validation result shown to the researcher is the direct output of
  a real strategylab validation call.
- The frontend never imports `strategylab` and never touches the
  filesystem directly — Path 1 reads happen over HTTP against the
  read-only workspace mount; Path 2 writes happen over HTTP to
  `strategylab-service`.
- Path 1 code never reads anything the `workspace_artifact_contract`
  doesn't document, even if it can technically see the file on the
  read-only mount.
- `strategylab`'s own repository and `pyproject.toml` are never touched by
  a console session.
