# k-chordal graphs

## Definition

A graph $G = (V, E)$ is **k-chordal** if every induced cycle in $G$ has length at most $k$.

**Key observation:** Chordal graphs are precisely 3-chordal graphs (all induced cycles have length ≤ 3, meaning no induced cycles of length ≥ 4).

More generally:
- **3-chordal** = chordal graphs (no induced cycles of length > 3)
- **4-chordal** = graphs with no induced cycles of length > 4
- **k-chordal** = graphs with no induced cycles of length > k

A graph contains an induced cycle of length $\ell$ if there exists a sequence of distinct vertices $v_1, v_2, \ldots, v_\ell$ such that:
- $(v_i, v_{i+1}) \in E$ for $i = 1, \ldots, \ell-1$
- $(v_\ell, v_1) \in E$
- No other edges connect vertices in this cycle (induced property)

## Key Equations

### Treelength Bound for k-chordal Graphs

For a $k$-chordal graph $G$ with tree decomposition $(T, \{V_t\}_{t \in V(T)})$:

$$\text{tl}(G) = O(k)$$

where the **treelength** is defined as:

$$\text{tl}(G) = \min \left\{ j \mid \exists \text{ tree decomposition where } d_G(u,v) \leq j \text{ for all } u,v \in V_t \right\}$$

**Special cases:**
$$\text{tl}(K_n) = 1 \quad \text{(complete graph)}$$
$$\text{tl}(G) = 1 \quad \text{if } G \text{ is chordal}$$

## Physical Intuition / Derivation

### Why k-chordality Matters

The concept of k-chordality provides a **gradual generalization** of chordal graphs. Rather than requiring the highly restrictive property that every cycle has a chord (3-chordal), we allow cycles up to length $k$, permitting sparser structures while retaining useful algorithmic properties.

### Connection to Tree Decomposition

The relationship between k-chordality and treelength reveals a fundamental principle:

1. **Chordal graphs** can be perfectly represented by tree decompositions where vertices in the same bag are already adjacent (treelength = 1)

2. **k-chordal graphs** allow vertices in the same bag to be at distance up to $O(k)$, reflecting that the graph is "nearly tree-like" with controlled cyclic structure

### Induced Cycles as Structural Obstruction

An induced cycle of length $\ell$ is the "worst case" local structure because:
- It cannot be decomposed further (no shortcuts exist)
- It forces vertices at distance $\ell-1$ to appear together in some bag
- Longer induced cycles require larger distances within bags

## Applications in Engineering

### 1. **Network Topology Analysis**
- Sparse communication networks often exhibit k-chordal structure
- Treelength bounds enable efficient routing algorithms with distance guarantees
- Used in delay-sensitive network design

### 2. **VLSI Circuit Layout**
- k-chordal models capture partially hierarchical circuits
- Tree decompositions guide hierarchical placement strategies
- Layering trees (as defined in source) decompose circuits into manageable layers

### 3. **Computational Geometry & Robotics**
- Merge trees and split trees (dual notions to layering trees) decompose configuration spaces
- k-chordal abstractions model motion planning graphs with bounded detours
- Enables efficient computation of approximate distances

### 4. **Wireless Sensor Networks**
- k-chordal properties guarantee bounded hop distances and latency
- Tree decompositions enable distributed algorithms with logarithmic communication complexity
- Structure guides localization algorithms

### 5. **Database Indexing (Join Trees)**
- Query optimization uses tree decompositions of constraint graphs
- k-chordal structure restricts query complexity
- Enables polynomial-time evaluation of certain database queries

## Common Mistakes / Pitfalls

### 1. **Confusing "chordal" with "k-chordal for large k"**
- ❌ Thinking 4-chordal ≈ chordal
- ✅ 3-chordal = chordal; everything else is strictly weaker
- The distinction is crucial: many properties break for $k > 3$

### 2. **Misinterpreting the treelength bound**
- ❌ Assuming treelength is exactly $k$ for a k-chordal graph
- ✅ It's $O(k)$ — a worst-case bound; actual treelength may be much smaller
- Different graphs with same $k$ can have vastly different treelengths

### 3. **Forgetting the "induced" qualifier**
- ❌ Assuming any cycle of length > k is forbidden
- ✅ Only **induced** cycles > k are forbidden; longer cycles with chords are allowed
- This distinction is essential for understanding the graph structure

### 4. **Overlooking computational complexity**
- ❌ Assuming that k-chordality automatically makes problems polynomial-time solvable
- ✅ While some problems become tractable, others remain hard unless additional structure is exploited

### 5. **Misapplying layering trees**
- ❌ Expecting the layering tree to be unique
- ✅ The tree depends on choice of root vertex $s$; different roots yield different decompositions
- The length bound $l(T) = O(k)$ holds for any choice of root

## See Also

- [[Chordal graphs]] — the foundational 3-chordal case with maximum clique tree structure
- [[Tree decomposition]] — formal framework for representing graphs as trees of subsets
- [[Treelength]] — distance metric within bags measuring how "close" decomposition is to true tree
- [[Layering tree (BFS decomposition)]] — practical construction tool partitioning