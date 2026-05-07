# LinIndex

## Definition

**LinIndex** is a specialized indexing data structure designed for context-free grammar (CFG) reachability and witness computation, optimized for the **linear+sparse regime**. Specifically, it targets grammars in **TALNF** (a linear normal form) where the grammar size parameter $m = O(n)$ is small relative to the input graph size $n$.

The key distinguishing feature of LinIndex is that it achieves **subcubic preprocessing** time—a breakthrough result unavailable to more general CFG indexing approaches like SatIndex. LinIndex maintains:
- A precomputed index over the input graph and grammar
- Direct support for $O(1)$ constant-time reachability queries
- Explicit witness paths (parse tree proofs) of length $O(|\pi|)$

This contrasts with general CNF indexing, which requires $O(|P|n^3)$ cubic-time preprocessing.

## Key Equations

### Preprocessing Complexity
$$T_{\text{preprocess}}(LinIndex) = O(|P|mn)$$

where:
- $|P|$ = grammar rule count
- $m$ = grammar size (linear grammar constraint: $m = O(n)$)
- $n$ = input graph size

**In the linear+sparse regime** ($m = O(n)$):
$$T_{\text{preprocess}}(LinIndex) = O(|P|n^2)$$

### Space Complexity
$$S(LinIndex) = O(|N|n^2)$$
where $|N|$ is the number of nonterminals.

### Query Complexity
$$T_{\text{query}} = O(1)$$
(constant time after preprocessing)

### Witness Output
$$T_{\text{witness}} = O(|\pi|)$$
where $|\pi|$ is the explicit length of the parse tree witness (proportional to the derivation length).

## Physical Intuition / Derivation

### Why Linearity Enables Subcubic Preprocessing

The cubic barrier for general CFG reachability (Theorem 6.1) arises from the need to enumerate all possible parse trees over all graph paths—a combinatorial explosion. For a general CNF grammar:
- Each grammar rule can match pairs of shorter derivations
- Over an $n$-node graph, this generates $O(n^3)$ intermediate subproblems (one per triple: start node, split point, end node)
- General CFGs require checking all such combinations

**Linear grammars** eliminate this explosion because:
1. Each rule has **at most one nonterminal** on the right-hand side, plus terminals
2. A derivation cannot "branch" and recombine unpredictably
3. The proof structure becomes more constrained—resembling a path rather than an arbitrary tree

This structural restriction reduces the effective grammar size from cubic to quadratic in the dynamic programming state space.

### The Three-Layer Architecture

LinIndex combines three components:

1. **Grammar Preprocessing**: Convert TALNF grammar to an index-friendly representation in $O(|P|mn)$ time
2. **Graph Indexing**: Compute reachability information compatible with the linear grammar structure in $O(|N|n^2)$ space
3. **Witness Interface**: On query, extract the explicit derivation in $O(|\pi|)$ time without reconstructing the full parse forest

The **witness interface** is the innovation: rather than storing all parse trees, LinIndex stores enough annotation to reconstruct any requested witness on-demand.

## Applications in Engineering

### 1. **Static Analysis & Program Verification**
LinIndex accelerates interprocedural dataflow analysis when the dataflow specification is naturally linear (e.g., simple call-chain constraints). Typical use:
- Verify that untrusted data cannot flow to sensitive sinks
- Query: "Can value X from source S reach sink T?"
- Answer provided in $O(1)$ after linear-time preprocessing

### 2. **Configuration Validation (JSON Schemas)**
The empirical evaluation in the source material applies LinIndex to **JSON schema validation**:
- Convert JSON schemas to linear CFGs (shown to be common in practice: see Section 7)
- Index each schema against its constraint grammar in subcubic time
- Validate documents in constant time per reachability check

**Practical benefit**: Schemas from Kubernetes, Snowplow, and Washington Post benefit from this acceleration.

### 3. **Type System & Language Checking**
Syntax-guided type checkers can use LinIndex for:
- Polymorphic type resolution under grammar-based constraints
- Reachability queries on type lattices encoded as linear CFGs
- Fast validation that all type assignments respect grammar rules

### 4. **Network Protocol Parsing & Validation**
Protocol specifications (e.g., HTTP, DNS) often have linear structure:
- Query whether a packet sequence respects the protocol grammar
- Constant-time reachability with explicit witness (the valid parse)
- Subcubic indexing cost amortized over many packets

### 5. **Graph Reachability in Restricted Classes**
Beyond pure CFG reachability, LinIndex applies to:
- **Dyck language recognition** (balanced parentheses) on directed graphs
- Verification that control-flow graphs respect nesting invariants
- Algebraic path problems on graph families with linear structure

## Common Mistakes / Pitfalls

### 1. **Confusing "Linear Grammar" with "Linear Time"**
**Pitfall**: Assuming LinIndex runs in linear $O(n)$ time.  
**Correct understanding**: "Linear" refers to the grammar form (at most one nonterminal per rule), not the complexity. Preprocessing is $O(|P|n^2)$ quadratic in the graph, but subcubic compared to the cubic general case.

### 2. **Applicability Beyond TALNF**
**Pitfall**: Applying LinIndex to arbitrary CFGs.  
**Correct understanding**: LinIndex requires the grammar to be in **TALNF** (a specific linear normal form). Converting a general CNF to this form may be impossible; general CNF grammars require SatIndex instead.

### 3. **Ignoring the Sparse Regime Assumption**
**Pitfall**: Assuming $O(n^2)$ preprocessing scales well for all graph sizes.  
**Correct understanding**: The linear+sparse regime assumes $m = O(n