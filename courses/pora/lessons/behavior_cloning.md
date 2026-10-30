---
video: tbLaFtYpWWU | CS 285: Lecture 2, Imitation Learning. Part 1 | RAIL | 24:48
---
## Imitation as supervised learning

The simplest way to teach a robot a skill is to show it. Record an expert, such as a person teleoperating a robot arm, as pairs of state and action $(s_i, a_i)$. Then train a policy to predict the expert's action from the state, exactly like any supervised learning problem:

$$\min_\theta \sum_i \big\| \pi_\theta(s_i) - a_i \big\|^2 \quad \text{or} \quad \min_\theta \sum_i -\log \pi_\theta(a_i \mid s_i)$$

That's **behavior cloning** (BC). The first loss fits actions directly; the second fits a probability distribution over actions.

## Why it's attractive

BC needs **no reward function**, which is often the hardest part of RL to design. It needs **no interaction** during training: the policy learns offline from logged data, so there are no risky trials on hardware. And it uses the ordinary deep learning toolkit. Given enough good demonstrations of the situations the robot will face, BC works remarkably well, and much of today's robot manipulation learning starts with it.

## Multimodal demonstrations

Experts don't always agree. Facing an obstacle, half the demonstrations pass it on the left and half on the right. Both are fine. But a policy trained with squared error predicts the **average** action, and the average of "left" and "right" is straight ahead, into the obstacle.

Fixes model a full distribution over actions instead of one answer: **mixture** models, **discretized** actions with a classifier, or **diffusion policies**, which can represent several distinct modes.

## Worked example: averaging two good answers

Demonstrations steer $+20°$ half the time and $-20°$ the other half. Compare the squared-error loss of two predictions:

- Predict $+20°$: errors are $0$ and $40$, so the mean loss is $(0 + 1600)/2 = 800$.
- Predict $0°$: errors are $20$ and $20$, so the mean loss is $(400 + 400)/2 = 400$.

Squared error prefers $0°$, the one action no expert ever took. The loss isn't broken; it's answering a different question ("what's the mean action?") than the one you meant.

## What BC doesn't handle

BC learns only from states the expert visited. Once the policy makes a small mistake, it reaches a state the expert never showed, makes a bigger mistake there, and drifts further. That's **covariate shift**, the subject of the next lesson, and the main reason BC policies that look good on held-out data can fail when run on the robot.

> **Common mistake:** the expert seeing more than the robot. If the teleoperator watched the whole room but the robot only has a wrist camera, the right action may not be predictable from the robot's input at all. Record demonstrations using only what the robot will observe.
