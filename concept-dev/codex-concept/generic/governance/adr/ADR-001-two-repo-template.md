---
id: ADR-001
status: accepted
date: 2026-08-20
updated: 2026-08-20
supersedes: []
---

# ADR-001: Two-Repo Template

The template separates consumer-facing product truth from builder
coordination.

`generic/` holds code, tests, deployment material, ADRs, specs, contracts,
unit governance, generated status, and the checker. `generic-dev/` holds the
protocol, work packages, prompts, build reports, typed issues, design
artifacts, state, archives, and agent operational memory.
