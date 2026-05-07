# Information Flow in Neural Networks

## Definition

**Information flow** in neural networks refers to the propagation and transformation of data (node features, embeddings, aggregated messages) through network layers, and the fundamental constraints on *what information becomes available at which nodes and at which layer*.

In the context of message-passing neural networks (MPNNs), information flow describes:

1. **Forward flow**: Aggregation of neighbor information into node representations (bottom-up)
2. **Reverse flow**: Back-propagation of computed node properties to neighbor sources (top-down)
3. **Information availability**: The set of graph structures and properties that can be reliably computed at a given depth and architecture

A critical insight is that information flow is **depth-limited**: features computed at layer $\ell$ are only available for aggregation at layer $\ell+1$. This creates a fundamental **information-flow bottleneck** that may require deeper networks to solve certain problems.

## Key Equations

### Information Availability Timeline

For a graph problem requiring detection of a property $P$ at node $u$:

$$\text{Available}_{\ell}(u) = \text{Aggregate}(\text{Available}_{\ell-1}(\text{neighbors}(u)))$$

where:
- $\ell = 0$: Only node attributes/types
- $\ell = 1$: Aggregated neighbor attributes  
- $\ell = 2$: Aggregated neighbor aggregations (second-order neighborhoods)
- $\ell \geq k$: Requires $k$ hops to propagate information from source nodes to $u$

### Multiplicity Counting (Port Numbering Compensation)

On multigraphs, the raw message multiplicity $m_a$ (number of messages arriving at attribute $a$) satisfies:

$$m_a = \sum_{v \in V} c(v \to a)$$

where $c(v \to a)$ is the multiplicity of edges from entity $v$ to attribute $a$. Without port numbering, we lose the ability to distinguish $c(v \to a) > 1$ from multiple distinct sources.

With **incoming port numbering** (Adaptation 2a):
- Edges from distinct entities receive distinct incoming port indices
- Parallel edges from the same entity share identical ports
- This restores: $|\text{distinct sources to } a| = |\{\text{distinct incoming ports at } a\}|$

## Physical Intuition / Derivation

### Why Depth Matters: The Dup Problem

Consider detecting whether an entity $u$ has a **duplicate attribute** (i.e., $\text{Dup}(u) = 1$ iff $u$ connects to multiple entities sharing a common attribute).

**Layer 0:** Each attribute $a$ knows only:
- Its own type (e.g., $\alpha_1$)
- No information about which entities reach it

**Layer 1 (Reverse messages):** Entity $u$ receives reverse messages from attributes, but these messages only carry layer-0 information:
- Message from $a$: "I am type $\alpha_1$"
- Entity $u$ cannot yet distinguish: *how many distinct entity neighbors contribute to each attribute?*

**Layer 2 (Forward aggregation, then Reverse):** 
- Layer 1 forward pass: Each attribute $a$ aggregates its entity predecessors, computing the **fan-in** (number of distinct entity sources)
- Layer 2 reverse pass: This fan-in information propagates back to entities
- Now entity $u$ can observe: "Attributes $a_1$ and $a_3$ both have fan-in $\geq 2$ and type $\alpha_1$" → $\text{Dup}(u) = 1$

**Necessity of two layers**: After layer 1, entity $u$ lacks the aggregated fan-in statistics that layer-1 forward aggregation computes. This is a **fundamental information-flow constraint**, not an architectural limitation.

### Port Numbering as Multigraph Adaptation

On **simple graphs** (at most one edge per type between any pair):
- Edge multiplicity = distinct source count automatically

On **multigraphs** (parallel edges allowed):
- Parallel edges from one entity inflate raw multiplicity without indicating multiple sources
- Incoming port numbering compensates by encoding the equivalence class of parallel edges

This makes incoming port numbering the **minimal sufficient adaptation** for multigraphs, analogous to how the simplicity assumption eliminates ambiguity on simple graphs.

### K2,r Detection Hardness

The $K_{2,r}$ co-reference predicate requires: *two entities of the same type share at least $r$ distinct typed attribute values*.

- **$K_{2,1}$ (Theorem 3):** Solvable with only reverse message passing (depth 2)
  - One duplicate attribute suffices; information about distinct sources flows in one reverse pass

- **$K_{2,r}$ for $r \geq 2$ (Theorem 5):** Requires **ego IDs** (node identifiers) even on simple graphs
  - Multiple shared attributes must be **correlated** to the same entity pair
  - Without ego IDs, nodes cannot distinguish "entity $v_1$ shares attributes $\{a_1, a_2\}$ with $u$" from "$v_1$ shares $\{a_1\}$ and $v_2$ shares $\{a_2\}$"
  - Ego IDs allow breaking symmetry and binding information to specific entity pairs

## Applications in Engineering

### 1. Graph Neural Network Architecture Design
- **Depth selection**: Problems requiring detection of $k$-hop correlations need at least $k+1$ layers
- **Reverse message passing**: Essential when aggregation must happen on attribute (or hidden) nodes before propagating back to entity nodes
- **Bidirectional MPNNs**: Design justified by information-flow necessity, not just empirical preference

### 2. Knowledge Graph Completion & Entity Resolution
- Detecting duplicate/co-referent entities in knowledge graphs requires layered aggregation
- **Port numbering in relational systems**: When multiple relations of the same type connect to the same target, port numbers distinguish parallel edges—critical for counting distinct sources
- Applications: deduplication in databases, entity linking in NLP

### 3. Graph-Based Recommender Systems
- User-item-attribute graphs benefit from