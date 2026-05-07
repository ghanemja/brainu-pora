# Rotation Representation

## Definition

**Rotation representation** is a data structure that encodes the combinatorial structure of a planar graph or pseudo-triangulation by storing, for each vertex, an **ordered list of its neighboring vertices** in rotational (circular) order around that vertex.

Formally, given a vertex set $V = \{v_0, v_1, \ldots, v_{N-1}\}$, a rotation representation consists of:

$$\text{rotations} : V \to \text{List}(V \cup \{-1\})$$

where `rotations[i]` is a cyclic list of neighbors of vertex $v_i$, and the special marker $-1$ denotes the **boundary** (exterior face) of the planar embedding.

### Key Properties:
- **Cyclic ordering**: The list of neighbors is ordered circularly; the last element wraps around to the first
- **Consistency**: If vertex $b$ appears in `rotations[a]`, then vertex $a$ must appear in `rotations[b]` (symmetry requirement)
- **Planarity**: The rotation representation uniquely defines a planar embedding by specifying the cyclic order of edges around each vertex

## Key Equations

**Successor/Predecessor in rotation:**

$$\text{succ}(e) = \text{darts}[a][\text{rotations}[a][(i+1) \bmod \text{size}]]$$

$$\text{pred}(e) = \text{darts}[a][\text{rotations}[a][(i-1) \bmod \text{size}]]$$

where $e$ is a dart from vertex $a$ to vertex $b$, indexed at position $i$ in `rotations[a]`, and $\text{size} = |\text{rotations}[a]|$.

**Dart reversal (symmetry):**

$$\text{rev}(e_{ab}) = \text{darts}[b][a]$$

This enforces that if dart $e$ goes from $a$ to $b$, its reverse must exist at $b$ pointing back to $a$.

## Physical Intuition / Derivation

### Why Rotation Representation?

Planar graphs are fundamentally **2D structures**. A rotation representation captures the essential geometric information—the *cyclic ordering of edges*—without explicitly storing coordinates. This is powerful because:

1. **Planarity is implicit**: Any planar embedding is fully determined by specifying, for each vertex, the cyclic order of incident edges. No coordinates needed.

2. **Combinatorial invariant**: The rotation representation is preserved under any homeomorphism of the plane; it depends only on combinatorial structure.

3. **Efficiency**: Storing an ordered list is lightweight (linear in edges), while explicitly storing vertex coordinates would require floating-point data and precision issues.

### Dart Representation (Algorithm A.5.1)

The algorithm converts a rotation representation into a **dart structure**—a distributed representation where:
- Each directed edge (dart) $e_{ab}$ stores:
  - `head(e)`: the target vertex
  - `rev(e)`: the reverse dart $e_{ba}$
  - `succ(e)`: the next dart in cyclic order around the source vertex
  - `pred(e)`: the previous dart in cyclic order

This **doubly-linked circular structure** makes it fast to traverse faces, edges, and vertex neighborhoods.

### Example

Consider a triangle with vertices $v_0, v_1, v_2$:

```
rotations[0] = [1, 2, -1]      (v₀ neighbors: v₁, v₂, then boundary)
rotations[1] = [2, 0, -1]      (v₁ neighbors: v₂, v₀, then boundary)
rotations[2] = [0, 1, -1]      (v₂ neighbors: v₀, v₁, then boundary)
```

This defines a planar triangle where the circular ordering matches a counterclockwise orientation.

## Applications in Engineering

### 1. **Computational Geometry & Mesh Processing**
- **Planar triangulation/pseudo-triangulation**: Computing constrained Delaunay triangulations and pseudo-triangulations (as in the source material)
- **Face enumeration**: Walking around faces of a planar subdivision
- **Topological analysis**: Detecting holes, genus, and connected components without coordinate data

### 2. **Graph Algorithms on Planar Graphs**
- **Planarity testing**: Certifying that a graph is planar by constructing a valid rotation representation
- **Planar separator algorithms**: Recursive decomposition leveraging planar structure
- **Dual graph construction**: Automatically deriving the dual graph from rotation data

### 3. **Robotics & Polygon Decomposition**
- **Configuration space analysis**: Representing pseudo-triangulations for motion planning in 2D environments
- **Visibility graphs**: Computing line-of-sight networks for path planning

### 4. **CAD/VLSI Design**
- **Topology-preserving data structures**: Maintaining planar subdivisions as layouts are edited
- **Region connectivity**: Tracking adjacency of polygonal regions without floating-point errors

### 5. **Combinatorial Topology**
- **Reducible configuration detection**: Finding homomorphic images and simplifying configurations (as in Section A.6 of the source)
- **Combinatorial equivalence**: Comparing planar graphs up to homotopy

## Common Mistakes / Pitfalls

### 1. **Forgetting Symmetry Constraints**
**Error**: Storing a neighbor in `rotations[a]` without ensuring the reverse relationship in `rotations[b]`.

**Fix**: Algorithm A.5.1 explicitly checks (line 24):
```
if darts[b][a] == nil then
    raise error  ← discrepancy detected
```

### 2. **Confusing Cyclic with Linear Indexing**
**Error**: Treating `rotations[i]` as a linear array without wrapping; failing to connect the last element back to the first.

**Fix**: Use modular arithmetic:
```
next_idx = (i + 1) % size
prev_idx = (i - 1 + size) % size
```

### 3. **Ignoring the Boundary Marker**