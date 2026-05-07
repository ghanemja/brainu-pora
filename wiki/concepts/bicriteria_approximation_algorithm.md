# bicriteria approximation algorithm

## Definition

A **bicriteria approximation algorithm** is an algorithm for optimization problems that relaxes the traditional single-criterion approximation by allowing violations in *two* dimensions simultaneously, trading off accuracy in one metric to achieve better approximation in another.

More formally, for an optimization problem with objective function $f$ and constraint set $\mathcal{C}$, a bicriteria $(\alpha, \beta)$-approximation algorithm is a polynomial-time (or FPT) algorithm that:

1. **Relaxes the constraint by factor $\beta$**: produces a solution satisfying constraints relaxed by multiplicative factor $\beta$ (e.g., uses $\beta m$ machines instead of $m$, or covers $\beta \cdot \text{OPT}$ elements instead of all)
2. **Approximates the objective by factor $\alpha$**: achieves objective value within multiplicative factor $\alpha$ of the optimum (where $\alpha \leq 1$ for maximization, $\alpha \geq 1$ for minimization)

The key insight is that slightly violating hard constraints (factor $\beta$) enables much stronger approximation guarantees (factor $\alpha$) compared to single-criterion approaches.

## Key Equations

For the **Parallel Maximum Coverage** (PMC) subproblem, the bicriteria guarantees discussed are:

$$(\alpha, \beta) = \left(1 - \frac{1}{e} - \varepsilon, O\left(\frac{\log m}{\log \log m}\right)\right) \quad \text{(randomized, poly-time)}$$

$$(\alpha, \beta) = \left(\left(1 - \frac{1}{e}\right)(1 - \varepsilon), 1 + \mu\right) \quad \text{(FPT in } m\text{)}$$

For **Parallel Min-Sum Set Cover** on unrelated machines:

$$\text{Approximation ratio} = O\left(\frac{\log m}{\log \log m}\right)$$

For related machines via densest subfamily:

$$\text{Approximation ratio} = \frac{8e}{e+1} + \varepsilon \approx 0.32 + \varepsilon$$

The constraint violation trades against the objective approximation. The $(1-1/e)$ factor arises from the classical greedy set cover / maximum coverage lower bound.

## Physical Intuition / Derivation

### Why Bicriteria Makes Sense

Traditional single-criterion approximation for hard problems requires either:
- Solving the exact problem (NP-hard) 
- Accepting poor approximation ratios (e.g., $O(\log n)$ for set cover)

Bicriteria relaxation unlocks the possibility of near-optimal solutions by asking: *"Can we afford a small, controlled violation of constraints?"*

### Concrete Example: Parallel Scheduling

In Min-Sum Set Cover on parallel machines:
- **Single criterion**: Schedule jobs on exactly $m$ machines, minimize total completion time → difficult
- **Bicriteria $(1-1/e, O(\log m / \log \log m))$**: Use slightly more machines (or allow elements to be covered slightly late), achieve near-optimal coverage quality

The constraint relaxation (extra machines or time) provides algorithmic flexibility that wouldn't exist under hard constraints.

### LP Relaxation + Randomized Rounding

The approach typically proceeds by:

1. **Relax integer constraints**: Convert the combinatorial problem to a linear program (LP) where variables take fractional values in $[0,1]$
2. **Solve LP**: Obtain fractional optimal solution $\text{OPT}_{\text{LP}}$
3. **Randomized rounding**: Round fractional variables probabilistically; violations of constraints happen with controlled probability
4. **Derandomization**: Use derandomization (e.g., Chernoff bounds) or FPT enumeration to guarantee solution quality

For PMC with LP relaxation:
- If element $e$ has fractional coverage $x_e \in [0,1]$ in the LP, round to covered with probability proportional to $x_e$
- Constraint violations occur when $x_e$ gets rounded "too aggressively"
- Bicriteria nature absorbs these probabilistic violations into the $\beta$ factor

## Applications in Engineering

### 1. **Cloud Computing / Resource Allocation**
- Allocate computational jobs across heterogeneous machines (related/unrelated) to minimize service completion time
- Constraint relaxation: Allow using $O(\log m)$ extra machines rather than the "optimal" $m$
- Gain: Provably near-optimal scheduling without NP-hard computation

### 2. **Network Design & Facility Location**
- Cover geographic regions with service facilities (sets) of different costs
- Constraint: Hard deadline on coverage time
- Bicriteria allows: Use slightly more facilities or miss deadline by $1+\varepsilon$ factor, achieve near-optimal cost

### 3. **Wireless Sensor Networks**
- Deploy sensors (sets) to cover monitoring regions (elements)
- Constraint: Limited energy or time windows
- Relaxation: Extend monitoring window by log factor, achieve near-optimal number of sensors

### 4. **Database Query Optimization**
- Select index sets to cover query patterns, minimizing response time sum
- Parallelism: Multiple processors execute different index selections
- Bicriteria: Allow processors mild resource overages, achieve good query latency

## Common Mistakes / Pitfalls

### 1. **Confusing $\alpha$ and $\beta$ directions**
Students often mix which dimension is relaxed vs. approximated. Remember:
- $\alpha$ = objective approximation (how close to optimal value)
- $\beta$ = constraint relaxation (how much we violate hard constraints)

### 2. **Assuming bicriteria is always weaker than single-criterion**
Actually, in practice $(1-1/e, O(\log m))$ may be *stronger* than achievable single-criterion approximations for the same problem, because polynomial-time single-criterion algorithms may only achieve $O(\log n)$ or worse.

### 3. **Neglecting when $\beta = 1 + \varepsilon$**
When constraint relaxation is *multiplicative* (like $1 + \mu$ factor), small absolute values of