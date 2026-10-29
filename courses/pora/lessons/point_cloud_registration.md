---
video: QWDM4cFdKrE | Iterative Closest Point (ICP) - 5 Minutes with Cyrill | Cyrill Stachniss | 5:02
video: 4uWSo8v3iQA | Iterative Closest Point (ICP) - Computerphile | Computerphile | 16:25
---
## The alignment problem

A lidar or depth camera gives you a cloud of 3-D points. **Registration** finds the rigid motion, a rotation $R$ and translation $t$, that lines up a source cloud $\{p_i\}$ with a target cloud $\{q_i\}$:

$$\min_{R,\, t} \; \sum_i \big\| R\, p_i + t - q_i \big\|^2$$

Align two consecutive scans and you get the robot's motion between them (lidar odometry). Align a scan to a stored map and you get localization. Align a scan to a model and you get an object's pose.

## With known matches, there's a closed form

If you know which $p_i$ corresponds to which $q_i$, the best $(R, t)$ comes straight out of linear algebra (the **Kabsch** or **Umeyama** method):

- Subtract the centroids: $p_i' = p_i - \bar p$ and $q_i' = q_i - \bar q$.
- Form $W = \sum_i p_i'\, q_i'^\top$ and take its SVD, $W = U \Sigma V^\top$.
- Then $R = V U^\top$ (flip the sign of the last column of $V$ if $\det R = -1$), and $t = \bar q - R \bar p$.

No iteration, no initial guess needed.

## ICP: guess the matches, solve, repeat

In practice you don't know the correspondences. **Iterative closest point** (ICP) guesses them:

- Transform the source by the current estimate, and match each source point to its **nearest** target point (using a k-d tree to make this fast).
- Solve the closed-form alignment for those matches.
- Repeat until the error stops decreasing.

Each round, better alignment gives better matches, and better matches give better alignment.

## Worked example: two points in 2-D

Source $p_1 = (0, 0)$, $p_2 = (1, 0)$; target $q_1 = (1, 1)$, $q_2 = (1, 2)$.

- Centroids: $\bar p = (0.5, 0)$ and $\bar q = (1, 1.5)$.
- Centered: $p' = (\mp 0.5, 0)$ and $q' = (0, \mp 0.5)$. The source points along $x$, the target along $y$: a $90°$ rotation, $R = \begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix}$.
- Translation: $t = \bar q - R \bar p = (1, 1.5) - (0, 0.5) = (1, 1)$.

Check: $R p_2 + t = (0, 1) + (1, 1) = (1, 2) = q_2$.

## It needs a good start

ICP only finds a local minimum. If the initial guess is far off, nearest neighbors are mostly wrong, and ICP converges confidently to the wrong alignment. So it's seeded with odometry, the previous pose, or a global method based on 3-D features.

Two upgrades are standard: **point-to-plane** error (distance to the target's local surface) converges much faster on flat structure, and **outlier rejection** drops matches longer than a threshold.

> **Common mistake:** taking a low final error as proof of a correct alignment. In a long featureless corridor, sliding the scan along the corridor barely changes the error, so ICP can be badly wrong along that direction while reporting a near-perfect fit.
