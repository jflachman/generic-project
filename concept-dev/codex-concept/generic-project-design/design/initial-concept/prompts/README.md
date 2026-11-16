<!--
  generic-project-design | design/initial-concept/prompts/README.md
-->

# Prompts — design sessions for the template

Each file is a durable session brief, not a chat message. Convention carried
from `strategy-lab-console` ([`../docs/02-console-approaches-inventory.md`](../docs/02-console-approaches-inventory.md)
§C2), with one addition: **YAML front matter**, because the tracker in
[`../PROMPT-TRACKER.md`](../PROMPT-TRACKER.md) should eventually be generated
from it rather than hand-maintained (D-10).

## Shape

```markdown
---
id: 001
title: <short title>
status: queued          # queued | in progress | closed
depends_on: []          # prompt ids
decides: [D-01, D-02]   # open questions this session should answer
touches: []             # paths, for collision detection
---

# NNN — <title>

## Goal
## What this session is NOT
## Mandatory reading
## Preconditions
## Deliverables
## Close-out
```

The **"What this session is NOT"** section is not optional. In the console
corpus it is the section that most reliably prevented scope creep.

## Status protocol

Mark `in progress` in the front matter **and** in the tracker at session
start; mark `closed` and remove from the tracker's ordered queue at session
end, with a link to the build report. Both ends — a tracker updated only at
close is wrong for the entire session.
