# Homomorphic Image

## Definition

A **homomorphic image** is the result of applying a homomorphism to an algebraic structure, producing a new structure that preserves the essential relational properties of the original while potentially simplifying or collapsing its complexity.

More formally, given a structure $(Z, \delta)$ (where $Z$ is a set and $\delta$ represents structural relations or operations) and a homomorphism $\varphi: (Z, \delta) \to (Z', \delta')$, the **homomorphic image** is the structure $(Z', \delta')$ that satisfies:

$$\varphi(\delta(a, b)) = \delta'(\varphi(a), \varphi(b))$$

for all relevant operations or relations $\delta$.

### Free Homomorphic Image

A **free homomorphic image** $(Z^\circ, \delta^\circ)$ respecting a set of constraints $S$ is the most general homomorphic image satisfying those constraints. It is universal in the sense that any other homomorphic image respecting $S$ can be obtained via a homomorphism from $(Z^\circ, \delta^\circ)$:

$$\varphi^\circ_1: (Z^\circ, \delta^\circ) \to (Z_1, \delta_1)$$

such that $\varphi^\circ_1 \circ \varphi^\circ = \varphi_1$.

## Key Equations

**Universal Property of Free Homomorphic Image:**

For any homomorphism $\varphi_1: (Z, \delta) \to (Z_1, \delta_1)$ respecting constraint set $S$, there exists a unique homomorphism:

$$\varphi^\circ_1 = \text{unique factorization such that } \varphi_1 = \varphi^\circ_1 \circ \varphi^\circ$$

**Identification Under Homomorphism:**

Given identification requests $\{(e_i, f_i)\}_{i=1}^k$, the free homomorphic image satisfies:

$$\varphi^\circ(e_i) = \varphi^\circ(f_i) \quad \forall i = 1, \ldots, k$$

while minimizing additional identifications beyond those forced by these constraints.

## Physical Intuition / Derivation

### Building the Concept

A homomorphic image captures the idea of **"what survives" when we apply a structure-preserving map**. 

Consider a concrete example: 
- Original structure: a geometric triangulation $Z$ with discharging rules $\delta$ (charge distribution across vertices and edges)
- Homomorphism: an embedding $\varphi$ placing the triangulation into a larger context
- Homomorphic image: the resulting triangulation retains the charge-flow properties

The **free homomorphic image** addresses the inverse problem: given certain mandatory identifications (e.g., "vertex $a$ must map to the same place as vertex $b$"), what is the *smallest* structure we must create?

### Iterative Construction

The source material describes an iterative algorithm using **union-find** data structures:

1. **Initialize:** Place all identification requests in a queue
2. **Iterate:** Process each identification $(e_i, f_i)$ by unifying their equivalence classes
3. **Propagate:** When unifying two elements, recursively unify any related elements (through operations in $\delta$) to maintain homomorphism properties
4. **Terminate:** When the queue empties, the roots of the union-find forest become the vertices and darts of $Z^\circ$

This construction guarantees minimality: no unnecessary identifications are performed.

## Applications in Engineering

### 1. **Graph and Network Optimization**
- Reducing circuit complexity by identifying equivalent nodes while preserving electrical properties
- Condensing state machines by merging behaviorally equivalent states
- **Application:** Finite state automata minimization in digital logic design

### 2. **Triangulation-Based Methods** (as shown in source material)
- Discharging rule analysis: proving properties like 4-colorability in planar graphs
- Combining multiple local rules into a single unified rule respecting identification constraints
- **Application:** Automated verification of graph coloring properties in compiler register allocation

### 3. **Algebraic Structures in Cryptography**
- Quotient groups and rings used in elliptic curve cryptography
- Identifying plaintext elements modulo encryption operations
- **Application:** Homomorphic encryption schemes (fully homomorphic encryption, partially homomorphic encryption)

### 4. **Model Reduction in Control Theory**
- Reducing high-dimensional system descriptions while preserving input-output relationships
- Creating simplified equivalent models for analysis
- **Application:** Balanced truncation, Krylov subspace methods

### 5. **Configuration Space Simplification**
- In robotics and mechanism design: reducing degrees of freedom via constraint identifications
- **Application:** Synthesis of linkage mechanisms with prescribed motion properties

## Common Mistakes / Pitfalls

1. **Confusing homomorphic images with isomorphic structures**
   - A homomorphic image need not be one-to-one; information *can* be lost
   - Isomorphic structures preserve cardinality and injectivity; homomorphic images do not

2. **Assuming minimality without verification**
   - Not all homomorphic images satisfying constraints are *free* (universal)
   - Free homomorphic images minimize identifications beyond those required by constraints
   - Failing to account for transitive closures of identifications

3. **Ignoring the difference between constructive and existential approaches**
   - Knowing a free homomorphic image exists (existential) is different from computing it
   - The union-find algorithm provides an explicit construction—naive equivalence methods may miss identifications implied by $\delta$

4. **Over-constraining during identification**
   - Identifying elements beyond the stated identification requests can destroy optimality
   - The free homomorphic image respects requests but adds *no extraneous* identifications

5. **Failing to preserve structure through identifications**
   - When identifying darts/vertices, all related structural elements must be consistently identified
   - Partial identifications that don't respect the homomorphism property are invalid

## See Also

- [[Homomorphism]] — the structure