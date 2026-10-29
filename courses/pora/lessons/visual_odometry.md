---

---
## Odometry from images

Wheel odometry counts wheel turns; **visual odometry** (VO) estimates the camera's motion from how the image changes. For each new frame it estimates the relative motion $T_{k-1,k}$ since the last frame and chains it onto the running pose:

$$T_k = T_{k-1}\, T_{k-1,k}$$

VO works where wheels slip or don't exist, such as drones, legged robots or handheld devices. It runs in real time and only looks at recent frames: it's the incremental, online version of structure from motion.

## Two ways to measure each step

- **Feature-based** VO detects and matches keypoints between frames, then solves for motion: the essential matrix for two monocular views, or PnP when 3-D points are already known (from stereo, depth, or earlier triangulation), always inside RANSAC.
- **Direct** VO skips features and adjusts the motion until the pixel intensities of one frame, warped into the next, line up best. It uses all image gradients, so it works in low-texture scenes, but it needs good photometric calibration.

Most systems also run a small bundle adjustment over a window of recent **keyframes** to smooth the estimates.

## Drift is unavoidable

Every step's estimate has a small error, and chaining steps composes the errors. Heading errors are the worst: a small rotation error makes every later step point slightly the wrong way, so position error grows faster than distance.

Monocular VO also drifts in **scale**, because each step's translation length is inferred, not measured. That's why VO is so often fused with an IMU (**visual-inertial odometry**), whose accelerometer fixes scale and gravity direction.

## Worked example: a tiny bias, a big error

A robot drives 100 m straight in 1 m steps. Each step, VO underestimates the turn by just $0.1°$, so after step $k$ the heading is off by $0.1° \times k$.

After 100 steps the heading is off by $10°$, and the sideways error is the sum of each step's sideways component:

$$\sum_{k=1}^{100} \sin(0.1° \cdot k) \approx 8.8 \text{ m}$$

A bias too small to notice in any single frame puts the robot almost 9 m off course: about 9% of the distance traveled.

## Loop closure resets the drift

If the robot comes back to a place it has seen, recognizing it gives a constraint between the current pose and the old one. **Place recognition** often uses a bag-of-visual-words image search, followed by geometric verification. The loop constraint goes into a **pose graph**, and optimizing the graph spreads the accumulated error across the whole loop, pulling the trajectory back into shape. That step turns VO into visual SLAM.

> **Common mistake:** treating VO drift as noise that averages out. It doesn't: errors accumulate like a random walk, and biases grow even faster. Report drift as a percentage of distance traveled, and test on runs as long as the real task.
