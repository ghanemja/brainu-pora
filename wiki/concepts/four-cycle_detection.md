# four-cycle detection

## Definition

**Four-cycle detection** is the computational problem of identifying and counting all four-cycles (4-cycles or $C_4$) in an undirected, unweighted graph $G = (V, E)$ with $n$ vertices and $m$ edges.

A **four-cycle** is a closed walk of length 4: a sequence of four distinct vertices $(a, b, c, d)$ connected by edges $(a,b), (b,c), (c,d), (d,a)$ that form a cycle. The vertices $a$ and $c$ are called **opposite nodes**, as are $b$ and $d$.

### Related Structures

Within a four-cycle $A \in \mathcal{T}$ (where $\mathcal{T}$ denotes the set of all four-cycles):
- $V(A)$ = set of 4 vertices in the cycle
- $E(A)$ = set of 4 edges in the cycle  
- $W(A)$ = set of 6 wedges (2-edge paths) in the cycle

The **heaviness** $t(z)$ of a substructure $z$ (node, edge, or wedge) is defined as the number of four-cycles containing that substructure.

---

## Key Equations

### Four-Cycle Count Estimation

For an undirected graph, the total number of four-cycles can be expressed via the trace formula:

$$T = \frac{1}{8} \text{tr}(A^4) - \text{(adjustments for lower-order structures)}$$

where $A$ is the adjacency matrix. The factor $1/8$ accounts for the 8 equivalent representations of each cycle (4 rotations × 2 directions).

### Sampling Probability Framework

For a substructure $z$ with heaviness $t(z)$, the sampling probability is determined by:

$$p(z) \propto t(z)^{\beta}$$

where the exponent $\beta$ and normalization constants are carefully chosen to control **variance** in the estimator while using sublinear space.

### Unbiased Estimator Construction

If a substructure $z$ is sampled with probability $p(z)$, the contribution to the count estimator is:

$$\hat{T} = \sum_{\text{sampled } z} \frac{\mathbb{1}[z \text{ in four-cycle}]}{p(z)}$$

ensuring $\mathbb{E}[\hat{T}] = T$.

---

## Physical Intuition / Derivation

### Why Four-Cycle Detection Matters

Four-cycles represent the simplest non-trivial **dense subgraphs** or **clustering patterns** in networks. They are fundamental to:
- Understanding **local graph structure** (related to but distinct from triangles)
- Detecting **communities** and **bipartite-like structures**
- Analyzing **feedback loops** in directed/undirected systems

### The Core Challenge

Naive enumeration requires checking all $O(n^4)$ or $O(m^2)$ candidate structures, which is prohibitively expensive for large graphs. The key insight is **adaptive sampling**:

1. **Heavy structures contribute disproportionately** to the cycle count (a wedge in many four-cycles contributes more to variance if sampled uniformly)

2. **Multi-level sampling** extends single-pass triangle-counting techniques:
   - Triangle counting samples **nodes** proportionally to degree (or a function thereof)
   - Four-cycle detection must coherently sample **nodes**, **edges**, and **wedges** with carefully balanced probabilities
   - Multiple passes allow the algorithm to collect and verify relevant structures

3. **Variance control** is achieved by sampling more frequently from "heavy" substructures (those appearing in many four-cycles), reducing estimator variance without increasing bias.

### Algorithmic Structure

The detection algorithm proceeds in phases:
1. **Detection Phase** (Section 5 of source): Identify existence of four-cycles
2. **Counting Phase** (Section 6): Enumerate and count all cycles using detection oracles
3. **Oracle Subroutines** (Section 7): Handle edge/wedge sampling and heaviness computations

---

## Applications in Engineering

### 1. **Network Analysis & Social Networks**
- Identify **clique-like communities** (four-cycles indicate dense local structure)
- Detect **reciprocal relationships** and **mutual followers** in social media
- Analyze **information flow patterns** with bidirectional reinforcement

### 2. **Bioinformatics & Protein Networks**
- Identify **feedback motifs** in gene regulatory networks
- Detect **protein complex candidates** via four-cycle patterns in protein-protein interaction networks

### 3. **Recommendation Systems**
- Find **user-item-user-item cycles** indicating correlated preferences
- Detect **collaborative filtering patterns** at the local level

### 4. **Communication Networks**
- Identify **routing loops** and **redundant paths** in network topology
- Analyze **mesh network robustness** via cycle prevalence

### 5. **Knowledge Graphs & Databases**
- Detect **inconsistencies** and **circular dependencies** in knowledge bases
- Find **transitive relationship violations** in knowledge graph completion

### 6. **Circuit & Hardware Design**
- Identify **feedback paths** and **cycles** in asynchronous circuit analysis
- Detect **timing closure** issues via cyclic path enumeration

---

## Common Mistakes / Pitfalls

### 1. **Confusing Four-Cycle with Triangle Counting**
- **Mistake**: Assuming single-pass node-sampling alone suffices
- **Reality**: Four-cycles require joint **edge and wedge sampling** to control variance. Triangle counting only needs node-level probabilistic assignment.

### 2. **Uniform Sampling Inefficiency**
- **Mistake**: Sampling all nodes, edges, or wedges with equal probability
- **Reality**: Heaviness-weighted sampling (probability $\propto t(z)$) dramatically reduces variance for sublinear-space algorithms

### 3. **Ignoring the Ordering in Tuple Notation**
- **Mistake**: Treating $(a, b, c, d)$ and $(a, c, b, d)$ as the same cycle
- **Reality**: These represent **different** cycles with different edge sets. Careful