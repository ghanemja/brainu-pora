# Correlation Clustering

## Definition

**Correlation clustering** is a graph partitioning problem where the goal is to partition vertices of an undirected, unweighted graph $G = (V, E)$ into clusters to minimize disagreements with pairwise similarity statements encoded in the edge structure.

Formally, given a graph $G = (V, E)$:
- **Vertices** represent objects to be clustered
- **Edges** represent pairwise similarity (objects that *should* be in the same cluster)
- **Clustering** $\mathcal{C}$ is a partition of $V$

The **cost** of a clustering is:
$$\text{Cost}(\mathcal{C}) = \underbrace{\text{# edges cut}}_{\text{similar pairs separated}} + \underbrace{\text{# non-edges within clusters}}_{\text{dissimilar pairs grouped}}$$

This cost function makes the problem fundamentally different from traditional clustering: we don't require input specifying the number of clusters or cluster sizes—the structure emerges from minimizing disagreement.

## Key Equations

**Approximation Ratio:** An algorithm achieves an $\alpha$-approximation if for any instance:
$$\text{Cost}(\text{Algorithm output}) \leq \alpha \cdot \text{Cost}(\text{OPT})$$

**Pivot Algorithm Cost Analysis:** The classic pivot-based approach achieves a **factor-3 approximation**. For a randomly selected pivot vertex $p$:
- Cluster $p$ with all its neighbors: $C_p = \{p\} \cup N(p)$
- Recursive call on remaining vertices $V \setminus C_p$

Recent bounds (as of 2026):
- Improved pivot variant: **2.9991-approximation**
- LP-based rounding: **2.06-approximation** (Chawla et al., 2015)
- Sherali–Adams hierarchy: **(1.994 + ε)-approximation** (Cohen-Addad et al., 2022)
- State-of-the-art: **1.73-approximation** (Cohen-Addad et al., 2023)

## Physical Intuition / Derivation

### Why This Problem Matters

Traditional clustering (e.g., $k$-means) requires specifying $k$ or using heuristics to determine cluster count. Correlation clustering sidesteps this: the "correct" number of clusters is implicitly defined by which partition minimizes disagreement with the similarity graph.

**Example:** Consider similarity judgments from multiple annotators on documents. Some pairs have consensus (similar), others don't. Correlation clustering finds the partition best explaining this noisy data without assuming a fixed cluster count.

### Why Pivot Algorithm Works (and Its Limitation)

The **pivot algorithm** is elegant:

1. Select a random vertex $p$ as pivot
2. Place $p$ and all neighbors in one cluster
3. Remove this cluster, recurse

**Why 3-approximation?** When we form cluster $C_p$:
- **Gains:** We correctly group all edges within $C_p$ (internal edges pay 0 cost)
- **Costs:** 
  - Edges leaving $C_p$ (cut edges) each cost 1
  - Non-edges within $C_p$ (internal non-edges) each cost 1

In the worst case, a vertex $p$ might be in a "bad cluster"—e.g., complete graph minus a matching, where many non-edges exist within the forced cluster. The factor of 3 comes from worst-case analysis of competing decisions.

### The Improvement: Removing Good Clusters First

The key insight of Lolck, Thorup, and Yan:

**Good clusters** have very few internal non-edges and very few edges leaving. These are "easy"—both the pivot algorithm and an oracle would agree.

If we identify and remove good clusters *before* pivot selection, we eliminate adversarial cases. With good clusters removed:
- Remaining graph has fewer "trap" structures
- Pivot choices become less damaging
- **Approximation improves to 2.9991**

This illustrates a general principle: algorithms perform better on well-behaved instances, and preprocessing to remove easy cases can tighten worst-case bounds.

## Applications in Engineering

### 1. **Entity Resolution / Record Linkage**
Database systems must merge duplicate records from multiple sources. Treat records as vertices; edges encode similarity scores (string matching, field agreement). Clustering merges duplicates without requiring manual specification of merge thresholds.

### 2. **Community Detection in Networks**
Social networks, citation networks, protein interaction networks. Edges represent relationships; we seek natural community structure without fixing community count. More flexible than modularity-based methods that require a priori parameters.

### 3. **Collaborative Filtering & Recommendation Systems**
User-item preference graphs with edges for "similar users" or "similar items." Clustering groups users/items for recommendation without fixing cohort sizes. Handles disagreement naturally (not all similar users want the same recommendations).

### 4. **Document Clustering & Information Retrieval**
Cluster documents based on textual similarity without deciding cluster count. Useful for search result organization, duplicate detection, and topic discovery.

### 5. **Machine Learning: Noisy Label Learning**
When training labels are noisy, correlation clustering on a similarity graph of training examples can identify coherent groups despite annotation disagreement. Avoids over-committing to a fixed cluster structure.

### 6. **Biological Data: Gene Clustering**
Gene expression similarity graphs can be clustered without assuming functional pathway count. Discovers natural groupings in omics data.

## Common Mistakes / Pitfalls

### 1. **Confusing with Agglomerative Clustering**
Correlation clustering is not greedy merging. The cost function is global; you can't decompose it into local merge decisions. Hierarchical clustering algorithms don't minimize correlation clustering cost.

### 2. **Expecting Deterministic Pivot Algorithms**
The randomized pivot algorithm has approximation ratio 3 *in expectation*. Single runs may perform worse. Use derandomization or multiple restarts for guarantees.

### 3. **Ignoring the "Complete Graph" Case**
If $G$ is a complete graph (all pairs similar), the optimal clustering is a single cluster with cost 0. But bad pivot choices can fragment this. Algorithms must handle fully-connected instances specially.

###