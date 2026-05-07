# Feedback Morse Order

## Definition

A **feedback Morse order** is a total ordering of vertices in a graph $G = (V, E)$ that partitions edges into two classes: **forward edges** (connecting vertices ordered earlier to later ones) and **backward edges** (connecting vertices ordered later to earlier ones). The ordering is *feedback* in the sense that it classifies edges relative to a directional ordering, enabling the identification of a feedback edge set (or equivalently, an acyclic subgraph after removing backward edges).

In the context of optimal Morse matching on complexes with bounded treewidth, a feedback Morse order $g$ on a subgraph $G_t$ is compatible with a state $(g, U)$ where:
- $g$ is the total order on vertices
- $U$ is the set of matched vertices
- The ordering must respect local matching constraints: each vertex is matched to at most one incident edge, and that edge must be backward in $g$

## Key Equations

For a feedback Morse order $g$ on graph $G_t$ with vertex set $V_t$, define:
$$\text{Forward}(g) = \{(u,v) \in E_t : u <_g v\}$$
$$\text{Backward}(g) = \{(u,v) \in E_t : v <_g u\}$$

The cost function for a state $(g, U)$ is:
$$c[t, g, U] = \min_{\text{compatible order extensions}} \sum_{v \in V_t \setminus U} \omega(v)$$

where $\omega(v)$ is the weight of unmatched vertex $v$, and the minimization is over all extensions of the order $g$ compatible with matching constraint $U$.

For a set $MI(g)$ of forced matched vertices (determined by backward edges within a bag at a join node):
$$MI(g) = \{u \in X_t : \exists v \in X_t \text{ with } (u,v) \in \text{Backward}(g) \text{ and } u, v \text{ both in bag } X_t\}$$

Feasibility at a join requires:
$$MI(g) \subseteq U_{\text{parent}} \quad \text{and} \quad MI(g) \subseteq U_{\text{child}_1}, U_{\text{child}_2}$$

## Physical Intuition / Derivation

### Why Ordering Matters for Matching

A Morse matching on a complex is a matching (set of disjoint edges) where each matched edge is oriented in a consistent direction relative to an acyclic function on vertices. The feedback Morse order operationalizes this: by imposing a total order, we canonically assign a direction to every edge. Backward edges (opposite to the order direction) become *candidates* for the matching, while forward edges cannot participate.

### Tree Decomposition Strategy

The algorithm processes a nice tree decomposition bottom-up, maintaining for each bag $X_t$ a DP table $c[t, g, U]$ representing:
- The vertex order $g$ restricted to the bag
- The current matching $U$ on those vertices
- The minimum weight of unmatched vertices

At each bag operation, the algorithm:

1. **Leaf**: Initializes with empty order, empty matching, cost 0
2. **Introduce-vertex**: Adds a new vertex $v$ to the order; must decide insertion position in $g$ (cost unchanged since $v$ is unmatched initially)
3. **Introduce-edge**: When edge $(u,v)$ appears:
   - If forward in $g$: cannot ever be backward in extensions, so ineligible for matching
   - If backward in $g$: *must* be in the matching; both endpoints transition from unmatched to matched
4. **Forget-vertex**: When $v$ leaves the bag, its matching status is final; if unmatched, incur cost $\omega(v)$
5. **Join**: Merge two subtrees with the same bag; enforce that no vertex outside $MI(g)$ is matched in both subtrees (since separated subtrees have no edges between them)

### Why This Works

The feedback Morse order decouples the matching decision from the full graph structure. Within a bag, the order determines which edges *must* be backward (and thus matchable); the DP selects the best matching subject to this constraint. Acyclicity is automatically preserved: extending a feedback Morse order remains a feedback Morse order, so acyclicity at the complex level is guaranteed by construction.

## Applications in Engineering

### 1. **Topology Optimization in Computational Homology**
Morse matchings reduce the complexity of simplicial complexes by collapsing matched cells, accelerating homology computation. Feedback Morse orders with bounded treewidth enable efficient reduction of large geometric meshes in CAD and scientific computing.

### 2. **Circuit and Network Design**
In graph-based circuit netlists or network topologies with tree-like structure, feedback Morse orders identify essential (unmatched) components while abstracting matched pairs, supporting hierarchical design and analysis.

### 3. **Parametrized Algorithm Design**
The treewidth-dependent complexity analysis (ETH-tight under Exponential Time Hypothesis) informs the design of solvers for bounded-treewidth instances in constraint satisfaction, planning, and discrete optimization problems that model feedback relationships.

### 4. **Mesh and Skeleton Analysis**
In shape analysis and skeleton extraction, Morse matchings simplify the connectivity graph while preserving critical topological features, enabling efficient data reduction in 3D modeling pipelines.

## Common Mistakes / Pitfalls

1. **Confusing forward/backward with edge direction**: A feedback Morse order is not the same as orienting the graph. The order is a total ranking of *vertices*; edges inherit directionality from this ranking, but the graph itself may be undirected.

2. **Forgetting the feasibility check on join**: Students often overlook that $MI(g)$ (edges forced backward by the bag order) must be matched in *both* child states and the parent. Neglecting this causes infeasible states to propagate.

3. **Thinking order extends arbitrarily**: When introducing a new vertex, inserting it at different positions in the order $g$ can change which edges become backward, affecting future matching decisions. The order is part of the state, not a free choice at the end.

4