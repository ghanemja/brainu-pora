# Next Fit Algorithm

## Definition

The **Next Fit** algorithm is a simple online bin packing algorithm that maintains a single "open" bin at any time. When a new item arrives:

1. If the item fits in the current open bin, place it there
2. If the item does **not** fit, close the current bin and open a new bin for the item

The algorithm never reopens a closed bin, making it extremely lightweight in terms of memory and computation.

**Online context**: The algorithm makes irrevocable placement decisions without knowledge of future items, characteristic of online problems.

## Key Equations

### Classic Bin Packing
For the standard bin packing problem (bin capacity = 1, no constraints), Next Fit achieves:

$$\text{Competitive Ratio} = 2$$

This means: $NF(I) \leq 2 \cdot OPT(I)$ for any instance $I$.

### Green Bin Packing (GBP)
In the generalized setting with a "green space" parameter $G \in [0,1)$ and cost multiplier $\beta$:

**Case 1: $\beta G \leq 1$ (small cost for non-green space)**
$$\text{Competitive Ratio} = \frac{2 + \beta(1-G)}{\beta + (1-\beta G)}$$

Special cases:
- When $\beta = 0$ or $G = 1$: ratio $= 2$ (recovers classic bin packing)
- When $\beta = 1, G = 0$: ratio $= 2$ (standard case)

**Case 2: $\beta G > 1$ (expensive non-green space)**

Using parameter $\tau \in [0, 1-G]$, items with $s_i \geq G + \tau$ are packed separately:

$$\text{Competitive Ratio} = \max\left\{\frac{G(1+\tau\beta)}{G+\tau}, \frac{G(2+\tau\beta)}{G+2\tau}, \frac{2+\tau\beta}{1+\tau\beta}\right\}$$

The optimal $\tau$ minimizes this maximum expression.

## Physical Intuition / Derivation

### Why Next Fit Achieves Ratio 2

Consider any instance with OPT using $k$ bins. Next Fit closes a bin only when the next item doesn't fit. Therefore:

$$\text{Sum of sizes in bins 1 and 2} > \text{bin capacity}$$
$$\text{Sum of sizes in bins 3 and 4} > \text{bin capacity}$$
$$\vdots$$

If Next Fit uses $2m$ bins, then $m$ pairs each have combined size exceeding capacity. Thus the total item size exceeds $m \times \text{capacity}$, meaning OPT requires at least $m$ bins. This gives $NF \leq 2 \cdot OPT$.

### GBP Motivation

Green Bin Packing models realistic constraints where:
- **Green space** ($G$): fraction of bin reserved for specific use (e.g., cooling, overhead)
- **Cost multiplier** ($\beta$): penalty for using non-green space (e.g., $\beta > 1$ means expensive)

The ratio formula shows how Next Fit's performance degrades as non-green space becomes more costly ($\beta$ increases) or when green space shrinks ($G$ decreases).

## Applications in Engineering

### 1. **Data Center Resource Allocation**
- Items = virtual machines or tasks; bins = physical servers
- Green space = reserved capacity for system services
- $\beta$ = cost ratio for consuming shared infrastructure vs. dedicated resources
- Next Fit used for low-complexity, real-time VM placement

### 2. **Memory Management in Embedded Systems**
- Bins = memory blocks; items = allocated objects
- Green space = reserved regions (stack, firmware)
- Simple, predictable memory fragmentation bounds

### 3. **Manufacturing / Production Line Scheduling**
- Items = jobs; bins = time slots or production lines
- Green space = setup/safety margin
- Fast heuristic for just-in-time scheduling

### 4. **Network Packet Scheduling**
- Items = packets; bins = time slots or buffers
- Competitive ratio bounds guarantee worst-case latency

### 5. **Energy-Aware Bin Packing**
- Items = computational tasks; cost = energy consumption
- $\beta$ = ratio of idle power to active power
- Analysis of trade-offs between opening new "bins" (servers) vs. overfilling existing ones

## Common Mistakes / Pitfalls

### 1. **Confusing Online vs. Offline Performance**
- Next Fit's ratio of 2 is tight for the online setting
- Offline bin packing with knowledge of all items achieves ratio 11/9 ≈ 1.22 (First Fit Decreasing)
- **Error**: Expecting online algorithms to match offline guarantees

### 2. **Assuming Ratio 2 Holds for GBP Without Proof**
- The formula $\frac{2 + \beta(1-G)}{\beta + (1-\beta G)}$ is **not** always 2 when $\beta \neq 0$ and $G \neq 1$
- **Error**: Naively applying classic results to generalized settings

### 3. **Ignoring Case Distinction ($\beta G \leq 1$ vs. $> 1$)**
- When $\beta G > 1$, Next Fit's behavior changes fundamentally
- Opening new bins becomes preferable to filling non-green space
- **Error**: Using Case 1 formula when Case 2 conditions hold

### 4. **Parameter Selection for $\tau$**
- The authors note that optimal $\tau$ must be computed; it is **not** arbitrary
- **Error**: Treating $\tau$ as a tuning parameter without minimization

### 5. **Asymptotic vs. Absolute Approximation**
- For finite item sizes, "asymptotic ratio" includes an additive constant: $A(I) \leq \alpha \cdot OPT(I) + \gamma$
- **Error**: Confusing $\alpha$ (asymptotic ratio)