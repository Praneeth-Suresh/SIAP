# Memory Systems, Context, and Retrieval

Planning extends the interpreter forward in imagined time. Memory extends it backward by deciding which parts of the past should remain available to future steps. The context window is not the agent's memory; it is the small working surface onto which memory is projected.

A memory system is therefore a control policy. It decides what to retain, compress, retrieve, and forget. A weak policy treats all past text as equally eligible for attention. A stronger policy asks which stored distinctions can change the next action, which evidence must remain auditable, and which stale traces should be kept out of the active state.

## Memory as Controlled State

Let memory state be \(m_t=(w_t,e_t,s_t)\): working, episodic, and semantic stores. Working memory holds the current control state. Episodic memory preserves concrete events and traces. Semantic memory stores distilled facts, patterns, and policies. A memory controller chooses operations
\[
u_t \in \{\texttt{write},\texttt{compress},\texttt{retrieve},\texttt{evict}\}
\]
by
\[
u_t = \mu_\theta(m_t,h_t),
\]
to optimize
\[
\max_\mu\ \mathbb{E}\!\left[\sum_t \gamma^t \big(\text{task\_utility}_t - \lambda_1\text{latency}_t - \lambda_2\text{token\_load}_t\big)\right].
\]
This is expected utility under systems constraints: retrieval is useful only when it improves decisions more than it costs [[33](../../references.md#ref-33)] [[34](../../references.md#ref-34)].

The Bellman view makes the intertemporal tradeoff explicit:
\[
V^\star(m,h)=\max_{u}\left\{r(m,h,u)+\gamma\,\mathbb{E}[V^\star(m',h')]\right\},
\]
where \(r\) already includes latency and token penalties [[5](../../references.md#ref-5)] [[4](../../references.md#ref-4)]. A write may be costly now but valuable later; an eviction may save context now but create future regret.

## Retrieval Is an Action

Sparse retrieval begins with counted words. The query is \(q\), the candidate document is \(d\), and a term \(t\) is one word-like unit from the query. The term frequency \(f(t,d)\) counts how often term \(t\) appears in document \(d\). The document length \(|d|\) counts the document's tokens or terms, and \(\mathrm{avgdl}\) is the average document length in the collection. \(\mathrm{IDF}(t)\), inverse document frequency, is large for rare terms and small for common terms; it says that `segmentation fault` is usually more diagnostic than `the`. The constants \(k_1\) and \(b\) are tunable knobs: \(k_1\) controls how quickly repeated occurrences stop adding much evidence, while \(b\) controls how strongly scores are normalized for document length. With those pieces named, BM25 scoring is
\[
\mathrm{BM25}(q,d)=\sum_{t\in q}\mathrm{IDF}(t)\frac{f(t,d)(k_1+1)}{f(t,d)+k_1\left(1-b+b|d|/\mathrm{avgdl}\right)},
\]
Dense retrieval begins from a different little machine. An embedding is a vector representation of text, such as \(e_q\) for a query and \(e_d\) for a document, chosen so that related meanings tend to live near one another in vector space. The inner product \(\langle e_q,e_d\rangle\) multiplies corresponding coordinates and sums the products. When the vectors are normalized, a larger inner product means a smaller angle between them, which often corresponds to greater semantic similarity. Dense retrieval often uses that inner-product similarity:
\[
s(q,d)=\langle e_q,e_d\rangle.
\]
These are complementary indexing geometries with different failure modes, not rival creeds [[46](../../references.md#ref-46)] [[15](../../references.md#ref-15)] [[47](../../references.md#ref-47)]. Sparse methods preserve lexical anchors and citations well; dense methods can recover paraphrases and semantic neighbors. Hybrid systems earn their complexity when those differences reduce downstream error.
The power of dense retrieval is paraphrase; the danger is a smooth confidence that can drift away from exact filenames, citation anchors, and error strings.

For retrieval-augmented generation, evidence quality propagates into output probability:
\[
p(y\mid x)\approx \sum_{d\in\mathcal{D}_k} p_\eta(d\mid x)\,p_\theta(y\mid x,d),
\]
so poor retrieval is injected into generation dynamics rather than appended as a harmless side note [[14](../../references.md#ref-14)]. The useful evaluation question is not "did the retriever find similar text?" but "did the retrieved evidence move the action ranking in the right direction?"

In this equation, \(\mathcal{D}_k\) is the top-\(k\) evidence set returned by
the retriever. The subscript \(k\) means the system keeps only a bounded number
of documents, because context, latency, and attention are finite. The term
\(p_\eta(d\mid x)\) is the retriever's probability or normalized score for
document \(d\) given query context \(x\); \(\eta\) names the retriever's
parameters. The term \(p_\theta(y\mid x,d)\) is the generator's probability of
answer \(y\) after seeing \(x\) and document \(d\); \(\theta\) names the
generator's parameters. The approximation sign acknowledges that production
systems usually approximate the full document sum with a short ranked list.

## Compression and Forgetting

Compression policy is an information-theoretic trade:
\[
R(D)=\min_{p(\hat x|x):\mathbb{E}[d(X,\hat X)]\le D} I(X;\hat X),
\]
which says to spend bitrate only on distinctions that matter under an accepted distortion level [[35](../../references.md#ref-35)]. In agent memory, the distortion measure should be task-relative. A summary that drops exact command output may be acceptable for narrative progress tracking and unacceptable for debugging a build failure.

Read \(X\) as the original trace or memory item and \(\hat X\) as its compressed
version. The conditional distribution \(p(\hat x\mid x)\) describes the
compressor: given original item \(x\), it may produce summary \(\hat x\). The
distortion \(d(X,\hat X)\) measures what the summary loses for the task at hand,
and the constraint \(\mathbb{E}[d(X,\hat X)]\le D\) says the average loss must
stay below tolerance \(D\). The mutual information \(I(X;\hat X)\) measures how
much information about the original survives in the summary. Thus \(R(D)\) is
the smallest amount of retained information needed to keep distortion at or
below \(D\). The equation is permission to forget only after specifying what
kind of forgetting the task can survive.

For example, suppose an agent runs `python3 scripts/build_latex_pdf.py` and the command fails with one exact line: `Undefined control sequence \mathbbm at topic-03 line 87`. A progress summary that says "PDF build failed in topic 3" may have low distortion for a project manager asking whether the publication artifact exists. It has ruinous distortion for the debugging policy, because the repair depends on the exact command, the exact TeX complaint, and the exact location. Rate-distortion thinking therefore does not say "summarize aggressively." It says: choose what may be lost only after naming the task that will suffer the loss.

Forgetting is equally active. Stale retrieved snippets, contaminated memories, duplicated summaries, and obsolete user preferences can all distort the current state. Cognitive multi-store theory is useful here because it separates short-lived working contents from longer-lived episodic and semantic stores [[48](../../references.md#ref-48)]. The engineering analogue is to attach provenance, timestamp, scope, and confidence to stored items so the controller can decide whether a memory belongs in the present decision.

```text
function MEMORY_STEP(sigma, uncertainty, phase):
    if new_observation_is_auditable(sigma):
        write(episodic, raw_observation, provenance)

    if context_pressure_high(sigma):
        compress(trace, preserve_links_to_raw_evidence)

    if uncertainty_blocks_action(uncertainty):
        docs <- retrieve(query_from_state(sigma), filters=scope_and_time)
        sigma <- add_to_working_memory(rerank(docs))

    evict_items(active_context, stale_or_low_value)
    return sigma
```

This sketch turns memory into part of the interpreter rather than an ungoverned transcript cache.

## Measuring Memory Policy

Memory should be evaluated at the decision boundary. For a legal research agent, the right case is the one that changes the answer safely. For a code agent, the right file is the one that localizes the bug or rules out a tempting false edit. For a personal assistant, the right memory is current, permissioned, and relevant to the user's actual intent.

The clean comparison is an ablation under a fixed budget. Run the same task distribution with no memory beyond the prompt, then with working state only, then with retrieval-backed memory. Hold the model, tool permissions, token ceiling, and time limit steady. Now the question becomes concrete: did memory improve task success or task-specific partial progress, or did it merely spend tokens remembering its own autobiography? Working state may help on short tasks by preserving the current plan and constraints. Retrieval-backed memory may help when the relevant evidence lies outside the current window. No memory may win when stale or distracting evidence is more dangerous than forgetfulness.

Useful measurements include retrieval precision@\(k\), latency, grounded answer faithfulness, and regret from eviction decisions under fixed token budgets. Stress tests should include adversarial distractors and contamination injections, because long context can amplify bad evidence as easily as good evidence [[16](../../references.md#ref-16)]. One nasty composition failure is especially common: reflection writes an inaccurate summary, retrieval later ranks that summary highly because it matches the task language, and the agent repeatedly promotes the false memory back into working state. The system then appears consistent because it keeps citing itself. The practical target is a memory economy: spend context where it changes decisions, preserve raw evidence where audits require it, and keep yesterday's convenient summary from overruling today's observation.

## Exercise

For one agent workflow, list five things it might remember. Assign each to working, episodic, or semantic memory. Then choose one item that should be compressed, one that should be retrieved only under a specific trigger, and one that should expire.
