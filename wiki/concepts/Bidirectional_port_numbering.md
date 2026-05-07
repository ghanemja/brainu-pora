# Bidirectional Port Numbering

## Definition

**Bidirectional port numbering** is a technique for enhancing Message Passing Neural Networks (MPNNs) operating on directed multigraphs. It assigns integer port labels to each edge that enable nodes to structurally distinguish between:
- Multiple parallel edges from the same source to the same destination
- Edges arriving from distinct predecessors
- Edges departing to distinct successors

Formally, each edge $e \in E$ is assigned:
- An **incoming port number** $p_{\text{in}}(e) \in \mathbb{N}$ (visible at the destination node)
- An **outgoing port number** $p_{\text{out}}(e) \in \mathbb{N}$ (visible at the source node)

These port numbers are attached as edge features and made visible to both endpoints during message passing.

## Constraints on Port Assignment

Port numbering must satisfy three invariants:

**(i) Parallel edges share ports:**  
All parallel edges from source $u$ to destination $v$ receive identical port numbers at both endpoints.

**(ii) Incoming port distinctness:**  
For any node $v$, edges from distinct sources $u_1 \neq u_2$ into $v$ must have distinct incoming ports:
$$\text{if } (u_1, v, \tau_1), (u_2, v, \tau_2) \in E \text{ and } u_1 \neq u_2, \text{ then } p_{\text{in}}(e_1) \neq p_{\text{in}}(e_2)$$

**(iii) Outgoing port distinctness:**  
For any node $u$, edges from $u$ to distinct destinations $v_1 \neq v_2$ must have distinct outgoing ports:
$$\text{if } (u, v_1, \tau_1), (u, v_2, \tau_2) \in E \text{ and } v_1 \neq v_2, \text{ then } p_{\text{out}}(e_1) \neq p_{\text{out}}(e_2)$$

## Key Equations

When port numbering is combined with [[reverse message passing]], the aggregation functions at layer $k$ become:

$$a_{\text{in}}^{(k)}(v) = \text{AGG}_{\text{in}}^{(k)} \left\{\left\{(h^{(k-1)}(w), \tau, p_{\text{in}}(e)) : (w, v, \tau) \in E\right\}\right\}$$

$$a_{\text{out}}^{(k)}(v) = \text{AGG}_{\text{out}}^{(k)} \left\{\left\{(h^{(k-1)}(w), \tau, p_{\text{out}}(e)) : (v, w, \tau) \in E\right\}\right\}$$

Node embedding update:
$$h^{(k)}(v) = \text{UPDATE}^{(k)}\left(h^{(k-1)}(v), a_{\text{in}}^{(k)}(v), a_{\text{out}}^{(k)}(v)\right)$$

The port numbers $(p_{\text{in}}(e), p_{\text{out}}(e))$ become additional input features to the aggregation functions, allowing the network to condition its message passing on the structural position of each edge.

## Physical Intuition / Derivation

### Why Bidirectional Port Numbering is Necessary

In a standard MPNN on a directed graph, messages flow along edge directions. However, this creates a critical expressiveness problem:

**The Entity-Attribute Problem:**  
Consider a typed entity-attribute graph where all edges point from entities to attributes (e.g., a knowledge graph). A standard forward-only MPNN would:
- Allow entity nodes to aggregate information from attribute neighbors ✓
- Prevent attribute nodes from receiving any neighbor information ✗

This breaks symmetry and prevents the network from computing functions that require bidirectional information flow.

### Why Port Numbers Matter

In a directed multigraph, multiple edges between the same pair of nodes create **structural ambiguity**. Without port numbering:

**Example (parallel edges):**
```
Node u --[edge 1, type A]→ Node v
Node u --[edge 2, type B]→ Node v
```

Both edges arrive at $v$ with the same source $u$. Without port numbering, standard aggregation functions like $\text{AGG}(\text{multiset})$ cannot distinguish which message originated from which edge. This loss of information means the network cannot compute functions that depend on which specific edge carried the message.

### Port Assignment Algorithm

A valid port numbering can be constructed in $O(|E| \log |E|)$ time via:

1. **Sort edges** by (destination, source, type) to assign incoming ports
2. **Sort edges** by (source, destination, type) to assign outgoing ports
3. **Assign sequential integers** within each equivalence class

This ensures all three constraints are satisfied by construction.

## Applications in Engineering

### 1. Knowledge Graph Representation Learning
Heterogeneous knowledge graphs often have multiple relation types between entities. Bidirectional port numbering enables:
- Distinguishing between parallel edges of different relation types
- Symmetric reasoning (entity → attribute and attribute → entity)
- More expressive graph embeddings for link prediction and entity classification

### 2. Circuit and Network Design
In directed network graphs (e.g., control flow graphs, dataflow graphs):
- Port numbers identify distinct control/data paths from the same source
- Bidirectional information flow helps detect feedback loops and data dependencies
- Critical for compiler intermediate representation (IR) analysis

### 3. Molecular Graph Neural Networks
Molecular graphs may contain multiple bonds between atoms:
- Bidirectional ports distinguish single/double/triple bonds in both directions
- Reverse message passing enables aromatic ring detection and conjugation detection
- Improves prediction of molecular properties and chemical reactivity

### 4. Social Network Analysis
In directed social graphs (followers, collaborators):
- Parallel edges represent different relationship types (trust, collaboration, communication)
- Bidirectional numbering enables detecting mutual influence and reciprocal relationships
- Port structure helps identify cl