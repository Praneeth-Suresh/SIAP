# Architecture

## Bounded Contexts

| Context | Owns | Does Not Own | Public Entry Point |
| --- | --- | --- | --- |
| Manuscript Sources | Chapter/topic Markdown, notes companions, references, citation anchors, SICP-like prose | Generated PDF/site artifacts | `book/index.md`, `book/chapters/*`, `book/references.md` |
| LaTeX Publication Build | Markdown merge, print-specific heading adjustment, internal reference rewriting, Pandoc/LaTeX invocation | Manuscript argument quality | `scripts/build_latex_pdf.py` |
| HTML/Site Build | Static website rendering, templates, CSS, GitHub Pages output | LaTeX/PDF typography | `scripts/build_site.py`, `scripts/build_pdf.py`, `templates/page.html`, `book/assets/style.css` |
| Beryl Control Plane | Agent rules, project context, routing, checks, generated tool shims | Book prose except when documenting durable workflow rules | `.beryl/agent/`, `.beryl/scripts/check.sh` |
| Generated Artifacts | Built files consumed by readers or deployment | Source-of-truth edits | `dist/`, `site/` |

## Boundary Rules

1. Edit manuscript source in `book/`; rebuild `dist/` and/or `site/` through scripts.
2. Do not hand-edit `dist/book-latex.md`, `dist/book.tex`, or `dist/book-latex.pdf` as source.
3. Print-specific transformations belong in `scripts/build_latex_pdf.py`, not in topic files unless the source itself is wrong.
4. Beryl canonical behavior lives in `.beryl/agent/`; generated shims are synchronized from Beryl templates.
5. Keep `AGENT.md` and `.beryl/agent/` semantically aligned while Beryl is adopted.
6. Treat `book/references.md` as the canonical bibliography and anchor target.

## Publication Build Architecture

The LaTeX build gathers:

1. `book/index.md` as an unnumbered preface.
2. Each chapter `index.md` as a numbered chapter.
3. Each topic file as a numbered section under its chapter.
4. `book/references.md` as an unnumbered references chapter.

The builder rewrites relative `references.md#ref-n` links into in-document anchors, rewrites local Markdown cross-links into section anchors, removes web-only chapter navigation lists from print output, and writes:

- `dist/book-latex.md`
- `dist/book.tex`
- `dist/book-latex.pdf`

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
- There is no conventional unit-test suite yet; Beryl project checks should report that project-specific tests are unavailable until configured.
