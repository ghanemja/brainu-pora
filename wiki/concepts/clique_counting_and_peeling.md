# Clique Counting and Peeling

## Definition

**Clique counting** is the computational problem of determining the number of cliques of a given size $k$ in an undirected graph $G = (V, E)$. A clique is a complete subgraph where every pair of vertices is connected by an edge.

**Clique peeling** (also called $k$-clique peeling) is an iterative graph decomposition technique that repeatedly identifies and removes cliques from a graph. More formally, it operates by progressively identifying structures satisfying clique properties and extracting them, often as a preprocessing or analysis step in larger graph algorithms.

These concepts are closely related to **$k$-core decomposition**, where instead of cliques, we iteratively remove vertices of degree less than $k$. The peeling framework generalizes across both clique and core-based decompositions.

## Key Equations

For a graph $G = (V, E)$ with $n = |V|$ vertices and $m = |E|$ edges:

**Number of maximal cliques:**
$$C_{\max}(G) = \text{count of all maximal cliques in } G$$

**Clique size distribution:**
The number of cliques of size exactly $k$ is denoted $\omega_k(G)$, where:
$$\sum_{k=1}^{|V|} \omega_k(G) = \text{total clique count}$$

**Degeneracy-based upper bound:**
For a graph with degeneracy $d$, the maximum clique size is bounded by $|V|$ and the peeling iterations required scales with $d$:
$$\text{Peeling iterations} \leq d + 1$$

## Physical Intuition / Derivation

### Why Clique Counting Matters

Cliques represent tightly-knit groups or cohesive structures:
- In social networks: friend groups where everyone knows everyone
- In biological networks: highly interactive protein complexes
- In collaboration graphs: research communities with dense internal collaboration

The problem is fundamentally hard (NP-complete for determining if a clique of size $k$ exists), but practical algorithms exploit graph structure.

### The Peeling Paradigm

Peeling works by **iterative removal**:

1. **Initialization:** Start with graph $G_0 = G$
2. **Iteration $i$:** 
   - Identify cliques (or in $k$-core: vertices with degree $< k$)
   - Mark them for removal
   - Compute $G_{i+1} = G_i \setminus \{\text{identified structures}\}$
3. **Termination:** When no more cliques/cores exist

**Key insight:** Parallel peeling is efficient because:
- Removal operations in iteration $i$ are independent (no dependencies between removed items)
- Remaining graph for iteration $i+1$ is smaller
- Multiple processors can identify different cliques simultaneously without conflicts

### Degeneracy Connection

A graph with degeneracy $d$ admits an **elimination ordering** where each vertex has at most $d$ neighbors appearing later in the ordering. This enables:
- Bounded clique sizes (maximum clique has size $\leq d+1$)
- Efficient sequential peeling in $O(d \cdot m)$ time
- Natural parallelization through level synchronization

## Applications in Engineering

### 1. **Social Network Analysis**
- Identifying cohesive communities via clique enumeration
- Friend group detection and recommendation systems
- Influence propagation modeling through dense subgraphs

### 2. **Biological Networks**
- Protein-protein interaction networks: finding multi-protein complexes (cliques = all-against-all interactions)
- Gene expression clustering
- Drug discovery (cliques represent synergistic compound targets)

### 3. **Database Systems & Knowledge Graphs**
- Finding densely connected entities in knowledge bases
- Triangle/clique counting for relationship strength inference
- Data deduplication via clique detection

### 4. **Distributed Systems & Parallel Computing**
- Batch-dynamic $k$-core decomposition for streaming graph updates
- Load balancing: clique peeling stages define synchronization barriers
- Graph partitioning based on core structure

### 5. **Computer Vision**
- Clique-based feature matching in image registration
- Scene understanding via object-object relationship cliques

## Common Mistakes / Pitfalls

### 1. **Confusing Cliques with Cores**
- **Error:** Treating $k$-clique and $k$-core as equivalent
- **Correction:** A $k$-core requires degree $\geq k$ (degree-based); a $k$-clique requires all-pairs connectivity (density-based). $k$-cliques are much more restrictive.

### 2. **Underestimating Computational Cost**
- **Error:** Assuming clique counting is "just like core decomposition"
- **Reality:** Clique enumeration is exponential in worst case (#P-hard); must use heuristics or exploit degeneracy bounds
- **Correction:** Use degeneracy-based algorithms; these give polynomial complexity when degeneracy is small

### 3. **Ignoring Parallel Dependencies**
- **Error:** Attempting to parallelize peeling without proper synchronization
- **Pitfall:** Removing a vertex while another thread is still examining its neighborhood
- **Correction:** Use explicit barrier synchronization at each peeling level; mark-and-sweep pattern ensures consistency

### 4. **Memory Inefficiency in Parallel Settings**
- **Error:** Each thread maintains independent copies of the full graph
- **Reality:** Leads to $O(p \cdot n)$ memory for $p$ processors
- **Correction:** Use shared adjacency structures with atomic operations or level-synchronous updates

### 5. **Not Exploiting Sparse Structure**
- **Error:** Treating all graphs as dense
- **Impact:** Dense algorithms degrade when graphs are sparse
- **Correction:** Use edge-centric representations; algorithms should scale with $m$, not $n^2$

## See Also

- [[k-core decomposition]] — degree-based graph peeling closely related to clique peeling
- [[Degeneracy and graph degeneracy ordering]] — fundamental structural property enabling efficient peeling
- [[Parallel graph algorithms]] — synchronization techniques and load balancing for distributed peeling
- [[Triangle counting]] — simpler case ($