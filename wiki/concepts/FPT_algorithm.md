# FPT Algorithm

## Definition

An **FPT algorithm** (Fixed-Parameter Tractable algorithm) is an algorithm that solves a computational problem in time $f(k) \cdot n^{O(1)}$, where:
- $k$ is a **parameter** (typically a structural property of the input smaller than the input size $n$)
- $f(k)$ is a computable function depending only on $k$
- $n^{O(1)}$ is a polynomial factor in the input size $n$

The key insight is that computational hardness is "confined" to the parameter $k$ rather than spread across the entire input. This makes FPT algorithms practical when $k$ is small, even if the general problem is NP-hard.

### Formal Context (from source)

In the d-EDMC (Euclidean Distance Matrix Completion) problem, Corollary 6 establishes:

$$\text{Runtime} = 2^{(d+1)O(t^2)} + n^{O(1)}$$

where:
- $d$ = dimension parameter for the embedding space
- $t$ = "block pattern" parameter (related to graph structure)
- $n$ = matrix size

---

## Key Equations

**General FPT runtime bound:**
$$T(n, k) = f(k) \cdot \text{poly}(n)$$

**For d-EDMC with t-block pattern exclusion (Corollary 6):**
$$T(n, d, t) = 2^{(d+1)O(t^2)} + n^{O(1)}$$

**For bounded unspecified entries per row (Corollary 9):**
$$n' \leq (d+1)(\Delta + 1)^2$$

where $\Delta$ is the maximum number of unspecified entries per row, achievable via kernel preprocessing.

---

## Physical Intuition / Derivation

### Why Structure Matters More Than Size

Many NP-hard problems become tractable when restricted to structured inputs. The insight is that **not all instances are equally hard**—those with special structure can be solved efficiently.

### Building Intuition Through the Matrix Example

1. **Unstructured case (intractable):** A partial matrix where you can specify any subset of entries gives no exploitable structure. Even with relaxed constraints, NP-hardness persists (Theorem 1).

2. **Structured case (tractable via FPT):** Impose the constraint that the complement graph of the underlying matrix structure excludes $K_{t,t}$ (complete bipartite graph with $t$ vertices on each side). This encodes locality:
   - Planar graphs: $K_{3,3}$-free (Kuratowski's theorem)
   - Bounded-degree graphs: $K_{(\Delta+1),(\Delta+1)}$-free
   - Minor-free graphs: $K_{t,t}$-free for parameter-dependent $t$

3. **How it changes complexity:** The $K_{t,t}$-freeness constraint limits how "dense" local neighborhoods can be. This enables:
   - **Kernelization:** Reduce instance $(M, d) \to (M', d)$ where $|M'|$ depends only on parameters, not original size
   - **Bounded search tree:** Enumerate solutions using a tree of depth $f(k)$ with branching factor controlled by the parameter

### The Kernel Compression (Theorem 4 & 8)

Kernel preprocessing produces an equivalent smaller instance:
$$n' \leq (d+1)(\Delta + 1)^2$$

This is **parameter-dependent but input-size independent**. Once compressed, polynomial-time algorithms apply to a tiny submatrix.

---

## Applications in Engineering

### 1. **Sensor Network Localization**
- **Problem:** Determine positions of sensors given partial pairwise distances (d-EDMC)
- **Parameter:** Dimension $d$ (typically 2–3) is small; network structure naturally exhibits low-degree or planar topology
- **Benefit:** FPT guarantees efficient localization even for incomplete measurements when network has bounded local complexity

### 2. **Computational Geometry & CAD**
- **Problem:** Reconstruct point clouds or mechanical assemblies from partial distance constraints
- **Parameter:** Embedding dimension $d$ (physical space is low-dimensional)
- **Benefit:** Practical algorithms for rigid-body configuration problems where classical approaches fail

### 3. **Machine Learning: Distance-Based Clustering**
- **Problem:** Complete a similarity/distance matrix for high-dimensional clustering
- **Parameter:** Intrinsic dimension or manifold structure (often much smaller than ambient dimension)
- **Benefit:** Scale to large datasets by exploiting low-dimensional geometry rather than ambient dimensionality

### 4. **Network Design & Optimization**
- **Problem:** Verify feasibility of network specifications with partial constraints
- **Parameter:** Degeneracy or bandwidth constraints on the underlying graph
- **Benefit:** FPT results guarantee decidability in polynomial time for graphs with bounded degeneracy (e.g., planar networks)

### 5. **Structural Biology (Protein Folding)**
- **Problem:** Determine 3D protein structure from incomplete NMR distance measurements
- **Parameter:** Embedding dimension $d = 3$, plus sparsity structure
- **Benefit:** FPT bounds justify heuristic algorithms used in structure refinement pipelines

---

## Common Mistakes / Pitfalls

### 1. **Confusing FPT with "Just Exponential in $n$"**
❌ *Wrong:* "My algorithm runs in $2^n$, so it's FPT."  
✓ *Right:* FPT requires the exponential term $f(k)$ to depend **only on parameter** $k$, not $n$. An algorithm running in $2^n$ is exponential, not FPT (unless $n$ is bounded by $k$).

### 2. **Ignoring Parameter Dependence**
❌ *Wrong:* "FPT algorithms are always practical."  
✓ *Right:* An FPT algorithm with $f(k) = 2^{2^k}$ is theoretically tractable but practically useless for moderate $k$. Check the $f(k)$ dependence