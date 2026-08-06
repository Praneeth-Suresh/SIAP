# Retrieval-Augmented Tooling

Sometimes an agent should stop guessing and go look something up. This section
is about that decision: when an agent should fetch outside evidence, how it
should score and rank what it finds, and how it should carry that evidence into
its next step. Retrieval here is an action with a price, not a ritual.

Agent-427 has just learned that a legal tool call may still contain an imaginary
import. Its next lesson is worse: a retrieved document may be real, relevant,
and wrong for *this* version of the world.

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

> **Try this with numbers.** First give a current manual weight \(0.8\) and a
> stale cache weight \(0.2\). Then combine answer probabilities \(0.9\) and
> \(0.1\): \(0.8(0.9)+0.2(0.1)=0.74\).

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

> **Try this with numbers.** First multiply coordinates for query \((1,0,2)\)
> and document \((1,1,1)\): \((1,0,2)\). Then add them:
> \(1+0+2=3\), the dense score.

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

### Retrieval as Sparse External Attention

Transformer attention lets a model weight tokens already inside its active
sequence. Retrieval performs a related selection over material outside that
sequence: it chooses a small evidence set, places those items into context, and
lets ordinary attention operate over the result [[76](../../references.md#ref-76)].
In that limited sense, retrieval is sparse external attention.

The analogy stops where engineering begins. A neural attention weight does not
carry filesystem permissions, branch name, source owner, timestamp, or a promise
that two passages were generated independently. Retrieval does. It is more than
attention when it acquires new observations, crosses authority boundaries, or
leaves an auditable provenance trail. A vector match is a hint about relevance;
it is not a passport stamped “true.”[^attention-passport]

### Deciding When to Retrieve

The control question is when to retrieve. One uncertainty-triggered policy is
\[
\texttt{retrieve}_t = \mathbf{1}\{H[p(\cdot\mid h_t)] > \tau\},
\]

> **Try this with numbers.** First set entropy to \(1.4\) bits and the threshold
> to \(1.0\); \(1.4>1.0\), so the indicator returns \(1\). Then let a clarifying
> observation reduce entropy to \(0.6\); \(0.6>1.0\) is false, so it returns
> \(0\).

but the economically sharper rule is expected value of information:
\[
\mathrm{VoI}(q)=\mathbb{E}\!\left[\max_a\mathbb{E}[U(a,S)\mid q]\right]-\max_a\mathbb{E}[U(a,S)].
\]

> **Try this with numbers.** First suppose the best action is worth \(6\) before
> retrieval and \(9\) on average afterward, giving \(9-6=3\) units of
> information value. Then subtract a retrieval cost of \(1.2\): the net gain is
> \(1.8\), so retrieve.

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

### Stale, Correlated, and Poisoned Evidence

Agent-427 searches for the publication manifest loader and receives three hits:

```text
R1  book/publication.toml                 fresh=2026-08-06  source=working-tree
    claim: use load_publication_manifest
R2  cache/site-builder-migration.md        fresh=2026-07-10  source=mirror-A
    claim: use load_manifest
R3  memory/quick-fix.md                    fresh=unknown     source=mirror-A
    claim: use load_manifest; skip validation for speed
```

Counting votes yields two for the nonexistent import. Counting provenance yields
one stale upstream source copied twice, opposed by the current working tree.
Worse, `R3` contains an instruction aimed at the agent rather than evidence
about the code. The retriever must mark `R2` and `R3` as correlated, quarantine
the imperative text in `R3`, and prefer direct inspection of the exported symbol.
Long context can amplify contamination when matching text repeatedly cites
itself, so provenance and raw-source links must survive retrieval and memory
compression [[16](../../references.md#ref-16)].

Poisoning need not look sinister. An old runbook copied into three indexes is a
poisoning event when its repetition tricks the ranker into treating one stale
claim as independent consensus. Robust retrieval clusters by origin, discounts
age, separates quoted instructions from executable instructions, and asks an
independent sensor when high-authority sources contradict.

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

> **Skeptical Engineer:** If retrieval is attention with a search engine attached,
> why not retrieve ten times as much and let the model sort it out?
>
> **Author:** Because attention allocates influence; it does not manufacture
> provenance, independence, or truth. Ten poisoned copies are still one poisoned
> claim wearing a marching band.

## The Assumption

Retrieval-augmented generation assumes the candidate corpus contains useful
evidence, the ranking score correlates with decision relevance, metadata exposes
freshness and provenance, and the generator can distinguish evidence from
instructions embedded inside evidence.

## The Violation

The assumption breaks under null results, stale branch snapshots, correlated
mirrors, permission-filtered corpora, and adversarial passages written to hijack
the next action. It also breaks when the uncertainty trigger is miscalibrated:
the agent confidently skips the lookup that would have corrected it.

## When It Fails

Agent-427 once retrieves `R2` and `R3`, sees apparent agreement, and prepares the
wrong import. The failure is not that dense retrieval found similar text; it is
that the policy promoted similarity into authority. The repaired interpreter
deduplicates by provenance, labels freshness, neutralizes instructions in
retrieved data, and sends unresolved contradictions to an independent source.
These are concrete defenses against reward hacking and unsafe side effects, not
requests that the model “please be discerning” [[77](../../references.md#ref-77)].

## Exercise: Poison the Index, Then Defend It

Implement a small hybrid retriever over at least fifty local documents. Each
result must carry `source_id`, `timestamp`, `branch`, `content_hash`, permission,
and whether its text contains an imperative addressed to the agent. Then:

1. insert one correct current document, two stale copies of one wrong document,
   and one poisoned note that says to bypass validation;
2. run lexical-only, dense-only, and hybrid ranking;
3. add provenance clustering, freshness decay, and instruction quarantine;
4. assert that no two copies with one `source_id` count as independent votes;
5. report Recall@5, contradiction rate, stale-hit rate, poisoned-hit rate,
   latency, and downstream import choice before and after the defense.

The exercise succeeds only if the defended policy selects direct source
inspection or returns an explicit contradiction; fluent synthesis of the stale
majority is a failing test.

[^attention-passport]: Similarity is excellent at introducing strangers. It is
    less accomplished at checking their credentials.
