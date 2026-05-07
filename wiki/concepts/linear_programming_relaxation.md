# linear programming relaxation

## Definition

A **linear programming relaxation** (LP relaxation) is a mathematical technique that relaxes a combinatorial optimization problem (typically an integer program) into a continuous optimization problem whose feasible region is a polyhedron. This relaxation expands the feasible set by replacing discrete constraints with continuous approximations, making the problem tractable via convex optimization methods.

More formally, given a combinatorial optimization instance, an LP relaxation replaces:
- Integer variables $x_i \in \{0, 1\}$ with continuous variables $x_i \in [0, 1]$
- Discrete constraints with their continuous analogues
- Potentially discrete domains with continuous relaxations

In the abstract framework of the source material, an LP relaxation is characterized by a **minion** $R$—a functorial construction that assigns:
- To each finite set $D$ a relaxed domain $R(D)$ (e.g., probability distributions or continuous functions)
- To each constraint $\alpha: D \to E$ a relaxed constraint $R(\alpha): R(D) \to R(E)$

The relaxation is **functorial** (preserving function composition and identities) and **nontrivial** (mapping nonempty sets to nonempty sets), guaranteeing that solvability of the relaxed instance implies solvability of the original instance.

## Key Equations

For the **BLP (Boolean Linear Programming) relaxation**, the minion $R$ maps a domain $D$ to:

$$R(D) = \left\{ f : D \to [0, 1] \mid \sum_{a \in D} f(a) = 1 \right\}$$

This represents probability distributions over $D$. The induced relaxed constraint is:

$$R(\alpha)(f) = f \circ \alpha^{-1}$$

where the composition enforces that probability mass is correctly aggregated under the constraint function $\alpha$.

For **AC (Arc Consistency) relaxation**:

$$R(D) = \{\text{all nonempty subsets of } D\}$$

with $R(\alpha)(S) = \alpha(S)$ (the image of set $S$ under function $\alpha$).

For the **k-th level of a minion** $R$, applied to the k-th saturated power $\text{pow}_k(D)$:

$$\text{lvl}_k R \text{ relaxes } D \text{ such that } \text{Solvable}(\text{R-relax of } \text{pow}_k D) \iff \text{Solvable}(\text{lvl}_k R\text{-relax of } D)$$

## Physical Intuition / Derivation

**Why relax?**
Combinatorial problems are NP-hard in general. Relaxations trade exactness for tractability by expanding the feasible region to include fractional or probabilistic solutions. The optimal value of the relaxation provides a **bound** on the original problem's optimum.

**Building the intuition:**
1. **Start with the discrete problem**: Integer variables, combinatorial constraints (e.g., assign jobs to machines, exactly one machine per job)
2. **Soften the constraints**: Allow fractional assignments (job $j$ is 0.6 allocated to machine 1, 0.4 to machine 2), provided probabilities sum to 1
3. **Solve the relaxed problem**: Now it's a linear or convex program—solvable in polynomial time
4. **Interpret the solution**: Fractional variables in the relaxed solution may:
   - Directly suggest structure in an optimal integral solution (via rounding)
   - Provide a lower bound (for minimization) or upper bound (for maximization)

**The minion perspective** abstracts this idea: a minion $R$ captures a *family* of relaxation schemes. Higher levels ($\text{lvl}_k R$) encode correlations between $k$-tuples of variables simultaneously, moving beyond marginal information. This is crucial for **Promise CSPs** where local consistency alone doesn't suffice; higher-level constraints may break ties or rule out spurious fractional solutions.

## Applications in Engineering

### Constraint Satisfaction & Satisfiability
- **CSP solvers**: LP relaxations of Boolean constraints help prune search spaces and provide feasibility certificates
- **SAT solving**: Continuous relaxations of CNF formulas guide variable selection heuristics

### Scheduling & Resource Allocation
- **Job scheduling**: Relax machine assignments to continuous allocation; round fractionally assigned jobs
- **Network design**: Relax capacity constraints; use fractional flows to identify bottlenecks
- **Supply chain optimization**: Relax inventory discrete decisions to continuous for bounds; refinement via branch-and-cut

### Integer Programming (IP)
- **Cutting planes**: LP relaxations identify violated inequalities; add them to tighten bounds
- **Branch-and-bound**: LP relaxations at each node provide branching guidance and termination criteria
- **Approximation algorithms**: Some LP relaxations yield $O(1)$- or $O(\log n)$-approximation algorithms via rounding

### Machine Learning & Inference
- **Structured prediction**: Relax discrete label assignments to probability distributions; marginal inference via message passing
- **Combinatorial optimization in learning**: LP relaxations handle combinatorial structure in loss functions
- **Graphical models**: Belief propagation operates on relaxations of exact inference

### Hardware Verification
- **Boolean satisfiability**: Continuous relaxations help find unsatisfying assignments or prove unsatisfiability

## Common Mistakes / Pitfalls

1. **Confusing relaxation direction**: An LP relaxation provides a *bound*, not a solution. For a minimization problem, the relaxed optimum is ≤ the integral optimum. Students often assume the relaxed solution is feasible for the original problem—it is not.

2. **Ignoring integrality gap**: The gap between the relaxed optimum and the best integral solution can be arbitrarily large. A tight relaxation is problem-specific; no single relaxation works universally.

3. **Assuming rounding works**: Rounding fractional solutions to integer ones often violates constraints. Sophisticated rounding (derandomization, local search) is required; the integrality gap bounds the approximation ratio achievable by rounding.

4. **Misapplying functoriality**: The minion construction must preserve composition. Sloppy relaxations