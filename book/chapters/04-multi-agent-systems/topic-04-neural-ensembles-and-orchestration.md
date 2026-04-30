# Neural Ensembles and Orchestration

An ensemble is a parliament of imperfect predictors. Its power comes from structured disagreement, not synchronized overconfidence.

## Formal aggregation model

Given predictors \(f_k(x)\), ensemble output is
\[
\hat{y}(x)=\sum_{k=1}^{K} w_k(x)\,f_k(x),\qquad \sum_k w_k(x)=1,\ w_k(x)\ge 0.
\]
For voting systems, \(\hat{y}=\operatorname{mode}\{f_k(x)\}\).  
For MoE, router \(g(x)\) selects sparse experts \(E(x)\subseteq\{1,\dots,K\}\).

Generalization gain is tied to error covariance: diverse-but-competent experts beat correlated experts.

Confidence-weighted routing can use softmax gates
\[
w_k(x)=\frac{\exp(g_k(x)/\tau)}{\sum_j \exp(g_j(x)/\tau)},
\]
or top-\(k\) sparse routing \(E(x)=\operatorname{TopK}(g(x),k)\) for compute control [[25](../../references.md#ref-25)] [[69](../../references.md#ref-69)].

## Orchestration as budgeted control

Specialist dispatch is a sequential decision problem:
\[
V^\star(s)=\max_a\left\{R(s,a)-\lambda_c C(a)-\lambda_l L(a)+\gamma\,\mathbb{E}[V^\star(s')]\right\},
\]
where \(a\) chooses which experts/agents to consult, \(C\) is monetary compute cost, and \(L\) is latency. This prevents "call everyone" from masquerading as sophistication.

## Three-theory braid

Deep-ensemble theory gives uncertainty and calibration benefits through independent predictors, mixture-of-experts routing gives conditional computation that scales by activating only relevant specialists, and orchestrated multi-agent societies operationalize those principles at workflow level, so collective prediction becomes a braid of foresight (expected-utility routing under cost/latency budgets), responsiveness (input-dependent gating and reweighting), and resilience (fault tolerance from diversity with reduced correlated error) [[26](../../references.md#ref-26)] [[67](../../references.md#ref-67)] [[25](../../references.md#ref-25)] [[68](../../references.md#ref-68)] [[69](../../references.md#ref-69)] [[23](../../references.md#ref-23)] [[27](../../references.md#ref-27)] [[33](../../references.md#ref-33)] [[34](../../references.md#ref-34)].

## How to study this formally

Measure ensemble lift over best single expert, calibration under shift, routing entropy (collapse detection), and cost-latency-normalized utility. The objective is not maximal committee size; it is minimal correlated error for a fixed budget.
