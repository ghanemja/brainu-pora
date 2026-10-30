---
video: IIt1LHIHYc4 | Understanding Sensor Fusion and Tracking, Part 5: How to Track Multiple Objects at Once | MATLAB | 15:28
---
## One filter per object

A detector gives a fresh, unconnected list of boxes every frame. **Tracking** links them over time, so the robot knows that this car is the same one it saw a moment ago, where it's heading and how fast.

Each **track** runs its own Kalman filter, usually with a constant-velocity model and state $(x, y, v_x, v_y)$. Between frames, every track predicts where its object should be next; when detections arrive, the matched ones correct their tracks. The filter's velocity estimate is what lets a planner predict where other agents will be.

## Data association: who is who?

Each frame, match detections to tracks. Build a **cost matrix** with one row per track and one column per detection. The cost is usually the Mahalanobis distance between the detection and the track's predicted position, or $1 - \text{IoU}$ between boxes. First **gate**: forbid pairs whose distance exceeds a threshold. Then solve the **assignment problem**, one detection per track at most and the lowest total cost overall, with the **Hungarian algorithm**.

## Worked example: greedy versus optimal

Two tracks, two detections, with costs:

$$\begin{array}{c|cc} & D_1 & D_2 \\ \hline T_1 & 1.0 & 4.0 \\ T_2 & 2.0 & 6.0 \end{array}$$

**Greedy** matching takes the cheapest pair first, $T_1$–$D_1$ at $1.0$, which leaves $T_2$–$D_2$ at $6.0$: total $7.0$. The Hungarian algorithm checks the alternative, $T_1$–$D_2$ plus $T_2$–$D_1$, which totals $4.0 + 2.0 = 6.0$, and picks it. Grabbing the best-looking pair first can force a bad match elsewhere.

## Birth and death of tracks

Not every detection is a new object, and not every miss means it's gone.

- **Birth**: an unmatched detection starts a tentative track, confirmed only after, say, 3 hits in 5 frames. This filters out one-off false detections.
- **Death**: a track that goes unmatched, perhaps occluded, keeps predicting for a few frames, then is deleted after, say, 5 misses.

Faster confirmation catches objects sooner but creates more false tracks; longer coasting survives occlusions but keeps ghosts alive.

## When association is ambiguous

In crowds, a detection can plausibly belong to several tracks. **JPDA** (joint probabilistic data association) updates each track with a weighted blend of the nearby detections. **MHT** (multiple hypothesis tracking) keeps several association histories alive and decides later. Modern trackers such as DeepSORT add **appearance** embeddings from a neural network, so two people crossing paths keep their identities.

> **Common mistake:** a tight gate with a constant-velocity model. When a car brakes hard or turns, its detection falls outside the gate, the track dies, and a new track with a new ID is born. The planner then sees a brand-new car with no velocity history. Widen the gate when uncertainty is high, or use a turning-aware motion model.
