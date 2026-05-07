# Pseudo-triangulation

## Definition

A **pseudo-triangulation** is a combinatorial data structure representing a planar subdivision (typically a triangulation or similar geometric decomposition) through an abstract labeling system that preserves structural relationships via darts, vertices, and incidence lists.

Formally, a pseudo-triangulation $Z$ consists of:
- A set of **vertices** $V(Z)$
- A set of **darts** (directed edges) $D(Z)$, where each dart $e$ has:
  - A head vertex $\text{head}(e)$
  - A tail vertex $\text{tail}(e)$ (implicit via reverse dart)
  - **Successor and predecessor pointers** within an incidence list
  - A **reverse pointer** $\text{rev}(e)$ yielding the opposite orientation

### Core Axioms (Requirements M1–M6)

The structure must satisfy:
1. **Incidence lists**: All darts with the same head are organized in a single cyclic incidence list
2. **Consistency**: Successor/predecessor and reverse pointers form a coherent topological structure
3. **Minimality** (for reduced form): The minimal homomorphic image $Z^\circ$ identifies maximally homomorphic darts/vertices without losing structural properties

## Key Equations

**Homomorphic Identification Invariant:**
$$\varphi(e) = \varphi(f) \iff \varphi_1(e) = \varphi_1(f) \text{ for all homomorphisms } \varphi_1$$

where $\varphi: Z \to Z^\circ$ is the canonical quotient map.

**Successor Preservation (Homomorphism Property):**
$$\varphi^\circ_1(\text{succ}^\circ(e^\circ)) = \text{succ}_1(\varphi^\circ_1(e^\circ))$$

**Minimality Condition:**
$$Z^\circ = \min\{Z' : \exists \text{ homomorphism } \varphi: Z \to Z'\}$$

## Physical Intuition / Derivation

### Why Pseudo-Triangulation Matters

A pseudo-triangulation abstracts away geometric coordinates while preserving the **combinatorial topology** of a planar graph or triangulated mesh. This is crucial because:

1. **Coordinate-free representation**: The structure depends only on incidence relationships, not embedding geometry
2. **Efficient identification**: When two darts or vertices are "functionally equivalent" (homomorphic), they can be merged without loss of information
3. **Computational reduction**: The minimal image $Z^\circ$ removes redundancy by collapsing isomorphic substructures

### Construction Process

The algorithm builds $Z^\circ$ iteratively:

1. Start with a raw pseudo-triangulation $Z$
2. For each identification request $(e, f)$ (darts that should be equivalent):
   - Check if this identification respects all homomorphisms
   - Recursively identify generated predecessor/successor pairs $(e', f')$ that are forced by the homomorphic consistency requirement
3. Perform all identifications simultaneously to yield the minimal image

**Key Invariant**: If a homomorphism $\varphi_1: Z \to Z_1$ exists and respects identifications in $S$, then there exists a *factorization*:
$$\varphi_1 = \varphi_1^\circ \circ \varphi^\circ$$
ensuring unique minimal decomposition.

### Single-List Condition Maintenance

The critical insight is that vertex/dart identification preserves the equivalence class structure:

$$\text{Each vertex equivalence class} \longleftrightarrow \text{exactly one dart equivalence class}$$

This is maintained inductively because identifying darts respects the successor/predecessor graph structure without immediately modifying pointers.

## Applications in Engineering

### 1. **Computational Geometry & Mesh Processing**
- **Planar subdivision simplification**: Reduce memory footprint of triangulated models by identifying topologically identical sub-meshes
- **Mesh compression**: Represent redundant structure compactly for transmission or archival

### 2. **Graph Algorithms**
- **Topological graph canonicalization**: Find minimal homomorphic representations for comparison and isomorphism testing
- **Compiler data flow analysis**: Represent program control-flow graphs where equivalent branches can be merged

### 3. **CAD/CAM Systems**
- **Feature recognition**: Identify repeated geometric patterns (e.g., holes, ribs) via homomorphic dart matching
- **Design reuse**: Detect when sub-features are equivalent up to symmetry transformations

### 4. **Spatial Databases**
- **Index compression**: Store planar partitions (e.g., geographic maps) using minimal pseudo-triangulations
- **Query optimization**: Exploit homomorphic equivalence to prune search spaces

### 5. **Symbolic Computation**
- **Pattern matching**: Identify structurally equivalent subexpressions in abstract syntax trees
- **Rewriting systems**: Use homomorphic reduction to normalize representations

## Common Mistakes / Pitfalls

### Pitfall 1: Confusing Pseudo-Triangulation with Geometry
**Mistake**: Assuming the structure encodes Euclidean coordinates or angles.  
**Reality**: A pseudo-triangulation is purely *combinatorial*; it preserves only incidence relationships. Two geometrically different triangulations may yield identical pseudo-triangulations.

### Pitfall 2: Premature Identification
**Mistake**: Identifying darts $(e, f)$ without checking that all homomorphic consequences are consistent.  
**Reality**: Identifying $(e, f)$ forces cascading identifications of successors/predecessors. Fail to propagate = invalid structure.

### Pitfall 3: Violating the Single-List Condition
**Mistake**: Merging equivalence classes in a way that creates multiple incidence lists for a single vertex.  
**Reality**: The construction algorithm maintains the invariant automatically, but manual modifications risk breaking $M6$. Always verify via equivalence class partitioning.

### Pitfall 4: Assuming Uniqueness Before Minimization
**Mistake**: Claiming two pseudo-triangulations representing the same structure are identical.  
**Reality**: Uniqueness holds only for the **minimal homomorphic image** $Z