# Retrieval-Augmented Tooling

Retrieval-augmented tooling is not "ask search then hope"; it is a policy for buying evidence when ignorance is expensive.

## Probabilistic retrieval-generation pipeline

For query context \(x\), retrieved document \(d\), and answer \(y\):
\[
p(y\mid x) = \sum_{d \in \mathcal{D}} p(y\mid x,d)\,p(d\mid x).
\]
Operationally, \(p(d\mid x)\) is retrieval/ranking and \(p(y\mid x,d)\) is grounded generation [[14](../../references.md#ref-14)]. Typical retrieval scores include dense similarity
\[
s_{\text{dense}}(q,d)=\langle e_q,e_d\rangle
\]
and lexical ranking such as BM25 [[15](../../references.md#ref-15)] [[46](../../references.md#ref-46)].

The control question is when to retrieve. One uncertainty-trigger policy is
\[
\texttt{retrieve}_t = \mathbf{1}\{H[p(\cdot\mid h_t)] > \tau\},
\]
but the economically sharper rule is expected value of information:
\[
\mathrm{VoI}(q)=\mathbb{E}\!\left[\max_a\mathbb{E}[U(a,S)\mid q]\right]-\max_a\mathbb{E}[U(a,S)].
\]
Retrieve when \(\mathrm{VoI}(q)\) exceeds retrieval cost.

## Retrieval as sequential control

Let action \(a_t\in\{\texttt{retrieve},\texttt{skip}\}\). Then a budget-aware Bellman control law is
\[
V^\star(h_t)=\max_{a_t}\left\{r(h_t,a_t)-\lambda\ell(a_t)+\gamma\,\mathbb{E}[V^\star(h_{t+1})]\right\},
\]
where \(\ell\) captures latency/token cost [[5](../../references.md#ref-5)] [[4](../../references.md#ref-4)]. This is the formal version of a practical truth: always retrieving is slow, never retrieving is reckless.

## Three-theory braid

Latent-document RAG gives the generative factorization \(p(y|x)=\sum_d p(y|x,d)p(d|x)\), DPR-style dense retrieval gives scalable semantic access via vector similarity, and classical probabilistic ranking gives lexical grounding with interpretable score structure, so the architecture becomes a living braid in which expected utility decides whether evidence acquisition is worth paying for, Bellman recursion propagates that decision through future uncertainty, and uncertainty-trigger feedback prevents both over-retrieval bloat and under-retrieval hallucination [[14](../../references.md#ref-14)] [[15](../../references.md#ref-15)] [[46](../../references.md#ref-46)] [[33](../../references.md#ref-33)] [[34](../../references.md#ref-34)].

## How to study this formally

Measure Recall@\(k\)/nDCG, citation faithfulness, contradiction rate, and end-task utility under fixed retrieval budgets. Compare always-retrieve, never-retrieve, and uncertainty/VoI-triggered policies. If retrieval cannot buy measurable uncertainty reduction per unit latency, it is ritual, not reasoning.
