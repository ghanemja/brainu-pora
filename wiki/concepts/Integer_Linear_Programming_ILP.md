# Integer Linear Programming (ILP)

## Definition

**Integer Linear Programming (ILP)** is an optimization problem where:
- We seek to maximize (or minimize) a linear objective function $c^\top x$
- Subject to linear equality or inequality constraints
- All decision variables must be integers: $x \in \mathbb{Z}^n$

The **standard-form ILP problem** (codimension $k$) is defined as:

$$\begin{align}
\text{maximize} \quad & c^\top x \\
\text{subject to} \quad & Ax = b \\
& x \in \mathbb{Z}^n_{\geq 0}
\end{align}$$

where:
- $A \in \mathbb{Z}^{k \times n}$ is a constraint matrix with full row rank ($\text{rank}(A) = k$)
- $b \in \mathbb{Z}^k$ is the right-hand side vector
- $c \in \mathbb{Z}^n$ is the objective coefficient vector
- $k$ is called the **codimension** of the system (number of equality constraints)
- $\Delta$ denotes the **maximum absolute value of a $k \times k$ minor** of $A$

The **Komlós discrepancy constant** $\kappa_k$ characterizes the minimum achievable maximum deviation (discrepancy) for matrices with $k$ columns having Euclidean norm at most 1.

---

## Key Equations

### Discrepancy Definition
The **discrepancy** of a vector $x \in \mathbb{R}^n$ with respect to a matrix $A$ is:
$$\text{disc}(A, x) = \|Ax - b\|_\infty$$

The **matrix discrepancy** is the minimum achievable discrepancy over all non-zero integer vectors:
$$\kappa_k = \sup_{A: \|a_i\|_2 \leq 1} \min_{x \in \mathbb{Z}^n \setminus \{0\}} \|Ax\|_\infty$$

### Running Time Complexity

**Optimization (maximization) problem:**
$$T_{\text{opt}} = \tilde{O}(\kappa_k)^{2k} \Delta^2 \cdot \text{poly}(n)$$

**Feasibility problem:**
$$T_{\text{feas}} = \tilde{O}(\kappa_k)^k \Delta \cdot \text{poly}(n)$$

Under current bounds where $\kappa_k = e^{\tilde{O}(\log^{1/4} k)}$:
- **Optimization:** $2^{\tilde{O}(k \log^{1/4} k)} \Delta^2 \cdot \text{poly}(n)$
- **Feasibility:** $2^{\tilde{O}(k \log^{1/4} k)} \Delta \cdot \text{poly}(n)$

**Under Komlós Conjecture** (conjectured: $\kappa_k = O(1)$), both reduce to:
$$T = 2^{O(k)} \Delta \cdot \text{poly}(n)$$

---

## Physical Intuition / Derivation

### Why ILP is Hard

Unlike Linear Programming (LP), where variables can be real-valued and solvable in polynomial time, the **integrality constraint** makes ILP NP-hard in general. Geometrically:

1. **LP feasible region** = convex polytope (easy: interior-point methods traverse smooth geometry)
2. **ILP feasible region** = lattice points inside the polytope (discrete, highly non-convex)

The "gap" between LP relaxation and ILP solution can be arbitrarily large, requiring combinatorial search.

### Discrepancy as a Measure of Lattice Sparsity

Komlós discrepancy captures the **inherent structure of integer lattices** under linear transformations:
- A matrix $A$ with **small discrepancy** forces integer solutions to cluster tightly in solution space
- High discrepancy means solutions are spread out, making them harder to enumerate

This is connected to **Hermite normal form** and **Frobenius numbers** in number theory—fundamental properties of how integer lattices align with hyperplanes.

### Dynamic Programming Strategy

The algorithm uses **discrepancy-based DP** where:
1. **State space** partitions the lattice into regions determined by bounds on $\|Ax - b\|_\infty$
2. **Transitions** use bounds on how much $Ax$ can change when modifying integer variables
3. **Pruning** exploits that solutions with large discrepancy can be rejected early

The parameter $\Delta$ (maximum minor) bounds how "twisted" the constraint matrix can be—larger $\Delta$ means more states and longer computation.

---

## Applications in Engineering

### 1. **Operations Research & Supply Chain**
- **Production planning:** Maximize profit subject to integer production quantities
- **Vehicle routing:** Integer number of trucks/routes with capacity constraints
- **Facility location:** Binary variables (open/close facilities) + flow conservation

### 2. **Power Systems & Energy**
- **Unit commitment:** Turn generators on/off (binary); respect ramp rate constraints (linear)
- **Microgrid scheduling:** Integer number of battery cycles, wind turbine settings
- **Transmission switching:** Binary variables for circuit breaker states

### 3. **Chip Design & VLSI**
- **Register allocation:** Assign integer registers to variables subject to precedence constraints
- **Gate placement:** Discrete coordinate optimization on chip layouts
- **Clock tree synthesis:** Integer buffer placement with skew/delay constraints

### 4. **Network Design**
- **Optimal routing:** Integer flow on edges with capacity constraints
- **Network resilience:** Binary edge/node activation with redundancy requirements
- **Spectrum allocation:** Integer frequency assignment in wireless networks

### 5. **Scheduling & Project Management**
- **Job scheduling:** Start times as integers, precedence and resource constraints
- **Timetabling:** Assign tasks to discrete time slots with conflict avoidance
- **Workforce scheduling:** Integer shifts per employee, coverage requirements

### 6. **Resource Allocation**