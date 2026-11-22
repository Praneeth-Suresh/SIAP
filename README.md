# Structure and Interpretation of Agentic Patterns

![Build Pipeline](https://img.shields.io/badge/build-uv%20scripts-6f42c1)
![Output](https://img.shields.io/badge/output-HTML%20%2B%20PDF-0a7f2e)
![Deploy](https://img.shields.io/badge/deploy-GitHub%20Pages-24292f?logo=github)
![Citations](https://img.shields.io/badge/citations-clickable%20%5Bn%5D-c97a00)

A work-in-progress book about building agentic systems. It teaches the ideas by constructing interpreters for reasoning, planning, and tool use in Python.

**[Read online](https://praneeth-suresh.github.io/SIAP/)** (start with *Part 0: The System in Action*) · **[Open the PDF](dist/book-latex.pdf)** · **[Build locally](#build-and-publish)**

The online reader is a published snapshot; it may lag the manuscript in this repository. If you spot a confusing example or a gap, [open an issue](https://github.com/Praneeth-Suresh/SIAP/issues).

## Project goals

1. Build a pedagogical path for agentic AI using **Python and modern agent/tooling frameworks** as today’s teaching language.
2. Walk readers through constructing **interpreters for reasoning loops, planners, and tool-using agents**, so architecture is learned by building.
3. Present a unifying conceptual frame for **autonomy, memory, and collaboration** rather than treating them as unrelated hacks.
4. Balance formal foundations (decision theory, reinforcement learning, symbolic methods, game theory) with practical systems work (LLM APIs, retrieval, orchestration runtimes).
5. Maintain a voice that is explanatory, witty, and slightly grandiose because big ideas deserve theatrical lighting.

## Why this manuscript matters

Agent builders already have models, frameworks, traces, and a great deal of nerve. What they often lack is a shared account of the machine they are building. SIAP makes the control structure visible enough to inspect, test, and improve.

![Agent-427 and Mira turn a collapsing pile of agent gadgets into a small, visible interpreter machine.](assets/readme/why-this-manuscript-matters.png)

- **Control becomes inspectable.** Objectives, state, actions, constraints, and stopping rules leave prompt folklore and enter the design.
- **Reasoning becomes debuggable.** Treating an agent loop as an interpreter gives failures a location: state, transition, guard, budget, or halt condition.
- **Memory becomes a policy.** Retrieval, compression, and forgetting must earn their cost by improving the next action.
- **Action becomes consequential.** Tools have contracts, side effects, risks, and recovery paths; safety is therefore architecture, not an apology afterward.
- **Collaboration becomes institutional.** More agents help only when protocols, incentives, and evaluation make the collective sturdier than a roomful of confident voices.

SIAP's wager is modest but consequential: stronger models matter, and clearer systems make their strength usable.

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

To preview the generated reader, run `python3 -m http.server 8000 --bind 127.0.0.1 --directory site` and open `http://127.0.0.1:8000/`. The **Deploy Book Site** workflow is manually dispatched; merging a README change does not update the live reader.

The site output in `site/` is GitHub Pages-compatible. It publishes the complete reader-facing book with hierarchical chapter/topic navigation and MathJax-rendered equations; companion `*-notes.md` files stay out of the public site. Print outputs are emitted to `dist/`:
- `book.pdf` (WeasyPrint from HTML/CSS)
- `book-latex.pdf` and `book.tex` (Pandoc + LaTeX engine for cleaner math)

For the LaTeX build, install system binaries:

```bash
sudo apt-get install pandoc tectonic
```

## Contributing

Contributions to the manuscript, visual system, and publication pipeline are welcome. Start with [CONTRIBUTING.md](CONTRIBUTING.md), then read the [Code of Conduct](CODE_OF_CONDUCT.md), [Security Policy](SECURITY.md), [Support Guide](SUPPORT.md), and [license guide](LICENSES.md). GitHub issue and pull-request templates provide the shortest path from good intention to a reviewable change.

## Writing conventions

- Every externally sourced idea must have a clickable numeric citation: `[[n](...)]`.
- `book/references.md` is the canonical bibliography index.
- Every topic file has a companion `*-notes.md` file with revision notes and at least one alternate rewrite.
