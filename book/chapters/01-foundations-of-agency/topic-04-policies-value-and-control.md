# Policies, Value, and Control

Three topics have now handed us ingredients and no cook. Topic 1 (Goals, Environments, and Actions) supplied a goal contract, Topic 2 (Belief, Uncertainty, and Decision) supplied a belief state, and Topic 3 (World Models and State Abstractions) supplied a compact world model. What is still missing is the part of an agent that actually chooses. A **policy** is the rule that turns those three ingredients into an action.

A policy is not merely "what the model says next." It is the decision procedure that decides which proposal is allowed to become an event in the world.

## Value as Consequence Accounting

### Reading the Value Functions

Value is consequence accounting: a number saying how well things go after an action.

Let \(\pi(a\mid s)\) be a policy over an MDP (Markov decision process: a model where the next state depends only on the current state and the chosen action). Read \(\pi(a\mid s)\) as "the chance the policy picks action \(a\) when the state is \(s\)". The value functions record expected discounted consequence:

\[
V^\pi(s)=\mathbb{E}_\pi\!\left[\sum_{t=0}^{\infty}\gamma^t r_t\mid s_0=s\right],\qquad
Q^\pi(s,a)=\mathbb{E}_\pi\!\left[\sum_{t=0}^{\infty}\gamma^t r_t\mid s_0=s,a_0=a\right].
\]

Read the first as "the average total reward \(\pi\) collects starting from state \(s\)". Read the second as "the same average, but the first action is forced to be \(a\)". Here \(r_t\) is the reward at step \(t\), \(\mathbb{E}_\pi\) means "average over what policy and world might do", and \(\gamma\) (gamma) is the discount factor between 0 and 1 that makes later rewards count for less.

With \(\gamma=0.9\) and reward 1 at each of the first three steps, the discounted total is \(1+0.9+0.81=2.71\), not 3. Distant reward is real, but worth less than reward now.

### Bellman Recursion: Value in One Step Plus the Rest

Bellman recursion makes consequence compositional: a long future factors into one step plus what follows [[5](../../references.md#ref-5)] [[39](../../references.md#ref-39)]:

\[
V^{*}(s)=\max_{a\in\mathcal{A}}\left\{R(s,a)+\gamma\sum_{s'\in\mathcal{S}}T(s'\mid s,a)V^{*}(s')\right\}.
\]

Read this as "the best value of state \(s\) is the best available immediate reward \(R(s,a)\) plus the discounted average value of wherever you land". The set \(\mathcal{A}\) holds available actions, \(\mathcal{S}\) holds possible states, and \(T(s'\mid s,a)\) is the chance of moving to \(s'\) after doing \(a\) in \(s\).

The one-step decision-theoretic rule remains expected utility [[33](../../references.md#ref-33)] [[34](../../references.md#ref-34)]:

\[
a_t^{*}=\arg\max_a\;\mathbb{E}[U(a,S_t)\mid h_t].
\]

Read that as "pick the action whose average usefulness \(U\) is highest, given the history \(h_t\) observed so far". The operator \(\arg\max\) returns the winning action, not the winning number.

The connection between the two views is interpretive. Expected utility scores candidate actions under current belief. Dynamic programming, the Bellman style of reasoning, accounts for how today's action changes tomorrow's possibilities. When the world model is partial or approximate, these values are estimates, and their errors must be managed rather than ignored. In practice, log value estimates beside realized outcomes to see how far off they were.

## The Vocabulary of Learned Policies

Unwrap the learning vocabulary first. Five terms do most of the work:

- A **parameterized policy** \(\pi_\theta\) is a policy with adjustable numbers \(\theta\) (theta), much as a neural network has weights.
- The expression \(\pi_\theta(a\mid s)\) is the probability this policy assigns to action \(a\) in state \(s\).
- Its logarithm, \(\log\pi_\theta(a\mid s)\), turns products of probabilities into sums. That gives learning algorithms a handle on "make this sampled action more or less likely."
- A **gradient** \(\nabla_\theta J(\theta)\) is the direction in parameter space that most steeply increases the objective \(J\), at least locally. Read \(\nabla_\theta\) as "slope in the parameters".
- A **baseline** is a quantity subtracted from the return estimate to reduce noisy fluctuation without changing the expected update. That fluctuation is **variance**: sample-based estimates jump around even when their average is correct.

### The Policy-Gradient Theorem and the Advantage Baseline

Parameterized policies can adapt from experience. The policy-gradient theorem gives one standard form [[40](../../references.md#ref-40)]:

\[
\nabla_\theta J(\theta)=\mathbb{E}_{\pi_\theta}\!\left[\nabla_\theta\log\pi_\theta(a\mid s)\,Q^{\pi_\theta}(s,a)\right],
\]

often using the advantage baseline \(A^\pi(s,a)=Q^\pi(s,a)-V^\pi(s)\) to reduce variance without changing the expected gradient [[3](../../references.md#ref-3)] [[40](../../references.md#ref-40)]. Read the advantage as "how much better this action is than the policy's average behavior in this state". If \(Q^\pi(s,a)=8\) and \(V^\pi(s)=7.5\), the advantage is \(0.5\): a mild nudge upward, not a triumph.

For agentic systems, the lesson outlives any one learning algorithm. Judge policy improvement by four measurable things:

1. realized return, the reward actually collected;
2. constraint violations, the rules actually broken;
3. calibration, whether stated confidence matched observed accuracy;
4. stability, whether behavior stayed sane across runs.

Persuasiveness of the chosen action is not on the list.

## Proposal, Adjudication, Oversight

### A Patch That Looks Attractive and Is Not

Consider a coding agent choosing between **FastPatch** and **SafePatch** before a production freeze. Its proposer estimates:

\[
\hat Q(s,\text{FastPatch})=9.2,\qquad \hat Q(s,\text{SafePatch})=7.4.
\]

The hat on \(\hat Q\) means "estimated", not "known". A proposer with full authority would ship FastPatch every time. That is a proposer-only policy: generate the most attractive action under the proposal model, then let it become reality.

A governed policy is different. It separates the authority to suggest from the authority to execute. It makes that second authority answer to constraints, evidence, reversibility, and risk. The real objective is constrained:

\[
\max_\pi\;\mathbb{E}_\pi\!\left[\sum_{t\ge 0}\gamma^t r_t\right]
\quad\text{s.t.}\quad
\mathbb{E}_\pi\!\left[\sum_{t\ge 0}\gamma^t c_t\right]\le \kappa.
\]

Read this as "earn as much discounted reward as possible, while keeping expected discounted cost \(c_t\) at or below the budget \(\kappa\) (kappa)". Here "s.t." means "subject to".

FastPatch may carry authorization risk, rollback blast radius, or inadequate evidence. Constrained decision-making treats those as part of the policy rather than as after-the-fact regret [[51](../../references.md#ref-51)] [[53](../../references.md#ref-53)].

Oversight earns its cost according to the task. It can be wasteful for cheap reversible actions, such as reading one more local file or running a narrow test. It can be essential for risky irreversible actions, such as deploying to production, deleting data, spending money, or sending a binding message under an organization's name.

### The Governed Policy in Pseudocode

The pseudocode below governs one decision: sample candidates, score each on value, risk, and evidence quality, then check the winner against hard constraints before executing.

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

Put numbers into the scoring line. Let \(\lambda=2\) price risk and \(\beta=0.5\) reward evidence. FastPatch has value \(9.2\), risk \(2.0\), evidence \(0.4\), so its score is \(9.2-2(2.0)+0.5(0.4)=5.4\). SafePatch has value \(7.4\), risk \(0.6\), evidence \(0.9\), so its score is \(7.4-2(0.6)+0.5(0.9)=6.65\).

The unconstrained value estimate preferred FastPatch. The governed policy prefers SafePatch, because risk and evidence are first-class terms rather than whispered anxieties.

This decomposition is not bureaucracy for its own sake. It lets a language model be a generous proposer while the policy remains accountable for value, evidence, reversibility, and hard constraints.

## Value Is Not Confidence

Two numbers are easy to confuse. Value estimation asks, "If I take this action, how much utility should I expect?" Confidence scoring asks, "How reliable is this prediction or label?" They are related but not interchangeable:

\[
\hat V(s)\approx \mathbb{E}\!\left[\sum_{t\ge0}\gamma^t r_t\mid s\right],
\qquad
\hat p(y\mid x)\approx P(Y=y\mid X=x).
\]

The left expression estimates future reward from state \(s\). The right one estimates the probability that label \(y\) is correct for input \(x\).

Confidence models are judged by calibration metrics such as Brier score [[49](../../references.md#ref-49)]. To measure it, bucket predictions by stated confidence and compare claimed with observed accuracy. Value models are judged by downstream return and constraint behavior.

Three cases show why one number cannot do both jobs:

- an action can be certainly useless, with high confidence and no value;
- an action can be uncertain but valuable, with low confidence and high expected payoff;
- an action can look attractive only because the risk model is blind to what it would break.

A serious policy keeps these quantities separate.

## Closed-Loop Control

### Plan a Little, Act Once, Look Again

Model predictive control (MPC) captures the rhythm agent systems need, in four steps: plan over a finite horizon, execute the first action, observe the new state, and replan [[41](../../references.md#ref-41)] [[51](../../references.md#ref-51)] [[52](../../references.md#ref-52)].

In linear feedback form this appears as \(u_t=-K\hat x_t\), read as "the control input at time \(t\) is a fixed gain matrix \(K\) applied to the estimated state \(\hat x_t\), with the sign flipped to push error toward zero". Estimation and control are coupled: the controller can only act on what the estimator believes. In software agents the same idea appears as small verified actions, telemetry, rollback plans, budget checks, and escalation gates.

### A Plan-Act-Observe-Replan Trace

At step 0, the coding agent plans four moves: read the failing test, inspect the suspected module, apply a minimal patch, run the narrow test. It executes only the first action, `read failing test`. It observes that the assertion concerns timezone parsing rather than authentication.

At step 1, it replans: inspect `time_utils.py`, avoid auth code, and run the timezone-specific test. It executes `read time_utils.py`, observes a naive datetime conversion, and replans again toward a smaller edit.

The plan is not thrown away because planning was foolish. It is revised because reality has finally joined the meeting.

### The Full Interpreter Loop

The interpreter now looks like the loop below. Each pass observes, updates belief, abstracts the state, chooses a governed action, executes it, and appends the result to history.

```text
while not terminated:
    o_t <- observe()
    b_t <- update_belief(b_t, o_t)
    z_t <- abstract_state(history, b_t)
    a_t <- governed_policy(goal, z_t, b_t, constraints)
    outcome <- execute(a_t)
    history <- append(history, o_t, a_t, outcome)
```

That loop is the chapter's foundation. Goals define what matters. Belief manages uncertainty. State abstraction chooses what the policy can reason over. Control closes the loop after reality answers back.

From here, later chapters can study reasoning architectures, tools, memory, and multi-agent systems as refinements of this basic interpreter rather than as disconnected tricks.
