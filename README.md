# Structure and Interpretation of Agentic Patterns

This repository is a drafting workspace for a SICP-inspired book on agentic systems, combining rigorous theory with practical engineering patterns.

## Project layout

- `book/` - chapter/topic markdown sources, topic rewrite notes, references, and CSS
- `scripts/` - Python build scripts for website and PDF outputs
- `site/` - generated HTML output for deployment (build artifact)
- `dist/` - generated print artifacts (`book.html`, `book.pdf`)

## Build commands

```bash
uv venv
uv pip install -r requirements.txt
uv run python scripts/build_site.py
uv run python scripts/build_pdf.py
```

The site output is written to `site/` and is compatible with GitHub Pages.
