# Memory Systems, Context, and Retrieval

Keep it, throw it away, or go looking for it: an agent faces those three choices constantly, and they are as much a part of the machine as the model itself. We will treat memory as a set of decisions with costs, not as a storage bin. By the end you should be able to say why a particular fact is in the prompt right now, and what it displaced.

Deliberation, Planning, and Search extends the interpreter forward into imagined time. Memory extends it backward. It decides which parts of the past should stay available to future steps. The context window is not the agent's memory. It is the small working surface onto which memory is projected, the way a slide is projected onto a wall.

## Memory Is a Policy, Not a Filing Cabinet

A memory system is a control policy. A *policy* is a rule for choosing what to do next. This particular policy chooses among four things: retain, compress, retrieve, and forget.

A weak policy treats all past text as equally eligible for attention. Everything that happened is still lying around, so everything competes for the model's limited notice. A stronger policy asks three sharper questions:

- Which stored distinctions can actually change the next action?
- Which evidence must remain auditable, meaning a human can later trace a claim to its source?
- Which stale traces should be kept out of the active state entirely?

## Memory as Controlled State

Let the memory state be \(m_t=(w_t,e_t,s_t)\). Read that as "at step \(t\), memory consists of three stores": working, episodic, and semantic.

- Working memory \(w_t\) holds the current control state: the plan, the constraints, the last observation.
- Episodic memory \(e_t\) preserves concrete events and traces: what was run, what was returned.
- Semantic memory \(s_t\) stores distilled facts, patterns, and policies: what has generally been true.

A memory controller chooses operations
\[
u_t \in \{\texttt{write},\texttt{compress},\texttt{retrieve},\texttt{evict}\}
\]
which reads "the control action at step \(t\) is one of write, compress, retrieve, or evict". Eviction is removal from the active context. The controller picks it by
\[
u_t = \mu_\theta(m_t,h_t),
\]
read as "the controller \(\mu\), with parameters \(\theta\), chooses \(u_t\) by looking at memory state \(m_t\) and history \(h_t\)". Its aim is
\[
\max_\mu\ \mathbb{E}\!\left[\sum_t \gamma^t \big(\text{task\_utility}_t - \lambda_1\text{latency}_t - \lambda_2\text{token\_load}_t\big)\right].
\]
Read that as "choose the controller that maximizes expected discounted task usefulness, minus a price for delay and a price for tokens consumed". Here \(\mathbb{E}\) means average over runs, \(\gamma\) is a discount factor between 0 and 1 that makes later payoffs count slightly less, and \(\lambda_1,\lambda_2\) are the prices you set on latency and token load.

This is expected utility under systems constraints: retrieval is useful only when it improves decisions more than it costs [[33](../../references.md#ref-33)] [[34](../../references.md#ref-34)]. A builder sets \(\lambda_1\) and \(\lambda_2\) by measurement, not by taste. If one extra retrieval adds 400 milliseconds and 1,200 tokens but lifts task success from 71% to 79%, it earns its keep. If it lifts success from 71% to 71.4%, it does not.

### Why Today's Write Is Tomorrow's Asset

The Bellman view makes the tradeoff across time explicit:
\[
V^\star(m,h)=\max_{u}\left\{r(m,h,u)+\gamma\,\mathbb{E}[V^\star(m',h')]\right\},
\]
read as "the best achievable long-run value of being in memory state \(m\) with history \(h\) equals the best immediate reward \(r\) plus the discounted average value of wherever you land next, written \(m'\) and \(h'\)". The reward \(r\) already includes latency and token penalties [[5](../../references.md#ref-5)] [[4](../../references.md#ref-4)].

Two consequences follow. A write may be costly now but valuable later, because it preserves the one line of output the repair will need. An eviction may save context now but create future regret, because the discarded item turns out to be the missing constraint.

## Retrieval Is an Action

Retrieval is not a lookup that happens off to the side. It is an action the agent takes, with a price and a risk.

### Sparse Retrieval Counts Words

Sparse retrieval begins with counted words. The query is \(q\), the candidate document is \(d\), and a term \(t\) is one word-like unit from the query. The term frequency \(f(t,d)\) counts how often term \(t\) appears in document \(d\). The document length \(|d|\) counts the document's tokens or terms, and \(\mathrm{avgdl}\) is the average document length in the collection.

\(\mathrm{IDF}(t)\), inverse document frequency, is large for rare terms and small for common terms. It says that `segmentation fault` is usually more diagnostic than `the`. The constants \(k_1\) and \(b\) are tunable knobs. \(k_1\) controls how quickly repeated occurrences stop adding much evidence, while \(b\) controls how strongly scores are normalized for document length.

With those pieces named, BM25 scoring is
\[
\mathrm{BM25}(q,d)=\sum_{t\in q}\mathrm{IDF}(t)\frac{f(t,d)(k_1+1)}{f(t,d)+k_1\left(1-b+b|d|/\mathrm{avgdl}\right)},
\]
read as "add up, over every term in the query, that term's rarity weight times a saturating count of how often it occurs in this document". Saturation is the point worth feeling: with \(k_1=1.2\), a term appearing once already earns about half the weight it can ever reach, and the tenth occurrence adds very little.

### Dense Retrieval Compares Directions

Dense retrieval begins from a different little machine. An embedding is a vector representation of text, such as \(e_q\) for a query and \(e_d\) for a document, chosen so that related meanings tend to live near one another in vector space.

The inner product \(\langle e_q,e_d\rangle\) multiplies corresponding coordinates and sums the products. When the vectors are normalized, a larger inner product means a smaller angle between them, which often corresponds to greater semantic similarity. Dense retrieval often uses that inner-product similarity:
\[
s(q,d)=\langle e_q,e_d\rangle.
\]
A two-coordinate example makes it concrete. If \(e_q=(0.6,0.8)\) and \(e_d=(0.8,0.6)\), the inner product is \(0.6\times0.8+0.8\times0.6=0.96\); both vectors have length 1, so a score of 0.96 out of a possible 1.00 means the directions nearly agree.

### Sparse and Dense Fail Differently

These are complementary indexing geometries with different failure modes, not rival creeds [[46](../../references.md#ref-46)] [[15](../../references.md#ref-15)] [[47](../../references.md#ref-47)]. Sparse methods preserve lexical anchors and citations well. Dense methods can recover paraphrases and semantic neighbors. Hybrid systems, which run both and merge the rankings, earn their complexity when those differences reduce downstream error.

The power of dense retrieval is paraphrase. The danger is a smooth confidence that can drift away from exact filenames, citation anchors, and error strings.

### Retrieved Evidence Enters the Generator's Arithmetic

For retrieval-augmented generation, usually abbreviated RAG, evidence quality propagates into output probability:
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

### Reading the Rate-Distortion Equation

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

### A Build Failure That Two Summaries Handle Differently

For example, suppose an agent runs `python3 scripts/build_latex_pdf.py` and the command fails with one exact line: `Undefined control sequence \mathbbm at topic-03 line 87`. A progress summary that says "PDF build failed in topic 3" may have low distortion for a project manager asking whether the publication artifact exists. It has ruinous distortion for the debugging policy, because the repair depends on the exact command, the exact TeX complaint, and the exact location. Rate-distortion thinking therefore does not say "summarize aggressively." It says: choose what may be lost only after naming the task that will suffer the loss.

### Forgetting Deserves the Same Care as Remembering

Forgetting is equally active. Four kinds of debris can all distort the current state:

- stale retrieved snippets that describe an older version of the world;
- contaminated memories that recorded something false;
- duplicated summaries that make one weak claim look like several;
- obsolete user preferences the user has since changed.

Cognitive multi-store theory is useful here because it separates short-lived working contents from longer-lived episodic and semantic stores [[48](../../references.md#ref-48)]. The engineering analogue is to attach provenance, timestamp, scope, and confidence to stored items. With those four tags present, the controller can decide whether a memory belongs in the present decision.

The following pseudocode shows one pass of the memory controller. It writes auditable observations, compresses only under context pressure while keeping links back to raw evidence, retrieves only when uncertainty is actually blocking action, and evicts what has gone stale.

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

Memory should be evaluated at the decision boundary, meaning the moment where the agent commits to an action. Three examples show what "the right memory" means in practice:

- For a legal research agent, the right case is the one that changes the answer safely.
- For a code agent, the right file is the one that localizes the bug or rules out a tempting false edit.
- For a personal assistant, the right memory is current, permissioned, and relevant to the user's actual intent.

### Ablation Under a Fixed Budget

The clean comparison is an ablation under a fixed budget. An *ablation* removes one component and re-measures. Run the same task distribution three ways: with no memory beyond the prompt, then with working state only, then with retrieval-backed memory. Hold the model, tool permissions, token ceiling, and time limit steady.

Now the question becomes concrete: did memory improve task success or task-specific partial progress, or did it merely spend tokens remembering its own autobiography? Each arm can win. Working state may help on short tasks by preserving the current plan and constraints. Retrieval-backed memory may help when the relevant evidence lies outside the current window. No memory may win when stale or distracting evidence is more dangerous than forgetfulness.

### Metrics, Stress Tests, and One Self-Citing Failure

Useful measurements include retrieval precision@\(k\), latency, grounded answer faithfulness, and regret from eviction decisions under fixed token budgets. Precision@\(k\) is the fraction of the top \(k\) results that are genuinely relevant; 3 relevant hits out of 5 returned is 0.6. Regret here is the drop in outcome caused by having thrown something away.

Stress tests should include adversarial distractors and contamination injections, because long context can amplify bad evidence as easily as good evidence [[16](../../references.md#ref-16)].

One nasty composition failure is especially common. Reflection writes an inaccurate summary. Retrieval later ranks that summary highly, because it matches the task language. The agent then repeatedly promotes the false memory back into working state. The system appears consistent because it keeps citing itself. Evaluating and Debugging Reasoners counts this as a contaminated-memory failure when it labels failures by transition.

The practical target is a memory economy: spend context where it changes decisions, preserve raw evidence where audits require it, and keep yesterday's convenient summary from overruling today's observation.

## Exercise

For one agent workflow, list five things it might remember. Assign each to working, episodic, or semantic memory. Then choose one item that should be compressed, one that should be retrieved only under a specific trigger, and one that should expire.

Work it in that order. Pick a workflow you know well, such as fixing a failing test or answering support tickets. A good answer names the trigger explicitly, for example "retrieve the deployment runbook only when a command touches production", and gives the expiry a reason, for example "the user's stated deadline expires when the deadline passes". A weak answer marks everything semantic and lets nothing expire.
