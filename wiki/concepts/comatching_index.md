# Comatching Index

## Definition

The **ε-comatching index** of a planar metric $(V, \text{dist})$ is the maximum cardinality of an **ε-comatching**—a set of terminal pairs $M = \{(p_1, q_1), \ldots, (p_L, q_L)\}$ in a planar graph $G$ where:

1. Each pair $(p_i, q_i)$ must be connected by a path in $G$
2. For any two distinct pairs $(p_i, q_i)$ and $(p_j, q_j)$, the "cross-distance" constraint holds:
   $$\max(\text{dist}(p_i, q_j), \text{dist}(p_j, q_i)) \leq (1-\varepsilon) \cdot \min(\text{dist}(p_i, q_i), \text{dist}(p_j, q_j))$$

This is a **metric parameter** quantifying how many "non-interfering" terminal pairs can simultaneously exist in a planar metric space for a given approximation parameter $\varepsilon \in (0,1)$.

The comatching index is formally bounded by a polynomial in $\varepsilon^{-1}$:

$$\text{CoMatch}_\text{planar}(\varepsilon) \leq L_\text{planar}(1/\varepsilon)$$

for some polynomial $L_\text{planar}$.

## Key Equations

**Cross-distance constraint** for a valid ε-comatching:
$$\text{dist}(p_i, q_j) \leq (1-\varepsilon) R, \quad \text{dist}(p_j, q_i) \leq (1-\varepsilon) R$$
where $R = \min_{(p,q) \in M} \text{dist}(p,q)$ is the minimum pair distance.

**Distance scaling unit** (local scale parameter):
$$\delta := \frac{\varepsilon}{100R}$$

**Rounded distance profile**: For vertices $u,v \in V(G)$, the discrete distance is:
$$d_\text{dist}(u,v) = \text{unique integer } i \text{ such that } i \cdot \delta \leq \text{dist}_G(u,v) < (i+1)\delta$$

**Separation lemma** (Corollary 5.6): If set $X$ is contained in union of $\alpha$ paths each of length $\leq \beta R$, the number of separated pairs is:
$$N_\text{sep}(X) = O(\alpha^4 \varepsilon^{-4}(1 + \beta\varepsilon^{-1})^4)$$

**Theorem 1.5 (Main Result)**: Maximum ε-comatching size in a clean planar metric instance:
$$L(\varepsilon) = O(\varepsilon^{-332} \log^{72}(\varepsilon^{-1}))$$

achieved through composition of three lemmas bounding reductions: local instances ($O(L_\text{local}^9 \varepsilon^{-8})$), linked non-crossing instances ($O(L_\text{linked}^{18} \log^{72} L_\text{linked} \cdot \varepsilon^{-80})$), and finally topological bounds ($O(\varepsilon^{-14})$).

## Physical Intuition / Derivation

### Why This Matters

The comatching index measures a fundamental **separation property** of planar metrics. Intuitively, it answers: *"How many disjoint routing problems can coexist in a planar network before they must interfere?"*

In a planar metric:
- Pairs in a comatching are "sparse" in the sense that routing one pair should not significantly constrain routing another
- The cross-distance constraint ensures pairs are either far apart or have similar internal distances (preventing "entanglement")
- Unlike general metrics, planarity imposes topological rigidity that bounds this interference polynomially

### Hierarchical Proof Strategy

The main theorem reduces through three increasingly controlled geometric classes:

1. **General planar instances** → **Local instances** (Lemma 5.1)
   - A local instance has terminal pairs clustered so paths remain relatively short
   - The reduction uses a function $\Lambda$ that iteratively removes pairs lying on different faces of the remaining graph

2. **Local instances** → **Linked non-crossing instances** (Lemma 5.2)
   - Non-crossing: no two paths $\gamma_i, \gamma_j$ intersect in $G$ itself
   - Linked: paths remain connected in a controlled way
   - This introduces the $\log^8 L$ factor: planar duality forces logarithmic structure

3. **Linked non-crossing instances** → **Topological bound** (Lemma 5.3)
   - Pure topological analysis of path families in the plane
   - Yields polynomial bound $\varepsilon^{-14}$ independent of instance size
   - Uses distance profile discretization to reduce infinite metric to discrete graph structure

### Distance Profiles as Discretization

The key technical tool is **rounded distance profiles**: by quantizing distances into units of $\delta = \varepsilon/(100R)$, the continuous metric reduces to a finite combinatorial object. Lemma 5.5 shows only $O(|Z|^4 \varepsilon^{-4})$ distinct profiles exist for any reference set $Z$. This finite discretization is what enables polynomial bounds.

## Applications in Engineering

### Network Routing and Resilience
- **Optical/transport networks**: Determines maximum number of independent fail-safe routing demands in a planar network topology; crucial for designing fault-tolerant circuits
- **Road networks**: Bounds on comatching index directly constrain multi-commodity flow problems in planar urban/regional transport systems

### VLSI Layout and Physical Design
- **Chip floorplanning**: Planar metrics model substrate constraints; comatching index quantifies how many signal paths can route independently without excessive congestion
- **Wire routing**: Bounds the complexity of simultaneous routing of multiple nets in 2D