# Extension: Time-Varying Arrivals (Peak Modeling)

## Motivation
Real demand varies by time-of-day. Constant λ underestimates rush-hour queue formation.

## Modeling change
Replace constant λ with λ(t):
- Non-homogeneous Poisson: A_t ~ Poisson(λ(t)·dt)

## Implementation plan
- Add a function `lambda_of_time(t)` in `src/simulation.py` or `src/utils.py`
- Allow config to define piecewise rates (e.g., [ (0,2,90), (2,4,50), ... ])

## Experiments (TODO)
- Compare constant λ vs peak λ(t)
- Plot queue length over time

## Expected outputs
- timeseries.csv
- queue_over_time.png

## Next
- Separate visible queue (till) vs bar backlog