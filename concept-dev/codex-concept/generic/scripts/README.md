# Governance Check Suite

`check-governance` validates the governance corpus for the two-repo template.
Run it locally before closing a session:

```powershell
generic\scripts\check-governance.ps1 --product-root generic --dev-root generic-dev
```

Exit contract:

- `0`: all selected checks passed.
- `1`: one or more governance invariants failed.
- `2`: command-line usage error from `argparse`.

Each check is independently runnable with `--check <name>`. Use
`--list-checks` to list names.

| Check | Prevents |
|---|---|
| `line-byte-budgets` | 147 KB "lightweight" contracts and 339 KB always-read state files. |
| `relative-links` | Constitutions pointing to files that do not exist. |
| `section-length` | Multi-thousand-line `##` sections with no internal structure. |
| `schemas` | Records drifting back into prose that cannot be queried or generated from. |
| `generated-files` | Hand-edited queues, stale indexes, and disagreeing generated views. |
| `sync-pins` | Six-week silent rot in mirrored contracts. |
| `dev-not-ignored` | Coordination files disappearing because the dev corpus is ignored. |
| `closed-prompts-have-reports` | Prompt sessions closing without durable evidence. |
| `mutable-state-in-constitution` | Constitutions becoming stale status files. |
| `no-amendment-drift` | Amendment-only updates that leave contradictory active meanings. |
| `issue-type-prefix-folder` | Gaps, bugs, deferred work, and upstream requests collapsing into one vague log. |

Budgets live in `governance-budgets.json` so changing D-07 values is a data
change, not a code edit.
