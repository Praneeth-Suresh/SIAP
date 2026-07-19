# Retrieval-Augmented Tooling

Retrieval-augmented tooling is the interpreter's way of asking the world for
evidence before it commits to an answer or an action. The retrieval call is not
a decorative prelude to generation. It is an external observation, purchased
under latency, permission, freshness, and relevance constraints, then folded
back into the agent's state.

This framing matters because many failures called "hallucination" are really
failures of evidence acquisition. The model was asked to act as if its prior
were enough. A retrieval-capable agent has a larger action space: it can search
the repository, inspect a table schema, query a memory index, open the current
policy, fetch a manual page, or decide that no new evidence is worth its cost.

## Probabilistic retrieval-generation pipeline

For query context \(x\), retrieved document \(d\), and answer \(y\):
\[
p(y\mid x) = \sum_{d \in \mathcal{D}} p(y\mid x,d)\,p(d\mid x).
\]
Operationally, \(p(d\mid x)\) is retrieval and ranking; \(p(y\mid x,d)\) is
grounded generation conditioned on the acquired evidence [[14](../../references.md#ref-14)].
The vertical bar in \(p(y\mid x,d)\) means "given." Read the equation this way:
the agent imagines each possible document \(d\), asks how likely answer \(y\)
would be if that document were the evidence, and weights that answer by how
likely the retriever was to select \(d\) for the query \(x\). The sum is not
saying the agent literally reads every document in the universe; it is a clean
idealization of a ranked evidence process.

Typical retrieval scores include dense similarity
\[
s_{\text{dense}}(q,d)=\langle e_q,e_d\rangle
\]
and lexical ranking such as BM25 [[15](../../references.md#ref-15)] [[46](../../references.md#ref-46)].
An embedding \(e_q\) or \(e_d\) is a vector representation of a query or
document. The angle brackets denote an inner product: multiply corresponding
coordinates and add them. Similar vectors point in similar semantic directions,
so a query about "permission checks before deletion" may retrieve a passage
about "authorization gates for destructive actions" even without exact word
overlap.

Dense retrieval buys semantic reach; lexical retrieval buys exact surface
matches and interpretable term evidence. Hybrid systems are common because the
two failures differ: an embedding may miss a precise identifier, while a lexical
ranker may miss a paraphrase.

The control question is when to retrieve. One uncertainty-triggered policy is
\[
\texttt{retrieve}_t = \mathbf{1}\{H[p(\cdot\mid h_t)] > \tau\},
\]
but the economically sharper rule is expected value of information:
\[
\mathrm{VoI}(q)=\mathbb{E}\!\left[\max_a\mathbb{E}[U(a,S)\mid q]\right]-\max_a\mathbb{E}[U(a,S)].
\]
Retrieve when \(\mathrm{VoI}(q)\) exceeds retrieval cost.

Here \(H\) is entropy, a measure of spread-out uncertainty. If the agent assigns
nearly all probability to one answer, entropy is low; if many answers remain
plausible, entropy is high. \(\tau\) is a threshold chosen by the designer. In
practice, this simple rule says: when the model is too uncertain, buy evidence
unless the evidence is too expensive or forbidden.

The value-of-information expression gives a sober interpretation of search.
The question is not "could more context be useful?" Almost always, yes. The
question is whether the expected change in the downstream decision is worth the
delay, token budget, privacy exposure, and distraction risk of importing more
text.

## Evidence as an action

Let the retrieval decision be an action
\(a_t\in\{\texttt{retrieve},\texttt{skip}\}\). A budget-aware control law prices
its latency and token cost while preserving the long-horizon effect on the
task [[5](../../references.md#ref-5)] [[4](../../references.md#ref-4)]. This is
the formal version of a practical truth: always retrieving is slow, never
retrieving is reckless.

An agentic retrieval policy should therefore be separate from the generation
policy. The retrieval policy observes task type, uncertainty, freshness
requirements, source permissions, and cost. It chooses among local search,
vector memory, web search, database lookup, tool documentation, or no retrieval.
The generation policy receives a bounded evidence set with provenance and
conflict information.

```text
need = uncertainty(task, history)
sources = allowed_sources(task, caller)
if value_of_information(need, sources) <= retrieval_cost:
  answer_from_current_state()
else:
  evidence = retrieve_and_rank(task, sources)
  answer_with_citations(evidence)
```

The small program hides a difficult discipline: retrieved text must not become
untyped context sludge. Each item should carry source, timestamp, access path,
rank score, and the claim it supports. If two sources disagree, the agent should
surface the conflict or acquire higher-authority evidence rather than smoothing
the contradiction into fluent prose.

For a beginner builder, this is where retrieval becomes tool design instead of
text stuffing. A source may be relevant but stale, authoritative but outside the
caller permission boundary, fresh but contradicted by a higher-authority manual,
or cheap but too vague to change the decision. A well-designed retrieval tool
returns enough metadata for the interpreter to reason about those differences.

## Where retrieval belongs

Retrieval should often precede irreversible action. A coding agent should
inspect relevant symbols before editing. A compliance agent should fetch the
current rule before advising. A data agent should retrieve schema and sample
rows before writing a query. A deployment agent should inspect recent incidents
and service health before changing production. In each case, retrieval is
valuable only if it can change the rational next move.

This also explains why retrieval quality cannot be judged by answer style
alone. Measure Recall@\(k\), nDCG, citation faithfulness, contradiction rate,
freshness error, tool-call efficiency, and end-task utility under fixed
retrieval budgets. Compare always-retrieve, never-retrieve, and uncertainty or
value-of-information policies. The comparison matters because each policy fails
differently: always-retrieve spends tokens and time even when the state is
already sufficient; never-retrieve turns stale memory into false confidence; a
conditional policy can still be wrong if its uncertainty signal is miscalibrated.
If retrieval cannot buy measurable uncertainty reduction per unit latency, it is
ritual rather than reasoning.

Recall@\(k\) asks whether the needed evidence appears somewhere in the top
\(k\) retrieved items. nDCG, normalized discounted cumulative gain, also cares
about order: useful evidence near rank 1 counts more than the same evidence
buried near rank 20. These metrics are not literary judgments of the final
answer. They are tests of whether the observation step gave the interpreter a
fair chance to know what it needed.

The theory pays off by preventing two expensive pathologies. Over-retrieval
bloats context, slows execution, and admits distractors. Under-retrieval lets
fluent priors masquerade as evidence. A retrieval-augmented agent is better not
because it keeps more documents nearby, but because it knows when an external
document deserves to govern the next interpreter step.

Composition can improve this judgment or spoil it. A planner that retrieves
fresh evidence once, then passes the evidence and provenance to subtasks, can
save calls and keep the collective anchored. A planner that retrieves
redundantly for every subtask may spend its budget proving the same fact four
times. Memory can help by remembering what was already checked, but stale memory
can also suppress retrieval that the current task plainly needs. Retrieval is
therefore most valuable for tasks with high uncertainty, fresh external facts,
inspectable evidence, and enough consequence that the delay is cheaper than the
mistake.
