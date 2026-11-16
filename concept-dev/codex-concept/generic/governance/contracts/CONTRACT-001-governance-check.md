---
id: CONTRACT-001
status: accepted
date: 2026-08-20
updated: 2026-08-20
owners: [template]
sync_required: true
---

# CONTRACT-001: Governance Check

Sessions that change scaffold or governance files run `check-governance`
against `generic/` and `generic-dev/` before close-out.

The PowerShell entry point is [../../scripts/check-governance.ps1](../../scripts/check-governance.ps1).
