# Typed Entity-Attribute Graph

## Definition

A **typed entity-attribute graph** is a directed, labeled graph structure used in data management and entity resolution to represent relationships between entities and their attributes, where both edges and nodes carry semantic type information.

Formally, a typed entity-attribute graph is a tuple $G = (E, A, T_E, T_A, \tau_V, \tau_E)$ where:

- $E$ = set of **entity nodes** (e.g., Person records, Organization records)
- $A$ = set of **attribute nodes** (e.g., email addresses, phone numbers, addresses)
- $T_E$ = set of **entity types** (e.g., $\{\text{Person, Organization}\}$)
- $T_A$ = set of **attribute types** (e.g., $\{\text{Email, Phone, Address}\}$)
- $\tau_V : E \cup A \to T_E \cup T_A$ = node type labeling function
- $\tau_E : E^2 \cup (E \times A) \to \Sigma$ = edge type labeling function (e.g., $\text{hasEmail, hasPhone}$)

The edge set contains directed edges of the form $(u, a, \tau)$ where $u \in E$, $a \in A$, and $\tau$ is the edge type indicating the relationship semantics.

## Key Equations

### Typed Neighborhood

For an entity $u \in E$, the **typed neighborhood** captures all attribute nodes reachable from $u$ along with their connecting edge types:

$$N_{\text{typed}}(u) = \{(a, \tau) \in A \times T_E : (u, a, \tau) \in E\}$$

This is a set of tuples, not a scalar count—it preserves both the attribute identity and the type of connection.

### Duplicate Detection via $K_{2,r}$ Problem

The core binary classification task is to determine if entity $u$ has duplicates at strength level $r$:

$$\text{Dup}_r(u) = \begin{cases} 
1 & \text{if } \exists v \in E \setminus \{u\}, \tau_V(v) = \tau_V(u), \\
& \quad |N_{\text{typed}}(u) \cap N_{\text{typed}}(v)| \geq r \\
0 & \text{otherwise}
\end{cases}$$

Key constraints:
- **Same-type constraint**: $\tau_V(u) = \tau_V(v)$ ensures duplicates are only detected within entity types (Person–Person, Organization–Organization, never mixed types)
- **Threshold parameter**: $r \geq 1$ controls evidence strength. $r=1$ is denoted $\text{Dup}(u)$
- **Intersection count**: $|N_{\text{typed}}(u) \cap N_{\text{typed}}(v)| \geq r$ counts shared typed attributes (not raw attribute values)

## Physical Intuition / Derivation

### Why Typed Edges?

Real-world data has **heterogeneous semantics**. A Person entity connects to attributes via semantically distinct relationships:
- An email address via edge type `hasEmail`
- A phone number via edge type `hasPhone`  
- A residential address via edge type `hasAddr`

Conflating these into a single edge type loses information: two people sharing the *same email* is quite different from two people sharing the *same phone number*.

### The Threshold Parameter $r$

The parameter $r$ encodes **evidential strength**:

| $r$ | Evidence Level | Example | Confidence |
|-----|---|---------|-----------|
| 1 | Weak match | Two Person records share only an email | Low (could be family, shared account) |
| 2 | Moderate match | Two Person records share email AND phone | High (unlikely coincidence) |
| 3+ | Strong match | Email + phone + address match | Very high (near-certain duplicate) |

**Why does $r=2$ require stronger GNNs?** 

At $r=1$, a simple neighborhood aggregation can detect if two entities share *any* attribute. At $r \geq 2$, the model must reason about *conjunctions* of evidence: "does $u$ share attribute set $A_1$ with some $v_1$ *and also* share attribute set $A_2$ with possibly a different $v_2$?" This requires the GNN to maintain and combine multiple compositional paths—a capability that single-layer or shallow architectures lack.

### The $K_{2,r}$ Connection

The name "$K_{2,r}$ detection" derives from graph theory: detecting whether the bipartite subgraph induced by an entity $u$ and its potential duplicate $v$ (with the shared attributes as the middle layer) contains a complete bipartite subgraph $K_{2,r}$ (two entity nodes fully connected to $r$ attribute nodes).

## Applications in Engineering

### Master Data Management (MDM)

In large enterprises (e.g., banking, healthcare), multiple systems maintain overlapping customer/patient records with inconsistent identifiers. Typed entity-attribute graphs:
- **Identify redundant records** before consolidation
- **Respect entity semantics**: only merge records of the same business type
- **Control merge aggressiveness** via $r$ parameter (higher $r$ = fewer false merges)

### Deduplication at Scale

For datasets with millions of entities:
- **Asymmetric cost**: False negatives (missing duplicates) harm data quality; false positives (incorrectly merging) are often more costly
- Tuning $r$ allows trading recall vs. precision based on domain requirements

### Knowledge Graph Cleaning

In knowledge bases (Wikidata, DBpedia), entity nodes may have duplicates from multiple sources. Typed attributes help distinguish:
- Textual descriptions (type: `hasDescription`)
- Identifiers like ISBN (type: `hasISBN`)  
- Related entities (type: `relatedTo`)

Enabling selective deduplication: merge only on identifier matches, not on fuzzy text similarity.

### Fraud Detection & Identity Verification

Financial systems use similar logic to flag suspicious accounts:
- Multiple accounts sharing phone number +