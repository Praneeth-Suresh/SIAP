# Tool Interfaces and Function Calling

Tool use is where an interpreter stops describing a computation and begins to
change a world outside its own text stream. The decisive artifact is therefore
not the prompt. It is the boundary contract: the small formal agreement that
says which requests can cross from linguistic intention into external effect,
what evidence will count as success, and how the system behaves when the call
is delayed, denied, or repeated.

In a Lisp evaluator, primitive procedures are trusted bridges from symbolic
expressions to machine operations. In an agentic interpreter, tool calls play
the same role. They are primitive operations, but now the machine operation may
send mail, alter a database, query a search index, move a cursor, deploy a
service, or charge a card. A good tool interface makes this bridge narrow,
typed, inspectable, and recoverable.

If the phrase "Lisp evaluator" is new, picture a small program that reads an
expression such as `(+ 2 3)` and knows that `+` is a primitive procedure: it is
not defined by more Lisp code inside the student's program, but by the
underlying machine. A JSON schema plays a similar role for a modern tool call.
It says which keys, strings, numbers, and objects form a legal request. The
schema is not the whole contract, but it is the first gate through which a
sentence-like intention becomes a machine-checkable action.

## Contract-first action semantics

Represent a tool \(f\) by
\[
f : X \to Y,\quad \texttt{Pre}_f(x),\ \texttt{Post}_f(x,y),\ \texttt{Cost}_f(x),\ \texttt{Risk}_f(x).
\]
The domain \(X\) is not merely a JSON shape. It is the set of requests for which
the tool has agreed to interpret the arguments. The precondition says what must
already be true; the postcondition says what the caller may rely on afterward;
the cost and risk annotations let the planner compare this action with other
ways of learning or acting.

An invocation \(u_t=(f_t,x_t,k_t)\), with idempotency key \(k_t\), is legal iff
schema, authorization, and preconditions pass:
\[
\texttt{legal}(u_t)=\mathbf{1}\{\texttt{schema\_ok}(x_t)\land \texttt{auth\_ok}(f_t)\land \texttt{Pre}_{f_t}(x_t)\}.
\]
Here "iff" means "if and only if": the invocation is legal exactly in the cases
where all three tests succeed. The symbol \(\mathbf{1}\{\cdots\}\) is an
indicator; it evaluates to 1 when the statement inside is true and to 0
otherwise. Thus the formula is not mysticism. It says that well-formed
arguments, permission, and a ready state are jointly necessary for the call to
cross the boundary.

The policy then chooses only among legal invocations:
\[
u_t^{*} = \arg\max_{u}\ \mathbb{E}[Q(\sigma_t,u)]-\lambda_c C(u)-\lambda_r R(u).
\]
This is a compact way to say something practical: the next call is selected not
because it is syntactically possible, but because its expected contribution is
worth its latency, price, permission exposure, and failure surface. For long
horizons, Bellman structure supplies the usual discipline: choosing a tool now
also changes the future state of permissions, memory, obligations, and recovery
options [[5](../../references.md#ref-5)] [[4](../../references.md#ref-4)].

The contract can be read as a small constitution for the primitive:

```text
tool create_invoice(order_id, amount, currency, idempotency_key)
  requires: caller has billing.write; order is approved; amount > 0
  ensures: exactly one invoice is durably associated with idempotency_key
  retry: safe with same idempotency_key
  risk: external financial record
  evidence: invoice id and ledger entry
```

This description is not decoration. It is executable design pressure. The
runtime can reject malformed arguments before the model improvises around them;
the planner can prefer reversible tools before irreversible ones; the auditor
can distinguish a schema failure from a permission failure or a broken
postcondition.

## Idempotent effects under at-least-once delivery

Retries are unavoidable; duplicate side effects are optional. Distributed
systems rarely guarantee that a request is executed exactly once. The practical
target is weaker and more useful: under at-least-once delivery, repeated
invocations with the same idempotency key should produce one durable effect and
one recorded result. Model the tool runtime as carrying a ledger \(L\) from
keys to outcomes and a keyed effect \(f_k\):
\[
\operatorname{invoke}(f,x,k,L)=
\begin{cases}
(L,L[k]) & k\in\operatorname{dom}(L),\\
(L\cup\{k\mapsto y\},y) & k\notin\operatorname{dom}(L),\ y=f_k(x).
\end{cases}
\]
The second branch is sound only if the effect and ledger write are one atomic
transaction, or if the external system itself interprets \(k\) so that
re-executing \(f_k(x)\) returns the same durable effect. A process that performs
\(f(x)\), crashes, and only then records \(L[k]\) has not achieved idempotent
visible behavior; it has created a duplicate-effect race. A minimal retry
controller can be written as
\[
n_{t+1}=\min(n_{\max},n_t+1),\qquad d_{t+1}=\beta d_t,\ \beta>1,
\]
with escalation when \(n_t=n_{\max}\). In other words: optimism in policy,
pessimism in side-effect handling.

The terms deserve to be slowed down. An idempotency key is a name for a logical
attempt, such as `invoice:order-431:v1`; at-least-once delivery means the
network may deliver the same request once, twice, or five times; a durable
effect is an effect that survives crashes; and an atomic transaction is a
"both-or-neither" update. The invoice failure trace is the cautionary tale:

```text
t0  agent sends create_invoice(order-431, key=invoice:order-431:v1)
t1  billing service creates invoice INV-9
t2  process crashes before local ledger records the key
t3  agent retries without an external idempotency guarantee
t4  billing service creates INV-10 for the same order
```

The repair is to make the ledger write and invoice creation atomic, or to make
the billing system itself recognize the key and return `INV-9` on retry. The
mathematics above is therefore a protection against a very ordinary mistake:
confusing "I did not receive the answer" with "the world did not change."

The interpreter should treat idempotency as part of the action, not as a
transport option. A retry without the original key is a new proposal to the
world. A retry with the original key is an inquiry into whether the previous
proposal took effect. This distinction is the difference between a resilient
payment system and an expensive accident.

## Tool calls as interpreter steps

Function calling, Toolformer-style API learning, and ReAct-style reason-act
traces should be understood as three views of the same transition system. Typed
schemas make language intent machine-checkable. Learned tool-use policies show
that a model can internalize when a primitive is useful from weak supervision.
Explicit reason-act traces expose the sequence of observations, decisions, and
effects so that the agent loop can be inspected rather than merely sampled
[[13](../../references.md#ref-13)] [[12](../../references.md#ref-12)] [[11](../../references.md#ref-11)].

The resulting architecture is interpreter-like. The model proposes a primitive
operation; the contract checker validates it; the runtime executes it or refuses
it; the observation is returned to the evaluator; the next step is conditioned
on that observation. The important design move is that refusal is a normal
transition, not a crash. A denied permission, an expired token, or a failed
postcondition becomes data for the next step.

```text
evaluate(state):
  proposal = policy(state)
  if not contract_allows(proposal):
    return evaluate(state.with_observation("rejected", reason))
  result = invoke_with_ledger(proposal)
  return evaluate(state.with_observation(result))
```

This loop is deliberately plain. Its strength lies in where it puts authority.
The language model may propose; the interface disposes. Illegal actions are not
left to prompt discipline. Risky actions are represented as risky before they
run. Expensive actions carry costs visible to the policy. Irreversible actions
must publish the evidence by which success or rollback will later be judged.

## Reading failures through the contract

A mature tool interface makes failures classifiable. Schema errors mean the
interpreter formed the wrong expression. Authorization errors mean the proposed
transition lies outside the caller's role. Precondition errors mean the state was
not ready. Postcondition errors mean execution did not establish what the tool
promised. Timeout and retry errors mean the agent is uncertain about the
external state and must consult the ledger, observe, or escalate.

The same failure table should be read against the task, not against tools in
the abstract. Reversible actions can tolerate exploratory calls and cheap
rollback; irreversible actions demand stronger preconditions and independent
evidence. Side-effect risk changes how much authority the tool should receive.
Retry semantics decide whether repetition is harmless, ambiguous, or a second
dangerous act. Evidence availability decides whether the agent can verify a
postcondition itself or must escalate to another sensor, another role, or a
human. Thus a tool pattern is not "good" merely because it exists. It is good
when the task's reversibility, risk, retry behavior, and evidence surface make
the contract strong enough to improve the interpreter's next state.

This gives tool evaluation a concrete shape. Track schema and precondition
violation rates, postcondition success, duplicate-side-effect rate, rollback
frequency, partial progress after failed calls, and utility gain per call under
fixed latency and token budgets. A tool interface is publishable engineering
when its failures are explained by the contract itself. Then language can touch
the world without pretending the world is just more language.
