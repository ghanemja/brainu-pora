# Lipschitz mapping

## Definition

A **Lipschitz mapping** (or Lipschitz continuous function) is a function between two metric spaces that bounds how rapidly the function values can change relative to changes in the input.

**Formal Definition:** Let $(X, d_X)$ and $(Y, d_Y)$ be metric spaces. A function $f: X \to Y$ is **Lipschitz continuous** with **Lipschitz constant** $c \geq 0$ if for all $x_1, x_2 \in X$:

$$d_Y(f(x_1), f(x_2)) \leq c \cdot d_X(x_1, x_2)$$

The **Lipschitz constant** is the smallest such $c$, denoted:

$$\text{Lip}(f) = \sup_{x_1 \neq x_2} \frac{d_Y(f(x_1), f(x_2))}{d_X(x_1, x_2)}$$

A function with $c < \infty$ is Lipschitz continuous. When $c < 1$, the function is called a **contraction mapping**.

### In Graph Theory Context

In the source material, a mapping $p: V(\tilde{H}) \to V(G)$ from a wireframe's vertex set to a graph's vertex set is $c$-Lipschitz if distances are scaled by at most the factor $c$ under the mapping.

## Key Equations

**Lipschitz continuity inequality:**
$$d_Y(f(x), f(y)) \leq c \cdot d_X(x, y)$$

**Lipschitz constant (infimum):**
$$\text{Lip}(f) = \inf\{c \geq 0 : d_Y(f(x), f(y)) \leq c \cdot d_X(x, y) \text{ for all } x, y \in X\}$$

**Composition property** (Lipschitz constants multiply):
If $f: X \to Y$ is $c_1$-Lipschitz and $g: Y \to Z$ is $c_2$-Lipschitz, then $g \circ f: X \to Z$ is $c_1 c_2$-Lipschitz.

**Contraction mapping inequality** (when $c < 1$):
$$d_Y(f(x), f(y)) \leq c \cdot d_X(x, y), \quad c < 1$$

## Physical Intuition / Derivation

### Why Lipschitz Continuity Matters

A Lipschitz mapping provides a **controlled bound on how much output can change when input changes slightly**. This is stronger than ordinary continuity (which requires bounds that can depend on location) but weaker than differentiability (which requires local linearity).

**Geometric Interpretation:**
- The Lipschitz condition states that the graph of $f$ lies between two cones of slope $\pm c$.
- For every step of size $\delta$ in the input space, the output can move by at most $c \cdot \delta$.
- This creates a "speed limit" on the function.

### Relationship to Derivatives

If $f: \mathbb{R}^n \to \mathbb{R}^m$ is differentiable with bounded gradient $\|Df(x)\| \leq c$ everywhere, then $f$ is $c$-Lipschitz (by the mean value theorem). Conversely, Lipschitz functions are differentiable almost everywhere (Rademacher's theorem).

### In Graph Geometry (from Source)

The source material uses Lipschitz mappings to preserve geometric structure when transforming graphs:
- A mapping $p: V(\tilde{H}) \to V(G)$ with constant $c$ ensures that distances in the wireframe graph $\tilde{H}$ are distorted by at most factor $c$ relative to the original graph $G$.
- This allows controlled simplification of planar graphs while preserving metric properties.
- **Example from Corollary 5.3:** The identity mapping of vertices remains $3c$-Lipschitz after constructing a simplified plane graph $G'$ from the original graph $G$, meaning shortest path distances scale by at most factor $3c$.

## Applications in Engineering

### 1. **Numerical Analysis & Optimization**
- **Gradient methods:** Functions with bounded Lipschitz gradients have convergence guarantees proportional to the Lipschitz constant.
- **Fixed-point iterations:** Contraction mappings ($c < 1$) guarantee unique fixed points (Banach fixed-point theorem).
- **Approximate solutions:** Bounds on solution error depend directly on Lipschitz constants.

### 2. **Control Theory**
- **Stability analysis:** Lipschitz continuous system dynamics ensure solutions exist and depend continuously on initial conditions.
- **Robustness:** Bounded Lipschitz constants quantify how disturbances propagate through systems.

### 3. **Machine Learning & Deep Networks**
- **Generalization bounds:** Lipschitz constraints on classifiers bound overfitting.
- **Adversarial robustness:** Networks with small Lipschitz constants are more robust to adversarial perturbations.
- **Wasserstein GANs:** Use Lipschitz constraints on discriminators for training stability.

### 4. **Graph Algorithms & Computational Geometry**
- **Graph simplification:** As in the source material, Lipschitz mappings allow coarsening planar graphs while bounding distortion of shortest paths.
- **Mesh generation:** Guarantees that simplified meshes maintain bounded geometric error.
- **Network routing:** Distance-preserving mappings ensure routing tables remain approximately optimal.

### 5. **Signal Processing**
- **Filter design:** Lipschitz continuity of filters ensures smooth response to input variations.
- **Sampling theory:** Bounds on sampling error depend on Lipschitz constants of band-limited signals.

### 6. **Differential Equations**
- **Existence & uniqueness:** Lipschitz continuous right-hand sides guarantee unique solutions (Picard-Lindelöf theorem).
- **Numerical integration:** Error bounds for ODE solvers depend explicitly on Lipschitz constants.

## Common Mistakes /