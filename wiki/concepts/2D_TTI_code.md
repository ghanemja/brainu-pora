# 2D TTI Code

## Definition

A **2D Translation-Translationally Invariant (TTI) code** is a CSS (Calderbank-Shor-Steane) topological quantum error-correcting code defined on a 2D lattice where qubits are placed on edges, and stabilizer checks are labeled by lattice sites. The code is characterized by translation symmetry in both spatial dimensions, enabling a compact representation using Laurent polynomials in two variables.

In the standard formulation, qubits reside on a 2D lattice with $n$ sites, each accommodating 2 qubits: one on the horizontal edge and one on the vertical edge. The code structure is captured entirely by a parity-check matrix expressed as a $2 \times 2$ block matrix of Laurent polynomials over $\mathbb{F}_2$.

## Key Equations

### Parity-Check Matrix Representation

The parity-check matrix of a 2D TTI code is:

$$H = \begin{pmatrix} H_X & 0 \\ 0 & H_Z \end{pmatrix} = \begin{pmatrix} 1 + x & 1 + y & 0 & 0 \\ 0 & 0 & 1 + x^{-1} & 1 + y^{-1} \end{pmatrix}$$

where:
- $x$ and $y$ are Laurent polynomial variables representing spatial translations in the horizontal and vertical directions
- $H_X$ encodes the $X$-type stabilizer checks
- $H_Z$ encodes the $Z$-type stabilizer checks
- The $(*)$ denotes the **antipode map**: $f(x,y)^* = \sum_{i,j} a_{ij} x^{-i} y^{-j}$ for $f(x,y) = \sum_{i,j} a_{ij} x^i y^j$

### Dagger Operation (Hermitian Conjugate)

$$H^\dagger = \begin{pmatrix} H_X^\dagger & 0 \\ 0 & H_Z^\dagger \end{pmatrix} = \begin{pmatrix} 1 + x^{-1} & 0 & 1 + y^{-1} & 0 \\ 0 & 1 + y & 0 & 1 + x \end{pmatrix}$$

The dagger operation transposes the matrix and applies the antipode map to each entry.

### Qubit Support Identification

For a horizontal qubit at site $(i,j)$:

$$H \begin{pmatrix} x^i y^j \\ 0 \\ x^i y^j \\ 0 \end{pmatrix}^T = \begin{pmatrix} x^i y^j + x^{i+1} y^j \\ x^i y^j + x^i y^{j+1} \end{pmatrix}^T$$

For a stabilizer check labeled by monomial $x^i y^j$:

$$\begin{pmatrix} x^i y^j & 0 \end{pmatrix} H = \begin{pmatrix} x^i y^j + x^{i+1} y^j & x^i y^j + x^i y^{j+1} \end{pmatrix}$$

These operations reveal the **2-nearest-neighbor structure** of the code.

## Physical Intuition / Derivation

### Lattice Structure and Qubit Placement

The 2D TTI code is built on a checkerboard-like 2D lattice where:
- Each site $(i,j)$ can host 2 qubits
- One qubit occupies the *horizontal edge* (connecting site $(i,j)$ to $(i+1,j)$)
- One qubit occupies the *vertical edge* (connecting site $(i,j)$ to $(i,j+1)$)

This edge-based qubit placement naturally encodes directional information.

### Translation Symmetry and Laurent Polynomials

The key insight is that stabilizer generators are **translation-invariant**. Rather than specifying stabilizers individually for each site, we encode them as Laurent polynomials where:
- The variable $x$ shifts indices in the horizontal direction: $x \cdot f(x,y) \to f(x,y)$ at site $(i+1, j)$
- The variable $y$ shifts indices in the vertical direction: $y \cdot f(x,y) \to f(x,y)$ at site $(i, j+1)$

A Laurent polynomial $1 + x$ in the parity-check matrix means a stabilizer check acts on qubits at positions related by horizontal translation (i.e., spanning from $x^i y^j$ to $x^{i+1} y^j$).

### CSS Code Structure

The block-diagonal form $\begin{pmatrix} H_X & 0 \\ 0 & H_Z \end{pmatrix}$ enforces:
- $X$-type stabilizers (tracked by $H_X$) act only on the qubits they constrain via their $X$ operators
- $Z$-type stabilizers (tracked by $H_Z$) act only on their qubits via $Z$ operators
- Orthogonality condition: $H_X H_Z^T = 0$ (modulo 2)

The antipode map in $H_Z = H_X^*$ ensures this orthogonality is maintained under the translation symmetry.

### Nearest-Neighbor Locality

The specific form $H_X = (1+x, 1+y)$ ensures each qubit is acted upon by exactly **two nearest-neighbor stabilizer checks**—one in each direction. This locality is crucial for:
- Efficient classical decoding algorithms
- Robust fault-tolerant quantum computation
- Topological protection (local indistinguishability of errors)

## Applications in Engineering

### Quantum Error Correction
2D TTI codes are fundamental to practical quantum computing:
- **Surface codes** (the most mature topological code for near-term devices) are instances of 2D TTI codes