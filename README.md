# Structure and Interpretation of Agentic Patterns

![Build Pipeline](https://img.shields.io/badge/build-uv%20scripts-6f42c1)
![Output](https://img.shields.io/badge/output-HTML%20%2B%20PDF-0a7f2e)
![Deploy](https://img.shields.io/badge/deploy-GitHub%20Pages-24292f?logo=github)
![Citations](https://img.shields.io/badge/citations-clickable%20%5Bn%5D-c97a00)

This repository is a scratchpad for a somewhat audacious goal: to do for agentic systems what classic CS texts did for programming itself. We are not collecting clever prompts; we are constructing a theory-backed craft of orchestration.

## Project goals

1. Build a pedagogical path for agentic AI using **Python and modern agent/tooling frameworks** as today’s teaching language.
2. Walk readers through constructing **interpreters for reasoning loops, planners, and tool-using agents**, so architecture is learned by building.
3. Present a unifying conceptual frame for **autonomy, memory, and collaboration** rather than treating them as unrelated hacks.
4. Balance formal foundations (decision theory, reinforcement learning, symbolic methods, game theory) with practical systems work (LLM APIs, retrieval, orchestration runtimes).
5. Maintain a voice that is explanatory, witty, and slightly grandiose because big ideas deserve theatrical lighting.

## Why this manuscript matters

The counterfactual matters. If this manuscript did not exist, agent development would not stop. Teams would still ship useful systems with contemporary frameworks, papers, eval suites, model APIs, retrieval systems, and a fair amount of production trial and error. The claim for SIAP is therefore not that it invents agency from nothing. The claim is that agent engineering is still too often carried by local craft knowledge, prompt folklore, framework defaults, and scattered intuitions borrowed from older fields. SIAP tries to turn that scattered inheritance into a usable computer science of orchestration: objectives, belief states, transition semantics, memory policies, tool contracts, safety constraints, feedback loops, protocols, incentives, and evaluation traces, all made explicit enough to teach, test, and improve.

The first argument is that SIAP makes the hidden control structure of agents visible. Without this contribution, builders can still define goals, call tools, and set constraints, but those commitments often remain implicit in prompts, product requirements, or the habits of a particular engineering team. That makes systems harder to compare and govern. A useful agent may appear to work, yet no one can say precisely what objective it is optimizing, what action space it is allowed to inhabit, which constraints are hard boundaries, what budget it is spending, or when it should stop. By grounding agents in goals, environments, actions, constraints, rewards, and control loops, SIAP turns "the model decided" into a sharper engineering question: what did the policy see, what did it value, what was it permitted to do, and what feedback changed its next step? The practical gain is inspectability. Agent development without this formalization is possible, but it remains more dependent on taste, anecdotes, and post-hoc interpretation.

The second argument is that reasoning loops become easier to debug when they are treated as interpreters. A skeptical reader might say that production teams already inspect traces, logs, tool calls, and model outputs, and that operational semantics sounds too formal for probabilistic systems. That objection is partly right for simple assistants. It fails for long-running, stateful, tool-using agents whose mistakes have external consequences. In those systems, transcript reading is not enough. A failure may come from a bad state abstraction, an illegal transition, a missing guard, a corrupted observation, an exhausted budget, or a halt condition that fired too early or too late. SIAP's interpreter frame gives names and contracts to those moving parts. It does not make messy model behavior magically deterministic, but it gives builders a disciplined way to localize causal responsibility inside the loop. Without that frame, agent debugging is still possible, but it is more like reading a dramatic diary than inspecting a machine.

The third argument is that memory and retrieval should be decision policies, not feature checkboxes. RAG, vector databases, long-context models, and memory stores already exist, so SIAP should not claim credit for making agents retrieve information. Its stronger contribution is to clarify when memory helps and when it harms. Without a value-of-information lens, systems drift toward two poor defaults: retrieve everything and invite distractors into the control state, or retrieve too little and let fluent priors masquerade as evidence. SIAP treats retrieval, compression, preservation, and forgetting as costly epistemic actions. The relevant question is not whether a document is semantically similar, but whether the evidence changes the next action enough to justify its latency, token cost, permission risk, and contamination risk. That distinction matters in practice. It tells a coding agent when to inspect another file before editing, a compliance agent when current policy must be fetched before advice, and a research agent when another source will no longer change the answer.

The fourth argument is that tool use, embodiment, feedback, and safety belong to one theory of consequential action. Modern frameworks already offer schemas, permissions, retries, approval gates, monitors, and guardrails, so SIAP's practical value is not the isolated existence of any one mechanism. Its value is showing why these mechanisms are structurally connected. A tool call is not just a function call wrapped in JSON. It is an action with preconditions, side effects, delay, reversibility, failure modes, risk, cost, confirmation signals, and postconditions. Once that is explicit, safety is no longer a layer of apologetic prose placed after capability. It becomes part of the action semantics: unsafe actions can be made unrepresentable, risky actions can be priced, ambiguous actions can escalate, retries can be idempotent, and failures can be classified by contract category. Without this synthesis, teams may still add guardrails, but they are more likely to add them piecemeal, after incidents, and without a shared account of how action should be bounded.

The fifth argument is that multi-agent systems need institutional design, not merely more participants. Many useful systems will remain single-agent systems, and many multi-agent demos add latency, cost, and ceremonial disagreement without improving decisions. SIAP should therefore not argue that more agents are inherently better. It should argue that agent collectives only become useful when communication, specialization, incentives, and evaluation are designed. Without that frame, it is easy to create a "researcher, critic, planner" workflow and mistake message volume for reasoning quality. The hard questions are institutional: who may speak, what kind of message binds the group, when is communication worth its cost, how are commitments represented, what incentives encourage honest competence claims, how is exploitability measured, and whether disagreement actually reduces correlated error. SIAP brings coordination protocols, mechanism design, equilibria, self-play, and ensemble theory into the practical work of agent orchestration. That makes multi-agent design less like assembling a room of confident voices and more like building a small institution whose behavior can survive pressure.

Taken together, these arguments define the practical research program behind the manuscript. SIAP advances the goal of building better agents by making agent systems more formal where formality pays rent: objectives become inspectable, uncertainty becomes actionable, memory becomes governed, tool use becomes contract-bound, safety becomes architectural, and collaboration becomes institutional. The field would continue without this synthesis, but it would be worse off in a specific way: more fragmented, less precise about failure, less disciplined about evidence and side effects, and more dependent on the private craft of individual teams. SIAP's wager is that better agents will come not only from stronger models, but from a clearer science of the systems that let models perceive, decide, act, recover, and cooperate.

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
