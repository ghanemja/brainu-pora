# Charge Distribution

## Definition

**Charge distribution** in the context of discharging rules refers to a formal mechanism for assigning and transferring discrete charge values across vertices of a planar graph structure, typically used in combinatorial graph theory and computational geometry.

Formally, a **discharging rule** $R$ is a six-tuple:

$$R = \left(G(R), \delta^-_R, \delta^+_R, s(R), t(R), r(R)\right)$$

where:

- **$G(R) = (V(R), E(R))$**: A near-triangulation (a planar graph where all faces except the outer face are triangles)
- **$\delta^-_R, \delta^+_R : V(R) \to \mathbb{N}$**: Lower and upper bound functions defining the valid degree range $[\delta^-_R(v), \delta^+_R(v)]$ for each vertex $v$
- **$s(R), t(R) \in V(R)$**: The source (tail) and target (head) vertices—distinct adjacent vertices
- **$r(R) \in \{1, 2\}$**: The charge amount transferred from $s(R)$ to $t(R)$

A configuration $(Z, \delta)$ **obeys rule $R$** if $Z$ is isomorphic to $G(R)$ and every pair of corresponding vertices satisfies:

$$\delta^-_R(v_R) \leq d(v_Z) \leq \delta^+_R(v_R)$$

where $d(v_Z)$ is the degree of the matched vertex in $Z$.

---

## Key Equations

### Degree Range Constraints

For each vertex $v$ in a configuration $Z$ matching rule $R$:

$$5 \leq \delta^-_R(v) \leq \delta^+_R(v)$$

with three possible range types:

1. **Fixed degree**: $\delta^-_R(v) = \delta^+_R(v) = d$ 
2. **Minimum degree**: $\delta^-_R(v) = 5 < \delta^+_R(v)$ (drawn with minus sign)
3. **No upper bound**: $\delta^-_R(v) < \delta^+_R(v) = \infty$ (drawn with plus sign)

### Charge Flow

The total charge transferred along an edge $st$ in graph $G$ equals:

$$q(st) = \sum_{R \in \mathcal{R}} r(R) \cdot \mathbb{1}[\text{rule } R \text{ applies at } st]$$

where $\mathcal{R}$ is the set of applicable rules and $\mathbb{1}[\cdot]$ is the indicator function.

---

## Physical Intuition / Derivation

### Motivation

Charge distribution is a proof technique for establishing structural properties of planar graphs (particularly the Four Color Theorem). The intuition is:

1. **Assign initial charge**: Give each vertex an initial charge proportional to its degree deficit from a target value (typically related to Euler's formula)

2. **Distribute charge via rules**: Define local redistribution rules that move charge between vertices based on their local configuration

3. **Reach contradiction or stability**: If the system cannot reach a stable state (where all vertices obey global constraints), the original configuration is impossible

### Graph-Theoretic Foundation

For a near-triangulation where all internal faces are triangles, Euler's formula gives:

$$|V| - |E| + |F| = 2$$

This constraint, combined with the fact that each triangle has 3 edges and each internal edge borders 2 triangles, creates inherent structural limitations on degree sequences. Charge distribution exploits these via local pattern matching.

### Rule Application Mechanics

- Each rule encodes a **forbidden or constrained configuration** as a local induced subgraph
- The source vertex $s(R)$ is a "problematic" vertex (e.g., low degree) that sends charge to the target $t(R)$ 
- Multiple symmetric orientations of the same pattern are treated as distinct rules (unless self-symmetric)
- The charge amount $r(R) \in \{1, 2\}$ quantifies the severity of the constraint

---

## Applications in Engineering

### 1. **Graph Coloring & Constraint Satisfaction**
- Verifying colorability of planar graphs (e.g., VLSI circuit layout, register allocation in compilers)
- Encoding degree constraints in network design problems

### 2. **Computational Topology**
- Proof verification for topological invariants in 3D mesh generation
- Validating triangulation properties in computational geometry

### 3. **Network Flow & Resource Allocation**
- Modeling charge as abstract "resource" flowing through networks
- Designing local redistribution protocols that guarantee global feasibility

### 4. **Combinatorial Optimization**
- Discharging rules formalize infeasibility proofs in integer programming
- Used in automated reasoning to rule out bad configurations

### 5. **Theorem Proving & Verification**
- Mechanized proof systems for formal verification of graph properties
- The Four Color Theorem proof (Appel-Haken, later computerized) relies on this framework

---

## Common Mistakes / Pitfalls

### 1. **Confusing Source and Target**
- The arrow direction matters: charge flows from $s(R)$ (tail) to $t(R)$ (head)
- Reversing this changes the proof argument entirely

### 2. **Ignoring Symmetry**
- Two rules that are reflections of each other across the $s(R)$-$t(R)$ edge are distinct (unless the rule is self-symmetric)
- Naive enumerations may undercount or overcount the rule set

### 3. **Overlooking Triangulation Requirement**
- Rules only apply to **facial triangles** in the configuration
- Induced subgraph patterns that don't form faces cannot trigger the rule
- This distinction is critical when applying rules to arbitrary triangulations

### 4. **Initial Charge Miscalculation**
- The choice of initial charge function determines feasibility
- Common choices: $\text{ch}(v) = d(v) - 6$ or variants