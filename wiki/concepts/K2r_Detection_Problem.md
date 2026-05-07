# K2,r Detection Problem

## Definition

The **K₂,ᵣ detection problem** is a binary node classification task in typed entity-attribute graphs used to identify potential duplicate entities in master data management (MDM) systems.

Given a typed entity-attribute graph $G = (E, A, T, E)$ where:
- $E$ = set of entity nodes
- $A$ = set of attribute nodes  
- $T_E$ = set of entity types
- $\mathcal{E}$ = set of typed edges $(u, a, \tau)$ with $u \in E$, $a \in A$, $\tau \in T_E$

Two entities $u$ and $v$ of the same type are flagged as potential duplicates if they share at least $r$ common typed attributes (typed neighbors connected via the same edge types).

### Formal Specification

For each entity $u \in E$, define the **typed neighborhood**:
$$N_{\text{typed}}(u) = \{(a, \tau) \in A \times T_E : (u, a, \tau) \in \mathcal{E}\}$$

The detection function is:
$$\text{Dup}_r(u) = \begin{cases} 
1 & \text{if } \exists v \in E \setminus \{u\}, \, \tau_V(v) = \tau_V(u), \, |N_{\text{typed}}(u) \cap N_{\text{typed}}(v)| \geq r \\
0 & \text{otherwise}
\end{cases}$$

where $\tau_V(u)$ denotes the entity type of node $u$.

When $r=1$, this is abbreviated as $\text{Dup}(u)$.

---

## Key Equations

**Typed Neighborhood Intersection Condition:**
$$|N_{\text{typed}}(u) \cap N_{\text{typed}}(v)| = |\{(a, \tau) : (u, a, \tau) \in \mathcal{E} \text{ and } (v, a, \tau) \in \mathcal{E}\}|$$

This counts shared (attribute, edge-type) pairs between entities of matching types.

**Multi-graph Variant:**
When comparing graphs $G_1$ and $G_2$ (e.g., in separation arguments):
$$\text{Dup}_{r,G}(u) = \begin{cases} 
1 & \text{if } \exists v, \, |N_{\text{typed}}^G(u) \cap N_{\text{typed}}^G(v)| \geq r \\
0 & \text{otherwise}
\end{cases}$$

---

## Physical Intuition / Derivation

### Why Type Constraints Matter

The same-type constraint $\tau_V(u) = \tau_V(v)$ ensures semantic meaningfulness. A Person and an Organization cannot be duplicates regardless of shared attributes—they represent fundamentally different entity categories. This mirrors real-world MDM: duplicate detection operates within schema-defined classes.

### Strength of Evidence via Threshold $r$

The parameter $r$ creates a **confidence spectrum**:

- **$r=1$ (weak evidence):** Two Person records sharing a single phone number may be coincidental (family members, shared business lines). High false-positive risk.

- **$r=2$ (moderate evidence):** Two records sharing both email *and* phone number indicates stronger alignment. Combined attribute uniqueness reduces random collisions.

- **$r \geq 3$ (strong evidence):** Sharing multiple attribute types (email + phone + address) becomes increasingly unlikely by chance.

**Key insight:** The jump from $r=1$ to $r=2$ is not merely a quantitative increase—it qualitatively changes the computational complexity. Detecting $K_{2,1}$ (bipartite graphs with one entity paired to multiple attributes) is simpler than detecting $K_{2,2}$ (requiring matching on attribute pairs), demanding more expressive graph neural network architectures.

### Graph-Theoretic Perspective

The name "$K_{2,r}$" references the **complete bipartite graph** $K_{2,r}$: a structure with 2 entity nodes connected to $r$ shared attribute nodes. The detection problem asks: *"Do entities $u$ and $v$ form a $K_{2,r}$ structure in the attribute subgraph?"*

---

## Applications in Engineering

### 1. **Master Data Management (MDM)**
Production databases accumulate duplicate customer/supplier records through:
- Manual entry variations (John vs. Jon Smith)
- System migrations merging disparate databases
- CRM platforms with inconsistent data entry

K₂,ᵣ detection enables automated duplicate flagging with tunable precision via $r$.

### 2. **Data Integration Pipelines**
When merging data from multiple sources:
- Source A: Customer {email: alice@corp.com, phone: 555-0100}
- Source B: Customer {email: alice@corp.com, phone: 555-0100, address: "123 Main St"}

Setting $r=2$ flags this as a probable duplicate before merge operations.

### 3. **Graph Neural Network (GNN) Expressiveness Benchmarking**
The K₂,ᵣ problem serves as a **complexity benchmark** for GNN architectures:
- Standard Message-Passing Neural Networks (MPNNs) solve $r=1$ efficiently
- $r \geq 2$ requires higher-order architectures (e.g., subgraph isomorphism modules, higher-dimensional Weisfeiler-Lehman tests)
- Drives design of more powerful GNN variants

### 4. **Financial Crime Detection**
Banks flag suspicious accounts sharing:
- Same phone number ($r=1$): possible shared device
- Same email + phone ($r=2$): probable fraud ring
- Same email + phone + address ($r=3$): coordinated criminal operation

### 5. **Supply Chain Integrity**
Manufacturing: detect duplicate supplier records that might indicate:
- Shell companies masquerading as multiple vendors
- Price manipulation schemes

---

## Common Mistakes / Pitfalls

### 1. **Ignoring Edge Type Diversity**
❌