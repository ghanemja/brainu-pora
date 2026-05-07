# multiplicative approximation

## Definition

A **multiplicative approximation** is a performance guarantee for an algorithm or solution that bounds the ratio of the algorithm's output cost to the optimal cost by a constant factor. If an algorithm produces a solution with cost $C_{\text{alg}}$ and the optimal solution has cost $C_{\text{opt}}$, then the algorithm provides a **$\rho$-multiplicative approximation** (or "$\rho$-approximation") if:

$$\frac{C_{\text{alg}}}{C_{\text{opt}}} \leq \rho$$

where $\rho \geq 1$ is called the **approximation ratio** or **approximation factor**. A smaller $\rho$ indicates a tighter (better) approximation to optimality.

### Contrast with Additive Approximation

Multiplicative approximations differ fundamentally from **additive approximations**, which bound the absolute difference:

$$C_{\text{alg}} - C_{\text{opt}} \leq \delta$$

Multiplicative bounds scale with problem size and are more robust when optimal costs vary widely, while additive bounds become meaningless when optimal costs are very small.

## Key Equations

**Approximation Ratio Definition:**
$$\rho = \max_{\text{instance}} \frac{C_{\text{alg}}}{C_{\text{opt}}}$$

**Approximation Quality (in percent):**
$$\text{Error} = \left(\rho - 1\right) \times 100\%$$

For example, a $1.5$-approximation has a $50\%$ error margin.

**Logarithmic Approximation Ratio:**
When dealing with exponential parameters (e.g., accuracy parameter $c = 1 + \epsilon$), worst-case ratios may scale as:
$$\rho = O(\log(1/\epsilon)) \text{ or } \rho = O(c^k)$$

where $k$ and $\epsilon$ are problem-specific parameters.

## Physical Intuition / Derivation

### Why Multiplicative Bounds Matter

In practical optimization problems, we rarely know the optimal solution. A multiplicative approximation gives us a **relative performance guarantee**: regardless of the problem instance, we know our algorithm will never perform worse than $\rho$ times optimal.

**Intuitive Example:**
- If $\rho = 2$, any instance where the optimal solution costs \$100 guarantees our algorithm costs at most \$200
- If the same instance had optimal cost \$1,000,000, our algorithm costs at most \$2,000,000
- The guarantee **scales with the problem's inherent difficulty**

### Why Theory vs. Practice Diverges

The source material demonstrates a key observation: **worst-case theoretical bounds often vastly overestimate actual performance.**

In the SKIN dataset experiments:
- **Theory predicted:** A $100$-approximation (i.e., $\rho = 100$)
- **Practice achieved:** Approximately a $4$-approximation (i.e., $\rho \approx 4$)

This divergence occurs because:

1. **Worst-case constructions are pathological:** Theoretical worst-case instances rarely arise in real data
2. **Parameter tuning effects:** As accuracy parameter $c = (1+\epsilon)$ decreases (tighter accuracy requirements), algorithms perform better multiplicatively:
   - $c = 100$: mean ratio $3.30$ 
   - $c = 1.1$: mean ratio $1.0006$

3. **Optimal cost dependency:** Multiplicative approximation quality degrades when optimal costs become very small relative to additive error terms (visible as spikes in Figure 3c when optimal low-rank approximation costs are near the Frobenius error magnitude).

## Applications in Engineering

### 1. **Approximation Algorithms (Computer Science)**
- **Scheduling problems:** Greedy scheduling algorithms guarantee $O(\log n)$ or constant-factor approximations
- **Traveling Salesman Problem (TSP):** Christofides algorithm provides $1.5$-approximation for metric TSP
- **Set Cover:** Greedy set cover achieves $O(\log n)$-approximation

### 2. **Streaming & Online Learning**
- **Low-rank matrix approximation** (as in source material): Maintain approximations with controlled multiplicative error as data streams arrive
- **Online convex optimization:** Regret bounds often expressed as multiplicative factors relative to optimal offline cost
- **Recourse control:** Balance solution quality ($\rho$ small) against solution stability (few updates)

### 3. **Control & Signal Processing**
- **Filter design:** Approximate optimal Wiener filter with computationally simpler alternatives, guaranteeing $\rho$-fold increase in mean-squared error
- **Quantization schemes:** Bound relative error in signal reconstruction after bit reduction

### 4. **Machine Learning & Optimization**
- **Convex relaxations:** Semidefinite programming relaxations provide multiplicative approximations to combinatorial problems (e.g., MaxCut with $\approx 0.878$-approximation)
- **Bandit algorithms:** Upper Confidence Bound (UCB) algorithms achieve logarithmic regret (multiplicative bound on cumulative loss)

### 5. **Network Design & Routing**
- **Facility location:** Greedy algorithms provide constant-factor approximations to facility location costs
- **Minimum spanning tree variants:** Bounded approximations for Steiner trees

## Common Mistakes / Pitfalls

### 1. **Confusing Approximation Ratio with Error Percentage**
**Mistake:** Saying a "$2$-approximation has $2\%$ error"

**Correct:** A $2$-approximation means the cost is at most **$2×$ optimal**, i.e., a **$100\%$ error margin** (cost can be up to double).

### 2. **Assuming Small Additive Error Implies Good Multiplicative Approximation**
**Mistake:** Trusting additive bounds when optimal cost is unknown/variable

**Pitfall:** An algorithm with additive error $\pm 10$ units performs extremely poorly if the optimal solution costs $11$ units (ratio approaches infinity), but excellently if optimal cost is $10,000$ units (ratio $\approx 1.001$).

### 3. **Ign