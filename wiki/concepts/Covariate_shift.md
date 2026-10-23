---
source: pora
chapter: 19
layer: L
kind: learned
tags: [pora, robot-autonomy, learned]
---
# Covariate shift

A cloned policy makes small errors, drifts into states the expert never showed, and errors compound. Understanding this explains most imitation learning failures and the fixes for them.

<!-- pora:begin -->
## In Principles of Robot Autonomy

- Read: [Chapter 19: Imitation Learning](https://porabook.com/book/imitation-learning/)
- Stack layer: Decisions & learning · learned
- Watch: [AA203 lecture 15: Imitation Learning](https://youtu.be/udHX5Auj7ik)

### Key ideas

1. Training states come from the expert's distribution, but at test time the learner visits states induced by its own policy; small mistakes push it into states never seen in training.
2. Errors compound: with per-step error ε, behavior cloning's expected cost can grow like O(ε T²) over horizon T, versus O(ε T) when trained on the learner's own state distribution.
3. DAgger fixes this by rolling out the learner, having the expert label the visited states, aggregating the data, and retraining; noise injection during demos (DART) also broadens coverage.

Try it: Simulate a 1-D lane-keeping task where the expert action is -k x; train a policy only on near-zero x, roll it out with small noise, and compare drift with a DAgger loop that adds expert-labeled visited states.

Needs first: [[Behavior_cloning]]

Part of [[Principles_of_Robot_Autonomy]]. Summary and study notes from the unofficial PoRA Atlas; the book is the authoritative reference.
<!-- pora:end -->
