# k-Bin Packing

## Definition

**k-Bin Packing** is a classical optimization problem in combinatorial algorithms: given a set of $n$ positive integers and a target value $T$, determine whether the items can be partitioned into $k$ bins such that the sum of items in each bin does not exceed $T$.

Formally:
- **Input**: A multiset of item sizes $S = \{s_1, s_2, \ldots, s_n\}$ where $s_i \in \mathbb{Z}^+$, a bin capacity $T$, and number of bins $k$.
- **Question**: Does a partition exist such that for each bin $i \in [k]$, $\sum_{j \in B_i} s_j \leq T$?

The problem is also denoted $P_k \| C_{\max}$ in scheduling notation, representing the makespan minimization problem on $k$ parallel machines.

## Key Equations

### Running Time Bounds

The known algorithmic and complexity-theoretic results are:

**Upper bounds (pseudopolynomial algorithms):**
$$T_{\text{alg}} = O(nT^{k-1})$$

**Conditional lower bounds (assuming Exponential Time Hypothesis):**
$$T_{\text{lower}} \geq 2^{o(n)}T^{o(k)}$$

For variants with additional structure, tighter SETH-based lower bounds hold:
$$T_{\text{lower}} \geq 2^{o(n)}T^{k-1-\varepsilon} \quad \text{(for all } \varepsilon > 0\text{)}$$

### Problem Parameterization

The problem is parameterized by two natural dimensions:
- Number of items: $n$
- Capacity and target: $T$ (with range $[1, \sum_i s_i]$)
- Number of bins: $k$

Hardness typically grows exponentially in both $n$ and $T$, but the dependency on $k$ varies across related scheduling variants.

## Physical Intuition / Derivation

### Why k-Bin Packing is Hard

k-Bin Packing generalizes the **Subset Sum** problem (the special case $k=1$). Subset Sum is $\texttt{NP}$-complete; k-Bin Packing extends this by requiring a partition into $k$ groups rather than finding a single subset.

The difficulty arises from:

1. **Combinatorial explosion**: The number of ways to partition $n$ items into $k$ bins grows as $k^n$, even before accounting for capacity constraints.

2. **Communication between bins**: Unlike Subset Sum (where we only need one "successful" subset), k-Bin Packing requires communicating feasibility information across multiple bins. The source material emphasizes this challenge via "creative encoding of communication between bins."

3. **ETH-based tightness**: The tight lower bound $2^{o(n)}T^{o(k)}$ reflects that:
   - The exponential factor $2^{\Theta(n)}$ comes from the item enumeration problem
   - The polynomial factor $T^{\Theta(k)}$ encodes the multi-dimensional packing constraint

### Why Lower Bounds Matter

The source material highlights that previous lower bounds by Jansen et al. (using $\log k$ factors in the exponent) were inherited by many downstream problems. The improved bounds eliminate this log-factor loss, providing tight conditional hardness results across a family of scheduling and graph problems.

## Applications in Engineering

### 1. **Parallel Task Scheduling**
Distributing computational tasks across $k$ processors with time constraints. Each processor has a deadline $T$, and tasks must be allocated to minimize makespan.

### 2. **Resource Allocation**
Packing jobs into $k$ machines or containers (cloud VMs, shipping containers, memory units) such that no resource exceeds capacity $T$.

### 3. **Load Balancing**
In distributed systems, k-Bin Packing models the problem of distributing load across $k$ servers to minimize the maximum server load.

### 4. **Cutting Stock & Manufacturing**
In industrial applications, this models cutting material from stock with waste minimization—items are cut from $k$ stock pieces of capacity $T$.

### 5. **Graph Partitioning**
Related problems like **Sparsest Cut on bounded treewidth graphs** and **Cluster Editing** reduce to k-Bin Packing, enabling hardness transfer to these graph-theoretic problems.

## Common Mistakes / Pitfalls

### 1. **Confusing Parameterization**
Students often conflate the problem size:
- $n$ (number of items) and $T$ (capacity) are *independent* parameters
- Hardness is doubly exponential: $2^{\Theta(n)} \cdot T^{\Theta(k)}$
- A problem that is "hard in $n$" but "easy in $T$" requires *pseudo*-polynomial algorithms, not polynomial ones

### 2. **Assuming ETH ≡ SETH**
- **ETH** (Exponential Time Hypothesis): SAT requires $2^{\Omega(n)}$ time
- **SETH** (Strong ETH): SAT requires $2^{(1-o(1))n}$ time
- The source material distinguishes between these; not all lower bounds hold under both!

### 3. **Ignoring the $o(\cdot)$ Notation**
The notation $2^{o(n)}T^{o(k)}$ means the exponents hide *sublinear* factors:
$$\text{Time} < 2^{cn}T^{dk} \quad \text{for arbitrarily small } c, d > 0$$
This is *weaker* than $2^{\Omega(n)}T^{\Omega(k)}$, representing the tightest known bounds.

### 4. **Overlooking Reductions**
k-Bin Packing lower bounds imply hardness for many scheduling variants (weighted completion time, tardiness, unfinished jobs). Reductions are more subtle than for Subset Sum due to multi-bin constraints.

### 5. **Confusing Approximation with Exact Complexity**
k-Bin Packing admits good approximation algorithms (