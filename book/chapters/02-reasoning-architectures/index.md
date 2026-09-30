# Chapter 2: Reasoning Architectures

At 3:47 AM on a Thursday, Agent-427 watches the CI pipeline turn red. The message says `signature verification failed: invalid timestamp`. The timestamp is valid. The message is a lie produced by an expired cache entry, the authentication maintainer left three months ago, and the runbook links to documentation that now returns `404 Not Found`. This is an unkind hour in which to discover that fluent text is not reasoning.

Welcome to Part 2's descent into the machinery. Part 0 showed an institution in motion. Part 1 asked how a single agent survives it. Now we open the casing and ask what must happen between observation and consequence: which thoughts are legal, which futures deserve simulation, which memories may enter the room, and which evidence earns a verdict.

## Reasoning Is an Interpreter, Not a Mood

Chapter 1 gave Agent-427 the basic cycle: observe, update belief, choose a governed action, execute, and learn from the result. Chapter 2 installs a smaller interpreter inside that cycle. The inner machine can think, plan, retrieve, and criticize before the outer machine touches a filesystem, an API, or somebody's regrettably production-shaped database.

That distinction is not decorative. Internal steps consume time and tokens. Retrieved memories can poison the state. Plans can become obsolete while they are being admired. A reflection can cite another reflection until fiction develops an impressive bibliography. Reasoning architecture is therefore the control of internal transitions, not an invitation to produce more monologue.

::: {.reader-question}
> **Skeptical Engineer:** Isn't this just a prompt with extra bureaucracy?
>
> **Author:** Only if the guards are prose. When a schema rejects an invented import, a budget stops a search, provenance excludes the wrong branch, and a replay identifies the transition that caused harm, the bureaucracy has become a machine. Civilization has been built on less.

:::

## Agent-427 Enters the War Room

The 3:47 failure does not end when the guard rejects the invented import. It grows more instructive with every topic, because each repair hands Agent-427 a new internal power and each power arrives with its own way to fail.

First the reasoning loop becomes an interpreter with labeled steps and executable invariants, so that the imaginary import can be caught as a language error rather than discovered as an outage. Then the agent learns to search over futures—and to notice that the world has changed while it was searching. By 4:06 it has memory, and memory turns out to be a war room in which evidence competes for scarce attention and a confident file from the wrong branch can win. Finally every trajectory goes before **The Verdict**, where Utility, Safety, and Calibration judge separately, because a correct final answer cannot pardon an unsafe path to it. The chapter's diagrams follow the same route: the interpreter loop, the memory war room, and the Verdict's three benches.

These mechanisms are options, not a royal procession. A one-line rename rarely deserves Monte Carlo tree search. A production migration usually deserves more than vibes and a hopeful `git push`.[^chapter2-ceremony] The recurring question is whether a pattern improves success, partial progress, efficiency, safety, or governability enough to pay its own rent.

[^chapter2-ceremony]: If your agent convenes a five-agent constitutional assembly to rename `x` to `count`, the architecture has achieved self-parody.

## Topics

1. [Reasoning Loops as Interpreters](topic-01-reasoning-loops-as-interpreters.md)
2. [Deliberation, Planning, and Search](topic-02-deliberation-planning-and-search.md)
3. [Memory Systems, Context, and Retrieval](topic-03-memory-systems-context-and-retrieval.md)
4. [Evaluating and Debugging Reasoners](topic-04-evaluating-and-debugging-reasoners.md)
