# Reasoning Loops as Interpreters

An agent loop is an interpreter in a tailored orchestration suit: it reads state, executes a semantic step, and returns a new state with fewer illusions about the world. Once we treat it this way, debugging becomes mathematics instead of transcript divination.

## Operational core: a tiny machine for thought and action

Let machine state be \(\sigma=(m,h,b,\tau,\kappa)\): memory \(m\), interaction history \(h\), belief \(b\), tool context \(\tau\), and control budget \(\kappa\). A loop step is a labeled transition
\[
\sigma \xrightarrow{\ell} \sigma',\qquad \ell\in\{\texttt{think},\texttt{act},\texttt{observe},\texttt{reflect}\},
\]
with legality defined by inference rules in the SOS style [[42](../../references.md#ref-42)]. For example, a tool call can only fire when schema checks and budget guards hold:
\[
\frac{\texttt{schema\_ok}(a,\tau)\ \wedge\ \kappa>0}{\langle \texttt{act}(a),\sigma\rangle \to \sigma'}.
\]
This is not aesthetic pedantry; it is how you make "invalid tool call" a theorem-violating event rather than a vague complaint.

The complete loop is the least fixed point of one-step execution:
\[
\mathcal{L}(\sigma)=
\begin{cases}
\sigma & \text{if }\texttt{halt}(\sigma)\\
\mathcal{L}(F(\sigma)) & \text{otherwise}
\end{cases}
\]
where \(F\) is the semantic step function. Invariant proofs then become first-class engineering artifacts: if \(I(\sigma)\) and \(I(\sigma)\Rightarrow I(F(\sigma))\), then \(I\) is preserved along all reachable traces.

## Utility compass and long-horizon control

Expected-utility foundations supply the "why" behind every transition: at decision time,
\[
a_t^\star=\arg\max_{a\in\mathcal{A}} \mathbb{E}[U(a,S_t)\mid h_t],
\]
so deliberation is justified only if it improves expected consequence quality [[33](../../references.md#ref-33)] [[34](../../references.md#ref-34)]. Over longer horizons, the same logic lifts to Bellman recursion on interpreter state:
\[
V^\star(\sigma)=\max_a\left\{r(\sigma,a)+\gamma\sum_{\sigma'}P(\sigma'\mid \sigma,a)V^\star(\sigma')\right\},
\]
making it explicit that today's loop policy is selecting tomorrow's option set [[5](../../references.md#ref-5)] [[4](../../references.md#ref-4)].

Control enters when compute and safety must remain stable under disturbance. A simple budget-feedback law can regulate deliberation intensity:
\[
\kappa_{t+1}=\kappa_t-\text{cost}(a_t)+\rho\big(\kappa_{\text{target}}-\kappa_t\big),
\]
and, in linearized settings, action can be represented as \(u_t=-K\hat x_t\) over estimated state \(\hat x_t\), emphasizing that loop quality is a closed-loop property, not a one-shot prompt property [[36](../../references.md#ref-36)] [[41](../../references.md#ref-41)].

## Three-theory braid

Structural operational semantics gives us legal moves as transition judgments \(\langle c,\sigma\rangle\to\sigma'\), abstract interpretation gives us scalable guarantees through \(F^\sharp=\alpha\circ F\circ\gamma\) with sound over-approximation of reachable states, and reason-act trajectories in modern LLM agents ground those abstractions in empirical traces where \(\texttt{think}\to\texttt{act}\to\texttt{observe}\to\texttt{reflect}\) is literally visible token by token, so the architecture of intelligence appears as a disciplined interplay of foresight (utility-guided policy), responsiveness (online transition updates), and resilience (invariants preserved under noisy tools and partial observability) [[42](../../references.md#ref-42)] [[43](../../references.md#ref-43)] [[11](../../references.md#ref-11)].

## How to study this formally

Instrument each transition label, prove step invariants (schema validity, budget non-negativity, permission monotonicity), and run interventional trace replay when failures occur [[6](../../references.md#ref-6)]. If you cannot state the semantics of your loop, you can still ship demos; you just cannot ship explanations.
