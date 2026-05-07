# Cycle Cover

## Definition

A **cycle cover** of a directed graph $G = (V, E)$ is a set of vertex-disjoint cycles such that every vertex in $V$ belongs to exactly one cycle. In the context of weighted graphs, a **minimum-weight cycle cover** is the cycle cover that minimizes the total weight of all edges in the cycles.

More formally: given a weighted directed graph $G$, a cycle cover $\text{CYC}(G) = \{c_1, c_2, \ldots, c_k\}$ is a partition of vertices such that:
- Each $c_i$ forms a directed cycle
- $V = \bigcup_{i=1}^{k} V(c_i)$ (every vertex is in exactly one cycle)
- $V(c_i) \cap V(c_j) = \emptyset$ for $i \neq j$ (cycles are vertex-disjoint)

The weight of the cycle cover is:
$$w(\text{CYC}(G)) = \sum_{c \in \text{CYC}(G)} w(c) = \sum_{e \in E(\text{CYC})} w(e)$$

where $E(\text{CYC})$ denotes all edges appearing in the cycles.

## Key Equations

For Algorithm 1 (the 8/3-approximation algorithm for shortest common superstring with reverse complements):

**Output length bound:**
$$\text{ALG}(S) = w(\text{CYC}(G_{\text{dist}}(T))) + \sum_{d \in \text{CYC}(G_{\text{dist}}(T))} \text{OV}_d$$

**Overlap loss per cycle:**
$$\text{OV}_d \leq \frac{2}{3} \sum_{\{j | t'_j \in d\}} w(c_j)$$

**Approximation ratio:**
$$\text{ALG}(S) \leq \frac{8}{3} \cdot \text{OPT}(S)$$

## Physical Intuition / Derivation

A cycle cover provides a systematic way to decompose a graph into independent cycles. The minimum-weight version is particularly useful in optimization problems where:

1. **Problem decomposition**: Complex string assembly or routing problems can be decomposed into independent cycles, which are easier to solve locally.

2. **Graph representation**: In the context of the Shortest Common Superstring (SCS) problem, vertices represent strings and edges represent overlaps between consecutive strings. A cycle cover represents a way to chain all input strings together, where each cycle must be "broken" to form a linear superstring.

3. **Structural guarantee**: By ensuring every vertex appears in exactly one cycle, the cycle cover guarantees complete coverage of the input without duplication, which is essential for approximation analysis.

**Why it works for SCS-RC:**
- Step 1: Build a distance graph from input strings $S$, compute a minimum-weight cycle cover
- Step 2: Extract strings from each cycle by concatenating overlapping strings
- Step 3: Create a new distance graph from the extracted strings and compute another cycle cover
- Step 4: Break cycles carefully by removing edges with bounded overlap loss (at most $\frac{2}{3}$ of the two incident edge weights)

This two-level decomposition ensures that the accumulated approximation error remains bounded at $\frac{8}{3}$ of the optimal solution.

## Applications in Engineering

### String Processing & Bioinformatics
- **DNA sequence assembly**: Determining the order of overlapping DNA fragments (reads) to reconstruct genomic sequences
- **De Bruijn graphs**: Cycle covers help identify Eulerian paths in assembly graphs
- **Shortest common superstring**: Finding minimal strings that contain all input sequences as substrings

### Logistics & Route Optimization
- **Vehicle routing**: Decomposing delivery networks into independent cycles for multi-vehicle routing problems
- **Circuit design**: Finding minimal interconnection patterns when routing must cover all components

### Network Design
- **Redundancy analysis**: Identifying independent failure-safe loops in communication networks
- **Graph partitioning**: Decomposing network topology for distributed processing

### Computational Geometry
- **Polygon coverage**: Partitioning planar graphs into independent cycles for efficient traversal

## Common Mistakes / Pitfalls

1. **Confusing with Eulerian cycles**: A cycle cover covers *vertices* (each vertex in exactly one cycle), while an Eulerian cycle covers *edges* (each edge exactly once). These are different concepts with different algorithms.

2. **Assuming uniqueness**: A graph typically has multiple valid cycle covers. The minimum-weight cycle cover is unique in terms of total weight, but the actual cycle structure may vary depending on tie-breaking in the algorithm.

3. **Ignoring self-loops**: The problem statement explicitly excludes self-loops (vertices with edges to themselves) from consideration, as they trivially form 1-cycles and don't contribute meaningfully to optimization.

4. **Overlooking approximation analysis dependencies**: In Algorithm 1, the $\frac{8}{3}$ ratio depends critically on:
   - Two-stage decomposition (cycles from $S$, then cycles from $T$)
   - The $\frac{2}{3}$ bound on overlap loss (Lemma 9)
   - Specific choices about when to use forward vs. reverse complement strings
   
   Modifying any step invalidates the approximation guarantee.

5. **Assuming polynomial-time computation is trivial**: Computing a minimum-weight cycle cover is polynomial-time solvable (via minimum-weight perfect matching in auxiliary graphs), but the implementation complexity is non-trivial.

## See Also

- [[Shortest Common Superstring Problem]] – primary application domain
- [[Minimum Weight Perfect Matching]] – algorithmic tool for computing cycle covers
- [[Distance Graph]] – graph construction used in string-based optimization
- [[Approximation Algorithms]] – theoretical framework for analyzing Algorithm 1
- [[Eulerian Paths and Circuits]] – related but distinct graph covering concept

## Sources

- Algorithm 1 and Theorem 11 from a manuscript on 8/3-approximation for SCS-RC (Shortest Common Superstring with Reverse Complements)
- Lemma 9 and Lemma 10 on overlap bounds and cycle breaking
- Section 4.2 discussion of cycle cover computation details