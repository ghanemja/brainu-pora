# Matroid

## Definition

A **matroid** is an abstract combinatorial structure that generalizes the notion of linear independence in vector spaces. Formally, a matroid $M = (E, \mathcal{I})$ consists of:

- A finite ground set $E$
- A collection $\mathcal{I}$ of subsets of $E$ (called *independent sets*) satisfying:
  1. **Empty set axiom**: $\emptyset \in \mathcal{I}$
  2. **Hereditary property**: If $I \in \mathcal{I}$ and $I' \subseteq I$, then $I' \in \mathcal{I}$
  3. **Exchange axiom**: If $I, J \in \mathcal{I}$ with $|I| < |J|$, then there exists $e \in J \setminus I$ such that $I \cup \{e\} \in \mathcal{I}$

A **polymatroid** generalizes matroids further by associating with each subset $T \subseteq E$ a value via a **rank function** $f: 2^E \to \mathbb{R}_{\geq 0}$ satisfying:
- $f(\emptyset) = 0$ (normalization)
- $f(T) \leq f(S)$ for $T \subseteq S$ (monotonicity)
- $f(S \cup T) + f(S \cap T) \leq f(S) + f(T)$ for all $S, T \subseteq E$ (submodularity)

The polymatroid base polytope is:
$$B(f) = \left\{ x \in \mathbb{R}^E : x(S) \leq f(S) \text{ for all } S \subseteq E, \quad x(E) = f(E) \right\}$$

where $x(S) = \sum_{e \in S} x_e$.

## Key Equations

**Submodular rank function (fundamental property):**
$$f(S \cup T) + f(S \cap T) \leq f(S) + f(T)$$

**Connectivity condition** for polymatroids: A polymatroid $(E, f)$ is connected if there is no non-empty proper subset $T \subsetneq E$ satisfying:
$$f(T) + f(E \setminus T) = f(E)$$

**Dimension of polymatroid base polytope:**
$$\dim B(f) = |E| - k$$
where $k$ is the number of connected components in the decomposition of $(E, f)$.

**Characterization of identifying sets** (Theorem 5.1): A set $S$ is identifying for a polymatroid $X = B(f)$ with connected components $\{E_1, \ldots, E_k\}$ if and only if:
$$|S \cap E_i| \geq |E_i| - 1 \quad \text{for all } i \in [k]$$

## Physical Intuition / Derivation

### From Linear Independence to Matroids

Matroids capture the essential combinatorial properties of linear independence:
- In a vector space, any two maximal linearly independent subsets (bases) have the same cardinality
- You can always "swap" an element in one basis for an element outside it to get another basis
- These properties hold *abstractly* without reference to vector spaces

The matroid formalism lets us study these properties in graph theory (cycle spaces), geometry (point configurations), and optimization without committing to a specific algebraic structure.

### Polymatroids as Generalizations

Polymatroids relax matroids by:
1. Allowing rank values to be fractional or arbitrary real numbers
2. Associating rank with every subset (not just independent sets)
3. Requiring *submodularity* instead of the strict matroid axioms

**Submodularity** intuitively says: adding an element to a larger set increases the rank less than adding it to a smaller set (diminishing returns property). This arises naturally in:
- Information theory (entropy is submodular)
- Graph theory (cut capacities are submodular)
- Optimization (resource allocation constraints)

### Connected Components

A polymatroid decomposes into independent "connected components" where no element interaction crosses component boundaries: $f(T) = \sum_{i} f(E_i \cap T)$.

For identifying or controlling sets, you need to "cover" each component sufficiently. Since each component has dimension $|E_i| - 1$, you must include at least $|E_i| - 1$ elements from component $i$ to distinguish all points in the base polytope.

## Applications in Engineering

### 1. **Network Flow and Cuts**
In directed graphs, the minimum $s$-$t$ cut function is submodular. Matroids characterize families of edge sets with special connectivity properties, used in:
- Interdiction problems (blocking paths/flows)
- Survivable network design
- Optimal spanning arborescences

### 2. **Optimization under Matroid Constraints**
Greedy algorithms work optimally for linear objectives over matroid bases:
$$\max \{ w^\top x : x \in B(M) \}$$
This is exploited in:
- Minimum spanning tree algorithms
- Auction design and mechanism design
- Submodular maximization

### 3. **Sensor Placement and Observability**
Identifying/controlling sets determine which measurements uniquely determine system state:
- In sensor networks, select minimum sensor locations to distinguish all feasible operating points
- Applied to power systems, building automation, and distributed control

### 4. **Information Theory and Data Compression**
Entropy functions are submodular; matroids model:
- Information sources with dependencies
- Optimal compression schemes
- Data aggregation in sensor networks

### 5. **Supply Chain and Production**
Polymatroid rank functions model:
- Resource constraints with substitutability
- Production capacity under shared resources
- Interdiction and resilience planning

## Common Mistakes / Pitfalls

### Mistake 1: Confusing Matroids with General Posets
**Wrong**: "A matroid is just any system of independent sets."