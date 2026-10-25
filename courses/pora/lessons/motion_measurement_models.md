---
video: IVTV7vJgIkU | Motion Models | Cyrill Stachniss | 41:12
---
## Two models every filter needs

The Bayes filter asks two questions: where could I be after this motion, $p(x_t \mid u_t, x_{t-1})$, and how likely is this reading from here, $p(z_t \mid x_t, m)$, given the map $m$. This lesson builds both for a robot moving in the plane.

## The motion model: odometry, plus noise

Odometry reports how the robot moved between two poses. A standard way to write any planar move is as three pieces: turn by $\delta_{\text{rot1}}$, drive straight $\delta_{\text{trans}}$, turn by $\delta_{\text{rot2}}$. Each piece gets its own noise, larger for bigger moves. To *sample* from the model, perturb the three pieces and apply them; to get the probability of a pose, ask how far its pieces are from the reported ones.

## The banana

Heading noise is what bends the distribution. Drive 5 m with a heading error of $\pm 0.1$ rad and the end point swings sideways by about $5 \times 0.1 = 0.5$ m, while distance noise only stretches it forwards and backwards. Sample many end points and they form a curved crescent, the "banana", not a round blob. A single Gaussian in $(x, y, \theta)$ can only approximate it.

## The measurement model: range and bearing

A robot at pose $(x, y, \theta)$ sees a landmark $m_j$ at $(m_{j,x}, m_{j,y})$. A range-bearing sensor (lidar picking out a pole, a camera detecting a sign) reports

$$r = \sqrt{(m_{j,x} - x)^2 + (m_{j,y} - y)^2}, \qquad \phi = \operatorname{atan2}(m_{j,y} - y,\ m_{j,x} - x) - \theta$$

plus Gaussian noise $\delta \sim \mathcal{N}(0, R)$. The bearing is measured relative to where the robot faces, which is why $\theta$ is subtracted.

## Worked example

The robot is at $(1, 1)$ facing $\theta = 0$, and a landmark is at $(4, 5)$. The offsets are $3$ and $4$, so

$$r = \sqrt{3^2 + 4^2} = 5\ \text{m}, \qquad \phi = \operatorname{atan2}(4, 3) \approx 0.93\ \text{rad} \approx 53^\circ$$

If the robot turns to face $\theta = 0.5$ rad without moving, the range stays 5 m and the bearing drops to about $0.43$ rad.

> **Common mistake:** adding independent noise to $x$ and $y$. That gives a round blob and misses how heading error turns into sideways error. Put the noise on the turn and the distance, the way the robot actually moves.
