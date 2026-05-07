# polytope

## Definition

A **polytope** is a bounded convex polyhedron, defined as the convex hull of a finite set of points in $\mathbb{R}^d$. Equivalently, a polytope is a bounded set that can be expressed as:

$$P = \{x \in \mathbb{R}^d : Ax \leq b\}$$

where $A \in \mathbb{R}^{m \times d}$ and $b \in \mathbb{R}^m$, provided the solution set is bounded.

**Key distinctions:**
- **Polyhedron**: unbounded convex set defined by linear inequalities
- **Polytope**: bounded polyhedron (finite extreme points)
- **Facet**: A maximal face of dimension $d-1$ (for a $d$-dimensional polytope in $\mathbb{R}^d$)
- **Vertex/Extreme point**: A point that cannot be expressed as a convex combination of other points in the set

A polytope is **full-dimensional** if its affine hull is all of $\mathbb{R}^d$. When a polytope is not full-dimensional (e.g., constrained to a lower-dimensional subspace), different linear inequalities can define the same facet with non-scaled normal vectors.

## Key Equations

**Vertex representation (V-representation):**
$$P = \text{conv}(v_1, v_2, \ldots, v_n) = \left\{ \sum_{i=1}^n \lambda_i v_i : \lambda_i \geq 0, \sum_{i=1}^n \lambda_i = 1 \right\}$$

**Inequality representation (H-representation):**
$$P = \{x \in \mathbb{R}^d : a_i^T x \leq b_i \text{ for } i = 1, \ldots, m\}$$

**Facet description:** A facet $F$ of polytope $P$ satisfies:
$$F = \{x \in P : a^T x = b\}$$
where $(a, b) \in \mathbb{Z}^d \times \mathbb{Z}$ defines the supporting hyperplane.

**Complexity measure (from source material):** For facet $F$, the coefficient complexity is characterized by:
- Maximum absolute coefficient: $\max_{e \in E} |a_e|$
- Coefficient diversity: $|\{a_e : e \in E\}|$ (number of distinct coefficient values)

## Physical Intuition / Derivation

Polytopes arise naturally when modeling systems with linear constraints:

1. **Feasible regions in optimization:** Linear programs have optimal solutions at vertices of the feasible polytope. The structure of the inequality description directly affects computational complexity.

2. **Combinatorial optimization:** Many discrete problems (matching, flows, traveling salesman) have natural polytope formulations. The graph of a polytope connects feasible solutions as vertices, with edges representing adjacent feasible bases.

3. **Dimension and constraint redundancy:** A polytope in $\mathbb{R}^d$ requires at least $d$ constraints to be non-trivial. Extra constraints can be redundant or necessary for characterizing facets.

4. **Facet complexity trade-off:** Some polytopes arising from polynomial-time solvable problems have surprisingly complicated facet descriptions (large or diverse coefficients), as exemplified in the source material with the odd-red perfect matching polytope $P(G,R)$. This demonstrates that **computational tractability does not guarantee simple inequality representations**—a key insight for algorithm design.

The non-full-dimensional case is particularly important: when affine constraints reduce dimensionality, multiple normal vectors can represent the same facet, creating additional complexity in the description.

## Applications in Engineering

**1. Operations Research & Optimization**
- Integer linear programming (ILP) formulations of scheduling, routing, and resource allocation
- Cutting plane algorithms exploit facet structure to strengthen relaxations
- Branch-and-cut methods use facet inequalities to prune the search space

**2. Polyhedral Combinatorics**
- Matching and assignment problems (bipartite matching polytopes)
- Network design and flow problems (cut polytopes)
- Traveling salesman problem polytopes (subtour elimination)

**3. Control Systems & Reachability Analysis**
- Represent reachable sets of linear systems as polytopes
- Verify safety constraints by testing feasibility over polytopic regions
- Model constraint sets in model predictive control (MPC)

**4. Robotics & Motion Planning**
- Configuration space obstacles modeled as polytopic regions
- Collision avoidance constraints via polytope separability
- Grasp planning with polytopic contact regions

**5. Computational Geometry**
- Volume computation and sampling from high-dimensional polytopes
- Vertex enumeration for geometric analysis
- Convex hull algorithms (fundamental subroutine)

**6. Machine Learning**
- Support vector machine (SVM) optimization over polytopes
- Adversarial robustness verification using polytopic input perturbations

## Common Mistakes / Pitfalls

1. **Confusing polyhedra and polytopes:** A polyhedron can be unbounded; polytopes must be bounded. Optimization over unbounded polyhedra requires special care.

2. **Assuming minimal inequality descriptions:** Not all inequality representations are minimal or non-redundant. Facet inequalities are minimal, but derived constraints may be redundant.

3. **Ignoring dimension reduction:** When a polytope is not full-dimensional, the affine hull's dimension matters critically. Comparing normal vectors directly without accounting for the subspace leads to errors.

4. **Coefficient size underestimation:** Even for tractable problems (polynomial-time solvable), facet inequalities may require exponentially large or diverse coefficients (see Theorem 1 in source). One cannot assume {0, ±1}-coefficient descriptions exist.

5. **Equivalence of representations:** Different vertex and inequality descriptions may have vastly different computational properties. Converting between H- and V-representations is NP-hard in general.

6. **Scaling assumptions:** In integer programming, assuming all coefficients can be bounded by problem parameters often fails for tight polytope descriptions.

## See Also

- [[linear programming]] – Optimization over polytopes
- [[polyhedral combinatorics]] – Study of polytopes from combinatorial structures
- [[conv