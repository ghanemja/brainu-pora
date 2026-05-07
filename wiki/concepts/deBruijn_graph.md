# deBruijn graph

## Definition

A **deBruijn graph** is a directed graph constructed from a set of strings (typically $k$-mers) where:

- **Vertices** represent all distinct $(k-1)$-mers
- **Edges** represent all distinct $k$-mers, with an edge from vertex $u$ to vertex $v$ labeled $c$ if the $(k-1)$-mer corresponding to $u$, with its last character removed and character $c$ appended, equals the $(k-1)$-mer corresponding to $v$

More formally: an edge exists from $(k-1)$-mer $u = s_1s_2\cdots s_{k-1}$ to $(k-1)$-mer $v = s_2s_3\cdots s_{k-1}c$ labeled with character $c$, representing the $k$-mer $s_1s_2\cdots s_{k-1}c$.

**Variant notation:** In some contexts (especially genomics), vertices may directly represent $k$-mers, with edges connecting overlapping $k$-mers by $(k-1)$ nucleotides of overlap.

## Key Equations

### Graph Construction
For an alphabet $\Sigma$ and $k$-mer length $k$:
- Number of possible vertices: $|\Sigma|^{k-1}$
- Number of edges in a complete graph: $|\Sigma| \cdot |\Sigma|^{k-1} = |\Sigma|^k$

### Vertex Degree
For a vertex representing $(k-1)$-mer $v$:
$$\text{in-degree}(v) = |\{c \in \Sigma : s_2\cdots s_{k-1}c = v\}|$$
$$\text{out-degree}(v) = |\{c \in \Sigma : vc' = \text{some }k\text{-mer}\}|$$

### Path Length Property
A path of length $\ell$ (containing $\ell$ edges) in the deBruijn graph represents a string of length $k + \ell - 1$ (the concatenation of overlapping $k$-mers along the path).

## Physical Intuition / Derivation

### Why deBruijn Graphs Exist

The deBruijn graph exploits a fundamental property of sequences: **overlapping redundancy**. Consider $k$-mers of length $k=3$:

$$\text{k-mers: } \{CAT, ATG, TGA, GAT\}$$

Notice that consecutive $k$-mers share $(k-1) = 2$ characters:
- $CAT$ ends with $AT$; $ATG$ begins with $AT$ → overlap
- $ATG$ ends with $TG$; $TGA$ begins with $TG$ → overlap

Rather than storing each $k$-mer independently, we can represent this as a path through shorter $(k-1)$-mers:

$$CA \to AT \to TG \to GA$$

with edges labeled: $T$, $G$, $A$ respectively, reconstructing the original sequence without duplication.

### Construction Intuition

The deBruijn graph is essentially a **suffix-prefix matching system**:
1. Extract all $(k-1)$-mers as vertices
2. For each $k$-mer, identify its prefix (first $k-1$ chars) and suffix (last $k-1$ chars)
3. Draw a directed edge from prefix-vertex to suffix-vertex

This structure naturally encodes which $k$-mers can follow one another in sequences, enabling **path-based traversal** that reconstructs longer sequences compactly.

## Applications in Engineering

### 1. **Genomic Assembly and Sequencing**
- **DNA sequence reconstruction:** Paths through deBruijn graphs correspond to assembled genome fragments. Short sequencing reads (k-mers) are assembled into contiguous sequences by finding Eulerian paths.
- **Reference-guided analysis:** Storing only k-mer spectra via spectrum-preserving string sets (SPSS) reduces memory in k-mer indexing for read mapping and variant calling.

### 2. **Metagenomic and Pangenomic Applications**
- **Multiple genome representation:** Pangenome graphs extend deBruijn structure to represent variation across multiple genome sequences simultaneously.
- **Contig compression:** Eulertigs and necklace covers (generalizations covering paths and cycles with attachments) minimize storage of k-mer spectra for multiple genomes.

### 3. **Short Tandem Repeat (STR) Detection**
- Repetitive sequences manifest as cycles in deBruijn graphs, enabling identification and quantification of STRs without explicit repeat detection.

### 4. **RNA and Protein Sequence Analysis**
- Codon usage analysis and motif discovery via k-mer enumeration in transcriptomic data.

### 5. **Bloom Filter and Probabilistic Data Structures**
- deBruijn graph-based indexing underpins scalable, memory-efficient k-mer counting structures (e.g., KMC, Jellyfish).

### 6. **Error Correction**
- Low-abundance k-mers (arising from sequencing errors) can be identified and corrected by analyzing deBruijn graph structure; true biological k-mers form larger connected components.

## Common Mistakes / Pitfalls

### 1. **Confusing Vertices and Edges with Biological Content**
Students often conflate:
- ✗ "The vertex represents a k-mer"
- ✓ "The *edge* represents a k-mer; the vertex represents a $(k-1)$-mer (the overlap region)"

This distinction is critical for understanding why paths compress sequences.

### 2. **Ignoring Multiplicity**
deBruijn graphs typically assume each k-mer appears once. When k-mers have **multiplicities** (e.g., from repetitive genomic regions or multiple sequencing reads), the graph must track edge multiplicities, not just connectivity. Failing to handle this causes information loss.

### 3. **Euler Path vs. Hamiltonian Path Confusion**
- **Eulerian path:** traverses every *edge* once (represents every k-mer once) — solvable in polynomial time
- **