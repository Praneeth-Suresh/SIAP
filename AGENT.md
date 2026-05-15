# AGENT.md

This file defines the durable principles and operating instructions for future agent sessions in this repository. Read README.md first to understand what this repository is about.

## Project voice and pedagogical stance (non-negotiable)

- Write in an explanatory, witty, slightly grandiose register inspired by SICP.
- Keep that voice consistent across README, chapters, topic rewrites, and supporting docs.
- Teach by construction: readers should see ideas become executable artifacts, not just slogans.

## Explicit SICP-homage commitments

1. **Pedagogical language first**: use Python (plus contemporary agent frameworks/tooling) as the teaching language, in the same spirit Lisp served SICP.
2. **Interpreter-centered learning**: walk through building interpreters for reasoning loops, planners, and tool-using agents.
3. **Unified conceptual framework**: present autonomy, memory, and collaboration as one coherent architecture, not disconnected patterns.
4. **Theory-practice balance**: pair decision theory, reinforcement learning, and symbolic reasoning with concrete LLM APIs and orchestration frameworks.

## Foundational principles of the book

1. **Agentic AI is orchestration science**: treat agents as interaction systems, not prompt wrappers.
2. **Formalize before implementing**: define goals, environments, state, actions, and control loops explicitly.
3. **Model uncertainty directly**: represent beliefs and decision trade-offs instead of assuming certainty.
4. **Use interpreter thinking**: loop semantics, state transitions, and invariants must be inspectable.
5. **Unify memory and action**: memory is a policy (retain/retrieve/forget), not transcript accumulation.
6. **Bridge theory to code**: map mathematical ideas to implementation patterns and measurable behavior.
7. **Design for institutions**: multi-agent coordination, negotiation, and equilibrium concerns are first-class.
8. **Prefer robust collectives**: ensembles/specialists with explicit routing often beat single-model fragility.
9. **Constrained autonomy wins**: safety, budgets, permissions, and escalation paths are architecture, not afterthoughts.

## Source and citation policy

- Citation policy: mixed authoritative sources (peer-reviewed papers + high-quality books/docs).
- Every externally sourced idea must include clickable numeric citation syntax: `[[n](...)]`.
- `book/references.md` is the canonical bibliography index and anchor target.

## Content structure conventions

- Book scope: **4 chapters**, up to **7 topics per chapter**.
- Each chapter has an `index.md`.
- Each topic has:
  - a primary file: `topic-XX-*.md`
  - a companion revision file: `topic-XX-*-notes.md`
- Each notes file must include:
  - concrete improvement notes
  - at least one alternative rewrite

## Build and deployment defaults

- Use **uv** for Python workflows:
  - `uv venv`
  - `uv pip install -r requirements.txt`
  - `uv run python scripts/build_site.py`
  - `uv run python scripts/build_pdf.py`
  - `uv run python scripts/build_latex_pdf.py`
- Generated outputs:
  - `site/` for static web deployment
  - `dist/book.html`, `dist/book.pdf`, `dist/book.tex`, and `dist/book-latex.pdf` for print/web artifacts
- GitHub Pages deploy workflow: `.github/workflows/deploy-pages.yml`

## Session workflow rules

- Keep chapter flow coherent unless a research-backed restructuring improves pedagogy.
- Preserve citation density and link integrity whenever content changes.
- Keep the project plan in `plan.md`; update it at meaningful milestones.

## Progress update (current milestone)

- Task 1 formalization pass completed across all primary topic files:
  - each topic now includes mathematical formalization where applicable,
  - a three-theory braid grounded in research literature,
  - explicit guidance for formal empirical study.
- Bibliography expanded substantially in `book/references.md` with additional authoritative papers/books.
- LaTeX rendering pipeline added via `scripts/build_latex_pdf.py` to produce math-clean PDF artifacts.

## Active rewrite protocol: Chapter 1 three-pass expansion

- For each Chapter 1 topic, run exactly three passes:
  1. **Pass 1 (notes-first migration + storyline design):**
     - move current main-topic ideas into the corresponding `*-notes.md`,
     - draft storyline development in prose paragraphs (each part as a separate paragraph),
     - append a list of alternative execution approaches at the end of the notes file.
  2. **Pass 2 (research and equation harvest):**
     - perform extensive web research on canonical equations and formalism,
     - append theory descriptions, equation sets, and connection logic beneath Pass 1 material in notes.
  3. **Pass 3 (main text synthesis via subagents):**
     - use subagents to transform notes into polished primary topic text,
     - produce narrative-driven prose that braids theory with explicit mathematics.
- Narrative target for Chapter 1 rewrites:
  - present the three-theory braid as a living architecture of decision-making,
  - make intelligence read as interplay between foresight, responsiveness, and resilience,
  - maintain scholarly clarity while inviting curiosity and reflection.

## Rewrite milestone: Chapter 2 three-pass expansion (completed)

- Applied the same three-pass workflow to all Chapter 2 topics:
  1. migrated prior main-topic ideas into companion notes,
  2. appended equation/theory research synthesis,
  3. rewrote primary topic text from a clean slate using notes as source.
- Expanded each Chapter 2 topic braid into full narrative treatment linking expected utility, dynamic planning/control, and robustness-oriented evaluation.
- Preserved clickable numeric citation style and reference anchors across new Chapter 2 content.

## Rewrite milestone: Chapters 3 and 4 three-pass expansion (completed)

- Applied the same three-pass workflow to all Chapter 3 and Chapter 4 topics:
  1. migrated prior main-topic ideas into companion notes,
  2. appended equation/theory research synthesis with external-source linking,
  3. rewrote primary topic text from a clean slate using notes as source.
- Expanded tool-use, safety, coordination, mechanism-design, strategic-dynamics, and ensemble-orchestration braids into full narrative treatments with explicit mathematical formalism.
- Preserved clickable numeric citation style and reference-anchor compatibility across all updated topic text.


## Current status
- Core scaffold is complete: chapter/topic sources, companion rewrite notes, references, build scripts, site template, stylesheet, and deployment workflow.
- Documentation baseline is refreshed: `.gitignore`, `README.md`, and `AGENT.md` now reflect project conventions and voice requirements.
- Task 1 completed: all primary topics were expanded with formal mathematical framing, theory triangulation, and deeper research-backed exposition.
- References expanded to include additional foundational and modern sources across decision theory, planning, control, retrieval, safety, and multi-agent game dynamics.
- LaTeX PDF rendering pipeline added to produce `dist/book.tex` and `dist/book-latex.pdf` for cleaner mathematical typesetting.
- Chapter 2 topics and notes now reflect full three-pass rewrites with storyline outlines, equation harvests, and polished narrative synthesis.
- Chapters 3 and 4 topics and notes now reflect full three-pass rewrites with storyline outlines, equation harvests, and polished narrative synthesis.

## Next steps
1. Add runnable code exercises per chapter (especially interpreter and planner sections).
2. Strengthen cross-links between theoretical claims and concrete orchestration patterns.
3. Continue style-pass editing to keep a consistent witty, slightly grandiose pedagogical tone.
4. Add benchmark/evaluation writeups for agent loop quality and tool-use reliability.
