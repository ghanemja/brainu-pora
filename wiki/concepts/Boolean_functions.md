# Boolean functions

## Definition

A **Boolean function** is a function $f: \{0,1\}^n \to \{0,1\}$ (or equivalently $f: \{\pm 1\}^n \to \{\pm 1\}$) that maps $n$ binary input variables to a single binary output.

More generally, a Boolean function can be represented as any mapping from binary assignments to truth values, where the input space consists of all possible combinations of $n$ binary variables.

### Orthogonal Disjunctive Normal Form (Orthogonal DNF)

A Boolean function $\varphi$ is in **orthogonal disjunctive normal form** if it can be expressed as a disjunction of terms:

$$\varphi = T_1 \vee T_2 \vee \cdots \vee T_m$$

where for every pair of distinct terms $T_i$ and $T_j$ (with $i \neq j$):

$$T_i \wedge T_j \models \bot$$

**Interpretation**: No single variable assignment can simultaneously satisfy more than one term. The terms form mutually exclusive (disjoint) sets of satisfying assignments. This property makes orthogonal DNFs particularly useful for efficient computation and analysis, as the contribution of each term can be evaluated independently.

## Key Equations

### Standard DNF Representation
A Boolean function in disjunctive normal form is expressed as:
$$f(x_1, \ldots, x_n) = \bigvee_{i=1}^{m} \bigwedge_{j \in S_i} x_j \wedge \bigwedge_{k \in \bar{S}_i} \neg x_k$$

where each term is a conjunction (AND) of literals (variables or their negations).

### Probability Computation in Orthogonal DNF
For an orthogonal DNF under independent feature distribution $D$:

$$P(\varphi = 1) = \sum_{i=1}^{m} P(T_i = 1)$$

When computing sufficient feature importance $v_g^{\text{suff}}$ for a subset $S$:

$$\text{Contribution of pair }(T_i, T_j) = P(x_S \in C^S_{T_i,T_j}) \cdot P(x_{\bar{S}} \in C^{\bar{S}}_{T_i}) \cdot P(x_{\bar{S}} \in C^{\bar{S}}_{T_j})$$

where $C^S_{T_i}$ denotes the constraints that term $T_i$ imposes on variables in $S$.

### Degree of Composed Functions
If a Boolean function $g$ has degree $k$ and is composed with an inverter function of degree $t$:

$$\deg(h) \leq k \cdot t$$

where $h(y) = g(\text{InvSamp}(y, r^*))$.

## Physical Intuition / Derivation

### Why Orthogonal DNF Matters

Consider an engineer analyzing a digital circuit or a machine learning model to understand which input features matter. With a standard DNF, multiple terms might be "active" simultaneously, making it ambiguous which term is responsible for the output. 

Orthogonal DNF resolves this by guaranteeing **mutual exclusivity**: exactly one term (or none) fires for any input. This mirrors the structure of many real systems:
- **Digital circuits**: Multiplexers route signals through mutually exclusive paths
- **Decision trees**: Each input follows exactly one branch (one term "fires")
- **Logic synthesis**: Orthogonal representations enable polynomial-time evaluation

### Computational Efficiency

The mutual exclusivity property enables polynomial-time computation. When analyzing $m^2$ pairs of terms (all possible pairs for interaction effects), we can:
1. Check if constraints are consistent in polynomial time
2. Skip inconsistent pairs immediately (they contribute zero)
3. Factor probability computations using independence

Without orthogonality, we'd need to subtract overlap regions (inclusion-exclusion principle), which becomes exponentially complex.

## Applications in Engineering

### 1. Digital Logic Design
Boolean functions form the foundation of digital circuits. Orthogonal DNF representations enable:
- **Circuit minimization**: Identify redundant logic paths that never coexist
- **Verification**: Simplified reasoning about mutual exclusivity ensures no race conditions
- **Hardware synthesis**: Direct translation from orthogonal form to non-overlapping logic gates

### 2. Feature Importance Analysis (Machine Learning)
When interpreting black-box models via Boolean logic approximations:
- Extract decision rules in orthogonal form to ensure each rule is non-redundant
- Compute feature sufficiency/importance scores in polynomial time (rather than exponential)
- Provide interpretable explanations where each factor contributes independently

### 3. Software Testing & Verification
Boolean functions model program logic:
- **Orthogonal DNF** ensures each test case exercises a distinct logical path
- Avoids redundant test coverage
- Critical for safety-critical systems (aerospace, automotive)

### 4. Cryptography & Pseudorandom Generation
In the provided sources, Boolean functions appear in the context of pseudorandom function inversion:
- Understand the composition of Boolean functions to analyze cryptographic security
- Degree bounds help quantify hardness of inverting composed functions

### 5. Network Switching & Routing
Boolean logic controls packet routing:
- Orthogonal DNF ensures packets take exactly one route (no conflicts)
- Prevents deadlock in switch fabric architectures

## Common Mistakes / Pitfalls

### 1. Confusing Boolean Functions with Logical Operators
**Mistake**: Treating "AND" and "OR" as generic set operations without respecting the binary constraint.
**Reality**: Boolean functions operate strictly on $\{0,1\}$ (or $\{\pm 1\}$) domain and codomain. Partial truth values don't exist.

### 2. Assuming DNF is Always Orthogonal
**Mistake**: Converting any function to DNF without checking for overlapping terms.
**Reality**: Arbitrary DNF can have exponentially many overlapping term pairs. Orthogonality requires deliberate construction or verification.

### 3. Neglecting the Cost of Orthogonalization
**Mistake**: Assuming orthogonal DNF is always more compact than standard DNF.
**Reality