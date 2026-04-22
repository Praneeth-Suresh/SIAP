# Safety Constraints and Guardrails

Agent safety is best modeled as constrained optimization: maximize utility subject to policy and risk constraints [[29](../../references.md#ref-29)] [[30](../../references.md#ref-30)].

Guardrails should exist at multiple layers:
1. prompt-level behavioral constraints,
2. tool-level argument validation,
3. runtime-level permission and budget controls,
4. human escalation paths.

This layered design reduces single-point safety failure and aligns with the principle that oversight should be external to the model’s own narrative confidence.

Constraint-aware orchestration is not anti-autonomy; it is the precondition for trustworthy autonomy.
