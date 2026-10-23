---
source: pora
chapter: 18
layer: L
kind: learned
tags: [pora, robot-autonomy, learned]
---
# Model-based RL & system ID

Learn a dynamics model from data and plan or control with it, connecting learning back to the control chapters.

<!-- pora:begin -->
## In Principles of Robot Autonomy

- Read: [Chapter 18: Reinforcement Learning](https://porabook.com/book/reinforcement-learning/)
- Stack layer: Decisions & learning · learned
- Watch: [AA203 lecture 13: Intro to Learning, System Identification and Adaptive Control](https://youtu.be/RtJSHiqOdgQ)
- Watch: [AA203 lecture 19: Model-based RL and Conclusions](https://youtu.be/ZXMThMHFD_w)

### Key ideas

1. Model-based RL fits a dynamics model x_t+1 ≈ f_θ(x_t, u_t) from data, e.g. by least squares for linear systems (system identification) or with neural nets, then plans or controls with it.
2. It is typically far more sample-efficient than model-free RL, since each transition trains a reusable model; planning can use MPC, iLQR, or simulated rollouts.
3. Model errors get exploited by the planner, which seeks regions where the model is wrong; ensembles, uncertainty estimates, short horizons, and replanning with new data mitigate this.

Try it: Simulate x_t+1 = A x_t + B u_t + noise for a 2-D system with random inputs, then recover A and B by least squares on stacked [x_t, u_t] and compare with the truth for 20 and 200 samples.

Needs first: [[reinforcement_learning]], [[State_space_model]]

Related: [[Model_predictive_control]]

Part of [[Principles_of_Robot_Autonomy]]. Summary and study notes from the unofficial PoRA Atlas; the book is the authoritative reference.
<!-- pora:end -->
