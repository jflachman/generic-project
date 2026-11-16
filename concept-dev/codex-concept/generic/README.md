# generic

`generic/` is the product repository in this two-repo template. It holds
application code, tests, deployment files, and durable governance a consumer
or maintainer needs.

The sibling coordination repository is [../generic-dev/](../generic-dev/).
Builder workflow, work packages, prompts, reports, issues, design notes, and
session state live there.

## Layout

- [CLAUDE.md](CLAUDE.md): stable product-side constitution and pointers.
- [AGENTS.md](AGENTS.md): pointer for non-Claude agents.
- [STATUS.md](STATUS.md): generated product snapshot.
- [governance/INDEX.md](governance/INDEX.md): generated governance map.
- [scripts/README.md](scripts/README.md): governance checker usage.

Run the checker before closing scaffold or governance work:

```powershell
scripts\check-governance.ps1 --product-root . --dev-root ..\generic-dev
```
