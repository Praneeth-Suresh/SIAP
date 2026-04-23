# Policies, Value, and Control

A policy is not merely “what the model says next”; it is the constitution that governs action under uncertainty, delay, and cost.

## Core equations

For policy \(\pi\),
\[
V^\pi(s)=\mathbb{E}_\pi\!\left[\sum_{t\ge0}\gamma^t r_t\mid s_0=s\right],\qquad
Q^\pi(s,a)=\mathbb{E}_\pi\!\left[\sum_{t\ge0}\gamma^t r_t\mid s_0=s,a_0=a\right].
\]
Optimality obeys Bellman recursion:
\[
V^{*}(s)=\max_a\left\{R(s,a)+\gamma\sum_{s'}T(s'\mid s,a)V^{*}(s')\right\}.
\]

When policies are parameterized by \(\theta\), gradient ascent uses
\[
\nabla_\theta J(\theta)=\mathbb{E}_{\pi_\theta}\!\left[\nabla_\theta \log \pi_\theta(a\mid s)\,Q^{\pi_\theta}(s,a)\right].
\]

## Three-theory braid

1. **Dynamic programming.** Bellman equations provide exact structure for value and control decomposition [[5](../../references.md#ref-5)] [[39](../../references.md#ref-39)].
2. **Policy-gradient methods.** Stochastic policies can be optimized directly with unbiased gradient estimators [[40](../../references.md#ref-40)].
3. **Model predictive control (MPC).** Receding-horizon optimization handles constraints and changing dynamics in real deployments [[41](../../references.md#ref-41)].

## How to study this formally

Treat orchestration as layered control: proposal policy, adjudication policy, and oversight policy. Compare designs on return, stability, and safety-constraint adherence under perturbations. A policy that looks brilliant on one trajectory but violates constraints under mild shift is theater, not control.
