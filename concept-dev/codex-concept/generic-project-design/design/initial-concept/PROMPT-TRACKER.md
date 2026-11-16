<!--
  generic-project-design | design/initial-concept/PROMPT-TRACKER.md
  Dogfooding: this design project runs on the mechanism it is designing.
  Carried from /workspaces/strategy-lab-console/.notes/work/PROMPT-TRACKER.md
  (created 2026-08-18).
-->

# Prompt tracker — template design

**Single source of truth for what to run next in this design project.**

Hand-maintained for now. It should become a **generated** artifact of the
prompt front matter once D-10 is decided — a hand-maintained queue is
exactly what produced three disagreeing "what's next" pointers in
`strategy-lab-console` ([`docs/03-what-broke-measured.md`](docs/03-what-broke-measured.md) §5).

## Status vocabulary

| Status | Meaning |
|---|---|
| `queued` | Written, not started. Sits in §1 |
| `in progress` | A session is running it now. Set **at session start** |
| `closed` | Ran to completion, build report exists. Removed from §1 |

**Protocol:** flip to `in progress` when a session starts; flip to `closed`,
link the build report, and delete the row from §1 when it ends. Both ends.

---

## 1. Run queue

| # | Prompt | Status | Decides | Why here |
|---|---|---|---|---|
| **1** | [prompts/004-build-instantiation-tooling.md](prompts/004-build-instantiation-tooling.md) | `queued` | — | Build `init` tooling, template manifest, and token conversion after scaffold population |

**Hard constraint:** #2 after #1; #3 after #2. The checker precedes the
scaffold on purpose — see prompt `002`'s Goal for the argument.

---

## 2. Inventory

| Prompt | Purpose | Status | Report |
|---|---|---|---|
| [001-decide-topology-and-formats](prompts/001-decide-topology-and-formats.md) | Answer the eight load-bearing open questions and update the accepted structure to match. Decision session, no scaffold. | `closed` | [20260819-decide-topology-and-formats](build-reports/20260819-decide-topology-and-formats.md) |
| [002-build-the-check-suite](prompts/002-build-the-check-suite.md) | Write `check-governance` — the executable form of every invariant — before there is a project to check. | `closed` | [20260820-build-the-check-suite](build-reports/20260820-build-the-check-suite.md) |
| [003-populate-the-two-repo-scaffold](prompts/003-populate-the-two-repo-scaffold.md) | Populate the accepted product/dev scaffold and run the checker against it. | `closed` | [20260820-populate-the-two-repo-scaffold](build-reports/20260820-populate-the-two-repo-scaffold.md) |
| [004-build-instantiation-tooling](prompts/004-build-instantiation-tooling.md) | Build the manifest and mechanical copy/rename/token-replacement path for instantiating the template. | `queued` | — |

---

## 3. Change log

| Date | Change |
|---|---|
| 2026-08-20 | Prompt 003 closed; two-repo scaffold populated, D-14 decided, prompt 004 queued. |
| 2026-08-20 | Prompt 003 started; status set to `in progress`. |
| 2026-08-20 | Prompt 002 closed; governance checker, fixtures, tests, and prompt 003 added. |
| 2026-08-20 | Prompt 002 started; status set to `in progress`. |
| 2026-08-19 | Prompt 001 closed; D-01…D-05 and D-09…D-11 decided; `docs/05-proposed-structure.md` updated as accepted baseline; build report added. |
| 2026-08-19 | Prompt 001 started; status set to `in progress`. |
| 2026-08-18 | Created with the initial concept. Two prompts written, both `queued`. |
