# Recursive Decomposition

## Definition

**Recursive decomposition** is an algorithmic technique for systematically breaking down a complex structure (typically a graph) into simpler substructures through hierarchical separation and decomposition. The method constructs a tree decomposition by recursively partitioning the vertex set using balanced separators, while carefully managing auxiliary sets that control both the depth and the width of the resulting decomposition.

Formally, given a graph $G = (V, E)$ and a target solution set $Z \subseteq V$, recursive decomposition produces a tree decomposition $\mathcal{T}$ where:
- Bags are subsets of vertices with bounded intersection with $Z$
- The decomposition respects hierarchical separations $(A, B)$ where $A \cup B = V$ and $A \cap B$ is a separator
- The algorithm balances multiple objectives simultaneously to control decomposition parameters

## Key Equations

**Balanced Separation Constraint:**
$$|A \cap B| = \tilde{O}(\sqrt{k})$$

where $k$ is a parameter bounding the solution size and $\tilde{O}$ denotes suppression of polylogarithmic factors.

**Bag-Solution Intersection Bound:**
$$|Z \cap \text{Bag}_i| \leq \tilde{O}(\sqrt{k})$$

for each bag $\text{Bag}_i$ in the tree decomposition.

**Accumulated Solution Growth (problematic):**
$$|Z \cap R| \leq \text{depth} \cdot \tilde{O}(\sqrt{k}) = \Theta(\log n) \cdot \tilde{O}(\sqrt{k})$$

This inequality illustrates the accumulation problem that requires "pattern mode" to resolve.

**Probability of Direct Separation Use:**
$$P(\text{use separation directly}) = 1 - \frac{1}{k}$$

## Physical Intuition / Derivation

### The Core Problem

When constructing tree decompositions, we face conflicting objectives:

1. **Balance for depth:** We want separators that split the vertex set roughly equally ($|A \setminus B| \approx |B \setminus A|$) to keep tree depth at $O(\log n)$

2. **Balance for auxiliary sets:** We maintain a set $R$ (retained vertices) that grows when we recursively decompose. If we naively include $A \cap B$ in $R$ at each step, it accumulates to $\text{poly}(k) \cdot \log n$, which is too large

3. **Controlling solution intersection:** We need $Z \cap (A \cap B)$ to stay bounded near $\tilde{O}(\sqrt{k})$ throughout—but this is unknown to the algorithm

### The Three-Mode Solution

The algorithm cycles through three separation modes in round-robin fashion to address these challenges:

**Mode 1: Vertex-balanced separation**
- Balance with respect to total vertices: $|A \setminus R| \approx |B \setminus R|$
- Maintains tree depth at $O(\log n)$
- Run deterministically

**Mode 2: Set-balanced separation** (probability $1 - 1/k$)
- Balance with respect to auxiliary set $R$: choose $(A, B)$ so $|A \cap R| \approx |B \cap R|$
- Prevents $R$ from growing unboundedly
- If the separation happens to have $|(Z - R) \cap A \cap B| \leq \tilde{O}(\sqrt{k})$, use it directly
- Otherwise, invoke enhancement procedure (Theorem 2.3)

**Mode 3: Pattern mode** (probability $1/k$)
- Seek a separation balanced with respect to the *unknown* set $Z \cap R$
- Without knowing $Z$, sample from $O(|R|)$ candidate separations and enhance
- Prevents accumulation of $|Z \cap R|$ across recursive levels

### Why This Works

Each mode addresses a scaling issue:
- After depth $d$, Mode 1 ensures $d = O(\log n)$
- Mode 2 activates frequently enough that $|R|$ remains at most $\text{poly}(k)$
- Mode 3 activates frequently enough that despite adding $\tilde{O}(\sqrt{k})$ solution vertices to $R$ per step, total accumulation stays bounded by careful probability analysis

The round-robin cycling ensures that no single bottleneck grows out of control.

## Applications in Engineering

### 1. **Parameterized Algorithm Design**
Recursive decomposition is fundamental to fixed-parameter tractable (FPT) algorithms for NP-hard problems:
- **Feedback Vertex Set:** Decompose a graph to find minimum vertices whose removal breaks all cycles
- **Vertex Cover:** Recursively partition to find minimum vertex cover with bounded parameter
- **Pathwidth/Treewidth Approximation:** Construct near-optimal width decompositions

### 2. **Circuit Design & VLSI**
- **Hierarchical partitioning:** Decompose large circuits into modules with minimal interconnect
- **Balanced block placement:** Ensure load is distributed evenly while minimizing communication between blocks

### 3. **Network Routing & Distributed Systems**
- **Hierarchical network decomposition:** Structure overlay networks as trees to control routing table sizes
- **Load balancing:** Recursively partition server clusters to distribute traffic with bounded bottlenecks

### 4. **Computational Biology**
- **Protein structure decomposition:** Recursively partition protein interaction networks to identify functional modules
- **Gene regulatory network analysis:** Decompose networks while preserving critical regulatory paths

### 5. **Data Structure Design**
- **Divide-and-conquer trees:** Build efficient query structures (e.g., segment trees, B-trees) through recursive decomposition
- **Cache-oblivious algorithms:** Decompose data recursively to exploit multi-level memory hierarchies

## Common Mistakes / Pitfalls

### 1. **Ignoring Auxiliary Set Growth**
**Mistake:** Including $A \cap B$ in $R$ without controlling its growth.
**Fix:** Balance separator choice between vertex-count and set-size criteria; don't use one criterion exclusively.

### 2. **Accumulation Without Periodic Rebalancing**
**Mistake:** Assuming that adding