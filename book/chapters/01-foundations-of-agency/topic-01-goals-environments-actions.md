# Goals, Environments, and Actions

Every agent story begins like an old sea tale: fog everywhere, limited instruments, and one irretrievable move at a time. If we cannot say what counts as “north,” what currents the world obeys, and which moves are legal, then we do not have an agent architecture yet—we have charisma and wishful thinking. The disciplined alternative is to specify goals, environment dynamics, and action semantics so that behavior can be analyzed, improved, and held accountable [[2](../../references.md#ref-2)].

## Running example: a coding agent under deadline

Imagine a coding agent tasked with shipping a bug fix before a release freeze. Its **goal** is not “write something clever,” but maximize expected task value (tests pass, regression risk low, deadline met). Its **environment** includes a partially observed repository state, flaky CI, and hidden downstream dependencies. Its **actions** include reading files, editing code, running tests, and opening a pull request. At each step it sees only a slice of the truth, chooses one action, and changes the very world it must reason about next [[3](../../references.md#ref-3)] [[7](../../references.md#ref-7)].

## Formal model (and how it maps to code)

Let the agent-environment system be
\[
\mathcal{M}=(\mathcal{S},\mathcal{O},\mathcal{A},T,\Omega,R,C,\gamma),
\]
where \(\mathcal{S}\) is latent state, \(\mathcal{O}\) observations, \(\mathcal{A}\) actions, \(T(s'\mid s,a)\) transition dynamics, \(\Omega(o\mid s,a)\) observation dynamics, \(R\) reward, \(C\) constraint costs, and \(\gamma\in(0,1)\) discount [[4](../../references.md#ref-4)] [[7](../../references.md#ref-7)] [[51](../../references.md#ref-51)].

A policy \(\pi(a\mid h_t)\), with history \(h_t=(o_{0:t},a_{0:t-1})\), solves the constrained objective
\[
\max_{\pi}\;J(\pi)=\mathbb{E}_{\pi,T,\Omega}\!\left[\sum_{t=0}^{\infty}\gamma^t R(s_t,a_t)\right]
\quad\text{s.t.}\quad
\mathbb{E}_{\pi}\!\left[\sum_{t=0}^{\infty}\gamma^t C_j(s_t,a_t)\right]\le\kappa_j\;\forall j.
\]
Natural-language prompts are therefore only the front door; the house is built from explicit \(R\), \(C\), and stopping criteria.

A practical Python mapping might look like this:

| Formal symbol | Meaning | Typical Python field |
|---|---|---|
| \(\mathcal{O}, o_t\) | observations | `AgentStep.observation` |
| \(\mathcal{A}, a_t\) | admissible and chosen actions | `AgentSpec.action_space`, `AgentStep.action` |
| \(R(s_t,a_t)\) | task utility signal | `AgentStep.reward` |
| \(C(s_t,a_t)\) | safety/budget costs | `AgentStep.costs` |
| \(T,\Omega\) | world and sensing models | `WorldModel.transition()`, `WorldModel.observe()` |
| \(\pi(a\mid h_t)\) | decision rule | `Policy.select_action(history)` |

When these fields are explicit, “agent behavior” stops being mystical and becomes inspectable engineering.

## Three-theory braid

Expected-utility theory gives us the compass by declaring that rational choice under uncertainty is to pick \(a^\star\) maximizing \(\sum_s P(s\mid a)U(s)\), so preference becomes computation rather than rhetoric [[33](../../references.md#ref-33)] [[34](../../references.md#ref-34)]; sequential decision theory then warns that single-step cleverness is a trap because each move reshapes tomorrow’s opportunity set, captured by \(V^\star(s)=\max_a\{R(s,a)+\gamma\sum_{s'}T(s'\mid s,a)V^\star(s')\}\) and, under partial observability, by belief updates \(b_{t+1}(s')=\eta\,\Omega(o_{t+1}\mid s',a_t)\sum_s T(s'\mid s,a_t)b_t(s)\), which force planning over information as well as outcomes [[4](../../references.md#ref-4)] [[5](../../references.md#ref-5)] [[7](../../references.md#ref-7)]; and feedback control finally keeps this entire edifice honest by insisting that plans must survive noisy reality through closed loops such as \(x_{t+1}=Ax_t+Bu_t+w_t\), \(y_t=Cx_t+v_t\), and corrective control \(u_t=-K\hat{x}_t\), with state estimation continuously updating \(\hat{x}_t\) from observations, so intelligence is not perfect prediction but graceful correction under disturbance [[36](../../references.md#ref-36)] [[39](../../references.md#ref-39)] [[41](../../references.md#ref-41)].

## Short exercise

Take a real prompt you use (for example, “Refactor this module safely and quickly”) and formalize it as \((R,C,\text{termination})\): define one reward term for functional correctness, one for latency or token cost, at least one hard safety constraint, and a measurable stopping condition. Then write one sentence explaining which part of your spec corresponds to utility, dynamics, and feedback.

## How to study this formally

Build small benchmark tasks where \(R\) and \(C\) are explicit, perturb observations and transition assumptions, and compare policies by constrained return, regret, and violation rate. If a system cannot state its objective and constraints mathematically, it may still be impressive—but it has not yet earned the full title of agent.

## Translating the Theory into Agentic Practice

The practical gift of this topic is a design discipline: before building a clever loop, write the agent's charter. A production agent should begin with an explicit goal specification, an environment boundary, an action vocabulary, constraint budgets, and termination rules. For a coding agent, this means distinguishing "produce a patch" from "produce a patch that passes named tests, preserves public contracts, avoids unsafe files, fits within a time budget, and escalates when evidence is insufficient." The first sentence is a wish. The second is an architecture.

In implementation terms, treat \(R\), \(C\), and \(\mathcal{A}\) as configuration objects, not as folklore trapped in a prompt. The action registry should say which operations exist, what inputs are legal, what side effects they may cause, how much they cost, and what postconditions must be checked. The planner should score candidate actions against the current belief state and constraint ledger. The runtime should record each observation-action-transition triple so that later debugging can ask: did the agent choose badly, observe badly, or operate under a badly specified objective?

This also changes how we design human oversight. A vague agent needs vague supervision: "please be careful." A formalized agent can expose precise gates: "this edit touches authentication," "this command exceeds budget," "this step reduces expected reward unless it obtains new evidence." Escalation becomes part of the state machine rather than an apology after the machine has wandered into the machinery room with a lit candle.

The value of learning the theory is therefore immediate. It teaches us to replace prompt charisma with inspectable control. Goals become reward models and acceptance tests; environments become typed sources of observation and uncertainty; actions become contracts; constraints become budgets and guards; feedback becomes telemetry and correction. Once these pieces are explicit, better agents can be compared, improved, and governed. Without them, every success is anecdote and every failure is an interpretive fog.
