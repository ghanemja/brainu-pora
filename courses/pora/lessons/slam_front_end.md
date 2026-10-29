---
video: A_-nHCK9oBs | ICRA 2024 - Visual Place Recognition: A Tutorial | Dr Stefan Schubert | 7:00
---
## Front end and back end

A SLAM system has two halves. The **front end** looks at raw sensor data and produces abstract constraints: "pose 41 is 0.52 m ahead of pose 40", "this feature is landmark 17", "this place is the same as pose 3". The **back end** (a filter or a pose graph optimizer) takes those constraints and computes the most likely poses and map.

The back end's math assumes the constraints are right. Most real SLAM failures come from the front end feeding it a wrong one.

## Turning sensor data into constraints

- **Cameras**: detect and describe features (ORB is common, since it's fast), match them across frames, and estimate relative motion from the matches with RANSAC.
- **Lidar**: register each scan to the previous one or to a local map with ICP; the resulting transform becomes an odometry constraint.

Every constraint needs a covariance (or information matrix) that says how much to trust it. A scan match in a long featureless corridor is solid across it but weak along it, and its covariance should say so.

## Data association with a gate

Before using an observation, decide which landmark it came from. Compare the measurement with each landmark's prediction using the **Mahalanobis distance** of the innovation $\nu$ with covariance $S$:

$$d^2 = \nu^\top S^{-1} \nu$$

Accept only if $d^2$ is below a chi-squared threshold, $5.99$ for a 2-D measurement at 95%. With $S = \operatorname{diag}(0.04, 0.0025)$ (range in m², bearing in rad²), an innovation $\nu = (0.3, 0.05)$ gives $d^2 = 2.25 + 1 = 3.25$: accept. An innovation $\nu = (0.6, 0)$ gives $d^2 = 9$: reject.

## Worked example: how many RANSAC tries?

RANSAC repeatedly fits a model to a random minimal set of $s$ matches and keeps the model with the most inliers. To get at least one all-inlier set with probability $p$, when a fraction $w$ of matches are inliers, it needs

$$N = \frac{\log(1 - p)}{\log(1 - w^s)}$$

With $p = 0.99$ and $w = 0.5$: the 8-point algorithm ($s = 8$) needs about 1177 tries, and the 5-point algorithm ($s = 5$) about 145. Smaller minimal sets make RANSAC much cheaper.

## Recognizing places: loop closure

To correct drift, the front end must notice when the robot returns to a place it has mapped. **Place recognition** compares the current view with past keyframes, using a bag-of-visual-words index or a learned global image descriptor, to propose candidates. Each candidate is then **verified geometrically**: match features, estimate the relative pose with RANSAC, and require enough inliers. Only then does it become a loop-closure constraint.

> **Common mistake:** trusting a loop closure because two images look alike. Office corridors, parking garages and warehouse aisles repeat. A single false loop closure can fold the map onto itself. Verify geometry, require consistency with neighboring frames, and use robust costs in the back end.
