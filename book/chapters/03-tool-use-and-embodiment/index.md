# Chapter 3: Tool Use and Embodiment

Intelligence without interfaces is monologue. For two chapters Agent-427 has
thought, planned, remembered, and been judged, and every consequential idea it
had stopped at a guard that said "proposal only." This chapter, the embodied
half of **Part 2: The Foundations in Motion**, removes that comfort. It turns
reasoning into action through APIs (application programming interfaces, the
entry points other software exposes), retrieval, and feedback from an
environment that may lag, contradict itself, or push back on purpose.

## The Interpreter Gains a Body

In earlier chapters, an action could be treated as a mathematical choice. Here an
action crosses a boundary. It lands in a filesystem, a browser, a database, a
search index, a queue, or a human approval process. Agent-427, born with a
contract and educated by a reasoning interpreter, now receives a body made of
schemas, permissions, clocks, caches, and consequences.[^chapter-three-body]
Its new powers are proposal forms for `write`, `test`, and `deploy`, and its new
job is the one Part 0 showed it doing: integrating changes into this book's own
publication pipeline, the same workflow Chapter 4 will treat as a small society.

## What Crossing the Boundary Costs

At the boundary, structural choices acquire observable costs. Permissions must
be checked before anything happens. Latency—the waiting time between request and
response—must be paid, and it adds up quickly: if one file read takes 200
milliseconds and the agent reads twelve files before editing, it has spent 2.4
seconds just looking. Some side effects cannot be undone. Feedback may arrive
long after the decision that caused it. And the world stubbornly continues
existing after the model has finished its sentence.

Those costs change which questions matter. Chapter 2 asked what Agent-427
should think. This chapter asks what it may do, what evidence it must fetch
first, and how it can tell whether the world actually changed. The four topics
answer roughly in that order. Topic 1 treats a tool call as a contract: a
schema, meaning a declared shape for arguments and results, is a grammar for
external action. Topic 2 treats retrieval as a purchased observation, evidence
paid for in tokens and time. Topic 3 gives the agent sensors, the channels by
which the world reports back, and actuators, the channels by which the agent
affects it—and then lets those channels lag and lie. Topic 4 builds the
machinery that refuses an attractive action when the evidence behind it has not
earned the risk. The mathematics in each gives names to ordinary design
choices, which is exactly why it is worth having.

::: {.reader-question}
> **Skeptical Engineer:** So Part 2 is where the elegant interpreter meets a
> timeout and discovers that the universe has no `undo` method?
>
> **Author:** Precisely. Foundations become useful when they survive contact with
> a world that does not share the agent's prompt.

:::

## Topics

1. [Tool Interfaces and Function Calling](topic-01-tool-interfaces-and-function-calling.md)
2. [Retrieval-Augmented Tooling](topic-02-retrieval-augmented-tooling.md)
3. [Embodiment: Sensors, Actuators, and Feedback](topic-03-embodiment-sensors-actuators-and-feedback.md)
4. [Safety Constraints and Guardrails](topic-04-safety-constraints-and-guardrails.md)

[^chapter-three-body]: This is embodiment without the chrome skeleton. A REST
    endpoint can resist your intentions just as effectively as a locked door,
    and usually with a less informative error message.
