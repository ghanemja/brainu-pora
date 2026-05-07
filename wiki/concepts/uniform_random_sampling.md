# Uniform Random Sampling

## Definition

Uniform random sampling is the process of selecting elements from a finite set such that each element (or configuration) has an **equal probability** of being chosen. In the context of graph/hypergraph analysis, this means drawing a subgraph (or graphlet) from all possible colorful subgraphs such that the probability of selecting any particular valid subgraph is $\frac{1}{N}$, where $N$ is the total number of valid subgraphs.

In the cited work, uniform random sampling is applied to **k-graphlets** (connected subgraphs with $k$ vertices and $k$ distinct color labels), ensuring that each colorful graphlet appears with equal probability in the sample, independent of how many spanning trees it contains.

## Key Equations

The fundamental counting equation for treelets uses dynamic programming recursion:

$$C(T, S, v) = \frac{1}{d} \sum_{\substack{S_1, S_2 \subset S \\ S_1 \cap S_2 = \emptyset}} C(T_1, S_1, v) \sum_{u \sim v} C(T_2, S_2, u)$$

where:
- $C(T, S, v)$ = count of h-treelets isomorphic to tree $T$, colored by set $S$, rooted at vertex $v$
- $T$ is split into subtrees $T_1$ (rooted at $v$) and $T_2$ (rooted at child of $v$)
- $d$ = normalization factor depending only on $T$
- $u \sim v$ denotes adjacency in the graph

**Sampling probability** at stage $i$:

$$P(\text{choose partition } S_1, S_2) \propto C(T_1, S_1, v) \cdot \sum_{u \sim v} C(T_2, S_2, u)$$

**Acceptance probability** for graphlet $G[U]$:

$$P(\text{accept } G[U]) = \frac{1}{\tau(G[U])}$$

where $\tau(G[U])$ is the number of spanning trees in $G[U]$. This inverse-weighting ensures uniform distribution over the final graphlet set.

## Physical Intuition / Derivation

### The Problem

When sampling graphlets from a graph, a naive approach (selecting random vertex subsets) produces a **biased distribution**: subgraphs with more spanning trees become overrepresented. This occurs because they can be "reached" through more different tree-decomposition paths during the sampling process.

### The Solution: Multi-Stage Rejection Sampling

The algorithm works in two phases:

**Phase 1: Build-up (Counting)**
- Use dynamic programming to count colorful k-treelets rooted at each vertex
- Recursively partition the target tree $T$ into smaller subtrees
- Compute counts bottom-up by combining subtree counts weighted by edge multiplicities
- Time complexity: $2^{O(k)} \cdot O(\|G\|)$ (exponential in $k$ but linear in graph size)

**Phase 2: Sampling (Rejection Sampling)**
1. **Stage 1**: Pick tree $T$ and root vertex $v$ with probability $\propto C(T, S, v)$
2. **Stages 2-n**: Recursively decompose $T$ and sample subtrees:
   - Choose color partition $(S_1, S_2)$ with probability proportional to the product of counts from both subtrees
   - Choose specific neighbor $u$ for $T_2$ according to its count
3. **Rejection step**: Accept the sampled graphlet $G[U]$ with probability $\propto 1/\tau(G[U])$ (inverse spanning tree count)

The rejection step **corrects the bias**: since subgraphs with more spanning trees are over-sampled during construction, down-weighting them by $1/\tau$ produces uniform final distribution.

### Why It Works

The probability of sampling a specific colorful graphlet $G[U]$ during construction is proportional to $\tau(G[U])$ (the number of tree decompositions that generate it). After applying the rejection probability $1/\tau(G[U])$:

$$P(\text{final acceptance of } G[U]) \propto \tau(G[U]) \cdot \frac{1}{\tau(G[U])} = \text{constant}$$

Thus all graphlets are equally likely. Expected time per sample: $2^{O(k)} \cdot O(\log n)$.

## Applications in Engineering

### 1. Network Motif Discovery
- **Biological networks**: Identify recurring protein-interaction patterns; distinguish functional modules from random noise
- **Social networks**: Find community structures and influence propagation patterns
- **Application**: Ensures unbiased statistical tests by eliminating over-sampling of highly-connected motifs

### 2. Graph Pattern Mining
- Unbiased sampling of subgraph patterns for frequent pattern mining
- Reduces computational cost by sampling representative graphlets rather than exhaustive enumeration
- Enables hypothesis testing on network structure

### 3. Hypergraph Analysis
- Extended to hypergraphs (e.g., co-authorship networks, chemical reaction systems) via auxiliary graph representation ($G_{\text{aif}}(H)$)
- Preserves connectivity properties: $H[U]$ is connected iff $G_{\text{aif}}[U]$ is connected
- Cost reduction from $\Omega(\|H\|^2)$ naive approaches to $2^{O(k)} \cdot O(\log n)$ per sample

### 4. Machine Learning Feature Extraction
- Generate unbiased graphlet features for graph neural networks
- Sample diverse substructures for training without over-emphasizing highly-connected regions

### 5. Quality Assurance in Large-Scale Networks
- Streaming/online analysis of evolving networks (e.g., streaming social media graphs)
- Limited memory budgets benefit from sampling rather than full enumeration

## Common Mistakes / Pitfalls

### 1. **Ignoring the Spanning Tree Correction**
**Mistake**: Skipping the rejection step (accepting all sampled graphlets).  
**Consequence**: Graphlets with many spanning trees appear orders of magnitude more