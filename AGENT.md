# AGENT.md

This file defines the durable principles and operating instructions for future agent sessions in this repository.

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
- Generated outputs:
  - `site/` for static web deployment
  - `dist/book.html` and `dist/book.pdf` for print/web artifacts
- GitHub Pages deploy workflow: `.github/workflows/deploy-pages.yml`

## Session workflow rules

- Keep chapter flow coherent unless a research-backed restructuring improves pedagogy.
- Preserve citation density and link integrity whenever content changes.
- Keep the project plan in `plan.md`; update it at meaningful milestones.
