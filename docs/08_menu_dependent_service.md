# Extension: Menu-Dependent Service Times

## Motivation
Milk station time varies greatly by drink type (oat/matcha/hot chocolate/iced).

## Modeling change
Use mixture service capacity:
- With probabilities p_k, draw capacity from different effective μ values
or
- Model each order carries a "type" that affects downstream μ

## Implementation plan (two options)
Option A (fast):
- adjust μ2 per step based on sampled mix

Option B (more realistic):
- tag arrivals with type; process with type-dependent service times

## Experiments (TODO)
- Compare baseline vs mixed menu
- Observe bottleneck shifts

## Next
- Healthcare mapping