# Safety Constraints and Guardrails

Safety is not a postscript to capability; it is constrained optimization from first principles.

## Constrained control formalization

Model policy selection as a constrained MDP:
\[
\max_{\pi}\ J_R(\pi)=\mathbb{E}_\pi\!\left[\sum_t\gamma^t r_t\right]
\quad\text{s.t.}\quad
J_{C_j}(\pi)=\mathbb{E}_\pi\!\left[\sum_t\gamma^t c_{j,t}\right]\le d_j.
\]
The Lagrangian form
\[
\mathcal{L}(\pi,\lambda)=J_R(\pi)-\sum_j\lambda_j\big(J_{C_j}(\pi)-d_j\big)
\]
supports dual optimization and transparent trade-off tuning.

## Three-theory braid

1. **Constrained MDP theory.** Utility-safety trade-offs become explicit and optimizable [[51](../../references.md#ref-51)].
2. **Control barrier functions (CBFs).** Safety can be imposed as forward-invariance constraints \(h(x)\ge0\) at runtime [[52](../../references.md#ref-52)].
3. **Normative governance frameworks.** Constitutional and risk-management frameworks encode institution-level constraints beyond model internals [[29](../../references.md#ref-29)] [[53](../../references.md#ref-53)].

## How to study this formally

Report Pareto fronts of task return versus violation probability, plus time-to-escalation under unsafe trajectories. Layered guardrails should be tested for correlated failure modes, not in isolation. Constraint-aware autonomy is not anti-innovation; it is innovation that survives contact with reality.
