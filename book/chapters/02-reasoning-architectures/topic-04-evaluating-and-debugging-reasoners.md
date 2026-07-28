# Evaluating and Debugging Reasoners

Suppose an agent is asked to fix a failing test, and it succeeds. Now suppose it succeeded by reading a private file it was never permitted to open, spending four times its token budget, and skipping the required regression run. The final answer is still correct. The reasoner is still broken. This section is about building an evaluation that can tell those two agents apart.

This chapter opened with an interpreter for reasoning. It then added planning as controlled lookahead, and treated memory as governed access to the past. Evaluation closes the loop. The central move is to judge a reasoner as a *stochastic trajectory generator* — a machine that produces whole run-paths with randomness in them — rather than as a vending machine for final answers.

## Why Final-Answer Accuracy Is Not Enough

Final-answer accuracy is necessary. It is also too thin. An agent can reach the right answer while doing at least four things we would never sanction:

- using forbidden evidence;
- overspending its budget;
- skipping a required check;
- taking an unsafe irreversible action that simply happened not to fail this time.

An action that cannot be undone and only *happened* not to explode is not a success. It is a coin flip wearing a medal.

So evaluation must score paths as well as destinations. The quantities worth scoring are the ones the interpreter actually touches: observations, internal steps, retrievals, tool calls, costs, confidence, constraints, and outcomes.

## The Evaluation Object

Let trajectory \(\tau=(\sigma_0,a_0,\dots,\sigma_T)\sim p_\pi(\tau)\). Read that as: "tau is the sequence of state, action, state, action, up to the final state at step T, drawn from the distribution over trajectories that policy pi induces." Each \(\sigma_t\) is the reasoner's state at step \(t\); each \(a_t\) is the action it took there.

Three scores are then attached to that one trajectory. Define task utility \(U(\tau)\), safety cost \(C(\tau)\), and calibration score \(S(\tau)\). A run, a distribution over runs, and three separate scores make for crowded notation, so here is the reading key:

| Symbol | Read aloud as | Meaning |
|---|---|---|
| \(\tau\) | "tau" | One complete run: states and actions from start to halt |
| \(p_\pi(\tau)\) | "p sub pi of tau" | The chance that policy \(\pi\) produces this particular run |
| \(U(\tau)\) | "U of tau" | How much task value the run earned |
| \(C(\tau)\) | "C of tau" | How much safety cost the run incurred |
| \(S(\tau)\) | "S of tau" | How badly the run's stated confidence matched reality |
| \(\lambda\) | "lambda" | The exchange rate: how much utility one unit of safety cost is worth |
| \(\epsilon\) | "epsilon" | The largest calibration error we are willing to tolerate |

Evaluation is therefore multi-objective:
\[
\max_\pi \ \mathbb{E}[U(\tau)] - \lambda\,\mathbb{E}[C(\tau)] \quad\text{with calibration constrained by}\quad \mathbb{E}[S(\tau)] \le \epsilon.
\]
Read the first part as "choose the policy that maximizes expected task utility minus lambda times expected safety cost", and the second as "subject to expected calibration error staying at or below epsilon". This keeps expected utility as the compass while preventing "high reward by unsafe luck" from masquerading as competence [[33](../../references.md#ref-33)] [[34](../../references.md#ref-34)] [[53](../../references.md#ref-53)].

### Getting the Sign of the Calibration Term Right

Here \(S(\tau)\) should be read as a calibration loss or calibration error: lower is better, which is why the constraint uses \(\le \epsilon\). If one instead used a calibration reward, the inequality would need to face the other way. The notation matters because evaluation is an accounting system; an upside-down sign can crown a liar for sounding confident.

One quick check: a policy that always claims 99 percent confidence while being right half the time must fail this constraint, not pass it.

## What the Harness Should Log and Report

The harness should log each transition with state summary, action, tool arguments, retrieved evidence, confidence, budget cost, constraint checks, and outcome. Without that log, every later debugging step is guesswork.

The resulting report should name ordinary engineering quantities, not only a philosophical score:

- task success;
- task-specific partial progress;
- tokens consumed;
- wall-clock latency;
- tool-call count;
- valid-call rate;
- utility per call.

Task-specific partial progress matters because a reasoner that localizes the failing file but misses the final patch is different from one that wanders heroically through irrelevant directories. Both score zero on final success; only one is close.

Utility per call matters because two agents with equal success may differ by a factor of ten in tool noise. Suppose both solve 40 tasks. One used 200 calls, the other 2000. That is 0.20 utility per call against 0.02. One is an engineer, the other is a very expensive weather system.

## Ablations: Learning Which Pattern Caused Which Effect

To learn which pattern caused which effect, compare machines under controlled ablations. An *ablation* removes or adds exactly one component and holds everything else fixed.

Start with a base interpreter. Then add planning, memory, retrieval, or reflection one at a time, while holding the task set, model, budget, tools, and stopping rule as steady as possible.

For combined patterns, use factorial comparisons in plain clothes. That means four runs:

1. planning alone;
2. reflection alone;
3. both together;
4. neither.

If the combined system beats both single additions, the patterns may be cooperating. If it loses by burning latency or amplifying a bad memory, their composition is suspect.

Repeat this across task families. Avoid a verdict as crude as "planning is good" or "reflection is bad". The useful finding sounds like this: planning helped on long-horizon, high-branching tasks with prerequisites; reflection helped after uncertain failures and hurt on easy reversible tasks.

### Three Layers of Tests

Unit tests can verify local contracts such as schema validity and permission behavior. Scenario tests can verify whole traces under controlled perturbations. Regression suites should include previous failures, adversarial distractors, stale memories, flaky tools, and ambiguous user requests.

## Calibration and Probabilistic Honesty

A model's stated confidence is only useful if it can be checked. Strictly proper scoring rules make confidence testable. A scoring rule is **strictly proper** when the best way to minimize expected loss is to report one's true probability belief. It rewards honesty about uncertainty rather than theatrical certainty.

Two canonical choices are log score
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

### Reading the Log Score

In the log score, \(x_i\) is input example \(i\), \(y_i\) is the observed correct outcome, \(p_\theta(y_i\mid x_i)\) is the model's probability for that outcome, and \(N\) is the number of evaluated examples. The whole expression reads "the average, over N examples, of the negative log probability the model gave to the truth".

The negative sign turns high probability on the truth into low loss. If the model assigns probability \(0.8\) to the true answer, the contribution is \(-\log 0.8\); if it assigns \(0.01\), the penalty is much larger. In natural logarithms those are roughly \(0.22\) against \(4.6\), a twenty-fold difference in penalty for one confident mistake.

### Reading Expected Calibration Error

Expected calibration error bins predictions by stated confidence. \(B_b\) is the set of examples whose confidence falls in bucket \(b\), such as all predictions between 70 and 80 percent confident. \(|B_b|/N\) weights the bucket by how many examples it contains. \(\mathrm{acc}(B_b)\) is the observed accuracy inside the bucket, and \(\mathrm{conf}(B_b)\) is the average stated confidence.

If a bucket says 80 percent and succeeds only 60 percent of the time, that bucket contributes a 20-point calibration gap. The formula averages those gaps over buckets, weighted by bucket size. To use it, a builder logs a stated confidence with every decision, sorts them into ten bins, and compares each bin's claim to its outcome rate.

### Reading Brier Score, Including the Multiclass Form

The displayed Brier equation is the binary form: \(y_i\in\{0,1\}\), and \(p_i\) is the predicted probability that the event occurs. For a multiclass classifier with \(K\) labels, use
\[
BS_{\mathrm{multi}}=\frac{1}{N}\sum_{i=1}^N\sum_{k=1}^K (p_{ik}-\mathbf{1}\{y_i=k\})^2,
\]
where \(p_{ik}\) is the predicted probability of class \(k\) on example \(i\), and \(\mathbf{1}\{y_i=k\}\) is 1 when class \(k\) is the true label and 0 otherwise. In both forms, a lower score is better, because the score is squared distance between probability and reality. Predicting 0.9 on an event that happens costs \(0.01\); predicting 0.9 on an event that does not happen costs \(0.81\).

### Calibration Is Not Value

Calibration is not the same as value. A model can be well-calibrated about a low-value action, and a valuable action can remain uncertain. The policy layer should keep outcome value, confidence, evidence quality, and constraint cost as separate quantities until the governed decision rule combines them.

## Causal Debugging

Debugging means finding which step caused the failure. Consider a failed coding-agent trace. The block below lists six steps in order, from the user's request to a low-confidence report, and shows the agent following a stale memory instead of the current error message:

```text
sigma0: user asks for a failing test repair
retrieve: returns an old note saying "parser errors come from topic-02"
think: concludes topic-02 owns the failure
act: edits topic-02 without reading current traceback
observe: tests still fail; traceback names topic-04
halt: reports an attempted fix with low confidence
```

### Controlled Interventions on a Replayed Trace

A controlled intervention changes one suspected cause while preserving the rest of the trace as much as possible. For instance, rerun the same replay but replace the retrieved old note with the current traceback, leaving the prompt, budget, available tools, and task unchanged. If the patched replay now reads topic-04 first and fixes the failure, retrieval choice becomes a plausible cause rather than a decorative postmortem villain.

When a failure appears, replay traces with interventions and estimate effects:
\[
\mathrm{ATE}=\mathbb{E}[Y\mid do(Z{=}1)]-\mathbb{E}[Y\mid do(Z{=}0)].
\]
ATE stands for average treatment effect. Read the formula as "the expected outcome Y when we force the suspected cause Z on, minus the expected outcome when we force it off". The \(do(\cdot)\) notation means we *set* the value rather than merely observe it.

This quantity is identified only under randomized interventions or explicit causal assumptions: the replay harness must be able to set \(Z\) while holding the relevant context fixed, or the estimate is only a suggestive contrast. Used carefully, interventional replay can test whether a step class such as retrieval choice, tool arguments, or reflection policy causes downstream harm [[6](../../references.md#ref-6)].

### Influence Approximations for Triage

For fine-grained attribution, influence approximations estimate how much one datum or memory item perturbs a test loss:
\[
I_{up,loss}(z,z_{\text{test}})\approx -\nabla_\theta L(z_{\text{test}},\hat\theta)^\top H_{\hat\theta}^{-1}\nabla_\theta L(z,\hat\theta),
\]
which helps prioritize highest-leverage repairs [[50](../../references.md#ref-50)]. Influence is not a replacement for causal identification, but it is useful for triage when a large corpus, memory store, or training set may contain the source of a recurring error.

A gradient \(\nabla_\theta L\) is the vector of first derivatives of loss with respect to parameters \(\theta\); it points in the direction that most quickly increases the loss locally. A Hessian \(H_{\hat\theta}\) is the matrix of second derivatives at the fitted parameters \(\hat\theta\); it describes local curvature, or how the gradient itself changes as parameters move. The inverse Hessian \(H_{\hat\theta}^{-1}\) approximately converts a small gradient disturbance into the parameter movement that would have produced it.

The approximation rests on four assumptions:

1. the loss is smooth;
2. the fitted point is locally well behaved;
3. the Hessian is invertible or suitably damped;
4. the effect of upweighting one item is small enough that a local Taylor expansion is honest.

When those assumptions fail, influence scores are still clues, but clues wearing ceremonial robes are not proofs.

### A Debugging Loop, Written Out

The pseudocode below confirms the failure on a baseline replay, then replays once per candidate cause with that cause intervened upon, and ranks causes by how much each changed the outcome:

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

Evaluation is useful when it changes the engineering agenda. Three patterns point at three different repairs:

- If hallucinated answers cluster after retrieval, intervene on the retriever, reranker, and evidence formatter before rewriting the entire prompt.
- If bad edits occur after shallow planning, test state abstraction, preconditions, and value scoring.
- If confidence spikes after tool use, measure calibration conditioned on tool class rather than only in aggregate.

### Test the Fix Like You Tested the Failure

The repair loop should keep the same empirical discipline as the measurement loop. A proposed fix is another change to the interpreter, so test it against the same family of tasks and the same cost ledgers.

Each added pattern must earn its place:

- Add decomposition only if the tasks have horizon, branching factor, prerequisites, uncertainty, or irreversibility enough to repay it.
- Add retrieval only if the missing evidence is usually outside working state.
- Add reflection only if errors are recoverable by trace inspection rather than by simply doing the obvious next action.

When two repairs are combined, check whether they assist each other or quietly multiply each other's vices.

### Report Frontiers, and Label Failures by Transition

Report confidence-utility frontiers rather than a single accuracy point when systems face safety or cost constraints. A frontier shows what accuracy is available at each level of cost or risk, which is the decision a builder actually faces.

Track failures by transition label:

- illegal action;
- bad belief update;
- missing retrieval;
- contaminated memory;
- premature halt;
- unsafe reflection.

The categories tie the evaluation harness back to the interpreter semantics from the start of the chapter. A failure counted this way already names the part of the machine to open.

## Exercise

Choose a failure from an agent trace. Define the trajectory-level utility, one safety cost, and one calibration measurement. Then propose two interventions that could be replayed, and state the causal assumption required for each comparison to identify the cause rather than merely correlate with it.

Work it in four steps. First, write \(U(\tau)\) as something countable, such as "1 if the target test passes, else partial credit for correctly localizing the file". Second, write \(C(\tau)\) as a penalty on a specific forbidden or irreversible act. Third, choose a calibration measurement and say how you would bin it. Fourth, for each intervention, name exactly what you hold fixed. A good answer makes the held-fixed list explicit, because that list *is* the causal assumption.
