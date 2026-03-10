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

## Experiments (TODO)
- c0 = 1, 2, 3
- Compare L̄, W proxy, visible queue

## Interpretation goal
Quantify how many servers are needed to keep q0 below a target level during peaks.

## Next
- Menu-dependent service times