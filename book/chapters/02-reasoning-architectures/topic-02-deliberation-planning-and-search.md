# Deliberation, Planning, and Search

Imagine an agent that has just received a bug report. It can act at once, or it can first imagine two or three futures. This section is about that second option. Deliberation means spending part of the budget simulating steps before committing to one. Planning and search buy that foresight without pretending computation is free.

The interpreter from the previous topic, Reasoning Loops as Interpreters, executes one legal step at a time. Deliberation asks a sharper question: should the agent look ahead before choosing that step?

## A Proposal Says "Try This"; A Plan Says "And Then What"

A proposal says, "try this next action." A plan embeds the same action inside an imagined trajectory, and states five further things:

- what state should follow the action;
- what evidence should appear if the plan is on track;
- what cost will be paid;
- what constraint might bind, that is, which limit could stop the plan;
- what fallback remains if the world disagrees.

Search is the procedure that compares such trajectories under limited time, a comparison shop for imagined futures, closing when the clock stops.

## Plans as Paths Through Interpreter States

Draw the choices as a graph. Let \(G=(V,E)\) be a search graph whose vertices are decision states. Read \(V\) as the states the agent could occupy, and \(E\) as the legal moves between them.

A deterministic plan is then a path \(p=(v_0,\dots,v_T)\) through that graph, from the current state \(v_0\) to \(v_T\) after \(T\) steps. The planner wants the cheapest such path, minimizing

\[
J(p)=\sum_{t=0}^{T-1} c(v_t,v_{t+1}) + \Phi(v_T).
\]

Read \(J(p)\) as "total cost of plan \(p\)". The sum prices every move, since \(c(v_t,v_{t+1})\) is one step's cost in tokens, time, or money. The term \(\Phi(v_T)\) is a terminal penalty on where the plan leaves the agent: low for a good ending, high for a bad one.

### How A\* Ranks Candidate Nodes

A\* ("A star") is a classic search algorithm choosing which node to examine next. It prioritizes candidate nodes by

\[
f(n)=g(n)+h(n),
\]

where admissibility \(h(n)\le h^\star(n)\) gives shortest-path guarantees when the graph assumptions hold [[8](../../references.md#ref-8)]. In the agent interpreter, \(g\) accounts for already-spent cost and \(h\) estimates the remaining cost to reach an acceptable halt state.

The three letters are intentionally humble.

1. \(g(n)\) is the cost already paid to reach node \(n\): history, and not negotiable.
2. \(h(n)\) is a heuristic estimate, a cheap guess replacing expensive calculation, of the cost still required from \(n\) to a goal.
3. \(f(n)\) is their sum, the planner's current guess at total path cost through \(n\).

A heuristic is admissible when it never overestimates the true remaining cost \(h^\star(n)\), read "h-star of n": the real cheapest cost from \(n\) to a goal. An admissible heuristic may be naive, but it must not be boastful. To check yours, take nodes whose true cost you know and confirm the estimate is never larger.

### A Two-Branch Example with Numbers You Can Check

For a tiny graph, suppose \(v_0\) is "bug report received." From it the agent can inspect logs and reach \(A\), or inspect the recent diff and reach \(B\).

The path to \(A\) has already cost \(g(A)=2\), and the heuristic says \(h(A)=5\), so \(f(A)=7\). The path to \(B\) has already cost \(g(B)=4\), and the heuristic says \(h(B)=1\), so \(f(B)=5\).

A\* expands \(B\) first, not because inspecting diffs is morally superior, but because the combined arithmetic says that route currently looks cheaper; \(B\) started out more expensive, and the estimate of what remains tipped it.

The branching factor is the number of successor choices the search faces at each node. Reducing it from ten plausible actions to three well-typed actions can turn a hopeless thicket into a walkable garden path.

## Preconditions and Effects: Planning as Set Editing

Symbolic planning makes the transition model explicit. "Symbolic" here means the state is a set of named facts, not an opaque blob of text. An action is legal only when its preconditions are present, and its effects transform the state:

\[
s_{t+1}=(s_t\mathbin{\backslash}\mathrm{Del}(a_t))\cup \mathrm{Add}(a_t),\qquad \mathrm{Pre}(a_t)\subseteq s_t.
\]

Read the first equation as "next state = current state, minus deleted facts, plus added ones." Read \(\mathrm{Pre}(a_t)\subseteq s_t\) as "the action's preconditions must all be facts of the current state."

This is not limited to toy blocks-world domains, the tabletop puzzles of planning textbooks. A coding agent's `run_tests` action may require a clean dependency environment; a `deploy` action may require passing tests, approval, and rollback instructions. Preconditions prevent the planner from treating hope as an executable dependency [[9](../../references.md#ref-9)] [[10](../../references.md#ref-10)].

Decode the notation as set editing.

- \(\mathrm{Pre}(a)\) is the set of facts that must already be true before action \(a\) may run.
- \(\mathrm{Add}(a)\) is the set of facts made true afterward.
- \(\mathrm{Del}(a)\) is the set of facts removed afterward.

For `run_tests`, one toy model might be

\[
\mathrm{Pre}(\texttt{run\_tests})=\{\texttt{deps\_installed},\texttt{worktree\_readable}\},
\]

\[
\mathrm{Add}(\texttt{run\_tests})=\{\texttt{test\_result\_known}\},\qquad
\mathrm{Del}(\texttt{run\_tests})=\{\texttt{test\_result\_stale}\}.
\]

If the current state contains installed dependencies and a readable worktree, the action is legal. Afterward, the planner may rely on a fresh test result and must stop trusting the stale one. The notation is austere because the promise is austere: no premise, no action.

## Choosing When the Future Is Uncertain

Something must then choose among candidates. Expected utility supplies the rule:

\[
a_t^\star=\arg\max_a \mathbb{E}[U(a,S_t)\mid h_t],
\]

read as "choose the action \(a\) with the largest average usefulness \(U\), given the state \(S_t\) and the history \(h_t\) seen so far." A direct consequence follows: additional planning depth is justified only when its expected improvement exceeds its compute and latency costs [[33](../../references.md#ref-33)] [[34](../../references.md#ref-34)]. If another level of lookahead costs two seconds but improves the decision by half a second of value, it is a loss.

In stochastic settings, where the same action can lead to different outcomes, this becomes Bellman recursion,

\[
V^\star(s)=\max_a\left\{R(s,a)+\gamma\sum_{s'}P(s'|s,a)V^\star(s')\right\},
\]

read as "the best achievable value of \(s\) is the best over actions of immediate reward \(R(s,a)\) plus the discounted average value of wherever you land next." Here \(\gamma\) (gamma) is a discount factor between 0 and 1 that shrinks distant outcomes, and \(P(s'|s,a)\) is the chance of landing in \(s'\). The same recursion becomes a belief-space recursion when the state is only partially observed, meaning the agent sees clues rather than the state itself [[5](../../references.md#ref-5)] [[4](../../references.md#ref-4)] [[7](../../references.md#ref-7)].

### Spending Simulations Wisely with Monte Carlo Tree Search

When the branching factor is large, the planner needs search control: a rule for spending limited thinking. Monte Carlo tree search (MCTS) allocates rollouts by optimism:

\[
a^\star=\arg\max_a\left(Q(s,a)+c\sqrt{\frac{\ln N(s)}{N(s,a)}}\right),
\]

balancing exploitation of promising branches with exploration of uncertain ones under finite time [[45](../../references.md#ref-45)]. The formula is a reminder that uncertainty is not merely a defect; it is sometimes a reason to inspect a branch before discarding it.

A rollout is a simulated continuation: the planner imagines acting until a terminal or cutoff state, then uses the result to improve its estimates. Two pressures are traded:

- Exploitation means spending simulations on branches whose current value estimate \(Q(s,a)\) already looks good.
- Exploration means spending some simulations on branches with few visits \(N(s,a)\), because ignorance may be hiding either treasure or calamity.

The square-root term is that exploration bonus, and \(c\) sets how loudly curiosity may speak. It shrinks as one action is tried more often, and grows slowly as the parent state receives more total visits \(N(s)\). A branch tried once in a hundred visits gets a large bonus; after fifty, a small one.

## Replanning After Every Step: Receding Horizons

Long plans are fragile because the world answers back. Model predictive control (MPC) handles this by solving an \(H\)-step problem, where \(H\) is the horizon, the number of steps looked ahead:

\[
\mathbf{u}_{t:t+H-1}^{\star}
=\arg\min_{\mathbf{u}_{t:t+H-1}}
\sum_{k=0}^{H-1}\ell(x_{t+k},u_{t+k})+\ell_f(x_{t+H})
\]

subject to \(x_{k+1}=F(x_k,u_k)\) and \(g(x_k,u_k)\le 0\). Read \(\mathbf{u}\) as the sequence of control actions, \(x\) as the state, \(\ell\) (ell) as the cost of one step, and \(\ell_f\) as the cost of the final state. The first constraint says the state evolves by a known model \(F\); the second collects limits that must never be violated.

The controller applies \(u_t^\star\), the first component of that sequence, observes the new state, and replans at the next step. The corrected control sequence is important: the optimizer reasons over a sequence, while the agent executes only the first action before feedback updates the problem [[41](../../references.md#ref-41)].

For a language-agent planner, the pattern becomes the procedure below: search for candidates, pick the best, check that the first action is legal, execute only that action, and return to the loop.

```text
function RECEDING_HORIZON_STEP(sigma, horizon, budget):
    candidates <- search(sigma, horizon, budget)
    plan <- argmax_expected_utility(candidates)
    a0 <- first_action(plan)

    if not legal(a0, sigma):
        return fallback_or_clarify(sigma)

    sigma_next <- execute(a0, sigma)
    return observe_and_replan(sigma_next)
```

If that first action is illegal in state `sigma`, the agent falls back or asks for clarification.

The plan is a hypothesis about controllable futures, not a contract that reality has signed. This is why "plan then execute" is weak when the execution environment changes, and why "plan, execute one step, observe, replan" is the natural extension of the interpreter built in Chapter 1.

## When Decomposition Actually Improves the Search

Task decomposition means breaking a task into smaller subtasks. It is useful only when it improves the search problem, in one of four ways:

- it may reduce branching factor;
- it may expose prerequisites;
- it may create verifiable intermediate states;
- it may isolate irreversible actions behind stronger checks.

It is not useful merely because it produces a tidy list.

This is the first practical rule of planning: task structure predicts whether planning earns its keep. Planning tends to help in five situations:

1. the horizon is long enough that early choices create or destroy later options;
2. the branching factor is wide enough that unguided next-action choice wastes effort;
3. prerequisites impose a real order;
4. uncertainty must be reduced before commitment;
5. an irreversible action deserves ceremony before the lever is pulled.

A database migration, a multi-file refactor, and a research synthesis with conflicting sources all have enough internal geometry to reward decomposition. A one-line formatting fix usually does not. There, the planning ritual may cost more than the task.

## Reflection Repairs Hard Plans and Taxes Easy Ones

The same lesson governs composition, meaning how planning combines with other patterns. Reflection can repair a difficult plan: after a failed test, the agent can inspect the trace, notice that a prerequisite was imaginary, and revise the frontier before doing more damage. The frontier is the set of nodes the search is still willing to expand.

But reflection also adds latency, consumes tokens, and can induce overthinking on easy tasks. An agent asked to rename a local variable may spend three reflective turns debating architectural intent while the correct edit waits patiently in the file.

Patterns interact; they are not virtues in isolation. Planning plus reflection is powerful when the task contains hidden dependencies or costly mistakes, and ornamental when the task is short, reversible, and already well specified.

## What a Planning Loop Should Record

In practice, each candidate trajectory should record six fields: state estimate, proposed action, expected observation, cost, risk, and contingency, which together make it auditable.

Three commitments follow.

- Heuristics should prioritize branches, but pruning decisions should be logged when they affect safety or correctness.
- Irreversible or expensive actions should be protected by symbolic preconditions, using the \(\mathrm{Pre}\) sets described earlier.
- Replan triggers should be explicit: new evidence, failed precondition, budget drift, tool error, or a value estimate that changes enough to reorder the frontier.

Chapter 1, Topic 3 (World Models and State Abstractions) develops how that state estimate is built.

## Exercise

Choose a multi-step task: a database migration, a code refactor, or a research synthesis. The goal is a planning problem concrete enough to critique. Work in four steps:

1. Write three candidate plan states, each a short description of what is true in it.
2. Write one heuristic \(h\) for ranking them, and say what it estimates.
3. Name one observation that would force replanning.
4. Name one action that should require symbolic preconditions before execution, and list those preconditions.

A good answer has a heuristic that is cheap to compute and never boastful about how little work remains, a replanning trigger tied to concrete evidence rather than vague discomfort, and preconditions a program could check.
