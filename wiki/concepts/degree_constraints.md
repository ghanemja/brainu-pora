# Degree Constraints

## Definition

**Degree constraints** specify the allowable range of vertex degrees in graph configurations used within the **discharging method**, a proof technique in combinatorial graph theory.

In formal terms, a degree constraint is a pair of functions:
- $\delta_R^- : V(R) \to \mathbb{N}$ (lower bound)
- $\delta_R^+ : V(R) \to \mathbb{N} \cup \{\infty\}$ (upper bound)

defined on the vertex set $V(R)$ of a rule graph $G(R)$, such that:

$$5 \leq \delta_R^-(v) \leq \delta_R^+(v) \text{ for each } v \in V(R)$$

A configuration $(Z, \delta)$ **obeys a rule** $R$ if there exists an isomorphism between $Z$ and $G(R)$ such that for every pair of corresponding vertices $(v_Z, v_R)$:

$$\delta_R^-(v_R) \leq d(v_Z) \leq \delta_R^+(v_R)$$

where $d(v_Z)$ denotes the degree of vertex $v_Z$ in the actual graph $Z$.

---

## Key Equations

**Degree range notation:**
$$\delta_R(v) \in [\delta_R^-(v), \delta_R^+(v)]$$

**Rule firing condition:**
A rule $R = (G(R), \delta_R^-, \delta_R^+, s(R), t(R), r(R))$ applies to an edge $st$ in graph $G$ when:
1. A subgraph $Z \subseteq G$ is isomorphic to $G(R)$
2. Every vertex $v$ in the matched configuration satisfies its degree constraint
3. Edge $st \in E(G)$ corresponds to the directed edge $(s(R), t(R))$ in $R$

**Charge flow:**
When rule $R$ applies at edge $st$, charge $r(R) \in \{1, 2\}$ flows from $s(R)$ to $t(R)$.

---

## Physical Intuition / Derivation

The discharging method is a technique for proving global graph properties (e.g., colorability, planarity constraints) by enforcing local structural constraints.

**Core idea:** Assign an initial charge to each vertex based on degree, then systematically redistribute ("discharge") charge between vertices according to rules. If the final charge configuration is impossible, the original structure cannot exist.

**Why degree constraints matter:**

1. **Specificity:** Rather than applying a rule to all configurations of a given size, degree constraints restrict application to only those where vertex degrees fall within specified ranges. This prevents overfitting and makes the proof more elegant.

2. **Charge conservation:** Each rule specifies exactly which vertices can participate (by degree range) and how much charge flows along a directed edge $(s(R), t(R))$. The constraint $\delta_R^-(v) \leq d(v) \leq \delta_R^+(v)$ ensures the rule only triggers for relevant configurations.

3. **Three canonical forms:** The notation captures three cases:
   - **Fixed degree** $\delta_R^-(v) = \delta_R^+(v) = k$: vertex must have exactly degree $k$
   - **Minimum threshold** $\delta_R^-(v) = 5 < \delta_R^+(v)$: vertex has degree at least 5
   - **Maximum unbounded** $\delta_R^-(v) < \delta_R^+(v) = \infty$: vertex has degree at least $\delta_R^-(v)$ with no upper limit

**Example:** A rule might specify that a degree-5 vertex (lower bound = upper bound = 5) adjacent to a degree-7+ vertex (lower bound = 7, upper bound = $\infty$) must pass charge in a particular direction. This ensures the rule only fires in the exact structural context intended.

---

## Applications in Engineering

### Graph Coloring & Scheduling
Degree constraints appear in **register allocation** and **task scheduling** problems. When modeling conflict graphs, constraints on vertex degree determine which nodes (tasks/registers) interact heavily and require careful scheduling.

### Planar Graph Analysis
In proving the **Four Color Theorem**, degree constraints ensure discharging rules apply only to locally reducible configurations. Engineers use this in:
- **Circuit layout** verification (ensuring planar embeddings)
- **Mesh generation** for finite element analysis (degree constraints on mesh vertices)

### Network Design & Routing
Degree constraints model **node capacity** in network graphs:
- Routers with degree constraints $[5, 12]$ can have 5–12 connections
- Degree constraints prevent over-subscription and guarantee feasible routing

### Structural Decomposition
In **compiler optimization** and **program analysis**, degree constraints in control-flow and data-dependence graphs identify bottlenecks (high-degree nodes) for optimization opportunities.

---

## Common Mistakes / Pitfalls

### 1. **Ignoring the Lower Bound of 5**
All degree constraints begin at $\delta^- \geq 5$. Students sometimes forget this is enforced uniformly, leading to rules that claim to apply to degree-4 vertices (which they don't).

### 2. **Confusing $\infty$ Semantics**
$\delta^+(v) = \infty$ does **not** mean "any degree." It means "at least $\delta^-(v)$." A rule with range $[7, \infty)$ does not apply to a degree-6 vertex.

### 3. **Misapplying Rules Symmetrically**
A rule $R$ and its reflection $R'$ are **distinct rules** unless explicitly symmetric. Applying the reflection without including it in the rule set is an error. The set of 84 rules in the Four Color Theorem proof accounts for both orientations of 42 asymmetric rules.

### 4. **Confusing Charge Direction**
The arrow on edge $(s(R), t(R))$ indicates **flow direction**. Charge moves from $s(R)$ (tail) to $t(R)$ (head). Reversing this invalidates the proof.

###