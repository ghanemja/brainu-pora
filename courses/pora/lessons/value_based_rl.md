---
video: TiAXhVAZQl8 | Q-learning - Explained! | CodeEmporium | 11:54
video: wrBUkpiRvCA | Deep Q-Learning - Combining Neural Networks and Reinforcement Learning | deeplizard | 10:50
---
## Action values make acting easy

The state value $V(s)$ says how good a state is, but to choose an action from it you'd need a model to predict where each action leads. The **action value** $Q(s, a)$, the expected return after taking $a$ in $s$ and then acting well, removes that need:

$$\pi(s) = \arg\max_a Q(s, a)$$

Just pick the action with the highest Q. No model required. **Value-based RL** learns Q from experience and acts greedily on it, with some exploration mixed in.

## The Q-learning update

After each transition $(s, a, r, s')$, move $Q(s, a)$ toward the reward plus the best value available from $s'$:

$$Q(s, a) \leftarrow Q(s, a) + \alpha \Big[ r + \gamma \max_{a'} Q(s', a') - Q(s, a) \Big]$$

It's TD learning applied to action values, with a max inside. The max means it learns the value of acting **greedily**, even while the robot is actually behaving ε-greedily to explore. That makes Q-learning **off-policy**: it can learn from any data, including old experience.

## Worked example: Q-learning versus SARSA

$Q(s, a) = 2$. The robot gets $r = -1$ and lands in $s'$, where its two actions have $Q = 3$ and $Q = 5$. Use $\gamma = 0.9$ and $\alpha = 0.5$.

- **Q-learning** uses the best next action: target $= -1 + 0.9 \times 5 = 3.5$, so $Q \leftarrow 2 + 0.5 \times 1.5 = 2.75$.
- Suppose the robot then explores and takes the $Q = 3$ action. **SARSA**, the on-policy version, uses that: target $= -1 + 0.9 \times 3 = 1.7$, so $Q \leftarrow 1.85$.

Q-learning values the greedy policy; SARSA values the policy actually being followed, exploration included.

## When it's guaranteed to work

With a table holding one Q per state–action pair, Q-learning converges to the optimal $Q^*$ as long as every pair keeps getting tried and the step size $\alpha$ shrinks suitably over time. Then the greedy policy on $Q^*$ is optimal. Tables only work for small, discrete problems, though: a camera image is far too big to tabulate.

## Deep Q-networks

**DQN** replaces the table with a neural network $Q_\theta(s, a)$ and trains it on the TD error. Two tricks keep it stable:

- **Experience replay** stores transitions and trains on random minibatches, breaking the correlation between consecutive steps.
- A **target network**, a slowly updated copy, computes the target, so the target doesn't chase itself.

The max also tends to pick actions whose value is overestimated by noise; **Double DQN** reduces this bias by choosing and evaluating the next action with different networks.

> **Common mistake:** using Q-learning for continuous actions like joint torques. The max over $a'$ becomes an optimization problem at every step. Discretize coarsely, or use actor-critic methods (DDPG, SAC) built for continuous actions.
