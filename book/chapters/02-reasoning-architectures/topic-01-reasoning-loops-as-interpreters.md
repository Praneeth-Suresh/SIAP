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

## Translating the Theory into Agentic Practice

The interpreter view gives agent builders a magnificent little hammer: define the loop as a machine with state, transitions, guards, and invariants. Instead of asking "what should the prompt say?", ask "what states can the system enter, what transitions are legal, and what must remain true after every step?" The prompt becomes one component inside a semantics, not the sovereign monarch of the whole arrangement.

In practice, the loop state should be a typed object: current task, belief summary, memory handles, tool permissions, budget ledger, pending commitments, and halt criteria. Each transition should have a name and a contract. `think` may update hypotheses but not mutate the outside world. `act` may call tools only through schemas and permission checks. `observe` may update belief but must preserve the raw result for audit. `reflect` may revise policy notes but should not launder failure into cheerful prose. These distinctions make execution traces intelligible.

This architecture improves debugging dramatically. When an agent fails, the question becomes local: did the planner choose an illegal transition, did a guard fail to block it, did observation parsing corrupt state, or did a preserved invariant turn out to be the wrong invariant? Trace replay can then intervene on a single transition class, replacing one retrieved document, one tool argument, or one budget threshold to test causal responsibility.

The value of the theory is that it turns agent loops into small languages. Once a loop is a language, we can give it syntax, semantics, tests, monitors, and eventually proofs of modest but precious properties. A reasoning agent whose operational semantics are explicit is no longer an oracle with a log file. It is an executable theory of thought, and its mistakes can be studied with instruments sharper than disappointment.
