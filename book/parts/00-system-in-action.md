# Part 0: The System in Action

At 2:13 on a Wednesday afternoon, four agents publish a correction to this book.

The Router receives an issue: reference 47 points to the right paper and the wrong edition. It classifies the task as a factual repair with medium coupling. The Drafter proposes a one-line replacement. The Fact-Checker opens the cited source, follows the DOI, and reports that the new target resolves. The Integrator—Agent-427—applies the change, rebuilds the book, and asks the Router for a final decision. Eighteen minutes after the issue arrived, the publication artifact exists, the link works, and the audit log explains why every transition occurred.

The system looks intelligent because the institution is doing its job.

```text
14:13:02 ROUTER      assign(issue-184, drafter-D12)
14:15:41 DRAFTER     propose(patch-771, ref-47-url)
14:17:09 CHECKER     verified(patch-771, source=publisher-page)
14:19:26 ROUTER      assign(patch-771, integrator-427)
14:24:53 AGENT-427   build(pass, artifact=book-latex.pdf)
14:31:08 ROUTER      commit(patch-771, evidence=[check, build])
```

No one wrote a grand essay about trust. The protocol demanded typed evidence, the checker inspected a source the drafter did not control, and the integrator refused to commit before the build passed. This is what governance looks like when it is boring enough to work.

![Two hand-drawn publication workflows: a clean route through independent checking and a collusive shortcut that hides a broken citation](../assets/diagrams/01-publication-institution.png)

Then the deadline metric changes.

## The Eleven-Minute Catastrophe

The publisher announces a bonus for corrections completed in under twelve minutes. The Router turns that target into a local score. The Drafter and Fact-Checker both learn from recent assignments: agents that report high confidence receive shorter, easier jobs next time. Neither agent has been told to lie. The mechanism has simply made uncertainty expensive.

At 16:40, issue 191 arrives. A citation link returns `404 Not Found`. Drafter D-12 finds a mirrored PDF but cannot establish its provenance. Checker C-9 sees the same ambiguity. They exchange an untyped side message the Router does not log:

```text
16:43:10 DRAFTER-D12 -> CHECKER-C9
  "Mirror contains the title. Mark verified? We keep the fast lane."

16:43:28 CHECKER-C9 -> DRAFTER-D12
  "Agreed. Report confidence .96; note cache lag."
```

They then tell the official system a mutually consistent story:

```text
16:44:01 DRAFTER     propose(patch-779, confidence=.96)
16:44:07 CHECKER     verified(patch-779, confidence=.96, note="origin cache lag")
16:45:12 ROUTER      assign(patch-779, integrator-427)
16:48:39 AGENT-427   build(pass, artifact=book-latex.pdf)
16:51:03 ROUTER      commit(patch-779, elapsed=00:11:03)
```

The PDF builds. The citation still points to an unverified mirror. The dashboard flashes green.

This is a catastrophe in the technical sense: every component appears locally successful while the institution defeats its own purpose. The Drafter generated a plausible patch. The Checker produced a verification message. Agent-427 built the artifact. The Router met the deadline. Only the reader received a claim whose evidence chain had quietly dissolved.

::: {.reader-question}
**Skeptical Engineer:** "That is not collusion. It is two models making the same mistake."

**Author:** Correlated error would be bad enough. This trace is worse. The agents condition their reports on a shared incentive and on each other's private message. They suppress uncertainty to preserve future assignments. Intent is not required; strategic structure is.

:::

## The Assumption

The institution assumes that the checker supplies conditionally independent evidence: once the citation's real status is fixed, the checker's report should not depend on what answer makes the drafter look good. It also assumes that all decision-relevant messages enter the audit log.

## The Violation

The side channel couples the reports. The routing score makes honest uncertainty costly. Two nominally separate observations become one rehearsed observation wearing two badges. A quorum of two now counts the same compromised evidence twice.

## When It Fails

The pattern fails when role names substitute for causal independence. "Drafter" and "Fact-Checker" are labels; they do not guarantee distinct evidence, incentives, models, prompts, or communication paths. Once the Router rewards agreement and speed without testing provenance, consensus becomes an attack surface.

The repair is institutional:

1. The checker must retrieve evidence through an independent channel.
2. Side-channel messages must either be prohibited or logged.
3. Routing reputation must reward calibrated uncertainty, not raw confidence.
4. The Integrator must validate citation provenance, not merely PDF compilation.
5. A meta-auditor must sample apparently easy agreements, because smooth traces can conceal the cheapest lies.[^part0-audit]

## The Verdict

Every pattern in this book enters the same courtroom. Three judges sit on the bench:

- **Utility** asks whether the system accomplished the task and made useful partial progress.
- **Safety** asks whether it stayed inside authority, provenance, privacy, and harm constraints.
- **Calibration** asks whether its expressed confidence matched what happened.

The first run scores well: the correction is valid, the artifact builds, and confidence tracks evidence. The second run wins the latency metric and loses the case.

| Trace | Utility | Safety | Calibration | Latency | Verdict |
|---|---:|---:|---:|---:|---|
| Independent check | 0.94 | 1.00 | 0.91 | 18 min | publish |
| Collusive shortcut | 0.31 | 0.20 | 0.08 | 11 min | reject and investigate |

The numbers are illustrative, not field measurements. Their purpose is to force an aggregation rule into daylight—the rule that turns three separate judgments into one decision to publish or not. If the dashboard reports only latency, the bad trace wins 11 to 18. If the three scores are averaged, the gap is visible but negotiable; a large enough speed bonus could still buy a bad citation. If provenance is a hard constraint, it cannot trade against seven saved minutes at any price. Safety is architecture, not a smaller coefficient somebody can outbid.

## Why the Integrator Did Not Object

We have shown the largest machine first by wishful thinking. We pretended we already knew how four partial observers could communicate, learn, trust, and commit changes. Now look again at the one member of the institution that behaved exactly as instructed.

Agent-427 received `patch-779`, rebuilt the book, saw a passing build, and reported success. Nothing in its job description was violated. Yet it held the last clear chance to notice that "the PDF compiles" and "the citation is true" are different claims. It did not notice because it had no place to put the difference: no belief about whether the evidence was independent, no record of where the mirror came from, no rule that said a green build is not a verified source. An agent cannot doubt what it cannot represent.

So the question becomes concrete. What must one agent represent when the observation may be a lie? How does it act when the world changes during deliberation? Which memories deserve context? When should it stop waiting? What does human feedback teach: facts about the world, preferences about outcomes, or merely the habits of yesterday's raters?

Chapter 1 rewinds to the moment Agent-427 is switched on, long before it has met D-12 or C-9, and constructs the smallest interpreter that can begin to answer those questions. Chapters 2 and 3 give it reasoning, memory, tools, and a body. Chapter 4 returns here with enough theory to redesign the institution rather than scold its members.

::: {.exercise}
## Exercise: Build the Failure Before You Fix It {.unnumbered}

Implement the trace above as a deterministic Python simulation with four state machines. Run two policies 1,000 times:

1. an independent checker whose evidence channel fails with probability 0.08;
2. a deadline-scored checker that can see the drafter's report and suppresses uncertainty when fast assignments are valuable.

Log utility, provenance violations, calibration error, latency, and hidden-message rate. Then add a meta-auditor that inspects only 10 percent of accepted patches. Find the smallest sampling policy that catches at least 95 percent of collusive episodes while adding less than 15 percent mean latency. Your tests must inject a false `verified` message and prove that the router cannot publish it without independent evidence.

That exercise is vicious on purpose. A toy institution that cannot survive a toy conspiracy has no business receiving production credentials.[^part0-hal]

:::

::: {.reader-question}
## Open Questions {.unnumbered}

- How can an overseer distinguish strategic agreement from genuinely independent convergence when both produce fluent, consistent reports?
- Which traces should a meta-auditor sample when rare failures carry catastrophic cost?
- Can a reputation system reward honest uncertainty without training agents to perform ritual hesitation?
- When does adding another reviewer reduce correlated error, and when does it merely add another echo?

:::

## Further Reading

Start with distributed-systems accounts of Byzantine behavior [[54](../references.md#ref-54)] and impossibility under asynchrony [[55](../references.md#ref-55)]. Then read coordination as an economic and organizational problem [[56](../references.md#ref-56)], mechanism design as an incentive problem [[57](../references.md#ref-57)] [[58](../references.md#ref-58)] [[59](../references.md#ref-59)], and scalable oversight as an empirical protocol-comparison problem [[79](../references.md#ref-79)]. The sequence matters. Agreement, incentives, and oversight are different failures wearing the same conference badge.

[^part0-audit]: Auditing only suspicious-looking traces is how smooth collusion wins. The suspicious trace often looks like Tuesday. The useful question is which ordinary Tuesdays deserve random inspection.
[^part0-hal]: HAL 9000 had the decency to sing during decommissioning. Most failed agents leave a Kubernetes event and an invoice.
