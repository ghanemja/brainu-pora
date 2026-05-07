# Euler Tour

## Definition

An **Euler tour** is a traversal of a tree or graph that visits every edge exactly once, typically in a depth-first manner. In the context of preprocessing for efficient queries (particularly lowest common ancestor problems), an **Euler tour** refers to a linearization of a rooted tree obtained by recording nodes in the order they are visited during a DFS traversal, including repeated visits when backtracking.

More formally, given a rooted tree $T = (V, E)$, an Euler tour produces a sequence $\text{ET}$ of length $2|V| - 1$ where:
- Each node $v \in V$ appears when first visited (entering) and when all its descendants are processed (exiting)
- The sequence respects the parent-child relationships in $T$

## Key Equations

**Euler Tour Length:**
$$|\text{ET}| = 2|V| - 1$$

where $|V|$ is the number of nodes in the tree.

**LCA Query Reduction (via Euler Tour + RMQ):**
For nodes $u$ and $v$ in a tree, their lowest common ancestor is the node with minimum depth in the Euler tour segment between the positions of $u$ and $v$:

$$\text{LCA}(u, v) = \arg\min_{w \in \text{ET}[p_u : p_v]} \text{depth}(w)$$

where $p_u$ and $p_v$ are the first occurrence positions of $u$ and $v$ in the Euler tour.

**Query Complexity:**
- Preprocessing: $O(n)$ time
- Query: $O(1)$ time (with Range Minimum Query preprocessing)

## Physical Intuition / Derivation

### Why Euler Tour Works

The key insight is that **ancestor-descendant relationships in a tree correspond to containment in the Euler tour**. When you perform DFS:

1. **Entering a node** — mark its first occurrence
2. **Leaving a node** — mark its last occurrence
3. All descendants of a node appear between its first and last occurrence

### Construction Algorithm

```
procedure DFA-EULER-TOUR(node v, parent p):
    APPEND v to ET                    // entering v
    for each child c of v:
        DFA-EULER-TOUR(c, v)
    APPEND v to ET                    // exiting v (optional, for full Euler tour)
```

### Why This Reduces LCA to RMQ

The **Lowest Common Ancestor** of two nodes $u$ and $v$ is the **shallowest node in the Euler tour** between their positions. This is because:

- Any path from $u$ to $v$ must pass through their LCA
- The LCA is the only node in that segment with the minimum depth
- Finding this minimum becomes a **Range Minimum Query (RMQ)** problem

With RMQ preprocessed via a data structure (e.g., sparse table), LCA queries drop from $O(\log n)$ to $O(1)$.

## Applications in Engineering

### 1. **Graph Analysis & Variation Graphs** (Genomic)
In the source context, Euler tours + LCA queries efficiently identify **ultrabubbles** in variation graphs:
- Detects structural variants in genomic data
- Complexity reduced from $O(K(n + m))$ to $O(Kn)$ where $K$ is the number of snarls
- Critical for bioinformatics pipelines processing large genome graphs

### 2. **Network Connectivity & Routing**
- Preprocessing rooted network topologies for fast ancestor queries
- Edge routing in hierarchical network designs

### 3. **Lowest Common Ancestor (LCA) Queries**
- **Phylogenetic trees**: Finding most recent common ancestors
- **File systems**: Determining common parent directories
- **Semantic networks**: Identifying conceptual relationships

### 4. **Dynamic Graph Processing**
- Preprocessing static tree structures to answer structural queries in constant time
- Foundation for more complex problems (path queries, distance queries, LCA variants)

### 5. **Compiler Optimization**
- Dominant tree analysis in control flow graphs
- Fast dominator tree queries

## Common Mistakes / Pitfalls

### 1. **Confusing Euler Tour with Euler Path**
- **Euler path/circuit**: visits every *edge* exactly once (classic graph problem, different constraints)
- **Euler tour (in this context)**: visits every *node* in a specific order during DFS

### 2. **Forgetting Preprocessing Cost**
- While Euler tour construction is $O(n)$, RMQ preprocessing adds overhead
- For one-off queries, naive LCA may be faster; Euler tour shines with many queries

### 3. **Assuming Arbitrary Graph Support**
- Euler tours work cleanly on **rooted trees**
- Applying to DAGs or general graphs requires care (linearization may not preserve ancestor-descendant relationships correctly)

### 4. **Overlooking Space Complexity**
- Euler tour requires $O(n)$ extra space for the linearization
- RMQ sparse table adds $O(n \log n)$ space
- May be prohibitive for very large trees

### 5. **Misapplying to Unrooted Graphs**
- Tree must be explicitly rooted for depth/ancestor semantics to work
- Choosing wrong root invalidates ancestor relationships

## See Also

- [[Lowest Common Ancestor (LCA)]] — primary application; finding nearest common ancestor in rooted trees
- [[Range Minimum Query (RMQ)]] — data structure that pairs with Euler tour for $O(1)$ LCA queries
- [[Depth-First Search (DFS)]] — fundamental traversal used to construct Euler tours
- [[Lowest Common Ancestor with Binary Lifting]] — alternative LCA approach with $O(\log n)$ queries, $O(n \log n)$ prep
- [[Snarl Detection]] — application domain mentioned in sources; identifying structural bubbles in variation graphs

## Sources

- Paten et al. (referenced as [2] in source) — hierarchical snarl decomposition algorithm
- Section 7.4 source material — RMQ–Euler tour combination technique for LCA
- Methods section on variation graph processing — practical implementation context