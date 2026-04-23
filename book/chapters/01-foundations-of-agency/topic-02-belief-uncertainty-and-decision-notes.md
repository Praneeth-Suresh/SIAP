# Notes: Belief, Uncertainty, and Decision

## What to improve

- Add a worked example contrasting deterministic heuristics with Bayesian updates.
- Introduce expected value of information with a small numerical calculation.
- Clarify when approximate inference is acceptable in production agent loops.

## Alternative rewrite

The mature engineer does not ask, “What does the model think?” but, “How uncertain is the model, and what action is justified under that uncertainty?” In agentic systems, epistemology is not philosophy class; it is latency budgets, retrieval calls, and whether you can trust the next tool invocation.

## Pass 1 - Migrated ideas from current main topic

The current topic formalizes uncertainty through belief states and Bayesian filtering, \(b_{t+1}(s') \propto \Omega(o_{t+1}\mid s')\sum_s T(s'\mid s,a_t)b_t(s)\), then evaluates policies in belief space via \(V^\pi(b)\). It reframes information gathering as an action using value of information and braids Bayesian decision theory, information theory, and calibration/proper scoring into one practical program for measuring epistemic quality in agent loops.

## Pass 1 - Storyline outline (paragraph-by-paragraph)

Paragraph 1 begins with a scene of epistemic humility: the agent stands in partial light, and belief is introduced as a living map rather than a static guess.

Paragraph 2 develops Bayesian update as the narrative heartbeat, where each observation edits the map and each edit changes which actions are rational.

Paragraph 3 introduces information as economic choice: queries, tool calls, and tests are investments whose value depends on how much uncertainty they retire per unit cost.

Paragraph 4 pivots from belief to accountability, explaining calibration as intellectual honesty—confidence must earn its probability mass through proper scoring and empirical checks.

Paragraph 5 resolves the arc by showing resilience as “knowing what you do not know” and using that knowledge to plan information-seeking actions deliberately.

## Pass 2 - Research synthesis: equations, theories, and connective tissue

Core mathematical spine for this topic: Bayesian filtering \(b'(s')=\eta\,O(o\mid s',a)\sum_s P(s'\mid s,a)b(s)\), posterior predictive \(P(o\mid b,a)=\sum_{s'}O(o\mid s',a)\sum_sP(s'\mid s,a)b(s)\), and belief-value objective \(V^\pi(b)=\mathbb{E}[\sum_t\gamma^t r_t\mid b_0=b]\) (from [POMDP](https://en.wikipedia.org/wiki/Partially_observable_Markov_decision_process), [belief-space notes](https://underactuated.mit.edu/belief.html)); uncertainty quantification by entropy \(H(X)=-\sum_x p(x)\log p(x)\) and information gain \(I(X;Y)=H(X)-H(X\mid Y)\) (Shannon program, source: [1948 paper](https://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf)); decision value of sensing by \(\mathrm{VoI}(q)=\mathbb{E}[\max_a\mathbb{E}[U(a,S)\mid q]]-\max_a\mathbb{E}[U(a,S)]\) and EVPI/EVSI framing (decision-analysis sources: [Value of Information](https://en.wikipedia.org/wiki/Value_of_information)); and epistemic honesty via proper scoring rules, especially log score \(-\log p_\theta(y)\) and Brier score \(BS=\frac1N\sum_t(f_t-o_t)^2\), with decomposition \(BS=REL-RES+UNC\) for calibration diagnostics ([Scoring rules](https://en.wikipedia.org/wiki/Scoring_rule), [Brier score](https://en.wikipedia.org/wiki/Brier_score)). The connection to foreground is that Bayesian belief updates supply the evolving state of knowledge, information theory prices ignorance and measurement, and proper scoring rules keep confidence tethered to reality rather than rhetoric.

## Additional alternate approaches for this rewrite

1. Tell the topic as a detective narrative in which each tool call is a clue and Bayesian update is the method for revising suspect probabilities.
2. Use a trading-floor metaphor where uncertainty, information cost, and expected gain are treated as portfolio decisions over actions.
3. Structure the exposition around one recurring numerical toy problem, updated at each section to show posterior movement and policy shifts.
4. Write as a dialogue between an overconfident planner and a calibration auditor, with equations settling each dispute.
