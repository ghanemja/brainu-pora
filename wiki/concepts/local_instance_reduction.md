# local instance reduction

## Definition

**Local instance reduction** is a proof technique that leverages the bounded size of local instances to establish upper bounds on the size of global instances through a pigeonhole argument. Given a problem instance with a maximum local instance size $L_{\text{local}}(\varepsilon)$, the method constructs a function $\Lambda$ that maps any instance of size $L_{\text{local}}(\varepsilon) + 1$ down to one of size $L_{\text{local}}(\varepsilon)$ by identifying and removing a single element that can be separated by the remaining structure. By analyzing the pre-images of this mapping via the pigeonhole principle, one derives a recursive bound relating the global instance size $L^{\#}$ to the local bound.

**Key insight:** If every instance exceeding the local threshold contains a removable element, then the existence of large global instances implies many copies of smaller instances exist, creating a contradiction when combined with structural constraints.

## Key Equations

Given a problem instance $D$ with $|D| = L^{\#}$ elements (triples of points), define the reduction function:

$$\Lambda: \binom{D}{L_{\text{local}}(\varepsilon)+1} \to \binom{D}{L_{\text{local}}(\varepsilon)}$$

$$\Lambda(I) = I \setminus \{\sigma_a\}$$

where $\sigma_a$ is any element that can be separated by the graph $G_{I \setminus \{\sigma_a\}}$ constructed from the remaining elements.

By the pigeonhole principle, there exists a set $S$ with:

$$|\Lambda^{-1}(S)| \geq \left\lceil \frac{L^{\#}}{L_{\text{local}}(\varepsilon) + 1} \right\rceil - 1 =: C$$

This yields the fundamental reduction inequality:

$$L^{\#} = O\left(L_{\text{local}}(\varepsilon)^{\alpha} \varepsilon^{-\beta}\right)$$

In the cited context, the exponents were derived as $\alpha = 9$ and $\beta = 8$.

## Physical Intuition / Derivation

The method works in three stages:

### Stage 1: Establish Removability
For any instance larger than the local bound, guarantee that at least one element can be removed without affecting the remaining structure's validity. This is possible because:
- The local instance defines the **maximum** size of "locally constrained" subproblems
- Any larger instance must contain redundancy—elements that don't participate in maximal local structures

### Stage 2: Count Pre-Images
Apply the pigeonhole principle: if we have $L^{\#}$ elements and each reduction function pre-image has size roughly $\frac{L^{\#}}{L_{\text{local}}(\varepsilon)+1}$, then some reduced set $S$ appears many times (i.e., many different elements can be the one removed).

Let $C = |\Lambda^{-1}(S)|$ be the count of "removable elements relative to $S$."

### Stage 3: Apply Structural Constraints
The key move is to apply a structural lemma (e.g., Claim 7.8 in the source) that bounds $C$ in terms of the graph structure:

$$C = O(L_{\text{local}}(\varepsilon)^{\alpha} \varepsilon^{-\beta})$$

This constraint on $C$ propagates backward to bound $L^{\#}$:

$$C \approx \frac{L^{\#}}{L_{\text{local}}(\varepsilon)+1} \implies L^{\#} = O(C \cdot L_{\text{local}}(\varepsilon))$$

The exponent grows with each recursive application, explaining the polynomial blow-up (here $\alpha = 9$).

## Applications in Engineering

### 1. **Graph Drawing & Planar Subdivision**
- Analyzing local constraints in planar graph embeddings (the origin of this technique)
- Proving bounds on the maximum size of "linked noncrossing double ladders" in planar graphs
- Applications to VLSI circuit layout verification

### 2. **Constraint Satisfaction & Logic**
- Bounding satisfying assignments for formulas with local structure constraints
- SAT/CSP solvers exploiting sparsity patterns to prune search spaces
- Proving complexity bounds for locally constrained logical systems

### 3. **Combinatorial Geometry**
- Analyzing point configuration spaces with bounded-degree local constraints
- Robot motion planning with localized collision avoidance
- Geometric data structure design (e.g., tree decompositions of planar graphs)

### 4. **Network Analysis**
- Bounding node degrees in networks where each node's neighborhood obeys strict constraints
- Analyzing fault-tolerant distributed systems with local redundancy guarantees

### 5. **Proof Systems**
- Establishing degree bounds for polynomial hierarchy separation
- Proving lower bounds on the size of refutations in local proof systems

## Common Mistakes / Pitfalls

1. **Assuming the pre-image is uniform:** Not all reduced sets $S$ have the same pre-image size. You must use the pigeonhole maximum and account for variation.

2. **Forgetting the +1 in the exponent:** The recursive relation is $L^{\#} / (L_{\text{local}} + 1)$, not $L^{\#} / L_{\text{local}}$. This shifts the bound substantially.

3. **Circular reasoning on removability:** One must **prove** (via structural properties) that every element in an over-large instance is indeed separable—this doesn't follow from the definition of "local instance" alone.

4. **Confusing local vs. global:** Students often conflate the local bound (defined intrinsically) with the global bound (derived via reduction). They are different quantities with different roles.

5. **Ignoring the growth of exponents:** Each application of the reduction may increase polynomial exponents ($L_{\text{local}}^9$ vs. $L_{\text{local}}^3$), dramatically weakening bounds. This is why careful engineering of the underlying structural lemmas is critical.

6. **Neglecting corner cases:** The argument typically requires $L \geq 3$ or similar; failing to verify boundary conditions invalidates the