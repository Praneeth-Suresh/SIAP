# Equilibria, Self-Play, and Learning Dynamics

Equilibrium is the grammar of strategic stability: who can deviate, who gains, and when dynamics settle or cycle.

## Formal game model

In a normal-form game \((N,\{A_i\},\{u_i\})\), mixed strategy profile \(\sigma^{*}\) is Nash if
\[
u_i(\sigma_i^{*},\sigma_{-i}^{*}) \ge u_i(\sigma_i,\sigma_{-i}^{*})\quad \forall i,\forall \sigma_i.
\]
For sequential interaction, Markov games extend MDPs with multi-agent action tuples and payoff vectors.

## Three-theory braid

1. **Nash equilibrium analysis.** Fixed points characterize unilateral stability and expose incentive misalignment [[19](../../references.md#ref-19)].
2. **Self-play in Markov games.** Repeated interaction drives policy co-adaptation and emergent conventions [[20](../../references.md#ref-20)] [[21](../../references.md#ref-21)].
3. **Learning dynamics.** Fictitious play and no-regret dynamics explain convergence to correlated/coarse-correlated equilibria in repeated games [[65](../../references.md#ref-65)] [[64](../../references.md#ref-64)] [[63](../../references.md#ref-63)].

## How to study this formally

Track exploitability, diversity collapse, and equilibrium selection under perturbation. Evaluate whether local agent improvements increase system-level welfare or merely shift failure to other roles. If strategic dynamics are ignored, “multi-agent” is just parallel monologue.
