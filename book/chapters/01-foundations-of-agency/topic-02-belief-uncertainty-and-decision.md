# Belief, Uncertainty, and Decision

Agentic systems rarely act with complete state information. The practical object is not certainty but calibrated belief: a probability distribution over plausible world states [[4](../../references.md#ref-4)] [[7](../../references.md#ref-7)].

This immediately reframes prompt engineering as decision theory. A prompt does not merely elicit text; it changes posterior belief and therefore downstream policy quality [[5](../../references.md#ref-5)].

Bayesian framing is especially useful for tool-using agents. Retrieval queries, API calls, and test executions can be interpreted as information-gathering actions whose value depends on uncertainty reduction and action cost [[6](../../references.md#ref-6)] [[14](../../references.md#ref-14)].

The design takeaway is blunt: systems that do not model uncertainty explicitly tend to overconfidently fail in exactly the regimes where autonomy matters most.
