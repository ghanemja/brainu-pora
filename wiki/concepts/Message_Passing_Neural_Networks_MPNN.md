# Message Passing Neural Networks (MPNN)

## Definition

A **Message Passing Neural Network (MPNN)** is a class of graph neural networks that learn representations of graph-structured data through iterative local message exchanges between neighboring nodes. At each layer, every node aggregates information from its neighbors, updates its representation, and passes updated messages to neighbors in the next layer.

Formally, an MPNN operates on a graph $\mathcal{G} = (\mathcal{V}, \mathcal{E})$ with node features $\mathbf{x}_v$ and learns node embeddings through:

$$h_v^{(k+1)} = \text{UPDATE}^{(k)}\left(h_v^{(k)}, \text{AGGREGATE}^{(k)}\left(\left\{h_u^{(k)} : u \in \mathcal{N}(v)\right\}\right)\right)$$

where:
- $h_v^{(k)}$ is the hidden representation of node $v$ at layer $k$
- $\mathcal{N}(v)$ is the neighborhood of node $v$
- **UPDATE** and **AGGREGATE** are differentiable functions (typically neural networks)

The initial node features are $h_v^{(0)} = \mathbf{x}_v$. After $K$ layers, final predictions are made using a **READOUT** function.

### Core Architectural Components

1. **Message Function**: Computes messages from neighbor $u$ to node $v$
   $$m_{u \to v}^{(k)} = f_{\text{msg}}^{(k)}(h_u^{(k)}, h_v^{(k)}, e_{uv})$$

2. **Aggregation Function**: Combines incoming messages (e.g., sum, mean, max)
   $$a_v^{(k)} = \text{AGG}\left(\{m_{u \to v}^{(k)} : u \in \mathcal{N}(v)\}\right)$$

3. **Update Function**: Refines node representation
   $$h_v^{(k+1)} = \text{MLP}\left([h_v^{(k)} \| a_v^{(k)}]\right)$$

where $\|$ denotes concatenation.

## Key Equations

### Standard MPNN Formulation

$$h_v^{(k+1)} = \phi^{(k)}\left(h_v^{(k)}, \bigoplus_{u \in \mathcal{N}(v)} \psi^{(k)}(h_v^{(k)}, h_u^{(k)}, e_{uv})\right)$$

where $\phi$ and $\psi$ are learnable neural networks and $\bigoplus$ is a permutation-invariant aggregation operator.

### Reverse Message Passing (for directed graphs)

$$h_v^{(k+1)} = \text{UPDATE}\left(h_v^{(k)}, \bigoplus_{u : v \to u} m_v^{(k)}\right)$$

Messages flow opposite the edge direction, necessary for certain entity resolution tasks.

### Ego ID Augmentation

To break symmetry in highly symmetric structures, augment node features with ego IDs:
$$\mathbf{x}_v^{\text{ego}} = [\mathbf{x}_v \| \text{one\_hot}(v)]$$

This enables the network to distinguish otherwise identical nodes.

### Port Numbering (for multigraphs)

Encode edge indices explicitly in aggregation:
$$a_v^{(k)} = \text{AGG}\left(\{\text{port\_id}(i) \oplus \psi^{(k)}(h_v^{(k)}, h_u^{(k)}) : i \in |E_{uv}|, u \in \mathcal{N}(v)\}\right)$$

where port IDs distinguish parallel edges.

## Physical Intuition / Derivation

### Why Message Passing?

Consider a network of agents (nodes) that only have local information. To solve global problems—like determining if two distant nodes belong to the same cluster or detecting cycles—agents must **gradually spread information** across the network. Each layer of the MPNN represents one "hop" of information flow, enabling nodes to learn patterns at increasing receptive field sizes.

### Receptive Field Growth

A critical insight: after $K$ layers, each node has access to information from all nodes within graph distance $K$. This is the **receptive field** of the network:

$$\text{Receptive Field}_{K} = \{u \in \mathcal{V} : d(v,u) \leq K\}$$

where $d(v,u)$ is the shortest path distance.

### Example: Why Dup₁ ≠ Dupr (the separation result)

**Dup₁ task**: Detect if an entity shares *at least one* attribute with another entity of the same type.

This is **purely local**: check if two entities have overlapping attributes. A 2-layer MPNN with only reverse message passing suffices:
- Layer 1: Each attribute node broadcasts its identity
- Layer 2: Each entity collects which entities share attributes with it

**Dupr task** ($r \geq 2$): Detect if an entity shares *at least r* attribute values (not just whether it shares with one other entity).

This requires verifying that the **same external entity appears at multiple attributes**. Without ego IDs to distinguish identical nodes, the network cannot track:
- "Is this the same entity appearing twice, or two different entities?"

This creates **cross-attribute identity correlation**, a fundamentally non-local requirement necessitating:
- Ego IDs (to break symmetry)
- 4 layers minimum (to propagate multi-hop identity confirmation)

### Information vs. Computation Trade-offs

The source material reveals a **sharp complexity gap**:

| Task | Sufficient Adaptations | Min. Depth | Why |
|------|----------------------|-----------|-----|
| Dup₁ | Reverse message passing | 2 | Local overlap detection |
| Dupr ($r \geq 2$