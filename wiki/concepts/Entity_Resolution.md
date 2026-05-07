# Entity Resolution

## Definition

**Entity Resolution** is the computational problem of identifying and linking multiple records or data points that refer to the same real-world entity despite variations in representation. In the context of knowledge graphs and databases, it answers the question: "Do two records describe the same entity?"

Formally, given a set of entities $E$ with attributes from domain $A$, entity resolution computes a function $f: E \times E \to \{0,1\}$ where $f(u,v) = 1$ indicates that entities $u$ and $v$ are co-referent (duplicates).

Entity resolution is also known as **record linkage**, **deduplication**, **coreference resolution**, or **entity matching**. The problem becomes non-trivial in the presence of **noisy, heterogeneous, or incomplete data** where identical strings cannot be relied upon for matching.

## Key Equations

### Hard (Exact) Matching

For entities of the same type, define the **hard overlap** predicate based on exact attribute matches:

$$\text{Dup}_r(u, v) = \begin{cases} 1 & \text{if } |A(u) \cap A(v)| \geq r \\ 0 & \text{otherwise} \end{cases}$$

where $A(u)$ denotes the set of attribute values for entity $u$, and $r$ is a threshold on the minimum number of shared attributes.

### Soft (Learned) Matching

For noisy data, learned embeddings enable graceful degradation. Define the **soft overlap** between entities $u$ and $v$ as:

$$\text{ov}_{\text{soft}}(u, v) = \sum_{a \in \text{attributes}} \text{sim}(\psi(a_u), \psi(a_v))$$

where:
- $\psi: A \to \mathbb{R}^d$ is a learned feature encoder mapping attribute strings to $d$-dimensional vectors
- $\text{sim}: \mathbb{R}^d \times \mathbb{R}^d \to [0,1]$ is a learned similarity function in the embedding space
- $a_u, a_v$ are the attribute values of entities $u$ and $v$

The MPNN (Message Passing Neural Network) readout produces a matching score:

$$\hat{y}(u, v) = \text{readout}(\{h^{(L)}(u), h^{(L)}(v)\})$$

where $h^{(L)}$ denotes node embeddings after $L$ message-passing rounds.

## Physical Intuition / Derivation

### Why Hard Matching Fails

Combinatorial, hash-based approaches work perfectly on clean data:
- **Exact string matching** via hash indices: $O(|E|)$ time complexity
- **Example**: "John Smith" matches "John Smith" → detected as duplicate
- **But**: "John Smith" vs. "J. Smith" → **missed entirely** (brittleness)

Real-world attribute values exhibit three categories of variation:

1. **String normalization differences**: "John Smith" vs. "JOHN SMITH"
2. **Abbreviations and formatting**: "J. Smith" vs. "John Smith"
3. **Data entry errors**: "Jon Smith" (typo) vs. "John Smith"

Hash-based matching catastrophically fails on any discrepancy; there is no graceful degradation.

### Why Soft Matching Works

Graph neural networks overcome brittleness by operating in a **learned continuous embedding space**:

1. **Feature encoding** $\psi$ maps attribute strings to vectors via:
   - Character-level neural networks (capture spelling variations)
   - Pretrained language models (capture semantic similarities)

2. **Similarity function** $\text{sim}$ learns relationships:
   - $\text{sim}(\psi("John Smith"), \psi("J. Smith"))$ → high value (close vectors)
   - $\text{sim}(\psi("John Smith"), \psi("Maria Garcia"))$ → low value (distant vectors)

3. **Message passing** aggregates soft signals across multiple attributes:
   - Single-attribute noise is dampened
   - Consensus across multiple attributes strengthens co-reference confidence
   - Result: **graceful degradation** rather than catastrophic failure

**Key insight**: The MPNN learns to weight and combine multiple weak signals of similarity rather than requiring any single definitive match criterion.

## Applications in Engineering

### Database Systems
- **Data cleaning pipelines**: Remove duplicate customer or product records in commercial databases
- **Master data management (MDM)**: Maintain single unified view of entities across multiple systems
- **Data warehousing**: Consolidate records from heterogeneous sources before analysis

### Knowledge Graphs & Linked Data
- **Knowledge base construction**: Link entity mentions across Wikipedia, DBpedia, Wikidata
- **Schema alignment**: Resolve references to same concept under different ontologies
- **Cross-lingual entity linking**: Match entities described in different languages

### Information Retrieval & NLP
- **Coreference resolution**: Link pronouns and named entities to canonical referents in text
- **Author disambiguation**: Identify when multiple publication records belong to same researcher
- **Query expansion**: Recognize that "NYC," "New York City," and "New York" are the same entity

### Bioinformatics
- **Protein/gene identification**: Link protein sequences and gene entries across databases (UniProt, GenBank)
- **Patient record linkage**: Connect medical records for same individual across hospital systems (HIPAA-compliant)

### Supply Chain & Logistics
- **Supplier deduplication**: Consolidate vendor records that refer to same company under different names
- **Part number normalization**: Link equivalent components across different manufacturers' catalogs

## Common Mistakes / Pitfalls

### 1. Assuming Clean Data
**Mistake**: Implementing hash-based exact matching for real-world data.
**Correction**: Budget for 5–30% noise in attribute values. Use soft matching from the start.

### 2. Ignoring Entity Type Information
**Mistake**: Attempting to match entities of different types (e.g., Person vs. Organization).
**Correction**: Enforce type consistency; separately resolve each entity type. Use typed attribute nodes ($\alpha_j \in T_A$, $\tau_j \in T_E$) to prevent nonsensical matches.

### 