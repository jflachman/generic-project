# Product Constitution

This is the product-side entry point for AI agents working on `generic/`.

Read [STATUS.md](STATUS.md) for the generated product snapshot and
[governance/INDEX.md](governance/INDEX.md) for governed records. Builder
workflow lives in [../generic-dev/PROTOCOL.md](../generic-dev/PROTOCOL.md),
and the generated run queue lives in [../generic-dev/QUEUE.md](../generic-dev/QUEUE.md).

Rules:

- Keep consumer-facing truth in this repository.
- Keep builder coordination in [../generic-dev/](../generic-dev/).
- Do not add mutable session history to this file.
- Run [scripts/check-governance.ps1](scripts/check-governance.ps1) before
  closing governance or scaffold work.
