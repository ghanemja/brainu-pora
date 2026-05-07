# Discharging Rules

## Definition

A **discharging rule** is a formal device used in graph-theoretic proofs, particularly in planar graph analysis and the Four Color Theorem. It defines a local configuration that permits controlled "charge flow" between vertices in a graph.

Formally, a rule is a six-tuple:
$$R = \left(G(R), \delta^-_R, \delta^+_R, s(R), t(R), r(R)\right)$$

where:

- **$G(R) = (V(R), E(R))$** is a *near-triangulation* (a planar graph where all faces except the outer face are triangles) such that $G(R) - v$ is connected for every $v \in V(R)$
- **$\delta^-_R, \delta^+_R : V(R) \to \mathbb{N} \cup \{\infty\}$** define degree constraints: for each vertex $v$, we require $5 \leq \delta^-_R(v) \leq \delta^+_R(v)$
- **$s(R), t(R) \in V(R)$** are distinct, adjacent vertices designated as the source (tail) and target (head) of the rule
- **$r(R) \in \{1, 2\}$** is the *charge amount* transferred from $s(R)$ to $t(R)$

### Configuration Obedience

A configuration $(Z, \delta)$ **obeys rule $R$** if:
1. $Z$ is isomorphic to $G(R)$ via some isomorphism $\phi$
2. For every pair of corresponding vertices $(v_Z, v_R)$ under $\phi$:
$$\delta^-_R(v_R) \leq \deg_Z(v_Z) \leq \delta^+_R(v_R)$$

In other words, the actual degree of each vertex in the configuration must fall within the prescribed range for that vertex type in the rule.

## Key Equations

**Degree Range Notation:**
$$\delta^-_R(v) \leq \deg(v) \leq \delta^+_R(v)$$

**Charge Flow Along Edge:**
When rule $R$ is applied at edge $st \in E(G)$, the charge transferred is:
$$q(s \to t) = r(R) \text{ (in the direction of the arrow)}$$

**Graphical Encoding of Degree Ranges:**
- **Fixed degree:** $\delta^-_R(v) = \delta^+_R(v) = d$ → vertex drawn with shape for degree $d$
- **Lower bounded:** $\delta^-_R(v) = 5 < \delta^+_R(v) < \infty$ → shape for $\delta^+_R(v)$ with a minus sign (−)
- **Upper bounded:** $\delta^-_R(v) < \delta^+_R(v) = \infty$ → shape for $\delta^-_R(v)$ with a plus sign (+)

## Physical Intuition / Derivation

Discharging rules encode a *proof by contradiction* strategy for planar graph properties:

### The Core Idea

1. **Assign initial charge:** Give each vertex $v$ a charge proportional to its degree or some structural property
2. **Apply local rules:** Use discharging rules to redistribute charge locally based on configuration patterns
3. **Invariant:** The total charge in the graph is conserved
4. **Contradiction:** Show that if a "bad" configuration exists (e.g., a vertex of degree < 5 that violates a coloring constraint), the final charge distribution is impossible

### Why This Works

- **Near-triangulations** constrain the local structure: knowing the degree ranges of neighboring vertices severely limits possible configurations
- **Finite rule sets** (e.g., 84 rules) guarantee that all possible local neighborhoods are covered
- **Facial triangle matching** ensures rules capture *induced* subgraph structures, preventing pathological cases

### Example Intuition

If you must prove "every planar graph has a vertex of degree ≤ 5," you can:
- Assume all vertices have degree ≥ 6 (contradiction hypothesis)
- Design rules so charge flows *away* from degree-6 vertices toward degree-7+ vertices
- Show the edge count and charge accounting become inconsistent

## Applications in Engineering

### 1. **Graph Coloring & Scheduling**
- Verify colorability of planar graphs in circuit design (register allocation, frequency assignment)
- The Four Color Theorem (proven via discharging) guarantees that planar graphs need at most 4 colors
- Applications: WiFi channel assignment on planar network topologies, compiler register allocation

### 2. **Planar Embedding Verification**
- Discharging proofs certify structural properties of planar subdivisions used in computational geometry
- Validate mesh quality in finite element analysis (FEA)
- Ensure no degenerate triangulations in CAD systems

### 3. **Verification of Graph Algorithms**
- Prove correctness of approximation algorithms on planar graphs
- Establish bounds on solution quality for NP-hard problems on planar inputs
- Examples: traveling salesman, minimum vertex cover on planar graphs

### 4. **Network Reliability Analysis**
- Use structural properties (min vertex degree, connectivity) to assess fault tolerance in planar network topologies
- Discharging rules help formalize minimum degree guarantees

### 5. **Mesh Generation & Optimization**
- Verify properties of triangulated surfaces in 3D graphics, CAD, and simulation
- Ensure compatibility conditions in multi-patch surface design

## Common Mistakes / Pitfalls

### 1. **Confusing Degree Ranges with Constraints**
❌ **Wrong:** "Rule $R$ requires all vertices to have degree in the range"  
✓ **Correct:** "A configuration *obeys* $R$ only if actual degrees match prescribed ranges in that specific pattern"

The rule is a *local pattern matcher*, not a global constraint.

### 2. **Forgetting Facial Triangle Matching**
❌ **Wrong:** "The rule applies to any isomorphic subgraph"  
✓ **Correct:** "