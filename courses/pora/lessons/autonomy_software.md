---
video: 7TVWlADXwRw | What Is ROS2? - Framework Overview | Raymond Andrade | 8:22
video: Fw8JQ5Q-ZwU | What Is Autonomous Navigation? | Autonomous Navigation, Part 1 | MATLAB | 11:30
---
## The stack: four jobs in a loop

An autonomous robot repeats the same loop many times per second, and the software is split along it:

- **Perception** turns raw sensor data (images, lidar scans) into useful facts: features, obstacles, detected objects.
- **Estimation** tracks the robot's own state, such as its pose and velocity, and often builds a map.
- **Planning** decides where to go and computes a path or trajectory.
- **Control** turns that trajectory into motor commands, correcting for errors as they happen.

The rest of the book covers these four jobs. This lesson is about how they fit together as running software.

## Modules talk through messages

Each job runs as a separate module, often a separate process, and modules communicate by passing **messages** with well-defined types. In **ROS**, the most common robot framework, a module **publishes** messages on a named **topic**, such as `/scan` or `/cmd_vel`, and any module can **subscribe** to it. Neither side needs to know the other exists.

That loose coupling is the point. You can swap a new planner in without touching perception, replay recorded sensor data to test a module offline, or run the same code in simulation and on the robot.

## Every module runs at its own rate

Modules don't run in lockstep:

- Motor control: 100 to 1000 Hz
- State estimation: 10 to 200 Hz, matched to the IMU and wheel encoders
- Perception: 10 to 30 Hz, limited by cameras and neural networks
- Global planning: about 1 Hz, or only when the goal or map changes

So a module almost never has perfectly fresh inputs. Every message carries a **timestamp**, and each module must cope with data that is late, out of date, or missing.

## Worked example: a latency budget

A car's camera runs at 30 Hz, so a frame can be up to 33 ms old before processing starts. Detection then takes 50 ms, tracking 5 ms, and planning 100 ms. From the moment light hits the sensor to a plan reflecting it:

$$33 + 50 + 5 + 100 = 188 \text{ ms}$$

At 15 m/s (54 km/h), the car moves $15 \times 0.188 \approx 2.8$ m in that time. The planner must reason about where things will be, not where they were seen, and every millisecond saved buys stopping distance.

## Tools you'll use

The book's exercises use **Python** with NumPy for the math, plotting libraries to look at the results, and simulation to test safely. Real systems add logging (recording every message, as ROS bags do) so a failure can be replayed and debugged offline, and unit tests for each module. Being able to replay the exact inputs that caused a failure is one of the biggest practical benefits of a modular stack.

> **Common mistake:** using whatever message arrived last, ignoring its timestamp. A 200 ms old pose combined with a fresh scan places obstacles in the wrong spot. Look up data at the time the measurement was taken, not the time it arrived.
