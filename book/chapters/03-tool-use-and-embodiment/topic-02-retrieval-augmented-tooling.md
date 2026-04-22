# Retrieval-Augmented Tooling

RAG is best understood as a tool chain: query formulation, retrieval, ranking, synthesis, and citation. Each stage is a controllable component with separate error surfaces [[14](../../references.md#ref-14)] [[15](../../references.md#ref-15)].

For agentic workflows, retrieval should be demand-driven by planner uncertainty, not indiscriminately invoked every turn. This keeps latency and context load aligned with epistemic need.

A practical architecture:
1. detect information gap,
2. issue retrieval query,
3. validate source quality,
4. ground generated claims to retrieved evidence.

The result is not merely better answers; it is better accountability.
