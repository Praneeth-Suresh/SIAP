# Reasoning Loops as Interpreters

An agent loop is an interpreter wearing orchestration clothing. Once we say this out loud, semantics, invariants, and proofs become available to us.

## Small-step semantics

Define machine state \(\sigma=(m, h, b, \tau)\): memory \(m\), interaction history \(h\), belief state \(b\), and tool context \(\tau\).  
Transitions are relations \(\sigma \xrightarrow{\ell} \sigma'\) labeled by step kind \(\ell \in \{\texttt{think},\texttt{act},\texttt{observe},\texttt{reflect}\}\).

An agent loop is the least fixed point of a transition functional:
\[
\mathcal{L}(\sigma)=
\begin{cases}
\sigma & \text{if }\texttt{halt}(\sigma)\\
\mathcal{L}(F(\sigma)) & \text{otherwise}
\end{cases}
\]
where \(F\) is one semantic step.

## Three-theory braid

1. **Structural operational semantics (SOS).** Behavior is specified via transition rules, making legal/illegal steps explicit [[42](../../references.md#ref-42)].
2. **Abstract interpretation.** We reason soundly about large state spaces using abstract domains and transfer functions [[43](../../references.md#ref-43)].
3. **Reason-act coupling in LLM agents.** ReAct-style trajectories instantiate interpreter steps over tool-mediated environments [[11](../../references.md#ref-11)].

## How to study this formally

Prove step invariants (schema validity, budget monotonicity), termination conditions, and recovery properties from error states. If you cannot define your loop semantics, you cannot debug your loop semantics; you can only squint at transcripts and hope.
