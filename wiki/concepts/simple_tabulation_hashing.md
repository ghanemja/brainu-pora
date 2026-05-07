# simple tabulation hashing

## Definition

Simple tabulation hashing is a randomized hash function construction that maps keys from a large domain into a smaller range by decomposing each key into independent characters (bytes or fixed-width blocks) and XORing precomputed random values from lookup tables. For a key $k$ decomposed into $c$ characters $k = (k_1, k_2, \ldots, k_c)$, the hash value is:

$$h(k) = T_1[k_1] \oplus T_2[k_2] \oplus \cdots \oplus T_c[k_c]$$

where each table $T_i$ is independently populated with uniformly random values from the target range $[m]$, and $\oplus$ denotes bitwise XOR.

Despite its simplicity, simple tabulation hashing provides strong theoretical guarantees on collision probability and independence properties, making it practical for high-probability analysis of randomized algorithms.

## Key Equations

**Hash function definition (general form):**
$$h(k) = \bigoplus_{i=1}^{c} T_i[k_i] \pmod{m}$$

**Collision probability bound (4-wise independent upper bound):**
For keys $x \neq y$, the probability that $h(x) = h(y)$ is at most $O(1/m)$ under certain conditions, with tighter bounds available depending on the structure of table sizes.

**Expected number of collisions in $n$ keys:**
$$E[\text{# collisions}] = \binom{n}{2} \cdot P(h(x) = h(y)) \leq \frac{n^2}{2m}$$

**Tail bound application (Chernoff/Chebyshev for weighted sums):**
For sums $S = \sum_{i} w_i X_i$ where $X_i$ are independent random variables with simple tabulation properties, concentration bounds yield:
$$P(S \geq (1+\delta)\mu) \leq \exp\left(-\frac{\delta^2 \mu}{3}\right)$$

## Physical Intuition / Derivation

### Why XOR?

The XOR operation preserves independence across character positions. When each character of a key is mapped independently through its own random table, XORing the results maintains the property that collisions depend only on the *disagreement pattern* between keys. If two keys differ in character position $i$, then $T_i[k_i] \oplus T_i[k_i']$ is uniformly distributed regardless of the values in other positions.

### Independence Structure

Simple tabulation achieves **4-wise independence**: for any four distinct keys $x, y, z, w$ and any four values $a, b, c, d$, the events
$$\{h(x)=a, h(y)=b, h(z)=c, h(w)=d\}$$
are independent (under standard assumptions on table sizes). This is strictly weaker than universal hashing but stronger than pairwise independence, and crucially, it holds with $O(1)$ space and time per hash evaluation.

### Why This Matters for High-Probability Bounds

In the referenced parallel algorithm context, simple tabulation enables concentration arguments on weighted sums of random variables where weights correspond to, e.g., vertex degrees or work costs. The 4-wise independence suffices to apply tail bounds (Chernoff, Hoeffding, or concentration inequalities for geometric random variables) without incurring union bounds over all possible key pairs—a technique essential for proving work bounds hold with high probability (probability $1 - n^{-\Omega(1)}$).

## Applications in Engineering

### 1. **Parallel Algorithm Analysis**
In work-efficient parallel algorithms (as demonstrated in the source), simple tabulation hashing enables:
- **Concentration analysis of vertex partition quality** in graph algorithms (MIS, coloring) by ensuring balanced cuts with high probability
- **Work distribution guarantees** in semisort and parallel sorting by controlling the variance of load-per-processor

### 2. **Hash Table Implementation**
- Fast, cache-friendly implementation via table lookups (minimal branch prediction failures)
- Suitable for real-time systems where worst-case hash evaluation time matters
- Used in competitive programming and systems with memory-access predictability constraints

### 3. **Randomized Data Structure Robustness**
- Cuckoo hashing and other collision-resolution schemes benefit from the tail-bound guarantees
- Skip lists and treaps with tabulation-based link selection
- Bloom filter implementations requiring controlled false-positive rates

### 4. **Monte Carlo Algorithm Certification**
- In distributed systems, tabulation hashing supports load-balancing proofs with high-probability guarantees
- Enables composition of multiple randomized routines without exponential union bounds

## Common Mistakes / Pitfalls

1. **Assuming universal hashing suffices:** Simple tabulation provides *4-wise independence*, not full universality. The distinction matters when applying concentration inequalities—union bounds over pairs (which suffice for universality) are weaker than the tail bounds enabled by higher independence.

2. **Ignoring table size dependencies:** The independence guarantees degrade if table sizes are not chosen carefully. Tables should be powers of 2 or primes relative to the range $m$ to avoid cascading collisions. Naively fixing all $T_i$ to size $2^b$ with $b < \log(m)$ can introduce bias.

3. **Confusing XOR with addition modulo $m$:** While XOR is standard in simple tabulation (bit-level operation), sum-based variants (addition mod $m$) have *different* independence properties and may not support the same tail bounds. The choice affects collision analysis fundamentally.

4. **Applying to non-decomposable keys:** Simple tabulation requires keys to be decomposable into independent fixed-width components. For variable-length strings or composite objects without a clear byte decomposition, preprocessing is required, and independence guarantees may not propagate.

5. **Over-relying on theoretical guarantees in practice:** While high-probability bounds are asymptotically strong, constants matter. For moderate $n$ (say, $n < 10^6$), the tail bound probability $1 - n^{-\Omega(1)}$ may still allow occasional bad events. Always profile and validate on realistic workloads.

## See Also

- [[universal hashing