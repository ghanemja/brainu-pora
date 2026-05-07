# Fixed-parameter tractability (FPT)

## Definition

**Fixed-parameter tractability** is a refined notion of computational tractability for problems with inherent *multi-dimensional complexity*. A decision problem is **FPT** with respect to a parameter $k$ if it can be solved in time $f(k) \cdot p(n)$, where:

- $n$ is the input size
- $k$ is a *parameter* (typically a structural property of the instance)
- $f$ is an arbitrary computable function (often exponential)
- $p(n)$ is a polynomial in $n$

Formally, a parameterized problem $(L, \kappa)$ is in **FPT** if there exists an algorithm $\mathcal{A}$, a function $f : \mathbb{N} \to \mathbb{N}$, and constants $c, d \in \mathbb{N}$ such that:

$$\text{time}(\mathcal{A} \text{ on } (x, k)) \leq f(k) \cdot |x|^c + d$$

where $\kappa(x) = k$ is the parameter value for instance $x$.

This contrasts with **classical NP-hardness**, which only considers $p(n)$ complexity (exponential in $n$ is considered intractable). FPT allows exponential dependence on $k$, making problems tractable when $k$ is small.

---

## Key Equations

### Running Time Characterization

$$T(n, k) = f(k) \cdot \text{poly}(n)$$

### Hardness Hierarchy: W-Hierarchy

Problems that are provably *not* in FPT belong to parameterized complexity classes:

$$\text{FPT} \subseteq \text{W[1]} \subseteq \text{W[2]} \subseteq \cdots \subseteq \text{XP}$$

where **XP** (slice-wise polynomial) allows $T(n, k) = n^{f(k)}$, much slower than FPT.

### Backdoor Parameterization

In backdoor analysis (as exemplified in QBF research), if $B$ is a backdoor of size $k$ to a tractable class $\mathcal{C}$:

$$\text{time} = f(k) \cdot \text{poly}(n)$$

The parameter $k = |B|$ measures the minimum number of variables/clauses that must be "fixed" to reduce to a tractable subproblem.

---

## Physical Intuition / Derivation

### Why FPT Matters

Classical complexity divides problems into polynomial (tractable) and NP-hard (intractable). But many real-world problems are:
- **Intractable in worst case** (NP-hard), yet
- **Tractable on practical instances** because those instances exhibit small *structural parameters*

**Example**: Finding a vertex cover of size $k$ is NP-hard in general, but solvable in $O(2^k \cdot n^2)$ time using branching. If your graph only needs 5 vertices removed to become edgeless, the algorithm runs in $O(32 \cdot n^2)$—fast!

### Why Not Just Use Classical Complexity?

- **Classical P/NP dichotomy**: "hard" means $n^{1000}$ is as bad as $2^n$—both are rejected
- **FPT perspective**: Recognizes that $2^k \cdot n^2$ is *practical* when $k \ll n$
- **Key insight**: Separate the exponential cost (tolerable if small) from polynomial cost (must be polynomial)

### Kernelization: The Core FPT Technique

Many FPT algorithms work via **kernelization**:
1. Apply reduction rules to compress the instance
2. Show that either the answer is determined, or $k$ decreases
3. Reach a **kernel**: an equivalent instance of size $g(k)$ (bounded by $k$ alone)
4. Solve the kernel by brute force in $f(k)$ time

$$\text{Original instance } \xrightarrow{\text{reduction rules}} \text{Kernel of size } g(k) \xrightarrow{\text{brute force}} \text{Answer}$$

---

## Applications in Engineering

### 1. **Computational Biology & Bioinformatics**
- **Phylogenetic tree reconstruction**: Parameterized by the number of allowed evolutionary events (small $k$)
- **Multiple sequence alignment**: Fixable parameterization by gap cost
- **Gene clustering**: Tractable when parameterized by cluster count

### 2. **Network Design & Optimization**
- **MAD tree problem** (minimum average distance spanning tree): FPT w.r.t. treewidth or modular width
  - Cable network design where structural width constraints exist
  - Minimize distance metrics under treewidth parameter
- **Steiner tree**: FPT in terminal count $k$; practical for small target sets

### 3. **Formal Verification & Model Checking**
- **Quantified Boolean Formula (QBF) solving**: FPT w.r.t. backdoor size to tractable syntactic classes (HORN, 2-SAT, AFFINE)
  - Hardware verification: Many industrial QBF instances have small backdoors even if formulas are huge
  - Controller synthesis: Quantifier depth + backdoor parameterization enables practical solving

### 4. **Constraint Satisfaction & SAT Solving**
- **SAT parameterized by backdoor size**: Classic result showing SAT is FPT
  - Modern SAT solvers exploit hidden structure; parameterization formalizes this
- **CNF clause structure**: FPT algorithms for bounded treewidth, pathwidth

### 5. **Graph Algorithms in VLSI & Circuit Design**
- **Vertex Cover, Feedback Vertex Set**: FPT in parameter size
  - VLSI placement problems modeled as graph problems with small deletion sets
- **Bounded treewidth**: Enables polynomial algorithms for NP-hard problems on tree-like circuit structures

### 6. **Operations Research & Logistics**
- **Facility location, clustering**: FPT in number of facilities/clusters