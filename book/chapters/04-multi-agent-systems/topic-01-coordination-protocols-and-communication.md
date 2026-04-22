# Coordination Protocols and Communication

Multi-agent systems succeed or fail on protocol quality. Communication is not free-form chatter; it is structured information exchange under timing and trust constraints [[17](../../references.md#ref-17)] [[18](../../references.md#ref-18)].

Common coordination patterns include blackboard systems, planner-executor splits, and committee voting. Each pattern defines who may propose, who may veto, and how conflicts are resolved.

For LLM agents, explicit message schemas and role contracts reduce ambiguity and improve debuggability [[24](../../references.md#ref-24)].

The key principle: coordination logic should be encoded as system rules, not inferred ad hoc from conversational style.
