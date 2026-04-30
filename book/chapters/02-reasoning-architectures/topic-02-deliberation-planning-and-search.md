# Deliberation, Planning, and Search

Deliberation is the art of paying for imagination before reality charges interest. Planning and search are how an agent buys that imagination without going computationally bankrupt.

## Planning as structured foresight

Let \(G=(V,E)\) be a search graph over decision states. A deterministic plan is a path \(p=(v_0,\dots,v_T)\) minimizing
\[
J(p)=\sum_{t=0}^{T-1} c(v_t,v_{t+1}) + \Phi(v_T),
\]
and A* prioritizes candidates by
\[
f(n)=g(n)+h(n),
\]
where admissibility \(h(n)\le h^\star(n)\) (and consistency when available) gives shortest-path guarantees [[8](../../references.md#ref-8)]. In symbolic planning, actions are model primitives with preconditions and effects:
\[
s_{t+1}=(s_t\setminus \mathrm{Del}(a_t))\cup \mathrm{Add}(a_t),\qquad \mathrm{Pre}(a_t)\subseteq s_t,
\]
which turns "reasoning" into explicit world-state transformation [[9](../../references.md#ref-9)] [[10](../../references.md#ref-10)].

## Uncertainty-aware planning and search control

Expected-utility foundations provide the selection compass:
\[
a_t^\star=\arg\max_a \mathbb{E}[U(a,S_t)\mid h_t],
\]
so planning depth is justified only when it increases downstream utility enough to beat its own compute cost [[33](../../references.md#ref-33)] [[34](../../references.md#ref-34)]. In stochastic settings this becomes Bellman recursion,
\[
V^\star(s)=\max_a\left\{R(s,a)+\gamma\sum_{s'}P(s'|s,a)V^\star(s')\right\},
\]
or belief-space variants for partial observability [[5](../../references.md#ref-5)] [[4](../../references.md#ref-4)] [[7](../../references.md#ref-7)].

When the horizon explodes, Monte Carlo tree search allocates rollouts by optimism:
\[
a^\star=\arg\max_a\left(Q(s,a)+c\sqrt{\frac{\ln N(s)}{N(s,a)}}\right),
\]
balancing exploitation and exploration under finite time [[45](../../references.md#ref-45)]. Receding-horizon control then executes only the first action of an \(H\)-step solve,
\[
u_t=\arg\min_{u_{t:t+H-1}} \sum_{k=0}^{H-1}\ell(x_{t+k},u_{t+k})+\ell_f(x_{t+H}),
\]
and replans at the next step, converting brittle open-loop plans into responsive closed-loop behavior [[41](../../references.md#ref-41)].

## Three-theory braid

Heuristic graph search gives an efficient map of plausible futures through \(f=g+h\), symbolic planning gives compositional world mechanics through precondition-effect algebra, and anytime/tree-search control gives temporal humility by improving solutions as long as budget remains, so intelligence appears as a braid of foresight (explicit lookahead), responsiveness (replanning under new observations), and resilience (graceful degradation when depth, branching factor, and latency constraints collide) [[8](../../references.md#ref-8)] [[9](../../references.md#ref-9)] [[44](../../references.md#ref-44)] [[45](../../references.md#ref-45)].

## How to study this formally

Benchmark plan utility against compute budget, replan frequency, and irreversible-error rate; report performance as a function of \(H\), branching factor \(b\), and heuristic misspecification. The best planner is not the one with the fanciest search tree; it is the one that still behaves coherently when its assumptions are wrong.
