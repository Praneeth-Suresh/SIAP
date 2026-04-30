# Safety Constraints and Guardrails

Safety is not a postscript to capability; it is optimization with explicit boundaries, encoded before the first tool call is ever allowed.

## Constrained control formulation

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

At state-action level, constrained Bellman structure appears as
\[
Q^\pi_\lambda(s,a)=r(s,a)-\sum_j\lambda_j c_j(s,a)+\gamma\,\mathbb{E}_{s'}[V^\pi_\lambda(s')],
\]
which makes "unsafe but high reward" mathematically explicit instead of politically vague.

## Runtime safety filter

Define safe set \(\mathcal{C}=\{x:h(x)\ge0\}\). Control barrier functions require
\[
\dot h(x,u)+\alpha(h(x))\ge0
\]
for class-\(\mathcal{K}\) function \(\alpha\), giving forward invariance of \(\mathcal{C}\) [[52](../../references.md#ref-52)]. A practical filter solves
\[
u^\star=\arg\min_u \|u-u_{\text{nom}}\|^2
\quad\text{s.t.}\quad
\dot h(x,u)+\alpha(h(x))\ge0,
\]
so nominal autonomy is preserved when safe and corrected when not.

## Three-theory braid

Constrained MDP theory gives the expected-utility compass with explicit harm budgets, control barrier functions give a feedback law that enforces state-space invariants online, and governance frameworks translate organizational risk appetite into operational policy envelopes, so safety becomes a braided architecture of foresight (optimize return while pricing risk), responsiveness (intervene at runtime through CBF-constrained control), and resilience (institutional constraints that persist beyond any single prompt or model version) [[51](../../references.md#ref-51)] [[52](../../references.md#ref-52)] [[29](../../references.md#ref-29)] [[53](../../references.md#ref-53)] [[33](../../references.md#ref-33)] [[34](../../references.md#ref-34)].

## How to study this formally

Report Pareto fronts of task return versus violation probability, dual-variable stability, and time-to-escalation under unsafe trajectories. Stress layered guardrails under correlated failures rather than isolated tests. Constraint-aware autonomy is not anti-innovation; it is innovation that survives contact with reality.
