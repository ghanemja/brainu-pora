# Comparison-based Sorting

## Definition

**Comparison-based sorting** is an algorithm paradigm that orders a set of elements by comparing pairs of elements and rearranging them based on the comparison outcomes. Formally, a comparison-based sorting algorithm for a set $X$ can only determine the relative order of elements through pairwise comparisons, where each comparison answers a query of the form "is $x_i < x_j$?"

A fundamental restriction applies: any comparison-based sorting algorithm requires at least $\Omega(n \log n)$ comparisons in the worst case to sort $n$ elements, since there are $n!$ possible orderings and each binary comparison provides at most one bit of information.

**Sorting under partial information** extends this classical model: given a directed acyclic graph (DAG) $G = (X, E)$ that encodes known ordering constraints (a partial order), one can sort $X$ using only comparisons consistent with $G$. The efficiency of such an algorithm depends on $e(G)$, the number of linear extensions (total orders) compatible with the partial order.

## Key Equations

**Information-theoretic lower bound:**
$$\text{Comparisons needed} \geq \log_2(n!)  = \Theta(n \log n)$$

**Sorting under partial information - comparison complexity:**
$$C(G) = \Theta(\log e(G))$$

where $e(G)$ is the number of sorted orders consistent with partial order $G$.

**Time complexity hierarchy** (for sorting under partial information with preprocessing):
- **Classical bound** (Cardinal et al., STOC'10): $O(n^{2.5})$ preprocessing + $O(\log e(G) + n)$ sorting time
- **Recent result** (van der Hoog & Rutschmann, FOCS'24): $O(n^{\omega})$ preprocessing where $\omega < 2.372$, then $O(\log e(G))$ sorting time
- **Tight bound** (Haeupler et al., SODA'25; this work): $O(m)$ preprocessing + $O(\log e(G))$ sorting time

Here $m$ is the number of edges in the partial order DAG.

## Physical Intuition / Derivation

### Why Comparison-Based Sorting is Fundamental

The $\Omega(n \log n)$ lower bound arises from information theory: sorting is a search problem through the space of $n!$ possible permutations. Each comparison has a binary outcome, so $k$ comparisons can distinguish at most $2^k$ cases. Therefore:
$$2^k \geq n! \implies k \geq \log_2(n!) \approx n \log_2 n$$

### The Partial Information Perspective

Many real-world scenarios don't start from complete ignorance. Instead, we have:
- Prior knowledge of some element relationships
- Constraint graphs from previous computations
- Domain-specific orderings that are already established

If we precompute and store these constraints in a DAG $G$, the remaining sorting problem is easier because we have "eliminated" orderings incompatible with $G$.

**Key insight:** The number of valid linear extensions $e(G)$ measures how much uncertainty remains. If $G$ is already a total order, $e(G) = 1$ and zero additional comparisons are needed. If $G$ is empty (no constraints), $e(G) = n!$ and we need $\approx n \log n$ comparisons.

### The Algorithm Structure

The modern approach (this work) achieves $O(m)$ preprocessing through:

1. **Preprocessing phase** ($O(m)$ time): 
   - Build a data structure encoding the partial order
   - Construct specialized heap structures that respect $G$
   - Index the space of linear extensions efficiently

2. **Sorting phase** ($O(\log e(G))$ comparisons):
   - Use adaptive strategies that eliminate large portions of remaining linear extensions per comparison
   - Employ "unified bound heaps" to extract information efficiently from the partial order
   - Merge or refine orderings incrementally

### Why Heaps Matter

The breakthrough introducing "unified bound heaps" optimizes the extraction of decision boundaries from a partially ordered set. Rather than extracting minimal elements naively ($O(n)$ per extraction), the heap structure allows logarithmic-time identification of which comparison will maximally partition the remaining linear extensions.

## Applications in Engineering

### 1. **Database Query Optimization**
Partial orders naturally arise in multi-attribute indexed queries. Tuple comparisons are expensive (disk I/O); sorting under partial information minimizes comparison operations by leveraging existing index constraints.

### 2. **External Sorting**
When sorting data that doesn't fit in memory, comparison costs dominate I/O. Preprocessing disk-resident partial orders reduces the number of comparisons required, directly translating to fewer disk accesses.

### 3. **Constraint Satisfaction and Scheduling**
In project scheduling (PERT/CPM networks), task dependencies form a DAG. Sorting tasks for execution while respecting dependencies is exactly the partial-information sorting problem.

### 4. **Machine Learning: Feature Ranking**
Feature importance is often partially known (some features dominate others, but relationships between others are unclear). Efficient sorting of features under partial information improves feature selection algorithms.

### 5. **Biological Sequence Analysis**
In phylogenetic reconstruction, evolutionary relationships between species form a partial order. Sorting organisms or sequences consistent with phylogenetic constraints uses this framework.

### 6. **VLSI and Circuit Design**
Topological sorting with partial constraints appears in circuit dependency graphs. Minimizing comparisons (gate operations) reduces chip design complexity.

## Common Mistakes / Pitfalls

### 1. **Confusing Partial Orders with Partial Sorting**
- **Mistake:** Thinking "partial information" means you only get a partial result.
- **Reality:** You get a *complete* sort, but you're given *partial* information about the elements beforehand. The output is always a total order.

### 2. **Ignoring Preprocessing Cost**
- **Mistake:** Focusing only on the $O(\log e(G))$ sorting time and ignoring the $O(m)$ preprocessing.
- **Reality:** For small problem instances, preprocessing dominates. Preprocessing-aware analysis is essential.

### 3. **Assuming DAG Size is Small**
- **Mistake:** Assuming a partial order has