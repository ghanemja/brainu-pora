# Principal Component Analysis (PCA)

## Definition

Principal Component Analysis (PCA) is an unsupervised dimensionality reduction technique that identifies orthogonal directions of maximum variance in high-dimensional data. It transforms a dataset of potentially correlated variables into a set of linearly uncorrelated variables called **principal components**, ordered by the amount of variance they explain.

Formally, given a data matrix $\mathbf{X} \in \mathbb{R}^{n \times d}$ with $n$ samples and $d$ features, PCA finds a set of orthonormal vectors $\{\mathbf{v}_1, \mathbf{v}_2, \ldots, \mathbf{v}_k\}$ (the principal components) such that projecting the data onto these vectors maximizes the total variance retained while minimizing information loss.

## Key Equations

**Covariance Matrix:**
$$\mathbf{C} = \frac{1}{n}\mathbf{X}^T\mathbf{X}$$

**Eigenvalue Decomposition:**
$$\mathbf{C}\mathbf{v}_i = \lambda_i \mathbf{v}_i$$

where $\lambda_i$ are eigenvalues (ordered: $\lambda_1 \geq \lambda_2 \geq \cdots \geq \lambda_d$) and $\mathbf{v}_i$ are the corresponding orthonormal eigenvectors.

**Variance Explained by Component $i$:**
$$\text{Var}_i = \lambda_i$$

**Cumulative Explained Variance Ratio:**
$$R_k = \frac{\sum_{i=1}^{k}\lambda_i}{\sum_{i=1}^{d}\lambda_i}$$

**Projection onto Principal Subspace:**
$$\mathbf{Y} = \mathbf{X}\mathbf{V}_k$$

where $\mathbf{V}_k = [\mathbf{v}_1, \mathbf{v}_2, \ldots, \mathbf{v}_k] \in \mathbb{R}^{d \times k}$ is the matrix of the first $k$ principal components.

**Reconstruction Error (Frobenius norm):**
$$\|\mathbf{X} - \mathbf{X}\mathbf{V}_k\mathbf{V}_k^T\|_F^2 = \sum_{i=k+1}^{d}\lambda_i$$

## Physical Intuition / Derivation

### Why Variance Matters

Imagine a cloud of points in high-dimensional space. Variance represents how "spread out" the data is along a given direction. Directions with high variance contain more information about the differences between data points, while low-variance directions are near-constant and carry little discriminative information.

### Step-by-Step Intuition

1. **Centering:** First, subtract the mean from each feature so the data is centered at the origin. This ensures we capture intrinsic variance rather than offset.

2. **Covariance Matrix:** The covariance matrix $\mathbf{C}$ captures pairwise relationships between features. Large positive/negative covariances indicate correlated features.

3. **Eigendecomposition:** The eigenvector $\mathbf{v}_1$ corresponding to the largest eigenvalue $\lambda_1$ points in the direction of maximum variance. The magnitude of the eigenvalue equals the variance along that direction.

4. **Greedy Optimization:** Subsequent eigenvectors are orthogonal to previous ones and capture the next-largest variance direction. This greedy approach provably maximizes total retained variance.

### Optimization Perspective

PCA solves:
$$\mathbf{v}_1 = \arg\max_{\|\mathbf{v}\|=1} \mathbf{v}^T\mathbf{C}\mathbf{v}$$

The Rayleigh quotient $\mathbf{v}^T\mathbf{C}\mathbf{v}/\mathbf{v}^T\mathbf{v}$ is maximized by the dominant eigenvector. Successive components solve the same problem in the orthogonal complement of previous solutions.

### Singular Value Decomposition (SVD) Connection

PCA can be computed via SVD of the centered data matrix:
$$\mathbf{X} = \mathbf{U}\mathbf{\Sigma}\mathbf{V}^T$$

where $\mathbf{V}$ columns are the principal components and $\sigma_i^2/n$ are the explained variances. This connection is crucial for numerical stability and streaming algorithms.

## Applications in Engineering

### 1. **Data Preprocessing & Feature Engineering**
- Reduce dimensionality before feeding into downstream models (neural networks, regression)
- Eliminate redundant, correlated features that add computational burden without information gain
- Decorrelate features for algorithms sensitive to multicollinearity (ridge regression, lasso)

### 2. **Image & Signal Processing**
- **Facial Recognition:** Project face images onto eigenfaces (first $k$ PCA components of face database); highly efficient for recognition at reduced dimensionality
- **Image Compression:** Store only the first $k$ principal components; reconstruction requires minimal memory while retaining quality
- **Denoising:** Low-variance components often capture noise; discarding them provides automatic noise suppression

### 3. **Anomaly Detection**
- Model normal data with PCA; large reconstruction error $\|\mathbf{x} - \mathbf{x}'\|$ indicates anomalies
- Efficient for streaming heterogeneous graphs and sensor networks
- Reconstruction-based detection automatically captures deviations from normal variance structure

### 4. **Quality Control & Manufacturing**
- Monitor multivariate sensor readings (temperature, pressure, vibration) in real time
- Detect process faults via PC scores falling outside control limits
- Identify sensor correlations to remove redundant instrumentation

### 5. **Genetics & Bioinformatics**
- Analyze gene expression data (thousands of genes, few samples)
- Identify principal axes of genetic variation across populations
- Visualize high-dimensional genomic data in 2D/3D for exploratory analysis

### 6. **Finance & Economics**
- Principal components in stock returns capture "market factor