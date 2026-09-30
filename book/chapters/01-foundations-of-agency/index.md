# Chapter 1: Foundations of Agency

## Part 1: The Single Agent

The Agent-427 of Part 0 could build a book, route through an institution, and help publish a bad citation. The Agent-427 that opens this chapter can do almost nothing. It is switched on with read-only repository access, no durable memory, and no deployment authority. Its first task arrives before it has earned anything more dangerous.

That poverty is deliberate. Part 0 asked why the Integrator did not object; the honest answer is that nobody had ever said, in a form a program could check, what it was for, what it could see, or what it was allowed to believe. Part 1 supplies those answers one at a time, and asks how this single agent survives long enough to become useful. We formalize each addition and then break its assumptions on purpose, so later patterns can be compared without mysticism, marketing fog, or the comforting fiction that production behaves like a theorem.

## One Interpreter, Extended Four Times

The chapter builds one running interpreter—a program that reads a specification and carries it out step by step—and makes it slightly less naive in each topic.

It starts with a contract, because an agent that cannot say what counts as success cannot be caught failing: Topic 1 (Goals, Environments, and Actions) writes down state, observation, action, reward, cost, constraint, and stopping. The contract immediately exposes a problem. Agent-427 never sees the true state of the repository, only file contents and test output that may be stale or wrong. Topic 2 (Belief, Uncertainty, and Decision) therefore gives it a belief: a running estimate of what is probably true, with a price attached to finding out more. Belief brings a new problem, since carrying every clue forever is expensive and brittle, so Topic 3 (World Models and State Abstractions) teaches the interpreter which parts of its history deserve to be kept and which are attic furniture. Only then does Topic 4 (Policies, Value, and Control) let the machine choose: a policy that weighs future consequences, learns from feedback, and stays inside the authority it was given.

Each topic ends the same honest way. We state the assumption that makes the formalism useful, violate it in the most production-like way available, and ask what the interpreter must do when the lovely model and the grubby world cease speaking to each other.

## Topics

1. [Goals, Environments, and Actions](topic-01-goals-environments-actions.md)
2. [Belief, Uncertainty, and Decision](topic-02-belief-uncertainty-and-decision.md)
3. [World Models and State Abstractions](topic-03-world-models-and-state-abstractions.md)
4. [Policies, Value, and Control](topic-04-policies-value-and-control.md)
