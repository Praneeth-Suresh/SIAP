# Architecture

## Bounded Contexts

| Context | Owns | Does Not Own | Public Entry Point |
| --- | --- | --- | --- |
| Manuscript Sources | Ordered publication manifest, part/chapter/topic Markdown, continuity and notes companions, references, citation anchors, SICP-like prose | Generated PDF/site artifacts | `book/publication.toml`, `book/index.md`, `book/parts/*`, `book/chapters/*`, `book/references.md` |
| Publication Enrichment | Sourced epigraph registry, visual placement registry, semantic reader blocks, strict coverage and pixel-geometry contracts | Core manuscript argument or generated output | `book/quotes.toml`, `book/visuals.toml`, `scripts/publication_enrichment.py`, `scripts/audit_visuals.py` |
| LaTeX Publication Build | Markdown merge, print-specific heading adjustment, internal reference rewriting, Pandoc/LaTeX invocation | Manuscript argument quality | `scripts/build_latex_pdf.py` |
| HTML/Site Build | Reader-facing manuscript manifest, static rendering, templates, CSS, MathJax configuration, GitHub Pages output | LaTeX/PDF typography and revision companions | `scripts/build_site.py`, `scripts/build_pdf.py`, `templates/page.html`, `book/assets/style.css` |
| Beryl Control Plane | Agent rules, project context, routing, checks, generated tool shims | Book prose except when documenting durable workflow rules | `.beryl/agent/`, `.beryl/scripts/check.sh` |
| Generated Artifacts | Built files consumed by readers or deployment | Source-of-truth edits | `dist/`, `site/` |

## Boundary Rules

1. Edit manuscript source in `book/`; rebuild `dist/` and/or `site/` through scripts.
2. Do not hand-edit `dist/book-latex.md`, `dist/book.tex`, or `dist/book-latex.pdf` as source.
3. Print-specific transformations belong in `scripts/build_latex_pdf.py`, not in topic files unless the source itself is wrong.
4. Beryl canonical behavior lives in `.beryl/agent/`; generated shims are synchronized from Beryl templates.
5. Keep `AGENT.md` and `.beryl/agent/` semantically aligned while Beryl is adopted.
6. Treat `book/references.md` as the canonical bibliography and anchor target.
7. The website publishes the preface, Part 0, chapter indexes, primary topic files, and references in reading order; `*-notes.md` files remain manuscript-workflow support and are never deployed.
8. `book/publication.toml` is the sole source of reader-facing order and section kind. Builders and manuscript audits load it through `scripts/publication_manifest.py`; they do not infer publication order from directory globs.
9. `book/continuity-ledger.md` is unpublished revision support for Agent-427's chronology.
10. Quotes and terminal cartoons are declared once in strict registries and injected by every builder; do not duplicate them in individual Markdown sources.
11. Exercises and reader questions use semantic fenced divisions. Their headings remain unnumbered in print and visually distinct on the site.
12. Every registered PNG must match its declared dimensions, measured content bounding box, and minimum safe padding before publication builds continue.

## Publication Build Architecture

The publication manifest orders:

1. `book/index.md` as an unnumbered preface.
2. `book/parts/00-system-in-action.md` as the unnumbered opening movement.
3. Each chapter `index.md` as a numbered chapter, followed by its topics.
4. `book/references.md` as an unnumbered references chapter.

The builder rewrites relative `references.md#ref-n` links into in-document anchors, rewrites local Markdown cross-links into section anchors, removes web-only chapter navigation lists from print output, and writes:

- `dist/book-latex.md`
- `dist/book.tex`
- `dist/book-latex.pdf`

Before format-specific rendering, every builder loads `book/quotes.toml` and
`book/visuals.toml`. Opening epigraphs follow the source H1; closing epigraphs
and terminal cartoons follow the complete section body. The visual audit checks
the actual PNG pixels rather than trusting declared metadata. Diagram rendering
and image generation feed `scripts/normalize_visual_assets.py`, which adds an
aspect-preserving print-safe matte before geometry is registered.

## Public Interface Rule

The public build commands are:

```bash
python3 scripts/build_latex_pdf.py
uv run python scripts/build_site.py
uv run python scripts/build_pdf.py
./.beryl/scripts/check.sh
```

Use the LaTeX build command for any publication-impacting change. Use the site build command for web-output changes.

## Generated Shims

Beryl installed these tool shims:

- `AGENTS.md`
- `CLAUDE.md`
- `.cursor/rules/agent-rules.md`
- `.github/copilot-instructions.md`
- `.codex/AGENTS.md`

Do not edit those manually. Edit `.beryl/agent/tool-instruction-template.md` or `.beryl/agent/agent-rules.md`, then run:

```bash
./.beryl/agent/scripts/sync-agent-env.sh
```

## Known Constraints

- The LaTeX build may require network access the first time Tectonic fetches its standard bundle.
- `scripts/build_pdf.py` requires Python package dependencies such as `markdown` and WeasyPrint.
- The site builder has focused standard-library regression tests; publication layout remains verified by explicit build and browser checks.
- Tectonic may warn about temporary absolute media paths created by Pandoc; the repository-relative paths remain preserved in `dist/book.tex`.
