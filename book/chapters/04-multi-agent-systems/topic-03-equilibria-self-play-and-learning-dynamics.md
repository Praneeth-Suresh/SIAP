# Equilibria, Self-Play, and Learning Dynamics

Equilibrium is the grammar of strategic stability: who can deviate, who gains, and when dynamics settle or cycle.

## Formal game model

In a normal-form game \((N,\{A_i\},\{u_i\})\), mixed strategy profile \(\sigma^{*}\) is Nash if
\[
u_i(\sigma_i^{*},\sigma_{-i}^{*}) \ge u_i(\sigma_i,\sigma_{-i}^{*})\quad \forall i,\forall \sigma_i.
\]
For sequential interaction, Markov games extend MDPs with multi-agent action tuples and payoff vectors.

A useful robustness metric is exploitability:
\[
\mathcal{E}(\sigma)=\sum_i\left(\max_{\sigma_i'}u_i(\sigma_i',\sigma_{-i})-u_i(\sigma)\right),
\]
which is zero only at exact equilibrium in two-player zero-sum settings.

Repeated adaptation is governed by regret:
\[
R_T^i=\max_a\sum_{t=1}^T u_i(a,a_{-i}^t)-\sum_{t=1}^T u_i(a_i^t,a_{-i}^t),
\]
and no-regret learning drives empirical play toward correlated equilibrium sets.

## Sequential strategic control

For Markov games, value recursion for player \(i\) under profile \(\pi\) is
\[
V_i^\pi(s)=\mathbb{E}_{a\sim \pi}\!\left[r_i(s,a)+\gamma\sum_{s'}P(s'|s,a)V_i^\pi(s')\right],
\]
with equilibrium planning replacing unilateral maximization by strategic best-response consistency [[20](../../references.md#ref-20)] [[5](../../references.md#ref-5)].

## Three-theory braid

Nash equilibrium analysis gives fixed-point notions of unilateral stability, self-play in Markov games gives the adaptive process by which policies co-evolve under repeated interaction, and learning-dynamics tools like fictitious play and no-regret updates characterize when trajectories converge, cycle, or fragment, so multi-agent intelligence appears as a braid of foresight (optimize expected utility against strategic responses), responsiveness (update policies from observed opponent behavior), and resilience (maintain low exploitability and bounded regret under perturbations) [[19](../../references.md#ref-19)] [[20](../../references.md#ref-20)] [[21](../../references.md#ref-21)] [[63](../../references.md#ref-63)] [[64](../../references.md#ref-64)] [[65](../../references.md#ref-65)] [[33](../../references.md#ref-33)] [[34](../../references.md#ref-34)].

## How to study this formally

Track exploitability, regret curves, diversity collapse, and equilibrium selection stability under perturbation. If strategic dynamics are ignored, "multi-agent" is just parallel monologue.
