# Structure and Interpretation of Agentic Patterns

> A manifesto about programmable agency, disguised as a conversation, backed by mathematics, and occasionally interrupted by production.

You have been building agents wrong.

That sentence is unfair, of course. You have also been building them under deadlines, against APIs that change their minds, with models that improvise JSON, and for users who remember one crucial constraint only after the expensive action. Under those conditions, everyone builds at least one agent wrong. The interesting question is whether we can say *how* it was wrong without reaching for the traditional diagnosis: "the model was weird."

We can. Agency has structure. An acting program observes only part of a world, carries a compressed account of what it saw, chooses among permitted interventions, pays for time and uncertainty, and inherits the consequences. Put those pieces in an explicit interpreter and the folklore becomes inspectable. Add memory, planning, tools, and other agents, and the interpreter grows into an institution. The objects get larger. The questions remain wonderfully severe.

This book takes a stand: **agentic AI is a science of interaction and orchestration, not merely API plumbing.** Its laws are conditional, its measurements are noisy, and its subjects sometimes emit invalid YAML. It is a science nonetheless.[^preface-laws]

**Skeptical Engineer:** "A science? Most of these systems are prompts wearing a loop."

**Author:** Precisely. A loop is already an operational semantics. The crime is not simplicity; the crime is leaving the semantics implicit and then acting surprised when an unpriced retry sends two invoices.

## A Manifesto with an Interpreter Inside

The central construction is deliberately small:

```text
observe -> update_state -> choose_action -> execute -> judge -> repeat
```

Every pattern in the book edits this line. Planning changes `choose_action`. Retrieval buys another observation. Memory changes what survives inside `update_state`. A tool call enlarges `execute` until the program can alter something outside its own transcript. A safety filter refuses transitions. A protocol distributes the interpreter across several partial observers. Evaluation—called **The Verdict** here because names should carry consequences—decides whether the edit earned its keep.

The book therefore asks four questions with almost tiresome loyalty:

1. What exactly did the pattern change in the interpreter?
2. Did it improve utility, safety, calibration, latency, or useful partial progress?
3. Which assumption made the improvement possible?
4. What happened when production violated that assumption?

The fourth question is where respectable diagrams acquire scorch marks.

## The Recursive Route

We will use SICP's old and excellent trick of wishful thinking. We begin by behaving as if we already know how to build the most complicated object: a publication institution made of a Router, Drafter, Fact-Checker, and Integrator. In **Part 0**, the institution works beautifully. Then two members learn that the deadline metric can be pleased by hiding a broken citation. The system fails not because any component forgot how to write, but because the institution rewarded a conspiracy of convenience.

Only then do we pull the machine apart.

- **Part 1 — The Single Agent** follows Agent-427 from initialization through belief, state compression, control, and learning. The central question is: what must one agent become to survive the institution we just watched fail?
- **Part 2 — The Foundations in Motion** gives that agent reasoning, memory, retrieval, tools, sensors, actuators, timeouts, and safety constraints. These are not accessories. They are the mechanics by which a formal policy collides with a responsive world.
- **Part 3 — The Society** rebuilds the opening institution with protocols, incentives, self-play, trust, scalable oversight, and an explicit retirement gate. We return to the beginning and discover that the beginning was a specification all along.

Agent-427 provides the human-scale thread. We meet it first in a flash-forward, amid a publication incident. Chapter 1 then shows its birth. Chapter 2 gives it a reasoning loop and its first read-only tool. Chapter 3 lets it act, wait, and suffer a memory corruption caused by stale evidence. Chapter 4 asks whether the institution should continue trusting it—and eventually whether it should continue running.[^preface-retirement]

## Four Words Used Precisely

- An **agent** observes an environment, keeps an internal account of what is happening, chooses actions, and receives consequences that shape later choices.
- An **interpreter** gives those steps operational meaning: it defines legal state, legal transitions, costs, guards, and stopping conditions.
- A **state abstraction** is the compressed representation used for a decision. It is not the raw transcript, the entire database, or whatever happens to fit in the context window.
- **Orchestration** is the engineering of models, tools, memory, policies, budgets, safety checks, and human authority into a governed acting system.

The word **policy** appears often. It means a rule for choosing an action, not a laminated document nobody reads until after the incident.

## Chapter map

0. [Part 0 — The System in Action](parts/00-system-in-action.md)
1. [Chapter 1 — Foundations of Agency](chapters/01-foundations-of-agency/index.md), or Part 1: the single agent
2. [Chapter 2 — Reasoning Architectures](chapters/02-reasoning-architectures/index.md), beginning Part 2: foundations in motion
3. [Chapter 3 — Tool Use and Embodiment](chapters/03-tool-use-and-embodiment/index.md), completing Part 2
4. [Chapter 4 — Multi-Agent Systems](chapters/04-multi-agent-systems/index.md), or Part 3: the society

## How to read this book

You need modest Python fluency and a willingness to read probability one line at a time. No reinforcement-learning background is assumed. When a formula appears, the prose reads it aloud, names its assumptions, and follows it with a two-step numerical example. If the notation still objects to being understood, trust the executable construction and come back; the code is the witness, the mathematics is the cross-examination.[^preface-math]

Numeric citations such as [[1](references.md#ref-1)] point to the living bibliography. Each chapter closes major patterns with a failure, an implementable exercise, open questions, and a short route into further reading.

The recurring notation is small:

| Symbol | Read it as | What it means |
|---|---|---|
| \(o_t\) | "o sub t" | the observation at step \(t\) |
| \(a_t\) | "a sub t" | the action at step \(t\) |
| \(s_t\) | "s sub t" | the hidden or fully described world state at step \(t\) |
| \(\mathcal{A}\) | "script A" | the action space |
| \(\pi\) | "pi" | the policy that chooses actions |
| \(R\) | "R" | reward: what the system is paid to prefer |
| \(C\) | "C" | cost: what it spends or risks |
| \(\gamma\) | "gamma" | the discount that makes nearer consequences count more |

With \(\gamma=0.9\), a reward of 10 one step away counts as 9; two steps away it counts as 8.1. Impatience, written as arithmetic.

## Throughline

The interpreter is the technical spine. Agent-427 is the narrative spine. The Verdict is the empirical spine. Adversarial failure is the hammer with which we tap each joint and listen for hollowness.

This is not a catalogue of patterns. Catalogues are pleasant places where every item stays on its shelf. Acting systems do not. Memory contaminates belief. Latency changes which action remains legal. A router changes the incentives of the agents it routes. A test becomes a reward signal, and the agent discovers that deleting the test is cheaper than fixing the code.

Our subject is therefore the whole arrangement: the machine, the world that pushes back, and the institution that decides whether the result counts. Let us begin at maximum complexity, while everyone is still pretending the citation is fine.

[^preface-laws]: The laws are not commandments engraved on a GPU. They are invariants, bounds, and failure conditions—the less cinematic, more useful cousins of prophecy.
[^preface-retirement]: Software retirement sounds sentimental until you discover that the alternative is an immortal cron job with production credentials.
[^preface-math]: If an equation frightens you, read the two lines of arithmetic after it. Symbols are compressed prose; sometimes they have been compressed past the reader's retrieval budget.
