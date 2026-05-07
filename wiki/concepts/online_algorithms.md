# Online Algorithms

## Definition

An **online algorithm** is an algorithm that must make irrevocable decisions about future requests without knowledge of what those requests will be. Specifically:

- Input arrives sequentially over time
- Algorithm must respond to each request immediately upon arrival
- Future requests are unknown when current decisions are made
- Once a decision is committed, it cannot be undone (or reversing is costly)

This contrasts with **offline algorithms**, which see the entire input in advance and can optimize globally.

The quality of an online algorithm is typically measured by its **competitive ratio**: the worst-case ratio of the algorithm's cost to the optimal offline algorithm's cost for the same input sequence.

$$\text{Competitive Ratio} = \max_{\text{all input sequences}} \frac{\text{Cost}_{\text{online}}(\sigma)}{\text{Cost}_{\text{offline}}(\sigma)}$$

where $\sigma$ denotes an input sequence.

---

## Key Equations & Metrics

### Competitive Ratio (Deterministic)
$$C_{\text{det}} = \sup_{\sigma} \frac{\text{ALG}(\sigma)}{\text{OPT}(\sigma)}$$

### Expected Competitive Ratio (Randomized)
$$C_{\text{rand}} = \sup_{\sigma} \frac{\mathbb{E}[\text{ALG}(\sigma)]}{\text{OPT}(\sigma)}$$

### Approximation via Overhead (Memory Allocation Example)
$$\text{Overhead} = \frac{\text{Total size of moved objects}}{\text{Size of triggering request}}$$

For polylogarithmic overhead:
$$\text{Overhead} = \mathcal{O}(\text{polylog}(\epsilon^{-1}))$$

---

## Physical Intuition / Derivation

### The Core Challenge

Online algorithms face a fundamental trade-off: **lack of future information forces conservative or adaptive strategies that may be suboptimal in hindsight.**

**Example: Memory Reallocation**

Imagine managing a parking garage with spaces of fixed size. Cars (objects) arrive and depart unpredictably. When a new car arrives:
- You know only that it needs a certain amount of space
- You don't know when other cars will leave
- You must decide immediately whether to:
  - Place it in available fragmented space, or
  - Rearrange parked cars (incurring movement cost)

If you knew the future (offline), you could pack perfectly. Online, you must guess whether rearrangement is worth it.

### Polylogarithmic Overhead Insight

The breakthrough in Jin (2026) uses the **sunflower lemma**—a combinatorial result stating that any large family of sets contains a "sunflower" structure. Applied to memory blocks:

- Instead of tracking arbitrary fragmentation, identify patterns in block sizes
- These patterns have special structure that permits efficient packing
- Expected overhead becomes $\mathcal{O}(\text{polylog}(\epsilon^{-1}))$ rather than $\tilde{\Omega}(\epsilon^{-1/2})$

The key insight: **structure in the problem space (sizes follow combinatorial patterns) enables better competitive guarantees than worst-case analysis alone.**

---

## Applications in Engineering

### 1. **Memory Management (Systems)**
- **Virtual memory paging**: deciding which pages to evict without knowing future accesses
- **Garbage collection**: compacting objects online to reduce fragmentation
- **Buffer pool management**: deciding which blocks to keep cached

### 2. **Scheduling & Resource Allocation**
- **Job scheduling on processors**: assigning jobs to machines as they arrive
- **Load balancing in distributed systems**: routing requests without knowing future load
- **Bandwidth allocation**: deciding packet priority without future demand

### 3. **Cache & Database Design**
- **Cache replacement policies** (LRU, LFU): evicting items without knowing future requests
- **Database query optimization**: choosing execution plans without statistics
- **Storage tiering**: moving data between fast/slow storage

### 4. **Network Routing**
- **Online shortest path**: routing packets before full network state known
- **Power grid management**: load balancing without future demand

### 5. **Financial Systems**
- **Online option pricing**: setting derivative prices without future underlying moves
- **Bid optimization**: deciding bid amounts without knowing competitor bids

---

## Common Mistakes / Pitfalls

### 1. **Confusing "Online" with "Real-Time"**
- Online ≠ fast execution
- An online algorithm can be slow; it just must decide immediately
- A real-time system is online but may have strict latency bounds

### 2. **Assuming Worst-Case = Average Case**
- Competitive ratio measures worst-case input sequences
- Adversarially chosen inputs (worst-case) are often unrealistic
- Expected/randomized analysis can be much better than deterministic bounds

### 3. **Ignoring the Gap Between Online and Offline**
- Some problems have $\Omega(n)$ competitive ratios (unavoidable)
- For others, the gap is small (e.g., paging is 2-competitive vs. optimal)
- Before designing an algorithm, prove lower bounds on what's achievable

### 4. **Not Distinguishing Deterministic vs. Randomized**
- Randomized online algorithms can beat deterministic ones
- But adversarial analysis assumes adversary knows the algorithm's randomness
- Expected competitive ratio is often much better than worst-case deterministic

### 5. **Overhead vs. Total Cost**
- In memory reallocation, "overhead" is the *cost of rearrangement*, not total memory used
- Easy to confuse "cost of adaptation" with "cost of operation"
- Define metrics clearly before claiming improvements

### 6. **Ignoring Practical Constraints**
- Polylog bounds look good theoretically but hide constants
- $\mathcal{O}(\text{polylog}(\epsilon^{-1}))$ may mean $(\log \epsilon^{-1})^{10}$ in practice
- Need empirical validation on real workloads

---

## See Also

- [[Competitive Ratio]] – formal measure of online algorithm quality
- [[Memory Fragmentation]] – the problem motivating memory reallocation algorithms
- [[Paging Problem]] – canonical online algorithm (page replacement)
- [[Sunflower Lemma]] – combinatorial tool from Erd