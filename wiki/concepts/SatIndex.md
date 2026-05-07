# SatIndex

## Definition

**SatIndex** is a preprocessed index data structure for answering satisfiability and witness queries on context-free grammars (CFGs) in Chomsky Normal Form (CNF). Given a CFG $G = (N, \Sigma, P, S)$ where $|N|$ is the number of nonterminals and $|P|$ is the number of productions, SatIndex supports:

- **Satisfiability queries**: $O(1)$ time to determine if a nonterminal $A \in N$ can derive a given string
- **Witness extraction**: $O(|\pi|)$ time to output an explicit derivation $\pi$ (a parse tree or proof object)

SatIndex is designed for **general CNF grammars** (without restrictions on grammar form), making it the broadest setting in the index family. It trades faster query time for higher preprocessing and space costs compared to restricted grammar variants like LinIndex.

## Key Equations

**Preprocessing complexity:**
$$T_{\text{preprocess}} = O(|P| \cdot n^3)$$

where $n$ is the string length and $|P|$ is the grammar size. This cubic dependence arises from the CYK (Cocke–Younger–Kasami) algorithm's inherent structure for general CFGs.

**Space complexity:**
$$S = O(|N| \cdot n^2)$$

The index maintains a table $T[i, j, A]$ for each substring $w[i:j]$ and nonterminal $A \in N$, storing whether $A \xrightarrow{*} w[i:j]$.

**Query and witness complexity:**
$$T_{\text{query}} = O(1), \quad T_{\text{witness}} = O(|\pi|)$$

Witness output is proportional to the derivation size—there is no additional overhead beyond the output itself (optimal witness representation).

## Physical Intuition / Derivation

### Building the Index: The CYK Foundation

SatIndex extends the classical **CYK parsing algorithm** into a queryable index:

1. **Recognize phase** (preprocessing): Fill a $|N| \times n \times n$ boolean table $T$ bottom-up:
   - Base case: $T[A, i, i+1] = \text{true}$ if $A \to w[i]$ is a production
   - Inductive case: $T[A, i, j] = \text{true}$ if $\exists$ production $A \to BC$ and $\exists k$ such that $T[B, i, k]$ and $T[C, k, j]$ both hold

2. **Index storage**: Retain the full DP table and back-pointers to record which productions fired in the base/inductive cases.

3. **Query**: Lookup $T[S, 0, n]$ in $O(1)$ time.

4. **Witness reconstruction**: Recursively follow stored back-pointers to reconstruct the derivation tree in linear time in the tree size.

### Why General CNF is Expensive

**General CNF imposes no restrictions** on the grammar structure (compare [[LinIndex]], which requires the grammar to be in **linear** form where each production has $\leq 1$ nonterminal on the right-hand side). This generality necessitates checking all possible split points $k \in [i, j)$ during the inductive step, yielding $O(|P| \cdot n^3)$ preprocessing.

The bottleneck is **dense reachability**: for each substring range $[i,j]$ and rule $A \to BC$, we must test $O(n)$ possible partitions, repeated $O(|N| \cdot n^2)$ times across all ranges and nonterminals.

### Trade-offs with Restricted Grammars

When the grammar is **linear** (at most one nonterminal per production), the split-point enumeration becomes unnecessary in many cases, enabling preprocessing to drop to $O(|P| \cdot n^2)$ or even $O(|P| \cdot n^2)$ with sparsity (see [[LinIndex]]).

## Applications in Engineering

### 1. **Configuration and Schema Validation**
SatIndex supports fast validation of JSON schemas and hierarchical configuration files against context-free constraints. Given a JSON document, the index answers "is this document valid?" in $O(1)$ and produces a parse tree in linear time—essential for DevOps tools and cloud infrastructure (e.g., Kubernetes configuration validation).

### 2. **Compiler Front-Ends**
Classic application: preprocess a grammar at compiler-generation time, then answer syntax queries at runtime without re-parsing. Supports incremental compilation and error recovery by caching witness information.

### 3. **Program Synthesis and Constraint-Based Search**
In domains like SmartStart (data-shape synthesis) or type-guided program synthesis, SatIndex enables fast filtering of candidate programs: query whether a synthesized expression satisfies the target grammar in $O(1)$ and extract witnesses for further refinement.

### 4. **Natural Language Processing (NLP)**
SatIndex can index context-free approximations of natural language grammars. At query time, check if a word sequence satisfies grammatical constraints in constant time, useful for grammar-based dialogue systems or syntax-aware machine translation.

### 5. **Network/Dyck Reachability**
In the broader ecosystem, SatIndex sits alongside [[SWDIndex]] (shortest witness) and [[DyckIndex]] for restricted graph classes. Together they form a family for reachability queries on annotated graphs where paths must conform to balanced/context-free structure (relevant to information-flow analysis, call-return matching in malware detection).

## Common Mistakes / Pitfalls

### 1. **Assuming $O(1)$ Witness Time**
A frequent error: students mistakenly believe witness extraction is also $O(1)$. **Witness output is $O(|\pi|)$**, proportional to the derivation size. If the grammar produces very large parse trees, extraction time grows linearly. The $O(1)$ query cost only determines *existence*, not output.

### 2. **Confusing Preprocessing Costs Across Variants**
Table 1 lists multiple indices. SatIndex's $O(|P| n^3