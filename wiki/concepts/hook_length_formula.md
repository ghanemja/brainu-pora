# Hook Length Formula

## Definition

The **hook length formula** is a combinatorial method for counting the number of standard Young tableaux (SYT) of a given shape. A standard Young tableau is a filling of a Young diagram with the integers 1 through $n$ (where $n$ is the total number of cells) such that entries are strictly increasing along rows (left to right) and down columns (top to bottom).

For a Young diagram of shape $\lambda$, the hook length formula states that the number of standard Young tableaux is:

$$f^\lambda = \frac{n!}{\prod_{(i,j) \in \lambda} h_{ij}}$$

where $h_{ij}$ is the **hook length** at cell $(i,j)$ in the Young diagram.

## Key Equations

### Hook Length Definition

For a cell $(i,j)$ in a Young diagram, the hook length is:

$$h_{ij} = \lambda_i - j + \lambda'_j - i + 1$$

where:
- $\lambda_i$ = length of row $i$
- $\lambda'_j$ = length of column $j$
- The formula counts: cells to the right + cells below + the cell itself

**Alternatively (geometric interpretation):**
$$h_{ij} = (\text{cells to the right}) + (\text{cells below}) + 1$$

### Hook Length Formula (Explicit Form)

$$f^\lambda = \frac{n!}{\prod_{(i,j) \in \lambda} h_{ij}}$$

For a partition $\lambda = (\lambda_1, \lambda_2, \ldots, \lambda_k)$ with $n = \sum_i \lambda_i$ cells total.

## Physical Intuition / Derivation

### Understanding Hook Lengths

Imagine filling a Young tableau cell by cell. When you place a number in cell $(i,j)$:
- It cannot be larger than the smallest number to its right in the same row
- It cannot be larger than the smallest number below it in the same column
- The hook length quantifies how many "restrictions" this placement imposes

**Visual Example (2×2 shape):**
```
□  □
□
```

Cell (1,1): hook length = 1 (right) + 1 (below) + 1 = 3
Cell (1,2): hook length = 0 (right) + 0 (below) + 1 = 1
Cell (2,1): hook length = 0 (right) + 0 (below) + 1 = 1

Count of SYT = $\frac{4!}{3 \cdot 1 \cdot 1} = \frac{24}{3} = 8$ ✓

### Why This Works: Bijective Reasoning

The hook length formula can be understood through the **RSK correspondence** (Robinson-Schensted-Knuth algorithm), which establishes a bijection between permutations and pairs of standard Young tableaux. The formula emerges from counting valid insertion sequences.

## Applications in Engineering

### 1. **Combinatorial Optimization**
- Counting feasible solutions to constraint satisfaction problems with partial order constraints
- Used in the permutation match puzzle research: determining the number of valid grid fillings

### 2. **Representation Theory & Quantum Chemistry**
- Computing dimensions of irreducible representations of the symmetric group $S_n$
- Applications in molecular orbital theory and quantum mechanics

### 3. **Algorithm Design & Analysis**
- Analyzing the complexity of sorting networks and sorting match puzzles
- Understanding the structure of valid permutations under constraints

### 4. **Scheduling & Resource Allocation**
- Counting valid schedules respecting precedence constraints
- Determining feasibility of constraint-based scheduling problems

### 5. **Computational Complexity**
- Establishing bounds on solution spaces for NP-complete problems
- From the source material: counting solutions to permutation match puzzles on $n \times n$ grids with ascending/descending constraints

## Common Mistakes / Pitfalls

### 1. **Confusing Hook Lengths with Cell Content**
❌ **Wrong:** Hook length is the value we place in the cell
✓ **Right:** Hook length is a property of the cell's position, computed before filling

### 2. **Miscounting the Hook Formula Terms**
❌ **Wrong:** Including diagonal cells as contributing to hooks
✓ **Right:** Only horizontal (right) + vertical (below) + 1 for the cell itself

### 3. **Off-by-One Errors**
❌ **Common mistake:** Computing $\lambda_i - j + \lambda'_j - i$ without the $+1$
✓ **Correct formula includes +1:** $h_{ij} = \lambda_i - j + \lambda'_j - i + 1$

### 4. **Applying to Non-Valid Diagrams**
❌ **Wrong:** Using hook formula for irregular or self-intersecting shapes
✓ **Right:** Formula only applies to valid Young diagrams (rows weakly decreasing left-to-right)

### 5. **Circular Dependencies in Understanding**
❌ **Pitfall:** The formula seems circular—why divide by hooks?
✓ **Insight:** The product of hooks encodes all valid constraint satisfaction paths

## See Also

- [[Standard Young Tableaux]] — the objects being counted
- [[Robinson-Schensted-Knuth Correspondence]] — bijective proof framework
- [[Young Diagrams]] — the visual shape structure
- [[Symmetric Group Representations]] — deep theoretical foundation
- [[Constraint Satisfaction Problems]] — application domain

## Sources

- Gajjar, K. & Misra, N. (2026). "Permutation Match Puzzles: How Young Tanvi Learned About Computational Complexity." *Proceedings of FUN 2026*, LIPIcs vol. 38, pp. 38:1–38:16
  - Directly applies hook length formula to count solutions of permutation match puzzles on $n \times n$ grids with ascending/descending constraints
  - Connects to DAG structure and constraint satisfaction