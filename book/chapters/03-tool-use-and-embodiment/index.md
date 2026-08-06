# Chapter 3: Tool Use and Embodiment

Intelligence without interfaces is monologue. This chapter is the embodied half of
**Part 2: The Foundations in Motion**. It turns reasoning into action through APIs
(application programming interfaces, the entry points other software exposes),
retrieval, and feedback from an environment that may lag, contradict itself, or
push back on purpose.

## The Interpreter Gains a Body

In earlier chapters, an action could be treated as a mathematical choice. Here an
action crosses a boundary. It lands in a filesystem, a browser, a database, a
search index, a queue, or a human approval process. Agent-427, born with a
contract and educated by a reasoning interpreter, now receives a body made of
schemas, permissions, clocks, caches, and consequences.[^chapter-three-body]

## What Crossing the Boundary Costs

At that crossing, structural choices acquire observable costs. Five of them recur throughout the chapter:

- Permissions must be checked before the action is allowed.
- Latency, the waiting time between request and response, must be paid.
- Side effects may be irreversible, so there is no undo.
- Feedback may arrive late, long after the decision that caused it.
- The world may stubbornly continue existing after the model has finished its sentence.

A small example makes the cost real. If one file read takes 200 milliseconds, and the agent reads twelve files before editing, it has spent 2.4 seconds on looking.

## The Questions This Chapter Asks

The running example carries forward Agent-427, now working on this book's own
publication pipeline, which is the same workflow Chapter 4 will treat as a small
society. The interesting questions shift away from "what should it think?" Three
sharper questions replace it:

1. What may it do?
2. What evidence must it fetch first?
3. How does it learn whether the world actually changed?

## Reading This Chapter as Engineering

Read this chapter as the engineering chapter of the book's formal story. Three plain readings carry most of the weight.

A schema, meaning a declared shape for arguments and results, is a grammar for external action. A retrieval result is a purchased observation: evidence you paid tokens and time to obtain. A sensor is any channel by which the world reports back, and an actuator is any channel by which the agent can affect that world.

The mathematics in the four topics that follow gives names to these ordinary design choices.

> **Skeptical Engineer:** So Part 2 is where the elegant interpreter meets a
> timeout and discovers that the universe has no `undo` method?
>
> **Author:** Precisely. Foundations become useful when they survive contact with
> a world that does not share the agent's prompt.

## Topics

1. [Tool Interfaces and Function Calling](topic-01-tool-interfaces-and-function-calling.md)
2. [Retrieval-Augmented Tooling](topic-02-retrieval-augmented-tooling.md)
3. [Embodiment: Sensors, Actuators, and Feedback](topic-03-embodiment-sensors-actuators-and-feedback.md)
4. [Safety Constraints and Guardrails](topic-04-safety-constraints-and-guardrails.md)

[^chapter-three-body]: This is embodiment without the chrome skeleton. A REST
    endpoint can resist your intentions just as effectively as a locked door,
    and usually with a less informative error message.
