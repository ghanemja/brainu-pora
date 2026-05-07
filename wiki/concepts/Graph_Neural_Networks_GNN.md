# Graph Neural Networks (GNN)

## Definition

A **Graph Neural Network (GNN)** is a class of neural network architectures designed to process and learn representations from graph-structured data. GNNs operate by iteratively aggregating information from neighboring nodes through message passing, enabling them to capture both local node properties and global graph structure.

### Core Components

- **Nodes**: Entities in the domain (atoms in molecules, users in social networks, etc.)
- **Edges**: Relationships or interactions between entities
- **Node Features**: Input attributes associated with each node
- **Message Passing**: The fundamental operation where nodes exchange and aggregate information with neighbors

A GNN is formally defined by a sequence of learned transformations applied at each layer:

$$h_v^{(k)} = \text{UPDATE}^{(k)}\left(h_v^{(k-1)}, \text{AGGREGATE}^{(k)}\left(\{h_u^{(k-1)} : u \in \mathcal{N}(v)\}\right)\right)$$

where:
- $h_v^{(k)}$ is the hidden representation of node $v$ at layer $k$
- $\mathcal{N}(v)$ is the set of neighbors of node $v$
- $\text{AGGREGATE}$ combines neighbor messages (mean, sum, or max pooling)
- $\text{UPDATE}$ transforms aggregated information with learned parameters

## Key Equations

### Message Passing Framework

The standard message-passing neural network (MPNN) update rule:

$$h_v^{(k)} = \phi\left(h_v^{(k-1)}, \square_{u \in \mathcal{N}(v)} \psi(h_v^{(k-1)}, h_u^{(k-1)}, e_{uv})\right)$$

where $\square$ denotes a permutation-invariant aggregation operator and $\psi, \phi$ are learnable functions.

### Reverse Message Passing (Backward Aggregation)

For certain tasks requiring target-to-neighbor propagation:

$$h_v^{(k)} = \phi\left(h_v^{(k-1)}, \square_{u : v \in \mathcal{N}(u)} \psi(h_v^{(k-1)}, h_u^{(k-1)})\right)$$

This extends message passing to include incoming edges, critical for detecting relationships like co-references in entity resolution.

### Ego ID Mechanism

Nodes augmented with unique identifiers to break symmetry:

$$h_v^{(k)} = \phi\left(h_v^{(k-1)}, \text{EGO\_ID}(v), \square_{u \in \mathcal{N}(v)} \psi(h_u^{(k-1)})\right)$$

Ego IDs enable nodes to distinguish themselves from structurally identical neighbors, essential for **cross-attribute identity correlation** tasks.

## Physical Intuition / Derivation

### Why Message Passing?

The fundamental insight is that **node representations should depend on local neighborhood structure**. Rather than treating graphs as fixed matrices (leading to non-scalability), GNNs compute node features through an iterative process mirroring diffusion of information:

1. **Layer 0**: Each node knows only itself
2. **Layer 1**: Each node knows its immediate neighbors
3. **Layer $k$**: Each node can aggregate information from all nodes within $k$-hops (its $k$-hop neighborhood)

### The Expressiveness Hierarchy

The source material reveals a **strict complexity hierarchy** for graph understanding tasks:

```
Task Complexity          | Required Adaptation       | Depth | Example
─────────────────────────|──────────────────────────|──────|──────────
Local matching (Dup₁)    | Reverse message passing  |  2   | "Do entities share ANY attribute?"
Shared attributes (Dupᵣ) | Ego IDs + reverse pass   |  4   | "Do entities share ≥r attributes?"
Cycle detection          | Ego IDs + directed edges |  k   | "Does a cycle of length l exist?"
```

**Why this hierarchy?** 

Dup₁ (checking if two entities share *any* attribute) requires only **backward aggregation** from target entities to their attributes—a purely local two-hop computation.

Dupᵣ ($r \geq 2$, checking if entities share *at least r* specific attributes) presents **cross-attribute identity correlation**: verifying that the *same* entity appears across *multiple* attributes is fundamentally non-local. Standard forward message passing cannot distinguish whether multiple observed connections originate from one entity or many. Ego IDs break this ambiguity by giving each node a unique identity that propagates through the network.

### Separation Theory Foundation

The source material establishes **necessity via indistinguishability**: for each adaptation, the authors construct graph pairs that are provably indistinguishable by MPNNs lacking that adaptation. This proves the adaptation is not merely helpful but mathematically required.

## Applications in Engineering

### Entity Resolution & Record Linkage
**Use Case**: Merging duplicate customer records across databases
- Determine if records represent the same physical entity by analyzing shared attributes (addresses, phone numbers, emails)
- Dup₁ identifies any overlap; Dupᵣ confirms substantial agreement
- **Critical**: Cross-attribute correlation prevents false merges

### Molecular Property Prediction
**Use Case**: Predicting chemical properties from atomic structure
- Nodes = atoms, edges = chemical bonds
- GNNs learn representations of local chemical environments
- Applications: drug discovery, materials science

### Social Network Analysis
**Use Case**: Community detection, influence propagation
- Nodes = users, edges = friendships/follows
- Reverse message passing identifies mutual connections (reciprocal relationships)
- Ego IDs distinguish individual users in otherwise symmetric network positions

### Knowledge Graph Completion
**Use Case**: Inferring missing relationships in structured knowledge
- Detecting cycles in entity-entity relationships indicates potential inference paths
- Typed entity-attribute graphs naturally model knowledge bases with heterogeneous data

### Recommendation Systems
**Use Case**: Collaborative filtering through graph structure
- Nodes = users and items, edges = interactions
- Message passing aggregates preference signals from similar users/items

## Common Mistakes /