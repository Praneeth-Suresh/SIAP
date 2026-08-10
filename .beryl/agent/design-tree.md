# Design Tree

## Current Design Concept

SIAP is a compact, publishable monograph organized around an agent interpreter. Each chapter elaborates one layer of the interpreter: primitive agency, reasoning architecture, external action, and multi-agent institutions. The repository now carries Beryl as the durable control plane so future agent sessions can reload the same publication criteria, build rules, and verification expectations.

## Open Decisions

| Decision | Options | Current Lean | Why |
| --- | --- | --- | --- |
| Legacy `AGENT.md` | Keep as historical root instruction; fold entirely into Beryl; remove after migration | Keep and keep aligned for now | User explicitly asked to carry `AGENT.md` context into Beryl; deletion should wait for explicit approval |
| HTML/CSS PDF path | Maintain alongside LaTeX; deprecate in favor of LaTeX | Maintain for now | README documents both outputs; LaTeX is publication artifact |
| Project-specific test command | Expand focused builder tests; rely on explicit builds for publication checks | Start with standard-library site-builder regression tests plus Beryl and build commands | The static-site manifest and navigation now have a fast deterministic test surface |

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
| Public book site | Keep the custom static builder; publish only reader-facing pages in manuscript order, with hierarchical chapter/topic navigation, adjacent-reading controls, and MathJax rendering | 2026-08-06 | n/a |
| Recursive editorial arc | Add an unnumbered Part 0 before the stable four chapters; Part 1 is Chapter 1's single-agent survival problem, Part 2 spans Chapters 2--3's reasoning, memory, tools, and embodied foundations, and Part 3 returns to Chapter 4's society | 2026-08-06 | [ADR 0008](adr/0008-publication-spine-and-recursive-arc.md) |
| Publication ordering | Declare reader-facing source order and section kind in `book/publication.toml`; all builders and manuscript audits consume the same manifest | 2026-08-06 | [ADR 0008](adr/0008-publication-spine-and-recursive-arc.md) |
| Exercise contract | Every topic ends in an implementable, code-required exercise; reference implementations may be added later without weakening the assignment | 2026-08-06 | n/a |
| Editorial contract | Audit formula examples, pattern assumptions/violations/failures, diagrams, citations, footnotes, and required production case studies deterministically | 2026-08-06 | [ADR 0008](adr/0008-publication-spine-and-recursive-arc.md) |
| Publication enrichment | Keep sourced epigraphs and visual placements in strict registries; inject them across every builder; require semantic unnumbered reader blocks and measured image safe areas | 2026-08-06 | [ADR 0009](adr/0009-publication-enrichment-contracts.md) |
| Terminal cartoon language | Use original silent, varied three-to-five-panel mini Sunday pages with the recurring Agent-427 cast, broken brush contours, bright paper, elastic acting, sparse reality, richer fantasy, and measured print-safe margins | 2026-08-07 | [ADR 0009](adr/0009-publication-enrichment-contracts.md) |
| Diagram delivery | Make registry alt text canonical; publish SVG masters in bounded web viewports and 2400×1400 PNG fallbacks in print; reject internal label and connector collisions | 2026-08-07 | [ADR 0009](adr/0009-publication-enrichment-contracts.md) |
| Public contribution surface | Keep contributor, conduct, security, support, license, issue, and pull-request guidance at the repository root; keep it distinct from internal Beryl agent instructions and publication-enrichment registries | 2026-08-10 | n/a |

## Publication Pass Record

## Complete Rewrite Placement Map

The editor-directed recursive arc preserves the stable chapter routes while changing the reader's encounter with them:

| Movement | Canonical source owner | Existing topics retained in place | New burden |
| --- | --- | --- | --- |
| Part 0: The System in Action | `book/parts/00-system-in-action.md` | none | Publication workflow, perfect run, collusive catastrophe, first Verdict, and the institutional question |
| Part 1: The Single Agent | Chapter 1 index and four Chapter 1 topics | goals/actions, belief, abstraction, policy/control | Agent-427's birth, The Gap for the POMDP tuple, learning lifecycle, and theorem violations |
| Part 2: The Foundations in Motion | Chapter 2 and Chapter 3 indexes and topics | interpreter, planning, memory, evaluation, tools, retrieval, embodiment, safety | memory war room, responsive environment, strategic sensing, poisoning, timeout action, and evaluation as The Verdict |
| Part 3: The Society | Chapter 4 index and four Chapter 4 topics | protocols, mechanisms, learning dynamics, orchestration | scalable oversight, Byzantine router lie, collusion simulation, trust interest, self-play stress, and retirement |

No existing topic changes ownership. The new part and narrative labels change the order of explanation, not stable chapter URLs.

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

- The manuscript is compact rather than SICP-length; future expansion should add maintained reference implementations for its code-required exercises rather than broad survey material.
- Chapter 4 now has a recurring worked example, but deeper Dec-POMDP treatment could be a future feature if the book expands.
- Bibliography normalization can continue, but current citations resolve and no material publication blocker remains.
- Generated artifacts are tracked, so source changes must rebuild them deliberately.

## Recording Rule

Update this file when publication architecture, chapter structure, build strategy, or Beryl workflow assumptions change. Create an ADR when a decision changes repository boundaries, generated-artifact policy, test strategy, or agent-control-plane structure.
