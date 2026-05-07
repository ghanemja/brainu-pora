# DDPM (Denoising Diffusion Probabilistic Models)

## Definition

**Denoising Diffusion Probabilistic Models (DDPMs)** are a class of generative models that learn to sample from a target distribution $\pi$ by iteratively denoising Gaussian-corrupted samples. The core idea is to reverse a forward diffusion process that gradually adds noise to data until it becomes unrecognizable, learning the reverse trajectory to recover clean samples.

Formally, DDPMs operate on the principle of score matching: training a neural network $\hat{s}_\sigma(\mathbf{x})$ to estimate the score function (gradient of log-density) $s_{\pi,\sigma}(\mathbf{x}) = \nabla_\mathbf{x} \log \pi_\sigma(\mathbf{x})$ at various noise levels $\sigma$, where $\pi_\sigma$ is the smoothed target distribution obtained by convolving $\pi$ with a Gaussian kernel of standard deviation $\sigma$.

## Key Equations

### Score Matching Training Objective
The standard training objective for DDPMs is:
$$\mathcal{L}(\hat{s}_\sigma) = \mathbb{E}_{\mathbf{x} \sim \pi_\sigma} \left[ \|\hat{s}_\sigma(\mathbf{x}) - s_{\pi,\sigma}(\mathbf{x})\|_2^2 \right]$$

This matches the $L^p$-accurate score assumption (with $p=2$) commonly used in theoretical analysis.

### Reverse Process (Sampling)
For a discrete sequence of noise levels $\sigma_1 > \sigma_2 > \cdots > \sigma_T \approx 0$, DDPM sampling proceeds iteratively:
$$\mathbf{x}_{t-1} = \mathbf{x}_t + (\sigma_t^2 - \sigma_{t-1}^2) \hat{s}_{\sigma_t}(\mathbf{x}_t) + \sqrt{\sigma_t^2 - \sigma_{t-1}^2} \cdot \mathbf{z}_t$$

where $\mathbf{z}_t \sim \mathcal{N}(0, \mathbf{I})$ is Gaussian noise. Starting from $\mathbf{x}_T \sim \mathcal{N}(0, \sigma_T^2 \mathbf{I})$, iterative application yields samples approaching $\pi$.

### Query Complexity Lower Bound
The fundamental lower bound for diffusion sampling (in worst case):
$$\text{Queries}_{\text{required}} = \Omega\left(\sqrt{d}\right)$$

where $d$ is the data dimension. This holds even when allowing TV (Total Variation) error as large as 0.99.

### Upper Bound with Lipschitz Regularity
When score estimates are $L$-Lipschitz, the required number of score queries reduces to:
$$\text{Queries} = O\left(L\sqrt{d}\right)$$

More generally, algorithms exploiting Lipschitz structure achieve:
$$\min\left(d, L^{1/3}d^{2/3}, Ld^{1/3}\right) \text{ queries}$$

## Physical Intuition / Derivation

### Forward Diffusion (Intuition)
Imagine a photograph of an object gradually becoming corrupted by static noise. At each timestep, the signal degrades but the structure becomes increasingly obscured. The forward process models this degradation mathematically through repeated convolution with Gaussians of increasing width.

### Why Score Functions?
The score $s_{\pi,\sigma}(\mathbf{x}) = \nabla_\mathbf{x} \log \pi_\sigma(\mathbf{x})$ points in the direction of highest density increase. In the noisy distribution, it indicates which direction to move to become more "data-like." This is a natural direction for the generative model to follow.

### Why Gaussian Smoothing?
Gaussian smoothing (Assumption 1) serves three purposes:
1. **Regularity**: Ensures infinite differentiability, making theoretical analysis tractable
2. **Practical alignment**: Mirrors distributions naturally sampled by early-stopped diffusion models
3. **Convergence guarantees**: Enables Total Variation (TV) convergence analysis rather than weaker divergences

### Complexity Intuition
The lower bound $\Omega(\sqrt{d})$ emerges because:
- The model must navigate a $d$-dimensional space from noise to data
- Each score query provides local directional information but limited global structure
- Curse of dimensionality: volume grows exponentially, requiring $\sqrt{d}$ times more "steps" to cover representative regions

The Lipschitz assumption breaks this: if the score field is smooth ($L$-Lipschitz), fewer local queries are needed because neighboring points have predictable scores.

## Applications in Engineering

### 1. **Image Generation & Restoration**
- **Inpainting**: Recovering missing regions in images by conditioning on known pixels
- **Super-resolution**: Generating high-resolution details consistent with low-res input
- **Medical imaging**: Artifact removal and image enhancement for CT/MRI scans

### 2. **3D Model Synthesis**
- Point cloud generation for CAD and robotics applications
- Mesh and voxel-based 3D shape generation
- Molecular structure prediction in computational chemistry

### 3. **Time Series & Control**
- Trajectory optimization in robotics (diffusion-based motion planning)
- Anomaly detection by modeling expected temporal patterns
- Synthetic sensor data generation for training robust systems

### 4. **Protein Structure Prediction**
- AlphaFold improvements: diffusion-based refinement of predicted structures
- De novo protein design generating novel functional sequences

### 5. **Hardware Design & Simulation**
- Generative design of circuit layouts and chip floorplans
- Physics-informed diffusion for simulation-based optimization

## Common Mistakes / Pitfalls

### 1. **Confusing Score with Density Gradient**
**Error**: Treating $\hat{s}_\sigma(\mathbf{x})$ as directly proportional to likelihood.
**Correction**: The score is $\nab