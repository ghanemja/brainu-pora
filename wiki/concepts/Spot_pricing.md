# Spot Pricing

## Definition

**Spot pricing** is a dynamic pricing mechanism that determines the cost of a commodity or service for immediate or near-immediate delivery based on current market conditions, supply-demand balance, and real-time availability. In contrast to long-term contracts with fixed or negotiated rates, spot pricing reflects instantaneous market equilibrium.

In the context of freight markets, spot pricing determines the price offered to carriers for executing individual truckload movements (loads) on a short-term basis, without prior capacity commitment. The spot price must balance:
- **Supply-side constraints**: available carrier capacity at that moment
- **Demand-side pressures**: urgent shipper requirements
- **Opportunity costs**: value of committing capacity to this load vs. alternative uses
- **Committed capacity**: existing long-term contracts that constrain available spot capacity

## Key Equations

For a freight marketplace coordinating contract and spot supply, the fundamental optimization problem is:

$$\min_{x, y} \sum_{t=1}^{T} \left[ C_t(x_t) + P_t^{\text{spot}}(y_t) \cdot y_t \right]$$

**Subject to:**
$$x_t + y_t \leq D_t \quad \text{(capacity constraint)}$$
$$y_t \geq 0, \quad x_t \leq X_t^{\text{contract}} \quad \text{(contract allocation)}$$

**Where:**
- $x_t$ = demand fulfilled by long-term contracts at time $t$
- $y_t$ = demand fulfilled by spot market at time $t$
- $D_t$ = total demand at time $t$
- $C_t(x_t)$ = cost of contract supply (typically fixed or piecewise linear)
- $P_t^{\text{spot}}(y_t)$ = spot price function (typically increasing in $y_t$)
- $X_t^{\text{contract}}$ = contracted capacity available at time $t$

The **shadow price** $\lambda_t$ at each time period represents the marginal value of one additional unit of capacity:

$$\lambda_t = \frac{\partial}{\partial X} \text{(optimal total cost)} \bigg|_{X=X_t}$$

This shadow price should be incorporated into the spot price to avoid wasteful over-allocation:

$$P_t^{\text{spot}} = f_t(y_t) + \lambda_t$$

where $f_t(y_t)$ represents the intrinsic spot market price (e.g., from competitive bidding).

## Physical Intuition / Derivation

### Why Coordination Matters

Consider a freight marketplace with both:
1. **Contract supply**: carriers committed to move loads at pre-negotiated fixed rates
2. **Spot supply**: carriers willing to move loads at prices determined by real-time supply-demand

**The coordination problem**: If the marketplace operator prices spot loads without considering contracted capacity, two pathologies emerge:

**Pathology 1 – Underpricing spot loads:** 
- The operator might offer a spot load at market rate $P_{\text{baseline}}$
- But if that load could have been served by contracted capacity, the true marginal cost is merely the contract rate (already paid)
- This leaves money on the table; some shippers willing to pay more than $P_{\text{baseline}}$ could absorb higher prices

**Pathology 2 – Overpricing and stranding capacity:**
- The operator might price a spot load too high, deterring demand
- Meanwhile, contracted capacity sits idle because it's reserved but not allocated
- The total system cost rises from both unused contract capacity and lost spot transactions

### Shadow Price Mechanics

The optimal solution recognizes that **committed contract capacity has an implicit value**. When contract capacity is scarce (demand exceeds total capacity), using one unit on a mediocre load prevents serving a high-value load later. The shadow price $\lambda_t$ quantifies this opportunity cost.

**Derivation sketch:**
Using dynamic programming, at each time step the value function is:

$$V_t(C) = \min_{y_t} \left\{ P_t^{\text{spot}}(y_t) \cdot y_t + \mathbb{E}[V_{t+1}(C - \min(D_t, X_t^{\text{contract}} + y_t))] \right\}$$

where $C$ is available capacity. The shadow price is $\lambda_t = -\frac{\partial V_t}{\partial C}$, representing how much the total cost increases per unit of capacity lost. The optimal spot price becomes:

$$P_t^{\text{spot,optimal}} = \lambda_t + \text{(competitive market rate)}$$

This ensures that high-value demands are fulfilled first, and contracted capacity is allocated efficiently across time.

### Algorithm: Dual Frank-Wolfe

The paper proposes a **Dual Frank-Wolfe algorithm** that iteratively:
1. Computes candidate shadow prices $\{\lambda_t\}$ using dual optimization
2. Runs spot pricing with these shadow prices injected
3. Observes realized demand and cost outcomes
4. Updates shadow prices to reduce regret

This approach is modular—it only requires "oracle access" to any spot-pricing protocol (e.g., sealed-bid auction, dynamic matching), making it agnostic to the marketplace's internal mechanism.

## Applications in Engineering

### 1. **Freight & Logistics Marketplaces**
- **Digital freight platforms** (e.g., Amazon's Middle Mile, Convoy, Flexport) use spot pricing alongside contracts to balance cost and service level
- Spot pricing signals excess demand to potential carriers, attracting additional supply dynamically
- Shadow prices ensure that contract capacity is not wasted on low-value routes

### 2. **Energy Markets**
- **Electricity spot markets** (e.g., ISO/RTO markets in the US) price power based on instantaneous supply-demand balance
- Long-term power purchase agreements (contracts) coexist with day-ahead and real-time spot prices
- Shadow pricing determines marginal costs, guiding resource dispatch and investment

### 3. **Cloud Computing & Capacity Markets**
- **Reserved instances** (contracts, e.g., AWS Reserved Instances) offer discounted rates for committed capacity
- **Spot instances** (e.g., AWS EC2 Spot) are priced dynamically