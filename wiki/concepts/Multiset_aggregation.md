# Multiset Aggregation

## Definition

**Multiset aggregation** is the process of combining multiple observations or elements—where duplicates are explicitly tracked and preserved—into a single representation. In the context of message-passing neural networks (MPNNs) on heterogeneous graphs, multiset aggregation refers to the collection and processing of neighborhood information as an unordered collection that maintains multiplicity.

Formally, given a node $u$ and its neighbors $\mathcal{N}(u)$, multiset aggregation constructs:

$$\text{AGG}(u) = \{\{h(v) : v \in \mathcal{N}(u)\}\}$$

where $\{\{\cdot\}\}$ denotes a multiset—an unordered collection where elements can appear more than once. The key distinction from set aggregation is that **count matters**: two nodes with identical embeddings contribute distinctly to the aggregation.

In **typed entity-attribute graphs**, the multiset tracked at each attribute node $a$ includes counts of incident edges by type:

$$M(a) = \{\{(\tau_V(u), \tau) : (u, a, \tau) \in E\}\}$$

where $\tau_V(u)$ is the type of entity $u$ and $\tau$ is the edge type.

---

## Key Equations

**Multiplicity function:** For a multiset $S$ and elements $x, y$:

$$\text{mult}_S(x, y) = \text{number of pairs } (x, y) \text{ in } S$$

**Duplication detection via multiset aggregation:** An entity $u$ is a duplicate of another same-typed entity $v$ if and only if they share a common attribute neighbor with matching edge types:

$$(a, \tau) \in \mathcal{N}_{\text{typed}}(u) \cap \mathcal{N}_{\text{typed}}(v) \neq \emptyset$$

This is detectable if and only if:

$$\text{mult}_{M(a)}(\tau_V(u), \tau') \geq 2$$

for some edge type $\tau'$, indicating at least two distinct same-typed entities connect to attribute $a$ via edges of type $\tau'$.

**Layer-wise MPNN aggregation:**
- **Layer 0:** Node embeddings $h^{(0)}(v) = \tau_V(v)$ (type indicator)
- **Layer 1 (forward):** Attributes aggregate entity types: $h^{(1)}(a) = \text{AGG}\{\{h^{(0)}(u) : (u, a, \tau) \in E\}\}$
- **Layer 2 (reverse):** Entities reconstruct neighborhood by aggregating back through attributes

---

## Physical Intuition / Derivation

### Why Multisets Matter

Consider a simple entity-attribute bipartite graph where we want to detect if two patients visited the same provider:

- **Patient A** → treated-by → **Provider X**
- **Patient B** → treated-by → **Provider X**

If we used **set** aggregation at Provider X, we would only record "at least one patient connected here." But **multiset** aggregation counts: "two distinct patients connect here."

### The 2-Hop Information Bottleneck

The source material establishes that **one layer is insufficient** for duplicate detection:

1. **After Layer 1 (forward pass):** Entity $u$ can only see its direct typed neighborhood $\mathcal{N}_{\text{typed}}(u) = \{(a, \tau) : (u, a, \tau) \in E\}$. This encodes which attributes $u$ connects to, but *not* whether other same-typed entities also connect to those attributes.

2. **After Layer 2 (reverse pass):** Each attribute $a$ has now learned the *multiset* of entity types incident to it. When this information flows back to $u$, it reveals: "Attribute $a$ has **two or more** connections from my entity type." This proves $u$ is not unique.

**Why we can't skip a hop:** In a simple graph, there is at most one edge from any entity to any attribute. So if the multiset at $a$ shows $\text{mult}_{M(a)}(\tau_V(u), \tau') \geq 2$, these edges must come from *different* entities. The second hop is essential to communicate this back.

### Multigraph Extension

When **parallel edges** are permitted (e.g., a patient visits the same provider three times, loaded from three separate source records), the multiset multiplicity grows naturally:

$$\text{mult}_{M(a)}(\tau_V(u), \tau') = 3$$

Now the MPNN must distinguish:
- Multiple parallel edges from the *same* entity to the *same* attribute (parallel multiplicity)
- Multiple edges from *different* entities to the same attribute (duplication signal)

Multigraph MPNNs aggregate over the **multiset of edge instances**, not just unique (source, target) pairs.

---

## Applications in Engineering

### 1. **Master Data Management (MDM)**
Entity deduplication in healthcare/financial systems requires detecting when multiple records refer to the same real-world entity. Multiset aggregation reveals shared attribute patterns:
- If **Patient A** and **Patient B** both have phone number 555-1234 and billing address "123 Main St," the duplicated attribute connections expose them as likely duplicates.

### 2. **Financial Crime Detection**
In **anti-money laundering (AML)** networks:
- Suspicious activity surfaces when the same account touches multiple high-risk intermediaries (a concentration pattern).
- Multiset counting detects: "Account $X$ has **three** separate transactions through money laundering shell entity $Z$."
- Average 17.92 parallel edges per node pair in real datasets (IBM AML).

### 3. **Heterogeneous Knowledge Graph Reasoning**
When querying whether two researchers are duplicates or competitors:
- Multiset aggregation of their co-authored papers, affiliated institutions, and citation patterns.
- Multiplicities encode collaboration intensity (e.g., "5 joint papers" vs. "1 joint paper").

### 4. **Supply Chain Network Analysis**
- Detecting counterfeit suppliers by observing