# Equilibria, Self-Play, and Learning Dynamics

Agents that share an environment eventually start learning from each other, and the system is never quite the same afterwards. Earlier topics designed the rules: Topic 1 (Coordination Protocols and Communication) decided who may speak, and Topic 2 (Negotiation and Mechanism Design) decided how scarce authority is handed out. The question now is whether those rules still hold once every participant has watched them operate and looked for a better move. The tools are game theory, multi-agent reinforcement learning, and self-play, all used as testing equipment rather than as decoration.

A multi-agent design is not fully described by its first successful trace. Once many interpreters share an environment, each agent can adapt to the others. The stable question is therefore not only "what did they do?" but "who could improve by doing something else after observing the rule?"

## The Protocol Trains the Agents That Run It

The same shared environment that made coordination possible now becomes the object of learning. Each interpreter updates two kinds of belief. It updates its belief about the task, and it updates its belief about the other interpreters.

That second kind of learning is easy to miss. In the publication workflow, it shows up in specific habits:

- The drafter learns which critiques block commits.
- The fact checker learns which warnings the integrator treats as decisive.
- The integrator learns which agents are calibrated, slow, strategic, or redundant.

Here "calibrated" means an agent whose stated confidence matches how often it turns out to be right. The consequence is uncomfortable and useful. The protocol is therefore a program that trains the agents who run it.

## Strategic Stability: When Nobody Wants to Deviate

### Reading a Payoff Table

The smallest strategic object is a normal-form game. That is a table listing each player's available actions and the payoff each player receives for every joint action. A payoff is just a number saying how good an outcome is for that player. There is no time axis inside the table; it is a snapshot of simultaneous choice.

A mixed strategy is a probability distribution over actions. In plain terms, the agent flips a weighted coin instead of always doing the same thing. For example, a reviewer might challenge a patch \(70\%\) of the time and approve it \(30\%\) of the time under the same visible signal.

The following table shows one such snapshot. A drafter chooses whether to submit a careful patch or a rushed patch. A checker chooses whether to inspect or skim. Each cell holds two numbers, written as \((\text{drafter},\text{checker})\): the drafter's payoff first, the checker's payoff second.

| drafter's choice | checker inspects | checker skims |
|---|---:|---:|
| drafter careful | \((3,2)\) | \((2,1)\) |
| drafter rushed | \((0,3)\) | \((4,-2)\) |

Read the corners to see the tension. When the drafter rushes and the checker skims, the drafter collects \(4\), the highest single payoff in the table, while the checker collects \(-2\). The rushed-and-skimmed cell is tempting for the drafter and bad for the collective. When the checker inspects, rushing pays the drafter \(0\) instead of \(4\), so the inspect column makes rushing less attractive. Equilibrium analysis asks which pattern survives once both roles understand this table, not which pattern looked noble in the first rehearsal.

### The Nash Condition, Stated and Read Aloud

Take a normal-form game \((N,\{A_i\},\{u_i\})\), read as "the set of players N, each player's action set A-sub-i, and each player's payoff function u-sub-i". A mixed strategy profile \(\sigma^{*}\), where \(\sigma\) now names a strategy rather than the machine state it named in Chapter 2, is Nash if no agent can improve by changing its own strategy while the others hold fixed:
\[
u_i(\sigma_i^{*},\sigma_{-i}^{*}) \ge u_i(\sigma_i,\sigma_{-i}^{*})\quad \forall i,\forall \sigma_i.
\]
Read \(\sigma_i\) as "the strategy of agent i" and \(\sigma_{-i}\) as "the strategies of everyone except agent i". The symbol \(\forall\) reads "for all". So the line says: for every agent, and for every alternative strategy that agent might try, switching alone does not raise its payoff. Nash's fixed-point result gives the central existence theorem for this kind of unilateral stability [[19](../../references.md#ref-19)].

The concept matters for agent systems because a protocol that works only before participants learn its incentives is not stable. Suppose a reviewer can gain influence by exaggerating severity. Suppose a worker can gain routing weight by overclaiming competence. In both cases the first demonstration has not tested the game the system will become.

### What Stability Looks Like in the Publication Workflow

In the publication workflow, a stable convention is not merely "the chapter was finished once." It is closer to this. After many chapters, three things hold at the same time:

1. The drafter does not gain by bypassing review.
2. The fact checker does not gain by marking every uncertainty as severe.
3. The integrator does not gain by rubber-stamping patches to reduce queue length.

Each role has a policy, meaning a rule for choosing actions, defined over what it can locally see. Those local observations include draft gaps, source quality, open critiques, time remaining, and the visible behavior of the others. Equilibrium asks whether those policies remain reasonable when the agents understand the incentives.

### Exploitability as a Robustness Metric

A useful robustness metric is exploitability:
\[
\mathcal{E}(\sigma)=\sum_i\left(\max_{\sigma_i'}u_i(\sigma_i',\sigma_{-i})-u_i(\sigma)\right).
\]
Read this as: for each agent, find the best payoff it could reach by switching strategy alone, subtract what it currently gets, then add those gaps across all agents. A tiny example: if one agent could gain \(0.3\) by deviating and another could gain \(0.0\), exploitability is \(0.3\).

In two-player zero-sum settings, where one player's gain is exactly the other's loss, zero exploitability corresponds to exact equilibrium. In general-sum agent societies, where payoffs need not cancel out, exploitability is still a valuable probe. It asks how much an entrant or deviator can gain against the current convention. To measure it in practice, train or hand-build a deviating agent and see how much extra reward it collects. Low exploitability is not the same as moral goodness, but it is evidence that the behavior is not merely held together by inattention.

## Learning While Interacting: Games That Have a State

### Markov Games Extend the Control Loop

Sequential interaction is better modeled as a Markov game. There is a shared state, each agent chooses an action, and each receives its own reward. For player \(i\) under joint policy profile \(\pi\),
\[
V_i^\pi(s)=\mathbb{E}_{a\sim \pi}\!\left[r_i(s,a)+\gamma\sum_{s'}P(s'|s,a)V_i^\pi(s')\right].
\]
Read \(V_i^\pi(s)\) as "the long-run value of state s for agent i when everyone follows the policy profile pi". Inside the brackets, \(r_i(s,a)\) is agent i's immediate reward for the joint action \(a\), \(\gamma\) is the discount factor that shrinks future value, and \(P(s'|s,a)\) is the chance of landing in next state \(s'\). Markov games extend the Bellman view of control to settings where the transition and reward consequences depend on several policies at once [[20](../../references.md#ref-20)] [[5](../../references.md#ref-5)]. Equilibrium planning therefore replaces unilateral maximization with best-response consistency: each policy must make sense against the others, not against an inert environment.

### Nobody Can See the Real State

Partial observability changes the interpretation of \(s\). No single role in the publication workflow sees the true state "chapter quality." Each sees a different slice:

- The drafter observes prose difficulty.
- The checker observes evidence strength.
- The integrator observes queue pressure and visible approvals.

A Dec-POMDP version, short for decentralized partially observable Markov decision process, would model each local observation stream explicitly. It then searches for joint policies that use messages and artifacts to coordinate under hidden quality. Exact solutions are rarely practical for rich language work. Still, the model prevents a common mistake: treating the final document as if it were the agents' shared state all along.

### Self-Play Manufactures Pressure

Self-play is one way to create such pressure. Systems like AlphaGo used repeated play and search to improve policies against increasingly strong opponents [[21](../../references.md#ref-21)]. The lesson for agentic workflows is broader than games. Run agents against copies, variants, adversaries, lazy collaborators, overconfident specialists, and strategically silent reviewers.

Two failure shapes follow directly. A debate protocol that converges with honest critics may fail when critics optimize for attention. A negotiation agent that succeeds against polite counterparts may simply have learned politeness as an environmental assumption.

### A Three-Round Regret Calculation

Before the regret formula, make the accounting painfully small. A router chooses one specialist each round: \(G\), a generalist, or \(S\), a security specialist. Payoff is \(1\) for a good route and \(0\) for a bad one. These three rounds list the task type, the router's choice, what each specialist would have earned, and what the router actually received.

```text
round  task type     router chose   payoff if G   payoff if S   received
1      prose         G              1             0             1
2      security      G              0             1             0
3      security      S              0             1             1
```

The router received \(2\) total. The best fixed action in hindsight is \(S\), also worth \(2\) on these three tasks; always choosing \(G\) would have been worth \(1\). External regret asks how much the router lost compared with the best single fixed action chosen after seeing the whole sequence. Here that difference is \(2 - 2 = 0\). That is a useful question, but it is not the only useful question.

### External Regret, Swap Regret, and Why the Difference Bites

Repeated adaptation is governed by regret:
\[
R_T^i=\max_a\sum_{t=1}^T u_i(a,a_{-i}^t)-\sum_{t=1}^T u_i(a_i^t,a_{-i}^t).
\]
Read \(R_T^i\) as "agent i's regret after T rounds": the best total payoff from one fixed action, minus the total the agent actually collected.

Two related names describe where such learning settles. In a **correlated equilibrium**, a shared signal recommends an action to each agent, and no agent gains by reinterpreting its own recommendation. A **coarse correlated equilibrium** is the weaker version: no agent gains by ignoring the signal entirely and committing to one fixed action instead.

External no-regret learning drives empirical play toward coarse correlated equilibrium sets. Correlated equilibrium requires stronger internal or swap-regret guarantees. The reason is that the deviation is not merely "always play action \(a\)" but "replace action \(a\) by action \(a'\) whenever the recommendation says \(a\)" [[65](../../references.md#ref-65)].

Swap regret asks a different question from the three-round routing example. It does not compare the router with "always \(G\)" or "always \(S\)." It compares the router with a rule for rewriting its own past recommendations: whenever the policy said \(G\) on a security-looking task, pretend it had said \(S\). Apply that swap to round 2 and the router's total rises from \(2\) to \(3\), so swap regret is positive even though external regret was zero.

This distinction is practical. A routing policy with low external regret may know that no single fixed specialist would have been better overall. It may still fail to learn that whenever it routes security incidents to a generalist, it should swap that decision to a security specialist.

### Older Dynamics, Still Diagnostic

Classical learning dynamics add more diagnostic lenses. Fictitious play studies agents that best respond to empirical frequencies of past play, that is, to how often each opponent action has appeared so far [[63](../../references.md#ref-63)]. Evolutionary game theory studies how populations of strategies grow, shrink, and stabilize under selection pressure [[64](../../references.md#ref-64)]. Both remind us that adaptation can converge, cycle, fragment, or collapse into monoculture, where every agent runs the same brittle strategy.

### Self-Play Built from Perturbations

Self-play for this workflow can be built from perturbations rather than board positions. Assemble a cast of deliberately imperfect participants:

- a drafter that sometimes overstates novelty,
- a checker that sometimes misses unsupported claims,
- an integrator under a tight deadline,
- adversarial variants that exploit the scoring rule.

Then replay the same chapter under altered budgets and message delays. If the learned convention depends on immediate critique delivery, or on a fact checker who always shares every search failure, the apparent equilibrium was partly an artifact of unrealistic observability.

## Dynamics as Tests: Metrics, Perturbations, and Repairs

### Four Quantities Worth Tracking

For builders, equilibrium analysis becomes a test discipline. Track four things:

- Exploitability: how easy is it for a new strategy to take advantage of the current protocol?
- Regret: would an agent have done better by consistently choosing a different role, message, or action?
- Diversity collapse: are all agents learning the same brittle convention?
- Hidden-quality regret, specific to the publication workflow: how often did local signals make a weak section look ready until after commit?

Then perturb payoffs, latencies, available tools, and adversary behavior, and see whether cooperation survives.

### Composition Becomes an Experiment

This is where composition stops being a slogan and becomes an experiment. A planner plus reviewer may improve quality when the reviewer has independent evidence. The same pair may create delay without insight when both inherit the same stale premise.

A negotiation rule plus reputation memory may elicit better reports; it may also teach agents which numbers to flatter. Self-play may discover robust conventions; it may also discover collusion, correlated behavior, or an incentive loophole that was invisible in isolated component scores. Topic 4 (Neural Ensembles and Orchestration) picks up that correlation problem from the side of aggregation.

Adaptation changes the task faced by every other interpreter. The question is not whether each component scored well alone, but whether the joint system remains useful after its components learn one another.

### Institutional Repairs, Not Better Speeches

When dynamics cycle, the repair is usually institutional rather than rhetorical. Add commitment rules, arbitration, memory, randomized tie-breaking, penalties for reversal, or a different mechanism. When collusion appears, change observability and rewards. When diversity collapses, preserve independent training data, model families, prompts, or evaluation routes.

The aim is not perfect harmony, which can hide suppression of useful disagreement. The aim is low exploitability, bounded regret, recoverable diversity, and stable cooperation under pressure.

Exercise: take the drafter and fact checker only. Define each action set, payoff proxy, local observation, and one possible deviation. What observation would tell you that the current review rule is an equilibrium-like convention rather than a fragile habit? A good answer names a measurable signal, such as a deviating drafter that skips review and gains nothing across many chapters, rather than a single successful run.
