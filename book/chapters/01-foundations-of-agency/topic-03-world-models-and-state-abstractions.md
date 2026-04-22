# World Models and State Abstractions

An agent that stores everything stores nothing usefully. State abstraction decides what history is compressed into a control-relevant representation [[2](../../references.md#ref-2)] [[4](../../references.md#ref-4)].

In modern LLM stacks, this appears as schema design: what lives in short-term context, long-term memory, vector stores, and external structured state [[16](../../references.md#ref-16)]. The abstraction boundary determines whether plans can be reused or must be reinvented each turn.

Causal structure matters. If a model cannot distinguish correlation from intervention, it plans with confidence and acts with confusion [[6](../../references.md#ref-6)]. Effective abstractions preserve variables that support counterfactual reasoning and tool selection.

A good chapter-level heuristic: each state field should answer either “what matters for next action?” or “what matters for post-hoc accountability?”
