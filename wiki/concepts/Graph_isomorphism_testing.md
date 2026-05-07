# Graph Isomorphism Testing

## Definition

**Graph isomorphism testing** is the problem of determining whether two graphs are structurally identical—that is, whether there exists a bijection between their vertex sets that preserves adjacency relationships. More formally, two graphs $G_1 = (V_1, E_1)$ and $G_2 = (V_2, E_2)$ are isomorphic if there exists a bijection $\phi: V_1 \to V_2$ such that $(u,v) \in E_1$ if and only if $(\phi(u), \phi(v)) \in E_2$.

In the context of neural graph representations, **graph isomorphism testing via message-passing neural networks (MPNNs)** refers to the capability of MPNN architectures to distinguish non-isomorphic graphs or detect specific structural properties (such as cycle participation) through learned node embeddings.

The source material focuses specifically on testing whether nodes participate in cycles of specific length $l$, denoted $\text{Cyc}_l(v)$, using ego-network identifiers and message-passing mechanisms.

## Key Equations

### Cycle Detection via Closed Walks

For a node $v$ on a directed graph, define:
- $\text{Cyc}_l(v)$ = 1 if node $v$ lies on a simple cycle whose length divides $l$; 0 otherwise
- $\text{flag}^{(l)}(v)$ = indicator of whether a closed walk of length $l$ exists from $v$

For functional graphs (where each node has exactly one outgoing edge), these are equivalent.

### Walk Detection Condition

On a cycle of length $c$:
$$\text{flag}^{(l)}(v) = 1 \iff c \mid l$$

where $c \mid l$ denotes "$c$ divides $l$."

For the directed cycle $C_{2l}$ (length $2l$), a walk of length $l$ from node $z_i$ terminates at the antipodal node:
$$z_i^{(l)} = z_{i+l} \neq z_i \quad \Rightarrow \quad \text{flag}^{(l)}(z_i) = 0$$

## Physical Intuition / Derivation

### Why Standard MPNNs Fail

Standard message-passing neural networks compute node embeddings through local aggregation of neighbor features. However, detecting whether a node lies on a cycle of specific length requires:

1. **Forward path propagation**: Information must travel along edges and eventually return to the starting node
2. **Cycle length discrimination**: The mechanism must distinguish cycles of different lengths

On general directed graphs, a key insight emerges: a node can participate in a closed *walk* of length $l$ without lying on a simple *cycle* of that length. For example, a node on a 3-cycle will have closed walks of lengths 3, 6, 9, ... even though it only participates in 3-cycles.

### Role of Ego IDs (Necessity and Sufficiency)

The source material establishes that **ego identifiers** (unique IDs for nodes) are both necessary and sufficient for cycle detection on functional graphs:

- **Necessity**: Without ego IDs, an MPNN cannot distinguish whether a node returns to itself (completing a cycle) or reaches a different node with identical features
- **Sufficiency on functional graphs**: The closing edge of a cycle carries the ego signal back to the starting node through forward aggregation alone—no reverse message passing required

### Why Reverse Message Passing Matters for General Graphs

On general multigraphs without the functional graph constraint, additional adaptations become necessary:

- **Port numbering** (Adaptation 2): Distinguishes between multiple edges between the same pair of nodes
- **Reverse message passing** (Adaptation 1): Enables information to flow backward, necessary because general graph structures may not provide forward paths back to entity nodes
- **Bidirectional communication**: Together with ego IDs, enables universal subgraph pattern detection through unique node identification

## Applications in Engineering

### 1. **Network Topology Verification**
In telecommunications and computer networks, verify that two network configurations are functionally equivalent before deployment, ensuring isomorphic routing structures.

### 2. **Chemical Compound Identification**
In chemistry informatics, test whether two molecular structures represent the same compound despite different drawing conventions (common in SMILES string comparisons and drug discovery pipelines).

### 3. **Anomaly Detection in Cyclic Systems**
In power systems and industrial control networks, detect whether a sensor or component lies on a critical feedback loop by testing cycle participation, flagging nodes that shouldn't be on control cycles.

### 4. **Circuit Design Verification**
In electronic design automation (EDA), verify that optimized circuit netlists are logically equivalent to reference designs—a canonical application of graph isomorphism in CAD tools.

### 5. **Social Network Analysis**
Detect equivalent community structures or role structures within different social networks, identifying isomorphic subgroups that exhibit identical connectivity patterns.

### 6. **Robotics and Motion Planning**
Test whether configuration spaces represented as roadmaps are topologically equivalent, critical for motion planning in manipulators and autonomous systems.

## Common Mistakes / Pitfalls

### 1. **Confusing Walks with Simple Cycles**
The most critical error highlighted in the source material: assuming that detecting closed walks of length $l$ automatically detects simple cycles of length $l$. On general graphs, a node on a 3-cycle will produce false positives for length-6 walks.

**Correct approach**: Use full architectural power (ego IDs + reverse message passing + port numbering) for general graphs; simpler adaptations suffice only on functional graphs.

### 2. **Neglecting the Necessity of Ego IDs**
Trying to perform cycle detection without node identifiers, relying only on structural aggregation. This fails because structurally identical nodes in different locations cannot be distinguished without explicit IDs.

**Fix**: Ensure MPNN architecture includes unique node identifiers passed through message aggregation.

### 3. **Assuming Undirected Graph Methods Work for Directed Graphs**
Cycle detection is fundamentally different in directed graphs (must respect edge direction) versus undirected graphs (bidirectional traversal). Directed cycles can have different functional properties.

### 4. **Ignoring Multigraph Complications**
On multigraphs (multiple edges between node pairs), failing to