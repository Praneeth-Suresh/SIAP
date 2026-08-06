# Notes: Embodiment: Sensors, Actuators, and Feedback

## What to improve

- Add one API-agent example with delayed feedback and corrective replanning.
- Add notation for observation and control lag.
- Add discussion of actuator saturation and permission boundaries.

## Alternative rewrite

Embodiment is where grand theories meet stubborn reality. A plan that ignores sensor noise, action latency, and delayed rewards is not bold; it is nonphysical.

## Pass 1 - Migrated ideas from current main topic

The current topic models embodiment with state dynamics \(x_{t+1}=f(x_t,u_t)+w_t\) and observations \(o_t=g(x_t)+v_t\), then treats control as long-horizon utility optimization under actuator/safety bounds. Its braid combines Kalman-style estimation, RL decision dynamics in MDP/POMDP form, and practical infrastructure coupling through latency and non-stationarity [[36](../../references.md#ref-36)] [[3](../../references.md#ref-3)] [[4](../../references.md#ref-4)] [[2](../../references.md#ref-2)].

## Pass 1 - Storyline outline (paragraph-by-paragraph)

Paragraph 1 opens with a physicality thesis: every agent is embodied because every action touches a delayed, lossy, capacity-limited environment.

Paragraph 2 introduces noisy sensing and delayed actuation as geometric distortions of the control loop.

Paragraph 3 develops state estimation and feedback control as the mechanism for converting raw observations into stable action [[36](../../references.md#ref-36)] [[41](../../references.md#ref-41)].

Paragraph 4 links immediate control choices to long-horizon regret through Bellman recursion and policy optimization [[5](../../references.md#ref-5)] [[3](../../references.md#ref-3)].

Paragraph 5 resolves with resilience: saturation, permission boundaries, and lag-aware replanning as first-class design constraints rather than implementation afterthoughts.

## Pass 2 - Research synthesis: equations, theories, and connective tissue

Equation set: delayed dynamics \(x_{t+1}=f(x_t,u_{t-d_u})+w_t\), delayed observation \(o_t=g(x_{t-d_o})+v_t\); Kalman predict-update \(\hat x_{t|t-1}=A\hat x_{t-1|t-1}+Bu_{t-1}\), \(K_t=P_{t|t-1}H^\top(HP_{t|t-1}H^\top+R)^{-1}\), \(\hat x_{t|t}=\hat x_{t|t-1}+K_t(o_t-H\hat x_{t|t-1})\) [[36](../../references.md#ref-36)]; LQR feedback \(u_t=-K\hat x_t\) from Riccati structure [[41](../../references.md#ref-41)]; RL objective \(J(\pi)=\mathbb{E}_\pi[\sum_t\gamma^t r_t]\) and Bellman optimality \(V^\star(s)=\max_a\{R(s,a)+\gamma\sum_{s'}P(s'|s,a)V^\star(s')\}\) [[3](../../references.md#ref-3)] [[4](../../references.md#ref-4)] [[5](../../references.md#ref-5)]; saturation constraint \(\|u_t\|_\infty\le u_{\max}\). External equation check in pass 2 used underactuated control notes for dynamic programming and LQR ([DP](https://underactuated.mit.edu/dp.html), [LQR](https://underactuated.mit.edu/lqr.html)). Connection narrative: estimation provides situational awareness, control provides immediate correction, and Bellman planning provides long-run coherence.

## Additional alternate approaches for this rewrite

1. Use an autonomous-warehouse robot story where observation lag causes near misses until feedback gains are redesigned.
2. Frame embodiment as "API robotics": sensors are telemetry endpoints, actuators are tool calls with side effects.
3. Teach through a two-loop diagram: fast stabilization loop and slow planning loop.
4. Write as a postmortem of saturation failure where valid commands exceeded permissioned actuation bounds.

## Editor Rewrite Alternative Before Primary Synthesis

Open in a responsive control room. Agent-427 sees queue depths 100, 80, and 5;
the first is stale, the second is noisy, and the third was forged by a worker
trying to avoid scale-out. Preserve the Kalman calculation, then show why its
Gaussian assumptions do not cover a strategic sensor. Give waiting and timeout
their own action semantics, and let an independent health probe break the tie
between contradictory observations. The exercise implements both a lag-aware
estimator and a quarantine path for adversarial readings.
