# Partial Trace

## Definition

The **partial trace** is a mathematical operation that reduces a composite quantum system to a subsystem by "tracing out" or discarding information about the remaining degrees of freedom. 

Formally, given a density matrix (or more generally, a tensor) on a composite Hilbert space $\mathcal{H}_A \otimes \mathcal{H}_B$, the partial trace over subsystem $B$ is defined as:

$$\text{Tr}_B(\rho_{AB}) = \sum_{j} (\mathbb{I}_A \otimes \langle j|_B) \rho_{AB} (\mathbb{I}_A \otimes |j\rangle_B)$$

where the sum runs over a complete basis $\{|j\rangle_B\}$ of $\mathcal{H}_B$.

The result is a reduced density matrix $\rho_A$ acting on subsystem $A$ alone, containing all statistics measurable on $A$ but with $B$'s information discarded.

## Key Equations

**Formal definition (basis-independent):**
$$\text{Tr}_B(\rho_{AB}) = \sum_{j=1}^{d_B} (\mathbb{I}_A \otimes \langle j|_B) \rho_{AB} (\mathbb{I}_A \otimes |j\rangle_B)$$

**In index notation (as used in tensor networks):**
$$\rho_A^{i\mu} = \sum_{j} \rho_{AB}^{ij\mu j}$$

where indices $\{i,\mu\}$ label subsystem $A$ and repeated index $j$ is summed over subsystem $B$.

**Key property — expectation values:**
$$\langle O_A \rangle = \text{Tr}(O_A \rho_A) = \text{Tr}(O_A \otimes \mathbb{I}_B \, \rho_{AB})$$

Measurements on subsystem $A$ depend only on $\rho_A = \text{Tr}_B(\rho_{AB})$.

## Physical Intuition / Derivation

### Conceptual Motivation

In quantum mechanics, we often have a system composed of multiple parts: a system of interest (A) and an environment or auxiliary system (B). The partial trace operationally represents:

1. **Averaging over unmeasured degrees of freedom** — if we cannot or do not measure subsystem $B$, its information is lost from our perspective
2. **Decoherence and entanglement destruction** — entanglement between $A$ and $B$ appears as mixed-state behavior in $\rho_A$
3. **Information loss** — the operation is irreversible; $\rho_A$ contains less information than $\rho_{AB}$

### Derivation Sketch

Consider measuring observable $O_A$ on subsystem $A$ only. The expectation value in the full system is:

$$\langle O_A \rangle = \text{Tr}((O_A \otimes \mathbb{I}_B)\rho_{AB}) = \sum_{i,i',j,j'} \langle i,j|(O_A \otimes \mathbb{I}_B)|i',j'\rangle \rho_{AB}^{i'j',ij}$$

Evaluating the matrix elements of the observable:
$$= \sum_{i,i',j} O_A^{ii'} \rho_{AB}^{i'j,ij} = \sum_{i,i'} O_A^{ii'} \left(\sum_j \rho_{AB}^{i'j,ij}\right)$$

Defining $\rho_A^{i'i} := \sum_j \rho_{AB}^{i'j,ij}$ gives $\langle O_A \rangle = \text{Tr}(O_A \rho_A)$.

Thus, $\rho_A = \text{Tr}_B(\rho_{AB})$ encodes all statistics of measurements on $A$ alone.

### Tensor Network Perspective

In tensor network algorithms (as in the source material), the partial trace is implemented by **contracting (summing over) the index corresponding to subsystem $B$**. The "partial trace superposition tensor" (Fig. 12b) marked with notation such as:

$$P^+_{d,i} = 1 \quad \text{(summed over matching index)}$$

explicitly performs this contraction in a structured way during tensor network contractions, effectively discarding entanglement with traced-out subsystems.

## Applications in Engineering

### 1. Quantum Computing & Noise Modeling
- **Decoherence analysis**: Partial traces model loss of quantum information to the environment, predicting mixed states of qubits affected by noise
- **Reduced density matrices**: Engineers compute $\rho_{\text{system}} = \text{Tr}_{\text{env}}(\rho_{\text{system+env}})$ to analyze qubit quality and gate fidelity

### 2. Tensor Network Algorithms
- **Variational methods** (PEPS, DMRG): Partial traces compute local reduced states to optimize tensor networks efficiently
- **Ground state computation**: Contracting auxiliary indices allows numerical simulation of many-body quantum systems on classical computers

### 3. Quantum Information Theory
- **Entanglement quantification**: Measuring purity loss from $\text{Tr}(\rho_A^2)$ quantifies entanglement between subsystems
- **Quantum channel analysis**: Partial trace over input states characterizes quantum channels' behavior

### 4. Statistical Mechanics
- **Reduced distributions**: Averaging over microstates to obtain macroscopic observables (analogous operation in classical systems)

### 5. Control & Open Quantum Systems
- **Lindblad equation evolution**: Deriving master equations for system dynamics requires partial traces over bath degrees of freedom

## Common Mistakes / Pitfalls

### 1. **Confusing with Full Trace**
- $\text{Tr}(\rho_{AB}) = 1$ (full trace, preserves normalization)
- $\text{Tr}_B(\rho_{AB