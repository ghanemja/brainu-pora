# Flow Matching

## Definition

**Flow Matching** is a framework for training generative models by learning to match a target probability distribution through continuous normalizing flows. Rather than explicitly modeling the score function (gradient of log-probability) as in diffusion models, flow matching directly learns a velocity field $\mathbf{v}_t(\mathbf{x})$ that transports samples from a simple prior distribution to the target data distribution over time $t \in [0, 1]$.

The core idea: construct a probability path $p_t(\mathbf{x})$ that interpolates between a simple prior $p_0(\mathbf{x})$ (typically Gaussian) and the target data distribution $p_1(\mathbf{x})$, then train a neural network to predict the vector field that generates this path.

## Key Equations

### Probability Path and Vector Field

For a probability path $p_t(\mathbf{x})$ with associated vector field $\mathbf{u}_t(\mathbf{x})$, the continuity equation relates them:

$$\frac{\partial p_t(\mathbf{x})}{\partial t} + \nabla \cdot (p_t(\mathbf{x}) \mathbf{u}_t(\mathbf{x})) = 0$$

This ensures mass conservation—the probability density evolves consistently with the flow of the vector field.

### Flow Matching Objective

Train a neural network $\mathbf{v}_\theta(t, \mathbf{x})$ to minimize:

$$\mathcal{L}_{\text{FM}} = \mathbb{E}_{t, p_t(\mathbf{x})} \left[ \left\| \mathbf{v}_\theta(t, \mathbf{x}) - \mathbf{u}_t(\mathbf{x}) \right\|^2 \right]$$

where $\mathbf{u}_t(\mathbf{x})$ is the target vector field derived from the probability path.

### Conditional Flow Matching (CFM)

For conditional flows, match conditional vector fields:

$$\mathcal{L}_{\text{CFM}} = \mathbb{E}_{t, \mathbf{x}_0 \sim p_0, \mathbf{x}_1 \sim p_1} \left[ \left\| \mathbf{v}_\theta(t, \mathbf{x}_t) - \mathbf{u}_t(\mathbf{x}_t | \mathbf{x}_0, \mathbf{x}_1) \right\|^2 \right]$$

where the conditional vector field can be computed in closed form for simple paths:

$$\mathbf{u}_t(\mathbf{x}_t | \mathbf{x}_0, \mathbf{x}_1) = \frac{\mathbf{x}_1 - \mathbf{x}_t}{1 - t}$$

for linear interpolation paths of the form $\mathbf{x}_t = (1-t)\mathbf{x}_0 + t\mathbf{x}_1$.

### Sampling via ODE

Once trained, generate samples by integrating the learned ODE:

$$\frac{d\mathbf{x}_t}{dt} = \mathbf{v}_\theta(t, \mathbf{x}_t), \quad \mathbf{x}_0 \sim p_0$$

from $t=0$ to $t=1$ using standard numerical solvers (Euler, RK45, etc.).

## Physical Intuition / Derivation

### Why Flow Matching?

Traditional diffusion models (DDPM, Score-Based) require computing score functions $\nabla \log p_t(\mathbf{x})$, which:
- Are difficult to estimate directly in high dimensions
- Require sophisticated training techniques (noise weighting schedules)
- Lead to coupling between model architecture and noise scheduling

Flow matching decouples these concerns by learning the **generator** of the path directly.

### Geometric Perspective

Imagine a cloud of data points gradually morphing into a cloud of noise:
- **Vector field** $\mathbf{u}_t(\mathbf{x})$ specifies the instantaneous direction each point should move
- **Training** matches the model's learned field $\mathbf{v}_\theta$ to this target field
- **Generation** follows the learned trajectories backward (or forward from noise)

The continuity equation ensures this is well-defined: if you know how the density changes and how the flow moves, you can solve for the velocity.

### Connection to Diffusion Models

Flow matching can be viewed as a **reparameterization** of diffusion models:
- Score function: $\mathbf{s}_t(\mathbf{x}) = \nabla \log p_t(\mathbf{x})$
- Vector field: $\mathbf{u}_t(\mathbf{x}) = -\frac{\sigma'(t)}{2\sigma^2(t)} \mathbf{x} + \sigma(t) \mathbf{s}_t(\mathbf{x})$ (for certain variance schedules)

However, flow matching's direct supervision (CFM) provides cleaner gradients than score-matching objectives.

### Why Conditional Flow Matching Works

The key insight: we can compute the conditional vector field **analytically** for simple interpolations without knowing $p_t(\mathbf{x})$. For straight-line paths:

$$\mathbf{x}_t = (1-t)\mathbf{x}_0 + t\mathbf{x}_1$$

The time-derivative is just:

$$\frac{d\mathbf{x}_t}{dt} = \mathbf{x}_1 - \mathbf{x}_0$$

Since we sample $\mathbf{x}_0$ from data and $\mathbf{x}_1$ from noise (or vice versa), we have direct supervision for the vector field at every point in time—no need to estimate the score.

## Applications in Engineering

### 1. **Generative Modeling for Scientific Data**
- **Molecular design**: Generate novel molecules or proteins by learning flows on molecular conformations
- **Physics simulations**: Learn to