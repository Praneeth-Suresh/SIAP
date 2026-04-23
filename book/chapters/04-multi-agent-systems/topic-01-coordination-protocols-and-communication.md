# Coordination Protocols and Communication

In multi-agent systems, communication is not chatter; it is distributed computation under uncertainty and delay.

## Formal protocol model

Let agents \(i\in\{1,\dots,n\}\) have local state \(x_i^t\) and messages \(m_{i\to j}^t\).  
A protocol \(\Pi\) defines transition rules
\[
(x_i^{t+1}, m_{i\to *}^{t+1}) = \Pi_i\!\left(x_i^t,\{m_{*\to i}^t\}\right).
\]
Correctness criteria include safety (nothing bad happens), liveness (something good eventually happens), and agreement/consistency when required.

## Three-theory braid

1. **Distributed consensus limits.** Byzantine agreement and impossibility results formalize what reliable coordination can and cannot guarantee [[54](../../references.md#ref-54)] [[55](../../references.md#ref-55)].
2. **Coordination theory.** Task dependencies and resource constraints determine which communication structures are efficient [[56](../../references.md#ref-56)].
3. **Role-based MAS architectures.** Agent communication languages and protocol roles improve traceability and conflict handling [[17](../../references.md#ref-17)] [[18](../../references.md#ref-18)].

## How to study this formally

Evaluate message complexity, consensus latency, deadlock frequency, and degradation under dropped/incorrect messages. Encode schemas and role permissions as enforceable protocol rules. If coordination depends on everyone being “reasonable,” it is not a protocol; it is a prayer.
