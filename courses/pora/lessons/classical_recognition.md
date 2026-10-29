---
video: 0Zib1YEE4LU | Histograms of Oriented Gradients (HOG) | UCF CRCV | 16:23
video: a4cFONdc6nc | Bag of Visual Words - 5 Minutes with Cyrill | Cyrill Stachniss | 5:21
---
## Hand-designed features plus a classifier

Before deep learning, recognition was a two-part pipeline. First, a person designs a **feature**: a fixed recipe that turns an image patch into a vector capturing shape or texture while ignoring lighting and small shifts. Then a **classifier**, often a support vector machine (SVM), learns from labeled examples which vectors belong to which class.

All the learning happens in the classifier. The features themselves never improve with more data, which turned out to be the limiting factor.

## HOG: histograms of oriented gradients

**HOG** describes shape by the directions of edges. Compute image gradients, split the window into $8 \times 8$-pixel **cells**, and in each cell build a 9-bin histogram of gradient directions, weighted by gradient strength. Then normalize groups of $2 \times 2$ cells (**blocks**) so lighting changes cancel out.

Dalal and Triggs' pedestrian detector uses a $64 \times 128$ window: $8 \times 16$ cells give $7 \times 15 = 105$ overlapping blocks, each with $4 \times 9 = 36$ numbers, for a $3780$-number descriptor fed to a linear SVM.

## Bag of visual words

For recognizing a whole image, such as "kitchen" versus "office", or for place recognition in SLAM, the **bag of visual words** borrows from text search:

- Collect many SIFT descriptors from training images and cluster them with k-means; each cluster center is a **visual word**.
- Describe an image by a histogram of how often each word appears in it, ignoring where.
- Classify or compare those histograms.

It's crude (it throws away layout) but fast, and image-retrieval versions are still used for loop closure.

## Worked example: why sliding windows are expensive

To find pedestrians anywhere in a $640 \times 480$ image, scan the $64 \times 128$ window across it with a stride of 8 pixels:

$$\frac{640 - 64}{8} + 1 = 73 \text{ positions across}, \qquad \frac{480 - 128}{8} + 1 = 45 \text{ down}$$

That's $73 \times 45 = 3285$ windows at one scale, each needing a 3780-number descriptor and a classifier score. Repeat on an image pyramid to catch people at other sizes, then use **non-maximum suppression** to merge the many overlapping hits. **Viola–Jones** face detection made this fast with a cascade that rejects most windows after a few cheap tests.

## Why learned features won

Fixed features work well when appearance is consistent, like upright pedestrians or frontal faces, and they need little data and are easy to inspect. But they can't adapt to the wide variety of appearance in the real world. In 2012 a CNN (AlexNet) learned its own features from data and beat the best hand-designed pipelines on ImageNet by a wide margin, and the field switched.

> **Common mistake:** expecting a hand-built detector to generalize past its training conditions. A HOG detector trained on upright, side-on pedestrians misses people who are sitting, cycling, or seen from above.
