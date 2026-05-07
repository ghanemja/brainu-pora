# Dual Frank Wolfe algorithm

## Definition

The **Dual Frank Wolfe (DFW) algorithm** is an iterative optimization method that solves large-scale convex optimization problems by computing shadow prices (dual variables) through a sequence of linear optimization steps. In the context of freight marketplace coordination, it computes dual prices that enable spot pricing policies to account for committed contract capacity constraints without requiring explicit dynamic programming over the full state space.

Formally, given a primal problem with resource constraints (e.g., contracted capacity):
$$\min_x f(x) \quad \text{s.t.} \quad g_i(x) \leq 0, \, i = 1, \ldots, m$$

the dual Frank Wolfe algorithm maintains dual variables $\lambda_i \geq 0$ (shadow prices) and iteratively:
1. Solves a linear program to find the best descent direction in primal space
2. Updates dual variables proportional to constraint violations
3. Converges to a solution where shadow prices correctly value scarce resources

## Key Equations

**Dual problem formulation:**
$$\mathcal{D}(\lambda) = \min_x \left[ f(x) + \sum_{i=1}^m \lambda_i g_i(x) \right]$$

**Frank Wolfe iteration (primal-dual framework):**

At iteration $t$, compute the linear oracle solution:
$$s_t = \arg\min_s \nabla f(x_t)^\top s \quad \text{(subject to feasible region)}$$

Update primal variable:
$$x_{t+1} = x_t + \gamma_t (s_t - x_t)$$

Update dual variables (for constraint-driven approach):
$$\lambda_i^{t+1} = \lambda_i^t + \eta_t \max(0, g_i(x_{t+1}))$$

where $\gamma_t$ is the step size (typically $\gamma_t = 2/(t+2)$ for Frank Wolfe) and $\eta_t$ is the dual step size.

**Regret bound:**

For large markets, the algorithm achieves:
$$\text{Regret}(T) = O\left(\frac{1}{\sqrt{T}}\right)$$

or in relative terms:
$$\frac{\text{Regret}(T)}{OPT} = O\left(\frac{1}{\sqrt{T}}\right)$$

where $OPT$ is the optimal cost and $T$ is the number of iterations.

## Physical Intuition / Derivation

### Why Dual Variables Matter

In freight marketplaces, there are two procurement channels:
- **Contracts**: Carriers commit to executing specific capacity (e.g., 100 truckloads/week at $X$ per load)
- **Spot market**: Individual loads are priced dynamically based on real-time supply/demand

The challenge: when a load is fulfilled via spot market at price $p_{spot}$, the system should "charge back" some value to the contract system if that contract capacity could have been used instead.

**Shadow prices solve this:**
$$\lambda^* = \text{value of additional unit of committed capacity}$$

If a contracted lane has shadow price $\lambda = \$500$, it means the contract capacity is worth $\$500/unit more than spot capacity. This allows spot pricing to incorporate scarcity information from contracts.

### Derivation Sketch

1. **Start with intractable problem**: Optimal dynamic program requires solving state enumeration over all possible future demand/capacity combinations—exponentially intractable.

2. **Relax to convex problem**: Model as:
   - Minimize: total procurement cost (contracts + spot)
   - Subject to: don't exceed contracted capacity per lane/time-period

3. **Decompose via duality**: The dual function $\mathcal{D}(\lambda)$ decomposes the problem:
   - For each $\lambda$, the spot pricing oracle solves: "Given shadow prices $\lambda$, what's the optimal spot pricing?"
   - Outer loop updates $\lambda$ based on whether constraints are violated

4. **Frank Wolfe convergence**: Instead of computing gradients of $f$ directly (hard), compute linear approximations iteratively. Each iteration solves only a linear program (the oracle), which is modular and scalable.

### Why This Works for Freight

- **Modularity**: Spot pricing protocol can be any algorithm (black box)—DFW only requires oracle access
- **Scalability**: Linear oracle + gradient updates scale to thousands of lanes, time periods, carrier types
- **Practical regret**: Even with $T \approx 100$ iterations, achieves $\sim 10\%$ improvement over status quo

## Applications in Engineering

### 1. **Digital Freight Marketplaces**
- Coordinate long-term carrier contracts with spot load pricing
- Compute lane-specific shadow prices to allocate scarce contracted capacity efficiently
- Empirically yields ~10% cost reduction vs. decoupled approaches

### 2. **Supply Chain Optimization**
- Integrate supplier contracts (long-term commitments) with spot procurement
- Dynamically adjust spot prices to reflect value of contracted resources
- Useful for semiconductor manufacturing, automotive supply chains

### 3. **Cloud Resource Markets**
- Coordinate reserved instances (contracts) with on-demand pricing (spot)
- Allocate reserved capacity to high-value workloads by computing shadow prices
- Similar problem structure: committed capacity vs. flexible on-demand

### 4. **Energy Markets**
- Balance day-ahead contracts with real-time spot pricing
- Shadow prices indicate where to preferentially dispatch contracted generation
- Addresses grid reliability while minimizing procurement costs

### 5. **Network Optimization / Traffic Engineering**
- General constrained flow problems (minimize routing cost subject to link capacity)
- Frank Wolfe iteration solves shortest path problem at each step
- Applied to routing and congestion pricing

## Common Mistakes / Pitfalls

### 1. **Assuming Convergence without Sufficient Iterations**
**Mistake**: Implementing DFW with very few iterations ($T < 10$) expecting near-optimal results.

**Reality**: Convergence is $O(1/\sqrt{T})$. Need $T \approx 100$–$1000$ to get within 1–3% of