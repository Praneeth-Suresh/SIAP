# World Models and State Abstractions

To model a world is to choose what to forget without forgetting what matters. Abstraction is compression under decision pressure.

## Formalization

Let \(\phi:\mathcal{S}\to\mathcal{Z}\) map ground states to abstract states. A homomorphic abstraction preserves control-relevant structure:
\[
R(s,a)=\bar{R}(\phi(s),a),\qquad
\sum_{s':\phi(s')=z'} T(s'\mid s,a)=\bar{T}(z'\mid \phi(s),a).
\]
Then planning in \(\mathcal{Z}\) approximates planning in \(\mathcal{S}\), with error bounded by abstraction distortion.

For causal world models, variables \(X\) follow structural equations \(X_i=f_i(\mathrm{Pa}(X_i),U_i)\). Interventions \(\mathrm{do}(X_j=x)\) define action semantics beyond passive prediction [[6](../../references.md#ref-6)].

## Three-theory braid

1. **State abstraction in MDPs.** Homomorphisms characterize when compressed states retain optimal-control content [[37](../../references.md#ref-37)].
2. **Bisimulation metrics.** Behavioral similarity can be quantified continuously, giving principled abstraction error control [[38](../../references.md#ref-38)].
3. **Causal modeling.** Structural causal models distinguish observation from intervention, crucial for tool-using agents that change their environment [[6](../../references.md#ref-6)].

## How to study this formally

Estimate value-loss \(\Delta V = \|V^{*} - \tilde{V}^{*}\circ\phi\|\), intervention accuracy under held-out counterfactuals, and policy robustness to distribution shift. In short: if abstraction gains speed but loses action relevance, you have invented a beautifully efficient hallucination engine.
