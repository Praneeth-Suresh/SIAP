# ADR 0009: Publication Enrichment Contracts

## Status

Accepted

## Context

The manuscript now requires a sourced opening and closing quotation system,
one original terminal cartoon for every reader-facing section, additional
technical diagrams, and exercise/question treatments that do not masquerade as
ordinary numbered exposition. Copying these elements into 23 Markdown files
would make placement drift across the site, HTML/PDF, and LaTeX builders. Image
generators also produce textured pixels at the canvas edge, so nominal image
dimensions cannot prove that trim and padding are safe.

## Decision

Declare quotations in `book/quotes.toml` and publication visuals in
`book/visuals.toml`. Both registries use stable IDs, manifest-relative source
ownership, explicit placement, and strict coverage. All builders load the same
records through `scripts/publication_enrichment.py`.

Opening epigraphs follow the source H1. Closing epigraphs and terminal cartoons
follow the complete source body; footnote renderers remain responsible for
collecting note definitions. Exercises and reader questions use semantic fenced
divisions and unnumbered headings, adapted to dedicated HTML sections and LaTeX
macros.

Every PNG visual declares its dimensions, measured content bounding box, and
minimum padding. `scripts/audit_visuals.py` compares those declarations with the
actual decoded pixels. Generated cartoons and diagrams pass through
`scripts/normalize_visual_assets.py`, which preserves aspect ratio while adding
a uniform print-safe matte. Publication builders stop when the contract fails.

Terminal cartoons use varied, silent three-to-five-panel mini Sunday pages.
They retain the original Agent-427 cast and tell one section-specific visual
argument through a sparse production setup, a richer imaginative or adversarial
turn, and a deadpan consequence. Panel grids may vary, but reading order,
character identity, print-safe margins, and the absence of borrowed characters
or copied panels are invariant.

## Consequences

- **Benefit:** Site and print surfaces receive identical quote and cartoon
  coverage without duplicating editorial content.
- **Benefit:** A missing section coda, duplicate cartoon, clipped image, or stale
  bounding box becomes a deterministic build failure.
- **Benefit:** Exercises and reader questions remain semantically and visually
  distinct while staying outside the normal heading-number sequence.
- **Tradeoff:** Replacing or regenerating an image requires normalization and a
  refreshed registry bounding box.
- **Tradeoff:** Quote changes require provenance metadata even when the visible
  epigraph is deliberately terse.
- **Follow-up:** Keep representative browser inspection and the LaTeX rebuild in
  the publication gate because pixel contracts cannot judge page composition.
