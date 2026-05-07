# Homomorphism

## Definition

A **homomorphism** in the context of dart representations is a structure-preserving map $\varphi: Z \to Z_1$ between two dart representations that respects the underlying graph structure and pointer relationships.

Specifically, for dart representations $Z$ and $Z_1$ with dart sets $E(Z)$ and $E(Z_1)$, a homomorphism $\varphi$ must satisfy:

- **Pointer preservation**: If $\varphi(e) = e_1$ for a dart $e \in E(Z)$, then:
  - $\varphi(\text{head}(e)) = \text{head}(e_1)$ (head vertices map consistently)
  - $\varphi(\text{rev}(e)) = \text{rev}(e_1)$ (reverse dart relationships are preserved)
  - $\varphi(\text{succ}(e)) = \text{succ}(e_1)$ (successor pointers are preserved, including nil-preservation)
  - $\varphi(\text{pred}(e)) = \text{pred}(e_1)$ (predecessor pointers are preserved, including nil-preservation)

- **Completeness**: For a connected dart representation $Z$ satisfying axiom (M6), the homomorphism is **uniquely determined** by the image of a single dart $e$. The image of all other darts and vertices is forced by tracing through the pointer structure.

- **Triangle preservation**: Inner triangles of the source pseudo-triangulation $Z$ map to inner triangles of the target pseudo-triangulation.

### Minimal Images

A dart representation $Z_1$ is called a **minimal image** of $Z$ under homomorphism $\varphi: Z \to Z_1$ if:

1. Every vertex and dart in $Z_1$ is the image of some vertex or dart in $Z$
2. For each dart $e_1 \in E(Z_1)$: $e_1$ has a non-nil successor/predecessor iff there exists $e \in E(Z)$ with $\varphi(e) = e_1$ where $e$ has the corresponding non-nil pointer

**Lemma 9.3** (Structure Preservation): If $Z$ is a dart representation satisfying axioms (M1)–(M6) for pseudo-triangulations and $Z_1$ is a minimal image of $Z$, then $Z_1$ also satisfies (M1)–(M6).

## Key Equations

The homomorphism property can be written concisely as a **commutation condition** for each pointer operation $\xi \in \{\text{head}, \text{rev}, \text{succ}, \text{pred}\}$:

$$\varphi \circ \xi = \xi \circ \varphi$$

For vertices and darts:
$$\varphi(\text{tail}(e)) = \text{tail}(\varphi(e))$$
$$\varphi(\text{head}(e)) = \text{head}(\varphi(e))$$

Nil-pointers are preserved:
$$\text{succ}(e) = \text{nil} \implies \text{succ}(\varphi(e)) = \text{nil}$$

## Physical Intuition / Derivation

### Why Unique Determination Matters

In a connected dart representation, all darts and vertices are topologically linked through pointer chains. When you map a single dart $e$ to $e_1$, you've established an anchor point. The homomorphism condition forces you to follow the same "path grammar":

- If you can reach dart $e'$ from $e$ via $\text{succ} \circ \text{succ} \circ \text{rev}$, then you must reach $\varphi(e')$ from $\varphi(e)$ via the same sequence in $Z_1$
- The entire structure unfolds deterministically from the initial choice

This is why you can trace through the entire graph—it's fully connected through its pointer relationships, and homomorphisms must be "deaf to noise" (they can't arbitrarily branch).

### The Terminal Pseudo-Triangulation

The most elegant homomorphism target is the **terminal object**: a single vertex $v$ with one self-loop dart $e$ where:
$$\text{head}(e) = \text{tail}(e) = v, \quad e = \text{rev}(e) = \text{succ}(e) = \text{pred}(e)$$

This represents a degenerate pseudo-triangulation and is the unique **terminal object** in the categorical sense—every pseudo-triangulation has exactly one homomorphism mapping into it (collapsing all structure). However, this is not always a **minimal image**, which reveals important structural information about the source.

## Applications in Engineering

### 1. **Topology Simplification in CAD/Mesh Generation**

Homomorphisms enable hierarchical representation of geometric structures:
- Map complex pseudo-triangulations to simpler ones while preserving topological constraints
- Verify that simplified meshes maintain facial consistency with original designs
- Certify minimal images as valid abstractions in multi-resolution geometry

### 2. **Circuit Topology Verification**

In electrical networks represented as directed graphs with labeled vertices (components):
- Homomorphisms check whether one circuit diagram can be redrawn as another while preserving connectivity
- Validate that rewiring preserves functional equivalence
- Detect symmetries and redundancies through minimal images

### 3. **Combinatorial Embedding Compression**

For large-scale geometric data structures:
- Use homomorphisms to compress planar embeddings by identifying topologically equivalent regions
- Maintain invariants under quotient operations (mapping multiple cells to single cells)
- Reduce storage for real-time graphics by using minimal images

### 4. **Formal Verification of Subdivisions**

In computational geometry and solid modeling:
- Verify that mesh refinement operations respect homomorphic relationships to coarser meshes
- Ensure adaptive refinement maintains consistency with boundary conditions
- Check that hexahedral or tetrahedral subdivisions preserve the mesh topology

## Common Mistakes / Pitfalls

### 1. **Confusing Homomorphisms with Isomorphisms**

A homomorphism *need not be injective