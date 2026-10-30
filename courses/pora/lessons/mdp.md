---
video: 4Fqt2Nk2lhY | Markov Decision Process (MDP) - 5 Minutes with Cyrill | Cyrill Stachniss | 3:36
video: 2iF9PRriA7w | Markov Decision Processes - Computerphile | Computerphile | 17:42
---
## The five pieces of an MDP

A **Markov decision process** is the standard model for deciding under uncertainty, one step at a time. It has five parts, $(S, A, P, R, \gamma)$:

- **States** $S$: the situations the robot can be in.
- **Actions** $A$: what it can do.
- **Transitions** $P(s' \mid s, a)$: the probability of landing in $s'$ after doing $a$ in $s$. A wheel may slip, a grasp may fail.
- **Reward** $R(s, a)$: how good it is to do $a$ in $s$. Costs are just negative rewards.
- **Discount** $\gamma \in [0, 1)$: how much less a reward counts for each step it's delayed.

## The Markov property

The model assumes the next state depends only on the current state and action, not on how you got there:

$$P(s_{t+1} \mid s_t, a_t, s_{t-1}, a_{t-1}, \dots) = P(s_{t+1} \mid s_t, a_t)$$

The payoff is huge: the best action can depend on the current state alone. So a solution is a **policy** $\pi(s)$, a rule mapping each state to an action, rather than a plan that depends on the entire history.

## What the robot is trying to maximize

The goal is the expected **discounted return**:

$$G_t = r_t + \gamma\, r_{t+1} + \gamma^2 r_{t+2} + \dots = \sum_{k=0}^{\infty} \gamma^k\, r_{t+k}$$

Discounting keeps infinite sums finite: a reward of 1 every step forever is worth $1/(1 - \gamma)$, which is 10 for $\gamma = 0.9$. It also sets the robot's effective horizon, roughly $1/(1 - \gamma)$ steps.

## Worked example: how discount changes a decision

A robot can reach a charger in four steps. Each step costs $-1$, and arriving earns $+10$, so the rewards are $(-1, -1, -1, +10)$.

- With $\gamma = 0.9$: $G = -1 - 0.9 - 0.81 + 10 \times 0.729 = 4.58$. Going is worth it.
- With $\gamma = 0.5$: $G = -1 - 0.5 - 0.25 + 10 \times 0.125 = -0.5$. Going looks worse than doing nothing.

Same task, same rewards. A small $\gamma$ makes the robot short-sighted: rewards four steps away barely count.

## Modeling a robot task as an MDP

Most of the work is choosing the pieces. The state must include everything that affects what happens next. Actions might be high-level (go to room 3) or low-level (wheel torques). Transition probabilities come from data or a simulator. The reward must say what you actually want, and only that.

> **Common mistake:** a state that isn't Markov. If the state holds a robot's position but not its velocity, the same "state" can lead to very different futures, and any policy built on it will be confused. If the past still matters, add what matters to the state.
