# Directed Multigraph

## Definition

A **directed multigraph** is a mathematical structure for representing systems with multiple types of relationships between entities. Formally, a typed directed multigraph is defined as a tuple:

$$G = (V, E, \text{src}, \text{dst}, T_V, T_E, \tau_V, \tau_E)$$

where:

- **$V$**: a finite set of vertices (nodes)
- **$E$**: a finite multiset of edges (allowing multiple edges between the same pair of vertices)
- **$\text{src}, \text{dst}: E \to V$**: source and destination functions mapping each edge to its endpoints
- **$T_V, T_E$**: sets of allowable vertex and edge types
- **$\tau_V: V \to T_V$**: vertex type assignment function
- **$\tau_E: E \to T_E$**: edge type assignment function

The key distinction from simple directed graphs is that:
1. **Multiple edges** between the same pair of vertices are permitted (multigraph property)
2. **Edge types** distinguish relationships semantically (typed property)
3. **Direction** is explicit: edges have defined source and destination nodes

### Predecessor and Successor Sets

For a node $v \in V$:
- **In-neighbors**: $N^{\text{in}}(v) = \{u \in V : \exists \tau \in T_E \text{ s.t. } (u, v, \tau) \in E\}$
- **Out-neighbors**: $N^{\text{out}}(v) = \{u \in V : \exists \tau \in T_E \text{ s.t. } (v, u, \tau) \in E\}$
- **Multi-edge representation**: Multiple edges $(u, v, \tau_1), (u, v, \tau_2), \ldots$ with different types are all retained

## Key Equations

### Message Passing Neural Network on Directed Multigraphs

For a depth-$K$ MPNN, embeddings are computed iteratively:

**Initialization:**
$$h^{(0)}(v) = \text{EMBED}(\tau_V(v), \mathbf{x}_v)$$

where $\mathbf{x}_v$ denotes input features and $\text{EMBED}$ encodes node type information.

**Aggregation (layer $k$):**
$$a^{(k)}_{\text{in}}(v) = \text{AGG}^{(k)}_{\text{in}} \left\{\!\!\left\{(h^{(k-1)}(u), \tau) : (u, v, \tau) \in E\right\}\!\!\right\}$$

The double-brace notation $\{\!\!\{\cdot\}\!\!\}$ denotes a multiset, preserving multiplicity of distinct $(u, \tau)$ pairs.

**Update (layer $k$):**
$$h^{(k)}(v) = \text{UPDATE}^{(k)}\left(h^{(k-1)}(v), a^{(k)}_{\text{in}}(v)\right)$$

**Readout:**
$$\hat{y}(v) = \text{READOUT}\left(h^{(K)}(v)\right)$$

### Aggregation Functions

Common permutation-invariant aggregation functions include:
- **Sum**: $\text{AGG}^{(k)}_{\text{in}} = \sum_{(u,\tau)} (h^{(k-1)}(u), \tau)$
- **Mean**: $\text{AGG}^{(k)}_{\text{in}} = \frac{1}{|E_{\text{in}}|} \sum_{(u,\tau)} (h^{(k-1)}(u), \tau)$
- **Max**: $\text{AGG}^{(k)}_{\text{in}} = \max_{(u,\tau)} (h^{(k-1)}(u), \tau)$ (element-wise)

## Physical Intuition / Derivation

### Why Multiple Edges and Types Matter

In real engineering systems, relationships between entities are rarely binary. Consider a circuit network:
- Two components may be connected by **multiple wire types** (signal, ground, power)
- These carry **distinct semantic information**—a simple directed graph loses this distinction

A directed multigraph naturally encodes:
1. **Relationship diversity**: Different edge types represent qualitatively different connections
2. **Redundancy and parallel paths**: Multiple edges between nodes model parallel transmission channels
3. **Type-specific behavior**: Node updates can depend on which edge types carry which information

### Connection to Graph Isomorphism Testing

The 1-Weisfeiler–Leman (1-WL) test iteratively refines node labels based on local neighborhoods:

$$l_t(v) = f\left(l_{t-1}(v), \left\{\!\!\{l_{t-1}(w) : w \in N(v)\}\!\!\right\}\right)$$

where $f$ is an injective hash function. The MPNN update rule directly parallels this:
- **Aggregation** corresponds to gathering the multiset of neighbor labels
- **Update** is a continuous, learnable analogue of label refinement
- **Permutation invariance** ensures the aggregation depends only on the multiset, not ordering

**Key insight**: MPNNs on directed multigraphs are at most as expressive as 1-WL testing—they cannot distinguish graphs that 1-WL cannot, and can distinguish many (but not necessarily all) graphs that 1-WL can.

## Applications in Engineering

### 1. **Circuit Design and Netlist Analysis**
- **Nodes**: circuit components (gates, resistors, capacitors)
- **Edge types**: signal connections, ground, power supply, control signals
- **Application**: Learning circuit properties (timing, power consumption) from topology; predicting parasitic effects

### 2. **Software Dependency Networks**
- **Nodes**: software modules or packages
- **Edge types**: function calls, data dependencies, version constraints, inheritance
- **Application**: Detecting circular dependencies, predicting breaking changes, code quality analysis

### 3. **