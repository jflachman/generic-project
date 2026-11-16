---
id: 20260820-build-the-check-suite
prompt: 002-build-the-check-suite
date: 2026-08-20
status: closed
validated:
  - unittest-fixtures-pass
  - decisions-written
  - tracker-closed
---

# Build Report: Build the Check Suite

## Summary

Prompt `002` built the first executable governance checker before the real
scaffold exists. The checker lives under `generic/scripts/`, reads tier and
rotation numbers from data, exposes independently runnable checks, and is
proved against a compact product/dev fixture pair.

## Decisions Closed

| Decision | Result |
|---|---|
| D-06 | Constitutions contain zero mutable state; only stable rules and pointers are allowed. |
| D-07 | Hot files: 200 lines / 20,000 bytes. Warm files: 500 lines / 80,000 bytes. `##` sections: 150 lines without `###`. Sync age: 45 days. |
| D-08 | State rotates by quarter, issues by status, and other files by checker-triggered size/structure failure; archived moves append to `archive/MANIFEST.yml`. |
| D-12 | The baseline suite covers every invariant in `05` §5, runs locally at session close, and can be wired into CI once the scaffold exists. |
| D-13 | `QUEUE.md` is exactly one generated queue from prompt front matter. |

## Files Changed

- `generic/scripts/check-governance.py`: executable governance checker.
- `generic/scripts/check-governance.ps1`: Windows wrapper.
- `generic/scripts/governance-budgets.json`: D-07 and sync-age numbers as data.
- `generic/scripts/README.md`: check catalog, scars, and exit-code contract.
- `generic/scripts/tests/`: valid fixture and failure tests for each baseline check.
- `docs/06-open-questions.md`: D-06, D-07, D-08, D-12, and D-13 decided.
- `prompts/002-build-the-check-suite.md`: marked closed.
- `prompts/003-populate-the-two-repo-scaffold.md`: next prompt added.
- `PROMPT-TRACKER.md`: prompt 002 closed and prompt 003 queued.

## Validation

Ran:

```powershell
python -m unittest discover -s generic\scripts\tests
```

Result:

```text
Ran 12 tests in 6.726s
OK
```

The tests include required failure coverage for amendment-only governance drift
and for issue records whose `type`, id prefix, and folder disagree.

## Follow-Up

Run prompt `003` next. It should populate `generic/` and `generic-dev/`,
generate the baseline views, close or defer D-14, and run `check-governance`
against the real scaffold rather than the fixture pair.
