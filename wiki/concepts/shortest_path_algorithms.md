# Shortest Path Algorithms

## Definition

A **shortest path algorithm** is a computational procedure that finds the path with minimum total cost (distance, time, or weight) between two nodes in a graph. Given a graph $G = (V, E)$ with edge weights $w: E \to \mathbb{R}^+$, the shortest path problem seeks a sequence of nodes $v_0, v_1, \ldots, v_k$ such that:

$$\text{dist}_G(v_0, v_k) = \min \left\{ \sum_{i=0}^{k-1} w(v_i, v_{i+1}) : \text{all paths from } v_0 \text{ to } v_k \right\}$$

The **distance** $\text{dist}_G(u, v)$ between two nodes is the weight sum of edges in any shortest path connecting them.

More specialized variants include:
- **Single-source shortest path**: finding shortest paths from one source to all other nodes
- **All-pairs shortest paths**: computing distances between every pair of nodes
- **Approximate shortest paths**: finding paths with distance within a multiplicative-additive factor

An **(α, β)-spanner** is a subgraph $H \subseteq G$ where distances are preserved within a bounded stretch:
$$\text{dist}_H(u, v) \leq \alpha \cdot \text{dist}_G(u, v) + \beta \quad \forall u, v \in V$$

This notion is central to efficient shortest path approximation.

## Key Equations

**Distance preservation in spanners:**
$$\text{dist}_H(x, y) \leq \alpha \cdot \text{dist}_G(x, y) + \beta$$

**Stretch factor:** For a pair $(x, y)$ in subgraph $H$:
$$\text{stretch}(x, y) = \frac{\text{dist}_H(x, y)}{\text{dist}_G(x, y)}$$

The goal of shortest path algorithms is often to keep stretch below threshold $\alpha$ with additive slack $\beta$.

**Bad pair detection criterion:**
$$\text{dist}_H(x, y) > \alpha \cdot \text{dist}_G(x, y) + \beta \quad \Rightarrow \quad (x,y) \text{ requires fixing}$$

**Bottleneck characterization:** An edge $e = (u, v)$ on path $P_{x,y}$ is $\alpha$-distant if:
$$\text{dist}_H(u, v) > \alpha \cdot \text{dist}_G(u, v)$$

## Physical Intuition / Derivation

Shortest path algorithms address a fundamental problem in optimization: how to navigate networks efficiently. The derivation progresses through three key insights:

### Attempt 1: Naive Completion (Over-Correction Problem)

The intuitive first approach adds all edges along any shortest path in $G$ to repair subgraph $H$:

```
While ∃ (x,y): dist_H(x,y) > α·dist_G(x,y) + β:
    Add all missing edges from shortest path P_{x,y}
```

**Problem:** This over-corrects. If we need only a small fix, adding an entire shortest path is wasteful—it forces $\text{dist}_H(x, y) = \text{dist}_G(x, y)$, which is stronger than necessary. The subgraph becomes too dense.

### Attempt 2: Bottleneck Fixing (Incomplete Solution)

Instead of adding all edges, we observe that only certain edges matter. Along path $P_{x,y}$, an edge is a **bottleneck** if the current subgraph $H$ doesn't already provide a good shortcut around it:

```
While ∃ (x,y): dist_H(x,y) > α·dist_G(x,y) + β:
    Find shortest path P_{x,y} in G
    For each edge e = (u,v) on P_{x,y}:
        If dist_H(u,v) > α·dist_G(u,v):  // α-distant
            Add e to H
```

**Key insight:** If all $\alpha$-distant edges on a path are added, then:
$$\text{dist}_{H'}(x, y) \leq \alpha \cdot \text{dist}_G(x, y)$$

This is because each segment between consecutive non-α-distant edges contributes at most $\alpha \cdot (\text{segment distance in } G)$.

**Remaining issue:** No explicit control over total edges added—worst case still too many iterations.

### Attempt 3: Shortcuts via Segmentation (Successful)

The final refinement exploits existing paths in $H$ to bypass bottlenecks. The algorithm partitions $P_{x,y}$ into **minimal segments**, where each segment is either:
- A single $\alpha$-distant edge, **or**
- Two vertices already connected in $H$ with stretch $\leq \alpha$

```
While ∃ (x,y): dist_H(x,y) > α·dist_G(x,y) + β:
    Find shortest path P_{x,y} in G
    Partition P_{x,y} into minimal segments
    Add edges for single-edge segments only
```

**Why it works:** By allowing "jumps" over multiple edges when $H$ already provides a good path, we:
1. Reduce redundant edge additions
2. Enforce sparsity: each pair is processed only when necessary
3. Maintain correctness: the recursive structure ensures distance bounds

This is analogous to **dynamic programming** in shortest path algorithms—we build the solution incrementally, leveraging previously solved subproblems.

## Applications in Engineering

### 1. **Network Routing & Communication**
- **Telephone networks**: Computing least-cost paths for call routing
- **IP routing protocols** (OSPF, IS-IS): Finding minimum-hop or minimum-delay routes
- **Software-defined networks (SDN)**: Computing paths for network flows in real-time

### 2. **Transportation & Logistics**
- **GPS navigation**: Finding fastest routes between locations (Dijkstra/A*)
- **