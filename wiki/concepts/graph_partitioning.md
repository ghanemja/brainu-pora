# Graph Partitioning

## Definition

**Graph partitioning** is the problem of dividing the vertices of a graph $G = (V, E)$ into disjoint subsets (clusters or partitions) according to some optimization criterion. The quality of a partition is typically measured by minimizing the number of edges crossing between partitions (cut edges) while respecting size or balance constraints.

In the context of **correlation clustering**—a variant relevant to the source material—the problem is formulated on an unweighted, undirected graph where edges represent *similarity* relationships. A clustering (partitioning) is evaluated by:

$$\text{Cost} = \underbrace{\text{(edges between different clusters)}}_{\text{disagreements}} + \underbrace{\text{(non-edges within same cluster)}}_{\text{disagreements}}$$

The goal is to find a partition minimizing the total disagreement cost—i.e., maximizing agreement between the graph structure and the clustering assignment.

## Key Equations

### Correlation Clustering Cost Function

For a partition $\mathcal{C} = \{C_1, C_2, \ldots, C_k\}$ of vertex set $V$:

$$\text{CC}(\mathcal{C}) = \left|\{(u,v) \in E : u \in C_i, v \in C_j, i \neq j\}\right| + \left|\{(u,v) \notin E : u, v \in C_i \text{ for some } i\}\right|$$

### Pivot Algorithm Approximation Ratio

The classic pivot-based algorithm (Ailon, Charikar, Newman [ACN08]) achieves an approximation ratio of **3**, meaning:

$$\text{Cost}_{\text{algorithm}} \leq 3 \cdot \text{Cost}_{\text{optimal}}$$

The improved variant presented in the source material reduces this to **2.9991** by preprocessing to remove good clusters before each pivot step.

### Approximation Hierarchy

Recent advances in correlation clustering approximation ratios:
- Pivot algorithm: **3-approximation**
- LP-based rounding: **2.5-approximation** (ACN08)
- Sherali–Adams LP hierarchy: **1.994 + ε-approximation** (CLN22)
- Preclustering + correlated rounding: **1.73-approximation** (CLLN23)

## Physical Intuition / Derivation

### Why Graph Partitioning Matters

Imagine clustering objects where we have pairwise similarity information (edges represent "similar pairs"). The problem is inherently combinatorial: we want clusters that are internally cohesive (dense) and mutually separated (sparse between clusters). However, the graph may contain conflicting signals—two similar objects might belong in different clusters when considering global structure.

### The Pivot Algorithm Intuition

The pivot-based approach works iteratively:

1. **Select a random pivot vertex** $v$ from the remaining unprocessed vertices
2. **Form a cluster** containing $v$ and *all its neighbors*—this is greedy cohesion
3. **Remove this cluster** from the graph
4. **Repeat** on the remaining graph until all vertices are clustered

**Why this achieves 3-approximation (roughly):** 
- When a pivot $v$ is chosen, edges within its neighborhood are "internal" (good). 
- However, edges from $v$'s neighbors to outside the cluster may be counted as disagreements.
- In the worst case (e.g., complete graph minus a matching), the algorithm can incur cost up to 3× optimal because it must break some edges in the optimal solution.

### Improving Beyond 3: The "Good Clusters" Insight

The source material observes that the worst-case examples (achieving ratio 3) all rely on **highly structured good clusters** (e.g., complete subgraphs minus a matching). The key improvement:

**Preprocess before each pivot step:** 
- Identify and remove "obviously good" clusters (dense subgraphs with clear boundaries)
- Apply the pivot algorithm to the remaining, harder graph
- This prevents the algorithm from making poor pivot choices on instances where optimal structure is already visible

This reduces the approximation ratio from 3 to **2.9991**, a small but meaningful improvement that shows the worst-case bound is not tight for real/realistic instances.

## Applications in Engineering

### 1. **VLSI Circuit Design & Layout**
Graph partitioning partitions circuits into logical blocks to minimize interconnect (wirelength) between blocks, reducing power consumption and improving timing closure.

### 2. **Parallel & Distributed Computing**
Partitioning computational graphs (task dependency graphs, data provenance) across processors minimizes inter-node communication. Critical for:
- Load balancing in distributed systems
- Parallel sparse matrix computations
- Map-Reduce job assignment

### 3. **Social Network Analysis**
Detecting communities (clusters of densely connected users) from friendship graphs; finding influential node groups or spam detection.

### 4. **Machine Learning & Data Clustering**
Graph-based semi-supervised learning, spectral clustering, and unsupervised community detection—converting similarity matrices into partitioned clusters.

### 5. **Mesh Partitioning in FEA/CFD**
Partitioning finite element or finite difference meshes across compute nodes; minimizing edge cuts reduces halo communication in PDE solvers.

### 6. **Network Routing & Telecommunications**
Partitioning IP networks into OSPF areas or clusters to reduce routing overhead and improve network resilience.

## Common Mistakes / Pitfalls

1. **Confusing edge cuts with optimal clustering:**
   - Minimizing cut size alone (e.g., using spectral partitioning) does not guarantee good correlation clustering.
   - Correlation clustering *also* penalizes non-edges within clusters, not just cut edges.

2. **Assuming approximation ratios scale with graph size:**
   - A 3-approximation is a multiplicative bound, independent of $|V|$ and $|E|$.
   - It does not improve with problem size; it's a worst-case guarantee.

3. **Overlooking instance structure:**
   - The pivot algorithm's 3-approximation is tight for *adversarial* graphs (complete graph minus matching).
   - On real-world instances with visible good clusters, performance is often much better—the source material exploits this with preprocessing.