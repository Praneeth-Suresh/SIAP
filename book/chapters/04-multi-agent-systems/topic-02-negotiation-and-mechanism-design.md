# Negotiation and Mechanism Design

Negotiation is what happens when autonomy meets scarcity. Mechanism design is how we stop that meeting from turning into chaos.

## Formal mechanism frame

A mechanism is
\[
\mathcal{M}=(N,\Theta, A, g, p),
\]
with agents \(N\), types \(\Theta\), outcome space \(A\), allocation rule \(g\), and transfers \(p\).  
Desired properties: incentive compatibility (IC), individual rationality (IR), and budget feasibility.

For truthful dominant-strategy reporting, each agent \(i\) should satisfy
\[
u_i\!\big(g(\hat\theta_i,\hat\theta_{-i}),p_i(\hat\theta_i,\hat\theta_{-i});\theta_i\big)
\ge
u_i\!\big(g(\theta'_i,\hat\theta_{-i}),p_i(\theta'_i,\hat\theta_{-i});\theta_i\big).
\]

## Three-theory braid

1. **VCG-style efficient mechanisms.** Transfer rules can align local truthfulness with global welfare [[57](../../references.md#ref-57)] [[58](../../references.md#ref-58)] [[59](../../references.md#ref-59)].
2. **Social-choice limits.** Gibbard-Satterthwaite impossibility reminds us that manipulation-free voting is highly constrained [[60](../../references.md#ref-60)] [[61](../../references.md#ref-61)].
3. **Contract-net negotiation.** Task delegation via bidding provides practical distributed allocation under heterogeneous capabilities [[62](../../references.md#ref-62)].

## How to study this formally

Measure allocative efficiency, truthfulness regret, and fairness under strategic reporting. Simulate adversarial type misreports and collusion. A negotiation protocol without incentive analysis is merely an argument with extra JSON.
