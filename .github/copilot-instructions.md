# Copilot Instructions for SIAP

## Build, test, and lint commands

Use `uv` for local Python workflows:

```bash
uv venv
uv pip install -r requirements.txt
```

Build commands:

```bash
uv run python scripts/build_site.py
uv run python scripts/build_pdf.py
uv run python scripts/build_latex_pdf.py
```

System dependencies used by existing scripts:

```bash
# For WeasyPrint PDF path
sudo apt-get install -y libcairo2 libpango-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info

# For LaTeX PDF path
sudo apt-get install -y pandoc tectonic
```

This repository currently has no configured automated test suite or linter commands (`pytest`, `ruff`, `mypy`, etc.), so there is no single-test command available yet.

## High-level architecture

- **Content source of truth is `book/`**:
  - `book/index.md` is the root entry.
  - `book/chapters/*/index.md` defines chapter-level navigation.
  - Topic files (`topic-XX-*.md`) hold primary narrative content.
  - `book/references.md` is the canonical bibliography.
- **`scripts/build_site.py`** renders **every** markdown file under `book/` into `site/` using `templates/page.html`, rewrites `.md` links to `.html`, and writes `.nojekyll`.
- **`scripts/build_pdf.py`** builds print artifacts in `dist/` by concatenating only:
  1. `book/index.md`
  2. chapter `index.md` files
  3. topic files excluding `*-notes.md`
  4. `book/references.md`
  It outputs `dist/book.html`, `dist/book.pdf`, and `dist/book.css`.
- **`scripts/build_latex_pdf.py`** uses the same section selection as `build_pdf.py`, rewrites references links for in-document anchors, then generates `dist/book-latex.md`, `dist/book.tex`, and `dist/book-latex.pdf` via Pandoc + a LaTeX engine (`tectonic` preferred).
- **Deployment** (`.github/workflows/deploy-pages.yml`) builds and publishes only the static `site/` artifact to GitHub Pages on pushes to `main` (or manual dispatch).

## Key repository conventions

- Preserve the project voice in prose changes: explanatory, witty, and slightly grandiose (SICP-inspired).
- Keep the pedagogical throughline centered on interpreters, explicit loop semantics, and theory-to-implementation mapping.
- Every externally sourced claim must use clickable numeric citation syntax: `[[n](...)]`.
- Treat `book/references.md` as the bibliography authority; update it when adding new citations.
- Keep chapter/topic structure consistent:
  - each chapter has an `index.md`;
  - each topic uses `topic-XX-*.md`;
  - each topic should have a companion `topic-XX-*-notes.md` with concrete improvement notes and at least one alternative rewrite.
- Prefer updating markdown sources and regenerating outputs through scripts rather than editing generated artifacts manually.
- Keep `plan.md` updated at meaningful milestones when doing multi-step content work.
