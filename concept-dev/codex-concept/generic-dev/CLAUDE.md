# Coordination Constitution

This is the coordination-side entry point for AI agents working on
`generic-dev/`.

Read [../generic/CLAUDE.md](../generic/CLAUDE.md) for the product-side
constitution, then use [PROTOCOL.md](PROTOCOL.md) for session workflow and
[QUEUE.md](QUEUE.md) for ordered work.

Rules:

- Keep builder coordination in this repository.
- Keep product code and durable consumer-facing governance in
  [../generic/](../generic/).
- Do not exclude this repository from agent reads.
