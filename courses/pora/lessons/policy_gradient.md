---
video: 5P7I-xPq8u8 | An introduction to Policy Gradient methods - Deep Reinforcement Learning | Arxiv Insights | 19:50
---
## Optimize the policy directly

Value-based methods learn values and derive a policy from them. **Policy gradient** methods skip that: they parameterize the policy itself, $\pi_\theta(a \mid s)$, for example a neural network that outputs a Gaussian over joint torques, and adjust $\theta$ by gradient ascent on the expected return

$$J(\theta) = \mathbb{E}_{\pi_\theta}\Big[ \sum_t \gamma^t r_t \Big]$$

This handles continuous actions naturally, can learn stochastic policies, and makes small, smooth changes to behavior, all of which suit robots.

## REINFORCE: push up what worked

The **policy gradient theorem** gives the gradient without needing a model:

$$\nabla_\theta J = \mathbb{E}\Big[ \sum_t \nabla_\theta \log \pi_\theta(a_t \mid s_t)\; G_t \Big]$$

Read it as: for each action taken, step in the direction that makes it more likely, scaled by the return $G_t$ that followed. Actions followed by high returns become more likely; actions followed by low returns become less likely. **REINFORCE** estimates this expectation by averaging over sampled episodes.

## Worked example: one REINFORCE step

A softmax policy over two actions has logits $\theta = (0, 0)$, so $\pi = (0.5, 0.5)$. The robot takes action 1 and gets return $G = 2$.

For a softmax, $\nabla_\theta \log \pi(a_1) = e_1 - \pi = (0.5, -0.5)$. With step size $\alpha = 0.1$:

$$\theta \leftarrow (0, 0) + 0.1 \times 2 \times (0.5, -0.5) = (0.1, -0.1)$$

Now $\pi(a_1) = 1 / (1 + e^{-0.2}) \approx 0.55$: action 1 became a bit more likely, as it should after a good result.

## Baselines cut the noise

Returns vary a lot, so these gradient estimates are very noisy. If every return lies between 90 and 110, every action gets pushed up, the good ones only slightly more than the bad. Subtracting a **baseline** $b(s)$ fixes this without biasing the gradient:

$$\nabla_\theta J = \mathbb{E}\big[ \nabla_\theta \log \pi_\theta(a_t \mid s_t)\, (G_t - b(s_t)) \big]$$

With $b(s) = V(s)$, the weight becomes the **advantage** $A(s, a) = Q(s, a) - V(s)$: how much better this action was than usual. Below-average actions are now pushed down.

## Actor-critic and PPO

**Actor-critic** methods learn the baseline too. A **critic** $V_w(s)$ is trained by TD learning, and its TD error $\delta = r + \gamma V_w(s') - V_w(s)$ serves as the advantage estimate for the **actor** $\pi_\theta$. Updates no longer wait for the episode to end.

**PPO** adds a guard: it clips the probability ratio $\pi_{\text{new}}/\pi_{\text{old}}$ to a range such as $[0.8, 1.2]$, so no update can change the policy too much at once. It's a common default for robot locomotion.

> **Common mistake:** too large a step size. A single big update can make the policy nearly deterministic on a bad action, and then it never samples anything else to learn from. Keep steps small, or use PPO-style clipping.
