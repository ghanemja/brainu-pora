# Binary Node Classification

## Definition

**Binary Node Classification** is the task of assigning each node in a graph to one of two discrete classes (typically labeled 0 or 1). In the context of entity resolution and duplicate detection, it determines whether each entity node belongs to the class of "duplicates" or "non-duplicates" based on graph structure and attribute sharing.

Formally, given a graph $G = (V, E)$ where $V$ is a set of nodes, a binary node classification task assigns a binary label $y_u \in \{0, 1\}$ to each node $u \in V$ according to some criterion $\mathcal{C}(u)$.

In the **duplicate entity detection** problem, the classification criterion is based on shared attributes:

$$\text{Dup}_r(u) = \begin{cases} 
1 & \text{if } \exists v \in E \setminus \{u\} : \tau_V(u) = \tau_V(v) \text{ and } |\mathcal{N}_{\text{typed}}(u) \cap \mathcal{N}_{\text{typed}}(v)| \geq r \\
0 & \text{otherwise}
\end{cases}$$

where:
- $\tau_V(u)$ is the type of entity $u$ (e.g., "Person", "Organization")
- $\mathcal{N}_{\text{typed}}(u) = \{(a, \tau) \in A \times T_E : (u, a, \tau) \in E\}$ is the **typed neighborhood** of $u$—the set of (attribute node, edge type) pairs connected to $u$
- $r$ is a threshold parameter controlling the strength of evidence required to flag a duplicate
- The intersection $|\mathcal{N}_{\text{typed}}(u) \cap \mathcal{N}_{\text{typed}}(v)|$ counts shared typed attributes between entities

## Key Equations

**Typed Neighborhood Definition:**
$$\mathcal{N}_{\text{typed}}(u) = \left\{(a, \tau) \in A \times T_E : (u, a, \tau) \in E\right\}$$

**General K₂,ᵣ Detection Problem (r-strength duplicate detection):**
$$\text{Dup}_{r,G}(u) = \begin{cases} 
1 & \text{if } \exists v \neq u : \tau_V(u) = \tau_V(v) \text{ and } |\mathcal{N}_{\text{typed}}(u) \cap \mathcal{N}_{\text{typed}}(v)| \geq r \\
0 & \text{otherwise}
\end{cases}$$

**Standard Case (r=1):**
$$\text{Dup}(u) = \text{Dup}_1(u)$$

**Strong Matching Case (r≥2):**
Two entities are flagged as strong duplicates when they share at least $r$ typed attributes, where $r \geq 2$.

## Physical Intuition / Derivation

### Why Typed Neighborhoods Matter

In real-world Master Data Management (MDM) systems, entities are connected to attributes through **typed edges** that encode the semantic relationship. For example:
- Person → Email via edge type `hasEmail`
- Person → Phone via edge type `hasPhone`
- Person → Address via edge type `hasAddr`

The key insight is that a **typed neighborhood** captures not just *which* attributes an entity connects to, but *how* it connects to them—the semantic type of the relationship matters.

### Threshold Parameter r: Evidence Strength

The parameter $r$ models **confidence in duplication**:

**r = 1 (Weak matches):** Two entities sharing a single attribute value may be coincidental. Examples:
- Two people sharing a phone number (family members, office phones)
- Two people with the same generic company email
- Two organizations at the same address (office building)

**r ≥ 2 (Strong matches):** Requiring multiple distinct typed attributes dramatically reduces false positives. Two people sharing the exact same email *and* phone number are far more likely to be genuine duplicates.

### Why Same-Type Constraint τᵥ(u) = τᵥ(v)?

Entity resolution only makes sense within entity types. A Person and an Organization should never be flagged as duplicates, even if they share an attribute value (e.g., both associated with the same address). This constraint ensures meaningful deduplication semantics.

### Complexity Implication

A crucial observation from the source material: **increasing r from 1 to r ≥ 2 requires strictly more powerful graph neural network architectures.** This reflects a fundamental difficulty: detecting 2-hop common neighbors requires higher-order reasoning than detecting 1-hop common neighbors. Weaker GNN models (like single-layer message-passing) cannot reliably compute $|\mathcal{N}_{\text{typed}}(u) \cap \mathcal{N}_{\text{typed}}(v)| \geq 2$.

## Applications in Engineering

### 1. **Master Data Management (MDM)**
Entity resolution is the primary application: consolidating duplicate customer, product, or supplier records across enterprise databases. Using $r \geq 2$ prevents false deduplication while catching true duplicates.

### 2. **Data Quality Assurance**
Identifying and flagging potential duplicates in data pipelines before they propagate through a system. The parameter $r$ can be tuned based on domain-specific duplicate risk.

### 3. **Knowledge Graph Construction**
Constructing knowledge graphs from unstructured sources often produces duplicate entities. Binary classification gates whether entities should be merged, protecting knowledge graph integrity.

### 4. **Fraud Detection**
In financial systems, identifying potentially fraudulent accounts that share multiple suspicious attributes (same device fingerprint, IP address, and billing address) while rejecting coincidental matches ($r \geq 2$).

### 5. **Record Linkage in Healthcare**
Matching patient records across hospital systems using multiple identifiers (SSN, birthdate, name) without falsely linking unrelated patients who happen to share one attribute.

### 6. **Bioinformatics Entity Matching**
Matching protein records, chemical compounds, or genomic