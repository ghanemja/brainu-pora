# Message passing neural networks (MPNNs)

## Definition

Message passing neural networks (MPNNs) are a class of graph neural networks that operate on graphs by iteratively updating node representations through local message exchange between neighboring nodes. In each layer, every node:

1. **Aggregates** messages from its neighbors
2. **Updates** its own representation using an aggregation function and a learnable update function
3. **Passes** updated information to neighbors in the next layer

MPNNs provide a unified framework for analyzing diverse graph neural network architectures (including graph convolutional networks, graph attention networks, and graph isomorphism networks) under a common computational paradigm.

## Key Equations

The standard MPNN forward pass for layer $\ell$ is:

$$m_i^{(\ell)} = \bigoplus_{j \in \mathcal{N}(i)} \text{MSG}^{(\ell)}(h_j^{(\ell-1)}, h_i^{(\ell-1)}, e_{ij})$$

$$h_i^{(\ell)} = \text{UPDATE}^{(\ell)}(h_i^{(\ell-1)}, m_i^{(\ell)})$$

where:
- $h_i^{(\ell)}$ = node $i$'s hidden representation at layer $\ell$
- $\mathcal{N}(i)$ = the neighborhood of node $i$ (incoming or outgoing, depending on graph direction)
- $\text{MSG}^{(\ell)}$ = learned message function (e.g., neural network)
- $e_{ij}$ = edge features or edge type between nodes $i$ and $j$
- $\bigoplus$ = aggregation operator (sum, mean, max, or learnable permutation-invariant function)
- $\text{UPDATE}^{(\ell)}$ = learned node update function

For **directed multigraphs** (multiple edge types), the message function becomes:

$$m_i^{(\ell)} = \bigoplus_{j \in \mathcal{N}(i)} \bigoplus_{r \in \mathcal{R}(i,j)} \text{MSG}_r^{(\ell)}(h_j^{(\ell-1)}, h_i^{(\ell-1)})$$

where $\mathcal{R}(i,j)$ enumerates distinct relation types between $i$ and $j$.

## Physical Intuition / Derivation

### Why Message Passing?

Traditional neural networks process fixed-size, fully-connected inputs. Graphs are **variable-size and sparse**—adjacent nodes are highly correlated, while distant nodes are not. Message passing leverages this locality:

1. **Local computation**: Each node needs only neighborhood information, enabling distributed, scalable computation
2. **Depth as receptive field**: After $\ell$ layers, node $i$ has aggregated information from all nodes within $\ell$ hops (its $\ell$-hop neighborhood)
3. **Permutation invariance**: The aggregation operator $\bigoplus$ must be invariant to the order in which neighbors are processed—this forces the use of symmetric functions (sum, mean, max)

### Building Understanding Through Layers

**Layer 0 (Input):** Each node starts with features $h_i^{(0)}$ (e.g., node type, attributes).

**Layer 1:** Each node collects direct neighbors' features via messages. A node can now distinguish itself from neighbors and compute local graph patterns (degree, local clustering).

**Layer 2:** Messages now encode information from 2-hop neighbors, enabling detection of paths and simple subgraph motifs.

**Layer $\ell$:** Each node "sees" the structure within $\ell$ hops. The receptive field grows linearly with depth.

### Limitations and Theoretical Characterization

The source material highlights a critical gap: **not all graph patterns can be distinguished by arbitrary MPNNs**. Key distinctions depend on:

- **Reverse message passing**: Allowing information flow along reversed (backward) edges in directed graphs
- **Directed multigraph port numbering**: Assigning canonical orderings to edge instances to break symmetries
- **Ego IDs**: Unique node identifiers to overcome permutation symmetries

For example, the **Dupr** (duplicate detection) and **Cycl** (cycle detection) tasks have different architectural requirements—some tasks require all three adaptations; others need only a subset. This motivates **separation theorems**: formal proofs that certain tasks *require* specific architectural features.

## Applications in Engineering

### Data Management and Entity Resolution
- **Entity matching**: Constructing entity-record graphs and using MPNNs (e.g., GraphER, HierGAT) to identify duplicate records across databases
- **Link prediction**: Predicting missing relationships in master data graphs while respecting anonymization and privacy constraints
- **Relation extraction**: Incorporating document structure and multi-relational edges (R-GCNs) to extract semantic relationships from unstructured data

### Knowledge Graph Completion
- Predicting missing edges in knowledge bases using multi-hop neighborhood patterns
- Handling typed relations via relation-specific message functions

### Molecular and Chemical Informatics
- Molecular property prediction: nodes = atoms, edges = bonds; MPNNs learn invariant representations for drug discovery
- Reaction prediction and mechanism analysis

### Social Networks and Recommendation Systems
- Community detection and link recommendation via neighborhood aggregation
- Influence propagation modeling in heterogeneous networks

### Robotics and Control
- Multi-agent coordination: agents as nodes, communication channels as edges
- Distributed planning over constraint graphs

### Supply Chain and Manufacturing Networks
- Fault propagation analysis in production systems
- Inventory optimization on supplier networks

## Common Mistakes / Pitfalls

1. **Confusing depth with expressiveness**: More layers ≠ more powerful. Shallow networks can fail on certain patterns (e.g., detecting cycles in sparse graphs), but blindly adding layers causes **over-squashing** (information from distant nodes gets compressed into fixed-size vectors) and **over-smoothing** (all node representations converge to similar values).

2. **Ignoring permutation invariance requirements**: Aggregation functions *must* be symmetric. Using non-symmetric operations (e.g., concatenation in a fixed order) breaks the theoretical guarantees and may overfit to the training graph's node ordering