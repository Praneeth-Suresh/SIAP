# Deliberation, Planning, and Search

The interpreter from the previous topic can execute one legal step at a time. Deliberation asks whether the agent should spend some of its budget simulating several steps before committing to one. Planning and search are disciplined ways to buy that foresight without pretending that computation is free.

The key distinction is between a proposal and a plan. A proposal says, "try this next action." A plan embeds that action in an imagined trajectory: what state should follow, what evidence should appear, what cost will be paid, what constraint might bind, and what fallback remains if the world disagrees. Search is the procedure that compares such trajectories under limited time.

## Plans as Paths Through Interpreter States

Let \(G=(V,E)\) be a search graph whose vertices are decision states. A deterministic plan is a path \(p=(v_0,\dots,v_T)\) minimizing
\[
J(p)=\sum_{t=0}^{T-1} c(v_t,v_{t+1}) + \Phi(v_T).
\]
A* prioritizes candidate nodes by
\[
f(n)=g(n)+h(n),
\]
where admissibility \(h(n)\le h^\star(n)\) gives shortest-path guarantees when the graph assumptions hold [[8](../../references.md#ref-8)]. In the agent interpreter, \(g\) accounts for already-spent cost and \(h\) estimates the remaining cost to reach an acceptable halt state.

The three letters are intentionally humble. \(g(n)\) is the cost already paid to reach node \(n\). \(h(n)\) is a heuristic estimate of the cost still required from \(n\) to a goal. \(f(n)\) is their sum, the planner's current guess at total path cost through \(n\). A heuristic is admissible when it never overestimates the true remaining cost \(h^\star(n)\); it may be naive, but it must not be boastful.

For a tiny graph, suppose \(v_0\) is "bug report received." From it the agent can inspect logs and reach \(A\), or inspect the recent diff and reach \(B\). The path to \(A\) has already cost \(g(A)=2\), and the heuristic says \(h(A)=5\), so \(f(A)=7\). The path to \(B\) has already cost \(g(B)=4\), and the heuristic says \(h(B)=1\), so \(f(B)=5\). A* expands \(B\) first, not because inspecting diffs is morally superior, but because the combined arithmetic says that route currently looks cheaper. The branching factor is the number of successor choices the search usually faces at each node; reducing it from ten plausible actions to three well-typed actions can turn a hopeless thicket into a walkable garden path.

Symbolic planning makes the transition model explicit. An action is legal only when its preconditions are present, and its effects transform the state:
\[
s_{t+1}=(s_t\mathbin{\backslash}\mathrm{Del}(a_t))\cup \mathrm{Add}(a_t),\qquad \mathrm{Pre}(a_t)\subseteq s_t.
\]
This is not limited to toy blocks-world domains. A coding agent's `run_tests` action may require a clean dependency environment; a `deploy` action may require passing tests, approval, and rollback instructions. Preconditions prevent the planner from treating hope as an executable dependency [[9](../../references.md#ref-9)] [[10](../../references.md#ref-10)].

Decode the notation as set editing. \(\mathrm{Pre}(a)\) is the set of facts that must already be true before action \(a\) may run. \(\mathrm{Add}(a)\) is the set of facts made true afterward. \(\mathrm{Del}(a)\) is the set of facts removed afterward. For `run_tests`, one toy model might be
\[
\mathrm{Pre}(\texttt{run\_tests})=\{\texttt{deps\_installed},\texttt{worktree\_readable}\},
\]
\[
\mathrm{Add}(\texttt{run\_tests})=\{\texttt{test\_result\_known}\},\qquad
\mathrm{Del}(\texttt{run\_tests})=\{\texttt{test\_result\_stale}\}.
\]
If the current state contains installed dependencies and a readable worktree, the action is legal. Afterward, the planner may rely on a fresh test result and must stop trusting the stale one. The notation is austere because the promise is austere: no premise, no action.

## Search Under Uncertainty

Expected utility supplies the selection rule:
\[
a_t^\star=\arg\max_a \mathbb{E}[U(a,S_t)\mid h_t],
\]
so additional planning depth is justified only when its expected improvement exceeds its compute and latency costs [[33](../../references.md#ref-33)] [[34](../../references.md#ref-34)]. In stochastic settings this becomes Bellman recursion,
\[
V^\star(s)=\max_a\left\{R(s,a)+\gamma\sum_{s'}P(s'|s,a)V^\star(s')\right\},
\]
or a belief-space recursion when the state is only partially observed [[5](../../references.md#ref-5)] [[4](../../references.md#ref-4)] [[7](../../references.md#ref-7)].

When the branching factor is large, the planner needs search control. Monte Carlo tree search allocates rollouts by optimism:
\[
a^\star=\arg\max_a\left(Q(s,a)+c\sqrt{\frac{\ln N(s)}{N(s,a)}}\right),
\]
balancing exploitation of promising branches with exploration of uncertain ones under finite time [[45](../../references.md#ref-45)]. The formula is a reminder that uncertainty is not merely a defect; it is sometimes a reason to inspect a branch before discarding it.

A rollout is a simulated continuation from the current state: the planner imagines taking actions until a terminal or cutoff state, then uses the result to improve its estimates. Exploitation means spending simulations on branches whose current value estimate \(Q(s,a)\) already looks good. Exploration means spending some simulations on branches with few visits \(N(s,a)\), because ignorance may be hiding either treasure or calamity. The square-root term is the exploration bonus; it shrinks as a particular action is tried more often, while growing slowly as the parent state receives more total visits.

## Receding Horizons

Long plans are fragile because the world answers back. Model predictive control handles this by solving an \(H\)-step problem,
\[
\mathbf{u}_{t:t+H-1}^{\star}
=\arg\min_{\mathbf{u}_{t:t+H-1}}
\sum_{k=0}^{H-1}\ell(x_{t+k},u_{t+k})+\ell_f(x_{t+H})
\]
subject to \(x_{k+1}=F(x_k,u_k)\) and \(g(x_k,u_k)\le 0\). The controller applies \(u_t^\star\), the first component of the optimized sequence, observes the new state, and replans at the next step. The corrected control sequence is important: the optimizer reasons over a sequence, while the agent executes only the first action before feedback updates the problem [[41](../../references.md#ref-41)].

For a language-agent planner, this pattern becomes:

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

The plan is a hypothesis about controllable futures, not a contract that reality has signed. This is why "plan then execute" is weak when the execution environment changes, and why "plan, execute one step, observe, replan" is the natural extension of the Chapter 1 interpreter.

## What Decomposition Is For

Task decomposition is useful only when it improves the search problem. It may reduce branching factor, expose prerequisites, create verifiable intermediate states, or isolate irreversible actions behind stronger checks. It is not useful merely because it produces a tidy list.

This is the first practical rule of planning: task structure predicts whether planning earns its keep. Planning tends to help when the horizon is long enough that early choices create or destroy later options; when the branching factor is wide enough that unguided next-action choice wastes effort; when prerequisites impose a real order; when uncertainty must be reduced before commitment; or when an irreversible action deserves ceremony before the lever is pulled. A database migration, a multi-file refactor, and a research synthesis with conflicting sources all have enough internal geometry to reward decomposition. A one-line formatting fix usually does not. There, the planning ritual may cost more than the task.

The same lesson governs composition. Reflection can repair a difficult plan: after a failed test, the agent can inspect the trace, notice that a prerequisite was imaginary, and revise the frontier before doing more damage. But reflection also adds latency, consumes tokens, and can induce overthinking on easy tasks. An agent asked to rename a local variable may spend three reflective turns debating architectural intent while the correct edit waits patiently in the file. Patterns interact; they are not virtues in isolation. Planning plus reflection is powerful when the task contains hidden dependencies or costly mistakes, and ornamental when the task is short, reversible, and already well specified.

In practice, each candidate trajectory should record state estimate, proposed action, expected observation, cost, risk, and contingency. Heuristics should prioritize branches, but pruning decisions should be logged when they affect safety or correctness. Irreversible or expensive actions should be protected by symbolic preconditions. Replan triggers should be explicit: new evidence, failed precondition, budget drift, tool error, or a value estimate that changes enough to reorder the frontier.

## Exercise

Choose a multi-step task such as a database migration, a code refactor, or a research synthesis. Write three candidate plan states and one heuristic \(h\) for ranking them. Then name one observation that would force replanning and one action that should require symbolic preconditions before execution.
