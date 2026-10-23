# Reinforcement Learning

## Definition

**Reinforcement Learning (RL)** is a machine learning paradigm in which an agent learns to make sequential decisions by interacting with an environment, receiving feedback in the form of rewards or penalties, and iteratively improving its decision-making policy without explicit supervision.

In the context of engineering optimization problems (such as scheduling), RL trains models to discover policies that map observed states to actions, minimizing a cost function (e.g., maximizing frame arrival times, reducing jitter, or meeting timing constraints).

### Key Characteristics:
- **Agent-Environment Interaction**: The agent observes the environment state, selects an action, receives a scalar reward, and transitions to a new state
- **Policy Learning**: The agent builds a decision rule (policy $\pi$) that maps states to actions
- **Exploration vs. Exploitation**: The agent balances trying new actions (exploration) with repeating known good actions (exploitation)
- **Temporal Credit Assignment**: The agent must learn which actions lead to delayed rewards

---

## Key Equations

### Bellman Equation (Value Function)

The expected cumulative discounted reward from state $s$ is:

$$V(s) = \mathbb{E}\left[\sum_{t=0}^{\infty} \gamma^t r_t \mid s_0 = s\right]$$

where:
- $V(s)$ is the **value function** (expected cumulative reward from state $s$)
- $r_t$ is the reward at time step $t$
- $\gamma \in [0,1)$ is the **discount factor** (future rewards weighted less heavily)

For state-action pairs:

$$Q(s,a) = \mathbb{E}[r + \gamma \max_{a'} Q(s',a') \mid s,a]$$

where $Q(s,a)$ is the **action-value function** giving the expected return of taking action $a$ in state $s$.

### Policy Gradient (Policy-Based Methods)

$$\nabla_\theta J(\theta) = \mathbb{E}[\nabla_\theta \log \pi_\theta(a|s) Q(s,a)]$$

where $\pi_\theta$ is a parameterized policy and $\theta$ are learnable parameters.

---

## Physical Intuition / Derivation

### Why RL for Scheduling Problems?

In hard combinatorial optimization problems like **no-wait scheduling**, the search space grows exponentially with problem size. Traditional algorithms (exhaustive search, greedy heuristics) either:
- Require prohibitive computation time (e.g., 3 hours for 1,500 streams with Tabu Search)
- Produce suboptimal solutions

RL sidesteps exhaustive enumeration by **learning a policy** that makes good local decisions sequentially. The agent observes the current partial schedule state and learns which stream to schedule next to minimize the objective (e.g., maximum arrival time).

### Training Loop:

1. **Initialization**: Create an empty schedule; agent observes state (unscheduled streams, current time windows)
2. **Action Selection**: Policy $\pi$ selects which stream to place next (guided by learned value estimates or sampling)
3. **Reward Signal**: Upon schedule completion, compute reward based on objective metrics (negative reward for constraint violations or high latency)
4. **Policy Update**: Backpropagate reward signal to improve future decisions via value/policy gradient methods
5. **Iteration**: Repeat with multiple training episodes until convergence

### Computational Trade-off:

Training time (∼400 seconds for 100 streams in Wang et al. [6]) is acceptable *offline*, whereas the resulting policy evaluates schedules in milliseconds *online*—suitable for dynamic TSN environments.

---

## Applications in Engineering

### 1. **Time-Sensitive Networking (TSN) Scheduling**
- **Problem**: Schedule data flows (streams) across networked switches to meet hard real-time deadlines
- **RL Advantage**: Learns policies that balance competing constraints (no-wait property, minimizing jitter) without explicit enumeration
- **Example**: Wang et al. [6] trained models to minimize maximum arrival time across all frames in a daisy-chain topology

### 2. **Job-Shop Scheduling**
- RL maps the scheduling problem to a graph coloring problem with restricted feasible "colors" (time slots)
- Explores the space of partial schedules, learning which decisions avoid bottlenecks

### 3. **Robotics & Control**
- Train robot controllers (navigation, manipulation) by rewarding task completion and penalizing collisions
- Natural fit for sequential decision-making in continuous or discrete spaces

### 4. **Resource Allocation in Cloud/Edge Computing**
- Allocate CPU, memory, network bandwidth across competing workloads
- RL learns to balance latency, throughput, and fairness

### 5. **Traffic Signal Control**
- Optimize green/red cycles by rewarding reduced congestion and waiting times
- Multi-agent RL extends to coordinated control across intersections

---

## Common Mistakes / Pitfalls

### 1. **Treating RL as a "Magic Bullet"**
- **Mistake**: Applying RL to every optimization problem without considering alternatives
- **Reality**: For small/medium problems, exact algorithms (MIP solvers, dynamic programming) or specialized heuristics may be faster and more reliable
- **Lesson**: RL excels at large-scale, high-dimensional problems where the reward signal is well-defined but the search space is intractable

### 2. **Poor Reward Design**
- **Mistake**: Rewarding only the final outcome (schedule feasibility)
- **Reality**: Sparse rewards make learning glacially slow; intermediate rewards ("shaping") guide exploration more effectively
- **Lesson**: Decompose the objective into differentiable, per-step feedback

### 3. **Scalability Illusion**
- **Mistake**: Assuming RL trained on 100 streams automatically scales to 45,000 flows
- **Reality**: Policy generalization requires careful architecture design and curriculum learning
- **Lesson**: Validate on realistic problem sizes; compare wall-clock time vs. exact/heuristic baselines

### 4. **Ignoring Offline vs. Online**
- **Mistake**: Counting training time in the total cost when online speed is the priority
- **Reality**: If scheduling is done offline (e.g., monthly), 400 seconds of training is acceptable;

<!-- pora:begin -->
## In Principles of Robot Autonomy

- Read: [Chapter 18: Reinforcement Learning](https://porabook.com/book/reinforcement-learning/)
- Stack layer: Decisions & learning · learned
- Run: [Widget Sales](https://colab.research.google.com/github/StanfordASL/pora-exercises/blob/main/ch18/exercises/widget_sales.ipynb) ([source](https://github.com/StanfordASL/pora-exercises/blob/main/ch18/exercises/widget_sales.ipynb))
- Watch: [AA203 lecture 14: Intro to Imitation Learning and Reinforcement Learning](https://youtu.be/7YdOx-ih0II)
- Watch: [AA203 lecture 16: Fundamentals of Reinforcement Learning](https://youtu.be/cqPbt3OfRK4)

### Key ideas

1. In RL the agent does not know P or R; it interacts with the environment, observing (s, a, r, s') tuples, and must learn a good policy from this experience.
2. Exploration versus exploitation: acting greedily on current estimates can miss better actions, so strategies like ε-greedy or optimism deliberately try uncertain actions.
3. Methods split into model-free (learn values or policies directly) and model-based (learn dynamics, then plan), and into on-policy versus off-policy depending on which policy generated the data.

Try it: Simulate a 10-armed bandit with Gaussian rewards and compare average reward over 1000 steps for ε = 0, 0.01, and 0.1 using sample-average value estimates.

Needs first: [[Markov_decision_processes]], [[Neural_network]]

Unlocks: [[Monte_Carlo_and_TD_learning]], [[Policy_gradients_and_actor-critic]], [[Model-based_RL_and_system_ID]], [[Inverse_reinforcement_learning]]

Part of [[Principles_of_Robot_Autonomy]]. Summary and study notes from the unofficial PoRA Atlas; the book is the authoritative reference.
<!-- pora:end -->
