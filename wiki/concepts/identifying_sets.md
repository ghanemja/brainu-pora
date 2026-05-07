# identifying sets

## Definition

An **identifying set** for a collection $X$ of states (subsets or vectors) is a subset $S \subseteq E$ of elements such that every state in $X$ can be uniquely distinguished by its restriction to $S$. Formally:

$$S \text{ is identifying for } X \iff \forall x, x' \in X: \quad x|_S = x'|_S \implies x = x'$$

where $x|_S$ denotes the restriction of $x$ to coordinates in $S$.

**Equivalence with controlling sets:** For binary vectors ($X \subseteq \{0,1\}^E$), identifying sets and controlling sets are equivalent concepts. However, for general integral vectors ($X \subseteq \mathbb{Z}^E$), identifying sets may exist where controlling sets do not.

---

## Key Equations

**Distinguishability condition:**
$$|S| \geq \log_2 |X|$$
(Information-theoretic lower bound; not always tight)

**Minimum-weight identifying set problem:**
$$\min_{S \subseteq E} \sum_{e \in S} w_e \quad \text{s.t.} \quad S \text{ is identifying for } X$$

where $w_e$ denotes the weight (cost) of element $e \in E$.

**For matroid bases:** Identifying sets correspond to partitions defined by connected components of the matroid structure.

---

## Physical Intuition / Derivation

### Why Identifying Sets Matter

Consider a system with multiple possible states. To determine which state the system is in, we cannot always afford to measure *all* elements of $E$. An identifying set is the *minimal collection of measurements* that provides complete information about the system state.

**Example: Network Flows**
- States $X$ = all $s$-$t$ flows in a network
- Elements $E$ = edges in the network
- An identifying set $S$ of edges is sufficient to uniquely determine any flow by observing flow values only on edges in $S$
- Not all edges need to be monitored—we can infer flows on unmeasured edges from flow conservation constraints

### The Dichotomy: Binary vs. Integral Vectors

**For binary vectors** (e.g., subset families, matchings, spanning trees):
- A set distinguishes two states iff it separates their support sets
- Identifying and controlling become identical
- Polynomial-time algorithms often exist

**For integral vectors** (e.g., general flows):
- Two vectors can have identical entries on $S$ but differ elsewhere
- Identifying sets are weaker than controlling sets
- Computational hardness increases dramatically

---

## Applications in Engineering

### 1. **Electrical Networks**
Monitor a minimum-weight subset of edges to uniquely determine all electrical flows. Theorem 3.2 shows this exploits the special structure of Kirchhoff constraints.

### 2. **Network Flow Problems**
- **$s$-$t$ flows in acyclic networks:** Achieve $\sqrt{m}$-approximation for minimum identifying set (where $m$ = number of arcs)
- **General networks with cycles:** Problem becomes $\Sigma_2^P$-complete; no better than $|E|$-factor approximation unless P=NP

### 3. **Matroid-Based Systems**
For matroid bases (e.g., spanning trees, matchings):
- Identifying sets correspond to connected components
- Minimum-weight sets computable in polynomial time
- Applies to graphic matroids (spanning trees) and cographic matroids (flows)

### 4. **Polymatroid Base Polyhedra**
Optimization over fractional relaxations of combinatorial structures (e.g., generalized flows, submodular function minimization)

### 5. **Discrete Combinatorial Optimization**
Sensor placement, group testing, and verification problems where explicit binary vector lists are given:
- $2\ln|X|$-approximation algorithm available
- This bound is tight (best possible unless P=NP)

---

## Complexity Summary Table

| Structure | Problem | Complexity | Algorithm |
|-----------|---------|-----------|-----------|
| Binary vectors ($X \subseteq \{0,1\}^E$) | Min-weight identifying set | Dependent on structure | Matroid-based: poly-time |
| $s$-$t$ flows (acyclic) | Min-size identifying set | NP-hard | $\sqrt{m}$-approximation |
| $s$-$t$ flows (general) | Min-size identifying set | $\Sigma_2^P$-complete | $\|E\|$-approximation (hardness: factor 2) |
| Matroid bases | Min-weight identifying set | Polynomial-time | Partition matroid algorithm |
| Explicit binary list | Min-weight identifying set | NP-hard | $2\ln\|X\|$-approximation (tight) |

---

## Common Mistakes / Pitfalls

1. **Conflating identifying and controlling:** These are equivalent only for binary vectors. For integral vectors, an identifying set need not control all states.

2. **Assuming greedy approximation:** The greedy set cover analysis yields $\ln |X|$ approximation, but for identifying sets the tight bound is $2\ln|X|$. Naive greedy often underperforms on structured instances.

3. **Ignoring network structure:** In acyclic networks, the $\sqrt{m}$ bound for paths is a significant improvement over the naive $|E|$-approximation. Overlooking this wastes algorithmic potential.

4. **Verification complexity:** For general networks, verifying whether a given set is identifying is itself NP-hard—one cannot even check feasibility in polynomial time without further assumptions.

5. **Weight vs. cardinality:** Minimizing the *number* of elements (cardinality) and minimizing *weighted cost* are different problems with different hardness bounds. Always clarify which objective applies.

6. **Matroid identification pitfall:** Even though matroid bases have polynomial-time solutions, *parameterizing* which elements are in an identifying set requires understanding the matroid's connected components—not obvious without explicit matroid oracle.

---

## See Also

- [[controlling sets]]
- [[cographic matroid]]
- [[matroid basis polytope]]
- [[network flow