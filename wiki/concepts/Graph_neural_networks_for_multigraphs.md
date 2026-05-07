# Graph Neural Networks for Multigraphs

## Definition

**Graph Neural Networks for Multigraphs** are neural architectures designed to operate on multigraphs—graphs where multiple edges of potentially different types can exist between the same pair of nodes. Unlike simple graphs (at most one edge per node pair), multigraphs require special handling to:

1. **Distinguish parallel edges** from multiple distinct sources
2. **Preserve edge type information** through message passing
3. **Count distinct sources** rather than aggregate edge multiplicities naively

**Typed Entity-Attribute Graphs** are a canonical multigraph structure with two node classes:
- **Entities**: nodes representing objects (e.g., database records)
- **Attributes**: nodes representing property values
- **Edges**: directed, labeled by type $\tau \in T$, connecting entities to attributes (and vice versa via reverse edges)

**Port numbering** is a critical adaptation for multigraphs: assigning unique integer labels to edges incident to each node. This allows the network to distinguish:
- **Incoming ports**: which source node sent each edge
- **Outgoing ports**: which target node receives each edge (less essential)

## Key Equations

### Message Passing with Reverse Aggregation

Standard MPNN reverse message passing at layer $\ell$ for entity $u$:

$$h_u^{(\ell)} = \text{AGG}\left( \left\{ \text{MSG}^{(\ell)}(h_a^{(\ell-1)}, \tau) : a \in N_\tau^{\text{rev}}(u) \right\} \right)$$

where:
- $N_\tau^{\text{rev}}(u)$ = attributes connected to $u$ via reverse edges of type $\tau$
- $\text{MSG}^{(\ell)}$ = message function incorporating attribute embeddings
- $\text{AGG}$ = aggregation function (typically sum, mean, or max)

### Port-Numbered Forward Aggregation

At attribute $a$, counting distinct entity sources with incoming port numbers:

$$h_a^{(\ell)} = \text{AGG}\left( \left\{ h_u^{(\ell-1)} : (u, a) \in E_\tau, \text{incoming\_port}(u,a) \neq \text{incoming\_port}(u',a) \text{ for } u \neq u' \right\} \right)$$

This ensures **parallel edges from the same entity share a port**, while **edges from different entities receive distinct ports**.

### K₂,ᵣ Co-reference Predicate

The core expressiveness question: can an MPNN detect when two entities of the same type share $r$ distinct typed attribute values?

$$K_{2,r}(u,v) = \left| \{ a : \exists \tau \in T, (u,a,\tau) \in E \land (v,a,\tau) \in E \land \text{distinct}(u,v) \} \right| \geq r$$

## Physical Intuition / Derivation

### Why Multigraphs Break Simple MPNN Designs

In a **simple graph** (at most one edge per node pair), the multiplicity of aggregated messages directly equals the number of distinct neighbors. But in a **multigraph**:

- A single entity $u$ might send 10 parallel edges (all of type $\tau_1$) to attribute $a$
- A MPNN without port information cannot distinguish: "Did 10 different entities send one edge each, or did one entity send 10 edges?"
- This breaks algorithms that rely on counting distinct sources—like detecting shared attributes

### Two-Layer Necessity for Dup Detection

The **Dup(u)** predicate asks: "Are there two attributes that share all the same entity-to-attribute connections as $u$?"

**Why two layers are necessary:**

1. **Layer 0 (initialization)**: Nodes encode only their type information
2. **Layer 1 (reverse aggregation)**: Entities receive messages from attributes, but these messages carry only layer-0 attribute type data. The crucial information—*how many distinct entities* connect to each attribute—hasn't been computed yet.
3. **Layer 1 (forward aggregation)**: Attributes aggregate over entities and count distinct sources. They learn: "I have 3 distinct entity sources of type $\sigma$."
4. **Layer 2 (reverse aggregation)**: Entities finally receive this fan-in information and can compare whether two attributes have the same source patterns.

This is an **information-flow bottleneck**: distinct-source counts cannot be computed in fewer than 2 layers because they require aggregation at attributes (layer 1) before being communicated back to entities (layer 2).

### Port Numbering as a Multigraph Adapter

**Incoming port numbering** plays the analogous role to **simplicity** on simple graphs:

| Property | Simple Graph | Multigraph + Incoming Ports |
|----------|--------------|---------------------------|
| Edge multiplicity | Always ≤ 1 | Arbitrary |
| Source distinctness | Implicit in topology | Restored via port assignment |
| Minimal information needed | Edge presence | Edge presence + source identity |

By the **port adaptation**, parallel edges from entity $u$ to attribute $a$ (even if there are 100 of them) all receive the same incoming port at $a$. Different entities get different ports. This **decouples edge count from source count**.

## Applications in Engineering

### 1. Knowledge Graph Completion & Entity Linking
- **Problem**: Database records may be linked via multiple relations (co-author, cited-by, same-institution)
- **Solution**: Typed entity-attribute GNNs detect when records share multiple relation types, enabling deduplication and entity resolution
- **Benefit**: Incoming port numbering ensures "5 co-authorships between A and B" doesn't get confused with "A and B plus 3 other co-authors"

### 2. Relational Database Integrity
- **Problem**: Verify whether two records should be merged based on shared attribute values
- **Solution**: K₂,ᵣ detection identifies records sharing ≥r distinct attributes
- **Benefit**: Minimal 2-layer architecture ensures computational efficiency on large schemas

### 3. Fraud Detection in Financial Networks
- **Problem