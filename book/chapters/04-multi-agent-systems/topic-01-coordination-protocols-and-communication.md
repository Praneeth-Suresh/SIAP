# Coordination Protocols and Communication

When many interpreters share an environment, communication is not an ornament added to intelligence. It is one of the control surfaces of the system. Each agent sees only part of the state, updates its own local machine, and emits messages that may change the machines around it. A protocol is the rule that makes those local steps compose.

The SICP way to read a multi-agent system is to ask what each interpreter treats as its environment. In a single evaluator, an expression is reduced against a frame of bindings. In a collective, the "frame" is distributed: private scratchpads, local observations, message queues, shared documents, tool outputs, locks, and audit logs. Coordination is the art of making these frames interact without pretending that any one agent sees the whole store.

## Protocols as distributed transition systems

Let agents \(i\in\{1,\dots,n\}\) have local state \(x_i^t\), incoming messages \(m_{*\to i}^t\), and outgoing messages \(m_{i\to *}^{t+1}\). A protocol \(\Pi\) defines the legal local transition
\[
(x_i^{t+1}, m_{i\to *}^{t+1}) = \Pi_i\!\left(x_i^t,\{m_{*\to i}^t\}\right).
\]
The global state is not stored in any one agent; it is induced by the product of local states, channels, clocks, and shared artifacts. That is why multi-agent debugging so often feels unlike single-agent debugging. The failure may not live inside one interpreter. It may live in the order in which interpreters heard each other.

Local state also includes belief. Agent \(i\) receives observation \(o_i^t\), maintains a belief \(b_i^t(s)\), and chooses both domain actions and communication actions:
\[
b_i^{t+1}=\operatorname{Update}_i(b_i^t,o_i^{t+1},m_{*\to i}^{t+1}).
\]
The shared artifact is not the same thing as shared belief. A fact checker may know that a citation is weak before that weakness appears in the draft; an integrator may see two unresolved comments but not the search failures behind them; a drafter may believe a paragraph is ready because no critique has arrived yet. Decentralized uncertainty begins here: agents act under different information, and communication is a costly attempt to reshape that information.

A few vocabulary words keep the difficulty honest. An asynchronous system is one in which messages can be delayed for an unknown amount of time; there is no dependable global clock that says, "if nothing arrived by now, nothing was sent." A crash fault is a plain failure-stop: an agent may halt and send no more messages. A Byzantine fault is more devious: an agent may lie, send inconsistent messages, corrupt state, or behave in any arbitrary way. The Byzantine courtier is not merely sleepy; he may be composing different letters to different generals.

Correctness criteria name the properties we want from this composed machine. Safety says that forbidden configurations are unreachable. Liveness says that required progress eventually occurs. Agreement, when the task requires it, says that the relevant local states converge:
\[
x_i^T=x_j^T\quad\forall i,j.
\]
Before naming the famous impossibility theorem, consider a two-agent trace. Agent \(A\) proposes value \(1\); agent \(B\) proposes value \(0\); each waits for the other's message before deciding.

```text
t=0    A sends propose(1) to B
t=1    B sends propose(0) to A
t=2    A receives nothing yet; the channel may be slow, or B may have crashed
t=3    B receives propose(1); B cannot tell whether A will receive propose(0)
t=4    A still receives nothing; deciding now risks disagreement, waiting risks no liveness
```

The trouble is epistemic, not theatrical. From \(A\)'s local view at \(t=4\), "B is slow" and "B has crashed" can look identical. If \(A\) must always decide eventually and must never disagree with \(B\), the protocol has to distinguish states that the local observations do not distinguish. Consensus theory makes these words sharp. Byzantine agreement studies what can be guaranteed when some participants may lie or fail arbitrarily [[54](../../references.md#ref-54)]. The FLP result shows that deterministic consensus cannot be guaranteed in a fully asynchronous system with even one crash fault [[55](../../references.md#ref-55)]. FLP does not say consensus is universally impossible. It says that a particular bundle of assumptions cannot all be kept at once. Practical systems regain progress by relaxing something: add timeouts and partial synchrony, allow randomization, use failure detectors, accept probabilistic termination, constrain failures, or weaken the decision requirement. These are not remote distributed-systems curiosities. They are warnings against designing agent collectives whose correctness silently assumes perfect timing, perfect honesty, and perfectly delivered messages.

Communication also has a price. A utility-aware protocol objective can be written
\[
\max_{\Pi}\ \mathbb{E}[U(\tau)]-\lambda\sum_t \|m_t\|,
\]
and, over long horizons, the protocol designer can view "ask another agent" as an action inside a Bellman recursion:
\[
V^\star(s)=\max_a\left\{R(s,a)-\lambda C_{\text{comm}}(a)+\gamma\sum_{s'}P(s'|s,a)V^\star(s')\right\}.
\]
Expected utility gives the one-step decision rule, while dynamic programming makes the future cost of coordination explicit [[33](../../references.md#ref-33)] [[34](../../references.md#ref-34)] [[5](../../references.md#ref-5)]. More messages are justified only when they improve the expected trace enough to pay for their latency, token cost, and confusion risk. In the fully general case, this is a decentralized partially observable Markov decision process: each agent has local observations and local actions, rewards depend on the joint trajectory, and no agent can condition on the complete state. Dec-POMDP reasoning is the clean formal home for this problem. It is usually too expensive to solve exactly, but it gives the right questions: what must be communicated, what can remain local, and which shared artifacts make the hidden state sufficiently inferable?

## Speech acts and commitments

Coordination theory studies dependencies among tasks, resources, and actors; communication is useful when it manages one of those dependencies [[56](../../references.md#ref-56)]. In agent systems, the most useful messages are therefore not free-form paragraphs but typed acts. A small grammar might include
\[
\{\texttt{observe},\texttt{propose},\texttt{critique},\texttt{vote},\texttt{decide},\texttt{commit},\texttt{handoff}\}.
\]
The grammar is not bureaucratic decoration. It tells each receiving interpreter how the message may update state. A proposal creates an option. A critique attaches a defeater. A vote changes a quorum calculation. A commitment creates an obligation that can later be satisfied, expired, or escalated.

Here a defeater is a reason that blocks or weakens an earlier claim: "this citation does not support the sentence" defeats the proposal until repaired. A quorum is the minimum pattern of approvals required before an action counts as collectively authorized; it might be "two of three reviewers," "one security reviewer plus one maintainer," or "all severe critiques resolved." Role guards make the grammar enforceable. A researcher may propose evidence with citations; a reviewer may challenge assumptions; an integrator may decide only after quorum or timeout. This is the difference between "agents discuss" and an actual institution. Role-based multi-agent accounts supply the vocabulary for designing such organizations as systems of authorized actions, responsibilities, and interaction protocols [[17](../../references.md#ref-17)] [[18](../../references.md#ref-18)].

Commitments deserve special treatment because they are where speech touches the environment. A commitment should record who owns the next action, what condition completes it, what deadline applies, and what recovery rule fires on failure. Message observability should be measured:
\[
\rho_{\text{log}}=\frac{\text{logged messages}}{\text{sent messages}}.
\]
If an auditor cannot reconstruct why the collective converged, deadlocked, or stampeded, the protocol has hidden part of its semantics. A deadlock is a state where every agent is waiting for some other event before it can move: the drafter waits for review, the reviewer waits for a revised patch, and the integrator waits for both, while no transition remains enabled.

## A shared publication environment

Consider three agents editing a publication chapter: a drafter, a fact checker, and an integrator. If all three simply write into the same file, the shared environment becomes a race condition. A minimal protocol is better:

1. The drafter may emit \(\texttt{propose(section, patch, rationale)}\).
2. The fact checker may emit \(\texttt{critique(claim, source, severity)}\) or \(\texttt{approve(claim)}\).
3. The integrator may emit \(\texttt{commit(patch)}\) only after all severe critiques are resolved or a timeout rule is invoked.

Each role is an interpreter over a different local environment. The drafter sees the outline, current prose, and unresolved writing tasks. The fact checker sees retrieval results, source quality notes, and claims extracted from the draft. The integrator sees the patch queue, role permissions, open critiques, and release criteria. The shared document is the heap they mutate: the common store of durable objects, just as a programming-language heap holds values that outlive one stack frame. The audit log is the continuation that lets another process resume the computation: it records "what remains to be done next" after the current interpreter yields, crashes, or hands off control.

A compact transition trace makes the semantics visible:

```text
state:
  draft.rev = 17
  queue = []
  critiques = {}

drafter.observe(draft.rev=17, open_gap="Dec-POMDP")
drafter.propose(section="coordination", patch=P1, claim=C1)
  -> queue += [P1]; claims += [C1]

fact_checker.observe(claim=C1, local_sources=[S1 weak, S2 strong])
fact_checker.critique(C1, source=S1, severity="major")
  -> critiques[P1] += ["major: S1 does not support C1"]

integrator.observe(queue=[P1], critiques[P1]=major)
integrator.defer(P1)
  -> queue[P1].status = "blocked"

drafter.revise(P1, citation=S2)
fact_checker.approve(C1)
integrator.commit(P1)
  -> draft.rev = 18; queue -= [P1]
```

This protocol does not make the agents wise. It makes their interaction inspectable. Missing approvals, contradictory commitments, role violations, and stalled dependencies become states the system can detect rather than moods the transcript happens to reveal. It also makes silence meaningful: if the fact checker has not observed the revised citation, the integrator should not interpret absence of critique as approval unless the timeout rule says so.

The value of this coordination depends on the task. Tightly coupled work, where
one agent's patch changes another agent's evidence, needs more communication
than decomposable work whose pieces can be checked independently. Poor
observability makes messages more valuable because local state must be surfaced;
long communication delay makes messages more expensive because the shared world
may have moved before they arrive. The publication workflow sits in the middle:
sections can be drafted separately, but claims, citations, tone, and release
status couple them again.

The practical tests follow from the semantics: message complexity, consensus
latency, deadlock rate, role-violation rate, recovery time after dropped
messages, stale-belief rate, artifact divergence, partial progress under
blocked dependencies, and degradation under corrupted or adversarial messages.
A coordination scheme that works only because every participant is reasonable is
not yet a protocol. It is a cooperative anecdote.
