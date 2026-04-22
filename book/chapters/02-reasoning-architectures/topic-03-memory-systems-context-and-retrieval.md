# Memory Systems, Context, and Retrieval

Memory is not “everything ever said.” Memory is a policy over what to retain, compress, retrieve, and forget [[16](../../references.md#ref-16)].

RAG systems operationalize episodic and semantic recall: dense retrieval locates external facts while the model synthesizes them into current reasoning [[14](../../references.md#ref-14)] [[15](../../references.md#ref-15)].

A useful architecture has at least three memory strata:

| Layer | Role |
|---|---|
| Working context | immediate decision state |
| Episodic log | recent trajectories and failures |
| Semantic store | durable concepts and references |

The retrieval policy should be explicit and testable, because memory errors usually appear as reasoning errors one layer later.
