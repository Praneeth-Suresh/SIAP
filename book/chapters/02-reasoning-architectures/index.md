# Chapter 2: Reasoning Architectures

Picture an agent asked to fix a failing test. Before editing a file, it reads the error, recalls what the module does, and sketches two candidate causes. All of that happens inside the agent, and this chapter is about those inner steps.

## Reasoning as an Interpreter, Not a Mood

This chapter treats reasoning systems as interpreters. An *interpreter* is a program that repeatedly reads a state and takes one legal step. Here the loop runs over thought, memory, action, and critique.

Chapter 1 gave us the basic agent machine, in five moves:

1. Observe the world.
2. Update belief, meaning the agent's current best account of hidden facts.
3. Choose a governed action, meaning one allowed by its constraints.
4. Execute it.
5. Learn from the result.

Chapter 2 adds a new layer inside that machine: a reasoning interpreter that can spend controlled internal steps before touching the outside world. Internal steps cost time and tokens, so budget them.

That layer changes the question. Instead of asking only "what should the agent do next?", we now ask "what legal thinking, planning, remembering, and self-checking steps may the agent run before it acts?"

## The Running Example, and the Four Things It Learns to Do

The running example is the same practical creature in a more elaborate costume: a coding or research agent trying to complete a task without inventing evidence, exceeding budget, or confusing a wish with a dependency. Wanting a library to export a function does not make the export exist.

Across this chapter, that agent will do four things:

- Reason as a transition system, meaning states plus rules for legal moves between them.
- Plan by searching through possible interpreter states.
- Retrieve memory as an action with cost and risk, not as a free lookup.
- Debug itself by inspecting whole traces rather than final answers alone.

## These Parts Are Options, Not a Mandatory Parade

Planning, memory, retrieval, and reflection should not be read as a royal procession of stages that every agent must always march through. They are alternative modifications to the same machine.

Consider three tasks. One may need a deeper search horizon, meaning it looks further ahead. Another may need a stricter memory policy. A third may need reflection after a failed tool call, and no reflection at all before a trivial answer.

The useful question is not "did we add all the fashionable organs?" but which change to state, control flow, feedback, memory, authority, or stopping condition improves *this* task enough to justify its cost. Sometimes none do.

## Topics

1. [Reasoning Loops as Interpreters](topic-01-reasoning-loops-as-interpreters.md)
2. [Deliberation, Planning, and Search](topic-02-deliberation-planning-and-search.md)
3. [Memory Systems, Context, and Retrieval](topic-03-memory-systems-context-and-retrieval.md)
4. [Evaluating and Debugging Reasoners](topic-04-evaluating-and-debugging-reasoners.md)
