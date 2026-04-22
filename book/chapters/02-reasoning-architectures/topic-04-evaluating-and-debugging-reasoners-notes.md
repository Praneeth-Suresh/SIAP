# Notes: Evaluating and Debugging Reasoners

## What to improve

- Add an explicit rubric for tool-call validity and grounding quality.
- Include one failure postmortem with before/after prompt and loop-policy edits.
- Add notes on statistical significance in benchmark comparisons.

## Alternative rewrite

In agent engineering, charisma is a confounder. We therefore instrument the loop, replay the trace, and score the decisions. If the system improves only when watched live, it has not improved.
