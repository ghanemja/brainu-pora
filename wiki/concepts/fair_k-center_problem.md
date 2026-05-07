# fair k-center problem

## Definition

The **fair k-center problem** is a constrained clustering problem where:

- **Input:** A set $P$ of $n$ data points in a metric space $(P, d)$, partitioned into disjoint groups $G_1, G_2, \ldots, G_m$ where $\bigcup_{i=1}^m G_i = P$, and fairness requirements $r_1, r_2, \ldots, r_m$ specifying how many centers must come from each group.

- **Output:** A subset $C \subseteq P$ of exactly $k$ centers such that $|C \cap G_i| = r_i$ for all groups $i$.

- **Objective:** Minimize the **radius** (maximum distance from any point to its nearest center):
$$\text{radius}(C) = \max_{p \in P} \min_{c \in C} d(p, c)$$

**Key distinction from classical k-center:** The classical [[k-center problem]] selects $k$ centers without any group-based constraints. The fair variant adds *diversity constraints* to ensure representation from each group.

## Key Equations

**Approximation Ratio Definition:**

An algorithm is an $\alpha$-approximation for fair k-center if for every instance, it produces a solution with radius at most $\alpha \cdot \text{OPT}$, where $\text{OPT}$ is the optimal radius for that instance.

**Bicriteria Relaxation:** Some variants relax the constraint to allow selecting up to $k + O(m)$ centers while maintaining group constraints, which can improve approximation factors.

## Physical Intuition / Derivation

### Why Fairness Matters in Clustering

The classical k-center problem optimizes purely for worst-case coverage distance. However, in real applications—facility location, resource allocation, hiring committees—selecting representatives *only* from the largest or most accessible groups creates systemic inequity. Fair k-center forces balanced representation.

**Example:** Suppose you're opening $k=2$ hospitals to serve a city with downtown (100 patients) and suburbs (50 patients). Classical k-center places both hospitals downtown (optimal distance). Fair k-center with $r_1 = r_2 = 1$ ensures each area gets a hospital, trading some distance for equity.

### Why It's Harder Than Classical k-Center

1. **Classical k-center:** Admits a polynomial-time **factor-2 approximation** (greedy farthest-point algorithm). The approximation ratio of 2 is tight (NP-hard to improve).

2. **Fair k-center:** Best known polynomial-time algorithm achieves **factor-3 approximation**. The cited paper proves this is tight: no polynomial-time $(3-\varepsilon)$-approximation exists unless $P=NP$.

**Intuition for the gap:** Fairness constraints force selection of centers from dispersed groups, reducing flexibility in center placement. The algorithm cannot always choose the globally optimal locations—it must respect group quotas even when they're suboptimal for radius minimization.

### Key Hardness Results

From the source paper:

- **Main result:** For any $\varepsilon > 0$, no polynomial-time algorithm achieves a $(3-\varepsilon)$-approximation for fair k-center in general metrics (assuming $P \neq NP$).

- **Scope of hardness:** The hardness holds even in highly restricted cases:
  - **Two-group case:** Only two disjoint groups with $r_1, r_2 \geq 1$ (at least one center from each)
  - **One-per-group:** Exactly one center selected from each of $k$ groups (i.e., $r_i = 1$ for all $i$)

- **Comparison to k-supplier:** Both the unconstrained and fair variants of the [[k-supplier problem]] admit factor-3 approximation, showing the fair k-center's hardness is not universal to fairness-constrained clustering.

## Applications in Engineering

### 1. **Facility Location & Urban Planning**
- Opening $k$ emergency services (hospitals, fire stations, police precincts) across regions with fairness requirements ensures underserved communities aren't overlooked for efficiency.
- Constraints: $r_i$ = minimum facilities required in district $i$.

### 2. **Workforce Diversity & Hiring**
- Selecting $k$ representative employees/candidates from groups (e.g., departments, demographics) to minimize "distance" to organization's skill requirements while maintaining diversity.
- Groups: departments, gender, ethnicity, seniority levels.

### 3. **Server Placement in Distributed Systems**
- Deploying $k$ caching/computing nodes across geographic regions or data centers, ensuring coverage from each critical region.
- Objective: minimize maximum latency to nearest server while serving all regions.

### 4. **Supply Chain & Warehouse Management**
- Positioning $k$ distribution warehouses across suppliers/regions to minimize maximum delivery distance while ensuring procurement from at least $r_i$ suppliers per region.
- Balances cost (number of warehouses) with service quality (coverage distance) and supply chain resilience (diversity of sources).

### 5. **Sensor Network Deployment**
- Selecting $k$ sensor nodes where groups represent physical zones; ensures monitoring coverage of each zone while minimizing maximum blind spot.

## Common Mistakes / Pitfalls

### 1. **Confusing Fair k-Center with Balanced k-Means**
- **k-means** minimizes sum-of-squared-distances; **fair k-center** minimizes maximum distance (min-max objective).
- Fair k-center's min-max formulation is inherently more robust to outliers.

### 2. **Ignoring the Factor-3 Barrier**
- Students often expect fair k-center to admit factor-2 approximations like classical k-center.
- **The hardness result states factor-3 is necessary.** Algorithms claiming factor-2 either:
  - Assume special metric structures (not general metrics), or
  - Relax fairness constraints (allow $r_i \pm O(1)$ instead of exact equality)

### 3. **Misapplying Greedy Farthest-Point**
- The standard greedy algorithm for classical k-center (pick farthest point not yet covered) does **