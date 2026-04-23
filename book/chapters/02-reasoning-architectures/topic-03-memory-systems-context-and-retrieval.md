# Memory Systems, Context, and Retrieval

Memory is policy, not pile: retain, compress, retrieve, forget. The trick is to optimize this policy under context-window scarcity.

## Formal memory policy

Let memory state be \(m_t=(w_t,e_t,s_t)\): working, episodic, and semantic stores.  
A memory controller chooses operations \(u_t \in \{\texttt{write},\texttt{compress},\texttt{retrieve},\texttt{evict}\}\) by
\[
u_t = \mu_\theta(m_t,h_t),
\]
to optimize
\[
\max_\mu\ \mathbb{E}\!\left[\sum_t \gamma^t \big(\text{task\_utility}_t - \lambda_1\text{latency}_t - \lambda_2\text{token\_load}_t\big)\right].
\]

## Three-theory braid

1. **Cognitive multi-store theory.** Distinct working/episodic/semantic strata suggest principled architectural separation [[48](../../references.md#ref-48)].
2. **Information-theoretic compression.** Retention is a rate-distortion tradeoff: keep bits that preserve decision value [[35](../../references.md#ref-35)].
3. **Modern retrieval theory.** Sparse/dense indexing and RAG latent-document models define end-to-end evidence pipelines [[14](../../references.md#ref-14)] [[15](../../references.md#ref-15)] [[46](../../references.md#ref-46)] [[47](../../references.md#ref-47)].

## How to study this formally

Evaluate retrieval precision/recall, downstream answer faithfulness, and regret from memory eviction decisions. Stress-test long-horizon tasks with adversarial distractors. If memory policy cannot be audited quantitatively, “long context” is just expensive amnesia.
