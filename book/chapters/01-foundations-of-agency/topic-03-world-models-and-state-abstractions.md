# World Models and State Abstractions

A world model is a map drawn during a storm: if you sketch every raindrop, you never choose a road; if you sketch only the horizon, you drive into a lake. State abstraction is that disciplined cartography—selective forgetting in service of competent action, where elegance is measured not by compression ratio alone, but by whether the agent still reaches the right future.

## Formalization

Let the ground control problem be an MDP \((\mathcal S,\mathcal A,T,R,\gamma)\) [[4](../../references.md#ref-4)] [[5](../../references.md#ref-5)], and let \(\phi:\mathcal S\to\mathcal Z\) be an abstraction map. Exact homomorphism requires reward and transition consistency [[37](../../references.md#ref-37)]:
\[
R(s,a)=\bar R(\phi(s),a),\qquad
\sum_{s':\phi(s')=z'}T(s'\mid s,a)=\bar T(z'\mid \phi(s),a).
\]
Then planning may occur in the compressed space via
\[
\bar V^{*}(z)=\max_{a\in\mathcal A}\Big[\bar R(z,a)+\gamma\sum_{z'}\bar T(z'\mid z,a)\bar V^{*}(z')\Big],
\]
and the lifted policy \(\pi(s)=\bar\pi(\phi(s))\) preserves optimal control structure in the original system [[37](../../references.md#ref-37)]. In approximate abstractions, if reward and transition mismatches are bounded by \(\varepsilon_R\) and \(\varepsilon_P\), a standard simulation-style bound is
\[
\|V^{*}-\bar V^{*}\!\circ\phi\|_\infty \lesssim \frac{\varepsilon_R}{1-\gamma}+\frac{\gamma R_{\max}}{(1-\gamma)^2}\varepsilon_P,
\]
which makes the central bargain explicit: every saved byte must pay rent in decision quality [[37](../../references.md#ref-37)] [[39](../../references.md#ref-39)].

Bisimulation metrics refine this bargain by turning “close enough” into geometry [[38](../../references.md#ref-38)]:
\[
d(s,s')=\max_{a\in\mathcal A}\Big(|R(s,a)-R(s',a)|+\gamma\,W_d\big(T(\cdot\mid s,a),T(\cdot\mid s',a)\big)\Big),
\]
with \(W_d\) the Kantorovich lift induced by \(d\). If \(d(s,s')\) is small, the states are behaviorally interchangeable up to a quantified tolerance.

And because agents act on worlds rather than merely describing them, causal world models encode mechanism, not just association [[6](../../references.md#ref-6)]:
\[
X_i=f_i(\mathrm{Pa}(X_i),U_i),\qquad P(x_1,\dots,x_n)=\prod_i P(x_i\mid \mathrm{pa}_i),
\]
while intervention semantics replace observation with surgery:
\[
P(x_1,\dots,x_n\mid \mathrm{do}(X_j=x))=\mathbf{1}[x_j=x]\prod_{i\neq j}P(x_i\mid \mathrm{pa}_i).
\]
That is the mathematical line between “I saw this happen” and “I can make this happen.”

## Code-facing pattern: logs are archives, state is policy fuel

A practical pattern is to separate **observation logs** (high-volume, append-only) from **decision state** (small, control-sufficient summary):

```python
from dataclasses import dataclass

@dataclass
class AgentMemory:
    event_log: list[dict]          # full transcript / telemetry archive
    decision_state: dict           # compact features used by planner


def ingest(observation: dict, mem: AgentMemory) -> AgentMemory:
    mem.event_log.append(observation)
    mem.decision_state = update_belief(mem.decision_state, observation)
    return mem


def act(mem: AgentMemory):
    return policy(mem.decision_state)
```

Use the log for audit and targeted retrieval, but let the policy read only \(z_t=\psi(h_t)\), a compressed sufficient statistic. In Chapter 2’s memory controller framing (see [Memory Systems, Context, and Retrieval](../02-reasoning-architectures/topic-03-memory-systems-context-and-retrieval.md)), retrieval should be a gated action with explicit cost, not an always-on reflex.

## Cautionary case: when memory abundance became planning starvation

One common failure mode is transcript maximalism: define state as \(s'_t=(s_t,\ell_t)\), where \(\ell_t\) is a long raw interaction log, then wonder why planning quality collapses. The planner now optimizes over irrelevant detail, value estimates become noisier, and action ranking destabilizes under tiny prompt perturbations. Formally, the right requirement is conditional sufficiency,
\[
P(s_{t+1},r_t\mid h_t,a_t)=P(s_{t+1},r_t\mid z_t,a_t),\qquad z_t=\psi(h_t),
\]
not archival completeness. If your state remembers everything except what the next decision needs, you have built a luxury memory palace with no steering wheel.

## Three-theory braid

State abstraction tells us how to compress without lying to control, bisimulation metrics tell us exactly how much behavioral truth was lost in that compression, and causal modeling tells us whether the compressed model still answers intervention questions rather than merely replaying correlations; together they define a disciplined pipeline in which action is still chosen by expected utility \(a_t^{*}=\arg\max_a\mathbb E[U(a,S_t)\mid z_t]\) [[34](../../references.md#ref-34)], long-horizon consequences are propagated through Bellman recursion \(V^{*}(z)=\max_a\{\bar R(z,a)+\gamma\sum_{z'}\bar T(z'\mid z,a)V^{*}(z')\}\) [[5](../../references.md#ref-5)] [[39](../../references.md#ref-39)], and execution closes the loop through feedback laws such as \(u_t=-K\hat x_t\), where estimation and control co-govern real behavior [[36](../../references.md#ref-36)] [[41](../../references.md#ref-41)]; the moral is wonderfully unforgiving: a useful world model must be compact enough to think with, faithful enough to plan with, and causal enough to intervene with, or else the agent remains a brilliant spectator of consequences it cannot reliably shape [[37](../../references.md#ref-37)] [[38](../../references.md#ref-38)] [[6](../../references.md#ref-6)].

## How to study this formally

Benchmark abstractions by (i) value loss \(\Delta_V=\|V^{*}-\tilde V^{*}\circ\phi\|_\infty\), (ii) intervention fidelity gaps on counterfactual test sets (compare \(P(Y\mid \mathrm{do}(X=x))\) predictions to observed outcomes), and (iii) robustness under distribution shift when retrieval budgets are constrained. Then run an ablation where you increase raw memory exposure while holding task and compute fixed; if extra memory hurts return, your agent is not under-informed—it is over-narrated.
