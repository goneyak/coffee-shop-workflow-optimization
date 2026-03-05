# Base Model: Multi-Stage Queue Simulation

## Motivation
We model a high-volume coffee shop workflow as a serial queueing system to identify structural bottlenecks.

## System
Arrival → Till → Shots → Milk → Exit  (each station can have c≥1 servers)

## Stochastic assumptions
- Arrivals per time step: A_t ~ Poisson(λ·dt)
- Service capacity per time step: S_{i,t} ~ Poisson(μ_i·dt)
- Transfer: served = min(queue, capacity)
- Capacity may come from multiple identical servers: total S_{i,t} ~ Poisson(c_i·μ_i·dt)

## Metrics
- L̄ = average customers-in-system (q0+q1+q2 averaged over time)
- Throughput = completed/hour
- W ≈ L̄ / Throughput (Little’s-law proxy)

## Implementation notes
- `src/simulation.py`: core simulation loop
- `src/experiments.py`: scenario runner + summary aggregation
- `src/config.py` or `configs/*.yaml`: parameters

## Known limitations
- constant λ (no peak)
- single-server
- no menu heterogeneity
- no abandonment

## Next
- Calibration and realism improvements