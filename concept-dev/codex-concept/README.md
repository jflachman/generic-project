<!--
  generic-project | README.md
-->

# generic-project — a two-repo project template for AI-led development

**This folder is a container, not a repository.** It has no `.git` of its own
and is never cloned. It exists so a project and its AI-coordination sibling
sit together on disk.

## The three folders

| Folder | Role | Published? |
|---|---|---|
| `generic/` | **Product repo.** Code, plus the durable governance a *consumer* needs — ADRs, contracts, unit specs. | Yes → GitHub |
| `generic-dev/` | **Coordination repo.** Everything a *builder* needs — session protocol, work packages, prompts, build reports, gap logs, design, state. No application code. | Yes → GitHub |
| `generic-project-design/` | **The design conversation** that produces the other two. **Deleted at instantiation.** | No |

`generic/` and `generic-dev/` are intentionally empty pending the decisions in
`generic-project-design/design/initial-concept/docs/06-open-questions.md`.

## Why two repos

The coordination corpus is the thing an AI agent depends on most and the thing
most likely to be `.gitignore`d out of existence. Measured in the source
project this template is derived from: **269 of 463 coordination files were
untracked**, and the directory was excluded from the agent's own default reads.
Giving it its own repo makes that failure impossible rather than discouraged.

## Instantiating

```
cp -r generic-project ../<family>-suite
rm -rf ../<family>-suite/generic-project-design
# rename, substitute tokens, git init each child, push both
```

Full sequence, the placeholder-token contract, and the ordering that matters:
`generic-project-design/design/initial-concept/docs/07-instantiation-checklist.md`.

**Naming note:** the recommended parent name is `<family>-suite/` — not
`<family>/`, which collides with the flagship child repo of the same name.
Reasoning in `docs/01-naming-and-repo-topology.md`.

## Start here

`generic-project-design/design/initial-concept/README.md`
