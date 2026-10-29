---
video: NrzmH_yerBU | Understanding the Particle Filter | Autonomous Navigation, Part 2 | MATLAB | 15:52
---
## A particle filter over the robot's pose

**Monte Carlo localization** (MCL) is a particle filter whose particles are robot poses $(x, y, \theta)$ in a known map. Each step:

- Move every particle with the motion model, sampling odometry noise so the cloud spreads.
- Weight every particle by $p(z \mid x, m)$: how well the scan it would see from its pose, in map $m$, matches the real scan.
- Resample.

It's the default localization method for indoor mobile robots: the ROS navigation stack's AMCL is an adaptive version of it.

## Scoring a scan with a likelihood field

Simulating every laser beam for every particle (the **beam model**) is slow. The **likelihood field** model is a fast shortcut. Precompute, for every map cell, the distance to the nearest obstacle. Then, for each beam, put its endpoint into the map from the particle's pose and look up that distance $d$. A small $d$ means the beam hit where a wall is. Each beam contributes $e^{-d^2 / 2\sigma^2}$, usually mixed with a small constant for random readings and max-range returns.

## Worked example: two particles, three beams

Use $\sigma = 0.1$ m. Particle A's three beam endpoints land $0.05$, $0.10$ and $0.02$ m from walls; particle B's land $0.5$, $0.05$ and $0.8$ m away. The log-likelihood is $-\sum d^2 / (2\sigma^2)$:

$$\text{A}: -\frac{0.0025 + 0.01 + 0.0004}{0.02} \approx -0.65, \qquad \text{B}: -\frac{0.25 + 0.0025 + 0.64}{0.02} \approx -44.6$$

So A is about $e^{44}$ times more likely. Even with three beams, one bad pose is ruled out at once. With 360 beams these numbers get extreme, which is why real systems subsample beams.

## Finding yourself from scratch

If the robot has no idea where it is, spread the particles uniformly over the free space of the map. That's **global localization**, which a Kalman filter can't do. At first many clusters survive, one for each place consistent with the scans so far; as the robot moves and sees distinctive structure, wrong clusters die out until one remains. Particle counts can adapt too: **KLD-sampling** uses many particles while the belief is spread out and few once it has converged.

## Recovering from being kidnapped

If the robot is picked up and moved, or the filter converged to the wrong place, there may be no particles near the true pose, and resampling can't create them. **Augmented MCL** watches the average measurement likelihood. When it falls sharply compared with its long-term average, the filter is probably lost, so it replaces a fraction of particles with random poses, which can then latch on to the true location.

> **Common mistake:** treating all 360 beams of a scan as independent. Neighboring beams hit the same wall and have correlated errors, so multiplying all their likelihoods makes the filter wildly overconfident and prone to collapse. Use a subset of beams, or soften each beam's likelihood.
