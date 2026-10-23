---
source: pora
chapter: 10
layer: S
kind: learned
tags: [pora, robot-autonomy, learned]
---
# Object detection & recognition

Locate and label objects with bounding boxes, the input most downstream tracking and planning modules consume.

<!-- pora:begin -->
## In Principles of Robot Autonomy

- Read: [Chapter 10: Object Detection and Recognition](https://porabook.com/book/object-detection/)
- Stack layer: Perception · learned
- Run: [Object Detection](https://colab.research.google.com/github/StanfordASL/pora-exercises/blob/main/ch10/exercises/object_detection.ipynb) ([source](https://github.com/StanfordASL/pora-exercises/blob/main/ch10/exercises/object_detection.ipynb))

### Key ideas

1. A detector outputs bounding boxes, class labels and confidence scores; boxes are compared with intersection over union (IoU), and accuracy is summarized by mean average precision (mAP).
2. Two-stage detectors (Faster R-CNN) propose regions then classify and refine them; one-stage detectors (YOLO, SSD, RetinaNet) predict classes and box offsets densely from anchors or points in one pass.
3. Detectors produce many overlapping boxes per object, so non-maximum suppression keeps the highest-scoring box and removes others whose IoU with it exceeds a threshold.

Try it: Write an iou(box_a, box_b) and a greedy NMS function in NumPy, and test them on 10 random jittered copies of the same box.

Needs first: [[Convolutional_neural_networks]]

Unlocks: [[3D_object_detection]], [[Object_tracking_and_data_association]]

Related: [[Classical_visual_recognition]]

Part of [[Principles_of_Robot_Autonomy]]. Summary and study notes from the unofficial PoRA Atlas; the book is the authoritative reference.
<!-- pora:end -->
