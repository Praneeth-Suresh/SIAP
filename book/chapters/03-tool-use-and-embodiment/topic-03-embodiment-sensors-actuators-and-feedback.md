# Embodiment: Sensors, Actuators, and Feedback

Embodiment means the world answers back. Our subject is agents whose actions
land somewhere real, and the delay between the acting and the landing. We build
a small model of that delay, learn to estimate the present from stale readings,
and see what changes when a tool call must settle before it can be trusted.

The body of a software agent is not made of metal. It is made of APIs
(application programming interfaces, the published entry points other systems
expose), filesystems, browsers, queues, clocks, caches, databases, rate limits,
permissions, and humans waiting for results. These bodies have delay, noise,
saturation, and failure modes. None of those problems become simpler because the
agent writes fluent sentences.

## Command, Effect, and Observation Are Three Different Things

An interpreter that touches the world must distinguish command from effect, and
effect from observation. A command is what the agent asked for. An effect is
what actually changed. An observation is what a sensor later reports. The three
can disagree for a while, and that interval is where most embodied bugs live.

Ordinary examples make the gap concrete:

- A click may not settle the page.
- A deploy may not become healthy.
- A database write may replicate later.
- A queue metric may describe the past.

Embodiment is the discipline of acting under those lags while remaining correct
enough to be trusted.

## A State-Space Model That Accounts for Lag

Before the equations, the plain idea: the world has a true condition the agent
cannot see directly, the agent pushes on it, and the report of what happened
arrives late. A state-space model is simply a pair of rules, one for how the
world moves and one for what the sensors say.

Let latent state \(x_t\), meaning hidden from the agent's sensors, plus control
\(u_t\) and observation \(o_t\):
\[
x_{t+1}=f(x_t,u_{t-d_u})+w_t,\qquad o_t=g(x_{t-d_o})+v_t,
\]
where \(d_u\) and \(d_o\) are actuation and observation lag. Read the first
equation aloud as "the state at the next step comes from the current state plus a
command issued \(d_u\) steps ago, plus a random disturbance." Read the second as
"today's observation is a function of a state from \(d_o\) steps ago, plus
measurement error."

The policy \(\pi\), the agent's rule for choosing actions, picks \(u_t\) under
bounds such as \(\|u_t\|_\infty\le u_{\max}\), because commands outside the
envelope are not bold; they are invalid.

### The Symbols, Read Aloud

A symbol you cannot pronounce is a symbol you will not remember, so here is a
short glossary of the ones this loop runs on:

| Symbol | Read it as | Concrete meaning |
|---|---|---|
| \(x_t\) | "the latent state at step t" | What is really going on, such as a service's true health |
| \(u_t\) | "the control at step t" | What the agent does, such as adding two workers |
| \(o_t\) | "the observation at step t" | What the sensors report, such as a queue depth measured thirty seconds ago |
| \(w_t\) | "process noise at step t" | Uncommanded changes in the world |
| \(v_t\) | "observation noise at step t" | Error in the measurement |
| \(d_u\), \(d_o\) | "actuation lag, observation lag" | How late a command lands, and how late a reading arrives |
| \(\|u_t\|_\infty\) | "the infinity norm of u at step t" | The largest absolute component of the command vector |

The infinity norm is a compact way to say that no single knob may be turned too
far at once. If a scale command is the vector \((+3, -1)\), its infinity norm is
3, so a bound of \(u_{\max}=2\) rejects it.

This model applies directly to ordinary software operations. The latent state
may be the real health of a service. The control may be a rollout, a rollback, or
a scale adjustment. The observation may be delayed telemetry. The disturbance
terms \(w_t\) and \(v_t\) stand for everything the agent did not command and
everything the sensor did not measure cleanly. Chapter 1, Topic 3 (World Models
and State Abstractions) develops the general habit of naming state before acting
on it; here the new wrinkle is that the naming must include time.

## The Estimation and Control Backbone

Two jobs must now be separated. Estimation asks what the state probably is.
Control asks what to do given that estimate. Classical engineering has a standard
answer for each.

### Predict, Then Correct: The Kalman Update

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
[[36](../../references.md#ref-36)] [[41](../../references.md#ref-41)].

Kalman filtering is the disciplined version of "predict, then correct." The hat
in \(\hat x\) marks an estimate rather than the truth. The subscript
\(t|t-1\) means "the estimate for time \(t\) before seeing time \(t\)'s
observation"; \(t|t\) means "after seeing it."

The remaining letters each have one job:

- Matrix \(A\) predicts how the state evolves on its own.
- Matrix \(B\) says how yesterday's command changes today's state.
- Matrix \(H\) says what the sensor can see.
- Matrix \(P\) records uncertainty in the estimate.
- Matrix \(R\) records observation noise. Control theory reuses the letter \(R\) here; it is not Chapter 1's reward.
- The Kalman gain \(K_t\) decides how strongly to trust the new observation
  relative to the prediction.

### Delay Requires an Augmented State

With observation delay \(d_o\), the state must be augmented, for example
\[
z_t=(x_t,x_{t-1},\ldots,x_{t-d_o}),
\]
so the filter estimates the present from a history that explicitly contains the
stale state being observed. Read \(z_t\) as "the stacked list of the present
state and the last \(d_o\) states." Calling a standard delay-free update
"lag-aware" without this augmentation is a category error.

The augmented state \(z_t\) is also an estimate, not an oracle. It contains
latent variables for the present and the recent past so the filter can reason
about which old state a delayed observation is actually describing. The agent is
carrying a little clockwork model of time, not a perfect diary of truth.

### Two Different K's: Estimation Gain Versus Feedback Gain

Do not confuse that \(K_t\) with the feedback gain \(K\) in \(u_t=-K\hat x_t\).
The first \(K_t\) belongs to estimation; it tells the interpreter how to update
belief. The second \(K\) belongs to control; it tells the actuator how hard to
push once a state estimate exists. LQR, linear-quadratic regulation, is the
classical setting where a linear system is controlled by minimizing a quadratic
penalty on state error and control effort. In practice you tune that penalty:
raise the price of control effort and the agent pushes more gently.

### A Worked Queue Estimate You Can Check Mentally

For a scalar queue example, suppose yesterday's delayed sensor says the queue
was 100 jobs. The model predicts that two added workers should have reduced it to
70 by now. A noisy current observation reports 80. A cautious Kalman gain of
\(K_t=0.25\) updates the estimate to
\(70+0.25(80-70)=72.5\).

The arithmetic is small on purpose: prediction and observation differ by 10 jobs,
and a quarter of 10 is 2.5. The agent should scale from 72.5, not blindly from the
stale 100 or the noisy 80.

### Act on an Estimate, Not on the Last String Received

The control-theoretic point is modest but powerful: the agent should act on an
estimate of present state, not on the last string it received. Long-run behavior
is still governed by the same reinforcement-learning objective
\(J(\pi)=\mathbb{E}_\pi[\sum_t\gamma^t r_t]\), read as "the expected sum of
rewards under the policy, with later rewards discounted by \(\gamma\) each step."
The state supplied to the policy must be earned through sensing and filtering
[[3](../../references.md#ref-3)] [[4](../../references.md#ref-4)]
[[5](../../references.md#ref-5)].

## Feedback in Ordinary Tools

Suppose a deployment agent scales workers from delayed queue telemetry. A naive
policy reacts to stale data and oscillates: queue high, scale up; delayed queue
still high, scale up again; delayed drop finally appears, scale down too far. A
lag-aware estimator plus a bounded feedback policy stabilizes behavior and cuts
rollback churn. Same API, different control geometry.

The loop that fixes the oscillation is short. Each line is one step:

```text
observe telemetry with timestamp
estimate current queue depth from delayed samples
choose bounded scale adjustment
wait for the expected settling interval
observe health before issuing the next adjustment
```

In words: timestamp the reading, correct for the lag, command within the bound,
wait for settling, then confirm health before commanding again.

### The Same Loop in Browsers, Databases, and Code

A browser agent follows the same pattern at smaller scale. It clicks, observes
the DOM (Document Object Model, the browser's live tree of page elements) after
the page has had time to respond, compares the new state to the
expected transition, and only then continues. A data agent runs a query, inspects
rows and errors, and updates its belief about the schema. A code agent edits,
runs tests, and treats failures as observations rather than insults.

### When Feedback Helps and When It Misleads

Feedback helps only when its timing and quality fit the task. If delay is short,
noise is low, disturbances are small, and the system has settled, feedback can
turn action into control.

Feedback can also lure the interpreter into overcorrection. That happens when the
sensor reports the past, when the world is being disturbed by other actors, or
when the actuator has not yet had time to take effect. Planning and reflection do
not automatically cure this. Composed with stale feedback, they may amplify
oscillation by inventing elaborate reasons to chase yesterday's measurement.

The practical question is always fourfold: what state does this observation
describe, how noisy is it, what changed while it was traveling, and has the
system had time to settle?

## Sensor and Actuator Models

A practical embodied architecture records two kinds of models, one for reading
the world and one for changing it.

Sensor models describe freshness, noise, authority, sampling delay, and blind
spots. Written down, they read like this:

- "CI status, meaning the continuous integration pipeline's report, is ten minutes old."
- "Repository search excludes generated code."
- "Browser state may have changed after navigation."

Actuator models describe effect delay, reversibility, rate limits, blast radius,
and confirmation signals:

- "Deployment takes five minutes to settle."
- "Email send is irreversible."
- "File edit is reversible until committed."

### Choosing Between Waiting, Probing, Acting, and Escalating

These models let the policy choose among four moves rather than always acting.
If telemetry is stale, observe again or widen uncertainty. If an actuator is
saturated, meaning further commands produce no additional effect, stop issuing
larger commands and choose a different route. If the confirmation signal never
arrives, consult an independent sensor before retrying an irreversible action.
Topic 4 (Safety Constraints and Guardrails) takes up the harder cases of
irreversibility.

### Where Control, Reward, and System Limits Meet

Three bodies of theory each supply one piece of this loop.
Control-theoretic estimation supplies the best available state from noisy,
delayed observations. Reinforcement learning supplies the long-horizon objective
that prices delayed consequences. System-level analysis supplies constraints such
as latency, rate limits, and actuator saturation
[[36](../../references.md#ref-36)] [[3](../../references.md#ref-3)]
[[4](../../references.md#ref-4)] [[2](../../references.md#ref-2)]. The shared
lesson is that autonomy is not the absence of feedback. It is obedience to the
right feedback at the right time.

### How to Measure Whether an Agent Is Safely Embodied

Evaluate embodied agents by measuring six things:

1. Delay margin, or how much extra lag the loop tolerates before going unstable.
2. Sensitivity to sensor noise.
3. Disturbance recovery, meaning how quickly the agent returns to target after an
   uncommanded change.
4. Settling time after actions.
5. Saturation events, counted whenever a command exceeded what the actuator could
   deliver.
6. Closed-loop stability with and without lag-aware estimation, run as an A/B
   comparison, meaning two matched groups of runs that differ in exactly one
   design choice.

An agent that ignores feedback geometry may still produce confident commands, but
it is not yet safely embodied.
