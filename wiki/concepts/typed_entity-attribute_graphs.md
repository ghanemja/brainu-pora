# typed entity-attribute graphs

## Definition

A **typed entity-attribute graph** is a multi-relational graph structure used to model entity resolution problems. It consists of:

- **Entity nodes**: partitioned into types (e.g., Person, Company, Product)
- **Attribute nodes**: representing feature values (e.g., addresses, names, identifiers)
- **Typed edges**: connecting entities to their attributes, labeled by attribute type
- **Optional entity-entity edges**: enabling cycle detection and relational patterns

Formally, a typed entity-attribute graph is a tuple $G = (V_e, V_a, E, \tau)$ where:
- $V_e$ = set of entity nodes with type function $\tau_e : V_e \to \mathcal{T}$
- $V_a$ = set of attribute nodes
- $E \subseteq (V_e \times V_a) \cup (V_e \times V_e)$ = edges between entities and attributes, or between entities
- $\tau : E \to \mathcal{A}$ = attribute type labeling function

The graph is **simple** if each entity-attribute pair appears in at most one edge, or **multigraph** if multiple typed edges can connect the same pair.

## Key Predicates and Theorems

### Co-reference Predicates

The family $\text{Dup}_r$ captures entity resolution patterns:

$$\text{Dup}_r(v, G) := \exists u \neq v \text{ with } \tau_e(u) = \tau_e(v) \land |\{a \in V_a : (v,a) \in E \land (u,a) \in E\}| \geq r$$

- **Dup₁**: Two same-type entities share *at least one* attribute value
- **Dup₂, Dup₃, ...**: Two same-type entities share *at least r* attribute values

### Cycle Participation Predicate

$$\text{Cycle}_l(v, G) := v \text{ lies on a cycle of length } l \text{ in the entity-entity subgraph}$$

## Key Equations

**Complexity Gap (Main Finding):**

| Predicate | Required Adaptations | Minimum Depth | Graph Class |
|-----------|---------------------|---------------|-------------|
| Dup₁ | Reverse message passing | 2 | Simple bipartite |
| Dup₂, Dup₃, ... | RMP + Ego IDs | 4 | Simple bipartite |
| Cycle_l | Ego IDs | depends on $l$ | Directed |

**Message Passing Layers:**

- **Dup₁**: $2$ layers (backward pass only)
- **Dup_r** ($r \geq 2$): $4$ layers (requires identity correlation)

## Physical Intuition / Derivation

### Why Dup₁ is "Easy" (Local Computation)

Detecting whether two same-type entities share *any* attribute requires only examining immediate neighbors:

1. **Layer 1**: Each entity collects its attribute neighbors
2. **Layer 2** (reverse): Each attribute backpropagates to all entity neighbors of the same type

If any entity receives a message from the same attribute via reverse edges, a co-reference is detected. This is purely **local** in the graph neighborhood—one hop out and one hop back.

### Why Dup_r (r≥2) is "Hard" (Cross-Attribute Identity Correlation)

Detecting whether the *same entity* appears at *multiple* attributes of a target is fundamentally harder:

```
Target entity v
    |      |      |
    attr₁  attr₂  attr₃
    |      |      |
    ----u----     (same entity u at multiple attributes)
```

The MPNN must verify **identity consistency across attributes**—that the entity backing attr₁ is the *same* entity backing attr₂. Without node IDs, the aggregation function cannot distinguish whether messages come from the same source or different sources. This requires:

- **Ego IDs**: Unique node identifiers so aggregation can track "this message came from node $u$"
- **4 layers**: Extra depth to correlate information across the attribute-entity-attribute path

### Mathematical Barrier

Without ego IDs, any permutation of entities that preserves the graph structure is indistinguishable to the MPNN. Dup_r (r≥2) requires breaking this symmetry by identifying which entity appears repeatedly—necessitating explicit node identity.

## Applications in Engineering

### 1. Data Integration & ETL
- **Deduplication**: Identifying duplicate customer records across CRM systems before merging
- **Graph merging**: Unifying knowledge graphs from multiple sources with typed properties
- **Minimal architecture principle**: Table 4 provides guidance on which GNN adaptations to implement for cost-benefit tradeoff

### 2. Knowledge Graph Completion
- Entity linking in NLP pipelines (e.g., linking mentions to canonical entities)
- Determining when two schema entities represent the same real-world object
- Dup_r predicates formalize the co-reference patterns used in entity disambiguation

### 3. Fraud Detection
- Cycle detection identifies unusual relationship patterns (e.g., circular fund transfers)
- Typed attribute matching reveals accounts sharing suspicious device IDs or IP addresses
- Ego IDs enable tracking persistent fraudster identities across multiple aliases

### 4. Master Data Management (MDM)
- Hierarchical entity resolution with type hierarchies (Person → Customer → VIP)
- Attribute-based blocking strategies: only compare entities sharing rare attribute values
- Guides MPNN architecture design: when is 2-layer sufficient vs. 4-layer required?

### 5. Scientific Data Reconciliation
- Unifying protein/gene databases with typed biological attributes
- Astronomical object catalogues with multi-wavelength observations (attributes of different types)

## Common Mistakes / Pitfalls

### 1. Conflating Graph Simplicity with Computational Simplicity
**Mistake**: Assuming simple bipartite graphs are always amenable to shallow architectures.

**Reality**: Only Dup₁ requires shallow networks on simple graphs. Dup_r (r≥2) provably requires depth 4 even on simple acyclic bipartite graphs.