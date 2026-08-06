# ADR 0008: Publication Spine and Recursive Arc

## Status

Accepted

## Context

SIAP's builders inferred reader-facing order independently from directory names. The editor-directed rewrite adds an unnumbered Part 0 before theory while preserving four stable numbered chapters, public routes, and generated artifacts. A hidden ordering convention would let the PDF, site, and editorial audit disagree.

## Decision

Declare every reader-facing Markdown source and its semantic kind in `book/publication.toml`. Load that manifest through `scripts/publication_manifest.py` in the LaTeX, HTML/PDF, site, and manuscript-audit paths.

The narrative map is:

- Part 0: `book/parts/00-system-in-action.md`, the publication institution before individual theory.
- Part 1: Chapter 1, the single agent and the approximation gap.
- Part 2: Chapters 2 and 3, reasoning, memory, tools, and embodied foundations.
- Part 3: Chapter 4, the agent society and its governance.

Existing chapter directories, topic ownership, chapter numbers, and public routes remain stable. `book/continuity-ledger.md` is explicitly excluded from the manifest.

## Consequences

- **Benefit:** Every publication surface and deterministic audit sees one explicit order.
- **Benefit:** Part 0 becomes a real source unit without masquerading as Chapter 0 or renumbering the book.
- **Benefit:** Notes and continuity material cannot leak into publication through recursive globbing.
- **Tradeoff:** Adding or moving reader-facing material now requires a manifest edit.
- **Follow-up:** Protect manifest order, kinds, existence, and exclusion rules with focused tests.
