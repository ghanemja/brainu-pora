# Hierarchical Decomposition

## Definition

**Hierarchical decomposition** is a recursive partitioning strategy that breaks a complex structure (typically a graph) into nested levels of simpler substructures. At each level, the structure is decomposed into **components** (or expanders in the graph-theoretic context) and a small set of **crossing edges** that connect different components. This process repeats on the remaining crossing edges until a termination criterion is met.

In the context of graph algorithms, a hierarchical decomposition using expander decomposition produces a sequence of levels:
$$G = G_0 \supset G_1 \supset G_2 \supset \cdots \supset G_l$$

where at each level $j$:
- Vertices are partitioned into disjoint components $V_1^{(j)}, V_2^{(j)}, \ldots, V_{k_j}^{(j)}$
- Each component induces a well-connected subgraph (an expander)
- A set $X_j$ of **crossing edges** connects different components
- The next level $G_{j+1}$ is formed from $X_j$

## Key Equations

**Edge reduction per iteration:**
$$|X_{i+1}| \leq \frac{|X_i|}{2} + C' \cdot n \cdot D \cdot \log^2(n)$$

**Exponential decay condition** (for $|X_i| \geq Cn\sqrt{f}\log^3(n)$):
$$|X_{i+1}| \leq \frac{3|X_i|}{4}$$

**Number of levels:**
$$l = O(\log n)$$

**Total space complexity** for storing the decomposition with parameter $f$:
$$\text{Space} = \tilde{O}(n\sqrt{f}) \text{ bits}$$

This space bound comprises:
- Component identities: $\tilde{O}(n)$ bits across all $l$ levels
- Vertex degrees: $O(\log n)$ bits per vertex across $l$ levels = $\tilde{O}(n)$ bits
- Sparse recovery sketches: $O(\sqrt{f})$ bits per vertex per level = $\tilde{O}(n\sqrt{f})$ bits
- Final crossing edges: $\tilde{O}(n\sqrt{f})$ bits

## Physical Intuition / Derivation

### Why Hierarchical Decomposition Works

The key insight is **geometric reduction**: by removing crossing edges at each level, we dramatically reduce the problem size, yet preserve enough information to answer queries.

**Intuition by analogy:** Consider partitioning a country into states, then states into counties, then counties into cities. To compute distance between two cities:
1. If they're in the same lowest-level partition, use local information
2. Otherwise, "zoom out" to the parent level and track which partitions they belong to
3. Repeat upward until finding a common ancestor
4. The path between cities must cross at specific partition boundaries (recorded as crossing edges)

### Why the Edge Count Shrinks

At each decomposition level, we extract an **expander decomposition**—a partition where each component is internally well-connected. The crossing edges form a small bottleneck set by expander properties. Specifically:

- Start with $\leq n^2$ edges
- After decomposition, crossing edges $|X_i| \leq \frac{|X_{i-1}|}{2} + O(n D \log^2 n)$
- For sufficiently large $|X_i|$ relative to $n$, the linear term dominates the division by 2
- This ensures exponential decay: $|X_i| \leq \frac{3|X_{i-1}|}{4}$
- After $O(\log n)$ iterations, only $\tilde{O}(n\sqrt{f})$ edges remain

### Space Efficiency

The $\tilde{O}(n\sqrt{f})$ space is achieved because:
1. Only $O(\log n)$ levels exist, so component information is logarithmic in overhead
2. Sparse recovery sketches (using Fact 2.3) compress edge information to $O(\sqrt{f})$ bits per vertex per level, amortized across all levels
3. The final small crossing edge set $|X_l| = O(n\sqrt{f}\log^3 n)$ takes $\tilde{O}(n\sqrt{f})$ bits to store explicitly

## Applications in Engineering

### 1. **Dynamic Connectivity & Distance Queries**
Hierarchical decomposition enables fast distance queries in graphs subject to edge deletions:
- Query time: polylog$(n)$
- Space: $\tilde{O}(n\sqrt{f})$ where $f$ is the number of deleted edges
- Used in **network reliability analysis** and **fault-tolerant routing**

### 2. **Network Design & Resilience**
- Identify critical bottleneck edges (crossing edges at high levels)
- Optimize placement of redundant links in telecommunications networks
- Assess network robustness to failures

### 3. **Sparse Graph Approximation**
- Construct sparsifiers with provable approximation guarantees
- Reduce computational burden in large-scale graph analysis
- Enable efficient algorithms on sparse proxies of dense graphs

### 4. **Distributed Computing**
- Hierarchical structure naturally maps to **multi-level distributed architectures**
- Each level can be processed at different compute nodes
- Crossing edges define inter-node communication requirements

### 5. **Compiler Optimization & Program Analysis**
- Decompose program dependence graphs hierarchically
- Identify parallelization opportunities within components
- Optimize data locality by clustering tightly-coupled operations

## Common Mistakes / Pitfalls

### 1. **Confusing "Crossing Edges" with "Deleted Edges"**
- **Mistake:** Thinking $X_i$ represents edges to be removed from the graph
- **Reality:** $X_i$ edges are **retained and become the input** to the next level; they represent all edges between different components at level $i$
- The algorithm doesn't delete edges from $G$; it extracts a sub-graph for the next recursion level

### 2. **Misunderstanding