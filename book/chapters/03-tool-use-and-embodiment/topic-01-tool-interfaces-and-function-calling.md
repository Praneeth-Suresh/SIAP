# Tool Interfaces and Function Calling

Tool use converts language competence into environmental leverage. The core abstraction is a typed function interface with explicit argument schema, preconditions, and postconditions [[12](../../references.md#ref-12)] [[13](../../references.md#ref-13)].

In robust systems, tools are not mere plugins; they are contracts. Contracts let planners reason about side effects, costs, retries, and irreversibility.

This design choice also improves interpretability. Tool calls become machine-checkable events in execution traces, enabling post-hoc audits and policy learning.

A minimal practical recommendation: every tool definition should include semantic purpose, latency class, failure modes, and rollback strategy.
