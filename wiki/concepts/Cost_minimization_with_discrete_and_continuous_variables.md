# Cost minimization with discrete and continuous variables

## Definition

Cost minimization with discrete and continuous variables is an optimization problem where the objective function (typically cost or loss) depends on both:
- **Discrete variables**: categorical choices, counts, or combinatorial selections (e.g., partition membership, number of parts)
- **Continuous variables**: real-valued parameters that can take any value in a range (e.g., weights, thresholds, fractional amounts)

The challenge is that these variable types interact in the cost function in non-trivial ways, making direct optimization difficult. The cost of a feasible solution depends simultaneously on discrete structural choices and continuous parameter tuning.

**Formal statement:** Find $(d, c) \in \mathcal{D} \times \mathbb{R}^m$ that minimizes
$$\text{Cost}(d, c) = f(d, c)$$
where $d$ represents discrete choices and $c$ represents continuous variables.

## Key Equations

### Signature-based cost representation
When discrete choices determine a *signature* (counts of discrete element types), the cost becomes a function of both the signature and continuous parameters:

$$\text{Cost}(\text{signature}) = g(n_1, n_2, \ldots, n_k; \sum c_i)$$

where $n_i$ are counts (discrete) and $\sum c_i$ is an aggregate of continuous variables.

### Rounding approximation
When continuous variables $\epsilon_i$ can be rounded to discrete levels $\lceil \epsilon_i / \delta \rceil \cdot \delta$, the cost perturbation is bounded:

$$|\text{Cost}(\epsilon_i) - \text{Cost}(\text{rounded } \epsilon_i)| \leq \mathcal{O}(1/\text{poly}(k)) \quad \text{additively}$$

This separation enables analysis of the discrete structure independently.

### One-sided convergence bound
For empirical cost estimation from $m$ samples:

$$\text{Cost}_{\text{emp}}(f) \leq \text{Cost}_{\text{true}}(f) + \mathcal{O}\left(\frac{|X|}{\varepsilon^2}\right) \quad \text{with high probability}$$

The one-sided convergence rate follows from:
$$\frac{1}{\varepsilon^3} \text{ samples suffice for convergence in optimal predictors}$$

## Physical Intuition / Derivation

### Why both variables matter

In many engineering systems, discrete and continuous optimization interact:

1. **Discrete choices determine structure**: Partitioning elements into groups, selecting hardware configurations, or choosing algorithm variants
2. **Continuous variables optimize within structure**: Once structure is fixed, parameters can be tuned smoothly
3. **The interaction creates a barrier**: The cost landscape has *both* discontinuous jumps (when switching discrete modes) and smooth gradients (in continuous subspaces)

### The challenge: Exponential discrete space

Without structure, there are $2^{|X|}$ possible partitions. Naive enumeration is intractable. The key insight is **signature reduction**: instead of tracking which specific element goes where, track only aggregate statistics.

**Example from the source:**
- Partition elements into parts with signatures $(t, 2t, 0)$ or $(t, 0, 2t)$ (three types of discrete elements)
- The cost depends on: how many elements of each type in each part (discrete) + sum of continuous weights in that part (continuous)
- By showing that irregular partitions are strictly suboptimal by $\Omega(1/k^2)$, the effective search space collapses to a small family

### Rounding strategy for tractability

**Procedure:**
1. Note that continuous variables $\epsilon_i$ satisfy approximate constraints (e.g., $\approx 1/(2k)$ up to relative error)
2. Round all $\epsilon_i$ to canonical values $\delta \lceil \epsilon_i / \delta \rceil$
3. Cost perturbation from rounding is $\mathcal{O}(1/\text{poly}(k))$ additively
4. After rounding, only finitely many *discrete signatures* exist
5. Enumerate over low-dimensional signature space; for each signature, optimize continuous variables via calculus

## Applications in Engineering

### 1. **Supply Chain & Logistics**
- **Discrete choice**: Which warehouse locations to open; how many delivery routes
- **Continuous variables**: Inventory levels at each location, shipment quantities, transportation costs
- **Optimization**: Minimize total cost while meeting demand constraints
- *Approach*: Fix warehouse count (discrete), optimize routing and inventory (continuous); compare across counts

### 2. **Power Systems & Microgrid Design**
- **Discrete choice**: Which generation units are online/offline (on/off switching); number of battery clusters
- **Continuous variables**: Power output of each unit, voltage/frequency setpoints, charging rates
- **Challenge**: Unit commitment (discrete) + economic dispatch (continuous)
- *Solution*: Lagrangian relaxation separates problems iteratively

### 3. **Machine Learning & Model Selection**
- **Discrete choice**: Network architecture (number of layers, layer types); partition of training data into subsets
- **Continuous variables**: Weights, learning rates, regularization parameters
- **Goal**: Minimize validation loss
- *Approach* (from source): Calibration with discrete partitions + continuous weight tuning

### 4. **Manufacturing & Process Control**
- **Discrete choice**: Number of production batches; machine allocation to tasks
- **Continuous variables**: Batch size, processing time, temperature/pressure setpoints
- **Objective**: Minimize production cost while meeting quality specs

### 5. **Integer Linear Programming (ILP) / Mixed-Integer Programming (MIP)**
- General formulation: $\min c^T x + d^T y$ subject to $Ax + By \leq b$, $x \in \mathbb{Z}^p$, $y \in \mathbb{R}^q$
- **Branch-and-bound**: Relaxes integers to reals, solves LP repeatedly

## Common Mistakes / Pitfalls

### 1. **Ignoring interaction effects**
❌ **Mistake**: Optimize discrete and continuous variables separately (sequential optimization).
✅ **Correct**: Recognize that discrete choice constrains the