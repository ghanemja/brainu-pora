# weight function

## Definition

A **weight function** is a mapping $\chi : V(G) \to \mathbb{R}_{\geq 0}$ (or more restrictively $\{0,1\}$) that assigns a non-negative scalar weight to each vertex in a graph $G$. In the context of decomposition and partitioning problems, it quantifies the "mass" or "importance" of vertices, enabling structured analysis of graph properties through weighted aggregation.

The **total weight** of a set $S \subseteq V(G)$ is defined as:
$$\chi(S) := \sum_{v \in S} \chi(v)$$

The total weight of the entire vertex set is denoted $W := \chi(V(G))$.

## Key Equations

For a tree decomposition $(T, \beta)$ with bags $b \in V(T)$ and corresponding vertex sets $\beta(b) \subseteq V(G)$:

**Bag weight:**
$$w_b = \chi(\beta(b)) = \sum_{v \in \beta(b)} \chi(v)$$

**Component weight** (after removing edge set $F$ from the decomposition tree):
$$w_C = \chi\left(\bigcup_{b \in C} \beta(b)\right)$$

where $C$ is a connected component of $T - F$.

**Fractional weight threshold** (from Lemma 3.6):
$$w_b \geq \frac{W}{4k} \quad \text{or} \quad w_C \geq \frac{W}{4k}$$

where $k$ is a parameter controlling the density of edge cuts.

## Physical Intuition / Derivation

Weight functions encode **non-uniform importance** in graph-theoretic problems. Consider a planar network where vertices represent cities (with populations $\chi(v)$) connected by roads (edges):

1. **Motivation for weighted analysis**: Not all vertices are equal. A tree decomposition partitions the graph into "bags" (overlapping subgraphs). To understand the graph's structure, we ask: *where is the mass concentrated?*

2. **Partitioning principle**: Lemma 3.6 guarantees a dichotomy—either:
   - Some bag contains a significant fraction ($\geq W/4k$) of the total weight, or
   - We can cut $k$ edges in the decomposition tree to isolate components, each with significant weight.

3. **Recursive structure**: This result enables **divide-and-conquer**: remove heavy bags or cut the tree strategically, recurse on lighter subproblems. The factor $1/4k$ represents the trade-off between bag density and cutting density.

4. **Why binary weights $\{0,1\}$?** In algorithmic applications, binary weights count *selected* vs. *unselected* vertices, allowing the lemma to apply to problems like finding balanced cuts or coresets (as seen in the Euclidean setting).

## Applications in Engineering

### 1. **Network Design & Load Balancing**
   - Assign $\chi(v) =$ traffic demand at node $v$
   - Use weight functions to find balanced partitions of network graphs
   - Ensure no single bag/partition handles more than a target fraction of total load

### 2. **Computational Geometry & Coresets**
   - In point set analysis, $\chi(v) = $ distance-dependent measure (e.g., $\chi(v) \in \{0,1\}$ indicating whether point $v$ is in the coreset)
   - Weight function ensures representative sampling: heavy components cannot be ignored
   - Applied to furthest-neighbor approximation (as in source material)

### 3. **VLSI & Circuit Partitioning**
   - Weight vertices by gate count, power consumption, or area
   - Minimize weighted edge-cut when partitioning circuits into subcells
   - Guarantee each partition has balanced weight

### 4. **Graph Coloring & Scheduling**
   - Assign $\chi(v) =$ task duration or resource requirement
   - Weighted tree decomposition ensures no scheduling subtask exceeds capacity

### 5. **Approximation Algorithms**
   - Weight functions enable **relative approximation**: guarantee solutions within factor $(1 + \epsilon)$ of optimal weighted metric
   - Key tool in deriving approximation schemes for NP-hard problems on planar/sparse graphs

## Common Mistakes / Pitfalls

### ❌ **Confusing global and local weight**
- **Mistake**: Treating $\chi(v)$ (single vertex) and $\chi(S)$ (set sum) identically in inequalities.
- **Fix**: Always track whether you're analyzing vertex weights or aggregate bag weights. The lemma's threshold $W/4k$ applies to bags (aggregates), not individual vertices.

### ❌ **Assuming uniform weight distribution**
- **Mistake**: Expecting all bags to have similar weight, even when a weight function is defined.
- **Fix**: Weight functions are inherently *non-uniform*. The lemma's value is precisely that it handles imbalanced weights without assuming structure.

### ❌ **Neglecting the tree decomposition structure**
- **Mistake**: Applying weight functions to arbitrary graphs without respect to the decomposition tree $T$.
- **Fix**: Weight functions are meaningful *relative to* a chosen decomposition. Different decompositions with the same graph can yield different structural properties.

### ❌ **Misinterpreting the dichotomy**
- **Mistake**: Thinking "either a heavy bag exists OR cutting edges isolates heavy components"—as if these are mutually exclusive.
- **Fix**: The dichotomy is a guarantee: *at least one* condition holds. Both may hold simultaneously. The power is that we're *guaranteed* to find a structured cut or heavy region.

### ❌ **Ignoring degree constraints**
- **Mistake**: Applying Lemma 3.6 to arbitrary decomposition trees.
- **Fix**: The lemma requires tree-degree $\leq 3$. Higher-degree trees may fail the conclusion.

## See Also

- [[tree decomposition]] — Foundational concept for partitioning graphs hierarchically
- [[treewidth]] — Measures graph complexity via decomposition bag sizes; interacts with weight functions in dynamic programming
- [[planar graphs