# Retrieval-Augmented Tooling

Sometimes an agent should stop guessing and go look something up. This section
is about that decision: when an agent should fetch outside evidence, how it
should score and rank what it finds, and how it should carry that evidence into
its next step. Retrieval here is an action with a price, not a ritual.

## Retrieval as an Observation the Agent Buys

Retrieval-augmented tooling is the interpreter's way of asking the world for
evidence before it commits to an answer or an action. Retrieval-augmented
generation, usually shortened to RAG, is the general name for this pattern.

The retrieval call is not a decorative prelude to generation. It is an external
observation. The agent buys that observation under four constraints: latency
(how long the lookup takes), permission (whether the caller may see the source),
freshness (whether the source is current), and relevance (whether it bears on
the task). What comes back is then folded into the agent's state.

This framing matters because many failures called "hallucination" are really
failures of evidence acquisition. The model was asked to act as if its prior
were enough. A prior here means the belief the model already carries from
training, before it looks anything up.

A retrieval-capable agent has a larger action space. It can:

- search the repository;
- inspect a table schema;
- query a memory index;
- open the current policy;
- fetch a manual page;
- or decide that no new evidence is worth its cost.

That last option is a real action, not a failure to act.

## The Probabilistic Retrieval-Generation Pipeline

The pipeline has two stages: find evidence, then answer using it. Writing that
down as probability makes the two stages separately inspectable.

Each piece of notation used in that pipeline gets a plain reading below:

| Symbol | Read it as |
|---|---|
| \(\mathcal{D}\) | the set of candidate documents the retriever can return |
| \(e_q\), \(e_d\) | vector embeddings of the query and of a document |
| \(H\) | entropy, a measure of how spread out the agent's uncertainty is |
| \(\tau\) | a threshold on entropy chosen by the designer |
| \(\mathrm{VoI}(q)\) | expected value of information for the query \(q\) |

For query context \(x\), retrieved document \(d\), and answer \(y\):
\[
p(y\mid x) = \sum_{d \in \mathcal{D}} p(y\mid x,d)\,p(d\mid x).
\]
Operationally, \(p(d\mid x)\) is retrieval and ranking; \(p(y\mid x,d)\) is
grounded generation conditioned on the acquired evidence [[14](../../references.md#ref-14)].

### Reading the Sum over Documents

The vertical bar in \(p(y\mid x,d)\) means "given." Read the equation this way:
the agent imagines each possible document \(d\), asks how likely answer \(y\)
would be if that document were the evidence, and weights that answer by how
likely the retriever was to select \(d\) for the query \(x\).

Suppose two candidate documents. The retriever gives
the first a selection chance of 0.8 and the second 0.2. Given the first, the
answer "the limit is 30 days" has probability 0.9; given the second, only 0.1.
Then \(p(y\mid x) = 0.8 \times 0.9 + 0.2 \times 0.1 = 0.74\). Notice that the
retriever's ranking, not the generator's fluency, did most of the work.

The sum is not saying the agent literally reads every document in the universe.
It is a clean idealization of a ranked evidence process.

### Dense and Lexical Retrieval Scores

Typical retrieval scores include dense similarity
\[
s_{\text{dense}}(q,d)=\langle e_q,e_d\rangle
\]
and lexical ranking such as BM25 [[15](../../references.md#ref-15)] [[46](../../references.md#ref-46)].
BM25 is a long-standing formula that scores a document by which query words it
contains and how rare those words are.

An embedding \(e_q\) or \(e_d\) is a vector representation of a query or
document. The angle brackets denote an inner product: multiply corresponding
coordinates and add them. For example, \(\langle (1,0,2),(1,1,1)\rangle
= 1 + 0 + 2 = 3\).

Similar vectors point in similar semantic directions. So a query about
"permission checks before deletion" may retrieve a passage about "authorization
gates for destructive actions" even without exact word overlap.

Each family buys something different:

- Dense retrieval buys semantic reach, matching meaning across different wording.
- Lexical retrieval buys exact surface matches and interpretable term evidence.

Hybrid systems are common because the two failures differ. An embedding may miss
a precise identifier such as `PolicyV3_2024`. A lexical ranker may miss a paraphrase.

### Deciding When to Retrieve

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
nearly all probability to one answer, entropy is low. If many answers remain
plausible, entropy is high. \(\tau\) is a threshold chosen by the designer.

The bold \(\mathbf{1}\{\cdot\}\) is an indicator: it equals 1 when the condition
inside holds and 0 otherwise. So the rule reads "retrieve at step \(t\) exactly
when uncertainty about the next answer exceeds \(\tau\)." In practice, this
simple rule says: when the model is too uncertain, buy evidence unless the
evidence is too expensive or forbidden.

### Value of Information as the Sharper Rule

The value-of-information expression, VoI for short, gives a sober interpretation
of search. Read it as the difference between two quantities: the best expected
usefulness \(U\) the agent could reach after seeing the answer to \(q\), minus
the best expected usefulness it can reach right now, averaging over the unknown state \(S\).

The question is not "could more context be useful?" Almost always, yes. The
question is whether the expected change in the downstream decision is worth the
delay, token budget, privacy exposure, and distraction risk of importing more
text.

To use this, you need no exact number. Estimate roughly: if a lookup costs two
seconds and would change the action in one case out of twenty, it pays only when
that case is expensive to get wrong.

## Evidence as an Action

Let the retrieval decision be an action
\(a_t\in\{\texttt{retrieve},\texttt{skip}\}\). Read that as: at step \(t\) the
agent picks either "retrieve" or "skip." A budget-aware control law prices
its latency and token cost while preserving the long-horizon effect on the
task [[5](../../references.md#ref-5)] [[4](../../references.md#ref-4)]. This is
the formal version of a practical truth: always retrieving is slow, never
retrieving is reckless.

### Separating the Retrieval Policy from the Generation Policy

An agentic retrieval policy should therefore be separate from the generation
policy. A policy is simply a rule for choosing actions.

The retrieval policy observes:

- the task type;
- current uncertainty;
- freshness requirements;
- source permissions;
- and cost.

It then chooses among local search, vector memory, web search, database lookup,
tool documentation, or no retrieval. The generation policy receives a bounded
evidence set with provenance and conflict information. Provenance means the
record of where each item came from.

### A Small Control Program for Retrieval

The following pseudocode shows that separation: estimate need, list
permitted sources, compare value against cost, then either answer from the
current state or retrieve, rank, and answer with citations.

```text
need = uncertainty(task, history)
sources = allowed_sources(task, caller)
if value_of_information(need, sources) <= retrieval_cost:
  answer_from_current_state()
else:
  evidence = retrieve_and_rank(task, sources)
  answer_with_citations(evidence)
```

### Typed Evidence Instead of Context Sludge

The small program hides a difficult discipline: retrieved text must not become
untyped context sludge. Each item should carry source, timestamp, access path,
rank score, and the claim it supports.

If two sources disagree, the agent should surface the conflict or acquire
higher-authority evidence. It should not smooth the contradiction into fluent
prose.

For a beginner builder, this is where retrieval becomes tool design instead of
text stuffing. A source may be:

- relevant but stale;
- authoritative but outside the caller permission boundary;
- fresh but contradicted by a higher-authority manual;
- or cheap but too vague to change the decision.

A well-designed retrieval tool returns enough metadata for the interpreter to
reason about those differences. Topic 1 (Tool Interfaces and Function Calling)
sets out the contract style that makes such metadata declarable.

## Where Retrieval Belongs

Retrieval should often precede irreversible action. Four examples make the rule
concrete:

- A coding agent should inspect relevant symbols before editing.
- A compliance agent should fetch the current rule before advising.
- A data agent should retrieve schema and sample rows before writing a query.
- A deployment agent should inspect recent incidents and service health before
  changing production.

In each case, retrieval is valuable only if it can change the rational next
move. Topic 4 (Safety Constraints and Guardrails) takes up what to do when the
next move is dangerous.

### Measuring Retrieval Quality

This also explains why retrieval quality cannot be judged by answer style
alone. Measure Recall@\(k\), nDCG, citation faithfulness, contradiction rate,
freshness error, tool-call efficiency, and end-task utility under fixed
retrieval budgets.

Then compare three policies: always-retrieve, never-retrieve, and an
uncertainty or value-of-information policy. The comparison matters because each
policy fails differently:

- always-retrieve spends tokens and time even when the state is already
  sufficient;
- never-retrieve turns stale memory into false confidence;
- a conditional policy can still be wrong if its uncertainty signal is
  miscalibrated.

If retrieval cannot buy measurable uncertainty reduction per unit latency, it is
ritual rather than reasoning.

Recall@\(k\) asks whether the needed evidence appears somewhere in the top
\(k\) retrieved items. Set \(k = 5\), and if the needed passage lands at rank 4,
Recall@5 counts it as found. nDCG, normalized discounted cumulative gain, also
cares about order: useful evidence near rank 1 counts more than the same
evidence buried near rank 20.

These metrics are not literary judgments of the final answer. They are tests of
whether the observation step gave the interpreter a fair chance to know what it
needed.

### Over-Retrieval and Under-Retrieval

The theory pays off by preventing two expensive pathologies. Over-retrieval
bloats context, slows execution, and admits distractors. Under-retrieval lets
fluent priors masquerade as evidence.

A retrieval-augmented agent is better not because it keeps more documents
nearby, but because it knows when an external document deserves to govern the
next interpreter step.

### How Composition and Memory Change the Calculation

Composition can improve this judgment or spoil it. A planner that retrieves
fresh evidence once, then passes the evidence and provenance to subtasks, can
save calls and keep the collective anchored. A planner that retrieves
redundantly for every subtask may spend its budget proving the same fact four
times.

Memory can help by remembering what was already checked. Stale memory can also
suppress retrieval that the current task plainly needs.

Retrieval is therefore most valuable for tasks with four properties together:
high uncertainty, fresh external facts, inspectable evidence, and enough
consequence that the delay is cheaper than the mistake.
