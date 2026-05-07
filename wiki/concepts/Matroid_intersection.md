# Matroid Intersection

## Definition

A **matroid intersection** problem asks: given $k$ matroids $\mathcal{M}_1, \mathcal{M}_2, \ldots, \mathcal{M}_k$ defined on a common ground set $U$, find a maximum-cardinality subset $S \subseteq U$ that is simultaneously independent in all matroids.

Formally, find:
$$S^* = \arg\max_{S \subseteq U} |S| \quad \text{such that} \quad S \in \mathcal{I}(\mathcal{M}_i) \text{ for all } i \in [k]$$

where $\mathcal{I}(\mathcal{M}_i)$ denotes the family of independent sets of matroid $\mathcal{M}_i$.

**Variant: Matroid Intersection with Constraints**

When additional structure is imposed (e.g., coloring, partitioning, or basis constraints), we reformulate the problem on an expanded ground set. For instance, a $q$-coloring problem over $k$ matroids can be reduced to $(k+1)$-matroid intersection by:
- Creating $q$ disjoint copies of the original ground set: $U' = U_1 \sqcup U_2 \sqcup \cdots \sqcup U_q$
- Defining $\mathcal{M}'_i$ as the disjoint union of $q$ copies of each input matroid $\mathcal{M}_i$
- Introducing a "partition matroid" $\mathcal{M}'_0$ that enforces at most one copy per element

## Key Equations

### Matroid Intersection Polytope (LP Relaxation)

The natural LP relaxation of the matroid intersection problem is:

$$\max \sum_{e \in U} x_e$$

subject to:

$$\sum_{e \in S} x_e \leq \text{rank}_{\mathcal{M}_i}(S) \quad \forall i \in [k], \, \forall S \subseteq U$$

$$x_e \geq 0 \quad \forall e \in U$$

This polytope is known to be integral (vertices are characteristic vectors of sets in the intersection), making it a foundation for exact algorithms.

### Cardinality Bound (König–Egerváry for Matroids)

For two matroids $\mathcal{M}_1, \mathcal{M}_2$ on ground set $U$:

$$\max \, |S| = \min_{A \subseteq U} \left( \text{rank}_{\mathcal{M}_1}(A) + \text{rank}_{\mathcal{M}_2}(U \setminus A) \right)$$

This generalizes Hall's theorem and matching in bipartite graphs.

## Physical Intuition / Derivation

### Why Matroid Intersection Matters

Matroids capture combinatorial independence structures (linear independence, forests in graphs, matchings, etc.). When we have **multiple independent constraints** that must be satisfied simultaneously—each naturally a matroid—their intersection becomes the natural feasibility region.

**Example**: In resource allocation, we might require:
1. Selected items form a spanning tree (graphic matroid)
2. Total weight stays under a budget (uniform matroid)
3. At most one item per category (partition matroid)

Finding a maximum set satisfying all three is a matroid intersection problem.

### The Reduction Strategy

The source material illustrates a sophisticated use of matroid intersection for **$k$-coloring**: instead of directly coloring vertices, we:

1. **Expand the ground set** to $U'$ with $q$ color classes
2. **Replicate constraints** across color copies
3. **Enforce partition structure** via $\mathcal{M}'_0$: each element appears in at most one color class

This transforms a difficult algorithmic problem (respecting independence in a union of matroids across colors) into a cleaner combinatorial optimization framework.

### The LP-Rounding Approach

The LOSZ-algorithm [referenced in source]:
- Solves the LP relaxation to obtain a fractional solution
- Constructs a basis $R$ of $\mathcal{M}'_0$ satisfying weaker guarantees
- Output is a basis (covers all colors) but may violate individual matroid constraints

The key insight is that **the LP solution possesses structure** that can be exploited post-hoc: one can identify conflicts and resolve them via a graph-coloring auxiliary problem rather than re-optimizing from scratch.

## Applications in Engineering

### 1. **Network Design & Routing**
- **Simultaneous spanning tree + degree constraint**: Select edges forming a tree while respecting degree limitations (partition matroid)
- **Multi-layer networks**: Ensure selected infrastructure is independent in capacity, topology, and failure modes

### 2. **Resource Allocation**
- **Scheduling with multiple precedence structures**: Tasks must respect process matroid (dependencies) AND partition matroid (machine assignment)
- **Portfolio optimization**: Assets must be diverse (uniform matroid) and satisfy industry exposure limits (partition matroid)

### 3. **Circuit & VLSI Design**
- **Gate selection**: Choose logic gates from a library such that they are linearly independent (linear matroid over a field) and each functional category is represented (partition matroid)
- **Interconnect design**: Routing paths must form a forest (graphic matroid) while respecting bandwidth-per-layer (uniform matroid per layer)

### 4. **Combinatorial Optimization & Approximation**
- **Matroid-constrained scheduling**: Assign jobs to machines respecting both precedence (graphic matroid) and load-balancing (uniform matroid) constraints
- **Hypergraph coloring**: Generalization of graph coloring where color classes must be independent in multiple hypergraphic structures

### 5. **Logistics & Supply Chain**
- **Supplier selection**: Choose suppliers to maintain supply chain independence (graphic matroid on supplier network) while respecting budget and capacity constraints (uniform, partition matroids)

## Common Mistakes / Pitfalls

### 1. **Assuming Greedy Works Universally**
- ❌ **Mistake**: Apply simple greedy (add maximum-weight element respecting mat