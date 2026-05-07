# Locality-Sensitive Hashing

## Definition

**Locality-sensitive hashing (LSH)** is a probabilistic technique for indexing high-dimensional data such that similar items hash to the same bucket with high probability, while dissimilar items hash to different buckets. Unlike standard hash functions that aim for uniform distribution regardless of data similarity, LSH exploits data geometry to accelerate approximate nearest-neighbor (ANN) search and similarity-based retrieval.

Formally, a family of hash functions $\mathcal{H}$ is **$(r, cr, p_1, p_2)$-sensitive** for a similarity measure $\text{sim}(x, y) \in [0,1]$ if for any two points $x, y$:

$$
\begin{cases}
P(h(x) = h(y)) \geq p_1 & \text{if } \text{sim}(x, y) \geq r \\
P(h(x) = h(y)) \leq p_2 & \text{if } \text{sim}(x, y) \leq cr
\end{cases}
$$

where $p_1 > p_2$ and $0 < c < 1$.

## Key Equations

### Single Hash Function Performance

The probability that a random hash function from a $(r, cr, p_1, p_2)$-sensitive family correctly pairs similar points is:

$$P_{\text{collision}}^{\text{similar}} = p_1$$

$$P_{\text{collision}}^{\text{dissimilar}} = p_2$$

### Multi-Stage Hashing

To improve discrimination, use $k$ independent hash functions combined via AND (all must agree):

$$P_k^{\text{similar}} = p_1^k$$

$$P_k^{\text{dissimilar}} = p_2^k$$

To amplify the similar-pair detection rate while controlling false positives, construct $L$ independent hash tables, each with $k$ functions (AND-amplification combined with OR-amplification):

$$P_L^{\text{similar}} = 1 - (1 - p_1^k)^L$$

$$P_L^{\text{dissimilar}} = 1 - (1 - p_2^k)^L$$

### Query Cost Trade-off

For $n$ points and parameter $\rho = \frac{\log p_2}{\log p_1}$, the expected number of distance computations during query is $O(n^\rho)$, balancing recall against computational cost.

## Physical Intuition / Derivation

### Why Standard Hashing Fails

A uniform hash function (e.g., MurmurHash) treats similar and dissimilar data identically—both distribute uniformly across buckets. This defeats similarity search because you must either:
- Check all buckets (no speedup), or
- Accept missing nearby points

### LSH Core Insight

Rather than fighting data geometry, exploit it. If you design hash functions that *respect* the similarity metric, similar points naturally cluster. The key is trading off:

1. **Precision vs. Recall**: Fewer hash functions → fewer buckets per hash table → more collisions (higher recall, more false positives)
2. **Number of Tables**: Multiple independent tables allow OR-amplification (accept a point if *any* table matches)

### Concrete Example: Hamming Distance

For binary vectors and Hamming distance, a simple LSH is the **bit-sampling hash**:

$$h(x) = x_i$$

where $i$ is a random bit position. Two vectors at Hamming distance $d$ collide with probability:

$$P(\text{collision}) = \frac{n - d}{n}$$

where $n$ is vector length. This is $(r, cr, p_1, p_2)$-sensitive for appropriately chosen thresholds, because collision probability decreases monotonically with distance.

Combining $k$ bits via AND gives collision probability $\left(\frac{n-d}{n}\right)^k$, suppressing false positives. Multiple tables amplify hits on true neighbors.

### Why It Works Theoretically

The method exploits **concentration of measure**: in high dimensions, distances cluster sharply around a mean. LSH functions are designed to have correlation structure matching this clustering, so thresholded similarity is preserved under hashing.

## Applications in Engineering

### 1. **Entity Resolution & Data Deduplication**
Zhang et al.'s **AutoBlock** system uses LSH to generate candidate pairs for entity matching in data integration pipelines. Rather than comparing all $O(n^2)$ pairs, LSH filters to promising candidates:
- Hash records by attribute tokens
- Pairs in same bucket become candidates for entity linker
- Dramatically reduces matching comparisons while maintaining recall

**Benefit**: Scales entity resolution to million-record datasets.

### 2. **Approximate Nearest-Neighbor Search**
Core use case across ML and information retrieval:
- **Image search**: Find visually similar images in a corpus
- **Recommendation systems**: Retrieve candidate items similar to user profile
- **Document clustering**: Identify near-duplicate web pages

Example: Pinterest's visual search engine uses LSH (via learned similarities) to retrieve similar pins at interactive latencies.

### 3. **Anomaly Detection**
Network intrusion detection systems use LSH-based clustering:
- Hash network flows by feature profiles
- Clusters contain similar traffic patterns
- Outliers (unusual flows in their buckets) flagged as anomalies

### 4. **Plagiarism & Copyright Detection**
SHINGLE-based LSH detects document similarity:
- Hash $k$-grams (consecutive token sequences) of documents
- Documents sharing many shingles hash to same buckets
- Efficiently identifies candidate plagiarism cases at scale

### 5. **Machine Learning Feature Hashing**
LSH-based feature hashing reduces dimensionality while preserving similarity structure for downstream models, particularly in online learning scenarios.

## Common Mistakes / Pitfalls

### 1. **Confusing LSH with Bloom Filters**
- **Bloom Filter**: Membership test (is $x$ in set $S$?)
- **LSH**: Similarity search (find $y$ in $S$ similar to query $x$)

Bloom filters don't preserve similarity structure; LSH does.

### 2. **Ignoring Parameter Tu