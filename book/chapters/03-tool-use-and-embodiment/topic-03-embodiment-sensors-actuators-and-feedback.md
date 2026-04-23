# Embodiment: Sensors, Actuators, and Feedback

Embodiment means the world can answer back. Even software-only agents are embodied in systems with latency, saturation, and irreversible side effects.

## State-space formalization

Let continuous latent state \(x_t\), control \(u_t\), and observation \(o_t\):
\[
x_{t+1}=f(x_t,u_t)+w_t,\qquad o_t=g(x_t)+v_t.
\]
The controller chooses \(u_t=\pi(o_{0:t},u_{0:t-1})\) to optimize long-run utility under actuator and safety bounds.

Sensor quality enters through observability; actuator quality enters through controllability and delay.

## Three-theory braid

1. **Control-theoretic state estimation.** Kalman-style filtering formalizes noisy sensing and recursive belief updates [[36](../../references.md#ref-36)].
2. **Reinforcement learning dynamics.** MDP/POMDP and return optimization model delayed consequences of action [[3](../../references.md#ref-3)] [[4](../../references.md#ref-4)].
3. **System-level environment coupling.** Agent loops embedded in real infrastructures require explicit modeling of latency, rate limits, and non-stationarity [[2](../../references.md#ref-2)].

## How to study this formally

Quantify sensor noise sensitivity, actuator saturation failures, and closed-loop stability under delays. Evaluate with perturbation tests and feedback-loop stress scenarios. An embodied agent that ignores feedback geometry is not autonomous; it is merely loud.
