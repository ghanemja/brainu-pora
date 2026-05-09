# Observability

**Observability** is the property of a system where internal state can be reconstructed from output measurements alone.

## Test

System (A, C) is observable iff observability matrix has full rank:

O = [C; CA; CA²; ...; CA^(n-1)]

## Use

Required for [[Kalman_filter]] convergence. Dual concept to controllability.

## Related

- [[State_space_model]]
- [[Kalman_filter]]
- [[Transfer_function]]
- [[Lyapunov_stability]]
