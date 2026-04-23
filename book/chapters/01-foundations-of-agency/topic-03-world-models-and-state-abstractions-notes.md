# Notes: World Models and State Abstractions

## What to improve

- Add one code-facing pattern for separating observation logs from decision state.
- Include a cautionary case where too much memory degraded planning quality.
- Add cross-reference to chapter 2 memory retrieval policy.

## Alternative rewrite

State is a political compromise between physics and budget. Keep too little, and the agent becomes amnesic theater. Keep too much, and it drowns in transcripts. The art is to preserve the sufficient statistics of future decisions, then ruthlessly discard vanity detail.

## Pass 1 - Migrated ideas from current main topic

The current topic defines abstraction as a map \(\phi:\mathcal{S}\to\mathcal{Z}\) that should preserve reward and transition structure well enough for control in compressed space, then extends this with causal world models using structural equations and interventions \(\mathrm{do}(\cdot)\). Its three-theory braid combines MDP homomorphisms, bisimulation-style similarity metrics, and causal modeling to argue that good compression must preserve decision-relevant counterfactual structure.

## Pass 1 - Storyline outline (paragraph-by-paragraph)

Paragraph 1 opens with the paradox of memory: to model everything is to decide nothing, and abstraction appears as selective forgetting in service of action.

Paragraph 2 introduces homomorphic abstraction as principled compression, showing that a smaller world can still carry the same control logic when structural constraints are respected.

Paragraph 3 adds bisimulation as the geometry of behavioral similarity, turning “these states are close enough” from intuition into measurable distance.

Paragraph 4 introduces causality as the difference between prediction and intervention, emphasizing that agents do not merely observe worlds—they perturb them.

Paragraph 5 braids the three strands into a practical doctrine: abstractions must be compact, behaviorally faithful, and intervention-aware to support robust planning.

## Pass 2 - Research synthesis: equations, theories, and connective tissue

Equation inventory for a rigorous rewrite: abstraction mapping \(\phi:\mathcal{S}\to\mathcal{Z}\) with reward/transition consistency \(R(s,a)\approx \bar R(\phi(s),a)\), \(\sum_{s':\phi(s')=z'}P(s'|s,a)\approx \bar P(z'|\phi(s),a)\) (state abstraction foundations in [Li, Walsh, Littman 2006](https://www.cs.rutgers.edu/~mlittman/papers/abstraction-06.pdf)); behavioral-distance control via bisimulation-type metrics, e.g. fixed-point form \(d(s,s')=\max_a\{|R(s,a)-R(s',a)|+\gamma\,W_d(P(\cdot|s,a),P(\cdot|s',a))\}\), where \(W_d\) is a transport distance over next-state distributions (metric approach from [Ferns, Panangaden, Precup](https://www.cs.mcgill.ca/~dprecup/publications/uai04.pdf) and general bisimulation relations in [Bisimulation](https://en.wikipedia.org/wiki/Bisimulation)); and causal structural representation \(X_i=f_i(\mathrm{Pa}(X_i),U_i)\) with interventions \(\mathrm{do}(X_j=x)\) and causal effect queries \(P(Y\mid \mathrm{do}(X=x))\) (SCM framing in Pearl and summarized in [Structural causal model](https://en.wikipedia.org/wiki/Structural_causal_model)). The integrative argument to develop is that abstraction decides what is computationally tractable, bisimulation metrics quantify what fidelity is lost, and causal modeling decides whether the compressed representation still answers intervention questions rather than merely correlational ones.

## Additional alternate approaches for this rewrite

1. Use a cartography metaphor (territory vs. map) where each theory answers a different question about map quality.
2. Build the chapter around successive compression experiments, measuring what control capability is lost or retained at each step.
3. Compare two competing world models (correlational vs. causal) on the same task and let outcomes reveal the conceptual gap.
4. Frame the narrative as an engineering postmortem of an agent failure caused by the wrong state abstraction.
