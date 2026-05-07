# Constraint Satisfaction Problem (CSP)

## Definition

A **Constraint Satisfaction Problem (CSP)** is a computational problem defined by:

- **Variables**: A finite set $X = \{x_1, x_2, \ldots, x_n\}$
- **Domains**: Each variable $x_i$ has an associated finite domain $D_i$ of allowable values
- **Constraints**: A set $C$ of constraints, each restricting the simultaneous assignment of values to a subset of variables

A **solution** to a CSP is a complete assignment $\sigma: X \rightarrow \bigcup_i D_i$ such that:
$$\sigma(x_i) \in D_i \text{ for all } x_i \in X$$
and every constraint in $C$ is satisfied.

The **CSP decision problem** asks: does a valid solution exist?

### Label Cover Representation

CSPs can be reformulated as **Label Cover (LC) instances**, which provide a uniform view for analysis:

- Original CSP variables and domains are preserved
- For each constraint $R$ over variables $x_1, \ldots, x_n$, introduce an auxiliary variable $y_R$ with domain equal to $R$ (the set of satisfying tuples)
- Add projection constraints: $x_i = \pi_i(y_R)$ for each $i$, where $\pi_i(a_1, \ldots, a_n) = a_i$

This transformation preserves satisfiability: solutions to the original CSP correspond exactly to solutions to the LC instance.

## Key Equations

For an LC instance, the consistency conditions can be expressed formally. Let $D_x'$ denote the reduced domain after applying a relaxation algorithm. The **Arc Consistency (AC)** property requires:

$$\forall \text{ constraint } x = \alpha(y): \quad \alpha(D_y') = D_x'$$

That is, the image of the reduced domain under the projection function equals the reduced domain of $x$.

For **Linear Programming (LP) relaxations**, fractional assignments are represented as probability distributions over domains:

$$\sum_{v \in D_x} p_x(v) = 1 \quad \text{where} \quad p_x(v) \in [0,1]$$

Constraints in the LP are relaxed to probabilistic consistency:

$$\mathbb{E}_{y \sim D_y}[\alpha(y)] = \mathbb{E}_{x \sim D_x}[x]$$

## Physical Intuition / Derivation

CSPs arise naturally in **discrete optimization and decision problems** where:

1. **Multiple interacting entities** (variables) each have limited choices (domains)
2. **Mutual constraints** limit which combinations are permissible

### Why Relaxations Matter

Direct CSP solving is NP-complete for most constraint types. **Relaxations** (AC, BLP, higher-order schemes) provide:

- **Pruning power**: Eliminate impossible values before exhaustive search
- **Refutation ability**: Prove unsatisfiability when domains become empty
- **Approximation hierarchy**: Higher relaxations capture stricter constraints

The LC formulation reveals the fundamental structure: constraints become first-class variables encoding *witnesses* to satisfaction. A constraint like $x \neq y$ becomes a variable whose domain is $\{(0,1), (1,0)\}$, and the problem reduces to ensuring consistency between original and constraint variables.

### Arc Consistency Example

Consider $x = 1, x \neq y, y \leq z$ over $\{0,1\}^3$:

1. Initial domains: $D_x = \{0,1\}, D_y = \{0,1\}, D_z = \{0,1\}$
2. Constraint $x = 1$ forces $D_x \leftarrow \{1\}$
3. Constraint $x \neq y$ with $D_x = \{1\}$ requires $y \neq 1$, so $D_y \leftarrow \{0\}$
4. Constraint $y \leq z$ with $D_y = \{0\}$ permits $D_z = \{0,1\}$
5. **Result**: Unique solution $(x, y, z) = (1, 0, 0)$ or $(1, 0, 1)$

## Applications in Engineering

### 1. Scheduling Problems
Assign tasks to time slots subject to resource and precedence constraints. Variables = tasks, domains = time intervals, constraints = no resource overallocation.

### 2. Circuit Design & Verification
Assign signal levels to circuit nodes. Variables = nodes, domains = $\{0, 1\}$, constraints = gate logic rules (e.g., AND, OR). Used in SAT solving for hardware verification.

### 3. Robot Motion Planning
Variables = joint angles or waypoint coordinates, domains = valid ranges, constraints = obstacle avoidance and kinematic limits.

### 4. Network Routing
Assign paths through a network. Variables = packets/flows, domains = valid routes, constraints = bandwidth capacity and delay bounds.

### 5. Computer Vision & Constraint Propagation
Structure-from-motion: variables = landmark coordinates, domains = 3D space region, constraints = epipolar geometry, photometric consistency.

## Common Mistakes / Pitfalls

1. **Confusing satisfiability with optimality**: CSPs are decision problems. Many applications require optimization (CSP + objective = combinatorial optimization). Relaxations prove feasibility but not minimality.

2. **Assuming AC completeness**: Arc consistency does NOT solve all CSPs. It prunes but typically requires backtracking search afterward. Higher-level relaxations (BLP, polynomial hierarchy) are strictly more powerful.

3. **Misinterpreting LC transformation**: The LC instance is NOT a simplification—it has more variables. Its value is *analytical*: it provides a uniform framework where relaxation techniques apply uniformly.

4. **Domain explosion in practice**: For large constraint arities $n$ and domains of size $d$, auxiliary variable domains in LC have size $d^n$, making explicit enumeration infeasible. Practical algorithms use implicit representations.

5. **Ignoring constraint semantics**: Generic CSP algorithms ignore what constraints *mean* (e.g., arithmetic structure). Domain-specific algorithms often outperform