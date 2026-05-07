# private-coin protocols

## Definition

A **private-coin protocol** is a distributed communication protocol in which an adversary can adaptively choose the problem instance (or distribution of alternatives) *after* observing the strategy employed by the protocol itself. This is in contrast to **public-coin protocols**, where the problem instance is fixed independently of the protocol's strategy.

In the context of quantum state certification (the source domain), a private-coin protocol allows a malicious adversary to:
1. Observe the quantum channels $\Phi_1, \ldots, \Phi_m$ selected by distributed nodes
2. Then adversarially choose a distribution $D \in \mathcal{D}_\varepsilon(1/d)$ of quantum states to maximize the difficulty of the certification task

This reversal of the order of moves between the protocol designer and the adversary leads to **stronger lower bounds** on the resources (e.g., number of nodes $m$) required for success.

## Key Equations

### Distinguishing Tasks in Private-Coin Setting

For a private-coin protocol to succeed at $\varepsilon$-certifying $d$-dimensional quantum states using $d_q$-dimensional quantum messages, the adversarial game condition is:

$$\max_{\Phi_1,\ldots,\Phi_m} \min_{D \in \mathcal{D}_\varepsilon(1/d)} D_{\chi^2}\left(\mathbb{E}_{\rho \sim D}\left[\bigotimes_{i=1}^m \Phi_i(\rho)\right] \,\Big\|\, \bigotimes_{i=1}^m \Phi_i\left(\frac{\mathbb{I}}{d}\right)\right) \geq \frac{1}{16} \tag{4.2}$$

Compare this to the **public-coin** condition:

$$\min_{D \in \mathcal{D}_\varepsilon(1/d)} \max_{\Phi_1,\ldots,\Phi_m} D_{\chi^2}\left(\mathbb{E}_{\rho \sim D}\left[\bigotimes_{i=1}^m \Phi_i(\rho)\right] \,\Big\|\, \bigotimes_{i=1}^m \Phi_i\left(\frac{\mathbb{I}}{d}\right)\right) \geq \frac{1}{16} \tag{4.1}$$

**Key difference:** The order of $\max$ and $\min$ is reversed. In private-coin, the adversary moves *second*, after observing the channels.

### Upper Bounding the Distinguishing Task

To derive lower bounds on $m$, one upper bounds the quantum $\chi^2$-divergence using the quantum Ingster–Suslina method:

$$D_{\chi^2}\left(\mathbb{E}_\theta[\sigma^{(m)}_\theta] \,\Big\|\, \sigma^{(m)}\right) = \mathbb{E}_{\theta,\theta'}[​\prod_{i=1}^m (1 + Z_i(\theta, \theta'))] - 1 \leq \mathbb{E}_{\theta,\theta'}[​\prod_{i=1}^m \exp(Z_i(\theta, \theta'))] \tag{4.3}$$

where $\theta, \theta'$ are i.i.d. parameters and:

$$Z_i(\theta, \theta') = \text{tr}\left(\sigma_i^{-1}(\sigma_{i,\theta} - \sigma_i)(\sigma_{i,\theta'} - \sigma_i)\right) \tag{4.4}$$

Here $\sigma_i$ is a reference state and $\sigma_{i,\theta}$ is a parameterized state family.

## Physical Intuition / Derivation

### Why Private-Coin is Harder

The essential difficulty stems from **information asymmetry**:

1. **Public-coin:** The adversary must commit to a single hard distribution $D$ upfront. The protocol designer, knowing which distribution will be used, can optimize the channels $\Phi_i$ to distinguish it. The protocol and adversary simultaneously "lock in" their choices.

2. **Private-coin:** The protocol designer must first commit to channels $\Phi_i$ *without knowing* the distribution. Only then does the adversary, observing these channels, choose the worst-case distribution $D$ tailored to defeat them. The adversary gains a strategic advantage.

### Game-Theoretic Framing

The distinguishing problem becomes a **two-player sequential game**:
- **Player 1 (Protocol):** Chooses quantum channels $\Phi_1, \ldots, \Phi_m$
- **Player 2 (Adversary):** After observing Player 1's choice, selects distribution $D$ to minimize the quantum $\chi^2$-divergence

The protocol's payoff is the distinguishability (larger is better); the adversary's is to minimize it. The max-min inequality in equation (4.2) formalizes this game tree.

### Why Stronger Bounds Emerge

The adversary's second-mover advantage allows them to:
- Target specific weaknesses in the chosen channels
- Pick a distribution that exploits the compression bottleneck ($d_q \ll d$)
- Potentially align the alternative hypotheses with the subspace where $\Phi_i$ has poor discrimination

As a result, more nodes $m$ are required to guarantee distinguishability against a private-coin adversary than against a public-coin adversary.

## Applications in Engineering

### 1. **Quantum Communication & Verification**
Private-coin bounds are essential when designing distributed quantum networks where verification must succeed against adaptive adversaries who can choose attack distributions after observing the protocol. Examples:
- Distributed quantum certification systems
- Byzantine-robust quantum protocols
- Quantum sensor networks where the adversary learns the measurement setup before crafting false signals

### 2. **Distributed Machine Learning**
Private-coin analysis applies to federated learning scenarios where:
- Central server designs learning algorithms
- Adversary then crafts poisoned data distributions to fool the algorithm
- Establishes sample complexity lower bounds for robust distributed learning

### 3. **Information Auditability & Compliance**
In engineering