<!--
  generic-project-design | design/initial-concept/docs/01-naming-and-repo-topology.md
-->

# 01 — Naming and repo topology

## 1. The parent folder name

You asked whether there is a better name than `generic-parent`. Yes — and
also better than the pattern in your own example.

Your example was: parent `strategy-lab/`, containing `strategy-lab/`,
`strategy-lab-dev/`, `strategy-lab-console/`, `strategy-lab-console-dev/`,
`strategy-lab-charts/`, `strategy-lab-charts-dev/`.

**The problem with that is the collision:** `strategy-lab/strategy-lab/`. It
costs you three concrete things:

- **Ambiguous references.** "It's in `strategy-lab/governance/`" now has two
  readings. Every path in every document has to be absolute or prefixed to
  disambiguate — and an AI agent resolving a relative path guesses.
- **Broken `cd` muscle memory**, for you and for the agent's shell commands.
- **`grep -r strategy-lab`** stops meaning anything useful.

### Options

| Candidate | Reads as | Verdict |
|---|---|---|
| `strategy-lab/` | the flagship repo | ✗ collides with the child of the same name |
| `strategy-lab-parent/` | a data-structure term | ✗ describes the folder's position, not its contents |
| `strategy-lab-workspace/` | a grouping of repos | ⚠ good English, but `{workspace}` already means *the data directory* throughout strategylab. Do not overload it **in this family** |
| `strategy-lab-repos/` | a grouping of repos | ○ honest, slightly flat |
| **`strategy-lab-suite/`** | a family of related products | ✓ **recommended** |

**Recommendation: `<family>-suite/`.** It never collides with a child, it is
obviously not itself a repo, it sorts adjacent to the children, and "suite"
already carries the right meaning (several shipped things that belong
together) without borrowing a term the domain has spoken for.

For the template as created, the parent is `generic-project/` — which is what
you asked for and works fine as a placeholder, since the name is replaced at
instantiation. The *rule* to encode in the template is `<family>-suite/`.

> **Note the one-project case.** If a family only ever has one product, the
> parent is nearly pure overhead — two folders in a wrapper. It still earns
> its place if you want the `-dev` sibling adjacent rather than nested, but
> it is worth deciding deliberately rather than by default. See **D-01**.

## 2. The `-dev` suffix

`<project>-dev` is short, sorts adjacent to `<project>`, and you have already
chosen it. The one thing worth weighing before it becomes 30 repos:

| Suffix | Risk |
|---|---|
| `-dev` | Reads to any outsider — and to a fresh agent — as *"the development branch/environment of the project"*. Someone clones it expecting code and gets build reports |
| `-ai` | Honest about the audience, but ages badly if a human ever curates it |
| `-notes` | Honest, matches the `.notes/` it replaces, understates it (it is a governed corpus, not notes) |
| `-build` / `-coord` | Precise, less conventional |

**Recommendation: keep `-dev`, and pay for it with one sentence.** The very
first line of `<project>-dev/README.md` must be a definition, not a welcome:

> *"This repository contains no application code. It is the AI-coordination
> corpus for `<project>` — protocol, work packages, prompts, build reports,
> issue records, and design history. It is not a development branch,
> environment, or fork of `<project>`."*

Ambiguity that is resolved in the first sentence of the thing itself is a
non-problem. Ambiguity resolved nowhere is how a 6-week contract drift
happens. See **D-02** if you would rather rename now — it is free today and
expensive at six repos.

## 3. Why two repos, not one or three

**Not one** (the console's current shape): the coordination corpus is
`.gitignore`d, so it is uncommitted, unshareable, and unrecoverable. Measured
in `strategy-lab-console` right now: **194 of 463 `.notes/` files tracked**,
each having needed an explicit `git add -f`. The remaining 269 exist on one
machine's disk. Un-ignoring it inside the product repo is the obvious
alternative, and it is defensible — but it puts thousands of high-churn
documents into the history, diff, and clone weight of a repo whose consumers
want the code. See **D-03**.

**Not three** (splitting design/mockups out from the coordination repo):
design output is consumed by exactly the same sessions that consume prompts
and build reports, and mockup-first is a step *of* the session protocol. A
third repo adds a sync boundary between things that are always read together.
Keep `design/` as a directory inside `<project>-dev/`.

**Two, with a pin.** The consequence of the split is that `<project>` and
`<project>-dev` can drift, and drift between repos is exactly the failure the
console just found the hard way — its mirror of an upstream contract rotted
six weeks across 11 of 18 files, and produced *zero* signal. The template
must therefore ship a **sync record and a one-command check from day one**,
not add one after the first incident. See `03-what-broke-measured.md` §7 and
**D-04**.

## 4. The resulting family, spelled out

```
strategy-lab-suite/                 ← container, no .git, never cloned
├── strategy-lab/                   ← repo   (product)
├── strategy-lab-dev/               ← repo   (coordination)
├── strategy-lab-console/           ← repo
├── strategy-lab-console-dev/       ← repo
├── strategy-lab-charts/            ← repo
└── strategy-lab-charts-dev/        ← repo
```

And the template that generates one pair:

```
generic-project/                    ← becomes <family>-suite/
├── generic/                        ← becomes <project>/
├── generic-dev/                    ← becomes <project>-dev/
└── generic-project-design/         ← deleted at instantiation
```

**One open question this raises:** a family has genuinely shared material —
the session protocol, the file-format rules, the lint script — and today each
console/charts/lab repo carries its own drifting copy. Options are a
`<family>-suite-dev/` shared repo, a git submodule, or accepting per-project
copies. See **D-05**.
