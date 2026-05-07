# Parameterized Complexity

## Definition

**Parameterized complexity** is a computational complexity framework that analyzes algorithmic problems by isolating a secondary **parameter** $k$ (distinct from the input size $n$) to better understand computational hardness. Rather than asking "is this problem solvable in polynomial time?", parameterized complexity asks: "can we solve this problem in time $f(k) \cdot \text{poly}(n)$ for some function $f$ depending only on $k$?"

A decision problem is **Fixed-Parameter Tractable (FPT)** with respect to parameter $k$ if it admits an algorithm with runtime:

$$T(n,k) = f(k) \cdot n^{O(1)}$$

where $f(k)$ is any computable function (often exponential, factorial, or worse) and the polynomial factor is independent of $k$.

This contrasts with **W[1]-hard** or **W[2]-hard** problems, which are believed to lack FPT algorithms under widely-held complexity conjectures (analogous to P ≠ NP).

### Kernelization

A central technique in parameterized complexity is **kernelization** (data reduction): an algorithm that preprocesses an instance $(x, k)$ into a smaller equivalent instance $(x', k')$ where:
- $|x'| \leq g(k)$ (kernel size bounds depend only on $k$)
- $k' \leq k$
- $(x, k)$ is a YES-instance if and only if $(x', k')$ is a YES-instance

A problem admitting a kernel of size $\text{poly}(k)$ is automatically FPT.

## Key Equations

### FPT Runtime Bound
$$T(n, k) \in O(f(k) \cdot n^c)$$
where $c$ is a constant independent of $k$.

### Kernel Size (Polynomial Kernels)
$$|K(I,k)| \in O(k^d)$$
for constant $d$; kernels can also be exponential or depend on other structural parameters.

### Enumeration with Polynomial Delay

For enumeration kernels, solutions must be output with **polynomial-delay**:

$$\text{Time between consecutive solutions} \in O(\text{poly}(n, k))$$

The **PD-kernel model** (from source material) requires that "good" solutions from the compressed instance are lifted to the original instance with polynomial delay, while "bad" solutions may be discarded.

## Physical Intuition / Derivation

### Why Parameters Matter

Consider **Vertex Cover** on a graph $G = (V, E)$: find a set $S \subseteq V$ with $|S| \leq k$ such that every edge has at least one endpoint in $S$.

- **Classical view**: NP-complete, worst-case exponential.
- **Parameterized view**: If $k$ is small (e.g., $k = 5$ vertices in a large graph), we can:
  1. Pick an edge $(u,v)$; either $u$ or $v$ must be in the cover
  2. Branch into two cases, reducing $k$ by 1 each time
  3. Achieve $O(2^k \cdot n)$ runtime: brutal for $k=30$, but tractable for $k \leq 10$

This is **intuitive** because problem hardness is often concentrated in the parameter, not the whole instance.

### Kernelization Intuition

Kernelization removes "obviously irrelevant" data:
- In Vertex Cover: any vertex of degree $> k$ must be in the cover (else its neighbors form a certificate it's impossible)
- Removing such vertices and updating the problem creates a **kernel** of size $O(k^2)$

The kernel acts as a **computational bottleneck**: once we reduce to the kernel, any algorithm (even brute-force) becomes tractable.

### Enumeration Kernels

The source material identifies a tension:
- **Enum-kernels** (Creignou et al.): Too permissive; yields trivial kernels for easy enumeration problems
- **Polynomial-delay kernels** (Golovach et al.): Too restrictive; discourages kernel development
- **PD-kernels** (new model): Allows filtering "bad" solutions in compressed space while efficiently lifting "good" solutions

This is crucial for **listing all solutions** (e.g., all vertex covers of size $\leq k$), not just finding one.

## Applications in Engineering

### 1. **Graph-Based Network Optimization**
Parameterized algorithms for network design problems (feedback vertex set, tree decomposition) enable exact solutions on moderately-complex networks that are NP-hard classically.

### 2. **Constraint Satisfaction & SAT Solving**
Many SAT/CSP preprocessors use kernelization-like techniques: unit propagation, pure literal elimination, and bounded-depth inference reduce instances before search.

### 3. **Bioinformatics & Genomics**
Sequence alignment and phylogenetic tree problems often have natural small parameters (e.g., edit distance, tree width). FPT algorithms provide exact solutions for medically-relevant datasets.

### 4. **VLSI & Circuit Design**
Feedback vertex set (removing minimum edges/nodes to make a circuit acyclic) is parameterized-tractable; used in timing analysis and test generation.

### 5. **Combinatorial Optimization in OR**
Vehicle routing, facility location, and clustering problems with structural parameters (number of clusters, degree bounds) benefit from FPT approximation and enumeration algorithms.

### 6. **Automated Theorem Proving & Knowledge Compilation**
Bounded treewidth and pathwidth parameters enable efficient knowledge compilation and model counting (counting solutions to CNF formulas).

## Common Mistakes / Pitfalls

### 1. **Confusing FPT with Polynomial-Time**
FPT means $f(k) \cdot \text{poly}(n)$, not polynomial overall. If $f(k) = 2^k$, an algorithm solving a problem on $n=1000, k=30$ requires $\approx 2^{30} \times 10^9$ operations—often **impractical** despite being "tractable."

### 2. **Overlooking