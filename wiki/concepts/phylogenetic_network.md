# Phylogenetic Network

## Definition

A **phylogenetic network** is a directed acyclic graph (DAG) that represents evolutionary relationships among species or sequences, generalizing the concept of a phylogenetic tree to allow for non-tree-like evolutionary processes such as:
- Horizontal gene transfer
- Hybridization
- Recombination
- Reticulate evolution

Formally, a phylogenetic network $N$ on a set of taxa $X$ is:
- A rooted DAG with root $\rho$
- Leaf set equal to $X$ (taxa labels)
- Every non-leaf, non-root vertex has in-degree + out-degree ≥ 3 (binary condition relaxed)
- **Reticulation vertices**: nodes with in-degree ≥ 2, representing points where evolutionary lineages merge (inheritance from multiple sources)
- **Tree vertices**: nodes with in-degree = 1

### Tree-Child Networks

A critical subclass is the **tree-child network**, which satisfies:

$$\text{Every non-leaf vertex has at least one child that is either a leaf or a reticulation}$$

This constraint ensures that non-treelike events (reticulations) are "resolved" by subsequent tree-like evolution, making the network interpretable as a valid evolutionary history.

### Unrooted Phylogenetic Networks

An **unrooted phylogenetic network** $U$ is an undirected graph representation where the root is not specified. A **tree-child orientation** $N$ of $U$ is a rooted orientation of its edges that:
1. Respects the DAG structure (acyclicity)
2. Satisfies the tree-child property for all non-leaf vertices
3. Creates a valid rooted phylogenetic network from the undirected skeleton

## Key Equations

### Network Properties

For a phylogenetic network $N$ with $|X| = n$ taxa:

$$\text{Cyclomatic complexity} = |E| - |V| + 1$$

where $|E|$ is the number of edges and $|V|$ is the number of vertices. For a tree: cyclomatic complexity = 0. For networks: complexity ≥ 1, with each reticulation contributing 1 to complexity.

$$\text{Number of reticulations} = r = |E| - |V| + 1$$

### Reticulation Gadget Orientation

In formal constructions (e.g., SAT reductions), the orientation of edges through gadgets must satisfy:

For a connection gadget $G_i$ with terminals $s$ (source/s-terminal) and $t$ (target/t-terminal):

$$\text{Either } s \to t \text{ (directed path) or } t \to s \text{ (reverse path)}$$

The tree-child property forces exactly one of these orientations to be consistent with the global network structure.

## Physical Intuition / Derivation

### Why Tree-Child Networks Matter

Phylogenetic trees assume **no reticulation**: each species has exactly one parent (uniparental inheritance). Tree-child networks relax this assumption while maintaining biological realism:

1. **Hybridization**: Two species interbreed → offspring inherits from two parents (reticulation)
2. **Horizontal gene transfer**: A gene is transferred between distantly related organisms, creating non-vertical inheritance
3. **Recombination**: Different genomic regions have different evolutionary histories

The tree-child property is critical because:
- **Computational tractability**: Ensures polynomial-time inference is possible
- **Evolutionary interpretation**: Non-tree events don't propagate indefinitely; they're "absorbed" into the tree structure
- **Identifiability**: Reticulations represent genuine evolutionary events, not artifacts of the model

### Construction Via Reticulation Gadgets

The source material describes a formal construction where:
- **Reticulation gadgets** encode the choice of which lineage receives gene flow
- **Connection gadgets** $G_i^1, G_i^2$ link the structure to biological variables (e.g., in SAT problems)
- **Orientation constraints**: The directed edges must form an acyclic network where each vertex's children respect the tree-child property

The acyclicity guarantee follows from:
$$\text{No vertex can have both parents and descendants in a way that creates a cycle}$$

In the construction, edges within gadgets are oriented consistently (e.g., $l_j^k \to t_j^k$ always), preventing cycles.

### Truth Assignment Correspondence

In reductions (e.g., SAT to phylogenetic network problems), a truth assignment $\beta$ determines network structure:

$$x_i = \text{T} \iff v_i^1 \text{ and } v_i^2 \text{ are both reticulations in } N$$

This bijection shows that certain **phylogenetic network properties are NP-complete** to compute.

## Applications in Engineering

### 1. **Bioinformatics & Evolutionary Biology**
- **Viral phylogenetics**: Reconstruct HIV/SARS-CoV-2 evolution with recombination
- **Microbial genomics**: Model horizontal gene transfer in bacteria and archaea
- **Plant evolution**: Represent polyploidy and hybridization events

### 2. **Computational Biology**
- **Haplotype inference**: Resolve conflicting genetic signals from recombination
- **Ancestral sequence reconstruction**: Infer gene sequences at reticulation nodes
- **Species tree inference**: Estimate species relationships when gene trees conflict

### 3. **Network Algorithms**
- **Complexity analysis**: Tree-child networks enable exponential-time algorithms that are optimal under complexity assumptions (e.g., FPT parameterized by reticulations)
- **SAT solvers and reductions**: Phylogenetic network problems reduce to/from NP-complete problems, informing algorithm design

### 4. **Data Structure Design**
- **Compact encodings**: Represent networks with $n$ taxa and $r$ reticulations using $O(n + r)$ space
- **Query answering**: Tree-child property enables efficient LCA (lowest common ancestor) queries on reticulation-containing networks

### 5. **Medical & Epidemiology**
- **Pathogen evolution**: Track recombinant strains in infectious disease outbreaks
- **Cancer genomics**: Model clonal evolution with horizontal gene transfer events

## Common