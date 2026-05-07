# Discharging Method

## Definition

The **discharging method** is a combinatorial proof technique that assigns "charges" (numerical weights) to vertices or faces of a graph, then systematically redistributes these charges according to local rules while preserving the total charge. By showing that the final charge distribution is impossible if certain structural properties hold, one derives a contradiction—proving that the graph must satisfy those structural properties.

In the context of graph coloring and the Four Color Theorem, the discharging method identifies regions of a planar graph with positive or zero **combinatorial curvature**, which corresponds to structural configurations that admit efficient reduction operations.

## Key Equations

**Initial Charge Assignment (Planar Graphs):**
$$\chi(v) = 6 - \deg(v) \quad \text{for vertex } v$$

or equivalently for faces:
$$\chi(f) = 2 - |f| \quad \text{for face } f \text{ with } |f| \text{ sides}$$

**Total Charge Conservation:**
$$\sum_{v \in V} \chi(v) = 2\pi \cdot \chi(\text{surface}) \quad \text{(Gauss-Bonnet discrete analog)}$$

For a planar graph (sphere topology, Euler characteristic $\chi = 2$):
$$\sum_{v \in V} (6 - \deg(v)) = 12$$

**Charge Flow Rule (Redistribution):**
If charge flows from vertex $u$ to adjacent vertex $v$:
$$\chi'(u) = \chi(u) - \delta_{uv}, \quad \chi'(v) = \chi(v) + \delta_{uv}$$

where $\delta_{uv} \geq 0$ is the amount discharged.

## Physical Intuition / Derivation

### Combinatorial Curvature Perspective

Imagine distributing "charge density" across a graph proportional to how much a vertex's degree deviates from 6 (the "flat" degree in a triangulation). 

- **Positive curvature**: $\deg(v) < 6$ → vertex $v$ starts with positive charge
- **Zero curvature**: $\deg(v) = 6$ → vertex starts neutral  
- **Negative curvature**: $\deg(v) > 6$ → vertex starts with negative charge

**The Key Insight:** 
Regions of positive curvature are "deficient" and contain reducible configurations. These are subgraphs whose 4-colorability can be solved independently, then reinserted maintaining global coloring.

### How Discharging Finds Reductions

1. **Initialize**: Assign charges based on degrees.
2. **Discharge Rules**: Vertices pass charge to neighbors according to local structural rules (e.g., "a degree-5 vertex sends charge to degree-4 neighbors").
3. **Final Contradiction**: Show that if NO reducible configuration exists, no valid final charge distribution is achievable—since charge cannot "disappear."
4. **Conclusion**: A reducible configuration must exist.

### Enhanced Finding: Linear Many Reductions

The paper's breakthrough shows that:
- Classical approaches find ONE reducible configuration per induction step → $O(n)$ steps → $O(n^2)$ time.
- By discharging more carefully, reductions exist even in **flat regions** (zero curvature) → find $\Theta(n)$ disjoint reductions → $O(\log n)$ induction depth → $O(n \log n)$ total time.

## Applications in Engineering

### 1. **Graph Coloring Algorithms**
- **Planar graphs**: Near-linear 4-coloring for circuit layout, frequency assignment in wireless networks.
- **Register allocation**: Compile-time optimization mapping variables to processor registers.

### 2. **Network Design**
- **Frequency reuse**: Assigning frequencies to cell towers (planar region model) with conflict avoidance.
- **Resource scheduling**: Task scheduling with dependency constraints where the conflict graph is sparse/planar.

### 3. **Computational Geometry**
- **Mesh generation**: Quality assurance in finite element meshes (degree bounds ensure good element shapes).
- **Cartographic generalization**: Detecting over-dense regions for aggregation/simplification.

### 4. **Theoretical Computer Science**
- **Approximation algorithms**: Using discharging to prove properties of optimal solutions (lower bounds).
- **Randomized algorithms**: Analyzing concentration inequalities via charge redistribution over random variables.

### 5. **VLSI Design**
- **Layer assignment**: Assigning components to fabrication layers while respecting planarity constraints.
- **Congestion analysis**: Detecting high-congestion regions in routing graphs.

## Common Mistakes / Pitfalls

### 1. **Forgetting Charge Conservation**
**Error**: Applying discharge rules that decrease total charge.  
**Fix**: Verify $\sum \chi'(v) = \sum \chi(v)$ after each rule application.

### 2. **Vague Discharge Rules**
**Error**: Rules like "send charge until some local property holds" without quantifying the amount.  
**Fix**: Specify explicit $\delta_{uv}$ formulas; use potential function arguments if needed.

### 3. **Assuming Planarity Unnecessarily**
**Error**: Using $\chi = 2$ (Euler characteristic of sphere) for non-planar or surface-embedded graphs.  
**Fix**: Adapt the initial charge to the correct surface genus: $\chi = 2 - 2g$ for genus $g$.

### 4. **Missing Boundary Cases**
**Error**: Discharge rules that don't account for low-degree vertices or irregular configurations.  
**Fix**: Enumerate all possible local neighborhoods explicitly; handle each case.

### 5. **Confusing "Existence" with "Constructivity"**
**Error**: Discharging proves existence of a reducible configuration but gives no algorithm to find it efficiently.  
**Fix**: The paper's contribution is combining discharging with explicit D-reducible configurations to make the proof **algorithmic**.

## See Also

- [[Four Color Theorem]] — The main result proved via discharging
- [[D-reducible Configuration]] — Graph substructures that preserve 4-colorability under contraction
- [[Combinatorial Curvature]] — Discrete analog of differential geometry