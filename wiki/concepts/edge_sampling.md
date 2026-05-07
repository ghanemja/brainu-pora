# Edge Sampling

## Definition

**Edge sampling** is a randomized algorithmic technique for analyzing large graphs and networks by selecting a random subset of edges and performing computations on this induced subgraph. In edge sampling, each edge $e \in E$ is included in the sample with independent probability $p \in (0,1]$, resulting in an expected sample size of $p|E|$.

More formally, given a graph $G = (V, E)$, edge sampling produces a subgraph $G' = (V, E')$ where:
$$E' = \{e \in E : e \text{ is sampled with probability } p\}$$

The sampled edges are used to estimate or compute graph properties while using sublinear space or time.

## Key Equations

**Expected sample size:**
$$\mathbb{E}[|E'|] = p \cdot |E|$$

**Variance scaling (for estimator unbiasedness):**
When estimating a count $X$ via sampling, the estimator $\hat{X} = \frac{Y}{p}$ (where $Y$ is the observed count in the sample) satisfies:
$$\text{Var}(\hat{X}) = \frac{\text{Var}(Y)}{p^2} \sim \frac{X}{p}$$

This illustrates the fundamental trade-off: lower sampling probability $p$ reduces space but increases variance.

**Space complexity for subgraph properties:**
For algorithms using edge sampling with probability $p$ to detect structures in a graph with $m$ edges:
$$\text{Space} = O(pm)$$

## Physical Intuition / Derivation

Edge sampling embodies a fundamental compression principle: *sacrifice precision (increase variance) to gain space efficiency*. 

**Why edge sampling alone is insufficient:** Consider the source material's "onion" example—a complete bipartite graph $K_{2,\kappa}$ with $\kappa = O(\sqrt{T})$ containing $T$ four-cycles but only $O(\kappa)$ edges. If we sample edges with probability $p$, a four-cycle $C_4$ survives in the sample only if all four of its edges are sampled, which happens with probability $p^4$. To detect even one four-cycle with reasonable probability requires $p = \Omega(1)$, negating any space savings.

**The variance problem:** Edge sampling's variance can explode for subgraph counting problems. Suppose we count a subgraph property $S$ (e.g., triangles) in the sample and scale by $1/p$ to estimate the true count. The variance scales as $1/p^2$ relative to the true count, potentially becoming unacceptably large for small $p$.

This limitation motivates **node sampling** as an alternative: sampling nodes with probability $p$ keeps all edges between sampled nodes, changing the failure mode to graphs with dense low-degree structures rather than sparse high-degree structures.

## Applications in Engineering

### 1. **Streaming Graph Analysis**
In single-pass streaming algorithms (e.g., for social network analysis), edge sampling maintains a random reservoir of edges when full storage is infeasible. Space-variance trade-offs guide the sampling rate based on accuracy requirements.

### 2. **Subgraph Counting & Motif Detection**
Bioinformatics and network science use edge sampling to estimate counts of graph motifs (triangles, cliques, cycles) in biological networks. Unbiased estimation requires post-scaling but suffers from variance growth.

### 3. **Network Monitoring & Anomaly Detection**
In cyber-physical systems and network security, sampling edges for real-time intrusion detection or congestion identification balances detection sensitivity against computational/storage overhead.

### 4. **Distributed Graph Processing**
Systems like GraphLab and PowerGraph use edge sampling for load balancing: randomly partition edges across machines to reduce communication while controlling variance in distributed computations.

### 5. **Matrix Sketching**
In machine learning, sampling entries of sparse matrices (represented as edge lists) enables approximate matrix operations (multiplication, spectral analysis) in sublinear space.

## Common Mistakes / Pitfalls

1. **Assuming edge sampling is uniformly effective:** Edge sampling fails dramatically on sparse graphs or graphs with structural heterogeneity (e.g., power-law degree distributions). The hardness instances in the source material (onions, bipartite graphs) show graphs where edge sampling requires $p = \Omega(1)$, destroying space efficiency.

2. **Forgetting to account for variance in estimators:** When estimating a count $Y$ from a sample, students often report $\hat{Y} = Y/p$ without acknowledging that $\text{Var}(\hat{Y}) = O(Y/p^2)$. Small $p$ yields wildly unstable estimates.

3. **Conflating edge vs. node sampling:** These are fundamentally different. Node sampling preserves structural properties within sampled nodes but struggles with rare motifs. Edge sampling directly decimates connectivity but can over-sample noise.

4. **Ignoring dependence between edges:** In subgraph counting, whether multiple edges co-occur is critical. Sampling edges independently destroys these correlations, requiring careful reweighting in estimators.

5. **Neglecting to validate on hard instances:** Always test algorithms on adversarial graphs (complete bipartite graphs, regular graphs, cliques) to identify failure modes before deployment.

## See Also

- [[Node Sampling]] — complementary technique addressing edge sampling's limitations by sampling vertices instead
- [[Streaming Algorithms]] — broader framework encompassing single-pass graph algorithms with memory constraints
- [[Subgraph Counting]] — core application domain; edge sampling used to estimate motif frequencies
- [[Variance Reduction Techniques]] — methods to control estimator variance in randomized algorithms
- [[Graph Sketching]] — compress graphs via random linear projections; related space-accuracy trade-offs

## Sources

- Vorotnikova, S. and McGregor, A. (2016). Counting cycles in streaming graphs. *Proceedings of MFCS* — discusses hard instances and edge vs. node sampling trade-offs in cycle counting
- Vorotnikova, S. (2015). *Tight space bounds for counting triangles and other substructures in streaming graphs* — establishes $\Omega(m/T^{1/3})$ lower bounds and motivates sampling strategy design