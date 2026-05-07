# Entropic Stability

## Definition

**Entropic stability** is a quantitative measure of how robustly a denoising process maintains information about a target distribution $\mu$ under perturbation. Formally, a vertex-field denoising process $(Y_t)_{t \in [0,1]}$ is **entropically stable with rate $C$ at time $\theta$** if, for any state $S$ with $\Pr[Y_\theta = S] > 0$ and any probability measure $\nu \ll (1-\theta) * \mu_S$ (absolutely continuous with respect to the conditional distribution), a KL-divergence-weighted inequality holds between the marginal distributions.

Entropic stability formalizes the intuition that the denoising process should not be overly sensitive to small perturbations in the conditional distribution at intermediate times. It quantifies "how much wiggle room" exists in the conditioned distribution before the process fails to reliably recover information about $\mu$.

---

## Key Equations

The fundamental characterization of entropic stability is given by **Lemma 2.18**:

A denoising process $(Y_t)_{t \in [0,1]}$ is entropically stable with rate $C$ at time $\theta$ if and only if for all $S$ with $\Pr[Y_\theta = S] > 0$, and all $\nu \ll (1-\theta) * \mu_S$:

$$\sum_{i \in [n] \setminus S} q_i \log \frac{q_i}{p_i} - (q_i - p_i) \leq C \cdot D_{\mathrm{KL}}\left(\nu \,\Big\|\, (1-\theta) * \mu_S\right)$$

where:
- $p := m((1-\theta) * \mu_S)$ is the mean vector of the base measure
- $q := m(\nu)$ is the mean vector of the perturbed measure
- $D_{\mathrm{KL}}(\cdot \| \cdot)$ is the Kullback-Leibler divergence
- $i \in [n] \setminus S$ indexes coordinates not yet revealed by the denoising process

**Interpretation:** The left-hand side measures a "soft" divergence between $q$ and $p$, combining entropy and mean-shift penalties. Entropic stability bounds this by the actual KL-divergence, with proportionality constant $C$.

---

## Physical Intuition / Derivation

### Denoising and Information Recovery

A denoising process interpolates between a trivial initial state (no information) and the target distribution:
- At $t = 0$: $Y_0 = \emptyset$ (empty information)
- At $t = 1$: $\text{Law}(Y_1) = \mu$ (full target distribution)

At intermediate time $\theta$, the process has revealed partial information encoded in state $Y_\theta = S \subseteq [n]$.

### The Stability Question

Once we condition on $Y_\theta = S$, the "future" distribution is $\mu_\theta := \text{Law}(Y_1 | Y_\theta)$. The question is:

> **How sensitive is the recovery of $\mu$ to small errors in our knowledge of $\mu_\theta$?**

If we have a slightly perturbed conditional $\nu$ instead of $(1-\theta) * \mu_S$, will the final distribution still be close to $\mu$?

### Why the Particular Form?

The left-hand side of the entropic stability inequality has two components:

1. **Entropy penalty** $\sum_i q_i \log(q_i/p_i)$: captures distributional divergence in a way that penalizes both over- and under-estimation
2. **Mean-shift penalty** $-\sum_i(q_i - p_i)$: directly quantifies deviation in expected values

This combination is chosen because:
- It is **weaker than full KL-divergence** (allowing for some tolerance)
- It **scales naturally** with the actual perturbation $D_{\mathrm{KL}}(\nu \| (1-\theta)*\mu_S)$
- It **respects the geometry** of the problem: only coordinates $i \notin S$ (unrevealed variables) matter

---

## Applications in Engineering

### 1. **Rapid Mixing of Markov Chains** (Statistical Physics)

Entropic stability is a core tool for proving polynomial mixing times of Glauber dynamics near critical points:

- **Localization schemes** use denoising to decompose a hard target distribution $\mu$ (e.g., Ising model at criticality) into easier intermediate distributions $\mu_t$
- Entropic stability ensures that the "easy" distributions $\mu_{t^*}$ remain sufficiently close to $\mu$ under the interpolation
- The mixing bound then combines:
$$T_{\mathrm{mix}}(\mu) \lesssim \exp\left(\int_0^{t^*} \min\left(n, \sup_{Y_t} \frac{1}{\delta(\mu_t)}\right) dt\right) \times \text{poly}(n)$$

### 2. **Inference and Approximate Sampling**

- **Posterior approximation**: When sampling from conditional distributions, entropic stability quantifies robustness to approximation errors in intermediate conditionals
- **Sequential inference**: In particle filters or sequential Monte Carlo, entropic stability bounds propagation of conditioning errors

### 3. **Phase Transition Analysis**

- **Criticality bounds**: Determines the threshold at which localization schemes remain effective as system size $n \to \infty$
- **Anti-ferromagnetic Ising models**: Specific localization schemes (stochastic localization, negative-field localization) are proven to satisfy entropic stability at chosen times $t^*$, enabling extension of results from the uniqueness regime to criticality

### 4. **Optimization and Annealing**

- **Simulated annealing robustness**: Entropic stability formalizes how perturbations in the annealing schedule affect convergence
- **Tempering methods**: Validates intermediate temperature schedules