# Mortar Graph

## Definition

A **mortar graph** is a hierarchical graph decomposition structure used in the construction of Steiner tree spanners and related geometric approximation algorithms. It partitions a graph (typically planar) into rectangular regions called **bricks**, which are connected via a sparse set of carefully placed **portals** on their boundaries. The mortar graph itself consists of these portals and the edges connecting them, acting as a "frame" that constrains and approximates the original graph's Steiner tree solutions.

### Key Components

- **Bricks**: Rectangular subgraphs obtained by recursive spatial subdivision
- **Portals**: Connection points placed on brick boundaries at regular intervals (approximately $l(B)/\theta$ apart for boundary length $l(B)$)
- **Mortar**: The low-cost skeletal graph formed by portals and their interconnections
- **Terminal attachment**: Internal vertices attach to boundaries through poly$(1/\varepsilon)$ designated connection points

## Key Equations

**Portal spacing** on a brick boundary $B$ with $\theta$ portals:
$$\text{Portal spacing} \approx \frac{l(B)}{\theta}$$

**Cost increase per brick** when rerouting internal trees to portals:
$$\Delta \text{cost}(B) \leq \frac{l(B) \cdot \text{poly}(1/\varepsilon)}{\theta}$$

**Total mortar graph length** after aggregation over all bricks:
$$\text{Length}(\text{mortar}) \leq \text{poly}(1/\varepsilon) \cdot \text{StTree}(G, T)$$

**Steiner tree spanner length** with Steiner trees computed for all portal subsets:
$$\text{Length}(\text{spanner}) \leq 2^{\text{poly}(1/\varepsilon)} \cdot \text{StTree}(G, T)$$

where $\varepsilon$ is a geometric approximation parameter and $\text{StTree}(G,T)$ denotes the optimal Steiner tree length connecting terminal set $T$ in graph $G$.

## Physical Intuition / Derivation

### Why Mortars?

The mortar graph addresses a fundamental tension: computing optimal Steiner trees globally is expensive, but we need to approximate them efficiently. Rather than solving the problem monolithically, mortars decompose it spatially.

### Construction Strategy

1. **Spatial Partitioning**: Recursively subdivide the geometric space (or planar embedding) into bricks. This is typically done via recursive bisection, creating a quad-tree-like structure.

2. **Portal Placement**: On each brick's boundary, place $\theta$ evenly-spaced portals. The number $\theta = \text{poly}(1/\varepsilon)$ is chosen large enough to capture solutions to desired accuracy $\varepsilon$.

3. **Interior Routing**: Any internal tree connecting terminals within brick $B$ originally attaches to the boundary at poly$(1/\varepsilon)$ points. These attach points are "redirected" to the nearest portal, incurring cost at most $l(B)/\theta$ per attachment.

4. **Aggregation**: Sum the rerouting costs across all bricks. With $\theta = \text{poly}(1/\varepsilon)$ sufficiently large, total penalty is bounded as:
$$\text{Total penalty} = \text{poly}(1/\varepsilon) \cdot \text{StTree}(G,T) / \theta \leq \varepsilon \cdot \text{StTree}(G,T)$$

### Spanner Construction

For **each brick** $B$ and **every subset** of its $\theta$ portals, compute an optimal Steiner tree connecting those portals within $B$. This tree is added to the spanner. Since:
- There are $2^{\theta}$ subsets of portals
- Each subset requires Steiner tree computation: $2^{O(\theta)} \cdot n^{O(1)}$ time
- For **planar bricks with boundary terminals**, computation is polynomial-time tractable [NP-hard in general, but tractable via dynamic programming when graph is planar and terminals lie on a face boundary]

The result is a spanner of length at most $2^{\text{poly}(1/\varepsilon)} \cdot \text{StTree}(G,T)$, achieving approximation factor $2^{\text{poly}(1/\varepsilon)}$.

## Applications in Engineering

### Network Design

- **Telecommunication networks**: Approximating minimum-cost routing topologies that connect terminals (cities, data centers) with geometric constraints
- **Optical fiber routing**: Planning physical layout of fiber links on a substrate where spatial decomposition (municipal neighborhoods, regions) is natural

### VLSI and Floorplanning

- **Routing channels**: Connecting signal nets in integrated circuit layouts where the chip is partitioned into hierarchical blocks, each with limited routing resources
- **Rectilinear Steiner trees**: Finding near-optimal interconnect trees in Manhattan geometry with poly-logarithmic approximation guarantees

### Geometric Approximation Algorithms

- **Metric approximation**: Constructing spanners with guaranteed distortion and size bounds for graphs embedded in the plane
- **Machine learning on graphs**: Hierarchical graph representations for fast nearest-neighbor and similarity queries

### Computational Geometry

- **Shortest path queries**: Enabling fast approximate shortest paths via portal networks (similar to separator-based hierarchical methods)
- **Traveling salesman problem (TSP)**: Hierarchical approaches to TSP approximation via recursive decomposition

## Common Mistakes / Pitfalls

1. **Ignoring the exponential factor**: The factor $2^{\text{poly}(1/\varepsilon)}$ is exponential in $1/\varepsilon$. For small approximation targets (small $\varepsilon$), the constant becomes prohibitively large. This trades *approximation quality for practicality*.

2. **Portal placement naïveté**: Simply placing portals at regular intervals assumes the boundary length is comparable to the geometry. In highly non-convex shapes or non-planar embeddings, uniform spacing may miss critical topology.

3. **Not accounting for interior sparsity**: The method assumes the interior of each brick can be summarized by its portal connectivity. This breaks down if internal structure