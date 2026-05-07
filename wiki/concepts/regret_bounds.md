# regret bounds

## Definition

**Regret bounds** quantify the performance of an online learning algorithm by measuring cumulative loss relative to the best fixed decision in hindsight. Formally, for an algorithm $\mathcal{A}$ operating over $T$ timesteps:

$$R_T = \sum_{t=1}^{T} \ell_t(\mathcal{A}_t) - \min_{i \in [n]} \sum_{t=1}^{T} \ell_t(i)$$

where:
- $\ell_t(\mathcal{A}_t)$ is the loss incurred by algorithm $\mathcal{A}$ at timestep $t$
- $\ell_t(i)$ is the loss of expert $i$ at timestep $t$
- The regret measures how much worse the online algorithm performs than the best expert selected retrospectively

**Regret is amortized** by normalizing over $T$: average regret per round = $R_T / T$.

A regret bound is **sublinear** if $R_T = o(T)$, ensuring the algorithm asymptotically matches the best expert's average loss as $T \to \infty$.

## Key Equations

### Classical Full-Information Setting
For the Exponential Weights Algorithm (EWA) with $n$ experts over $T$ rounds:

$$R_T = O\left(\sqrt{T \log n}\right)$$

Per-round regret: $\bar{R}_T = O\left(\sqrt{\frac{\log n}{T}}\right)$

### Bandit Setting
For the EXP3 algorithm (expert selection with bandit feedback):

$$R_T = O\left(\sqrt{nT \log n}\right)$$

### Distributed Experts Problem (Main Result)
For $n$ experts distributed across $s$ servers with $\ell_p$ norm aggregation:

$$R_T \gtrsim \frac{1}{\sqrt{T}} \cdot \text{polylog}(nsT)$$

Communication cost:

$$\text{Comm} = O\left(\left(\frac{n}{R_T^2} + \frac{s}{R_T^2}\right) \cdot \max(s^{1-2/p}, 1) \cdot \text{polylog}(nsT)\right) \text{ bits}$$

## Physical Intuition / Derivation

### Why Regret Bounds Matter

In sequential decision-making, the algorithm must choose between:
1. **Exploitation**: selecting the expert appearing best so far
2. **Exploration**: trying other experts to gather information

Regret bounds formalize this exploration-exploitation tradeoff. A bound of $\sqrt{T}$ (rather than linear $T$) indicates the algorithm "learns" from experience—its average loss converges to the best expert.

### Why $\sqrt{T}$ is Natural

Consider $n$ experts with adversarial losses. The information-theoretic argument:
- After $t$ steps, you've eliminated roughly $\log(1/\epsilon)$ possibilities per "doubling" of experiments
- To identify the best expert among $n$ requires $\Omega(\log n)$ bits of information
- Spread over $T$ rounds, this gives $\sqrt{T \log n}$ regret

**Multiplicative Weights Analysis**: 
- Maintain weights $w_i(t)$ for each expert, updated as $w_i(t+1) = w_i(t) \cdot (1-\eta \ell_t(i))$ with learning rate $\eta = \sqrt{\log n / T}$
- The exponential weighting ensures:
  - Good experts remain weighted high (exploitation)
  - Bad experts decrease gradually, allowing exploration
  - Optimal rate balances competing terms in the regret decomposition

### Distributed Extension

The paper extends this to distributed settings where expert losses are computed via an $\ell_p$ norm across $s$ servers. The key challenge: minimizing **both regret and communication**. The factor $\max(s^{1-2/p}, 1)$ reflects:
- For $p = \infty$ (max norm): all $s$ servers always contribute equally
- For $p = 2$ (Euclidean): correlation structure allows selective communication
- For small $p$: few servers dominate, reducing communication overhead

## Applications in Engineering

### 1. **Hyperparameter Optimization & Model Selection**
Multiple pretrained model architectures evaluated on distributed datasets. The algorithm selects deployment configuration while minimizing validation loss, with communication constraints between a central controller and dataset repositories.

### 2. **Distributed Recommendation Systems**
Different ranking functions deployed across geographically distributed servers (each handling a region/demographic). Central coordinator learns which ranking to use, with regret bounds guaranteeing convergence to best performer while limiting inter-datacenter bandwidth.

### 3. **Federated Online Learning**
Mobile devices or edge nodes act as "servers"; each expert (model version) trained locally. Central server conducts expert selection while bound on communication prevents network congestion.

### 4. **Adaptive Resource Allocation**
In cloud systems, choose among $n$ resource allocation policies (CPU scheduling, memory management) each evaluated on $s$ machines. Regret bounds guarantee low cumulative overhead compared to best policy.

### 5. **Reinforcement Learning Policy Selection**
Agents (servers) train policies; central controller selects which policy to deploy at each step. Regret measures suboptimality vs. best fixed policy, while communication bound limits policy synchronization.

## Common Mistakes / Pitfalls

### 1. **Confusing Regret with Loss**
Students often compute cumulative loss $\sum \ell_t$ and call it "regret." Regret is the **excess** loss relative to the best expert: $\sum \ell_t(\text{algo}) - \sum \ell_t(\text{best expert})$. A constant-loss scenario has zero regret despite nonzero cumulative loss.

### 2. **Assuming Regret is Always Sublinear**
Without exploration, regret can be $\Theta(T)$. The $\sqrt{T}$ bound requires explicit hedging (e.g., Multiplicative Weights). Pure greedy algorithms achieve only $O(n T)$