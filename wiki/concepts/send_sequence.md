# send sequence

## Definition

A **send sequence** is a parameterized protocol specification in contention resolution systems, defining the probability with which messages (called "balls") at each collision level attempt retransmission in a given time step.

Formally, a send sequence is a sequence $p = (p_0, p_1, p_2, \ldots)$ where:
- Each $p_k \in (0, 1]$ represents the **send probability** for messages that have experienced exactly $k$ collisions
- $W_k = 1/p_k$ is the corresponding **backoff wait factor** or inverse send rate
- The sequence governs the dynamics of a [[backoff process]] with a specified birth rate $\lambda > 0$

The send sequence works in conjunction with a probabilistic collision model to determine system stability and throughput.

## Key Equations

At each time step $t$, for each bin $i$ (collision count), the number of attempting messages is drawn from a binomial distribution:

$$s_i(t) \sim \text{Binomial}(B_i(t), p_i)$$

where $B_i(t)$ is the population of bin $i$ before sends at time $t$.

A message successfully escapes (is transmitted without collision) if exactly one message sends across **all bins combined**:

$$e_i(t) = \begin{cases} s_i(t) & \text{if } |s_i(t)| = 1 \text{ and } \left|\bigcup_{k \geq 0} s_k(t)\right| = 1 \\ \emptyset & \text{otherwise} \end{cases}$$

Messages that collide are promoted to the next bin:

$$b_i(t) = (B_i(t) \setminus s_i(t)) \cup (s_{i-1}(t) \setminus e_{i-1}(t))$$

For system **stability** (positive recurrence to empty state), the send sequence must satisfy capacity constraints related to the birth rate $\lambda$.

## Physical Intuition / Derivation

### Why Send Sequences Matter

In a shared communication channel (radio access, Ethernet collision domains, etc.), multiple messages may attempt transmission simultaneously, causing collisions. A **send sequence** provides a feedback control mechanism:

1. **First attempt** ($k=0$): New messages send with probability $p_0$ (typically $p_0 = 1$ for immediate first try)
2. **After collision** ($k \geq 1$): Messages in collision bin $k$ backoff with probability $p_k < p_0$, spreading retransmission attempts over future time steps

### Example: Binary Exponential Backoff

The classical IEEE 802.3 Ethernet backoff uses:
$$p_k = \frac{1}{2^k} \quad \text{for} \quad k \leq 10$$

This exponentially decreases send probability with collision count, roughly doubling the waiting period each time.

### Markov Chain Perspective

The state space is $\mathbf{b}(t) = (b_0(t), b_1(t), b_2(t), \ldots)$ where $b_i(t)$ counts messages with exactly $i$ collisions. Since this state is a deterministic function of the previous state and independent Poisson births plus binomial send samples, the backoff process forms a **countable-state Markov chain**.

Stability requires the chain be **positive recurrent**—starting from the empty state, it returns to empty state with probability 1 in finite expected time.

## Applications in Engineering

### 1. **Wireless Medium Access Control (MAC)**
- 802.11 WiFi: CSMA/CA uses adaptive send sequences based on congestion
- LoRaWAN: Adaptive spreading factors and retry probabilities for collision avoidance
- Cellular uplink: Contention resolution protocols in random access channels (RACH)

### 2. **Packet Radio Networks**
- ALOHA and slotted ALOHA: Pure send sequence with $p_k = p$ (constant) for all $k$
- CSMA (Carrier Sense Multiple Access): Deterministic backoff sequences before reattempting

### 3. **Computer Networks**
- Ethernet collision domains: Binary exponential backoff on shared bus topologies
- CAN bus (automotive): Priority-based send sequences with deterministic retry intervals

### 4. **Database Concurrency Control**
- Optimistic locking: Retry send sequences when transaction conflicts occur
- Lock-free data structures: Adaptive backoff in compare-and-swap retries

### 5. **IoT and Energy Harvesting**
- Where send energy is costly, sequences with small $p_k$ preserve power while maintaining throughput

## Common Mistakes / Pitfalls

### 1. **Confusing Send Sequence with Schedule**
**Mistake:** Treating $p_k$ as a deterministic time delay rather than a probability.  
**Reality:** $p_k$ is a sending *probability*; the actual time between attempts is random (geometric wait).

### 2. **Assuming All Sequences Stabilize**
**Mistake:** Any send sequence "should work" if you backoff enough.  
**Reality:** Sequence stability depends on birth rate $\lambda$. Overly conservative sequences ($p_k$ too small) can starve under load.

### 3. **Ignoring the Empty State Definition**
**Mistake:** Optimizing only for high-load throughput.  
**Reality:** Stability explicitly requires positive recurrence to the *empty state*. A system that delivers packets under load but never clears residual collisions is unstable.

### 4. **Linear vs. Exponential Backoff Misconception**
**Mistake:** Assuming exponential backoff ($p_k = 1/2^k$) is always superior.  
**Reality:** Optimality depends on network model, birth rate, and delay sensitivity. Linear backoff can sometimes outperform exponential under specific conditions.

### 5. **Forgetting about Birth Rate Coupling**
**Mistake:** Designing a sequence without considering the arrival rate $\lambda$.  
**Reality:** A sequence stable at $\lambda = 0.5$ may be unstable at $\lambda = 1.0$. Capacity is determined by the send sequence