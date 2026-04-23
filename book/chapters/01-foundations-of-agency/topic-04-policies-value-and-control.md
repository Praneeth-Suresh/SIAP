# Policies, Value, and Control

A policy is not merely “what the model says next”; it is the constitution of an artificial polity under uncertainty, delay, and temptation. If goals are the crown and actions are the ministers, policy is the legal code that keeps cleverness from mutiny.

## Core equations

Let \(\pi(a\mid s)\) be a policy over an MDP. The long-run bookkeeping is value:
\[
V^\pi(s)=\mathbb{E}_\pi\!\left[\sum_{t=0}^{\infty}\gamma^t r_t\mid s_0=s\right],\qquad
Q^\pi(s,a)=\mathbb{E}_\pi\!\left[\sum_{t=0}^{\infty}\gamma^t r_t\mid s_0=s,a_0=a\right].
\]
Bellman recursion turns this into a compositional law of consequence [[5](../../references.md#ref-5)] [[39](../../references.md#ref-39)]:
\[
V^{*}(s)=\max_{a\in\mathcal{A}}\left\{R(s,a)+\gamma\sum_{s'\in\mathcal{S}}T(s'\mid s,a)V^{*}(s')\right\}.
\]
At one step, decision-theoretic choice is expected utility [[33](../../references.md#ref-33)] [[34](../../references.md#ref-34)]:
\[
a_t^{*}=\arg\max_a\;\mathbb{E}[U(a,S_t)\mid h_t].
\]
With parameterized policies, adaptation follows the policy-gradient theorem [[40](../../references.md#ref-40)]:
\[
\nabla_\theta J(\theta)=\mathbb{E}_{\pi_\theta}\!\left[\nabla_\theta\log\pi_\theta(a\mid s)\,Q^{\pi_\theta}(s,a)\right],
\]
and often uses the advantage baseline
\[
A^\pi(s,a)=Q^\pi(s,a)-V^\pi(s)
\]
to reduce variance without changing the expected gradient [[3](../../references.md#ref-3)] [[40](../../references.md#ref-40)].

## A failure case: brilliant proposal, absent oversight

Consider a coding agent choosing between **FastPatch** and **SafePatch** before a production freeze. The proposal policy has superb local instincts and estimates
\[
\hat Q(s,\text{FastPatch})=9.2,\qquad \hat Q(s,\text{SafePatch})=7.4,
\]
so without governance it ships FastPatch every time. But the real system is constrained:
\[
\max_\pi\;\mathbb{E}_\pi\!\left[\sum_{t\ge 0}\gamma^t r_t\right]
\quad\text{s.t.}\quad
\mathbb{E}_\pi\!\left[\sum_{t\ge 0}\gamma^t c_t\right]\le \kappa,
\]
and FastPatch quietly violates a hard safety budget (auth bypass risk, rollback blast radius), yielding high short-term reward and catastrophic tail cost [[51](../../references.md#ref-51)] [[53](../../references.md#ref-53)]. Capability, unguided, became a speedrun into policy debt.

## Proposal/adjudication/oversight composition (pseudo-code)

```text
function ACT(state x_t, history h_t):
    candidates <- ProposePolicy.sample_actions(x_t, h_t, K)

    # Adjudication: optimize task value under soft risk penalty
    for a in candidates:
        value[a] <- V_hat(x_t, a)
        risk[a]  <- C_hat(x_t, a)
        score[a] <- value[a] - lambda * risk[a]
    a_star <- argmax_a score[a]

    # Oversight: enforce hard constraints before execution
    if violates_hard_constraints(x_t, a_star):
        a_safe <- OversightPolicy.fallback(x_t, h_t)   # safe default / escalate
        return a_safe

    return a_star
```

This split does something monoliths rarely do: it lets imagination be bold, judgment be quantitative, and governance be stubborn.

## Value estimation is not confidence scoring

Value estimation asks, “If I take this action, how much discounted utility should I expect?” Confidence scoring asks, “How sure am I that my prediction or label is correct?” They are cousins, not twins. Formally,
\[
\hat V(s)\approx \mathbb{E}\!\left[\sum_{t\ge0}\gamma^t r_t\mid s\right]
\]
is about outcome magnitude, while a confidence model outputs
\[
\hat p(y\mid x)\approx P(Y=y\mid X=x)
\]
and is judged by calibration metrics such as Brier score
\[
\mathrm{BS}=\frac{1}{N}\sum_{i=1}^N (p_i-y_i)^2
\]
[[49](../../references.md#ref-49)]. An action can have high confidence and low value (certainly safe but useless), or lower confidence and high value (risky but worth it); policy quality depends on expected utility, not swagger.

## Three-theory braid

Dynamic programming gives the grammar of optimality through Bellman structure, where every present act is a price tag on future possibility \(V^{*}(s)=\max_a\{R(s,a)+\gamma\sum_{s'}T(s'\mid s,a)V^{*}(s')\}\) [[5](../../references.md#ref-5)] [[39](../../references.md#ref-39)]; policy-gradient learning then supplies adaptation when models are partial and function approximation is unavoidable, nudging parameters by \(\nabla_\theta J(\theta)=\mathbb{E}[\nabla_\theta\log\pi_\theta(a\mid s)Q^{\pi_\theta}(s,a)]\) so control laws can learn from experience instead of scripture [[40](../../references.md#ref-40)] [[3](../../references.md#ref-3)]; and model predictive control operationalizes this in the unruly present by repeatedly solving a finite-horizon constrained optimization, executing the first move, re-measuring reality, and replanning, with feedback law intuition captured by forms like \(u_t=-K\hat x_t\), so expected utility \(a^{*}=\arg\max_a\mathbb{E}[U(a,S)\mid h]\) becomes not a one-shot maxim but an institutional loop in which proposing, deciding, and policing co-evolve under uncertainty, constraints, and disturbance [[34](../../references.md#ref-34)] [[41](../../references.md#ref-41)] [[51](../../references.md#ref-51)] [[52](../../references.md#ref-52)].

## How to study this formally

Evaluate layered policies with ablations: proposer-only, proposer+adjudicator, and full proposer+adjudicator+oversight. Report constrained return, violation rate, closed-loop stability indicators, and calibration of risk/confidence heads under matched latency budgets. If the “smartest” policy wins only when constraints are ignored, you have not built control—you have built a very articulate gamble.
