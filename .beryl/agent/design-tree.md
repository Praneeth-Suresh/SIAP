# Design Tree

## Current Design Concept

SIAP is a compact, publishable monograph organized around an agent interpreter. Each chapter elaborates one layer of the interpreter: primitive agency, reasoning architecture, external action, and multi-agent institutions. The repository now carries Beryl as the durable control plane so future agent sessions can reload the same publication criteria, build rules, and verification expectations.

## Open Decisions

| Decision | Options | Current Lean | Why |
| --- | --- | --- | --- |
| Runnable exercises | Keep pseudocode only; add executable Python notebooks/scripts; add tests around examples | Add focused Python exercises later | AGENT.md identifies runnable code exercises as the next manuscript improvement, but publication PDF is already passable |
| Legacy `AGENT.md` | Keep as historical root instruction; fold entirely into Beryl; remove after migration | Keep and keep aligned for now | User explicitly asked to carry `AGENT.md` context into Beryl; deletion should wait for explicit approval |
| HTML/CSS PDF path | Maintain alongside LaTeX; deprecate in favor of LaTeX | Maintain for now | README documents both outputs; LaTeX is publication artifact |
| Project-specific test command | Configure `python3 scripts/build_latex_pdf.py` as broad check; leave no-op until faster test suite exists | Use Beryl check plus explicit build commands in testing policy | Beryl affected-test config should not invent a unit-test suite |

## Settled Decisions

| Decision | Choice | Date | ADR |
| --- | --- | --- | --- |
| Publication artifact | `dist/book-latex.pdf` | 2026-07-19 | n/a |
| Print class | LaTeX `book` class with front matter and chapter/topic hierarchy | 2026-07-19 | n/a |
| Book structure | Four chapters: foundations, reasoning architectures, tool use/embodiment, multi-agent systems | 2026-07-19 | n/a |
| Style target | SICP-like academic, philosophical, integrative exposition | 2026-07-19 | n/a |
| Repetitive heading policy | Avoid visible template headings such as "Three-theory braid" | 2026-07-19 | n/a |
| Citation anchor strategy | Native Markdown spans in `book/references.md` for Pandoc labels | 2026-07-19 | n/a |
| Beryl profile | Full profile installed: agent core, shims, checks, githooks, CI, driver | 2026-07-19 | n/a |
| Accessibility floor | Entry-level undergraduate readers must receive first-use definitions, symbol explanations, worked traces, and engineering consequences without removing existing equations or concepts | 2026-07-19 | n/a |
| Research-question spine | Pattern representation, effectiveness, composition effects, and task dependence provide the implicit connective questions from preface through evaluation passages | 2026-07-19 | n/a |

## Publication Pass Record

The publication pass used:

- gpt-5.6 critic agents for manuscript gates.
- gpt-5.5 worker agents for bounded chapter rewrites.
- Deterministic local checks: `python3 scripts/build_latex_pdf.py`, `git diff --check`, generated-artifact scans, and Python script compilation.
- Final gpt-5.6 verdict: **PASS. No material publication blockers remain.**

Material corrections made:

- Corrected topic/chapter numbering by changing book assembly order and heading demotion.
- Converted LaTeX output to `book` class with proper front matter.
- Removed stale local `.md` links from publication artifact by converting them to internal anchors.
- Replaced raw HTML bibliography anchors with Pandoc-native labels.
- Corrected idempotency to require atomic ledger/effect behavior or keyed external effects.
- Corrected dominant-strategy truthfulness to compare true report \(\theta_i\) against alternative \(\theta_i'\).
- Corrected MPC control-sequence notation, no-regret equilibrium distinction, causal replay assumptions, and lag-aware filtering.

## Pressure Points

- The manuscript is compact rather than SICP-length; future expansion should add executable exercises rather than broad survey material.
- Chapter 4 now has a recurring worked example, but deeper Dec-POMDP treatment could be a future feature if the book expands.
- Bibliography normalization can continue, but current citations resolve and no material publication blocker remains.
- Generated artifacts are tracked, so source changes must rebuild them deliberately.

## Recording Rule

Update this file when publication architecture, chapter structure, build strategy, or Beryl workflow assumptions change. Create an ADR when a decision changes repository boundaries, generated-artifact policy, test strategy, or agent-control-plane structure.
