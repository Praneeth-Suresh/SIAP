# Memory Systems, Context, and Retrieval

Memory is policy, not pile: retain, compress, retrieve, forget. A capable agent treats context as scarce capital and allocates it with the same seriousness we reserve for money, time, and safety.

## Formal memory control problem

Let memory state be \(m_t=(w_t,e_t,s_t)\): working, episodic, and semantic stores.  
A memory controller chooses operations \(u_t \in \{\texttt{write},\texttt{compress},\texttt{retrieve},\texttt{evict}\}\) by
\[
u_t = \mu_\theta(m_t,h_t),
\]
to optimize
\[
\max_\mu\ \mathbb{E}\!\left[\sum_t \gamma^t \big(\text{task\_utility}_t - \lambda_1\text{latency}_t - \lambda_2\text{token\_load}_t\big)\right].
\]
This is expected utility under systems constraints: retrieval is good only if it improves decisions more than it costs [[33](../../references.md#ref-33)] [[34](../../references.md#ref-34)].

One useful control view is Bellman recursion on memory state:
\[
V^\star(m,h)=\max_{u}\left\{r(m,h,u)+\gamma\,\mathbb{E}[V^\star(m',h')]\right\},
\]
where \(r\) already includes latency and token penalties [[5](../../references.md#ref-5)] [[4](../../references.md#ref-4)].

## Retrieval and compression mechanics

Sparse retrieval can be represented by BM25 scoring:
\[
\mathrm{BM25}(q,d)=\sum_{t\in q}\mathrm{IDF}(t)\frac{f(t,d)(k_1+1)}{f(t,d)+k_1\left(1-b+b|d|/\mathrm{avgdl}\right)},
\]
while dense retrieval often uses inner-product similarity
\[
s(q,d)=\langle e_q,e_d\rangle.
\]
These are not rival religions; they are complementary indexing geometries with different failure modes [[46](../../references.md#ref-46)] [[15](../../references.md#ref-15)] [[47](../../references.md#ref-47)].

Compression policy is an information-theoretic trade:
\[
R(D)=\min_{p(\hat x|x):\mathbb{E}[d(X,\hat X)]\le D} I(X;\hat X),
\]
which says you should only pay bitrate for distinctions that matter to downstream decisions [[35](../../references.md#ref-35)].

For retrieval-augmented generation, evidence quality propagates to output probability:
\[
p(y\mid x)\approx \sum_{d\in\mathcal{D}_k} p_\eta(d\mid x)\,p_\theta(y\mid x,d),
\]
so poor retrieval is not a side issue; it is directly injected into generation dynamics [[14](../../references.md#ref-14)].

## Three-theory braid

Cognitive multi-store theory gives architectural separation (what kind of memory should hold what), information theory gives compression discipline (what fidelity is worth paying for), and modern retrieval theory gives operational evidence flow (how useful context is recovered in time), so memory becomes an active braid of foresight (saving what future policies will need), responsiveness (retrieving the right fragment now), and resilience (evicting stale or contaminated traces before they derail behavior) [[48](../../references.md#ref-48)] [[35](../../references.md#ref-35)] [[14](../../references.md#ref-14)] [[15](../../references.md#ref-15)] [[46](../../references.md#ref-46)] [[47](../../references.md#ref-47)].

## How to study this formally

Evaluate retrieval precision@\(k\), latency, grounded answer faithfulness, and regret from eviction decisions under fixed token budgets. Stress-test with adversarial distractors and contamination injections, then verify whether policy-level edits (not prompt cosmetics) reduce failure recurrence [[16](../../references.md#ref-16)]. If memory policy is not measurable, "long context" is often just expensive amnesia.

## Translating the Theory into Agentic Practice

Memory theory teaches that better agents are not built by pouring the past into the context window until the window groans. They are built by deciding what kind of past each future decision deserves. Working memory should hold the current control state. Episodic memory should preserve concrete events and traces. Semantic memory should store distilled patterns, policies, and domain facts. The agent's memory controller decides which store to write, query, compress, or evict.

A practical agent should therefore expose memory operations as first-class actions. `write` stores a new observation with provenance. `compress` turns bulky traces into decision-relevant summaries while retaining links to raw evidence. `retrieve` is triggered by uncertainty, task phase, or value of information. `evict` removes stale, duplicated, or harmful context from the active state. This is not clerical tidiness; it is how the agent prevents irrelevant history from becoming an unelected adviser.

Retrieval should be evaluated at the decision boundary, not merely at the document boundary. The question is not "did we retrieve something similar?" but "did the retrieved evidence change the action ranking in the right direction?" For a legal research agent, the right case is the one that changes the answer safely. For a code agent, the right file is the one that localizes the bug or rules out a tempting but false edit. For a personal assistant, the right memory is current, permissioned, and relevant to the user's actual intent.

The practical value of the theory is a memory economy. It gives us policies for spending context, metrics for retrieval quality, and defenses against contamination. A memory-rich agent without retrieval control is a library after an earthquake. A memory-governed agent is closer to a scholar: it knows what to keep on the desk, what to leave in the stacks, and when a dusty footnote is worth summoning into daylight.
