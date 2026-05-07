# Superadditive Functions

## Definition

A function $f: \mathbb{R}_{\geq 0} \to \mathbb{R}$ is **superadditive** if for all $x, y \geq 0$:

$$f(x + y) \geq f(x) + f(y)$$

That is, the function value at the sum of two arguments is at least as large as the sum of the function values at those arguments individually.

A function is **strictly superadditive** if the inequality is strict for all $x, y > 0$.

A related concept is **superadditive with respect to a baseline**: a function $f$ is superadditive if $f(x) - f(0)$ is superadditive (i.e., $f(x+y) - f(0) \geq f(x) - f(0) + f(y) - f(0)$), which is equivalent to:

$$f(x + y) \geq f(x) + f(y) - f(0)$$

## Key Equations

**Basic superadditivity inequality:**
$$f(x + y) \geq f(x) + f(y) \quad \forall x, y \geq 0$$

**Normalized superadditivity (fixed-baseline):**
$$f(x + y) - f(0) \geq [f(x) - f(0)] + [f(y) - f(0)]$$

**Iterated form:** For any finite collection $x_1, x_2, \ldots, x_n \geq 0$:
$$f\left(\sum_{i=1}^{n} x_i\right) \geq \sum_{i=1}^{n} f(x_i) - (n-1)f(0)$$

**Inverse relationship:** A function $f$ is superadditive if and only if its negative $-f$ is [[subadditive functions|subadditive]].

## Physical Intuition / Derivation

### Why superadditivity matters

Superadditive functions capture situations where **combining resources produces disproportionately large benefits**—the whole is worth more than the sum of its parts.

### Geometric interpretation

Imagine a cost function that penalizes "exposure" or "uncovered material":

- When you have intervals in an ordering problem, each interval contributes to the total cost based on how much of it remains uncovered by previously-placed intervals.
- If the cost function $f$ is superadditive, placing two gaps sequentially creates a worse penalty than placing them separately.
- This means **consolidating gaps amplifies costs nonlinearly**.

### Example: Exponential functions

The function $f(x) = 2^x$ is superadditive because:
$$2^{x+y} = 2^x \cdot 2^y \geq 2^x + 2^y \quad \text{(for } x, y > 0\text{)}$$

This holds because exponential growth is strictly multiplicative, and multiplication of positive numbers $> 1$ exceeds addition.

### Derivation from concavity (partial)

While superadditivity is **not equivalent** to concavity or convexity:
- **Concave functions** (like $\ln(x)$) are typically **subadditive**
- **Convex functions** (like $x^2$) are typically **superadditive** for $x, y > 0$

However, the relationship is not one-to-one; superadditivity is a *combinatorial* property independent of local curvature.

## Applications in Engineering

### 1. Interval Scheduling & Bioinformatics
The primary motivating application from the source: ordering n intervals (e.g., DNA sequences, genomic features) to minimize exposure cost.
- **Use case:** Given a cost function $f$ that assigns penalties to uncovered regions, find the optimal ordering.
- **Computational insight:** When $f$ is superadditive, dynamic programming solutions run in polynomial time despite the exponential search space.

### 2. Load Consolidation in Logistics
Superadditive cost functions model scenarios where combining shipments creates nonlinear penalties:
- Fuel cost for a truck with payload $x + y$ exceeds the sum of costs for payloads $x$ and $y$ separately (e.g., due to non-linear fuel efficiency).
- **Implication:** Break shipments apart to minimize costs when the cost function is superadditive.

### 3. Resource Allocation & Capacity Planning
In cloud computing and data center management:
- Total power consumption for running combined workloads can exceed the sum of individual consumptions due to switching overhead, thermal effects, and coordinated activity.
- Superadditive power functions justify **workload separation**.

### 4. Network Flow & Congestion
Congestion cost on a link is often superadditive:
$$\text{Cost}(f + g) > \text{Cost}(f) + \text{Cost}(g)$$
where superadditivity captures how additional flow amplifies delays non-linearly (e.g., via queuing theory).

### 5. Manufacturing & Batch Processing
Setup costs and rework penalties in manufacturing can be superadditive:
- Processing batch size $x + y$ incurs worse quality loss than separately processing batches of size $x$ and $y$ if contamination/interference propagates.

## Common Mistakes / Pitfalls

### Mistake 1: Confusing with Convexity
**Error:** "Superadditive functions are convex."

**Reality:** Superadditivity is a *combinatorial* property; convexity is a *geometric* property. Some superadditive functions are not convex, and vice versa.
- $f(x) = 2^x$ is both superadditive and strictly convex.
- A carefully constructed piecewise linear function can be superadditive but not globally convex.

### Mistake 2: Ignoring the Baseline $f(0)$
**Error:** Assuming superadditivity holds without checking that $f(0) = 0$.

**Reality:** Many practical cost functions have $f(0) \neq 0$ (a fixed overhead). Always verify whether you're testing $f(x+y) \geq f(x) + f(y)$ or the normalized form $f(x+y) - f(0) \