# Node Sampling

## Definition

**Node sampling** is a probabilistic technique for estimating graph properties (particularly subgraph counts) by sampling a subset of vertices according to specified probability distributions, then analyzing the induced subgraph structure formed by these sampled nodes across multiple stream passes.

In the context of streaming algorithms, node sampling involves:
1. Selecting multiple independent sets of nodes, each according to a different sampling probability $p_i$
2. Making multiple passes over the edge stream to collect edges within the induced subgraphs of sampled nodes
3. Using structural patterns (e.g., four-cycle counts) in the resulting subgraph to estimate global graph properties

Unlike uniform sampling strategies, node sampling can employ **non-uniform probability distributions** tailored to the estimation task at hand.

## Key Equations

For a node $v$ sampled with probability $p$, the expected number of edges retained in the induced subgraph is:

$$\mathbb{E}[\text{edges}] = p^2 \cdot m$$

where $m$ is the total number of edges in the original graph.

The space complexity achieved through multi-pass node sampling for four-cycle counting is:

$$\text{Space} = \tilde{O}\left(\frac{m}{\sqrt{T}}\right)$$

where $T$ is the number of passes allowed, and $\tilde{O}(\cdot)$ notation hides poly($\log n, 1/\epsilon$) factors.

For variance control in estimators, the **heaviness** of a structural element (node, edge, or wedge) is defined relative to a sampling-dependent threshold:

$$\text{Heaviness}(u) = |\{C_4 : u \in C_4\}|$$

where $C_4$ denotes a four-cycle. A structural element is considered **heavy** if its heaviness exceeds a threshold $\tau(p)$ that depends on its sampling probability $p$.

## Physical Intuition / Derivation

### Why Node Sampling?

Traditional dense subgraph sampling (edge sampling) requires space proportional to $O(m)$ to maintain reasonable fidelity. Node sampling achieves better space efficiency because:

- **Quadratic reduction**: Sampling $pn$ nodes yields $\approx p^2 m$ edges in the induced subgraph
- **Variance-space tradeoff**: Multiple passes compensate for information loss in any single pass
- **Structured patterns**: Four-cycles and other subgraphs provide sufficient statistical power to estimate global properties despite sparsification

### Multi-Pass Collection Strategy

The algorithm operates as follows:

1. **Initialization**: Fix sampling probabilities $p_1, p_2, \ldots, p_k$ 
2. **Pass $i$**: Sample nodes according to $p_i$; traverse the edge stream once, collecting all edges $(\{u,v\} : \text{both } u,v \text{ sampled in pass } i\})$
3. **Estimation**: Count four-cycles in each induced subgraph; use these counts to form an unbiased estimator of the global count

### Heaviness and Variance Control

The critical technical challenge is **variance amplification** due to dependencies:

- In the full graph, a four-cycle is a deterministic structure
- Under node sampling, whether a given four-cycle appears depends on sampling outcomes, creating complex dependencies
- Nodes (or edges/wedges) participating in many four-cycles contribute disproportionately to estimator variance

**Sampling-dependent heaviness thresholds** address this:

$$\tau(p) = \tau(p_i) \text{ for each node/edge/wedge and each sampling probability } p_i$$

A structural element is excluded from variance reduction only if its heaviness $\gg \tau(p_i)$. Crucially, $\tau(p)$ depends on the **particular sampling probability** of that element, not just the graph structure alone.

### Why Refined Heaviness?

Computing exact heaviness requires $\Omega(m)$ space—exceeding the algorithm's space budget. The refined heaviness definition:
- Can be computed during stream processing within $\tilde{O}(m/\sqrt{T})$ space
- Introduces minor overcounting of four-cycles (bounded by $\epsilon$-fraction of total)
- Maintains sufficient accuracy for variance concentration

## Applications in Engineering

### 1. **Graph Analytics at Scale**
- **Social network analysis**: Estimating clustering coefficients and motif distributions in graphs with billions of edges
- **Network anomaly detection**: Identifying suspicious subgraph patterns (e.g., coordinated account clusters) using four-cycle prevalence
- **Recommendation systems**: Inferring community structure without storing the full graph

### 2. **Database Systems & Data Warehousing**
- **Graph databases**: Approximate subgraph pattern matching in streaming property graphs
- **Data quality assessment**: Detecting cycles and dependencies in massive ETL/data lineage graphs

### 3. **Network Monitoring & Cybersecurity**
- **DDoS detection**: Identifying highly-connected attack patterns using motif analysis
- **Network topology summarization**: Maintaining compressed representations of evolving network graphs
- **Traffic engineering**: Counting flow-level structures (via node sampling) without packet-level storage

### 4. **Bioinformatics & Systems Biology**
- **Protein interaction networks**: Estimating functional motif frequencies in PPI networks
- **Metabolic pathway analysis**: Counting important cyclic feedback structures in biochemical networks

### 5. **Machine Learning Infrastructure**
- **Graph neural network training**: Efficient mini-batch subgraph sampling for GNN convergence
- **Knowledge graph completion**: Estimating missing relations by analyzing four-cycle patterns

## Common Mistakes / Pitfalls

### 1. **Confusing with Uniform Sampling**
**Mistake**: Assuming node sampling uses uniform probability $p = c/n$.  
**Reality**: The algorithm uses *multiple sampling rounds* with potentially *different, carefully chosen probabilities* to optimize the variance-space tradeoff.

### 2. **Ignoring Sampling-Dependent Thresholds**
**Mistake**: Using a single heaviness threshold $\tau$ across all samples.  
**Reality**: Heavy-hitter exclusion must be threshold $\tau(p_i)$, which varies per sampling probability. A node heavy at $p_1$ may not be heavy at $p_2$.

### 3. **