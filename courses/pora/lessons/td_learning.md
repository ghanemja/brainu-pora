---
video: uJX_72MnKg8 | Foundation of Q-learning | Temporal Difference Learning explained! | CodeEmporium | 10:11
---
## Estimating values from experience

A policy's value $V^\pi(s)$ is the expected return starting from $s$. Without a model you can't compute it with the Bellman equation, but you can estimate it from experience. There are two basic ways: wait for the actual return at the end of an episode (**Monte Carlo**), or update after every step using your own estimate of the next state's value (**temporal-difference** learning, or TD).

Both are the building blocks of value-based RL.

## Monte Carlo: average what actually happened

Run an episode to the end. For each state visited, compute the return $G_t$ that actually followed, and nudge the estimate toward it with step size $\alpha$:

$$V(s_t) \leftarrow V(s_t) + \alpha \big[ G_t - V(s_t) \big]$$

Averaged over many episodes, this converges to the true value. It's **unbiased**, since $G_t$ is a real sample of the return. But it has high **variance**, because one return sums many random rewards, and it can only update once the episode is over.

## TD(0): learn from the next step

TD replaces the full return with one real reward plus the current estimate of where you landed:

$$V(s_t) \leftarrow V(s_t) + \alpha \big[ \underbrace{r_t + \gamma V(s_{t+1})}_{\text{TD target}} - V(s_t) \big]$$

The bracket is the **TD error** $\delta_t$: how much better or worse the step turned out than expected. Using your own estimate inside the target is called **bootstrapping**. TD updates after every step, works for tasks that never end, and has lower variance, but it's biased while $V$ is still inaccurate.

## Worked example: one update each way

Current estimates: $V(s) = 5$ and $V(s') = 8$. The robot gets $r = 1$ moving from $s$ to $s'$. Use $\gamma = 0.9$ and $\alpha = 0.1$.

- **TD(0)**: target $= 1 + 0.9 \times 8 = 8.2$, so $\delta = 3.2$ and $V(s) \leftarrow 5 + 0.1 \times 3.2 = 5.32$.
- **Monte Carlo**: suppose the episode ends with an actual return $G = 10$ from $s$. Then $V(s) \leftarrow 5 + 0.1 \times (10 - 5) = 5.5$.

TD could update right away; Monte Carlo had to wait for the episode to finish.

## In between: n-step returns and TD(λ)

You don't have to choose an extreme. An **n-step** target uses $n$ real rewards before bootstrapping:

$$G_t^{(n)} = r_t + \gamma r_{t+1} + \dots + \gamma^{n-1} r_{t+n-1} + \gamma^n V(s_{t+n})$$

$n = 1$ is TD(0), and $n$ to the end of the episode is Monte Carlo. **TD(λ)** blends all of them with weights decaying by λ. Middle values often learn fastest.

> **Common mistake:** bootstrapping from a terminal state. When $s_{t+1}$ ends the episode, there's no future, so the target is just $r_t$. Using a stale, nonzero $V(s_{t+1})$ there feeds made-up value into everything upstream.
