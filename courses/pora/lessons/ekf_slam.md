---
video: nUNSDXTY_oU | Simultaneous Localization and Mapping (SLAM): EKF SLAM | Gustaf Hendeby | 15:38
---
## Put the map in the state

In EKF localization the landmarks were known. In **SLAM** (simultaneous localization and mapping) they aren't, so EKF SLAM simply adds them to the state. With $N$ point landmarks in the plane:

$$\mu = (x,\ y,\ \theta,\ m_{1,x},\ m_{1,y},\ \dots,\ m_{N,x},\ m_{N,y})$$

That's $3 + 2N$ numbers, with a single joint covariance $\Sigma$ of size $(3 + 2N) \times (3 + 2N)$. Its off-diagonal blocks are the key: they record how the error in each landmark is tied to the error in the robot's pose and in every other landmark.

## Predict touches only the robot

Landmarks don't move, so the motion model only changes the pose. The Jacobian $F$ is the identity except for the $3 \times 3$ robot block. The prediction updates the robot's mean, the robot's $3 \times 3$ covariance, and the robot–landmark cross terms, at a cost linear in $N$. The robot's uncertainty grows as usual, and the landmark blocks stay the same.

## Correct moves everything

When the robot observes landmark $j$, the measurement Jacobian $H$ is nonzero only in the robot's columns and landmark $j$'s columns. But the gain $K = \bar\Sigma H^\top S^{-1}$ involves the full covariance, so it's generally nonzero everywhere. One observation of one landmark corrects the robot and every landmark correlated with it.

A landmark seen for the first time is added to the state, with its position computed from the robot's pose and the measurement, and its covariance initialized from both their uncertainties.

## Why correlations make loop closure work

Landmarks seen from nearby poses share the same pose error, so they become strongly correlated. Now the robot drives a long loop, its pose growing uncertain, and re-observes the first landmark it mapped, which is still well known. That one update pins the robot's pose down. Through the correlations it also pulls in every landmark seen along the way, and the whole map's uncertainty shrinks at once.

## Worked example: how the cost grows

- 100 landmarks: the state has $3 + 200 = 203$ entries and $\Sigma$ has $203^2 = 41{,}209$.
- 1000 landmarks: the state has 2003 entries and $\Sigma$ has $2003^2 \approx 4.0$ million, about 32 MB in double precision.

Each update rewrites that whole matrix, so cost grows as $N^2$, and past linearization errors are never fixed. Beyond a few hundred landmarks, graph optimization takes over.

> **Common mistake:** a wrong data association. If an observation of landmark 7 is fused as landmark 12, the EKF can't undo it: the error spreads through the correlations into the whole map and the filter becomes confidently wrong. Gate associations, and when in doubt, skip the measurement.
