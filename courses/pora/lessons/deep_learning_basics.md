---
video: aircAruvnKk | But what is a neural network? | Deep learning chapter 1 | 3Blue1Brown | 18:40
video: Ilg3gGewQ5U | Backpropagation, intuitively | Deep Learning Chapter 3 | 3Blue1Brown | 12:47
---
## A network is a stack of simple layers

A neural network is a function built from layers. Each layer multiplies its input by a weight matrix, adds a bias, and applies a simple nonlinearity $\sigma$:

$$h = \sigma(W x + b)$$

A common choice is the **ReLU**, $\sigma(z) = \max(0, z)$. The nonlinearity is essential: without it, stacked layers multiply out to a single matrix, and the network could only represent linear maps. With it, enough layers can approximate almost any function, such as from pixels to "is there a pedestrian here?"

## The loss says what "good" means

Training needs a single number to minimize, the **loss**, averaged over examples.

- For predicting numbers (regression), **mean squared error**: $L = \tfrac{1}{N} \sum_i (\hat y_i - y_i)^2$.
- For choosing among classes, the network outputs probabilities through a softmax, and **cross-entropy** penalizes a low probability on the correct class: $L = -\log p_{\text{correct}}$. Predicting the right class with $p = 0.9$ costs $0.11$; with $p = 0.1$ it costs $2.3$.

## Backpropagation is the chain rule

To improve the weights you need $\partial L / \partial w$ for every weight, often millions of them. **Backpropagation** gets all of them in one backward sweep. The forward pass computes and stores each layer's output. Then, starting from the loss, the chain rule passes derivatives back layer by layer, each layer reusing the result from the layer after it. The cost is about twice a forward pass, whatever the number of weights. Frameworks such as PyTorch do this automatically.

## Stochastic gradient descent

Training repeats one simple update:

$$\theta \leftarrow \theta - \alpha\, \nabla_\theta L_{\text{batch}}$$

Here the gradient is computed on a small random **minibatch**, say 32 examples, rather than the full dataset. Each step is cheap and noisy, and the noise even helps escape poor regions. The **learning rate** $\alpha$ is the most important setting: too large and training diverges, too small and it crawls. Popular variants such as Adam adapt the step for each weight.

## Worked example: one gradient step

A single weight predicts $\hat y = w x$. Take input $x = 2$, target $y = 3$, current $w = 1$, and loss $L = \tfrac12 (\hat y - y)^2$.

- Forward: $\hat y = 2$, so $L = \tfrac12 (2 - 3)^2 = 0.5$.
- Backward: $\partial L / \partial w = (\hat y - y)\, x = (-1)(2) = -2$.
- Update with $\alpha = 0.1$: $w = 1 - 0.1 \times (-2) = 1.2$.

Now $\hat y = 2.4$ and $L = 0.18$. Repeating drives $w$ toward $1.5$.

> **Common mistake:** judging a model by its training loss. A big network can memorize its training set. Trust the loss on held-out validation data instead.
