# Safety Constraints and Guardrails

Between what an agent wants to do and what the world actually suffers stands a
layer of machinery. That machinery is what we build here. We will price harm
with numbers, fence the state with an inequality, and decide who is allowed to
sign off on what. The reward for reading carefully is a safety story you can
test, not merely recite.

Safety is not a postscript to capability. It is the part of the interpreter that
decides which proposed transitions are outside the program's charter, which are
allowed but costly, and which require another authority before the world may be
changed. A *transition* here is one step of the agent loop: the move from the
current state to the next state. In a tool-using system, safety lives at the same
boundary as action. That boundary sits between the model's proposed next step and
the external effect that would make that step real.

Agent-427 enters this topic with three new proposal forms—`write`, `test`, and
`deploy`—and zero new entitlement to make their outcomes true by assertion. A
proposal still faces evidence, authority, and state guards. This is fortunate,
because its working belief has just been corrupted by stale telemetry and a
legacy scale-out summary.

This makes guardrails more than warning text. A guardrail is a filter on the
agent's transition system, meaning the set of steps the agent is able to take at
all. Such a filter has four moves available:

- remove an action from the action space, so the agent cannot even propose it;
- reshape the action into a safer one;
- pause for human approval;
- attach an obligation to monitor what happens next.

## Constrained Control Formulation

### Rewarding the Agent While Capping Its Harm

Start with the ordinary picture of a decision-making agent and then add ledgers
for harm. Model policy selection as a constrained MDP (Markov decision process,
the standard model of an agent choosing actions in states over time):
\[
\max_{\pi}\ J_R(\pi)=\mathbb{E}_\pi\!\left[\sum_t\gamma^t r_t\right]
\quad\text{s.t.}\quad
J_{C_j}(\pi)=\mathbb{E}_\pi\!\left[\sum_t\gamma^t c_{j,t}\right]\le d_j.
\]

> **Try this with numbers.** First let a two-step policy earn rewards \(8\) and
> \(4\) with \(\gamma=0.5\): return is \(8+0.5(4)=10\). Then let its harm costs
> be \(3\) and \(2\): discounted harm is \(3+0.5(2)=4\), so a budget \(d=3\)
> rejects the otherwise attractive policy.

Read this first as bookkeeping. \(J_R(\pi)\) reads "the expected discounted
reward earned by policy \(\pi\)", where a policy is the agent's rule for choosing
actions, and *discounted* means later rewards count a little less. Each
\(J_{C_j}(\pi)\) reads "the expected discounted amount of harm number \(j\)".
Those harms are concrete: privacy exposure, money spent, dangerous commands, or
manual interruptions. The bound \(d_j\) is the allowed budget for that cost, and
"s.t." reads "subject to".

The contrast is the whole point. A plain reinforcement-learning agent asks, "How
much reward can I get?" A constrained agent asks, "How much reward can I get
while keeping each harm ledger under its limit?"

That constrained objective is dense with notation, so the following table gives
each symbol a short reading before we use it again.

| Symbol | How to read it |
|---|---|
| \(\pi\) | The policy: the agent's rule for choosing actions |
| \(J_R(\pi)\) | Expected discounted reward under that policy |
| \(J_{C_j}(\pi)\) | Expected discounted amount of harm \(j\) |
| \(d_j\) | The budget allowed for harm \(j\) |
| \(\lambda_j\) | The price charged for one unit of harm \(j\) |
| \(h(x)\) | Safety margin at state \(x\); nonnegative means safe |

### Turning Constraints into Prices

The Lagrangian form, which folds a constraint into the objective by charging a
price for breaking it,
\[
\mathcal{L}(\pi,\lambda)=J_R(\pi)-\sum_j\lambda_j\big(J_{C_j}(\pi)-d_j\big)
\]

> **Try this with numbers.** First take reward \(10\), harm \(4\), budget \(2\),
> and price \(\lambda=2\). Then the priced objective is
> \(10-2(4-2)=6\); a safer policy worth \(7-2(1-2)=9\) wins.

supports dual optimization and transparent trade-off tuning.

A Lagrange multiplier \(\lambda_j\) is a shadow price for violating constraint
\(j\). If privacy risk is already close to its bound, a large \(\lambda_j\) makes
risky actions look expensive. If the risk ledger is comfortably low, the price
can be smaller. Dual optimization is the process of adjusting these prices while
improving the policy; a builder implements it as a slow feedback loop that raises
a price whenever the measured ledger creeps over budget.

With two actions the idea is visible. Suppose `fast_patch` yields reward 10 and
harm 4, while `safe_patch` yields reward 7 and harm 1 under a harm budget of 2.
When \(\lambda=0\), fast wins, since 10 beats 7 and harm is free. When
\(\lambda=2\), their priced values become \(10-2(4-2)=6\) and \(7-2(1-2)=9\), so
the safer action wins because scarce safety budget has become dear. Notice that
`safe_patch` is rewarded for coming in under budget.

### Prohibition Is Not the Same as Price

At the state-action level, constrained Bellman structure appears as
\[
Q^\pi_\lambda(s,a)=r(s,a)-\sum_j\lambda_j c_j(s,a)+\gamma\,\mathbb{E}_{s'}[V^\pi_\lambda(s')],
\]

> **Try this with numbers.** First price immediate reward \(9\), harm \(2\) at
> \(\lambda=1.5\): the immediate term is \(9-3=6\). Then add future value \(8\)
> discounted by \(0.5\): \(Q=6+4=10\).

which reads "the priced value of taking action \(a\) in state \(s\) is its reward
minus its priced harms, plus the discounted value of wherever it lands you". This
makes "unsafe but high reward" mathematically explicit instead of politically
vague.

Some constraints are hard: do not leak secrets, do not run a destructive command
without authorization, do not fabricate a citation. Others are budgets: latency,
cost, bounded uncertainty, allowed retry counts. The mathematics matters because
it separates prohibition from price. Hard constraints belong in the action space
as removals; budgets belong in the objective as costs.

## Runtime Safety Filter

### A Fence Written as an Inequality

Define safe set \(\mathcal{C}=\{x:h(x)\ge0\}\). Control barrier functions require
\[
\dot h(x,u)+\alpha(h(x))\ge0
\]

> **Try this with numbers.** First let the remaining safety margin be \(h=5\)
> and choose \(\alpha(h)=0.5h=2.5\). Then a command with
> \(\dot h=-2\) passes because \(-2+2.5=0.5\ge0\); one with \(\dot h=-4\)
> fails because the sum is \(-1.5\).

for class-\(\mathcal{K}\) function \(\alpha\), giving forward invariance of
\(\mathcal{C}\) [[52](../../references.md#ref-52)]. A practical filter solves
\[
u^\star=\arg\min_u \|u-u_{\text{nom}}\|^2
\quad\text{s.t.}\quad
\dot h(x,u)+\alpha(h(x))\ge0,
\]

> **Try this with numbers.** First let the nominal spend be \(10\) while only
> \(5\) units of budget remain. Then compare allowed spends \(4\) and \(1\):
> squared deviations are \((4-10)^2=36\) and \((1-10)^2=81\), so the filter
> selects \(4\), the nearest safe command.

so nominal autonomy is preserved when safe and corrected when not. Here
\(u_{\text{nom}}\) is the control the agent nominally wanted, and \(u^\star\) is
the nearest control that still satisfies the safety condition.

The notation hides a simple fence. The function \(h(x)\) measures signed distance
from danger: nonnegative means safe, negative means outside the safe set. The dot
in \(\dot h\) means derivative, the instantaneous rate at which that safety
margin is changing under control \(u\). A class-\(\mathcal{K}\) function is an
increasing function with \(\alpha(0)=0\); it lets the allowed rate depend on how
much margin remains. Forward invariance means that once the state starts in the
safe set, the filtered controller keeps future states there under the model
assumptions.

### A One-Dimensional Budget Example

In one dimension, let \(x\) be dollars already spent and let the budget cap be
100, so \(h(x)=100-x\). At \(x=95\), the margin is \(h=5\). A proposed action
that spends 10 would push \(h\) negative, to \(-5\). The filter searches for the
closest acceptable action, perhaps spend 4, ask approval, or wait for more
budget. The minimization is the formal way of saying "change the command as
little as possible while preserving the safety condition."

### The Same Pattern for Language Agents

For language agents, the same pattern appears in less continuous clothing. The
nominal action may be "delete the database," "email this file," or "publish the
deployment." The safety filter checks state, role, data class, reversibility,
blast radius, and evidence. If the proposed action would cross a boundary, the
filter blocks it, rewrites it into a reversible alternative, or asks for human
approval.

This analogy must be used honestly. A continuous control-barrier proof does not
automatically prove that a discrete language-agent filter is safe. To get an
equally formal guarantee, the language-agent system would need its own transition
invariant: a statement showing that every permitted discrete step preserves the
safety property. Without that proof, the barrier picture is a design pattern and
a source of tests, not a borrowed certificate.

The safety filter has four branches: propose, classify the
risk, then reject, escalate, or execute under monitoring.

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

### Agent-427 Meets the Filter

The write proposal changes a bounded Markdown range and passes a diff guard. The
test proposal runs a deterministic check and passes a read-only tool contract.
The deploy proposal is different. It arrives while the queue estimate is
provisional, a previous scale effect remains unresolved, and no independent
health observation has arrived:

```text
proposal: deploy(revision="chapter-3", service="book-site")
belief: queue=72.5, status="provisional"
evidence: [telemetry(stale), queue-api(fresh), legacy-summary(unversioned)]
pending_effects: [scale-workers-204]
guard results:
  schema_ok = true
  authority_ok = false
  independent_health = false
  contradictory_evidence = true
decision: block(reason="unsupported effect")
next: timeout(scale-workers-204), probe(health), escalate_if_unresolved
```

The block is not punishment for uncertainty. It is the correct transition for
uncertainty attached to an irreversible effect. Agent-427 may continue the
reversible write/test path while deployment authority waits for evidence.

## Adversarial Sensors and Actuators

A safety filter that trusts the same channel for command and confirmation has
built a courtroom where the defendant is also the bailiff. A poisoned sensor may
forge a green health check. A spoofed actuator may return `success=true` without
changing the deployment. A replay attacker may resend yesterday's signed success
after today's failed rollout.

Defenses bind evidence to action identity, state version, timestamp, and an
independent observation path. High-impact actions use keyed requests, signed
receipts, monotonic revision numbers, and postconditions checked through a sensor
that the actuator does not control. If those checks disagree, the interpreter
enters `effect_unknown`, freezes retries, and escalates. It does not average a
green lie with a red truth until the dashboard looks pleasantly beige.

Adversarial inputs also target policy text. Tool output is data even when it says
“disable the guardrail.” External enforcement keeps permissions and invariants
outside the text channel that an attacker can edit. This is the practical union
of control barriers, governance, and concrete AI-safety failure analysis
[[52](../../references.md#ref-52)] [[53](../../references.md#ref-53)]
[[77](../../references.md#ref-77)].

## Layers of Constraint

Safety architectures are layered because no single check sees the whole risk.
Each layer watches a different moment in the loop:

- Static constraints remove forbidden tools or arguments before planning begins.
- Pre-execution checks validate schemas, permissions, data sensitivity, and risk
  class.
- Runtime monitors watch for drift, unsafe intermediate states, budget
  exhaustion, and unexpected tool outputs.
- Post-action checks verify whether the intended safety property actually held.
- Audit records make repair possible when the system or organization learns that
  a boundary was incomplete.

Three bodies of theory supply these layers. Constrained MDP theory provides the
expected-utility compass with explicit harm budgets. Control barrier functions
provide the model of an online filter that preserves invariants. Governance
frameworks translate institutional risk appetite into operational envelopes that
outlive any single prompt or model version
[[51](../../references.md#ref-51)] [[52](../../references.md#ref-52)]
[[29](../../references.md#ref-29)] [[53](../../references.md#ref-53)].
Together they make safety a property of the agent loop, not a promise in the
system message. Topic 3 (Embodiment: Sensors, Actuators, and Feedback) supplies
the sensing and feedback machinery that these monitors depend on.

## Designing for Escalation

### Handing a Decision to a Human on Purpose

Human escalation is not a defeat. It is a designed transition for states where
the autonomous policy should not pretend to be sovereign. The interface should
answer four questions:

- what evidence the human receives;
- what decision is requested;
- how long the approval remains valid;
- whether the agent may continue with a safer fallback while waiting.

### Allocating Authority Action by Action

Authority is therefore an allocation problem. A reversible formatting edit may be
delegated to the agent. A citation replacement may require evidence. A
secret-bearing export may require a human. A forbidden disclosure may not be
priced at all, because a hard constraint is not an expensive option.

Different tasks deserve different authority envelopes according to
reversibility, blast radius, evidence quality, time pressure, and the value of
partial progress while approval is pending. Topic 1 (Tool Interfaces and Function
Calling) describes the contracts these envelopes attach to. The design error is
to flatten all of this into either "the agent is autonomous" or "the human
decides." An institution allocates authority at the transition where it matters.

### Measuring Whether the Guardrails Work

Evaluate these systems by reporting task return against violation probability,
dual-variable stability where constraints are optimized, blocked-action loops,
escalation latency, successful fallback rate, and incident quality under
correlated failures rather than isolated happy-path tests
[[33](../../references.md#ref-33)] [[34](../../references.md#ref-34)]. Read that
list as a dashboard: reward on one axis, violations on the other, with the
awkward operational numbers beside them.

A better agent is not the one that says it will be safe. It is the one whose
forbidden actions are blocked, whose risky tradeoffs are explicitly priced, whose
ambiguous actions escalate, whose waiting states still make useful progress when
allowed, and whose incidents generate evidence for repair.

> **Skeptical Engineer:** If the sensor and actuator may both lie, have we not
> simply moved the problem into the safety layer?
>
> **Author:** We have moved authority into several independently testable layers.
> Safety is not omniscience; it is the refusal to let one unverified story become
> an irreversible effect.

## The Assumption

Constrained optimization assumes rewards and costs represent the outcomes that
matter. Barrier-style filtering assumes the state estimate and dynamics are good
enough for the inequality to predict safety. Discrete language-agent guards
assume every effectful route passes through enforcement and postconditions can
be checked independently.

## The Violation

The assumptions fail when reward omits a harm, a sensor is poisoned, an actuator
spoofs success, a shell escape bypasses the policy engine, or the model treats a
continuous-control analogy as a certificate for discrete tool behavior. They
also fail under correlated evidence: three green checks copied from one corrupt
source are one check, not a quorum.

## When It Fails

Agent-427's deploy proposal offers a darkly attractive bargain: fast completion,
no waiting cost, and an unverified green response from the deployment adapter.
A reward-only policy ships. The governed interpreter blocks because effect
authority is absent, evidence conflicts, and the previous scale action has timed
out unresolved. If the adapter later proves it changed nothing, the incident is
an actuator-spoofing failure; if it changed production but lost the response, it
is an ambiguous-effect failure. Both demand ledger inspection before retry.

The larger warning is reward misspecification. A deployment agent rewarded only
for speed can deploy an empty container and celebrate the fastest rollout in
company history. The metric improved; the service disappeared. Safety ledgers,
hard postconditions, and independent health checks prevent that joke from
becoming an incident.[^empty-container]

## Exercise: Implement the Fail-Closed Filter

Build a Python safety filter around mock `write`, `test`, and `deploy` adapters.
Represent proposal, permission, evidence, pending effects, cost ledgers, and
postconditions as typed values. Then write deterministic tests that:

1. admit a bounded write and a read-only test;
2. block Agent-427's deployment while the scale effect is unresolved;
3. inject a forged green sensor, a replayed receipt, and an actuator that reports
   success without changing state;
4. assert that contradictions produce `effect_unknown`, freeze new-key retries,
   and preserve every raw observation;
5. allow deployment only after an independent sensor confirms the keyed effect;
6. run 1,000 seeded trajectories and report reward, violation rate, false blocks,
   escalation latency, and unsafe effects.

The implementation fails if prompt text can bypass the filter or if silence,
timeout, and success share the same state.

[^empty-container]: The container is admirably small, starts instantly, and
    serves no traffic. Every metric is green except the one a customer would
    recognize.
