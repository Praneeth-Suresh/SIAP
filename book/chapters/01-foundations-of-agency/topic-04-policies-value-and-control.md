# Policies, Value, and Control

The policy is the operational constitution of an agent: a rule for selecting actions from state. Value functions estimate long-term consequences and stabilize decision-making under delayed outcomes [[3](../../references.md#ref-3)] [[5](../../references.md#ref-5)].

For LLM agents, policy often combines model proposals with explicit control layers: validators, rankers, budget constraints, and termination logic. This hybridization mirrors classic control decomposition between planner and controller [[4](../../references.md#ref-4)].

A practical implementation pattern is to separate:
1. proposal policy (what actions are suggested),
2. adjudication policy (which suggestion survives),
3. oversight policy (when to escalate or halt).

This decomposition supports measurable guarantees and creates interfaces where formal analysis can enter an otherwise stochastic system.
