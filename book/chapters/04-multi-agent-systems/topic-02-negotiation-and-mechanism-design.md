# Negotiation and Mechanism Design

Coordination assumes that agents must fit their actions together. Negotiation adds a sharper difficulty: the agents may not value the same outcomes. Once many interpreters share an environment with scarce resources, private information, and local objectives, the system needs rules that make useful revelation and useful allocation more attractive than strategic noise.

The shared-environment view matters here because private information is not abstract decoration. It is the part of the environment bound only inside one interpreter. A drafter knows how hard a rewrite will be. A fact checker knows which claims produced thin evidence. An integrator knows the release deadline and the cost of reopening a committed section. Mechanism design asks how to build an outer evaluator whose rules make those private bindings show up in useful, checkable form.

## Mechanisms as games we choose

Start with a toy scarcity problem. There is one edit slot before release. Agent \(D\), the drafter, privately knows that using the slot for a conceptual rewrite is worth \(8\) units to final quality and costs \(3\) units of effort. Agent \(F\), the fact checker, privately knows that using the slot for citation repair is worth \(6\) units and costs \(1\). The agents' types are these private facts about value and cost. A report is what each agent tells the mechanism, such as "my edit is worth \(8\) and costs \(3\)." An allocation is the mechanism's chosen outcome: give the slot to \(D\), give it to \(F\), or use no slot. A transfer is a payoff adjustment imposed by the mechanism: money in an auction, but in agent workflows often priority, reputation, review burden, future budget, or blame.

The desiderata can be read in this tiny example. Incentive compatibility means truthful reporting should be the best policy, so \(D\) should not gain by pretending the rewrite is worth \(30\). Individual rationality means an honest participant should not be made worse off by joining, so \(F\) should not be assigned unrewarded work whose effort cost exceeds its expected benefit. Efficiency means the chosen allocation should maximize total value net of relevant costs, so the slot should go where it improves the shared artifact most, not where the loudest report points. With these words in hand, the notation is less imperial.

A mechanism is
\[
\mathcal{M}=(N,\Theta, A, g, p),
\]
with agents \(N\), type spaces \(\Theta\), outcome space \(A\), allocation rule \(g\), and transfers \(p\). A type \(\theta_i\) represents what agent \(i\) privately knows: cost, preference, skill, urgency, risk, or capacity. The mechanism asks for reports \(\hat\theta_i\), chooses an outcome \(g(\hat\theta)\), and applies transfers \(p(\hat\theta)\).

The designer usually wants some combination of incentive compatibility, individual rationality, budget feasibility, fairness, and efficiency. In the utility expression below, \(u_i(\cdot;\theta_i)\) is evaluated using agent \(i\)'s true type, even when the report is false; \(\hat\theta_{-i}\) denotes the other agents' reports. Dominant-strategy truthfulness requires that honest reporting be best for each agent regardless of the others' reports:
\[
u_i\!\big(g(\theta_i,\hat\theta_{-i}),p_i(\theta_i,\hat\theta_{-i});\theta_i\big)
\ge
u_i\!\big(g(\theta'_i,\hat\theta_{-i}),p_i(\theta'_i,\hat\theta_{-i});\theta_i\big).
\]
Efficient allocation seeks
\[
g(\hat\theta)\in\arg\max_{a\in A}\sum_i v_i(a,\hat\theta_i).
\]
Vickrey, Clarke, and Groves mechanisms show one classic way to align reported local valuations with a welfare-maximizing allocation [[57](../../references.md#ref-57)] [[58](../../references.md#ref-58)] [[59](../../references.md#ref-59)]. One canonical transfer form is
\[
p_i(\hat\theta)=h_i(\hat\theta_{-i})-\sum_{j\ne i}v_j(g(\hat\theta),\hat\theta_j),
\]
which charges each participant for the externality it imposes on the rest of the system. The sign convention here is that \(p_i\) is a payment made by agent \(i\) to the mechanism, so larger \(p_i\) lowers utility when utility is written as value minus payment. Some texts use the opposite convention, treating transfers as money received; the algebra changes sign, not substance.

The point is not that every agent workflow should implement VCG payments. The point is that a rule changes behavior by changing payoffs. In software, "payment" may be money, but it may also be priority, budget, reputation, access to tools, future routing probability, review burden, or blame assignment. A reviewer rewarded only for finding flaws will learn a different policy from a reviewer rewarded for improving final decision quality.

## Scarcity inside agent societies

Multi-agent systems allocate scarce things constantly: model calls, tool permissions, human attention, wall-clock time, memory, authority to commit a patch, or the right to answer a user. A contract-net protocol makes this operational: a manager announces a task, agents bid, the manager awards the contract, and the selected agent executes [[62](../../references.md#ref-62)]. The protocol is simple, but its quality depends on the scoring rule. If every specialist gains by saying "I can do it," bids become optimism. If bids are scored by calibrated confidence, task completion, latency, and downstream correction cost, specialists have a path to reveal competence honestly.

Return to the publication workflow. The integrator has one edit slot before release. The drafter wants the slot for a conceptual rewrite; the fact checker wants it for citation repair. Both requests are locally rational, and both are based on observations the integrator cannot directly inspect. A mechanism can ask each agent to report a tuple such as \((\text{impact},\text{risk},\text{effort},\text{evidence})\), then allocate the slot by a rule announced in advance. The evidence field is a shared artifact: it turns a private belief into an object the other interpreters can test. The effort and risk fields remain partly private, so the rule must make systematic exaggeration expensive through later scoring.

Social-choice theory marks the limits of this ambition. Gibbard-Satterthwaite style impossibility results show that broad classes of voting systems are manipulable once preferences are unrestricted and there are at least three outcomes [[60](../../references.md#ref-60)] [[61](../../references.md#ref-61)]. This does not make mechanism design futile. It prevents magical thinking. The designer must know which assumptions buy strategy-proofness, which constraints are being relaxed, and where manipulation will be measured rather than wished away.

In repeated settings, mechanism choice itself becomes sequential control:
\[
V^\star(s)=\max_m\left\{R(s,m)-\lambda\,\mathrm{manip\_risk}(m)+\gamma\,\mathbb{E}[V^\star(s')]\right\}.
\]
Expected utility supplies the local comparison among mechanisms, and dynamic programming expresses the long-run cost of creating exploitable incentives [[33](../../references.md#ref-33)] [[34](../../references.md#ref-34)] [[5](../../references.md#ref-5)]. An institution learns when it changes the rules after observing how strategic behavior exploits the old ones.

## Delegation in the publication workflow

Suppose the integrator must assign the next revision task to the drafter, fact checker, or a synthesis pass. Each agent reports a cost \(c_i\), confidence \(q_i\), expected latency \(\ell_i\), and the artifact it can produce. A naive router asks, "Who wants this?" A mechanism-aware router scores
\[
s_i = \alpha q_i-\beta c_i-\delta \ell_i-\eta\,\mathrm{correction\_rate}_i
\]
and later updates each agent's reputation from verified outcomes. This reputation router is an accountability heuristic, not a theorem of truthfulness wearing a small hat. It becomes mechanism-like only when reports are later checked against outcomes, when agents expect repeated interaction, and when the update rule makes misreporting costly enough to matter. Without verification, a reputation score can become a decoration on self-advertisement. The reports are still imperfect, but miscalibration has a cost. Confidence becomes an accountable forecast rather than a persuasive adjective.

The same structure handles communication limits. If the fact checker has only enough budget to verify three claims, the mechanism should not ask for a global truth verdict. It should ask for a prioritized claim list and a confidence interval over the unchecked remainder. In Dec-POMDP language, the mechanism is shaping which local observations become public signals. It cannot remove partial observability, but it can choose the artifacts that make later coordination less blind.

Mechanisms are not useful merely because several agents are present. If tasks
are plentiful, preferences aligned, information public, and no one has reason
to misreport, a simple queue may be better than an auction in ceremonial robes.
Mechanisms earn their keep under scarcity, private information, or incentive
conflict: one edit slot, one reviewer with rare access, one release deadline,
one agent that benefits from overstating confidence, or one budget that cannot
fund every plausible specialist. The task predicts the institution. Scarcity
asks for allocation, private information asks for elicitation, and incentive
conflict asks for rules that make useful behavior cheaper than strategic fog.

The formal evaluation should therefore include allocative efficiency, truthfulness regret, fairness across agents or users, budget balance when transfers are literal, sensitivity to collusion, and performance under strategic misreports. A negotiation protocol without incentive analysis is merely an argument with extra JSON. A useful mechanism arranges the shared environment so that local pursuit of advantage produces information the collective can actually use.
