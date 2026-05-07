# de Bruijn graphs

## Definition

A **de Bruijn graph** of order $k$ over an alphabet $\Sigma$ is a directed multigraph $G = (V, E)$ where:

- **Vertices** are all distinct strings (nodes) of length $k-1$ over $\Sigma$
- **Edges** represent strings of length $k$: an edge from node $u$ to node $v$ labeled with symbol $c$ exists if the last $k-2$ characters of $u$ concatenated with $c$ equals $v$

Equivalently, an edge from $u = s_1s_2\cdots s_{k-1}$ to $v = s_2s_3\cdots s_{k-1}c$ represents the $k$-mer $s_1s_2\cdots s_{k-1}c$.

**In sequence assembly contexts:** A de Bruijn graph of order $k$ is constructed from a collection of $k$-mers (length-$k$ substrings). Each distinct $k$-mer contributes one directed edge, where:
- The source node is the $(k-1)$-prefix of the $k$-mer
- The target node is the $(k-1)$-suffix of the $k$-mer
- Edge multiplicity equals the frequency of the $k$-mer in the input

## Key Equations

For a $k$-mer string $s = c_1c_2\cdots c_k$:

$$\text{source}(s) = c_1c_2\cdots c_{k-1}$$
$$\text{target}(s) = c_2c_3\cdots c_k$$

**Eulerian trail correspondence:** In a de Bruijn graph, an Eulerian trail (path traversing every edge exactly once) corresponds to a sequence that contains every $k$-mer in the input exactly once as a substring.

For a sequence of length $L$ containing all edges (where $m = $ total number of $k$-mer occurrences):
$$L = m + k - 1$$

This is because each edge adds one new character beyond the overlap with previous characters.

## Physical Intuition / Derivation

### Why de Bruijn Graphs?

The key insight is **overlap encoding**: rather than storing full strings, we encode the information content in edges. This dramatically reduces space and computational complexity.

**Example (DNA sequencing):** Suppose we have $k$-mers: `ACGT`, `CGTA`, `GTAA`, `TAAC`

| $k$-mer | Source (prefix) | Target (suffix) |
|---------|-----------------|-----------------|
| ACGT    | ACG             | CGT             |
| CGTA    | CGT             | GTA             |
| GTAA    | GTA             | TAA             |
| TAAC    | TAA             | AAC             |

This creates a chain:
```
ACG → CGT → GTA → TAA → AAC
 |     |     |     |
 +-----+-----+-----+  (edges represent k-mers)
```

An Eulerian trail through all edges produces: `ACGTAAC` (length $4 + 3 - 1 = 6$), which contains all four 4-mers exactly once.

### Why Multigraphs?

In real applications (genome assembly, data analysis), the same $k$-mer often appears multiple times. A **directed multigraph** allows parallel edges with identical endpoints but different frequencies, directly encoding repetition without duplication of nodes.

## Applications in Engineering

### 1. **Genomics & Sequence Assembly**
The primary application: short DNA reads from sequencing machines contain overlapping $k$-mers. Building a de Bruijn graph and finding Eulerian trails reconstructs the original DNA sequence(s). The frequency of each $k$-mer edge encodes sequencing depth and helps detect copy number variations.

### 2. **Data Compression & Graph Compression**
De Bruijn graphs compactly represent string collections. Instead of storing all strings, store the graph structure; traversals recover original data. Useful for:
- Indexed sequence databases
- Repetitive pattern detection
- Lossless compression of string sets

### 3. **Privacy & Anonymization**
Enumerate candidate reconstructions from aggregate data (e.g., Eulerian trails representing possible individual records in differentially-private datasets). The enumeration of distinct node-sequences corresponds to distinct possible outputs.

### 4. **De Novo Assembly Algorithms**
Industrial tools (SPAdes, Velvet, SOAPdenovo) use de Bruijn graphs with:
- Multiple values of $k$ for robustness
- Error correction via variant enumeration
- Bubble detection (alternate paths representing sequencing errors)

### 5. **Graph Pattern Enumeration**
More generally, de Bruijn graphs support efficient enumeration of distinct paths satisfying length or edge-frequency constraints.

## Common Mistakes / Pitfalls

### **Mistake 1: Confusing Nodes with $k$-mers**
**Wrong:** "Nodes represent $k$-mers."  
**Right:** Nodes represent $(k-1)$-mers; *edges* represent $k$-mers. This is crucial for understanding multiplicity and assembly length formulas.

### **Mistake 2: Assuming Edge-Distinct = Node-Distinct**
In simple graphs, these coincide. In **multigraphs**, multiple edges between the same pair of nodes produce different edge sequences but identical node sequences. For assembly, **node-distinctness** is usually relevant (different assemblies = different DNA sequences), while edge-distinctness may count the same assembled sequence multiple times.

### **Mistake 3: Forgetting Multiplicity**
Treating multi-edges as single edges ignores frequency information. In genomics, edge multiplicity = $k$-mer abundance; losing it destroys information about coverage depth and polymorphisms.

### **Mistake 4: Ignoring Directionality**
De Bruijn graphs are *directed*. The edge $u \to v$ is distinct from $v \to u$. This matters for DNA strand orientation and ensures prefix-suffix overlaps work correctly.

### **Mistake 5: Assuming All Eulerian Trails Exist**
Only graphs where every node has equal in-degree and out-degree (Eulerian condition)