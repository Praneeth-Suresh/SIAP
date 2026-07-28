# Chapter 4: Multi-Agent Systems

When one agent is uncertain, we consult evidence. When many agents are uncertain, we need institutions.

This chapter is about several agents working at once on one task. One agent is a program. Many agents are a small society, and societies need rules.

## From One Interpreter to Many

Chapter 1 built a single interpreter. It observes the environment, updates state, chooses an action, executes it, and loops. This chapter adds one more layer around that interpreter. Now several such machines run at once. Each has its own partial state, meaning it sees only a slice of the world. Each has its own budget, its own memory, and its own authority. Yet all of them affect one shared world.

## Why Benefits Stop Adding Up

This is the decisive test of composition. Two agents look like twice the capability. Say one agent alone finishes 6 tasks an hour. Two rarely finish 12, because they now queue behind the same file lock and the same rate limit. Benefits that looked additive in isolation stop being additive once interpreters share state, cost, authority, latency, and incentives.

The new layer is therefore not "more prompting." It is an institutional evaluator: an evaluator that runs the rules of a group rather than the steps of one agent. Four kinds of rules do that work:

- Protocols decide who may speak.
- Mechanisms decide how scarce authority is allocated.
- Learning dynamics reveal which conventions survive adaptation.
- Ensembles decide when disagreement is useful evidence rather than noise.

## The Running Example: This Book's Publication Workflow

The running example is the publication workflow itself. A drafter proposes text. A fact checker tests claims. An integrator commits patches. A router decides which interpreter should see the next fragment of work.

The shared document becomes the common heap, the one store every agent may touch. The audit log becomes the continuation, the record of what still must happen. Messages, votes, bids, critiques, and commits become the visible transitions. By them, many local evaluators simulate one larger, stranger program.

## Topics

1. [Coordination Protocols and Communication](topic-01-coordination-protocols-and-communication.md)
2. [Negotiation and Mechanism Design](topic-02-negotiation-and-mechanism-design.md)
3. [Equilibria, Self-Play, and Learning Dynamics](topic-03-equilibria-self-play-and-learning-dynamics.md)
4. [Neural Ensembles and Orchestration](topic-04-neural-ensembles-and-orchestration.md)
