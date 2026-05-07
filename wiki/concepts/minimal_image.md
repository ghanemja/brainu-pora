# minimal image

## Definition

A **minimal image** is a homomorphic image of a dart representation that satisfies a maximality condition on structural preservation.

Formally, given dart representations $Z$ and $Z_1$ with a homomorphism $\varphi: Z \to Z_1$, the representation $Z_1$ is a **minimal image of** $Z$ if:

1. **Surjectivity on reachable elements**: Every vertex and dart in $Z_1$ is the image of some vertex or dart in $Z$ under $\varphi$.

2. **Pointer preservation**: For any dart $e_1 \in E(Z_1)$, the dart $e_1$ has a non-nil successor/predecessor if and only if there exists a dart $e \in E(Z)$ with $\varphi(e) = e_1$ such that $e$ has the corresponding non-nil successor/predecessor.

In essence, a minimal image removes only necessary redundancy while preserving all topological information that is actually used in the structure.

## Key Equations

**Homomorphism uniqueness condition** (connected case):
$$\text{If } Z \text{ is connected and satisfies (M6), then } \varphi \text{ is uniquely determined by } \varphi(e) = e_1 \text{ for any choice of } e \in E(Z)$$

**Minimality criterion**:
$$e_1 \in E(Z_1) \text{ has non-nil pointer} \iff \exists e \in \varphi^{-1}(e_1) \text{ with non-nil corresponding pointer}$$

**Fundamental preservation property** (Lemma 9.3):
$$Z_1 \text{ is minimal image of } Z, \, Z \text{ satisfies (M1)–(M6)} \implies Z_1 \text{ satisfies (M1)–(M6)}$$

## Physical Intuition / Derivation

### Why Minimal Images Matter

Consider a dart representation as an explicit encoding of a combinatorial structure (typically a pseudo-triangulation). A naive homomorphism might collapse the structure completely, losing essential information. A **minimal image** represents the "simplest version" of the original structure that still retains all the topology being actively used.

### Construction Process

Given a connected dart representation $Z$ satisfying axiom (M6):

1. **Choose a seed dart**: Pick any dart $e \in E(Z)$ and decide its image $e_1 \in E(Z_1)$.

2. **Trace connectivity**: Since $Z$ is connected, traverse all reachable darts using:
   - Successor pointers ($\text{succ}$)
   - Predecessor pointers ($\text{pred}$)
   - Reverse darts ($\text{rev}$)
   - Head function ($\text{head}$)

3. **Enforce homomorphism property**: Each pointer operation in $Z$ must map to corresponding operations in $Z_1$.

4. **Verify minimality**: Check that no dart in $Z_1$ has "phantom" pointers—every non-nil pointer corresponds to actual structure in $Z$.

### The Terminal Pseudo-Triangulation

A special case illustrates the concept: the **one-dart loop** terminal object consists of:
- Single vertex $v$
- Single dart $e$ with $\text{head}(e) = v$ and $e = \text{rev}(e) = \text{succ}(e) = \text{pred}(e)$

This is a valid image of *every* pseudo-triangulation (plays the role of a terminal object in category theory), but it is rarely a **minimal** image. The distinction is crucial: an image need not be minimal.

## Applications in Engineering

### 1. Computational Topology & Mesh Processing
Minimal images enable efficient mesh simplification: reducing a detailed triangulation to its minimal essential representation while preserving topological invariants. Critical for:
- Memory-constrained embedded systems (robotics, aerospace)
- Real-time rendering (graphics pipelines)
- Geometric data compression

### 2. Finite Element Analysis
When coarsening FEM meshes, minimal images ensure that:
- Structural continuity is maintained
- Boundary conditions remain properly specified
- Computational cost reduction doesn't introduce spurious singularities

### 3. CAD/CAM Systems
In solid modeling:
- Computing canonical representations of part boundaries
- Detecting topologically equivalent designs
- Establishing minimal feature sets needed to reconstruct geometry

### 4. Graph Compression
For directed graph representations:
- Identify structurally minimal equivalent graphs
- Enable lossless compression with pointer elimination
- Optimize storage in network routing tables

### 5. Symbolic Computation
In algebraic topology software:
- Convert over-determined presentations to minimal ones
- Verify that homomorphisms preserve essential structure
- Validate categorical relationships

## Common Mistakes / Pitfalls

### Mistake 1: Confusing "Image" with "Minimal Image"
**Error**: Assuming that if $\varphi(Z) = Z_1$, then $Z_1$ is minimal.  
**Correction**: Minimality requires the additional pointer-preservation condition. A structure can be an image without being minimal—the terminal loop example demonstrates this.

### Mistake 2: Over-Reliance on Surjectivity
**Error**: Believing that surjectivity of $\varphi$ alone guarantees minimality.  
**Correction**: You must also verify the pointer condition: every non-nil pointer in $Z_1$ must come from a dart in the preimage that actually had that pointer.

### Mistake 3: Forgetting Nil-Pointers
**Error**: Treating nil (undefined) pointers the same as actual pointers.  
**Correction**: The minimality condition explicitly distinguishes: $e_1$ has nil successor iff *all* preimages of $e_1$ have nil successor. This is critical for boundary vertices and edges.

### Mistake 4: Ignoring Connectivity Requirements
**Error**: Applying uniqueness results to disconnected representations.  
**Correction**: The uniqueness of $\varphi$ given $\varphi(e) = e_1$ *requires* $Z$ to be connected (and satisfy M6). Disconnected representations admit multiple homomorphisms.

### Mistake 5