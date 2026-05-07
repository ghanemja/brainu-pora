# wireframe

## Definition

A **wireframe** is a sparse, planar graph structure derived from a complex geometric intersection graph that preserves essential connectivity while dramatically reducing complexity. Formally, given an intersection graph $G$ of geometric objects in the plane, a wireframe $\tilde{H}$ is a 2-connected planar subgraph (or near-subgraph) where:

1. Each vertex $v \in V(\tilde{H})$ has a parent object $p(v) \in V(G)$, indicating that $v$ is geometrically located within $p(v)$
2. For each edge $uv \in E(\tilde{H})$, the corresponding polygonal curve connecting $u$ and $v$ can be decomposed into segments inside $p(u)$ and inside $p(v)$
3. The wireframe may have multiple vertices mapping to the same parent object
4. $|\tilde{H}|$ is significantly smaller than $|G|$: fewer edges and vertices

**Intuitive view**: Think of a wireframe as a "skeletal" representation—it extracts the topological and spatial relationships of the intersection graph while discarding redundant details about individual objects.

## Key Equations

For a face region $R$ bounded by the wireframe, the spanning property requires that for any two points $x, y$ on the North boundary:

$$d_{\text{North}}(x,y) \leq (1+\varepsilon) \cdot d_{G|_R}(x,y)$$

where $G|_R$ is the **restricted intersection graph**: all objects $v \in V(G)$ are intersected with region $R$, creating component subobjects.

**Complexity reduction**: If $G$ has $n$ vertices, the wireframe satisfies:
$$|E(\tilde{H})| = \text{poly}(1/\varepsilon) \cdot \text{SubsetTSP}(G, T)$$

where SubsetTSP bounds the traveling salesman problem on relevant object subsets.

## Physical Intuition / Derivation

### Why Wireframes Are Needed

Intersection graphs of geometric objects can be extremely dense, making exact algorithms intractable. A wireframe construction extracts only the "critical" structure:

1. **Planar skeleton first**: Identify key vertices and edges that capture topology
2. **Region decomposition**: Divide the plane into faces along wireframe edges
3. **Boundary division**: For each face, partition its boundary into two arcs (North/South) such that direct boundary paths are approximately as short as geodesics through interior objects
4. **Hierarchical refinement**: Recursively apply this decomposition to smaller regions

### Technical Challenge

When subdividing a region $R$ into $R'$ by cutting along a polygonal curve, the component count explodes: objects intersected by the cutting curve fragment into multiple pieces. Naive recursion creates exponentially many objects.

**Solution**: Carefully choose the cutting polygonal curve to minimize fragmentation—a non-trivial optimization that prevents exponential blowup in complexity.

### Spanning Property Guarantee

The wireframe construction ensures that any path $P$ between two terminals in the original graph $G$ can be approximated by a path using wireframe edges and restricted subgraph connections, with bounded distortion $(1+\varepsilon)$.

## Applications in Engineering

### 1. **Computational Geometry & Algorithm Design**
- Sparsification of geometric intersection graphs for faster shortest-path queries
- Approximation algorithms with guaranteed $(1+\varepsilon)$-optimality
- Divide-and-conquer strategies on geometric domains

### 2. **Network Routing & Planning**
- Road networks with obstacles as geometric objects (buildings, terrain)
- Wireless sensor networks with coverage regions
- Robot path planning in cluttered environments

### 3. **Mesh Generation & Finite Element Analysis**
- Creating coarse hierarchical representations of complex meshes
- Multigrid solvers: wireframe acts as coarse grid
- Reducing FEA problem size while preserving physical accuracy

### 4. **Spatial Data Structures**
- Index structures for geographic information systems (GIS)
- Quadtree/octree refinement: wireframe is a coarse level
- Efficient spatial queries on object collections

### 5. **VLSI & Circuit Design**
- Floorplan hierarchies where wireframe represents block-level topology
- Placement and routing constraints with region decomposition

## Common Mistakes / Pitfalls

### 1. **Confusing Wireframe with Subgraph**
- A wireframe is **not necessarily a subgraph** of $G$
- Multiple wireframe vertices can map to the same parent object
- ❌ Wrong: "The wireframe is just a sparse subgraph of the intersection graph"
- ✓ Correct: "It's a projection-like abstraction that may reuse objects"

### 2. **Assuming Linear Complexity**
- The $(1+\varepsilon)$ approximation parameter affects size polynomially
- Finer approximations require more wireframe vertices/edges
- ❌ Wrong: "The wireframe is always linear in the original graph size"
- ✓ Correct: "Wireframe size scales as $\text{poly}(1/\varepsilon) \cdot n$"

### 3. **Ignoring Boundary Fragmentation**
- Cutting objects along curve boundaries creates new objects
- Naive recursive subdivision causes exponential growth
- ❌ Wrong: "Each subdivision reduces size monotonically"
- ✓ Correct: "Cutting strategy must be optimized to prevent fragmentation"

### 4. **Forgetting the 2-Connectivity Requirement**
- The wireframe must be **2-connected** for the skeleton construction
- This ensures robust face decomposition and boundary division
- ❌ Wrong: "Any sparse planar graph works as a wireframe"
- ✓ Correct: "The wireframe must be 2-edge-connected for the algorithm"

### 5. **Misinterpreting the Spanning Property**
- Paths need not stay entirely in the wireframe
- They use wireframe edges **plus** shortest paths within restricted subgraphs $G|_R$
- ❌ Wrong: "All paths between terminals must lie in the wireframe"
- ✓ Correct: "Paths may traverse interior, but