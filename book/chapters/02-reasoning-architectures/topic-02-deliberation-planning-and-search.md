# Deliberation, Planning, and Search

Planning gives agents temporal coherence: actions are selected for trajectory quality, not local plausibility [[8](../../references.md#ref-8)] [[9](../../references.md#ref-9)] [[10](../../references.md#ref-10)].

LLM agents often blend symbolic planning with learned heuristics. A search tree may be explicit (tool calls, simulation branches) while scoring is neural and context-dependent [[11](../../references.md#ref-11)].

Three planning modes are practical in orchestration:
1. one-shot plan then execute,
2. interleaved plan/act/replan,
3. speculative branching with pruning.

The correct mode depends on environment volatility, tool latency, and the cost of wrong irreversible actions.
