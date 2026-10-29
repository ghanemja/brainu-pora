---
video: svn9-xV7wjk | How YOLO Object Detection Works | DeepBean | 17:04
video: VAo84c1hQX8 | C4W3L07 Nonmax Suppression | DeepLearningAI | 8:02
---
## What a detector outputs

A classifier says *what* is in an image. A **detector** says what and *where*: a list of bounding boxes, each with a class label and a confidence score. For example, "pedestrian, 0.93, box from $(120, 80)$ to $(180, 240)$".

That list is what the rest of the stack consumes. Trackers follow the boxes over time, and planners treat them as obstacles to avoid. So a missed pedestrian or a phantom car flows straight into the robot's decisions.

## Comparing boxes with IoU

To check a predicted box against the truth, or two predictions against each other, use **intersection over union**:

$$\text{IoU} = \frac{\text{area of overlap}}{\text{area of union}}$$

Two $4 \times 4$ boxes, one from $(0, 0)$ to $(4, 4)$ and one from $(2, 2)$ to $(6, 6)$, overlap in a $2 \times 2$ square. The union is $16 + 16 - 4 = 28$, so $\text{IoU} = 4 / 28 \approx 0.14$. A prediction usually counts as correct if its IoU with a true box of the same class is at least $0.5$.

## Two-stage and one-stage detectors

- **Two-stage** detectors such as Faster R-CNN first propose regions likely to contain objects, then classify each region and refine its box. They're accurate, but slower.
- **One-stage** detectors such as YOLO, SSD and RetinaNet predict class scores and box offsets densely, for every cell of a feature map, in one pass. They're fast enough for real-time robots.

Many predict boxes relative to preset **anchor** boxes of typical shapes; newer **anchor-free** designs predict object centers and sizes directly.

## Non-maximum suppression

A dense detector fires many overlapping boxes for each object. **Non-maximum suppression** (NMS) cleans them up:

- Sort the boxes by score and keep the best one.
- Delete every remaining box whose IoU with it is above a threshold, say $0.5$.
- Repeat with the next-best remaining box.

Three boxes on one car, scored $0.9$, $0.8$ and $0.6$, with IoUs of $0.7$ and $0.6$ to the best, collapse to the $0.9$ box.

## Measuring accuracy: mAP

As you lower the score threshold, the detector finds more true objects (higher **recall**) but also makes more false detections (lower **precision**). **Average precision** (AP) is the area under the precision–recall curve for one class; **mAP** averages it over classes. Benchmarks also state the IoU threshold, such as mAP@0.5, or an average over thresholds from 0.5 to 0.95.

> **Common mistake:** an NMS threshold that is too low for crowds. Two pedestrians walking side by side can have boxes with IoU above $0.5$, and NMS deletes one of them. In crowded scenes, raise the threshold or use a detector that handles overlap.
