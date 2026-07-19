# Ubiquitous Language

| Term | Technical Symbol / Path | Definition | Constraints | Avoid |
| --- | --- | --- | --- | --- |
| SIAP | `Structure and Interpretation of Agentic Patterns` | The book manuscript and repository project. | Must preserve SICP-like voice and theory/practice integration. | Treating it as a generic AI survey |
| Publication Artifact | `dist/book-latex.pdf` | The PDF that should be immediately publishable. | Must be regenerated through `scripts/build_latex_pdf.py`. | Hand-editing generated PDF/TeX |
| Manuscript Source | `book/**/*.md` | Canonical editable book content. | Primary topic files drive the book; notes files are revision support. | Editing `dist/` as source |
| Topic File | `book/chapters/*/topic-*.md` | Primary prose unit under a chapter. | Should flow naturally and avoid visible templates. | Formula pile, boxed pattern |
| Notes Companion | `*-notes.md` | Revision notes and alternate rewrites. | Excluded from publication build. | Treating notes as published prose |
| Agent Interpreter | `observe -> update_state -> choose_action -> execute` | Central constructive spine of the book. | Later chapters should elaborate this spine. | One-off analogies disconnected from the spine |
| Belief State | `b_t(s)` | Agent representation of uncertainty under partial observability. | Should drive action, retrieval, and communication decisions. | Confidence as decoration |
| State Abstraction | `phi: S -> Z` | Decision-relevant compression of history/state. | Must preserve behaviorally relevant distinctions. | Raw transcript as state |
| Tool Contract | `Pre`, `Post`, `Cost`, `Risk`, idempotency key | Boundary between language and external effect. | Must classify failures and guard side effects. | Prompt-only safety |
| Idempotent Effect | keyed effect plus ledger | At-least-once delivery yields one durable visible effect. | Requires atomic ledger/effect or keyed external operation. | "Exactly once" network fantasy |
| Safety Filter | constrained transition guard | Runtime mechanism that blocks or escalates unsafe actions. | Architecture, not apology. | Post-hoc safety prose |
| Decentralized Belief | `b_i^t(s)` | Local beliefs held by agents sharing only partial observations/messages. | Chapter 4 protocols must account for local information limits. | Assuming one global omniscient state |
| Shared Publication Environment | drafter/fact-checker/integrator workflow | Running Chapter 4 example for many interpreters sharing artifacts. | Use to explain protocols, incentives, learning dynamics, orchestration. | Abstract committees without state |
| Beryl Control Plane | `.beryl/agent/` | Canonical repository-owned agent context, checks, and routing. | Generated shims must sync from Beryl. | Editing shims manually |
| Generated Shim | `AGENTS.md`, `.codex/AGENTS.md`, etc. | Tool-specific entry file generated from Beryl. | Do not edit directly. | Divergent tool instructions |
| Deterministic Gate | `./.beryl/scripts/check.sh` | Beryl aggregate check command. | Run after edits; report unavailable project checks. | Claiming verification without output |
| LaTeX Build | `python3 scripts/build_latex_pdf.py` | Publication PDF build command. | Run for publication-impacting changes. | Relying only on source scans |
| Design Tree | `.beryl/agent/design-tree.md` | Living record of open/settled project decisions. | Update for durable workflow/build/book-structure decisions. | Chat-only decisions |
