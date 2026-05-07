# Support Vector Machines

## Definition

Support Vector Machines (SVMs) are supervised learning algorithms for binary classification that find an optimal **linear decision boundary** (hyperplane) separating two classes by maximizing the margin between them. An SVM learns a function $f : \mathbb{R}^n \to \{±1\}$ of the form:

$$f(\mathbf{x}) = \text{sign}(\mathbf{w} \cdot \mathbf{x} - \theta)$$

where $\mathbf{w} \in \mathbb{R}^n$ is the normal vector to the separating hyperplane and $\theta$ is the bias term. The algorithm selects a subset of training points called **support vectors** that lie closest to the decision boundary and are critical for defining it.

**Key insight**: SVMs solve a convex optimization problem, guaranteeing a globally optimal solution (unlike many heuristic approaches).

## Key Equations

### Linearly Separable Case (Hard-Margin SVM)

For a training set $\{(\mathbf{x}_i, y_i)\}_{i=1}^m$ where $y_i \in \{±1\}$, maximize the margin by solving:

$$\min_{\mathbf{w}, \theta} \frac{1}{2}\|\mathbf{w}\|^2$$

subject to the constraints:
$$y_i(\mathbf{w} \cdot \mathbf{x}_i - \theta) \geq 1 \quad \forall i$$

The **margin** (distance between the hyperplane and the nearest points) is $\gamma = \frac{1}{\|\mathbf{w}\|}$. Maximizing margin is equivalent to minimizing $\|\mathbf{w}\|^2$.

### Non-Separable Case (Soft-Margin SVM)

When data cannot be perfectly separated, introduce slack variables $\xi_i \geq 0$:

$$\min_{\mathbf{w}, \theta, \boldsymbol{\xi}} \frac{1}{2}\|\mathbf{w}\|^2 + C\sum_{i=1}^m \xi_i$$

subject to:
$$y_i(\mathbf{w} \cdot \mathbf{x}_i - \theta) \geq 1 - \xi_i \quad \forall i$$

where the **hyperparameter** $C > 0$ controls the trade-off between margin size and misclassification tolerance. Large $C$ penalizes errors heavily; small $C$ allows more violations.

### Kernel Trick (Non-Linear Classification)

For non-linearly separable data, map inputs to a high-dimensional feature space via kernel function $K(\mathbf{x}_i, \mathbf{x}_j) = \phi(\mathbf{x}_i) \cdot \phi(\mathbf{x}_j)$:

$$f(\mathbf{x}) = \text{sign}\left(\sum_{i=1}^m \alpha_i y_i K(\mathbf{x}_i, \mathbf{x}) - \theta\right)$$

where $\alpha_i \geq 0$ are Lagrange multipliers (learned coefficients). Support vectors are points with $\alpha_i > 0$.

**Common kernels**:
- Linear: $K(\mathbf{x}_i, \mathbf{x}_j) = \mathbf{x}_i \cdot \mathbf{x}_j$
- Polynomial: $K(\mathbf{x}_i, \mathbf{x}_j) = (1 + \mathbf{x}_i \cdot \mathbf{x}_j)^d$
- RBF (Radial Basis Function): $K(\mathbf{x}_i, \mathbf{x}_j) = \exp(-\gamma\|\mathbf{x}_i - \mathbf{x}_j\|^2)$

## Physical Intuition / Derivation

### Why Maximize Margin?

SVMs embody the principle of **structural risk minimization**: a larger margin provides better generalization. Intuitively:
- A classifier with a narrow margin relies heavily on precise positioning of training data
- A classifier with a large margin is robust to small perturbations and generalizes better to unseen data
- Margin maximization naturally limits model complexity

### Geometric Interpretation

The optimal separating hyperplane is positioned equidistant from the closest points of each class. These closest points are the **support vectors**—they "support" or define the decision boundary. Remarkably, non-support vectors can be removed without changing the solution, making SVMs interpretable and efficient.

### Convex Optimization Perspective

The SVM objective is a convex optimization problem:
- The constraint set is convex (intersection of half-spaces)
- The objective function $\frac{1}{2}\|\mathbf{w}\|^2$ is convex

This guarantees:
- **Unique global optimum** (no local minima)
- Efficient algorithms exist (quadratic programming solvers)
- Theoretical generalization bounds are available

### Kernel Trick Intuition

Kernels enable SVMs to learn non-linear boundaries by implicitly working in transformed feature spaces $\phi(\mathbf{x})$ *without explicitly computing* the transformation. For example, a polynomial kernel implicitly includes all polynomial combinations of features. The dot product $K(\mathbf{x}_i, \mathbf{x}_j)$ measures similarity in the transformed space while keeping computation efficient.

## Applications in Engineering

### Pattern Recognition & Computer Vision
- **Face recognition**: SVMs classify facial feature vectors extracted from images
- **Handwritten digit recognition**: Map pixel intensities to decision boundaries
- **Defect detection**: Manufacturing quality control by classifying images as defective/non-defective

### Biological & Medical Engineering
- **Disease diagnosis**: Classify patients based on biomarkers and clinical measurements (e.g., cancer detection)
- **Protein function prediction**: Classify protein sequences using string kernels
- **Gene expression analysis**: Separate disease subtypes from microarray data

### Signal Processing & Communications
- **Radar/sonar target classification**: Distinguish enemy vs. friendly targets from signal features
- **Speech emotion recognition