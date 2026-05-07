# Free completion

## Definition

A **free completion** of a configuration $(Z, \delta)$ is a near-triangulation $\tilde{Z}$ constructed by:

1. Starting with an embedded planar graph $Z$ with a designated outer facial walk
2. Adding a cycle $R$ (the **ring**) disjoint from $Z$
3. Connecting vertices on the outer face of $Z$ to vertices on $R$ via new edges
4. Ensuring that $R$ becomes the outer facial cycle of $\tilde{Z}$
5. Containing the original configuration $(Z, \delta)$ within $\tilde{Z}$

The free completion is also called the **extended configuration** of $Z$. It is the minimal near-triangulation that preserves the configuration while adding a "closure" cycle.

### Ring Structure

The ring $R = R(Z)$ is the outer facial cycle of the free completion. Its length is uniquely determined by:

$$|R| = \sum_{v \in V(Z)} (\delta(v) - d_Z(v)) - t = \sum_{v \in V(Z)} \delta(v) - 2|E(Z)| - t$$

where:
- $\delta(v)$ = prescribed degree (from configuration specification) at vertex $v$
- $d_Z(v)$ = actual degree of $v$ in $Z$
- $t$ = length of the outer facial walk of $Z$

## Key Equations

**Ring length formula:**
$$|R| = \sum_{v \in V(Z)} \delta(v) - 2|E(Z)| - t$$

**Equivalently (via handshaking lemma):**
$$|R| = \sum_{v \in V(Z)} (\delta(v) - d_Z(v)) - t$$

**Degree sum constraint:**
The formula reflects that $2|E(Z)| = \sum_{v \in V(Z)} d_Z(v)$ for any graph.

## Physical Intuition / Derivation

### Motivation

In graph coloring reduction arguments, configurations serve as "problematic" local structures. To prove a configuration is **reducible**, one must show that any 4-coloring of the exterior region can be extended through the configuration.

The free completion provides a canonical embedding that:
- **Isolates** the configuration $Z$ from the rest of graph $G$
- **Closes off** the outer face with a minimal ring $R$
- **Preserves** all degree constraints from the configuration specification

### Why This Construction Works

The ring length formula emerges from a **deficit accounting principle**:

- At each vertex $v \in Z$, there is a "deficit" $\delta(v) - d_Z(v)$ between required and actual degree
- This deficit is "absorbed" by the ring $R$ through edges connecting $Z$ to $R$
- The outer facial walk of length $t$ already uses $t$ edge-endpoints on the boundary of $Z$
- Thus the ring must accommodate: (total deficit) - (boundary edges) = $\sum \delta(v) - 2|E(Z)| - t$

### Handling Cut-Vertices

A key feature: the free completion is **unambiguous even if $Z$ contains cut-vertices** (vertices whose removal disconnects $Z$). This follows from the property that the construction only depends on local degree data and outer face structure, not on $Z$'s connectivity.

## Applications in Engineering

### 1. **Graph Coloring & Circuit Verification**
Free completions are central to automated proofs of the **Four Color Theorem** (4CT):
- Decompose planar graphs into configurations
- Show each configuration is "reducible" via free completion analysis
- Verify 4-colorability cascades from local to global structure

### 2. **Planar Subdivision Algorithms**
In computational geometry and CAD:
- Free completions define canonical "completion regions" for partial mesh designs
- Used to verify consistency of mesh refinement where degree constraints matter
- Ring topology captures boundary interaction requirements

### 3. **Constraint Satisfaction in VLSI Design**
Planar graph layouts with degree constraints (power/ground routing):
- Free completion determines minimum feasible ring sizes
- Guides routing feasibility checks before full layout

### 4. **Topological Reducibility Analysis**
Any system requiring:
- Local constraint satisfaction (per vertex)
- Global boundary closure
- Certification of reducibility

Benefits from free completion as a **canonical normal form**.

## Common Mistakes / Pitfalls

### Mistake 1: Confusing Ring with Outer Face
**Error**: Assuming $R$ is the same as the original outer facial walk of $Z$.

**Reality**: $R$ is a *new* cycle added to close off $Z$. The original outer walk is part of $Z$ but may be internal in $\tilde{Z}$.

### Mistake 2: Ignoring the Configuration Specification
**Error**: Computing ring length without reference to $\delta(v)$ requirements.

**Reality**: The ring length formula depends **critically** on $\delta(v)$. Without the degree specification, the construction is undefined.

### Mistake 3: Assuming Ring is Simple
**Error**: Expecting $R$ to be a non-self-intersecting cycle in all cases.

**Reality**: The ring $R$ is a simple cycle in the abstract sense, but its embedding in $G$ may self-intersect, creating apparent cut-vertices in $G - V(Z)$.

### Mistake 4: Overconstraining the Ring
**Error**: Imposing additional requirements on $R$ beyond being a facial cycle.

**Reality**: The ring is minimal; its only role is closure. Vertices and edges on $R$ may be identified in the ambient graph $G$ arbitrarily.

### Mistake 5: Misunderstanding Extendibility
**Error**: Treating 0-extendibility as automatic.

**Reality**: A coloring of $R$ is $0$-extendible only if it admits a valid extension to all of $\tilde{Z}$. This is a **property to be verified**, not a default.

## See Also

- [[Configuration (graph theory)]] — the local structure being completed
- [[Reducibility (graph coloring)]] — how free completions enable reduction arguments
- [[Kempe chains]] — color-swapping mechanism used to modify color