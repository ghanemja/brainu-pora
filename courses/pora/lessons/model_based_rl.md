---
video: ztT2ZLWTfXw | Why Choose Model-Based Reinforcement Learning? | MATLAB | 15:01
---
## Learn the dynamics, then plan

Model-free RL learns what to do directly from trial and error. **Model-based RL** first learns how the world responds, a dynamics model

$$x_{t+1} \approx f_\theta(x_t, u_t)$$

fitted to logged transitions, and then plans or controls with that model using tools from earlier chapters: MPC, iLQR, or simulated rollouts to train a policy. It closes the loop between learning and classical control: the controller is classical, the model is learned.

## System identification

For a linear model $x_{t+1} = A x_t + B u_t$, fitting is ordinary least squares, called **system identification**. Stack the parameters as $\Theta = [A \;\; B]$ and minimize

$$\sum_t \big\| x_{t+1} - \Theta \begin{bmatrix} x_t \\ u_t \end{bmatrix} \big\|^2$$

which has a closed-form solution. For nonlinear systems, $f_\theta$ might be a physics model with unknown parameters (mass, friction) or a neural network. The data must **excite** the system: if the robot never turned sharply in the logs, the model knows nothing about sharp turns.

## Worked example: fitting a scalar model

Fit $x_{t+1} = a\, x_t + b\, u_t$ to three logged transitions:

- $x = 1$, $u = 0$ gave $x' = 0.9$
- $x = 1$, $u = 1$ gave $x' = 1.4$
- $x = 2$, $u = 0$ gave $x' = 1.8$.

The first gives $a = 0.9$, and the third agrees: $0.9 \times 2 = 1.8$. The second then gives $0.9 + b = 1.4$, so $b = 0.5$. Least squares returns exactly $a = 0.9$, $b = 0.5$, since the data has no noise. With the model in hand, LQR or MPC can design a controller without another trial.

## Why it's sample-efficient

Every transition teaches the model something reusable, whatever task you later plan for. Model-free methods, by contrast, squeeze only a weak learning signal from each reward. So model-based methods often need an order of magnitude or more fewer real trials, which is what matters on hardware. The cost is computation: planning with the model at every step, or training a policy inside it.

## The planner exploits model errors

A planner hunts for whatever the model says is best, including places where the model is simply wrong: "push here and the robot flies forward". These errors are invisible to the planner but break the plan on the real robot. Standard defenses:

- **Ensembles** of models, treating disagreement as uncertainty and avoiding it.
- Short planning horizons with frequent **replanning** from real measurements (MPC).
- Collecting new data where the planner actually goes, and refitting.

> **Common mistake:** fitting a model on data from a narrow range and then planning far outside it. A model trained on slow driving says nothing reliable about fast driving, however low its training error.
