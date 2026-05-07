# Duplicate Entity Detection

## Definition

**Duplicate Entity Detection** is a binary node classification problem on typed entity-attribute graphs where the goal is to identify whether an entity has a potential duplicate partner. Two entities are considered potential duplicates if:

1. They are of the **same type** (e.g., both Person records, both Organization records)
2. They share a **minimum threshold number of common attribute values** across potentially different attribute types

This is formalized as the **K_{2,r} detection problem**, where r ≥ 1 specifies the minimum number of shared typed attributes required to classify an entity as having a duplicate.

---

## Key Equations

**Typed Neighborhood Definition:**

For an entity $u \in E$ in a typed entity-attribute graph, the typed neighborhood is:

$$N_{\text{typed}}(u) = \{(a, \tau) \in A \times T_E : (u, a, \tau) \in E\}$$

where:
- $A$ is the set of attribute nodes
- $T_E$ is the set of edge types
- $(u, a, \tau)$ represents an edge from entity $u$ to attribute $a$ with type $\tau$

**Duplicate Detection (K_{2,r} Problem):**

$$\text{Dup}_r(u) = \begin{cases} 1 & \text{if } \exists v \in E \setminus \{u\}, \, \tau_V(v) = \tau_V(u), \\ & |N_{\text{typed}}(u) \cap N_{\text{typed}}(v)| \geq r \\ 0 & \text{otherwise} \end{cases}$$

where:
- $\tau_V(u)$ is the type of entity $u$
- $r$ is the threshold of shared typed attributes
- The cardinality $|N_{\text{typed}}(u) \cap N_{\text{typed}}(v)|$ counts common (attribute, edge-type) pairs

**Standard Case (r=1):**

$$\text{Dup}(u) = \text{Dup}_1(u)$$

---

## Physical Intuition / Derivation

### Building the Model from Duplicates

Consider a **Master Data Management (MDM)** scenario: a company has two customer databases that need to be merged. Some records represent the same person but were entered separately, creating duplicates.

**Why typed neighborhoods?**

Records aren't just sets of values—they're structured:
- A person has email *via* the `hasEmail` edge type
- A person has phone *via* the `hasPhone` edge type
- A person has address *via* the `hasAddr` edge type

The typed neighborhood $(a, \tau)$ captures both *what* attribute is shared and *how* it's connected. This is essential because:

$$N_{\text{typed}}(u) = \{(\text{smith@x.com}, \text{hasEmail}), (\text{555-1234}, \text{hasPhone}), \ldots\}$$

### The Role of Threshold r

**Weak Match (r=1):** Two people sharing only a phone number might be:
- Coincidental (family members on a shared plan)
- False positives in a naive system

**Strong Match (r=2):** Two people sharing the same email *and* the same phone number is far more reliable evidence of duplication.

**Why this matters computationally:** Detecting $r=1$ duplicates (single shared attributes) is easier—a simple neighborhood comparison suffices. However, detecting $r \geq 2$ duplicates requires tracking *intersections* of neighborhoods, which involves higher-order reasoning and typically requires more expressive Graph Neural Network (GNN) architectures (e.g., those capable of computing multi-hop or subgraph patterns).

### Same-Type Constraint

The constraint $\tau_V(u) = \tau_V(v)$ ensures semantic consistency:
- A Person record cannot be a duplicate of an Organization record
- This mirrors real-world entity resolution where duplicates must belong to the same entity class

---

## Applications in Engineering

### 1. **Master Data Management (MDM)**
- **Healthcare:** Merging patient records across hospital systems to prevent duplicate medical histories and ensure accurate treatment
- **Finance:** Detecting duplicate customer accounts in banking systems to prevent fraud and regulatory issues
- **Enterprise:** Consolidating company data from multiple acquisitions or legacy systems

### 2. **Data Quality and Cleaning**
- **Database Integration:** Post-merge processes in ETL (Extract-Transform-Load) pipelines
- **Data Deduplication:** Reducing storage overhead by identifying and removing redundant records
- **CRM Systems:** Maintaining single customer views across sales, marketing, and support channels

### 3. **Knowledge Graph Construction**
- **Named Entity Linking:** Identifying when different records refer to the same real-world entity
- **Knowledge Base Refinement:** Merging duplicate nodes in large-scale knowledge graphs (Wikipedia, Wikidata)
- **Citation Networks:** Detecting duplicate author/paper records in academic databases

### 4. **Fraud Detection and Security**
- **Identity Verification:** Flagging suspicious duplicate account creations
- **AML Compliance:** Detecting the same individual using multiple identity documents
- **Cybersecurity:** Identifying cloned or impersonated accounts across platforms

### 5. **E-commerce and Marketplaces**
- **Product Deduplication:** Identifying duplicate product listings across sellers
- **Seller Networks:** Detecting when a single actor operates multiple seller accounts
- **Inventory Management:** Consolidating duplicate items in catalogs

---

## Common Mistakes / Pitfalls

### 1. **Ignoring the Same-Type Constraint**
**Mistake:** Comparing entities without checking type compatibility.

**Why it fails:** A Person and an Organization may share attributes (e.g., an office address) but are fundamentally different entities. This leads to false positives.

**Correct approach:** Always enforce $\tau_V(u) = \tau_V(v)$ before comparison.

---

### 2. **Treating r=1 and r≥2 as Equally Computable**
**Mistake:** Using simple neighborhood-matching algorithms for all values of r.

**Why it fails:** 
- $r=1$ is a *local* property (does u have any common neighbor with another same