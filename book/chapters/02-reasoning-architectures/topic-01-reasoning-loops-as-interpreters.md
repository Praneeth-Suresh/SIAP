# Reasoning Loops as Interpreters

A modern agent loop resembles a small interpreter: parse context, evaluate candidate actions, execute one, update state, repeat [[1](../../references.md#ref-1)] [[11](../../references.md#ref-11)].

The key move is to make loop semantics explicit. Which variables are mutable? Which transitions are legal? Which errors are recoverable? Without these declarations, “autonomy” degenerates into optimistic recursion.

The interpreter lens also makes compositionality tractable. We can define loop combinators (plan-then-act, act-then-reflect, branch-and-vote) and reason about their invariants, costs, and failure modes [[2](../../references.md#ref-2)].

In this framing, prompt text is only one layer. The loop itself is the machine.
