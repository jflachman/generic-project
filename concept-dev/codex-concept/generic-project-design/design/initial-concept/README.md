<!--
  generic-project-design | design/initial-concept/README.md
  Written 2026-08-18. Source material: /workspaces/strategy-lab-console
  (measured, not remembered), plus /workspaces/strategy-lab and
  /workspaces/strategy-lab-charts for the family pattern.
-->

# Initial concept — a reusable two-repo project template for AI-led development

**Status:** concept, nothing decided. This directory is the working area for
the design conversation; every recommendation below is a starting position to
argue with, not a settled choice.

---

## 1. The problem this template is for

A project built primarily by an AI agent accumulates two very different kinds
of material:

1. **The product** — source, tests, and the durable documents that describe
   what it is and why it is shaped that way (architecture decisions,
   contracts, specs). A consumer of the project needs these.
2. **The coordination corpus** — session protocols, work packages, prompts,
   build reports, gap logs, mockups, run queues, state. Only a *builder* of
   the project needs these, but the builder needs them constantly, and they
   grow far faster than the product does.

In `strategy-lab-console` these live in one repo, and the second kind is
`.gitignore`d. The measured result: **269 of 463 coordination files are not
version-controlled at all**, and the ones that are required
`git add -f` one at a time. The same directory is also listed in
`.claudeignore`, so the corpus the AI depends on is nominally excluded from
the AI's own default reads.

That is the single largest structural problem this template exists to fix,
and it drives the whole layout: **the coordination corpus gets its own git
repository.**

---

## 2. The three folders

Created under `/workspaces/generic-project/`:

| Folder | Role | Ships? |
|---|---|---|
| `generic/` | The **product repo** — code plus the durable governance a consumer needs. Cloned to GitHub. | Yes |
| `generic-dev/` | The **coordination repo** — everything the AI needs to build the product: protocol, work packages, prompts, build reports, gaps, design, state. Cloned to GitHub. | Yes |
| `generic-project-design/` | The **scaffolding conversation** — where we design the other two. **Deleted at instantiation time.** Never cloned. | No |

Both `generic/` and `generic-dev/` are currently empty on purpose. They get
populated once the open decisions in [`docs/06-open-questions.md`](docs/06-open-questions.md)
are made — filling them in first would prejudge the answers.

## 3. How it is meant to be used

```
cp -r generic-project/  ../my-thing-suite/     # copy the parent
rm -rf my-thing-suite/generic-project-design/  # drop the scaffolding
# rename generic/ → my-thing/, generic-dev/ → my-thing-dev/
# substitute the placeholder tokens
git init in each; push both to GitHub
```

Mechanics, token list, and the ordering that matters:
[`docs/07-instantiation-checklist.md`](docs/07-instantiation-checklist.md).

The parent folder is a **container, not a repo** — it is never cloned, has no
`.git` of its own, and exists so a family of related projects sits together
on disk. `strategy-lab` is exactly such a family: `strategy-lab`,
`strategy-lab-console`, `strategy-lab-charts`, each with a `-dev` sibling.

---

## 4. Reading order for this concept

| # | Document | What it settles (or asks) |
|---|---|---|
| 1 | [`docs/01-naming-and-repo-topology.md`](docs/01-naming-and-repo-topology.md) | What to call the parent (**recommendation: `<family>-suite/`, not `<family>/`**), the `-dev` suffix question, and why two repos rather than one or three |
| 2 | [`docs/02-console-approaches-inventory.md`](docs/02-console-approaches-inventory.md) | The 17 mechanisms from `strategy-lab-console` worth carrying forward, each with what it actually buys |
| 3 | [`docs/03-what-broke-measured.md`](docs/03-what-broke-measured.md) | The seven measured failures in the same repo. Read this before 05 — the layout is a response to it |
| 4 | [`docs/04-file-formats-for-ai-readers.md`](docs/04-file-formats-for-ai-readers.md) | Markdown vs YAML vs JSON vs XML, per file *role*. Includes the token arithmetic and why XML is a prompt-delimiter, not a file format |
| 5 | [`docs/05-proposed-structure.md`](docs/05-proposed-structure.md) | A concrete proposed tree for `generic/` and `generic-dev/`, with the one rule that decides which repo anything goes in |
| 6 | [`docs/06-open-questions.md`](docs/06-open-questions.md) | **The discussion agenda.** 14 numbered decisions, options, and my lean on each |
| 7 | [`docs/07-instantiation-checklist.md`](docs/07-instantiation-checklist.md) | Copy → rename → publish, and the placeholder-token contract that makes it mechanical |

`prompts/` and `build-reports/` are the working directories for this design
project itself — it runs on the same protocol it is designing. See
[`PROMPT-TRACKER.md`](PROMPT-TRACKER.md).

---

## 5. The three questions everything else hangs off

Stated here so they do not get lost in the detail:

1. **Where is the line between the two repos?** Proposed rule:
   *the product repo holds what a **consumer** of the project needs; the dev
   repo holds what a **builder** of it needs.* It is clean, it explains the
   real cases (a contract another repo mirrors is consumer-facing; a build
   report is not), and it is arguable — see D-03.
2. **What stops files from growing until they are unreadable?** Budgets are
   worthless without a check. Proposal: a hot/cold/archive tier, a declared
   line budget per tier, and a lint script in CI that fails the build. See
   D-06 through D-08.
3. **What is markdown and what is data?** Proposal: prose and rationale stay
   markdown; anything enumerated, filtered, counted, or status-tracked
   becomes YAML front matter with a generated markdown view. The three
   biggest files in the console are all the second kind stored as the first.
   See D-09 through D-11.
