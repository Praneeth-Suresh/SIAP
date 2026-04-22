# Evaluating and Debugging Reasoners

An agent that seems eloquent may still be strategically inept. Evaluation must target trajectories, not just final text outputs [[30](../../references.md#ref-30)].

Reasoning QA should include:
1. success rate on goal completion,
2. tool-use correctness,
3. calibration under uncertainty,
4. failure recoverability.

Trace-based diagnostics are especially valuable: each loop iteration is an observable state transition that can be inspected, replayed, and scored [[24](../../references.md#ref-24)].

The practical doctrine is harsh and useful: if you cannot replay and score a reasoning path, you are optimizing anecdotes.
