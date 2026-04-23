# Structure and Interpretation of Agentic Patterns

![Build Pipeline](https://img.shields.io/badge/build-uv%20scripts-6f42c1)
![Output](https://img.shields.io/badge/output-HTML%20%2B%20PDF-0a7f2e)
![Deploy](https://img.shields.io/badge/deploy-GitHub%20Pages-24292f?logo=github)
![Citations](https://img.shields.io/badge/citations-clickable%20%5Bn%5D-c97a00)

This repository is a workshop for a somewhat audacious goal: to do for agentic systems what classic CS texts did for programming itself. We are not collecting clever prompts; we are constructing a theory-backed craft of orchestration.

## Project goals

1. Build a pedagogical path for agentic AI using **Python and modern agent/tooling frameworks** as today’s teaching language.
2. Walk readers through constructing **interpreters for reasoning loops, planners, and tool-using agents**, so architecture is learned by building.
3. Present a unifying conceptual frame for **autonomy, memory, and collaboration** rather than treating them as unrelated hacks.
4. Balance formal foundations (decision theory, reinforcement learning, symbolic methods, game theory) with practical systems work (LLM APIs, retrieval, orchestration runtimes).
5. Maintain a voice that is explanatory, witty, and slightly grandiose—because big ideas deserve a bit of theatrical lighting.

## Project layout

| Path | Purpose |
|---|---|
| `book/` | Chapter and topic markdown sources, rewrite-notes companions, references, and stylesheet |
| `scripts/` | Python build scripts for website, HTML/CSS PDF, and LaTeX PDF generation |
| `templates/` | HTML page template used by the site builder |
| `site/` | Generated static website (deployment artifact) |
| `dist/` | Generated print artifacts (`book.html`, `book.pdf`) |

## Build and publish

```bash
uv venv
uv pip install -r requirements.txt
uv run python scripts/build_site.py
uv run python scripts/build_pdf.py
uv run python scripts/build_latex_pdf.py
```

The site output in `site/` is GitHub Pages-compatible. Print outputs are emitted to `dist/`:
- `book.pdf` (WeasyPrint from HTML/CSS)
- `book-latex.pdf` and `book.tex` (Pandoc + LaTeX engine for cleaner math)

For the LaTeX build, install system binaries:

```bash
sudo apt-get install pandoc tectonic
```

## Writing conventions

- Every externally sourced idea must have a clickable numeric citation: `[[n](...)]`.
- `book/references.md` is the canonical bibliography index.
- Every topic file has a companion `*-notes.md` file with revision notes and at least one alternate rewrite.
