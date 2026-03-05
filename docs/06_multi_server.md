# Extension: Multi-Server Till (Staffing)

## Motivation
Till is a bottleneck; staffing strategy is often the most actionable lever.

## Modeling change
Till becomes M/M/c-like in discrete time:
- total till capacity per step: Poisson(c * μ0 * dt)

## Implementation plan
- Add parameter `c0` (number of till servers)
- In simulation, sample:
  S0_t ~ Poisson(c0 * μ0 * dt)

## Experiments
The following table summarizes results from running three configurations with
c0 = 1, 2, 3 tills (all other service rates held equal to the baseline).

| Till servers | Avg Queue (L̄) | Throughput (orders/hr) | Wait ↔ L/λ (min) | Avg q0 | Avg q1 | Avg q2 |
|--------------|----------------|------------------------|------------------|--------|--------|--------|
| 1            | 14.05          | 57.90                 | 14.6             | 8.71   | 2.03   | 3.31   |
| 2            | 6.64           | 59.32                 | 6.7              | 0.72   | 2.23   | 3.69   |
| 3            | 6.14           | 59.40                 | 6.2              | 0.32   | 2.22   | 3.60   |

These values are the means over 300 simulation runs. Peak queue measurements
also declined (peak q0 from 25.9 to 5.18).

### Key takeaways
- Increasing the number of tills reduces the average queue and wait time
  dramatically, especially when going from one to two servers.
- Further addition (third till) provides diminishing marginal benefit because
  the downstream Shots/Milk stages constrain throughput.
- Throughput itself slightly increases with additional staff as the system
  operates closer to capacity, but it remains bounded by the slowest stage.

## Interpretation goal
Quantify how many servers are needed to keep q0 below a target level during peaks.

## Next
- Menu-dependent service times