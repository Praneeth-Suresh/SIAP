# Belief, Uncertainty, and Decision

The competent agent does not worship certainty; it manages uncertainty with discipline. Belief is a computational object, not a mood.

## Bayesian formalization

With latent state \(s_t\), history \(h_t\), and belief \(b_t(s)=P(s_t=s\mid h_t)\), updates follow
\[
b_{t+1}(s') = \eta\,\Omega(o_{t+1}\mid s')\sum_{s}T(s'\mid s,a_t)b_t(s),
\]
where \(\eta\) normalizes. Decision quality is evaluated through belief-state value:
\[
V^\pi(b)=\mathbb{E}\!\left[\sum_{t\ge 0}\gamma^t R(s_t,a_t)\mid b_0=b,\pi\right].
\]

Information gathering is itself an action. The value of information for query \(q\) is
\[
\operatorname{VoI}(q)=\mathbb{E}\!\left[\max_a \mathbb{E}[U(a,s)\mid h_t,q]\right]
\;-\;\max_a \mathbb{E}[U(a,s)\mid h_t].
\]

## Three-theory braid

1. **Bayesian decision theory.** Rational action under uncertainty is posterior-weighted expected utility [[34](../../references.md#ref-34)] [[7](../../references.md#ref-7)].
2. **Information theory.** Entropy and mutual information quantify epistemic uncertainty and expected reduction from sensing/retrieval actions [[35](../../references.md#ref-35)].
3. **Proper scoring and calibration.** Probabilistic outputs must be evaluated with strictly proper rules to avoid overconfident nonsense dressed as confidence [[49](../../references.md#ref-49)].

## How to study this formally

Run ablations where retrieval, tool probes, or clarification questions are treated as costly information actions. Measure calibration (ECE/Brier), downstream utility, and VoI realized per unit latency/token cost. If epistemic actions do not improve calibrated decision quality, the loop is decorative, not deliberative.
