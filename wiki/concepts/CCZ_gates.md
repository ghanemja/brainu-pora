# CCZ gates

## Definition

The **Controlled-Controlled-Z gate** (CCZ), also called the **Toffoli gate** when expressed in the computational basis, is a three-qubit quantum gate that applies a phase of $-1$ (a Z rotation) to the quantum state if and only if all three qubits are in the $|1\rangle$ state.

**Gate action in the computational basis:**
$$\text{CCZ}|q_1 q_2 q_3\rangle = \begin{cases}
-|q_1 q_2 q_3\rangle & \text{if } q_1 = q_2 = q_3 = 1 \\
|q_1 q_2 q_3\rangle & \text{otherwise}
\end{cases}$$

Equivalently, the CCZ gate is the diagonal unitary:
$$\text{CCZ} = \text{diag}(1, 1, 1, 1, 1, 1, 1, -1)$$

**Relationship to Toffoli:** The CCZ and Toffoli (CCNOT) gates are related by Hadamard conjugation on the target qubit:
$$\text{Toffoli} = (I \otimes I \otimes H) \cdot \text{CCZ} \cdot (I \otimes I \otimes H)$$

This interconvertibility means that optimizing one gate directly translates to the other with only two additional single-qubit gates.

---

## Key Equations

**Matrix representation in the computational basis:**
$$\text{CCZ} = \begin{pmatrix}
1 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
0 & 1 & 0 & 0 & 0 & 0 & 0 & 0 \\
0 & 0 & 1 & 0 & 0 & 0 & 0 & 0 \\
0 & 0 & 0 & 1 & 0 & 0 & 0 & 0 \\
0 & 0 & 0 & 0 & 1 & 0 & 0 & 0 \\
0 & 0 & 0 & 0 & 0 & 1 & 0 & 0 \\
0 & 0 & 0 & 0 & 0 & 0 & 1 & 0 \\
0 & 0 & 0 & 0 & 0 & 0 & 0 & -1
\end{pmatrix}$$

**Phase polynomial encoding:** For a Clifford+T circuit, the phase operator can be expressed as a polynomial over $\mathbb{F}_2$ (binary field), where CCZ gates appear through **CP decomposition** of signature tensors. A rank-1 CP term contributes a single CCZ gate acting on parity qubits.

**Conversion cost:**
$$\text{CCZ} \leftrightarrow \text{Toffoli: cost of } 2H \text{ gates}$$

---

## Physical Intuition / Derivation

### Why Three Qubits?

The CCZ gate implements a **three-body interaction**, the minimum necessary for universal quantum computation beyond Clifford gates. Two-qubit controlled gates (CZ, CNOT) form the Clifford group and cannot create entanglement in certain quantum algorithms; a third control qubit enables non-Clifford phase manipulations.

### Interpretation as Phase Accumulation

The CCZ gate can be understood as a **conditional phase gate**: it applies a phase to the joint state only when a specific combinatorial condition is met (all three qubits high). This is natural for implementing:
- **Arithmetic circuits** over finite fields where operations depend on multiple bit conditions
- **Phase polynomials** in the Clifford+T formalism, where non-Clifford gates are isolated as phase corrections

### CP Decomposition Context

In the source material, CCZ gates arise from **CP (Canonical Polyadic) decomposition** of cubic symmetric tensors:

$$T(i,j,k) = \sum_{r=1}^{r_{\text{cp}}} a_r(i) \cdot a_r(j) \cdot a_r(k)$$

Each rank-1 term corresponds to a single CCZ gate acting on **parity qubits** (linear combinations of the original qubits). The CP rank $r_{\text{cp}}$ directly determines the number of CCZ gates needed—a critical optimization target for fault-tolerant quantum circuits.

### Hadamard Conjugation to Toffoli

The equivalence to Toffoli via Hadamard conjugation emerges because:
- CCZ applies phase based on state ownership (diagonal operation)
- Toffoli applies a NOT conditioned on two controls
- Hadamards convert between phase (Z-basis) logic and bit-flip (X-basis) logic

---

## Applications in Engineering

### 1. **Clifford+T Circuit Optimization**

CCZ gates are a primary target for optimization in fault-tolerant quantum computing. Since Clifford+T is the universal gate set most compatible with surface codes, minimizing CCZ (or equivalently Toffoli) count directly reduces:
- Physical qubit overhead
- Circuit depth and error accumulation
- Quantum volume requirements

### 2. **Finite Field Arithmetic**

CCZ gates efficiently implement multiplication and inversion in $\text{GF}(2^n)$ (Galois fields), critical for:
- Post-quantum cryptography circuits (lattice-based, code-based schemes)
- AES and other symmetric encryption on quantum computers
- Elliptic curve arithmetic

The tensor decomposition methods yield improved Toffoli counts for polynomial multiplication over $\mathbb{F}_2$.

### 3. **Phase Polynomial Realization**

In the phase polynomial representation of quantum circuits, the non-Clifford operator can be decomposed as:
$$U_{\text{phase}} = \prod_{(i,j,k)} \text{CCZ}_{i,j,k}^{c_{ijk