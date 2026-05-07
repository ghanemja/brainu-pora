# Neighborhood Aggregation

## Definition

**Neighborhood aggregation** is a graph neural network (GNN) mechanism that computes embeddings for nodes by aggregating information from their local neighborhoods. In the context of message-passing neural networks (MPNNs), it is the process by which a node collects, processes, and combines messages or feature representations from its neighboring nodes across one or more hops.

More formally, in a typed entity-attribute graph, **typed neighborhood aggregation** restricts aggregation to neighbors of specific types. For an entity $u$, the **typed neighborhood** is:

$$N_{\text{typed}}(u) = \{(a, \tau') : \exists \text{ edge } (u, a, \tau') \in E\}$$

where $(a, \tau')$ denotes an attribute node $a$ connected via edge type $\tau'$.

In the bipartite entity-attribute setting, neighborhood aggregation occurs across two hops:
1. **Forward aggregation**: entities propagate type information to their attribute neighbors
2. **Reverse aggregation**: aggregated information flows back to entities, allowing detection of shared neighbors among same-typed entities

## Key Equations

### Single-Layer Aggregation (Forward Message Passing)

For a node $u$ at depth $\ell$:

$$h^{(\ell)}(u) = \text{AGG}\left(\left\{h^{(\ell-1)}(v) : v \in N(u)\right\}\right)$$

where $\text{AGG}$ is an aggregation function (e.g., sum, mean, or more complex functions) and $N(u)$ denotes the neighborhood of $u$.

### Typed Neighborhood Aggregation

For reverse message passing in typed graphs:

$$h^{(\ell)}(u) = \text{AGG}_{\text{rev}}\left(\left\{(h^{(\ell-1)}(a), \tau) : (u, a, \tau) \in E\right\}\right)$$

where the aggregation preserves type information $\tau$ alongside attribute embeddings.

### Multiplicity Detection via 2-Hop Aggregation

A node $u$ detects if another same-typed entity shares its neighborhood through:

$$\text{Dup}(u) = \begin{cases} 1 & \text{if } \exists v \neq u : \tau_V(v) = \tau_V(u) \text{ and } N_{\text{typed}}(u) \cap N_{\text{typed}}(v) \neq \emptyset \\ 0 & \text{otherwise} \end{cases}$$

This requires exactly **2 layers** of message passing (forward + reverse) on bipartite entity-attribute graphs.

## Physical Intuition / Derivation

### Why Neighborhood Aggregation Works

Neighborhood aggregation exploits the **locality principle**: the features and relationships of nearby nodes are informative for predicting properties of a target node. Rather than maintaining a full graph embedding, only local neighborhoods need to be processed, making the algorithm **scalable and interpretable**.

### The 2-Hop Necessity (Depth Minimality)

Consider the duplicate detection problem in entity resolution:

**Layer 0 (Initialization):** Each entity $u$ has its attribute type $\tau_V(u)$ and each attribute $a$ has its incoming entity types.

**Layer 1 (Forward Aggregation):** Entities send their type information to attributes. Each attribute $a$ now has a multiset of entity types: $\{\tau_V(v) : (v, a, \tau) \in E\}$. However, entity $u$ at this stage only sees its own typed neighborhood $N_{\text{typed}}(u)$ in its embedding $h^{(1)}(u)$—no information about *other* entities' neighbors.

**Layer 2 (Reverse Aggregation):** Attributes send back their aggregated entity-type information. Now entity $u$ can compare: if two same-typed entities share an attribute neighbor, the reverse messages will reveal that multiple entities of the same type visited the shared attribute. This comparison is **impossible with only 1 layer** because no information about competing entities reaches $u$.

**Counterexample (Separation Graphs):** Consider two graphs $G_1$ and $G_2$:
- $G_1$: Entities $u, v$ (same type), both connect to attribute $a$ via edge $\tau_1$. Result: $\text{Dup}(u) = 1$ (duplication detected)
- $G_2$: Only entity $u$ connects to $a$. Result: $\text{Dup}(u) = 0$ (no duplication)

After layer 1, both entities have identical embeddings because $N_{\text{typed}}(u) = \{(a, \tau_1)\}$ in both cases. **The distinction requires layer 2.**

## Applications in Engineering

### 1. **Master Data Management (MDM)**
Entity deduplication in master data pipelines. When patient records from multiple sources are ingested without consolidation, neighborhood aggregation detects when multiple records share attribute neighbors (providers, addresses), indicating likely duplicates.

### 2. **Graph-Based Recommendation Systems**
User-item bipartite graphs benefit from 2-hop aggregation: recommend items liked by users similar to the target user by aggregating information through user-item neighborhoods.

### 3. **Knowledge Graph Completion**
Predicting missing edges in heterogeneous knowledge graphs by aggregating type-specific neighborhoods to infer relationships.

### 4. **Financial Crime Detection**
In directed multigraphs (e.g., transaction networks with 17.92 edges per node pair on average), neighborhood aggregation identifies suspicious patterns by detecting entities with abnormally high shared connections to intermediary nodes.

### 5. **Molecular Property Prediction**
Atom-level predictions in chemistry leverage neighborhood aggregation over bonded atoms; 2-hop aggregation captures effects of atom environments at extended distances.

## Common Mistakes / Pitfalls

### 1. **Confusing Information Flow**
Students often assume that 1-layer aggregation is sufficient for any task. **Reality:** Tasks requiring comparison of neighborhoods (e.g., duplicate detection) inherently need at least 2 layers. Test with the separation graphs $G_1$ and $G_2$—they