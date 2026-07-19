# Embodiment: Sensors, Actuators, and Feedback

Embodiment means the world answers back. The body of a software agent is not
made of metal; it is made of APIs, filesystems, browsers, queues, clocks,
caches, databases, rate limits, permissions, and humans waiting for results.
These bodies have delay, noise, saturation, and failure modes that do not become
simpler because the agent is fluent.

An interpreter that touches the world must therefore distinguish command from
effect and effect from observation. A click may not settle the page. A deploy
may not become healthy. A database write may replicate later. A queue metric may
describe the past. Embodiment is the discipline of acting under those lags while
remaining correct enough to be trusted.

## Lag-aware state-space model

Let latent state \(x_t\), control \(u_t\), and observation \(o_t\):
\[
x_{t+1}=f(x_t,u_{t-d_u})+w_t,\qquad o_t=g(x_{t-d_o})+v_t,
\]
where \(d_u\) and \(d_o\) are actuation and observation lag. Policy \(\pi\)
chooses \(u_t\) under bounds such as \(\|u_t\|_\infty\le u_{\max}\), because
commands outside the envelope are not bold; they are invalid.

The variables are ordinary once named. The latent state \(x_t\) is what is
really going on but cannot be inspected perfectly, such as the current health of
a service. The control \(u_t\) is what the agent does, such as adding two
workers. The observation \(o_t\) is what the sensors report, such as a queue
depth measured thirty seconds ago. The noise terms \(w_t\) and \(v_t\) represent
uncommanded changes in the world and error in measurement. The infinity norm
\(\|u_t\|_\infty\) means the largest absolute component of the command vector;
it is a compact way to say that no single knob may be turned too far at once.

This model applies directly to ordinary software operations. The latent state
may be the real health of a service; the control may be a rollout, rollback, or
scale adjustment; the observation may be delayed telemetry. The disturbance
terms \(w_t\) and \(v_t\) stand for everything the agent did not command and
everything the sensor did not measure cleanly.

## Estimation-control backbone

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
[[36](../../references.md#ref-36)] [[41](../../references.md#ref-41)]. With
observation delay \(d_o\), the state must be augmented, for example
\[
z_t=(x_t,x_{t-1},\ldots,x_{t-d_o}),
\]
so the filter estimates the present from a history that explicitly contains the
stale state being observed. Calling a standard delay-free update "lag-aware"
without this augmentation is a category error.

Kalman filtering is the disciplined version of "predict, then correct." The
hat in \(\hat x\) marks an estimate. The subscript \(t|t-1\) means "the estimate
for time \(t\) before seeing time \(t\)'s observation"; \(t|t\) means "after
seeing it." Matrix \(A\) predicts how the state evolves on its own, \(B\) says
how yesterday's command changes today's state, \(H\) says what the sensor can
see, \(P\) records uncertainty in the estimate, and \(R\) records observation
noise. The Kalman gain \(K_t\) decides how strongly to trust the new
observation relative to the prediction.

Do not confuse that \(K_t\) with the feedback gain \(K\) in \(u_t=-K\hat x_t\).
The first \(K_t\) belongs to estimation; it tells the interpreter how to update
belief. The second \(K\) belongs to control; it tells the actuator how hard to
push once a state estimate exists. LQR, linear-quadratic regulation, is the
classical setting where a linear system is controlled by minimizing a quadratic
penalty on state error and control effort.

For a scalar queue example, suppose yesterday's delayed sensor says the queue
was 100 jobs, the model predicts that two added workers should have reduced it
to 70 by now, and a noisy current observation reports 80. A cautious Kalman gain
of \(K_t=0.25\) updates the estimate to
\(70+0.25(80-70)=72.5\). The agent should scale from 72.5, not blindly from the
stale 100 or the noisy 80.

The augmented state \(z_t\) is also an estimate, not an oracle. It contains
latent variables for the present and recent past so the filter can reason about
which old state a delayed observation is actually describing. The agent is
carrying a little clockwork model of time, not a perfect diary of truth.

The control-theoretic point is modest but powerful: the agent should act on an
estimate of present state, not on the last string it received. Long-run behavior
is still governed by the same reinforcement-learning objective
\(J(\pi)=\mathbb{E}_\pi[\sum_t\gamma^t r_t]\), but the state supplied to the
policy must be earned through sensing and filtering [[3](../../references.md#ref-3)]
[[4](../../references.md#ref-4)] [[5](../../references.md#ref-5)].

## Feedback in ordinary tools

Suppose a deployment agent scales workers from delayed queue telemetry. A naive
policy reacts to stale data and oscillates: queue high, scale up; delayed queue
still high, scale up again; delayed drop finally appears, scale down too far. A
lag-aware estimator plus bounded feedback policy stabilizes behavior and cuts
rollback churn. Same API, different control geometry.

```text
observe telemetry with timestamp
estimate current queue depth from delayed samples
choose bounded scale adjustment
wait for the expected settling interval
observe health before issuing the next adjustment
```

A browser agent follows the same pattern at smaller scale. Click, observe the
DOM after the page has had time to respond, compare the new state to the
expected transition, and only then continue. A data agent runs a query, inspects
rows and errors, and updates its belief about the schema. A code agent edits,
runs tests, and treats failures as observations rather than insults.

Feedback helps only when its timing and quality fit the task. If delay is short,
noise is low, disturbances are small, and the system has settled, feedback can
turn action into control. If the sensor reports the past, if the world is being
disturbed by other actors, or if the actuator has not yet had time to take
effect, feedback can lure the interpreter into overcorrection. Planning and
reflection do not automatically cure this; composed with stale feedback, they
may amplify oscillation by inventing elaborate reasons to chase yesterday's
measurement. The practical question is always: what state does this observation
describe, how noisy is it, what changed while it was traveling, and has the
system had time to settle?

## Sensor and actuator models

A practical embodied architecture records two kinds of models. Sensor models
describe freshness, noise, authority, sampling delay, and blind spots: "CI
status is ten minutes old," "repository search excludes generated code,"
"browser state may have changed after navigation." Actuator models describe
effect delay, reversibility, rate limits, blast radius, and confirmation
signals: "deployment takes five minutes to settle," "email send is
irreversible," "file edit is reversible until committed."

These models let the policy choose between waiting, probing, acting, and
escalating. If telemetry is stale, observe again or widen uncertainty. If an
actuator is saturated, stop issuing larger commands and choose a different
route. If the confirmation signal never arrives, consult an independent sensor
before retrying an irreversible action.

Control-theoretic estimation supplies the best available state from noisy,
delayed observations; reinforcement learning supplies the long-horizon
objective that prices delayed consequences; system-level analysis supplies
constraints such as latency, rate limits, and actuator saturation
[[36](../../references.md#ref-36)] [[3](../../references.md#ref-3)]
[[4](../../references.md#ref-4)] [[2](../../references.md#ref-2)]. The shared
lesson is that autonomy is not the absence of feedback. It is obedience to the
right feedback at the right time.

Evaluate embodied agents by measuring delay margin, sensitivity to sensor
noise, disturbance recovery, settling time after actions, saturation events, and
closed-loop stability with and without lag-aware estimation. An agent that
ignores feedback geometry may still produce confident commands, but it is not
yet safely embodied.
