# Linear Convergence

## Definition

**Linear convergence** is a property of iterative optimization algorithms where the error decreases by a constant factor at each iteration. Formally, an algorithm exhibits linear convergence if there exist constants $0 < \rho < 1$ and $\epsilon_0 > 0$ such that:

$$\|e_{k+1}\| \leq \rho \|e_k\|$$

for all iterations $k$ where $\|e_k\| < \epsilon_0$, where $e_k$ is the error at iteration $k$ and $\rho$ is the **linear convergence rate** (or contraction factor).

In the context of stochastic training with noise, linear convergence often occurs **up to a noise-dependent error floor**:

$$\|e_k\| \leq \rho^k \|e_0\| + \mathcal{O}(\sigma^2)$$

where $\sigma^2$ represents the noise level in the stochastic gradient estimator. This means the algorithm exponentially suppresses initial error but eventually saturates at a level determined by irreducible stochasticity.

## Key Equations

**Exponential error decay (deterministic case):**
$$\|e_k\| \leq \rho^k \|e_0\|$$

**Convergence to noise ball (stochastic case):**
$$\mathbb{E}[\|e_k\|] \leq \rho^k \|e_0\| + C\kappa^2$$

where $\kappa^2$ is the mask variance and $C$ is a problem-dependent constant.

**Iteration complexity:**
The number of iterations to achieve error $\epsilon$ scales as:
$$k(\epsilon) = \mathcal{O}\left(\log\frac{\|e_0\|}{\epsilon}\right)$$

**Log-linear error decay:**
$$\log \|e_k\| \leq k \log \rho + \log \|e_0\|$$

This produces a characteristic **linear trajectory when error is plotted on a logarithmic scale**.

## Physical Intuition / Derivation

### Why Linear Convergence Matters

Standard iterative methods (gradient descent, Newton's method) don't always guarantee exponential error reduction. Linear convergence is significant because:

- **Logarithmic iteration count**: To reduce error from $\epsilon_0$ to $\epsilon$, we need roughly $\log(\epsilon_0/\epsilon) / \log(1/\rho)$ iterations—exponentially better than sublinear methods.
- **Predictable training**: Each epoch reduces loss by a consistent multiplicative factor, enabling reliable training schedules.

### Mechanism in Stochastic Training

In overparameterized neural networks trained with biased stochastic gradient estimators (e.g., with Gaussian masking):

1. **Initialization**: Start at some initial error $\|e_0\|$ away from the solution.

2. **Gradient descent step**: Update parameters via
   $$\theta_{k+1} = \theta_k - \eta \nabla \hat{\ell}(\theta_k)$$
   where $\nabla \hat{\ell}$ is a biased but low-variance gradient estimate.

3. **Contraction mapping property**: In a sufficiently smooth loss landscape (guaranteed by overparameterization and the Neural Tangent Kernel regime), the update contracts errors:
   $$\|e_{k+1}\| \approx (1 - \eta \lambda_{\min}) \|e_k\| + \text{noise}$$
   where $\lambda_{\min} > 0$ is the minimum curvature, yielding $\rho = 1 - \eta \lambda_{\min}$.

4. **Noise floor**: Stochastic noise from the masking variance accumulates, preventing convergence below $\mathcal{O}(\kappa^2)$. The algorithm "shakes" around the solution but doesn't penetrate the noise ball.

### Connection to Lyapunov Stability

Linear convergence is analogous to **exponential stability** in dynamical systems: perturbations decay exponentially back to an equilibrium (or a small neighborhood thereof in the stochastic case).

## Applications in Engineering

### Neural Network Training with Differential Privacy
- **Privacy-utility tradeoff**: Gaussian masking (adding noise to activations) provides formal privacy guarantees while maintaining linear convergence. The mask variance $\kappa^2$ directly controls both privacy budget and final error floor.
- **Certified defenses**: Provably defend against membership inference attacks (MIA) by trading some accuracy for privacy, with convergence rates dictating the time-to-solution.

### Federated Learning
- Linear convergence enables prediction of total communication rounds needed when training on decentralized data with noisy gradient estimates.
- Synchronization noise acts like stochastic perturbations; linear convergence theory quantifies allowed heterogeneity.

### Robust Optimization
- When training robust networks (against adversarial perturbations), noise-injected methods exhibit linear convergence to robust solutions with error floors determined by robustness margins.
- Dropout and other stochastic regularizers produce similar linear convergence behavior.

### Adaptive Sampling and Variance Reduction
- Methods like SVRG (Stochastic Variance Reduced Gradient) combine linear convergence rates with reduced noise floors through gradient snapshots.

## Common Mistakes / Pitfalls

### 1. **Confusing Linear Convergence with Convergence to Zero**
Linear convergence does *not* mean loss decreases linearly (like $L(k) = L_0 - ck$). It means error decreases **exponentially** in iteration count.
- **Correct**: $\|e_k\| \sim e^{-ck}$ (exponential)
- **Incorrect**: $\|e_k\| \sim \|e_0\| - ck$ (linear)

### 2. **Ignoring the Noise Floor**
Assuming theoretical linear convergence guarantees reaching machine precision. In practice, stochastic noise creates an irreducible error floor. Training beyond this floor wastes compute.

### 3. **Conflating with Quadratic or Superlinear Convergence**
Newton's method achieves **quadratic convergence** ($\|e