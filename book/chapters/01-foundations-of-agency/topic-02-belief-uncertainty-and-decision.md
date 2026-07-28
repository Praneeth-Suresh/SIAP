# Belief, Uncertainty, and Decision

An agent almost never gets to see the world as it truly is. It sees fragments,
and must act anyway. Something has to turn those fragments into a picture solid
enough to act on. That machinery is called *belief*, and it is the second
component of the interpreter we are building.

The interpreter from Topic 1 (Goals, Environments, and Actions) cannot read the
true state of the world directly. It sees test output, file contents, user
messages, logs, retrieval results, and tool failures. Belief is the agent's
working account of what those observations imply. It is not a mood of confidence.
It is the state variable that makes action possible under *partial
observability* (the ordinary situation in which the agent's sensors show only
part of what is going on).

## Belief as Runtime State, Not a Feeling

Belief is a variable the program carries between steps, like a counter or a
cache. Three symbols do the work.

The table below names the three quantities that appear in every belief equation
in this section, together with how to read each one aloud.

| Symbol | Read it as | Meaning |
|---|---|---|
| \(s_t\) | "the state at step t" | The *latent* (hidden from the agent's sensors) state of the world |
| \(h_t=(o_{0:t},a_{0:t-1})\) | "the history at step t" | Everything observed so far, plus every action taken so far |
| \(b_t(s)=P(s_t=s\mid h_t)\) | "the belief at step t assigns to state s" | How likely the agent thinks state \(s\) is, given that history |

Under a POMDP (partially observable Markov decision process) interpretation,
belief evolves by Bayesian filtering [[7](../../references.md#ref-7)]
[[4](../../references.md#ref-4)]:

\[
b_{t+1}(s')=\eta\,\Omega(o_{t+1}\mid s',a_t)\sum_{s\in\mathcal{S}}T(s'\mid s,a_t)b_t(s),
\]

where \(\eta\) normalizes the distribution. The observation model also gives a
prediction about what the agent expects to see next:

\[
P(o_{t+1}\mid b_t,a_t)=\sum_{s'}\Omega(o_{t+1}\mid s',a_t)\sum_s T(s'\mid s,a_t)b_t(s).
\]

Read the filter as two moves: **predict**, then **correct**.

1. The inner sum \(\sum_s T(s'\mid s,a_t)b_t(s)\) predicts how likely each next
   state \(s'\) is after action \(a_t\), before the new observation arrives.
   Here \(T\) is the transition model and \(\mathcal{S}\) is the set of possible
   states.
2. The likelihood \(\Omega(o_{t+1}\mid s',a_t)\) then corrects that prediction.
   It asks how plausible the observed evidence would be if \(s'\) were true.
3. The constant \(\eta\), the Greek letter eta, is just the normalizer that
   makes all the updated probabilities add to \(1\).

Some vocabulary, defined once and used forever after. Conditional probability
\(P(X\mid Y)\) means "the probability of \(X\) after assuming or observing
\(Y\)." A **prior** is the belief before the new observation. A **likelihood**
is how well a possible state explains the observation. The **posterior** is the
corrected belief after combining them.

A two-state example makes the arithmetic concrete. Suppose the agent believes a
bug is in module A with probability \(0.5\) and in module B with probability
\(0.5\). A test fails. If that failure has likelihood \(0.9\) under "bug in A"
and \(0.1\) under "bug in B", the unnormalized scores are \(0.45\) and \(0.05\).
Divide by their sum, \(0.5\), and belief becomes \(0.9\) for A and \(0.1\) for
B. That division by \(0.5\) is \(\eta\) doing its only job.

### Why Approximate Belief Still Counts as Belief

These equations are idealized. Real agents often use scores, hypotheses,
retrieval rankings, or learned estimators instead of exact distributions. The
key requirement is not mathematical ceremony. It is that observations change the
variables that action selection depends on.

The pseudocode below shows the minimum shape of a belief update in a practical
agent. It takes the old belief, a new observation, and the action just taken,
and returns a new belief made of three parts: the surviving hypotheses, a
recalibrated confidence, and the gaps that still matter for the decision.

```text
function UPDATE_BELIEF(belief, observation, action):
    hypotheses <- revise_hypotheses(belief.hypotheses, observation)
    confidence <- recalibrate(hypotheses, observation.source, observation.freshness)
    unknowns <- identify_decision_relevant_gaps(hypotheses)
    return Belief(hypotheses, confidence, unknowns)
```

In a coding agent, a failing test should increase belief in some fault
hypotheses and decrease others. A missing dependency error should not be treated
like a behavioral regression. A stale document should count as evidence with a
weaker likelihood than a current API response. This is what it means for belief
to be an operational object.

## Decisions in Belief Space

Once belief is explicit, decision quality can be evaluated in belief space. In
sequential problems this value is recursive. An action is good partly because of
the observations and opportunities it makes available later
[[5](../../references.md#ref-5)].

\[
V^\pi(b)=\mathbb{E}\!\left[\sum_{t\ge 0}\gamma^t R(s_t,a_t)\mid b_0=b,\pi\right].
\]

Read that as "the value of following policy \(\pi\) from belief \(b\) is the
expected total reward, with rewards further in the future shrunk by the discount
factor \(\gamma\)." The symbol \(\mathbb{E}\) means "expected value", the
probability-weighted average.

At a single step, the expected-utility rule is:

\[
a_t^\star=\arg\max_{a\in\mathcal{A}}\mathbb{E}[U(a,S_t)\mid h_t],
\]

which reads "the best action \(a^\star\) is the one in the action set
\(\mathcal{A}\) with the highest average utility \(U\), averaged over the states
the history \(h_t\) still allows." This holds assuming the utility model and
belief distribution are adequate for the decision at hand
[[33](../../references.md#ref-33)] [[34](../../references.md#ref-34)]. The
assumption matters. If the belief state omits a safety-relevant variable, the
expected utility calculation can be precise and still wrong.

### Two Roads and a Hidden Storm

Suppose an agent chooses between **Shortcut** \(A\) and **Detour** \(B\), while
weather \(S\in\{\text{clear},\text{storm}\}\) is hidden. Utilities are
\(U(A,\text{clear})=10\), \(U(A,\text{storm})=-20\), and
\(U(B,\text{clear})=U(B,\text{storm})=4\). With no forecast and equal prior
probabilities, \(A\) has expected utility \(-5\), so \(B\) is better. If a
forecast is 90 percent accurate and predicts clear weather, then \(A\)'s
expected utility becomes \(0.9(10)+0.1(-20)=7\), so \(A\) is better. The world
did not change; the action ranking changed because the belief did.

The arithmetic is small enough to leave on the page. Before querying,
\[
\mathbb{E}[U(A)]=0.5(10)+0.5(-20)=-5.
\]
After a forecast \(q=\text{clear}\) with 90 percent accuracy,
\[
\mathbb{E}[U(A)\mid q=\text{clear}]=0.9(10)+0.1(-20)=7>4=\mathbb{E}[U(B)\mid q=\text{clear}],
\]
so the shortcut becomes rational. If instead \(q=\text{storm}\), then
\[
\mathbb{E}[U(A)\mid q=\text{storm}]=0.1(10)+0.9(-20)=-17<4,
\]
so the detour remains rational. The same pair of roads supports different
actions because belief, not bravado, mediates between observation and control.

## Information Has a Price

Information gathering is not a prelude to action. It is an action with cost,
latency, and opportunity cost. Two features of a task decide whether another
query is worth making:

- **Uncertainty.** If the relevant state is already known well enough, another
  query is incense, not engineering.
- **The size of the action gap.** If the best action is far ahead of its rivals,
  evidence must be very surprising to change the ranking. If the alternatives
  are nearly tied, a small observation can be decisive.

A query is worthwhile when it is likely to change the decision enough to pay for
itself. The value of information, written VoI, states that condition exactly:

\[
\operatorname{VoI}(q)=\mathbb{E}\!\left[\max_a \mathbb{E}[U(a,s)\mid h_t,q]\right]
\;-\;\max_a \mathbb{E}[U(a,s)\mid h_t].
\]

Read it as "the best you expect to do after learning the answer to \(q\), minus
the best you can do now." To use it in practice, price the query in the same
units as utility and compare.

In the route example, querying the forecast raises expected utility from \(4\)
to \(5.5\):
\[
0.5\cdot 7 + 0.5\cdot 4 = 5.5,
\]
so the value of information is \(1.5\). The two halves of that sum are the two
possible forecasts: clear, worth \(7\), and storm, worth \(4\). If the query
costs \(0.8\), ask first. If it costs \(2\), act without it.

### Entropy and Mutual Information: Measuring What Is Left to Learn

Information theory gives related measures of remaining uncertainty. Entropy
measures how spread out the belief is:
\[
H(S\mid h)=-\sum_s b(s)\log b(s).
\]
Mutual information measures how much a query \(Q\) is expected to reduce that
uncertainty:
\[
I(S;Q\mid h)=H(S\mid h)-H(S\mid h,Q).
\]
These symbols are not rival decision rules. \(H(S\mid h)\) says how much
uncertainty about state \(S\) remains after history \(h\). \(I(S;Q\mid h)\) says
how much of that uncertainty the query may retire. The value-of-information
calculation then asks whether retiring that uncertainty changes the action
ranking enough to pay for the query [[35](../../references.md#ref-35)].

A quick check on entropy. A belief split \(0.5/0.5\) has entropy \(\log 2\), the
largest possible value for two states. A belief of \(1.0/0.0\) has entropy
\(0\), because nothing is left to learn. Entropy measures confusion; only VoI
measures whether that confusion is expensive.

### Deciding Now While Protecting Later

Sequential control carries the same idea forward in time through a belief-space
Bellman equation:
\[
V^\star(b)=\max_a\{r(b,a)+\gamma\sum_o P(o\mid b,a)V^\star(\tau(b,a,o))\}.
\]
Here \(b\) is the current belief, \(r(b,a)\) is the immediate reward of acting
from that belief, \(P(o\mid b,a)\) is the probability of seeing observation
\(o\), and \(\tau(b,a,o)\) is the updated belief after action and observation.
The agent is therefore not merely selecting an action; it is selecting the
future quality of its own epistemic state [[5](../../references.md#ref-5)]
[[7](../../references.md#ref-7)].

The control loop now becomes a short branch on the size of the action gap. If
one action clearly wins, act. If not, consider buying evidence. If evidence
cannot help either, act with the assumption written down, or hand the decision
to a human.

```text
if action_gap(belief) is large:
    act(best_action)
else if cheap_observation_can_change_ranking(belief):
    gather_information()
else:
    act_with_recorded_assumption_or_escalate()
```

This pattern turns "be uncertain" into a policy. It also explains why more
retrieval is not automatically better. Retrieval, search, and external evidence
help only when they can move belief in a way that changes the ranking of
available actions, or at least changes whether acting, waiting, or escalating is
justified. Evidence is useful when it changes calibrated action quality per unit
cost. In feedback-control terms, estimation and action are coupled: the agent
measures because the measurement may change the next control move, and it acts
knowing that the next measurement may correct it
[[36](../../references.md#ref-36)] [[41](../../references.md#ref-41)].

## Approximation and Calibration

Exact Bayesian filtering is often too expensive for production loops.
Approximation is acceptable when it is decision-safe, not merely statistically
elegant. Let

\[
\Delta(b)=Q(b,a^\star)-\max_{a\ne a^\star}Q(b,a)
\]

be the action gap, read as "the value of the best action minus the value of the
best runner-up." If an approximation \(\tilde Q\) has uniform error
\(\lvert \tilde Q(b,a)-Q(b,a)\rvert\le \varepsilon_Q\), then the greedy action
is unchanged whenever \(\Delta(b)>2\varepsilon_Q\). The error can push the best
action down by \(\varepsilon_Q\) and the runner-up up by \(\varepsilon_Q\), so
\(2\varepsilon_Q\) is the worst-case swing. This simple bound is useful because
it ties inference quality to policy quality: approximation error matters most
near decision boundaries [[37](../../references.md#ref-37)]
[[38](../../references.md#ref-38)].

For example, suppose a coding agent estimates \(Q(b,\text{SafePatch})=10\) and
\(Q(b,\text{FastPatch})=7\), so the action gap is \(\Delta=3\). If the value
approximation can be wrong by at most \(\varepsilon_Q=1\) for each action, then
\(2\varepsilon_Q=2\), and \(3>2\). Even after accounting for approximation
error, SafePatch remains the greedy choice. If the gap were only \(1.5\), the
same estimator would not justify confidence in the ranking; the agent should
gather evidence, choose the safer default, or escalate.

### Making Confidence Mean Something

Calibration is the corresponding empirical discipline. A confidence estimate
should mean what it says under proper scoring rules such as the Brier score
[[49](../../references.md#ref-49)]. For a binary event, the Brier score is
\((p-y)^2\), where \(p\) is the predicted probability and \(y\) is \(1\) if the
event happened and \(0\) otherwise; lower is better. Predicting a test will pass
with probability \(0.8\) and then seeing it fail gives \((0.8-0)^2=0.64\).
Predicting \(0.2\) and seeing failure gives \(0.04\). A builder can measure this
directly: log each stated probability, log what happened, and average the
squared differences.

Calibrated belief also changes what an agent can say about itself. A
belief-aware customer-support agent can distinguish "I know the refund policy"
from "I know the policy but not whether this order qualifies." A belief-aware
coding agent can distinguish "the failing test localizes the bug" from "three
modules remain plausible, so editing now is premature."

The interpreter has therefore gained its second component. Goals and actions
define what the agent is trying to do; belief defines what the agent thinks is
true enough to justify the next move. Topic 3 (World Models and State
Abstractions) takes up the next question: which parts of the world deserve to be
in the state at all.
