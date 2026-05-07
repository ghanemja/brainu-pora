# Dobrushin condition

## Definition

The **Dobrushin condition** is a quantitative criterion for **spatial mixing** in graphical models (particularly Ising models and other spin systems) that ensures the influence of distant variables decays rapidly.

For a graphical model with variables $X_1, \ldots, X_n$ on a graph $G = (V, E)$, the Dobrushin condition asserts that there exists a constant $\alpha < 1$ such that for all vertices $i \in V$ and any two configurations $\sigma, \sigma'$ that differ only at vertex $j \neq i$:

$$\left|\mathbb{P}(X_i = x \mid \text{neighbors of } i, X_j = \sigma_j) - \mathbb{P}(X_i = x \mid \text{neighbors of } i, X_j = \sigma'_j)\right| \leq \alpha$$

This bounds the **maximal influence** that flipping a single spin exerts on the conditional distribution at any other site.

---

## Key Equations

**Dobrushin's sufficient condition for spatial mixing:**

Let $\beta J$ denote the inverse temperature times interaction strength in an Ising model. The Dobrushin condition holds if:

$$\beta J < \ln 2 \quad \text{(for standard ferromagnetic Ising)}$$

More generally, for Ising models on degree-bounded graphs:

$$\alpha = \max_i \sum_{j \sim i} |\beta J_{ij}| < 1$$

where the sum is over neighbors $j$ of vertex $i$.

**Consequence for decay of correlations:**

Under the Dobrushin condition, correlations decay exponentially:

$$|\mathbb{E}[X_i X_j] - \mathbb{E}[X_i]\mathbb{E}[X_j]| \leq C \cdot \alpha^{d(i,j)}$$

where $d(i,j)$ is the graph distance and $C$ is a constant independent of the distance.

---

## Physical Intuition / Derivation

### Why spatial mixing matters

In high-dimensional systems, we want the conditional distribution at one site to be **weakly sensitive** to changes far away. When this holds:

1. **Information cannot propagate far:** Changes at distant sites have exponentially decaying influence
2. **Local properties dominate:** Long-range correlations vanish, enabling local approximations
3. **Uniqueness of Gibbs measure:** The system has a unique equilibrium state (no phase transitions)

### Building the condition

The Dobrushin condition formalizes this via **influence bounds**. Consider site $i$ with neighbors and a distant site $j$:

- The conditional distribution $\mathbb{P}(X_i \mid \text{rest})$ should change negligibly if we alter $X_j$
- Since $j$ is distant from $i$, they are not neighbors—their interaction is **indirect**, mediated through intermediate sites
- By bounding how much each intermediate site can be influenced, we show the cumulative influence decays

For Ising models, this works in the **high-temperature regime** (small $\beta J$), where thermal fluctuations destroy long-range order.

---

## Applications in Engineering

### 1. **Statistical Learning Theory**
- **Polynomial approximation of halfspaces:** Under the Dobrushin condition, halfspaces defined by Ising models have low $L^1$-approximation degree $O(\log^2(1/\varepsilon)/\varepsilon^2)$ (vs. $O(\log(1/\varepsilon)/\varepsilon^2)$ in uniform case)
- **Agnostic learning:** Enables efficient learning of approximately-correct classifiers

### 2. **Graphical Model Inference**
- **Message-passing algorithms (BP, TRW):** Dobrushin condition implies convergence of belief propagation and guarantees good approximations to marginals
- **Partition function estimation:** Under spatial mixing, the log-partition function can be approximated via local partition functions

### 3. **Sampling & Counting**
- **MCMC mixing:** The condition guarantees rapid mixing of Markov chain Monte Carlo samplers
- **#P-hardness avoidance:** Problems tractable under spatial mixing become intractable without it

### 4. **Hardware Design & Thermal Systems**
- **Circuit behavior:** Spatial mixing in physical systems ensures local perturbations don't cascade globally (fault tolerance)
- **Temperature stability:** In materials, Dobrushin-like conditions prevent runaway thermal feedback

### 5. **Inverse Sampling for Transfer**
- **Sampler-inverter pairs:** Enables transference from uniform distribution learning to graphical model learning (as shown in Table 2)

---

## Common Mistakes / Pitfalls

### 1. **Confusing Dobrushin with other mixing conditions**
- **Dobrushin** bounds single-variable influence; **mixing time** measures convergence of MCMC
- One does not imply the other without additional structure

### 2. **Assuming Dobrushin for all Ising models**
- Holds only in high-temperature regime ($\beta J < \ln 2$)
- Fails near phase transitions where correlations become long-range
- **Pitfall:** Using it without checking temperature!

### 3. **Over-interpreting "spatial mixing"**
- Spatial mixing ≠ independence
- Variables remain correlated; the condition only bounds how **conditional** distributions change with distant variables
- Does not imply clustering or marginal concentration

### 4. **Forgetting bounded-degree requirement**
- For meaningful constants, degrees must be bounded (typically $d_{\max} = O(1)$)
- On unbounded-degree graphs, the condition may hold but give loose constants

### 5. **Ignoring the distinction: uniform vs. graphical model**
- Learning bounds under Dobrushin are **polynomial in the bound's parameters**, but can be worse than uniform due to constants
- Table 2 shows: $O(\log^2(1/\varepsilon)/\varepsilon^2)$ for Dobrushin vs. $O(\log(1/\varepsilon)/\varepsilon^2)$ uniform—quadratic in log-factor

---

## See Also

- [[Spatial Mixing