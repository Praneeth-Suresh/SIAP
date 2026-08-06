# Agent Rules

## Always-On SIAP Defaults

These rules combine Beryl operating discipline with the durable project stance from `AGENT.md`.

1. Read `README.md`, `.beryl/agent/project-brief.md`, and this file before substantial work.
2. Route work through `.beryl/agent/task-routing.md` and load the matching workflow skill before editing.
3. Preserve the SICP-like voice: explanatory, witty, slightly grandiose, mathematically serious.
4. Teach by construction. Prefer interpreter state, transitions, pseudocode, and executable artifacts over slogans.
5. Keep agentic AI framed as orchestration science: goals, environments, beliefs, actions, memory, tools, safety, feedback, and institutions.
6. Preserve citation integrity. Externally sourced claims need clickable numeric citations into `book/references.md`.
7. Do not hand-edit generated `dist/` or `site/` artifacts except by running build scripts.
8. Do not weaken tests or checks to pass implementation.
9. Do not use sub-agents unless the user explicitly asks for sub-agents, parallel agents, reviewer agents, or competing implementations.

## Before Editing

1. Classify the task:
   - manuscript/prose publication work,
   - build/artifact work,
   - Beryl/control-plane work,
   - site/deployment work,
   - explanation/review/debugging.
2. Read the smallest relevant context files:
   - manuscript work: `AGENT.md`, `.beryl/agent/project-brief.md`, `.beryl/agent/design-tree.md`, affected chapter/topic files, `book/references.md` when citations change.
   - build work: `.beryl/agent/architecture.md`, `.beryl/agent/testing-policy.md`, relevant `scripts/` files.
   - Beryl work: `.beryl/agent/README.md`, `.beryl/agent/task-routing.md`, affected `.beryl/agent/` files.
3. Identify generated artifacts that must be rebuilt.
4. State success checks for non-trivial work.

## Manuscript Rules

1. Maintain the four-chapter spine unless deliberately redesigning the book.
2. Keep primary topic files publication-ready; keep scratch/revision alternatives in `*-notes.md`.
3. Avoid visible repetitive scaffolds such as "Three-theory braid", "How to study this formally", and boxed "Translating the Theory..." endings.
   The editor-mandated headings `The Assumption`, `The Violation`, and `When It Fails` are a deliberate exception: use them for major patterns, but make the surrounding prose specific rather than templated.
4. Avoid equation piles. State assumptions, interpretation, failure conditions, and one worked consequence where possible.
5. Continue the running interpreter arc rather than adding disconnected survey material.
6. Preserve the Chapter 4 publication workflow example when changing multi-agent material unless there is a better recurring example.
7. Treat display equations as executable claims: follow every published display formula with a two-step `Try this with numbers` example.
8. Keep Agent-427's chronology consistent with `book/continuity-ledger.md`, which is revision support and must not be published.

## Build Rules

1. `dist/book-latex.pdf` is the publication artifact.
2. Use `python3 scripts/build_latex_pdf.py` for publication PDF rebuilds.
3. Use `uv run python scripts/build_site.py` for web output when dependencies are available.
4. Do not manually patch `dist/book.tex` or `dist/book-latex.md`; fix the source or builder.
5. If a build command requires network or missing dependencies, report that clearly.

## Beryl Rules

1. `.beryl/agent/` is the canonical Beryl context.
2. Generated shims are not source. After changing canonical Beryl rules/templates, run:

   ```bash
   ./.beryl/agent/scripts/sync-agent-env.sh
   ```

3. Run `./.beryl/scripts/check.sh` after edits.
4. Keep `.beryl/agent/session-state.md` temporary and clear it when no longer needed.

## Before Finishing

Final response must include:

- What changed.
- Commit-boundary grouping for changed files.
- Checks run.
- Checks skipped or unavailable.
- Whether generated artifacts changed.
- Whether tests or `tests/.manifest.sha256` changed.
- Which Beryl/workflow skill was used, if applicable.
- Whether temporary session state was cleared or not used.
