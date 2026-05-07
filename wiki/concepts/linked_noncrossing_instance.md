# Linked Noncrossing Instance

## Definition

A **linked noncrossing instance** is a combinatorial-topological structure consisting of a set of vertex pairs $\{(p_i, q_i)\}_{i=1}^{\ell}$ in a metric space (typically embedded in the plane or a graph) such that:

1. **Linkedness constraint**: For each pair $(p_i, q_i)$, there exists a path $\langle p_i q_i \rangle$ in the underlying graph with bounded length relative to the direct distance between endpoints.

2. **Pairwise disjointness constraint**: All paths are pairwise disjoint, meaning $\langle p_i q_i \rangle \cap \langle p_j q_j \rangle = \emptyset$ for $i \neq j$ (except possibly at endpoints).

3. **Separation property**: For any two distinct pairs $(i,j)$, the "crossing paths" $\langle p_i q_j \rangle$ and $\langle p_j q_i \rangle$ are also pairwise disjoint.

The structure forms a **comatching** (complementary matching) in the underlying graph with topological constraints enforcing a specific planar arrangement.

---

## Key Equations

### Path Length Constraint

For a linked noncrossing instance with distortion parameter $\varepsilon$:

$$\text{dist}(p_i, q_i) \leq (1+\varepsilon)R$$

where $R$ is a reference distance scale and the paths realize this distance approximately in the metric.

### Separation Lemma (Contradiction Proof)

For crossing paths $\langle p_i q_j \rangle$ and $\langle p_j q_i \rangle$, if they intersect at vertex $u$:

$$2(1-\varepsilon)R \geq \text{dist}(p_i, q_j) + \text{dist}(p_j, q_i)$$

$$= [\text{dist}(p_i, u) + \text{dist}(u, q_j)] + [\text{dist}(p_j, u) + \text{dist}(u, q_i)]$$

$$\geq \text{dist}(p_i, q_i) + \text{dist}(p_j, q_j) > 2R$$

This inequality is a contradiction when paths satisfy the linkedness constraint, proving the crossing paths must be disjoint.

### Size Bound

The maximum number of pairs in a linked noncrossing instance is bounded by:

$$\ell = O(1/\varepsilon)$$

This logarithmic/inverse relationship arises from the topological constraints forcing a "ladder-like" arrangement (Figure 6) in planar embeddings.

---

## Physical Intuition / Derivation

### Why the Constraint Structure Matters

A linked noncrossing instance emerges when studying **packing problems** in metric spaces with topological constraints:

1. **Linkedness** ensures paths don't collapse—they must "work hard" to connect their endpoints, ruling out degenerate cases.

2. **Pairwise disjointness** of the main paths $\langle p_i q_i \rangle$ prevents trivial overlaps but allows a nontrivial geometric structure.

3. **Separation of crossing paths** is the **key insight**: If we want to go from $p_i$ to $q_j$ AND from $p_j$ to $q_i$ simultaneously, these paths cannot meet. This forces an alternating, interleaved arrangement—essentially a **planar ladder structure**.

### Derivation of the Separation Lemma

The contradiction proof is elegant:
- Suppose paths $\langle p_i q_j \rangle$ and $\langle p_j q_i \rangle$ meet at vertex $u$.
- By triangle inequality, the sum of distances via the intersection point equals the sum if we "break" the paths at $u$.
- Rearranging: the sum bounds $\text{dist}(p_i, q_i) + \text{dist}(p_j, q_j)$ from below.
- But this sum must exceed $2R$ (the total "budget"), contradicting the linkedness constraint.
- **Conclusion**: The paths *must* avoid each other, forcing a geometric ordering.

---

## Applications in Engineering

### 1. **Network Routing & VLSI Design**
- Routing multiple nets in circuit layouts with non-crossing constraint reduces interference and crosstalk.
- The linked noncrossing structure ensures disjoint paths for critical signal pairs, improving signal integrity.

### 2. **Planar Graph Algorithms**
- Used in analyzing upper bounds on the size of **distance-based matchings** in planar graphs.
- Relevant to approximation algorithms for bottleneck matching and facility location problems.

### 3. **Metric Embedding & Dimension Reduction**
- Provides bounds on **VC-dimension** (mentioned in source material) of distance ball systems.
- Used to prove data-dependent bounds for learning algorithms in metric spaces.

### 4. **Graph Minor Theory & Topology**
- Extends to **bounded genus graphs** via cutting into planar components; relevant to:
  - Topological graph algorithms
  - Routing and packing on non-planar surfaces (bounded-genus networks)

### 5. **Wireless Network Covering**
- Linked structures arise when placing non-interfering broadcast regions with distance constraints.
- The arrangement bound $O(1/\varepsilon)$ gives hardness limits for certain coverage problems.

---

## Common Mistakes / Pitfalls

### 1. **Confusing "Pairwise Disjoint" Constraints**
   - *Error*: Assuming that if paths $\langle p_i q_i \rangle$ and $\langle p_j q_j \rangle$ are disjoint, then the crossing paths $\langle p_i q_j \rangle$ and $\langle p_j q_i \rangle$ are automatically disjoint.
   - *Correct*: The crossing constraint requires a separate proof (Lemma 2.1). It follows from linkedness, not main-path disjointness.

###