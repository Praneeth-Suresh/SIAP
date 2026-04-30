# Tool Interfaces and Function Calling

Tool use is where language stops narrating and starts doing. The central artifact is not the prompt; it is the contract that decides which actions are legal, useful, and survivable under failure.

## Contract-first action semantics

Represent tool \(f\) by
\[
f : X \to Y,\quad \texttt{Pre}_f(x),\ \texttt{Post}_f(x,y),\ \texttt{Cost}_f(x),\ \texttt{Risk}_f(x).
\]
An invocation \(u_t=(f_t,x_t,k_t)\) with idempotency key \(k_t\) is legal iff schema, auth, and preconditions pass:
\[
\texttt{legal}(u_t)=\mathbf{1}\{\texttt{schema\_ok}(x_t)\land \texttt{auth\_ok}(f_t)\land \texttt{Pre}_{f_t}(x_t)\}.
\]
Policy selection then becomes constrained expected utility:
\[
u_t^{*} = \arg\max_{u}\ \mathbb{E}[Q(\sigma_t,u)]-\lambda_c C(u)-\lambda_r R(u).
\]
For long horizons, the same logic lifts to Bellman structure:
\[
V^\star(\sigma)=\max_u\left\{r(\sigma,u)+\gamma\sum_{\sigma'}P(\sigma'|\sigma,u)V^\star(\sigma')\right\},
\]
so choosing a tool now is also choosing the future state of permissions, memory, and recovery options [[5](../../references.md#ref-5)] [[4](../../references.md#ref-4)].

## Exactly-once behavior and fallback control

Retries are unavoidable; duplicate side effects are optional. Idempotency gives a functional target:
\[
f(f(x,k),k)=f(x,k),
\]
which means repeated delivery under the same key \(k\) does not multiply real-world effects. A minimal retry controller can be written as
\[
n_{t+1}=\min(n_{\max},n_t+1),\qquad d_{t+1}=\beta d_t,\ \beta>1,
\]
with escalation when \(n_t=n_{\max}\). In other words: optimism in policy, pessimism in side-effect handling.

## Three-theory braid

Schema-typed interfaces convert language intent into machine-checkable arguments, Toolformer-style learning shows that models can internalize when and how to call APIs from weak supervision, and ReAct-style trajectories turn those calls into explicit reason-act state transitions, so the whole orchestration loop reads like a disciplined control system in which expected utility chooses candidate actions \(u_t^\star=\arg\max_u \mathbb{E}[Q]-\lambda_cC-\lambda_rR\), Bellman recursion maintains long-horizon consistency \(V^\star(\sigma)=\max_u\{r+\gamma\mathbb{E}[V^\star]\}\), and retry/idempotency feedback prevents transient outages from becoming irreversible side effects [[13](../../references.md#ref-13)] [[12](../../references.md#ref-12)] [[11](../../references.md#ref-11)] [[33](../../references.md#ref-33)] [[34](../../references.md#ref-34)].

## How to study this formally

Track schema/precondition violation rate, postcondition success rate, duplicate-side-effect rate, rollback frequency, and utility gain per call under fixed latency budgets. A tool interface is mature when failures are classifiable by contract category, not by vibes.
