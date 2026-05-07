# Reverse message passing

## Definition

**Reverse message passing** is an architectural adaptation for Message Passing Neural Networks (MPNNs) that enables information flow **against the direction of edges** in directed graphs. In each layer, nodes aggregate information from both their predecessors (incoming edges) and successors (outgoing edges), with these two aggregations computed separately and then combined in the node update step.

Formally, an MPNN is said to employ reverse message passing when each node $v$ maintains two independent aggregation pathways:
- **Incoming aggregation**: messages from predecessors (nodes $w$ where $(w, v, \tau) \in E$)
- **Outgoing aggregation**: messages from successors (nodes $w$ where $(v, w, \tau) \in E$)

This is in contrast to standard MPNNs, which only aggregate information flowing **along** edge directions.

## Key Equations

At layer $k$, a node $v$ computes two separate aggregations:

$$a^{(k)}_{\text{in}}(v) = \text{AGG}^{(k)}_{\text{in}} \left\{\!\!\left\{(h^{(k-1)}(w), \tau) : (w, v, \tau) \in E\right\}\!\!\right\}$$

$$a^{(k)}_{\text{out}}(v) = \text{AGG}^{(k)}_{\text{out}} \left\{\!\!\left\{(h^{(k-1)}(w), \tau) : (v, w, \tau) \in E\right\}\!\!\right\}$$

The node embedding is then updated by combining both aggregations:

$$h^{(k)}(v) = \text{UPDATE}^{(k)}\left(h^{(k-1)}(v), a^{(k)}_{\text{in}}(v), a^{(k)}_{\text{out}}(v)\right)$$

where:
- $h^{(k)}(v)$ is the embedding of node $v$ at layer $k$
- $\text{AGG}^{(k)}_{\text{in}}, \text{AGG}^{(k)}_{\text{out}}$ are learnable aggregation functions (e.g., sum, mean, max)
- $\text{UPDATE}^{(k)}$ is a learnable update function (e.g., multi-layer perceptron)
- $\tau$ denotes edge type labels (for typed graphs)

## Physical Intuition / Derivation

### Why Reverse Message Passing Matters

Consider a **typed entity-attribute graph** where all edges point from entities to attributes. In a standard MPNN:
- Entities can send messages to attributes (following edge direction)
- Attributes **cannot** receive messages from other attributes
- Entities cannot receive information from attributes

This creates an asymmetry: attributes remain isolated from one another and cannot communicate information back to entities. The graph's structure becomes essentially "read-only" in the backward direction.

**Reverse message passing solves this** by allowing information to flow both ways:
1. Forward direction: Entities→Attributes (standard message passing)
2. Backward direction: Attributes→Entities (reverse message passing)

### Expressivity Argument

The fundamental motivation is **expressive power**. There exist graph properties and structural patterns that cannot be computed without bidirectional information flow. For example:

- **Attribute-based entity similarity**: An entity node cannot determine if another entity shares the same attributes unless information flows back from attributes to entities.
- **Cycle detection in DAGs**: Distinguishing DAGs from general digraphs requires nodes to "understand" their successors, not just predecessors.

By maintaining separate `in` and `out` aggregations, the UPDATE function can learn to distinguish and weight information based on direction, enabling the network to compute directionally-dependent features.

### Computational Trade-off

Reverse message passing increases per-layer complexity:
- Standard MPNN: $O(|E|)$ per layer (one message per edge)
- With reverse passing: $O(2|E|) = O(|E|)$ asymptotically, but with higher constant factors due to dual aggregation pathways

The cost is justified when the target task requires bidirectional reasoning; omitting it for unnecessary tasks wastes computational resources.

## Applications in Engineering

### Knowledge Graph Reasoning
Entity-attribute knowledge graphs often have directed semantics (e.g., "Person → hasAge → 25"). Reverse message passing allows entities to aggregate attribute information for tasks like entity classification or link prediction in heterogeneous graphs.

### Compiler Intermediate Representations
In compiler optimization, control flow graphs and data dependency graphs are inherently directed. Nodes need information about both downstream uses and upstream definitions to compute properties like reaching definitions or liveness analysis. Reverse message passing enables neural models to learn these classic compiler analyses.

### Recommendation Systems
Bipartite graphs (users ↔ items) often have directional semantics. Reverse message passing allows items to aggregate user-side information without treating the graph as undirected, preserving semantic asymmetry.

### Circuit Design & Netlist Analysis
Electronic circuit netlists represent directed signal flow (inputs → gates → outputs). Reverse message passing enables neural networks to reason about signal propagation in both directions for tasks like timing analysis or fault diagnosis.

### Molecular Property Prediction
In directed molecular graphs (bonds with directionality), reverse message passing can improve expressiveness for learning stereochemistry or reaction center properties by allowing atoms to aggregate information about both incoming and outgoing bonds.

## Common Mistakes / Pitfalls

### Mistake 1: Confusing Reverse Message Passing with Undirected Graphs
**Wrong**: "Reverse message passing just makes the graph undirected."
**Correct**: Reverse passing preserves directionality but adds *separate* reverse information flow. The UPDATE function can distinguish "messages from predecessors" vs. "messages from successors," unlike true undirected graphs where this distinction is erased.

### Mistake 2: Assuming Reverse Passing is Always Necessary
**Wrong**: "Every directed graph task needs reverse message passing."
**Correct**: Tasks where information only flows "downhill" (e.g., DAG processing with topological ordering) may not require reverse passing. Unnecessary adaptations waste computation without improving expressiveness.

### Mistake 3: Neglecting Separate Aggregation Functions
**Wrong**: Using the same aggregation function