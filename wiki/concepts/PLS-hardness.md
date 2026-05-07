# PLS-hardness

## Definition

**PLS-hardness** (Polynomial Local Search-hardness) is a computational complexity classification for local optimization problems that are as hard as the hardest problems in the **PLS complexity class**.

A problem is **PLS-hard** if every problem in the PLS class can be reduced to it in polynomial time. This means:
- There exists a polynomial-time computable reduction from a known PLS-complete problem to the target problem
- Finding an approximate solution to a PLS-hard problem is computationally intractable (assuming PLS ≠ P)
- No polynomial-time algorithm is known or believed to exist for solving the problem exactly or approximately

**Context in optimization:** A problem $\Pi$ is PLS-hard if we can construct a polynomial-time reduction from a PLS-complete problem (such as **Iter**, the Iterative Local Search problem) to $\Pi$, such that every solution of $\Pi$ corresponds to a solution of the original problem instance.

### Relationship to other hardness classes:
- **PLS ⊆ TFNP** (Total Function NP): Every PLS instance has a solution
- **PLS-completeness** is stronger than NP-hardness for decision problems (since PLS problems are total function problems requiring explicit solutions)
- PLS-hardness applies to problems where finding *any* local optimum is hard, not just determining existence

---

## Key Equations

While PLS-hardness is primarily a complexity-theoretic concept rather than an algorithmic one, the formal definition involves polynomial-time reductions:

**Polynomial-time reduction from problem $A$ to problem $B$:**
$$\text{If } \exists \text{ poly-time computable } f: \text{instances}(A) \to \text{instances}(B)$$
$$\text{such that } \forall x \in \text{instances}(A): \text{Sol}(x, A) \text{ maps to } \text{Sol}(f(x), B)$$
$$\text{then } B \text{ is at least as hard as } A$$

**For Interior-SOSP (Second-Order Stationary Point):** A point $x^* \in [0,1]^2$ is an $(\epsilon_0, \epsilon_0)$-SOSP if:
$$\|\nabla f(x^*)\| \leq \epsilon_0 \quad \text{and} \quad \lambda_{\min}(\nabla^2 f(x^*)) \geq -\epsilon_0$$

where $\lambda_{\min}$ denotes the smallest eigenvalue of the Hessian.

---

## Physical Intuition / Derivation

### Why PLS-hardness matters:

1. **Local Search Perspective:** PLS captures the complexity of finding local optima in combinatorial or continuous optimization. Unlike NP-hardness (which asks "does a solution exist?"), PLS-hardness asks "can we find a local minimum efficiently?"

2. **The Reduction Strategy:** Proving PLS-hardness requires showing that an arbitrary instance of a PLS-complete problem (like **Iter**) can be *embedded* into the target problem through a polynomial-time construction. For Interior-SOSP:
   - A discrete grid domain $[2^n]$ (exponential in problem size) is mapped to a continuous 2D box $[0,N]^2$ where $N = \Theta(2^n)$
   - Grid cells are colored according to gradient and Hessian information
   - Function values assigned to grid corners encode the Iter instance's directed graph structure
   - Smooth interpolation (biquintic) preserves these encodings while ensuring twice-differentiability

3. **Key Construction Insight:** Using **biquintic interpolation**, the reduction constructs a smooth function $f: [0,N]^2 \to \mathbb{R}$ such that:
   - Every second-order stationary point of $f$ corresponds to a valid solution of the embedded Iter instance
   - The function satisfies smoothness constraints required by Interior-SOSP
   - No unwanted approximate SOSPs exist outside the encoded solution points

4. **Why it's non-trivial:** The main technical challenge is ensuring that the smooth interpolation does not accidentally create spurious approximate SOSPs. Previous techniques (four groups of grid cells from Fiat-Shamir based constructions) identify FOSPs but are insufficient for SOSP characterization, requiring new techniques.

---

## Applications in Engineering

### 1. **Optimization Algorithm Development**
- **Motivation:** If Interior-SOSP is PLS-hard, spending effort on provably polynomial-time algorithms for finding SOSPs is likely wasted. Engineers should focus on:
  - Heuristic methods with empirical performance guarantees
  - Specialized structure exploitation (convexity, sparsity, etc.)
  - Approximate or fixed-parameter algorithms

### 2. **Nonlinear Programming & Continuous Optimization**
- **Relevance:** Many engineering design problems minimize non-convex objectives (neural network training, structural optimization, control design)
- **Implication:** Guaranteeing convergence to local minima in reasonable time is computationally infeasible in worst case
- **Practical impact:** Focus shifts to local convergence rates, empirical performance, and initialization strategies rather than global guarantees

### 3. **Machine Learning**
- **Neural Network Training:** Finding second-order stationary points in high-dimensional loss landscapes is PLS-hard; explains why convergence guarantees are difficult
- **Implication:** Practitioners should use adaptive learning rates, momentum, and careful initialization rather than waiting for formal convergence proofs

### 4. **Game Theory & Equilibrium Finding**
- **Nash Equilibrium Computation:** Related to finding local optima in potential games; PLS-hardness results inform what equilibrium concepts are computationally tractable

### 5. **Robotics Path Planning**
- **Local Minima in Configuration Space:** Robot motion planning over non-convex obstacle spaces involves finding local minima; PLS-hardness explains why "intelligent" local planning is hard

---

## Common Mistakes / Pitfalls

### 1. **Confusing PLS-hardness with NP-hardness**
- **Mistake:** Thinking PLS-hardness is about decision problems or satisfiability
- **Reality:** PLS-hardness applies to optimization/