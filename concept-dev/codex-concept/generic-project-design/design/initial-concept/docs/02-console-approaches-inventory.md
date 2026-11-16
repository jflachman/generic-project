<!--
  generic-project-design | design/initial-concept/docs/02-console-approaches-inventory.md
  Every claim here was checked against /workspaces/strategy-lab-console on
  2026-08-18, not recalled.
-->

# 02 — What `strategy-lab-console` does that is worth keeping

Seventeen mechanisms, grouped by what they control. For each: what it is,
and **what it actually buys** — because several of these look like ceremony
until you see the failure they prevent.

The companion document is [`03-what-broke-measured.md`](03-what-broke-measured.md).
Read both before designing the tree; roughly half of these mechanisms are
excellent and half are excellent *ideas* whose implementation collapsed under
its own volume.

---

## A. Controlling what the agent reads

### A1 — A two-file constitution: `CLAUDE.md` + `VIBE_SESSION_PROTOCOL.md`

`CLAUDE.md` (14 KB) answers *what is this project and what may I never do*.
`VIBE_SESSION_PROTOCOL.md` (12 KB) answers *how does a session run, step by
step*. The split holds up: the first is stable, the second is procedural, and
separating them means a protocol change does not touch the constitution.

**Buys:** a new session reaches competence in two files.

### A2 — A numbered, capped, mandatory reading order — with an explicit *stop*

Six numbered items, several conditional ("only if the session touches
Path 2"), closing with: *"Do not begin implementation until steps 1–5 (and 6,
when it applies) are complete."*

**Buys:** the failure mode it prevents is not ignorance, it is *ingestion* —
an agent that reads 40 documents and then has no budget left to work.

### A3 — Explicit negative reading rules

The list says what **not** to read as forcefully as what to read: *"never a
strategylab ADR, slice contract, or the full `AGENTS.md`."*

**Buys:** this is the highest-leverage line in the whole corpus. Positive
lists are advisory — an agent that finds an interesting adjacent document
will read it. Only a prohibition stops that.

### A4 — A routing table in `ai-reference/`

`ai-reference/ui-dev-reference.md` (24 KB) carries a capability taxonomy, a
screen inventory, and a **function → "load exactly this one upstream doc"**
routing table.

**Buys:** it converts "read the upstream corpus" into "read one file," and it
is the mechanism that makes A2's cap survivable. This is the single most
transferable idea in the repo.

---

## B. Governing the work

### B1 — A closed capability taxonomy

`governance/UI_CAPABILITIES.md` defines 16 numbered categories, and protocol
step 2 requires every request to be classified into one out loud — *"If it
doesn't fit cleanly, say so before proceeding — don't force-fit it."*

**Buys:** the escape hatch is the point. Forcing classification finds
scope creep at minute one instead of at review.

### B2 — Per-unit contracts from a template, including a "must never" section

`governance/screens/*.md`, each generated from `_TEMPLATE.md`, with a
**"What this screen must never do"** section carrying inherited boilerplate
(*"must never show a validation result the UI computed itself"*).

**Buys:** governed negative space. Most templates specify only what a thing
does; the bugs come from what it quietly started doing.

### B3 — ADRs with stable ids, referenced by id everywhere

`ADR-UI-001/002/003`, cited by number in prose across the corpus.

**Buys:** decisions become addressable. "Per `ADR-UI-001`" is checkable;
"as we discussed" is not.

### B4 — A default build order, with deviation as a *speech act*

`CLAUDE.md` mandates that multi-stage plans are built earliest-domain-stage
first, and that deviating "must be stated explicitly to the researcher and
confirmed, not applied silently." It then names the real incident that caused
the rule.

**Buys:** two things. Sensible defaults, and — more valuable — a norm that
*silence is the violation*. Deviating is allowed; deviating quietly is not.

### B5 — Rules cite the incident that produced them

The build-order rule ends: *"(This corrected a real instance:
`.notes/work/package001/DESIGN.md` originally migrated Backtest first for
exactly this smallest-mechanism reasoning — reordered 2026-08-07.)"*

**Buys:** rules with a scar are obeyed; rules without one get "optimized
away" by the next agent that finds them inconvenient.

---

## C. Structuring multi-session work

### C1 — Work packages

`.notes/work/packageNNN/` = `README.md` (why this exists) + `DESIGN.md`
(architecture) + `PLAN.md` (phases, decisions, dependencies) +
`prompts/` (session briefs) + `build-reports/`.

**Buys:** an initiative larger than one session gets a home, so its context
survives a `/clear`. Note that packages 003 and 004 deliberately have *no*
`DESIGN.md` — package004 says why: *"prompt `002`'s entire deliverable is a
design — putting a `DESIGN.md` here now would prejudge it."* The template is
applied with judgment, which is the right way to apply one.

### C2 — Prompts as durable, numbered session briefs

Each is a file, not a chat message: Goal / Mandatory reading / Preconditions /
**"Two things this phase is not"** / deliverables.

**Buys:** reproducibility and reviewability — you can read what the next
session will do before it does it. The negative-scope section is doing most
of the work.

### C3 — Decision tables with the answer written back in

`PLAN.md` files carry `D-A`…`D-F` tables where each row is a question whose
cell is later overwritten with the resolution and its date — including
struck-through dissolved ones (*"`D-F` ~~Accept pandas_ta's numpy cap?~~
**Dissolved by `D-A`'s revision**"*).

**Buys:** the question and its answer stay in one place. A decision recorded
elsewhere is a decision that will be relitigated.

### C4 — A build report per session, without exception

`.notes/build-reports/<YYYYMMDD>-<slug>.md`, 66 files, mandated *"every
session, not just full builds; a scoping-only or decision-only session still
reports what was decided and why."*

**Buys:** the "we discussed this once" problem, solved. The exceptionless
framing is load-bearing — the sessions most worth recording are the ones that
produced no code.

### C5 — One ordered run queue with a status lifecycle

`.notes/work/PROMPT-TRACKER.md` (created 2026-08-18): every package, every
prompt, `queued` → `in progress` → `closed`, one ordered §1, rows deleted
from the queue as they close. Wired into protocol step 1 *and* step 8, so it
is updated at both ends of a session.

**Buys:** it replaced three competing "what's next" pointers. The design
lesson is in the wiring, not the file: a tracker only updated at session end
is stale for the whole session.

---

## D. Not losing what a session learned

### D1 — Two gap logs, with an explicit routing rule

`.notes/gaps/console-gaps.md` (this repo can close it) vs
`.notes/strategy-lab/gap-requests.md` (needs an upstream change first), and a
one-line test to route by: *"can a console session alone close this, with no
strategylab code change?"*

**Buys:** two backlogs with different cadences and different owners stop
contaminating each other.

### D2 — Stable ids, a status lifecycle, and "do not act unilaterally"

`GAP-CONSOLE-NNN` / `GAPREQ-NNN`; `open` → `planned` → `wontfix` → `closed`;
closed entries stay in the file; and explicitly: *"a session deciding on its
own to 'clean up the gaps backlog' is not [fine], unless asked."*

**Buys:** the anti-helpfulness clause is the good part. Without it, agents
opportunistically drain backlogs and every session becomes unbounded.

### D3 — Amendment-in-place with the original left visible

package002's README amends its own estimates with a dated block and
strikethrough — *"the original text is struck through rather than rewritten,
so the estimate and the measurement stay distinguishable."*

**Buys:** you can audit whether the original reasoning was sound, which a
clean overwrite destroys.

### D4 — "Verify against the real thing, do not trust this document"

Recurring instruction: *"**Read the real raise**, do not trust this prompt's
quoting of it."* And, on a line number that shifted by one: *"Grep the
sentence, do not trust either number."*

**Buys:** the corpus stops being a second source of truth that can rot
silently. Every prompt teaches its own fallibility.

### D5 — Provenance header on every file

Every document opens with `<!-- Project | path/to/self.md -->`.

**Buys:** a file pasted into a chat still knows where it came from — and an
agent asked to update "the plan" can tell which of four plans it is holding.

### D6 — A separate, machine-readable agent-memory tier

`.wolf/` (OpenWolf): `anatomy.md` (505 files with descriptions and token
sizes), `cerebrum.md` (preferences / learnings / **Do-Not-Repeat**),
`buglog.json`, `memory.md`, `STATUS.md`.

**Buys:** a place for *agent-operational* knowledge ("`frontend/` is pnpm,
not npm") that would pollute governance if filed there. The Do-Not-Repeat
list is the standout — it is the only structure in the repo that reliably
prevents a *repeated* mistake rather than recording a past one.

---

## E. Design discipline

### E1 — A mockup-first gate with a human decision point

*"Every new screen, wizard, tool, or editor starts with mockups, not code"* —
2–3 variants plus a researcher-workflow narrative each, and a direction
picked before the contract is written. `.notes/design/mockups/` holds 285
files across 13 screens.

**Buys:** cheap iteration where iteration is cheap. The narrative-per-variant
requirement is what keeps it from being a beauty contest.

### E2 — Contract mirroring across a repo boundary

The console keeps a local copy of the upstream artifact contract and reads
*only* that, never upstream's own governance.

**Buys:** genuine decoupling — until the mirror rots. See
[`03-what-broke-measured.md`](03-what-broke-measured.md) §7 for the bill.

---

## Summary — the transferable core

If only five things carry over, these:

1. **A2/A3** — a capped reading order with explicit prohibitions.
2. **A4** — the routing table that makes the cap survivable.
3. **B2** — per-unit contracts with a governed "must never" section.
4. **C4/C5** — a build report every session, and exactly one ordered queue.
5. **D2/D4** — stable ids with an anti-unilateral clause, and the standing
   instruction to verify against the real artifact rather than the document.
