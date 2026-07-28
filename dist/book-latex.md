# Preface {-}

> A text for readers who suspect that agentic systems are not a bag of orchestration tricks, but programmable structures with laws, invariants, and failure modes.

This is a book about programs that act. Some software answers a question and stops. The software in this book keeps going: it looks at the world, decides something, does something, and then has to live with the result. That loop is the object of study here, and it turns out to have structure worth teaching.

The book follows the arc of *Structure and Interpretation of Computer Programs*. We start with the primitive elements of agency. We assemble them into interpreters. We study the architectures that make those interpreters useful. Then we examine what happens when many such systems act in one shared environment.

## A first trace, before any theory

Watch one small machine work. Suppose a coding agent sees this line of test output:

```
test_auth.py::test_expired_token FAILED
```

A careless system would jump straight to editing a file. This one writes down what it now believes:

```
{failing_behavior: "expired token",
 suspects: ["auth/session.py"],
 risk: "login regression"}
```

Then it chooses the action `read auth/session.py`. It observes a changed comparison against the token expiry time. It revises what it believes:

```
{suspected_cause: "off-by-one expiry check", evidence: "source inspected"}
```

Only now does it choose `edit auth/session.py`. Two ordinary actions, one small structure between them. That structure is the whole point: the observation became internal state before it became an action. Everything else in this book is an argument about what belongs in that state, who may change it, and what it costs to carry.

## Four words used precisely

Four terms recur constantly, so they are pinned down here rather than left to context:

- An **agent** is a system that observes some environment, keeps an internal account of what is going on, chooses actions, and receives consequences that shape its later choices.
- An **interpreter** is the explicit loop that gives those steps operational meaning: observe, update internal state, choose an action, execute, repeat.
- A **state abstraction** is the compressed representation the interpreter actually uses when deciding. It is not the whole raw transcript of everything that has happened. In the trace above, the short dictionary is the state abstraction; the full test log is not.
- **Orchestration** is the engineering discipline of arranging models, tools, memory, policies, budgets, safety checks, and human escalation so that the loop behaves like a governed machine rather than an improvising monologue. A **policy**, in the sense used throughout, is simply the agent's rule for choosing actions.

## Every pattern is an edit to the interpreter

The research program of this book begins with a modest trick. Treat each agentic pattern not as a recipe, but as a change to that interpreter. A pattern may alter any of the following:

- the state the agent carries,
- the control flow by which it reasons,
- the feedback it listens to,
- the memory it may consult,
- the authority it is permitted to exercise,
- the condition under which it must stop.

Making the change visible lets us ask the less glamorous but more useful question: did it earn its keep? So the questions this book keeps returning to are these four.

**First, how is a pattern represented structurally?** Name the part of the interpreter it edits. A vague pattern cannot be compared with anything.

**Second, what does it do to the measurable outcomes?** The evidence we care about is final task success, partial progress before failure, token use, latency, tool-call efficiency, and a smaller number of dangerous almost-actions. A pattern that lifts success from 60 to 66 tasks out of 100 while tripling token cost has not obviously won.

**Third, how do combined patterns interact?** Patterns collide as often as they cooperate. Retrieval may make planning sharper, or it may flood the policy with irrelevant facts. Oversight may prevent a bad deployment, or it may spend ceremony on a cheap, reversible step.

**Fourth, which task characteristics predict when a pattern helps?** Uncertainty, action stakes, reversibility, horizon length, available feedback, and budget all shift the answer. The right design is therefore a function of the task, not a fashion.

## How to read this book

The prerequisites are modest but real. You should be comfortable reading short Python-like pseudocode. You should be able to read a basic probability statement such as \(P(A\mid B)\), which reads "the chance of A given that B holds." You should also be able to read a summation such as \(\sum_t\), which means "add this quantity over the indicated steps."

No reinforcement-learning background is assumed. The early chapters build the needed vocabulary as they go. Numeric citations like [[1](#ref-1)] point to the reference list, where you can trace the scholarly ancestry of an idea.

Notation follows a small and stable convention. Time is written with subscripts, and sets are written with calligraphic letters. The following table lists the symbols that recur across the whole book, with the way to read each one aloud. Each chapter introduces further notation where it is needed, and defines it there:

| Symbol | Read it as | What it means |
|---|---|---|
| \(o_t\) | "o sub t" | the observation at step \(t\) |
| \(a_t\) | "a sub t" | the action at step \(t\) |
| \(s_t\) | "s sub t" | the world state at step \(t\), whether hidden from the agent or fully described |
| \(\mathcal{A}\) | "script A" | the action space, meaning the set of actions available |
| \(\pi\) | "pi" | a policy: a rule for choosing actions |
| \(R\) | "R" | a reward, which says what helped |
| \(C\) | "C" | a cost, which says what was spent or risked |
| \(\gamma\) | "gamma" | a discount, which says that nearer consequences count more heavily than distant ones |

A worked reading of the last row: with \(\gamma = 0.9\), a reward of 10 arriving one step from now is valued at 9, and the same reward two steps away is valued at 8.1. Impatience, written as arithmetic.

The central claim of this project is that agentic AI is a science of interaction and orchestration, not merely API plumbing.

Chapter 1 (Foundations of Agency) develops the core interpreter. Goals specify what matters. Belief tracks uncertainty. State abstraction makes history usable. Control turns action into a feedback loop. The later chapters elaborate that same interpreter with reasoning patterns, tools, memory, embodiment, and social coordination.

The method is constant. Each chapter changes the running interpreter, then asks when that change earns its cost in success, progress, efficiency, safety, or governability.


# Foundations of Agency

A thermostat holds a room at 21 degrees Celsius. It reads a sensor, then switches a heater on or off. That is already agency in miniature: a goal, an environment, and an action. Agency begins with that deceptively simple triad of **goals**, **environments**, and **actions**. We formalize it here, then progressively add uncertainty, representation, and control, so that later patterns can be compared without mysticism or marketing fog.

## One Interpreter, Extended Four Times

We build one running interpreter: a program that reads a specification and carries it out step by step. Each topic adds one layer to that interpreter, and one word to our vocabulary of comparison.

Topic 1 (Goals, Environments, and Actions) gives the loop a contract. It says what counts as state, observation, action, reward, cost, constraint, and stopping.

Topic 2 (Belief, Uncertainty, and Decision) adds belief. A thermostat's sensor can drift or lie. Belief lets the interpreter act when it does not know the true state.

Topic 3 (World Models and State Abstractions) adds representation, through state abstraction. The interpreter learns to carry the useful part of its history, without dragging the whole attic downstairs.

Topic 4 (Policies, Value, and Control) adds policy, feedback, authority, and control. Single choices become governed action.


## Goals, Environments, and Actions

Before anything clever can happen, an agent needs three things: something it is trying to achieve, a world it is acting inside, and a list of moves it is allowed to make. Those three things get written down here as a contract. Every later chapter extends that contract, and it is the first thing you inspect when an agent misbehaves.

An agent is not a model that emits impressive text. It is an interpreter for situated action. At each step it does four things:

- it reads a partial observation, meaning it sees only some of what is going on;
- it updates what it thinks is going on;
- it chooses an admissible action, meaning one the system permits;
- it accepts that the action changes the next problem it must solve.

Before we can discuss belief, memory, planning, or control, we need the contract that this interpreter is running.

### The Three Parts of the Contract

The contract has three parts, and each answers a different question:

- A **goal** says what outcomes count as better or worse.
- An **environment** says what can change outside the agent, and what the agent can observe.
- An **action vocabulary** says which interventions are legal, costly, reversible, and checkable.

Without these parts, the system may still be useful. But its behavior is difficult to compare, debug, or govern [[2](#ref-2)]. That difficulty is the practical cost of leaving the contract implicit.

### A Coding Agent Under Deadline

Imagine a coding agent tasked with shipping a bug fix before a release freeze. Its goal is not "write something clever." A defensible goal combines four pressures at once:

- the value of the task itself;
- the risk of causing a regression, meaning breaking something that used to work;
- deadline pressure;
- cost.

Its environment is only partly visible to it. That environment includes a partially observed repository, flaky continuous integration (CI, the automated system that builds and tests each change), hidden downstream dependencies, and a user whose constraints may be underspecified.

Its actions are ordinary engineering moves: reading files, editing code, running tests, asking for clarification, and opening a pull request. Each action does three things at once. It produces an observation, it consumes budget, and it may make later actions easier or harder [[3](#ref-3)] [[7](#ref-7)].

### The Smallest Agent Interpreter

This is already enough to write the smallest agent interpreter. The pseudocode below keeps a running `state` and a `history` of what happened, then loops: observe, update, choose, execute, record.

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

This loop is the experimental baseline for the rest of the book. Before adding retrieval, planning, reflection, tool governance, or multiple agents, we can ask what this plain interpreter achieves on its own. Five measurements are enough to start:

- whether it completes the task;
- how far it gets before stopping;
- how many tokens and tool calls it spends;
- how long it waits on feedback;
- which failures remain.

Later patterns are not magic additions. They are controlled mutations of this loop, and each one should be judged against the baseline this plain interpreter sets.

The rest of the chapter refines the three vague functions in this loop. Topic 2 (Belief, Uncertainty, and Decision) asks what `update_state` should mean when the world is uncertain. Topic 3 (World Models and State Abstractions) asks what information belongs in `state` rather than in the raw transcript. Topic 4 (Policies, Value, and Control) asks how `choose_action` becomes a policy that remains useful under constraints and feedback.

### Formal Contract

A common mathematical model is a partially observable Markov decision process (POMDP) with constraints. "Partially observable" means the agent cannot see the true state directly. The model is written as an eight-part tuple:

\[
\mathcal{M}=(\mathcal{S},\mathcal{O},\mathcal{A},T,\Omega,R,C,\gamma).
\]

Read that aloud as "the model M consists of states S, observations O, actions A, transitions T, observation model Omega, reward R, cost C, and discount gamma." Eight symbols in a single line is a lot to hold in mind, so the table in "From Symbols to Interfaces" maps each one to a field you would actually implement.

#### States, Observations, and Actions

Here \(\mathcal{S}\) is **latent world state**: the complete condition of the world that matters but is not directly visible. For the coding agent, \(s\in\mathcal{S}\) ("a state s drawn from the set S") might include the real bug location, whether a dependency is stale, and whether an unseen integration test will fail. The word latent simply means "present in the world, hidden from the agent's sensors."

\(\mathcal{O}\) is the set of observations, such as file contents, test output, logs, and user messages. \(\mathcal{A}\) is the action set, including `read_file`, `edit_file`, `run_tests`, `ask_user`, and `open_pr`.

#### How the World Moves and What the Agent Sees

The term \(T(s'\mid s,a)\) is the **transition dynamics**. Read it as "the chance the next hidden state is s-prime, given the current state s and action a." If \(a\) is `edit_file`, \(T\) describes how likely that edit is to move the repository from "bug present" to "bug fixed" or, less gloriously, to "new regression introduced."

The term \(\Omega(o\mid s,a)\) is the **observation model**. Read it as "the chance the agent sees observation o after action a when the world is in state s." A flaky test suite has an observation model with noise: the same hidden state can produce a pass one minute and a failure the next.

The last three symbols are the scoring machinery. \(R(s,a)\) is reward, \(C(s,a)\) is constraint cost, and \(\gamma\in(0,1)\) is a **discount factor**, a number strictly between zero and one that makes nearer consequences count more than distant ones [[4](#ref-4)] [[7](#ref-7)] [[51](#ref-51)].

#### The Markov Assumption Is a Design Choice

The Markov assumption is an interpretation, not a fact about reality. It says that the state representation is rich enough that the next transition can be modeled from the current state and action alone. When that assumption fails, the repair is usually one of three moves: better state, better memory, or a more cautious policy.

#### Reading the Objective, with Two Numbers

A policy \(\pi(a\mid h_t)\), with history \(h_t=(o_{0:t},a_{0:t-1})\), is evaluated by expected return subject to constraints. A **policy** is the rule for choosing actions. The notation \(\pi(a\mid h_t)\) reads "the probability that the policy chooses action \(a\) given history \(h_t\)," where the history holds every observation up to step \(t\) and every action before it.

Before the infinite sum appears, consider two concrete steps with \(\gamma=0.9\). Suppose `read_file` earns immediate reward \(R_0=1\) because it gathers useful evidence, and `edit_file` earns \(R_1=8\) after the evidence points to the right line. The two-step discounted return is

\[
R_0+\gamma R_1 = 1 + 0.9\cdot 8 = 8.2.
\]

If the first action instead rushed an edit with \(R_0=4\) but caused a next-step regression \(R_1=-5\), the return would be \(4+0.9(-5)=-0.5\). Patience wins here by more than eight points. Discounting does not worship delay; it merely lets the contract compare immediate temptation with later consequence.

The full objective extends that arithmetic over all future steps, and adds a budget line for every kind of cost:

\[
\max_{\pi}\;J(\pi)=\mathbb{E}_{\pi,T,\Omega}\!\left[\sum_{t=0}^{\infty}\gamma^t R(s_t,a_t)\right]
\quad\text{s.t.}\quad
\mathbb{E}_{\pi}\!\left[\sum_{t=0}^{\infty}\gamma^t C_j(s_t,a_t)\right]\le\kappa_j\;\forall j.
\]

Read it as "choose the policy with the largest expected discounted reward, subject to each expected discounted cost \(C_j\) staying under its own ceiling \(\kappa_j\)." This equation should not be mistaken for a demand that every product team hand-code a perfect reward function. Its practical use is diagnostic. It forces the designer to say three things out loud: which outcomes are being optimized, which costs are merely tradeoffs, and which constraints should stop the agent even when the short-term reward looks attractive.

### From Symbols to Interfaces

The same contract can be expressed as ordinary engineering fields. The table below pairs each formal symbol with its plain meaning and with the kind of field or method that carries it in code.

| Formal symbol | Meaning | Typical implementation field |
|---|---|---|
| \(\mathcal{O}, o_t\) | observations | `AgentStep.observation` |
| \(\mathcal{A}, a_t\) | admissible and chosen actions | `AgentSpec.action_space`, `AgentStep.action` |
| \(R(s_t,a_t)\) | task utility signal | `AgentStep.reward` |
| \(C(s_t,a_t)\) | safety, budget, or policy costs | `AgentStep.costs` |
| \(T,\Omega\) | world and sensing assumptions | `WorldModel.transition()`, `WorldModel.observe()` |
| \(\pi(a\mid h_t)\) | decision rule | `Policy.select_action(history)` |

Read the table as a promise: every symbol in this table must eventually become something you can log and inspect at runtime.

#### Utility, Option Value, and Correction After Measurement

Three older fields each contribute one rule to this contract.

Expected-utility theory supplies the local decision criterion: choose the action with greatest expected utility under the current interpretation of the world [[33](#ref-33)] [[34](#ref-34)].

Sequential decision theory adds that a locally attractive action can be bad if it destroys future options. That is the lesson captured by Bellman recursion in fully observed settings, where the value of a state is defined in terms of the values of the states it leads to [[5](#ref-5)].

Feedback control adds the implementation discipline: plans must be corrected after new measurements arrive, because disturbances and model error are normal rather than exceptional [[36](#ref-36)] [[39](#ref-39)] [[41](#ref-41)].

#### What This Demands of an Action Registry

For the coding agent, this means the action registry should say more than "can run shell commands." It should record five things per action:

- which commands are allowed;
- what they may modify;
- what evidence they are expected to produce;
- how much budget they consume;
- which postconditions must be checked afterwards.

A vague prompt asks the agent to be careful. A contract gives the runtime something to inspect.

### Exercise

Take a real prompt you use, such as "refactor this module safely and quickly." Rewrite it as a small agent contract with these parts:

- One reward term for functional correctness.
- One task-success condition that says what "done well enough" means.
- One meaningful intermediate milestone, such as "the failing test is reproduced" or "the risky subsystem has been identified."
- One reward or cost term for latency, money, or token use.
- At least one hard constraint.
- A measurable stopping condition, including when to stop after partial progress rather than spend the budget theatrically.
- The legal actions available to the agent.

Then identify which part of your spec describes utility, which part describes dynamics, and which part creates feedback. A good answer names a specific field for each of the three, and states each stopping condition as a number or a checkable test rather than an adjective. If you cannot answer those questions, the agent is still being steered by prose where it needs an interface.


## Belief, Uncertainty, and Decision

An agent almost never gets to see the world as it truly is. It sees fragments,
and must act anyway. Something has to turn those fragments into a picture solid
enough to act on. That machinery is called *belief*, and it is the second
component of the interpreter we are building.

The interpreter from Topic 1 (Goals, Environments, and Actions) cannot read the
true state of the world directly. It sees test output, file contents, user
messages, logs, retrieval results, and tool failures. Belief is the agent's
working account of what those observations imply. It is not a mood of confidence.
It is the state variable that makes action possible under *partial
observability* (the ordinary situation in which the agent's sensors show only
part of what is going on).

### Belief as Runtime State, Not a Feeling

Belief is a variable the program carries between steps, like a counter or a
cache. Three symbols do the work.

The table below names the three quantities that appear in every belief equation
in this section, together with how to read each one aloud.

| Symbol | Read it as | Meaning |
|---|---|---|
| \(s_t\) | "the state at step t" | The *latent* (hidden from the agent's sensors) state of the world |
| \(h_t=(o_{0:t},a_{0:t-1})\) | "the history at step t" | Everything observed so far, plus every action taken so far |
| \(b_t(s)=P(s_t=s\mid h_t)\) | "the belief at step t assigns to state s" | How likely the agent thinks state \(s\) is, given that history |

Under a POMDP (partially observable Markov decision process) interpretation,
belief evolves by Bayesian filtering [[7](#ref-7)]
[[4](#ref-4)]:

\[
b_{t+1}(s')=\eta\,\Omega(o_{t+1}\mid s',a_t)\sum_{s\in\mathcal{S}}T(s'\mid s,a_t)b_t(s),
\]

where \(\eta\) normalizes the distribution. The observation model also gives a
prediction about what the agent expects to see next:

\[
P(o_{t+1}\mid b_t,a_t)=\sum_{s'}\Omega(o_{t+1}\mid s',a_t)\sum_s T(s'\mid s,a_t)b_t(s).
\]

Read the filter as two moves: **predict**, then **correct**.

1. The inner sum \(\sum_s T(s'\mid s,a_t)b_t(s)\) predicts how likely each next
   state \(s'\) is after action \(a_t\), before the new observation arrives.
   Here \(T\) is the transition model and \(\mathcal{S}\) is the set of possible
   states.
2. The likelihood \(\Omega(o_{t+1}\mid s',a_t)\) then corrects that prediction.
   It asks how plausible the observed evidence would be if \(s'\) were true.
3. The constant \(\eta\), the Greek letter eta, is just the normalizer that
   makes all the updated probabilities add to \(1\).

Some vocabulary, defined once and used forever after. Conditional probability
\(P(X\mid Y)\) means "the probability of \(X\) after assuming or observing
\(Y\)." A **prior** is the belief before the new observation. A **likelihood**
is how well a possible state explains the observation. The **posterior** is the
corrected belief after combining them.

A two-state example makes the arithmetic concrete. Suppose the agent believes a
bug is in module A with probability \(0.5\) and in module B with probability
\(0.5\). A test fails. If that failure has likelihood \(0.9\) under "bug in A"
and \(0.1\) under "bug in B", the unnormalized scores are \(0.45\) and \(0.05\).
Divide by their sum, \(0.5\), and belief becomes \(0.9\) for A and \(0.1\) for
B. That division by \(0.5\) is \(\eta\) doing its only job.

#### Why Approximate Belief Still Counts as Belief

These equations are idealized. Real agents often use scores, hypotheses,
retrieval rankings, or learned estimators instead of exact distributions. The
key requirement is not mathematical ceremony. It is that observations change the
variables that action selection depends on.

The pseudocode below shows the minimum shape of a belief update in a practical
agent. It takes the old belief, a new observation, and the action just taken,
and returns a new belief made of three parts: the surviving hypotheses, a
recalibrated confidence, and the gaps that still matter for the decision.

```text
function UPDATE_BELIEF(belief, observation, action):
    hypotheses <- revise_hypotheses(belief.hypotheses, observation)
    confidence <- recalibrate(hypotheses, observation.source, observation.freshness)
    unknowns <- identify_decision_relevant_gaps(hypotheses)
    return Belief(hypotheses, confidence, unknowns)
```

In a coding agent, a failing test should increase belief in some fault
hypotheses and decrease others. A missing dependency error should not be treated
like a behavioral regression. A stale document should count as evidence with a
weaker likelihood than a current API response. This is what it means for belief
to be an operational object.

### Decisions in Belief Space

Once belief is explicit, decision quality can be evaluated in belief space. In
sequential problems this value is recursive. An action is good partly because of
the observations and opportunities it makes available later
[[5](#ref-5)].

\[
V^\pi(b)=\mathbb{E}\!\left[\sum_{t\ge 0}\gamma^t R(s_t,a_t)\mid b_0=b,\pi\right].
\]

Read that as "the value of following policy \(\pi\) from belief \(b\) is the
expected total reward, with rewards further in the future shrunk by the discount
factor \(\gamma\)." The symbol \(\mathbb{E}\) means "expected value", the
probability-weighted average.

At a single step, the expected-utility rule is:

\[
a_t^\star=\arg\max_{a\in\mathcal{A}}\mathbb{E}[U(a,S_t)\mid h_t],
\]

which reads "the best action \(a^\star\) is the one in the action set
\(\mathcal{A}\) with the highest average utility \(U\), averaged over the states
the history \(h_t\) still allows." This holds assuming the utility model and
belief distribution are adequate for the decision at hand
[[33](#ref-33)] [[34](#ref-34)]. The
assumption matters. If the belief state omits a safety-relevant variable, the
expected utility calculation can be precise and still wrong.

#### Two Roads and a Hidden Storm

Suppose an agent chooses between **Shortcut** \(A\) and **Detour** \(B\), while
weather \(S\in\{\text{clear},\text{storm}\}\) is hidden. Utilities are
\(U(A,\text{clear})=10\), \(U(A,\text{storm})=-20\), and
\(U(B,\text{clear})=U(B,\text{storm})=4\). With no forecast and equal prior
probabilities, \(A\) has expected utility \(-5\), so \(B\) is better. If a
forecast is 90 percent accurate and predicts clear weather, then \(A\)'s
expected utility becomes \(0.9(10)+0.1(-20)=7\), so \(A\) is better. The world
did not change; the action ranking changed because the belief did.

The arithmetic is small enough to leave on the page. Before querying,
\[
\mathbb{E}[U(A)]=0.5(10)+0.5(-20)=-5.
\]
After a forecast \(q=\text{clear}\) with 90 percent accuracy,
\[
\mathbb{E}[U(A)\mid q=\text{clear}]=0.9(10)+0.1(-20)=7>4=\mathbb{E}[U(B)\mid q=\text{clear}],
\]
so the shortcut becomes rational. If instead \(q=\text{storm}\), then
\[
\mathbb{E}[U(A)\mid q=\text{storm}]=0.1(10)+0.9(-20)=-17<4,
\]
so the detour remains rational. The same pair of roads supports different
actions because belief, not bravado, mediates between observation and control.

### Information Has a Price

Information gathering is not a prelude to action. It is an action with cost,
latency, and opportunity cost. Two features of a task decide whether another
query is worth making:

- **Uncertainty.** If the relevant state is already known well enough, another
  query is incense, not engineering.
- **The size of the action gap.** If the best action is far ahead of its rivals,
  evidence must be very surprising to change the ranking. If the alternatives
  are nearly tied, a small observation can be decisive.

A query is worthwhile when it is likely to change the decision enough to pay for
itself. The value of information, written VoI, states that condition exactly:

\[
\operatorname{VoI}(q)=\mathbb{E}\!\left[\max_a \mathbb{E}[U(a,s)\mid h_t,q]\right]
\;-\;\max_a \mathbb{E}[U(a,s)\mid h_t].
\]

Read it as "the best you expect to do after learning the answer to \(q\), minus
the best you can do now." To use it in practice, price the query in the same
units as utility and compare.

In the route example, querying the forecast raises expected utility from \(4\)
to \(5.5\):
\[
0.5\cdot 7 + 0.5\cdot 4 = 5.5,
\]
so the value of information is \(1.5\). The two halves of that sum are the two
possible forecasts: clear, worth \(7\), and storm, worth \(4\). If the query
costs \(0.8\), ask first. If it costs \(2\), act without it.

#### Entropy and Mutual Information: Measuring What Is Left to Learn

Information theory gives related measures of remaining uncertainty. Entropy
measures how spread out the belief is:
\[
H(S\mid h)=-\sum_s b(s)\log b(s).
\]
Mutual information measures how much a query \(Q\) is expected to reduce that
uncertainty:
\[
I(S;Q\mid h)=H(S\mid h)-H(S\mid h,Q).
\]
These symbols are not rival decision rules. \(H(S\mid h)\) says how much
uncertainty about state \(S\) remains after history \(h\). \(I(S;Q\mid h)\) says
how much of that uncertainty the query may retire. The value-of-information
calculation then asks whether retiring that uncertainty changes the action
ranking enough to pay for the query [[35](#ref-35)].

A quick check on entropy. A belief split \(0.5/0.5\) has entropy \(\log 2\), the
largest possible value for two states. A belief of \(1.0/0.0\) has entropy
\(0\), because nothing is left to learn. Entropy measures confusion; only VoI
measures whether that confusion is expensive.

#### Deciding Now While Protecting Later

Sequential control carries the same idea forward in time through a belief-space
Bellman equation:
\[
V^\star(b)=\max_a\{r(b,a)+\gamma\sum_o P(o\mid b,a)V^\star(\tau(b,a,o))\}.
\]
Here \(b\) is the current belief, \(r(b,a)\) is the immediate reward of acting
from that belief, \(P(o\mid b,a)\) is the probability of seeing observation
\(o\), and \(\tau(b,a,o)\) is the updated belief after action and observation.
The agent is therefore not merely selecting an action; it is selecting the
future quality of its own epistemic state [[5](#ref-5)]
[[7](#ref-7)].

The control loop now becomes a short branch on the size of the action gap. If
one action clearly wins, act. If not, consider buying evidence. If evidence
cannot help either, act with the assumption written down, or hand the decision
to a human.

```text
if action_gap(belief) is large:
    act(best_action)
else if cheap_observation_can_change_ranking(belief):
    gather_information()
else:
    act_with_recorded_assumption_or_escalate()
```

This pattern turns "be uncertain" into a policy. It also explains why more
retrieval is not automatically better. Retrieval, search, and external evidence
help only when they can move belief in a way that changes the ranking of
available actions, or at least changes whether acting, waiting, or escalating is
justified. Evidence is useful when it changes calibrated action quality per unit
cost. In feedback-control terms, estimation and action are coupled: the agent
measures because the measurement may change the next control move, and it acts
knowing that the next measurement may correct it
[[36](#ref-36)] [[41](#ref-41)].

### Approximation and Calibration

Exact Bayesian filtering is often too expensive for production loops.
Approximation is acceptable when it is decision-safe, not merely statistically
elegant. Let

\[
\Delta(b)=Q(b,a^\star)-\max_{a\ne a^\star}Q(b,a)
\]

be the action gap, read as "the value of the best action minus the value of the
best runner-up." If an approximation \(\tilde Q\) has uniform error
\(\lvert \tilde Q(b,a)-Q(b,a)\rvert\le \varepsilon_Q\), then the greedy action
is unchanged whenever \(\Delta(b)>2\varepsilon_Q\). The error can push the best
action down by \(\varepsilon_Q\) and the runner-up up by \(\varepsilon_Q\), so
\(2\varepsilon_Q\) is the worst-case swing. This simple bound is useful because
it ties inference quality to policy quality: approximation error matters most
near decision boundaries [[37](#ref-37)]
[[38](#ref-38)].

For example, suppose a coding agent estimates \(Q(b,\text{SafePatch})=10\) and
\(Q(b,\text{FastPatch})=7\), so the action gap is \(\Delta=3\). If the value
approximation can be wrong by at most \(\varepsilon_Q=1\) for each action, then
\(2\varepsilon_Q=2\), and \(3>2\). Even after accounting for approximation
error, SafePatch remains the greedy choice. If the gap were only \(1.5\), the
same estimator would not justify confidence in the ranking; the agent should
gather evidence, choose the safer default, or escalate.

#### Making Confidence Mean Something

Calibration is the corresponding empirical discipline. A confidence estimate
should mean what it says under proper scoring rules such as the Brier score
[[49](#ref-49)]. For a binary event, the Brier score is
\((p-y)^2\), where \(p\) is the predicted probability and \(y\) is \(1\) if the
event happened and \(0\) otherwise; lower is better. Predicting a test will pass
with probability \(0.8\) and then seeing it fail gives \((0.8-0)^2=0.64\).
Predicting \(0.2\) and seeing failure gives \(0.04\). A builder can measure this
directly: log each stated probability, log what happened, and average the
squared differences.

Calibrated belief also changes what an agent can say about itself. A
belief-aware customer-support agent can distinguish "I know the refund policy"
from "I know the policy but not whether this order qualifies." A belief-aware
coding agent can distinguish "the failing test localizes the bug" from "three
modules remain plausible, so editing now is premature."

The interpreter has therefore gained its second component. Goals and actions
define what the agent is trying to do; belief defines what the agent thinks is
true enough to justify the next move. Topic 3 (World Models and State
Abstractions) takes up the next question: which parts of the world deserve to be
in the state at all.


## World Models and State Abstractions

What should an agent carry in its head from one decision to the next? Two ideas answer that question. A **world model** says how the world tends to change. A **state abstraction** says which parts of the past are worth keeping when choosing the next action. Get these wrong and the agent either forgets what it needed or chokes on what it did not.

Belief cannot remain an ever-growing transcript. An agent that remembers every token as equally available state has not become wise; it has made planning expensive and brittle.

The design problem is selective forgetting. Forget too much and the agent loses the variables that make action competent. Retain too much and the policy drowns in irrelevant distinctions. Good abstraction is compression in service of control.

### From History to Decision State

#### The Formal Setup: Compressing a Decision Problem

Let the ground control problem be a **Markov decision process (MDP)**, written as the tuple \((\mathcal S,\mathcal A,T,R,\gamma)\) [[4](#ref-4)] [[5](#ref-5)]. Read the pieces aloud like this: \(\mathcal S\) is the set of states, \(\mathcal A\) is the set of actions, \(T\) is the transition rule saying which state comes next, \(R\) is the reward, and \(\gamma\) (gamma) is the discount that makes distant rewards count less.

Now let \(\phi:\mathcal S\to\mathcal Z\) map detailed states to abstract states. Read \(\phi\) (phi) as "the compression map that sends a detailed state to its coarser label". Exact **homomorphism** requires reward and transition consistency [[37](#ref-37)]:

\[
R(s,a)=\bar R(\phi(s),a),\qquad
\sum_{s':\phi(s')=z'}T(s'\mid s,a)=\bar T(z'\mid \phi(s),a).
\]

A homomorphism is a structure-preserving map. In ordinary programming terms, \(\phi\) is a compression function. It is allowed to rename and merge states only when the merged states still behave the same way for decisions.

The barred symbols \(\bar R\) and \(\bar T\) live in the abstract world \(\mathcal Z\). So \(\bar T(z'\mid z,a)\) means "the transition probability between abstract states after compression". The sum on the left collects all detailed next states \(s'\) that \(\phi\) maps into the same abstract state \(z'\).

#### A Four-State Coding Example You Can Check by Hand

Here is a four-state coding example. Let the detailed states be:

- \(s_1=\) "tests red because dependency missing";
- \(s_2=\) "tests red because dependency missing and cache stale";
- \(s_3=\) "tests red because behavior regressed";
- \(s_4=\) "tests green".

A useful abstraction might map \(\phi(s_1)=\phi(s_2)=z_D\) for dependency trouble, \(\phi(s_3)=z_B\) for behavioral bug, and \(\phi(s_4)=z_G\) for green.

Now check the two conditions with small numbers. Suppose the action `install_dependency` gives reward \(+3\) in both \(s_1\) and \(s_2\), and moves to \(z_G\) with probabilities \(0.80\) and \(0.78\). The rewards match exactly, and the transition probabilities differ by only \(0.02\). Merging \(s_1\) and \(s_2\) therefore approximately preserves reward and transition.

Contrast that with a bad merge. Suppose `edit_logic` gives \(-2\) in \(s_1\) but \(+6\) in \(s_3\). Collapsing \(s_1\) and \(s_3\) into a single `tests_red` state fails action preservation. The same abstract state would recommend incompatible repairs, because the reward gap is \(8\), not \(0\).

#### Planning Inside the Compressed Space

Under those assumptions, planning can occur in the compressed space:

\[
\bar V^{*}(z)=\max_{a\in\mathcal A}\Big[\bar R(z,a)+\gamma\sum_{z'}\bar T(z'\mid z,a)\bar V^{*}(z')\Big].
\]

Read this as: the best long-run value of an abstract state is the best available immediate abstract reward plus the discounted average value of wherever that action lands you. The practical payoff is that the planner never has to look at the full detailed state space.

#### What Approximate Abstractions Cost You

The assumptions are strong. Approximate abstractions are more realistic. Their errors should be interpreted as possible value loss rather than as harmless summarization noise. A standard simulation-style bound has the shape

\[
\|V^{*}-\bar V^{*}\!\circ\phi\|_\infty \lesssim \frac{\varepsilon_R}{1-\gamma}+\frac{\gamma R_{\max}}{(1-\gamma)^2}\varepsilon_P,
\]

where \(\varepsilon_R\) and \(\varepsilon_P\) bound reward and transition mismatch [[37](#ref-37)] [[39](#ref-39)]. The message is practical. Every compressed-away detail is acceptable only if it does not materially change the action the agent should take.

Two pieces of notation deserve a plain reading. The norm \(\|\cdot\|_\infty\), called the **supremum norm** or **sup norm**, means "look at the largest absolute error over all states". The symbol \(\lesssim\) means "bounded up to a conventional constant or omitted technical factor". It is a mathematician's compact way of saying that the right-hand side controls the scale of the left-hand side.

The assumptions behind the bound are doing real work:

- rewards must be bounded by \(R_{\max}\), the largest reward magnitude;
- the discount must satisfy \(\gamma<1\);
- \(\varepsilon_R\) and \(\varepsilon_P\) must genuinely bound the abstraction's reward and transition errors.

Watch the discount term. With \(\gamma=0.9\), the factor \(1/(1-\gamma)^2\) is \(100\). With \(\gamma=0.99\) it is \(10{,}000\). If \(\gamma\) is close to \(1\), small transition errors can echo for a long time. That is why a cheerful summary such as `repo_status: messy` is not enough for high-stakes editing.

### Logs Are Archives; State Is Policy Fuel

#### Separating the Audit Trail from the Decision State

A useful implementation separates raw memory from decision state. The code below keeps two fields: an append-only `event_log` for auditing and retrieval, and a small `decision_state` that the policy actually reads. Ingestion writes to both; acting reads only the compact one.

```python
from dataclasses import dataclass

@dataclass
class AgentMemory:
    event_log: list[dict]        # audit trail and retrieval source
    decision_state: dict         # compact features used by policy


def ingest(observation: dict, mem: AgentMemory) -> AgentMemory:
    mem.event_log.append(observation)
    evidence = extract_decision_relevant_features(observation)
    mem.decision_state = update_state(mem.decision_state, evidence)
    return mem


def act(mem: AgentMemory):
    return policy(mem.decision_state)
```

For a coding agent, the decision state may include:

- the failing behavior;
- the touched files;
- dependency hints;
- test status;
- active constraints;
- unresolved hypotheses;
- remaining budget.

It usually does not need every line of conversation. Raw logs remain available for audit and targeted retrieval. But retrieval should be a gated action with explicit cost, as later memory systems will develop in more detail (see [Memory Systems, Context, and Retrieval](#memory-systems-context-and-retrieval)).

#### The Sufficiency Condition That Licenses Forgetting

The formal requirement is conditional sufficiency:

\[
P(s_{t+1},r_t\mid h_t,a_t)=P(s_{t+1},r_t\mid z_t,a_t),\qquad z_t=\psi(h_t).
\]

Read the left side as "the chance of the next state and this step's reward given the whole history \(h_t\) and the action \(a_t\)". Read the right side the same way, but with the compressed state \(z_t\) in place of the history. The map \(\psi\) (psi) is the summarizer that turns history into that compact state.

This says that, for the next decision, the compressed state \(z_t\) carries the predictive information from history that matters. It does not say the archive is useless. It says the policy should not be forced to plan over the archive unless the current decision needs it.

Action selection can then be interpreted as expected-utility maximization over \(z_t\), provided the abstraction preserves the distinctions that affect utility [[34](#ref-34)]. A quick check for builders: if two histories produce the same \(z_t\) but you would want different next actions, the abstraction is already broken.

### Behavioral and Causal Fidelity

#### Measuring "Close Enough" with Bisimulation Distance

Bisimulation metrics sharpen the idea of "close enough" by measuring whether two states behave similarly under action [[38](#ref-38)]:

\[
d(s,s')=\max_{a\in\mathcal A}\Big(|R(s,a)-R(s',a)|+\gamma\,W_d\big(T(\cdot\mid s,a),T(\cdot\mid s',a)\big)\Big),
\]

with \(W_d\) the Kantorovich lift induced by \(d\), which turns a distance between single states into a distance between distributions over states. If \(d(s,s')\) is small, the states are interchangeable up to a quantified tolerance. If "test failed because dependency missing" and "test failed because behavior regressed" collapse into the same feature `tests_red`, the abstraction may be compact, but it is not behaviorally faithful.

A **bisimulation** asks whether two states can answer the same action questions. Do they give similar immediate rewards? Do they lead to similar distributions over future states? The first term in the formula checks reward. The second term compares transition distributions.

\(W_d\), the **Kantorovich lifting**, is a way to lift a distance between individual states into a distance between probability distributions over states. Intuitively, it asks how much "work" is needed to transport probability mass from one next-state distribution to the other, when moving mass between unlike states is expensive.

The exact transport machinery can wait; the engineering lesson cannot. If two situations lead to different repair actions, their distance should not be treated as zero merely because the same red test banner appears.

#### Why Acting Agents Need Causal Models, Not Just Correlations

Agents also need causal fidelity when they intervene. A causal world model encodes mechanisms rather than only associations [[6](#ref-6)]:

\[
X_i=f_i(\mathrm{Pa}(X_i),U_i),\qquad P(x_1,\dots,x_n)=\prod_i P(x_i\mid \mathrm{pa}_i).
\]

Intervention semantics replace observation with action:

\[
P(x_1,\dots,x_n\mid \mathrm{do}(X_j=x))=\mathbf{1}[x_j=x]\prod_{i\neq j}P(x_i\mid \mathrm{pa}_i).
\]

These are **structural causal equations**. Each variable \(X_i\) is produced by a function \(f_i\) of its parents \(\mathrm{Pa}(X_i)\) and background disturbance \(U_i\). Read \(\mathrm{Pa}(X_i)\) as "the parents of \(X_i\)", meaning the variables that directly cause it. The product factorization says the joint probability can be assembled from each variable given its parents.

The notation \(\mathrm{do}(X_j=x)\) means an intervention: set \(X_j\) to \(x\) by action, rather than merely observing that it happened to equal \(x\). The indicator \(\mathbf{1}[x_j=x]\) reads "one when \(x_j\) equals \(x\), zero otherwise", which is how the equation records that the intervened variable no longer listens to its parents. In code-agent language, observing that "tests pass after a cache clear" is not the same as knowing that clearing the cache caused the pass. Perhaps the dependency install was the real mechanism.

That distinction matters for agents because they do not merely predict. They edit files, send messages, allocate resources, and call tools. "This change correlated with lower latency" is weaker than "raising worker count lowers queue latency after a delay and raises cost".

A state abstraction that erases the difference between correlation and intervention will mislead control. Feedback laws such as \(u_t=-K\hat x_t\) are a reminder of the point. Read that as "the control input at time \(t\) is minus a gain matrix \(K\) times the estimated state \(\hat x_t\)". The estimated state is not a report for its own sake; it is the input to correction [[36](#ref-36)] [[41](#ref-41)].

### Studying Abstractions

#### Good Compression Depends on the Task

Evaluate abstractions by downstream behavior. The quality of a compression is task-dependent, because different tasks preserve different distinctions.

- A customer-support agent may need order status, policy version, and jurisdiction, while safely ignoring the poetic texture of the complaint.
- A coding agent may need failing behavior, touched files, dependency state, and test scope, while ignoring most pleasantries in the transcript.
- A summarizer may compress away execution permissions that a deployment agent must keep in letters ten feet high.

#### Five Measurements Worth Taking

These are the quantities to instrument when you are judging a candidate abstraction:

- Value loss: \(\Delta_V=\|V^{*}-\tilde V^{*}\circ\phi\|_\infty\), read as "the largest gap, over all states, between true optimal value and the abstract value pulled back through \(\phi\)". Estimate it by scoring the abstract policy in the detailed environment.
- Intervention fidelity: predicted and observed effects under controlled actions. Measure it by taking the action deliberately and comparing outcome to prediction.
- Robustness under distribution shift, meaning a change between the situations the abstraction was designed on and the ones it now meets, especially when retrieval budgets are constrained. Measure it by rerunning the same tasks with a tighter retrieval budget and watching how fast value loss grows.
- Action preservation: whether states mapped to the same \(z\) really support the same action.
- Token and latency savings: whether the smaller state reduces context size, model time, retrieval work, and tool waiting, without buying those savings by erasing decision-relevant variables.

The interpreter now has a compact internal language. Topic 1 (Goals, Environments, and Actions) gave it a contract. Topic 2 (Belief, Uncertainty, and Decision) gave it belief. This topic gives it a state representation small enough to act on but faithful enough to trust. The remaining question is how action selection becomes governed control rather than a single eager choice.


## Policies, Value, and Control

Three topics have now handed us ingredients and no cook. Topic 1 (Goals, Environments, and Actions) supplied a goal contract, Topic 2 (Belief, Uncertainty, and Decision) supplied a belief state, and Topic 3 (World Models and State Abstractions) supplied a compact world model. What is still missing is the part of an agent that actually chooses. A **policy** is the rule that turns those three ingredients into an action.

A policy is not merely "what the model says next." It is the decision procedure that decides which proposal is allowed to become an event in the world.

### Value as Consequence Accounting

#### Reading the Value Functions

Value is consequence accounting: a number saying how well things go after an action.

Let \(\pi(a\mid s)\) be a policy over an MDP (Markov decision process: a model where the next state depends only on the current state and the chosen action). Read \(\pi(a\mid s)\) as "the chance the policy picks action \(a\) when the state is \(s\)". The value functions record expected discounted consequence:

\[
V^\pi(s)=\mathbb{E}_\pi\!\left[\sum_{t=0}^{\infty}\gamma^t r_t\mid s_0=s\right],\qquad
Q^\pi(s,a)=\mathbb{E}_\pi\!\left[\sum_{t=0}^{\infty}\gamma^t r_t\mid s_0=s,a_0=a\right].
\]

Read the first as "the average total reward \(\pi\) collects starting from state \(s\)". Read the second as "the same average, but the first action is forced to be \(a\)". Here \(r_t\) is the reward at step \(t\), \(\mathbb{E}_\pi\) means "average over what policy and world might do", and \(\gamma\) (gamma) is the discount factor between 0 and 1 that makes later rewards count for less.

With \(\gamma=0.9\) and reward 1 at each of the first three steps, the discounted total is \(1+0.9+0.81=2.71\), not 3. Distant reward is real, but worth less than reward now.

#### Bellman Recursion: Value in One Step Plus the Rest

Bellman recursion makes consequence compositional: a long future factors into one step plus what follows [[5](#ref-5)] [[39](#ref-39)]:

\[
V^{*}(s)=\max_{a\in\mathcal{A}}\left\{R(s,a)+\gamma\sum_{s'\in\mathcal{S}}T(s'\mid s,a)V^{*}(s')\right\}.
\]

Read this as "the best value of state \(s\) is the best available immediate reward \(R(s,a)\) plus the discounted average value of wherever you land". The set \(\mathcal{A}\) holds available actions, \(\mathcal{S}\) holds possible states, and \(T(s'\mid s,a)\) is the chance of moving to \(s'\) after doing \(a\) in \(s\).

The one-step decision-theoretic rule remains expected utility [[33](#ref-33)] [[34](#ref-34)]:

\[
a_t^{*}=\arg\max_a\;\mathbb{E}[U(a,S_t)\mid h_t].
\]

Read that as "pick the action whose average usefulness \(U\) is highest, given the history \(h_t\) observed so far". The operator \(\arg\max\) returns the winning action, not the winning number.

The connection between the two views is interpretive. Expected utility scores candidate actions under current belief. Dynamic programming, the Bellman style of reasoning, accounts for how today's action changes tomorrow's possibilities. When the world model is partial or approximate, these values are estimates, and their errors must be managed rather than ignored. In practice, log value estimates beside realized outcomes to see how far off they were.

### The Vocabulary of Learned Policies

Unwrap the learning vocabulary first. Five terms do most of the work:

- A **parameterized policy** \(\pi_\theta\) is a policy with adjustable numbers \(\theta\) (theta), much as a neural network has weights.
- The expression \(\pi_\theta(a\mid s)\) is the probability this policy assigns to action \(a\) in state \(s\).
- Its logarithm, \(\log\pi_\theta(a\mid s)\), turns products of probabilities into sums. That gives learning algorithms a handle on "make this sampled action more or less likely."
- A **gradient** \(\nabla_\theta J(\theta)\) is the direction in parameter space that most steeply increases the objective \(J\), at least locally. Read \(\nabla_\theta\) as "slope in the parameters".
- A **baseline** is a quantity subtracted from the return estimate to reduce noisy fluctuation without changing the expected update. That fluctuation is **variance**: sample-based estimates jump around even when their average is correct.

#### The Policy-Gradient Theorem and the Advantage Baseline

Parameterized policies can adapt from experience. The policy-gradient theorem gives one standard form [[40](#ref-40)]:

\[
\nabla_\theta J(\theta)=\mathbb{E}_{\pi_\theta}\!\left[\nabla_\theta\log\pi_\theta(a\mid s)\,Q^{\pi_\theta}(s,a)\right],
\]

often using the advantage baseline \(A^\pi(s,a)=Q^\pi(s,a)-V^\pi(s)\) to reduce variance without changing the expected gradient [[3](#ref-3)] [[40](#ref-40)]. Read the advantage as "how much better this action is than the policy's average behavior in this state". If \(Q^\pi(s,a)=8\) and \(V^\pi(s)=7.5\), the advantage is \(0.5\): a mild nudge upward, not a triumph.

For agentic systems, the lesson outlives any one learning algorithm. Judge policy improvement by four measurable things:

1. realized return, the reward actually collected;
2. constraint violations, the rules actually broken;
3. calibration, whether stated confidence matched observed accuracy;
4. stability, whether behavior stayed sane across runs.

Persuasiveness of the chosen action is not on the list.

### Proposal, Adjudication, Oversight

#### A Patch That Looks Attractive and Is Not

Consider a coding agent choosing between **FastPatch** and **SafePatch** before a production freeze. Its proposer estimates:

\[
\hat Q(s,\text{FastPatch})=9.2,\qquad \hat Q(s,\text{SafePatch})=7.4.
\]

The hat on \(\hat Q\) means "estimated", not "known". A proposer with full authority would ship FastPatch every time. That is a proposer-only policy: generate the most attractive action under the proposal model, then let it become reality.

A governed policy is different. It separates the authority to suggest from the authority to execute. It makes that second authority answer to constraints, evidence, reversibility, and risk. The real objective is constrained:

\[
\max_\pi\;\mathbb{E}_\pi\!\left[\sum_{t\ge 0}\gamma^t r_t\right]
\quad\text{s.t.}\quad
\mathbb{E}_\pi\!\left[\sum_{t\ge 0}\gamma^t c_t\right]\le \kappa.
\]

Read this as "earn as much discounted reward as possible, while keeping expected discounted cost \(c_t\) at or below the budget \(\kappa\) (kappa)". Here "s.t." means "subject to".

FastPatch may carry authorization risk, rollback blast radius, or inadequate evidence. Constrained decision-making treats those as part of the policy rather than as after-the-fact regret [[51](#ref-51)] [[53](#ref-53)].

Oversight earns its cost according to the task. It can be wasteful for cheap reversible actions, such as reading one more local file or running a narrow test. It can be essential for risky irreversible actions, such as deploying to production, deleting data, spending money, or sending a binding message under an organization's name.

#### The Governed Policy in Pseudocode

The pseudocode below governs one decision: sample candidates, score each on value, risk, and evidence quality, then check the winner against hard constraints before executing.

```text
function ACT(decision_state z_t, belief b_t, history h_t):
    candidates <- proposer.sample_actions(z_t, b_t, K)

    for a in candidates:
        value[a] <- estimate_return(z_t, b_t, a)
        risk[a] <- estimate_constraint_cost(z_t, b_t, a)
        evidence[a] <- evidence_quality(b_t, a)
        score[a] <- value[a] - lambda * risk[a] + beta * evidence[a]

    a_star <- argmax(score)

    if violates_hard_constraints(z_t, b_t, a_star):
        return fallback_or_escalate(z_t, b_t, h_t)

    return execute(a_star)
```

Put numbers into the scoring line. Let \(\lambda=2\) price risk and \(\beta=0.5\) reward evidence. FastPatch has value \(9.2\), risk \(2.0\), evidence \(0.4\), so its score is \(9.2-2(2.0)+0.5(0.4)=5.4\). SafePatch has value \(7.4\), risk \(0.6\), evidence \(0.9\), so its score is \(7.4-2(0.6)+0.5(0.9)=6.65\).

The unconstrained value estimate preferred FastPatch. The governed policy prefers SafePatch, because risk and evidence are first-class terms rather than whispered anxieties.

This decomposition is not bureaucracy for its own sake. It lets a language model be a generous proposer while the policy remains accountable for value, evidence, reversibility, and hard constraints.

### Value Is Not Confidence

Two numbers are easy to confuse. Value estimation asks, "If I take this action, how much utility should I expect?" Confidence scoring asks, "How reliable is this prediction or label?" They are related but not interchangeable:

\[
\hat V(s)\approx \mathbb{E}\!\left[\sum_{t\ge0}\gamma^t r_t\mid s\right],
\qquad
\hat p(y\mid x)\approx P(Y=y\mid X=x).
\]

The left expression estimates future reward from state \(s\). The right one estimates the probability that label \(y\) is correct for input \(x\).

Confidence models are judged by calibration metrics such as Brier score [[49](#ref-49)]. To measure it, bucket predictions by stated confidence and compare claimed with observed accuracy. Value models are judged by downstream return and constraint behavior.

Three cases show why one number cannot do both jobs:

- an action can be certainly useless, with high confidence and no value;
- an action can be uncertain but valuable, with low confidence and high expected payoff;
- an action can look attractive only because the risk model is blind to what it would break.

A serious policy keeps these quantities separate.

### Closed-Loop Control

#### Plan a Little, Act Once, Look Again

Model predictive control (MPC) captures the rhythm agent systems need, in four steps: plan over a finite horizon, execute the first action, observe the new state, and replan [[41](#ref-41)] [[51](#ref-51)] [[52](#ref-52)].

In linear feedback form this appears as \(u_t=-K\hat x_t\), read as "the control input at time \(t\) is a fixed gain matrix \(K\) applied to the estimated state \(\hat x_t\), with the sign flipped to push error toward zero". Estimation and control are coupled: the controller can only act on what the estimator believes. In software agents the same idea appears as small verified actions, telemetry, rollback plans, budget checks, and escalation gates.

#### A Plan-Act-Observe-Replan Trace

At step 0, the coding agent plans four moves: read the failing test, inspect the suspected module, apply a minimal patch, run the narrow test. It executes only the first action, `read failing test`. It observes that the assertion concerns timezone parsing rather than authentication.

At step 1, it replans: inspect `time_utils.py`, avoid auth code, and run the timezone-specific test. It executes `read time_utils.py`, observes a naive datetime conversion, and replans again toward a smaller edit.

The plan is not thrown away because planning was foolish. It is revised because reality has finally joined the meeting.

#### The Full Interpreter Loop

The interpreter now looks like the loop below. Each pass observes, updates belief, abstracts the state, chooses a governed action, executes it, and appends the result to history.

```text
while not terminated:
    o_t <- observe()
    b_t <- update_belief(b_t, o_t)
    z_t <- abstract_state(history, b_t)
    a_t <- governed_policy(goal, z_t, b_t, constraints)
    outcome <- execute(a_t)
    history <- append(history, o_t, a_t, outcome)
```

That loop is the chapter's foundation. Goals define what matters. Belief manages uncertainty. State abstraction chooses what the policy can reason over. Control closes the loop after reality answers back.

From here, later chapters can study reasoning architectures, tools, memory, and multi-agent systems as refinements of this basic interpreter rather than as disconnected tricks.


# Reasoning Architectures

Picture an agent asked to fix a failing test. Before editing a file, it reads the error, recalls what the module does, and sketches two candidate causes. All of that happens inside the agent, and this chapter is about those inner steps.

## Reasoning as an Interpreter, Not a Mood

This chapter treats reasoning systems as interpreters. An *interpreter* is a program that repeatedly reads a state and takes one legal step. Here the loop runs over thought, memory, action, and critique.

Chapter 1 gave us the basic agent machine, in five moves:

1. Observe the world.
2. Update belief, meaning the agent's current best account of hidden facts.
3. Choose a governed action, meaning one allowed by its constraints.
4. Execute it.
5. Learn from the result.

Chapter 2 adds a new layer inside that machine: a reasoning interpreter that can spend controlled internal steps before touching the outside world. Internal steps cost time and tokens, so budget them.

That layer changes the question. Instead of asking only "what should the agent do next?", we now ask "what legal thinking, planning, remembering, and self-checking steps may the agent run before it acts?"

## The Running Example, and the Four Things It Learns to Do

The running example is the same practical creature in a more elaborate costume: a coding or research agent trying to complete a task without inventing evidence, exceeding budget, or confusing a wish with a dependency. Wanting a library to export a function does not make the export exist.

Across this chapter, that agent will do four things:

- Reason as a transition system, meaning states plus rules for legal moves between them.
- Plan by searching through possible interpreter states.
- Retrieve memory as an action with cost and risk, not as a free lookup.
- Debug itself by inspecting whole traces rather than final answers alone.

## These Parts Are Options, Not a Mandatory Parade

Planning, memory, retrieval, and reflection should not be read as a royal procession of stages that every agent must always march through. They are alternative modifications to the same machine.

Consider three tasks. One may need a deeper search horizon, meaning it looks further ahead. Another may need a stricter memory policy. A third may need reflection after a failed tool call, and no reflection at all before a trivial answer.

The useful question is not "did we add all the fashionable organs?" but which change to state, control flow, feedback, memory, authority, or stopping condition improves *this* task enough to justify its cost. Sometimes none do.


## Reasoning Loops as Interpreters

Read an agent's reasoning as a small programming language: it has a state, a set of legal moves, and a rule that says when the computation is finished. Once you see reasoning that way, you can ask precise questions about it instead of admiring it. You can also debug it, which is the more useful skill.

### What a Reasoning Architecture Adds to the Loop

Chapter 1 ended with an agent interpreter. Its cycle was: observe, update belief, abstract state, choose a governed action, execute, and repeat.

A reasoning architecture is a refinement of that interpreter. It is the part of the agent that decides which internal computations count as legal steps before an external action is allowed to occur. In other words, it governs the thinking that happens between two moments of consequence.

This shift matters because "reasoning" is otherwise too easy to treat as a mood of the model. In an engineered agent, reasoning is a transition system: a machine that moves from one state to another by named steps. Such a system has four visible parts:

- state, meaning everything the loop currently knows and holds;
- admissible moves, meaning the steps the loop is allowed to take;
- guards and budgets, meaning the conditions and resources that permit a move;
- halting conditions, also called stopping conditions in this book, meaning the test that says the computation is done.

Once those pieces are explicit, we can ask ordinary semantic questions. What states can this loop reach? Which transitions mutate the outside world? Which invariants are preserved? Which failures are illegal states rather than disappointing outputs? The last question is the sharpest one. A disappointing output is a matter of taste; an illegal state is a bug with a location.

### Why "Pattern" Must Mean Something Mechanical

Call an agentic pattern a disciplined change to this little machine. A pattern earns the name by changing one of five things:

1. It may add a field to state, such as a plan frontier (the set of plan steps still open) or a memory handle (a reference the loop can use to fetch stored material).
2. It may add legal transitions, such as `retrieve` or `critique`.
3. It may introduce a feedback channel, such as test results that update the controller rather than merely decorate the transcript.
4. It may strengthen authority guards before dangerous actions.
5. It may change the halt predicate, so the agent stops only after evidence, budget, and task conditions line up.

This definition keeps the word "pattern" from becoming incense. A pattern is not a vibe; it is a modification to machine state, legal transitions, feedback channels, authority guards, or the predicate that says the computation is done.

### The Machine State

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
with legality defined by inference rules in the style of structural operational semantics [[42](#ref-42)]. Read the arrow as "state sigma steps to state sigma-prime by a step of kind ell".

A tool call, for example, can fire only when its arguments satisfy the tool schema and the loop still has budget:
\[
\frac{\texttt{schema\_ok}(a,\tau)\ \wedge\ \kappa>0}{\langle \texttt{act}(a),\sigma\rangle \to \sigma'}.
\]

#### Reading the Inference Rule as a Legal Tablet

Read the inference rule as a tiny legal-code tablet. The facts in the numerator, the upper part of the fraction, are premises. Here there are two of them: the proposed action \(a\) must match the tool context \(\tau\), and the remaining budget \(\kappa\) must be positive. The statement in the denominator, the lower part, is the transition the interpreter is allowed to take when those premises hold.

Structural operational semantics is the discipline of defining a language by such local execution rules. It does not offer a paragraph saying what the whole program "means". It specifies which small steps are legal from each state.

The rule is small, but its effect is large. An invalid tool call becomes a violation of the agent language, not a vague "model mistake". A builder checks this rule by refusing the call at the boundary: if the arguments fail validation, or the budget reads zero, no external call is made and the refusal is recorded with a reason.

#### Traces, Reachability, and Invariants

The complete loop is the execution relation generated by repeated one-step execution:
\[
\sigma_0 \xrightarrow{\ell_0} \sigma_1
\xrightarrow{\ell_1}\cdots
\xrightarrow{\ell_{T-1}} \sigma_T,
\qquad \texttt{halt}(\sigma_T).
\]
Read this as a chain: the loop starts at \(\sigma_0\), takes labeled steps one at a time, and stops at \(\sigma_T\) because the halt test finally holds there.

If one wants a denotational account, this relation can later be embedded in an ordered domain and studied by fixed-point methods. For engineering purposes the operational trace is already powerful. If \(I(\sigma)\) holds initially and every legal transition preserves it, then \(I\) holds along every reachable trace. That includes traces that halt late and traces that fail early.

#### The Vocabulary Behind Reachability

Several technical words are doing quiet work here, so each deserves a plain definition.

- An invariant is a property that should remain true after every legal step. Two practical examples: "external actions require permission", and "raw observations are stored before summaries are trusted."
- A reachable state is any \(\sigma_T\) that can be produced from the initial state \(\sigma_0\) by zero or more legal transitions. Unreachable states may be imaginable, but the interpreter can never actually enter them.
- Denotational semantics gives meanings by mapping programs or transition systems into mathematical objects, often functions.
- An ordered domain is a collection of meanings arranged by an information order, where one approximation can be less precise than another.
- A fixed point is a value \(x\) with \(F(x)=x\). In semantics it often describes the stable meaning obtained when repeatedly applying a behavior equation no longer changes what we know.

Freshmen need not worship these terms, but they should recognize the ceremony. Local transition rules generate traces, traces define reachability, and reachability is where invariants either live or perish.

### Four Kinds of Steps

The labels separate internal computation from external consequence. Each label carries a different contract:

- `think` may update candidate hypotheses, plan fragments, or uncertainty estimates. It must not mutate the outside world.
- `act` is the only transition that invokes an external tool or changes an external system.
- `observe` incorporates tool results, user replies, or environment measurements into belief while preserving raw evidence for audit.
- `reflect` revises policies, summaries, or future search heuristics, without pretending that a failed action succeeded.

#### A Semantic Skeleton in Pseudocode

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

### Utility and Control Inside the Loop

The transition system needs a selection principle. Something must say which legal move to take.

#### Choosing the Next Step by Expected Consequence

Expected-utility theory supplies the local one:
\[
a_t^\star=\arg\max_{a\in\mathcal{A}} \mathbb{E}[U(a,S_t)\mid h_t],
\]
so deliberation is justified only when it improves expected consequences enough to pay for itself [[33](#ref-33)] [[34](#ref-34)]. Read the formula as "pick the action \(a\) from the action set \(\mathcal{A}\) whose average usefulness, given the history so far, is highest".

A tiny example makes the accounting concrete. Suppose acting now succeeds with probability \(0.6\) for a payoff of \(10\), so its expected value is \(6\). Suppose one extra retrieval step raises the success chance to \(0.8\), giving \(8\), but costs \(1\). The extra thinking is worth it: \(8-1=7\) beats \(6\). Raise the retrieval cost to \(3\) and it is not.

Over longer horizons, the same idea lifts to Bellman recursion on interpreter state:
\[
V^\star(\sigma)=\max_a\left\{r(\sigma,a)+\gamma\sum_{\sigma'}P(\sigma'\mid \sigma,a)V^\star(\sigma')\right\},
\]
which makes the next-step policy accountable for the options it creates or destroys later [[5](#ref-5)] [[4](#ref-4)]. Read \(V^\star(\sigma)\) as "the best long-run value obtainable from state sigma", \(r(\sigma,a)\) as the immediate reward, \(\gamma\) as the discount that shrinks future value, and \(P(\sigma'\mid\sigma,a)\) as the chance of landing in \(\sigma'\). With \(r=1\), \(\gamma=0.9\), and a single successor worth \(10\), the value is \(1+0.9\times 10=10\).

#### Regulating Deliberation with a Budget Law

Control enters because reasoning consumes scarce resources and operates under disturbance. A simple budget-feedback law can regulate deliberation intensity:
\[
\kappa_{t+1}=\kappa_t-\text{cost}(a_t)+\rho\big(\kappa_{\text{target}}-\kappa_t\big),
\]
and, in linearized settings, action can be represented as \(u_t=-K\hat x_t\) over estimated state \(\hat x_t\). Read that second expression as "the control input \(u\) at time \(t\) is a gain matrix \(K\) applied, with a minus sign, to the current estimate of the state".

The point is not that every language agent is a linear controller. The point is that loop quality is a closed-loop property. The system must measure, correct, and continue under model error [[36](#ref-36)] [[41](#ref-41)].

#### Reading the Budget Equation Slowly

The budget equation deserves a plain reading, one step at a time.

1. Start with current budget \(\kappa_t\).
2. Subtract the cost of the chosen step.
3. Then add the feedback term \(\rho(\kappa_{\text{target}}-\kappa_t)\).

If \(\kappa_t\) is below the target and \(\rho>0\), this term is positive; if it is above the target, the term is negative. Try numbers: with \(\kappa_t=40\), a step cost of \(6\), a target of \(50\), and \(\rho=0.5\), the feedback term is \(0.5\times(50-40)=5\), so \(\kappa_{t+1}=40-6+5=39\).

Thus the law intentionally replenishes or tightens the budget as a control signal, not as a magical refund for tokens already spent. A production system might implement that replenishment as "allow a little more cheap reflection because the loop is under its deliberation target". Or it might clamp the term at zero when budgets are hard safety limits.

The equation models a regulator; the engineering policy decides what \(\kappa\) really is. It may be a soft deliberation allowance, a hard money limit, or two ledgers kept separately so the empire does not pay twice for one thought.

### From Semantics to Debugging

Once the loop is a small language, debugging becomes local. Instead of rereading the transcript for mood, you ask four pointed questions:

- Did the planner choose a legal transition?
- Did the guard fail to block an illegal action?
- Did observation parsing corrupt belief?
- Did a preserved invariant turn out to be the wrong invariant?

Abstract interpretation gives a way to over-approximate reachable states through
\[
F^\sharp=\alpha\circ F\circ\gamma,
\]
so some guarantees can be checked without enumerating every concrete trace [[43](#ref-43)]. Modern reason-act agents make this especially useful, because their traces expose interleaved reasoning, action, and observation steps in a form that can be instrumented [[11](#ref-11)].

#### Abstract Interpretation with a Two-State Budget

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

#### Designing the Loop State as a Typed Object

The practical lesson is to design the loop state as a typed object, with named fields rather than a bag of text. A workable set of fields is:

- current task;
- belief summary;
- memory handles;
- tool permissions;
- budget ledger;
- pending commitments;
- halt criteria.

Each transition should have a name and a contract. The prompt is then one component inside a semantics, not the sovereign description of the whole system.

### Exercise

Take an agent loop you have built or used. The goal is to state its invariants precisely enough to test them.

1. Write three invariants that should hold after every transition. At least one should concern budget, one should concern permissions, and one should concern evidence preservation.
2. For each invariant, identify the transition label most likely to violate it: `think`, `act`, `observe`, or `reflect`.
3. For each invariant, name the observation you would need in the trace to diagnose the violation.

A good answer is checkable. "The loop is careful with money" is not an invariant; "no `act` step runs when the budget ledger reads zero or less, and every `act` step appends its cost to the ledger" is, because a reader can point at the trace entry that proves or breaks it.


## Deliberation, Planning, and Search

Imagine an agent that has just received a bug report. It can act at once, or it can first imagine two or three futures. This section is about that second option. Deliberation means spending part of the budget simulating steps before committing to one. Planning and search buy that foresight without pretending computation is free.

The interpreter from the previous topic, Reasoning Loops as Interpreters, executes one legal step at a time. Deliberation asks a sharper question: should the agent look ahead before choosing that step?

### A Proposal Says "Try This"; A Plan Says "And Then What"

A proposal says, "try this next action." A plan embeds the same action inside an imagined trajectory, and states five further things:

- what state should follow the action;
- what evidence should appear if the plan is on track;
- what cost will be paid;
- what constraint might bind, that is, which limit could stop the plan;
- what fallback remains if the world disagrees.

Search is the procedure that compares such trajectories under limited time, a comparison shop for imagined futures, closing when the clock stops.

### Plans as Paths Through Interpreter States

Draw the choices as a graph. Let \(G=(V,E)\) be a search graph whose vertices are decision states. Read \(V\) as the states the agent could occupy, and \(E\) as the legal moves between them.

A deterministic plan is then a path \(p=(v_0,\dots,v_T)\) through that graph, from the current state \(v_0\) to \(v_T\) after \(T\) steps. The planner wants the cheapest such path, minimizing

\[
J(p)=\sum_{t=0}^{T-1} c(v_t,v_{t+1}) + \Phi(v_T).
\]

Read \(J(p)\) as "total cost of plan \(p\)". The sum prices every move, since \(c(v_t,v_{t+1})\) is one step's cost in tokens, time, or money. The term \(\Phi(v_T)\) is a terminal penalty on where the plan leaves the agent: low for a good ending, high for a bad one.

#### How A\* Ranks Candidate Nodes

A\* ("A star") is a classic search algorithm choosing which node to examine next. It prioritizes candidate nodes by

\[
f(n)=g(n)+h(n),
\]

where admissibility \(h(n)\le h^\star(n)\) gives shortest-path guarantees when the graph assumptions hold [[8](#ref-8)]. In the agent interpreter, \(g\) accounts for already-spent cost and \(h\) estimates the remaining cost to reach an acceptable halt state.

The three letters are intentionally humble.

1. \(g(n)\) is the cost already paid to reach node \(n\): history, and not negotiable.
2. \(h(n)\) is a heuristic estimate, a cheap guess replacing expensive calculation, of the cost still required from \(n\) to a goal.
3. \(f(n)\) is their sum, the planner's current guess at total path cost through \(n\).

A heuristic is admissible when it never overestimates the true remaining cost \(h^\star(n)\), read "h-star of n": the real cheapest cost from \(n\) to a goal. An admissible heuristic may be naive, but it must not be boastful. To check yours, take nodes whose true cost you know and confirm the estimate is never larger.

#### A Two-Branch Example with Numbers You Can Check

For a tiny graph, suppose \(v_0\) is "bug report received." From it the agent can inspect logs and reach \(A\), or inspect the recent diff and reach \(B\).

The path to \(A\) has already cost \(g(A)=2\), and the heuristic says \(h(A)=5\), so \(f(A)=7\). The path to \(B\) has already cost \(g(B)=4\), and the heuristic says \(h(B)=1\), so \(f(B)=5\).

A\* expands \(B\) first, not because inspecting diffs is morally superior, but because the combined arithmetic says that route currently looks cheaper; \(B\) started out more expensive, and the estimate of what remains tipped it.

The branching factor is the number of successor choices the search faces at each node. Reducing it from ten plausible actions to three well-typed actions can turn a hopeless thicket into a walkable garden path.

### Preconditions and Effects: Planning as Set Editing

Symbolic planning makes the transition model explicit. "Symbolic" here means the state is a set of named facts, not an opaque blob of text. An action is legal only when its preconditions are present, and its effects transform the state:

\[
s_{t+1}=(s_t\mathbin{\backslash}\mathrm{Del}(a_t))\cup \mathrm{Add}(a_t),\qquad \mathrm{Pre}(a_t)\subseteq s_t.
\]

Read the first equation as "next state = current state, minus deleted facts, plus added ones." Read \(\mathrm{Pre}(a_t)\subseteq s_t\) as "the action's preconditions must all be facts of the current state."

This is not limited to toy blocks-world domains, the tabletop puzzles of planning textbooks. A coding agent's `run_tests` action may require a clean dependency environment; a `deploy` action may require passing tests, approval, and rollback instructions. Preconditions prevent the planner from treating hope as an executable dependency [[9](#ref-9)] [[10](#ref-10)].

Decode the notation as set editing.

- \(\mathrm{Pre}(a)\) is the set of facts that must already be true before action \(a\) may run.
- \(\mathrm{Add}(a)\) is the set of facts made true afterward.
- \(\mathrm{Del}(a)\) is the set of facts removed afterward.

For `run_tests`, one toy model might be

\[
\mathrm{Pre}(\texttt{run\_tests})=\{\texttt{deps\_installed},\texttt{worktree\_readable}\},
\]

\[
\mathrm{Add}(\texttt{run\_tests})=\{\texttt{test\_result\_known}\},\qquad
\mathrm{Del}(\texttt{run\_tests})=\{\texttt{test\_result\_stale}\}.
\]

If the current state contains installed dependencies and a readable worktree, the action is legal. Afterward, the planner may rely on a fresh test result and must stop trusting the stale one. The notation is austere because the promise is austere: no premise, no action.

### Choosing When the Future Is Uncertain

Something must then choose among candidates. Expected utility supplies the rule:

\[
a_t^\star=\arg\max_a \mathbb{E}[U(a,S_t)\mid h_t],
\]

read as "choose the action \(a\) with the largest average usefulness \(U\), given the state \(S_t\) and the history \(h_t\) seen so far." A direct consequence follows: additional planning depth is justified only when its expected improvement exceeds its compute and latency costs [[33](#ref-33)] [[34](#ref-34)]. If another level of lookahead costs two seconds but improves the decision by half a second of value, it is a loss.

In stochastic settings, where the same action can lead to different outcomes, this becomes Bellman recursion,

\[
V^\star(s)=\max_a\left\{R(s,a)+\gamma\sum_{s'}P(s'|s,a)V^\star(s')\right\},
\]

read as "the best achievable value of \(s\) is the best over actions of immediate reward \(R(s,a)\) plus the discounted average value of wherever you land next." Here \(\gamma\) (gamma) is a discount factor between 0 and 1 that shrinks distant outcomes, and \(P(s'|s,a)\) is the chance of landing in \(s'\). The same recursion becomes a belief-space recursion when the state is only partially observed, meaning the agent sees clues rather than the state itself [[5](#ref-5)] [[4](#ref-4)] [[7](#ref-7)].

#### Spending Simulations Wisely with Monte Carlo Tree Search

When the branching factor is large, the planner needs search control: a rule for spending limited thinking. Monte Carlo tree search (MCTS) allocates rollouts by optimism:

\[
a^\star=\arg\max_a\left(Q(s,a)+c\sqrt{\frac{\ln N(s)}{N(s,a)}}\right),
\]

balancing exploitation of promising branches with exploration of uncertain ones under finite time [[45](#ref-45)]. The formula is a reminder that uncertainty is not merely a defect; it is sometimes a reason to inspect a branch before discarding it.

A rollout is a simulated continuation: the planner imagines acting until a terminal or cutoff state, then uses the result to improve its estimates. Two pressures are traded:

- Exploitation means spending simulations on branches whose current value estimate \(Q(s,a)\) already looks good.
- Exploration means spending some simulations on branches with few visits \(N(s,a)\), because ignorance may be hiding either treasure or calamity.

The square-root term is that exploration bonus, and \(c\) sets how loudly curiosity may speak. It shrinks as one action is tried more often, and grows slowly as the parent state receives more total visits \(N(s)\). A branch tried once in a hundred visits gets a large bonus; after fifty, a small one.

### Replanning After Every Step: Receding Horizons

Long plans are fragile because the world answers back. Model predictive control (MPC) handles this by solving an \(H\)-step problem, where \(H\) is the horizon, the number of steps looked ahead:

\[
\mathbf{u}_{t:t+H-1}^{\star}
=\arg\min_{\mathbf{u}_{t:t+H-1}}
\sum_{k=0}^{H-1}\ell(x_{t+k},u_{t+k})+\ell_f(x_{t+H})
\]

subject to \(x_{k+1}=F(x_k,u_k)\) and \(g(x_k,u_k)\le 0\). Read \(\mathbf{u}\) as the sequence of control actions, \(x\) as the state, \(\ell\) (ell) as the cost of one step, and \(\ell_f\) as the cost of the final state. The first constraint says the state evolves by a known model \(F\); the second collects limits that must never be violated.

The controller applies \(u_t^\star\), the first component of that sequence, observes the new state, and replans at the next step. The corrected control sequence is important: the optimizer reasons over a sequence, while the agent executes only the first action before feedback updates the problem [[41](#ref-41)].

For a language-agent planner, the pattern becomes the procedure below: search for candidates, pick the best, check that the first action is legal, execute only that action, and return to the loop.

```text
function RECEDING_HORIZON_STEP(sigma, horizon, budget):
    candidates <- search(sigma, horizon, budget)
    plan <- argmax_expected_utility(candidates)
    a0 <- first_action(plan)

    if not legal(a0, sigma):
        return fallback_or_clarify(sigma)

    sigma_next <- execute(a0, sigma)
    return observe_and_replan(sigma_next)
```

If that first action is illegal in state `sigma`, the agent falls back or asks for clarification.

The plan is a hypothesis about controllable futures, not a contract that reality has signed. This is why "plan then execute" is weak when the execution environment changes, and why "plan, execute one step, observe, replan" is the natural extension of the interpreter built in Chapter 1.

### When Decomposition Actually Improves the Search

Task decomposition means breaking a task into smaller subtasks. It is useful only when it improves the search problem, in one of four ways:

- it may reduce branching factor;
- it may expose prerequisites;
- it may create verifiable intermediate states;
- it may isolate irreversible actions behind stronger checks.

It is not useful merely because it produces a tidy list.

This is the first practical rule of planning: task structure predicts whether planning earns its keep. Planning tends to help in five situations:

1. the horizon is long enough that early choices create or destroy later options;
2. the branching factor is wide enough that unguided next-action choice wastes effort;
3. prerequisites impose a real order;
4. uncertainty must be reduced before commitment;
5. an irreversible action deserves ceremony before the lever is pulled.

A database migration, a multi-file refactor, and a research synthesis with conflicting sources all have enough internal geometry to reward decomposition. A one-line formatting fix usually does not. There, the planning ritual may cost more than the task.

### Reflection Repairs Hard Plans and Taxes Easy Ones

The same lesson governs composition, meaning how planning combines with other patterns. Reflection can repair a difficult plan: after a failed test, the agent can inspect the trace, notice that a prerequisite was imaginary, and revise the frontier before doing more damage. The frontier is the set of nodes the search is still willing to expand.

But reflection also adds latency, consumes tokens, and can induce overthinking on easy tasks. An agent asked to rename a local variable may spend three reflective turns debating architectural intent while the correct edit waits patiently in the file.

Patterns interact; they are not virtues in isolation. Planning plus reflection is powerful when the task contains hidden dependencies or costly mistakes, and ornamental when the task is short, reversible, and already well specified.

### What a Planning Loop Should Record

In practice, each candidate trajectory should record six fields: state estimate, proposed action, expected observation, cost, risk, and contingency, which together make it auditable.

Three commitments follow.

- Heuristics should prioritize branches, but pruning decisions should be logged when they affect safety or correctness.
- Irreversible or expensive actions should be protected by symbolic preconditions, using the \(\mathrm{Pre}\) sets described earlier.
- Replan triggers should be explicit: new evidence, failed precondition, budget drift, tool error, or a value estimate that changes enough to reorder the frontier.

Chapter 1, Topic 3 (World Models and State Abstractions) develops how that state estimate is built.

### Exercise

Choose a multi-step task: a database migration, a code refactor, or a research synthesis. The goal is a planning problem concrete enough to critique. Work in four steps:

1. Write three candidate plan states, each a short description of what is true in it.
2. Write one heuristic \(h\) for ranking them, and say what it estimates.
3. Name one observation that would force replanning.
4. Name one action that should require symbolic preconditions before execution, and list those preconditions.

A good answer has a heuristic that is cheap to compute and never boastful about how little work remains, a replanning trigger tied to concrete evidence rather than vague discomfort, and preconditions a program could check.


## Memory Systems, Context, and Retrieval

Keep it, throw it away, or go looking for it: an agent faces those three choices constantly, and they are as much a part of the machine as the model itself. We will treat memory as a set of decisions with costs, not as a storage bin. By the end you should be able to say why a particular fact is in the prompt right now, and what it displaced.

Deliberation, Planning, and Search extends the interpreter forward into imagined time. Memory extends it backward. It decides which parts of the past should stay available to future steps. The context window is not the agent's memory. It is the small working surface onto which memory is projected, the way a slide is projected onto a wall.

### Memory Is a Policy, Not a Filing Cabinet

A memory system is a control policy. A *policy* is a rule for choosing what to do next. This particular policy chooses among four things: retain, compress, retrieve, and forget.

A weak policy treats all past text as equally eligible for attention. Everything that happened is still lying around, so everything competes for the model's limited notice. A stronger policy asks three sharper questions:

- Which stored distinctions can actually change the next action?
- Which evidence must remain auditable, meaning a human can later trace a claim to its source?
- Which stale traces should be kept out of the active state entirely?

### Memory as Controlled State

Let the memory state be \(m_t=(w_t,e_t,s_t)\). Read that as "at step \(t\), memory consists of three stores": working, episodic, and semantic.

- Working memory \(w_t\) holds the current control state: the plan, the constraints, the last observation.
- Episodic memory \(e_t\) preserves concrete events and traces: what was run, what was returned.
- Semantic memory \(s_t\) stores distilled facts, patterns, and policies: what has generally been true.

A memory controller chooses operations
\[
u_t \in \{\texttt{write},\texttt{compress},\texttt{retrieve},\texttt{evict}\}
\]
which reads "the control action at step \(t\) is one of write, compress, retrieve, or evict". Eviction is removal from the active context. The controller picks it by
\[
u_t = \mu_\theta(m_t,h_t),
\]
read as "the controller \(\mu\), with parameters \(\theta\), chooses \(u_t\) by looking at memory state \(m_t\) and history \(h_t\)". Its aim is
\[
\max_\mu\ \mathbb{E}\!\left[\sum_t \gamma^t \big(\text{task\_utility}_t - \lambda_1\text{latency}_t - \lambda_2\text{token\_load}_t\big)\right].
\]
Read that as "choose the controller that maximizes expected discounted task usefulness, minus a price for delay and a price for tokens consumed". Here \(\mathbb{E}\) means average over runs, \(\gamma\) is a discount factor between 0 and 1 that makes later payoffs count slightly less, and \(\lambda_1,\lambda_2\) are the prices you set on latency and token load.

This is expected utility under systems constraints: retrieval is useful only when it improves decisions more than it costs [[33](#ref-33)] [[34](#ref-34)]. A builder sets \(\lambda_1\) and \(\lambda_2\) by measurement, not by taste. If one extra retrieval adds 400 milliseconds and 1,200 tokens but lifts task success from 71% to 79%, it earns its keep. If it lifts success from 71% to 71.4%, it does not.

#### Why Today's Write Is Tomorrow's Asset

The Bellman view makes the tradeoff across time explicit:
\[
V^\star(m,h)=\max_{u}\left\{r(m,h,u)+\gamma\,\mathbb{E}[V^\star(m',h')]\right\},
\]
read as "the best achievable long-run value of being in memory state \(m\) with history \(h\) equals the best immediate reward \(r\) plus the discounted average value of wherever you land next, written \(m'\) and \(h'\)". The reward \(r\) already includes latency and token penalties [[5](#ref-5)] [[4](#ref-4)].

Two consequences follow. A write may be costly now but valuable later, because it preserves the one line of output the repair will need. An eviction may save context now but create future regret, because the discarded item turns out to be the missing constraint.

### Retrieval Is an Action

Retrieval is not a lookup that happens off to the side. It is an action the agent takes, with a price and a risk.

#### Sparse Retrieval Counts Words

Sparse retrieval begins with counted words. The query is \(q\), the candidate document is \(d\), and a term \(t\) is one word-like unit from the query. The term frequency \(f(t,d)\) counts how often term \(t\) appears in document \(d\). The document length \(|d|\) counts the document's tokens or terms, and \(\mathrm{avgdl}\) is the average document length in the collection.

\(\mathrm{IDF}(t)\), inverse document frequency, is large for rare terms and small for common terms. It says that `segmentation fault` is usually more diagnostic than `the`. The constants \(k_1\) and \(b\) are tunable knobs. \(k_1\) controls how quickly repeated occurrences stop adding much evidence, while \(b\) controls how strongly scores are normalized for document length.

With those pieces named, BM25 scoring is
\[
\mathrm{BM25}(q,d)=\sum_{t\in q}\mathrm{IDF}(t)\frac{f(t,d)(k_1+1)}{f(t,d)+k_1\left(1-b+b|d|/\mathrm{avgdl}\right)},
\]
read as "add up, over every term in the query, that term's rarity weight times a saturating count of how often it occurs in this document". Saturation is the point worth feeling: with \(k_1=1.2\), a term appearing once already earns about half the weight it can ever reach, and the tenth occurrence adds very little.

#### Dense Retrieval Compares Directions

Dense retrieval begins from a different little machine. An embedding is a vector representation of text, such as \(e_q\) for a query and \(e_d\) for a document, chosen so that related meanings tend to live near one another in vector space.

The inner product \(\langle e_q,e_d\rangle\) multiplies corresponding coordinates and sums the products. When the vectors are normalized, a larger inner product means a smaller angle between them, which often corresponds to greater semantic similarity. Dense retrieval often uses that inner-product similarity:
\[
s(q,d)=\langle e_q,e_d\rangle.
\]
A two-coordinate example makes it concrete. If \(e_q=(0.6,0.8)\) and \(e_d=(0.8,0.6)\), the inner product is \(0.6\times0.8+0.8\times0.6=0.96\); both vectors have length 1, so a score of 0.96 out of a possible 1.00 means the directions nearly agree.

#### Sparse and Dense Fail Differently

These are complementary indexing geometries with different failure modes, not rival creeds [[46](#ref-46)] [[15](#ref-15)] [[47](#ref-47)]. Sparse methods preserve lexical anchors and citations well. Dense methods can recover paraphrases and semantic neighbors. Hybrid systems, which run both and merge the rankings, earn their complexity when those differences reduce downstream error.

The power of dense retrieval is paraphrase. The danger is a smooth confidence that can drift away from exact filenames, citation anchors, and error strings.

#### Retrieved Evidence Enters the Generator's Arithmetic

For retrieval-augmented generation, usually abbreviated RAG, evidence quality propagates into output probability:
\[
p(y\mid x)\approx \sum_{d\in\mathcal{D}_k} p_\eta(d\mid x)\,p_\theta(y\mid x,d),
\]
so poor retrieval is injected into generation dynamics rather than appended as a harmless side note [[14](#ref-14)]. The useful evaluation question is not "did the retriever find similar text?" but "did the retrieved evidence move the action ranking in the right direction?"

In this equation, \(\mathcal{D}_k\) is the top-\(k\) evidence set returned by
the retriever. The subscript \(k\) means the system keeps only a bounded number
of documents, because context, latency, and attention are finite. The term
\(p_\eta(d\mid x)\) is the retriever's probability or normalized score for
document \(d\) given query context \(x\); \(\eta\) names the retriever's
parameters. The term \(p_\theta(y\mid x,d)\) is the generator's probability of
answer \(y\) after seeing \(x\) and document \(d\); \(\theta\) names the
generator's parameters. The approximation sign acknowledges that production
systems usually approximate the full document sum with a short ranked list.

### Compression and Forgetting

Compression policy is an information-theoretic trade:
\[
R(D)=\min_{p(\hat x|x):\mathbb{E}[d(X,\hat X)]\le D} I(X;\hat X),
\]
which says to spend bitrate only on distinctions that matter under an accepted distortion level [[35](#ref-35)]. In agent memory, the distortion measure should be task-relative. A summary that drops exact command output may be acceptable for narrative progress tracking and unacceptable for debugging a build failure.

#### Reading the Rate-Distortion Equation

Read \(X\) as the original trace or memory item and \(\hat X\) as its compressed
version. The conditional distribution \(p(\hat x\mid x)\) describes the
compressor: given original item \(x\), it may produce summary \(\hat x\). The
distortion \(d(X,\hat X)\) measures what the summary loses for the task at hand,
and the constraint \(\mathbb{E}[d(X,\hat X)]\le D\) says the average loss must
stay below tolerance \(D\). The mutual information \(I(X;\hat X)\) measures how
much information about the original survives in the summary. Thus \(R(D)\) is
the smallest amount of retained information needed to keep distortion at or
below \(D\). The equation is permission to forget only after specifying what
kind of forgetting the task can survive.

#### A Build Failure That Two Summaries Handle Differently

For example, suppose an agent runs `python3 scripts/build_latex_pdf.py` and the command fails with one exact line: `Undefined control sequence \mathbbm at topic-03 line 87`. A progress summary that says "PDF build failed in topic 3" may have low distortion for a project manager asking whether the publication artifact exists. It has ruinous distortion for the debugging policy, because the repair depends on the exact command, the exact TeX complaint, and the exact location. Rate-distortion thinking therefore does not say "summarize aggressively." It says: choose what may be lost only after naming the task that will suffer the loss.

#### Forgetting Deserves the Same Care as Remembering

Forgetting is equally active. Four kinds of debris can all distort the current state:

- stale retrieved snippets that describe an older version of the world;
- contaminated memories that recorded something false;
- duplicated summaries that make one weak claim look like several;
- obsolete user preferences the user has since changed.

Cognitive multi-store theory is useful here because it separates short-lived working contents from longer-lived episodic and semantic stores [[48](#ref-48)]. The engineering analogue is to attach provenance, timestamp, scope, and confidence to stored items. With those four tags present, the controller can decide whether a memory belongs in the present decision.

The following pseudocode shows one pass of the memory controller. It writes auditable observations, compresses only under context pressure while keeping links back to raw evidence, retrieves only when uncertainty is actually blocking action, and evicts what has gone stale.

```text
function MEMORY_STEP(sigma, uncertainty, phase):
    if new_observation_is_auditable(sigma):
        write(episodic, raw_observation, provenance)

    if context_pressure_high(sigma):
        compress(trace, preserve_links_to_raw_evidence)

    if uncertainty_blocks_action(uncertainty):
        docs <- retrieve(query_from_state(sigma), filters=scope_and_time)
        sigma <- add_to_working_memory(rerank(docs))

    evict_items(active_context, stale_or_low_value)
    return sigma
```

This sketch turns memory into part of the interpreter rather than an ungoverned transcript cache.

### Measuring Memory Policy

Memory should be evaluated at the decision boundary, meaning the moment where the agent commits to an action. Three examples show what "the right memory" means in practice:

- For a legal research agent, the right case is the one that changes the answer safely.
- For a code agent, the right file is the one that localizes the bug or rules out a tempting false edit.
- For a personal assistant, the right memory is current, permissioned, and relevant to the user's actual intent.

#### Ablation Under a Fixed Budget

The clean comparison is an ablation under a fixed budget. An *ablation* removes one component and re-measures. Run the same task distribution three ways: with no memory beyond the prompt, then with working state only, then with retrieval-backed memory. Hold the model, tool permissions, token ceiling, and time limit steady.

Now the question becomes concrete: did memory improve task success or task-specific partial progress, or did it merely spend tokens remembering its own autobiography? Each arm can win. Working state may help on short tasks by preserving the current plan and constraints. Retrieval-backed memory may help when the relevant evidence lies outside the current window. No memory may win when stale or distracting evidence is more dangerous than forgetfulness.

#### Metrics, Stress Tests, and One Self-Citing Failure

Useful measurements include retrieval precision@\(k\), latency, grounded answer faithfulness, and regret from eviction decisions under fixed token budgets. Precision@\(k\) is the fraction of the top \(k\) results that are genuinely relevant; 3 relevant hits out of 5 returned is 0.6. Regret here is the drop in outcome caused by having thrown something away.

Stress tests should include adversarial distractors and contamination injections, because long context can amplify bad evidence as easily as good evidence [[16](#ref-16)].

One nasty composition failure is especially common. Reflection writes an inaccurate summary. Retrieval later ranks that summary highly, because it matches the task language. The agent then repeatedly promotes the false memory back into working state. The system appears consistent because it keeps citing itself. Evaluating and Debugging Reasoners counts this as a contaminated-memory failure when it labels failures by transition.

The practical target is a memory economy: spend context where it changes decisions, preserve raw evidence where audits require it, and keep yesterday's convenient summary from overruling today's observation.

### Exercise

For one agent workflow, list five things it might remember. Assign each to working, episodic, or semantic memory. Then choose one item that should be compressed, one that should be retrieved only under a specific trigger, and one that should expire.

Work it in that order. Pick a workflow you know well, such as fixing a failing test or answering support tickets. A good answer names the trigger explicitly, for example "retrieve the deployment runbook only when a command touches production", and gives the expiry a reason, for example "the user's stated deadline expires when the deadline passes". A weak answer marks everything semantic and lets nothing expire.


## Evaluating and Debugging Reasoners

Suppose an agent is asked to fix a failing test, and it succeeds. Now suppose it succeeded by reading a private file it was never permitted to open, spending four times its token budget, and skipping the required regression run. The final answer is still correct. The reasoner is still broken. This section is about building an evaluation that can tell those two agents apart.

This chapter opened with an interpreter for reasoning. It then added planning as controlled lookahead, and treated memory as governed access to the past. Evaluation closes the loop. The central move is to judge a reasoner as a *stochastic trajectory generator* — a machine that produces whole run-paths with randomness in them — rather than as a vending machine for final answers.

### Why Final-Answer Accuracy Is Not Enough

Final-answer accuracy is necessary. It is also too thin. An agent can reach the right answer while doing at least four things we would never sanction:

- using forbidden evidence;
- overspending its budget;
- skipping a required check;
- taking an unsafe irreversible action that simply happened not to fail this time.

An action that cannot be undone and only *happened* not to explode is not a success. It is a coin flip wearing a medal.

So evaluation must score paths as well as destinations. The quantities worth scoring are the ones the interpreter actually touches: observations, internal steps, retrievals, tool calls, costs, confidence, constraints, and outcomes.

### The Evaluation Object

Let trajectory \(\tau=(\sigma_0,a_0,\dots,\sigma_T)\sim p_\pi(\tau)\). Read that as: "tau is the sequence of state, action, state, action, up to the final state at step T, drawn from the distribution over trajectories that policy pi induces." Each \(\sigma_t\) is the reasoner's state at step \(t\); each \(a_t\) is the action it took there.

Three scores are then attached to that one trajectory. Define task utility \(U(\tau)\), safety cost \(C(\tau)\), and calibration score \(S(\tau)\). A run, a distribution over runs, and three separate scores make for crowded notation, so here is the reading key:

| Symbol | Read aloud as | Meaning |
|---|---|---|
| \(\tau\) | "tau" | One complete run: states and actions from start to halt |
| \(p_\pi(\tau)\) | "p sub pi of tau" | The chance that policy \(\pi\) produces this particular run |
| \(U(\tau)\) | "U of tau" | How much task value the run earned |
| \(C(\tau)\) | "C of tau" | How much safety cost the run incurred |
| \(S(\tau)\) | "S of tau" | How badly the run's stated confidence matched reality |
| \(\lambda\) | "lambda" | The exchange rate: how much utility one unit of safety cost is worth |
| \(\epsilon\) | "epsilon" | The largest calibration error we are willing to tolerate |

Evaluation is therefore multi-objective:
\[
\max_\pi \ \mathbb{E}[U(\tau)] - \lambda\,\mathbb{E}[C(\tau)] \quad\text{with calibration constrained by}\quad \mathbb{E}[S(\tau)] \le \epsilon.
\]
Read the first part as "choose the policy that maximizes expected task utility minus lambda times expected safety cost", and the second as "subject to expected calibration error staying at or below epsilon". This keeps expected utility as the compass while preventing "high reward by unsafe luck" from masquerading as competence [[33](#ref-33)] [[34](#ref-34)] [[53](#ref-53)].

#### Getting the Sign of the Calibration Term Right

Here \(S(\tau)\) should be read as a calibration loss or calibration error: lower is better, which is why the constraint uses \(\le \epsilon\). If one instead used a calibration reward, the inequality would need to face the other way. The notation matters because evaluation is an accounting system; an upside-down sign can crown a liar for sounding confident.

One quick check: a policy that always claims 99 percent confidence while being right half the time must fail this constraint, not pass it.

### What the Harness Should Log and Report

The harness should log each transition with state summary, action, tool arguments, retrieved evidence, confidence, budget cost, constraint checks, and outcome. Without that log, every later debugging step is guesswork.

The resulting report should name ordinary engineering quantities, not only a philosophical score:

- task success;
- task-specific partial progress;
- tokens consumed;
- wall-clock latency;
- tool-call count;
- valid-call rate;
- utility per call.

Task-specific partial progress matters because a reasoner that localizes the failing file but misses the final patch is different from one that wanders heroically through irrelevant directories. Both score zero on final success; only one is close.

Utility per call matters because two agents with equal success may differ by a factor of ten in tool noise. Suppose both solve 40 tasks. One used 200 calls, the other 2000. That is 0.20 utility per call against 0.02. One is an engineer, the other is a very expensive weather system.

### Ablations: Learning Which Pattern Caused Which Effect

To learn which pattern caused which effect, compare machines under controlled ablations. An *ablation* removes or adds exactly one component and holds everything else fixed.

Start with a base interpreter. Then add planning, memory, retrieval, or reflection one at a time, while holding the task set, model, budget, tools, and stopping rule as steady as possible.

For combined patterns, use factorial comparisons in plain clothes. That means four runs:

1. planning alone;
2. reflection alone;
3. both together;
4. neither.

If the combined system beats both single additions, the patterns may be cooperating. If it loses by burning latency or amplifying a bad memory, their composition is suspect.

Repeat this across task families. Avoid a verdict as crude as "planning is good" or "reflection is bad". The useful finding sounds like this: planning helped on long-horizon, high-branching tasks with prerequisites; reflection helped after uncertain failures and hurt on easy reversible tasks.

#### Three Layers of Tests

Unit tests can verify local contracts such as schema validity and permission behavior. Scenario tests can verify whole traces under controlled perturbations. Regression suites should include previous failures, adversarial distractors, stale memories, flaky tools, and ambiguous user requests.

### Calibration and Probabilistic Honesty

A model's stated confidence is only useful if it can be checked. Strictly proper scoring rules make confidence testable. A scoring rule is **strictly proper** when the best way to minimize expected loss is to report one's true probability belief. It rewards honesty about uncertainty rather than theatrical certainty.

Two canonical choices are log score
\[
\mathcal{L}_{\log}=-\frac{1}{N}\sum_{i=1}^N \log p_\theta(y_i\mid x_i),
\]
and Brier score
\[
BS=\frac{1}{N}\sum_{i=1}^N (p_i-y_i)^2.
\]
For bucketed predictions \(B_b\), expected calibration error is
\[
\mathrm{ECE}=\sum_b \frac{|B_b|}{N}\left|\mathrm{acc}(B_b)-\mathrm{conf}(B_b)\right|.
\]
Low calibration error means the system's probabilities are interpretable commitments, not decorative numbers [[49](#ref-49)].

#### Reading the Log Score

In the log score, \(x_i\) is input example \(i\), \(y_i\) is the observed correct outcome, \(p_\theta(y_i\mid x_i)\) is the model's probability for that outcome, and \(N\) is the number of evaluated examples. The whole expression reads "the average, over N examples, of the negative log probability the model gave to the truth".

The negative sign turns high probability on the truth into low loss. If the model assigns probability \(0.8\) to the true answer, the contribution is \(-\log 0.8\); if it assigns \(0.01\), the penalty is much larger. In natural logarithms those are roughly \(0.22\) against \(4.6\), a twenty-fold difference in penalty for one confident mistake.

#### Reading Expected Calibration Error

Expected calibration error bins predictions by stated confidence. \(B_b\) is the set of examples whose confidence falls in bucket \(b\), such as all predictions between 70 and 80 percent confident. \(|B_b|/N\) weights the bucket by how many examples it contains. \(\mathrm{acc}(B_b)\) is the observed accuracy inside the bucket, and \(\mathrm{conf}(B_b)\) is the average stated confidence.

If a bucket says 80 percent and succeeds only 60 percent of the time, that bucket contributes a 20-point calibration gap. The formula averages those gaps over buckets, weighted by bucket size. To use it, a builder logs a stated confidence with every decision, sorts them into ten bins, and compares each bin's claim to its outcome rate.

#### Reading Brier Score, Including the Multiclass Form

The displayed Brier equation is the binary form: \(y_i\in\{0,1\}\), and \(p_i\) is the predicted probability that the event occurs. For a multiclass classifier with \(K\) labels, use
\[
BS_{\mathrm{multi}}=\frac{1}{N}\sum_{i=1}^N\sum_{k=1}^K (p_{ik}-\mathbf{1}\{y_i=k\})^2,
\]
where \(p_{ik}\) is the predicted probability of class \(k\) on example \(i\), and \(\mathbf{1}\{y_i=k\}\) is 1 when class \(k\) is the true label and 0 otherwise. In both forms, a lower score is better, because the score is squared distance between probability and reality. Predicting 0.9 on an event that happens costs \(0.01\); predicting 0.9 on an event that does not happen costs \(0.81\).

#### Calibration Is Not Value

Calibration is not the same as value. A model can be well-calibrated about a low-value action, and a valuable action can remain uncertain. The policy layer should keep outcome value, confidence, evidence quality, and constraint cost as separate quantities until the governed decision rule combines them.

### Causal Debugging

Debugging means finding which step caused the failure. Consider a failed coding-agent trace. The block below lists six steps in order, from the user's request to a low-confidence report, and shows the agent following a stale memory instead of the current error message:

```text
sigma0: user asks for a failing test repair
retrieve: returns an old note saying "parser errors come from topic-02"
think: concludes topic-02 owns the failure
act: edits topic-02 without reading current traceback
observe: tests still fail; traceback names topic-04
halt: reports an attempted fix with low confidence
```

#### Controlled Interventions on a Replayed Trace

A controlled intervention changes one suspected cause while preserving the rest of the trace as much as possible. For instance, rerun the same replay but replace the retrieved old note with the current traceback, leaving the prompt, budget, available tools, and task unchanged. If the patched replay now reads topic-04 first and fixes the failure, retrieval choice becomes a plausible cause rather than a decorative postmortem villain.

When a failure appears, replay traces with interventions and estimate effects:
\[
\mathrm{ATE}=\mathbb{E}[Y\mid do(Z{=}1)]-\mathbb{E}[Y\mid do(Z{=}0)].
\]
ATE stands for average treatment effect. Read the formula as "the expected outcome Y when we force the suspected cause Z on, minus the expected outcome when we force it off". The \(do(\cdot)\) notation means we *set* the value rather than merely observe it.

This quantity is identified only under randomized interventions or explicit causal assumptions: the replay harness must be able to set \(Z\) while holding the relevant context fixed, or the estimate is only a suggestive contrast. Used carefully, interventional replay can test whether a step class such as retrieval choice, tool arguments, or reflection policy causes downstream harm [[6](#ref-6)].

#### Influence Approximations for Triage

For fine-grained attribution, influence approximations estimate how much one datum or memory item perturbs a test loss:
\[
I_{up,loss}(z,z_{\text{test}})\approx -\nabla_\theta L(z_{\text{test}},\hat\theta)^\top H_{\hat\theta}^{-1}\nabla_\theta L(z,\hat\theta),
\]
which helps prioritize highest-leverage repairs [[50](#ref-50)]. Influence is not a replacement for causal identification, but it is useful for triage when a large corpus, memory store, or training set may contain the source of a recurring error.

A gradient \(\nabla_\theta L\) is the vector of first derivatives of loss with respect to parameters \(\theta\); it points in the direction that most quickly increases the loss locally. A Hessian \(H_{\hat\theta}\) is the matrix of second derivatives at the fitted parameters \(\hat\theta\); it describes local curvature, or how the gradient itself changes as parameters move. The inverse Hessian \(H_{\hat\theta}^{-1}\) approximately converts a small gradient disturbance into the parameter movement that would have produced it.

The approximation rests on four assumptions:

1. the loss is smooth;
2. the fitted point is locally well behaved;
3. the Hessian is invertible or suitably damped;
4. the effect of upweighting one item is small enough that a local Taylor expansion is honest.

When those assumptions fail, influence scores are still clues, but clues wearing ceremonial robes are not proofs.

#### A Debugging Loop, Written Out

The pseudocode below confirms the failure on a baseline replay, then replays once per candidate cause with that cause intervened upon, and ranks causes by how much each changed the outcome:

```text
function DEBUG_FAILURE(trace, failure_predicate):
    baseline <- replay(trace)
    assert failure_predicate(baseline)

    for z in candidate_causes(trace):
        patched <- intervene(trace, z)
        outcome <- replay(patched)
        record_effect(z, failure_predicate(outcome))

    return ranked_causes_by_effect()
```

The important constraint is that `intervene` must change the candidate cause while preserving enough of the surrounding context for the comparison to mean anything.

### From Scores to Repairs

Evaluation is useful when it changes the engineering agenda. Three patterns point at three different repairs:

- If hallucinated answers cluster after retrieval, intervene on the retriever, reranker, and evidence formatter before rewriting the entire prompt.
- If bad edits occur after shallow planning, test state abstraction, preconditions, and value scoring.
- If confidence spikes after tool use, measure calibration conditioned on tool class rather than only in aggregate.

#### Test the Fix Like You Tested the Failure

The repair loop should keep the same empirical discipline as the measurement loop. A proposed fix is another change to the interpreter, so test it against the same family of tasks and the same cost ledgers.

Each added pattern must earn its place:

- Add decomposition only if the tasks have horizon, branching factor, prerequisites, uncertainty, or irreversibility enough to repay it.
- Add retrieval only if the missing evidence is usually outside working state.
- Add reflection only if errors are recoverable by trace inspection rather than by simply doing the obvious next action.

When two repairs are combined, check whether they assist each other or quietly multiply each other's vices.

#### Report Frontiers, and Label Failures by Transition

Report confidence-utility frontiers rather than a single accuracy point when systems face safety or cost constraints. A frontier shows what accuracy is available at each level of cost or risk, which is the decision a builder actually faces.

Track failures by transition label:

- illegal action;
- bad belief update;
- missing retrieval;
- contaminated memory;
- premature halt;
- unsafe reflection.

The categories tie the evaluation harness back to the interpreter semantics from the start of the chapter. A failure counted this way already names the part of the machine to open.

### Exercise

Choose a failure from an agent trace. Define the trajectory-level utility, one safety cost, and one calibration measurement. Then propose two interventions that could be replayed, and state the causal assumption required for each comparison to identify the cause rather than merely correlate with it.

Work it in four steps. First, write \(U(\tau)\) as something countable, such as "1 if the target test passes, else partial credit for correctly localizing the file". Second, write \(C(\tau)\) as a penalty on a specific forbidden or irreversible act. Third, choose a calibration measurement and say how you would bin it. Fourth, for each intervention, name exactly what you hold fixed. A good answer makes the held-fixed list explicit, because that list *is* the causal assumption.


# Tool Use and Embodiment

Intelligence without interfaces is monologue. This chapter turns reasoning into action through APIs (application programming interfaces, the entry points other software exposes), retrieval, and feedback from the environment the agent is coupled to.

## The Interpreter Gains a Body

In earlier chapters, an action could be treated as a mathematical choice. Here an action crosses a boundary. It lands in a filesystem, a browser, a database, a search index, a queue, or a human approval process.

## What Crossing the Boundary Costs

At that crossing, structural choices acquire observable costs. Five of them recur throughout the chapter:

- Permissions must be checked before the action is allowed.
- Latency, the waiting time between request and response, must be paid.
- Side effects may be irreversible, so there is no undo.
- Feedback may arrive late, long after the decision that caused it.
- The world may stubbornly continue existing after the model has finished its sentence.

A small example makes the cost real. If one file read takes 200 milliseconds, and the agent reads twelve files before editing, it has spent 2.4 seconds on looking.

## The Questions This Chapter Asks

The running example carries forward Chapter 2's coding agent, now working on this book's own publication pipeline, which is the same workflow Chapter 4 will treat as a small society. The interesting questions shift away from "what should it think?" Three sharper questions replace it:

1. What may it do?
2. What evidence must it fetch first?
3. How does it learn whether the world actually changed?

## Reading This Chapter as Engineering

Read this chapter as the engineering chapter of the book's formal story. Three plain readings carry most of the weight.

A schema, meaning a declared shape for arguments and results, is a grammar for external action. A retrieval result is a purchased observation: evidence you paid tokens and time to obtain. A sensor is any channel by which the world reports back, and an actuator is any channel by which the agent can affect that world.

The mathematics in the four topics that follow gives names to these ordinary design choices.


## Tool Interfaces and Function Calling

There is a moment when an agent stops talking and starts doing. A tool call is
that moment. What follows examines the contract that decides which requests may
touch the outside world, and what happens when a call is slow, refused, or sent
twice.

Tool use is where an interpreter stops describing a computation and begins to
change a world outside its own text stream. The decisive artifact is therefore
not the prompt. It is the boundary contract: the small formal agreement that
says which requests can cross from linguistic intention into external effect,
what evidence will count as success, and how the system behaves when the call
is delayed, denied, or repeated.

### Tool Calls Are the Primitive Operations of an Agent

In a Lisp evaluator, primitive procedures are trusted bridges from symbolic
expressions to machine operations. In an agentic interpreter, tool calls play
the same role. They are primitive operations, but now the machine operation may
do any of the following:

- send mail;
- alter a database;
- query a search index;
- move a cursor;
- deploy a service;
- charge a card.

A good tool interface makes this bridge narrow, typed, inspectable, and
recoverable: few allowed requests, request shapes declared in advance, a record
a person can read, and mistakes that can be undone or at least detected.

If the phrase "Lisp evaluator" is new, picture a small program that reads an
expression such as `(+ 2 3)` and knows that `+` is a primitive procedure: it is
not defined by more Lisp code inside the student's program, but by the
underlying machine. A JSON schema plays a similar role for a modern tool call.
JSON, short for JavaScript Object Notation, is a plain-text format for
structured data, and a schema is a declaration of which structures are legal. It
says which keys, strings, numbers, and objects form a legal request. The schema
is not the whole contract, but it is the first gate through which a
sentence-like intention becomes a machine-checkable action.

### Contract-First Action Semantics

The plain idea first: before you let an agent call a tool, write down what the
tool needs, what it promises, what it costs, and how much damage it can do.
Then let the runtime enforce that writing.

Represent a tool \(f\) by
\[
f : X \to Y,\quad \texttt{Pre}_f(x),\ \texttt{Post}_f(x,y),\ \texttt{Cost}_f(x),\ \texttt{Risk}_f(x).
\]
Read the first part as "the tool f maps a request x drawn from the request set X
to a result y in the result set Y". The four annotations read as "the
precondition of f at x", "the postcondition of f on x and y", "the cost of f at
x", and "the risk of f at x". The domain \(X\) is not merely a JSON shape. It is
the set of requests for which
the tool has agreed to interpret the arguments. The precondition says what must
already be true; the postcondition says what the caller may rely on afterward;
the cost and risk annotations let the planner compare this action with other
ways of learning or acting.

#### When Is a Call Legal?

An invocation \(u_t=(f_t,x_t,k_t)\), with idempotency key \(k_t\), is legal iff
schema, authorization, and preconditions pass:
\[
\texttt{legal}(u_t)=\mathbf{1}\{\texttt{schema\_ok}(x_t)\land \texttt{auth\_ok}(f_t)\land \texttt{Pre}_{f_t}(x_t)\}.
\]
Read \(u_t\) as "the invocation at step t", made of a chosen tool, its
arguments, and a key that names this attempt. Here "iff" means "if and only if":
the invocation is legal exactly in the cases where all three tests succeed. The
symbol \(\mathbf{1}\{\cdots\}\) is an indicator; it evaluates to 1 when the
statement inside is true and to 0 otherwise. The symbol \(\land\) reads "and".
Thus the formula is not mysticism. It says that well-formed arguments,
permission, and a ready state are jointly necessary for the call to cross the
boundary.

A builder checks this by logging all three test results on every attempt, so a
blocked call always names the test that stopped it.

#### Choosing Among the Legal Calls

The policy then chooses only among legal invocations:
\[
u_t^{*} = \arg\max_{u}\ \mathbb{E}[Q(\sigma_t,u)]-\lambda_c C(u)-\lambda_r R(u).
\]
Read this as "pick the invocation u that maximizes its expected value in the
current state, minus a price for cost and a price for risk". The term
\(\mathbb{E}[Q(\sigma_t,u)]\) is the expected usefulness of invocation u in
state \(\sigma_t\); \(C(u)\) is its cost; \(R(u)\) is its risk, which reuses the letter \(R\) that Chapter 1 gave to reward; and
\(\lambda_c\) and \(\lambda_r\) are weights that say how much you care about
each.

A tiny worked example makes the shape clear. One call has expected value 10,
cost 2, and risk 1; another has expected value 11, cost 2, and risk 6. With
\(\lambda_c = 1\) and \(\lambda_r = 1\), the first scores 10 - 2 - 1 = 7 and the
second scores 11 - 2 - 6 = 3. The less useful call wins because it is safer.

This is a compact way to say something practical: the next call is selected not
because it is syntactically possible, but because its expected contribution is
worth its latency, price, permission exposure, and failure surface. For long
horizons, Bellman structure supplies the usual discipline: choosing a tool now
also changes the future state of permissions, memory, obligations, and recovery
options [[5](#ref-5)] [[4](#ref-4)].
Bellman structure is the habit of valuing an action by its immediate payoff plus
the value of the situation it leaves behind.

#### A Contract Written Out in Full

The contract can be read as a small constitution for the primitive. This contract
spells out one invoicing tool: its arguments, its requirements, its
guarantee, its retry rule, its risk category, and the evidence it returns.

```text
tool create_invoice(order_id, amount, currency, idempotency_key)
  requires: caller has billing.write; order is approved; amount > 0
  ensures: exactly one invoice is durably associated with idempotency_key
  retry: safe with same idempotency_key
  risk: external financial record
  evidence: invoice id and ledger entry
```

This description is not decoration. It is executable design pressure. Three
different readers gain something concrete from it:

- the runtime can reject malformed arguments before the model improvises around
  them;
- the planner can prefer reversible tools before irreversible ones;
- the auditor can distinguish a schema failure from a permission failure or a
  broken postcondition.

### Idempotent Effects Under At-Least-Once Delivery

Retries are unavoidable; duplicate side effects are optional. Distributed
systems rarely guarantee that a request is executed exactly once. The practical
target is weaker and more useful: under at-least-once delivery, repeated
invocations with the same idempotency key should produce one durable effect and
one recorded result.

The terms deserve to be slowed down before the mathematics arrives:

- An idempotency key is a name for a logical attempt, such as
  `invoice:order-431:v1`.
- At-least-once delivery means the network may deliver the same request once,
  twice, or five times.
- A durable effect is an effect that survives crashes.
- An atomic transaction is a "both-or-neither" update.
- Idempotent means that doing the same thing again changes nothing further.

#### The Ledger Rule

Model the tool runtime as carrying a ledger \(L\) from keys to outcomes and a
keyed effect \(f_k\):
\[
\operatorname{invoke}(f,x,k,L)=
\begin{cases}
(L,L[k]) & k\in\operatorname{dom}(L),\\
(L\cup\{k\mapsto y\},y) & k\notin\operatorname{dom}(L),\ y=f_k(x).
\end{cases}
\]
Read the two branches in order. The first says: if key k is already in the
ledger's domain, return the ledger unchanged with the stored outcome \(L[k]\).
The second says: if the key is new, run the effect to get y, add the
pair "key maps to y" to the ledger, and return y.

The second branch is sound only if the effect and ledger write are one atomic
transaction, or if the external system itself interprets \(k\) so that
re-executing \(f_k(x)\) returns the same durable effect. A process that performs
\(f(x)\), crashes, and only then records \(L[k]\) has not achieved idempotent
visible behavior; it has created a duplicate-effect race.

#### Backing Off Instead of Hammering

A minimal retry controller can be written as
\[
n_{t+1}=\min(n_{\max},n_t+1),\qquad d_{t+1}=\beta d_t,\ \beta>1,
\]
with escalation when \(n_t=n_{\max}\). Read \(n_t\) as "the number of attempts
made so far at step t" and \(d_t\) as "the delay before the next attempt". The
attempt count climbs by one but never past its ceiling \(n_{\max}\), and the
delay is multiplied by a growth factor \(\beta\) greater than one. With
\(d_0 = 1\) second and \(\beta = 2\), the delays run 1, 2, 4, 8 seconds. When
the ceiling is reached, the system escalates rather than retrying forever. In
other words: optimism in policy, pessimism in side-effect handling.

#### How Duplicate Invoices Actually Happen

The invoice failure trace is the cautionary tale. Five lines follow one
attempt through a crash and a retry, and end with two invoices instead of one.

```text
t0  agent sends create_invoice(order-431, key=invoice:order-431:v1)
t1  billing service creates invoice INV-9
t2  process crashes before local ledger records the key
t3  agent retries without an external idempotency guarantee
t4  billing service creates INV-10 for the same order
```

The repair is to make the ledger write and invoice creation atomic, or to make
the billing system itself recognize the key and return `INV-9` on retry. The
The ledger rule is therefore a protection against a very ordinary mistake:
confusing "I did not receive the answer" with "the world did not change."

The interpreter should treat idempotency as part of the action, not a transport
option. A retry without the original key is a new proposal to the
world. A retry with the original key is an inquiry into whether the previous
proposal took effect. This distinction is the difference between a resilient
payment system and an expensive accident.

### Tool Calls as Interpreter Steps

Function calling, Toolformer-style API learning, and ReAct-style reason-act
traces should be understood as three views of the same transition system. API
stands for application programming interface, and a reason-act trace is a
written record that alternates a thought with an action. Each view contributes
one thing:

- Typed schemas make language intent machine-checkable.
- Learned tool-use policies show that a model can internalize when a primitive
  is useful from weak supervision, meaning training signals that are noisy or
  indirect rather than hand-labelled.
- Explicit reason-act traces expose the sequence of observations, decisions, and
  effects so that the agent loop can be inspected rather than merely sampled
  [[13](#ref-13)] [[12](#ref-12)] [[11](#ref-11)].

The resulting architecture is interpreter-like. The model proposes a primitive
operation; the contract checker validates it; the runtime executes it or refuses
it; the observation is returned to the evaluator; the next step is conditioned
on that observation. The important design move is that refusal is a normal
transition, not a crash. A denied permission, an expired token, or a failed
postcondition becomes data for the next step.

This loop is the whole idea in five lines of pseudocode. The policy makes a
proposal; a rejected proposal is fed back as an observation rather than thrown
as an error; an accepted proposal is invoked through the ledger; either way the
loop continues with a richer state.

```text
evaluate(state):
  proposal = policy(state)
  if not contract_allows(proposal):
    return evaluate(state.with_observation("rejected", reason))
  result = invoke_with_ledger(proposal)
  return evaluate(state.with_observation(result))
```

This loop is deliberately plain. Its strength lies in where it puts authority.
The language model may propose; the interface disposes. Four consequences
follow. Illegal actions are not left to prompt discipline. Risky actions are
represented as risky before they run. Expensive actions carry costs visible to
the policy. Irreversible actions must publish the evidence by which success or
rollback will later be judged. Topic 4 (Safety Constraints and Guardrails)
returns to what happens when a proposal must be blocked outright.

### Reading Failures Through the Contract

A mature tool interface makes failures classifiable. Each failure class points
at a different part of the machine:

- Schema errors mean the interpreter formed the wrong expression.
- Authorization errors mean the proposed transition lies outside the caller's
  role.
- Precondition errors mean the state was not ready.
- Postcondition errors mean execution did not establish what the tool promised.
- Timeout and retry errors mean the agent is uncertain about the external state
  and must consult the ledger, observe, or escalate.

#### The Same Tool Is Not Equally Safe in Every Task

The same failure table should be read against the task, not against tools in the
abstract. Four task properties change the verdict:

1. Reversible actions can tolerate exploratory calls and cheap rollback;
   irreversible actions demand stronger preconditions and independent evidence.
2. Side-effect risk changes how much authority the tool should receive.
3. Retry semantics decide whether repetition is harmless, ambiguous, or a second
   dangerous act.
4. Evidence availability decides whether the agent can verify a postcondition
   itself or must escalate to another sensor, another role, or a human. Topic 3
   (Embodiment: Sensors, Actuators, and Feedback) takes up that sensing question
   directly.

Thus a tool pattern is not "good" merely because it exists. It is good when the
task's reversibility, risk, retry behavior, and evidence surface make the
contract strong enough to improve the interpreter's next state.

#### What to Measure

This gives tool evaluation a concrete shape. Track the following, all countable
from ordinary logs:

- schema and precondition violation rates;
- postcondition success;
- duplicate-side-effect rate;
- rollback frequency;
- partial progress after failed calls;
- utility gain per call under fixed latency and token budgets.

If 200 calls produce 6 schema violations, that is a 3 percent rate; a climbing
rate usually means the schema and the model's habits have drifted apart. A tool
interface is publishable engineering when its failures are
explained by the contract itself. Then language can touch the world without
pretending the world is just more language.


## Retrieval-Augmented Tooling

Sometimes an agent should stop guessing and go look something up. This section
is about that decision: when an agent should fetch outside evidence, how it
should score and rank what it finds, and how it should carry that evidence into
its next step. Retrieval here is an action with a price, not a ritual.

### Retrieval as an Observation the Agent Buys

Retrieval-augmented tooling is the interpreter's way of asking the world for
evidence before it commits to an answer or an action. Retrieval-augmented
generation, usually shortened to RAG, is the general name for this pattern.

The retrieval call is not a decorative prelude to generation. It is an external
observation. The agent buys that observation under four constraints: latency
(how long the lookup takes), permission (whether the caller may see the source),
freshness (whether the source is current), and relevance (whether it bears on
the task). What comes back is then folded into the agent's state.

This framing matters because many failures called "hallucination" are really
failures of evidence acquisition. The model was asked to act as if its prior
were enough. A prior here means the belief the model already carries from
training, before it looks anything up.

A retrieval-capable agent has a larger action space. It can:

- search the repository;
- inspect a table schema;
- query a memory index;
- open the current policy;
- fetch a manual page;
- or decide that no new evidence is worth its cost.

That last option is a real action, not a failure to act.

### The Probabilistic Retrieval-Generation Pipeline

The pipeline has two stages: find evidence, then answer using it. Writing that
down as probability makes the two stages separately inspectable.

Each piece of notation used in that pipeline gets a plain reading below:

| Symbol | Read it as |
|---|---|
| \(\mathcal{D}\) | the set of candidate documents the retriever can return |
| \(e_q\), \(e_d\) | vector embeddings of the query and of a document |
| \(H\) | entropy, a measure of how spread out the agent's uncertainty is |
| \(\tau\) | a threshold on entropy chosen by the designer |
| \(\mathrm{VoI}(q)\) | expected value of information for the query \(q\) |

For query context \(x\), retrieved document \(d\), and answer \(y\):
\[
p(y\mid x) = \sum_{d \in \mathcal{D}} p(y\mid x,d)\,p(d\mid x).
\]
Operationally, \(p(d\mid x)\) is retrieval and ranking; \(p(y\mid x,d)\) is
grounded generation conditioned on the acquired evidence [[14](#ref-14)].

#### Reading the Sum over Documents

The vertical bar in \(p(y\mid x,d)\) means "given." Read the equation this way:
the agent imagines each possible document \(d\), asks how likely answer \(y\)
would be if that document were the evidence, and weights that answer by how
likely the retriever was to select \(d\) for the query \(x\).

Suppose two candidate documents. The retriever gives
the first a selection chance of 0.8 and the second 0.2. Given the first, the
answer "the limit is 30 days" has probability 0.9; given the second, only 0.1.
Then \(p(y\mid x) = 0.8 \times 0.9 + 0.2 \times 0.1 = 0.74\). Notice that the
retriever's ranking, not the generator's fluency, did most of the work.

The sum is not saying the agent literally reads every document in the universe.
It is a clean idealization of a ranked evidence process.

#### Dense and Lexical Retrieval Scores

Typical retrieval scores include dense similarity
\[
s_{\text{dense}}(q,d)=\langle e_q,e_d\rangle
\]
and lexical ranking such as BM25 [[15](#ref-15)] [[46](#ref-46)].
BM25 is a long-standing formula that scores a document by which query words it
contains and how rare those words are.

An embedding \(e_q\) or \(e_d\) is a vector representation of a query or
document. The angle brackets denote an inner product: multiply corresponding
coordinates and add them. For example, \(\langle (1,0,2),(1,1,1)\rangle
= 1 + 0 + 2 = 3\).

Similar vectors point in similar semantic directions. So a query about
"permission checks before deletion" may retrieve a passage about "authorization
gates for destructive actions" even without exact word overlap.

Each family buys something different:

- Dense retrieval buys semantic reach, matching meaning across different wording.
- Lexical retrieval buys exact surface matches and interpretable term evidence.

Hybrid systems are common because the two failures differ. An embedding may miss
a precise identifier such as `PolicyV3_2024`. A lexical ranker may miss a paraphrase.

#### Deciding When to Retrieve

The control question is when to retrieve. One uncertainty-triggered policy is
\[
\texttt{retrieve}_t = \mathbf{1}\{H[p(\cdot\mid h_t)] > \tau\},
\]
but the economically sharper rule is expected value of information:
\[
\mathrm{VoI}(q)=\mathbb{E}\!\left[\max_a\mathbb{E}[U(a,S)\mid q]\right]-\max_a\mathbb{E}[U(a,S)].
\]
Retrieve when \(\mathrm{VoI}(q)\) exceeds retrieval cost.

Here \(H\) is entropy, a measure of spread-out uncertainty. If the agent assigns
nearly all probability to one answer, entropy is low. If many answers remain
plausible, entropy is high. \(\tau\) is a threshold chosen by the designer.

The bold \(\mathbf{1}\{\cdot\}\) is an indicator: it equals 1 when the condition
inside holds and 0 otherwise. So the rule reads "retrieve at step \(t\) exactly
when uncertainty about the next answer exceeds \(\tau\)." In practice, this
simple rule says: when the model is too uncertain, buy evidence unless the
evidence is too expensive or forbidden.

#### Value of Information as the Sharper Rule

The value-of-information expression, VoI for short, gives a sober interpretation
of search. Read it as the difference between two quantities: the best expected
usefulness \(U\) the agent could reach after seeing the answer to \(q\), minus
the best expected usefulness it can reach right now, averaging over the unknown state \(S\).

The question is not "could more context be useful?" Almost always, yes. The
question is whether the expected change in the downstream decision is worth the
delay, token budget, privacy exposure, and distraction risk of importing more
text.

To use this, you need no exact number. Estimate roughly: if a lookup costs two
seconds and would change the action in one case out of twenty, it pays only when
that case is expensive to get wrong.

### Evidence as an Action

Let the retrieval decision be an action
\(a_t\in\{\texttt{retrieve},\texttt{skip}\}\). Read that as: at step \(t\) the
agent picks either "retrieve" or "skip." A budget-aware control law prices
its latency and token cost while preserving the long-horizon effect on the
task [[5](#ref-5)] [[4](#ref-4)]. This is
the formal version of a practical truth: always retrieving is slow, never
retrieving is reckless.

#### Separating the Retrieval Policy from the Generation Policy

An agentic retrieval policy should therefore be separate from the generation
policy. A policy is simply a rule for choosing actions.

The retrieval policy observes:

- the task type;
- current uncertainty;
- freshness requirements;
- source permissions;
- and cost.

It then chooses among local search, vector memory, web search, database lookup,
tool documentation, or no retrieval. The generation policy receives a bounded
evidence set with provenance and conflict information. Provenance means the
record of where each item came from.

#### A Small Control Program for Retrieval

The following pseudocode shows that separation: estimate need, list
permitted sources, compare value against cost, then either answer from the
current state or retrieve, rank, and answer with citations.

```text
need = uncertainty(task, history)
sources = allowed_sources(task, caller)
if value_of_information(need, sources) <= retrieval_cost:
  answer_from_current_state()
else:
  evidence = retrieve_and_rank(task, sources)
  answer_with_citations(evidence)
```

#### Typed Evidence Instead of Context Sludge

The small program hides a difficult discipline: retrieved text must not become
untyped context sludge. Each item should carry source, timestamp, access path,
rank score, and the claim it supports.

If two sources disagree, the agent should surface the conflict or acquire
higher-authority evidence. It should not smooth the contradiction into fluent
prose.

For a beginner builder, this is where retrieval becomes tool design instead of
text stuffing. A source may be:

- relevant but stale;
- authoritative but outside the caller permission boundary;
- fresh but contradicted by a higher-authority manual;
- or cheap but too vague to change the decision.

A well-designed retrieval tool returns enough metadata for the interpreter to
reason about those differences. Topic 1 (Tool Interfaces and Function Calling)
sets out the contract style that makes such metadata declarable.

### Where Retrieval Belongs

Retrieval should often precede irreversible action. Four examples make the rule
concrete:

- A coding agent should inspect relevant symbols before editing.
- A compliance agent should fetch the current rule before advising.
- A data agent should retrieve schema and sample rows before writing a query.
- A deployment agent should inspect recent incidents and service health before
  changing production.

In each case, retrieval is valuable only if it can change the rational next
move. Topic 4 (Safety Constraints and Guardrails) takes up what to do when the
next move is dangerous.

#### Measuring Retrieval Quality

This also explains why retrieval quality cannot be judged by answer style
alone. Measure Recall@\(k\), nDCG, citation faithfulness, contradiction rate,
freshness error, tool-call efficiency, and end-task utility under fixed
retrieval budgets.

Then compare three policies: always-retrieve, never-retrieve, and an
uncertainty or value-of-information policy. The comparison matters because each
policy fails differently:

- always-retrieve spends tokens and time even when the state is already
  sufficient;
- never-retrieve turns stale memory into false confidence;
- a conditional policy can still be wrong if its uncertainty signal is
  miscalibrated.

If retrieval cannot buy measurable uncertainty reduction per unit latency, it is
ritual rather than reasoning.

Recall@\(k\) asks whether the needed evidence appears somewhere in the top
\(k\) retrieved items. Set \(k = 5\), and if the needed passage lands at rank 4,
Recall@5 counts it as found. nDCG, normalized discounted cumulative gain, also
cares about order: useful evidence near rank 1 counts more than the same
evidence buried near rank 20.

These metrics are not literary judgments of the final answer. They are tests of
whether the observation step gave the interpreter a fair chance to know what it
needed.

#### Over-Retrieval and Under-Retrieval

The theory pays off by preventing two expensive pathologies. Over-retrieval
bloats context, slows execution, and admits distractors. Under-retrieval lets
fluent priors masquerade as evidence.

A retrieval-augmented agent is better not because it keeps more documents
nearby, but because it knows when an external document deserves to govern the
next interpreter step.

#### How Composition and Memory Change the Calculation

Composition can improve this judgment or spoil it. A planner that retrieves
fresh evidence once, then passes the evidence and provenance to subtasks, can
save calls and keep the collective anchored. A planner that retrieves
redundantly for every subtask may spend its budget proving the same fact four
times.

Memory can help by remembering what was already checked. Stale memory can also
suppress retrieval that the current task plainly needs.

Retrieval is therefore most valuable for tasks with four properties together:
high uncertainty, fresh external facts, inspectable evidence, and enough
consequence that the delay is cheaper than the mistake.


## Embodiment: Sensors, Actuators, and Feedback

Embodiment means the world answers back. Our subject is agents whose actions
land somewhere real, and the delay between the acting and the landing. We build
a small model of that delay, learn to estimate the present from stale readings,
and see what changes when a tool call must settle before it can be trusted.

The body of a software agent is not made of metal. It is made of APIs
(application programming interfaces, the published entry points other systems
expose), filesystems, browsers, queues, clocks, caches, databases, rate limits,
permissions, and humans waiting for results. These bodies have delay, noise,
saturation, and failure modes. None of those problems become simpler because the
agent writes fluent sentences.

### Command, Effect, and Observation Are Three Different Things

An interpreter that touches the world must distinguish command from effect, and
effect from observation. A command is what the agent asked for. An effect is
what actually changed. An observation is what a sensor later reports. The three
can disagree for a while, and that interval is where most embodied bugs live.

Ordinary examples make the gap concrete:

- A click may not settle the page.
- A deploy may not become healthy.
- A database write may replicate later.
- A queue metric may describe the past.

Embodiment is the discipline of acting under those lags while remaining correct
enough to be trusted.

### A State-Space Model That Accounts for Lag

Before the equations, the plain idea: the world has a true condition the agent
cannot see directly, the agent pushes on it, and the report of what happened
arrives late. A state-space model is simply a pair of rules, one for how the
world moves and one for what the sensors say.

Let latent state \(x_t\), meaning hidden from the agent's sensors, plus control
\(u_t\) and observation \(o_t\):
\[
x_{t+1}=f(x_t,u_{t-d_u})+w_t,\qquad o_t=g(x_{t-d_o})+v_t,
\]
where \(d_u\) and \(d_o\) are actuation and observation lag. Read the first
equation aloud as "the state at the next step comes from the current state plus a
command issued \(d_u\) steps ago, plus a random disturbance." Read the second as
"today's observation is a function of a state from \(d_o\) steps ago, plus
measurement error."

The policy \(\pi\), the agent's rule for choosing actions, picks \(u_t\) under
bounds such as \(\|u_t\|_\infty\le u_{\max}\), because commands outside the
envelope are not bold; they are invalid.

#### The Symbols, Read Aloud

A symbol you cannot pronounce is a symbol you will not remember, so here is a
short glossary of the ones this loop runs on:

| Symbol | Read it as | Concrete meaning |
|---|---|---|
| \(x_t\) | "the latent state at step t" | What is really going on, such as a service's true health |
| \(u_t\) | "the control at step t" | What the agent does, such as adding two workers |
| \(o_t\) | "the observation at step t" | What the sensors report, such as a queue depth measured thirty seconds ago |
| \(w_t\) | "process noise at step t" | Uncommanded changes in the world |
| \(v_t\) | "observation noise at step t" | Error in the measurement |
| \(d_u\), \(d_o\) | "actuation lag, observation lag" | How late a command lands, and how late a reading arrives |
| \(\|u_t\|_\infty\) | "the infinity norm of u at step t" | The largest absolute component of the command vector |

The infinity norm is a compact way to say that no single knob may be turned too
far at once. If a scale command is the vector \((+3, -1)\), its infinity norm is
3, so a bound of \(u_{\max}=2\) rejects it.

This model applies directly to ordinary software operations. The latent state
may be the real health of a service. The control may be a rollout, a rollback, or
a scale adjustment. The observation may be delayed telemetry. The disturbance
terms \(w_t\) and \(v_t\) stand for everything the agent did not command and
everything the sensor did not measure cleanly. Chapter 1, Topic 3 (World Models
and State Abstractions) develops the general habit of naming state before acting
on it; here the new wrinkle is that the naming must include time.

### The Estimation and Control Backbone

Two jobs must now be separated. Estimation asks what the state probably is.
Control asks what to do given that estimate. Classical engineering has a standard
answer for each.

#### Predict, Then Correct: The Kalman Update

For linearized delay-free dynamics, Kalman filtering gives recursive belief
updates:
\[
\hat x_{t|t-1}=A\hat x_{t-1|t-1}+Bu_{t-1},\qquad
K_t=P_{t|t-1}H^\top(HP_{t|t-1}H^\top+R)^{-1},
\]
\[
\hat x_{t|t}=\hat x_{t|t-1}+K_t(o_t-H\hat x_{t|t-1}),
\]
followed by feedback control \(u_t=-K\hat x_t\) in LQR style
[[36](#ref-36)] [[41](#ref-41)].

Kalman filtering is the disciplined version of "predict, then correct." The hat
in \(\hat x\) marks an estimate rather than the truth. The subscript
\(t|t-1\) means "the estimate for time \(t\) before seeing time \(t\)'s
observation"; \(t|t\) means "after seeing it."

The remaining letters each have one job:

- Matrix \(A\) predicts how the state evolves on its own.
- Matrix \(B\) says how yesterday's command changes today's state.
- Matrix \(H\) says what the sensor can see.
- Matrix \(P\) records uncertainty in the estimate.
- Matrix \(R\) records observation noise. Control theory reuses the letter \(R\) here; it is not Chapter 1's reward.
- The Kalman gain \(K_t\) decides how strongly to trust the new observation
  relative to the prediction.

#### Delay Requires an Augmented State

With observation delay \(d_o\), the state must be augmented, for example
\[
z_t=(x_t,x_{t-1},\ldots,x_{t-d_o}),
\]
so the filter estimates the present from a history that explicitly contains the
stale state being observed. Read \(z_t\) as "the stacked list of the present
state and the last \(d_o\) states." Calling a standard delay-free update
"lag-aware" without this augmentation is a category error.

The augmented state \(z_t\) is also an estimate, not an oracle. It contains
latent variables for the present and the recent past so the filter can reason
about which old state a delayed observation is actually describing. The agent is
carrying a little clockwork model of time, not a perfect diary of truth.

#### Two Different K's: Estimation Gain Versus Feedback Gain

Do not confuse that \(K_t\) with the feedback gain \(K\) in \(u_t=-K\hat x_t\).
The first \(K_t\) belongs to estimation; it tells the interpreter how to update
belief. The second \(K\) belongs to control; it tells the actuator how hard to
push once a state estimate exists. LQR, linear-quadratic regulation, is the
classical setting where a linear system is controlled by minimizing a quadratic
penalty on state error and control effort. In practice you tune that penalty:
raise the price of control effort and the agent pushes more gently.

#### A Worked Queue Estimate You Can Check Mentally

For a scalar queue example, suppose yesterday's delayed sensor says the queue
was 100 jobs. The model predicts that two added workers should have reduced it to
70 by now. A noisy current observation reports 80. A cautious Kalman gain of
\(K_t=0.25\) updates the estimate to
\(70+0.25(80-70)=72.5\).

The arithmetic is small on purpose: prediction and observation differ by 10 jobs,
and a quarter of 10 is 2.5. The agent should scale from 72.5, not blindly from the
stale 100 or the noisy 80.

#### Act on an Estimate, Not on the Last String Received

The control-theoretic point is modest but powerful: the agent should act on an
estimate of present state, not on the last string it received. Long-run behavior
is still governed by the same reinforcement-learning objective
\(J(\pi)=\mathbb{E}_\pi[\sum_t\gamma^t r_t]\), read as "the expected sum of
rewards under the policy, with later rewards discounted by \(\gamma\) each step."
The state supplied to the policy must be earned through sensing and filtering
[[3](#ref-3)] [[4](#ref-4)]
[[5](#ref-5)].

### Feedback in Ordinary Tools

Suppose a deployment agent scales workers from delayed queue telemetry. A naive
policy reacts to stale data and oscillates: queue high, scale up; delayed queue
still high, scale up again; delayed drop finally appears, scale down too far. A
lag-aware estimator plus a bounded feedback policy stabilizes behavior and cuts
rollback churn. Same API, different control geometry.

The loop that fixes the oscillation is short. Each line is one step:

```text
observe telemetry with timestamp
estimate current queue depth from delayed samples
choose bounded scale adjustment
wait for the expected settling interval
observe health before issuing the next adjustment
```

In words: timestamp the reading, correct for the lag, command within the bound,
wait for settling, then confirm health before commanding again.

#### The Same Loop in Browsers, Databases, and Code

A browser agent follows the same pattern at smaller scale. It clicks, observes
the DOM (Document Object Model, the browser's live tree of page elements) after
the page has had time to respond, compares the new state to the
expected transition, and only then continues. A data agent runs a query, inspects
rows and errors, and updates its belief about the schema. A code agent edits,
runs tests, and treats failures as observations rather than insults.

#### When Feedback Helps and When It Misleads

Feedback helps only when its timing and quality fit the task. If delay is short,
noise is low, disturbances are small, and the system has settled, feedback can
turn action into control.

Feedback can also lure the interpreter into overcorrection. That happens when the
sensor reports the past, when the world is being disturbed by other actors, or
when the actuator has not yet had time to take effect. Planning and reflection do
not automatically cure this. Composed with stale feedback, they may amplify
oscillation by inventing elaborate reasons to chase yesterday's measurement.

The practical question is always fourfold: what state does this observation
describe, how noisy is it, what changed while it was traveling, and has the
system had time to settle?

### Sensor and Actuator Models

A practical embodied architecture records two kinds of models, one for reading
the world and one for changing it.

Sensor models describe freshness, noise, authority, sampling delay, and blind
spots. Written down, they read like this:

- "CI status, meaning the continuous integration pipeline's report, is ten minutes old."
- "Repository search excludes generated code."
- "Browser state may have changed after navigation."

Actuator models describe effect delay, reversibility, rate limits, blast radius,
and confirmation signals:

- "Deployment takes five minutes to settle."
- "Email send is irreversible."
- "File edit is reversible until committed."

#### Choosing Between Waiting, Probing, Acting, and Escalating

These models let the policy choose among four moves rather than always acting.
If telemetry is stale, observe again or widen uncertainty. If an actuator is
saturated, meaning further commands produce no additional effect, stop issuing
larger commands and choose a different route. If the confirmation signal never
arrives, consult an independent sensor before retrying an irreversible action.
Topic 4 (Safety Constraints and Guardrails) takes up the harder cases of
irreversibility.

#### Where Control, Reward, and System Limits Meet

Three bodies of theory each supply one piece of this loop.
Control-theoretic estimation supplies the best available state from noisy,
delayed observations. Reinforcement learning supplies the long-horizon objective
that prices delayed consequences. System-level analysis supplies constraints such
as latency, rate limits, and actuator saturation
[[36](#ref-36)] [[3](#ref-3)]
[[4](#ref-4)] [[2](#ref-2)]. The shared
lesson is that autonomy is not the absence of feedback. It is obedience to the
right feedback at the right time.

#### How to Measure Whether an Agent Is Safely Embodied

Evaluate embodied agents by measuring six things:

1. Delay margin, or how much extra lag the loop tolerates before going unstable.
2. Sensitivity to sensor noise.
3. Disturbance recovery, meaning how quickly the agent returns to target after an
   uncommanded change.
4. Settling time after actions.
5. Saturation events, counted whenever a command exceeded what the actuator could
   deliver.
6. Closed-loop stability with and without lag-aware estimation, run as an A/B
   comparison, meaning two matched groups of runs that differ in exactly one
   design choice.

An agent that ignores feedback geometry may still produce confident commands, but
it is not yet safely embodied.


## Safety Constraints and Guardrails

Between what an agent wants to do and what the world actually suffers stands a
layer of machinery. That machinery is what we build here. We will price harm
with numbers, fence the state with an inequality, and decide who is allowed to
sign off on what. The reward for reading carefully is a safety story you can
test, not merely recite.

Safety is not a postscript to capability. It is the part of the interpreter that
decides which proposed transitions are outside the program's charter, which are
allowed but costly, and which require another authority before the world may be
changed. A *transition* here is one step of the agent loop: the move from the
current state to the next state. In a tool-using system, safety lives at the same
boundary as action. That boundary sits between the model's proposed next step and
the external effect that would make that step real.

This makes guardrails more than warning text. A guardrail is a filter on the
agent's transition system, meaning the set of steps the agent is able to take at
all. Such a filter has four moves available:

- remove an action from the action space, so the agent cannot even propose it;
- reshape the action into a safer one;
- pause for human approval;
- attach an obligation to monitor what happens next.

### Constrained Control Formulation

#### Rewarding the Agent While Capping Its Harm

Start with the ordinary picture of a decision-making agent and then add ledgers
for harm. Model policy selection as a constrained MDP (Markov decision process,
the standard model of an agent choosing actions in states over time):
\[
\max_{\pi}\ J_R(\pi)=\mathbb{E}_\pi\!\left[\sum_t\gamma^t r_t\right]
\quad\text{s.t.}\quad
J_{C_j}(\pi)=\mathbb{E}_\pi\!\left[\sum_t\gamma^t c_{j,t}\right]\le d_j.
\]
Read this first as bookkeeping. \(J_R(\pi)\) reads "the expected discounted
reward earned by policy \(\pi\)", where a policy is the agent's rule for choosing
actions, and *discounted* means later rewards count a little less. Each
\(J_{C_j}(\pi)\) reads "the expected discounted amount of harm number \(j\)".
Those harms are concrete: privacy exposure, money spent, dangerous commands, or
manual interruptions. The bound \(d_j\) is the allowed budget for that cost, and
"s.t." reads "subject to".

The contrast is the whole point. A plain reinforcement-learning agent asks, "How
much reward can I get?" A constrained agent asks, "How much reward can I get
while keeping each harm ledger under its limit?"

That constrained objective is dense with notation, so the following table gives
each symbol a short reading before we use it again.

| Symbol | How to read it |
|---|---|
| \(\pi\) | The policy: the agent's rule for choosing actions |
| \(J_R(\pi)\) | Expected discounted reward under that policy |
| \(J_{C_j}(\pi)\) | Expected discounted amount of harm \(j\) |
| \(d_j\) | The budget allowed for harm \(j\) |
| \(\lambda_j\) | The price charged for one unit of harm \(j\) |
| \(h(x)\) | Safety margin at state \(x\); nonnegative means safe |

#### Turning Constraints into Prices

The Lagrangian form, which folds a constraint into the objective by charging a
price for breaking it,
\[
\mathcal{L}(\pi,\lambda)=J_R(\pi)-\sum_j\lambda_j\big(J_{C_j}(\pi)-d_j\big)
\]
supports dual optimization and transparent trade-off tuning.

A Lagrange multiplier \(\lambda_j\) is a shadow price for violating constraint
\(j\). If privacy risk is already close to its bound, a large \(\lambda_j\) makes
risky actions look expensive. If the risk ledger is comfortably low, the price
can be smaller. Dual optimization is the process of adjusting these prices while
improving the policy; a builder implements it as a slow feedback loop that raises
a price whenever the measured ledger creeps over budget.

With two actions the idea is visible. Suppose `fast_patch` yields reward 10 and
harm 4, while `safe_patch` yields reward 7 and harm 1 under a harm budget of 2.
When \(\lambda=0\), fast wins, since 10 beats 7 and harm is free. When
\(\lambda=2\), their priced values become \(10-2(4-2)=6\) and \(7-2(1-2)=9\), so
the safer action wins because scarce safety budget has become dear. Notice that
`safe_patch` is rewarded for coming in under budget.

#### Prohibition Is Not the Same as Price

At the state-action level, constrained Bellman structure appears as
\[
Q^\pi_\lambda(s,a)=r(s,a)-\sum_j\lambda_j c_j(s,a)+\gamma\,\mathbb{E}_{s'}[V^\pi_\lambda(s')],
\]
which reads "the priced value of taking action \(a\) in state \(s\) is its reward
minus its priced harms, plus the discounted value of wherever it lands you". This
makes "unsafe but high reward" mathematically explicit instead of politically
vague.

Some constraints are hard: do not leak secrets, do not run a destructive command
without authorization, do not fabricate a citation. Others are budgets: latency,
cost, bounded uncertainty, allowed retry counts. The mathematics matters because
it separates prohibition from price. Hard constraints belong in the action space
as removals; budgets belong in the objective as costs.

### Runtime Safety Filter

#### A Fence Written as an Inequality

Define safe set \(\mathcal{C}=\{x:h(x)\ge0\}\). Control barrier functions require
\[
\dot h(x,u)+\alpha(h(x))\ge0
\]
for class-\(\mathcal{K}\) function \(\alpha\), giving forward invariance of
\(\mathcal{C}\) [[52](#ref-52)]. A practical filter solves
\[
u^\star=\arg\min_u \|u-u_{\text{nom}}\|^2
\quad\text{s.t.}\quad
\dot h(x,u)+\alpha(h(x))\ge0,
\]
so nominal autonomy is preserved when safe and corrected when not. Here
\(u_{\text{nom}}\) is the control the agent nominally wanted, and \(u^\star\) is
the nearest control that still satisfies the safety condition.

The notation hides a simple fence. The function \(h(x)\) measures signed distance
from danger: nonnegative means safe, negative means outside the safe set. The dot
in \(\dot h\) means derivative, the instantaneous rate at which that safety
margin is changing under control \(u\). A class-\(\mathcal{K}\) function is an
increasing function with \(\alpha(0)=0\); it lets the allowed rate depend on how
much margin remains. Forward invariance means that once the state starts in the
safe set, the filtered controller keeps future states there under the model
assumptions.

#### A One-Dimensional Budget Example

In one dimension, let \(x\) be dollars already spent and let the budget cap be
100, so \(h(x)=100-x\). At \(x=95\), the margin is \(h=5\). A proposed action
that spends 10 would push \(h\) negative, to \(-5\). The filter searches for the
closest acceptable action, perhaps spend 4, ask approval, or wait for more
budget. The minimization is the formal way of saying "change the command as
little as possible while preserving the safety condition."

#### The Same Pattern for Language Agents

For language agents, the same pattern appears in less continuous clothing. The
nominal action may be "delete the database," "email this file," or "publish the
deployment." The safety filter checks state, role, data class, reversibility,
blast radius, and evidence. If the proposed action would cross a boundary, the
filter blocks it, rewrites it into a reversible alternative, or asks for human
approval.

This analogy must be used honestly. A continuous control-barrier proof does not
automatically prove that a discrete language-agent filter is safe. To get an
equally formal guarantee, the language-agent system would need its own transition
invariant: a statement showing that every permitted discrete step preserves the
safety property. Without that proof, the barrier picture is a design pattern and
a source of tests, not a borrowed certificate.

The safety filter has four branches: propose, classify the
risk, then reject, escalate, or execute under monitoring.

```text
proposal = policy(state)
risk = classify(proposal, state)
if forbidden(risk):
  reject(proposal)
elif requires_approval(risk):
  ask_human(proposal, evidence)
else:
  execute_with_monitor(proposal)
```

The important feature is placement. The filter stands between proposal and
effect, not between effect and apology.

### Layers of Constraint

Safety architectures are layered because no single check sees the whole risk.
Each layer watches a different moment in the loop:

- Static constraints remove forbidden tools or arguments before planning begins.
- Pre-execution checks validate schemas, permissions, data sensitivity, and risk
  class.
- Runtime monitors watch for drift, unsafe intermediate states, budget
  exhaustion, and unexpected tool outputs.
- Post-action checks verify whether the intended safety property actually held.
- Audit records make repair possible when the system or organization learns that
  a boundary was incomplete.

Three bodies of theory supply these layers. Constrained MDP theory provides the
expected-utility compass with explicit harm budgets. Control barrier functions
provide the model of an online filter that preserves invariants. Governance
frameworks translate institutional risk appetite into operational envelopes that
outlive any single prompt or model version
[[51](#ref-51)] [[52](#ref-52)]
[[29](#ref-29)] [[53](#ref-53)].
Together they make safety a property of the agent loop, not a promise in the
system message. Topic 3 (Embodiment: Sensors, Actuators, and Feedback) supplies
the sensing and feedback machinery that these monitors depend on.

### Designing for Escalation

#### Handing a Decision to a Human on Purpose

Human escalation is not a defeat. It is a designed transition for states where
the autonomous policy should not pretend to be sovereign. The interface should
answer four questions:

- what evidence the human receives;
- what decision is requested;
- how long the approval remains valid;
- whether the agent may continue with a safer fallback while waiting.

#### Allocating Authority Action by Action

Authority is therefore an allocation problem. A reversible formatting edit may be
delegated to the agent. A citation replacement may require evidence. A
secret-bearing export may require a human. A forbidden disclosure may not be
priced at all, because a hard constraint is not an expensive option.

Different tasks deserve different authority envelopes according to
reversibility, blast radius, evidence quality, time pressure, and the value of
partial progress while approval is pending. Topic 1 (Tool Interfaces and Function
Calling) describes the contracts these envelopes attach to. The design error is
to flatten all of this into either "the agent is autonomous" or "the human
decides." An institution allocates authority at the transition where it matters.

#### Measuring Whether the Guardrails Work

Evaluate these systems by reporting task return against violation probability,
dual-variable stability where constraints are optimized, blocked-action loops,
escalation latency, successful fallback rate, and incident quality under
correlated failures rather than isolated happy-path tests
[[33](#ref-33)] [[34](#ref-34)]. Read that
list as a dashboard: reward on one axis, violations on the other, with the
awkward operational numbers beside them.

A better agent is not the one that says it will be safe. It is the one whose
forbidden actions are blocked, whose risky tradeoffs are explicitly priced, whose
ambiguous actions escalate, whose waiting states still make useful progress when
allowed, and whose incidents generate evidence for repair.


# Multi-Agent Systems

When one agent is uncertain, we consult evidence. When many agents are uncertain, we need institutions.

This chapter is about several agents working at once on one task. One agent is a program. Many agents are a small society, and societies need rules.

## From One Interpreter to Many

Chapter 1 built a single interpreter. It observes the environment, updates state, chooses an action, executes it, and loops. This chapter adds one more layer around that interpreter. Now several such machines run at once. Each has its own partial state, meaning it sees only a slice of the world. Each has its own budget, its own memory, and its own authority. Yet all of them affect one shared world.

## Why Benefits Stop Adding Up

This is the decisive test of composition. Two agents look like twice the capability. Say one agent alone finishes 6 tasks an hour. Two rarely finish 12, because they now queue behind the same file lock and the same rate limit. Benefits that looked additive in isolation stop being additive once interpreters share state, cost, authority, latency, and incentives.

The new layer is therefore not "more prompting." It is an institutional evaluator: an evaluator that runs the rules of a group rather than the steps of one agent. Four kinds of rules do that work:

- Protocols decide who may speak.
- Mechanisms decide how scarce authority is allocated.
- Learning dynamics reveal which conventions survive adaptation.
- Ensembles decide when disagreement is useful evidence rather than noise.

## The Running Example: This Book's Publication Workflow

The running example is the publication workflow itself. A drafter proposes text. A fact checker tests claims. An integrator commits patches. A router decides which interpreter should see the next fragment of work.

The shared document becomes the common heap, the one store every agent may touch. The audit log becomes the continuation, the record of what still must happen. Messages, votes, bids, critiques, and commits become the visible transitions. By them, many local evaluators simulate one larger, stranger program.


## Coordination Protocols and Communication

Several agents working the same job at the same time is not one agent doing more of it. Each one sees only a slice of the situation. Each one can send messages that change what the others believe and do. The rules governing those messages are called a protocol, and designing, reading, and testing one is the work ahead.

When many interpreters share an environment, communication is not an ornament added to intelligence. It is one of the control surfaces of the system. Each agent sees only part of the state, updates its own local machine, and emits messages that may change the machines around it. A protocol is the rule that makes those local steps compose.

The SICP way to read a multi-agent system, after *Structure and Interpretation of Computer Programs*, the classic text this book echoes, is to ask what each interpreter treats as its environment. In a single evaluator, an expression is reduced against a frame of bindings, meaning a table of names and their current values. In a collective, that frame is distributed across many places at once:

- private scratchpads,
- local observations,
- message queues,
- shared documents,
- tool outputs,
- locks,
- audit logs.

Coordination is the art of making these frames interact without pretending that any one agent sees the whole store. "Store" here means the full collection of state that the system holds; no single agent gets to read all of it.

### Protocols as Distributed Transition Systems

#### Local State, Messages, and the Missing Global View

A protocol is best written as a transition rule: given what an agent holds and what just arrived, what does it hold next and what does it say next?

Let agents \(i\in\{1,\dots,n\}\) have local state \(x_i^t\), incoming messages \(m_{*\to i}^t\), and outgoing messages \(m_{i\to *}^{t+1}\). Read \(x_i^t\) as "the private state of agent i at step t". Read \(m_{*\to i}^t\) as "everything sent to agent i, from anyone, at step t"; the star means "any sender". A protocol \(\Pi\) defines the legal local transition
\[
(x_i^{t+1}, m_{i\to *}^{t+1}) = \Pi_i\!\left(x_i^t,\{m_{*\to i}^t\}\right).
\]
Read this as: agent i's rule takes its current private state and its inbox, and returns its next private state together with the messages it sends.

The global state is not stored in any one agent. It is induced by the product of local states, channels, clocks, and shared artifacts. That is why multi-agent debugging so often feels unlike single-agent debugging. The failure may not live inside one interpreter. It may live in the order in which interpreters heard each other. In practice this means your logs must record message arrival order, not only message content.

#### Beliefs Differ Even When the Document Does Not

Local state also includes belief, which is an agent's estimate of what is true given what it has seen. Agent \(i\) receives observation \(o_i^t\), maintains a belief \(b_i^t(s)\), and chooses both domain actions and communication actions:
\[
b_i^{t+1}=\operatorname{Update}_i(b_i^t,o_i^{t+1},m_{*\to i}^{t+1}).
\]
Read \(b_i^t(s)\) as "how likely agent i thinks the world is in state s at step t". The update line says the new belief comes from the old belief, the newest observation, and the newest messages.

The shared artifact is not the same thing as shared belief. Three small examples make the gap concrete:

- A fact checker may know that a citation is weak before that weakness appears in the draft.
- An integrator may see two unresolved comments but not the search failures behind them.
- A drafter may believe a paragraph is ready because no critique has arrived yet.

Decentralized uncertainty begins here: agents act under different information, and communication is a costly attempt to reshape that information.

#### Words for Timing and Failure

A few vocabulary words keep the difficulty honest. An asynchronous system is one in which messages can be delayed for an unknown amount of time. There is no dependable global clock that says, "if nothing arrived by now, nothing was sent." A crash fault is a plain failure-stop: an agent may halt and send no more messages. A Byzantine fault is more devious: an agent may lie, send inconsistent messages, corrupt state, or behave in any arbitrary way. The Byzantine courtier is not merely sleepy; he may be composing different letters to different generals.

#### Safety, Liveness, and Agreement

Correctness criteria name the properties we want from this composed machine. Safety says that forbidden configurations are unreachable. Liveness says that required progress eventually occurs. Agreement, when the task requires it, says that the relevant local states converge:
\[
x_i^T=x_j^T\quad\forall i,j.
\]
Read this as "at the final step T, every pair of agents i and j holds the same state"; the upside-down A means "for all". A builder checks safety with invariant assertions on state, liveness with timeouts on progress, and agreement by diffing the agents' final records.

#### A Two-Agent Trace Where Slow and Dead Look Alike

Before naming the famous impossibility theorem, consider a two-agent trace. Agent \(A\) proposes value \(1\); agent \(B\) proposes value \(0\); each waits for the other's message before deciding. The following trace lists, step by step, what each agent sends and what each agent still does not know.

```text
t=0    A sends propose(1) to B
t=1    B sends propose(0) to A
t=2    A receives nothing yet; the channel may be slow, or B may have crashed
t=3    B receives propose(1); B cannot tell whether A will receive propose(0)
t=4    A still receives nothing; deciding now risks disagreement, waiting risks no liveness
```

The trouble is epistemic, not theatrical: it is about knowledge, not drama. From \(A\)'s local view at \(t=4\), "B is slow" and "B has crashed" can look identical. If \(A\) must always decide eventually and must never disagree with \(B\), the protocol has to distinguish states that the local observations do not distinguish. That is the squeeze.

#### What FLP and Byzantine Agreement Actually Forbid

Consensus theory makes these words sharp. Byzantine agreement studies what can be guaranteed when some participants may lie or fail arbitrarily [[54](#ref-54)]. The FLP result, named for its authors Fischer, Lynch, and Paterson, shows that deterministic consensus cannot be guaranteed in a fully asynchronous system with even one crash fault [[55](#ref-55)].

FLP does not say consensus is universally impossible. It says that a particular bundle of assumptions cannot all be kept at once. Practical systems regain progress by relaxing something:

- add timeouts and partial synchrony,
- allow randomization,
- use failure detectors,
- accept probabilistic termination,
- constrain failures,
- or weaken the decision requirement.

These are not remote distributed-systems curiosities. They are warnings against designing agent collectives whose correctness silently assumes perfect timing, perfect honesty, and perfectly delivered messages.

#### Paying for Messages: Expected Utility and the Bellman View

Communication also has a price. A utility-aware protocol objective can be written
\[
\max_{\Pi}\ \mathbb{E}[U(\tau)]-\lambda\sum_t \|m_t\|,
\]
which reads "choose the protocol that maximizes the expected value of the whole run, minus a price \(\lambda\) times the total size of all messages sent". Here \(\tau\) is the trajectory, the full record of what happened.

Over long horizons, the protocol designer can view "ask another agent" as an action inside a Bellman recursion:
\[
V^\star(s)=\max_a\left\{R(s,a)-\lambda C_{\text{comm}}(a)+\gamma\sum_{s'}P(s'|s,a)V^\star(s')\right\}.
\]
Read \(V^\star(s)\) as "the best long-run value obtainable from state s". Inside the braces: immediate reward, minus the communication cost of the action, plus the discounted value of wherever you land next, where \(\gamma\) shrinks future value relative to present value.

A tiny worked number helps. Suppose asking a reviewer raises the chance of a correct chapter from 0.70 to 0.90, and a correct chapter is worth 10. The expected gain is \(0.20 \times 10 = 2\). If the message costs 0.5 in latency and tokens, the net is 1.5, so ask. If the same message only moved the chance from 0.88 to 0.90, the gain is 0.2 and the net is negative, so do not ask.

Expected utility gives the one-step decision rule, while dynamic programming makes the future cost of coordination explicit [[33](#ref-33)] [[34](#ref-34)] [[5](#ref-5)]. More messages are justified only when they improve the expected trace enough to pay for their latency, token cost, and confusion risk.

#### Dec-POMDPs: The Honest Formal Home

In the fully general case, this is a decentralized partially observable Markov decision process, abbreviated Dec-POMDP. "Partially observable" means each agent sees only clues about the state, not the state itself. Three properties define it: each agent has local observations and local actions, rewards depend on the joint trajectory, and no agent can condition on the complete state.

Dec-POMDP reasoning is the clean formal home for this problem. It is usually too expensive to solve exactly, but it gives the right questions: what must be communicated, what can remain local, and which shared artifacts make the hidden state sufficiently inferable? Topic 2 (Negotiation and Mechanism Design) takes up the case where the agents also have conflicting preferences about the answer.

### Speech Acts and Commitments

#### A Small Grammar of Typed Messages

Coordination theory studies dependencies among tasks, resources, and actors; communication is useful when it manages one of those dependencies [[56](#ref-56)]. In agent systems, the most useful messages are therefore not free-form paragraphs but typed acts, meaning messages with a declared kind. A small grammar might include
\[
\{\texttt{observe},\texttt{propose},\texttt{critique},\texttt{vote},\texttt{decide},\texttt{commit},\texttt{handoff}\}.
\]
This set is read as the seven allowed message kinds: report something seen, offer something, object to something, register a preference, settle the matter, take on an obligation, and pass work to someone else.

The grammar is not bureaucratic decoration. It tells each receiving interpreter how the message may update state:

- A proposal creates an option.
- A critique attaches a defeater.
- A vote changes a quorum calculation.
- A commitment creates an obligation that can later be satisfied, expired, or escalated.

#### Defeaters, Quorums, and Role Guards

Here a defeater is a reason that blocks or weakens an earlier claim: "this citation does not support the sentence" defeats the proposal until repaired. A quorum is the minimum pattern of approvals required before an action counts as collectively authorized. It might be "two of three reviewers," "one security reviewer plus one maintainer," or "all severe critiques resolved."

Role guards make the grammar enforceable, by checking that the sender is allowed to send that kind of message:

- A researcher may propose evidence with citations.
- A reviewer may challenge assumptions.
- An integrator may decide only after quorum or timeout.

This is the difference between "agents discuss" and an actual institution. Role-based multi-agent accounts supply the vocabulary for designing such organizations as systems of authorized actions, responsibilities, and interaction protocols [[17](#ref-17)] [[18](#ref-18)].

#### Commitments, Logging Ratio, and Deadlock

Commitments deserve special treatment because they are where speech touches the environment. A commitment should record four things: who owns the next action, what condition completes it, what deadline applies, and what recovery rule fires on failure.

Message observability should be measured:
\[
\rho_{\text{log}}=\frac{\text{logged messages}}{\text{sent messages}}.
\]
Read \(\rho_{\text{log}}\) as "the fraction of sent messages that were written down". If 90 of 100 messages are logged, \(\rho_{\text{log}}=0.9\), and one message in ten is invisible to any later review. If an auditor cannot reconstruct why the collective converged, deadlocked, or stampeded, the protocol has hidden part of its semantics.

A deadlock is a state where every agent is waiting for some other event before it can move. The drafter waits for review, the reviewer waits for a revised patch, and the integrator waits for both, while no transition remains enabled.

### A Shared Publication Environment

#### Three Roles, Three Local Environments

Consider three agents editing a publication chapter: a drafter, a fact checker, and an integrator. If all three simply write into the same file, the shared environment becomes a race condition, where the result depends on who happens to write last. A minimal protocol is better:

1. The drafter may emit \(\texttt{propose(section, patch, rationale)}\).
2. The fact checker may emit \(\texttt{critique(claim, source, severity)}\) or \(\texttt{approve(claim)}\).
3. The integrator may emit \(\texttt{commit(patch)}\) only after all severe critiques are resolved or a timeout rule is invoked.

Each role is an interpreter over a different local environment:

- The drafter sees the outline, current prose, and unresolved writing tasks.
- The fact checker sees retrieval results, source quality notes, and claims extracted from the draft.
- The integrator sees the patch queue, role permissions, open critiques, and release criteria.

#### The Document as Heap, the Log as Continuation

The shared document is the heap they mutate: the common store of durable objects, just as a programming-language heap holds values that outlive one stack frame. The audit log is the continuation that lets another process resume the computation. A continuation records "what remains to be done next" after the current interpreter yields, crashes, or hands off control.

#### Reading a Transition Trace

A compact transition trace makes the semantics visible. The trace starts from a state with draft revision 17, an empty patch queue, and no critiques. It then follows one patch, P1, through proposal, a major critique, a block, a revision, an approval, and finally a commit that advances the revision to 18.

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

This protocol does not make the agents wise. It makes their interaction inspectable. Missing approvals, contradictory commitments, role violations, and stalled dependencies become states the system can detect rather than moods the transcript happens to reveal. It also makes silence meaningful. If the fact checker has not observed the revised citation, the integrator should not interpret absence of critique as approval unless the timeout rule says so.

#### When Coordination Is Worth Its Cost

The value of this coordination depends on the task. Tightly coupled work, where one agent's patch changes another agent's evidence, needs more communication than decomposable work whose pieces can be checked independently. Poor observability makes messages more valuable, because local state must be surfaced. Long communication delay makes messages more expensive, because the shared world may have moved before they arrive.

The publication workflow sits in the middle. Sections can be drafted separately, but claims, citations, tone, and release status couple them again. Topic 4 (Neural Ensembles and Orchestration) asks the related question of when extra participants improve an answer at all.

#### Tests That Tell You It Is a Protocol

The practical tests follow from the semantics. Measure each of these on real runs:

- message complexity,
- consensus latency,
- deadlock rate,
- role-violation rate,
- recovery time after dropped messages,
- stale-belief rate,
- artifact divergence,
- partial progress under blocked dependencies,
- and degradation under corrupted or adversarial messages.

Run that last test deliberately, by injecting a lying agent, rather than waiting for one to appear. A coordination scheme that works only because every participant is reasonable is not yet a protocol. It is a cooperative anecdote. Topic 3 (Equilibria, Self-Play, and Learning Dynamics) studies what happens when the participants adapt to each other over many such runs.


## Negotiation and Mechanism Design

Coordination assumes that agents must fit their actions together. Negotiation adds a sharper difficulty: the agents may not value the same outcomes. This section is about writing the rules of the game itself, so that agents find it more attractive to reveal useful information than to generate strategic noise. Once many interpreters share one environment with scarce resources, private information, and local objectives, somebody has to design that rulebook. That designer is you.

### One Edit Slot, Two Eager Agents

Start with a toy scarcity problem.

There is one edit slot before release. Agent \(D\), the drafter, privately knows that using the slot for a conceptual rewrite is worth \(8\) units to final quality and costs \(3\) units of effort. Agent \(F\), the fact checker, privately knows that using the slot for citation repair is worth \(6\) units and costs \(1\). Nobody else can see those numbers.

Four words carry the rest of this section:

- A **type** is the private fact an agent holds about its own value and cost. \(D\)'s type is the pair \(8\) and \(3\).
- A **report** is what the agent tells the mechanism, such as "my edit is worth \(8\) and costs \(3\)." A report may be a lie.
- An **allocation** is the outcome the mechanism chooses: give the slot to \(D\), give it to \(F\), or use no slot at all.
- A **transfer** is a payoff adjustment the mechanism imposes. In an auction it is money. In agent workflows it is often priority, reputation, review burden, future budget, or blame.

The arithmetic already bites. \(D\) nets \(8-3=5\); \(F\) nets \(6-1=5\). The two candidate edits are worth the same once effort is priced, so the tiebreak has to come from the announced rule rather than from whoever reports most loudly.

### What the Designer Wants: Truthfulness, Fair Entry, and Efficiency

Three desiderata (the properties a designer asks a rulebook to have) can be read directly off that example.

**Incentive compatibility** means truthful reporting should be the best policy. \(D\) should not gain by pretending the rewrite is worth \(30\).

**Individual rationality** means an honest participant should not be made worse off by joining. \(F\) should not be assigned unrewarded work whose effort cost exceeds its expected benefit.

**Efficiency** means the chosen allocation should maximize total value net of relevant costs. The slot should go where it improves the shared artifact most, not where the loudest report points.

To check these as a builder, run the rule against fabricated reports. Feed it an inflated claim, then ask whether the inflating agent ended up better off. If it did, the rule is not incentive compatible, whatever the design document says. With these words in hand, the notation is less imperial.

### Private Information Is Part of the Environment

The shared-environment view from Topic 1 (Coordination Protocols and Communication) matters here, because private information is not abstract decoration. It is the part of the environment bound only inside one interpreter.

A drafter knows how hard a rewrite will be. A fact checker knows which claims produced thin evidence. An integrator knows the release deadline and the cost of reopening a committed section. None of that is visible from outside.

Mechanism design asks how to build an outer evaluator whose rules make those private bindings show up in useful, checkable form.

### The Mechanism Tuple, Read Aloud

The mechanism tuple leans on eight pieces of notation, so here is a reading guide.

| Symbol | Read aloud as | Meaning |
|---|---|---|
| \(N\) | "the agent set N" | Who participates in the mechanism |
| \(\Theta\) | "big theta" | The type spaces, that is, all private facts agents could hold |
| \(\theta_i\) | "theta sub i" | Agent \(i\)'s true type |
| \(\hat\theta_i\) | "theta hat sub i" | Agent \(i\)'s reported type, truthful or not |
| \(\hat\theta_{-i}\) | "theta hat minus i" | The reports of every agent except \(i\) |
| \(A\) | "the outcome space A" | Every allocation the mechanism could choose |
| \(g\) | "the allocation rule g" | The function from reports to an outcome |
| \(p\) | "the transfer rule p" | The function from reports to payments |

A mechanism is
\[
\mathcal{M}=(N,\Theta, A, g, p),
\]
with agents \(N\), type spaces \(\Theta\), outcome space \(A\), allocation rule \(g\), and transfers \(p\). A type \(\theta_i\) represents what agent \(i\) privately knows: cost, preference, skill, urgency, risk, or capacity. The mechanism asks for reports \(\hat\theta_i\), chooses an outcome \(g(\hat\theta)\), and applies transfers \(p(\hat\theta)\).

The designer usually wants some combination of incentive compatibility, individual rationality, budget feasibility, fairness, and efficiency. Choosing a mechanism means choosing which of those five to trade away.

### Writing Truthfulness as an Inequality

Truthfulness can be stated as an inequality rather than a hope. In the inequality that states it, \(u_i(\cdot;\theta_i)\) is evaluated using agent \(i\)'s true type, even when the report is false; \(\hat\theta_{-i}\) denotes the other agents' reports.

Dominant-strategy truthfulness requires that honest reporting be best for each agent regardless of the others' reports:
\[
u_i\!\big(g(\theta_i,\hat\theta_{-i}),p_i(\theta_i,\hat\theta_{-i});\theta_i\big)
\ge
u_i\!\big(g(\theta'_i,\hat\theta_{-i}),p_i(\theta'_i,\hat\theta_{-i});\theta_i\big).
\]
Read the left side as "what agent \(i\) really gets when it tells the truth." Read the right side as "what it really gets from any lie \(\theta'_i\)." The word *dominant* is the strong part: the inequality must hold for every possible behaviour of the other agents, not merely on average.

### Efficient Allocation and the Vickrey-Clarke-Groves Transfer

Efficient allocation seeks
\[
g(\hat\theta)\in\arg\max_{a\in A}\sum_i v_i(a,\hat\theta_i).
\]
That reads: "pick the outcome \(a\) whose total reported value, summed over all agents, is largest."

Vickrey, Clarke, and Groves mechanisms show one classic way to align reported local valuations with a welfare-maximizing allocation [[57](#ref-57)] [[58](#ref-58)] [[59](#ref-59)]. One canonical transfer form is
\[
p_i(\hat\theta)=h_i(\hat\theta_{-i})-\sum_{j\ne i}v_j(g(\hat\theta),\hat\theta_j),
\]
which charges each participant for the externality it imposes on the rest of the system. An externality here is the value other agents lose because this agent won.

Put the edit slot through it. Suppose the tie breaks toward \(D\), and let \(h_i\) be the value the others would have enjoyed if \(D\) had never shown up, which is \(F\)'s net \(5\). With \(D\) winning, the others actually receive \(0\). So \(D\) pays \(5-0=5\): exactly the value it displaced. Because the two edits tie at \(5\), \(D\)'s surplus here is exactly zero; raise \(D\)'s value to \(6\) and the winner keeps \(1\).

The sign convention here is that \(p_i\) is a payment made by agent \(i\) to the mechanism, so larger \(p_i\) lowers utility when utility is written as value minus payment. Some texts use the opposite convention, treating transfers as money received; the algebra changes sign, not substance.

### Payments That Are Not Money

The point is not that every agent workflow should implement VCG payments, where VCG abbreviates Vickrey-Clarke-Groves. The point is that a rule changes behavior by changing payoffs.

In software, "payment" may be money, but it may also be priority, budget, reputation, access to tools, future routing probability, review burden, or blame assignment. A reviewer rewarded only for finding flaws will learn a different policy from a reviewer rewarded for improving final decision quality. Both reviewers are rational; they were simply paid for different things.

### Scarcity Inside Agent Societies

Multi-agent systems allocate scarce things constantly: model calls, tool permissions, human attention, wall-clock time, memory, authority to commit a patch, or the right to answer a user.

A contract-net protocol makes this operational: a manager announces a task, agents bid, the manager awards the contract, and the selected agent executes [[62](#ref-62)]. The protocol is simple, but its quality depends on the scoring rule. If every specialist gains by saying "I can do it," bids become optimism. If bids are scored by calibrated confidence, task completion, latency, and downstream correction cost, specialists have a path to reveal competence honestly.

### Allocating the Edit Slot by an Announced Rule

Return to the publication workflow. The integrator has one edit slot before release. The drafter wants the slot for a conceptual rewrite; the fact checker wants it for citation repair. Both requests are locally rational, and both are based on observations the integrator cannot directly inspect.

A mechanism can ask each agent to report a tuple such as \((\text{impact},\text{risk},\text{effort},\text{evidence})\), then allocate the slot by a rule announced in advance. Announcing the rule first is what makes it a mechanism rather than a mood.

The evidence field is a shared artifact: it turns a private belief into an object the other interpreters can test. The effort and risk fields remain partly private, so the rule must make systematic exaggeration expensive through later scoring.

### The Impossibility Results That Keep Us Honest

Social-choice theory, the study of how group preferences turn into group decisions, marks the limits of this ambition. Gibbard-Satterthwaite style impossibility results show that broad classes of voting systems are manipulable once preferences are unrestricted and there are at least three outcomes [[60](#ref-60)] [[61](#ref-61)].

This does not make mechanism design futile. It prevents magical thinking. The designer must know which assumptions buy strategy-proofness, which constraints are being relaxed, and where manipulation will be measured rather than wished away.

### Choosing Mechanisms over Time

In repeated settings, mechanism choice itself becomes sequential control:
\[
V^\star(s)=\max_m\left\{R(s,m)-\lambda\,\mathrm{manip\_risk}(m)+\gamma\,\mathbb{E}[V^\star(s')]\right\}.
\]
Read this as: the long-run value of state \(s\) comes from choosing the mechanism \(m\) with the best immediate reward \(R(s,m)\), minus a penalty \(\lambda\) times its manipulation risk. To that total you add the discounted expected value \(\gamma\,\mathbb{E}[V^\star(s')]\) of wherever the system lands next.

Expected utility supplies the local comparison among mechanisms, and dynamic programming expresses the long-run cost of creating exploitable incentives [[33](#ref-33)] [[34](#ref-34)] [[5](#ref-5)]. An institution learns when it changes the rules after observing how strategic behavior exploits the old ones. Topic 3 (Equilibria, Self-Play, and Learning Dynamics) studies what that adaptation converges to.

### Delegation in the Publication Workflow

Suppose the integrator must assign the next revision task to the drafter, fact checker, or a synthesis pass. Each agent reports a cost \(c_i\), confidence \(q_i\), expected latency \(\ell_i\), and the artifact it can produce.

A naive router asks, "Who wants this?" A mechanism-aware router scores
\[
s_i = \alpha q_i-\beta c_i-\delta \ell_i-\eta\,\mathrm{correction\_rate}_i
\]
and later updates each agent's reputation from verified outcomes. The Greek letters \(\alpha\), \(\beta\), \(\delta\), and \(\eta\) are weights the designer picks; they say how much confidence, cost, latency, and past corrections each count. With all four weights set to \(1\), an agent reporting \(q_i=0.9\), \(c_i=0.2\), \(\ell_i=0.3\), and a correction rate of \(0.1\) scores \(0.9-0.2-0.3-0.1=0.3\).

This reputation router is an accountability heuristic, not a theorem of truthfulness wearing a small hat. It becomes mechanism-like only under three conditions:

1. Reports are later checked against outcomes.
2. Agents expect repeated interaction, so today's exaggeration has a tomorrow.
3. The update rule makes misreporting costly enough to matter.

Without verification, a reputation score can become a decoration on self-advertisement. The reports are still imperfect, but miscalibration has a cost. Confidence becomes an accountable forecast rather than a persuasive adjective. Topic 4 (Neural Ensembles and Orchestration) takes up routing among specialists in more depth.

### Shaping Which Observations Become Public

The same structure handles communication limits. If the fact checker has only enough budget to verify three claims, the mechanism should not ask for a global truth verdict. It should ask for a prioritized claim list and a confidence interval over the unchecked remainder.

In Dec-POMDP language, the mechanism is shaping which local observations become public signals. A Dec-POMDP is a decentralized partially observable Markov decision process, introduced in Topic 1 (Coordination Protocols and Communication): each agent sees only its own slice of the world. The mechanism cannot remove partial observability, but it can choose the artifacts that make later coordination less blind.

### When a Mechanism Is Not Worth Its Ceremony

Mechanisms are not useful merely because several agents are present. If tasks are plentiful, preferences aligned, information public, and no one has reason to misreport, a simple queue may be better than an auction in ceremonial robes.

Mechanisms earn their keep under scarcity, private information, or incentive conflict. The recurring cases are concrete: one edit slot, one reviewer with rare access, one release deadline, one agent that benefits from overstating confidence, or one budget that cannot fund every plausible specialist.

The task predicts the institution. Scarcity asks for allocation. Private information asks for elicitation, meaning rules that draw private facts into the open. Incentive conflict asks for rules that make useful behavior cheaper than strategic fog.

### Evaluating a Mechanism

The formal evaluation should therefore measure six things:

- allocative efficiency, or how close the chosen outcome comes to the best available total value;
- truthfulness regret, the extra payoff an agent could have won by lying;
- fairness across agents or users;
- budget balance, when transfers are literal money;
- sensitivity to collusion, when agents coordinate their reports;
- performance under strategic misreports, tested by deliberately feeding the rule dishonest inputs.

A negotiation protocol without incentive analysis is merely an argument with extra JSON. A useful mechanism arranges the shared environment so that local pursuit of advantage produces information the collective can actually use.


## Equilibria, Self-Play, and Learning Dynamics

Agents that share an environment eventually start learning from each other, and the system is never quite the same afterwards. Earlier topics designed the rules: Topic 1 (Coordination Protocols and Communication) decided who may speak, and Topic 2 (Negotiation and Mechanism Design) decided how scarce authority is handed out. The question now is whether those rules still hold once every participant has watched them operate and looked for a better move. The tools are game theory, multi-agent reinforcement learning, and self-play, all used as testing equipment rather than as decoration.

A multi-agent design is not fully described by its first successful trace. Once many interpreters share an environment, each agent can adapt to the others. The stable question is therefore not only "what did they do?" but "who could improve by doing something else after observing the rule?"

### The Protocol Trains the Agents That Run It

The same shared environment that made coordination possible now becomes the object of learning. Each interpreter updates two kinds of belief. It updates its belief about the task, and it updates its belief about the other interpreters.

That second kind of learning is easy to miss. In the publication workflow, it shows up in specific habits:

- The drafter learns which critiques block commits.
- The fact checker learns which warnings the integrator treats as decisive.
- The integrator learns which agents are calibrated, slow, strategic, or redundant.

Here "calibrated" means an agent whose stated confidence matches how often it turns out to be right. The consequence is uncomfortable and useful. The protocol is therefore a program that trains the agents who run it.

### Strategic Stability: When Nobody Wants to Deviate

#### Reading a Payoff Table

The smallest strategic object is a normal-form game. That is a table listing each player's available actions and the payoff each player receives for every joint action. A payoff is just a number saying how good an outcome is for that player. There is no time axis inside the table; it is a snapshot of simultaneous choice.

A mixed strategy is a probability distribution over actions. In plain terms, the agent flips a weighted coin instead of always doing the same thing. For example, a reviewer might challenge a patch \(70\%\) of the time and approve it \(30\%\) of the time under the same visible signal.

The following table shows one such snapshot. A drafter chooses whether to submit a careful patch or a rushed patch. A checker chooses whether to inspect or skim. Each cell holds two numbers, written as \((\text{drafter},\text{checker})\): the drafter's payoff first, the checker's payoff second.

| drafter's choice | checker inspects | checker skims |
|---|---:|---:|
| drafter careful | \((3,2)\) | \((2,1)\) |
| drafter rushed | \((0,3)\) | \((4,-2)\) |

Read the corners to see the tension. When the drafter rushes and the checker skims, the drafter collects \(4\), the highest single payoff in the table, while the checker collects \(-2\). The rushed-and-skimmed cell is tempting for the drafter and bad for the collective. When the checker inspects, rushing pays the drafter \(0\) instead of \(4\), so the inspect column makes rushing less attractive. Equilibrium analysis asks which pattern survives once both roles understand this table, not which pattern looked noble in the first rehearsal.

#### The Nash Condition, Stated and Read Aloud

Take a normal-form game \((N,\{A_i\},\{u_i\})\), read as "the set of players N, each player's action set A-sub-i, and each player's payoff function u-sub-i". A mixed strategy profile \(\sigma^{*}\), where \(\sigma\) now names a strategy rather than the machine state it named in Chapter 2, is Nash if no agent can improve by changing its own strategy while the others hold fixed:
\[
u_i(\sigma_i^{*},\sigma_{-i}^{*}) \ge u_i(\sigma_i,\sigma_{-i}^{*})\quad \forall i,\forall \sigma_i.
\]
Read \(\sigma_i\) as "the strategy of agent i" and \(\sigma_{-i}\) as "the strategies of everyone except agent i". The symbol \(\forall\) reads "for all". So the line says: for every agent, and for every alternative strategy that agent might try, switching alone does not raise its payoff. Nash's fixed-point result gives the central existence theorem for this kind of unilateral stability [[19](#ref-19)].

The concept matters for agent systems because a protocol that works only before participants learn its incentives is not stable. Suppose a reviewer can gain influence by exaggerating severity. Suppose a worker can gain routing weight by overclaiming competence. In both cases the first demonstration has not tested the game the system will become.

#### What Stability Looks Like in the Publication Workflow

In the publication workflow, a stable convention is not merely "the chapter was finished once." It is closer to this. After many chapters, three things hold at the same time:

1. The drafter does not gain by bypassing review.
2. The fact checker does not gain by marking every uncertainty as severe.
3. The integrator does not gain by rubber-stamping patches to reduce queue length.

Each role has a policy, meaning a rule for choosing actions, defined over what it can locally see. Those local observations include draft gaps, source quality, open critiques, time remaining, and the visible behavior of the others. Equilibrium asks whether those policies remain reasonable when the agents understand the incentives.

#### Exploitability as a Robustness Metric

A useful robustness metric is exploitability:
\[
\mathcal{E}(\sigma)=\sum_i\left(\max_{\sigma_i'}u_i(\sigma_i',\sigma_{-i})-u_i(\sigma)\right).
\]
Read this as: for each agent, find the best payoff it could reach by switching strategy alone, subtract what it currently gets, then add those gaps across all agents. A tiny example: if one agent could gain \(0.3\) by deviating and another could gain \(0.0\), exploitability is \(0.3\).

In two-player zero-sum settings, where one player's gain is exactly the other's loss, zero exploitability corresponds to exact equilibrium. In general-sum agent societies, where payoffs need not cancel out, exploitability is still a valuable probe. It asks how much an entrant or deviator can gain against the current convention. To measure it in practice, train or hand-build a deviating agent and see how much extra reward it collects. Low exploitability is not the same as moral goodness, but it is evidence that the behavior is not merely held together by inattention.

### Learning While Interacting: Games That Have a State

#### Markov Games Extend the Control Loop

Sequential interaction is better modeled as a Markov game. There is a shared state, each agent chooses an action, and each receives its own reward. For player \(i\) under joint policy profile \(\pi\),
\[
V_i^\pi(s)=\mathbb{E}_{a\sim \pi}\!\left[r_i(s,a)+\gamma\sum_{s'}P(s'|s,a)V_i^\pi(s')\right].
\]
Read \(V_i^\pi(s)\) as "the long-run value of state s for agent i when everyone follows the policy profile pi". Inside the brackets, \(r_i(s,a)\) is agent i's immediate reward for the joint action \(a\), \(\gamma\) is the discount factor that shrinks future value, and \(P(s'|s,a)\) is the chance of landing in next state \(s'\). Markov games extend the Bellman view of control to settings where the transition and reward consequences depend on several policies at once [[20](#ref-20)] [[5](#ref-5)]. Equilibrium planning therefore replaces unilateral maximization with best-response consistency: each policy must make sense against the others, not against an inert environment.

#### Nobody Can See the Real State

Partial observability changes the interpretation of \(s\). No single role in the publication workflow sees the true state "chapter quality." Each sees a different slice:

- The drafter observes prose difficulty.
- The checker observes evidence strength.
- The integrator observes queue pressure and visible approvals.

A Dec-POMDP version, short for decentralized partially observable Markov decision process, would model each local observation stream explicitly. It then searches for joint policies that use messages and artifacts to coordinate under hidden quality. Exact solutions are rarely practical for rich language work. Still, the model prevents a common mistake: treating the final document as if it were the agents' shared state all along.

#### Self-Play Manufactures Pressure

Self-play is one way to create such pressure. Systems like AlphaGo used repeated play and search to improve policies against increasingly strong opponents [[21](#ref-21)]. The lesson for agentic workflows is broader than games. Run agents against copies, variants, adversaries, lazy collaborators, overconfident specialists, and strategically silent reviewers.

Two failure shapes follow directly. A debate protocol that converges with honest critics may fail when critics optimize for attention. A negotiation agent that succeeds against polite counterparts may simply have learned politeness as an environmental assumption.

#### A Three-Round Regret Calculation

Before the regret formula, make the accounting painfully small. A router chooses one specialist each round: \(G\), a generalist, or \(S\), a security specialist. Payoff is \(1\) for a good route and \(0\) for a bad one. These three rounds list the task type, the router's choice, what each specialist would have earned, and what the router actually received.

```text
round  task type     router chose   payoff if G   payoff if S   received
1      prose         G              1             0             1
2      security      G              0             1             0
3      security      S              0             1             1
```

The router received \(2\) total. The best fixed action in hindsight is \(S\), also worth \(2\) on these three tasks; always choosing \(G\) would have been worth \(1\). External regret asks how much the router lost compared with the best single fixed action chosen after seeing the whole sequence. Here that difference is \(2 - 2 = 0\). That is a useful question, but it is not the only useful question.

#### External Regret, Swap Regret, and Why the Difference Bites

Repeated adaptation is governed by regret:
\[
R_T^i=\max_a\sum_{t=1}^T u_i(a,a_{-i}^t)-\sum_{t=1}^T u_i(a_i^t,a_{-i}^t).
\]
Read \(R_T^i\) as "agent i's regret after T rounds": the best total payoff from one fixed action, minus the total the agent actually collected.

Two related names describe where such learning settles. In a **correlated equilibrium**, a shared signal recommends an action to each agent, and no agent gains by reinterpreting its own recommendation. A **coarse correlated equilibrium** is the weaker version: no agent gains by ignoring the signal entirely and committing to one fixed action instead.

External no-regret learning drives empirical play toward coarse correlated equilibrium sets. Correlated equilibrium requires stronger internal or swap-regret guarantees. The reason is that the deviation is not merely "always play action \(a\)" but "replace action \(a\) by action \(a'\) whenever the recommendation says \(a\)" [[65](#ref-65)].

Swap regret asks a different question from the three-round routing example. It does not compare the router with "always \(G\)" or "always \(S\)." It compares the router with a rule for rewriting its own past recommendations: whenever the policy said \(G\) on a security-looking task, pretend it had said \(S\). Apply that swap to round 2 and the router's total rises from \(2\) to \(3\), so swap regret is positive even though external regret was zero.

This distinction is practical. A routing policy with low external regret may know that no single fixed specialist would have been better overall. It may still fail to learn that whenever it routes security incidents to a generalist, it should swap that decision to a security specialist.

#### Older Dynamics, Still Diagnostic

Classical learning dynamics add more diagnostic lenses. Fictitious play studies agents that best respond to empirical frequencies of past play, that is, to how often each opponent action has appeared so far [[63](#ref-63)]. Evolutionary game theory studies how populations of strategies grow, shrink, and stabilize under selection pressure [[64](#ref-64)]. Both remind us that adaptation can converge, cycle, fragment, or collapse into monoculture, where every agent runs the same brittle strategy.

#### Self-Play Built from Perturbations

Self-play for this workflow can be built from perturbations rather than board positions. Assemble a cast of deliberately imperfect participants:

- a drafter that sometimes overstates novelty,
- a checker that sometimes misses unsupported claims,
- an integrator under a tight deadline,
- adversarial variants that exploit the scoring rule.

Then replay the same chapter under altered budgets and message delays. If the learned convention depends on immediate critique delivery, or on a fact checker who always shares every search failure, the apparent equilibrium was partly an artifact of unrealistic observability.

### Dynamics as Tests: Metrics, Perturbations, and Repairs

#### Four Quantities Worth Tracking

For builders, equilibrium analysis becomes a test discipline. Track four things:

- Exploitability: how easy is it for a new strategy to take advantage of the current protocol?
- Regret: would an agent have done better by consistently choosing a different role, message, or action?
- Diversity collapse: are all agents learning the same brittle convention?
- Hidden-quality regret, specific to the publication workflow: how often did local signals make a weak section look ready until after commit?

Then perturb payoffs, latencies, available tools, and adversary behavior, and see whether cooperation survives.

#### Composition Becomes an Experiment

This is where composition stops being a slogan and becomes an experiment. A planner plus reviewer may improve quality when the reviewer has independent evidence. The same pair may create delay without insight when both inherit the same stale premise.

A negotiation rule plus reputation memory may elicit better reports; it may also teach agents which numbers to flatter. Self-play may discover robust conventions; it may also discover collusion, correlated behavior, or an incentive loophole that was invisible in isolated component scores. Topic 4 (Neural Ensembles and Orchestration) picks up that correlation problem from the side of aggregation.

Adaptation changes the task faced by every other interpreter. The question is not whether each component scored well alone, but whether the joint system remains useful after its components learn one another.

#### Institutional Repairs, Not Better Speeches

When dynamics cycle, the repair is usually institutional rather than rhetorical. Add commitment rules, arbitration, memory, randomized tie-breaking, penalties for reversal, or a different mechanism. When collusion appears, change observability and rewards. When diversity collapses, preserve independent training data, model families, prompts, or evaluation routes.

The aim is not perfect harmony, which can hide suppression of useful disagreement. The aim is low exploitability, bounded regret, recoverable diversity, and stable cooperation under pressure.

Exercise: take the drafter and fact checker only. Define each action set, payoff proxy, local observation, and one possible deviation. What observation would tell you that the current review rule is an equilibrium-like convention rather than a fragile habit? A good answer names a measurable signal, such as a deviating drafter that skips review and gains nothing across many chapters, rather than a single successful run.


## Neural Ensembles and Orchestration

Sometimes several flawed workers, combined, beat the best worker alone. Sometimes they simply repeat one mistake in unison, only louder. This section is about telling those two cases apart, and about the machinery that sends each task to the right specialist. Two words will do most of the work: an *ensemble* is a group of predictors whose separate answers are combined into one, and *orchestration* narrows here to the routing part of the discipline the preface defined, namely the logic that decides who is consulted at all.

An ensemble is useful when several imperfect interpreters make different errors. The central question is not how many voices the system can summon. It is whether their diversity reduces the error that matters, under the budget that actually exists.

In Chapter 4's recurring publication workflow, the ensemble is not just a bag of answers. It is a set of interpreters bound to different parts of the environment:

- the drafter is bound to exposition and structure;
- the fact checker is bound to claims and sources;
- the integrator is bound to release constraints and consistency.

Orchestration then decides three things: which interpreter receives which expression, which environment bindings (the names and values it is allowed to see) it may read, and which side effects it may perform. Those three decisions are the whole design surface.

### Aggregating Imperfect Predictors

Start with the simplest combination rule: take a weighted average of what each expert says. Given predictors \(f_k(x)\), a weighted ensemble produces
\[
\hat{y}(x)=\sum_{k=1}^{K} w_k(x)\,f_k(x),\qquad \sum_k w_k(x)=1,\ w_k(x)\ge 0.
\]
Read \(f_k(x)\) as "the answer that expert number \(k\) gives for input \(x\)", and \(w_k(x)\) as "how much we trust expert \(k\) on this particular input". The weights are non-negative and sum to one, so the result \(\hat{y}(x)\) ("y-hat of x", the ensemble's prediction) stays on the same scale as the individual answers. For voting systems, \(\hat{y}=\operatorname{mode}\{f_k(x)\}\), which reads "take whichever answer was given most often".

The gain comes from competent diversity. If predictors make independent or weakly correlated errors, aggregation can improve accuracy and uncertainty estimates. If they share the same blind spot, the ensemble may only make the mistake more confidently.

#### Why Three Independent Reviewers Beat One

Suppose three reviewers each have \(80\%\) accuracy and make independent errors on a binary decision. Majority vote is wrong only when at least two are wrong:
\[
{3\choose 2}(0.2)^2(0.8)+(0.2)^3=0.104.
\]
The first term counts the three ways that exactly two reviewers err while one is right. The second term is the single case where all three err. Their sum is \(0.104\), so independent majority voting raises accuracy from \(80\%\) to \(89.6\%\). Nearly ten points of accuracy for the price of two extra calls is a real bargain.

#### Why Correlated Errors Erase That Bargain

Now suppose all three reviewers use the same flawed source extraction step, so their errors are perfectly correlated. When one is wrong, all are wrong, and the majority is still wrong \(20\%\) of the time. Three voices have produced one error with a choir robe.

The lesson for a builder is procedural, not philosophical: before adding a reviewer, ask what would have to differ for its mistakes to differ. Deep ensembles are valuable partly because independently trained predictors can improve calibration and predictive uncertainty [[26](#ref-26)]. Calibration means that stated confidence matches observed accuracy, so claims made with \(90\%\) confidence turn out right about nine times in ten. Classical ensemble methods make the same theme explicit: diversity matters only when the individual models remain useful [[67](#ref-67)]. A committee of confident incompetents averages to nothing.

#### Routing with Mixtures of Experts

Mixture-of-experts (MoE) systems add conditional computation, meaning the system spends compute only where it expects a return. A router \(g(x)\) chooses which experts to activate for an input, rather than paying for every expert every time. Confidence-weighted routing can use softmax gates
\[
w_k(x)=\frac{\exp(g_k(x)/\tau)}{\sum_j \exp(g_j(x)/\tau)},
\]
where \(g_k(x)\) is the router's raw score for expert \(k\), and the formula turns those scores into weights that sum to one. An alternative is sparse top-\(k\) routing,
\[
E(x)=\operatorname{TopK}(g(x),k),
\]
which selects a small set \(E(x)\) of experts to run.

The softmax temperature \(\tau\) ("tau") controls how sharp the routing distribution is. Small \(\tau\) makes the largest gate score dominate; large \(\tau\) spreads weight more evenly. Top-\(k\) routing means "activate only the \(k\) highest-scoring experts," such as the two best specialists out of sixteen, and give the rest no computation for this input.

To see whether a router is doing anything interesting, measure its spread. Routing entropy measures how spread out the router's choices are,
\[
H(w)=-\sum_k w_k\log w_k,
\]
so low entropy means the router almost always chooses the same expert, while high entropy means it distributes work broadly. Neither extreme is automatically healthy; the number is a diagnostic, not a target. Early adaptive mixtures of local experts introduced this divide-and-route pattern [[68](#ref-68)]. Sparsely gated MoE layers and Switch Transformers show how the same principle can scale neural computation by activating only a small subset of experts per input [[25](#ref-25)] [[69](#ref-69)].

### From Neural Experts to Agent Societies

It is tempting to treat a team of agents as an MoE layer wearing business clothes. The analogy between neural ensembles and multi-agent societies is useful but limited, and both halves of that sentence matter.

#### What the Analogy Gets Right

It is useful because both kinds of system depend on the same five concerns: specialization, routing, aggregation, calibration, and correlated-error control. A coding workflow may route architecture questions to a design reviewer, risky edits to a safety reviewer, failing tests to a debugger, and final synthesis to an integrator. A research workflow may combine retrieval, statistical critique, domain expertise, and writing. Surveys of multi-agent systems built from large language models describe many such patterns at the workflow level [[23](#ref-23)].

#### What the Analogy Gets Wrong

The analogy breaks when we forget that agents are not just differentiable submodules inside one loss function. A differentiable module is a component whose outputs change smoothly enough with respect to its parameters that gradient descent can assign credit through it. Neural experts usually share training infrastructure, optimization objectives, and a tightly specified interface.

Agent societies are messier. They may use tools, memory, permissions, natural language, human escalation, and changing local objectives. They can misunderstand instructions, strategically shape reports, duplicate hidden sources, or alter the environment while the router is still deciding. Minsky's "society of mind" is a suggestive metaphor for intelligence built from many smaller processes, not a license to treat every committee as a well-calibrated MoE layer [[27](#ref-27)].

#### What an Agentic Router Actually Hands Out

This distinction changes the orchestration problem. A neural router mostly selects computation. An agentic router selects computation plus authority, information exposure, side effects, latency, and incentive pressure. Choosing an agent is closer to signing a permission slip than to picking a matrix multiply.

The orchestration layer should therefore maintain expert profiles that record, for each participant:

- domain strengths and historical accuracy;
- calibration, latency, and cost;
- permissions and known failure modes;
- correlation with the other experts.

The aggregator should combine outputs by confidence, evidence, role, independence, and past reliability. The monitor should watch for collapse, which shows up in four recognizable ways: one expert always dominates, all experts cite the same weak source, critics converge into ceremony, or routing entropy falls because the system has learned convenience rather than competence.

#### The Router Is Another Partial Observer

The router itself is another partial observer. It sees task metadata, past scores, queue length, and visible artifacts. It may not see the drafter's uncertainty, the fact checker's failed searches, or a subtle inconsistency until someone emits the right message.

Good orchestration therefore exposes structured summaries, claim inventories, confidence reports, and provenance trails. These artifacts are not paperwork. They are the shared environment that lets separately specialized interpreters approximate a joint belief.

### Budgeted Orchestration

Deciding whom to consult next, given what you have already learned, is a sequential decision problem. Specialist dispatch can be written as one:
\[
V^\star(s)=\max_a\left\{R(s,a)-\lambda_c C(a)-\lambda_l L(a)+\gamma\,\mathbb{E}[V^\star(s')]\right\},
\]
where \(a\) chooses which experts or agents to consult, \(C\) is monetary or compute cost, and \(L\) is latency. The equation packs a great deal into one line, so every symbol in it is given a plain reading in the table below.

| Symbol | How to read it |
|---|---|
| \(V^\star(s)\) | the best long-run value obtainable from orchestration state \(s\) |
| \(a\) | the action of consulting a particular set of experts |
| \(R(s,a)\) | the immediate benefit of that consultation |
| \(C(a)\) | its money or compute cost |
| \(L(a)\) | its latency, in wall-clock delay |
| \(\lambda_c,\lambda_l\) | prices that convert cost and delay into the same units as benefit |
| \(\gamma\,\mathbb{E}[V^\star(s')]\) | the discounted expected value of the state \(s'\) you land in next |

A tiny instance: if consulting a second reviewer adds \(R=0.05\) of expected accuracy but costs \(\lambda_c C=0.03\) and \(\lambda_l L=0.04\) in priced delay, the call is worth \(-0.02\) and should not happen. Expected utility and dynamic programming give the formal discipline behind the obvious engineering rule: "call everyone" is not sophistication when the marginal expert mostly adds delay, contradiction, or correlated noise [[33](#ref-33)] [[34](#ref-34)] [[5](#ref-5)].

#### A Four-Step Orchestration Loop

A useful orchestration loop has four steps:

1. Estimate task features and uncertainty: domain, coupling, reversibility, freshness, evidence availability, permission class, and tolerance for delay.
2. Route to a small set of specialists whose errors are likely to be different.
3. Aggregate with calibration rather than rank or verbosity.
4. Update the profiles from verified outcomes.

In the publication workflow, those four steps might mean this:

- route a new section to the drafter,
- extract claims for the fact checker,
- route only unresolved conflicts to the integrator,
- store the final patch plus the evidence trail as training data for future routing.

The objective is not maximal committee size. It is minimal correlated error for a fixed budget.

#### When Uncertainty Is Spread Across Agents

Decentralized uncertainty is the hard case for ensembles. If the drafter and fact checker both inherit the same mistaken premise from the outline, their agreement should not be counted as independent evidence. If the fact checker cannot reveal a source because of access limits, the aggregator should distinguish three different verdicts: "verified false," "not verified," and "verified but not shareable." Collapsing them loses exactly the information a reviewer needs.

Reasoning about decentralized partially observable Markov decision processes (Dec-POMDPs), introduced in Topic 1 (Coordination Protocols and Communication), sits behind these engineering choices. Route actions are communication actions, artifacts are public observations, and expert calls are costly attempts to reduce uncertainty in the joint policy.

#### What to Report in an Evaluation

Evaluation should report a wide panel rather than a single score:

- ensemble lift over the best single expert;
- calibration under distribution shift;
- routing entropy and expert utilization balance;
- disagreement quality and stale-artifact rate;
- provenance diversity and correlated-error interactions;
- permission denials and stopping accuracy;
- cost-latency-normalized utility.

Distribution shift means the future inputs no longer come from the same pattern as the examples used to train, tune, or score the router. Yesterday's fact checks were biomedical citations, today's are legal claims, and the old confidence calibration may now be a charming historical artifact.

A successful agent society is not merely louder than its members. It is a routed ensemble whose disagreements contain information, whose redundancy buys fault tolerance, and whose final decision is better than the most confident participant acting alone.

### The Institution Is Still an Interpreter

The book's arc now folds back to the single interpreter. Chapter 1, Topic 4 (Policies, Value, and Control) gave us a loop that observes, updates, chooses, and acts. Chapter 4 has not replaced that loop with a parliament of mist. It has shown how to place many such loops in one environment and make their interaction explicit: protocols for messages, mechanisms for incentives, dynamics for adaptation, and ensembles for error reduction.

The institution is still an interpreter, but its registers are distributed across agents, artifacts, and logs. To build it well is to do five things at once:

- route by the task's real features;
- buy ensemble lift only when independence exists;
- watch for correlated errors and altered incentives;
- account for cost, latency, and permission;
- stop when another call would add ceremony rather than control.

The smallest sufficient institution for the task is the one whose collective computation remains legible enough that wisdom, when it appears, is not mistaken for accident.


# References {-}

1. []{#ref-1}Abelson, H., Sussman, G. J., & Sussman, J. (1996). *Structure and Interpretation of Computer Programs* (2nd ed.). MIT Press. <https://mitpress.mit.edu/9780262510875/>
2. []{#ref-2}Russell, S., & Norvig, P. (2021). *Artificial Intelligence: A Modern Approach* (4th ed.). Pearson. <https://aima.cs.berkeley.edu/>
3. []{#ref-3}Sutton, R. S., & Barto, A. G. (2018). *Reinforcement Learning: An Introduction* (2nd ed.). MIT Press. <http://incompleteideas.net/book/the-book-2nd.html>
4. []{#ref-4}Puterman, M. L. (1994). *Markov Decision Processes*. Wiley. <https://onlinelibrary.wiley.com/doi/book/10.1002/9780470316887>
5. []{#ref-5}Bellman, R. (1957). *Dynamic Programming*. Princeton University Press. <https://press.princeton.edu/books/hardcover/9780691651873/dynamic-programming>
6. []{#ref-6}Pearl, J. (2009). *Causality* (2nd ed.). Cambridge University Press. <https://www.cambridge.org/core/books/causality/94D5B8E8B2A5E0D970AA4A8DE3A2F5DD>
7. []{#ref-7}Kaelbling, L. P., Littman, M. L., & Cassandra, A. R. (1998). Planning and acting in partially observable stochastic domains. *AI*, 101(1-2), 99-134. <https://www.sciencedirect.com/science/article/pii/S000437029800023X>
8. []{#ref-8}Hart, P. E., Nilsson, N. J., & Raphael, B. (1968). A formal basis for A* search. *IEEE TSSC*, 4(2), 100-107. <https://ieeexplore.ieee.org/document/4082128>
9. []{#ref-9}Fikes, R. E., & Nilsson, N. J. (1971). STRIPS. *AI*, 2(3-4), 189-208. <https://www.sciencedirect.com/science/article/pii/0004370271900105>
10. []{#ref-10}Ghallab, M., Nau, D., & Traverso, P. (2004). *Automated Planning*. Elsevier. <https://shop.elsevier.com/books/automated-planning/ghallab/978-1-55860-856-6>
11. []{#ref-11}Yao, S., et al. (2022). ReAct: Synergizing reasoning and acting in language models. <https://arxiv.org/abs/2210.03629>
12. []{#ref-12}Schick, T., et al. (2023). Toolformer: Language models can teach themselves to use tools. <https://arxiv.org/abs/2302.04761>
13. []{#ref-13}OpenAI. Function calling guide. <https://platform.openai.com/docs/guides/function-calling>
14. []{#ref-14}Lewis, P., et al. (2020). Retrieval-augmented generation for knowledge-intensive NLP tasks. *NeurIPS 2020*. <https://arxiv.org/abs/2005.11401>
15. []{#ref-15}Karpukhin, V., et al. (2020). Dense passage retrieval. *EMNLP 2020*. <https://arxiv.org/abs/2004.04906>
16. []{#ref-16}Packer, C., et al. (2023). MemGPT: Towards LLMs as operating systems. <https://arxiv.org/abs/2310.08560>
17. []{#ref-17}Wooldridge, M. (2009). *An Introduction to MultiAgent Systems* (2nd ed.). Wiley. <https://www.wiley.com/en-us/An+Introduction+to+MultiAgent+Systems%2C+2nd+Edition-p-9780470519462>
18. []{#ref-18}Shoham, Y., & Leyton-Brown, K. (2009). *Multiagent Systems*. Cambridge University Press. <https://www.cs.ubc.ca/~kevinlb/MAS/>
19. []{#ref-19}Nash, J. (1950). Equilibrium points in n-person games. *PNAS*, 36(1), 48-49. <https://www.pnas.org/doi/10.1073/pnas.36.1.48>
20. []{#ref-20}Littman, M. L. (1994). Markov games as a framework for multi-agent RL. *ICML 1994*. <https://www.cs.rutgers.edu/~mlittman/papers/ml94-final.pdf>
21. []{#ref-21}Silver, D., et al. (2016). Mastering the game of Go with deep neural networks and tree search. *Nature*, 529, 484-489. <https://www.nature.com/articles/nature16961>
22. []{#ref-22}Oliehoek, F. A., & Amato, C. (2016). *A Concise Introduction to Dec-POMDPs*. Springer. <https://link.springer.com/book/10.1007/978-3-319-28929-8>
23. []{#ref-23}Cambria, E., et al. (2025). Survey of LLM-based multi-agent systems. <https://arxiv.org/abs/2402.01680>
24. []{#ref-24}Wu, Q., et al. (2023). AutoGen: Enabling next-gen LLM applications via multi-agent conversation. <https://arxiv.org/abs/2308.08155>
25. []{#ref-25}Shazeer, N., et al. (2017). Outrageously large neural networks: The sparsely-gated mixture-of-experts layer. <https://arxiv.org/abs/1701.06538>
26. []{#ref-26}Lakshminarayanan, B., Pritzel, A., & Blundell, C. (2017). Simple and scalable predictive uncertainty estimation using deep ensembles. *NeurIPS 2017*. <https://arxiv.org/abs/1612.01474>
27. []{#ref-27}Minsky, M. (1988). *The Society of Mind*. Simon & Schuster. <https://www.amazon.com/Society-Mind-Marvin-Minsky/dp/0671657135>
28. []{#ref-28}Kahneman, D. (2011). *Thinking, Fast and Slow*. Farrar, Straus and Giroux. <https://us.macmillan.com/books/9780374533557/thinkingfastandslow>
29. []{#ref-29}Anthropic. (2022). Constitutional AI. <https://arxiv.org/abs/2212.08073>
30. []{#ref-30}OpenAI. (2023). GPT-4 Technical Report. <https://arxiv.org/abs/2303.08774>
31. []{#ref-31}WeasyPrint documentation. <https://doc.courtbouillon.org/weasyprint/stable/>
32. []{#ref-32}GitHub Pages documentation. <https://docs.github.com/pages>
33. []{#ref-33}Von Neumann, J., & Morgenstern, O. (1944). *Theory of Games and Economic Behavior*. Princeton University Press. <https://press.princeton.edu/books/hardcover/9780691130613/theory-of-games-and-economic-behavior>
34. []{#ref-34}Savage, L. J. (1954). *The Foundations of Statistics*. Wiley. <https://archive.org/details/foundationsofsta00sava>
35. []{#ref-35}Shannon, C. E. (1948). A mathematical theory of communication. *Bell System Technical Journal*, 27, 379-423, 623-656. <https://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf>
36. []{#ref-36}Kalman, R. E. (1960). A new approach to linear filtering and prediction problems. *Journal of Basic Engineering*, 82(1), 35-45. <https://asmedigitalcollection.asme.org/fluidsengineering/article/82/1/35/397706/A-New-Approach-to-Linear-Filtering-and>
37. []{#ref-37}Li, L., Walsh, T. J., & Littman, M. L. (2006). Towards a unified theory of state abstraction for MDPs. *ISAIM 2006*. <https://www.cs.rutgers.edu/~mlittman/papers/abstraction-06.pdf>
38. []{#ref-38}Ferns, N., Panangaden, P., & Precup, D. (2004). Metrics for finite Markov decision processes. *UAI 2004*. <https://www.cs.mcgill.ca/~dprecup/publications/uai04.pdf>
39. []{#ref-39}Bertsekas, D. P. (2017). *Dynamic Programming and Optimal Control* (4th ed.). Athena Scientific. <https://www.mit.edu/~dimitrib/dpbook.html>
40. []{#ref-40}Sutton, R. S., McAllester, D., Singh, S., & Mansour, Y. (1999). Policy gradient methods for reinforcement learning with function approximation. *NeurIPS 1999*. <https://papers.nips.cc/paper/1713-policy-gradient-methods-for-reinforcement-learning-with-function-approximation.pdf>
41. []{#ref-41}Rawlings, J. B., Mayne, D. Q., & Diehl, M. M. (2017). *Model Predictive Control: Theory, Computation, and Design* (2nd ed.). Nob Hill. <https://sites.engineering.ucsb.edu/~jbraw/mpc/>
42. []{#ref-42}Plotkin, G. D. (1981). A structural approach to operational semantics. Aarhus University technical report DAIMI FN-19. <https://www.cs.tufts.edu/comp/150FP/archive/gordon-plotkin/sos.pdf>
43. []{#ref-43}Cousot, P., & Cousot, R. (1977). Abstract interpretation: A unified lattice model for static analysis. *POPL 1977*. <https://dl.acm.org/doi/10.1145/512950.512973>
44. []{#ref-44}Dean, T., & Boddy, M. (1988). An analysis of time-dependent planning. *AAAI 1988*. <https://cdn.aaai.org/AAAI/1988/AAAI88-003.pdf>
45. []{#ref-45}Kocsis, L., & Szepesvári, C. (2006). Bandit based Monte-Carlo planning. *ECML 2006*. <https://link.springer.com/chapter/10.1007/11871842_29>
46. []{#ref-46}Robertson, S., & Zaragoza, H. (2009). The probabilistic relevance framework: BM25 and beyond. *Foundations and Trends in IR*, 3(4), 333-389. <https://www.nowpublishers.com/article/Details/INR-019>
47. []{#ref-47}Malkov, Y. A., & Yashunin, D. A. (2018). Efficient and robust approximate nearest neighbor search using hierarchical navigable small world graphs. *IEEE TPAMI*, 42(4), 824-836. <https://arxiv.org/abs/1603.09320>
48. []{#ref-48}Atkinson, R. C., & Shiffrin, R. M. (1968). Human memory: A proposed system and its control processes. In *The Psychology of Learning and Motivation* (Vol. 2). <https://www.sciencedirect.com/science/article/pii/S0079742108604223>
49. []{#ref-49}Gneiting, T., & Raftery, A. E. (2007). Strictly proper scoring rules, prediction, and estimation. *JASA*, 102(477), 359-378. <https://sites.stat.washington.edu/raftery/Research/PDF/Gneiting2007jasa.pdf>
50. []{#ref-50}Koh, P. W., & Liang, P. (2017). Understanding black-box predictions via influence functions. *ICML 2017*. <https://arxiv.org/abs/1703.04730>
51. []{#ref-51}Altman, E. (1999). *Constrained Markov Decision Processes*. Chapman and Hall/CRC. <https://www.routledge.com/Constrained-Markov-Decision-Processes/Altman/p/book/9781584883593>
52. []{#ref-52}Ames, A. D., Xu, X., Grizzle, J. W., & Tabuada, P. (2017). Control barrier function based quadratic programs for safety critical systems. *IEEE TAC*, 62(8), 3861-3876. <https://doi.org/10.1109/TAC.2016.2638961>
53. []{#ref-53}NIST. (2023). *Artificial Intelligence Risk Management Framework (AI RMF 1.0)*. <https://www.nist.gov/itl/ai-risk-management-framework>
54. []{#ref-54}Lamport, L., Shostak, R., & Pease, M. (1982). The Byzantine generals problem. *ACM TOPLAS*, 4(3), 382-401. <https://dl.acm.org/doi/10.1145/357172.357176>
55. []{#ref-55}Fischer, M. J., Lynch, N. A., & Paterson, M. S. (1985). Impossibility of distributed consensus with one faulty process. *JACM*, 32(2), 374-382. <https://groups.csail.mit.edu/tds/papers/Lynch/jacm85.pdf>
56. []{#ref-56}Malone, T. W., & Crowston, K. (1994). The interdisciplinary study of coordination. *ACM Computing Surveys*, 26(1), 87-119. <https://ccs.mit.edu/papers/CCSWP157/CCSWP157.html>
57. []{#ref-57}Vickrey, W. (1961). Counterspeculation, auctions, and competitive sealed tenders. *Journal of Finance*, 16(1), 8-37. <https://onlinelibrary.wiley.com/doi/10.1111/j.1540-6261.1961.tb02789.x>
58. []{#ref-58}Clarke, E. H. (1971). Multipart pricing of public goods. *Public Choice*, 11, 17-33. <https://link.springer.com/article/10.1007/BF01726210>
59. []{#ref-59}Groves, T. (1973). Incentives in teams. *Econometrica*, 41(4), 617-631. <https://www.jstor.org/stable/1914085>
60. []{#ref-60}Gibbard, A. (1973). Manipulation of voting schemes: A general result. *Econometrica*, 41(4), 587-601. <https://www.jstor.org/stable/1914083>
61. []{#ref-61}Satterthwaite, M. A. (1975). Strategy-proofness and Arrow's conditions. *Journal of Economic Theory*, 10(2), 187-217. <https://www.sciencedirect.com/science/article/pii/0022053175900502>
62. []{#ref-62}Smith, R. G. (1980). The contract net protocol. *IEEE Transactions on Computers*, C-29(12), 1104-1113. <https://ieeexplore.ieee.org/document/1675516>
63. []{#ref-63}Brown, G. W. (1951). Iterative solution of games by fictitious play. In *Activity Analysis of Production and Allocation*. <https://cowles.yale.edu/sites/default/files/files/pub/mon/m13-all.pdf>
64. []{#ref-64}Weibull, J. W. (1997). *Evolutionary Game Theory*. MIT Press. <https://mitpress.mit.edu/9780262731218/evolutionary-game-theory/>
65. []{#ref-65}Hart, S., & Mas-Colell, A. (2000). A simple adaptive procedure leading to correlated equilibrium. *Econometrica*, 68(5), 1127-1150. <https://www.ma.huji.ac.il/hart/abs/adapt.html>
66. []{#ref-66}Krogh, A., & Vedelsby, J. (1995). Neural network ensembles, cross validation, and active learning. *NeurIPS 1994*. <https://papers.nips.cc/paper/1001-neural-network-ensembles-cross-validation-and-active-learning.pdf>
67. []{#ref-67}Dietterich, T. G. (2000). Ensemble methods in machine learning. *MCS 2000*. <https://link.springer.com/chapter/10.1007/3-540-45014-9_1>
68. []{#ref-68}Jacobs, R. A., Jordan, M. I., Nowlan, S. J., & Hinton, G. E. (1991). Adaptive mixtures of local experts. *Neural Computation*, 3(1), 79-87. <https://www.cs.toronto.edu/~hinton/absps/jjnh91.pdf>
69. []{#ref-69}Fedus, W., Zoph, B., & Shazeer, N. (2022). Switch Transformers: Scaling to trillion parameter models with simple and efficient sparsity. *JMLR*, 23(120), 1-39. <https://www.jmlr.org/papers/v23/21-0998.html>
