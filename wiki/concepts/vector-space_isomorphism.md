# vector-space isomorphism

## Definition

A **vector-space isomorphism** is a linear map $\varphi: V \to W$ between two vector spaces (over the same field) that is bijective—both injective (one-to-one) and surjective (onto). Equivalently, $\varphi$ is an invertible linear transformation that preserves the algebraic structure of the vector space.

In the context of chain complexes and quantum error correction, a vector-space isomorphism $\varphi$ establishes a structure-preserving correspondence between elements of one complex and another, allowing syndromes and error configurations to be mapped between different representations while maintaining the underlying mathematical relations.

### Formal Properties

For $\varphi: V \to W$ to be a vector-space isomorphism:

1. **Linearity:** $\varphi(\alpha u + \beta v) = \alpha\varphi(u) + \beta\varphi(v)$ for all $u, v \in V$ and scalars $\alpha, \beta$
2. **Injectivity:** $\ker(\varphi) = \{0\}$
3. **Surjectivity:** $\text{Im}(\varphi) = W$
4. **Invertibility:** There exists $\varphi^{-1}: W \to V$ such that $\varphi \circ \varphi^{-1} = \text{id}_W$ and $\varphi^{-1} \circ \varphi = \text{id}_V$

Two vector spaces are **isomorphic** if such a bijective linear map exists between them.

## Key Equations

### Basic Isomorphism Maps

In quantum error correction on 2D topological codes, vector-space isomorphisms decompose a code space into tractable components:

$$\varphi_2 = U_Z^{-\dagger}: C_2 \to \bigoplus_{i=1}^{r} \tilde{C}_2^{(i)} \oplus \tilde{A}_2$$

$$\varphi_1 = \begin{pmatrix} V_X^{-1} & 0 \\ 0 & V_Z^{\dagger} \end{pmatrix}: C_1 \to \bigoplus_{i=1}^{r} \tilde{C}_1^{(i)} \oplus \tilde{A}_1$$

$$\varphi_0 = U_X: C_0 \to \bigoplus_{i=1}^{r} \tilde{C}_0^{(i)} \oplus \tilde{A}_0$$

where:
- $C_k$ denotes the $k$-th chain complex of the original code
- $\tilde{C}^{(i)}$ are chain complexes of individual trivial codes
- $\tilde{A}$ represents the trivial product state sector
- $A^{-\dagger} = (A^{\dagger})^{-1}$ denotes the inverse in vector space sense

### Chain Isomorphism Property

The tuple $\varphi = (\varphi_2, \varphi_1, \varphi_0)$ forms a **chain isomorphism** between chain complexes when it commutes with boundary operators $\partial$:

$$\varphi_{k-1} \circ \partial_k = \tilde{\partial}_k \circ \varphi_k$$

for all relevant $k$.

### Direct Sum Decomposition

The isomorphism maps the full complex to a direct sum:

$$C \xrightarrow{\varphi} \bigoplus_{i=1}^{r} \tilde{C}^{(i)} \oplus \tilde{A}$$

Projection maps $\pi^{(i)} = (\pi_2^{(i)}, \pi_1^{(i)}, \pi_0^{(i)})$ and $\pi^A$ extract individual components while preserving the chain structure.

## Physical Intuition / Derivation

### Why Vector-Space Isomorphisms Matter in QEC

In quantum error correction, the original stabilizer code lives in a high-dimensional Hilbert space with complex entanglement patterns. Direct decoding is computationally hard. A vector-space isomorphism provides a **change of basis** that transforms the problem into one or more independent, simpler subproblems.

**Concrete Example:** Consider a 2D topological code under coarse-graining:

1. **Original space:** A single large chain complex $C$ representing syndrome and error spaces
2. **Transformed space:** A direct sum $\bigoplus_i \tilde{C}^{(i)} \oplus \tilde{A}$, where:
   - Each $\tilde{C}^{(i)}$ is a planar graph matching problem (solvable in polynomial time)
   - $\tilde{A}$ is a trivial product state (no decoding needed)

### How the Isomorphism Works

The unitary matrices $U_X$, $U_Z$, $V_X$, $V_Z$ are constructed to:

1. **Separate degrees of freedom:** Decouple the original code into independent trivial codes
2. **Preserve the boundary operator structure:** Ensure $\varphi$ is a chain map
3. **Map error configurations:** Transform Pauli errors on original qubits to errors on the decoupled codes
4. **Map syndromes:** Transform measurement outcomes (syndrome bits) proportionally

The key insight is that **isomorphic spaces have identical algebraic properties**—so decoding one is equivalent to decoding the other, but the new representation may be computationally tractable.

## Applications in Engineering

### 1. Quantum Error Correction & Fault-Tolerance
- **Decoding reduction:** Transform hard decoding problems (NP-hard in general) into parallelizable matching problems
- **Scalability:** Enable efficient classical processing of topological codes for quantum computers
- **Noise model mapping:** Connect experimental noise to theoretical error channels

### 2. Signal Processing & Information Theory
- **Change of basis:** Simplify linear transformations in communications (e.g., source/channel coding)