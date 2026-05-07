# parallel semisort

## Definition

**Parallel semisort** is an algorithm that rearranges an array of $n$ records with keys from a universe $U$ into *semisorted order* — a relaxed sorting where records with the same key are grouped together, but the relative order within groups is unspecified. The algorithm achieves $O(n)$ work with high probability while exploiting parallelism through careful load balancing.

**Semisorted order** means:
- All records with key $x$ occupy a contiguous segment
- Different keys appear in sorted order
- Within each key's segment, order is arbitrary

This is a weaker requirement than full sorting, enabling faster parallel computation when full ordering isn't needed.

## Key Equations

### Allocation Function
For a sampled count $s$, allocate space:
$$f(s) = \alpha\left(c\log n + \sqrt{2sc\log n}\right)$$

where $\alpha$ is an overflow safety factor and $c$ is a constant tuned via concentration bounds.

### Work Bound via Chernoff
The underallocation failure probability (by Chernoff lower tail) is:
$$\Pr[\hat{W} \leq \mu - t] \leq \exp\left(-\frac{t^2}{2\mu}\right) = \exp(-c\log n) = n^{-c}$$

### Total Allocated Space
$$T = \alpha\sum_{x \in H} f(\sigma_x) + \sum_{b \in [B]} f(\sigma_b)$$

with high probability concentration giving $T = \Theta(n)$.

### Rehashing Collision Probability
Using a 2-universal hash family into range of size $m_b^K$:
$$\Pr[\text{collision}] \leq \binom{D}{2} \cdot \frac{1}{m_b^K} \leq \frac{m_b^2}{2m_b^K} = \frac{1}{2m_b^{K-2}} \leq \frac{1}{2} \quad \text{for } K \geq 3$$

Each rehash attempt succeeds independently with $p \geq 1/2$; total attempts follow $\text{Geometric}(1/2)$.

## Physical Intuition / Derivation

### Why Semisort?

Full sorting requires $\Omega(n\log n)$ comparisons in the worst case. But many applications (e.g., grouping records by ID, then processing each group independently) only need records grouped by key. Semisort exploits this relaxation.

### Three-Phase Structure

**Phase 1: Sampling to Estimate Sizes**
- Randomly sample each record with probability $p_s \approx \sqrt{\log n / n}$ to get a quick estimate
- Compute sample counts $\sigma_x$ and $\sigma_b$ per key and bucket
- Use concentration inequalities (Chernoff bounds) to ensure sample counts reliably estimate true multiplicities $N_x$, $N_b$

Why sampling? Direct counting costs $O(n)$ space upfront; sampling gives good estimates with $O(\sqrt{n\log n})$ samples.

**Phase 2: Heavy-Key vs. Light-Key Partition**
- **Heavy** keys: those with sample count $\sigma_x \geq \tau$ (threshold)
  - Allocated dedicated output regions
  - Few in number (at most $O(n/\tau)$)
- **Light** keys: everything else
  - Packed into buckets, then refined locally

This separation isolates the easy case (heavy keys, predictable sizes) from the hard case (light keys, noisy size estimates).

**Phase 3: Local Rehashing**
- Within each bucket $C_b$ of light records, rehash into a smaller range
- Collision-handling via radix sort + linear scan
- Independent geometric-distributed attempts per bucket
- Concentrate via weighted sum of independent geometric RVs (Theorem 2.3)

### Why High Probability Bounds?

Using union bounds over keys and buckets:
$$\Pr[E_{\text{under}}] = \Pr[\exists x: N_x > f(\sigma_x) \text{ or } \exists b: N_b > f(\sigma_b)]$$

Each event has tail probability $n^{-c}$; union bound over $\leq 2n$ events gives $\Pr[E_{\text{under}}] \leq O(n^{1-c})$, hence $n^{-\Omega(1)}$ with tuned $c$.

## Applications in Engineering

### 1. **Database Indexing and Grouping**
Semisort is ideal when building hash-based indexes or grouping records (SQL GROUP BY) without needing full sort. Faster than sorting when key distribution is skewed (many duplicates).

### 2. **Distributed Key-Value Aggregation**
In MapReduce-style systems, semisort replaces full sorting during the shuffle phase. Reduces network traffic and computation since only key groups need coherence, not global order.

### 3. **Bucketing for Approximate Query Processing**
Data warehousing: partition records into buckets for approximate range queries. Semisort provides bucket boundaries without per-record ordering overhead.

### 4. **Parallel Cache-Oblivious Algorithms**
The heavy/light partition and local rehashing adapt naturally to cache hierarchies; light keys exploit locality within buckets, heavy keys use dedicated paths.

### 5. **Load Balancing in Task Distribution**
When assigning work to processors, semisort groups similar tasks together (by type/resource requirement), enabling better load balancing without global ordering.

## Common Mistakes / Pitfalls

### 1. **Confusing Semisort with Bucketing**
Semisort guarantees *all* records with the same key are contiguous; plain bucketing may split keys across buckets if hash collisions aren't resolved. Semisort is deterministic in grouping (post-algorithm), even if internally probabilistic.

### 2. **Assuming $O(n)$ Work Without High Probability Caveats**
The $O(n)$ bound holds **with high probability** (failure $n^{-\Omega(1)}$),