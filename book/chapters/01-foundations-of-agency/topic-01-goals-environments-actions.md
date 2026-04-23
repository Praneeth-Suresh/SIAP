# Goals, Environments, and Actions

Agency begins with a compact covenant: choose actions that push a world toward a goal. The covenant sounds poetic until we formalize it, at which point it becomes testable engineering [[2](../../references.md#ref-2)].

## Formal model

Let an agent-environment system be
\[
\mathcal{M} = (\mathcal{S}, \mathcal{O}, \mathcal{A}, T, \Omega, R, C, \gamma),
\]
where \(T(s' \mid s,a)\) is transition dynamics, \(\Omega(o \mid s)\) is observation dynamics, \(R\) is task reward, \(C\) is a constraint vector (cost, risk, budget), and \(\gamma \in (0,1)\) is discount.

A policy \(\pi(a\mid h_t)\), with history \(h_t=(o_{0:t},a_{0:t-1})\), seeks
\[
\max_{\pi}\ \mathbb{E}_{\pi,T,\Omega}\!\left[\sum_{t=0}^{\infty}\gamma^t R(s_t,a_t)\right]
\quad\text{s.t.}\quad
\mathbb{E}_{\pi}\!\left[\sum_{t=0}^{\infty}\gamma^t C_j(s_t,a_t)\right] \le \kappa_j.
\]
Natural-language goals are therefore specifications that must be compiled into \(R\), \(C\), and termination conditions.

## Three-theory braid

1. **Expected-utility foundations.** Rational preference under uncertainty is represented by utility maximization; this turns “what should I do?” into a mathematical objective [[33](../../references.md#ref-33)] [[34](../../references.md#ref-34)].
2. **Sequential decision theory.** MDP/POMDP formalisms model how present action sculpts future opportunity, not just immediate text quality [[4](../../references.md#ref-4)] [[7](../../references.md#ref-7)].
3. **Feedback control.** In open worlds, behavior is closed-loop: observations update state estimates, which update action, which perturbs the world again [[36](../../references.md#ref-36)] [[39](../../references.md#ref-39)].

## How to study this formally

Define benchmark tasks with explicit \((R,C)\), estimate transition uncertainty, and compare policies by constrained return, regret, and violation rate. If a system cannot state its objective and constraints mathematically, it has not yet earned the title “agent”; it is still a very articulate reflex.
