# backoff process

## Definition

A **backoff process** is a mathematical model for managing **collision resolution** in distributed communication systems where multiple agents (messages/packets) compete to transmit over a shared medium.

**Formal Definition (Definition 1.3):**

Given a send sequence $p = (p_0, p_1, p_2, \ldots)$ where each $p_k \in (0,1]$ and birth rate $\lambda > 0$, the backoff process $X$ maintains a state vector:

$$\mathbf{b}^X(t) = (b_0^X(t), b_1^X(t), b_2^X(t), \ldots)$$

where $b_i^X(t)$ is the **set of messages (balls) that have collided exactly $i$ times** during time steps $1, \ldots, t$.

**Key components:**

- **Bins**: Messages are organized into bins indexed by collision count $i$
- **Balls**: Messages/packets competing for transmission
- **Birth rate $\lambda$**: Average number of new messages arriving per time step (Poisson distribution)
- **Send probability $p_i$**: Probability that a message in bin $i$ attempts transmission at the current step

## Key Equations

**State evolution at time step $t$:**

1. **New arrivals** (Poisson-distributed):
   $$n^X(t) \sim \text{Poisson}(\lambda)$$

2. **Bin populations after births, before sending**:
   $$B_0^X(t) = n^X(t) \cup b_0^X(t-1)$$
   $$B_i^X(t) = b_i^X(t-1), \quad i \geq 1$$

3. **Send attempt from bin $i$**: Each ball independently sends with probability $p_i$
   $$s_i^X(t) \subseteq B_i^X(t), \quad |s_i^X(t)| \sim \text{Binomial}(|B_i^X(t)|, p_i)$$

4. **Escape condition** (successful transmission):
   $$e_i^X(t) = \begin{cases} s_i^X(t) & \text{if } |s_i^X(t)| = 1 \text{ and no collisions across bins} \\ \emptyset & \text{otherwise} \end{cases}$$

5. **Bin updates for next step**:
   $$b_0^X(t) = B_0^X(t) \setminus s_0^X(t)$$
   $$b_i^X(t) = (B_i^X(t) \setminus s_i^X(t)) \cup (s_{i-1}^X(t) \setminus e_{i-1}^X(t)), \quad i \geq 1$$

Messages that collide advance to the next bin, and messages that escape are successfully transmitted and removed from the system.

**Stability criterion:**

The backoff process $X$ is **stable** if the empty state is positive recurrent:
- The process returns to $\mathbf{b}(t) = \emptyset$ with probability 1
- The expected return time $\mathbb{E}[\tau_0]$ is finite

## Physical Intuition / Derivation

### Core Mechanism

A backoff process models what happens when multiple parties try to transmit on a shared channel:

1. **Initial attempt**: New messages arrive (birth) and attempt transmission at rate $p_0$
2. **Collision detection**: If multiple messages send simultaneously, they collide
3. **Exponential backoff**: Collided messages move to bin $i+1$ and retry with lower probability $p_i$ at future steps
4. **Recovery**: A message escapes (succeeds) only when it transmits alone

### Why Bins?

The bin structure implements **multiplicative backoff**: messages that have collided multiple times reduce transmission probability, decreasing the likelihood of future collisions. This is analogous to Ethernet/802.11 backoff algorithms.

### Why Markovian?

The state $\mathbf{b}^X(t)$ completely determines the stochastic evolution at step $t+1$ because:
- Only the current collision history (bin occupancy) influences future transmission probabilities
- New arrivals are independent (Poisson process)
- Each transmission decision is independent given bin membership

### Stability Analysis

For large $\lambda$ (high arrival rate), the system can become **unstable**: bins accumulate messages faster than they escape. Stability requires appropriate choice of send probabilities $(p_0, p_1, \ldots)$ such that:

$$\sum_{i=0}^{\infty} p_i \text{ (effective throughput)} > \lambda \text{ (arrival rate)}$$

## Applications in Engineering

### 1. **MAC Layer Protocols**
- **CSMA/CD (Ethernet)**: Classic backoff process where colliding packets double their backoff window
- **802.11 WiFi**: Implements collision avoidance with exponential backoff schedules
- **LoRaWAN**: Random access protocols for IoT use adaptive backoff

### 2. **Network Contention Resolution**
- **Channel access in wireless networks**: Multiple devices compete for spectrum
- **Distributed medium access**: Decentralized systems without central arbitration
- **Contention-based protocols**: Sensor networks, ad-hoc networks

### 3. **Queue Management**
- **Retransmission protocols**: TCP congestion control uses backoff-like mechanisms
- **Load balancing**: Systems redirect colliding requests to secondary resources (bins)

### 4. **Resource Allocation**
- **Shared memory access**: Multiprocessor systems with cache coherency
- **Database locking**: Transaction conflicts trigger backoff-and-retry

### 5. **Queueing Theory**
- **Performance analysis of random access networks**
- **Stability characterization** for distributed systems
- **Throughput optimization** through send sequence design

## Common Mistakes / Pitfalls

### 1. **Confusing collision count with wait time**
- **Mistake**: Assuming bin $i$ messages have waited $i$ steps