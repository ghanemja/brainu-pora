# Entity-Attribute Graphs

## Definition

An **entity-attribute graph** is a bipartite directed multigraph $G = (E \cup A, \mathcal{E})$ where:

- **Entity nodes** $E$ represent primary objects (e.g., patients, customers, accounts), each with a **type** $\tau_V(u) \in T_V$
- **Attribute nodes** $A$ represent secondary features or references, each with a **type** $\tau_V(a) \in T_A$
- **Directed edges** $\mathcal{E} \subseteq E \times A \times T_{\mathcal{E}}$ connect entities to attributes, labeled with **edge types** $\tau' \in T_{\mathcal{E}}$ (e.g., "treated by", "visited", "owns")
- **Multiplicity** allows parallel edges of the same type between the same entity-attribute pair (multigraph setting)

In the **simple** (non-multi) variant, at most one edge of each type exists between any entity-attribute pair.

A **typed neighborhood** of entity $u$ is:
$$N_{\text{typed}}(u) = \{(a, \tau') : (u, a, \tau') \in \mathcal{E}\}$$

## Key Equations

### Multiplicity Function

For a node $S$ (typically an attribute node), define the multiplicity of types as:
$$\text{mult}_S(\tau, \tau') = \text{count of edges from entities of type } \tau \text{ to } S \text{ with edge type } \tau'$$

### Duplication Detection Predicate

The **Dup** function detects whether entity $u$ has a same-type "competitor" sharing attributes:
$$\text{Dup}(u) = \begin{cases} 1 & \text{if } \exists v \neq u: \tau_V(v) = \tau_V(u) \text{ and } N_{\text{typed}}(u) \cap N_{\text{typed}}(v) \neq \emptyset \\ 0 & \text{otherwise} \end{cases}$$

### Message-Passing Formulation

For an MPNN with two layers and reverse message passing:

**Layer 1 (Forward):** Aggregate entity info to attributes
$$h^{(1)}(a) = \text{AGG}\left(\{h^{(0)}(u), \tau' : (u, a, \tau') \in \mathcal{E}\}\right)$$

**Layer 2 (Reverse):** Entities learn about competing entity types at shared attributes
$$h^{(2)}(u) = \text{AGG}\left(\{h^{(1)}(a), \tau' : (u, a, \tau') \in \mathcal{E}\}\right)$$

## Physical Intuition / Derivation

### Why Two Layers Are Necessary and Sufficient

**The core insight:** Computing $\text{Dup}(u)$ requires detecting whether other entities of the same type share attribute neighbors with $u$. This information is inherently 2-hop:

1. **Layer 1 (Forward hop):** Entity $u$ sends its type $\tau_V(u)$ to all its attribute neighbors $(a_i, \tau')$. Each attribute $a$ now aggregates the *set of entity types* incident to it.

2. **Layer 2 (Reverse hop):** Entity $u$ receives back from each attribute $a$ the multiset of types incident to $a$. If $u$ observes another entity type $\tau_V(u)$ arriving at some shared attribute, then $\text{Dup}(u) = 1$.

**Why not 1 layer?** After one forward pass, $h^{(1)}(u)$ encodes only $\tau_V(u)$ and its own typed neighborhood $N_{\text{typed}}(u) = \{(a_i, \tau'_i)\}$. But this is insufficient—two distinct entities $u$ and $v$ with identical typed neighborhoods $N_{\text{typed}}(u) = N_{\text{typed}}(v)$ may or may not be duplicates, depending on whether other entities of the same type as $u$ and $v$ share those same attributes. This *fan-in information* (which entity types contribute to each attribute) only becomes available in Layer 2.

### Formal Necessity Argument

Consider two separation graphs $G_1$ and $G_2$:
- In both: entity $u$ has $N_{\text{typed}}(u) = \{(a, \tau_1)\}$
- In $G_1$: attribute $a$ also receives an edge from another entity $v$ of type $\tau_V(u)$ → $\text{Dup}(u) = 1$
- In $G_2$: attribute $a$ receives edges only from entities of *different* types → $\text{Dup}(u) = 0$

After Layer 1, $h^{(1)}(u)$ is identical in both graphs (no information about $v$). Only Layer 2 distinguishes them.

## Applications in Engineering

### Master Data Management (MDM)

Entity-attribute graphs naturally model **deduplication pipelines** in healthcare and financial systems:
- **Entities:** Patient records, account holders
- **Attributes:** Medical IDs, phone numbers, email addresses, SSN
- **Edge types:** "has\_ID", "linked\_by\_phone", etc.
- **Task:** Flag duplicate entities that share identifying attributes

This is critical in *blocking* and *match candidate generation*—reducing quadratic comparison costs to linear or sublinear.

### Financial Transaction Networks

Anti-money-laundering (AML) systems represent:
- **Entities:** Accounts, customers, agents
- **Attributes:** Bank branches, transaction counterparties, IP addresses
- **Edge types:** "sent\_from", "received\_at", "logged\_in\_via"
- **Multiplicity:** Real systems show ~17.92 edges per node pair on average (IBM AML dataset)

The multigraph setting is essential because the same entity pair may have multiple transactions, and losing multiplicity information degrades anom