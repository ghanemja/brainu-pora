# Exponential Time Hypothesis

## Definition

The **Exponential Time Hypothesis (ETH)** is a foundational conjecture in computational complexity theory, introduced by Impagliazzo, Paturi, and Zehavi (2001). It states:

**The $3$-SAT problem cannot be solved in subexponential time in the number of variables.**

More formally: there exists a constant $c > 0$ such that $3$-SAT on $n$ variables requires time $2^{cn}$ in the worst case; equivalently, $3$-SAT is not solvable in $2^{o(n)}$ time.

This conjecture is accepted as a working hypothesis in the complexity community to rule out certain algorithmic breakthroughs. It is **weaker** than $\text{P} \neq \text{NP}$ (which allows for polynomial algorithms), but stronger than most standard complexity assumptions.

## Key Equations

**ETH Statement:**
$$\exists c > 0 : \text{3-SAT on } n \text{ variables requires } \Omega(2^{cn}) \text{ time}$$

**Contrapositive (used in hardness proofs):**
$$\text{If a problem has a } 2^{o(k)}n^{O(1)}\text{-time algorithm} \implies \text{ETH fails}$$

**Consequent hardness results:**
For a parameterized problem with parameter $k$ and input size $n$:
- **ETH-tight lower bound**: No $2^{o(f(k))} n^{O(1)}$-time algorithm exists unless ETH fails
- **Matching upper bound**: An FPT algorithm achieving $2^{O(f(k))} n^{O(1)}$ time is **essentially optimal** under ETH

### Common running time classes under ETH

| Complexity Class | ETH Implication |
|---|---|
| $2^{O(k)}n^{O(1)}$ | Consistent with ETH; likely optimal for hard problems |
| $2^{o(k)}n^{O(1)}$ | Contradicts ETH if proven to exist |
| $2^{O(k \log k)}n^{O(1)}$ | Tighter dependence; often ETH-tight for structural parameters like treewidth |
| $n^{O(k)}$ | XP (slice-wise polynomial); does not constrain ETH |

## Physical Intuition / Derivation

### Why ETH matters

The hypothesis bridges the gap between:
- **Upper bounds**: Algorithms we can design (often exponential but with varying bases)
- **Lower bounds**: Worst-case hardness we can prove (typically via NP-hardness alone)

Without assuming ETH, NP-hardness only tells us a problem is *at least* as hard as 3-SAT; it says nothing about whether a $2^{\sqrt{n}}$ or even $2^{n/2}$ algorithm might exist. ETH rules out such "surprising" subexponential algorithms.

### Example intuition: Why ETH constrains parameterized complexity

Consider a problem parameterized by $k$ with input size $n$:
- A *trivial* algorithm runs in $2^k n^{O(1)}$ time (enumerate all $2^k$ parameter values, process in polynomial time)
- ETH asks: **Can we do fundamentally better than the obvious exponential bound?**

If a problem admits a $2^{o(k)}n^{O(1)}$ algorithm, it means we can exploit problem structure to achieve *subexponential* dependence on $k$. ETH says this should be rare—reserved only for tractable cases.

### Hardness reduction strategy

To show a problem is **ETH-hard**:
1. Assume the problem has a $2^{o(f(k))}n^{O(1)}$ algorithm
2. Construct a reduction from 3-SAT (or from a known ETH-hard problem)
3. If $f(k)$ maps the reduction size $m \to k$ such that $m = \omega(f(k))$, this contradicts ETH

This is more powerful than NP-hardness alone, because it rules out entire algorithm classes.

## Applications in Engineering

### 1. **Parameterized Algorithm Design for NP-Hard Problems**

When a problem is **NP-hard but ETH-hard with parameter $k$**:
- **Upper bound strategy**: Design FPT algorithms matching the ETH lower bound
- **Example** (from source materials):
  - *$H$-free Subdivision*: Bounded search-tree algorithm runs in $2^{O(k)}n^{O(1)}$ time
  - ETH proves this is optimal for many graph classes $H$ (no $2^{o(k)}$ improvement possible)
  - Engineers designing exact solvers use this as a ceiling for algorithm development

### 2. **Topology & Simplicial Complexes**

**Optimal Morse Matching (OMM)** on bounded-treewidth complexes:
- **Problem**: Minimize critical simplices in a discrete gradient field (applications in computational topology, manifold analysis)
- **ETH result** (from source): No $2^{o(k \log k)}n^{O(1)}$-time algorithm exists (where $k = $ treewidth)
- **Practical impact**: 
  - Algorithm achieving $2^{O(k \log k)}n$ is provably near-optimal
  - Engineers working on 3D mesh simplification, homology computation know this boundary
  - Approximation or heuristic approaches are justified as better than exact computation in large instances

### 3. **Graph Modification Problems**

**Edge Subdivision to achieve $H$-free property**:
- **Problem**: Remove forbidden induced subgraphs by subdividing edges (network design, graph editing)
- **Engineering context**: 
  - Planning networks where certain graph structures must be avoided
  - Parameterized by $k$ (number of subdivisions allowed)
- **ETH hardness**: Rules out $2^{o(k)}$ algorithms; engineers use $2^{O(k)}$ bounded search-tree methods
- **Industrial example**: Telecommunications network modification to break specific topological constraints

### 4. **Algorithm