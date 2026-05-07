# FPT (Fixed-Parameter Tractability)

## Definition

**Fixed-Parameter Tractability (FPT)** is a complexity classification for decision problems where the computational hardness is separated into two independent factors: the input size $n$ and a problem-specific parameter $k$.

A decision problem is **FPT with respect to parameter $k$** if there exists an algorithm that solves instances in time:

$$T(n, k) = f(k) \cdot \text{poly}(n)$$

where:
- $f(k)$ is an arbitrary computable function depending *only* on the parameter $k$
- $\text{poly}(n)$ is a polynomial in the input size $n$
- The exponent of the polynomial is *independent* of $k$

**In contrast:**
- **W[1]-hard problems**: conjectured to not be FPT (analogous to NP-hardness for classical complexity)
- **XP (Slice-wise Polynomial)**: solvable in time $n^{f(k)}$ where the polynomial degree depends on $k$ (weaker than FPT)
- **Para-NP**: NP-hard even for fixed $k$ (clearly not FPT)

## Key Equations

**FPT Runtime Characterization:**
$$\boxed{T(n,k) = f(k) \cdot n^{O(1)}}$$

**Kernel/Preprocessing Bounds:**

If a parameterized problem is FPT, then a polynomial-time **kernelization** algorithm exists that reduces any instance $(I, k)$ to an equivalent instance $(I', k')$ where:
$$|I'| \leq g(k) \text{ for some function } g$$

**Polynomial Kernel (stronger result):**
$$|I'| \leq k^{O(1)} \text{ (or even } k^c \text{ for specific constant } c\text{)}$$

**Complexity Hierarchy:**
$$\text{FPT} \subseteq \text{W[1]} \subseteq \text{W[2]} \subseteq \cdots \subseteq \text{XP}$$

## Physical Intuition / Derivation

### Why Separate the Parameter?

Classical complexity (P vs NP) treats all input aspects uniformly. For many real-world problems, however, one factor is inherently small:

- **Graph problems**: finding a vertex cover of size $k$ in a graph with $n$ vertices (where $k \ll n$)
- **Scheduling**: processing $n$ tasks with at most $k$ machines
- **Compiler optimization**: code with at most $k$ loop nesting levels

### Building FPT Algorithms

**Strategy 1: Bounded Search Tree**
```
Solve(G, k):
  if k < 0: return FALSE
  if is_solution(G): return TRUE
  branch on k decision points, recursively solve subproblems
  T(n,k) = 2^k · poly(n)  [FPT!]
```

**Strategy 2: Kernelization**
```
Solve(I, k):
  (I', k') ← Kernelize(I, k)     [poly-time reduction]
  if |I'| > g(k): return FALSE
  Brute-force on I' of bounded size
  T(n,k) = poly(n) + f(k)  [FPT!]
```

**Strategy 3: Dynamic Programming on Tree Decomposition**

For problems parameterized by treewidth $tw$:
$$T(n, tw) = n^{O(1)} \cdot 2^{O(tw \log tw)}$$

### The Threshold Phenomenon

FPT algorithms exploit the insight that when a problem is "hard," the hardness is concentrated in the parameter $k$, not spread across the entire input.

For example, in the source material's **d-COC/dist-to-G problem**:
- Instances are reduced to a kernel where the number of connected components is bounded by $(d-1) \cdot b + 1) \cdot |M|^b$
- This bound depends only on the distance-to-graph-class $|M|$ and structural constant $d$, not on the full graph $|V(G)|$
- Thus the problem becomes FPT when other conditions hold

## Applications in Engineering

### 1. **VLSI Circuit Design & Chip Layout**
- **Vertex Cover on subgraphs**: routing problems with parameter = number of critical connections
- **Feedback Vertex Set (FVT)**: breaking cycles in dependency graphs with FPT algorithms parameterized by number of cycles to break
- Runtime: $O(1.2738^k + kn)$ for unbounded search trees beats classical exponential methods when $k$ is small

### 2. **Software Engineering & Compiler Optimization**
- **Code structure analysis**: parameterized by loop nesting depth or cyclomatic complexity
- Algorithms for detecting code clones within bounded edit-distance parameter
- Source control merge: FPT algorithms for detecting conflicting edits (parameter = number of conflicts)

### 3. **Bioinformatics & Computational Biology**
- **Phylogenetic tree reconstruction**: parameterized by number of mutations from reference
- **Protein folding constraints**: parameterized by number of constraint violations
- **Gene sequence alignment**: FPT when parameterized by edit distance $k$ (Levenshtein distance)

### 4. **Network & Infrastructure**
- **Minimum feedback arc set** in directed graphs (scheduling dependencies): FPT parameterized by arc set size
- **Graph coloring** with bounded degeneracy: FPT for sparse networks
- **Facility location problems**: parameterized by number of facilities to place

### 5. **Robotics & Path Planning**
- **Motion planning with obstacles**: parameterized by number of "narrow passages" or corridor constraints
- FPT algorithms for reconfiguration planning where $k$ = number of moves

### 6. **Distributed Systems**
- **Consensus with Byzantine faults**: FPT algorithms parameterized by number of faulty nodes $f$
- **Sensor network deployment**: FPT for placing sensors in graphs parameterized by coverage holes

## Common Mistakes / Pitfalls

### 1