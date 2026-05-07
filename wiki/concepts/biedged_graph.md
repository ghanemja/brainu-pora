# biedged graph

## Definition

A **biedged graph** is a directed graph in which each edge is colored either **black** or **grey**, used primarily in computational biology and graph theory for representing genomic sequences and their variations.

Formally, a biedged graph $G = (V, E_B \cup E_G)$ consists of:
- A vertex set $V$
- A set of **black edges** $E_B$ (representing reference/canonical paths)
- A set of **grey edges** $E_G$ (representing alternative/variant paths)

**Key structural property**: Each black edge $(u, v) \in E_B$ is inherently directed and partitions its endpoints into:
- A **left node** (source of the black edge)
- A **right node** (sink of the black edge)

Left nodes of black edges cannot have outgoing grey edges; right nodes cannot have incoming grey edges (by definition).

---

## Key Equations

### Snarl Characterization

A **snarl** is a minimal subgraph pair defined by frontier nodes $s_{n1}$ and $s_{n2}$ such that:
- All paths from $s_{n1}$ to $s_{n2}$ within the snarl are disjoint at internal vertices
- The pair cannot be decomposed into smaller snarls

An **ultrabubble** is a snarl satisfying:

$$\text{Ultrabubble} = \text{Snarl} \cap \text{(acyclic)} \cap \text{(tip-free)}$$

where a snarl is an ultrabubble if and only if its induced subgraph contains:
- No cycles
- No tips (vertices with in-degree = 0 or out-degree = 0, except frontier nodes)

### Complexity Bound

For naive detection of ultrabubbles among $K$ snarls:

$$\text{Complexity} = O(K(n + m))$$

where $n = |V|$ and $m = |E_B \cup E_G|$, requiring DFS/BFS per snarl.

---

## Physical Intuition / Derivation

### Motivation from Genomic Graphs

Biedged graphs model **genome assembly and haplotyping**:

- **Black edges** represent high-confidence or reference genome sequences (the "backbone")
- **Grey edges** represent alternative sequences arising from:
  - Genetic variants (SNPs, indels)
  - Sequencing polymorphisms
  - Structural alternatives

### Why Two Colors?

The bipartite coloring elegantly captures biological reality:

1. **Reference path** (black edges): follows a canonical sequence
2. **Variant paths** (grey edges): capture deviations without breaking the topology

This structure allows efficient algorithms for detecting **ultrabubbles**—the locally resolvable variation regions where alternative paths reconverge.

### Snarl vs. Ultrabubble

- A **snarl** is any topologically minimal region between two frontier nodes
- An **ultrabubble** adds the constraint that the region is acyclic and contains no dead-ends (tips)

**Theorem 1** elegantly shows a fundamental constraint: A snarl defined by two left nodes of black edges can **never** form an ultrabubble because:

1. Left nodes of black edges have no outgoing grey edges (by definition)
2. If they define a snarl, their outgoing black edges are removed
3. Thus both become **sinks** in the extracted subgraph
4. An acyclic graph requires at least one source, but any source formed would violate the snarl's structure
5. This creates a topological impossibility

---

## Applications in Engineering

### 1. **Computational Biology & Genome Assembly**
- Detecting variation bubbles in de Bruijn graphs representing short-read sequences
- Identifying and resolving haplotypes from mixed genomic samples
- Filtering true variants from sequencing artifacts

### 2. **Pangenome Graph Construction**
- Building compact representations of multiple genome sequences
- Efficient storage of genomic variation across populations
- Query algorithms for sequence alignment to population graphs

### 3. **Graph Compression & Indexing**
- Identifying structural redundancy in large directed acyclic graphs
- Constructing minimal feedback-arc representations
- Index construction for substring/pattern queries on graph-encoded sequences

### 4. **Variant Calling Pipeline**
- Distinguishing genuine genetic variants (ultrabubbles) from artifacts
- Filtering low-complexity regions and repetitive sequences
- Characterizing confidence in variant boundaries

---

## Common Mistakes / Pitfalls

### 1. **Confusing Snarls with Ultrabubbles**
**Mistake**: Treating all snarls as ultrabubbles or vice versa.

**Reality**: A snarl is a *topological* structure; an ultrabubble additionally requires acyclicity and absence of tips. Many snarls are not ultrabubbles.

### 2. **Misapplying the Black/Grey Edge Semantics**
**Mistake**: Assuming grey edges are optional or "less important" edges.

**Reality**: In genomic contexts, grey edges carry *equal* information about true biological variation. The coloring reflects *certainty* in the reference assembly, not biological importance.

### 3. **Ignoring Theorem 1 Constraints**
**Mistake**: Attempting to find ultrabubbles defined by two left (or two right) nodes of black edges.

**Reality**: Such configurations are **topologically impossible**. Snarls with this frontier structure automatically fail the ultrabubble test.

### 4. **Naive Algorithm Complexity**
**Mistake**: Running independent DFS/BFS for each snarl detection without considering the $O(K(n+m))$ cost.

**Reality**: For large graphs with many snarls, this naive approach becomes prohibitive. Use lowest-common-ancestor (LCA) preprocessing for better amortized performance.

### 5. **Trivial Snarls as Degenerate Cases**
**Mistake**: Dismissing trivial (minimal) snarls as meaningless.

**Reality**: Trivial snarls are valid structures and valid minimal ultrabubbles; they represent single edges or minimal paths without variation and must be handled in any complete algorithm.

---

## See Also

- [[Directed Acyclic Graph (DAG)]] —