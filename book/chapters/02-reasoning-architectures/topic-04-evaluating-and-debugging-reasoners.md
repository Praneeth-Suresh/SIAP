# Evaluating and Debugging Reasoners

The chapter began with an interpreter, added planning as controlled lookahead, and treated memory as governed access to the past. Evaluation closes the loop. A reasoner should be judged as a stochastic trajectory generator, not merely as a producer of final answers.

Final-answer accuracy is necessary, but it is too thin. An agent can arrive at the right answer by using forbidden evidence, overspending budget, skipping a required check, or taking an unsafe irreversible action that happened not to fail. Evaluation must therefore score paths as well as destinations: observations, internal steps, retrievals, tool calls, costs, confidence, constraints, and outcomes.

## The Evaluation Object

Let trajectory \(\tau=(\sigma_0,a_0,\dots,\sigma_T)\sim p_\pi(\tau)\). Define task utility \(U(\tau)\), safety cost \(C(\tau)\), and calibration score \(S(\tau)\). Evaluation is multi-objective:
\[
\max_\pi \ \mathbb{E}[U(\tau)] - \lambda\,\mathbb{E}[C(\tau)] \quad\text{with calibration constrained by}\quad \mathbb{E}[S(\tau)] \le \epsilon.
\]
This keeps expected utility as the compass while preventing "high reward by unsafe luck" from masquerading as competence [[33](../../references.md#ref-33)] [[34](../../references.md#ref-34)] [[53](../../references.md#ref-53)].

Here \(S(\tau)\) should be read as a calibration loss or calibration error: lower is better, which is why the constraint uses \(\le \epsilon\). If one instead used a calibration reward, the inequality would need to face the other way. The notation matters because evaluation is an accounting system; an upside-down sign can crown a liar for sounding confident.

The harness should log each transition with state summary, action, tool arguments, retrieved evidence, confidence, budget cost, constraint checks, and outcome. The resulting report should name ordinary engineering quantities, not only a philosophical score: task success, task-specific partial progress, tokens consumed, wall-clock latency, tool-call count, valid-call rate, and utility per call. Task-specific partial progress matters because a reasoner that localizes the failing file but misses the final patch is different from one that wanders heroically through irrelevant directories. Utility per call matters because two agents with equal success may differ by a factor of ten in tool noise; one is an engineer, the other is a very expensive weather system.

To learn which pattern caused which effect, compare machines under controlled ablations. Start with a base interpreter, then add planning, memory, retrieval, or reflection one at a time while holding the task set, model, budget, tools, and stopping rule as steady as possible. For combined patterns, use factorial comparisons in plain clothes: run planning alone, reflection alone, both together, and neither. If the combined system beats both single additions, the patterns may be cooperating. If it loses by burning latency or amplifying a bad memory, their composition is suspect. Repeat this across task families so the result is not "planning is good" or "reflection is bad," but "planning helped on long-horizon, high-branching tasks with prerequisites; reflection helped after uncertain failures and hurt on easy reversible tasks."

Unit tests can verify local contracts such as schema validity and permission behavior. Scenario tests can verify whole traces under controlled perturbations. Regression suites should include previous failures, adversarial distractors, stale memories, flaky tools, and ambiguous user requests.

## Calibration and Probabilistic Honesty

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
Low calibration error means the system's probabilities are interpretable commitments, not decorative numbers [[49](../../references.md#ref-49)].

A scoring rule is **strictly proper** when the best way to minimize expected
loss is to report one's true probability belief. It rewards honesty about
uncertainty rather than theatrical certainty. In the log score,
\(x_i\) is input example \(i\), \(y_i\) is the observed correct outcome,
\(p_\theta(y_i\mid x_i)\) is the model's probability for that outcome, and
\(N\) is the number of evaluated examples. The negative sign turns high
probability on the truth into low loss. If the model assigns probability
\(0.8\) to the true answer, the contribution is \(-\log 0.8\); if it assigns
\(0.01\), the penalty is much larger.

Expected calibration error bins predictions by stated confidence. \(B_b\) is
the set of examples whose confidence falls in bucket \(b\), such as all
predictions between 70 and 80 percent confident. \(|B_b|/N\) weights the bucket
by how many examples it contains. \(\mathrm{acc}(B_b)\) is the observed accuracy
inside the bucket, and \(\mathrm{conf}(B_b)\) is the average stated confidence.
If a bucket says 80 percent and succeeds only 60 percent of the time, that
bucket contributes a 20-point calibration gap. The formula averages those gaps
over buckets.

The displayed Brier equation is the binary form: \(y_i\in\{0,1\}\), and \(p_i\) is the predicted probability that the event occurs. For a multiclass classifier with \(K\) labels, use
\[
BS_{\mathrm{multi}}=\frac{1}{N}\sum_{i=1}^N\sum_{k=1}^K (p_{ik}-\mathbf{1}\{y_i=k\})^2,
\]
where \(p_{ik}\) is the predicted probability of class \(k\) on example \(i\). In both forms, a lower score is better, because the score is squared distance between probability and reality.

Calibration is not the same as value. A model can be well-calibrated about a low-value action, and a valuable action can remain uncertain. The policy layer should keep outcome value, confidence, evidence quality, and constraint cost as separate quantities until the governed decision rule combines them.

## Causal Debugging

Consider a failed coding-agent trace:

```text
sigma0: user asks for a failing test repair
retrieve: returns an old note saying "parser errors come from topic-02"
think: concludes topic-02 owns the failure
act: edits topic-02 without reading current traceback
observe: tests still fail; traceback names topic-04
halt: reports an attempted fix with low confidence
```

A controlled intervention changes one suspected cause while preserving the rest of the trace as much as possible. For instance, rerun the same replay but replace the retrieved old note with the current traceback, leaving the prompt, budget, available tools, and task unchanged. If the patched replay now reads topic-04 first and fixes the failure, retrieval choice becomes a plausible cause rather than a decorative postmortem villain.

When a failure appears, replay traces with interventions and estimate effects:
\[
\mathrm{ATE}=\mathbb{E}[Y\mid do(Z{=}1)]-\mathbb{E}[Y\mid do(Z{=}0)].
\]
This quantity is identified only under randomized interventions or explicit causal assumptions: the replay harness must be able to set \(Z\) while holding the relevant context fixed, or the estimate is only a suggestive contrast. Used carefully, interventional replay can test whether a step class such as retrieval choice, tool arguments, or reflection policy causes downstream harm [[6](../../references.md#ref-6)].

For fine-grained attribution, influence approximations estimate how much one datum or memory item perturbs a test loss:
\[
I_{up,loss}(z,z_{\text{test}})\approx -\nabla_\theta L(z_{\text{test}},\hat\theta)^\top H_{\hat\theta}^{-1}\nabla_\theta L(z,\hat\theta),
\]
which helps prioritize highest-leverage repairs [[50](../../references.md#ref-50)]. Influence is not a replacement for causal identification, but it is useful for triage when a large corpus, memory store, or training set may contain the source of a recurring error.

A gradient \(\nabla_\theta L\) is the vector of first derivatives of loss with respect to parameters \(\theta\); it points in the direction that most quickly increases the loss locally. A Hessian \(H_{\hat\theta}\) is the matrix of second derivatives at the fitted parameters \(\hat\theta\); it describes local curvature, or how the gradient itself changes as parameters move. The inverse Hessian \(H_{\hat\theta}^{-1}\) approximately converts a small gradient disturbance into the parameter movement that would have produced it. The approximation assumes the loss is smooth, the fitted point is locally well behaved, the Hessian is invertible or suitably damped, and the effect of upweighting one item is small enough that a local Taylor expansion is honest. When those assumptions fail, influence scores are still clues, but clues wearing ceremonial robes are not proofs.

```text
function DEBUG_FAILURE(trace, failure_predicate):
    baseline <- replay(trace)
    assert failure_predicate(baseline)

    for z in candidate_causes(trace):
        patched <- intervene(trace, z)
        outcome <- replay(patched)
        record_effect(z, failure_predicate(outcome))

    return ranked_causes_by_effect()
```

The important constraint is that `intervene` must change the candidate cause while preserving enough of the surrounding context for the comparison to mean anything.

## From Scores to Repairs

Evaluation is useful when it changes the engineering agenda. If hallucinated answers cluster after retrieval, intervene on the retriever, reranker, and evidence formatter before rewriting the entire prompt. If bad edits occur after shallow planning, test state abstraction, preconditions, and value scoring. If confidence spikes after tool use, measure calibration conditioned on tool class rather than only in aggregate.

The repair loop should keep the same empirical discipline as the measurement loop. A proposed fix is another change to the interpreter, so test it against the same family of tasks and the same cost ledgers. Add decomposition only if the tasks have horizon, branching factor, prerequisites, uncertainty, or irreversibility enough to repay it. Add retrieval only if the missing evidence is usually outside working state. Add reflection only if errors are recoverable by trace inspection rather than by simply doing the obvious next action. When two repairs are combined, check whether they assist each other or quietly multiply each other's vices.

Report confidence-utility frontiers rather than a single accuracy point when systems face safety or cost constraints. Track failures by transition label: illegal action, bad belief update, missing retrieval, contaminated memory, premature halt, or unsafe reflection. The categories tie the evaluation harness back to the interpreter semantics from the start of the chapter.

## Exercise

Choose a failure from an agent trace. Define the trajectory-level utility, one safety cost, and one calibration measurement. Then propose two interventions that could be replayed, and state the causal assumption required for each comparison to identify the cause rather than merely correlate with it.
