# Neural Ensembles and Orchestration

An ensemble is useful when several imperfect interpreters make different errors. The central question is not how many voices the system can summon, but whether their diversity reduces the error that matters under the budget that exists.

In Chapter 4's recurring publication workflow, the ensemble is not just a bag of answers. It is a set of interpreters bound to different parts of the environment: the drafter to exposition and structure, the fact checker to claims and sources, the integrator to release constraints and consistency. Orchestration decides which interpreter receives which expression, which environment bindings it can see, and which side effects it may perform.

## Aggregating imperfect predictors

Given predictors \(f_k(x)\), a weighted ensemble produces
\[
\hat{y}(x)=\sum_{k=1}^{K} w_k(x)\,f_k(x),\qquad \sum_k w_k(x)=1,\ w_k(x)\ge 0.
\]
For voting systems, \(\hat{y}=\operatorname{mode}\{f_k(x)\}\). The gain comes from competent diversity: if predictors make independent or weakly correlated errors, aggregation can improve accuracy and uncertainty estimates; if they share the same blind spot, the ensemble may only make the mistake more confidently. Suppose three reviewers each have \(80\%\) accuracy and make independent errors on a binary decision. Majority vote is wrong only when at least two are wrong:
\[
{3\choose 2}(0.2)^2(0.8)+(0.2)^3=0.104.
\]
So independent majority voting raises accuracy from \(80\%\) to \(89.6\%\). Now suppose all three use the same flawed source extraction step, so their errors are perfectly correlated. When one is wrong, all are wrong, and the majority is still wrong \(20\%\) of the time. Three voices have produced one error with a choir robe. Deep ensembles are valuable partly because independently trained predictors can improve calibration and predictive uncertainty [[26](../../references.md#ref-26)]. Classical ensemble methods make the same theme explicit: diversity matters only when the individual models remain useful [[67](../../references.md#ref-67)].

Mixture-of-experts systems add conditional computation. A router \(g(x)\) chooses which experts to activate for an input, rather than paying for every expert every time. Confidence-weighted routing can use softmax gates
\[
w_k(x)=\frac{\exp(g_k(x)/\tau)}{\sum_j \exp(g_j(x)/\tau)},
\]
or sparse top-\(k\) routing
\[
E(x)=\operatorname{TopK}(g(x),k).
\]
The softmax temperature \(\tau\) controls how sharp the routing distribution is. Small \(\tau\) makes the largest gate score dominate; large \(\tau\) spreads weight more evenly. Top-\(k\) routing means "activate only the \(k\) highest-scoring experts," such as the two best specialists out of sixteen, and give the rest no computation for this input. Routing entropy measures how spread out the router's choices are,
\[
H(w)=-\sum_k w_k\log w_k,
\]
so low entropy means the router almost always chooses the same expert, while high entropy means it distributes work broadly. Early adaptive mixtures of local experts introduced this divide-and-route pattern [[68](../../references.md#ref-68)]. Sparsely gated MoE layers and Switch Transformers show how the same principle can scale neural computation by activating only a small subset of experts per input [[25](../../references.md#ref-25)] [[69](../../references.md#ref-69)].

## From neural experts to agent societies

The analogy between neural ensembles and multi-agent societies is useful but limited. It is useful because both systems depend on specialization, routing, aggregation, calibration, and correlated-error control. A coding workflow may route architecture questions to a design reviewer, risky edits to a safety reviewer, failing tests to a debugger, and final synthesis to an integrator. A research workflow may combine retrieval, statistical critique, domain expertise, and writing. Surveys of LLM-based multi-agent systems describe many such patterns at the workflow level [[23](../../references.md#ref-23)].

The analogy breaks when we forget that agents are not just differentiable submodules inside one loss function. A differentiable module is a component whose outputs change smoothly enough with respect to its parameters that gradient descent can assign credit through it. Neural experts usually share training infrastructure, optimization objectives, and a tightly specified interface. Agent societies may use tools, memory, permissions, natural language, human escalation, and changing local objectives. They can misunderstand instructions, strategically shape reports, duplicate hidden sources, or alter the environment while the router is still deciding. Minsky's "society of mind" is a suggestive metaphor for intelligence built from many smaller processes, not a license to treat every committee as a well-calibrated MoE layer [[27](../../references.md#ref-27)].

This distinction changes the orchestration problem. A neural router mostly selects computation. An agentic router selects computation plus authority, information exposure, side effects, latency, and incentive pressure. The orchestration layer should therefore maintain expert profiles: domain strengths, historical accuracy, calibration, latency, cost, permissions, failure modes, and correlation with other experts. The aggregator should combine outputs by confidence, evidence, role, independence, and past reliability. The monitor should watch for collapse: one expert always dominates, all experts cite the same weak source, critics converge into ceremony, or routing entropy falls because the system has learned convenience rather than competence.

The router itself is another partial observer. It sees task metadata, past scores, queue length, and visible artifacts; it may not see the drafter's uncertainty, the fact checker's failed searches, or a subtle inconsistency until someone emits the right message. Good orchestration therefore exposes structured summaries, claim inventories, confidence reports, and provenance trails. These artifacts are not paperwork. They are the shared environment that lets separately specialized interpreters approximate a joint belief.

## Budgeted orchestration

Specialist dispatch is a sequential decision problem:
\[
V^\star(s)=\max_a\left\{R(s,a)-\lambda_c C(a)-\lambda_l L(a)+\gamma\,\mathbb{E}[V^\star(s')]\right\},
\]
where \(a\) chooses which experts or agents to consult, \(C\) is monetary or compute cost, and \(L\) is latency. Expected utility and dynamic programming give the formal discipline behind the obvious engineering rule: "call everyone" is not sophistication when the marginal expert mostly adds delay, contradiction, or correlated noise [[33](../../references.md#ref-33)] [[34](../../references.md#ref-34)] [[5](../../references.md#ref-5)].

A useful orchestration loop has four steps. First, estimate task features and
uncertainty: domain, coupling, reversibility, freshness, evidence availability,
permission class, and tolerance for delay. Second, route to a small set of
specialists whose errors are likely to be different. Third, aggregate with
calibration rather than rank or verbosity. Fourth, update the profiles from
verified outcomes. In the publication workflow, that might mean routing a new
section to the drafter, extracting claims for the fact checker, routing only
unresolved conflicts to the integrator, and storing the final patch plus the
evidence trail as training data for future routing. The objective is not maximal
committee size; it is minimal correlated error for a fixed budget.

Decentralized uncertainty is the hard case for ensembles. If the drafter and fact checker both inherit the same mistaken premise from the outline, their agreement should not be counted as independent evidence. If the fact checker cannot reveal a source because of access limits, the aggregator should distinguish "verified false," "not verified," and "verified but not shareable." Dec-POMDP reasoning sits behind these engineering choices: route actions are communication actions, artifacts are public observations, and expert calls are costly attempts to reduce uncertainty in the joint policy.

Evaluation should report ensemble lift over the best single expert, calibration
under distribution shift, routing entropy, expert utilization balance,
disagreement quality, stale-artifact rate, provenance diversity,
correlated-error interactions, permission denials, stopping accuracy, and
cost-latency-normalized utility. Distribution shift means the future inputs no
longer come from the same pattern as the examples used to train, tune, or score
the router: yesterday's fact checks were biomedical citations, today's are legal
claims, and the old confidence calibration may now be a charming historical
artifact. A successful agent society is not merely louder than its members. It
is a routed ensemble whose disagreements contain information, whose redundancy
buys fault tolerance, and whose final decision is better than the most confident
participant acting alone.

The book's arc now folds back to the single interpreter. Chapter 1 gave us a
loop that observes, updates, chooses, and acts. Chapter 4 has not replaced that
loop with a parliament of mist. It has shown how to place many such loops in one
environment and make their interaction explicit: protocols for messages,
mechanisms for incentives, dynamics for adaptation, and ensembles for error
reduction. The institution is still an interpreter, but its registers are
distributed across agents, artifacts, and logs. To build it well is to route by
the task's real features, buy ensemble lift only when independence exists, watch
for correlated errors and altered incentives, account for cost, latency, and
permission, and stop when another call would add ceremony rather than control.
The smallest sufficient institution for the task is the one whose collective
computation remains legible enough that wisdom, when it appears, is not mistaken
for accident.
