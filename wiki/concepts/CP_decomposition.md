# CP Decomposition

## Definition

**CP decomposition** (Canonical Polyadic decomposition, also called tensor rank decomposition or PARAFAC) is a factorization method that expresses a multi-dimensional tensor as a sum of rank-1 components. In the context of quantum circuit optimization, CP decomposition decomposes a cubic phase polynomial tensor into a sum of outer products:

$$T = \sum_{i=1}^{r_{cp}} \mathbf{a}_i \otimes \mathbf{b}_i \otimes \mathbf{c}_i$$

where $r_{cp}$ is the CP rank (minimal number of rank-1 terms needed), and each rank-1 component is an outer product of vectors.

For quantum gate implementation, this decomposition directly translates to a sum of **CCZ (Controlled-Controlled-Z) gates** acting on parity qubits, with the rank $r_{cp}$ determining the gate count. Each rank-1 term corresponds to one Toffoli (or equivalent CCZ) gate in the quantum circuit.

## Key Equations

**Tensor representation:**
$$T_{ijk} = \sum_{\ell=1}^{r_{cp}} A_{i\ell} B_{j\ell} C_{k\ell}$$

where $T$ is a cubic (order-3) tensor and $A, B, C$ are factor matrices.

**Gate cost relation:**
$$\text{CCZ gate count} = r_{cp}$$

**Relationship to phase polynomials** (in $\mathbb{F}_2$):
A symmetric order-3 signature tensor represents a phase operator implementable via CCZ gates, where the CP rank bounds the quantum resource requirement.

## Physical Intuition / Derivation

### Motivation in Quantum Circuits

Quantum circuits in the Clifford+T universal gate set require minimizing non-Clifford gates (T-gates and CCZ/Toffoli gates) for fault tolerance. The phase operator of such circuits can be represented as a tensor:

1. **Phase polynomial encoding**: Each quantum circuit induces a phase polynomial—a multilinear function over $\mathbb{F}_2$ capturing which computational paths accumulate phase shifts.

2. **Tensor representation**: This polynomial maps naturally to a tensor where each entry encodes phase contributions for input combinations.

3. **Decomposition benefit**: Finding a low-rank CP decomposition of this tensor directly yields a circuit with fewer CCZ gates—each rank-1 component implements one controlled phase operation.

### Algorithmic Connection

The decomposition exploits the fact that a rank-1 tensor $\mathbf{a} \otimes \mathbf{b} \otimes \mathbf{c}$ has a particularly simple quantum implementation:
- Compute parities (CNOT operations)
- Apply a single CCZ gate
- Uncompute parities

Minimizing the number of such terms minimizes gate count.

### NP-Hardness Context

Finding the optimal CP rank is **NP-hard** in general, motivating development of heuristic algorithms including:
- **Symplectic Gaussian Elimination (SGE)** for direct rank reduction
- **Basis change optimization** to reduce algebraic thickness
- **Flip graph search** for cubic phase polynomial optimization

## Applications in Engineering

### 1. **Quantum Circuit Synthesis and Optimization**
   - Primary use: Minimize CCZ/Toffoli gate counts in fault-tolerant quantum computers
   - Reduces resource overhead for error correction
   - Applicable to any circuit decomposable into phase operators (Clifford+T universal gate sets)

### 2. **Finite Field Arithmetic**
   - **GF(2ᵖ) multiplication circuits**: CP decomposition yields improved Toffoli counts for polynomial multiplication over $\mathbb{F}_2$
   - Critical for cryptographic and error-correcting code implementations in quantum processors

### 3. **Quantum Algorithm Compilation**
   - Benchmarked on standard circuit families (QFT₄, arithmetic circuits)
   - Provides automated optimization with fixed hyperparameters and modest computational overhead
   - Enables portable quantum compilation across hardware architectures

### 4. **Gate Minimization for NISQ Devices**
   - Addresses practical constraints of near-term quantum computers
   - Reduces circuit depth and error propagation through fewer high-depth gates

## Common Mistakes / Pitfalls

### 1. **Confusing CP rank with tensor dimensions**
   - **Error**: Assuming CP rank equals tensor size
   - **Reality**: CP rank can be much smaller (or occasionally larger in degenerate cases); it measures minimal decomposition, not size

### 2. **Treating CP decomposition as unique**
   - **Error**: Assuming the decomposition is unique once found
   - **Reality**: CP decomposition is not unique in general; multiple distinct decompositions may yield the same rank

### 3. **Greedy optimization without initialization**
   - **Error**: Running iterative rank-reduction algorithms from random initialization
   - **Reality**: CP decomposition provides superior initialization for subsequent Waring decomposition and T-count optimization; proper seeding dramatically improves convergence

### 4. **Ignoring symmetry structure**
   - **Error**: Treating generic tensors the same as symmetric tensors
   - **Reality**: Symmetric order-3 tensors (like phase polynomials) have special structure; exploiting this yields better bounds

### 5. **Overlooking parity constraints**
   - **Error**: Forgetting that quantum implementations restrict to parity-based bases
   - **Reality**: CCZ gates act on **parity qubits** (linear combinations of computational basis qubits), requiring careful basis tracking

## Relationship to Other Decompositions

In the quantum gate optimization context, CP decomposition complements:

- **[[Waring Decomposition]]** — decomposes symmetric tensors as sum of powers of linear forms; used for T-count optimization (rank-$r_w$ ↔ $r_w$ T gates)
- **[[Tensor Decomposition]]** — broader framework encompassing Tucker, Tensor Train, and other factorizations
- **[[Phase Polynomial Representation]]** — the underlying encoding of quantum circuit phase information that makes tensor methods applicable
- **[[Symplectic Gaussian Elimination]]** — algorithm for reducing CP rank via linear algebra over $\mathbb{F}_2$
- **[[Clifford+