# Bipartite graph detection

## Definition

**Bipartite graph detection** is the computational problem of determining whether a graph $G = (V, E)$ contains a complete bipartite subgraph $K_{m,n}$ (a bipartite clique with $m$ nodes in one partition and $n$ in the other). More generally, it encompasses:

1. **Recognition**: Determining if a graph is bipartite (2-colorable)
2. **Subgraph detection**: Finding or detecting specific bipartite structures like $K_{2,r}$ (complete bipartite graphs)
3. **Structural analysis**: Understanding the bipartite properties of entity-attribute graphs where edges flow in one direction (entities → attributes)

In the context of **Message-Passing Neural Networks (MPNNs)**, bipartite graph detection refers to the expressiveness limitations and architectural requirements needed for MPNNs to reliably detect bipartite substructures.

## Key Equations

### Graph Bipartiteness Condition

A graph $G = (V, E)$ is bipartite if and only if it contains no odd cycles. Equivalently, vertices can be partitioned into sets $V_1$ and $V_2$ such that:

$$\forall (u, v) \in E: (u \in V_1 \land v \in V_2) \lor (u \in V_2 \land v \in V_1)$$

### Complete Bipartite Graph $K_{m,n}$

$$K_{m,n} = (V_1 \cup V_2, E), \quad |V_1| = m, |V_2| = n, \quad E = V_1 \times V_2$$

For $K_{2,r}$ detection, we seek subgraphs with 2 nodes on one side and $r$ on the other.

### MPNN Computational Complexity

**Without ego IDs** (per layer):
$$T_{\text{forward}} = O(|E|)$$

**With ego IDs** (per layer):
$$T_{\text{with ego IDs}} = O(|V| \cdot |E|)$$

This represents an unavoidable $O(|V|)$ multiplicative overhead for detecting $K_{2,r}$ structures where $r \geq 2$.

## Physical Intuition / Derivation

### Why Bipartite Graphs Matter for Neural Graph Algorithms

Consider an **entity-attribute graph** where:
- Entity nodes $\mathcal{E}$ (e.g., users, products)
- Attribute nodes $\mathcal{A}$ (e.g., tags, properties)
- Edges flow unidirectionally: $\mathcal{E} \to \mathcal{A}$

This enforces **no incoming edges to entities**: $N_{\text{in}}(u) = \emptyset$ for all $u \in \mathcal{E}$.

### The Core Expressive Limitation

Standard **forward aggregation** in MPNNs aggregates messages from outgoing neighbors:

$$h_v^{(k+1)} = \text{AGGREGATE}\left(\{h_u^{(k)} : u \in N_{\text{out}}(v)\}\right)$$

In entity-attribute graphs, entity nodes have no incoming edges. Therefore:
- Entity embeddings receive **no graph-structural information** from any depth of forward aggregation
- Without **reverse message passing** (aggregating from incoming neighbors), the network cannot distinguish between structurally different entities

### Symmetry Breaking Mechanisms

Three architectural additions are required:

1. **Reverse Message Passing**: Aggregates from incoming neighbors $N_{\text{in}}(v)$, essential for entity-attribute architectures
2. **Port Numbering**: Distinguishes edges by type/direction in directed multigraphs
3. **Ego IDs**: Assigns unique identifiers to nodes within the same structural class

**Theorem 8 (Informal)**: For $K_{2,r}$ detection with $r \geq 2$, port numbering alone induces a two-class partition of entities where nodes within each class remain indistinguishable. Ego IDs break this class-level symmetry by providing absolute identity information independent of graph structure.

### Weisfeiler-Leman (1-WL) Analogy

The indistinguishability results mirror classical **1-WL color refinement** failures:
- Nodes with identical multisets of neighbor colors remain indistinguishable
- In $d$-regular graphs, all nodes receive identical multisets indefinitely
- **Port numbering + ego IDs** extend expressivity beyond 1-WL, but this extension is necessary and non-trivial for bipartite subgraph detection

## Applications in Engineering

### 1. **Knowledge Graph Completion**
Entity-attribute bipartite graphs represent (entity, property, value) triples. Detecting bipartite substructures helps identify:
- Fraud rings (users with suspiciously identical attribute patterns)
- Recommendation anomalies
- Missing links in incomplete knowledge bases

### 2. **Anomaly Detection in Networked Systems**
Bipartite structures appear in:
- **Bank transaction networks**: (account, merchant) pairs; detecting $K_{2,r}$ reveals coordinated fraud
- **Network intrusion detection**: (internal host, external IP) connections; structured patterns indicate advanced persistent threats
- **Supply chain networks**: (supplier, buyer) relationships

### 3. **Biological Network Analysis**
Bipartite graphs model:
- Protein-protein interaction networks with typed interactions
- Gene-disease associations
- Metabolic networks (substrate-enzyme pairs)

Detecting structured bipartite subgraphs identifies functional modules.

### 4. **Social Network Analysis**
- **Coordinated inauthentic behavior**: Multiple accounts (entities) interacting with identical target accounts (attributes)
- **Influence cascades**: Following patterns in follower-followee bipartite structures
- **Community detection**: Bipartite community structure (users-content, authors-citations)

### 5. **Graph Neural Network Design**
Understanding bipartite graph detection requirements informs:
- **Heterogeneous GNN architecture** (distinguishing entity types requires ego IDs)
- **Computational budget allocation** (forward-only vs. reverse+forward passes)
- **Expressivity trade