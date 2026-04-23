# Retrieval-Augmented Tooling

RAG is not a monolith; it is a pipeline whose stages can each be formalized, measured, and improved.

## Probabilistic formulation

For query context \(x\), retrieved document \(d\), and answer \(y\):
\[
p(y\mid x) = \sum_{d \in \mathcal{D}} p(y\mid x,d)\,p(d\mid x).
\]
Operationally, \(p(d\mid x)\) is retrieval/ranking, while \(p(y\mid x,d)\) is grounded generation. Agentic retrieval triggers should depend on uncertainty:
\[
\texttt{retrieve}_t = \mathbf{1}\{H[p(\cdot\mid h_t)] > \tau\}.
\]

## Three-theory braid

1. **Latent-document generation.** RAG models combine parametric generation with non-parametric memory [[14](../../references.md#ref-14)].
2. **Dense representation retrieval.** DPR-style dual encoders formalize semantic nearest-neighbor access to large corpora [[15](../../references.md#ref-15)].
3. **Classical IR ranking theory.** Probabilistic ranking (e.g., BM25 family) provides robust lexical grounding and interpretable ranking signals [[46](../../references.md#ref-46)].

## How to study this formally

Measure retrieval nDCG/Recall@k, citation faithfulness, and end-task utility under retrieval budget constraints. Compare always-retrieve versus uncertainty-triggered retrieval policies. If retrieval cannot justify its latency with measurable uncertainty reduction, it is ritual, not reasoning.
