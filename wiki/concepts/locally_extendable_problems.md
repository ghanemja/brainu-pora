# Locally Extendable Problems

## Definition

A **locally extendable problem** is a graph algorithmic problem that admits a deterministic procedure capable of extending a partial solution across a graph cut in work proportional to the cut size. Formally, given:

- A graph $G = (V, E)$ with a partition of vertices into sets $A$ and $B$ (separated by a cut $C$)
- A valid solution $S_A$ on the subgraph induced by $A$

A problem is locally extendable if there exists a deterministic algorithm that computes a valid solution $S$ on $G \cup B$ using work bounded by $O(|C|)$, where $|C|$ is the size of the cut (number of edges crossing the partition).

**Key characteristic**: The extension procedure's complexity depends only on the *interface* between solution components, not on the sizes of the components themselves.

## Key Equations

### Work Bound for Locally Extendable Problems

For a problem with local extensibility, a divide-and-conquer parallel algorithm achieves:

$$W(n) = O(m) \text{ work with high probability}$$

$$D(n) = O(\text{polylog}(n)) \text{ depth with high probability}$$

where $m = |E|$ is the number of edges in the input graph.

### Cut-Based Work Analysis

If a graph is partitioned into components with maximum cut size $C_{\max}$, the total extension work across all cuts is:

$$W_{\text{ext}} = \sum_{\text{all cuts}} O(|C_i|) = O(m)$$

This holds because each edge contributes to at most one cut in a recursive partition tree.

### Culled Balanced Partition Guarantee

After removing a polylogarithmic-sized "cull set" of high-degree vertices:

$$|V_{\text{cull}}| = O(\text{polylog}(n))$$

The remaining graph admits a balanced random partition with high probability:

$$\left||A| - |B|\right| = O(n / 2) \quad \text{whp}$$

$$|C| = O\left(\frac{m}{\text{polylog}(n)}\right) \quad \text{whp}$$

## Physical Intuition / Derivation

### Why Local Extensibility Matters

Consider computing a maximal independent set (MIS) on a graph:

1. **Without local extensibility**: If you solve MIS independently on each partition and try to merge, you might need $O(n)$ work per merge to fix conflicts throughout the component—work not proportional to the cut.

2. **With local extensibility**: MIS is locally extendable because vertices in the cut can be processed independently based only on their neighbors across the partition. Work scales with edge count, not vertex count.

### The Culled Partition Scheme

The algorithm works in phases:

**Phase 1 (Culling)**: Iteratively identify and remove vertices with degree $> \text{polylog}(n)$. This requires only $O(\text{polylog}(n))$ rounds because:
- At each step, removing one high-degree vertex reduces total degree sum
- Only polylogarithmic iterations needed until all remaining vertices have bounded degree
- Work: $O(n \text{ polylog}(n)) = O(n)$ total

**Phase 2 (Partition)**: Apply a random vertex partition to remaining low-degree graph:
- For a graph with maximum degree $\Delta = O(\text{polylog}(n))$, a random balanced partition yields:
  - $\mathbb{E}[|C|] = O(n/2)$ by linearity of expectation
  - $|C| = O(n/2 \pm o(n))$ with high probability via bounded differences inequality

**Phase 3 (Recurse)**: Solve subproblems on smaller pieces, extend solutions across cuts using local extensibility.

### Work Accumulation

$$\text{Total Work} = \underbrace{O(n)}_{\text{culling}} + \underbrace{O(m/\text{polylog}(n))}_{\text{cut work per level}} \times \underbrace{O(\text{polylog}(n))}_{\text{depth}} = O(m)$$

The key insight: although depth grows polylogarithmically, the per-level work shrinks by a matching polylogarithmic factor due to balanced cuts.

## Applications in Engineering

### 1. **Graph Coloring**
- Problem: $(Δ+1)$-vertex coloring
- Local extension: Recolor vertices in the cut based only on their incident edges
- Practical use: Register allocation in compilers, frequency assignment in wireless networks
- **Bounds achieved**: $O(m)$ work, $O(\text{polylog}(n))$ depth whp

### 2. **Maximal Independent Set**
- Problem: Find maximum subset of non-adjacent vertices
- Local extension: Include cut vertices greedily; update only affected neighbors
- Practical use: Task scheduling, network routing, resource allocation
- **Bounds achieved**: $O(m)$ work, $O(\text{polylog}(n))$ depth whp

### 3. **Parallel Semisort**
- Problem: Partition array into sorted blocks of polylogarithmic size
- Local extension: Merge sorted pieces by redistributing elements across boundaries
- Practical use: Sorting engines for databases, GPU sorting pipelines
- **Bounds achieved**: $O(n)$ work, $O(\text{polylog}(n))$ depth whp

### 4. **Distributed Systems**
- Graph algorithms in MapReduce/Spark (each partition is independently solvable, reduced communication across cuts)
- Decomposition of social networks into locally-computable features
- Parallel graph processing frameworks (GraphLab, PowerGraph)

## Common Mistakes / Pitfalls

### 1. **Confusing Work with Depth**
**Mistake**: Assuming that because depth is polylogarithmic, work must also scale as $\text{polylog}(n)$.

**Reality**: Work can be linear while depth is polylogarithmic. The culled partition scheme enables this by carefully balancing:
$$\text{Work per level} \times \text{Number of levels} = O(m/\