# Notes: Goals, Environments, and Actions

## What to improve

- Add a concrete running example (research assistant, coding agent, or robot).
- Tighten the link between abstract symbols and implementation fields in Python classes.
- Include one short exercise asking readers to formalize a real prompt as an objective.

## Alternative rewrite

Suppose an agent wakes each turn, peers at a sliver of reality, and must choose one irrevocable move. If we cannot state what it wants, what it can see, and what it can do, then we do not have an architecture; we have vibes. The disciplined path is to name the goal, model the environment class, and enumerate valid actions before discussing prompts or frameworks.

## Pass 1 - Migrated ideas from current main topic

The current topic frames agency as a formal covenant between objectives and interventions: define \(\mathcal{M}=(\mathcal{S},\mathcal{O},\mathcal{A},T,\Omega,R,C,\gamma)\), optimize discounted return under constraints, and treat natural-language goals as specifications that must be compiled into explicit reward, cost, and stopping structures. The three-theory braid currently combines expected-utility foundations, sequential decision theory (MDP/POMDP), and feedback control, then closes with an evaluation protocol based on constrained return, regret, and violation rates.

## Pass 1 - Storyline outline (paragraph-by-paragraph)

Paragraph 1 opens with a navigator in fog: every intelligent act is a wager, and the first responsibility of design is to decide what “north” means before setting sail.

Paragraph 2 introduces expected utility as the compass needle, translating preference and uncertainty into a scalar objective so the question “what should I do?” becomes operational rather than rhetorical.

Paragraph 3 broadens to sequential worlds, where action is not a point decision but a trajectory commitment, and MDP/POMDP structure explains why foresight is a computational necessity rather than academic ornament.

Paragraph 4 introduces feedback control as the art of staying honest to reality, showing how closed-loop correction turns brittle plans into resilient behavior under disturbance.

Paragraph 5 braids the three strands into a design ethic: intelligence is not certainty, but disciplined adaptation guided by utility, dynamics, and correction.

## Pass 2 - Research synthesis: equations, theories, and connective tissue

Canonical equation set to anchor this narrative: expected utility as \(a^\*=\arg\max_{a\in\mathcal{A}}\sum_s p(s\mid a)u(s)\) (decision-theoretic baseline from von Neumann-Morgenstern/Savage formulations; see [Stanford Encyclopedia](https://plato.stanford.edu/entries/decision-theory/) and [expected utility overview](https://en.wikipedia.org/wiki/Expected_utility_hypothesis)); sequential objective as \(\max_\pi \mathbb{E}_\pi[\sum_{t=0}^\infty \gamma^t r_t]\) with Bellman recursion \(V^\*(s)=\max_a\{R(s,a)+\gamma\sum_{s'}P(s'\mid s,a)V^\*(s')\}\) (MDP/Bellman structure from [MDP](https://en.wikipedia.org/wiki/Markov_decision_process), [Bellman equation](https://en.wikipedia.org/wiki/Bellman_equation), and control notes in [Underactuated DP](https://underactuated.mit.edu/dp.html)); partial observability upgrade through belief dynamics \(b'(s')=\eta\,O(o\mid s',a)\sum_s P(s'\mid s,a)b(s)\) (POMDP formalization in [POMDP](https://en.wikipedia.org/wiki/Partially_observable_Markov_decision_process) and [belief-space derivation](https://underactuated.mit.edu/belief.html)); and feedback correction through state-space control \(x_{t+1}=f(x_t,u_t)+w_t,\; y_t=g(x_t)+v_t\) with linear feedback \(u_t=-Kx_t\) as an interpretable closed-loop archetype (Kalman/control framing in [Kalman filter](https://en.wikipedia.org/wiki/Kalman_filter) and [Underactuated state estimation](https://underactuated.mit.edu/state_estimation.html)). The connective logic to emphasize is: expected utility defines **what** is worth pursuing, dynamic programming defines **when** and **how** actions propagate value through time, and feedback control defines **how** plans survive contact with noisy reality.

## Additional alternate approaches for this rewrite

1. Build the full topic around one continuous case study (a coding agent shipping a patch under uncertainty), introducing each theory exactly at the moment the case study demands it.
2. Start with a historical arc (Bernoulli to Bellman to Kalman) and then reinterpret each milestone through modern LLM-agent orchestration.
3. Use a contrast structure: first show a “clever but fragile” prompt-only system, then progressively formalize it into a robust agent using the three-theory braid.
4. Frame the topic as a courtroom argument where each theory serves as a different kind of evidence for what constitutes rational action.

## Editor-Rewrite Alternative: Birth Inside the Approximation Stack

Open with Agent-427 receiving a sandboxed, read-only diagnosis task: classify a broken citation without editing the manuscript or retaining durable memory. Treat its POMDP contract as a useful constitution immediately betrayed by implementation. Walk down the approximation stack symbol by symbol: finite state versus a 10,000-token history, stationary dynamics versus an API that changes during deliberation, conditionally modeled observations versus correlated and adversarial telemetry, reward versus a test-deleting optimizer, and a mathematical action space versus malformed JSON. Preserve the formal tuple and constrained-return objective, but follow each formal block with arithmetic and each ideal with an interpreter repair. End with an executable exercise that asks the reader to implement validators and reproduce reward gaming rather than merely describe a contract. Reserve the fixed 03:47 timestamp/404/wrong-import incident for Chapter 2.

The preferred synthesis takes this lifecycle alternative because it gives Chapter 1 a birth scene, a technical spine, and a reason to care about every symbol. It retains the existing contract and coding example, while making the gap between model and machine the actual subject rather than an apologetic paragraph.
