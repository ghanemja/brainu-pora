# Inductive aggregation

## Definition

**Inductive aggregation** is a proof and construction technique used in graph neural networks (GNNs) to establish what functions can and cannot be computed by message-passing neural networks (MPNNs). It proceeds in two phases:

1. **Inductive step**: Show that a property holds at depth $K+1$ by assuming it holds at depth $K$, typically by analyzing how messages aggregate at nodes of different classes (typed entities, attributes, etc.)

2. **Reverse aggregation**: In multi-relational graphs, examine how information flows backward through reverse message-passing mechanisms to ensure messages from ego (query) entities are properly distinguished and correlated.

The technique is particularly valuable for proving **impossibility results** (showing certain functions cannot be computed without additional mechanisms like ego IDs or port numbering) and **sufficiency results** (constructing explicit MPNN architectures that compute desired functions).

---

## Key Equations

### Message Passing at Layer $K$

For an entity $v$ sending a message to an attribute $a$ via edge type $\tau$ at layer 1:

$$\text{msg}^{(1)}(v, a, \tau) = \left(\tau_V(v), \text{ego}_u(v), \tau\right)$$

where:
- $\tau_V(v)$ = type of sender entity $v$
- $\text{ego}_u(v) \in \{0, 1\}$ = indicator that $v$ is the query (ego) entity $u$
- $\tau$ = edge type

### Ego-Type Collection via Aggregation

An attribute $a$ collects the set of edge types through which the ego entity connects:

$$\text{EgoTypes}(a) := \left\{\tau \in T_E : \text{some message into } a \text{ has } \text{ego}_u(v)=1 \text{ and edge type } \tau\right\}$$

### Realizable Aggregation Function

The per-message function that filters messages from ego entities:

$$f\left((\sigma, \text{fl}), \tau\right) = \text{fl} \cdot \mathbf{e}_\tau \in \{0,1\}^{|T_E|}$$

where $\text{fl} = \text{ego}_u(v) \in \{0,1\}$ and $\mathbf{e}_\tau$ is the one-hot encoding of edge type $\tau$. The aggregation sums these vectors: $\sum_{\text{messages}} f(...)$ produces a binary encoding of which edge types carried ego-originated messages.

### Embedding Storage at Layer 1

Each attribute stores:

$$h^{(1)}(a) = \left(\tau_V(a), \text{EgoTypes}(a)\right)$$

---

## Physical Intuition / Derivation

### Why Inductive Aggregation Matters

MPNNs compute functions through **layered message passing**: at each layer $K$, nodes aggregate information from their neighborhood at distance $K$. To understand what *can* be computed, we need to track:

- **What information is available** at layer $K$ (forward direction)
- **What information propagates backward** through reverse edges (cross-attribute correlation)
- **Whether identity is preserved** across different neighborhoods

### The Fundamental Obstacle: Cross-Attribute Identity Correlation

Consider the **Dupr problem**: determine if a given entity $u$ has the same entity $v$ appearing as a predecessor across $r \geq 2$ *different attributes*.

**Local computation alone fails** because:
- Each attribute independently sees edges from $v$ to itself
- Without explicit identity tracking, all same-type entities look identical
- One cannot *correlate* "did entity $v$ appear at attribute $a_1$?" with "did the same entity $v$ appear at attribute $a_2$?"

**Solution via ego IDs**: 
- Tag the query entity $u$ with a special flag (ego ID) that persists through message passing
- When $u$ sends a message to an attribute, that attribute learns "$u$ connects via this edge type"
- Attributes can then share which edge types the ego entity uses, enabling correlation across attributes

### Inductive Structure

The inductive proof has two complementary parts:

**Base case (Layer 0)**: Entities and attributes know only their own type.

**Inductive step (Class-1 entities)**:
Assume entities at layer $K$ have computed aggregations of depth-$K$ neighborhoods. At layer $K+1$, each entity aggregates messages from attributes at layer $K$, which contain the accumulated information about ego connectivity.

**Reverse aggregation (Class-2 entities)**:
When messages flow backward from class-2 entities (attributes) to class-1 entities (entities), the same multiset structure appears:
$$\left\{\left(h^{(k-1)}_{\alpha_j}, \tau_j, 2, j\right) : j = 1, \ldots, r\right\}$$

This establishes that the inductive hypothesis holds at the reverse direction, closing the proof.

---

## Applications in Engineering

### 1. **Graph Neural Network Design & Expressiveness Analysis**
   - Determines which GNN architectures can solve specific graph-based tasks (knowledge graphs, scene graphs, heterogeneous networks)
   - Guides addition of mechanisms (ego embeddings, port numbering) to increase expressiveness

### 2. **Knowledge Graph Completion & Entity Resolution**
   - Used to prove that certain relation patterns (e.g., whether an entity appears multiple times across relations) require explicit identity tracking
   - Informs design of GNNs for multi-hop reasoning and entity linking

### 3. **Typed Graph Databases & Query Optimization**
   - Establishes which first-order logical queries can be answered by neural methods vs. requiring classical database engines
   - Helps determine when to augment query engines with neural layers vs. pure symbolic execution

### 4. **Heterogeneous Information Networks (HINs)**
   - Critical for analyzing tasks on networks with multiple entity and edge types (e.g., academic graphs: authors, papers, venues)
   - Determines expressiveness gaps between different GNN variants

### 5. **Verification & Correctness Certificates**
   - Provides formal proof that a given MPNN architecture is **insufficient