# Decision Tree

## Definition

A **decision tree** is a hierarchical model that represents a sequence of decisions and their consequences in a structured, tree-like format. Each node in the tree represents a decision point (internal node) or an outcome (leaf node), and each edge represents the result of a decision or a random event.

In the context of adaptive optimization problems (such as the stochastic knapsack problem), a decision tree formally encodes:
- **Root**: The initial state before any decisions
- **Internal nodes**: Decision points where an algorithm chooses an action based on information revealed so far
- **Edges**: Transitions labeled with outcomes (e.g., item sizes, capacities)
- **Leaves**: Terminal states representing completed packing or failure (overflow)

A **root-to-leaf path** traces one complete execution trajectory through the tree, representing one possible sequence of decisions and random outcomes.

## Key Equations

For an instance $I$ with an optimal adaptive policy $\sigma_{\text{AD}}$, the **adaptivity gap** is defined as:

$$G(I) = \frac{\text{ADAPT}(I)}{\text{ALG}(I)}$$

where:
- $\text{ADAPT}(I)$ = expected value achieved by an optimal adaptive policy
- $\text{ALG}(I)$ = expected value achieved by an optimal non-adaptive (fixed-order) policy

The semi-adaptivity gap for $k$ adaptive decision points is:

$$G_k(I) = \frac{\text{ADAPT}(I)}{\text{ALG}_k(I)}$$

For the Risky Stochastic Knapsack problem restricted to the $H_2$ family of instances:

$$G(H_2) = 1 + \ln(2) \approx 1.69$$

## Physical Intuition / Derivation

### Why Decision Trees Matter in Adaptive Optimization

In problems like stochastic knapsack packing, an **adaptive policy** exploits information revealed during execution:

1. Insert item 0 → observe its stochastic size $S_0$
2. If $S_0 \leq B_{\text{remaining}}$, decide which item to insert next based on $S_0$'s outcome
3. Continue adapting decisions to revealed information

A **non-adaptive policy** commits to a fixed insertion order before any sizes are observed.

The decision tree visualizes this hierarchy:
- At each internal node, the algorithm branches based on an observed random outcome (e.g., whether $S_0 > 1$)
- Paths through the tree represent different outcomes; different paths may follow different item orderings
- Leaf nodes show final packing outcomes

### Path Equivalence Under Instance Transformations

The source material proves that for any root-to-leaf path in an adaptive decision tree for instance $I$:
- The accumulated item sizes and values remain **unchanged** when compound items (groups of original items) are substituted
- This ensures that capacity distributions at decision points are preserved
- Therefore, the adaptivity gap is preserved under certain transformations

This allows researchers to **simplify the instance family** while maintaining the worst-case gap:

$$\sup_{I \in H_2} G(I) = \sup_{I' \in H'_2} G(I')$$

where $H'_2 \subset H_2$ is a restricted subfamily with simpler structure.

## Applications in Engineering

### 1. **Online Bin Packing and Resource Allocation**
Decision trees model real-time scheduling where job sizes or resource requirements are revealed sequentially. Adaptive algorithms reorder job insertion based on observed sizes, improving packing efficiency.

### 2. **Stochastic Inventory and Knapsack Problems**
In supply chain optimization, item weights/costs are uncertain until received. Decision trees encode adaptive policies for weight-capacity-constrained vehicles or warehouses.

### 3. **Machine Learning: Classification and Regression**
Decision trees partition feature space at each node based on observed feature values, building a hierarchy of decisions. Each path from root to leaf defines a classification rule or regression prediction.

### 4. **Fault Diagnosis and Testing**
In system troubleshooting, decision trees model sequential testing: observe a symptom, branch to next test based on outcome, leading to diagnosis (leaf).

### 5. **Game Theory and Decision Analysis**
Game trees (specialized decision trees) represent move sequences in multi-agent systems, where each node is a decision point for one player.

## Common Mistakes / Pitfalls

### 1. **Confusing Adaptive and Non-Adaptive Policies**
❌ *Mistake*: Assuming all polynomial-time algorithms are adaptive.  
✓ *Correct*: Non-adaptive policies fix a decision (e.g., item order) *before* any randomness is resolved. Adaptive policies observe outcomes and adjust.

### 2. **Overcounting Decision Points**
❌ *Mistake*: Treating every random event as a decision point.  
✓ *Correct*: A decision tree node represents only points where the algorithm *makes a choice* (not passive observation of uncontrollable randomness).

### 3. **Ignoring Path Dependencies**
❌ *Mistake*: Analyzing each path independently without checking consistency across the full tree.  
✓ *Correct*: Tree constraints (like disjointness of item sets in compound items) ensure valid policies at all paths simultaneously.

### 4. **Confusing Adaptivity Gap with Approximation Ratio**
❌ *Mistake*: Thinking adaptivity gap measures distance from optimal (it doesn't).  
✓ *Correct*: Gap $G(I) = \frac{\text{OPT}_{\text{adaptive}}}{\text{OPT}_{\text{non-adaptive}}}$ measures the *advantage* of adaptivity, which can be $> 1$.

### 5. **Assuming All Instances are Equally Hard**
❌ *Mistake*: Using worst-case gap over all instances without considering restricted families.  
✓ *Correct*: Lemma 6 shows the semi-adaptivity gap (for $k$ decisions) is achieved on specific subfamily $H_k$, requiring careful construction.

## See Also

- [[Stochastic Knapsack Problem]] – primary application domain
- [[Adaptive Policy]] – the algorithm framework encoded by decision trees
- [[Non-Adaptive Policy]] – baseline for measuring adaptivity gaps
- [[