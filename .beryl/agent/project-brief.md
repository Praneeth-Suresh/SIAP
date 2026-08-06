# Project Brief

## Product Goal

Build **Structure and Interpretation of Agentic Patterns (SIAP)** into a publishable, theory-backed book about agentic AI systems. The book should read as an academic and philosophical homage to SICP: ideas are taught by construction, formalized with mathematics, and grounded in concrete agent interpreter patterns.

## Primary Readers

1. **Agent builders** who need a principled way to design reasoning loops, memory, tools, safety filters, and multi-agent protocols.
2. **Entry-level undergraduate readers** encountering agent design, decision theory, control, planning, game theory, and retrieval for the first time; the book must define unfamiliar terms, connect symbols to practical examples, and preserve rigor without assuming graduate background.
3. **Researchers and advanced students** who want decision theory, control, planning, game theory, and retrieval connected to practical LLM orchestration.
4. **Future coding agents working in this repository** who need stable project context, build commands, and publication criteria.

## Publication Criteria

1. The manuscript must be an interesting collection of topics, well explained in expository prose and backed by rigorous theory.
2. The style must match the academic, philosophical, integrative spirit of SICP: computer science with mathematical aesthetics.
3. The writing must flow naturally from idea to idea. Avoid repetitive visible templates such as "Three-theory braid", "How to study this formally", or boxed "Translating the Theory..." endings.
4. `dist/book-latex.pdf` is the publication artifact. It must build cleanly enough for release, with correct chapter/topic hierarchy, references, math, and code layout.
5. Accessibility edits must be additive in spirit: preserve all existing concepts, equations, citations, and formal claims while adding first-use definitions, symbol guides, tiny worked examples, assumptions, and practical engineering consequences.
6. The book's coherence should be organized around four research questions, introduced naturally rather than mechanically: how agentic patterns are represented structurally; how they affect success, partial progress, token use, latency, and tool-call efficiency; how combined patterns interact; and which task characteristics predict when a pattern helps.

## Primary Workflows

1. **Publication editing**: revise Markdown sources in `book/` while preserving citation integrity, chapter flow, and the SICP-like voice.
2. **Book artifact generation**: run `python3 scripts/build_latex_pdf.py` to produce `dist/book-latex.md`, `dist/book.tex`, and `dist/book-latex.pdf`.
3. **Website generation**: run `uv run python scripts/build_site.py` for the static site when web output changes.
4. **Beryl verification**: run `./.beryl/scripts/check.sh` after edits and report any unavailable project-specific checks honestly.

## Current Publication State

The August 6, 2026 complete rewrite introduced the institution before the individual: a new Part 0 shows
a publication society succeeding and then colluding, Chapter 1 asks how Agent-427 survives it, Chapters
2--3 expose the machinery, and Chapter 4 returns to governance. A canonical publication manifest now
drives every builder. The manuscript pairs each display formula with arithmetic, each primary pattern
with its assumption and violation, and each topic with a code-required exercise. Ten reproducible diagrams,
adversarial failure interludes, skeptical-engineer exchanges, The Verdict evaluation frame, and a
deterministic editorial audit make those promises testable.

The July 19, 2026 publication pass completed a critic/worker loop:

- A gpt-5.6 critic reviewed the manuscript against the publication criteria.
- gpt-5.5 workers revised Chapters 1 through 4 in bounded write scopes.
- A second gpt-5.6 critic identified remaining formal and layout blockers.
- A final structural pass deepened Chapter 4 around many interpreters sharing an environment.
- A final gpt-5.6 publication gate returned: **PASS. No material publication blockers remain. Further critique would be repetitive.**

Key outcomes from that pass:

- The book now follows a running interpreter arc: goals/actions, belief, state abstraction, control, reasoning semantics, planning, memory, evaluation, tools, embodiment, safety, and multi-agent institutions.
- Repetitive template headings were removed from the publication manuscript.
- Formal corrections were made for idempotent effects, MPC control sequences, causal replay assumptions, lag-aware state augmentation, no-regret equilibrium distinctions, and dominant-strategy truthfulness.
- `scripts/build_latex_pdf.py` now builds a real LaTeX `book` document with front matter, author metadata, unnumbered preface/references, chapter/topic hierarchy, internal reference links, and no decorative source separators.

## Beginner-Accessibility Pass

A later pass rewrote all twenty-one published sections for entry-level readers, per publication criterion 5.
Each section was drafted by two competing writer agents and selected by a judge agent, then audited by
independent reviewer agents. Durable rules that came out of it:

- Preserve first-heading lines byte-identically; the LaTeX build resolves cross-file links through them.
- Preserve the preface headings `## Chapter map`, `## How to read this book`, and `## Throughline`, and the
  `## Topics` heading in chapter index files, because the build matches them by exact text.
- Chapter and topic headings use Title Case; the preface keeps sentence case.
- Cross-references are written by name, as `Topic N (Exact Title)` within a chapter and
  `Chapter M, Topic N (Exact Title)` across chapters, never as "above" or "below".
- Symbols reused with a new meaning (for example \(R\), \(\gamma\), \(\sigma\)) must say so where reused.
- Do not reintroduce uniform scaffolding phrasing across files.
- Content preservation is checked against the pre-rewrite baseline: citation multisets, display-math
  counts, code fences, table rows, title lines, and word counts.

## Non-Goals

- Do not turn SIAP into a generic AI survey.
- Do not add topics that break the four-chapter spine unless the chapter map is deliberately redesigned.
- Do not hand-edit generated `dist/` files except through build scripts.
- Do not weaken citation density or remove mathematical rigor for style alone.
- Do not replace human review; Beryl makes review easier, not unnecessary.

## External Systems

| System | Why it exists | Interface owner | Failure fallback |
| --- | --- | --- | --- |
| Pandoc | Converts merged Markdown to LaTeX and PDF inputs | `scripts/build_latex_pdf.py` | Report missing binary and keep source edits verifiable |
| Tectonic/LaTeX engine | Builds `dist/book-latex.pdf` | local toolchain | Use an installed alternate engine if available; otherwise report unavailable PDF build |
| Python Markdown + WeasyPrint | Builds HTML/CSS PDF path | `scripts/build_pdf.py` | Report missing Python package/system dependency |
| GitHub Pages | Publishes `site/` output | `.github/workflows/deploy-pages.yml` | Build locally and report deployment not run |
| Beryl | Agent control plane and deterministic safety gate | `.beryl/` | Report unavailable project-specific checks honestly |

## Definition Of Done

A change is complete only when it has all of the following:

1. Source edits preserve the SIAP voice and publication criteria.
2. Durable project context changes are reflected in `.beryl/agent/` and, if relevant, `AGENT.md`.
3. Generated artifacts are rebuilt when build inputs change.
4. `./.beryl/scripts/check.sh` runs, or unavailable checks are explicitly reported.
5. `python3 scripts/build_latex_pdf.py` runs for publication-impacting changes, or the reason it could not run is reported.
6. Final response states changed files, checks run, skipped/unavailable checks, and whether generated artifacts changed.
