# Stabilizer Codes

## Definition

**Stabilizer codes** are a class of quantum error-correcting codes defined by a set of commuting Hermitian operators (stabilizers) whose eigenspaces encode logical quantum information. An $n$-qubit stabilizer code is characterized by a stabilizer group $\mathcal{S}$—an abelian subgroup of the Pauli group $\mathcal{P}_n$—where the code space is the common $+1$ eigenspace of all stabilizers.

For CSS (Calderbank-Shor-Steane) stabilizer codes, the stabilizer group factors into separate X and Z stabilizers:
$$\mathcal{S} = \langle X \text{ stabilizers} \rangle \times \langle Z \text{ stabilizers} \rangle$$

where X stabilizers act exclusively with Pauli X operators and Z stabilizers with Pauli Z operators. This structure enables independent correction of bit-flip and phase-flip errors.

### Parity-Check Matrix Formulation

For CSS codes on lattices (e.g., 2D topological codes), the parity-check matrix is block-diagonal:

$$H = \begin{pmatrix} H_X & 0 \\ 0 & H_Z \end{pmatrix}$$

where $H_X$ and $H_Z$ are typically represented as matrices over Laurent polynomials in spatial coordinates. For a 2D lattice with qubits on edges:

$$H_X = \begin{pmatrix} 1 + x \\ 1 + y \end{pmatrix}, \quad H_Z = \begin{pmatrix} 1 + y^{-1} \\ 1 + x^{-1} \end{pmatrix}$$

The columns correspond to horizontal and vertical edges; entries in $\mathbb{F}_2[x^{\pm 1}, y^{\pm 1}]$ (Laurent polynomials over $\mathbb{F}_2$) represent which qubits each stabilizer acts on.

---

## Key Equations

### Stabilizer Action via Matrix Operations

For a qubit labeled by monomial $x^i y^j$:

$$H \begin{pmatrix} x^i y^j \\ 0 \\ x^i y^j \\ 0 \end{pmatrix}^{\top} = \begin{pmatrix} x^i y^j + x^{i+1} y^j \\ x^i y^j + x^i y^{j+1} \end{pmatrix}^{\top}$$

This shows that a horizontal qubit at site $(i,j)$ is checked by X stabilizers at $(i,j)$ and $(i+1,j)$, and by Z stabilizers at $(i,j)$ and $(i,j+1)$.

### Antipode Map (Dagger Operation)

The dagger operation on the parity-check matrix applies the antipode map $*$ to each entry:

$$f(x,y)^* = \sum_{i,j} a_{ij} x^{-i} y^{-j} \quad \text{for} \quad f(x,y) = \sum_{i,j} a_{ij} x^i y^j$$

This ensures the dual code respects the lattice geometry. For the transpose:

$$H^{\dagger} = \begin{pmatrix} H_X^{\dagger} & 0 \\ 0 & H_Z^{\dagger} \end{pmatrix} = \begin{pmatrix} 1 + x^{-1} & 0 & 1 + y^{-1} & 0 \\ 0 & 1 + y & 0 & 1 + x \end{pmatrix}$$

### Logical Operators

Logical X and Z operators commute with all stabilizers but are not themselves in $\mathcal{S}$. They form a quotient group:

$$\text{Logical operators} \in \mathcal{P}_n / \mathcal{S}$$

The number of encoded logical qubits is:
$$k = \log_2(\dim \text{code space}) = n - \text{rank}(H)$$

---

## Physical Intuition / Derivation

### Why Stabilizers?

Measurement of a stabilizer $g \in \mathcal{S}$ on an encoded state yields eigenvalue $+1$ (for states in the code space). If an error $e$ occurs, measurement returns $-1$ for those stabilizers anticommuting with $e$:

$$\{e, g\} \neq 0 \implies \langle g \rangle_{\text{post-measurement}} = -1$$

The pattern of $-1$ eigenvalues (the **syndrome**) reveals error type and location without destroying quantum information.

### Lattice Geometry

In 2D topological codes (e.g., toric code), stabilizers are assigned to lattice plaquettes and vertices:
- **Plaquette (Z) stabilizers**: measure parity of 4 Z operators on edges surrounding a face
- **Vertex (X) stabilizers**: measure parity of 4 X operators meeting at a vertex

Each qubit couples to exactly 4 stabilizers (2 X, 2 Z). This nearest-neighbor structure enables local, efficient error correction.

### Distance and Encoding

The **code distance** $d$ is the minimum weight of a non-trivial logical operator. For 2D codes on lattices of size $L$:
$$d \sim L$$

Logical information persists as global, non-local degrees of freedom—the code encodes $k=2$ logical qubits in $O(L^2)$ physical qubits, with distance $O(L)$.

---

## Applications in Engineering

### Quantum Computing

- **Error mitigation on near-term devices**: Surface codes (a CSS stabilizer code variant) are the leading candidate for fault-tolerant quantum computing; IBM, Google, and IonQ develop surface code implementations.
- **Logical qubit encoding**: Stabilizer codes protect quantum algorithms (Shor's, Grover's, VQE) against decoherence and gate errors.

### Quantum Communication