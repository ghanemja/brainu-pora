# Lindbladian

## Definition

A **Lindbladian** is the generator of a quantum dynamical semigroup—the quantum mechanical analogue of a classical Markov process. It describes the continuous-time evolution of a quantum system that is open (interacting with an environment) and non-unitary.

Formally, the Lindbladian $\mathcal{L}$ acts on density operators $\rho$ via:

$$\frac{d\rho}{dt} = \mathcal{L}(\rho)$$

The standard form of a Lindbladian is:

$$\mathcal{L}(\rho) = -\frac{i}{\hbar}[H, \rho] + \sum_k \gamma_k \left(L_k \rho L_k^\dagger - \frac{1}{2}\{L_k^\dagger L_k, \rho\}\right)$$

where:
- $H$ is the system Hamiltonian
- $L_k$ are **Lindblad operators** (or "jump operators") describing coupling to the environment
- $\gamma_k \geq 0$ are decay rates
- $\{A, B\} = AB + BA$ is the anticommutator

A Lindbladian is said to **satisfy detailed balance** with respect to a state $\sigma$ if:

$$\text{Tr}(A^\dagger \mathcal{L}(B) \sigma) = \text{Tr}(B^\dagger \mathcal{L}(A) \sigma)$$

for all operators $A, B$. This ensures the stationary state is $\sigma$ and the evolution respects thermodynamic equilibrium.

## Key Equations

### Standard Lindblad Master Equation
$$\frac{d\rho}{dt} = -\frac{i}{\hbar}[H, \rho] + \mathcal{D}(\rho)$$

where the **dissipative term** is:

$$\mathcal{D}(\rho) = \sum_k \gamma_k L_k \rho L_k^\dagger - \frac{\gamma_k}{2}(L_k^\dagger L_k \rho + \rho L_k^\dagger L_k)$$

### Mixing Time via Dobrushin Condition
For a quasi-local Lindbladian mixing to a Gibbs state $\sigma$ with decay rates $\gamma_k$, the **mixing time** (time to reach within $\varepsilon$ of the stationary state) is:

$$t_{\text{mix}}(\varepsilon) = O\left(\frac{\log(n/\varepsilon)}{c_{\text{gap}}}\right)$$

where $c_{\text{gap}}$ is the spectral gap (related to the contraction rate in the Dobrushin framework):

$$c_{\text{gap}} \sim \min_j \sum_k \gamma_k |\langle \text{overlap in sector } k \rangle|$$

For the canonical choice with arbitrary on-site field $h$ and inverse temperature $\beta$:

$$c_{\text{diag}} := \frac{e^{-1/4}}{\sqrt{2}} \quad \text{(universal constant independent of } h \text{ and } \beta\text{)}$$

### Contraction in Pauli Sectors
When the local Hamiltonian is diagonal in the Z-basis with $V_j = \frac{h}{2}\sigma_Z^{(j)}$, contraction rates in different Pauli sectors are:

- **X/Y sector**: $1 - \delta \int_{-\infty}^{\infty} \gamma_j(\omega) (a^2 + b^2 + 2c^2) d\omega$
- **Z sector**: $1 - \delta \int_{-\infty}^{\infty} \gamma_j(\omega) (2a^2 + 2b^2) d\omega$

where $a, b, c$ are Fourier components of the Heisenberg-evolved observable, with frequency shifts $\pm h$ and $0$ respectively.

## Physical Intuition / Derivation

### Origin from Open Quantum Systems

A Lindbladian emerges naturally when a closed quantum system (the "system") couples weakly to a large environment (reservoir). By tracing out the environment degrees of freedom and assuming Markovian evolution (memoryless), one derives the Lindblad master equation. This is the quantum extension of classical Fokker-Planck equations.

### Role of Lindblad Operators

The operators $L_k$ represent **dissipative channels**:
- If $L_k = \sqrt{\gamma_k} \sigma^-$ (lowering operator), this models spontaneous emission
- If $L_k = \sqrt{\gamma_k} \sigma^+$, this models spontaneous absorption
- Multiple $L_k$ can represent different dissipative pathways (decay, dephasing, heating, etc.)

The term $L_k \rho L_k^\dagger$ represents "jumps" in the state, while $-\frac{1}{2}\{L_k^\dagger L_k, \rho\}$ enforces trace preservation and ensures probability conservation.

### Detailed Balance and Thermalization

When a Lindbladian satisfies detailed balance with respect to a Gibbs state:

$$\sigma_{\text{Gibbs}} = \frac{e^{-\beta H}}{Z(\beta)}$$

the evolution **thermalizes** the system. The external field in the Hamiltonian can induce entanglement, but the quasi-local structure of the dissipation (nearby sites couple weakly through the environment) allows the Dobrushin condition to apply, guaranteeing rapid mixing.

### Role of External Fields

In the cited work, arbitrary on-site external fields $h \cdot \sigma_Z^{(j)}$ shift the oscillation frequencies of observables in the Heisenberg picture by $\pm h$. The key insight is that the **transition-weight function** $\gamma_j(\omega)$ (Gaussian centered at the appropriate frequency gap) still picks up sufficient overlap with the frequency-shifted Pauli operators, yiel