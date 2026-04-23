# Evaluating and Debugging Reasoners

If you only score final answers, you reward lucky shortcuts and miss systematic failure. Reasoners must be judged as stochastic processes over trajectories.

## Formal evaluation object

Let trajectory \(\tau=(\sigma_0,a_0,\dots,\sigma_T)\sim p_\pi(\tau)\).  
Define task utility \(U(\tau)\), safety cost \(C(\tau)\), and calibration score \(S(\tau)\).  
Evaluation is multi-objective:
\[
\max_\pi \ \mathbb{E}[U(\tau)] - \lambda\,\mathbb{E}[C(\tau)] \quad\text{with calibration constrained by}\quad \mathbb{E}[S(\tau)] \le \epsilon.
\]

## Three-theory braid

1. **Proper scoring rules.** Calibration and probabilistic honesty are measured with strictly proper losses (e.g., log score, Brier) [[49](../../references.md#ref-49)].
2. **Trace-based causal diagnosis.** Interventional replay and counterfactual edits reveal which loop step caused failure [[6](../../references.md#ref-6)].
3. **Influence-based debugging.** Influence-function approximations identify training/data points or memory entries that drive specific errors [[50](../../references.md#ref-50)].

## How to study this formally

Instrument every loop step, replay with controlled interventions, and report confidence-utility frontiers rather than single accuracy points. A reasoning stack graduates from demo to system only when its failures are reproducible, attributable, and reducible.
