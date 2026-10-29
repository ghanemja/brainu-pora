---
video: hN8dL55rP5I | Understanding Sensor Fusion and Tracking, Part 3: Fusing a GPS and IMU to Estimate Pose | MATLAB | 14:01
---
## Sensors with complementary errors

No single sensor is good at everything. An **IMU** measures acceleration and rotation rate hundreds of times per second, with little noise, but integrating it to get position piles up error without limit. **GPS** gives an absolute position about once a second, noisy to a few meters, but its error doesn't grow over time.

Fused, you get the best of both: smooth, high-rate estimates from the IMU, with GPS keeping the drift bounded. Wheel odometry with lidar, or a camera with an IMU, pair up for the same reason.

## The IMU predicts, the GPS corrects

The usual design is a Kalman filter (an EKF once orientation is in the state). The IMU drives the **prediction** step at its own rate. In 1-D, with state $(p, v)$ and measured acceleration $a$:

$$p \leftarrow p + v\, \Delta t + \tfrac12 a\, \Delta t^2, \qquad v \leftarrow v + a\, \Delta t$$

and the covariance grows by the process noise each step. Whenever a GPS fix arrives, run a **measurement update** with $H = \begin{bmatrix} 1 & 0 \end{bmatrix}$ and $R = \sigma_{\text{GPS}}^2$. Different rates are handled naturally: predict at every IMU sample, correct whenever a fix shows up.

## Worked example: why the IMU alone isn't enough

An uncorrected accelerometer bias of $b = 0.05$ m/s² gives a position error of $\tfrac12 b\, t^2$:

- after 10 s: $\tfrac12 \times 0.05 \times 100 = 2.5$ m
- after 60 s: $\tfrac12 \times 0.05 \times 3600 = 90$ m.

Now add GPS with $\sigma = 2$ m, so $R = 4$ m². If the predicted position variance just before a fix is $\bar\Sigma = 1$ m², the gain is $K = 1 / (1 + 4) = 0.2$: each fix moves the estimate 20% of the way toward the GPS reading. Fixes keep arriving, so the error stays bounded instead of growing with $t^2$. Adding the bias to the state lets the filter estimate and remove it too.

## Time and frames must line up

Fusion is only as good as its bookkeeping:

- **Timestamps.** A GPS fix that is 100 ms old, applied as if it were current, is 2 m wrong for a car at 20 m/s. Apply it at the time it was measured.
- **Extrinsics.** A GPS antenna 1 m behind the IMU traces a different path whenever the vehicle turns. The **lever arm** between them must be in the model.
- **Frames.** IMU data is in the body frame and GPS in a world frame; mix them up and the filter fights itself.

## Honest noise covariances

The filter weights each sensor by its covariance, so wrong values give wrong weights. Too small an $R$ and the estimate jumps with every noisy fix; too small a $Q$ and the filter stops listening to its sensors. A practical check is the **innovation**: if the gap between the measurement and its prediction is consistently larger than its predicted spread $S$, the filter is overconfident.

> **Common mistake:** taking $R$ from the GPS datasheet's open-sky accuracy. Near buildings, reflections (multipath) produce errors of tens of meters. A filter that trusts those fixes jumps with them. Inflate $R$ in bad conditions, or reject fixes with an innovation gate.
