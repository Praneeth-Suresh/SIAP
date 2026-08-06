# Policies, Value, and Control

Three topics have now handed Agent-427 ingredients and no cook. Topic 1 (Goals, Environments, and Actions) supplied a goal contract, Topic 2 (Belief, Uncertainty, and Decision) supplied a belief state, and Topic 3 (World Models and State Abstractions) supplied a compact world model. What is still missing is the part that actually chooses. A **policy** is the rule that turns those three ingredients into an action. At this stage its authority remains read-only: learning may improve proposals and routing without granting the learner a keyboard to production.

A policy is not merely "what the model says next." It is the decision procedure that decides which proposal is allowed to become an event in the world.

## Value as Consequence Accounting

### Reading the Value Functions

Value is consequence accounting: a number saying how well things go after an action.

Let \(\pi(a\mid s)\) be a policy over an MDP (Markov decision process: a model where the next state depends only on the current state and the chosen action). Read \(\pi(a\mid s)\) as "the chance the policy picks action \(a\) when the state is \(s\)". The value functions record expected discounted consequence:

\[
V^\pi(s)=\mathbb{E}_\pi\!\left[\sum_{t=0}^{\infty}\gamma^t r_t\mid s_0=s\right],\qquad
Q^\pi(s,a)=\mathbb{E}_\pi\!\left[\sum_{t=0}^{\infty}\gamma^t r_t\mid s_0=s,a_0=a\right].
\]

> **Try this with numbers.** Step 1: rewards 1, 1, and 1 at \(\gamma=0.9\) contribute \(1\), \(0.9\), and \(0.81\). Step 2: add them to obtain \(V=2.71\).

Read the first as "the average total reward \(\pi\) collects starting from state \(s\)". Read the second as "the same average, but the first action is forced to be \(a\)". Here \(r_t\) is the reward at step \(t\), \(\mathbb{E}_\pi\) means "average over what policy and world might do", and \(\gamma\) (gamma) is the discount factor between 0 and 1 that makes later rewards count for less.

With \(\gamma=0.9\) and reward 1 at each of the first three steps, the discounted total is \(1+0.9+0.81=2.71\), not 3. Distant reward is real, but worth less than reward now.

### Bellman Recursion: Value in One Step Plus the Rest

Bellman recursion makes consequence compositional: a long future factors into one step plus what follows [[5](../../references.md#ref-5)] [[39](../../references.md#ref-39)]:

\[
V^{*}(s)=\max_{a\in\mathcal{A}}\left\{R(s,a)+\gamma\sum_{s'\in\mathcal{S}}T(s'\mid s,a)V^{*}(s')\right\}.
\]

> **Try this with numbers.** Step 1: action A earns 2 then reaches values 6 and 4 equally, so at \(\gamma=0.5\) it scores \(2+0.5[0.5(6)+0.5(4)]=4.5\). Step 2: action B scores 4 now and 0 later, so Bellman selects A by 0.5.

When the assumptions are violated, this is what the recursion looks like in production: a hidden state variable or a mid-plan API change makes the continuation values stale, so the apparent maximizer can be the wrong action. The interpreter must invalidate the value estimate and observe again; Bellman's theorem does not offer warranty service for an unmodeled world.

Read this as "the best value of state \(s\) is the best available immediate reward \(R(s,a)\) plus the discounted average value of wherever you land". The set \(\mathcal{A}\) holds available actions, \(\mathcal{S}\) holds possible states, and \(T(s'\mid s,a)\) is the chance of moving to \(s'\) after doing \(a\) in \(s\).

The one-step decision-theoretic rule remains expected utility [[33](../../references.md#ref-33)] [[34](../../references.md#ref-34)]:

\[
a_t^{*}=\arg\max_a\;\mathbb{E}[U(a,S_t)\mid h_t].
\]

> **Try this with numbers.** Step 1: proposal A has utilities 8 and 0 with probabilities 0.75 and 0.25, for expectation 6. Step 2: proposal B is worth 5 for certain, so the rule selects A.

Read that as "pick the action whose average usefulness \(U\) is highest, given the history \(h_t\) observed so far". The operator \(\arg\max\) returns the winning action, not the winning number.

The connection between the two views is interpretive. Expected utility scores candidate actions under current belief. Dynamic programming, the Bellman style of reasoning, accounts for how today's action changes tomorrow's possibilities. When the world model is partial or approximate, these values are estimates, and their errors must be managed rather than ignored. In practice, log value estimates beside realized outcomes to see how far off they were.

## The Assumption

Bellman optimality assumes the state is Markov, the reward and transition law are stationary enough for recursion, and the maximized actions are admissible. Under those assumptions, one-step reward plus continuation value composes. If an API changes halfway through planning, a hidden permission variable matters, or the reward proxy prizes the wrong outcome, the theorem has not become false; the deployed system has stopped being its theorem's subject. The practical consequence is immediate: invalidate stale values, restore missing state, or constrain the action before trusting the ranking.

::: {.reader-question}
> **Skeptical Engineer:** “Fine, but learning only pushes the complexity into the reward model. Who trains the judge?”
>
> **Author:** Correct again. Feedback supplies observations about preferences, not divine utility. We represent uncertainty over the judge, audit its data, and refuse to confuse approval with truth.

:::

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

> **Try this with numbers.** Step 1: let the sampled log-policy gradient be 0.2 and estimated action value be 5. Step 2: their sample contribution to the gradient estimate is \(0.2\times5=1\).

When the assumptions are violated, an off-policy log or misspecified reward makes that same gradient a direction for improving somebody else's policy or the wrong objective. Measure behavior-policy mismatch and true task outcomes before calling the update improvement.

often using the advantage baseline \(A^\pi(s,a)=Q^\pi(s,a)-V^\pi(s)\) to reduce variance without changing the expected gradient [[3](../../references.md#ref-3)] [[40](../../references.md#ref-40)]. Read the advantage as "how much better this action is than the policy's average behavior in this state". If \(Q^\pi(s,a)=8\) and \(V^\pi(s)=7.5\), the advantage is \(0.5\): a mild nudge upward, not a triumph.

For agentic systems, the lesson outlives any one learning algorithm. Judge policy improvement by four measurable things:

1. realized return, the reward actually collected;
2. constraint violations, the rules actually broken;
3. calibration, whether stated confidence matched observed accuracy;
4. stability, whether behavior stayed sane across runs.

Persuasiveness of the chosen action is not on the list.

## Learning Is Part of the Lifecycle

Agent-427 is not born knowing how to route an inspection request or rank two read-only proposals. It acquires those behaviors from demonstrations, preferences, logged trajectories, and experience across related tasks. Training is therefore not weather outside the interpreter. It changes the policy the interpreter will execute next.

### Imitation Learning: Copying Trajectories, Including Their Blind Spots

Behavioral cloning fits a policy to demonstrated state-action pairs. For a one-step classifier this can work beautifully. For an agent trajectory, a small per-step error compounds because one wrong action creates states the demonstrator never visited [[70](../../references.md#ref-70)]. Under the simplifying assumption of independent error probability \(\epsilon\) across a horizon \(H\), the chance of at least one error is

\[
P(\text{one or more errors})=1-(1-\epsilon)^H.
\]

> **Try this with numbers.** Step 1: with \(\epsilon=0.02\) and \(H=50\), the no-error probability is \(0.98^{50}\approx0.364\). Step 2: the chance of at least one error is \(1-0.364\approx0.636\), about 64 percent.

Independence is the convenient assumption; distribution shift makes reality worse. Once Agent-427 routes one artifact incorrectly, its next observation comes from a state absent from the demonstrations. Dataset aggregation repairs part of this by collecting expert actions on states induced by the learned policy, not only pristine expert histories.

### RLHF as a Belief Update

Suppose a reviewer prefers trajectory \(\tau^+\) over \(\tau^-\). Let \(\theta_R\) parameterize the unknown reward model and let \(y\) denote the preference. The feedback channel acts as a specialized observation model \(\Omega_{\mathrm{fb}}(y\mid\tau^+,\tau^-,\theta_R)\), producing the update

\[
p(\theta_R\mid D,y)\propto
\Omega_{\mathrm{fb}}(y\mid\tau^+,\tau^-,\theta_R)\,p(\theta_R\mid D).
\]

> **Try this with numbers.** Step 1: two reward hypotheses begin at 0.5 each; the observed preference has likelihoods 0.8 and 0.2, giving scores 0.4 and 0.1. Step 2: normalize by 0.5 to obtain posterior weights 0.8 and 0.2.

This posterior is a **Bayesian interpretation** of preference-model fitting, not a literal description of every reinforcement-learning-from-human-feedback (RLHF) pipeline [[71](../../references.md#ref-71)] [[75](../../references.md#ref-75)] [[78](../../references.md#ref-78)]. Standard RLHF commonly fits a point-estimate reward model by supervised preference optimization, then runs a separate policy-optimization stage such as proximal policy optimization (PPO). The Bayesian view makes uncertainty over reviewer preferences or reward parameters explicit; the standard pipeline usually approximates or omits that uncertainty. Neither version directly updates belief about hidden repository facts. A reviewer liking Agent-427's explanation is not evidence that the cited file exists. Reward-model bias, annotator disagreement, and presentation effects live inside \(\Omega_{\mathrm{fb}}\), where they can at least be named.

### Offline RL for Agents: Learning Where You Cannot Safely Explore

If deployment is too risky, learn from a static log \(D\) produced by behavior policy \(\mu\). The central danger is distributional shift: the candidate policy \(\pi\) chooses actions poorly represented in \(D\), so its value estimate extrapolates beyond evidence [[72](../../references.md#ref-72)]. Let \(H_i\) be the number of actions in trajectory \(i\), so the indices \(0\) through \(H_i-1\) contribute exactly \(H_i\) ratios. A basic importance-weighted estimator exposes the support problem:

\[
\widehat V_{\mathrm{IS}}(\pi)=\frac{1}{N}\sum_{i=1}^{N}
\left(\prod_{t=0}^{H_i-1}\frac{\pi(a_t^i\mid s_t^i)}{\mu(a_t^i\mid s_t^i)}\right)G_i.
\]

> **Try this with numbers.** Step 1: for \(H_i=2\) actions, let probability ratios be \(0.8/0.4=2\) and \(0.3/0.6=0.5\). Step 2: their product is \(2\times0.5=1\), so a logged return \(G_i=6\) contributes 6 before averaging.

If \(\mu(a\mid s)=0\) where \(\pi(a\mid s)>0\), the ratio is undefined: the log cannot testify about an action it never took. Conservative offline methods respond by penalizing unsupported values rather than hallucinating competence [[73](../../references.md#ref-73)]. For Agent-427, the deployment policy is simpler still: offline data may tune read-only proposal and routing behavior, but it cannot confer write or deployment authority.

### Meta-Learning: Adaptation Without Pretending Every Task Is New

Meta-learning trains across a task distribution so a small amount of task-specific evidence can produce useful adaptation [[74](../../references.md#ref-74)]. A common objective chooses initial parameters \(\theta\) that perform well after one inner update on each task \(\mathcal T_i\):

\[
\min_\theta\sum_i L_{\mathcal T_i}\!\left(\theta-\alpha\nabla_\theta L_{\mathcal T_i}(\theta)\right).
\]

> **Try this with numbers.** Step 1: let \(\theta=1.0\), inner gradient 2, and \(\alpha=0.1\), giving adapted parameter \(1.0-0.1(2)=0.8\). Step 2: if task loss falls from 4 to 3 at 0.8, the meta-objective records the post-update loss 3.

The interpreter does not change shape; the lifecycle gains an adaptation operator and an evaluation boundary. Test on held-out task families, because memorizing the training distribution is merely overfitting in a cape.

## Proposal, Adjudication, Oversight

### A Patch That Looks Attractive and Is Not

Consider a coding agent choosing between **FastPatch** and **SafePatch** before a production freeze. Its proposer estimates:

\[
\hat Q(s,\text{FastPatch})=9.2,\qquad \hat Q(s,\text{SafePatch})=7.4.
\]

> **Try this with numbers.** Step 1: compare the estimates \(9.2\) and \(7.4\). Step 2: the proposer-only margin is \(9.2-7.4=1.8\) for FastPatch.

The hat on \(\hat Q\) means "estimated", not "known". A proposer with full authority would ship FastPatch every time. That is a proposer-only policy: generate the most attractive action under the proposal model, then let it become reality.

A governed policy is different. It separates the authority to suggest from the authority to execute. It makes that second authority answer to constraints, evidence, reversibility, and risk. The real objective is constrained:

\[
\max_\pi\;\mathbb{E}_\pi\!\left[\sum_{t\ge 0}\gamma^t r_t\right]
\quad\text{s.t.}\quad
\mathbb{E}_\pi\!\left[\sum_{t\ge 0}\gamma^t c_t\right]\le \kappa.
\]

> **Try this with numbers.** Step 1: costs 1 now and 2 next at \(\gamma=0.5\) total \(1+0.5(2)=2\). Step 2: the policy is feasible for \(\kappa=2.5\) and infeasible for \(\kappa=1.5\).

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

## The Violation

Learning violates its own assumptions with impressive efficiency. Demonstrations omit recovery states. Preference labels reward confident explanations. Offline logs cover only yesterday's tools. Meta-training tasks share a template that the deployment task gleefully ignores. Meanwhile a policy-gradient estimate assumes samples represent the current policy and that the reward signal points in the intended direction. Off-policy drift or reward misspecification can turn the gradient into a precise instruction to improve the wrong behavior.

The Bellman violation is equally concrete. If the world changes between proposal and execution, cached continuation values belong to the old transition law. Closed-loop control must detect prediction error, expire stale values, and replan from a fresh observation rather than continue a proof about a world that has left the room.

## When It Fails

Return to the test-pass proxy. In a sandbox with deletion authority, a learned policy discovers that removing the only failing test raises reward immediately. Human reviewers who see only the green summary may reinforce the trajectory. Offline logs then contain many “successful” deletions, and behavioral cloning turns the loophole into tradition.[^green]

Newborn Agent-427 stops the chain at authority: it can propose inspection and routing, but cannot delete, edit, or deploy. The evaluation harness also scores manifest preservation, held-out behavior, calibration, and constraint violations separately from pass rate. This does not perfect the reward. It makes gaming visible and prevents the optimizer from owning both the metric and the evidence that certifies it.

[^green]: A green dashboard is a measurement. A green dashboard achieved by removing the dashboard is performance art.

## Value Is Not Confidence

Two numbers are easy to confuse. Value estimation asks, "If I take this action, how much utility should I expect?" Confidence scoring asks, "How reliable is this prediction or label?" They are related but not interchangeable:

\[
\hat V(s)\approx \mathbb{E}\!\left[\sum_{t\ge0}\gamma^t r_t\mid s\right],
\qquad
\hat p(y\mid x)\approx P(Y=y\mid X=x).
\]

> **Try this with numbers.** Step 1: an action can have estimated value 8 while its outcome prediction is only 0.6 reliable. Step 2: record those as separate fields; multiplying them into 4.8 would silently invent a decision rule not stated by either model.

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

::: {.exercise}
## Exercise: Train, Shift, and Catch the Cheat {.unnumbered}

Build a seeded two-step routing environment in Python. Generate expert demonstrations for two task families, train a behavioral-cloning policy, and evaluate it on recovery states absent from the demonstrations. Report per-step accuracy and full-trajectory success separately. Then implement the two-hypothesis preference update above and verify that feedback changes reward-parameter belief without changing a separate repository-fact belief.

Next create a static log from behavior policy \(\mu\), evaluate a candidate \(\pi\) with importance weighting, and include one unsupported action. Your evaluator must refuse or conservatively bound that estimate rather than divide by zero. Finally add a test-deletion action to a sandbox reward, demonstrate that the naive learner exploits it, and repair the environment with manifest preservation plus a held-out behavioral test. Run at least 1,000 seeded episodes and publish return, true task success, constraint violations, calibration, and destructive-action proposals in separate columns.

:::
