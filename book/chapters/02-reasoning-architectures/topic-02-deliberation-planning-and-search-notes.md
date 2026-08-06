# Notes: Deliberation, Planning, and Search

## What to improve

- Add one side-by-side case study: symbolic planner vs reactive loop.
- Introduce planning horizon and branching factor estimates.
- Clarify when search depth should be budget-capped.

## Alternative rewrite

Deliberation is a wager against greediness. Planning says, “I refuse to be seduced by the next attractive token; show me the downstream consequences.” Search then operationalizes humility: inspect alternatives before committing reality to one.

## Pass 1 - Migrated ideas from current main topic

The current topic defines planning as path optimization over a search graph \(G=(V,E)\) with objective \(J(p)=\sum_t c(v_t,v_{t+1})+\Phi(v_T)\), highlights admissible heuristics \(h(v)\le h^\star(v)\) for A* guarantees, and expands to stochastic settings through belief-space planning and MCTS rollouts. The existing braid combines heuristic graph search, STRIPS-style symbolic planning, and anytime/tree-search control under real-time compute limits [[8](../../references.md#ref-8)] [[9](../../references.md#ref-9)] [[10](../../references.md#ref-10)] [[44](../../references.md#ref-44)] [[45](../../references.md#ref-45)].

## Pass 1 - Storyline outline (paragraph-by-paragraph)

Paragraph 1 starts at an intellectual crossroads: the reactive agent wants the next token now, while the planner asks what that token commits us to five moves later.

Paragraph 2 develops planning as explicit state-space imagination, introducing horizon \(H\), branching factor \(b\), and the painful economics of combinatorial growth.

Paragraph 3 introduces expected utility as the criterion that converts "many possible futures" into a ranked set of plans under uncertainty [[33](../../references.md#ref-33)] [[34](../../references.md#ref-34)].

Paragraph 4 braids symbolic operators, heuristic search, and Monte Carlo control as complementary instruments: structure for correctness, heuristics for speed, and sampling for volatility [[9](../../references.md#ref-9)] [[45](../../references.md#ref-45)].

Paragraph 5 closes with graceful degradation: anytime planning and receding-horizon control ensure the system can still act coherently when the clock, budget, or world model is against it [[44](../../references.md#ref-44)] [[41](../../references.md#ref-41)].

## Pass 2 - Research synthesis: equations, theories, and connective tissue

Equation set to emphasize: A* priority \(f(n)=g(n)+h(n)\) with admissibility \(h(n)\le h^\star(n)\) and consistency \(h(n)\le c(n,n')+h(n')\) for optimality/efficiency claims [[8](../../references.md#ref-8)]; deterministic planning objective \(p^\star=\arg\min_p\sum_t c(s_t,a_t)\) with STRIPS transition \(s_{t+1}=(s_t\setminus \text{Del}(a_t))\cup \text{Add}(a_t)\) under precondition \(Pre(a_t)\subseteq s_t\) [[9](../../references.md#ref-9)] [[10](../../references.md#ref-10)]; stochastic control by Bellman recursion \(V^\star(s)=\max_a\{R(s,a)+\gamma\sum_{s'}P(s'|s,a)V^\star(s')\}\) and belief-space analogue for partial observability [[5](../../references.md#ref-5)] [[4](../../references.md#ref-4)] [[7](../../references.md#ref-7)]; MCTS selection via UCT \(a^\star=\arg\max_a \left(Q(s,a)+c\sqrt{\frac{\ln N(s)}{N(s,a)}}\right)\) as exploration-exploitation tradeoff [[45](../../references.md#ref-45)]; and receding-horizon control \(u_t=\arg\min_{u_{t:t+H-1}}\sum_{k=0}^{H-1}\ell(x_{t+k},u_{t+k})+\ell_f(x_{t+H})\) executed in feedback at each step [[41](../../references.md#ref-41)]. The narrative connection: symbolic models define what can happen, search estimates what is promising, and control laws keep action stable when plans meet reality.

## Additional alternate approaches for this rewrite

1. Use a mountaineering metaphor: heuristics estimate altitude, planners map routes, and anytime search decides when to climb now versus scout more.
2. Center the topic on one warehouse-robot case where symbolic plans, A*, and MCTS are compared under increasing uncertainty.
3. Tell it as a duel between "greedy now" and "strategic later," with equations as arbitration.
4. Build the exposition around budget clocks, showing how each planning method spends seconds and buys down regret.

## Editor-Rewrite Alternative Before Primary Synthesis

Make Agent-427's first plan fail because time passes. At 3:47:18 the agent plans against API version 2; at 3:47:51 the service rolls to version 3; at 3:48:07 the agent faithfully executes a now-obsolete step and oscillates between two incompatible repairs. Use the trace to distinguish a plan from a prophecy. Retain graph search, A*, symbolic preconditions, expected utility, Bellman recursion, MCTS, and receding-horizon control, then put `The Assumption`, `The Violation`, and `When It Fails` around the stationary-model bargain. The exercise should require a runnable planner, a changing environment, logged replans, and a measured failure rate rather than a prose itinerary.
