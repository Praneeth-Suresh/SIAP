# Notes: Policies, Value, and Control

## What to improve

- Add pseudo-code for proposal/adjudication/oversight composition.
- Introduce one failure case where the proposal policy was strong but oversight absent.
- Clarify differences between value estimation and confidence scoring.

## Alternative rewrite

A single monolithic “decide()” is seductive and usually wrong. Durable agents separate imagination from judgment and judgment from governance. Policy then ceases to be a line of code and becomes a layered institution.

## Pass 1 - Migrated ideas from current main topic

The current topic formalizes policy through value functions \(V^\pi, Q^\pi\), Bellman optimality recursion, and policy-gradient optimization for parameterized policies. It braids dynamic programming, policy-gradient learning, and MPC into a layered control view where proposal, adjudication, and oversight policies are compared by return, stability, and constraint adherence under perturbation.

## Pass 1 - Storyline outline (paragraph-by-paragraph)

Paragraph 1 begins with governance language: policy is the constitution of action, not a single sampling call from a model.

Paragraph 2 develops value functions as long-horizon moral bookkeeping, where Bellman recursion reveals how present choice prices future possibility.

Paragraph 3 introduces policy gradients as adaptation machinery, showing how experience reshapes control laws when exact models are unavailable.

Paragraph 4 turns to MPC as pragmatic foresight under constraints, recomputing near-term plans as reality drifts and measurements arrive.

Paragraph 5 unifies the braid into institutional design: resilient agents separate proposing, deciding, and policing so that capability does not outrun control.

## Pass 2 - Research synthesis: equations, theories, and connective tissue

Formal toolkit to assemble here: value definitions \(V^\pi(s)=\mathbb{E}_\pi[\sum_{t\ge0}\gamma^t r_t\mid s_0=s]\), \(Q^\pi(s,a)=\mathbb{E}_\pi[\sum_{t\ge0}\gamma^t r_t\mid s_0=s,a_0=a]\), and Bellman optimality \(V^\*(s)=\max_a\{R(s,a)+\gamma\sum_{s'}P(s'|s,a)V^\*(s')\}\) ([MDP](https://en.wikipedia.org/wiki/Markov_decision_process), [Bellman](https://en.wikipedia.org/wiki/Bellman_equation), [Underactuated DP](https://underactuated.mit.edu/dp.html)); policy optimization via score-function gradient \(\nabla_\theta J(\theta)=\mathbb{E}_{\pi_\theta}[\nabla_\theta\log\pi_\theta(a\mid s)\,Q^{\pi_\theta}(s,a)]\) and advantage-variance reduction \(A^\pi(s,a)=Q^\pi(s,a)-V^\pi(s)\) (policy-gradient lineage in [Sutton et al. 1999](https://papers.nips.cc/paper_files/paper/1999/hash/464d828b85b0bed98e80ade0a5c43b0f-Abstract.html)); and receding-horizon control via constrained finite-horizon optimization \( \min_{u_{0:N-1}} \sum_{k=0}^{N-1}(x_k^\top Qx_k+u_k^\top Ru_k)+x_N^\top Q_f x_N \) subject to \(x_{k+1}=f(x_k,u_k)\), with linear-quadratic special case solved by Riccati equations \(A^\top P+PA-PBR^{-1}B^\top P+Q=0\) (see [Underactuated LQR](https://underactuated.mit.edu/lqr.html), [MPC](https://en.wikipedia.org/wiki/Model_predictive_control), [Algebraic Riccati equation](https://en.wikipedia.org/wiki/Algebraic_Riccati_equation)). The connective claim should be that dynamic programming explains optimality structure, policy gradients explain learnability under function approximation, and MPC/Riccati machinery explain how to operationalize control with hard constraints and continual replanning.

## Additional alternate approaches for this rewrite

1. Build the topic as a constitutional-design essay: legislature (proposal), judiciary (adjudication), and regulator (oversight), each tied to one theory family.
2. Use a robotics control arc from Bellman to MPC to show how classical control ideas map directly onto LLM-agent orchestration loops.
3. Structure around one recurring failure mode (reward hacking), then show how each theory contributes a specific preventive mechanism.
4. Write as a studio critique of four policy designs, scoring each with value, stability, and safety metrics before selecting a final architecture.
