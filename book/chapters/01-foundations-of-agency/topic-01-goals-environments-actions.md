# Goals, Environments, and Actions

An agentic system can be defined as a process that maps observations to actions in pursuit of a goal [[2](../../references.md#ref-2)]. The form looks innocent, but this mapping hides assumptions about what the world is, what can be sensed, and what counts as success.

In practical LLM systems, goals often begin as natural language instructions. To engineer them rigorously, we translate instructions into objective functions, constraints, and stopping criteria [[1](../../references.md#ref-1)] [[3](../../references.md#ref-3)].

Environment modeling is where toy demos become science: open-loop prompting assumes a frozen world, while real agents operate in partially observable, changing environments [[7](../../references.md#ref-7)]. Actions then become interventions that alter future observations, not just outputs for a log file.

## Minimal formal sketch

| Symbol | Meaning |
|---|---|
| \(s_t\) | latent world state |
| \(o_t\) | observation at time \(t\) |
| \(a_t\) | action chosen at time \(t\) |
| \(G\) | goal/objective functional |

The engineering principle is to keep this sketch explicit in code and docs, so architecture decisions can be audited against a shared formal target.
