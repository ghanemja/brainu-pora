# Graph Embedding

## Definition

A **graph embedding** is an assignment of vertices and edges of a graph $G = (V, E)$ to a geometric space (typically the plane or sphere) such that:

1. Each vertex $v \in V$ is mapped to a distinct point in the space
2. Each edge $uv \in E$ is mapped to a continuous curve connecting the corresponding vertex positions
3. Edges intersect only at their endpoints (in a *planar embedding*)

For planar graphs, an embedding partitions the plane into connected regions called **faces**. A **triangulation** is a planar embedding where every face (except possibly the outer/infinite face) is bounded by exactly three edges.

### Formal Characterization

For a triangulation $G$ with $|V| = n$ vertices, the **extended degree-bounded ball** $\overline{B}^d_r(v)$ denotes the induced subgraph of all vertices within graph distance $r$ from vertex $v$, restricted to vertices of degree $\leq d$. This local neighborhood structure completely determines discharge rules and charge propagation along incident edges.

## Key Equations

**Charge Distribution Bound (Lemma 6.1):**
$$T(v) \leq 60 - 2 \cdot d_G(v)$$

where:
- $T(v)$ is the final charge at vertex $v$
- $d_G(v)$ is the degree of $v$ in embedding $G$

**Consequence:**
$$T(v) \leq 54 \text{ (for all valid triangulations)}$$

**Restricted Discharge Bound (Lemma 7.2):**

Without obstructing cycles or reducible configurations in $\overline{B}^8_2(v)$:
$$\varphi(u, v) \leq 5$$

With no restrictions (arbitrary triangulation):
$$\varphi(u, v) \leq 8$$

where $\varphi(u, v)$ is the charge sent along directed edge $u \to v$.

**Degree-Aware Bound:**
$$T(v) \leq -\frac{2}{31} d_G(v) \quad \text{if } d_G(v) \geq 31$$

## Physical Intuition / Derivation

### Why Embeddings Matter

A planar embedding *rigidifies* abstract graph structure into geometric form. This is crucial because:

- **Local geometry constrains global properties:** The planarity constraint (no edge crossings) severely limits which edges can exist near a vertex
- **Charge discharging models structural balance:** The framework models how "charge" (excess or deficit relative to some target) redistributes through local interactions
- **Degree-bounded neighborhoods suffice:** Remarkably, rules involving only vertices within distance 2 with degree $\leq 8$ can enforce global bounds

### The Discharging Method

The source material uses a **discharging framework**:

1. **Initial charge assignment:** $T_0(v) = 10(6 - d_G(v))$ distributes charge inversely to degree
2. **Local rules (Figure 6):** Vertices apply rules to send charge along edges to neighbors, based on local topology patterns
3. **Maximal charge flow:** Through orientation-aware rule application, charge $\varphi(u,v)$ flows along each edge $uv$
4. **Final bound:** The maximum final charge $T(v) = T_0(v) + \sum_u (\varphi(u,v) - \varphi(v,u))$ is bounded

**Key insight:** Lemma 6.4 proves that all discharge along edges incident to $v$ depends only on the structure in $\overline{B}^8_2(v)$—the 2-hop neighborhood with degree bound 8. This **locality property** makes computer-assisted verification feasible.

### Why the Specific Bounds?

- The bound $\varphi(u,v) \leq 8$ for arbitrary triangulations is discovered via exhaustive computer search over all possible combinations of discharging rules
- The bound $\varphi(u,v) \leq 5$ when local obstructing structures are absent is stronger, reducing the solution space
- The threshold $d_G(v) \geq 31$ emerges because high-degree vertices can receive charge from many neighbors; the bound transitions from a constant to a degree-dependent form

## Applications in Engineering

### Graph Planarity Testing & VLSI Design
- **Circuit layout:** Determining if a circuit graph can be routed without wire crossings is fundamentally a planarity testing problem
- **Layer assignment:** Minimizing the number of physical layers in multi-layer PCBs relies on understanding planar embeddings

### Mesh Generation & Finite Element Analysis
- **Triangulation quality:** Engineers select triangulations with bounded vertex degree to ensure numerical stability in FEM solvers
- **Adaptive refinement:** Embedding theory guides how to subdivide meshes while maintaining geometric constraints

### Graph Drawing & Visualization
- **Orthogonal layouts:** Algorithms for drawing graphs with minimal edge crossings use embedding properties
- **Network visualization:** Social networks and dependency graphs leverage planarity to reduce cognitive load

### Approximation Algorithms for Hard Problems
- **Graph coloring:** The discharging method (from which these lemmas derive) originally proved the **Four Color Theorem**
- **Structural graph theory:** Bounds on local structure enable divide-and-conquer approximations for NP-hard problems (e.g., vertex cover, independent set in bounded-degree graphs)

### Computational Geometry
- **Voronoi/Delaunay diagrams:** Triangulation embeddings of point sets drive spatial data structures for collision detection and proximity queries
- **Surface parameterization:** 3D mesh embedding onto 2D domains uses local angle/area distortion bounds analogous to charge constraints

## Common Mistakes / Pitfalls

### 1. **Confusing the Graph with Its Embedding**
- ❌ "A graph is planar" → Often means "a planar *embedding* exists," not "this particular layout is planar"
- ✓ A single abstract graph may have multiple non-equivalent planar embeddings

### 2. **Assuming All Discharging Rules Are Symmetric**
- ❌ Applying rules in both directions uniformly ignores orientation
- ✓