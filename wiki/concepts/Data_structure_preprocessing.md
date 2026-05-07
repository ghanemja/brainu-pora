# Data Structure Preprocessing

## Definition

**Data structure preprocessing** is the process of organizing and transforming a raw dataset into an indexed, queryable form before runtime to enable efficient subsequent operations. In the context of nearest neighbor search, preprocessing takes a dataset $X = \{x_1, x_2, \ldots, x_n\}$ lying in a metric space $(M, d_M)$ and constructs an auxiliary data structure that supports fast queries answering proximity questions.

Formally, a preprocessing scheme for the **Approximate Near Neighbor (ANN)** problem is defined as:

**Definition (c,r)-ANN:** Given a metric space $(M, d_M)$, approximation factor $c \geq 1$, and radius $r > 0$, preprocess a dataset $X \subseteq M$ such that for any query point $q \in M$ with $d_M(q, X) \leq r$ (where $d_M(q, X) := \min_{x^* \in X} d_M(x^*, q)$), the data structure reports $x \in X$ satisfying:

$$d_M(q, x) \leq c \cdot r$$

For randomized schemes, this holds with probability at least $2/3$.

## Key Equations

### Complexity Tradeoffs

The efficiency of a preprocessing scheme is characterized by three parameters:

$$\text{Total Cost} = \underbrace{\text{Preprocessing Time}}_{\approx \text{Space}} + \underbrace{\text{Space}}_{\text{poly}(n, d)} + \underbrace{\text{Query Time}}_{\text{poly}(d, \log n)}$$

### Distance Constraints in $\ell_p$ Spaces

For $\ell_p$ metrics, the distance between points is:

$$d_p(x, y) = \left(\sum_{i=1}^{d} |x_i - y_i|^p\right)^{1/p}$$

The approximation guarantees depend on the dimensionality $d$ and metric parameter $p$:

| Approximation Factor | Space | Query Time | Reference |
|---|---|---|---|
| $O(\log^{1/p} n \log \log d)$ | $\text{poly}(nd)$ | — | AIK09, And09 |
| $2^{O((\log d)^{2/3}(\log \log d)^{1/3})}$ | $\text{poly}(nd)$ | — | ANN+18b |
| $2^{O(p)}$ | $\text{poly}(nd)$ | — | BG19 |
| $p^{O(1)} + \log \log p$ | $\text{poly}(dn)$ | $\text{poly}(d \log n)$ | KPS25 |

## Physical Intuition / Derivation

### Why Preprocessing is Necessary

Consider a naive approach: given a query $q$, compute distances to all $n$ points and return the nearest. This requires $O(nd)$ query time—prohibitive for large datasets queried repeatedly. Preprocessing trades one-time cost for dramatic query speedup.

### The Reduction Pipeline

The classical **[HIM12]** reduction decomposes approximate NNS into polylogarithmic instances of approximate near neighbor:

1. **Coarse filtering:** Partition the metric space into regions of radius $r, cr, c^2r, \ldots$
2. **Point location:** Use a data structure to identify which region(s) contain the query
3. **Local search:** Exhaustively search the identified region(s)

### Why $\ell_p$ Metrics Matter

$\ell_p$ spaces exhibit fundamentally different geometry:

- **$p = 2$ (Euclidean):** Well-understood; admits geometric techniques (Voronoi diagrams, spatial hashing)
- **$p > 2$:** The "ball" becomes increasingly cube-like, reducing geometric properties; requires combinatorial techniques
- **$p = \infty$ (Chebyshev):** Maximum coordinate; entirely axis-aligned

The challenge for **fast query time** (i.e., $\text{poly}(d \log n)$ rather than exponential in $d$) is that high-dimensional metric spaces suffer from the **curse of dimensionality**—most points are roughly equidistant from any given query in high dimensions, making discrimination difficult.

### Key Insight: Space-Time-Approximation Tradeoff

Fast query structures cannot afford to examine $\Omega(n)$ or even $\Omega(n^{\epsilon})$ points. Instead, they must:

1. **Compress information** through careful indexing (increasing space $\rightarrow$ better query time)
2. **Tolerate approximation** rather than exact nearest neighbors (relaxing accuracy $\rightarrow$ faster queries)
3. **Exploit metric properties** specific to $\ell_p$ geometry

## Applications in Engineering

### 1. Machine Learning & Similarity Search
- **Image retrieval:** Preprocess image embeddings in CNN feature space ($\ell_2$ or $\ell_p$); query with new image
- **Recommendation systems:** Find similar users/items in embedding space; millions of queries per second

### 2. Database Query Optimization
- **Spatial databases:** Nearest neighbor joins on geographic or feature data
- **Approximate string matching:** Map strings to metric space; use NNS for typo correction

### 3. Computer Vision & Graphics
- **Point cloud processing:** Fast k-NN in 3D scans (typically $\ell_2$ or adaptive metrics)
- **Visual search:** Preprocess gallery of descriptors; answer "similar image" queries in milliseconds

### 4. Information Retrieval
- **Vector semantic search:** Index billions of sentence embeddings; retrieve documents semantically similar to query
- **Plagiarism detection:** Compare documents via embedding distance

### 5. Signal Processing & Compression
- **Codebook learning:** Preprocess centroids of VQ (vector quantization); find nearest codeword at decode time
- **Approximate matching in time series:** Detect patterns via nearest neighbor in high-dimensional sliding windows

### 6. Scientific Computing
- **Molecular dynamics:** Find nearby particles in phase space ($\ell_