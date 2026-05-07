# Tree Containment

## Definition

**Tree containment** is the problem of determining whether an unrooted phylogenetic tree $T$ is **displayed by** (i.e., embedded in) an unrooted phylogenetic network $U$, both defined on the same leaf set $X$.

More formally: given an unrooted phylogenetic tree $T$ on leaf set $X$ and an unrooted phylogenetic network $U$ on $X$, the **Unrooted Tree Containment problem** asks whether there exists an embedding of $T$ into $U$ such that all tree edges are represented by paths in the network.

### Related Definitions

- **Split**: An $X$-split is a bipartition $X_1|X_2$ where $X_1 \cup X_2 = X$, $X_1 \cap X_2 = \emptyset$, and $|X_i| \geq 1$ for $i \in \{1,2\}$.

- **Cut-edge**: An edge $e$ in a network $U$ is a cut-edge if its removal increases the number of connected components.

- **Induced split**: A cut-edge $e$ in $U$ induces split $X_1|X_2$ if all paths between leaves in $X_1$ and leaves in $X_2$ must pass through $e$.

- **Conflicting split**: Splits $X_1|X_2$ and $Y_1|Y_2$ are **incompatible** if all four intersections $X_1 \cap Y_1$, $X_1 \cap Y_2$, $X_2 \cap Y_1$, $X_2 \cap Y_2$ are non-empty. An instance $(T, U)$ has a conflicting split if an incompatible pair exists between splits in $T$ and $U$.

## Key Equations

**Compatibility condition for splits**: Two $X$-splits $X_1|X_2$ and $Y_1|Y_2$ are compatible if and only if:
$$\text{at least one of } \{X_1 \cap Y_1, X_1 \cap Y_2, X_2 \cap Y_1, X_2 \cap Y_2\} = \emptyset$$

**Necessary condition for tree display** (Observation 12): If $(T, U)$ has a conflicting split, then $U$ does not display $T$.

## Physical Intuition / Derivation

### Why This Matters

Phylogenetic networks extend phylogenetic trees by allowing nodes with multiple parents (reticulation events), which model phenomena like horizontal gene transfer, hybridization, or recombination. However, networks must still be able to "contain" biologically plausible tree topologies.

### The Core Insight

Each edge in a tree induces a split of the leaf set—removing an edge partitions leaves into two groups. A network displays a tree only if:

1. **Every tree split is consistent with network splits**: For each edge in $T$ that partitions leaves as $Y_1|Y_2$, there must exist a cut-edge in $U$ inducing the same or a compatible split.

2. **No conflicting splits exist**: Splits that are mutually incompatible (all four intersections non-empty) cannot coexist in both $T$ and $U$.

### Why Conflicting Splits Are Fatal

If $T$ requires split $Y_1|Y_2$ but $U$ requires the incompatible split $X_1|X_2$, then no continuous embedding of $T$ into $U$ can satisfy both constraints simultaneously. This is because:
- In $T$: all leaves must stay on their side of the split edge
- In $U$: all paths between $X_1$ and $X_2$ must cross cut-edge $e$
- These requirements are geometrically incompatible

## Algorithms

**Polynomial-time verification** (Section 5.3-5.4): For 3-cuttable networks (networks where every cut yields at most 3 components), tree containment can be solved in polynomial time via:

1. **Reduction rules** that systematically simplify $(T, U)$ pairs
2. **Split consistency checking** via reduction of the instance to smaller subproblems
3. **Early termination** on conflicting splits (Observation 12)

The algorithm exploits the assumption **(A1)**: no conflicting splits exist at input.

## Applications in Engineering

### Phylogenetics & Evolutionary Biology
- **Horizontal gene transfer detection**: Networks with conflicting splits indicate evolutionary scenarios involving gene transfer
- **Hybridization analysis**: Determining whether an observed phylogenetic tree could arise from a hybrid speciation network
- **Multi-locus sequence analysis**: Reconciling gene trees (the input trees $T$) with species networks (the networks $U$)

### Network Design & Verification
- **Redundancy validation**: Checking whether specific connectivity patterns (trees) can traverse a redundant network topology
- **Protein interaction networks**: Verifying whether functional pathways (trees) are supported by known interaction networks

### Computational Biology
- **RNA secondary structure prediction**: Determining if predicted secondary structures embed in known folding networks
- **Disease pathway analysis**: Validating whether disease propagation trees are consistent with biological network models

## Common Mistakes / Pitfalls

1. **Assuming compatibility is transitive**: If $X_1|X_2$ is compatible with $Y_1|Y_2$, and $Y_1|Y_2$ is compatible with $Z_1|Z_2$, this does NOT guarantee $X_1|X_2$ is compatible with $Z_1|Z_2$. Compatibility is pairwise, not global.

2. **Confusing "displaying" with graph containment**: A network displaying a tree is NOT the same as the tree being a subgraph. The tree's edges become *paths* in the network, possibly using multiple network edges.

3. **Overlooking trivial splits**: Trivial splits ($|X_1|=1$ or $|X_2|=1$) are present in every tree/network but provide no constraint. Focusing on non-trivial splits is crucial.

4. **Forgetting bidirectionality of incompatibility**: If $X_1|X_2$ conflicts with $Y_1|Y_2$, then