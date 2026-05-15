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

## Translating the Theory into Agentic Practice

Planning theory tells us when an agent should spend computation imagining futures and when it should stop admiring its own imagination and act. In a practical agent, deliberation depth should be a controlled resource. The system should choose between direct action, shallow lookahead, full task decomposition, tool-assisted simulation, or human clarification according to expected utility and cost. A planner that always thinks is slow; a planner that never thinks is merely quick to be wrong.

For implementation, represent plans as explicit candidate trajectories: state estimate, proposed action, expected observation, cost, risk, and contingency. Use heuristics to prioritize branches, but record why a branch was pruned. Use symbolic preconditions for irreversible or expensive actions. Use search when the task has combinatorial structure, such as multi-file refactoring, multi-step data cleaning, deployment sequencing, or negotiation. Use receding-horizon control when the world will answer back after each move, as most worlds impolitely do.

The theory also clarifies the role of decomposition in LLM agents. A task breakdown is not valuable because it looks organized; it is valuable when it reduces branching factor, exposes dependencies, or creates intermediate states that can be verified. "Plan then execute" is weak if the plan cannot absorb new observations. "Plan, execute one step, observe, replan" is stronger because it treats the plan as a living hypothesis rather than a stone tablet.

To design better agents, give the planner a search budget, a heuristic, a fallback, and a replan trigger. Teach it to price computation, detect dead ends, and prefer reversible exploration before irreversible commitment. The theory of search is valuable because it rescues agents from both extremes: the tiny tyranny of next-token reflex and the imperial sprawl of infinite deliberation. Competent agency lives in the treaty between foresight and budget.
