# Goals, Environments, and Actions

An agent is not a model that emits impressive text. It is an interpreter for situated action. At each step it reads a partial observation, updates what it thinks is going on, chooses an admissible action, and accepts that the action changes the next problem it must solve. Before we can discuss belief, memory, planning, or control, we need the contract that this interpreter is running.

The contract has three parts. A **goal** says what outcomes count as better or worse. An **environment** says what can change outside the agent and what the agent can observe. An **action vocabulary** says which interventions are legal, costly, reversible, and checkable. Without these parts, the system may still be useful, but its behavior is difficult to compare, debug, or govern [[2](../../references.md#ref-2)].

## A Coding Agent Under Deadline

Imagine a coding agent tasked with shipping a bug fix before a release freeze. Its goal is not "write something clever." A defensible goal combines task value, regression risk, deadline pressure, and cost. Its environment includes a partially observed repository, flaky CI, hidden downstream dependencies, and a user whose constraints may be underspecified. Its actions include reading files, editing code, running tests, asking for clarification, and opening a pull request. Each action produces an observation, consumes budget, and may make later actions easier or harder [[3](../../references.md#ref-3)] [[7](../../references.md#ref-7)].

This is already enough to write the smallest agent interpreter:

```text
state <- initial_state()
history <- []

while not terminated(state, history):
    observation <- observe(environment, state)
    state <- update_state(state, observation)
    action <- choose_action(goal, state, legal_actions(state))
    outcome <- execute(action)
    history <- history + [(observation, action, outcome)]
```

This loop is the experimental baseline for the rest of the book. Before adding retrieval, planning, reflection, tool governance, or multiple agents, we can ask what this plain interpreter achieves: whether it completes the task, how far it gets before stopping, how many tokens and tool calls it spends, how long it waits on feedback, and which failures remain. Later patterns are not magic additions; they are controlled mutations of this loop.

The rest of the chapter refines the three vague functions in this loop. Topic 2 asks what `update_state` should mean when the world is uncertain. Topic 3 asks what information belongs in `state` rather than in the raw transcript. Topic 4 asks how `choose_action` becomes a policy that remains useful under constraints and feedback.

## Formal Contract

A common mathematical model is a partially observable Markov decision process with constraints:

\[
\mathcal{M}=(\mathcal{S},\mathcal{O},\mathcal{A},T,\Omega,R,C,\gamma).
\]

Here \(\mathcal{S}\) is **latent world state**: the complete condition of the world that matters but is not directly visible. For the coding agent, \(s\in\mathcal{S}\) might include the real bug location, whether a dependency is stale, and whether an unseen integration test will fail. The word latent simply means "present in the world, hidden from the agent's sensors." \(\mathcal{O}\) is the set of observations, such as file contents, test output, logs, and user messages. \(\mathcal{A}\) is the action set, including `read_file`, `edit_file`, `run_tests`, `ask_user`, and `open_pr`.

The term \(T(s'\mid s,a)\) is the **transition dynamics**: the probability that the next latent state is \(s'\) if the current state is \(s\) and the agent takes action \(a\). If \(a\) is `edit_file`, \(T\) describes how likely that edit is to move the repository from "bug present" to "bug fixed" or, less gloriously, to "new regression introduced." The term \(\Omega(o\mid s,a)\) is the **observation model**: the probability that the agent sees observation \(o\) after action \(a\) when the world is in state \(s\). A flaky test suite has an observation model with noise. \(R(s,a)\) is reward, \(C(s,a)\) is constraint cost, and \(\gamma\in(0,1)\) is a **discount factor**, a number that makes nearer consequences count more than distant ones [[4](../../references.md#ref-4)] [[7](../../references.md#ref-7)] [[51](../../references.md#ref-51)]. The Markov assumption is an interpretation, not a fact about reality: it says that the state representation is rich enough that the next transition can be modeled from the current state and action. When that assumption fails, the repair is usually better state, better memory, or a more cautious policy.

A policy \(\pi(a\mid h_t)\), with history \(h_t=(o_{0:t},a_{0:t-1})\), is evaluated by expected return subject to constraints. A **policy** is the decision rule. The notation \(\pi(a\mid h_t)\) reads "the probability that the policy chooses action \(a\) given history \(h_t\)." Before the infinite sum appears, consider two concrete steps with \(\gamma=0.9\). Suppose `read_file` earns immediate reward \(R_0=1\) because it gathers useful evidence, and `edit_file` earns \(R_1=8\) after the evidence points to the right line. The two-step discounted return is

\[
R_0+\gamma R_1 = 1 + 0.9\cdot 8 = 8.2.
\]

If the first action instead rushed an edit with \(R_0=4\) but caused a next-step regression \(R_1=-5\), the return would be \(4+0.9(-5)=-0.5\). Discounting does not worship delay; it merely lets the contract compare immediate temptation with later consequence.

\[
\max_{\pi}\;J(\pi)=\mathbb{E}_{\pi,T,\Omega}\!\left[\sum_{t=0}^{\infty}\gamma^t R(s_t,a_t)\right]
\quad\text{s.t.}\quad
\mathbb{E}_{\pi}\!\left[\sum_{t=0}^{\infty}\gamma^t C_j(s_t,a_t)\right]\le\kappa_j\;\forall j.
\]

This equation should not be mistaken for a demand that every product team hand-code a perfect reward function. Its practical use is diagnostic. It forces the designer to say which outcomes are being optimized, which costs are merely tradeoffs, and which constraints should stop the agent even when the short-term reward looks attractive.

## From Symbols to Interfaces

The same contract can be expressed as ordinary engineering fields:

| Formal symbol | Meaning | Typical implementation field |
|---|---|---|
| \(\mathcal{O}, o_t\) | observations | `AgentStep.observation` |
| \(\mathcal{A}, a_t\) | admissible and chosen actions | `AgentSpec.action_space`, `AgentStep.action` |
| \(R(s_t,a_t)\) | task utility signal | `AgentStep.reward` |
| \(C(s_t,a_t)\) | safety, budget, or policy costs | `AgentStep.costs` |
| \(T,\Omega\) | world and sensing assumptions | `WorldModel.transition()`, `WorldModel.observe()` |
| \(\pi(a\mid h_t)\) | decision rule | `Policy.select_action(history)` |

Expected-utility theory supplies the local decision criterion: choose the action with greatest expected utility under the current interpretation of the world [[33](../../references.md#ref-33)] [[34](../../references.md#ref-34)]. Sequential decision theory adds that a locally attractive action can be bad if it destroys future options, which is the lesson captured by Bellman recursion in fully observed settings [[5](../../references.md#ref-5)]. Feedback control adds the implementation discipline: plans must be corrected after new measurements arrive, because disturbances and model error are normal rather than exceptional [[36](../../references.md#ref-36)] [[39](../../references.md#ref-39)] [[41](../../references.md#ref-41)].

For the coding agent, this means the action registry should say more than "can run shell commands." It should say which commands are allowed, what they may modify, what evidence they are expected to produce, how much budget they consume, and which postconditions must be checked. A vague prompt asks the agent to be careful. A contract gives the runtime something to inspect.

## Exercise

Take a real prompt you use, such as "refactor this module safely and quickly." Rewrite it as a small agent contract:

- One reward term for functional correctness.
- One task-success condition that says what "done well enough" means.
- One meaningful intermediate milestone, such as "the failing test is reproduced" or "the risky subsystem has been identified."
- One reward or cost term for latency, money, or token use.
- At least one hard constraint.
- A measurable stopping condition, including when to stop after partial progress rather than spend the budget theatrically.
- The legal actions available to the agent.

Then identify which part of your spec describes utility, which part describes dynamics, and which part creates feedback. If you cannot answer those questions, the agent is still being steered by prose where it needs an interface.
