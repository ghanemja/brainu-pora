# Low-Rank Approximation

## Definition

**Low-rank approximation** is a dimensionality reduction technique that represents high-dimensional data using a lower-dimensional subspace while preserving the most significant information. Formally, given a data matrix $\mathbf{A} \in \mathbb{R}^{m \times n}$ of rank $r$, a rank-$k$ approximation (where $k < r$) seeks to find a matrix $\mathbf{B}$ of rank at most $k$ that minimizes reconstruction error:

$$\min_{\text{rank}(\mathbf{B}) \leq k} \|\mathbf{A} - \mathbf{B}\|_F$$

where $\|\cdot\|_F$ denotes the Frobenius norm.

In the context of **feature engineering**, low-rank approximation identifies a low-dimensional feature subspace on which downstream machine learning models are trained. The approximation factors (e.g., principal components or basis vectors) define which features or feature combinations are used.

### Consistency and Recourse Extension

**Consistent low-rank approximation** extends the basic definition to account for temporal stability in online/streaming settings. When data evolves, the approximation should:
- Maintain high reconstruction quality
- Minimize **recourse**: the cumulative number of changes to selected features or the feature subspace across time steps
- Produce stable representations that do not fluctuate unpredictably with minor data perturbations

## Key Equations

### Standard Frobenius Norm Objective

$$\mathbf{B}^* = \arg\min_{\text{rank}(\mathbf{B}) \leq k} \|\mathbf{A} - \mathbf{B}\|_F^2 = \sum_{i=1}^m \sum_{j=1}^n (A_{ij} - B_{ij})^2$$

### SVD Solution (Eckart-Young Theorem)

For the optimal rank-$k$ approximation, the singular value decomposition provides:

$$\mathbf{A} = \mathbf{U}\boldsymbol{\Sigma}\mathbf{V}^\top$$

The best rank-$k$ approximation is:

$$\mathbf{B}^* = \mathbf{U}_k\boldsymbol{\Sigma}_k\mathbf{V}_k^\top$$

where $\mathbf{U}_k$, $\boldsymbol{\Sigma}_k$, $\mathbf{V}_k$ retain only the top $k$ singular values and corresponding vectors. The approximation error is:

$$\|\mathbf{A} - \mathbf{B}^*\|_F = \sqrt{\sum_{i=k+1}^r \sigma_i^2}$$

### Consistent Low-Rank Approximation (Online Setting)

Given a sequence of data matrices $\mathbf{A}^{(t)}$ arriving over time $t = 1, 2, \ldots, T$, minimize:

$$\min_{\{\mathbf{B}^{(t)}\}} \sum_{t=1}^T \left(\|\mathbf{A}^{(t)} - \mathbf{B}^{(t)}\|_F^2 + \lambda \cdot d(\mathbf{B}^{(t)}, \mathbf{B}^{(t-1)})\right)$$

where $d(\cdot,\cdot)$ is a distance metric penalizing feature subspace changes, and $\lambda$ balances approximation quality against stability.

## Physical Intuition / Derivation

### Why Low-Rank Works

Real-world data often lies approximately on a lower-dimensional manifold despite being represented in high dimensions. For example:
- Images of faces cluster in a subspace of pixel space
- Text documents can be represented by a handful of latent topics
- Time-series signals contain dominant frequencies

The SVD decomposes data into orthogonal directions ordered by explained variance. The top $k$ singular vectors capture the directions along which data varies most; discarding directions with small singular values removes noise and redundancy.

### Downstream Cascading Effects

When low-rank approximation selects features for downstream models:
- **High recourse** = features change frequently → models must retrain constantly → operational cost and latency penalties
- **Low recourse** = stable features → fewer retrainings → maintained service quality and reliability

In dynamic settings, even small data updates can rotate the principal component space significantly if the data distribution is poorly conditioned. Consistent formulations explicitly penalize such rotations.

### Connection to Stability

From a numerical perspective, ill-conditioned data (gap between $\sigma_k$ and $\sigma_{k+1}$ is small) makes the rank-$k$ subspace sensitive to perturbations. Stability can be improved by either:
1. Smoothing the data evolution (temporal regularization)
2. Selecting rank-$k$ approximations that are robust to small perturbations
3. Allowing controlled, gradual changes to the feature subspace rather than abrupt switches

## Applications in Engineering

### Feature Engineering & Machine Learning
- **Dimensionality reduction** for training models on high-dimensional inputs (images, text, genomics)
- Reduces training time and memory consumption
- Reduces overfitting through regularization effect
- In **consistent settings**: maintains stable feature sets across model retraining cycles, reducing engineering overhead

### Biometrics & Security
- Fingerprint and iris recognition: low-dimensional representations must be stable across captures to enable reliable identification
- High recourse would cause legitimate users to be rejected if their biometric representation drifts

### Image & Signal Processing
- **Compression**: represent images/signals with fewer basis elements (e.g., JPEG uses DCT, a form of low-rank approximation)
- **Denoising**: reconstruct clean signals by projecting onto low-rank subspace
- **Object detection, handwriting recognition, facial recognition**: derived features should not fluctuate unpredictably as new training data arrives

### Text Mining & Information Retrieval
- **Latent Semantic Analysis (LSA)**: low-rank approximation of term-document matrices to discover hidden topics
- **Word embeddings**: dense low-dimensional representations of words
- Must maintain coherence in embeddings over time to preserve search quality and classification