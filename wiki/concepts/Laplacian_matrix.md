# Laplacian Matrix

## Definition

For a graph $G = (V, E, w)$ with $|V| = n$ vertices, edge set $E$, and nonnegative edge weights $w_e$ for $e \in E$, the **Laplacian matrix** $L_G$ (or simply $L$ when context is clear) is defined as:

$$L_G = \sum_{(u,v)=e \in E} w_e (\mathbf{1}_u - \mathbf{1}_v)(\mathbf{1}_u - \mathbf{1}_v)^\top$$

where $\mathbf{1}_u$ and $\mathbf{1}_v$ are indicator vectors with 1 in position $u$ (or $v$) and 0 elsewhere.

**Equivalent form** (for standard presentation): The Laplacian can equivalently be written as:
$$L = D - W$$
where $D$ is the diagonal degree matrix ($D_{ii} = \sum_j w_{ij}$) and $W$ is the weighted adjacency matrix.

The Laplacian is an $n \times n$ symmetric, positive semidefinite matrix with the following properties:
- All rows and columns sum to zero: $L \mathbf{1} = \mathbf{0}$
- It has a zero eigenvalue with eigenvector $\mathbf{1}$
- For connected graphs, the nullspace is exactly $\text{span}(\mathbf{1})$

## Key Equations

**Quadratic form interpretation:**
$$x^\top L x = \sum_{(u,v) \in E} w_{uv}(x_u - x_v)^2$$

This shows $L$ measures weighted smoothness: it penalizes differences across edges.

**Effective resistance** between vertices $u$ and $v$:
$$R_{\text{eff}}(u,v) = (\mathbf{1}_u - \mathbf{1}_v)^\top L_G^+ (\mathbf{1}_u - \mathbf{1}_v)$$

where $L^+$ is the **pseudoinverse** of $L$ (Moore-Penrose inverse).

**Spanning tree probability** (connection to random spanning trees):
$$\Pr[e \in T] = w_e \cdot R_{\text{eff}}(e) = w_e (\mathbf{1}_u - \mathbf{1}_v)^\top L^+ (\mathbf{1}_u - \mathbf{1}_v)$$

where $T$ is a random spanning tree sampled from the distribution weighted by edge weights.

## Physical Intuition / Derivation

### Motivation from Harmonic Analysis

The Laplacian originates from discretizing the continuous Laplacian operator $\nabla^2$. If we think of vertex values $x_i$ as temperatures or potentials on a network, the quadratic form $x^\top L x$ measures total "roughness"—how much values differ across connected edges. Minimizing this encourages smoothness.

### From the Outer Product Form

Each edge $(u,v)$ with weight $w_e$ contributes $w_e(\mathbf{1}_u - \mathbf{1}_v)(\mathbf{1}_u - \mathbf{1}_v)^\top$ to the Laplacian. This encodes:
- The difference vector $(\mathbf{1}_u - \mathbf{1}_v)$ selects components $u$ and $v$
- The outer product creates a rank-1 contribution
- Summing over all edges builds the full matrix

When expanded, this naturally produces:
- Diagonal entries: $L_{ii} = \sum_{j:(i,j) \in E} w_{ij}$ (weighted degree)
- Off-diagonal entries: $L_{ij} = -w_{ij}$ for edges, 0 otherwise

### Connection to Random Spanning Trees

The effective resistance $R_{\text{eff}}(u,v)$ emerges as a fundamental measure of "distance" in the weighted graph that accounts for all parallel paths. The matrix forest theorem connects $L^+$ to spanning tree marginals: an edge is more likely to appear in a random spanning tree if it has low effective resistance (many alternative paths reduce its criticality).

## Applications in Engineering

### 1. **Network Analysis & Electrical Circuits**
- **Resistance distance:** Effective resistance models actual electrical resistance in resistor networks; the Laplacian pseudoinverse directly computes these values
- **Current flow:** In a resistor network, applying voltage $V$ induces current $I = (V_u - V_v)G_{uv}$, and equilibrium is found by solving $Lx = 0$ (relaxed case) or $Lx = f$ (with sources)

### 2. **Graph Clustering & Spectral Methods**
- **Spectral clustering:** The eigenvectors of $L$ (particularly those with small eigenvalues) reveal natural clusters
- **Graph cuts:** The second-smallest eigenvalue (algebraic connectivity) bounds optimal graph partitions
- **Laplacian eigenmaps:** Use low-energy eigenvectors for non-linear dimensionality reduction

### 3. **Distributed Algorithms**
- **Random spanning tree sampling:** The Laplacian enables efficient algorithms for sampling uniform or weighted random spanning trees in distributed settings (e.g., Broadcast Congested Clique model)
- **Spectral sparsification:** Compute sparse approximations $\tilde{L}$ satisfying $(1-\varepsilon)x^\top Lx \le x^\top \tilde{L}x \le (1+\varepsilon)x^\top Lx$ to reduce communication/computation in large networks

### 4. **Dynamical Systems & Control**
- **Consensus algorithms:** The Laplacian governs convergence in multi-agent systems; $\dot{x} = -Lx$ drives all agents to consensus
- **Network robustness:** Spectral gap $\lambda_2(L)$ measures resilience to perturbations

### 5. **Machine Learning & Graph Neural Networks**
- **Graph convolutions:** GNNs use