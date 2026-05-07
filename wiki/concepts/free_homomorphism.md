# Free Homomorphism

## Definition

A **free homomorphism** $\varphi_\circ: Z \to Z_\circ$ is a homomorphism from a dart representation $Z$ to a simplified structure $Z_\circ$ that is **universally most general** with respect to a set of identification constraints $S$. 

More precisely: $\varphi_\circ$ is free if for any other homomorphism $\varphi': Z \to Z'$ respecting the same constraints $S$, there exists a unique homomorphism $\varphi'_\circ: Z_\circ \to Z'$ such that:

$$\varphi' = \varphi'_\circ \circ \varphi_\circ$$

The image $Z_\circ$ is called the **free homomorphic image** of $Z$ respecting $S$. The terminology "free" reflects this universal property—no additional identifications are imposed beyond those logically required by $S$.

## Key Equations

For a dart $e \in Z$ and pointer function $P$, the homomorphism property requires:

$$\text{If } P(e) \neq \text{nil}, \text{ then } \varphi_\circ(P(e)) = P_\circ(\varphi_\circ(e))$$

For the **head and reversal pointers** $(P \in \{\text{head}, \text{rev}\})$:
$$P_\circ(e_\circ) = \varphi_\circ(P(e_\circ))$$

For **successor and predecessor pointers** $(P \in \{\text{succ}, \text{pred}\})$:
$$P_\circ(e_\circ) = \begin{cases} \varphi_\circ(P(e_\circ)) & \text{if } P(e_\circ) \neq \text{nil} \\ \text{nil} & \text{otherwise} \end{cases}$$

**Minimality condition:** For each dart $e_\circ \in Z_\circ$:
$$P_\circ(e_\circ) = \text{nil} \iff P(e) = \text{nil} \text{ for all } e \in Z \text{ with } \varphi_\circ(e) = e_\circ$$

## Physical Intuition / Derivation

### Construction via Identification Queues

The free homomorphism is constructed iteratively by resolving identification constraints:

1. **Initialization:** Each dart in $Z$ begins as its own equivalence class (representative root).

2. **Constraint Processing:** When a constraint $(e_1, e_2) \in S$ requires identification:
   - Merge the equivalence classes containing $e_1$ and $e_2$
   - Generate **homomorphic identification requests**: pairs of pointers that must now point to identified darts
   - Queue these requests for processing

3. **Propagation:** Processing an identification $(f, e)$ examines all pointer relationships. If $P(f) \neq \text{nil}$ and $P(e) = \text{nil}$, we must identify $P(f)$ with itself, forcing pointer consistency:
   - Queue new identifications like $(P(f), e')$ for darts $e'$ equivalent to $e$
   
4. **Termination:** Since each identification reduces the total number of representative roots, the process terminates. The final roots form $Z_\circ$, and $\varphi_\circ$ maps each dart to its root.

### Why "Free"?

The construction imposes **only the identifications logically entailed** by $S$ and the homomorphism property. Any coarser quotient (fewer identifications) would violate the homomorphism property; any finer quotient introduces unnecessary structure. This optimality is encoded in the universal factorization property above.

## Applications in Engineering

### Computational Geometry & Topological Data Structures
- **Mesh simplification**: Free homomorphisms identify topologically redundant edges/vertices while preserving structural coherence
- **Combinatorial map processing**: Quotient operations on cyclic dart orderings that must respect adjacency relationships

### Compiler Design & Symbolic Computation
- **Type unification**: Free homomorphisms model the most general unifier—the minimal substitution satisfying a set of type equations
- **Graph rewriting**: Computing the minimal quotient graph that satisfies structural constraints while preserving all necessary distinctions

### Database Schema Integration
- **Relational schema merging**: Identifying attributes/entities across heterogeneous sources requires free homomorphisms to avoid over-collapsing distinct semantic entities

### Formal Language Theory
- **Quotient automata**: Computing the coarsest bisimulation equivalence respecting observable behavior constraints

## Common Mistakes / Pitfalls

### 1. **Confusing Freeness with Triviality**
The free homomorphism is **not** the identity map. It is maximal in the sense of coarseness (fewest identifications), not minimality of structure.

### 2. **Forgetting Nil-Pointer Constraints**
The minimality condition requires that $P_\circ(e_\circ) = \text{nil}$ if and only if $P(e) = \text{nil}$ for **all** preimages. One missing pointer breaks homomorphism property.

### 3. **Over-Identifying via Naive Union-Find**
Simply merging equivalence classes without propagating pointer consistency creates invalid structures. The algorithm's queue-based approach ensures transitive closure of constraints.

### 4. **Ignoring Universal Factorization**
The free property means $\varphi_\circ$ is a **source** (initial object) in the category of homomorphisms respecting $S$. Solutions to constraint problems should factor through $\varphi_\circ$, not circumvent it.

### 5. **Assuming Pointer Values Are Preserved**
For `succ` and `pred` pointers, setting to nil is necessary. You cannot arbitrarily choose pointer targets—they are determined by the image roots under $\varphi_\circ$.

## See Also

- [[Homomorphism]] – The general mapping concept preserving structure
- [[