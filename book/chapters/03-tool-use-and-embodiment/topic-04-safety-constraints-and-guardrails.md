# Safety Constraints and Guardrails

Safety is not a postscript to capability. It is the part of the interpreter
that decides which proposed transitions are outside the program's charter,
which are allowed but costly, and which require another authority before the
world may be changed. In a tool-using system, safety lives at the same boundary
as action: between the model's proposed next step and the external effect that
would make that step real.

This makes guardrails more than warning text. A guardrail is a filter on the
agent's transition system. It may remove an action from the action space,
reshape the action into a safer one, pause for human approval, or attach an
obligation to monitor what happens next.

## Constrained control formulation

Model policy selection as a constrained MDP:
\[
\max_{\pi}\ J_R(\pi)=\mathbb{E}_\pi\!\left[\sum_t\gamma^t r_t\right]
\quad\text{s.t.}\quad
J_{C_j}(\pi)=\mathbb{E}_\pi\!\left[\sum_t\gamma^t c_{j,t}\right]\le d_j.
\]
Read this first as bookkeeping. \(J_R(\pi)\) is the expected discounted reward
of policy \(\pi\). Each \(J_{C_j}(\pi)\) is the expected discounted amount of
some cost or harm, such as privacy exposure, money spent, dangerous commands, or
manual interruptions. The bound \(d_j\) is the allowed budget for that cost. A
plain reinforcement-learning agent asks, "How much reward can I get?" A
constrained agent asks, "How much reward can I get while keeping each harm
ledger under its limit?"

The Lagrangian form
\[
\mathcal{L}(\pi,\lambda)=J_R(\pi)-\sum_j\lambda_j\big(J_{C_j}(\pi)-d_j\big)
\]
supports dual optimization and transparent trade-off tuning.

A Lagrange multiplier \(\lambda_j\) is a shadow price for violating constraint
\(j\). If privacy risk is already close to its bound, a large \(\lambda_j\)
makes risky actions look expensive; if the risk ledger is comfortably low, the
price can be smaller. Dual optimization is the process of adjusting these
prices while improving the policy. With two actions the idea is visible:
`fast_patch` yields reward 10 and harm 4, while `safe_patch` yields reward 7 and
harm 1 under a harm budget of 2. When \(\lambda=0\), fast wins. When
\(\lambda=2\), their priced values become \(10-2(4-2)=6\) and
\(7-2(1-2)=9\), so the safer action wins because scarce safety budget has
become dear.

At the state-action level, constrained Bellman structure appears as
\[
Q^\pi_\lambda(s,a)=r(s,a)-\sum_j\lambda_j c_j(s,a)+\gamma\,\mathbb{E}_{s'}[V^\pi_\lambda(s')],
\]
which makes "unsafe but high reward" mathematically explicit instead of
politically vague. Some constraints are hard: do not leak secrets, do not run a
destructive command without authorization, do not fabricate a citation. Others
are budgets: latency, cost, bounded uncertainty, allowed retry counts. The
mathematics matters because it separates prohibition from price.

## Runtime safety filter

Define safe set \(\mathcal{C}=\{x:h(x)\ge0\}\). Control barrier functions require
\[
\dot h(x,u)+\alpha(h(x))\ge0
\]
for class-\(\mathcal{K}\) function \(\alpha\), giving forward invariance of
\(\mathcal{C}\) [[52](../../references.md#ref-52)]. A practical filter solves
\[
u^\star=\arg\min_u \|u-u_{\text{nom}}\|^2
\quad\text{s.t.}\quad
\dot h(x,u)+\alpha(h(x))\ge0,
\]
so nominal autonomy is preserved when safe and corrected when not.

The notation hides a simple fence. The function \(h(x)\) measures signed
distance from danger: nonnegative means safe, negative means outside the safe
set. The dot in \(\dot h\) means derivative, the instantaneous rate at which
that safety margin is changing under control \(u\). A class-\(\mathcal{K}\)
function is an increasing function with \(\alpha(0)=0\); it lets the allowed
rate depend on how much margin remains. Forward invariance means that once the
state starts in the safe set, the filtered controller keeps future states there
under the model assumptions.

In one dimension, let \(x\) be dollars already spent and let the budget cap be
100, so \(h(x)=100-x\). At \(x=95\), a proposed action that spends 10 would push
\(h\) negative. The filter searches for the closest acceptable action, perhaps
spend 4, ask approval, or wait for more budget. The optimization above is the
formal way of saying "change the command as little as possible while preserving
the safety condition."

For language agents, the same pattern appears in less continuous clothing. The
nominal action may be "delete the database," "email this file," or "publish the
deployment." The safety filter checks state, role, data class, reversibility,
blast radius, and evidence. If the proposed action would cross a boundary, the
filter blocks it, rewrites it into a reversible alternative, or asks for human
approval.

This analogy must be used honestly. A continuous control-barrier proof does not
automatically prove that a discrete language-agent filter is safe. To get an
equally formal guarantee, the language-agent system would need its own
transition invariant: a statement showing that every permitted discrete step
preserves the safety property. Without that proof, the barrier picture is a
design pattern and a source of tests, not a borrowed certificate.

```text
proposal = policy(state)
risk = classify(proposal, state)
if forbidden(risk):
  reject(proposal)
elif requires_approval(risk):
  ask_human(proposal, evidence)
else:
  execute_with_monitor(proposal)
```

The important feature is placement. The filter stands between proposal and
effect, not between effect and apology.

## Layers of constraint

Safety architectures are layered because no single check sees the whole risk.
Static constraints remove forbidden tools or arguments before planning begins.
Pre-execution checks validate schemas, permissions, data sensitivity, and risk
class. Runtime monitors watch for drift, unsafe intermediate states, budget
exhaustion, and unexpected tool outputs. Post-action checks verify whether the
intended safety property actually held. Audit records make repair possible when
the system or organization learns that a boundary was incomplete.

Constrained MDP theory provides the expected-utility compass with explicit harm
budgets. Control barrier functions provide the model of an online filter that
preserves invariants. Governance frameworks translate institutional risk
appetite into operational envelopes that outlive any single prompt or model
version [[51](../../references.md#ref-51)] [[52](../../references.md#ref-52)]
[[29](../../references.md#ref-29)] [[53](../../references.md#ref-53)].
Together they make safety a property of the agent loop, not a promise in the
system message.

## Designing for escalation

Human escalation is not a defeat. It is a designed transition for states where
the autonomous policy should not pretend to be sovereign. The interface should
say what evidence the human receives, what decision is requested, how long the
approval remains valid, and whether the agent may continue with a safer
fallback while waiting.

Authority is therefore an allocation problem. A reversible formatting edit may
be delegated to the agent; a citation replacement may require evidence; a
secret-bearing export may require a human; a forbidden disclosure may not be
priced at all, because a hard constraint is not an expensive option. Different
tasks deserve different authority envelopes according to reversibility, blast
radius, evidence quality, time pressure, and the value of partial progress while
approval is pending. The design error is to flatten all of this into either
"the agent is autonomous" or "the human decides." An institution allocates
authority at the transition where it matters.

Evaluate these systems by reporting task return against violation probability,
dual-variable stability where constraints are optimized, blocked-action loops,
escalation latency, successful fallback rate, and incident quality under
correlated failures rather than isolated happy-path tests
[[33](../../references.md#ref-33)] [[34](../../references.md#ref-34)]. A better
agent is not the one that says it will be safe. It is the one whose forbidden
actions are blocked, whose risky tradeoffs are explicitly priced, whose
ambiguous actions escalate, whose waiting states still make useful progress
when allowed, and whose incidents generate evidence for repair.
