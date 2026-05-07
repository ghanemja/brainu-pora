# vertex degree

## Definition

The **vertex degree** $d_G(v)$ of a vertex $v$ in a graph $G$ is the number of edges incident to $v$. In a triangulation (a maximal planar graph), this counts the edges connecting $v$ to its neighbors.

For an oriented edge $uv$, the degree $d_G(v)$ determines how the charge redistribution (via discharging rules) is distributed across all incident edges.

### Formal Statement
For a triangulation $G$ and vertex $v \in V(G)$:
$$d_G(v) \geq 3$$
The minimum degree is 3 because every vertex in a triangulation must have at least 3 incident edges.

## Key Equations

### Defect Bound (Lemma 6.1)
For any vertex $v$ in a triangulation $G$:
$$T(v) \leq 60 - 2 \cdot d_G(v)$$

This is a fundamental relationship between vertex degree and the discharging deficit $T(v)$.

**Consequences:**
$$T(v) \leq 54 \quad \text{(since } d_G(v) \geq 3\text{)}$$

For vertices of high degree ($d_G(v) \geq 31$):
$$T(v) \leq -\frac{2}{31}d_G(v)$$

### Edge Charge Bound (Lemma 7.1)
For any oriented edge $uv$:
$$\varphi(u, v) \leq 8$$

where $\varphi(u, v)$ denotes the charge sent from $u$ to $v$ via discharging rules.

Over all neighbors of $v$:
$$\sum_{i=0}^{d_G(v)-1} \varphi(u_i, v) \leq 8 \cdot d_G(v)$$

### Restricted Edge Charge (Lemma 7.2)
When local structural constraints are enforced (no obstructing cycles or reducible configurations in $\tilde{B}_2^8(v) \cap \tilde{B}_2^8(u)$):
$$\varphi(u, v) \leq 5$$

## Physical Intuition / Derivation

### Degree as a Structural Parameter

In graph theory, vertex degree is a **topological invariant**—it directly encodes local connectivity. In planar triangulations:

- **Low-degree vertices** ($d_G(v) = 3, 4$): act as "deficient" regions that must be compensated by neighboring vertices through charge redistribution.
- **High-degree vertices** ($d_G(v) \geq 7$): can absorb excess charge from neighbors.

### Why the Defect Decreases with Degree

The equation $T(v) \leq 60 - 2 \cdot d_G(v)$ captures a **charge conservation principle**:

Starting with initial charge:
$$T_0(v) = 10(6 - d_G(v))$$

After redistribution, each of the $d_G(v)$ incident edges can receive charge $\leq 8$ from neighbors:
$$T(v) = T_0(v) + \sum_{u \sim v} \varphi(u, v) \leq 10(6 - d_G(v)) + 8 \cdot d_G(v) = 60 - 2d_G(v)$$

**Higher degree → more incident edges → more incoming charge → lower net deficit.**

### Ball-Based Locality

The discharging rules depend only on graph structures within the extended degree-bounded ball $\tilde{B}_2^8(v)$ (all vertices reachable within distance 2, where intermediate vertices have degree $\leq 8$). This means:

- The charge behavior at $v$ is **locally determined**.
- The interaction between two adjacent vertices $u, v$ depends on $\tilde{B}_2^8(u) \cap \tilde{B}_2^8(v)$.

## Applications in Engineering

### 1. **Mesh Quality Assessment (Computational Geometry)**
Vertex degree is critical in finite element method (FEM) mesh quality:
- **Equitable degree distribution** improves condition numbers of stiffness matrices.
- Vertices with $d_G(v) \gg$ average degree create poor-quality elements → numerical instability.
- Aspect-ratio-conscious meshing algorithms target degree bounds.

### 2. **Network Design & Routing (Electrical / Telecommunications)**
- In circuit networks, vertex degree determines current distribution capacity.
- High-degree nodes become bottlenecks; degree bounds inform redundancy requirements.
- Optimal routing minimizes max-degree for reliability.

### 3. **Structural Analysis (Civil Engineering)**
In truss and frame structures modeled as graphs:
- Degree bounds correlate with load-bearing capacity per joint.
- Over-constrained systems (high degree) can cause stress concentration.
- Load redistribution algorithms exploit degree-limited charge flow analogues.

### 4. **Graph-Based Optimization (Machine Learning / Operations Research)**
- Discharging arguments (parameterized by degree) prove properties of sparse graphs.
- Used in approximation algorithms for problems on bounded-degree graphs.
- Guides preprocessing: degree reduction heuristics before solving.

## Common Mistakes / Pitfalls

### 1. **Confusing Degree Constraints with Global Planarity**
**Error:** "If all $d_G(v) \geq 4$, the graph is more 'connected.'"

**Reality:** In a triangulation, degree distribution is rigidly constrained by the planar structure. Increasing some degrees *forces* others to decrease (by handshaking lemma: $\sum_v d_G(v) = 2|E|$, fixed for a given triangulation).

### 2. **Assuming Linear Charge Scaling**
**Error:** "If $d_G(v)$ doubles, then charge should double."

**Reality:** The relationship is $T(v) \leq 60 - 2d_G(v)$—*nonlinear*. Doubling degree reduces deficit by only $2