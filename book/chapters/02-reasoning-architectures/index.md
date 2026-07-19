# Chapter 2: Reasoning Architectures

This chapter treats reasoning systems as interpreters: they execute loops over thought, memory, action, and critique.

Chapter 1 gave us the basic agent machine: observe the world, update belief, choose a governed action, execute it, and learn from the result. Chapter 2 adds a new layer inside that machine: a reasoning interpreter that can spend controlled internal steps before touching the outside world. Instead of asking only "what should the agent do next?", we now ask "what legal thinking, planning, remembering, and self-checking steps may the agent run before it acts?"

The running example is the same practical creature in a more elaborate costume: a coding or research agent trying to complete a task without inventing evidence, exceeding budget, or confusing a wish with a dependency. It will reason as a transition system, plan by searching through possible interpreter states, retrieve memory as an action with cost and risk, and debug itself by inspecting whole traces rather than final answers alone.

Planning, memory, retrieval, and reflection should not be read as a royal procession of stages that every agent must always march through. They are alternative modifications to the same machine. One task may need a deeper search horizon; another may need a stricter memory policy; a third may need reflection after a failed tool call and no reflection at all before a trivial answer. The useful question is not "did we add all the fashionable organs?", but which change to state, control flow, feedback, authority, or termination improves this task enough to justify its cost.

## Topics

1. [Reasoning Loops as Interpreters](topic-01-reasoning-loops-as-interpreters.md)
2. [Deliberation, Planning, and Search](topic-02-deliberation-planning-and-search.md)
3. [Memory Systems, Context, and Retrieval](topic-03-memory-systems-context-and-retrieval.md)
4. [Evaluating and Debugging Reasoners](topic-04-evaluating-and-debugging-reasoners.md)
