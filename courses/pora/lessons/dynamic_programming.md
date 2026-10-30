---
video: 9JZID-h6ZJ0 | Bellman Equation - Explained! | CodeEmporium | 9:05
---
## The principle of optimality

If the fastest route from San Francisco to Los Angeles passes through San Jose, then its San Jose to Los Angeles part must be the fastest route from San Jose. Otherwise you could swap in a faster tail and beat the "fastest" route.

That's Bellman's **principle of optimality**: every tail of an optimal policy is optimal for the problem that starts where the tail starts. It means you can solve a long problem by solving its last step first, then the last two, and so on, reusing each answer.

## The backward recursion

For a problem with $N$ stages, terminal cost $h$, step cost $g$ and dynamics $x_{k+1} = f(x_k, u_k, w_k)$ with noise $w_k$:

$$J_N(x) = h(x), \qquad J_k(x) = \min_u \; \mathbb{E}\big[\, g(x, u) + J_{k+1}(f(x, u, w)) \,\big]$$

$J_k(x)$ is the optimal **cost-to-go** from state $x$ at stage $k$. The $u$ achieving each minimum is the optimal action, so DP produces a full **feedback policy** $\pi_k(x)$, valid from any state, not just a single plan.

## Worked example: greedy versus backward

Go from A to D. The edges cost A→B 2, A→C 4, B→D 5 and C→D 1.

Work backward from the goal: $J(D) = 0$, then $J(B) = 5$ and $J(C) = 1$. Then

$$J(A) = \min(2 + J(B),\ 4 + J(C)) = \min(7,\ 5) = 5$$

So the best route is A→C→D, at cost 5. A greedy robot takes the cheaper first step to B and ends up paying 7. DP accounts for what each choice leads to, not just what it costs now.

## The Bellman equation

With an infinite horizon and discount $\gamma$, the cost-to-go stops depending on the stage, and the recursion becomes an equation the optimal value function must satisfy:

$$V^*(s) = \max_a \Big[ R(s, a) + \gamma \sum_{s'} P(s' \mid s, a)\, V^*(s') \Big]$$

Written with rewards and a max, it's the same idea: the value of a state is the best immediate reward plus the discounted value of where you land. Value and policy iteration solve it.

## The same idea everywhere

Many algorithms in this course are DP in disguise. **LQR** is DP where the cost-to-go stays quadratic, $J_k(x) = x^\top P_k x$, so the recursion reduces to the Riccati equation. **Dijkstra** is DP on a graph, settling nodes in order of cost. **Value iteration** is DP for MDPs. Even iLQR is DP on a local quadratic model.

> **Common mistake:** assuming DP is always practical. Exact DP stores a value for every state. A 6-D state with 100 grid values per dimension has $10^{12}$ states: the **curse of dimensionality**. Real problems need structure (as in LQR) or approximation (as in deep RL).
