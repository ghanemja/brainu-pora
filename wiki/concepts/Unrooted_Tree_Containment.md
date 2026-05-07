# Unrooted Tree Containment

## Definition

**Unrooted Tree Containment** is a computational decision problem that asks: given an unrooted phylogenetic tree $T$ on leaf set $X$ and an unrooted phylogenetic network $U$ on the same leaf set $X$, does the network $U$ **display** (or contain) the tree $T$?

Formally, an instance is the tuple $(T, U)$. The problem asks whether there exists an **embedding** $\varphi$ of $T$ into $U$ such that:
- Each leaf of $T$ maps bijectively to the corresponding leaf in $U$
- Each edge of $T$ maps to a path (sequence of edges) in $U$
- The mapping respects the tree structure—specifically, edge-disjoint path mappings must compose correctly

A network $U$ **displays** tree $T$ if such an embedding exists, making $(T, U)$ a **yes-instance**; otherwise it is a **no-instance**.

---

## Key Equations

The problem is typically parameterized by:
- **Leaf set cardinality**: $|X| = n$ (number of leaves)
- **Network properties**: A network $U$ is **simple 3-cuttable** if every cut (edge removal) produces at most 3 connected components, and contains no "cherry" (adjacent leaves connected to the same internal vertex that is a cut-vertex)
- **Entangled path uniqueness** (Lemma 17): For a yes-instance, the path $P^* = \varphi(\{x,p\}) \circ \varphi(\{p,y\})$ between images of cherry $(x,y)$ through parent $p$ is **unique** in $U$

The embedding must preserve the compositional structure:
$$P^* = \varphi(e_1) \circ \varphi(e_2) \circ \cdots \circ \varphi(e_k)$$
where $e_1, e_2, \ldots, e_k$ are edges of $T$ along a path, and $\circ$ denotes path concatenation.

---

## Physical Intuition / Derivation

### Why This Problem Matters

In phylogenetics, a tree $T$ represents a **hypothesized evolutionary history** with no reticulate events (horizontal gene transfer, hybridization). A network $U$ represents a **richer evolutionary model** that may include reticulation. The containment question asks: "Can the simple evolutionary tree $T$ be explained as one possible history consistent with the more complex network $U$?"

### The Role of Cherries and Entangled Paths

A **cherry** $\{x, y\}$ is a pair of adjacent leaves in $T$ with a common parent $p$. When embedding $T$ into $U$, the images of the edges $\{x,p\}$ and $\{p,y\}$ concatenate into a single path $P^*$ in $U$. 

- **Entanglement** (technical definition in the source): A path in $U$ avoids certain problematic structures. The uniqueness of $P^*$ is crucial because it pins down where the image of $p$ must lie.
- If $P^*$ cannot be entangled (Rule 3(I)), or if a required third path (through another leaf $z$) cannot be embedded consistently (Rule 3(II)), then no embedding exists.

### Reduction Strategy (Rule 3)

The lemma describes a **reduction by edge elimination**:

1. Identify a cherry $\{x, y\}$ in $T$ with parent $p$
2. Observe that in any valid embedding, the entangled path $P^*$ from $x$ to $y$ must exist in $U$
3. Find an edge $e = \{u, w\}$ in $U$ where:
   - $u$ is on path $P^*$ (specifically, an internal vertex reached by some path from $p$)
   - $w$ is **not** involved in the mapping of any cherry-related structure
4. Remove $e$ to produce $(T, U')$: the instance has a solution iff $(T, U')$ does (statement (ii))

This reduction shrinks the problem while preserving solvability, enabling **kernelization** and fixed-parameter tractability arguments.

---

## Applications in Engineering

### 1. **Computational Biology & Phylogenetics**
   - **Sequence alignment validation**: Determine if a gene tree derived from sequence comparison is consistent with a species network inferred from multiple loci
   - **Horizontal gene transfer detection**: Networks with reticulation edges model gene transfer events; checking if simpler trees embed validates evolutionary hypotheses

### 2. **Network Reconstruction**
   - **Minimum network inference**: Among candidate networks explaining observed sequences, prefer the minimal one that displays all inferred trees
   - **Uncertainty quantification**: Bootstrap replicates of gene trees must embed in any robust species network

### 3. **Evolutionary Data Fusion**
   - **Multi-locus analysis**: Different genomic regions may suggest different trees due to incomplete lineage sorting. A network simultaneously displaying multiple trees reconciles conflicting signals

### 4. **Software Verification (Graph Isomorphism Analog)**
   - While not directly engineering, the problem is **NP-hard in general**, motivating study of **parameterized algorithms** (tractable for bounded tree width, bounded number of reticulations, small leaf counts) relevant to constraint-satisfaction and circuit-design problems

---

## Common Mistakes / Pitfalls

### 1. **Confusing Embedding with Graph Homomorphism**
   - **Mistake**: Thinking that vertices of $T$ must map injectively (one-to-one) to vertices of $U$
   - **Reality**: Vertices can map to the same vertex, but **edge paths must be vertex-disjoint** (except at endpoints). Edges of $T$ are guaranteed to map to distinct edge sequences.

### 2. **Ignoring Path Entanglement Constraints**
   - **Mistake**: Assuming any path in $U$ connecting the images of leaves suffices
   - **Reality**: Rule 3 imposes strict conditions on **how** paths can be composed. A path must be **entangled** (avoid introducing impossible cut-edges or cherries). Non-entangled paths