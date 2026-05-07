# Skyscraper Invariant

## Definition

The **Skyscraper Invariant** is a refined, stability-aware filtration of the classical rank invariant for multiparameter persistence modules. For a $d$-parameter persistence module $V$ and a threshold parameter $\theta \in \mathbb{R}$, the Skyscraper invariant assigns to each pair of indices $\alpha \leq \beta \in \mathbb{R}^d$ a value:

$$s_\theta^V(\alpha, \beta) = \text{rank of the persistence map } V_\alpha \to V_\beta$$

computed after **filtering to elements that persist over parameter regions with volume at most $1/\theta$**.

Formally, this filtration is induced by the **Harder-Narasimhan (HN) filtration** of the module under a central charge concentrated at a single parameter value. The skyscraper invariant thus parameterizes a family of rank invariants indexed by stability thresholds, creating a richer descriptor than the unfiltered rank invariant alone.

### Relationship to Rank Invariant

The classical **rank invariant** $\text{rk}_V(\alpha, \beta)$ counts the total rank of the persistence map from $\alpha$ to $\beta$ without discrimination. The Skyscraper invariant refines this by:
- Stratifying the rank by persistence "lifetime" 
- Retaining only features stable at scale $\theta$
- Creating a filtration that is strictly stronger (more informative) than rank alone

## Key Equations

**Skyscraper Invariant Definition:**
$$s_\theta^V(\alpha, \beta) = \dim \text{Im}\left(V_\alpha \xrightarrow{f_{\alpha,\beta}} V_\beta\right) \bigg|_{\text{HN-filtered at } \theta}$$

where the HN filtration selects components whose support region has measure $\leq 1/\theta$.

**Filtering Condition:**
For a component $C$ of $V$, inclusion in the HN filtration at scale $\theta$ requires:
$$\text{vol}(\text{supp}(C)) \leq \frac{1}{\theta}$$

**Wall-and-Chamber Decomposition:**
The set of central charges is partitioned into regions (chambers) within which the HN filtration remains constant. Chamber boundaries (walls) are determined by the lower envelope of $d-1$ degree polynomials:

$$\text{Wall}(V) = \text{LowerEnvelope}(\{P_i(z) : i \in I\})$$

where $\deg(P_i) = d-1$ and $|I|$ is the number of distinct module substructures.

## Physical Intuition / Derivation

### Why the Skyscraper Invariant?

Think of a multifiltered dataset as a "landscape" where different regions light up at different parameter combinations. The rank invariant counts all features connecting two heights, but doesn't distinguish between:
- A feature that persists across a wide region (robust, important)
- A feature that persists only in a tiny corner (fragile, noise-like)

The Skyscraper invariant corrects this by asking: **"If I only trust features that persist over relatively compact regions, how many connections do I see?"** As $\theta$ increases, you become more permissive, recovering more rank; as $\theta \to \infty$, you approach the full rank invariant.

### HN Filtration Connection

The Harder-Narasimhan filtration is a classical tool from algebraic geometry (stability of vector bundles). Here it's repurposed: by choosing a central charge supported at coordinate $\alpha$, we create a notion of "stability at point $\alpha$." The HN filtration sorts module components by their stability, naturally creating a filtration by persistence scale.

### Computational Path

1. **Input:** Multiparameter module $V$ (given as quiver representation)
2. **For each scale $\theta$:** Compute HN filtration under central charges at critical parameter values
3. **Extract:** Ranks of persistence maps restricted to stable components
4. **Output:** Family of refined rank invariants, one per scale

## Applications in Engineering

### 1. **Biomedical Data Analysis**
The paper demonstrates computing a filtered Multiparameter Landscape on biomedical datasets. The Skyscraper invariant helps:
- Distinguish robust topological features from noise-driven artifacts
- Quantify feature stability across biological conditions
- Feed interpretable features into ML pipelines for classification/clustering

### 2. **Material Science & 3D Imaging**
Multiparameter filtrations (e.g., scale and intensity threshold) produce persistence modules where Skyscraper invariants:
- Characterize pore networks robust to noise in computed tomography scans
- Filter out spurious topological features from segmentation artifacts
- Enable stability metrics for structure quality

### 3. **Sensor Networks & Signal Processing**
Multiparameter data (time × frequency × spatial location) benefit from:
- Detecting persistent events vs. transient noise
- Separating stable signal components by their coherence lifetime
- Machine-learning-friendly feature vectors via invariant vectorization

### 4. **Time-Series & Anomaly Detection**
Sliding-window persistence modules can use Skyscraper invariants to:
- Identify anomalies with stability guarantees
- Track changes in topological signature across regimes
- Replace raw persistence barcodes with erosion-stable summaries

## Common Mistakes / Pitfalls

### 1. **Confusing with Standard Rank Invariant**
❌ **Mistake:** Treating Skyscraper invariant and rank invariant as equivalent.  
✓ **Correct:** Skyscraper invariant is a *filtration* (family) of refined rank invariants; it is strictly stronger and more informative.

### 2. **Misinterpreting the Scale Parameter $\theta$**
❌ **Mistake:** Thinking $\theta$ is an arbitrary threshold to tune.  
✓ **Correct:** $\theta$ has geometric meaning—it bounds the *volume* of the region over which a feature persists. Higher $\theta$ = more lenient (larger region allowed).

### 3. **Assuming Direct Computation Scalability**