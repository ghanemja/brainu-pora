# Graph Neural Network Expressiveness

## Definition

**Graph Neural Network (GNN) expressiveness** refers to the theoretical capacity of a GNN architecture to learn and compute arbitrary functions on graph-structured data. More formally, it characterizes which graph properties, subgraph patterns, and node/graph functions a given GNN can provably represent.

A GNN architecture is said to be **expressive** for a task if there exists a configuration of weights and parameters such that the network can correctly compute the target function. Conversely, an architecture that is provably **inexpressive** for a task cannot learn that function regardless of:
- Training procedure or optimization algorithm
- Dataset size or sampling strategy
- Network overparameterization

In the context of **Message Passing Neural Networks (MPNNs)** on directed multigraphs, expressiveness is fundamentally limited by the information available at each node during aggregation. Standard MPNNs without structural adaptations often cannot distinguish between certain graph patterns, leading to **expressive bottlenecks**.

## Key Equations

### Standard Message Passing Update (Layer $k$)

For an undirected graph, the basic MPNN update is:

$$a^{(k)}(v) = \text{AGG}^{(k)}\left\{\left(h^{(k-1)}(w), \tau(v,w)\right) : (v,w) \in E\right\}$$

$$h^{(k)}(v) = \text{UPDATE}^{(k)}\left(h^{(k-1)}(v), a^{(k)}(v)\right)$$

where:
- $h^{(k)}(v)$ is the embedding of node $v$ at layer $k$
- $\text{AGG}^{(k)}$ is a permutation-invariant aggregation function (e.g., sum, mean)
- $\tau(v,w)$ is the edge type/label
- $\text{UPDATE}^{(k)}$ is a learnable update function

### Reverse Message Passing (Directed Graphs)

For directed multigraphs, separate aggregations over incoming and outgoing edges:

$$a^{(k)}_{\text{in}}(v) = \text{AGG}^{(k)}_{\text{in}}\left\{\left(h^{(k-1)}(w), \tau\right) : (w, v, \tau) \in E\right\}$$

$$a^{(k)}_{\text{out}}(v) = \text{AGG}^{(k)}_{\text{out}}\left\{\left(h^{(k-1)}(w), \tau\right) : (v, w, \tau) \in E\right\}$$

$$h^{(k)}(v) = \text{UPDATE}^{(k)}\left(h^{(k-1)}(v), a^{(k)}_{\text{in}}(v), a^{(k)}_{\text{out}}(v)\right)$$

### Port-Numbered Aggregation

When port numbering is applied (to distinguish parallel edges):

$$a^{(k)}_{\text{in}}(v) = \text{AGG}^{(k)}_{\text{in}}\left\{\left(h^{(k-1)}(w), \tau, p_{\text{in}}(e), p_{\text{out}}(e)\right) : (w, v, \tau) \in E\right\}$$

Port numbering constraints:
- **(i)** Parallel edges from source $u$ to destination $v$ share identical $(p_{\text{in}}, p_{\text{out}})$ pairs
- **(ii)** Distinct sources into $v$ receive distinct $p_{\text{in}}$ values
- **(iii)** Distinct destinations from $u$ receive distinct $p_{\text{out}}$ values

## Physical Intuition / Derivation

### Why Standard MPNNs Fail

Consider a simple directed graph where all edges point from **entities** to **attributes** (a common pattern in knowledge graphs). A standard MPNN propagates information only in the forward direction:

```
Entity1 → Attribute1
Entity1 → Attribute2
Entity2 → Attribute1
```

Without reverse message passing, entity nodes aggregate only their own information and never "see" their attribute neighbors. Thus, entities that share attributes cannot distinguish themselves based on graph structure alone—a critical failure for graph isomorphism detection or entity linking tasks.

### The Expressiveness Hierarchy

The source material implicitly establishes an expressiveness hierarchy:

1. **Base MPNN**: Unidirectional aggregation only
   - Cannot handle directed graphs with semantically important edge direction
   - Loses information in entity-attribute structures

2. **MPNN + Reverse Message Passing**: Bidirectional information flow
   - Restores some expressiveness for directed graphs
   - But still cannot distinguish parallel edges or edge ordering

3. **MPNN + Reverse Passing + Port Numbering**: Fully expressive for directed multigraphs
   - Edge ordering is encoded in port assignments
   - Parallel edges become distinguishable
   - Achieves maximal expressiveness (at computational cost)

### The Computational Trade-off

The key insight is **expressiveness vs. efficiency**:
- Full expressiveness (ego IDs + bidirectional port numbering): $O(|V|^2)$ complexity per layer
- Minimal adaptations: $O(|V| + |E|)$ complexity but reduced expressiveness

The fundamental question becomes: **which adaptations are necessary for a specific task?** Omitting unnecessary adaptations yields quadratic computational savings without sacrificing correctness.

## Applications in Engineering

### 1. Knowledge Graph Reasoning
In semantic web and knowledge graph completion, entities have typed relationships (attributes):
- Entity-attribute edges are directional and should be distinguished from entity-entity links
- Reverse message passing allows entities to implicitly learn attribute values
- Port numbering handles multi-valued attributes (same entity has multiple values for the same attribute)

### 2. Circuit Design & EDA
Graph-based representations of electronic circuits often require:
- Directed edges (signal flow, power distribution)
- Multiple parallel edges (control signals, data buses on the same connection)
- Structured message passing to distinguish input vs. output relationships in analog designs