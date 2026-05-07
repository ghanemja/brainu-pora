# Objective Function Optimization

## Definition

**Objective function optimization** is the process of finding the values of decision variables that minimize or maximize a scalar objective function subject to constraints. In engineering, the objective function typically quantifies a quantity of interest—cost, utility, energy, time, or performance—that we seek to optimize over a feasible solution space.

Formally, an optimization problem is stated as:
$$\text{minimize (or maximize)} \quad f(\mathbf{x})$$
$$\text{subject to} \quad \mathbf{g}(\mathbf{x}) \leq 0, \quad \mathbf{h}(\mathbf{x}) = 0$$

where $\mathbf{x} \in \mathbb{R}^n$ is the vector of decision variables, $f: \mathbb{R}^n \to \mathbb{R}$ is the objective function, and the constraints define the feasible region.

In scheduling and combinatorial optimization contexts (as illustrated in the source material), the objective often takes the form of a weighted sum representing cumulative cost:

$$\text{minimize} \quad \sum_{j=1}^{m} w_j C_j$$

where $w_j$ is the weight (priority, cost coefficient) of item $j$ and $C_j$ is its completion time or cost contribution.

---

## Key Equations

### Standard Weighted Sum Form

For a scheduling problem with $m$ jobs, the objective function expressing total weighted completion time is:

$$\sum_{j=1}^{m} w_j C_j$$

### Decomposition into Block Structure

When jobs are organized into $n$ blocks $B_1, B_2, \ldots, B_n$, with starting time $s_i$ for block $i$ and total processing weight $W_i = \sum_{j \in B_i} w_j$, the objective can be decomposed as:

$$\sum_{j=1}^{m} w_j C_j = \sum_{i=1}^{n} \sum_{j \in B_i} w_j \left( s_i + \sum_{\substack{l \in B_i \\ l \preceq j}} w_l \right)$$

Rearranging (as shown in equations 6–7 of the source):

$$= M \sum_{i=1}^{n} (i-1)W_i + \sum_{j=1}^{m} w_j^2 + \sum_{j=1}^{m} \sum_{l \preceq j} w_l w_j$$

### Optimal Value Characterization

For a feasible solution with blocks of equal weight ($W_i = T = W/n$ for all $i$), the optimal objective value simplifies to a baseline determined by problem structure:

$$u_{\text{YES}} = \text{constant determined by problem parameters}$$

The gap between achieved and optimal objective values indicates solution quality.

---

## Physical Intuition / Derivation

### Why Minimize Weighted Completion Time?

In scheduling, **completion time** $C_j$ measures when job $j$ finishes. If job $j$ has **weight** $w_j$ (representing priority, cost per unit time, or penalty), then $w_j C_j$ represents the **total burden** imposed by delaying that job.

**Intuition:** 
- A job with high weight (critical, expensive) should finish early.
- A job with low weight can afford to finish later.
- Summing $w_j C_j$ over all jobs gives total system cost.

### Block Decomposition Insight

The source decomposes the problem into **blocks**—logical groupings of jobs. Within each block $B_i$:

1. Jobs are sequenced internally, contributing $\sum_{l \in B_i, l \preceq j} w_l$ to the completion time of job $j$.
2. Each job also experiences the full starting time $s_i$ of its block.

The total cost factors into:
- **Idle cost**: $M(i-1)W_i$ — the delay from forcing block $i$ to start at time $(i-1)M$
- **Internal cost**: $\sum_{j} w_j^2 + \text{cross-terms}$ — cumulative delays within blocks

### Ideal Configuration

When all blocks have **equal weight** ($W_i = T$ for all $i$), we achieve a balanced solution where:
- Each separator (boundary job) completes exactly at its deadline.
- No "slack" or unused capacity.
- The objective function reaches its optimal baseline value.

This is characteristic of feasible solutions to the underlying combinatorial problem (e.g., 3-Partition) that the scheduling problem encodes.

---

## Applications in Engineering

### 1. **Manufacturing & Job Shop Scheduling**
Minimize weighted completion time to balance production priorities:
- High-priority orders (high $w_j$) finish first.
- Standard orders absorb lateness cost.
- Reduces both inventory holding costs and customer penalties.

### 2. **Project Management**
Assign resources to minimize cumulative project overhead:
- $w_j$ = cost per unit time for task $j$ (labor, equipment, overhead).
- $C_j$ = when task $j$ completes.
- Objective: finish expensive tasks early.

### 3. **Supply Chain Optimization**
Sequence shipments or batches to minimize warehousing costs:
- $w_j$ = storage cost per unit time for item $j$.
- Optimal schedule reduces inventory exposure.

### 4. **Electrical Grid Dispatch**
Minimize weighted fuel/wear cost of generator commitment:
- $w_j$ = marginal cost of operating generator $j$.
- $C_j$ = cumulative output or run time.
- Objective: prioritize cheap, durable generation.

### 5. **Machine Learning & Algorithm Tuning**
Optimize hyperparameters or model weights to minimize loss:
$$\text{minimize} \quad L(\mathbf{w}) + \lambda ||\mathbf{w}||^2$$
- Objective balances fit quality against model complexity.

### 6. **NP-Hardness Reductions**
Encode combinatorial problems (e.g., 3-Partition) as scheduling instances: