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

## Translating the Theory into Agentic Practice

Evaluation theory tells us to stop treating the final answer as the whole creature. An agent is a trajectory generator: it observes, reasons, retrieves, calls tools, edits state, spends budget, and sometimes leaves footprints in external systems. Better evaluation therefore scores the path as well as the destination. The agent may answer correctly by using forbidden evidence, calling an unnecessary expensive tool, or taking an unsafe shortcut. Such victories should be recorded as warnings, not medals.

A practical evaluation harness should log each step with state summary, action, tool arguments, evidence, confidence, cost, constraint checks, and outcome. Unit tests can verify local contracts: schema validity, permission behavior, refusal policy, retrieval filters. Scenario tests can verify full trajectories under controlled perturbations. Regression suites should include previous failures, adversarial distractors, stale memories, flaky tools, and ambiguous user requests. The harness should make failures reproducible enough that repair is engineering, not exorcism.

Debugging then becomes causal. If a hallucinated answer appears, intervene on retrieval and rerun. If a bad edit lands, intervene on the planner's state abstraction, then on the value scorer, then on the safety filter. If confidence is miscalibrated, test whether the model is overconfident everywhere or only after particular tools or memory types. Influence and trace analysis help prioritize repairs that remove causes rather than polish symptoms.

The theory is valuable because it defines what maturity looks like. A better agent is not merely more accurate; it is calibrated, auditable, resistant to familiar failures, and cheaper to debug after unfamiliar ones. Evaluation becomes the agent's laboratory constitution: every claim must be measured, every failure must have a trace, and every improvement must survive old adversaries returning in new forms.
