---
video: qo355ALvLRI | Inverse Reinforcement Learning Explained | Edan Meyer | 19:59
---
## Learn the reward, not the actions

Behavior cloning copies what the expert did. **Inverse reinforcement learning** (IRL) asks why. It assumes the expert is acting near-optimally for some unknown reward $R$, finds a reward under which the demonstrations look optimal, and then runs ordinary RL or planning on that reward to get a policy.

A reward is a compact description of a goal. "Reach the goal quickly, keep well away from people" can apply in a building the expert never visited, while a cloned policy can't.

## Many rewards fit the same behavior

IRL is **ill-posed**. The reward $R = 0$ makes every behavior optimal, so it explains any demonstration and teaches nothing. Many other rewards fit too. Methods add structure to pick a sensible one.

A common choice is a reward that's linear in hand-chosen **features**, $R(s) = w^\top \phi(s)$, such as distance traveled or closeness to pedestrians. Then IRL looks for weights $w$ under which a policy that **matches the expert's average feature counts** does as well as the expert.

## Worked example: which weights explain the expert?

Features per trip: $\phi = $ (meters driven, seconds spent near pedestrians). The expert averages $(50, 2)$. Two alternative policies average $A = (40, 8)$ and $B = (55, 2.5)$.

- With $w = (-1, -10)$: the expert scores $-50 - 20 = -70$, A scores $-40 - 80 = -120$, and B scores $-55 - 25 = -80$. The expert is best, so these weights are consistent with the demonstrations.
- With $w = (-1, 0)$, which only cares about distance: A scores $-40$ and beats the expert's $-50$. That reward can't explain why the expert took the longer route, so IRL rejects it.

## Maximum entropy IRL

**Maximum entropy IRL** resolves the ambiguity with a probabilistic model of the expert. Trajectories with higher reward are exponentially more likely, $p(\tau) \propto e^{R(\tau)}$, and nothing else is assumed. This also tolerates imperfect experts, whose occasional mistakes simply become less likely trajectories. Learning follows the gradient: expert feature counts minus the feature counts expected under the current reward. When they match, the reward explains the data.

## Why bother, and what it costs

A learned reward often transfers better than a cloned policy: to new environments, different dynamics, even different robots. It's also interpretable: you can read off what the expert seemed to trade off. The price is computation. Most IRL methods solve an RL or planning problem inside every iteration of the reward search. Adversarial methods such as GAIL avoid the explicit inner loop, though they don't give you a reusable reward.

> **Common mistake:** features that leave out what the expert cares about. If drivers slow down for school zones but no feature encodes school zones, no choice of weights can explain the slowdown, and the learned reward will be wrong elsewhere to compensate.
