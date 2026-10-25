---
video: kYB8IZa5AuE | Linear transformations and matrices | 3Blue1Brown | 10:59
video: PFDu9oVAE-g | Eigenvectors and eigenvalues | 3Blue1Brown | 17:16
---
## Why a robotics course starts here

Almost everything in this course is written as vectors and matrices. A robot's state is a vector: a wheeled robot's pose is $x = (p_x, p_y, \theta)$. A model of how it moves, a controller, and a sensor's noise are all matrices acting on those vectors. You don't need the whole subject, just four ideas.

## 1. A matrix is a machine that moves vectors

Multiplying $A x$ takes the columns of $A$ and mixes them using the entries of $x$:

$$\begin{bmatrix} a & b \\ c & d \end{bmatrix} \begin{bmatrix} x_1 \\ x_2 \end{bmatrix} = x_1 \begin{bmatrix} a \\ c \end{bmatrix} + x_2 \begin{bmatrix} b \\ d \end{bmatrix}$$

So the columns of $A$ tell you where the axis directions land. That picture is what the first video above animates.

## 2. Solving $A x = b$

Asking "which $x$ produces $b$?" is solving $A x = b$. If $A$ is square and invertible, $x = A^{-1} b$. If $A$ squashes space flat (its **rank** is less than its size), some $b$ can never be reached, and that idea returns later as **controllability**.

## 3. Eigenvalues tell you what repeated steps do

Many robot models step forward in time as $x_{k+1} = A x_k$, so $x_k = A^k x_0$. An **eigenvector** $v$ is a direction that $A$ only stretches: $A v = \lambda v$. Along it, $k$ steps multiply by $\lambda^k$. If every eigenvalue has $|\lambda| < 1$, every state shrinks to zero; one eigenvalue with $|\lambda| > 1$ and some state blows up. That is the whole idea of **stability** for linear systems.

## 4. When there's no exact answer: least squares

With more equations than unknowns (say 100 noisy sensor readings, 3 unknowns), $A x = b$ usually has no solution. Least squares picks the $x$ that makes the error $\|A x - b\|^2$ smallest, given by the normal equations $A^\top A\, x = A^\top b$. Every estimator in Part III builds on this.

## Worked example

Take $A = \begin{bmatrix} 0.9 & 0.2 \\ 0 & 0.5 \end{bmatrix}$. It is triangular, so its eigenvalues are the diagonal entries: $\lambda_1 = 0.9$ and $\lambda_2 = 0.5$. Both have $|\lambda| < 1$, so $x_{k+1} = A x_k$ decays to zero from any start. The slow one, $0.9$, sets the pace: after 20 steps that part has shrunk to $0.9^{20} \approx 0.12$ of its size, while the $0.5$ part is essentially gone ($0.5^{20} \approx 10^{-6}$).

> **Common mistake:** reading stability off the entries of $A$. A matrix can have small entries and still blow up, or big entries and still decay. Check the eigenvalues.
