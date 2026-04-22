# Notes: Tool Interfaces and Function Calling

## What to improve

- Add one canonical JSON schema example with validation errors.
- Include a section on idempotency and exactly-once semantics.
- Add fallback policy examples for tool outages.

## Alternative rewrite

A tool definition is a constitution, not a convenience method. Once we specify arguments, side effects, and failure semantics, the agent can reason about action instead of improvising with brittle string tricks.
