# First Fit Algorithm

## Definition

The **First Fit (FF) algorithm** is a greedy online bin packing heuristic that places each arriving item into the **first bin** (in order of opening) that has sufficient remaining capacity. If no open bin can accommodate the item, a new bin is opened.

**Formal Statement:**
- Maintain bins in the order they were opened
- For each incoming item of size $s$:
  1. Scan bins sequentially from the first opened bin
  2. Place the item in the first bin $b$ where $\text{remaining\_capacity}(b) \geq s$
  3. If no such bin exists, open a new bin and place the item there

## Key Equations

**Competitive Ratio (Single-dimensional case):**
$$C_{\text{FF}} = \mu + 2 + O(1/\mu)$$

More precisely, First Fit achieves a competitive ratio of:
$$C_{\text{FF}} \leq (\mu + 2)d + 1$$

where:
- $\mu$ = ratio of the largest item size to bin capacity
- $d$ = maximum number of items in any bin in an optimal solution
- The lower bound for any deterministic algorithm is $\mu$

**Cost Relationship:**
$$\text{Cost}_{\text{FF}} \leq (2 + \varepsilon) \cdot \text{OPT} \quad \text{(asymptotically, for bounded item sizes)}$$

## Physical Intuition / Derivation

### Why First Fit Works

First Fit exploits a simple principle: **reuse existing bins before opening new ones**. By scanning from the oldest bin, the algorithm ensures:

1. **Locality of Bin Usage**: Items are preferentially packed into early bins, leaving later bins with more "room to work with"
2. **Gap Minimization**: Wasted space tends to cluster in later bins rather than scatter across many bins

### Proof Sketch of Competitive Ratio

Consider any two consecutive bins $b_i$ and $b_{i+1}$ in a First Fit packing:

**Lemma:** If First Fit opens bin $b_{i+1}$, then $b_i$ cannot accommodate any remaining item that fits in $b_{i+1}$.

This implies: For any two consecutive open bins, the **sum of their utilizations exceeds the bin capacity** (in expectation). More formally:

$$\text{usage}(b_i) + \text{usage}(b_{i+1}) > C$$

where $C$ is bin capacity. Aggregating across all bins:

$$\sum_{i=1}^{n} \text{usage}(b_i) > \frac{n-1}{2} \cdot C$$

Therefore:
$$n < \frac{2 \cdot \text{Total Item Size}}{C} + 1 \leq 2 \cdot \text{OPT} + 1$$

This yields the classical $2$-approximation guarantee for bounded item sizes.

### Extension to Dynamic Settings

In dynamic bin packing (where items depart), First Fit's strength diminishes because:
- It cannot "revisit" earlier bins to fill gaps created by departures
- **Round-Robin Next Fit** (a variant) addresses this by cyclically scanning all open bins, achieving ratio $(\mu+2)d + 1$

## Applications in Engineering

### 1. **Memory Allocation**
- **Heap fragmentation reduction**: Operating systems use First Fit variants to allocate memory blocks
- Minimizes the number of disjoint memory regions ("bins")

### 2. **Task Scheduling**
- **Multiprocessor scheduling**: Assign tasks to processors to minimize total processors needed
- First Fit maps naturally to assigning each task to the first processor with sufficient idle capacity

### 3. **Data Center Resource Management**
- **VM placement**: Pack virtual machines onto physical servers based on CPU/memory requirements
- Reduces the number of active servers (power efficiency)

### 4. **Cutting Stock / Trim Loss**
- **Industrial manufacturing**: Pack orders onto standard-length materials (sheet metal, lumber)
- Minimizes material waste and setup costs

### 5. **Database Indexing**
- **B-tree node packing**: Assign records to disk blocks using First Fit principles
- Balances I/O efficiency and space utilization

## Common Mistakes / Pitfalls

### 1. **Assuming FF is Optimal**
❌ **Wrong:** "First Fit minimizes the number of bins"  
✓ **Correct:** FF gives a 2-approximation; it can use up to $\approx 2 \times \text{OPT}$ bins in the worst case

**Example:** Items of sizes $[6, 6, 5, 5, 4, 4, 4, 4]$ with bin capacity $10$:
- First Fit uses 4 bins: $[6,4], [6,4], [5,5], [4,4]$
- Optimal uses 3 bins: $[6,4], [6,4], [5,5]$ ✗ (infeasible)
- Actually optimal is 4 bins, so FF is optimal here

### 2. **Confusing with Best Fit**
❌ **Wrong:** "First Fit and Best Fit use the same logic"  
✓ **Correct:** 
- **First Fit**: Use first bin that fits (low computational cost)
- **Best Fit**: Use bin with *smallest remaining space* that fits (higher cost, often worse competitive ratio)

### 3. **Ignoring Item Ordering**
❌ **Wrong:** "FF always produces the same packing"  
✓ **Correct:** FF's performance is **input-dependent**
- Adversarial orderings can force FF to use $2 \times \text{OPT}$ bins
- This is the nature of online algorithms

### 4. **Applicability in Dynamic Settings**
❌ **Wrong:** "First Fit works equally well when items depart"  
✓ **Correct:** FF fails in dynamic settings because it cannot reuse space in earlier bins
- Use **Round-Robin Next Fit** or other Any-Fit variants instead

### 5. **Overhead Neglect**
❌