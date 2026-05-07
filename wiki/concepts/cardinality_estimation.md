# cardinality estimation

## Definition

**Cardinality estimation** is the problem of determining the number of distinct elements in a data stream or dataset, particularly when:
- The stream is too large to fit in memory
- Elements arrive sequentially and cannot be revisited
- Approximate answers are acceptable with bounded error

It is a foundational problem in streaming algorithms with applications ranging from network traffic analysis to genomic data processing. The goal is to minimize both **space complexity** and **time complexity** while maintaining accuracy guarantees.

## Key Equations

### Standard Error for LogLog-family Estimators

$$\text{Standard Error} \propto \frac{1}{\sqrt{B}}$$

where $B$ is the number of buckets. Doubling accuracy requires quadrupling the number of buckets.

### Space Complexity Comparison

| Algorithm | Space Complexity | Notes |
|-----------|------------------|-------|
| Linear Counting | $O(n)$ | Stores all elements; only feasible for small cardinalities |
| LogLog | $B \times \log(\log(C))$ | Accurate at high cardinalities; $C$ is max representable cardinality |
| HyperLogLog (HLL) | $B \times \log(\log(C))$ | Hybrid approach; faster transition than pure LogLog |
| DynamicLogLog (DLL) | $4B + \log(\log(C))$ | Shared exponent reduces cardinality dependence to near-constant |

### DynamicLogLog Exponent Doubling

In traditional LogLog, squaring maximum representable cardinality (doubling the exponent) requires:
$$\Delta \text{space} = B \text{ bits}$$

In DynamicLogLog, this requires only:
$$\Delta \text{space} = 1 \text{ bit (global state)}$$

This is achieved through a **shared exponent** across all buckets rather than per-bucket exponents.

## Physical Intuition / Derivation

### Why Cardinality Estimation is Hard

Consider counting distinct IP addresses in network traffic. A naive approach stores every IP seen — impossible at billion-element scale. We need probabilistic methods that work with **bounded memory**.

### Core Insight: Leading Zero Distribution

All LogLog-family algorithms exploit this principle: **the position of the first 1-bit in the binary representation of a hash value is approximately geometric**. 

For a random hash $h$ of an element:
- Probability of leading $k$ zeros: $\approx 2^{-k}$
- If we observe an element with $k$ leading zeros, we can infer there are roughly $2^k$ elements total

**Example:** Observing an element with 8 leading zeros suggests we've seen ~256 distinct elements.

### Why Linear Counting Works at Low Cardinalities

At low cardinalities, most buckets are **empty**. If we have $B$ buckets and $n$ distinct elements, the number of empty buckets is:

$$\text{Empty buckets} \approx B \cdot e^{-n/B}$$

We can invert this to estimate $n$:
$$n \approx -B \ln\left(\frac{\text{Empty buckets}}{B}\right)$$

This is **accurate when collision probability is low** (small $n$ relative to $B$).

### Why LogLog Works at High Cardinalities

At high cardinalities, nearly all buckets have at least one element. We track the **maximum leading zero count** $\rho_{\max}$ seen across all buckets:

$$\text{Cardinality} \approx 2^{\rho_{\max}} \cdot B \cdot c$$

where $c$ is a calibration constant. The key insight: $\rho_{\max}$ grows logarithmically with cardinality, so we can represent astronomically large numbers with few bits per bucket.

### HyperLogLog: The Hybrid Approach

HyperLogLog blends Linear Counting (at small cardinalities) and LogLog (at large cardinalities) using a **smooth transition function**. However, this transition creates a known **error spike** in the mid-range.

### DynamicLogLog: Shared Exponent Innovation

Traditional approaches store the exponent **per-bucket**, requiring $\log(\log(C))$ bits per bucket. DynamicLogLog stores a **single global exponent** shared across all buckets:

- Each bucket stores only the **mantissa** (the fractional/leading-zero part) in 4 bits
- A global exponent adjusts the baseline scaling
- When a bucket's mantissa exceeds capacity, the global exponent increments
- This allows **early exits** — once the global exponent is set, most hash operations require only bucket update, not exponent checks (99.9% of operations at high cardinality)

This reduces space from $B \times \log(\log(C))$ to $4B + \log(\log(C))$ — the $\log(\log(C))$ term becomes negligible.

### Dynamic Linear Counting (DLC)

A novel refinement that eliminates the need for **correction factors** at transitions between estimation modes by continuously blending estimates across all cardinality ranges.

## Applications in Engineering

### Networking & Database Systems
- **Flow cardinality**: Estimating unique source/destination IP pairs in network traffic
- **Query optimization**: Estimating distinct values in database columns without scanning entire tables
- **Bloom filter sizing**: Determining approximate set cardinalities to design filters

### Bioinformatics & Genomics
- **Sequence assembly**: Counting distinct k-mers (DNA subsequences) to assess genome coverage
- **Species abundance**: Estimating distinct species or sequences in metagenomic samples
- **Error detection**: Identifying sequencing errors via unexpected cardinality drops

### Distributed Systems & Analytics
- **Unique users/events**: Real-time counting of unique identifiers in high-volume data streams
- **Deduplication**: Identifying duplicate records across distributed datasets
- **Cardinality statistics**: Supporting query planners in distributed query engines (Spark, Presto)

### Ecology & Population Studies
- **Species richness**: Estimating total species count from field samples
- **Mark-recapture**: Inferring population sizes from capture-recapture experiments

### Security & Anomaly Detection
- **Bot detection**: Identifying abnormal cardinality distributions in connection attempts