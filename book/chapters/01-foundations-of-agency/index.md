# Chapter 1: Foundations of Agency

A thermostat holds a room at 21 degrees Celsius. It reads a sensor, then switches a heater on or off. That is already agency in miniature: a goal, an environment, and an action. Agency begins with that deceptively simple triad of **goals**, **environments**, and **actions**. We formalize it here, then progressively add uncertainty, representation, and control, so that later patterns can be compared without mysticism or marketing fog.

## One Interpreter, Extended Four Times

We build one running interpreter: a program that reads a specification and carries it out step by step. Each topic adds one layer to that interpreter, and one word to our vocabulary of comparison.

Topic 1 (Goals, Environments, and Actions) gives the loop a contract. It says what counts as state, observation, action, reward, cost, constraint, and stopping.

Topic 2 (Belief, Uncertainty, and Decision) adds belief. A thermostat's sensor can drift or lie. Belief lets the interpreter act when it does not know the true state.

Topic 3 (World Models and State Abstractions) adds representation, through state abstraction. The interpreter learns to carry the useful part of its history, without dragging the whole attic downstairs.

Topic 4 (Policies, Value, and Control) adds policy, feedback, authority, and control. Single choices become governed action.

## Topics

1. [Goals, Environments, and Actions](topic-01-goals-environments-actions.md)
2. [Belief, Uncertainty, and Decision](topic-02-belief-uncertainty-and-decision.md)
3. [World Models and State Abstractions](topic-03-world-models-and-state-abstractions.md)
4. [Policies, Value, and Control](topic-04-policies-value-and-control.md)
