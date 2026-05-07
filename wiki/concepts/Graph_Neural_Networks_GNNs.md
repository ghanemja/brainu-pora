# Graph Neural Networks (GNNs)

## Definition

A **Graph Neural Network (GNN)** is a class of neural network architectures designed to learn representations and make predictions on graph-structured data. GNNs operate through a **message-passing** paradigm where node representations are iteratively updated by aggregating information from neighboring nodes.

Formally, a GNN comprises:
- **Node types** $\sigma \in T_E$ (entity types)
- **Attribute types** $\alpha_j \in T_A$ 
- **Edge types** $\tau_j \in T_E$
- **Type maps** $\tau_V$ (node types) and $\tau_E$ (edge types)
- **Readout function** producing output $\hat{y}(v)$ at node $v$

A GNN is *correct* for a target predicate $f$ when $\hat{y}(v) = f(v)$ for every node $v$ across all input graphs $G$.

## Key Equations

### Message-Passing Neural Network (MPNN) Update Rule

The core iterative update at each node is:

$$h^{(k+1)}(v) = \text{UPDATE}\left(h^{(k)}(v), \text{AGGREGATE}\left(\{h^{(k)}(u) : u \in N(v)\}\right)\right)$$

where:
- $h^{(k)}(v)$ is the hidden state of node $v$ at layer $k$
- $N(v)$ denotes the neighborhood of node $v$
- $\text{AGGREGATE}$ pools neighbor representations (e.g., summation, mean, max)
- $\text{UPDATE}$ transforms the aggregated message using learned parameters

### Soft Matching via Embeddings

For noisy data, define the **soft attribute overlap** between entities $u, v$:

$$\text{ov}_{\text{soft}}(u, v) = \sum_{a_u \in A(u), a_v \in A(v)} \text{sim}(\psi(a_u), \psi(a_v))$$

where:
- $\psi: A \to \mathbb{R}^d$ is a learned feature encoder mapping attribute strings to $d$-dimensional vectors
- $\text{sim}: \mathbb{R}^d \times \mathbb{R}^d \to [0, 1]$ measures similarity in embedding space (e.g., cosine similarity, Euclidean distance)
- $A(u)$ denotes the set of attribute nodes attached to entity $u$

## Physical Intuition / Derivation

### Why Message-Passing?

The message-passing framework mirrors how information naturally propagates through physical systems:

1. **Local computation**: Each node only needs information from immediate neighbors, enabling distributed, scalable computation.

2. **Iterative refinement**: Multiple message-passing layers (hops) allow information from distant nodes to eventually reach any given node. After $k$ layers, a node has aggregated information from nodes up to $k$ hops away.

3. **Permutation invariance**: The aggregation function must be symmetric (invariant to neighbor ordering), mirroring the fact that graph structure is order-independent.

### Soft Matching vs. Hard Matching

Traditional entity resolution uses **hard matching**: two attribute strings are either identical or not—a binary decision prone to failure under noise.

GNNs enable **soft matching**:
- Learn an embedding space $\psi$ where semantically similar strings (e.g., "John Smith" vs. "J. Smith") map to nearby vectors
- Compute continuous similarity scores in this learned space
- Aggregate soft signals across multiple attributes, allowing the message-passing network to *learn robust co-reference patterns*

This graceful degradation under noise is crucial for real-world applications where perfect data is rare.

### Readout and Prediction

The final node representation $h^{(K)}(v)$ (after $K$ layers) is passed through a readout/classification head to produce predictions:

$$\hat{y}(v) = \text{READOUT}(h^{(K)}(v))$$

The readout function maps learned representations to task-specific outputs (e.g., co-reference scores, node labels, link predictions).

## Applications in Engineering

### 1. **Entity Resolution & Data Cleaning**
- Identify duplicate records across databases with noisy, partially-matching attributes
- Learn soft similarity metrics from labeled duplicate/non-duplicate pairs
- Aggregate evidence across multiple attributes to make robust matching decisions

### 2. **Knowledge Graph Completion**
- Predict missing links and infer new relations between entities
- Leverage multi-hop neighborhood information to reason about entity connections

### 3. **Molecular Chemistry**
- Represent molecules as graphs (atoms = nodes, bonds = edges)
- Predict molecular properties (toxicity, solubility) from atomic structure
- Design novel compounds by learning generative models over molecular graphs

### 4. **Social Network Analysis**
- Predict user interests, detect communities, or identify influential nodes
- Model user interactions (edges) to infer latent preferences

### 5. **Traffic & Logistics**
- Represent road/shipping networks as graphs
- Predict congestion, optimize routing, forecast demand at nodes

### 6. **Recommendation Systems**
- Model users and items as bipartite graphs with interaction edges
- Use message-passing to aggregate preferences across user neighborhoods

### 7. **Circuit Design & EDA**
- Represent circuit netlists as hypergraphs
- Predict timing, power consumption, manufacturability from local circuit structure

## Common Mistakes / Pitfalls

### 1. **Confusing GNNs with CNNs on Images**
Many assume GNNs are just "CNNs for graphs." While both use local, iterative operations, GNNs must handle **variable neighborhood sizes** and **irregular connectivity**, unlike the regular grid structure of images. The aggregation function must be **permutation-invariant**, not convolution.

### 2. **Ignoring the Over-Smoothing Problem**
As the number of layers increases, node representations tend to converge to nearly identical values. This limits the benefit of deep GNNs. This is fundamentally different from ResNets in CNNs and requires specialized architectural solutions (e.g., residual connections, gating, layer normalization).

### 3.