# Geometric Optimization

## Definition

**Geometric optimization** is an algorithmic and mathematical framework for solving online optimization problems where decisions must be made sequentially in response to requests, with costs that depend on geometric properties of the solution space. The goal is to minimize the worst-case ratio between the total cost incurred by the online algorithm and the cost of the optimal offline solution that knows all requests in advance.

In the context of the **MaxHedge algorithm**, geometric optimization specifically addresses how to position response points in a geometric domain (e.g., a plane) such that:
1. Each response point lies within a feasible region determined by the current request
2. The movement cost between consecutive response points is controlled by a target competitive ratio $\rho$
3. The algorithm remains feasible (valid) throughout the sequence of requests

## Key Equations

The optimal cost for a request sequence segment $X_i$ is given by:

$$o_i = \text{OPT}(X_i; \alpha) = |X_0 T_i| = \sqrt{\frac{s}{s-4+2i} - 4s + (1+s)^2 \sin^2(\alpha)}$$

where $s$ is a geometric parameter and $\alpha$ is an angle parameter characterizing the request geometry.

For the **MaxHedge algorithm** with competitive ratio parameter $\rho$, the response point $Z_i$ satisfies:

$$|Z_{i-1}Z_i| = \rho(o_i - o_{i-1})$$

where $Z_i$ lies on the ray from $T_i$ through $T_{i+1}$:

$$Z_i = T_i + z_i(T_{i+1} - T_i), \quad z_i \geq 0$$

Geometrically, $Z_i$ is determined as the intersection of:
- The half-line $\overrightarrow{T_i T_{i+1}}$ (direction of next request)
- A circle centered at $Z_{i-1}$ with radius $\rho(o_i - o_{i-1})$ (movement constraint)

The cumulative cost of algorithm ALG for $i$ requests is:

$$c_i = \text{ALG}(X_i; \alpha) = \sum_{j=0}^{i-1} |P_j P_{j+1}|$$

The competitive ratio is:

$$\text{Competitive Ratio} = \max_{\text{all request sequences}} \frac{\text{ALG cost}}{\text{OPT cost}}$$

## Physical Intuition / Derivation

### The Online Decision Problem

Imagine a service facility (or robotic arm) that must respond to incoming requests at different locations. The facility incurs a cost proportional to the distance traveled between requests. However, the facility operator only knows *current and past* requests, not future ones—this is the online constraint.

An offline algorithm with knowledge of all requests can plan an optimal path. An online algorithm must make greedy decisions, potentially hedging against uncertainty about future requests.

### MaxHedge Strategy

**Maximal hedging** means the algorithm positions itself as far as possible toward the next anticipated request direction while respecting a self-imposed competitive ratio bound $\rho$. 

The algorithm works as follows:

1. **Constraint**: The distance traveled in round $i$ is fixed at $\rho(o_i - o_{i-1})$, where $o_i$ is the optimal cost so far. This ensures that cumulative cost grows at a controlled rate proportional to $\rho$ times the optimal growth.

2. **Direction**: The algorithm moves along the ray toward the next request $T_{i+1}$, hedging for that direction.

3. **Geometric Construction**: The next position $Z_i$ is found by solving a circle-ray intersection problem—moving distance $\rho(o_i - o_{i-1})$ from the previous position $Z_{i-1}$ while staying on the hedge direction.

### Failure Modes

MaxHedge **fails** in round $i$ if the circle (of allowed movement) and the hedge ray do not intersect. Geometrically, this means:

- The movement budget $\rho(o_i - o_{i-1})$ is too small to reach the hedge direction from the current position, *or*
- The geometry becomes infeasible (e.g., the point drifts too far from the feasible region)

The **optimal online algorithm** is MaxHedge with the smallest $\rho$ that succeeds on all prefixes of the request sequence. This value of $\rho$ is the tight competitive ratio for that instance.

### Validity Constraint

For a valid execution, $Z_i$ must remain on the same side of the y-axis (or boundary) as $T_i$. This ensures the algorithm doesn't "wrap around" in ways that violate problem geometry. When this constraint is violated, the point is projected back to the boundary—a necessary fix that complicates analysis but only occurs in regimes irrelevant to the lower bound construction.

## Applications in Engineering

### 1. **Online Facility Location & Routing**
- Warehouses or service centers must respond to incoming customer requests without knowing future demand
- Geometric optimization determines movement strategies that minimize worst-case travel costs
- Applications: delivery routing, mobile robot path planning, emergency response coordination

### 2. **Real-Time Control Systems**
- Actuators (robotic arms, CNC machines, drones) must position themselves in response to sequential task requests
- Geometric constraints (workspace boundaries, collision avoidance) are enforced via feasible regions
- MaxHedge-like strategies minimize energy expenditure while preparing for expected next tasks

### 3. **Competitive Analysis of Algorithms**
- Analyzing the performance of online algorithms against adversarial request sequences
- Proving lower bounds on what any algorithm can achieve (no algorithm can beat MaxHedge)
- Designing algorithms with provable competitive ratio guarantees

### 4. **Motion Planning Under Uncertainty**
- Autonomous vehicles deciding how to position themselves given partial information about traffic
- Manufacturing systems responding to job orders with limited knowledge of future demand
- Hedge strategies balance immediate task completion with readiness for likely next tasks

### 5. **Financial Hedging (Theoretical Foundation)**
- Options pricing and portfolio rebalancing in uncertain markets
- The geometric framework mirrors financial decisions: commit resources (movement budget) while maintaining flexibility (staying