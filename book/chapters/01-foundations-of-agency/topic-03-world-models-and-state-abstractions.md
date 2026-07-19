# World Models and State Abstractions

Belief cannot remain an ever-growing transcript. An agent that remembers every token as equally available state has not become wise; it has made planning expensive and brittle. A world model says how the world tends to change. A state abstraction says which parts of history are worth carrying into the next decision.

The design problem is selective forgetting. Forget too much and the agent loses the variables that make action competent. Retain too much and the policy drowns in irrelevant distinctions. Good abstraction is compression in service of control.

## From History to Decision State

Let the ground control problem be an MDP \((\mathcal S,\mathcal A,T,R,\gamma)\) [[4](../../references.md#ref-4)] [[5](../../references.md#ref-5)], and let \(\phi:\mathcal S\to\mathcal Z\) map detailed states to abstract states. Exact homomorphism requires reward and transition consistency [[37](../../references.md#ref-37)]:

\[
R(s,a)=\bar R(\phi(s),a),\qquad
\sum_{s':\phi(s')=z'}T(s'\mid s,a)=\bar T(z'\mid \phi(s),a).
\]

A **homomorphism** is a structure-preserving map. In ordinary programming terms, \(\phi\) is a compression function that is allowed to rename and merge states only when the merged states still behave the same way for decisions. The barred symbols \(\bar R\) and \(\bar T\) live in the abstract world \(\mathcal Z\). Thus \(\bar T(z'\mid z,a)\) means "the transition probability between abstract states after compression," while the sum on the left collects all detailed next states \(s'\) that \(\phi\) maps into the same abstract state \(z'\).

Here is a four-state coding example. Let the detailed states be \(s_1=\) "tests red because dependency missing," \(s_2=\) "tests red because dependency missing and cache stale," \(s_3=\) "tests red because behavior regressed," and \(s_4=\) "tests green." A useful abstraction might map \(\phi(s_1)=\phi(s_2)=z_D\) for dependency trouble, \(\phi(s_3)=z_B\) for behavioral bug, and \(\phi(s_4)=z_G\) for green. If the action `install_dependency` gives reward \(+3\) in both \(s_1\) and \(s_2\), and moves to \(z_G\) with probabilities \(0.80\) and \(0.78\), then merging \(s_1\) and \(s_2\) approximately preserves reward and transition. If `edit_logic` gives \(-2\) in \(s_1\) but \(+6\) in \(s_3\), collapsing \(s_1\) and \(s_3\) into a single `tests_red` state fails action preservation: the same abstract state would recommend incompatible repairs.

Under those assumptions, planning can occur in the compressed space:

\[
\bar V^{*}(z)=\max_{a\in\mathcal A}\Big[\bar R(z,a)+\gamma\sum_{z'}\bar T(z'\mid z,a)\bar V^{*}(z')\Big].
\]

The assumptions are strong. Approximate abstractions are more realistic, and their errors should be interpreted as possible value loss rather than as harmless summarization noise. A standard simulation-style bound has the shape

\[
\|V^{*}-\bar V^{*}\!\circ\phi\|_\infty \lesssim \frac{\varepsilon_R}{1-\gamma}+\frac{\gamma R_{\max}}{(1-\gamma)^2}\varepsilon_P,
\]

where \(\varepsilon_R\) and \(\varepsilon_P\) bound reward and transition mismatch [[37](../../references.md#ref-37)] [[39](../../references.md#ref-39)]. The message is practical: every compressed-away detail is acceptable only if it does not materially change the action the agent should take.

The norm \(\|\cdot\|_\infty\), called the **supremum norm** or **sup norm**, means "look at the largest absolute error over all states." The symbol \(\lesssim\) means "bounded up to a conventional constant or omitted technical factor"; it is a mathematician's compact way of saying the right-hand side controls the scale of the left-hand side. The assumptions behind the bound are doing real work: rewards must be bounded by \(R_{\max}\), the discount must satisfy \(\gamma<1\), and \(\varepsilon_R,\varepsilon_P\) must genuinely bound the abstraction's reward and transition errors. If \(\gamma\) is close to \(1\), small transition errors can echo for a long time, which is why a cheerful summary such as `repo_status: messy` is not enough for high-stakes editing.

## Logs Are Archives; State Is Policy Fuel

A useful implementation separates raw memory from decision state:

```python
from dataclasses import dataclass

@dataclass
class AgentMemory:
    event_log: list[dict]        # audit trail and retrieval source
    decision_state: dict         # compact features used by policy


def ingest(observation: dict, mem: AgentMemory) -> AgentMemory:
    mem.event_log.append(observation)
    evidence = extract_decision_relevant_features(observation)
    mem.decision_state = update_state(mem.decision_state, evidence)
    return mem


def act(mem: AgentMemory):
    return policy(mem.decision_state)
```

For a coding agent, the decision state may include failing behavior, touched files, dependency hints, test status, active constraints, unresolved hypotheses, and remaining budget. It usually does not need every line of conversation. Raw logs remain available for audit and targeted retrieval, but retrieval should be a gated action with explicit cost, as later memory systems will develop in more detail (see [Memory Systems, Context, and Retrieval](../02-reasoning-architectures/topic-03-memory-systems-context-and-retrieval.md)).

The formal requirement is conditional sufficiency:

\[
P(s_{t+1},r_t\mid h_t,a_t)=P(s_{t+1},r_t\mid z_t,a_t),\qquad z_t=\psi(h_t).
\]

This says that, for the next decision, the compressed state \(z_t\) carries the predictive information from history that matters. It does not say the archive is useless. It says the policy should not be forced to plan over the archive unless the current decision needs it. Action selection can then be interpreted as expected-utility maximization over \(z_t\), provided the abstraction preserves the distinctions that affect utility [[34](../../references.md#ref-34)].

## Behavioral and Causal Fidelity

Bisimulation metrics sharpen the idea of "close enough" by measuring whether two states behave similarly under action [[38](../../references.md#ref-38)]:

\[
d(s,s')=\max_{a\in\mathcal A}\Big(|R(s,a)-R(s',a)|+\gamma\,W_d\big(T(\cdot\mid s,a),T(\cdot\mid s',a)\big)\Big),
\]

with \(W_d\) the Kantorovich lift induced by \(d\). If \(d(s,s')\) is small, the states are interchangeable up to a quantified tolerance. If "test failed because dependency missing" and "test failed because behavior regressed" collapse into the same feature `tests_red`, the abstraction may be compact, but it is not behaviorally faithful.

A **bisimulation** asks whether two states can answer the same action questions: do they give similar immediate rewards, and do they lead to similar distributions over future states? The first term checks reward. The second term compares transition distributions. \(W_d\), the **Kantorovich lifting**, is a way to lift a distance between individual states into a distance between probability distributions over states. Intuitively, it asks how much "work" is needed to transport probability mass from one next-state distribution to the other when moving mass between unlike states is expensive. The exact transport machinery can wait; the engineering lesson cannot. If two situations lead to different repair actions, their distance should not be treated as zero merely because the same red test banner appears.

Agents also need causal fidelity when they intervene. A causal world model encodes mechanisms rather than only associations [[6](../../references.md#ref-6)]:

\[
X_i=f_i(\mathrm{Pa}(X_i),U_i),\qquad P(x_1,\dots,x_n)=\prod_i P(x_i\mid \mathrm{pa}_i).
\]

Intervention semantics replace observation with action:

\[
P(x_1,\dots,x_n\mid \mathrm{do}(X_j=x))=\mathbf{1}[x_j=x]\prod_{i\neq j}P(x_i\mid \mathrm{pa}_i).
\]

These are **structural causal equations**. Each variable \(X_i\) is produced by a function \(f_i\) of its parents \(\mathrm{Pa}(X_i)\) and background disturbance \(U_i\). The product factorization says the joint probability can be assembled from each variable given its parents. The notation \(\mathrm{do}(X_j=x)\) means an intervention: set \(X_j\) to \(x\) by action, rather than merely observing that it happened to equal \(x\). In code-agent language, observing that "tests pass after a cache clear" is not the same as knowing that clearing the cache caused the pass; perhaps the dependency install was the real mechanism.

That distinction matters for agents because they do not merely predict. They edit files, send messages, allocate resources, and call tools. "This change correlated with lower latency" is weaker than "raising worker count lowers queue latency after a delay and raises cost." A state abstraction that erases the difference between correlation and intervention will mislead control. Feedback laws such as \(u_t=-K\hat x_t\) are a reminder that the estimated state is not a report for its own sake; it is the input to correction [[36](../../references.md#ref-36)] [[41](../../references.md#ref-41)].

## Studying Abstractions

Evaluate abstractions by downstream behavior. The quality of a compression is task-dependent because different tasks preserve different distinctions. A customer-support agent may need order status, policy version, and jurisdiction, while safely ignoring the poetic texture of the complaint. A coding agent may need failing behavior, touched files, dependency state, and test scope, while ignoring most pleasantries in the transcript. A summarizer may compress away execution permissions that a deployment agent must keep in letters ten feet high.

- Value loss: \(\Delta_V=\|V^{*}-\tilde V^{*}\circ\phi\|_\infty\).
- Intervention fidelity: predicted and observed effects under controlled actions.
- Robustness under distribution shift when retrieval budgets are constrained.
- Action preservation: whether states mapped to the same \(z\) really support the same action.
- Token and latency savings: whether the smaller state reduces context size, model time, retrieval work, and tool waiting without buying those savings by erasing decision-relevant variables.

The interpreter now has a compact internal language. Topic 1 gave it a contract, Topic 2 gave it belief, and this topic gives it a state representation small enough to act on but faithful enough to trust. The remaining question is how action selection becomes governed control rather than a single eager choice.
