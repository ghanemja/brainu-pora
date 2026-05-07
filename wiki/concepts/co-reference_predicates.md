# co-reference predicates

## Definition

**Co-reference predicates** are a family of graph-theoretic predicates, denoted $\text{Dupr}$, that capture the evidence pattern: *"two entities of the same type share at least $r$ attribute values."*

More formally, given a typed entity-attribute bipartite graph $G = (E \cup A, E_{\text{edge}})$ where:
- $E$ is a set of entity nodes, partitioned by type
- $A$ is a set of attribute value nodes
- $(e, a) \in E_{\text{edge}}$ if entity $e$ references attribute value $a$

The predicate $\text{Dupr}(e_1, e_2)$ evaluates to **true** if and only if:
$$|\{a \in A : (e_1, a) \in E_{\text{edge}} \land (e_2, a) \in E_{\text{edge}} \land \text{type}(e_1) = \text{type}(e_2)\}| \geq r$$

That is, entities $e_1$ and $e_2$ of the same type point to at least $r$ common attribute values.

The **co-reference predicate hierarchy** consists of:
- $\text{Dup1}$: two same-type entities share **at least 1 attribute** (detecting any overlap)
- $\text{Dup2}$: two same-type entities share **at least 2 attributes** (detecting multiple overlap)
- $\text{Dupr}$: generalization to threshold $r$

## Key Equations

### Predicate Definition
$$\text{Dupr}(e_1, e_2) := |\text{Common}(e_1, e_2)| \geq r$$

where the common attribute set is:
$$\text{Common}(e_1, e_2) = \{a \in N(e_1) : a \in N(e_2)\}$$

and $N(e)$ denotes the neighborhood of entity $e$ in the attribute layer.

### MPNN Expressivity Lower Bound
For $\text{Dup1}$ (single shared attribute), the minimum depth required is:
$$d_{\min}(\text{Dup1}) = 2$$
(with reverse message passing)

For $\text{Dupr}$ with $r \geq 2$ (multiple shared attributes), the sharp lower bound is:
$$d_{\min}(\text{Dupr}) = 4$$
(requiring ego IDs and bidirectional message passing)

### Architectural Necessity Theorem
An MPNN architecture can compute $\text{Dupr}$ if and only if it satisfies:
- For $r = 1$: reverse message passing (RMP) in 2 layers suffices
- For $r \geq 2$: ego IDs + RMP + port numbering in 4 layers are necessary and sufficient

## Physical Intuition / Derivation

### Why $\text{Dup1}$ is "Easy" (2 layers, local)

To detect if two entities share *any* attribute, each attribute node independently broadcasts:
1. **Layer 1 (forward)**: Each entity sends its identity to all attributes it references
2. **Layer 2 (reverse)**: Each attribute checks if two distinct same-type entities reference it, and signals this back to both

The computation is **purely local** to individual attributes—no global coordination needed. Think of it as: *"Can attribute $a$ see both $e_1$ and $e_2$?"* This requires only asking neighbors' neighbors, well within a depth-2 MPNN.

**Separation example**: Consider two entity pairs:
- Pair A: entities $e_1, e_2$ sharing attribute $a_1$ only
- Pair B: entities $e_1', e_2'$ with no shared attributes

A 1-layer MPNN cannot distinguish these (it only sees immediate neighborhoods).

### Why $\text{Dupr}$ ($r \geq 2$) is "Hard" (4 layers, requires ego IDs)

Detecting multiple shared attributes requires **cross-attribute identity correlation**: verifying that the *same* entity appears at multiple distinct attributes of the target.

1. **Layers 1-2 (forward+reverse)**: Broadcast which attributes are common
2. **Layers 3-4 (with ego IDs)**: Track entity identity across multiple attribute references to confirm it's the same source entity appearing multiple times

Without ego IDs, an MPNN loses persistent node identity in aggregation steps and cannot distinguish:
- Entity $e_1$ independently sharing attributes $a_1$ and $a_2$ with $e_2$ ✓
- Some other entity $e_1'$ sharing only $a_1$, and yet another entity $e_1''$ sharing only $a_2$ ✗

**Separation instance** (acyclic bipartite graph):
```
e₁ ─────→ a₁ ←───── e₂
 └──────→ a₂ ←────┘
```
vs. two separate shared-attribute pairs on disjoint attributes.

Any depth-3 MPNN without ego IDs will confuse these structures; depth-4 with ego IDs can distinguish them by tracking which entity identity flows through multiple aggregations.

## Applications in Engineering

### 1. **Master Data Management (MDM)**
Entity resolution is the core problem in consolidating customer records across fragmented databases:
- **CRM consolidation**: Identify duplicate customer accounts (sharing email, phone, address)
- **Supplier databases**: Merge purchase orders referring to the same vendor (company name variants, multiple SKUs)
- Practitioners use $\text{Dup2}$ or $\text{Dup3}$ as matching criteria (require 2-3 shared attributes for confidence)

### 2. **Knowledge Graph Construction**
Disambiguating entities from noisy sources (web tables, reviews, knowledge bases):
- **Person linking**: Cross-reference records sharing both name and organization
- **Product deduplication**: Match SKUs sharing multiple attribute values (brand, model, category)
- The expressivity hierarchy guides which GNN architectural features are necessary for a given matching threshold

### 