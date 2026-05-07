# Graph-based Attribute Matching

## Definition

Graph-based Attribute Matching is a machine learning approach for entity resolution (deduplication) that leverages Graph Neural Networks (GNNs) to identify when two database records refer to the same real-world entity, despite noisy, incomplete, or inconsistent attribute values.

Unlike traditional combinatorial methods that require exact string matching, graph-based attribute matching operates in a learned continuous embedding space where semantically similar attributes map to nearby vectors. This enables **soft matching**—graceful degradation under noise rather than categorical failure.

### Core Components

- **Entities**: Database records to be matched (denoted $v \in V$)
- **Attributes**: Properties of entities (e.g., name, address, phone)
- **Attribute types**: Categorical labels $\alpha_j \in T_A$ 
- **Entity types**: Record classes $\sigma \in T_E$
- **Edge types**: Relationships between entities and attributes $\tau_j \in T_E$

The problem: Given two entities $u, v$, determine if they are **co-referent** (refer to the same entity) despite attribute noise and variation.

---

## Key Equations

### Soft Overlap Between Entities

$$\text{ov}^{\text{soft}}(u,v) = \sum_{a \in A_u \cap A_v} \text{sim}(\psi(a_u), \psi(a_v))$$

Where:
- $\psi: A \to \mathbb{R}^d$ is a **feature encoder** mapping attribute strings to $d$-dimensional embeddings
- $\text{sim}: \mathbb{R}^d \times \mathbb{R}^d \to [0,1]$ is a learnable **similarity function** (e.g., cosine, learned MLP)
- $A_u, A_v$ are the attribute sets of entities $u, v$
- The sum aggregates soft similarity across all shared attribute *types*

### MPNN Readout for Co-reference Prediction

$$\hat{y}(v) = f_{\text{readout}}(\{h^{(T)}(v), h^{(T)}(a) : a \in A_v\})$$

Where:
- $h^{(T)}(v)$ is the final hidden state of node $v$ after $T$ message-passing rounds
- The readout function aggregates node embeddings to produce a scalar co-reference score
- A correct MPNN achieves $\hat{y}(v) = f(v)$ for all input graphs $G$ and target predicate $f$

### Co-reference Predicate (Exact Matching Baseline)

$$\text{Dupr}(u,v) = \begin{cases} 1 & \text{if } |A_u \cap A_v| \geq r \\ 0 & \text{otherwise} \end{cases}$$

Entities $u$ and $v$ are co-referent if they share at least $r$ exact typed attribute values. (Computable in $O(|E|)$ on clean data via hash-based grouping.)

---

## Physical Intuition / Derivation

### Why Exact Matching Fails

In pristine, canonicalized databases, hash-based joins solve entity resolution in linear time: group records by shared attributes using a hash table. **But real data is dirty.**

Consider matching employee records:
- "John Smith" ≠ "J. Smith" (abbreviation)
- "john.smith@company.com" ≠ "john_smith@company.com" (formatting)
- "Robert Johnson, Jr." ≠ "Bob Johnson" (nickname + suffix)

A hash-based approach treats these as **different people entirely**, missing true duplicates.

### The GNN Solution: Continuous Embedding Space

The key insight is to **relax exact matching into soft matching** via learned embeddings:

1. **Encode attributes**: A character-level neural network or pre-trained language model (e.g., BERT) maps each attribute string into a continuous vector $\psi(a) \in \mathbb{R}^d$.

2. **Compute soft similarity**: Rather than testing $\psi(a_u) = \psi(a_v)$ (exact match), compute a similarity score $\text{sim}(\psi(a_u), \psi(a_v)) \in [0,1]$.
   - "John Smith" and "J. Smith" may have $\text{sim} = 0.85$ (nearby in embedding space)
   - "John Smith" and "Maria Garcia" have $\text{sim} = 0.02$ (distant)

3. **Aggregate across attributes**: A Graph Neural Network message-passing scheme computes node embeddings by aggregating information across multiple attributes and entities:
   $$h^{(t+1)}(v) = \text{AGGREGATE}\left(\{h^{(t)}(v)\} \cup \{h^{(t)}(u) : (u,v) \in E\}\right)$$
   This allows the model to learn patterns: *if two entities share similar names AND similar addresses, they're likely duplicates.*

4. **Train on labeled examples**: Backpropagation adjusts $\psi$, $\text{sim}$, and the GNN parameters to correctly classify known duplicate and non-duplicate pairs.

### Why This Works: Robustness Under Noise

- **Graceful degradation**: A single typo reduces similarity from 1.0 to 0.95, not 1.0 to 0.0.
- **Multi-signal fusion**: The MPNN learns to weight evidence across many attributes; one noisy attribute doesn't kill the decision.
- **Learned representations**: The encoder $\psi$ adapts to the domain (names, addresses, etc.) and data distribution.

---

## Applications in Engineering

### Database Systems
- **Data deduplication**: Merge customer records, eliminate duplicate product listings in e-commerce catalogs
- **Data quality pipelines**: Identify and flag potential duplicates for manual review or automatic consolidation

### Customer Relationship Management (CRM)
- **Customer 360**: Unify fragmented customer profiles across multiple touchpoints (web, mobile, in-store)
- **Churn prediction**: More accurate