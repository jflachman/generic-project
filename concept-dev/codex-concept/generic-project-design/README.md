<!--
  generic-project-design | README.md
-->

# generic-project-design

The working area for designing `generic/` and `generic-dev/`. **This folder is
deleted when the template is instantiated** — nothing here ships.

Everything discussed here is fair game to change: governance structure, how
files are kept from growing without bound, how information is archived so it
is retained without cluttering `CLAUDE.md` / `AGENTS.md`, and which files
should be Markdown vs YAML vs JSON given that the primary reader is an AI.

```
design/
└── initial-concept/          ← current and only design round
    ├── README.md             ← the concept + reading order   ← START HERE
    ├── PROMPT-TRACKER.md     ← what to run next
    ├── docs/                 ← concept documents 01–07
    ├── prompts/              ← session briefs
    └── build-reports/        ← one per session, without exception
```

Later design rounds become sibling directories under `design/`
(`design/<round-name>/`), each with the same three subfolders. The initial
round is not rewritten when a later one supersedes it — it is marked
superseded and left as history.

This project runs on the protocol it is designing, deliberately: prompts are
files, every session writes a build report, and there is exactly one ordered
queue. If the mechanism is annoying at this scale, that is data.
