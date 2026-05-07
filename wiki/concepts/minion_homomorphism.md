# minion homomorphism

## Definition

A **minion homomorphism** is a family of functions that establishes a structure-preserving map between two minions. Formally, given two minions $R$ and $S$, a minion homomorphism $\xi$ consists of a collection of functions:

$$\xi(D) : R(D) \to S(D)$$

for every finite set $D$, such that these functions **commute with all lifted operations**. That is, for every function $\alpha : D \to E$, the following diagram commutes:

$$\begin{array}{ccc}
R(D) & \xrightarrow{\xi(D)} & S(D) \\
\downarrow R(\alpha) & & \downarrow S(\alpha) \\
R(E) & \xrightarrow{\xi(E)} & S(E)
\end{array}$$

This ensures that $\xi(E) \circ R(\alpha) = S(\alpha) \circ \xi(D)$.

In other words, a minion homomorphism is a **natural transformation** between minion functors that respects the relaxation structure.

---

## Key Equations

**Commutativity condition** (defining property of minion homomorphism):
$$\xi(E) \circ R(\alpha) = S(\alpha) \circ \xi(D) \quad \forall \alpha : D \to E$$

**Relaxation correspondence**:
If $\xi : R \to S$ is a minion homomorphism and $D$ is an LC instance, then:
- The $R$-relaxation of $D$ has a solution $\Rightarrow$ The $S$-relaxation of $D$ has a solution

This is expressed via the pushforward of solutions along $\xi$.

---

## Physical Intuition / Derivation

### Hierarchical Relaxations

A minion homomorphism formalizes the intuitive notion that some relaxations are "coarser" or "stronger" than others. For example:

- **Weaker relaxation (more expressive)**: BLP (linear programming over probability distributions) can model more constraint behaviors than AC (subsets).
- **Stronger relaxation (more restrictive)**: When we have a homomorphism $\xi : \text{BLP} \to \text{AC}$, solutions to AC are also solutions to BLP, but not vice versa.

### Construction Flow

Consider the transition from **BLP to AC**:

1. In BLP, $R(D)$ consists of probability distributions: functions $f : D \to [0,1]$ with $\sum_{a \in D} f(a) = 1$
2. In AC, $S(D)$ consists of nonempty subsets of $D$
3. The homomorphism $\xi(D)$ maps each probability distribution $f$ to its **support set**: $\xi(D)(f) = \{a \in D : f(a) > 0\}$

This mapping respects the constraint structure: if $\alpha : D \to E$, then the support of $R(\alpha)(f)$ (which extends $f$ along $\alpha$) equals the $\alpha$-image of the support of $f$, which is $S(\alpha)(\xi(D)(f))$.

### Higher-Level Insight

The source material introduces **$k$-th level minion homomorphisms** ($\text{lvl}_k R$), which generalize relaxations to capture correlations among $k$-tuples of variables rather than individual points. The key insight is that:

$$\text{R-relaxation of } \text{pow}^k D \text{ is solvable} \iff \text{lvl}^k R\text{-relaxation of } D \text{ is solvable}$$

This allows a single minion structure to encode multi-variable constraint information through the saturated power construction.

---

## Applications in Engineering

### 1. **Constraint Satisfaction & Algorithms**
   - Minion homomorphisms organize a hierarchy of approximate solvers (AC $\to$ BLP $\to$ SDP)
   - Engineers choose solver strength based on problem hardness and available computational budget
   - Example: Network flow with probabilistic constraints uses BLP; deterministic AC suffices for simple feasibility checks

### 2. **Promise Constraint Satisfaction Problems (Promise CSPs)**
   - Minion homomorphisms directly characterize which relaxations distinguish between satisfiable and unsatisfiable instances
   - Critical for approximation algorithms in scheduling, resource allocation, and graph coloring
   - The homomorphism structure predicts algorithm performance across different problem classes

### 3. **Linear & Semidefinite Programming**
   - SDP relaxations of combinatorial problems are structured as minion homomorphisms from more fine-grained relaxations
   - Applications: MAX-CUT, graph partitioning, sensor localization
   - Minion homomorphisms explain why SDP solutions project onto valid LP solutions

### 4. **Machine Learning / Probabilistic Inference**
   - BLP minions model belief propagation and probabilistic inference algorithms
   - Homomorphisms between different inference schemes (BP $\to$ mean-field) provide theoretical guarantees
   - Used in loopy belief propagation analysis

### 5. **Verification & Formal Methods**
   - Minion homomorphisms structure abstract interpretation hierarchies
   - Different abstractions (interval analysis, polyhedra, octagons) form chains via minion homomorphisms
   - Engineers select abstraction coarseness balancing precision and verification time

---

## Common Mistakes / Pitfalls

1. **Confusing directionality**: A homomorphism $\xi : R \to S$ means $R$ is more refined/expressive than $S$. Solutions in $S$ lifts to $R$, not vice versa. Students often reverse this.

2. **Assuming all relaxations form a total order**: Not every pair of minions has a homomorphism between them. AC and SDP are *incomparable*—neither strictly relaxes the other. They capture different constraint structures.

3. **Ignoring functoriality requirements**: Minions must preserve function composition and identities. A "relaxation" that doesn't is not a valid minion and won't satisfy the theoretical guarantees.

4. **Misapplying