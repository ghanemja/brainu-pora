---
source: pora
chapter: 5
layer: S
kind: classical
tags: [pora, robot-autonomy, classical]
---
# Robot sensors

Encoders, IMUs, GPS, lidar, radar, and cameras: what each measures, at what rate, and how it fails.

<!-- pora:begin -->
## In Principles of Robot Autonomy

- Read: [Chapter 5: Introduction to Robot Sensors](https://porabook.com/book/robot-sensors/)
- Stack layer: Perception · classical
- Watch: [AA174A lecture 7: Sensors and Introduction to Computer Vision](https://youtu.be/emb_KF3OSu0)

### Key ideas

1. Proprioceptive sensors measure the robot itself (wheel encoders, IMU accelerometers and gyros); exteroceptive sensors measure the world (lidar, radar, cameras, GPS, sonar).
2. Each sensor trades off rate, range and failure modes: IMUs run at hundreds of Hz but drift when integrated; GPS gives absolute position at ~1-10 Hz but degrades near buildings and indoors; encoders miss wheel slip.
3. Active sensors (lidar, radar, sonar) emit energy and measure returns, so they work in the dark; passive cameras give rich texture but struggle with low light, glare, and lack direct depth.

Try it: Simulate a gyro with constant bias 0.01 rad/s plus noise, integrate it for 10 minutes in NumPy, and plot how the heading error grows.

Unlocks: [[Measurement_noise_models]], [[Sensor_fusion]]

Part of [[Principles_of_Robot_Autonomy]]. Summary and study notes from the unofficial PoRA Atlas; the book is the authoritative reference.
<!-- pora:end -->
