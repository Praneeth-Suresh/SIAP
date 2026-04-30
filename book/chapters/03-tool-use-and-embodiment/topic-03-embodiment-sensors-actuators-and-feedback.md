# Embodiment: Sensors, Actuators, and Feedback

Embodiment means the world answers back. Even software-only agents are embodied in infrastructure with delay, noise, saturation, and permissions that do not negotiate.

## Lag-aware state-space model

Let latent state \(x_t\), control \(u_t\), and observation \(o_t\):
\[
x_{t+1}=f(x_t,u_{t-d_u})+w_t,\qquad o_t=g(x_{t-d_o})+v_t,
\]
where \(d_u\) and \(d_o\) are actuation and observation lag. Policy \(\pi\) chooses \(u_t\) under bounds such as \(\|u_t\|_\infty\le u_{\max}\), because commands outside the envelope are not bold; they are invalid.

## Estimation-control backbone

For linearized dynamics, Kalman filtering gives recursive belief updates:
\[
\hat x_{t|t-1}=A\hat x_{t-1|t-1}+Bu_{t-1},\qquad
K_t=P_{t|t-1}H^\top(HP_{t|t-1}H^\top+R)^{-1},
\]
\[
\hat x_{t|t}=\hat x_{t|t-1}+K_t(o_t-H\hat x_{t|t-1}),
\]
followed by feedback control \(u_t=-K\hat x_t\) in LQR style [[36](../../references.md#ref-36)] [[41](../../references.md#ref-41)].

Long-run behavior is still Bellman-governed:
\[
V^\star(s)=\max_a\left\{R(s,a)+\gamma\sum_{s'}P(s'|s,a)V^\star(s')\right\},
\]
with policy objective \(J(\pi)=\mathbb{E}_\pi[\sum_t\gamma^t r_t]\) [[3](../../references.md#ref-3)] [[4](../../references.md#ref-4)] [[5](../../references.md#ref-5)].

## API embodiment example

Suppose a deployment agent scales workers from delayed queue telemetry. A naive policy reacts to stale data and oscillates; a lag-aware estimator plus bounded feedback policy stabilizes behavior and cuts rollback churn. Same API, different control geometry.

## Three-theory braid

Control-theoretic estimation supplies the best available state from noisy delayed observations, reinforcement-learning and Bellman structure supply the long-horizon objective that prices delayed consequences, and system-level coupling analysis supplies non-negotiable constraints like latency, rate limits, and actuator saturation, so embodied intelligence appears as one continuous braid of foresight (optimize return over time), responsiveness (update estimates every observation), and resilience (maintain stable bounded feedback \(u_t=-K\hat x_t\) under disturbance) [[36](../../references.md#ref-36)] [[3](../../references.md#ref-3)] [[4](../../references.md#ref-4)] [[2](../../references.md#ref-2)].

## How to study this formally

Measure delay margin, sensor-noise sensitivity, saturation events, and closed-loop stability under perturbations. Compare with and without lag-aware estimation/control. An embodied agent that ignores feedback geometry is not autonomous; it is merely loud.
