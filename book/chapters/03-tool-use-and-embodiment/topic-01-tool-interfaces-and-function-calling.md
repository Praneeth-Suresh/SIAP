# Tool Interfaces and Function Calling

Tool use is where language stops narrating and starts doing. The central artifact is not the prompt—it is the contract.

## Formal contract model

Represent tool \(f\) by
\[
f : X \to Y,\quad \text{with } \texttt{Pre}_f(x),\ \texttt{Post}_f(x,y),\ \texttt{Cost}_f(x),\ \texttt{Risk}_f(x).
\]
An invocation is legal iff \(\texttt{Pre}_f(x)=\texttt{true}\).  
A planner selects tool call \(u_t=(f_t,x_t)\) by maximizing expected utility under cost/risk constraints:
\[
u_t^{*} = \arg\max_{u} \ \mathbb{E}[Q(\sigma_t,u)] - \lambda_c \texttt{Cost}(u) - \lambda_r \texttt{Risk}(u).
\]

## Three-theory braid

1. **Schema-typed interfaces.** Function-calling schemas convert natural-language intent into machine-checkable arguments [[13](../../references.md#ref-13)].
2. **Self-supervised tool-use learning.** Toolformer-style training demonstrates that models can internalize tool-selection policies from weak supervision [[12](../../references.md#ref-12)].
3. **Compositional action semantics.** Reason-act trajectories make tool calls first-class state transitions suitable for replay and policy improvement [[11](../../references.md#ref-11)].

## How to study this formally

Track precondition violation rate, postcondition success, rollback frequency, and utility gain per call. A tool interface is mature when failures are classifiable by contract violation rather than “the model seemed confused.”
