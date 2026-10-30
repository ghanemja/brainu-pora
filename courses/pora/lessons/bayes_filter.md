---
video: oUq0a8jHSQg | Bayes Filter - 5 Minutes with Cyrill | Cyrill Stachniss | 5:03
video: nVU1DQ-_R5E | The Bayes Filter: A Tool Every Roboticist Should Know | James Han | 5:25
---
## Keep a belief, not a guess

A robot never knows exactly where it is. Instead of one best guess, the Bayes filter keeps a **belief**: a probability for every possible state, given everything it has done and seen so far,

$$\mathrm{bel}(x_t) = p(x_t \mid z_{1:t}, u_{1:t})$$

where $u$ are the controls (what it commanded) and $z$ are the measurements. A sharp belief means "I'm fairly sure"; a spread-out one means "I could be in several places".

## Two steps, repeated forever

**Predict.** When the robot moves, push the belief through the motion model. Motion is noisy, so the belief spreads out:

$$\overline{\mathrm{bel}}(x_t) = \int p(x_t \mid u_t, x_{t-1})\, \mathrm{bel}(x_{t-1})\, dx_{t-1}$$

**Correct.** When a measurement arrives, reweight every state by how well it explains that measurement, then renormalize so the probabilities sum to one ($\eta$ is that normalizer):

$$\mathrm{bel}(x_t) = \eta\, p(z_t \mid x_t)\, \overline{\mathrm{bel}}(x_t)$$

This works step by step, without replaying history, because of the **Markov assumption**: the current state holds everything the past can tell you about the future.

## The book's hallway

A robot drives along a hallway with doors and a sensor that looks for a door. Moving smears its belief forward; seeing a door sharpens the belief around positions next to doors. In a hallway with several identical doors, the belief can have several peaks at once, which the Bayes filter represents fine, and which a single Gaussian (the Kalman filter) can't.

## Worked example: one door, two readings

Before sensing, the robot thinks it's in front of a door with probability $P(\text{door}) = 0.5$. Its sensor says "door" with probability $0.6$ when there is one, and falsely with probability $0.2$ when there isn't. It reads "door":

$$P(\text{door} \mid z) = \frac{0.6 \times 0.5}{0.6 \times 0.5 + 0.2 \times 0.5} = \frac{0.30}{0.40} = 0.75$$

A second "door" reading (without moving) uses $0.75$ as the new prior:

$$\frac{0.6 \times 0.75}{0.6 \times 0.75 + 0.2 \times 0.25} = \frac{0.45}{0.50} = 0.9$$

Each reading is weak on its own; together they get the robot to 90% sure.

> **Common mistake:** forgetting to normalize. Multiplying by the likelihood gives 0.30 and 0.10, not probabilities. Dividing by their sum (the $\eta$) is what turns them into 0.75 and 0.25.
