---
video: xZYjdlFuvXs | Lecture 2.1 Sensors | xLAB for Safe Autonomous Systems | 6:36
---
## Two ways to sort sensors

- **Proprioceptive** sensors measure the robot itself: wheel encoders (how far each wheel turned) and the IMU (accelerometers for acceleration, gyroscopes for turn rate).
- **Exteroceptive** sensors measure the world: lidar, radar, sonar, cameras and GPS.

A second split: **active** sensors (lidar, radar, sonar) send out energy and time the return, so they work in the dark. **Passive** sensors (cameras) just collect light, which gives rich detail but no direct depth, and they struggle with glare and low light.

## Every sensor has a failure mode

- **Encoders** are fast and cheap, but they count wheel turns, not motion: on ice or a slippery floor they report distance the robot never travelled.
- **IMUs** run at hundreds of Hz, but they measure rates. To get heading or position you integrate, and any small bias grows into a large error.
- **GPS** gives absolute position at 1 to 10 Hz, a few metres accurate outdoors, and degrades near tall buildings and fails indoors.
- **Lidar** gives precise ranges to walls and objects, but rain, glass and black surfaces confuse it.
- **Cameras** see texture and colour, but need light and give no depth from a single image.

That's why robots carry several sensors and fuse them: each one covers another's failure mode, which is what the next lessons build.

## Worked example: integrated sensors drift

A gyroscope with a tiny constant bias of $0.01$ rad/s (about half a degree per second) is integrated for heading. After 10 minutes the heading error is

$$0.01 \times 600 = 6\ \text{rad} \approx 344^\circ$$

almost a full turn the wrong way, from a bias you'd never notice in one reading. An encoder with a 1% wheel-radius error does the same to distance: 1 m of error every 100 m.

> **Common mistake:** trusting a proprioceptive sensor over long periods. Anything you integrate drifts. You need an exteroceptive sensor (lidar against walls, GPS, a camera seeing landmarks) to pull the estimate back.
