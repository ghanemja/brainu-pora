# Jensen's Formula

## Definition

Jensen's formula is a classical result in complex analysis that relates the magnitude of an analytic function to the distribution of its zeros in the complex plane. In the context of statistical mechanics and computational physics, it provides a rigorous bound on the number and location of zeros of a partition function $Z(\beta)$ in terms of averages of $|Z(\beta)|^2$ (annealed moments).

**Mathematical Statement (Classical):**
For an analytic function $f(z)$ with zeros $z_1, z_2, \ldots, z_n$ inside a disk $|z| < R$:

$$\log|f(0)| = \frac{1}{2\pi} \int_0^{2\pi} \log|f(Re^{i\theta})| \, d\theta - \sum_{k=1}^{n} \log\frac{R}{|z_k|}$$

**Statistical Mechanics Application:**
For a partition function $Z(\beta)$ where $\beta$ is a complex variable:

$$\mathbb{E}[\log|Z(\beta)|] \leq \frac{1}{2\pi}\int_0^{2\pi} \log\mathbb{E}[|Z(\beta e^{i\theta})|^2] \, d\theta$$

This allows control of the *quenched* average (disorder-dependent) via the *annealed* average (disorder-averaged), which is typically much easier to compute.

## Key Equations

**Jensen's Inequality (Log-Convexity Form):**
$$\log\mathbb{E}[|Z(\beta)|^2] \geq \mathbb{E}[\log|Z(\beta)|^2] = 2\mathbb{E}[\log|Z(\beta)|]$$

**Zero-Counting Bound:**
If $Z(\beta)$ has no zeros in a region $\Omega \subset \mathbb{C}$, then for all $\beta \in \Omega$:

$$|Z(\beta)| \geq \exp\left(\mathbb{E}_{\text{disorder}}[\log|Z(\beta)|]\right)$$

This is equivalent to saying:
$$\mathbb{E}[|Z(\beta)|^2] \geq |\mathbb{E}[Z(\beta)]|^2$$

with equality only when $Z(\beta)$ is deterministic (no disorder fluctuations).

## Physical Intuition / Derivation

### Why This Matters

In many-body quantum systems (particularly those with quenched disorder), computing properties requires evaluating the partition function $Z(\beta) = \text{Tr}(e^{-\beta H})$ at complex inverse temperatures. However:

1. **The Sign Problem:** Direct sampling fails when $Z(\beta)$ has large fluctuations or complex values across disorder realizations
2. **Replica Trick Failure:** The standard replica trick requires non-rigorous analytic continuation
3. **Rigorous Alternative:** Jensen's formula provides a *provably rigorous* bound that avoids these issues

### The Key Insight

Jensen's formula exploits the convexity of $\log|f|$ for analytic $f$. The crucial observation is:

- **Annealed average** $\mathbb{E}[|Z(\beta)|^2]$ is typically polynomial to compute (via path integral or Gaussian methods)
- **Quenched average** $\mathbb{E}[\log|Z(\beta)|]$ is what we actually want but appears intractable
- Jensen bridges them: if $Z(\beta)$ stays nonzero in region $\Omega$, the annealed moment controls disorder fluctuations

### Example: SYK Model

For the Sachdev-Ye-Kitaev (SYK) model with $q$-body random interactions:

$$\mathbb{E}[|Z(\beta)|^2] = \int \mathcal{D}J \, e^{-S_{\text{eff}}(J,\beta)}$$

can be evaluated using replica symmetry and saddle-point methods in large-$N$ limit. If this averaged partition function has no zeros in region $|\text{Re}\beta| \lesssim 0.01$, $|\text{Im}\beta| \lesssim 3.4$, then:

$$\mathbb{E}[\log|Z(\beta)|] \text{ is bounded and } Z(\beta) \neq 0 \text{ for most disorder realizations}$$

## Applications in Engineering

### 1. **Quantum Simulation & Gibbs Sampling**
- Enables classical algorithms (Barvinok's method) to estimate thermal properties of quantum systems quasi-polynomially
- Avoids exponential overhead from sign problems in fermionic/frustrated systems
- Relevant for [[Quantum Algorithm Complexity]] bounds

### 2. **Statistical Physics of Disordered Systems**
- Rigorously establishes "zero-free regions" where partition function remains nonsingular
- Critical for understanding phase transitions in spin glasses, SYK models, and Hubbard systems
- Connects to [[Free Energy Calculations]] and [[Replica Symmetry Breaking]]

### 3. **Polynomial-Time Approximation Algorithms**
- Fundamental tool in Barvinok's interpolation method for #P-hard counting problems
- Used to approximate partition functions of bounded-degree systems (Ising models, graph colorings)
- Applies to systems with large entanglement entropy that would classically be intractable

### 4. **Complex Analysis in Control Theory**
- Bounds location of poles/zeros of transfer functions without explicit calculation
- Useful for stability analysis of uncertain systems
- Relevant to [[Nyquist Stability Criterion]] and robust control design

### 5. **Machine Learning (Generative Models)**
- Can bound the log-likelihood (equivalent to partition function) in energy-based models
- Applies to [[Boltzmann Machines]] and related graphical models

## Common Mistakes / Pitfalls

### 1. **Confusing Quenched and Annealed Averages**
❌ *Wrong:* "Jensen's formula directly gives $\mathbb{E}[\log Z]$ from $\log\mathbb{E}[|Z|^2]$"  
✅ *Correct