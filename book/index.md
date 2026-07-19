# Structure and Interpretation of Agentic Patterns

> A text for readers who suspect that agentic systems are not a bag of orchestration tricks, but programmable structures with laws, invariants, and failure modes.

This book follows a SICP-like arc: start with the primitive elements of agency, assemble them into interpreters, study the architectures that make those interpreters useful, and then examine what happens when many such systems act in shared environments.

An **agent**, in this book, is a system that observes some environment, maintains an internal account of what is going on, chooses actions, and receives consequences that affect later choices. An **interpreter** is the explicit loop that gives those steps operational meaning: observe, update internal state, choose an action, execute, and repeat. A **state abstraction** is the compressed representation the interpreter actually uses for decisions, rather than the whole raw transcript of everything that has happened. **Orchestration** is the engineering discipline of arranging models, tools, memory, policies, budgets, safety checks, and human escalation so that this loop behaves like a governed machine instead of an improvising monologue.

The book's research program begins with a modest trick: every agentic pattern is treated as a change to that interpreter. A pattern may alter the state the agent carries, the control flow by which it reasons, the feedback it listens to, the memory it may consult, the authority it is permitted to exercise, or the condition under which it must stop. Once the change is visible, we can ask the less glamorous but more useful question: did it earn its keep? The evidence may be final task success, partial progress before failure, token use, latency, tool-call efficiency, or a smaller number of dangerous almost-actions. Patterns can also collide or cooperate. Retrieval may make planning better, or it may flood the policy with irrelevant facts; oversight may prevent a bad deployment, or it may waste ceremony on a cheap reversible step. The right design therefore depends on the task: uncertainty, action stakes, reversibility, horizon length, available feedback, and budget all predict which machinery is worth carrying.

## Chapter map

1. [Chapter 1 - Foundations of Agency](chapters/01-foundations-of-agency/index.md)
2. [Chapter 2 - Reasoning Architectures](chapters/02-reasoning-architectures/index.md)
3. [Chapter 3 - Tool Use and Embodiment](chapters/03-tool-use-and-embodiment/index.md)
4. [Chapter 4 - Multi-Agent Systems](chapters/04-multi-agent-systems/index.md)

## How to read this book

The prerequisites are modest but real. You should be comfortable reading short Python-like pseudocode, basic probability statements such as \(P(A\mid B)\), and summations such as \(\sum_t\), which mean "add this quantity over the indicated steps." No reinforcement-learning background is assumed; the early chapters build the needed vocabulary as they go. Follow numeric citations like [[1](references.md#ref-1)] to the reference list when you want the scholarly ancestry of an idea.

Notation follows a small convention. Time is written with subscripts: \(o_t\) is the observation at step \(t\), \(a_t\) is the action at step \(t\), and \(s_t\) is the hidden or fully described world state at step \(t\). Sets use calligraphic letters such as \(\mathcal{A}\) for the action space. A policy \(\pi\) is a rule for choosing actions. A reward \(R\) says what helped; a cost \(C\) says what was spent or risked; a discount \(\gamma\) says that nearer consequences count more heavily than distant ones.

As a tiny trace, suppose a coding agent observes `test_auth.py::test_expired_token FAILED`. Its interpreter state becomes something like `{failing_behavior: "expired token", suspects: ["auth/session.py"], risk: "login regression"}`. It chooses the action `read auth/session.py`, observes a changed comparison against token expiry, updates the state to `{suspected_cause: "off-by-one expiry check", evidence: "source inspected"}`, and only then chooses `edit auth/session.py`. The two actions may look mundane. Their importance is that observation became interpreter state before it became action.

## Throughline

The central claim of this project is that agentic AI is a science of interaction and orchestration, not merely API plumbing. Chapter 1 develops the core interpreter: goals specify what matters, belief tracks uncertainty, state abstraction makes history usable, and control turns action into a feedback loop. Later chapters elaborate that interpreter with reasoning patterns, tools, memory, embodiment, and social coordination.

Methodologically, each chapter changes the running interpreter and then asks when that change earns its cost in success, progress, efficiency, safety, or governability.
