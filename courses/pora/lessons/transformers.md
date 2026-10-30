---
video: eMlx5fFNoYc | Attention in transformers, step-by-step | Deep Learning Chapter 6 | 3Blue1Brown | 26:10
video: j3VNqtJUoz0 | Vision Transformer Quick Guide - Theory and Code in (almost) 15 min | DeepFindr | 16:51
---
## Tokens that look at each other

A transformer treats its input as a set of **tokens**: words, image patches, lidar pillars, or a mix. Each layer lets every token gather information from every other token, weighted by how relevant they are to each other. That's **attention**.

A CNN only lets a pixel see its neighborhood, and it takes many layers to connect distant parts of an image. Attention connects everything in one layer, so the model can relate, say, a pedestrian on one side of the image to a crosswalk on the other.

## The attention formula

Each token's vector is mapped by three learned matrices to a **query** (what am I looking for?), a **key** (what do I contain?) and a **value** (what do I pass on?). Stacking them into matrices $Q$, $K$, $V$:

$$\text{Attention}(Q, K, V) = \operatorname{softmax}\!\left( \frac{Q K^\top}{\sqrt{d_k}} \right) V$$

Row $i$ of the softmax holds token $i$'s weights over all tokens, summing to 1. Dividing by $\sqrt{d_k}$ keeps the scores from growing with the vector size $d_k$. **Multi-head** attention runs several of these in parallel, each free to focus on a different kind of relationship.

## Worked example: one query, two tokens

Let $d_k = 2$, the query be $q = (1, 0)$, the keys $k_1 = (1, 0)$ and $k_2 = (0, 1)$, and the values $v_1 = (10, 0)$ and $v_2 = (0, 10)$.

- Scores: $q \cdot k_1 / \sqrt2 \approx 0.71$ and $q \cdot k_2 / \sqrt2 = 0$.
- Softmax: $e^{0.71} \approx 2.03$ and $e^0 = 1$, giving weights $2.03 / 3.03 \approx 0.67$ and $0.33$.
- Output: $0.67\, v_1 + 0.33\, v_2 = (6.7, 3.3)$.

The query matches token 1 better, so the output leans toward token 1's value.

## Vision transformers

A **ViT** cuts a $224 \times 224$ image into $16 \times 16$ patches: $14 \times 14 = 196$ tokens. Each patch's $16 \cdot 16 \cdot 3 = 768$ pixel values are mapped by a learned linear layer to an embedding, and a learned **positional embedding** is added so the model knows where each patch came from. Then come stacked blocks of attention and small MLPs. For classification, an extra learned token collects the answer.

## The costs

Attention compares every token with every other, so its cost grows as $N^2$. With 196 tokens that's about 38,000 pairs per head per layer; with $8 \times 8$ patches, $784$ tokens give over 600,000, sixteen times more.

Transformers also have weaker built-in assumptions than CNNs, which know that nearby pixels are related. So ViTs need more data or large-scale pretraining to match CNNs, and they pull ahead once they get it.

> **Common mistake:** leaving out positional information. Attention by itself ignores order: shuffle the tokens and each output just shuffles with them. Without positional embeddings, a ViT can't tell the top of the image from the bottom.
