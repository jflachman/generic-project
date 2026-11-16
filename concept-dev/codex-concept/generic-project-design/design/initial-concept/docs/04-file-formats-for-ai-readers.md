<!--
  generic-project-design | design/initial-concept/docs/04-file-formats-for-ai-readers.md
-->

# 04 — Markdown, YAML, JSON, XML: which, where, and why

You asked where files should be XML/YAML/JSON "because the primary user is
AI." This is the recommendation, plus the reasoning to argue with.

## 1. Start by rejecting the premise

"The reader is an AI, therefore use a machine format" does not follow.
Modern models read markdown natively and *reason better* over prose than over
deeply nested data — the rationale in an ADR is the highest-value content in
a governance corpus and does not survive being schematised. Converting the
console's ADRs to YAML would lose the thing that makes them useful.

The axis that actually matters is not the reader. It is **what the file is
for**:

> **Prose explains. Data enumerates.**
> Format by which of those a file is doing — and notice when one file is
> doing both, because that is where the console's three largest files went
> wrong.

`console-gaps.md` is 181 KB because ~200 *records* (id, status, severity,
links) were stored as free prose. It cannot be filtered, counted, or sorted
without an LLM reading all 2,935 lines. That is not a markdown problem; it is
a records-as-prose problem.

## 2. Token cost, measured

Same three gap records, four encodings:

| Format | Bytes | vs YAML |
|---|---|---|
| Markdown table | 688 | **90%** |
| YAML | 765 | 100% |
| JSON | 938 | 123% |
| XML | 1,077 | **141%** |

Markdown tables win on raw size for homogeneous rows — keys are stated once
instead of per record — but they are brittle: no nesting, no multi-line
values, no comments, and a ragged row is silently valid. JSON pays ~23% over
YAML in punctuation. **XML pays ~41% and buys nothing here.**

The correct reading of this table is *not* "always use markdown tables." It
is: **the format differences are small enough (10–40%) that they should never
drive the decision.** Structure and enforceability should. A 181 KB file
saved as XML instead of YAML is still a 181 KB file you have to load.

## 3. The recommendation, by file role

| Role | Format | Why |
|---|---|---|
| Constitution (`CLAUDE.md`, `AGENTS.md`) | **Markdown** | Read in full, every session, by a model. Prose is the point |
| Session protocol | **Markdown** | Procedure with rationale |
| ADRs, design docs, contracts | **Markdown**, YAML front matter for `id`/`status`/`date`/`supersedes` | The body is argument; only the metadata is queryable |
| Build reports | **Markdown**, YAML front matter | Same. Front matter makes 66 reports indexable without reading them |
| Prompts | **Markdown** + YAML front matter (`id`, `package`, `status`, `depends_on`, `touches`) | The front matter is what generates the tracker — see §5 |
| **Issue logs** | **YAML** (one record per entry) + generated markdown index | Gaps, deferred items, bugs, and upstream requests are records |
| **Prompt tracker / run queue** | **Generated** from prompt front matter | Never hand-maintained; see §5 |
| Unit/screen inventory + status | **Generated** from per-unit front matter | Same argument |
| Routing table (`ai-reference/`) | **YAML** source, generated markdown view | It is a lookup table with one purpose: exact-match retrieval |
| Agent-operational memory (`anatomy`, `buglog`, do-not-repeat) | **JSON or YAML** | Written and read by tooling far more than by a human. OpenWolf already does this |
| Machine-generated catalogs, indexes, lockfiles, lint output | **JSON** | Emitted and consumed by scripts; nobody hand-edits them |
| Anything | **XML** | ✗ Never as a file format. See §4 |

**One-line rule for the constitution:**

> *If a session ever needs to ask "how many are `open`?", "which are blocked
> on X?", or "what is next?" — it is data. Store it as YAML records and
> generate the human view. Everything else is markdown.*

## 4. Where XML does belong

XML earns its 41% overhead in exactly one place, and it is not on disk:
**as delimiters inside a prompt.** Anthropic's own guidance is that Claude
attends reliably to `<instructions>`, `<context>`, `<example>` tags in a
prompt, because the tags disambiguate where a block starts and ends in a flat
token stream.

So: use XML-style tags to *frame regions inside a document that is fed to a
model* — a prompt template's sections, a long quoted artifact embedded in a
brief. Do not use `.xml` as a storage format for governance records. The
distinction is between **markup for attention** and **serialization for
storage**.

## 5. The pattern that fixes the console's three biggest files

**Front matter for facts, prose for reasons, generated views for queries.**

```markdown
---
id: BUG-CONSOLE-049
type: bug
status: planned
severity: high
found_in: 20260815-primitives-dataset-picker.md
planned_in: package003/prompts/003-tier1-small-fixes-batch.md
---

# Path 1 / Path 2 workspace mismatch is invisible

**Why deferred:** ...
**What it would take:** ...
```

This is not a novel idea — it is exactly what your own agent-memory
directory already does (`name`/`description`/`metadata.type` front matter,
one fact per file, a generated `MEMORY.md` index). It works there. It is the
same shape the corpus needs at project scale.

What it gives you:

- **One record per file** — files stop growing without bound; the *directory*
  grows instead, which is free.
- **Cold by default** — a session loads the index (small, generated) and only
  the two or three entries it needs.
- **Queryable without an LLM** — `grep`, `yq`, or a 20-line script answers
  "what is open and high severity" for zero tokens.
- **The derived view is generated, never authored** — which structurally
  prevents `03-what-broke-measured.md` §5's three-competing-queues failure.
  You cannot have two disagreeing queues if the queue is a build artifact.

The cost is real and should be stated: more files, a generator to maintain,
and a rule that generated files are never hand-edited (worth a header banner
and a CI check). See **D-09**, **D-10**, **D-11**.

## 6. What stays plain markdown, deliberately

Do not schematise: ADR bodies, design narratives, mockup workflow narratives,
the "why deferred" and "what it would take" prose in a gap, build-report
findings, prompt instructions. These are the parts a future session actually
needs to *think* with, and every one of them was written because a table
could not carry it.

The failure mode to avoid is over-correcting — a corpus of pure YAML is
queryable and says nothing about why anything is true.
