# edge-capacitated setting

## Definition

The **edge-capacitated setting** is a network flow problem variant where capacity constraints are imposed on the edges of a directed graph, rather than (or in addition to) on the nodes. In this setting:

- Each edge $e$ in a directed graph $G = (V, E)$ has an associated **capacity** $c(e) \geq 0$
- The maximum flow on any edge cannot exceed its capacity
- Flows must satisfy flow conservation at all intermediate nodes
- The edge-capacitated setting contrasts with the **vertex-capacitated setting**, where capacity limits apply to nodes instead

Formally, for a directed graph with source $s$ and sink $t$, a feasible flow $f$ must satisfy:

$$f(e) \leq c(e) \quad \forall e \in E$$

along with flow conservation constraints at each node except $s$ and $t$.

## Key Equations

**Flow Conservation:**
$$\sum_{e \text{ entering } v} f(e) = \sum_{e \text{ leaving } v} f(e) \quad \forall v \in V \setminus \{s,t\}$$

**Maximum Flow (Ford-Fulkerson):**
$$\text{Max Flow} = \min_{\text{cuts}} \text{(Minimum Cut Capacity)}$$

**Flow-Cut Gap Bound (parametrized by weight $W$):**
$$\text{flow-cut gap} = O(W^c)$$

where $W$ is the total weight of all edges in the graph and $c$ is a constant depending on the problem structure.

## Physical Intuition / Derivation

### Why Edge Capacities Matter

In practical systems, capacity constraints on edges (links, pipes, cables) are often more natural than constraints on nodes:

- **Communication networks:** Each link between routers has a bandwidth limit
- **Fluid transport:** Pipes have diameter-dependent flow limits independent of junction constraints
- **Road networks:** Highway segments have throughput limits (edges) distinct from intersection processing capacity (nodes)

### Flow-Cut Gap Intuition

The **flow-cut gap** measures how efficiently a fractional relaxation approximates integral flow solutions. In the edge-capacitated setting:

1. **Fractional flows** allow flow to split arbitrarily across paths (linear programming relaxation)
2. **Integral flows** must route flow along whole unit quantities (combinatorial problem)
3. The gap quantifies the worst-case ratio: $\frac{\text{fractional optimal}}{\text{integral optimal}}$

#### Parametrization by $W$ (not $n$)

The source material emphasizes parametrizing by total weight $W$ rather than node count $n$ because:

- **Invariance to irrelevant structure:** Isolated nodes or unreachable components don't affect connectivity but inflate $n$
- **True hardness reflection:** $W$ captures the actual complexity imposed by edge constraints
- **Better bounds:** For some problem classes, $O(W^c)$ gaps can be proven, whereas $O(n^c)$ may be loose

**Reduction from $W$-bounded to $n$-bounded:** If vertex flow-cut gap is $O(W^c)$, then it is also $O(n^{\frac{c}{1+c}})$ via preprocessing that "cuts" high-weight nodes. This explains the hierarchy: bounds on $W$ are stronger.

## Applications in Engineering

### Network Routing & Load Balancing
- **Telecommunications:** Computing maximum throughput between network nodes with link bandwidth constraints
- **Data center networking:** Ensuring fair flow distribution respecting switch port capacities
- **Content delivery:** Routing traffic to respect edge capacity limits on backbone links

### Transportation & Logistics
- **Traffic flow optimization:** Modeling vehicle flow on highway segments with capacity limits
- **Supply chain networks:** Routing goods through distribution networks where edges (shipping routes) have fixed throughput
- **Urban transit:** Balancing passenger flow across limited-capacity transit corridors

### Fluid & Thermal Systems
- **Pipeline networks:** Computing steady-state flow rates with pipe diameter constraints
- **HVAC systems:** Air distribution with duct capacity limits
- **Cooling networks:** Thermal fluid circulation respecting pipe throughput

### Resource Allocation
- **Cloud computing:** Task scheduling with link capacity constraints between servers
- **Power grids:** Optimizing electricity flow subject to transmission line capacities
- **Water distribution:** Municipal networks with pipe capacity constraints

## Common Mistakes / Pitfalls

### 1. **Confusing Node and Edge Capacities**
Mistake: Assuming that high node capacity automatically allows high edge flow.
- **Reality:** A node can have infinite capacity but be bottlenecked by incident edges
- **Fix:** Carefully identify where constraints apply in the problem formulation

### 2. **Ignoring Flow Conservation**
Mistake: Solving for flows without enforcing conservation at intermediate nodes.
- **Reality:** Flow "disappears" at intermediate nodes violates physical laws
- **Fix:** Always include $\sum_{\text{in}} f = \sum_{\text{out}}$ for all non-source/sink nodes

### 3. **Assuming Integral = Fractional**
Mistake: Using LP relaxation solution as if it were integral feasible.
- **Reality:** Fractional flows may not decompose into path flows respecting integrality
- **Fix:** Apply rounding techniques and account for the flow-cut gap

### 4. **Misapplying $W$ vs $n$ Parametrization**
Mistake: Using an $O(n)$ bound when an $O(W)$ bound is available and tighter.
- **Reality:** $W$ eliminates dependency on irrelevant structure
- **Fix:** Check whether parametrization by total capacity/weight is available

### 5. **Overlooking Negative-Capacity Edges**
Mistake: Assuming all capacities are positive.
- **Reality:** Some formulations allow reverse flows; only non-negative capacities are standard
- **Fix:** Verify capacity sign conventions in the specific problem context

## See Also

- [[vertex-capacitated setting]] — dual formulation with node capacity constraints
- [[flow-cut gap]] — fundamental ratio between fractional and integral flow optimal values
- [[maximum flow problem]] — classical polynomial-time solvable flow optimization
- [[multi-commodity flow]] — extension to multiple source-sink pairs with shared edges
- [[minimum cut]] — dual problem determining maximum flow by cut minimization

##