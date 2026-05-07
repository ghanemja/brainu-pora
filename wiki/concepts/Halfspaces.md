# Halfspaces

## Definition

A **halfspace** in $\mathbb{R}^d$ is a subset of Euclidean space defined by a linear inequality. Formally, a halfspace is the set of all points satisfying:

$$H = \{\mathbf{x} \in \mathbb{R}^d : \mathbf{w} \cdot \mathbf{x} + b \leq 0\}$$

where $\mathbf{w} \in \mathbb{R}^d$ is a weight vector, $b \in \mathbb{R}$ is a bias term, and $\mathbf{w} \cdot \mathbf{x}$ denotes the dot product.

The boundary of a halfspace is a *hyperplane*, the $(d-1)$-dimensional surface where $\mathbf{w} \cdot \mathbf{x} + b = 0$. The halfspace itself is one of the two regions created by this hyperplane.

**In machine learning context:** A halfspace classifier is a Boolean function that computes:
$$f(\mathbf{x}) = \text{sign}(\mathbf{w} \cdot \mathbf{x} + b)$$

This is the fundamental basis of **linear classifiers** including perceptrons, support vector machines (SVMs), and logistic regression.

## Key Equations

**Halfspace definition (inequality form):**
$$H = \{\mathbf{x} : \mathbf{w}^T \mathbf{x} + b \leq 0\}$$

**Decision boundary:**
$$\mathbf{w}^T \mathbf{x} + b = 0$$

**Sign function (classifier output):**
$$f(\mathbf{x}) = \begin{cases} +1 & \text{if } \mathbf{w}^T \mathbf{x} + b > 0 \\ -1 & \text{if } \mathbf{w}^T \mathbf{x} + b < 0 \end{cases}$$

**Distance from point to hyperplane:**
$$d(\mathbf{x}, H) = \frac{|\mathbf{w}^T \mathbf{x} + b|}{\|\mathbf{w}\|}$$

where $\|\mathbf{w}\| = \sqrt{\sum_{i=1}^d w_i^2}$ is the Euclidean norm.

**Margin (in linear classification):**
$$\text{margin} = \min_i \frac{|\mathbf{w}^T \mathbf{x}_i + b|}{\|\mathbf{w}\|}$$

The margin represents the distance from the separating hyperplane to the nearest data point.

## Physical Intuition / Derivation

### Geometric Interpretation

A halfspace divides $\mathbb{R}^d$ into two regions:
- **Positive halfspace:** $\mathbf{w}^T \mathbf{x} + b > 0$ (one side of the hyperplane)
- **Negative halfspace:** $\mathbf{w}^T \mathbf{x} + b < 0$ (the other side)

The normal vector $\mathbf{w}$ points perpendicular to the hyperplane boundary. Any point exactly on the hyperplane satisfies $\mathbf{w}^T \mathbf{x} + b = 0$.

### Why Halfspaces Matter

1. **Simplicity:** Linear decision boundaries are among the simplest classifiers to compute and understand.

2. **Expressiveness Trade-off:** While a single halfspace can only separate linearly separable data, compositions of halfspaces (e.g., via neural networks) can approximate complex nonlinear boundaries.

3. **Learning Theory Connection:** Understanding halfspace learning is central to computational learning theory. Key results include:
   - The VC dimension of halfspaces in $\mathbb{R}^d$ is exactly $d+1$
   - This implies generalization bounds for learning halfspaces from samples

4. **Noise Robustness:** Research shows that halfspace classifiers have special properties regarding their robustness to noise and bounded independence (as referenced in the source material).

### Derivation from Optimization Perspective

Learning a halfspace typically involves solving:

$$\min_{\mathbf{w}, b} \sum_{i=1}^n \ell(y_i(\mathbf{w}^T \mathbf{x}_i + b)) + \lambda \|\mathbf{w}\|^2$$

where:
- $\ell$ is a loss function (hinge loss for SVMs, logistic loss for logistic regression)
- $y_i \in \{-1, +1\}$ are binary labels
- $\lambda$ is a regularization parameter

The optimal $\mathbf{w}$ and $b$ define a halfspace that minimizes classification error while controlling model complexity.

## Applications in Engineering

### 1. Machine Learning & Computer Vision
- **Object Detection:** Bounding boxes in image recognition are axis-aligned halfspaces
- **Image Classification:** Initial layers of neural networks learn halfspace boundaries
- **Support Vector Machines (SVMs):** Direct application to binary classification in high-dimensional spaces

### 2. Control Systems
- **State Space Partitioning:** Halfspaces divide control state spaces for switching logic
- **Safety Constraints:** Linear constraints in optimal control (e.g., trajectory planning) define feasible regions as intersections of halfspaces
- **Reachability Analysis:** Forward reachable sets in hybrid systems often characterized by linear inequalities

### 3. Operations Research & Optimization
- **Linear Programming:** Feasible regions are defined as intersections of halfspaces
- **Resource Allocation:** Constraints represent resource limits (halfspaces in capacity space)
- **Polytope Representation:** Any polytope is the intersection of finitely many halfspaces

### 4. Robotics
- **Path Planning:** Obstacles and joint limits define halfspace constraints
- **Collision Avoidance:** Linear separating hyperplanes between robot configuration and obstacle configurations
- **Workspace Analysis:** Reachable workspace characterized by linear constraints

### 5. Signal Processing
- **Classification:** Threshold-based decision rules