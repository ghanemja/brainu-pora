# Waterfall Method

## Definition

The **waterfall method** is an algorithmic technique for solving combinatorial optimization problems (particularly **QUDO** – Quadratic Unconstrained Discrete Optimization problems) using tensor network contractions. The method iteratively generates and processes tensors of decreasing dimensionality, cascading through successive computational stages to find near-optimal or optimal solutions.

In the context of this method, at each stage $k$, a **k-tensor** is contracted to produce a vector of $d$ components. The algorithm iterates by extracting specific components and regenerating tensors from all possible previous configurations until a termination condition is met (e.g., uniform tensor obtained or iteration limit reached).

## Key Equations

**Success Probability:**
The probability of successful cascade completion decreases as:
$$P_{\text{success}} = O(P^k)$$

where $P$ is the probability of obtaining a constant/uniform vector $Y_m$ at each stage, and $k$ is the cascade depth.

**Component Reduction:**
Each successive vector requires $d$ times fewer components than the previous one:
$$\text{Components}_k = \frac{\text{Components}_{k-1}}{d}$$

**Computational Complexity (Time):**
The number of combinations that must be evaluated at depth $k$ is:
$$T = d^k$$

**Spatial Complexity (Memory):**
- **Worst case:** $O(nd^{k+1})$ tensor elements
- **Optimized case (with uniform tensor pruning):** $O(md^{k+1})$ where $m \in [1, n]$ is the number of iterations until a uniform tensor appears, and $m$ decreases as $P$ increases.

**Relative Error Metric:**
$$\varepsilon_{\text{relative}} = 1 - \frac{C(\vec{x}_{tn})}{C(\vec{x}_{\text{OR}})}$$

where $C(\vec{x}_{tn})$ is the tensor network solution cost and $C(\vec{x}_{\text{OR}})$ is the reference optimizer cost.

## Physical Intuition / Derivation

### Why "Waterfall"?

The name reflects the cascading structure: tensors of dimensionality $k$ progressively contract to lower dimensions, like water flowing down successive steps. At each stage, the problem dimensionality decreases by a factor related to $d$.

### The Probability Bottleneck

The critical insight is the **cascade probability decay**: as you apply the waterfall procedure repeatedly (increasing $k$), the likelihood that all generated tensors yield the same consistent result decays **exponentially** as $P^k$. This is because:

1. At stage 1: Probability of uniform result is $P$
2. At stage 2: Must obtain uniformity from **all** stage-1 outcomes, so probability becomes $P \cdot P = P^2$
3. At stage $k$: Probability is $P^k$

For large $k$, this approaches zero, rendering the method unfeasible unless $P$ is exceptionally high.

### Memory-Computation Trade-off

The method exhibits a classic trade-off:
- **Without optimization:** Must store up to $O(d^k)$ intermediate tensors, consuming $O(nd^{k+1})$ space
- **With uniform tensor pruning:** If the algorithm achieves a uniform tensor early (expected at iteration $m$), tensors can be discarded, reducing space to $O(md^{k+1})$. This is only beneficial when $m \ll n$, requiring high probability $P$ of early uniformity.

## Applications in Engineering

### 1. **Discrete Optimization in Operations Research**
- Vehicle routing problems (VRP variants)
- Job scheduling with hard/soft constraints
- Portfolio optimization with discrete asset selections

### 2. **Constraint Satisfaction Problems (CSP)**
- Logic circuit satisfiability (SAT)
- Manufacturing constraint propagation
- Network design with discrete variable selection

### 3. **Quantum-Inspired Classical Optimization**
- Problems traditionally targeted by quantum annealing (e.g., Ising models, QUBO formulations)
- Hybrid classical-quantum algorithm development

### 4. **Large-Scale Combinatorial Engineering**
- Supply chain network optimization
- Power grid reconfiguration
- Resource allocation in distributed systems

### 5. **Comparison with Industry Solvers**
Experimental results show the waterfall tensor method **outperforms OR-TOOLS** (Google's optimization suite) on several benchmark instances, achieving lower cost solutions with competitive runtime, making it viable for problems where standard solvers struggle.

## Common Mistakes / Pitfalls

### 1. **Ignoring the Probability Decay**
Practitioners often underestimate how quickly $P^k$ vanishes. A seemingly reasonable $P = 0.9$ becomes impractical at $k > 20$ ($P^{20} \approx 0.122$). Always precompute expected feasibility before committing to large-$k$ problems.

### 2. **Misjudging Memory Requirements**
The worst-case $O(nd^{k+1})$ bound can ambush developers. Don't assume uniform tensor pruning will activate; validate empirically that your problem class achieves high $P$ values early.

### 3. **Incorrect Parameter Tuning**
The termination threshold $\tau$ (problem-size-dependent) is critical. Setting $\tau$ too loosely allows excessive computation; too strictly causes premature termination with suboptimal solutions. Precompute $\tau$ based on instance characteristics.

### 4. **Confusing with Waterfall Software Development**
Do not conflate this algorithmic method with the sequential waterfall software development lifecycle—they are unrelated concepts.

### 5. **Incompatible Problem Formulation**
The method requires problems expressible as **discrete, bounded optimization** over tensor networks. Continuous problems or those without natural tensor structure will not benefit.

### 6. **Cherry-Picking Baselines**
Comparing only against OR-TOOLS without considering GUROBI, CPLEX, or problem-specific heuristics may overstate performance. Note that free solver versions have variable limitations.

## See Also

- [[Tensor Network Contraction]] – Foundation for computing k-tensor operations
- [[Quadratic Unconstrained Discrete Optimization (QUBO)]] – Problem class tackled by water