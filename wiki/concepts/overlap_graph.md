# Overlap Graph

## Definition

An **overlap graph** is a directed weighted graph used to represent the overlapping relationships between a set of strings (typically DNA sequences or similar biological sequences). Given a string set $S = \{s_1, s_2, \ldots, s_n\}$, the overlap graph $G_{\text{ov}}(S)$ is constructed as follows:

- **Vertices**: Each string $s_i \in S$ corresponds to a vertex in the graph
- **Edges**: A directed edge exists from vertex $u$ to vertex $v$ if the suffix of $\text{str}(u)$ overlaps with the prefix of $\text{str}(v)$
- **Edge Weights**: Each edge $(u, v)$ is weighted by $\text{ov}(\text{str}(u), \text{str}(v))$, representing the length of the maximum overlap between the strings

In genomic applications, the overlap graph accounts for **reverse complements** by treating each string $s$ with two oriented copies: $s^+$ (the string itself) and $s^-$ (its reverse complement $\text{rc}(s)$). This creates an augmented vertex set $\tilde{S} = \{s^+ \mid s \in S\} \cup \{s^- \mid s \in S\}$.

## Key Equations

**Overlap function** between strings $u$ and $v$:
$$\text{ov}(u, v) = \max\{k \geq 0 : u[|u|-k+1:|u|] = v[1:k]\}$$

where $u[i:j]$ denotes the substring from position $i$ to $j$.

**Bipartite representation** for cycle cover computation:
The overlap graph is transformed into a bipartite graph $\tilde{G} = (V_{\text{out}}, V_{\text{in}}, \tilde{E}, w)$ where:
- $V_{\text{out}} = \{u^{\text{out}} \mid u \in \tilde{S}\}$ (outgoing edge endpoints)
- $V_{\text{in}} = \{u^{\text{in}} \mid u \in \tilde{S}\}$ (incoming edge endpoints)
- $\tilde{E} = (V_{\text{out}} \times V_{\text{in}}) \setminus \bigcup_{u \in \tilde{S}} \{(u^{\text{out}}, u^{\text{in}}), (u^{\text{out}}, \bar{u}^{\text{in}})\}$
- $w(u^{\text{out}}, v^{\text{in}}) = \text{ov}(\text{str}(u), \text{str}(v))$

The constraint that vertices $u^{\text{out}}$ and $\bar{u}^{\text{in}}$ cannot be matched simultaneously is enforced via auxiliary gadget edges with zero weight.

## Physical Intuition / Derivation

### Why Overlap Graphs Matter

In DNA sequence assembly, the fundamental problem is to reconstruct long sequences from shorter overlapping fragments (reads). Each read can be represented as a vertex, and an overlap graph encodes which reads can be connected based on their sequence similarity.

### From Overlaps to Paths

When we find an edge from read $u$ to read $v$ with high overlap weight, this suggests that:
1. The suffix of $u$ matches the prefix of $v$
2. They likely represent consecutive or near-consecutive positions in the original genome
3. Concatenating them (removing the overlap) produces a merged sequence

A **path** through the overlap graph corresponds to a sequence of reads that can be assembled into a longer contig.

### The Cycle Cover Problem

Rather than finding simple paths, cycle covers are used because:
1. They guarantee efficient handling of circular genomes or plasmids
2. A **maximum-weight cycle cover** simultaneously decomposes the graph into disjoint cycles with maximum total overlap weight
3. Each cycle represents an independent reconstructed sequence

### Reverse Complement Handling

Biological DNA strands have two complementary orientations. By creating two vertices for each string ($s^+$ and $s^-$), the algorithm can:
- Consider both forward and reverse readings of each sequence
- Maintain uniformity in constraint handling
- Enforce that exactly one orientation is selected via the constraint: for each $u \in \tilde{S}$, either $(u^{\text{out}}, u^{\text{in}})$ is matched OR $(\bar{u}^{\text{out}}, \bar{u}^{\text{in}})$ is matched, but not both

### Relaxation via Auxiliary Gadgets

The direct constraint (cases (i) and (ii)) is NP-hard to enforce directly in a matching formulation. Instead:
1. A weaker constraint is imposed: $u^{\text{out}}$ and $\bar{u}^{\text{in}}$ cannot be simultaneously matched
2. Auxiliary vertices $x_u$ with zero-weight edges are introduced as "stopgaps"
3. Computing a maximum-weight perfect matching in the augmented graph $G'$ (via general graph matching algorithms) provides a valid solution
4. The relaxation ensures the solution weight $\geq$ the optimal cycle cover weight

## Applications in Engineering

### Genomic Assembly
- **DNA sequence reconstruction**: Converting millions of short reads (from sequencing machines) into contiguous sequences (contigs)
- **Microbial genome finishing**: Completing genomes of bacteria and archaea with limited computational resources
- **Metagenomic assembly**: Assembling sequences from complex microbial communities

### Sequence Alignment and Comparison
- **Identifying gene homology**: Finding overlapping sequences across species to infer evolutionary relationships
- **Quality control in sequencing**: Detecting and filtering erroneous reads based on overlap consistency

### RNA and Protein Engineering
- **EST (Expressed Sequence Tag) clustering**: Grouping partial cDNA sequences into genes
- **Protein domain identification**: Finding overlapping structural domains across protein families

### Graph-Based Data Compression
- **De Bruijn graph simplification**: Overlap graphs can be converted to de Bruijn graphs for memory-efficient representation
- **Reference-free compression**: Exploiting overlap structure in sequences without requiring a reference genome