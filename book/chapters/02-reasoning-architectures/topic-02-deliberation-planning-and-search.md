# Deliberation, Planning, and Search

Deliberation is the art of spending computation now to avoid regret later.

## Formal planning frame

Let \(G=(V,E)\) be a search graph over decision states. A plan is a path \(p=(v_0,\dots,v_T)\) minimizing
\[
J(p)=\sum_{t=0}^{T-1} c(v_t,v_{t+1}) + \Phi(v_T),
\]
with admissible heuristic \(h(v)\le h^{*}(v)\) for A* optimality.

In stochastic domains, planning becomes belief-space optimization or Monte Carlo tree search over sampled rollouts.

## Three-theory braid

1. **Heuristic graph search.** A* gives optimality guarantees under admissibility/consistency assumptions [[8](../../references.md#ref-8)].
2. **Symbolic planning.** STRIPS-style operators and planning-domain models encode action preconditions/effects for compositional plan construction [[9](../../references.md#ref-9)] [[10](../../references.md#ref-10)].
3. **Anytime and tree-search control.** UCT/MCTS and anytime planning trade compute for solution quality under real-time budgets [[44](../../references.md#ref-44)] [[45](../../references.md#ref-45)].

## How to study this formally

Benchmark plan quality against compute budget, replan frequency, and irreversible-error rate. Analyze sensitivity to heuristic misspecification and environment volatility. The best planner is not the one with the fanciest tree; it is the one whose assumptions fail gracefully.
