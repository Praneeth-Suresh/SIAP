# Notes: Coordination Protocols and Communication

## What to improve

- Add one formal protocol example (propose, critique, decide, commit).
- Include message-level observability requirements.
- Add a failure case involving role confusion.

## Alternative rewrite

A team of agents without protocol is a choir with no score: loud, earnest, and misaligned. Coordination begins when speech acts become typed operations with accountable outcomes.

## Pass 1 - Migrated ideas from current main topic

The current topic models coordination as protocol-driven distributed state transitions \((x_i^{t+1},m_{i\to *}^{t+1})=\Pi_i(x_i^t,\{m_{*\to i}^t\})\), with correctness goals spanning safety, liveness, and agreement. Its braid combines consensus limits (Byzantine and FLP), coordination-theory resource/task coupling, and role-based MAS communication architectures [[54](../../references.md#ref-54)] [[55](../../references.md#ref-55)] [[56](../../references.md#ref-56)] [[17](../../references.md#ref-17)] [[18](../../references.md#ref-18)].

## Pass 1 - Storyline outline (paragraph-by-paragraph)

Paragraph 1 opens with institutional necessity: multiple agents need protocol the way traffic needs lanes.

Paragraph 2 introduces typed speech acts (propose, critique, decide, commit) as legal protocol moves rather than free-form chat.

Paragraph 3 frames communication as expected-utility investment under bandwidth and latency constraints [[33](../../references.md#ref-33)] [[34](../../references.md#ref-34)].

Paragraph 4 introduces impossibility and fault-tolerance limits to prevent overpromising under adversarial or delayed networks.

Paragraph 5 resolves with resilience architecture: role separation, observability, and escalation preserve coherence when messages are late or wrong.

## Pass 2 - Research synthesis: equations, theories, and connective tissue

Equation candidates: protocol transition map \(s_{t+1}=\Pi(s_t,m_t)\), agreement condition \(x_i^T=x_j^T\ \forall i,j\), utility-cost objective \(\max_\Pi \mathbb{E}[U(\tau)]-\lambda\sum_t\|m_t\|\), and coordination Bellman recursion \(V^\star(s)=\max_a\{R(s,a)-\lambda C_{\text{comm}}(a)+\gamma\sum_{s'}P(s'|s,a)V^\star(s')\}\) [[5](../../references.md#ref-5)] [[4](../../references.md#ref-4)]. For observability and diagnosis: trace completeness ratio \(\rho=\frac{\text{logged messages}}{\text{sent messages}}\). Fault limits to reference conceptually from Byzantine/FLP literature [[54](../../references.md#ref-54)] [[55](../../references.md#ref-55)]. External pass-2 checks included distributed-coordination and mechanism references already cataloged, plus web review for strategic mechanism context (VCG summary link used below chapter notes). Connective claim: protocols price communication, enforce legality, and preserve collective convergence under uncertainty.

## Additional alternate approaches for this rewrite

1. Write as an air-traffic-control narrative where every speech act is typed and acked.
2. Build around one protocol trace with role confusion and repaired role guards.
3. Teach with a courtroom metaphor: proposals are motions, commits are rulings, and logs are evidence.
4. Frame as a distributed transaction system with explicit commit/abort semantics.
