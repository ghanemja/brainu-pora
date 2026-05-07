# Triangle Counting

## Definition

**Triangle counting** is the problem of determining the number of triangles (3-cycles) in an undirected, unweighted graph $G = (V, E)$ where $|V| = n$ and $|E| = m$. A triangle is a set of three distinct vertices $\{u, v, w\}$ where all three edges $(u,v)$, $(v,w)$, and $(u,w)$ exist in $E$.

In the **detection variant**, the goal is to determine whether triangles exist. In the **counting variant**, the goal is to output an estimate $\hat{T}$ of the true triangle count $T$ with guaranteed accuracy guarantees, typically requiring:

$$|{\hat{T} - T}| \leq \varepsilon T$$

with high probability, where $\varepsilon$ is an error parameter.

### Related Structures

A **wedge** (or "open triangle") is a path of length 2: vertices $(u, v, w)$ connected by edges $(u,v)$ and $(v,w)$. A triangle "closes" a wedge by adding edge $(u,w)$.

A **four-cycle** (or 4-cycle) is a cycle of length 4, denoted $(a, b, c, d)$ with edges $(a,b), (b,c), (c,d), (d,a)$. Four-cycles are useful as auxiliary structures in sampling-based triangle counting algorithms because they provide a mechanism to control variance through careful probabilistic analysis.

## Key Equations

### Basic Counting Formula

The naive triangle count sums over all possible triples:

$$T = \frac{1}{6} \sum_{u \in V} \sum_{v \in V} \sum_{w \in V} \mathbb{1}[(u,v), (v,w), (u,w) \in E]$$

The factor $1/6$ accounts for ordering symmetry (each triangle counted 6 times via different orderings).

### Sampling Estimator

In sampling-based approaches, let $S_v$ denote the indicator that vertex $v$ is sampled with probability $p_v$. The unbiased estimator using importance sampling becomes:

$$\hat{T} = \sum_{\text{triangles } (u,v,w)} \frac{\mathbb{1}[u,v,w \text{ sampled}]}{p_u \cdot p_v \cdot p_w}$$

For variance control, the sampling probabilities are typically set as a function of **heaviness** $t(z)$—the number of triangles containing substructure $z$—so that:

$$p_z \propto \sqrt{t(z)}$$

### Variance Bound

The variance of the estimator relates to the second moment of the sampling weights:

$$\text{Var}(\hat{T}) \propto \sum_{\text{triangles}} \frac{1}{p_u \cdot p_v \cdot p_w}$$

Optimal variance is achieved when sampling probabilities are proportional to the "heaviness" of substructures, yielding:

$$\text{Var}(\hat{T}) = O(T^{3/2})$$

under appropriate heaviness-based sampling schemes.

## Physical Intuition / Derivation

### Why Triangles Matter

Triangles are fundamental structures in networks:
- **Local clustering**: High triangle density indicates tightly-knit groups
- **Transitivity**: If A trusts B and B trusts C, does A trust C? (Triangle closure)
- **Anomaly detection**: Unusual triangle patterns signal fraud or bot behavior

### The Sampling Problem

Naive enumeration requires checking all $O(n^3)$ or $O(m \cdot n)$ potential triangles, infeasible for billion-node graphs. Sampling provides a path forward, but introduces a **variance-bias tradeoff**:

1. **Uniform sampling**: Sample each node with equal probability. Problem: rare triangles (with low-degree nodes) are severely underweighted, causing huge variance.

2. **Heaviness-aware sampling**: Nodes involved in many triangles are "heavy." By sampling heavy nodes with higher probability and reweighting by $1/p_v$, we concentrate samples on high-contribution triangles, reducing variance dramatically.

### Four-Cycles as Auxiliary Structure

The source material mentions using four-cycles for **multi-pass algorithms**:
- A wedge $(u, v, w)$ becomes a triangle if edge $(u,w)$ exists
- A four-cycle $(a, b, c, d)$ can be viewed as two overlapping wedges
- By sampling nodes, edges, *and* wedges jointly and analyzing four-cycles, the algorithm can decompose and control variance across multiple passes, achieving sublinear space

## Applications in Engineering

### 1. Social Network Analysis
- **Community detection**: Dense triangle regions indicate communities
- **Influence propagation**: Triangle-rich neighborhoods amplify information spread
- Example: LinkedIn/Facebook use triangle metrics to recommend mutual connections

### 2. Anomaly Detection
- **Fraud networks**: Money laundering rings form tight triangle clusters
- **Bot detection**: Coordinated bots create artificial triangle patterns
- Application: PayPal, Stripe detect fraudulent merchant rings

### 3. Database & Knowledge Graph Querying
- **Pattern matching**: Count labeled triangles (e.g., "knows-collaborates-manages")
- **Data integration**: Detect redundancy/conflicts via triangular relationships
- Example: DBpedia, Wikidata query engines

### 4. Recommender Systems
- **Collaborative filtering**: User-item-item triangles indicate co-preference
- **Cold-start mitigation**: Triangle metrics improve recommendations for new users

### 5. Internet Topology & Routing
- **AS-path analysis**: Triangles in autonomous system graphs indicate routing inefficiency
- **Resilience**: High triangle density = redundant paths

### 6. Biological Networks
- **Protein-protein interactions**: Triangles indicate functional modules
- **Gene regulatory networks**: Feedback loops (triangles) are common motifs

## Common Mistakes / Pitfalls

### 1. Confusing "Triangle" with "3-Clique"
A triangle is a simple cycle of length 3. A 3-clique (complete graph $K_3$) is the same structure. **