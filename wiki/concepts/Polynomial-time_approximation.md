# Polynomial-time Approximation

## Definition

A **polynomial-time approximation** is a computational approach that replaces an intractable optimization problem with a tractable surrogate problem, such that:

1. The surrogate is solvable in polynomial time
2. Any feasible solution to the surrogate is feasible for the original problem (conservatism)
3. The optimal cost of the surrogate is asymptotically close to the true optimum in the limit of interest

In the context of high-reliability systems, polynomial-time approximations maintain the first-order cost structure of the original problem while introducing only polynomial (not exponential) overhead. An **Asymptotic Fully Polynomial-Time Approximation Scheme (AFPTAS)** further guarantees a $(1 + \varepsilon)$-approximation to the surrogate optimum for any desired accuracy $\varepsilon > 0$.

## Key Equations

### Surrogate Feasibility
A solution is **surrogate-feasible** if it satisfies the efficiently computable upper bounds in place of exact constraints:

$$\text{Exact constraint: } P(\text{error}_i) \leq \delta_i$$
$$\text{Surrogate constraint: } \text{UpperBound}_i \leq \delta_i$$

where the upper bound is derived via union bound and Chernoff bounds.

### Cost Approximation Ratio
The optimality gap converges to unity as error tolerance shrinks:

$$\lim_{\delta \to 0} \frac{\text{Cost}_{\text{surrogate}}^*}{\text{Cost}_{\text{exact}}^*} = 1$$

The excess cost vanishes at rate:

$$\text{Cost}_{\text{surrogate}}^* - \text{Cost}_{\text{exact}}^* = o(\text{dominant cost scale})$$

with the gap being **logarithmically smaller** than the primary budget scale.

### AFPTAS Guarantee
An AFPTAS algorithm returns a solution with cost satisfying:

$$\text{Cost}_{\text{AFPTAS}} \leq (1 + \varepsilon) \cdot \text{Cost}_{\text{surrogate}}^*$$

for any $\varepsilon > 0$, with runtime polynomial in problem size and $\log(1/\varepsilon)$.

## Physical Intuition / Derivation

### Why Exact Problems Are Intractable

Many engineering optimization problems involve probabilistic constraints on rare events (e.g., failure probability $< 10^{-6}$). Evaluating these constraints requires either:
- Simulation with exponentially many samples
- Exact computation over exponentially many states

Both are computationally prohibitive.

### The Surrogate Construction Strategy

The derivation proceeds via two fundamental techniques:

**Step 1: Union Bound Decomposition**
A multi-class error probability is decomposed into pairwise comparisons via union bound (Lemma 1):

$$P(\text{any error}) = P\left(\bigcup_{i,j} \text{error}_{ij}\right) \leq \sum_{i,j} P(\text{error}_{ij})$$

This trades a complex joint probability for a sum of manageable pairwise terms.

**Step 2: Chernoff Exponential Bounds**
Each pairwise error probability is upper-bounded using Chernoff-type concentration inequalities (Proposition 1):

$$P(\text{error}_{ij}) \leq e^{-f(\text{query cost})}$$

where $f$ captures the correct exponential decay but introduces polynomial prefactors.

### Why the Gap is Small

The surrogate captures the **exponential decay structure** governing asymptotic behavior:
- True cost: $C^* = \log(1/\delta) / D + \text{lower order terms}$
- Surrogate cost: $C_s^* = \log(1/\delta) / D + O(1)$

The difference is $O(1)$ — constant overhead independent of the safety requirement. Relative to the exponential scale $\log(1/\delta)$, this becomes negligible, hence convergence to unity.

### Feasibility Preservation

**Key property:** If a query plan satisfies the surrogate constraints (which are conservative upper bounds), it automatically satisfies the exact constraints:

$$\text{UpperBound}_i \leq \delta_i \implies P(\text{error}_i) \leq \text{UpperBound}_i \leq \delta_i$$

This ensures that solutions optimized for the tractable surrogate are valid for the original problem.

## Applications in Engineering

### 1. **Multi-Model Inference Systems**
In systems combining multiple language models or classifiers:
- **Problem:** Optimize query allocation to minimize cost while guaranteeing joint error probability across all models
- **Application:** Replace intractable joint probability constraints with Chernoff bounds on pairwise misclassifications
- **Benefit:** Polynomial-time algorithm returns near-optimal resource allocation

### 2. **Reliable Embedded Systems**
Safety-critical systems (automotive, aerospace) with multiple redundant sensors:
- **Problem:** Design query strategy to achieve reliability $R > 1 - 10^{-8}$ at minimum cost
- **Application:** Surrogate replaces rare-event probability evaluation with efficiently computable upper bounds
- **Benefit:** Certifiable designs without Monte Carlo sampling overhead

### 3. **Adaptive Experimental Design**
Sequential testing in clinical trials or material science:
- **Problem:** Allocate experimental budget to minimize total cost while controlling false-discovery rate
- **Application:** Union bounds + Chernoff concentration bounds decompose multi-hypothesis problem
- **Benefit:** AFPTAS guarantees $(1+\varepsilon)$-approximate adaptive designs in polynomial time

### 4. **Network Reliability Planning**
Telecommunications or power grid design:
- **Problem:** Provision redundant paths/components to meet end-to-end reliability while minimizing cost
- **Application:** Surrogate constraints replace path-level failure probabilities with tractable upper bounds
- **Benefit:** Asymptotically optimal plans for high-reliability infrastructure

### 5. **Machine Learning with Confidence Bounds**
Training with certified robustness guarantees:
- **Problem:** Optimize model selection and ensemble size subject to worst-case error $\leq \delta$
- **