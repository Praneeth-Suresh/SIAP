# Structure and Interpretation of Agentic Patterns

> A text for readers who suspect that agentic systems are not a bag of orchestration tricks, but programmable structures with laws, invariants, and failure modes.

This is a book about programs that act. Some software answers a question and stops. The software in this book keeps going: it looks at the world, decides something, does something, and then has to live with the result. That loop is the object of study here, and it turns out to have structure worth teaching.

The book follows the arc of *Structure and Interpretation of Computer Programs*. We start with the primitive elements of agency. We assemble them into interpreters. We study the architectures that make those interpreters useful. Then we examine what happens when many such systems act in one shared environment.

## A first trace, before any theory

Watch one small machine work. Suppose a coding agent sees this line of test output:

```
test_auth.py::test_expired_token FAILED
```

A careless system would jump straight to editing a file. This one writes down what it now believes:

```
{failing_behavior: "expired token",
 suspects: ["auth/session.py"],
 risk: "login regression"}
```

Then it chooses the action `read auth/session.py`. It observes a changed comparison against the token expiry time. It revises what it believes:

```
{suspected_cause: "off-by-one expiry check", evidence: "source inspected"}
```

Only now does it choose `edit auth/session.py`. Two ordinary actions, one small structure between them. That structure is the whole point: the observation became internal state before it became an action. Everything else in this book is an argument about what belongs in that state, who may change it, and what it costs to carry.

## Four words used precisely

Four terms recur constantly, so they are pinned down here rather than left to context:

- An **agent** is a system that observes some environment, keeps an internal account of what is going on, chooses actions, and receives consequences that shape its later choices.
- An **interpreter** is the explicit loop that gives those steps operational meaning: observe, update internal state, choose an action, execute, repeat.
- A **state abstraction** is the compressed representation the interpreter actually uses when deciding. It is not the whole raw transcript of everything that has happened. In the trace above, the short dictionary is the state abstraction; the full test log is not.
- **Orchestration** is the engineering discipline of arranging models, tools, memory, policies, budgets, safety checks, and human escalation so that the loop behaves like a governed machine rather than an improvising monologue. A **policy**, in the sense used throughout, is simply the agent's rule for choosing actions.

## Every pattern is an edit to the interpreter

The research program of this book begins with a modest trick. Treat each agentic pattern not as a recipe, but as a change to that interpreter. A pattern may alter any of the following:

- the state the agent carries,
- the control flow by which it reasons,
- the feedback it listens to,
- the memory it may consult,
- the authority it is permitted to exercise,
- the condition under which it must stop.

Making the change visible lets us ask the less glamorous but more useful question: did it earn its keep? So the questions this book keeps returning to are these four.

**First, how is a pattern represented structurally?** Name the part of the interpreter it edits. A vague pattern cannot be compared with anything.

**Second, what does it do to the measurable outcomes?** The evidence we care about is final task success, partial progress before failure, token use, latency, tool-call efficiency, and a smaller number of dangerous almost-actions. A pattern that lifts success from 60 to 66 tasks out of 100 while tripling token cost has not obviously won.

**Third, how do combined patterns interact?** Patterns collide as often as they cooperate. Retrieval may make planning sharper, or it may flood the policy with irrelevant facts. Oversight may prevent a bad deployment, or it may spend ceremony on a cheap, reversible step.

**Fourth, which task characteristics predict when a pattern helps?** Uncertainty, action stakes, reversibility, horizon length, available feedback, and budget all shift the answer. The right design is therefore a function of the task, not a fashion.

## Chapter map

1. [Chapter 1 - Foundations of Agency](chapters/01-foundations-of-agency/index.md)
2. [Chapter 2 - Reasoning Architectures](chapters/02-reasoning-architectures/index.md)
3. [Chapter 3 - Tool Use and Embodiment](chapters/03-tool-use-and-embodiment/index.md)
4. [Chapter 4 - Multi-Agent Systems](chapters/04-multi-agent-systems/index.md)

## How to read this book

The prerequisites are modest but real. You should be comfortable reading short Python-like pseudocode. You should be able to read a basic probability statement such as \(P(A\mid B)\), which reads "the chance of A given that B holds." You should also be able to read a summation such as \(\sum_t\), which means "add this quantity over the indicated steps."

No reinforcement-learning background is assumed. The early chapters build the needed vocabulary as they go. Numeric citations like [[1](references.md#ref-1)] point to the reference list, where you can trace the scholarly ancestry of an idea.

Notation follows a small and stable convention. Time is written with subscripts, and sets are written with calligraphic letters. The following table lists the symbols that recur across the whole book, with the way to read each one aloud. Each chapter introduces further notation where it is needed, and defines it there:

| Symbol | Read it as | What it means |
|---|---|---|
| \(o_t\) | "o sub t" | the observation at step \(t\) |
| \(a_t\) | "a sub t" | the action at step \(t\) |
| \(s_t\) | "s sub t" | the world state at step \(t\), whether hidden from the agent or fully described |
| \(\mathcal{A}\) | "script A" | the action space, meaning the set of actions available |
| \(\pi\) | "pi" | a policy: a rule for choosing actions |
| \(R\) | "R" | a reward, which says what helped |
| \(C\) | "C" | a cost, which says what was spent or risked |
| \(\gamma\) | "gamma" | a discount, which says that nearer consequences count more heavily than distant ones |

A worked reading of the last row: with \(\gamma = 0.9\), a reward of 10 arriving one step from now is valued at 9, and the same reward two steps away is valued at 8.1. Impatience, written as arithmetic.

## Throughline

The central claim of this project is that agentic AI is a science of interaction and orchestration, not merely API plumbing.

Chapter 1 (Foundations of Agency) develops the core interpreter. Goals specify what matters. Belief tracks uncertainty. State abstraction makes history usable. Control turns action into a feedback loop. The later chapters elaborate that same interpreter with reasoning patterns, tools, memory, embodiment, and social coordination.

The method is constant. Each chapter changes the running interpreter, then asks when that change earns its cost in success, progress, efficiency, safety, or governability.
