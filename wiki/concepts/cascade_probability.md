# Cascade Probability

## Definition

**Cascade probability** refers to the compounding probability of success across sequential stages or iterations in a cascading algorithm, where each stage depends on the successful completion of previous stages. In the context of tensor network optimization methods, it quantifies the likelihood that a "waterfall" or cascading decomposition process will yield uniform (constant) tensors at successive levels, enabling computational efficiency gains.

Formally, if $P$ is the probability of obtaining a uniform tensor at a single stage, the cascade probability for $k$ cascading stages is:

$$P_{\text{cascade}}(k) = O(P^k)$$

This represents the compounded probability of success across all $k$ stages, where each additional stage multiplies the base probability by $P$.

## Key Equations

**Single-stage success probability:**
$$P = \Pr[\text{uniform tensor obtained}]$$

**Cascade success probability for } k \text{ stages}:**
$$P_k = O(P^k)$$

**Number of components to verify at stage } i \text{}:**
$$\text{Components}_i = O(d^k)$$

**Spatial complexity with cascade probability:**
$$\text{Space} = O(m \cdot d^{k+1})$$

where $m \in [1, n]$ is the expected number of iterations until obtaining a uniform tensor:
$$\mathbb{E}[m] = \frac{1}{P}$$

**Relative error metric for algorithm comparison:**
$$\varepsilon_{\text{relative}} = 1 - \frac{C(\vec{x}_{\text{tn}})}{C(\vec{x}_{\text{OR}})}$$

where $C(\vec{x}_{\text{tn}})$ and $C(\vec{x}_{\text{OR}})$ are costs from tensor network and OR-TOOLS solutions respectively.

## Physical Intuition / Derivation

### Why Cascade Probability Matters

In cascading decomposition algorithms, the method succeeds when intermediate tensors achieve a uniform (constant-valued) state. This uniform state allows subsequent operations to:
- Reduce computational requirements by a factor of $d$
- Eliminate stored tensor states (garbage collection opportunity)
- Dramatically decrease spatial complexity from $O(n d^{k+1})$ to $O(m d^{k+1})$

### The Compounding Problem

Consider a $k$-stage cascade. At each stage independently, the probability of obtaining uniformity is $P$. Since stages are sequential and dependent:
- Stage 1 succeeds with probability $P$
- Stages 1 *and* 2 both succeed with probability $P \cdot P = P^2$
- Stages 1, 2, *and* 3 all succeed with probability $P^3$

Thus: $P_k = P^k$

### Practical Consequence

For small $P$ and large $k$, cascade probability becomes vanishingly small. For example:
- If $P = 0.9$ and $k = 10$: $P_{10} \approx 0.349$ (reasonable)
- If $P = 0.5$ and $k = 10$: $P_{10} \approx 0.00098$ (infeasible)

This **exponential decay in success probability** is the fundamental limitation of cascading methods. The source material explicitly states: *"the effectiveness of the waterfall method depends on the probability of having the same result for all new tensors generated from all possible previous configurations."*

### Empirical Measurement

The cascade probability for $k=1$ (single stage) is the critical empirical parameter that determines whether the entire method is viable. The effectiveness threshold depends on problem-specific characteristics and must be measured for each application domain.

## Applications in Engineering

### 1. **Tensor Network Optimization**
- **Constraint satisfaction problems**: Cascading decompositions for QUBO (Quadratic Unconstrained Binary Optimization) problems
- **Advantage**: Outperforms standard solvers (e.g., OR-TOOLS) on multiple benchmark instances
- **Requirement**: Monitoring cascade probability to ensure solution quality

### 2. **Large-Scale Combinatorial Optimization**
- Decomposing high-dimensional tensors into solvable sub-problems
- Spatial complexity reduction from $O(n d^{k+1})$ to $O(m d^{k+1})$ when $m \ll n$
- Critical for problems with $n > 10^6$ variables where memory is constrained

### 3. **Signal Processing & Dimensionality Reduction**
- Multi-stage tensor contractions in signal decomposition
- Each cascade stage represents a filtering or compression operation
- Cascade probability determines expected number of stages needed

### 4. **Machine Learning (Tensor Methods)**
- Hierarchical tensor decomposition for neural networks
- Pruning intermediate layers based on uniform tensor detection
- Reducing model footprint while maintaining accuracy

### 5. **Quantum Computing (Classical Simulation)**
- Simulating quantum circuits through tensor networks
- Cascade probability affects computational feasibility of classical simulation

## Common Mistakes / Pitfalls

### 1. **Ignoring Exponential Decay**
❌ **Wrong**: "We can always cascade to arbitrary depth $k$"
✓ **Right**: Recognize that $P_k = O(P^k)$ becomes prohibitively small for modest $k$ unless $P$ is very close to 1.

### 2. **Confusing Independent vs. Sequential Probability**
❌ **Wrong**: Adding probabilities across stages ($P_1 + P_2 + \ldots + P_k$)
✓ **Right**: Cascading requires *all* stages to succeed, so multiply: $P_1 \times P_2 \times \ldots \times P_k$

### 3. **Neglecting Empirical Measurement**
❌ **Wrong**: Assuming $P$ is theoretically derivable without testing
✓ **Right**: Empirically measure $P$ for $k=1$ before deploying the cascading algorithm, as stated in the source material

### 4. **Not Accounting for the $m$ Factor**
❌ **Wrong**: Claiming spatial complexity is always $O(d^{k+1})$ in cascading methods
✓ **Right**: Actual complexity is $O(m \cdot