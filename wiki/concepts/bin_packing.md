# Bin Packing

## Definition

**Bin packing** is a combinatorial optimization problem where items of varying sizes must be assigned to a minimum number of **unit-capacity bins** (containers) such that the total size of items in each bin does not exceed capacity. Each item $i$ has a size $s_i \in (0, 1]$.

**Formal statement (classic):** Given a set of items with sizes $\{s_1, s_2, \ldots, s_n\}$, partition them into bins of capacity 1 to minimize the number of bins used.

**Green Bin Packing (GBP)** extends this with an **energy consumption model**: Each bin incurs energy cost based on how much of its capacity is utilized beyond a "green threshold." Parameters $G \in [0,1]$ (green capacity) and $\beta \geq 0$ (energy cost per unit) define the energy function:

$$f_{\beta,G}(x) = \max\{0, \beta(x - G)\}$$

where $x$ is the total size of items in a bin. The objective becomes:

$$\text{minimize} \quad (\text{number of bins}) + \sum_{\text{all bins}} f_{\beta,G}(x_j)$$

**Constrained Green Bin Packing (CGBP)** reverses the objective: minimize bins used subject to a constraint that total energy consumption does not exceed upper bound $U$.

## Key Equations

### Energy Consumption Function
$$f_{\beta,G}(x) = \max\{0, \beta(x - G)\}$$

This is **piecewise linear**: zero energy for $x \leq G$, then linear increase at slope $\beta$ for $x > G$.

### Total Cost (GBP)
$$\text{Cost} = B + \sum_{j=1}^{B} f_{\beta,G}(x_j)$$

where $B$ is the number of bins used and $x_j$ is the total item size in bin $j$.

### Approximation Ratio
For bin packing algorithms, the approximation ratio $\rho$ is defined as:

$$\rho = \frac{\text{Cost}_{\text{algorithm}}}{\text{Cost}_{\text{OPT}}}$$

Current best known: **$\frac{3}{2}$-approximation** for both GBP and CGBP (matches classical BP lower bound).

## Physical Intuition / Derivation

### Classic Bin Packing Intuition

Imagine packing boxes into shipping containers. Each container costs money to open, so you want to minimize containers used. However, you're constrained: overstuffing violates safety regulations. The problem is **NP-hard** (non-deterministic polynomial hard), meaning no known polynomial-time exact algorithm exists for large instances.

### Green Bin Packing Intuition

Now extend the scenario to **data centers with renewable energy**:

- Each data center (bin) has a baseline capacity $G$ powered by solar/wind (free, "green" energy)
- Demand exceeding $G$ requires purchasing fossil fuel energy at cost $\beta$ per unit
- Trade-off: opening more bins (fixed cost = 1) vs. overloading fewer bins (variable energy cost)

**Example:** If $G = 0.6$, $\beta = 2$, and you pack a single bin with total size $x = 0.8$:
$$f_{\beta,G}(0.8) = \max\{0, 2(0.8 - 0.6)\} = 2(0.2) = 0.4 \text{ units of energy cost}$$

The total cost of this single bin is $1 + 0.4 = 1.4$ (one bin opened + energy penalty).

### Why the Problem is Hard

The energy cost is a **non-additive function**: the cost of packing items together differs from packing them separately. This couples bin-filling decisions in non-trivial ways, preventing simple greedy algorithms from achieving optimality.

## Applications in Engineering

### 1. **Cloud Computing & Data Centers**
- Minimize operational cost (rack opening + power consumption) while respecting renewable energy budgets
- Green load balancing across geographically distributed data centers
- Critical for sustainability goals in hyperscale computing

### 2. **Truck Loading & Logistics**
- Pack shipments to minimize fuel consumption (vehicles underutilized up to a threshold $G$, then fuel cost increases superlinearly)
- E.g., fuel consumption only increases significantly beyond weight threshold $G$

### 3. **Memory Allocation**
- Allocate memory pages to minimize both the number of memory blocks (fixed cost) and power consumption
- Modern processors have "sleep states" requiring full capacity utilization threshold $G$ before high-power modes activate

### 4. **Bin Assembly in Manufacturing**
- Pack components into shipping containers where labor (opening a bin) has fixed cost, but packaging materials scale with overfilling

### 5. **Network Bandwidth Allocation**
- Assign flows to physical links where idle capacity up to $G$ consumes minimal energy, but above-threshold transmission consumes nonlinear power

## Common Mistakes / Pitfalls

### 1. **Confusing GBP with Weighted Bin Packing**
- **Mistake:** Thinking energy cost is simply $\beta \cdot x$ (linear in bin usage)
- **Reality:** Cost is $\max\{0, \beta(x-G)\}$ — the threshold $G$ creates a discontinuity at zero cost
- This threshold fundamentally changes algorithm design

### 2. **Ignoring the Trade-off Structure**
- **Mistake:** Greedily filling one bin to capacity (classic First-Fit Decreasing)
- **Reality:** Partially-filled bins may be preferable if energy cost of consolidation exceeds opening a new bin
- Example: With $\beta = 10$ and $G = 0.9$, packing a size-0.1 item alone (cost $10 \times 0.1 = 1.0$) is cheaper than adding it to a bin with size 0.85 (cost $10 \times 0.05 = 0.5$ extra, but maybe you wanted to leave that bin nearly empty)

### 3.