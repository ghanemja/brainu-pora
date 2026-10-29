---
video: l87rgLg90HI | Policy and Value Iteration | CIS 522 - Deep Learning | 16:39
---
## Solving an MDP when you know the model

When the transitions $P$ and rewards $R$ are known, you can compute the optimal values and policy exactly, without trial and error. Two classic algorithms do it. Both are dynamic programming, and both are the foundation for the reinforcement learning methods that follow, which do the same thing from samples instead of a model.

## Value iteration

Start from any guess, such as $V_0 = 0$, and apply the Bellman update to every state, over and over:

$$V_{k+1}(s) = \max_a \Big[ R(s, a) + \gamma \sum_{s'} P(s' \mid s, a)\, V_k(s') \Big]$$

Each sweep shrinks the worst-case error by at least a factor of $\gamma$, because the update is a **contraction**. So $V_k$ converges to $V^*$ from any start. Then the optimal policy picks the action achieving the max in each state.

## Policy iteration

Policy iteration alternates two steps:

- **Evaluate** the current policy exactly, by solving the linear system $V^\pi = R^\pi + \gamma P^\pi V^\pi$, one equation per state.
- **Improve** it greedily, $\pi(s) \leftarrow \arg\max_a \big[ R(s, a) + \gamma \sum_{s'} P(s' \mid s, a)\, V^\pi(s') \big]$.

Each improvement is at least as good as the last. There are finitely many policies, so it stops, usually after only a handful of iterations, when the policy no longer changes.

## Worked example: stay or go

Two states, $\gamma = 0.9$. In $s_1$: "stay" earns 1 and stays in $s_1$; "go" earns 0 and moves to $s_2$. In $s_2$, the only action earns 2 and stays.

**Policy iteration**, starting with "stay": $V(s_1) = 1/(1 - 0.9) = 10$, and $V(s_2) = 2/0.1 = 20$. Improve: in $s_1$, "stay" gives $1 + 0.9 \times 10 = 10$ and "go" gives $0 + 0.9 \times 20 = 18$, so switch to "go". Re-evaluate: $V(s_1) = 18$. Nothing changes after that: done in two rounds.

**Value iteration** from zero: $(1, 2)$, then $(1.9, 3.8)$, then $(3.42, 5.42)$. The greedy action in $s_1$ flips to "go" at sweep 3, but the values creep toward $(18, 20)$ for many more sweeps.

## Which one to use

Policy iteration takes few iterations, but each one solves a linear system over all states. Value iteration's sweeps are cheap but can take many of them when $\gamma$ is near 1. Both need the full model and a sweep over every state, so they're limited to problems small enough to tabulate, or used with approximations.

> **Common mistake:** too few value iteration sweeps with $\gamma$ close to 1. The error shrinks by only a factor $\gamma$ per sweep: with $\gamma = 0.99$, cutting it 100-fold takes about 460 sweeps. Check the change between sweeps, not a fixed count.
