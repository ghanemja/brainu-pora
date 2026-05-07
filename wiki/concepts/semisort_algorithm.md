# semisort algorithm

## Definition

**Semisort** is a parallel algorithmic primitive that permutes an array of $n$ records such that all records with equal keys are contiguous, without requiring full global sorting. The problem sits between unordered shuffling and complete sorting, making it useful as a preprocessing step in divide-and-conquer parallel algorithms.

**Formal Statement:** Given an array $A$ of $n$ records with keys from an arbitrary universe $U$, rearrange $A$ so that for any two records with keys $k_1$ and $k_2$ where $k_1 \neq k_2$, if record $i$ has key $k_1$ and record $j$ has key $k_2$, then all records with key $k_1$ appear before all records with key $k_2$, or vice versa—provided no ordering constraint is imposed between different keys.

More precisely: records are partitioned into contiguous blocks by key, though the relative order of these blocks is arbitrary.

---

## Key Equations

The semisort algorithm achieves:

$$\text{Work} = O(n) \text{ whp (with high probability)}$$

$$\text{Depth} = O(\log^2 n) \text{ whp}$$

**Allocation function** for destination arrays:
$$\text{size}(D_x) = \alpha \cdot f(\sigma_x)$$

where:
- $\sigma_x$ = sampled count of records with key $x$
- $\alpha \geq 2$ = slack factor (overcounting buffer)
- $f(\cdot)$ = allocation function (typically $f(m) = \Theta(m \log n)$ for light buckets)

**Sampling rate:**
$$p_s = \Theta\left(\frac{1}{\log n}\right)$$

**Heavy key threshold:**
$$\tau = \Theta(\log n)$$

**Number of light buckets:**
$$B = \Theta\left(\frac{n}{\log^2 n}\right)$$

---

## Physical Intuition / Derivation

### Why Semisort Matters

Full sorting requires $\Omega(n \log n)$ work sequentially. Many divide-and-conquer algorithms only need records grouped by key, not globally ordered. Semisort exploits this to avoid the $\log n$ factor for comparison-based sorting.

### Three-Phase Algorithm (GSSB Framework)

**Phase 1: Sampling & Bucketing**

The algorithm takes a random sample of $p_s \cdot n = \Theta(n/\log n)$ records. By sampling, we estimate the frequency of each key using order statistics:
- A key $x$ is **heavy** if it appears $\geq \tau = \Theta(\log n)$ times
- A key $x$ is **light** otherwise

This separation is crucial: heavy keys don't benefit from hashing (collision cost dominates), while light keys have low collision probability when distributed to $B$ buckets via hash function $h: U \to [B]$.

**Why this works:** With $B = \Theta(n/\log^2 n)$ buckets and light records uniformly hashed, the expected number of light records per bucket is $O(\log^2 n)$, manageable for local processing.

**Phase 2: Placement**

Pre-allocate destination arrays:
- For each heavy key $x$: allocate array $D_x^H$ of size $\alpha f(\sigma_x)$
- For each light bucket $b$: allocate array $D_b^L$ of size $\alpha f(\sigma_b)$

The slack factor $\alpha$ guarantees placement succeeds with high probability using **randomized placement** (see [[randomized rounding]] / ball-and-bins arguments).

**Phase 3: Local Semisort**

Process each destination independently:
- **Heavy keys:** Records already separated by key—just write to their pre-allocated arrays
- **Light records in bucket $D_b^L$:** Pack into contiguous array $C_b$, then semisort internally

For light buckets, the original GSSB uses a parallel hash table + radix sort, incurring $O(1)$ expected work per record (total $O(n)$ expected work). **The key innovation** is upgrading Phase 3 to achieve $O(n)$ work **with high probability** while maintaining $O(\log^2 n)$ depth.

### The Core Technical Contribution

The authors show that within each packed light bucket $C_b$:
- Any distinct key appears at most $O(\log^2 n)$ times whp (by Chernoff bounds on the sampling + hashing)
- Local semisort can be done deterministically (or with concentration) in $O(m_b)$ work per bucket
- Total work aggregates to $O(n)$ whp across all buckets

This replaces reliance on hash table performance (which is only expected) with high-probability guarantees.

---

## Applications in Engineering

### 1. **Parallel Graph Algorithms**
Semisort is used in edge-processing pipelines (e.g., bucketing edges by source/destination vertex) before localizing computation. Enables $O(m \log n)$ work for certain graph algorithms like connected components or triangle counting.

### 2. **Distributed Database Grouping**
In MapReduce-style systems, semisort serves as a lightweight preprocessing step before group-by aggregations, reducing communication overhead compared to full sort.

### 3. **Sorting Networks & Parallel Comparison Exchange**
Semisort is a natural intermediate for building efficient parallel sorting networks with polylogarithmic depth.

### 4. **Load Balancing in Sparse Computations**
Grouping irregular data (e.g., sparse matrix rows by nonzero count) before distributing to processors, minimizing load imbalance.

### 5. **Cache-Oblivious Algorithm Design**
Semisort enables cache-efficient partitioning in algorithms where only grouping (not total order) is needed, reducing cache misses.

---

## Common Mistakes / Pitfalls

### 1. **Confusing "contiguous groups" with "sorted"**
Students often think semisort must produce a globally sorted array. In fact, keys $k_1$ and