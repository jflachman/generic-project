---
id: 20260820-populate-the-two-repo-scaffold
prompt: 003-populate-the-two-repo-scaffold
date: 2026-08-20
status: closed
validated:
  - unittest-fixtures-pass
  - check-governance-real-scaffold
  - d-14-decided
  - tracker-closed
---

# Build Report: Populate the Two-Repo Scaffold

## Summary

Prompt `003` replaced the placeholder `generic/` and `generic-dev/` content
with the first real two-repo scaffold. The scaffold contains no
project-specific application code. It does include baseline governance,
coordination records, generated views, issue records, state, archive and agent
memory stubs, and bidirectional agent entry points.

## Decisions Closed

| Decision | Result |
|---|---|
| D-14 | Both repos carry a small `CLAUDE.md` that points at the other, and both repos are mounted as siblings in one parent workspace. No symlink baseline and no ignore rule may exclude the coordination corpus. |

## Files Changed

- `generic/`: product README, `CLAUDE.md`, `AGENTS.md`, generated `STATUS.md`,
  governance records, generated governance indexes and views, and empty
  `src/`, `tests/`, and `deploy/` directories.
- `generic-dev/`: coordination README, `CLAUDE.md`, `PROTOCOL.md`, generated
  `QUEUE.md`, seed work package, build report index, typed issue records,
  design/state indexes, archive manifest, and agent memory stubs.
- `docs/06-open-questions.md`: D-14 decided.
- `prompts/003-populate-the-two-repo-scaffold.md`: marked closed.
- `prompts/004-build-instantiation-tooling.md`: next prompt queued.
- `PROMPT-TRACKER.md`: prompt 003 closed and prompt 004 queued.

## Validation

Ran the prompt `002` precondition:

```powershell
python -m unittest discover -s generic\scripts\tests
```

Result:

```text
Ran 12 tests in 7.579s
OK
```

Ran the checker against the real scaffold:

```powershell
python generic\scripts\check-governance.py --product-root generic --dev-root generic-dev --today 2026-08-20
```

Result: passed with no output.

## Follow-Up

Run prompt `004` next. It should build the instantiation tooling for copying
the template, deleting the design project, renaming the sibling repos, and
replacing placeholder tokens.
