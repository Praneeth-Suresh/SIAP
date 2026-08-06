# Notes: Memory Systems, Context, and Retrieval

## What to improve

- Add a retrieval quality metric table (precision@k, groundedness, latency).
- Add examples of harmful memory contamination.
- Add pseudocode for retrieval-policy hooks in the loop interpreter.

## Alternative rewrite

Context windows are weather; memory systems are climate. A serious agent survives beyond the current prompt by deciding what history deserves permanence and what should evaporate without regret.

## Pass 1 - Migrated ideas from current main topic

The current topic models memory as policy over working, episodic, and semantic stores \(m_t=(w_t,e_t,s_t)\), with controller action \(u_t\in\{\texttt{write},\texttt{compress},\texttt{retrieve},\texttt{evict}\}\) chosen by \(u_t=\mu_\theta(m_t,h_t)\). Its objective maximizes discounted task utility while penalizing latency and token load, and its braid links cognitive multi-store theory, rate-distortion thinking, and modern sparse/dense retrieval plus RAG evidence flow [[48](../../references.md#ref-48)] [[35](../../references.md#ref-35)] [[46](../../references.md#ref-46)] [[47](../../references.md#ref-47)] [[14](../../references.md#ref-14)] [[15](../../references.md#ref-15)].

## Pass 1 - Storyline outline (paragraph-by-paragraph)

Paragraph 1 opens with scarcity: the context window is a tiny stage, and memory policy is the casting director deciding who gets to speak.

Paragraph 2 introduces memory strata as labor specialization, where working memory handles immediate control, episodic memory preserves events, and semantic memory stores compressed structure [[48](../../references.md#ref-48)].

Paragraph 3 shifts to decision economics: each retrieval or write is an expected-utility trade between downstream accuracy and immediate compute/token cost [[33](../../references.md#ref-33)] [[34](../../references.md#ref-34)].

Paragraph 4 braids compression and retrieval: rate-distortion says what fidelity is worth paying for, while indexing/reranking says how quickly and reliably the right evidence can be recovered [[35](../../references.md#ref-35)] [[46](../../references.md#ref-46)] [[15](../../references.md#ref-15)].

Paragraph 5 closes with resilience and contamination control, showing that forgetting is not negligence but active safety policy when stale or poisoned context threatens action quality.

## Pass 2 - Research synthesis: equations, theories, and connective tissue

Equation stack for rewrite depth: memory-control Bellman form \(V^\star(m,h)=\max_u\{r(m,h,u)-\lambda_1\ell_{\text{lat}}-\lambda_2\ell_{\text{tok}}+\gamma\,\mathbb{E}[V^\star(m',h')]\}\) to formalize long-run memory policy [[5](../../references.md#ref-5)] [[4](../../references.md#ref-4)]; expected utility of retrieval \(EU(\texttt{retrieve})=\mathbb{E}[U(a^\star\mid m\oplus \hat d)]-c_{\text{retrieve}}\) to decide if memory access is worth it [[33](../../references.md#ref-33)] [[34](../../references.md#ref-34)]; rate-distortion program \(R(D)=\min_{p(\hat x|x):\mathbb{E}[d(X,\hat X)]\le D} I(X;\hat X)\) for principled compression [[35](../../references.md#ref-35)]; sparse scoring via BM25 \(\text{BM25}(q,d)=\sum_{t\in q}\text{IDF}(t)\frac{f(t,d)(k_1+1)}{f(t,d)+k_1(1-b+b|d|/\text{avgdl})}\) and dense retrieval score \(s(q,d)=\langle e_q,e_d\rangle\) to connect indexing regimes [[46](../../references.md#ref-46)] [[15](../../references.md#ref-15)] [[47](../../references.md#ref-47)]; and end-to-end RAG likelihood \(p(y|x)\approx \sum_{d\in\mathcal{D}_k}p_\eta(d|x)\,p_\theta(y|x,d)\) to show how retrieval quality propagates into generation quality [[14](../../references.md#ref-14)]. The key connective claim: memory quality is not "more tokens," but controlled information flow from acquisition to compression to action.

## Additional alternate approaches for this rewrite

1. Present the topic as a library operations story: acquisitions, cataloging, circulation, and deaccessioning mapped to write/retrieve/compress/evict.
2. Build around a failure case where one contaminated memory entry corrupts several downstream tool calls, then repair it with policy constraints.
3. Use a legal brief style in which each retrieved document must justify its relevance and reliability before entering context.
4. Anchor the exposition around one persistent assistant persona that improves over sessions by disciplined memory curation rather than prompt bloat.

## Editor-Rewrite Alternative Before Primary Synthesis

Replace the filing cabinet with a war room. Agent-427 retrieves `service.yaml` from `main` while standing on `legacy-v2`, whose service is configured in `service.toml`; walk through the wrong retrieval, wrong edit, failed parser, seductive summary, and repair line by line. Treat retrieval as sparse attention over an external corpus, then show where that analogy breaks: retrieval changes the available evidence, provenance, latency, and attack surface. Preserve the three-store abstraction as a useful map, but surround it with interference, consolidation, and deliberate forgetting. Include a complete self-citing contamination trace in which a false reflection becomes semantic memory, gets retrieved as evidence, and earns confidence by citing its own descendants. End with an implementable memory controller and a rate-distortion experiment.
