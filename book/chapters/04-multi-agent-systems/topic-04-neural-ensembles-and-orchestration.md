# Neural Ensembles and Orchestration

An ensemble is a parliament of imperfect predictors. Its power comes from structured disagreement, not uniform certainty.

## Formal aggregation model

Given predictors \(f_k(x)\), ensemble output is
\[
\hat{y}(x)=\sum_{k=1}^{K} w_k(x)\,f_k(x),\qquad \sum_k w_k(x)=1,\ w_k(x)\ge 0.
\]
For voting systems, \(\hat{y}=\operatorname{mode}\{f_k(x)\}\).  
For MoE, router \(g(x)\) selects sparse experts \(E(x)\subseteq\{1,\dots,K\}\).

Generalization gain is tied to error covariance: diverse-but-competent experts beat correlated experts.

## Three-theory braid

1. **Deep ensembles and uncertainty.** Independent predictors improve calibration and robustness under shift [[26](../../references.md#ref-26)] [[67](../../references.md#ref-67)].
2. **Mixture-of-experts routing.** Sparse specialization with learned gating yields scalable conditional computation [[25](../../references.md#ref-25)] [[68](../../references.md#ref-68)] [[69](../../references.md#ref-69)].
3. **Orchestrated societies of specialists.** Multi-agent compositions operationalize ensemble principles at workflow scale [[23](../../references.md#ref-23)] [[27](../../references.md#ref-27)].

## How to study this formally

Measure ensemble gain versus best single expert, calibration under OOD inputs, and routing entropy (to detect expert collapse). The objective is not maximal committee size; it is minimal correlated error for a fixed budget.
