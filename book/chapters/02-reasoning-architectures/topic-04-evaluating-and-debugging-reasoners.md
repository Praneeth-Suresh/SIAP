# Evaluating and Debugging Reasoners

If you only score final answers, you reward lucky shortcuts and miss mechanism-level failure. Reasoners must be evaluated as stochastic trajectory generators whose confidence, actions, and side effects can all be audited.

## Formal evaluation object

Let trajectory \(\tau=(\sigma_0,a_0,\dots,\sigma_T)\sim p_\pi(\tau)\).  
Define task utility \(U(\tau)\), safety cost \(C(\tau)\), and calibration score \(S(\tau)\).  
Evaluation is multi-objective:
\[
\max_\pi \ \mathbb{E}[U(\tau)] - \lambda\,\mathbb{E}[C(\tau)] \quad\text{with calibration constrained by}\quad \mathbb{E}[S(\tau)] \le \epsilon.
\]
This keeps expected utility as the compass while preventing "high reward by unsafe luck" from masquerading as competence [[33](../../references.md#ref-33)] [[34](../../references.md#ref-34)] [[53](../../references.md#ref-53)].

## Probabilistic honesty and calibration

Strictly proper scoring rules make confidence testable. Two canonical choices are log score
\[
\mathcal{L}_{\log}=-\frac{1}{N}\sum_{i=1}^N \log p_\theta(y_i\mid x_i),
\]
and Brier score
\[
BS=\frac{1}{N}\sum_{i=1}^N (p_i-y_i)^2.
\]
For bucketed predictions \(B_b\), expected calibration error is
\[
\mathrm{ECE}=\sum_b \frac{|B_b|}{N}\left|\mathrm{acc}(B_b)-\mathrm{conf}(B_b)\right|.
\]
Low calibration error means the system's probabilities are interpretable promises, not decorative numbers [[49](../../references.md#ref-49)].

## Causal and influence-based debugging

When a failure appears, replay traces with interventions and estimate effects:
\[
\mathrm{ATE}=\mathbb{E}[Y\mid do(Z{=}1)]-\mathbb{E}[Y\mid do(Z{=}0)].
\]
This identifies which step class (retrieval choice, tool args, reflection policy) actually causes downstream harm [[6](../../references.md#ref-6)]. For fine-grained attribution, influence approximations estimate how much one datum or memory item perturbs a test loss:
\[
I_{up,loss}(z,z_{\text{test}})\approx -\nabla_\theta L(z_{\text{test}},\hat\theta)^\top H_{\hat\theta}^{-1}\nabla_\theta L(z,\hat\theta),
\]
which helps prioritize highest-leverage repairs [[50](../../references.md#ref-50)].

## Three-theory braid

Proper scoring rules discipline what the model says it knows, causal trace diagnosis disciplines what the loop actually does when perturbed, and influence-based methods discipline where the error came from in data or memory space, so evaluation becomes a braid of foresight (calibrated confidence before action), responsiveness (interventional replay during incidents), and resilience (targeted edits that reduce recurrence rather than moving symptoms around) [[49](../../references.md#ref-49)] [[6](../../references.md#ref-6)] [[50](../../references.md#ref-50)].

## How to study this formally

Instrument every loop step, score confidence and outcomes jointly, replay with controlled interventions, and report confidence-utility frontiers rather than single accuracy points. A reasoning stack graduates from demo to system only when failures are reproducible, attributable, and reducible.
