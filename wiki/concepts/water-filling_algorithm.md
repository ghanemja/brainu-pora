# water-filling algorithm

## Definition

The **water-filling algorithm** is an optimal dynamic resource allocation policy that distributes divisible resources among competing agents or channels to maximize equity in load distribution. The algorithm operates greedily: at each arrival or allocation decision point, it assigns the next unit of resource to the agent currently holding the least load.

More formally, given a sequence of resource requests $E = (r_1, r_2, \ldots, r_T)$ and $n$ agents with initial loads $x_i(0) = 0$, the water-filling algorithm produces a load vector $\mathbf{x} = (x_1, x_2, \ldots, x_n)$ where each request $r_t$ is allocated to agent $i^* = \arg\min_i x_i(t-1)$ (breaking ties arbitrarily), updating $x_{i^*}(t) = x_{i^*}(t-1) + r_t$.

## Key Equations

**Majorization Relation (Preorder):**
A vector $\mathbf{x}$ is majorized by vector $\mathbf{y}$ (written $\mathbf{x} \preceq_m \mathbf{y}$) if, when both are sorted in descending order, the cumulative sums satisfy:
$$\sum_{i=1}^{k} x_{(i)} \geq \sum_{i=1}^{k} y_{(i)} \quad \text{for all } k = 1, \ldots, n$$

**Schur-Monotone Functions:**
A function $f: \mathbb{R}^n \to \mathbb{R}$ is **Schur-concave** if $\mathbf{x} \preceq_m \mathbf{y} \implies f(\mathbf{x}) \geq f(\mathbf{y})$ (equity-promoting).
A function is **Schur-convex** if the inequality reverses (inequity-promoting).

**Common Equity Objectives:**
- Nash social welfare: $f(\mathbf{x}) = \left(\prod_{i=1}^{n} x_i\right)^{1/n}$ (Schur-concave)
- Fractional matching: $f(\mathbf{x}) = \sum_{i=1}^{n} \min(c, x_i)$ (Schur-concave for capacity $c > 0$)
- $\ell_p$-norm: $f(\mathbf{x}) = \|\mathbf{x}\|_p = \left(\sum_{i=1}^{n} |x_i|^p\right)^{1/p}$ (Schur-convex, penalizes inequity)
- Gini index: measures relative inequality (Schur-convex)

**Core Optimality Result (Theorem 1):**
For any request sequence $E$ and any deterministic allocation policy $A$ that deviates from water-filling:
$$\text{OPT}(E) \preceq_m \text{WF}(E) \preceq_m A(E)$$

where $\text{WF}(E)$ is the load vector produced by water-filling and $\text{OPT}(E)$ is the unique majorization-minimal feasible allocation.

## Physical Intuition / Derivation

Imagine filling a container with $n$ vertical tubes of varying heights, representing agent loads. Pour water continuously into the container. The water naturally fills to the lowest level first, leveling all tubes evenly—this is the water-filling algorithm's logic.

**Why it works:**

1. **Majorization captures equity directly**: A more "level" distribution (smaller spread between agents) majorizes one with larger disparities. This is precisely what equity means across most reasonable objectives.

2. **Greedy necessity**: At any moment, if you assign the next unit to anyone other than the currently-lowest-loaded agent, you create unnecessary disparity. An adversary can then exploit this by requesting resources that compound the imbalance.

3. **Minimax optimality**: Water-filling minimizes the worst-case majorization position. If you deviate:
   - Against an **adaptive adversary** (knows your policy): they see your deviation and craft a request sequence to make your allocation less equitable than water-filling's
   - Against an **oblivious adversary** (fixes sequence in advance): water-filling still dominates for Schur-monotone objectives, guaranteeing performance across all equity metrics

4. **Hindsight-optimality**: The set of all feasible allocations (respecting the constraint that total load equals sum of requests) has a unique minimum under majorization—the hindsight-optimal $\text{OPT}(E)$. Water-filling is the closest any online algorithm can get to this ideal without future knowledge.

## Applications in Engineering

### Parallel Computing & Load Balancing
Distribute incoming jobs across processors to minimize worst-case completion time (makespan). Water-filling spreads jobs to the least-loaded CPU, balancing latency equitably across workers.

### Wireless Communication (Power Allocation)
Water-filling originates in information theory (Shannon's classic result) for allocating transmission power across frequency subchannels to maximize capacity while respecting power constraints. The algorithm fills each channel's power "up to the water level" where marginal return equalizes.

### Cloud Resource Management
Allocate computational resources (CPU, memory, I/O) among competing virtual machines or containers to ensure fair service quality and prevent starvation.

### Network Routing
Distribute traffic across multiple paths to achieve balanced congestion. Lower-congestion paths receive additional flow until parity is reached.

### Manufacturing & Job Scheduling
Schedule jobs on machines with varying production rates to minimize variance in completion times and avoid idle capacity disparities.

### Bandwidth Allocation
In network switches and routers, allocate available bandwidth among competing flows proportionally to their demands while maintaining fairness (max-min fairness is a majorization-optimal objective).

## Common Mistakes / Pitfalls

1. **Confusing with equal allocation**: Water-filling does *not* always result in equal loads. It produces equitable loads *given the request sequence*; if requests are skewed, loads will be too. Equal allocation may be strictly worse under majorization.

2. **