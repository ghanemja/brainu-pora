# Graph Homomorphism

## Definition

A **graph homomorphism** is a structure-preserving map between two graphs. Formally, given graphs $G = (V_G, E_G)$ and $H = (V_H, E_H)$, a graph homomorphism is a function $\phi: V_G \to V_H$ such that:

$$\text{if } (u, v) \in E_G \text{, then } (\phi(u), \phi(v)) \in E_H$$

That is, the homomorphism must map edges in the domain graph to edges in the codomain graph. Note that a homomorphism does **not** require injectivity (one-to-one) or surjectivity (onto).

**Key Distinction:** A homomorphism differs from a graph isomorphism, which requires a bijective correspondence that preserves and reflects the full graph structure (both presence and absence of edges).

## Key Equations

The fundamental property of a homomorphism can be expressed in set notation:

$$\phi(E_G) \subseteq E_H$$

where $\phi(E_G) = \{(\phi(u), \phi(v)) : (u,v) \in E_G\}$.

For vertex-labeled graphs with attribute functions (as in the source material), a homomorphism $\phi: Z_R \to Z_C$ must additionally preserve or respect vertex attributes. In the context of the source, this involves constraint functions $\delta_C$ and $\delta'_C$:

$$\text{if } \delta_R(u) = d \text{, then } \delta_C(\phi(u)) \text{ must be compatible with } d$$

## Physical Intuition / Derivation

### Why Homomorphisms Matter

Graph homomorphisms formalize the notion of **structural embedding** without requiring perfect correspondence. Consider:

- **Relaxed equivalence**: A homomorphism allows multiple vertices in $G$ to map to a single vertex in $H$. This captures "coarse-graining" or abstraction.
  
- **Constraint preservation**: If $G$ satisfies a property expressible in terms of edges (e.g., "no odd cycles"), then a homomorphism to $H$ ensures $H$ respects that property locally.

- **Complexity reduction**: In applications like graph coloring or constraint satisfaction, finding a homomorphism to a small graph (e.g., a complete graph $K_k$) can encode a $k$-coloring.

### Example from Source Context

In the excerpt, the map from $Z_R$ to $Z_C$ uses homomorphisms to determine whether a rule $R$ applies to a vertex configuration. The homomorphism respects:
- The underlying graph structure (vertices and edges)
- Vertex degree constraints ($\delta^-$ and $\delta^+$ bound vertex degrees)

If a vertex $u_R \in Z_R$ with bounded degree maps to $u \in Z_C$ via the homomorphism, then the degree constraints in $Z_C$ at $\phi(u_R)$ must be at least as permissive as those in $Z_R$.

## Applications in Engineering

### 1. **Graph Coloring & Register Allocation**
In compiler design, graph homomorphisms to $K_k$ (complete graph on $k$ vertices) correspond to proper $k$-colorings. Register allocators use this to assign $k$ registers to program variables.

### 2. **Constraint Satisfaction Problems (CSP)**
A CSP solution corresponds to a homomorphism from a constraint graph to a domain graph. Homomorphisms help:
- Verify feasibility of assignments
- Identify bottlenecks in constraint propagation

### 3. **Network Protocol Verification**
In distributed systems, homomorphisms between protocol state graphs verify that an implementation refines a specification: if there's a homomorphism from implementation to specification, safety properties are preserved.

### 4. **Computational Geometry & CAD**
Homomorphisms between planar graphs (as in the source's cartwheel structures) help verify that complex geometric configurations reduce to simpler ones—critical for plane graph algorithms and mesh generation.

### 5. **Tiling & Pattern Matching**
In image processing and materials science, finding homomorphisms from a target pattern graph to a data graph identifies occurrences of that pattern (allowing for scaling/abstraction).

## Common Mistakes / Pitfalls

### 1. **Confusing with Isomorphism**
**Mistake:** Assuming a homomorphism must be bijective.  
**Correction:** Homomorphisms are generalizations—they can collapse vertices. Use isomorphism only when requiring a perfect 1-to-1 correspondence.

### 2. **Forgetting Edge Direction**
**Mistake:** In directed graphs, failing to respect edge orientation.  
**Correction:** For directed graphs, a homomorphism must map directed edges $(u \to v)$ to directed edges $(\phi(u) \to \phi(v))$.

### 3. **Not Checking Attribute Preservation**
**Mistake:** Verifying structural homomorphism but ignoring vertex/edge labels or attributes (as in the source material with $\delta_C$).  
**Correction:** Ensure all attributes, weights, and constraint functions are respected by the map $\phi$.

### 4. **Assuming Uniqueness**
**Mistake:** Treating a homomorphism as unique when multiple valid maps may exist.  
**Correction:** Multiple homomorphisms can exist between the same pair of graphs; algorithms must enumerate or count them as needed.

### 5. **Complexity Overestimation**
**Mistake:** Assuming finding a homomorphism is always hard.  
**Correction:** For fixed target graphs, homomorphism testing can be polynomial (e.g., to trees or bipartite graphs), though it's NP-complete for general targets.

## See Also

- [[Graph Isomorphism]] — bijective homomorphisms preserving and reflecting structure
- [[Graph Coloring]] — application of homomorphisms to complete graphs
- [[Constraint Satisfaction Problem]] — optimization using homomorphism existence
- [[Planar Graph Reduction]] — using homomorphisms to reduce complex configurations
- [[Category Theory and Morphisms]] — homomorphisms as arrows in the category of graphs

## Sources

- Excerpt from formal graph reduction proof (likely from Four Color Theorem verification work involving cartwheel reducibility and