# Graph Neural Networks

## Definition

**Graph Neural Networks (GNNs)** are a class of deep learning architectures designed to process and learn representations from graph-structured data. They operate through **message passing**: iteratively aggregating information from neighboring nodes to update each node's representation, enabling the network to capture both local neighborhood structure and global graph properties.

A GNN processes a graph $G = (V, E)$ where $V$ is the set of nodes and $E$ is the set of edges. At layer $\ell$, each node $u$ maintains an embedding $\mathbf{h}_u^{(\ell)} \in \mathbb{R}^d$. The core operation is:

$$\mathbf{h}_u^{(\ell)} = \text{AGGREGATE}^{(\ell)}\left(\{\mathbf{h}_v^{(\ell-1)} : v \in \mathcal{N}(u)\}\right)$$

where $\mathcal{N}(u)$ denotes the neighborhood of node $u$.

In **Message Passing Neural Networks (MPNNs)**, this is formalized as:
- **Message phase**: Each edge $(u,v)$ computes a message $\mathbf{m}_{uv}^{(\ell)}$ based on source and target embeddings
- **Aggregation phase**: Node $u$ aggregates messages from all incoming neighbors
- **Update phase**: Node $u$ updates its embedding using an update function

## Key Equations

### Standard MPNN Forward Pass

$$\mathbf{m}_v^{(\ell)} = \text{AGGREGATE}\left(\{\text{MESSAGE}(h_u^{(\ell-1)}, h_v^{(\ell-1)}) : u \in \mathcal{N}(v)\}\right)$$

$$\mathbf{h}_v^{(\ell)} = \text{UPDATE}\left(\mathbf{h}_v^{(\ell-1)}, \mathbf{m}_v^{(\ell)}\right)$$

### Reverse Message Passing (for Typed Graphs)

For **entity-attribute graphs** with typed edges, reverse message passing allows information to flow backward from attributes to entities:

$$\mathbf{h}_u^{(\ell)} = \text{UPDATE}\left(\mathbf{h}_u^{(\ell-1)}, \text{AGGREGATE}_{\text{reverse}}\left(\{\mathbf{h}_a^{(\ell-1)} : (u, a, \tau) \in E\}\right)\right)$$

where the aggregation operates on embeddings from attribute neighbors, conditioned on edge type $\tau$.

### Common Aggregation Functions

**Sum aggregation** (most common):
$$\mathbf{m}_v^{(\ell)} = \sum_{u \in \mathcal{N}(v)} \mathbf{W}^{(\ell)} \mathbf{h}_u^{(\ell-1)}$$

**Mean aggregation**:
$$\mathbf{m}_v^{(\ell)} = \frac{1}{|\mathcal{N}(v)|} \sum_{u \in \mathcal{N}(v)} \mathbf{W}^{(\ell)} \mathbf{h}_u^{(\ell-1)}$$

**Attention-based aggregation** (Graph Attention Networks):
$$\mathbf{m}_v^{(\ell)} = \sum_{u \in \mathcal{N}(v)} \alpha_{uv} \mathbf{W}^{(\ell)} \mathbf{h}_u^{(\ell-1)}$$

where $\alpha_{uv}$ are learned attention weights computed via softmax over neighborhood.

## Physical Intuition / Derivation

### Why Message Passing?

GNNs solve a fundamental problem: **how to share information across a discrete irregular structure** (a graph) while maintaining permutation invariance and parameter efficiency.

Traditional neural networks assume **grid-like or Euclidean structure** (convolutions assume spatial regularity). Graphs are irregular: nodes have variable degree, no canonical ordering, and connections encode semantic relationships rather than spatial proximity.

**Message passing** provides a principled solution:
1. **Local computation**: Each node independently processes its neighborhood
2. **Iterative propagation**: By stacking $L$ layers, information diffuses $L$ hops away
3. **Permutation invariance**: Aggregation functions (sum, mean, max) are invariant to the ordering of neighbors
4. **Parameter sharing**: The same transformation applies at all nodes, improving sample efficiency

### Depth Minimality in Typed Graphs

The source material establishes a key depth requirement: **detecting duplicate entities in entity-attribute graphs requires exactly 2 layers with reverse message passing** and cannot be accomplished in 1 layer.

**Why 2 layers are necessary** (intuitive):

Consider entity $u$ wants to know if another entity $v$ (of the same type) shares any of its attribute neighbors.

- **Layer 1 (forward pass)**: Entity $u$ sends its type information to all its attribute neighbors
- **Layer 1 (reverse pass)**: Each attribute aggregates the types of all incident entities
- **Layer 2 (reverse pass)**: Entity $u$ receives back a summary of which types share each attribute neighbor

A 1-layer network cannot accomplish this: after one message round, $u$ knows its own typed neighborhood $\mathcal{N}_{\text{typed}}(u)$ but has no information about whether other same-type entities share those neighbors. The key insight is that **2-hop information along the bipartite entity-attribute structure is essential**.

### Multigraph Complexity

In **multigraphs** (where parallel edges between the same node pair are allowed), standard GNNs must be extended to handle **edge multiplicities**. This arises naturally in:
- Master data management: multiple claims from different sources/times between the same entity-attribute pair
- Transaction networks: multiple transfers between the same account pair

The aggregation must now account for multiplicity: 
$$\mathbf{m}_v^{(\ell)} = \text{AGGREGATE}\left(\left\{\text{MESSAGE}(h_u^{(\ell-1)}, h_