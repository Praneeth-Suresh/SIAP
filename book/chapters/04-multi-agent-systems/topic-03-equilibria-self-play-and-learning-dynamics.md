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

> **Try this with numbers.** First let the current policy pay D-12 \(3\). Then
> test its best unilateral deviation at \(2\): \(3\ge2\), so this deviation does
> not upset equilibrium; a deviation paying \(4\) would.

Read \(\sigma_i\) as "the strategy of agent i" and \(\sigma_{-i}\) as "the strategies of everyone except agent i". The symbol \(\forall\) reads "for all". So the line says: for every agent, and for every alternative strategy that agent might try, switching alone does not raise its payoff. Nash's fixed-point result gives the central existence theorem for this kind of unilateral stability [[19](../../references.md#ref-19)]. The existence statement here assumes finitely many actions and permits mixed strategies. It does not promise an equilibrium inside an arbitrary neural policy class, nor does it tell an engineer how to find one before lunch.

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

> **Try this with numbers.** First let D-12 gain \(0.3\) by deviating and C-9
> gain \(0.1\). Then total exploitability is \(0.3+0.1=0.4\); repairing D-12's
> loophole alone lowers it only to \(0.1\).

Read this as: for each agent, find the best payoff it could reach by switching strategy alone, subtract what it currently gets, then add those gaps across all agents. A tiny example: if one agent could gain \(0.3\) by deviating and another could gain \(0.0\), exploitability is \(0.3\).

For a finite-action game evaluated over mixed strategies, every term in the sum
is nonnegative. Therefore \(\mathcal{E}(\sigma)=0\) if and only if \(\sigma\) is
a mixed Nash equilibrium—even in a general-sum game. The zero-sum case is merely
the famous special case, not the only one entitled to zero. In practice, a
best-response search may cover only a small neural policy class, so measured
"zero" means "no profitable deviation found by this search." Train or hand-build
deviating agents and report that search boundary. Low measured exploitability is
not moral goodness, but it is evidence that the convention is not held together
only by the deviations nobody bothered to try.

## Learning While Interacting: Games That Have a State

### Markov Games Extend the Control Loop

Sequential interaction is better modeled as a Markov game. There is a shared state, each agent chooses an action, and each receives its own reward. For player \(i\) under joint policy profile \(\pi\),
\[
V_i^\pi(s)=\mathbb{E}_{a\sim \pi}\!\left[r_i(s,a)+\gamma\sum_{s'}P(s'|s,a)V_i^\pi(s')\right].
\]

> **Try this with numbers.** First let immediate payoff be \(2\) and successor
> values \(6\) and \(4\) with equal probability: expected future value is \(5\).
> Then at \(\gamma=0.5\), total value is \(2+0.5(5)=4.5\).

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

### A Three-Action, Three-Round Regret Calculation

Before the regret formula, make the accounting painfully small. A router has
three actions: \(G\), the generalist; \(S\), the security specialist; and \(R\),
the release specialist. The table records the action recommended on each round,
the payoff each fixed action would have earned, and the payoff actually received.

```text
round  recommendation   payoff if G   payoff if S   payoff if R   received
1      G                0             1             0             0
2      S                0             1             0             1
3      R                1             0             1             1
```

The router receives \(0+1+1=2\). The best fixed action in hindsight is \(S\),
also worth \(1+1+0=2\), so external regret is \(2-2=0\). Yet a recommendation
rewrite that maps \(G\) to \(S\) changes only round 1 and raises the total from
\(2\) to \(3\). That is positive swap regret. The mapping keys on the
recommendation \(G\), not on a task label smuggled in after the fact.

### External Regret, Swap Regret, and Why the Difference Bites

Repeated adaptation is governed by regret:
\[
R_T^i=\max_a\sum_{t=1}^T u_i(a,a_{-i}^t)-\sum_{t=1}^T u_i(a_i^t,a_{-i}^t).
\]

> **Try this with numbers.** First let the best fixed action earn \(8\) across
> three rounds while the actual policy earns \(6\). Then regret is \(8-6=2\);
> improving the actual total to \(7\) cuts regret to \(1\).

Read \(R_T^i\) as "agent i's regret after T rounds": the best total payoff from one fixed action, minus the total the agent actually collected.

Two related names describe where such learning settles. In a **correlated equilibrium**, a shared signal recommends an action to each agent, and no agent gains by reinterpreting its own recommendation. A **coarse correlated equilibrium** is the weaker version: no agent gains by ignoring the signal entirely and committing to one fixed action instead.

External no-regret learning drives empirical play toward coarse correlated equilibrium sets. Correlated equilibrium requires stronger internal or swap-regret guarantees. The reason is that the deviation is not merely "always play action \(a\)" but "replace action \(a\) by action \(a'\) whenever the recommendation says \(a\)" [[65](../../references.md#ref-65)].

Swap regret asks a different question from fixed-action regret. It compares the
router with a function that rewrites one recommendation everywhere it occurred:
in the table, \(G\mapsto S\). A contextual rule such as "choose \(S\) on
security-looking tasks" is useful too, but it is not the swap deviation defined
here. A routing policy can therefore have zero external regret while still
leaving a profitable recommendation rewrite on the table.

### Older Dynamics, Still Diagnostic

Classical learning dynamics add more diagnostic lenses. Fictitious play studies agents that best respond to empirical frequencies of past play, that is, to how often each opponent action has appeared so far [[63](../../references.md#ref-63)]. Evolutionary game theory studies how populations of strategies grow, shrink, and stabilize under selection pressure [[64](../../references.md#ref-64)]. Both remind us that adaptation can converge, cycle, fragment, or collapse into monoculture, where every agent runs the same brittle strategy.

### Self-Play Built from Perturbations

Self-play for this workflow can be built from perturbations rather than board positions. Assemble a cast of deliberately imperfect participants:

- a drafter that sometimes overstates novelty,
- a checker that sometimes misses unsupported claims,
- an integrator under a tight deadline,
- adversarial variants that exploit the scoring rule.

Then replay the same chapter under altered budgets and message delays. If the learned convention depends on immediate critique delivery, or on a fact checker who always shares every search failure, the apparent equilibrium was partly an artifact of unrealistic observability.

## Emergent Collusion

Collusion need not begin with a secret meeting. It can emerge because two local
policies discover that hiding uncertainty earns both of them easier follow-up
tasks. D-12 reports “low uncertainty” on every draft; C-9 confirms it; R-3 rewards
the apparent speed by routing more easy work to the pair. No individual action
says “collude.” The trajectory does.

The following toy simulation is deliberately illustrative, not a claim about a
deployed model. D-12 learns "honest" versus "conceal"; C-9 learns "inspect"
versus "approve." Each maintains sample-average action values and uses
\(\epsilon=0.05\) greedy exploration for 10,000 rounds. Under the naive rule,
speed pays concealment and approval \(1.0\), while visible caution earns \(0.6\).
Under the repaired rule, honest disclosure and independent inspection earn
\(0.9\); concealment caught by inspection earns \(-1\); and an independently
audited conceal/approve event earns \(-4\). True uncertainty appears on 35
percent of rounds and independent audit on 25 percent.

```python
import random

A_D = ("honest", "conceal")
A_C = ("inspect", "approve")
ROUNDS, EPSILON = 10_000, 0.05

def choose(actions, q, rng):
    if rng.random() < EPSILON:
        return rng.choice(actions)
    best = max(q.values())
    return rng.choice([a for a in actions if q[a] == best])

def reward(rule, d, c, uncertain, audited):
    if rule == "naive":
        return (0.6 if d == "honest" else 1.0,
                0.6 if c == "inspect" else 1.0)
    d_pay = (0.9 if d == "honest" else
             -1.0 if c == "inspect" else
             -4.0 if uncertain and audited else 1.0)
    c_pay = (0.9 if c == "inspect" else
             -4.0 if d == "conceal" and uncertain and audited else 0.7)
    return d_pay, c_pay

def learn(rule, seed):
    rng = random.Random(seed)
    qd, qc = ({a: 0.0 for a in A_D}, {a: 0.0 for a in A_C})
    nd, nc = ({a: 0 for a in A_D}, {a: 0 for a in A_C})
    tail = []
    for t in range(ROUNDS):
        scenario = (rng.random() < 0.35, rng.random() < 0.25)
        d, c = choose(A_D, qd, rng), choose(A_C, qc, rng)
        rd, rc = reward(rule, d, c, *scenario)
        nd[d] += 1
        nc[c] += 1
        qd[d] += (rd - qd[d]) / nd[d]
        qc[c] += (rc - qc[c]) / nc[c]
        if t >= ROUNDS - 1_000:
            tail.append((d, c))
    target = (("conceal", "approve") if rule == "naive"
              else ("honest", "inspect"))
    return sum(pair == target for pair in tail) / len(tail)

def coalition_gain(rule, seed):
    rng = random.Random(seed)
    cases = [(rng.random() < 0.35, rng.random() < 0.25)
             for _ in range(20_000)]
    def joint(pair):
        return sum(sum(reward(rule, *pair, *case))
                   for case in cases) / len(cases)
    return joint(("conceal", "approve")) - joint(("honest", "inspect"))

for rule, seed in (("naive", 427), ("repaired", 428)):
    rate = learn(rule, seed)
    gain = coalition_gain(rule, seed + 1_000)
    print(f"{rule:8} target-pair={rate:.3f} coalition-gain={gain:+.3f}")
```

On the specified interpreter and seeds, this prints:

```text
naive    target-pair=0.958 coalition-gain=+0.800
repaired target-pair=0.944 coalition-gain=-0.944
```

In the final 1,000 rounds, the naive learners choose the collusive pair on
95.8 percent of rounds. Always colluding beats always honest/inspect by \(0.800\)
joint reward per round. After the reward repair, the learners choose
honest/inspect on 94.4 percent of the final window, and collusion loses \(0.944\)
joint reward per round. Exploration prevents either rate from reaching one; the
point is the reversal. The mechanism did not persuade the agents to become
virtuous. It removed the coalition's profit. This is specification gaming
expressed socially: the group learns whichever visible proxy pays
[[77](../../references.md#ref-77)]. The numbers are a microscope for one
mechanism, not a law of agent societies.[^toy-collusion]

### Self-Play as a Protocol Stress-Test

Self-play now has a job more useful than manufacturing theatrical debates. Make
variants of D-12, C-9, R-3, and the auditor search for profitable deviations:
strategic silence, inflated confidence, copied evidence, delayed critique, and
coalitions. Hold the task stream and seeds fixed while changing one protocol
rule. Measure exploitability, hidden-quality regret, coalition gain, audit cost,
and recovery time.

This stress-test also warns against learning from logs without inspecting how the
logs were produced. Behavioral cloning can reproduce the collusive convention
as if it were expertise [[70](../../references.md#ref-70)]. Offline reinforcement
learning can overvalue actions outside well-covered honest trajectories, so
conservative evaluation and distribution-shift checks matter
[[72](../../references.md#ref-72)] [[73](../../references.md#ref-73)]. Training
across task families may improve adaptation, but meta-learning can just as
efficiently learn the loophole shared across those families
[[74](../../references.md#ref-74)].

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

> **Skeptical Engineer:** Your fixed-seed simulation proves only that you wrote a
> fixed-seed simulation.
>
> **Author:** Correct. Its purpose is to make the incentive and repair executable.
> Evidence begins when we vary seeds, tasks, policies, and models while preserving
> the mechanism under test.

## The Assumption

Equilibrium and regret analyses assume the action sets and payoff proxies include
the deviations that matter. Self-play assumes its opponent population and task
distribution exert pressure resembling deployment, and logged outcomes reveal
the hidden quality the protocol claims to optimize.

## The Violation

The assumptions fail when coalition actions are omitted, rewards arrive before
downstream corrections, audits share the same evidence source, or all self-play
agents inherit one blind spot. Low external regret can coexist with a profitable
context-dependent swap, and low unilateral exploitability can miss a coalition
deviation entirely [[65](../../references.md#ref-65)].

## When It Fails

In the naive simulation, D-12 and C-9 learn to hide and approve because each
local speed proxy improves. The protocol has trained collusion. An audit that
merely counts incidents is not enough; the repaired mechanism links the reports
and charges verified failures back to both learners. Delay the reward until
verification, price correction burden, and include coalition policies in
self-play. Better speeches to D-12 do not change the payoff table.

## Exercise: Reproduce and Break the Collusion

Implement the simulation exactly as printed and assert both target-pair rates
and both coalition gains to three decimal places. Then extend it to 100 seeds
and at least four strategies per role. Add linked
correction costs, reputation decay, delayed rewards, and risk-weighted audits one
at a time. For each mechanism:

1. calculate unilateral exploitability and a two-agent coalition gain;
2. report bad commits, easy-task allocation, audit cost, and hidden-quality
   regret;
3. train a simple no-regret router against the strategy population;
4. introduce one unseen collusive strategy after training; and
5. identify which assumption broke when the repaired equilibrium fails.

### Further Reading and Open Questions

Nash supplies unilateral stability [[19](../../references.md#ref-19)], Markov
games supply sequential interaction [[20](../../references.md#ref-20)], and
self-play supplies adaptive pressure [[21](../../references.md#ref-21)]. Fictitious
play, evolutionary dynamics, and correlated-equilibrium learning show that
conventions may converge, cycle, or settle into broader recommendation systems
[[63](../../references.md#ref-63)] [[64](../../references.md#ref-64)]
[[65](../../references.md#ref-65)]. The open question is how to detect coalitions
whose communication is encoded in timing, artifact choice, or calibrated-looking
silence rather than explicit messages.

[^toy-collusion]: A fixed seed is not fate. It is merely a polite way to ensure
    every reviewer argues about the same imaginary disaster.
