# Graph Decomposition

## Definition

**Graph decomposition** is the process of partitioning a graph $G = (V, E)$ into subgraphs with specific structural properties, typically for algorithmic, analytical, or optimization purposes. In the context of parameterized complexity and kernelization, decomposition often refers to:

1. **Structural decomposition**: Breaking a graph into simpler components (e.g., connected components, tree decompositions)
2. **Modular decomposition**: Identifying vertex subsets that induce specific structural patterns
3. **Essence-preserving decomposition**: Constructing graphs whose solutions to optimization problems compose according to specific functions

More formally, given a graph $G$ and a property $\mathcal{P}$, a decomposition produces subgraphs $G_1, G_2, \ldots, G_k$ such that:
- The subgraphs collectively capture the structure relevant to $\mathcal{P}$
- Solutions in individual subgraphs can be combined to yield solutions in $G$
- The decomposition respects the problem's optimization criteria

In the source material, **essence** $\gamma: [0, d+1] \to [0, d+1]$ describes how a graph's connectivity properties compose when solutions are removed, particularly for caterpillar graphs in vertex cover problems.

## Key Equations

### Compositional Property of Essence

For decomposed graphs $C_1$ and $C_2$ merged into $C_x$, the essence satisfies:

$$\gamma(x) = \gamma_2(\gamma_1(x)) \quad \forall x \in [0, d+1]$$

where:
- $\gamma_1(x)$ = essence of component $C_1$ under constraint $x$
- $\gamma_2(y)$ = essence of component $C_2$ under constraint $y$
- $\gamma(x)$ = essence of composite graph $C_x$

### Solution Size Composition

For optimal solutions $S$ respecting degree constraint $d$:

$$|S| = \text{OPT}_d(C_1) + \text{OPT}_d(C_2)$$

This states that solutions in composed graphs decompose additively, provided the subgraph properties are preserved.

### Connected Component Constraint

For a removed vertex set $S \subseteq V$, if $Z$ denotes a connected component in $G - S$:

$$|Z| \leq d \implies \text{constraint satisfied}$$

When $|Z| > d$, the solution is infeasible across the decomposition.

## Physical Intuition / Derivation

### Why Decomposition Works

Graph decomposition exploits **locality**: many graph problems have optimal substructure where:
1. Solutions in isolated subgraphs are independently optimal
2. Interface vertices (boundaries between subgraphs) constrain how solutions interact
3. The structure of connectivity near removal sets determines feasibility

### Building Intuition with Caterpillars

A **caterpillar graph** is a tree where all vertices lie within distance 1 of a central "spine" path. The source material constructs caterpillars with prescribed essence functions:

- **Spine**: Central path defining the graph's backbone
- **Pendants**: Leaves attached to spine vertices, encoding constraint information
- **Essence**: Describes the minimal vertex removal needed to keep each connected component size $\leq d$

**Example**: A caterpillar with spine $v_1 - v_2 - v_3$ and pendants attached to $v_2$ can be decomposed into:
- Left subgraph: $v_1$ and its pendants
- Right subgraph: $v_3$ and its pendants
- Connection: $v_2$ acts as the interface

The essence $\gamma(x)$ encodes: "When I remove vertices up to size $x$ from the left component, the right component needs to remove $\gamma(x)$ vertices to maintain component-size bounds."

### Compositional Proof Strategy

The proof in the source proceeds by:

1. **Assume** $S$ is an optimal solution for composite graph $C_x = C_1 \cup C_2$
2. **Decompose** $S = (S \cap V(C_1)) \cup (S \cap V(C_2))$
3. **Verify** that $S \cap V(C_1)$ is optimal for $C_1$ with parameter $x$ (by size argument)
4. **Prove by contradiction**: If $S \cap V(C_2)$ were suboptimal for $C_2$ with parameter $\gamma_1(x)$, then connected components in $C_x - S$ would exceed size $d$ (contradiction)
5. **Conclude**: The composition law $\gamma = \gamma_2 \circ \gamma_1$ holds exactly

## Applications in Engineering

### 1. **Parameterized Algorithm Design**
- **Vertex Cover on Degree-Bounded Modifiers**: Decomposing graphs by distance to maximum-degree-$c$ subgraphs yields efficient kernels for $c \leq 2$
- **Reduction Rules**: Decomposed components enable deriving polynomial kernels (smaller equivalent problem instances)

### 2. **Network Analysis & Design**
- **Fault Tolerance**: Decomposing communication networks into subgraphs identifies critical vertices (modulators) whose removal disconnects the network
- **Hierarchical Routing**: Breaking networks into decomposed layers reduces routing complexity from global to local decisions

### 3. **VLSI & Circuit Design**
- **Placement & Routing**: Decomposing circuit hypergraphs into modules enables hierarchical placement strategies
- **Testability**: Identifying decomposable test structures reduces verification complexity

### 4. **Machine Learning & Social Networks**
- **Community Detection**: Decomposing networks into densely-connected components identifies hidden structures
- **Influence Maximization**: Computing compositions of influence functions over decomposed subnetworks

### 5. **Computational Biology**
- **Protein Interaction Networks**: Decomposing PPI graphs into functional modules predicts protein roles
- **Phylogenetic Analysis**: Tree decompositions of evolutionary graphs reconstruct ancestral structures

## Common Mistakes / Pitfalls

### 1. **Assuming Additivity Without Verification**
**Mistake**: Using $|S|