# Count-Min Sketch (CMS)

## Definition

The Count-Min Sketch is a probabilistic data structure that estimates the frequency of elements in a stream using sublinear space. It trades off accuracy for memory efficiency, making it useful for high-speed stream processing where exact counts cannot be maintained for all elements.

**Core Concept:** A CMS maintains a two-dimensional array of $d$ independent hash functions and $w$ counters per hash function. When an element arrives, it is hashed by all $d$ hash functions, and each corresponding counter is incremented. To query the estimated count of an element, the minimum value across all $d$ hash table lookups is returned.

## Key Equations

**CMS Structure:**
$$\text{CMS}[i][h_i(x)] \text{ for } i = 1, 2, \ldots, d$$

where:
- $h_i$ is the $i$-th independent hash function mapping elements to $\{0, 1, \ldots, w-1\}$
- $d$ is the number of hash functions (depth)
- $w$ is the number of counters per hash function (width)

**Estimation:**
$$\hat{f}(x) = \min_{i=1}^{d} \text{CMS}[i][h_i(x)]$$

**Error Guarantee:**
With probability at least $1 - \delta$, the estimated frequency $\hat{f}(x)$ satisfies:
$$f(x) \leq \hat{f}(x) \leq f(x) + \epsilon N$$

where:
- $\epsilon = \frac{e}{w}$ (relative error parameter)
- $N$ is the total number of stream elements processed
- $w \approx \frac{e}{\epsilon}$ counters per hash function
- $d = \ln(1/\delta)$ hash functions

**Space Complexity:**
$$O(d \cdot w) = O\left(\frac{1}{\epsilon} \ln\frac{1}{\delta}\right)$$

## Physical Intuition / Derivation

### Why Minimum Over Multiple Hash Functions?

When an element $x$ is hashed, collisions with other elements cause its counter to be incremented beyond its true frequency. Each hash function independently causes different collisions—element $x$ may collide with elements $\{a, b, c\}$ under hash function $h_1$, but different elements $\{d, e, f\}$ under $h_2$.

Taking the **minimum** across all hash functions reduces the impact of collisions: if $x$ collides heavily under $h_1$ but barely under $h_2$, the minimum gives a better estimate. This works because:
- The true frequency $f(x)$ contributes to every counter along the path
- Collision artifacts vary independently across hash functions
- The minimum is most likely to be the true count or close to it

### Counter Sizing and Saturation

A critical challenge emerges when counters are fixed-width (e.g., 8-bit): they saturate at $2^8 - 1$, capping estimation accuracy. The source material discusses several approaches to address this:

**Hierarchical Counter Sharing:** Use short counters (e.g., 6-bit) for lower-order bits and shared overflow counters in upper levels. However, this creates cascading errors—in the worst case, a single element's overflow propagates through $\Theta(\log(N/w))$ levels, and shared counters amplify errors across $\Theta(N/w)$ other elements.

**Counter Merging:** Start with larger counters and strategically merge adjacent counters to reclaim space, maintaining a hierarchy to handle value sizes appropriately.

## Applications in Engineering

### 1. **Network Traffic Monitoring**
- **Heavy hitter detection:** Identify the top $k$ frequent source/destination IP pairs in high-speed networks
- **DDoS attack detection:** Track volumetric anomalies with bounded memory on line cards
- **Example:** Cisco and other router vendors use CMS variants to monitor millions of flows with kilobytes of memory

### 2. **Database Query Optimization**
- **Cardinality estimation:** Estimate distinct element counts and frequency distributions for query planning
- **Join selectivity prediction:** Inform optimizer decisions without full table scans
- **Histogram generation:** Build approximate frequency histograms for cost estimation

### 3. **Cache Admission Policies**
- **Frequency-based replacement:** Track element access frequencies to decide which items to evict from LRU caches
- **Integration with adaptive replacement cache (ARC):** Hybrid policies combining frequency and recency

### 4. **Web/Search Analytics**
- **Trending topics:** Track word/phrase frequencies in real-time streams (Twitter, search queries)
- **Popular items:** Estimate product view counts without logging every access
- **Rate limiting:** Monitor per-user request counts across distributed systems

### 5. **Security and Anomaly Detection**
- **Intrusion detection:** Track suspicious pattern frequencies in network packets
- **Bot detection:** Monitor username/password attempt frequencies
- **Spam filtering:** Estimate spam word frequencies with minimal memory overhead

## Common Mistakes / Pitfalls

### 1. **Misinterpreting the Minimum as Accurate**
The minimum estimate is **biased optimistically**—it never underestimates true frequency, but can overestimate significantly in high-collision scenarios. Students often assume the estimate is "close" without understanding that error scales with total stream size $N$.

### 2. **Ignoring the $(f(x) + \epsilon N)$ Error Term**
The error bound is not relative to $f(x)$; it is **absolute** in the form $\epsilon N$. For a stream of 1 billion elements with $\epsilon = 0.001$, even a true count of 1 million can have an error of ±1 million. This is unacceptable for low-frequency elements.

### 3. **Fixed vs. Adaptive Counter Widths**
Using uniform counter widths (e.g., 32-bit) wastes space on infrequent elements. The source material emphasizes that most counters are small; adaptive sizing through hierarchies or compression can recover significant memory, but introduces query overhead.

### 4. **Confusing CMS with Hash Tables**
CMS does not store actual items; it only tracks counts