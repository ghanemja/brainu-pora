---
video: GDmhrAHxgQE | Core Concepts: Imitation Learning | Sanjiban Choudhury | 16:00
---
## Training states and test states differ

Supervised learning assumes test data looks like training data. Behavior cloning breaks that assumption. Training states come from the **expert's** state distribution: where the expert drove. At run time, the states come from the **learner's** own distribution: where the learner drives. The two match only while the learner is perfect.

This mismatch between the inputs seen in training and in use is called **covariate shift**, and it explains most failures of imitation learning.

## Errors compound

Picture a learned car that drifts 10 cm from the lane center. The expert always drove in the center, so the training data never showed what to do from 10 cm off. The policy guesses, a bit worse than before, and drifts to 30 cm, which is even less familiar. A small error has put it in states where it is more likely to make larger errors.

The expert never made the first mistake, so it never demonstrated the recovery.

## Worked example: how bad it can get

Suppose the cloned policy errs with probability $\varepsilon$ on states like the expert's, and an episode lasts $T$ steps.

- Trained on its **own** state distribution, its expected cost grows like $\varepsilon T$.
- Trained only on the **expert's** states, a mistake can derail every remaining step, so the worst case grows like $\varepsilon T^2$.

With $\varepsilon = 1\%$ and $T = 100$: $\varepsilon T = 1$, but $\varepsilon T^2 = 100$. Doubling the episode length quadruples the worst case. Longer tasks suffer the most.

## DAgger: ask the expert where the learner went

**DAgger** (dataset aggregation) collects data from the learner's own distribution:

- Train a policy on the expert demonstrations.
- Run the policy, and record the states it actually visits.
- Ask the expert what they would have done in each of those states.
- Add these labeled states to the dataset, retrain, and repeat.

After a few rounds, the training data covers the states the learner really reaches, including the recoveries. The cost is that the expert must be available to label states.

## Other ways to broaden coverage

- **Noise injection** during demonstrations (DART): perturb the expert's actions slightly while recording, so the data shows the expert recovering from small deviations.
- **Recovery demonstrations**: deliberately start from bad states and record the fix.
- **Synthetic views**: NVIDIA's early self-driving system used left and right cameras, labeled with corrective steering, to simulate the car being off-center.

> **Common mistake:** declaring success from validation loss on held-out demonstrations. Those are still expert states, so a low loss says nothing about the states the policy will reach. Evaluate by running the policy closed-loop, in simulation or on the robot.
