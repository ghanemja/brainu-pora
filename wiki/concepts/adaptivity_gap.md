# Adaptivity Gap

## Definition

The **adaptivity gap** is a measure of the performance loss incurred by restricting a decision-maker to non-adaptive (static) policies compared to fully adaptive policies that can make decisions based on observed outcomes.

Formally, for an optimization problem instance $I$, the adaptivity gap is defined as:

$$G(I) = \frac{\text{ADAPT}(I)}{\text{ALG}(I)}$$

where:
- $\text{ADAPT}(I)$ = optimal value achievable by an **adaptive policy** (one that observes random outcomes and adjusts decisions dynamically)
- $\text{ALG}(I)$ = optimal value achievable by a **non-adaptive policy** (a fixed sequence of decisions determined in advance)

The **family adaptivity gap** $G(\mathcal{F})$ for a problem class $\mathcal{F}$ is:

$$G(\mathcal{F}) = \sup_{I \in \mathcal{F}} G(I)$$

This represents the worst-case ratio over all instances in that class.

---

## Key Equations

**Adaptivity gap composition** (for $k$-adaptive policies):

$$G(I'_T) = \frac{\text{ADAPT}(I'_T)}{\text{ALG}(I'_T)} \geq \frac{\text{ADAPT}(I)}{\text{ALG}(I)} = G_k(I)$$

where $I'_T$ denotes the transformed instance with tree constraints and $G_k(I)$ is the $k$-adaptivity gap.

**For Risky Stochastic Knapsack (Risky-SK):**

$$G(H_2) = G(H^T_2) = 1 + \ln(2) \approx 1.693$$

This shows the adaptivity gap for a key problem family is exactly $1 + \ln(2)$, with or without tree constraints.

---

## Physical Intuition / Derivation

### Why Adaptivity Creates a Gap

Consider a decision-maker facing a stochastic knapsack problem:

1. **Non-adaptive policy**: Must commit to a sequence of items *before* observing any outcomes (e.g., sizes). If initial items are large, the knapsack fills quickly and valuable later items cannot be added.

2. **Adaptive policy**: Observes the actual size of each inserted item before deciding what to insert next. If an item is smaller than expected, the decision-maker can insert more; if larger, they can substitute.

The gap arises because:
- **Adaptive strategies** can route around bad outcomes (small probability events that consume capacity)
- **Non-adaptive strategies** must hedge against all scenarios simultaneously, leading to conservative item selection

### Instance Construction (Risky-SK Example)

The source material demonstrates how to find worst-case instances:

1. Start with instance $I$ with $n+1$ items (indexed 0, 1, ..., n)
2. Item 0 has deterministic value $v_0 = 1$ but random size $S_0$ with $\Pr(S_0 > 1) = p_0$
3. Items $i \geq 1$ have deterministic values $v_i$ (ordered $v_1 \geq v_2 \geq \cdots$) and size distributions
4. An optimal adaptive policy chooses item 0 first, then **conditionally** selects among items $\{1, \ldots, n\}$ based on whether $S_0 \leq 1$

The adaptive tree naturally partitions decisions:
- Path 1: If $S_0 > 1$ (probability $p_0$), insert remaining items from subset
- Path 2: If $S_0 \leq 1$ (probability $1-p_0$), insert different items

Non-adaptive policies cannot make this conditional choice—they must commit upfront.

### Progressive Refinement to Worst Case

The methodology in the source narrows down from all instances in family $H_2$ to a structured subfamily $H'_2 \subseteq H_2$ by:
- **Lemma 7 (Step 1)**: Ruling out instances whose size distributions are unnecessarily complex
- **Iterative elimination**: Each transformation preserves (up to $\varepsilon$) the adaptivity gap while removing instances that cannot achieve maximum gap

This creates a *canonical worst-case family* that is analytically tractable yet tight.

---

## Applications in Engineering

### 1. **Supply Chain & Inventory Management**
- Compare value of **real-time demand observation** vs. **pre-committed purchasing decisions**
- Quantify ROI of demand-sensing systems that enable adaptive restocking

### 2. **Resource Allocation under Uncertainty**
- **Cloud computing**: Adaptive job scheduling (observe task sizes, reorder queue) vs. static schedules
- **Network routing**: Adaptively reroute packets (observe congestion) vs. fixed routing tables
- Gap guides investment in monitoring/sensing infrastructure

### 3. **Portfolio Optimization**
- Adaptive rebalancing (observe returns, adjust weights) vs. buy-and-hold strategies
- Adaptivity gap indicates how much value active management can capture

### 4. **Scheduling & Project Management**
- Adaptive task ordering (observe completion times, prioritize remaining tasks) vs. static Gantt charts
- Predicts value of flexible project execution vs. rigid plans

### 5. **Robotics & Control**
- Feedforward control (non-adaptive) vs. feedback control (adaptive)
- Adaptivity gap characterizes performance loss from removing sensors/feedback

### 6. **Mechanism Design**
- Comparing **sequential revelation mechanisms** (adaptive information release) to **simultaneous-move games**
- Gap bounds welfare loss from commitment to fixed auction formats

---

## Common Mistakes / Pitfalls

### 1. **Confusing Adaptivity Gap with Approximation Ratio**
- **Wrong**: "An approximation ratio of 2 means adaptivity gap is 2"
- **Right**: Adaptivity gap compares two optimal policies (adaptive vs. non-adaptive), while approximation ratio compares algorithm to optimal. They measure different things.

### 2. **Assuming Adaptivity Always Helps**
- **Mistake**: Thinking adaptivity gap is always > 