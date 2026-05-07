# bond dimension

## Definition

The **bond dimension** is the maximum size of the index connecting two adjacent tensors in a tensor network. It determines the number of degrees of freedom carried along the "bonds" (connections) between tensor nodes.

Formally, in a tensor network where adjacent tensors are connected by contraction indices, if a bond connects two tensors, the bond dimension $d$ specifies how many distinct values that index can take. When representing a tensor network as matrices (a common computational approach), a bond dimension $d$ with $k$ neighbors per tensor results in matrix dimensions of $d^k × d^k$.

## Key Equations

For a tensor network representation using matrices:

**Matrix dimensions from bond dimension:**
$$\text{Matrix size} = d^k × d^k$$

where:
- $d$ = bond dimension (size of each individual bond)
- $k$ = number of neighbors interacting with a given tensor

**Computational complexity scaling:**

- **Tensor method:** $O(knd^k)$
- **Matrix-vector method:** $O(nd^{2k})$ (naive), $O(nd^{k+1})$ (with sparsity exploitation)
- **With intermediate reuse:** $O(nd^{k+1})$ total

The key scaling relationships are:
$$\text{Operations per contraction} \propto d^{k+1}$$
$$\text{Memory per tensor} = O(d^{k+1}) \text{ (sparse case)}$$

## Physical Intuition / Derivation

### Why Bond Dimension Matters

Imagine decomposing a complex system into a chain of simpler components (tensors). Each component must store information about how it connects to neighbors. The bond dimension quantifies *how much information* flows across each connection.

**Building intuition through an example:**

Consider a tensor network representing a quantum system or probabilistic graphical model:
- Each tensor encodes local information about one variable/site
- Bonds represent dependencies between neighboring sites
- A small bond dimension $d$ limits how much "entanglement" or correlation can be captured
- Larger $d$ provides richer representation but increases computational cost

### Transformation to Matrix Form

The document illustrates converting 4-order tensors to matrices: if tensor $M_3$ has 6 indices formed by $3 × 2$ neighbor pairs, it becomes an $d^3 × d^3$ matrix. This flattening preserves all information but changes the algorithmic structure, allowing use of highly optimized linear algebra libraries.

### Sparsity and Complexity Reduction

The tensors in these networks exhibit inherent sparsity: each tensor has $k-1$ pairs of input-output indices with matching values (constraints from the problem structure). This means despite nominal size $d^{k+1}$, only $O(d^{k+1})$ elements are actually non-zero, enabling dramatic complexity reduction compared to dense matrix operations.

## Applications in Engineering

### Tensor Network Contraction Problems
- **Quantum circuit simulation:** Bond dimensions represent entanglement capacity; managing them is crucial for classically simulating quantum algorithms
- **Probabilistic inference:** In graphical models, bond dimension relates to the complexity of representing marginal distributions

### Machine Learning & Scientific Computing
- **Neural network compression:** Related to rank reduction and dimensionality reduction techniques
- **Sparse tensor decomposition:** Engineering systems with many variables benefit from controlled bond dimensions
- **Numerical PDEs:** Tensor network methods with bounded bond dimensions solve high-dimensional differential equations efficiently

### Optimization & Constraint Problems
- The source material applies this to **QUDO (Quadratic Unconstrained Discrete Optimization)** solvers
- Systems where variables interact with few neighbors (low $k$) can exploit small bond dimensions
- Computational savings are significant: $O(nd^{k+1})$ vs. naive $O(n^{2k})$ scaling

### Signal Processing
- Hierarchical signal decomposition with controlled bandwidth (bond dimension) per level
- Efficient filtering in multi-scale analysis

## Common Mistakes / Pitfalls

### 1. **Confusing Bond Dimension with System Size**
Bond dimension $d$ is not the number of variables $n$—it's the per-connection bandwidth. A large system can have small bond dimensions if correlations are localized.

### 2. **Overlooking the Neighbor Dependence**
The complexity doesn't just scale with $d$; it scales with $d^k$ where $k$ is the number of neighbors. A modest increase in $k$ dramatically raises computational cost. This severely limits applicability to sparse-neighbor problems.

### 3. **Missing Sparsity Exploitation**
Naive matrix multiplication with $d^k × d^k$ matrices appears to cost $O(d^{2k})$, but the inherent sparsity reduces this to $O(d^{k+1})$. Implementations that don't exploit this structure waste computational resources.

### 4. **Not Reusing Intermediate Computations**
The document emphasizes that reusing intermediate contractions reduces full network contraction from $O(n^2d^{k+1})$ to $O(nd^{k+1})$. Naive sequential contraction ignores this savings.

### 5. **Assuming Universal Applicability**
These methods are efficient *only when $k$ is small*. For fully-connected graphs or dense tensor networks, bond dimension arguments don't provide speedup.

## See Also

- [[Tensor Network Contraction]] – framework for understanding how bond dimensions affect overall network complexity
- [[Graphical Models and Factor Graphs]] – probabilistic interpretation of tensor networks and bond structure
- [[Sparse Tensor Decomposition]] – mathematical techniques exploiting sparsity to reduce complexity
- [[Tree Tensor Network States]] – hierarchical tensor structures where bond dimension controls representational power
- [[Quantum Circuit Simulation]] – application domain where bond dimension = entanglement entropy, limiting classical simulation

## Sources

- Lecture/paper excerpt on tensor network contraction with computational complexity analysis (focus on Sections III.B.2, complexity calculations, matrix-vector formulation)
- Discussion of transformation from 4-order tensor to matrix representation (Fig. 5 context)
- Application to QUDO solver and sparse tensor optimization