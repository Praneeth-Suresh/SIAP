# Chapter 3: Tool Use and Embodiment

Intelligence without interfaces is monologue. This chapter turns reasoning into action through APIs, retrieval, and environment-coupled feedback.

The interpreter now gains a body. In earlier chapters, an action could be
treated as a mathematical choice; here an action crosses a boundary into a
filesystem, browser, database, search index, queue, or human approval process.
At that crossing, structural choices acquire observable costs: permissions must
be checked, latency must be paid, side effects may be irreversible, feedback may
arrive late, and the world may stubbornly continue existing after the model has
finished its sentence. The running example is still a software agent revising
and publishing a book, but the interesting questions shift from "what should it
think?" to "what may it do, what evidence must it fetch first, and how does it
learn whether the world actually changed?"

A freshman reader should read this chapter as the engineering chapter of the
book's formal story. A schema is a grammar for external action. A retrieval
result is a purchased observation. A sensor is any channel by which the world
reports back, and an actuator is any channel by which the agent can affect that
world. The mathematics below gives names to these ordinary design choices.

## Topics

1. [Tool Interfaces and Function Calling](topic-01-tool-interfaces-and-function-calling.md)
2. [Retrieval-Augmented Tooling](topic-02-retrieval-augmented-tooling.md)
3. [Embodiment: Sensors, Actuators, and Feedback](topic-03-embodiment-sensors-actuators-and-feedback.md)
4. [Safety Constraints and Guardrails](topic-04-safety-constraints-and-guardrails.md)
