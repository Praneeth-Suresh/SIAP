# Equilibria, Self-Play, and Learning Dynamics

A multi-agent design is not fully described by its first successful trace. Once many interpreters share an environment, each agent can adapt to the others. The stable question is therefore not only "what did they do?" but "who could improve by doing something else after observing the rule?"

The same shared environment that made coordination possible now becomes the object of learning. Each interpreter updates not only its belief about the task, but its belief about the other interpreters. The drafter learns which critiques block commits. The fact checker learns which warnings the integrator treats as decisive. The integrator learns which agents are calibrated, slow, strategic, or redundant. The protocol is therefore a program that trains the agents who run it.

## Strategic stability

The smallest strategic object is a normal-form game: a table that lists each player's available actions and the payoff each player receives for every joint action. There is no time axis inside the table; it is a snapshot of simultaneous choice. A mixed strategy is a probability distribution over actions, as when a reviewer challenges a patch \(70\%\) of the time and approves \(30\%\) of the time under the same visible signal.

For example, suppose a drafter chooses whether to submit a careful patch or a rushed patch, while a checker chooses whether to inspect or skim. Payoffs are written as \((\text{drafter},\text{checker})\):

| | checker inspects | checker skims |
|---|---:|---:|
| drafter careful | \((3,2)\) | \((2,1)\) |
| drafter rushed | \((0,3)\) | \((4,-2)\) |

The rushed-and-skimmed cell is tempting for the drafter and bad for the collective; the inspect column makes rushing less attractive. Equilibrium analysis asks which pattern survives once both roles understand this table, not which pattern looked noble in the first rehearsal.

In a normal-form game \((N,\{A_i\},\{u_i\})\), a mixed strategy profile \(\sigma^{*}\) is Nash if no agent can improve by changing its own strategy while the others hold fixed:
\[
u_i(\sigma_i^{*},\sigma_{-i}^{*}) \ge u_i(\sigma_i,\sigma_{-i}^{*})\quad \forall i,\forall \sigma_i.
\]
Nash's fixed-point result gives the central existence theorem for this kind of unilateral stability [[19](../../references.md#ref-19)]. The concept matters for agent systems because a protocol that works only before participants learn its incentives is not stable. If a reviewer can gain influence by exaggerating severity, or a worker can gain routing weight by overclaiming competence, the first demonstration has not tested the game the system will become.

In the publication workflow, a stable convention is not merely "the chapter was finished once." It is closer to this: after many chapters, the drafter does not gain by bypassing review, the fact checker does not gain by marking every uncertainty as severe, and the integrator does not gain by rubber-stamping patches to reduce queue length. Each role has a policy over local observations: draft gaps, source quality, open critiques, time remaining, and the visible behavior of the others. Equilibrium asks whether those policies remain reasonable when the agents understand the incentives.

A useful robustness metric is exploitability:
\[
\mathcal{E}(\sigma)=\sum_i\left(\max_{\sigma_i'}u_i(\sigma_i',\sigma_{-i})-u_i(\sigma)\right).
\]
In two-player zero-sum settings, zero exploitability corresponds to exact equilibrium. In general-sum agent societies, exploitability is still a valuable probe: it asks how much an entrant or deviator can gain against the current convention. Low exploitability is not the same as moral goodness, but it is evidence that the behavior is not merely held together by inattention.

## Learning while interacting

Sequential interaction is better modeled as a Markov game, where the state is shared, each agent chooses an action, and each receives its own reward. For player \(i\) under joint policy profile \(\pi\),
\[
V_i^\pi(s)=\mathbb{E}_{a\sim \pi}\!\left[r_i(s,a)+\gamma\sum_{s'}P(s'|s,a)V_i^\pi(s')\right].
\]
Markov games extend the Bellman view of control to settings where the transition and reward consequences depend on several policies at once [[20](../../references.md#ref-20)] [[5](../../references.md#ref-5)]. Equilibrium planning replaces unilateral maximization with best-response consistency: each policy must make sense against the others, not against an inert environment.

Partial observability changes the interpretation of \(s\). No single role in the publication workflow sees the true state "chapter quality." The drafter observes prose difficulty, the checker observes evidence strength, and the integrator observes queue pressure and visible approvals. A Dec-POMDP version would model each local observation stream explicitly and search for joint policies that use messages and artifacts to coordinate under hidden quality. Exact solutions are rarely practical for rich language work, but the model prevents a common mistake: treating the final document as if it were the agents' shared state all along.

Self-play is one way to create such pressure. Systems like AlphaGo used repeated play and search to improve policies against increasingly strong opponents [[21](../../references.md#ref-21)]. The lesson for agentic workflows is broader than games: run agents against copies, variants, adversaries, lazy collaborators, overconfident specialists, and strategically silent reviewers. A debate protocol that converges with honest critics may fail when critics optimize for attention. A negotiation agent that succeeds against polite counterparts may simply have learned politeness as an environmental assumption.

Before the regret formula, make the accounting painfully small. A router chooses one specialist each round: \(G\), a generalist, or \(S\), a security specialist. Payoff is \(1\) for a good route and \(0\) for a bad one.

```text
round  task type     router chose   payoff if G   payoff if S   received
1      prose         G              1             0             1
2      security      G              0             1             0
3      security      S              0             1             1
```

The router received \(2\) total. The best fixed action in hindsight is \(S\), also worth \(2\) on these three tasks; always choosing \(G\) would have been worth \(1\). External regret asks how much the router lost compared with the best single fixed action chosen after seeing the whole sequence. That is a useful question, but it is not the only useful question.

Repeated adaptation is governed by regret:
\[
R_T^i=\max_a\sum_{t=1}^T u_i(a,a_{-i}^t)-\sum_{t=1}^T u_i(a_i^t,a_{-i}^t).
\]
External no-regret learning drives empirical play toward coarse correlated equilibrium sets. Correlated equilibrium requires stronger internal or swap-regret guarantees, because the deviation is not merely "always play action \(a\)" but "replace action \(a\) by action \(a'\) whenever the recommendation says \(a\)" [[65](../../references.md#ref-65)]. Swap regret asks a different question from the three-round calculation above. It does not compare the router with "always \(G\)" or "always \(S\)." It compares the router with a rule for rewriting its own past recommendations: whenever the policy said \(G\) on a security-looking task, pretend it had said \(S\). This distinction is practical. A routing policy with low external regret may know that no single fixed specialist would have been better overall; it may still fail to learn that whenever it routes security incidents to a generalist, it should swap that decision to a security specialist.

Classical learning dynamics add more diagnostic lenses. Fictitious play studies agents that best respond to empirical frequencies of past play [[63](../../references.md#ref-63)]. Evolutionary game theory studies how populations of strategies grow, shrink, and stabilize under selection pressure [[64](../../references.md#ref-64)]. Both remind us that adaptation can converge, cycle, fragment, or collapse into monoculture.

Self-play for this workflow can be built from perturbations rather than board positions. Run a drafter that sometimes overstates novelty, a checker that sometimes misses unsupported claims, an integrator under a tight deadline, and adversarial variants that exploit the scoring rule. Then replay the same chapter under altered budgets and message delays. If the learned convention depends on immediate critique delivery or on a fact checker who always shares every search failure, the apparent equilibrium was partly an artifact of unrealistic observability.

## Dynamics as tests

For builders, equilibrium analysis becomes a test discipline. Track
exploitability: how easy is it for a new strategy to take advantage of the
current protocol? Track regret: would an agent have done better by consistently
choosing a different role, message, or action? Track diversity collapse: are all
agents learning the same brittle convention? In the publication workflow, also
track hidden-quality regret: how often did local signals make a weak section
look ready until after commit? Perturb payoffs, latencies, available tools, and
adversary behavior, then see whether cooperation survives.

This is where composition stops being a slogan and becomes an experiment. A
planner plus reviewer may improve quality when the reviewer has independent
evidence; the same pair may create delay without insight when both inherit the
same stale premise. A negotiation rule plus reputation memory may elicit better
reports; it may also teach agents which numbers to flatter. Self-play may
discover robust conventions; it may also discover collusion, correlated
behavior, or an incentive loophole that was invisible in isolated component
scores. Adaptation changes the task faced by every other interpreter. The
question is not whether each component scored well alone, but whether the joint
system remains useful after its components learn one another.

When dynamics cycle, the repair is usually institutional rather than rhetorical. Add commitment rules, arbitration, memory, randomized tie-breaking, penalties for reversal, or a different mechanism. When collusion appears, change observability and rewards. When diversity collapses, preserve independent training data, model families, prompts, or evaluation routes. The aim is not perfect harmony, which can hide suppression of useful disagreement. The aim is low exploitability, bounded regret, recoverable diversity, and stable cooperation under pressure.

Exercise: take the drafter and fact checker only. Define each action set, payoff proxy, local observation, and one possible deviation. What observation would tell you that the current review rule is an equilibrium-like convention rather than a fragile habit?
