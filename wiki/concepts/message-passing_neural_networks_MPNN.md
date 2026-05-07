# message-passing neural networks (MPNN)

## Definition

A **message-passing neural network (MPNN)** is a class of graph neural networks (GNNs) that learns representations of graph-structured data by iteratively aggregating and transforming information from a node's neighborhood. At each layer, nodes update their hidden states by:

1. **Aggregating messages** from neighboring nodes
2. **Applying a learnable transformation** to the aggregated information
3. **Updating the node representation** based on its previous state and the aggregated messages

In the context of **entity-attribute graphs** (bipartite graphs connecting entities to their attribute values), MPNNs can be enriched with architectural extensions:
- **Reverse message passing**: allows information to flow from attribute nodes back to entity nodes
- **Port numbering**: distinguishes between different edge types or connection orderings
- **Ego IDs**: node-specific identifiers enabling awareness of node identity across layers

## Key Equations

The standard MPNN update rule for node $v$ at layer $\ell$ is:

$$h_v^{(\ell+1)} = \text{UPDATE}^{(\ell)}\left(h_v^{(\ell)}, \text{AGGREGATE}^{(\ell)}\left(\{h_u^{(\ell)} : u \in \mathcal{N}(v)\}\right)\right)$$

where:
- $h_v^{(\ell)}$ is the hidden state of node $v$ at layer $\ell$
- $\mathcal{N}(v)$ is the neighborhood of node $v$
- $\text{AGGREGATE}$ is a permutation-invariant function (e.g., sum, mean, max)
- $\text{UPDATE}$ is a learnable function (typically a neural network)

For **reverse message passing** on bipartite entity-attribute graphs, the flow is bidirectional:

$$h_{\text{entity}}^{(\ell+1)} = \text{UPDATE}_E\left(h_{\text{entity}}^{(\ell)}, \text{AGGREGATE}\left(\{h_{\text{attr}}^{(\ell)} : \text{attr} \in \mathcal{N}(\text{entity})\}\right)\right)$$

$$h_{\text{attr}}^{(\ell+1)} = \text{UPDATE}_A\left(h_{\text{attr}}^{(\ell)}, \text{AGGREGATE}\left(\{h_{\text{entity}}^{(\ell)} : \text{entity} \in \mathcal{N}(\text{attr})\}\right)\right)$$

The **expressivity threshold** for detecting $r$ shared attributes between entities of the same type:

- **Single shared attribute ($r=1$)**: Requires **2 layers** with reverse message passing (local computation)
- **Multiple shared attributes ($r>1$)**: Requires **4 layers** with ego IDs (non-local computation)

This captures the fundamental distinction between **local attribute checking** and **cross-attribute identity correlation**.

## Physical Intuition / Derivation

### Why Message Passing?

Graph neural networks must respect the **permutation invariance** of neighborhood structure: the order in which neighbors are processed should not affect the outcome. MPNNs achieve this through aggregation functions that combine information from all neighbors in a symmetric way.

### The Two-Stage Process

1. **Message Construction**: Each neighbor computes a "message" (a feature vector) based on its current state
2. **Aggregation**: The receiving node combines all incoming messages via a commutative operation
3. **Update**: The node incorporates aggregated information with its previous state

### Depth vs. Expressivity

The **receptive field** of an MPNN grows with depth:
- Layer 0: Node sees itself only
- Layer 1: Node sees neighbors at distance 1
- Layer $\ell$: Node sees neighbors at distance ≤ $\ell$

For **entity resolution on bipartite graphs**, the depth requirements reflect computational complexity:

- **Detecting one shared attribute**: Entity $A$ must check if attributes point to another entity $B$. A single reverse pass (entity → attribute → entity) suffices in 2 layers.

- **Detecting $r \geq 2$ shared attributes**: Entity $A$ must verify the *same* entity $B$ appears at multiple attributes. This requires "identity correlation"—ensuring the entity identity is maintained across attribute hops. Without ego IDs, the network cannot distinguish whether multiple attributes point to the same entity or different entities. **Ego IDs** provide explicit node identifiers, breaking this symmetry and enabling the network to track identity. Four layers enable:
  - Layer 1–2: Entity→Attribute→Entity (local attribute checking)
  - Layer 3–4: Cross-attribute consistency verification (identity correlation)

### Separation Theory

The source material establishes **tight expressivity hierarchies**—provably minimal architectures:
- **Lower bounds**: Graph pairs that all simpler architectures cannot distinguish (via Weisfeiler–Leman argument)
- **Upper bounds**: Explicit MPNN constructions that solve the problem with minimal depth and features

## Applications in Engineering

### Master Data Management (MDM)
Deduplicating customer, product, or supplier records across databases. MPNNs learn that records sharing multiple attributes likely represent the same real-world entity.

### Knowledge Graph Completion
Predicting missing entities or relations by reasoning about entity-attribute connectivity patterns.

### Recommendation Systems
Learning user-item representations where bipartite user-product graphs are common. MPNNs aggregate signals from intermediate attributes (categories, genres, etc.).

### Fraud Detection
Identifying suspicious activity by detecting shared attributes between accounts (same IP address, phone number, email domain) via entity-attribute graphs.

### Computer Vision & Scene Graphs
Connecting visual objects to their attributes (color, size, material) and predicting relationships between them.

### Molecular Property Prediction
Atoms and bonds form graphs; MPNNs aggregate atom features to predict molecular properties.

### Network Anomaly Detection
Detecting coordinated attack patterns in bipartite networks (users-to-hosts, IPs-to-ports) by identifying shared attributes.

## Common Mistakes / Pitfalls

### 1. **Over-architecture without justification**
Including reverse message passing, port numbering, and ego IDs by default adds unnecessary computation. The separation theory