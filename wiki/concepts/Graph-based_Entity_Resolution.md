# Graph-based Entity Resolution

## Definition

**Graph-based Entity Resolution** is a framework for identifying duplicate or conflicting entity records within a knowledge graph by analyzing shared attributes through typed entity-attribute graphs. The core task is to classify entities as potential duplicates based on the overlap in their attribute neighborhoods.

Formally, given a **typed entity-attribute graph** $G = (E, A, \mathcal{E})$ where:
- $E$ = set of entities (e.g., Person, Organization records)
- $A$ = set of attribute nodes (e.g., email addresses, phone numbers)
- $\mathcal{E} \subseteq E \times A \times T_E$ = typed edges connecting entities to attributes
- $T_E$ = set of edge types (e.g., hasEmail, hasPhone, hasAddr)
- $\tau_V: E \to T_V$ = type function assigning entity types

Two entities are potential **duplicates** if they are of the same type and share attribute values through edges of matching types.

---

## Key Equations

### Typed Neighborhood

For an entity $u \in E$, the **typed neighborhood** captures all attribute-edge type pairs connected to $u$:

$$N_{\text{typed}}(u) = \{(a, \tau) \in A \times T_E : (u, a, \tau) \in \mathcal{E}\}$$

This is the fundamental building block—it enumerates both *what* attributes an entity possesses and *how* they are connected (the edge type).

### Duplicate Detection at Threshold $r$

The **$K_{2,r}$ duplicate detection problem** classifies entity $u$ as a duplicate if there exists another entity $v$ of the same type sharing at least $r$ typed attribute connections:

$$\text{Dup}_r(u) = \begin{cases} 1 & \text{if } \exists v \in E \setminus \{u\}, \tau_V(v) = \tau_V(u), \\ & |N_{\text{typed}}(u) \cap N_{\text{typed}}(v)| \geq r \\ 0 & \text{otherwise} \end{cases}$$

When $r = 1$, this is abbreviated $\text{Dup}(u)$ and captures *any* shared typed attribute. When comparing graphs explicitly:

$$\text{Dup}_{r,G}(u) \quad \text{or simply} \quad \text{Dup}_{G}(u) \text{ when } r=1$$

### Intersection of Typed Neighborhoods

The count of shared typed attributes between two entities $u$ and $v$:

$$|N_{\text{typed}}(u) \cap N_{\text{typed}}(v)| = \text{number of (attribute node, edge type) pairs both entities connect to}$$

---

## Physical Intuition / Derivation

### Why Typed Edges Matter

In naive entity resolution, we might ask: "Do entities $u$ and $v$ share any attribute node?" This ignores crucial context. Consider:
- Person $u$ has email smith@x.com via edge *hasEmail*
- Person $v$ has email smith@x.com via edge *hasEmail*  
→ **Strong evidence of duplication**

But if $u$ connected via *hasEmail* and $v$ via *hasMetadata*, the shared attribute node becomes accidental. By pairing attribute nodes with edge types into tuples $(a, \tau)$, we enforce **semantic consistency**: only duplicates should share attributes through the *same type of connection*.

### The Threshold Parameter $r$

The parameter $r$ controls **evidence strength**:

- **$r = 1$ (weak evidence):** Two Person records sharing *only* a phone number might be coincidental (family members share devices; companies issue generic emails). Many false positives.

- **$r = 2$ (strong evidence):** Two Person records sharing *both* email *and* phone number are statistically far more likely to be genuine duplicates. The conjunction of independent attributes dramatically reduces false positives.

- **$r = 3$ (very strong evidence):** Matching email *and* phone *and* address is near-certain duplication for most domains.

This threshold reflects a key insight: **attribute types are heterogeneous and often independent**. A second matching attribute across a different type (e.g., email vs. phone) provides multiplicative confidence gain.

### Type Constraint: $\tau_V(u) = \tau_V(v)$

Entity-resolution duplicates only make sense within the same semantic class:
- Two *Person* records can be duplicates
- Two *Organization* records can be duplicates  
- A *Person* and *Organization* **cannot** be duplicates

This hard constraint prevents nonsensical cross-category matches.

---

## Applications in Engineering

### 1. **Master Data Management (MDM)**
In enterprise data systems (CRM, ERP, data warehouses), millions of customer/supplier records accumulate from mergers, acquisitions, and multiple entry points. Graph-based entity resolution identifies which records represent the same real-world entity, enabling data consolidation and 360° customer views.

**Example:** A bank acquires another bank. Customer "John Smith" appears in both legacy systems with email john.smith@oldbank.com (in one) and phone 555-0123 (in the other). Detecting $\text{Dup}_2$ on the merged graph flags them for consolidation.

### 2. **Knowledge Graph Construction**
Building knowledge graphs from heterogeneous sources (web, databases, scientific literature) requires deduplication. Graph-based ER identifies when different source entries refer to the same person, place, or concept.

**Example:** DBpedia, Wikidata integration: multiple sources mention "Mount Everest" with aliases, coordinates, and historical records. The typed-graph approach avoids conflating "Mount Everest" with "Mount Kilimanjaro" just because both have "mountain" attributes—it respects the *type* of connection.

### 3. **Fraud Detection in Financial Networks**
Payment networks model transactions as entity-attribute relationships (e.g., Person → BankAccount, Person → Address). Duplicates suggest money laundering or identity fraud.

**Example:** Two customer profiles with the same bank account (attribute) and address (attribute) but different names, where $r=