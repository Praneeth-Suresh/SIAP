# Policies, Value, and Control

The agent interpreter now has a goal contract, a belief state, and a compact world model. A policy is the rule that turns those ingredients into action. It is not merely "what the model says next." It is the decision procedure that decides which proposal may become an event in the world.

## Value as Consequence Accounting

Let \(\pi(a\mid s)\) be a policy over an MDP. The value functions record expected discounted consequence:

\[
V^\pi(s)=\mathbb{E}_\pi\!\left[\sum_{t=0}^{\infty}\gamma^t r_t\mid s_0=s\right],\qquad
Q^\pi(s,a)=\mathbb{E}_\pi\!\left[\sum_{t=0}^{\infty}\gamma^t r_t\mid s_0=s,a_0=a\right].
\]

Bellman recursion makes the consequence compositional [[5](../../references.md#ref-5)] [[39](../../references.md#ref-39)]:

\[
V^{*}(s)=\max_{a\in\mathcal{A}}\left\{R(s,a)+\gamma\sum_{s'\in\mathcal{S}}T(s'\mid s,a)V^{*}(s')\right\}.
\]

The one-step decision-theoretic rule remains expected utility [[33](../../references.md#ref-33)] [[34](../../references.md#ref-34)]:

\[
a_t^{*}=\arg\max_a\;\mathbb{E}[U(a,S_t)\mid h_t].
\]

The connection is interpretive. Expected utility scores candidate actions under current belief; dynamic programming accounts for how the action changes later possibilities. When the world model is partial or approximate, these values are estimates whose errors must be managed rather than ignored.

Before the next equation, unwrap the learning vocabulary. A **parameterized policy** \(\pi_\theta\) is a policy with adjustable numbers \(\theta\), much as a neural network has weights. The expression \(\pi_\theta(a\mid s)\) is the probability that this policy assigns to action \(a\) in state \(s\). Its logarithm, \(\log\pi_\theta(a\mid s)\), turns products of probabilities into sums and gives learning algorithms a convenient handle on "make this sampled action more or less likely." A **gradient** \(\nabla_\theta J(\theta)\) is the direction in parameter space that most steeply increases the objective \(J\), at least locally. A **baseline** is a quantity subtracted from the return estimate to reduce noisy fluctuation without changing the expected update. That noisy fluctuation is **variance**: the tendency of sample-based estimates to jump around even when their average is correct.

Parameterized policies can adapt from experience. The policy-gradient theorem gives one standard form [[40](../../references.md#ref-40)]:

\[
\nabla_\theta J(\theta)=\mathbb{E}_{\pi_\theta}\!\left[\nabla_\theta\log\pi_\theta(a\mid s)\,Q^{\pi_\theta}(s,a)\right],
\]

often using the advantage baseline \(A^\pi(s,a)=Q^\pi(s,a)-V^\pi(s)\) to reduce variance without changing the expected gradient [[3](../../references.md#ref-3)] [[40](../../references.md#ref-40)]. For agentic systems, the lesson is broader than any one learning algorithm: policy improvement should be judged by realized return, constraint violations, calibration, and stability, not by how persuasive the chosen action sounds.

## Proposal, Adjudication, Oversight

Consider a coding agent choosing between **FastPatch** and **SafePatch** before a production freeze. Its proposer estimates:

\[
\hat Q(s,\text{FastPatch})=9.2,\qquad \hat Q(s,\text{SafePatch})=7.4.
\]

If this proposer had full authority, it would ship FastPatch every time. That is a proposer-only policy: generate the most attractive action under the proposal model, then let it become reality. A governed policy is different. It separates the authority to suggest from the authority to execute, and it makes that second authority answer to constraints, evidence, reversibility, and risk. The real objective is constrained:

\[
\max_\pi\;\mathbb{E}_\pi\!\left[\sum_{t\ge 0}\gamma^t r_t\right]
\quad\text{s.t.}\quad
\mathbb{E}_\pi\!\left[\sum_{t\ge 0}\gamma^t c_t\right]\le \kappa.
\]

FastPatch may carry auth risk, rollback blast radius, or inadequate evidence. Constrained decision-making treats those as part of the policy rather than as after-the-fact regret [[51](../../references.md#ref-51)] [[53](../../references.md#ref-53)]. Oversight earns its cost according to the task. It can be wasteful for cheap reversible actions such as reading one more local file or running a narrow test. It can be essential for risky irreversible actions such as deploying to production, deleting data, spending money, or sending a binding message under an organization's name.

```text
function ACT(decision_state z_t, belief b_t, history h_t):
    candidates <- proposer.sample_actions(z_t, b_t, K)

    for a in candidates:
        value[a] <- estimate_return(z_t, b_t, a)
        risk[a] <- estimate_constraint_cost(z_t, b_t, a)
        evidence[a] <- evidence_quality(b_t, a)
        score[a] <- value[a] - lambda * risk[a] + beta * evidence[a]

    a_star <- argmax(score)

    if violates_hard_constraints(z_t, b_t, a_star):
        return fallback_or_escalate(z_t, b_t, h_t)

    return execute(a_star)
```

Put numbers into the scoring line. Suppose \(\lambda=2\) and \(\beta=0.5\). FastPatch has value \(9.2\), risk \(2.0\), and evidence quality \(0.4\), so its score is \(9.2-2(2.0)+0.5(0.4)=5.4\). SafePatch has value \(7.4\), risk \(0.6\), and evidence quality \(0.9\), so its score is \(7.4-2(0.6)+0.5(0.9)=6.65\). The unconstrained value estimate preferred FastPatch; the governed policy prefers SafePatch because risk and evidence are first-class terms rather than whispered anxieties.

This decomposition is not bureaucracy for its own sake. It lets a language model be a generous proposer while the policy remains accountable for value, evidence, reversibility, and hard constraints.

## Value Is Not Confidence

Value estimation asks, "If I take this action, how much utility should I expect?" Confidence scoring asks, "How reliable is this prediction or label?" They are related but not interchangeable:

\[
\hat V(s)\approx \mathbb{E}\!\left[\sum_{t\ge0}\gamma^t r_t\mid s\right],
\qquad
\hat p(y\mid x)\approx P(Y=y\mid X=x).
\]

Confidence models are judged by calibration metrics such as Brier score [[49](../../references.md#ref-49)]. Value models are judged by downstream return and constraint behavior. An action can be certainly useless, uncertain but valuable, or attractive only because the risk model is blind. A serious policy keeps these quantities separate.

## Closed-Loop Control

Model predictive control captures the rhythm that agent systems need: plan over a finite horizon, execute the first action, observe the new state, and replan [[41](../../references.md#ref-41)] [[51](../../references.md#ref-51)] [[52](../../references.md#ref-52)]. In linear feedback form this appears as \(u_t=-K\hat x_t\), where estimation and control are coupled. In software agents the same idea appears as small verified actions, telemetry, rollback plans, budget checks, and escalation gates.

A concrete plan-act-observe-replan trace makes the rhythm visible. At step 0, the coding agent plans: read the failing test, inspect the suspected module, apply a minimal patch, run the narrow test. It executes only the first action, `read failing test`, and observes that the assertion concerns timezone parsing rather than authentication. At step 1, it replans: inspect `time_utils.py`, avoid auth code, and run the timezone-specific test. It executes `read time_utils.py`, observes a naive datetime conversion, and replans again toward a smaller edit. The plan is not thrown away because planning was foolish; it is revised because reality has finally joined the meeting.

The full interpreter now looks like this:

```text
while not terminated:
    o_t <- observe()
    b_t <- update_belief(b_t, o_t)
    z_t <- abstract_state(history, b_t)
    a_t <- governed_policy(goal, z_t, b_t, constraints)
    outcome <- execute(a_t)
    history <- append(history, o_t, a_t, outcome)
```

That loop is the chapter's foundation. Goals define what matters. Belief manages uncertainty. State abstraction chooses what the policy can reason over. Control closes the loop after reality answers back. From here, later chapters can study reasoning architectures, tools, memory, and multi-agent systems as refinements of this basic interpreter rather than as disconnected tricks.
