# p-degenerate graphs

## Definition

A graph $G = (V, E)$ is **p-degenerate** (or has **degeneracy p**) if every subgraph of $G$ contains a vertex of degree at most $p$. Equivalently, the vertices of $G$ can be ordered such that each vertex has at most $p$ neighbors that appear later in the ordering (called a **degeneracy ordering**).

The **degeneracy** of a graph is the smallest integer $p$ for which the graph is $p$-degenerate. A graph class has **bounded degeneracy** if all graphs in the class are $p$-degenerate for some fixed constant $p$.

### Formal Characterization

A graph $G$ has degeneracy $\deg(G) = p$ if and only if:

$$\deg(G) = \min\{p : \text{every subgraph } H \subseteq G \text{ has a vertex with degree} \leq p\}$$

Equivalently, there exists an ordering $v_1, v_2, \ldots, v_n$ of vertices such that:

$$|N^+(v_i)| \leq p \quad \forall i$$

where $N^+(v_i) = \{v_j : j > i \text{ and } (v_i, v_j) \in E\}$ are the **forward neighbors** of $v_i$ in the ordering.

## Key Equations

**Edge bound for p-degenerate graphs:**
$$|E| \leq p|V|$$

This follows directly from the degeneracy ordering: summing forward degrees gives $\sum_i |N^+(v_i)| \leq pn$.

**Chromatic number bound:**
$$\chi(G) \leq p + 1$$

Any $p$-degenerate graph is $(p+1)$-colorable by greedily coloring vertices in reverse degeneracy order.

## Physical Intuition / Derivation

### Why Bounded Degeneracy Matters

Degeneracy captures a notion of **local sparsity**: even though the graph may have high-degree vertices (hubs), every subgraph contains a "low-density" region. This is fundamentally different from bounded-degree models, which restrict *all* vertices to have degree $\leq p$.

**Key structural insight:** A $p$-degenerate graph can have arbitrarily high maximum degree, but cannot have $p+1$ mutually adjacent vertices (a clique). The densest subgraph structure is inherently limited.

### Building Intuition

- **Planar graphs** are 5-degenerate (and 4-degenerate if not bipartite)
- **Graph families with excluded minors** (e.g., $K_r$-free graphs) have bounded degeneracy
- The degeneracy ordering provides a **natural decomposition**: each vertex depends on at most $p$ earlier vertices

### Constructing a Degeneracy Ordering

The greedy algorithm works:
1. While $G \neq \emptyset$:
   - Find a vertex $v$ with minimum degree in the current $G$
   - Add $v$ to the ordering
   - Remove $v$ from $G$

The maximum degree of any vertex in this process is the graph's degeneracy.

## Applications in Engineering

### 1. **Graph Property Testing in Restricted Models**
In the random neighbor oracle model, testers query uniform neighbors of vertices. For $p$-degenerate graphs, the structural constraint enables:
- **One-sided error testable properties** can be completely characterized based on connectivity of forbidden subgraphs
- High-degree hubs can hide violations across neighborhoods; testability depends on whether forbidden structures can be fragmented

### 2. **Distributed Algorithms & Network Design**
Degeneracy bounds apply to:
- **Social networks and web graphs** (often have bounded degeneracy despite heavy tails in degree distribution)
- **Hierarchical network design**: degeneracy ordering provides a natural priority ordering for distributed algorithms
- **Coloring and scheduling**: the $(p+1)$-coloring guarantee enables efficient distributed resource allocation

### 3. **Sparse Graph Algorithms**
For graphs with $|E| = O(p|V|)$:
- **Dynamic algorithm efficiency**: maintaining properties under edge insertions/deletions
- **Memory-constrained algorithms**: sparse representation and streaming algorithms
- **Approximation algorithms**: exploit local structure via degeneracy ordering

### 4. **Machine Learning on Graphs**
- **Graph neural networks**: degeneracy bounds help analyze message-passing complexity and receptive field growth
- **Feature selection**: degeneracy ordering identifies core vs. peripheral structure
- **Graph sampling**: degeneracy-aware sampling preserves structural properties better

### 5. **VLSI & Circuit Layout**
- **Planar circuit graphs**: their bounded degeneracy enables efficient placement algorithms
- **Routing and interconnect optimization**: degeneracy ordering guides hierarchical routing strategies

## Common Mistakes / Pitfalls

### 1. **Confusing Degeneracy with Maximum Degree**
❌ *Mistake:* "A $p$-degenerate graph has maximum degree $p$."

✓ *Correct:* A $p$-degenerate graph can have arbitrarily high maximum degree. The constraint is that *every subgraph* (not every vertex in the full graph) has a low-degree vertex.

### 2. **Assuming Degeneracy Order is Unique**
A graph may have multiple valid degeneracy orderings. The degeneracy value itself is unique, but the specific ordering is not canonical.

### 3. **Misapplying Edge Bounds**
❌ *Mistake:* "A $p$-degenerate graph on $n$ vertices has exactly $pn$ edges."

✓ *Correct:* It has *at most* $pn$ edges. Sparse $p$-degenerate graphs may have far fewer edges.

### 4. **Ignoring Hub Visibility in Testing**
When testing $p$-degenerate graphs via neighbor sampling, high-degree vertices ("hubs") can strategically mask forbidden substructures across their neighborhoods. Simple forbidden-subgraph characterizations (sufficient for minor-closed families) fail here.

### 5. **Assuming Bounded Degeneracy Implies Bounded