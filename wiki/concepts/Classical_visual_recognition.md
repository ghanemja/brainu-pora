---
source: pora
chapter: 8
layer: S
kind: classical
tags: [pora, robot-autonomy, classical]
---
# Classical visual recognition

Recognize objects from hand-designed features and classifiers, the approach learned models later replaced.

<!-- pora:begin -->
## In Principles of Robot Autonomy

- Read: [Chapter 8: Classical Methods for Perception](https://porabook.com/book/classical-perception/)
- Stack layer: Perception · classical
- Watch: [AA174A lecture 11: Classic Visual Recognition](https://youtu.be/GsIRJJ5sYoU)

### Key ideas

1. Classical pipelines hand-design features, such as HOG (histograms of oriented gradients in cells) or bag-of-visual-words built by clustering SIFT descriptors, and feed them to a classifier like an SVM.
2. Detection used sliding windows over positions and scales, scoring each with the classifier (e.g. Dalal-Triggs HOG + linear SVM for pedestrians, Viola-Jones Haar cascades for faces), then non-maximum suppression.
3. These methods are interpretable and data-efficient but the fixed features limit accuracy on varied appearance; learned CNN features largely replaced them after AlexNet (2012).

Try it: Compute HOG features with skimage.feature.hog on a few images and visualize the gradient histograms to see what a linear SVM would actually see.

Needs first: [[Image_filtering_and_convolution]], [[Feature_detection_and_matching]]

Part of [[Principles_of_Robot_Autonomy]]. Summary and study notes from the unofficial PoRA Atlas; the book is the authoritative reference.
<!-- pora:end -->
