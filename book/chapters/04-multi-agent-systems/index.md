# Chapter 4: Multi-Agent Systems

When one agent is uncertain, we consult evidence. When many agents are uncertain, we need institutions.

Chapter 1 built a single interpreter: observe the environment, update state,
choose an action, execute it, and loop. This chapter adds one more layer around
that interpreter. Now several such machines run at once, each with its own
partial state, budget, memory, and authority, while all of them affect a shared
world. This is the decisive test of composition. Benefits that looked additive
in isolation stop being additive once interpreters share state, cost, authority,
latency, and incentives. The new layer is therefore not "more prompting." It is
an institutional evaluator: protocols decide who may speak, mechanisms decide
how scarce authority is allocated, learning dynamics reveal which conventions
survive adaptation, and ensembles decide when disagreement is useful evidence
rather than noise.

The running example is the publication workflow itself. A drafter proposes text, a fact checker tests claims, an integrator commits patches, and a router decides which interpreter should see the next fragment of work. The shared document becomes the common heap; the audit log becomes the continuation; messages, votes, bids, critiques, and commits become the visible transitions by which many local evaluators simulate one larger, stranger program.

## Topics

1. [Coordination Protocols and Communication](topic-01-coordination-protocols-and-communication.md)
2. [Negotiation and Mechanism Design](topic-02-negotiation-and-mechanism-design.md)
3. [Equilibria, Self-Play, and Learning Dynamics](topic-03-equilibria-self-play-and-learning-dynamics.md)
4. [Neural Ensembles and Orchestration](topic-04-neural-ensembles-and-orchestration.md)
