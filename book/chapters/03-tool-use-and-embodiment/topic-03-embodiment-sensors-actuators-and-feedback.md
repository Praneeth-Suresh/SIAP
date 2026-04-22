# Embodiment: Sensors, Actuators, and Feedback

Embodiment means the agent’s actions alter a world that pushes back. Even purely software agents are embodied in infrastructures: APIs rate-limit, files mutate, humans respond, and markets move.

Classical control and RL provide the language for this feedback geometry: observations, actions, transition dynamics, and reward signals [[3](../../references.md#ref-3)] [[4](../../references.md#ref-4)].

In production systems, embodiment design includes:
1. sensor fidelity (what can be observed),
2. actuator safety (what can be changed),
3. feedback delay (when outcomes are known).

Ignoring these constraints yields an “intelligent” agent that is mathematically under-informed and operationally overconfident.
