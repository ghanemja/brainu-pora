# SDP Relaxation

## Definition

**SDP relaxation** (Semidefinite Programming relaxation) is a convex optimization technique that relaxes a computationally hard combinatorial or algebraic constraint satisfaction problem into a semidefinite program, which can be solved in polynomial time. 

In the context of constraint satisfaction problems (CSPs), an SDP relaxation transforms discrete constraints into continuous vector representations, typically mapping domain elements to vectors in $\mathbb{R}^N$ or finite fields. The key idea is to replace hard combinatorial conditions with weaker linear/bilinear algebraic conditions on vectors while preserving the essential structure of the original problem.

For a minion $M$ describing a problem class, an SDP relaxation finds vectors:
$$v_x(a) \in \mathbb{R}^N \text{ (or } \mathbb{Z}^N_2\text{) for each domain element } a \in D_x$$

such that:
- Vectors satisfy orthogonality or near-orthogonality conditions
- Original constraints map to algebraic conditions on inner products
- The solution is polynomially computable


## Key Equations

### Standard SDP Relaxation Condition

For vectors $v, w$ representing domain elements, the relaxation typically enforces:

$$M(v, w) + M(w, v) = w(v) \cdot w(w) + v \cdot w$$

where:
- $M$ is a bilinear form on the vector space
- $w(v)$ denotes the *weight* (coordinate sum modulo field characteristic)
- $v \cdot w$ is the standard inner product

### Minion Summation in SDP

For a function $\alpha: D \to E$, the relaxation maintains:

$$\sum_{a \in D} v_a = i$$

where $i$ is a unit-weight vector independent of the specific constraint. This ensures the solution aggregates correctly across constraints.

### Orthogonality Constraint

For each constraint $x$, vectors assigned to distinct domain elements must be pairwise orthogonal:

$$v_x(a) \cdot v_x(b) = \delta_{ab} \quad (\text{or similar orthogonality condition})$$

where $\delta_{ab}$ is the Kronecker delta (up to relaxation tolerance).

### Gram Matrix Representation

The fundamental connection between vector representations and SDP is through Gram matrices:

$$G_{ab} = v_a \cdot v_b$$

The problem is feasible if and only if $G$ is positive semidefinite (PSD), i.e., $G \succeq 0$.


## Physical Intuition / Derivation

### Why Relax?

Many CSPs are NP-hard in their original discrete form. For example:
- Graph coloring with few colors
- Satisfiability problems
- Integer programming

Computing exact solutions requires exponential time in the worst case. An SDP relaxation trades exactness for computational tractability.

### From Discrete to Continuous

**The key insight:** Instead of assigning discrete values (e.g., colors $\{0, 1\}$) to variables, we assign unit vectors in high-dimensional space. 

- **Original problem:** $f(a) \in \mathbb{Z}_2$  
- **Relaxed problem:** $v(a) \in \mathbb{R}^N$ with $\|v(a)\| = 1$

Constraints are "softened" by expressing them as linear/bilinear forms on the vectors. The space of possible vectors is much larger than the discrete set, making the problem easier to solve.

### The Convexity Advantage

Semidefinite programs are **convex optimization problems**:
- Any local optimum is a global optimum
- Interior-point methods solve them in polynomial time (e.g., $O(n^{3.5})$)
- Multiple algorithms: ellipsoid method, interior-point, first-order methods

### Connection to the Fundamental Theorem of PCSPs

The source material references PCSPs (Promise Constraint Satisfaction Problems) and shows that SDP relaxations can be combined with field relaxations (e.g., $\mathbb{Z}_p^2$) to obtain minion homomorphisms that characterize solution structure. The vector representation bridges discrete combinatorial structure and continuous convex geometry.


## Applications in Engineering

### 1. **Communication & Coding Theory**
- **Decoding hard instances:** SDP relaxations approximate maximum-likelihood decoding for error-correcting codes
- **Sparse recovery:** Compressed sensing uses SDP to recover sparse signals from few measurements
- Example: LDPC code decoding via semidefinite relaxations of the original combinatorial problem

### 2. **Control & Optimization**
- **Robust control:** SDP methods synthesize controllers for systems with uncertain parameters
- **Convex relaxation of non-convex control laws:** Original problem may be bilinear; SDP relaxation makes it tractable
- **Sum-of-squares (SOS) methods:** Relax polynomial non-negativity into SDP constraints

### 3. **Electrical Engineering (Power Systems)**
- **Optimal power flow (OPF):** Dispatch generators to minimize cost while respecting physical constraints
  - Original AC-OPF is non-convex
  - Rank-1 or low-rank SDP relaxations provide tight bounds on optimal cost
- **Stability analysis:** Lyapunov functions for networked systems via SDP
- Example: $10^{-4}$ to $10^{-2}$ optimality gap for IEEE test cases

### 4. **Machine Learning**
- **Kernel methods:** SDP relaxations of clustering and max-cut problems
- **Semidefinite embeddings:** Learn similarity matrices that satisfy PSD constraints
- **Structured prediction:** Relax discrete label assignment into continuous relaxation

### 5. **Operations Research**
- **Max-cut problem:** SDP relaxation (Goemans-Williamson algorithm) achieves 0.878-approximation
  - Best known classical algorithm
  - Widely used in VLSI design (circuit partitioning)
- **Graph coloring:** SDP bounds on chromatic number
- **Quadratic assignment:** Relax permutation matrices into doubly-stochastic matrices in SDP

### 6. **Mechanical/Aerospace Engineering**
- **Structural optimization