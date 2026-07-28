# Reasoning Loops as Interpreters

Read an agent's reasoning as a small programming language: it has a state, a set of legal moves, and a rule that says when the computation is finished. Once you see reasoning that way, you can ask precise questions about it instead of admiring it. You can also debug it, which is the more useful skill.

## What a Reasoning Architecture Adds to the Loop

Chapter 1 ended with an agent interpreter. Its cycle was: observe, update belief, abstract state, choose a governed action, execute, and repeat.

A reasoning architecture is a refinement of that interpreter. It is the part of the agent that decides which internal computations count as legal steps before an external action is allowed to occur. In other words, it governs the thinking that happens between two moments of consequence.

This shift matters because "reasoning" is otherwise too easy to treat as a mood of the model. In an engineered agent, reasoning is a transition system: a machine that moves from one state to another by named steps. Such a system has four visible parts:

- state, meaning everything the loop currently knows and holds;
- admissible moves, meaning the steps the loop is allowed to take;
- guards and budgets, meaning the conditions and resources that permit a move;
- halting conditions, also called stopping conditions in this book, meaning the test that says the computation is done.

Once those pieces are explicit, we can ask ordinary semantic questions. What states can this loop reach? Which transitions mutate the outside world? Which invariants are preserved? Which failures are illegal states rather than disappointing outputs? The last question is the sharpest one. A disappointing output is a matter of taste; an illegal state is a bug with a location.

## Why "Pattern" Must Mean Something Mechanical

Call an agentic pattern a disciplined change to this little machine. A pattern earns the name by changing one of five things:

1. It may add a field to state, such as a plan frontier (the set of plan steps still open) or a memory handle (a reference the loop can use to fetch stored material).
2. It may add legal transitions, such as `retrieve` or `critique`.
3. It may introduce a feedback channel, such as test results that update the controller rather than merely decorate the transcript.
4. It may strengthen authority guards before dangerous actions.
5. It may change the halt predicate, so the agent stops only after evidence, budget, and task conditions line up.

This definition keeps the word "pattern" from becoming incense. A pattern is not a vibe; it is a modification to machine state, legal transitions, feedback channels, authority guards, or the predicate that says the computation is done.

## The Machine State

Let machine state be
\[
\sigma=(m,h,b,\tau,\kappa),
\]
where \(m\) is memory, \(h\) is interaction history, \(b\) is belief, \(\tau\) is tool context, and \(\kappa\) is the remaining control budget. Read \(\sigma\) aloud as "sigma, the current machine state", and read \(\kappa\) as "kappa, the budget left".

That is a good many letters for one definition, so the following table gathers them in one place for reference:

| Symbol | Read aloud as | Meaning |
|---|---|---|
| \(\sigma\) | "sigma" | the whole machine state at one moment |
| \(m\) | "m" | memory the loop can consult |
| \(h\) | "h" | the interaction history so far |
| \(b\) | "b" | the agent's belief about the situation |
| \(\tau\) | "tau" | tool context: which tools exist and what shapes their arguments take |
| \(\kappa\) | "kappa" | the remaining control budget for deliberation and action |
| \(\ell\) | "ell" | the label naming which kind of step was taken |

A loop step is a labeled transition
\[
\sigma \xrightarrow{\ell} \sigma',\qquad \ell\in\{\texttt{think},\texttt{act},\texttt{observe},\texttt{reflect}\},
\]
with legality defined by inference rules in the style of structural operational semantics [[42](../../references.md#ref-42)]. Read the arrow as "state sigma steps to state sigma-prime by a step of kind ell".

A tool call, for example, can fire only when its arguments satisfy the tool schema and the loop still has budget:
\[
\frac{\texttt{schema\_ok}(a,\tau)\ \wedge\ \kappa>0}{\langle \texttt{act}(a),\sigma\rangle \to \sigma'}.
\]

### Reading the Inference Rule as a Legal Tablet

Read the inference rule as a tiny legal-code tablet. The facts in the numerator, the upper part of the fraction, are premises. Here there are two of them: the proposed action \(a\) must match the tool context \(\tau\), and the remaining budget \(\kappa\) must be positive. The statement in the denominator, the lower part, is the transition the interpreter is allowed to take when those premises hold.

Structural operational semantics is the discipline of defining a language by such local execution rules. It does not offer a paragraph saying what the whole program "means". It specifies which small steps are legal from each state.

The rule is small, but its effect is large. An invalid tool call becomes a violation of the agent language, not a vague "model mistake". A builder checks this rule by refusing the call at the boundary: if the arguments fail validation, or the budget reads zero, no external call is made and the refusal is recorded with a reason.

### Traces, Reachability, and Invariants

The complete loop is the execution relation generated by repeated one-step execution:
\[
\sigma_0 \xrightarrow{\ell_0} \sigma_1
\xrightarrow{\ell_1}\cdots
\xrightarrow{\ell_{T-1}} \sigma_T,
\qquad \texttt{halt}(\sigma_T).
\]
Read this as a chain: the loop starts at \(\sigma_0\), takes labeled steps one at a time, and stops at \(\sigma_T\) because the halt test finally holds there.

If one wants a denotational account, this relation can later be embedded in an ordered domain and studied by fixed-point methods. For engineering purposes the operational trace is already powerful. If \(I(\sigma)\) holds initially and every legal transition preserves it, then \(I\) holds along every reachable trace. That includes traces that halt late and traces that fail early.

### The Vocabulary Behind Reachability

Several technical words are doing quiet work here, so each deserves a plain definition.

- An invariant is a property that should remain true after every legal step. Two practical examples: "external actions require permission", and "raw observations are stored before summaries are trusted."
- A reachable state is any \(\sigma_T\) that can be produced from the initial state \(\sigma_0\) by zero or more legal transitions. Unreachable states may be imaginable, but the interpreter can never actually enter them.
- Denotational semantics gives meanings by mapping programs or transition systems into mathematical objects, often functions.
- An ordered domain is a collection of meanings arranged by an information order, where one approximation can be less precise than another.
- A fixed point is a value \(x\) with \(F(x)=x\). In semantics it often describes the stable meaning obtained when repeatedly applying a behavior equation no longer changes what we know.

Freshmen need not worship these terms, but they should recognize the ceremony. Local transition rules generate traces, traces define reachability, and reachability is where invariants either live or perish.

## Four Kinds of Steps

The labels separate internal computation from external consequence. Each label carries a different contract:

- `think` may update candidate hypotheses, plan fragments, or uncertainty estimates. It must not mutate the outside world.
- `act` is the only transition that invokes an external tool or changes an external system.
- `observe` incorporates tool results, user replies, or environment measurements into belief while preserving raw evidence for audit.
- `reflect` revises policies, summaries, or future search heuristics, without pretending that a failed action succeeded.

### A Semantic Skeleton in Pseudocode

One compact interpreter makes those contracts visible. The pseudocode below loops until the halt test passes, asks a controller which label to run next, performs the matching update, and checks the invariants after every step. Note that only the `act` branch carries the two guards, schema validity and positive budget.

```text
while not halt(sigma):
    ell <- controller.select_label(sigma)

    if ell == think:
        sigma <- propose_or_score(sigma)
    if ell == act:
        require schema_ok(action, sigma.tools)
        require sigma.budget > 0
        sigma <- execute_external_action(sigma)
    if ell == observe:
        sigma <- update_belief_from_raw_observation(sigma)
    if ell == reflect:
        sigma <- revise_internal_policy_notes(sigma)

    require invariants_hold(sigma)
```

This is not meant as a production runtime. It is a semantic skeleton. A real implementation may use event logs, queues, type systems, and permission services. The same distinction remains: reasoning steps are interpreter transitions whose side effects must be named.

## Utility and Control Inside the Loop

The transition system needs a selection principle. Something must say which legal move to take.

### Choosing the Next Step by Expected Consequence

Expected-utility theory supplies the local one:
\[
a_t^\star=\arg\max_{a\in\mathcal{A}} \mathbb{E}[U(a,S_t)\mid h_t],
\]
so deliberation is justified only when it improves expected consequences enough to pay for itself [[33](../../references.md#ref-33)] [[34](../../references.md#ref-34)]. Read the formula as "pick the action \(a\) from the action set \(\mathcal{A}\) whose average usefulness, given the history so far, is highest".

A tiny example makes the accounting concrete. Suppose acting now succeeds with probability \(0.6\) for a payoff of \(10\), so its expected value is \(6\). Suppose one extra retrieval step raises the success chance to \(0.8\), giving \(8\), but costs \(1\). The extra thinking is worth it: \(8-1=7\) beats \(6\). Raise the retrieval cost to \(3\) and it is not.

Over longer horizons, the same idea lifts to Bellman recursion on interpreter state:
\[
V^\star(\sigma)=\max_a\left\{r(\sigma,a)+\gamma\sum_{\sigma'}P(\sigma'\mid \sigma,a)V^\star(\sigma')\right\},
\]
which makes the next-step policy accountable for the options it creates or destroys later [[5](../../references.md#ref-5)] [[4](../../references.md#ref-4)]. Read \(V^\star(\sigma)\) as "the best long-run value obtainable from state sigma", \(r(\sigma,a)\) as the immediate reward, \(\gamma\) as the discount that shrinks future value, and \(P(\sigma'\mid\sigma,a)\) as the chance of landing in \(\sigma'\). With \(r=1\), \(\gamma=0.9\), and a single successor worth \(10\), the value is \(1+0.9\times 10=10\).

### Regulating Deliberation with a Budget Law

Control enters because reasoning consumes scarce resources and operates under disturbance. A simple budget-feedback law can regulate deliberation intensity:
\[
\kappa_{t+1}=\kappa_t-\text{cost}(a_t)+\rho\big(\kappa_{\text{target}}-\kappa_t\big),
\]
and, in linearized settings, action can be represented as \(u_t=-K\hat x_t\) over estimated state \(\hat x_t\). Read that second expression as "the control input \(u\) at time \(t\) is a gain matrix \(K\) applied, with a minus sign, to the current estimate of the state".

The point is not that every language agent is a linear controller. The point is that loop quality is a closed-loop property. The system must measure, correct, and continue under model error [[36](../../references.md#ref-36)] [[41](../../references.md#ref-41)].

### Reading the Budget Equation Slowly

The budget equation deserves a plain reading, one step at a time.

1. Start with current budget \(\kappa_t\).
2. Subtract the cost of the chosen step.
3. Then add the feedback term \(\rho(\kappa_{\text{target}}-\kappa_t)\).

If \(\kappa_t\) is below the target and \(\rho>0\), this term is positive; if it is above the target, the term is negative. Try numbers: with \(\kappa_t=40\), a step cost of \(6\), a target of \(50\), and \(\rho=0.5\), the feedback term is \(0.5\times(50-40)=5\), so \(\kappa_{t+1}=40-6+5=39\).

Thus the law intentionally replenishes or tightens the budget as a control signal, not as a magical refund for tokens already spent. A production system might implement that replenishment as "allow a little more cheap reflection because the loop is under its deliberation target". Or it might clamp the term at zero when budgets are hard safety limits.

The equation models a regulator; the engineering policy decides what \(\kappa\) really is. It may be a soft deliberation allowance, a hard money limit, or two ledgers kept separately so the empire does not pay twice for one thought.

## From Semantics to Debugging

Once the loop is a small language, debugging becomes local. Instead of rereading the transcript for mood, you ask four pointed questions:

- Did the planner choose a legal transition?
- Did the guard fail to block an illegal action?
- Did observation parsing corrupt belief?
- Did a preserved invariant turn out to be the wrong invariant?

Abstract interpretation gives a way to over-approximate reachable states through
\[
F^\sharp=\alpha\circ F\circ\gamma,
\]
so some guarantees can be checked without enumerating every concrete trace [[43](../../references.md#ref-43)]. Modern reason-act agents make this especially useful, because their traces expose interleaved reasoning, action, and observation steps in a form that can be instrumented [[11](../../references.md#ref-11)].

### Abstract Interpretation with a Two-State Budget

Here \(F\) is the concrete one-step transformer over detailed states, while \(F^\sharp\) is the cheaper abstract transformer over a coarser world. The abstraction function \(\alpha\) forgets detail on purpose. The concretization function \(\gamma\) says which concrete states an abstract description may represent. This \(\gamma\) is not Chapter 1's discount factor; abstract interpretation traditionally reuses the letter for concretization. Read \(F^\sharp=\alpha\circ F\circ\gamma\) as "expand the abstract description, take one concrete step, then forget the detail again".

For the budget component alone, one exact little abstraction is
\[
\alpha_\kappa(\kappa)=
\begin{cases}
\texttt{positive}, & \kappa>0,\\
\texttt{exhausted}, & \kappa\le 0,
\end{cases}
\qquad
\gamma_\kappa(\texttt{positive})=\{\kappa\mid \kappa>0\},\quad
\gamma_\kappa(\texttt{exhausted})=\{\kappa\mid \kappa\le 0\}.
\]

If the safety question is merely "can an `act` transition fire?", this two-state budget kingdom is enough. All positive budgets permit the premise \(\kappa>0\), and exhausted budgets do not.

The price is precision. A concrete budget of \(1\) and a concrete budget of \(100\) both become `positive`. So the abstract checker can protect legality while remaining gloriously ignorant about whether the agent can afford a long opera of reflection.

### Designing the Loop State as a Typed Object

The practical lesson is to design the loop state as a typed object, with named fields rather than a bag of text. A workable set of fields is:

- current task;
- belief summary;
- memory handles;
- tool permissions;
- budget ledger;
- pending commitments;
- halt criteria.

Each transition should have a name and a contract. The prompt is then one component inside a semantics, not the sovereign description of the whole system.

## Exercise

Take an agent loop you have built or used. The goal is to state its invariants precisely enough to test them.

1. Write three invariants that should hold after every transition. At least one should concern budget, one should concern permissions, and one should concern evidence preservation.
2. For each invariant, identify the transition label most likely to violate it: `think`, `act`, `observe`, or `reflect`.
3. For each invariant, name the observation you would need in the trace to diagnose the violation.

A good answer is checkable. "The loop is careful with money" is not an invariant; "no `act` step runs when the budget ledger reads zero or less, and every `act` step appends its cost to the ledger" is, because a reader can point at the trace entry that proves or breaks it.
