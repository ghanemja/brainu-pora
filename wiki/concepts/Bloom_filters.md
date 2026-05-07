# Bloom Filters

## Definition

A **Bloom filter** is a space-efficient probabilistic data structure used to test whether an element belongs to a set. It trades the possibility of false positives for dramatic space savings compared to storing the full set.

A Bloom filter consists of:
- A bit array of length $m$ bits, initially all zeros
- A set of $k$ independent hash functions $h_1, h_2, \ldots, h_k$, each mapping elements to positions in $\{0, 1, \ldots, m-1\}$

**Insertion operation:** To add element $x$, compute $h_i(x)$ for all $i \in \{1, \ldots, k\}$ and set those bit positions to 1.

**Membership query:** To test if $x$ is in the set, compute $h_i(x)$ for all $i$ and return TRUE if all corresponding bits are set to 1; otherwise return FALSE.

## Key Equations

**False positive rate (idealized):** For a filter with $m$ bits, $k$ hash functions, and $n$ inserted elements:

$$\varepsilon \approx \left(1 - e^{-kn/m}\right)^k$$

This assumes:
- All hash functions distribute uniformly
- Hash function outputs are independent
- The bit array is large relative to $n$

**Bits per element (bpe):** The space efficiency is often expressed as:

$$\text{bpe} = \frac{m}{n}$$

**Optimal hash function count:** Given a false positive rate target $\varepsilon$ and ratio $\text{bpe}$:

$$k^* = \text{bpe} \cdot \log_2(1/\varepsilon) \approx \frac{m}{n} \ln 2$$

The optimal choice is approximately $k^* = \text{bpe} \cdot \ln 2 \approx 0.693 \cdot \text{bpe}$.

**Space-time tradeoff (practical):** Accounting for discrete hash function counts and practical bit patterns, the actual false positive rate when implementing with integer $k$ and $\text{bpe}$ is:

$$\varepsilon_{\text{actual}}(k, \text{bpe}) = \left(1 - e^{-k/\text{bpe}}\right)^k$$

## Physical Intuition / Derivation

### Why False Positives Occur

Imagine inserting $n$ elements. Each insertion sets $k$ bits to 1. As more elements are added, the probability that a random bit position remains 0 decreases exponentially. When querying a non-member element $x$, all $k$ hash positions must happen to be set to 1—a collision pattern—causing a false positive.

### Derivation of $\varepsilon$

After inserting $n$ elements with $k$ hash functions into an $m$-bit array:
- Expected number of 1-bits: $m(1 - e^{-kn/m})$ (from the coupon collector perspective)
- For a query element, probability that a single bit position is 1: $p = 1 - e^{-kn/m}$
- Probability all $k$ positions are 1: $\varepsilon = p^k = (1 - e^{-kn/m})^k$

This derivation assumes uniform hashing and independence between positions.

### Why Discrete Parameter Selection Matters

In practice, implementations choose $k$ from integers (you cannot make 1.5 hash function calls). The source material emphasizes that selecting $(k, \text{bpe})$ pairs from discrete options produces different false positive rates than continuous optimization. **AutoCSF's parameter selection** evaluates $\varepsilon$ at each realizable configuration and picks the one with the largest empirical lower bound on space savings—avoiding mismatches between theory and implementation.

## Applications in Engineering

### 1. **Database and Cache Systems**
   - **Negative lookups:** A Bloom filter is queried before accessing expensive storage (database, disk, network). If the filter says "not present," the lookup is skipped entirely.
   - **Example:** LevelDB and RocksDB use Bloom filters to avoid disk seeks for non-existent keys.

### 2. **Network Routing and Firewalls**
   - **Packet classification:** Route lookups or firewall rules can be indexed with Bloom filters to quickly determine if a packet matches a rule set without examining the full table.

### 3. **Distributed Systems and Cache Coherence**
   - **Bloom filter networks:** Multicast systems use Bloom filters to summarize which nodes have cached data, reducing broadcast traffic.

### 4. **Bioinformatics and Sequence Matching**
   - **k-mer filtering:** Genomic sequence analysis uses Bloom filters to quickly reject sequences that cannot contain specific k-mers, pre-filtering expensive alignment steps.

### 5. **Data Deduplication and Stream Processing**
   - **Duplicate detection:** Web crawlers and log aggregators use Bloom filters to identify duplicate URLs or log entries with minimal memory overhead.

### 6. **Compressed Static Functions (Filter-Augmented)**
   - **Skewed distributions:** The source material discusses augmenting a CSF (compressed static function) with a Bloom filter for majority values. When the value distribution is highly skewed (e.g., one value appears in 50% of keys), storing a separate filter for the majority case saves space compared to storing all keys in the CSF.

## Common Mistakes / Pitfalls

### 1. **Assuming False Negatives Are Possible**
   Bloom filters have **no false negatives**—if an element is in the set, the filter will always return TRUE. The only source of error is false positives. Confusion here leads to incorrect system design.

### 2. **Ignoring Discrete Hash Function Overhead**
   Many analyses assume $k$ can be any real number $\approx 0.693 \cdot \text{bpe}$. In practice, $k$ is an integer, and using $k = 1$ or $k = 2$ when theory suggests $k = 1.5$ significantly changes actual false positive rates. The source material emphasizes this: empirical parameter selection may differ from continuous optimization by one discrete step.

### 